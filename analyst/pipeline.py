"""Orchestrator — runs every agent in order, on point-in-time data only.

Input contract (all user-supplied, all stamped with as_of):
  prices: list[float], as_of: str, company_type: str,
  fundamentals: dict, previous_fundamentals: dict, news_text: str,
  market_prices: list[float] (optional, for beta), price: float (latest price),
  valuation_inputs: dict (dcf/ev_ebitda/pe/pb/revenue values, each optional)
Output: dict with every agent's output, the debate, the audit log, and
the falsifier — what would change the verdict. No buy/sell recommendation.
"""
from . import audit, debate, fundamental, risk, sentiment, technical, valuation

def run(inp):
    log = audit.AuditLog()
    log.add("input_received", {"as_of": inp.get("as_of"), "company_type": inp.get("company_type"), "n_prices": len(inp.get("prices", []))})
    prices = inp["prices"]
    tech = {"sma20": technical.sma(prices, 20) if len(prices) >= 20 else None,
            "rsi14": technical.rsi(prices, 14) if len(prices) >= 15 else None,
            "macd": technical.macd(prices) if len(prices) >= 26 else None,
            "bollinger": technical.bollinger(prices) if len(prices) >= 20 else None}
    log.add("technical", tech)
    fund = fundamental.ratios(inp.get("fundamentals", {}))
    piot = fundamental.piotroski(inp.get("fundamentals", {}), inp.get("previous_fundamentals", {}))
    log.add("fundamental", {"ratios": fund, "piotroski": piot["score"]})
    rets = risk.returns_from_prices(prices)
    risk_out = {"var_5pct": risk.historical_var(rets), "cvar_5pct": risk.historical_cvar(rets),
                "max_drawdown": risk.max_drawdown(prices),
                "beta": risk.beta(rets, risk.returns_from_prices(inp["market_prices"])) if inp.get("market_prices") else None}
    log.add("risk", risk_out)
    blended = valuation.blended_value(inp["company_type"], inp.get("valuation_inputs", {}))
    price = inp.get("price")
    gap = (blended - price) / price if blended is not None and price else None
    log.add("valuation", {"blended": blended, "gap_vs_price": gap, "weights": valuation.WEIGHTS[inp["company_type"]]})
    sent = sentiment.sentiment_score(inp.get("news_text", ""))
    log.add("sentiment", sent)
    deb = debate.debate({"rsi": tech["rsi14"], "piotroski_score": piot["score"],
                         "var_5pct": risk_out["var_5pct"], "max_drawdown": risk_out["max_drawdown"], "valuation_gap": gap})
    log.add("debate", deb)
    assert log.verify(), "audit chain broken — this should never happen"
    return {"as_of": inp.get("as_of"), "company_type": inp["company_type"], "technical": tech,
            "fundamental_ratios": fund, "piotroski": piot, "risk": risk_out,
            "valuation": {"blended_value": blended, "gap_vs_price": gap},
            "sentiment": sent, "debate": deb, "audit_valid": True,
            "audit_entries": len(log.entries),
            "falsifier": "This verdict flips if: Piotroski drops below 4, RSI crosses 70/30, VaR exceeds 10%, or a new filing changes the valuation inputs.",
            "disclaimer": "Research only. Not investment advice. No trade is made by this system."}

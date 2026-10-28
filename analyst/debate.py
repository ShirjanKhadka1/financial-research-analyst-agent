"""Bull vs Bear debate + Risk Veto — the TradingAgents debate, made deterministic.
No LLM: each side is scored from the computed numbers, so the debate cannot
invent a fact. The Risk Manager can veto or scale down, never be overridden
by a good story."""
def debate(metrics):
    """metrics: dict with rsi, piotroski_score, var_5pct, max_drawdown, valuation_gap
    (blended value vs price, as a fraction; positive = value above price)."""
    bull=[]; bear=[]
    if metrics.get("piotroski_score") is not None and metrics["piotroski_score"]>=7: bull.append(f"Piotroski {metrics['piotroski_score']}/9 — strong fundamentals")
    if metrics.get("piotroski_score") is not None and metrics["piotroski_score"]<=3: bear.append(f"Piotroski {metrics['piotroski_score']}/9 — weak fundamentals")
    if metrics.get("rsi") is not None and metrics["rsi"]>70: bear.append(f"RSI {metrics['rsi']:.1f} — overbought")
    if metrics.get("rsi") is not None and metrics["rsi"]<30: bull.append(f"RSI {metrics['rsi']:.1f} — oversold")
    if metrics.get("valuation_gap") is not None and metrics["valuation_gap"]>0.2: bull.append(f"Blended value {metrics['valuation_gap']:.0%} above price")
    if metrics.get("valuation_gap") is not None and metrics["valuation_gap"]<-0.2: bear.append(f"Blended value {metrics['valuation_gap']:.0%} below price")
    veto=False; veto_reason=None
    if metrics.get("var_5pct") is not None and metrics["var_5pct"]>0.10: veto=True; veto_reason="5% VaR above 10% — risk not priced, position scaled to zero by Risk Manager"
    if metrics.get("max_drawdown") is not None and metrics["max_drawdown"]<-0.40: veto=True; veto_reason="Max drawdown below -40% — Risk Manager veto"
    verdict="No clear edge — hold for more evidence" if not bull and not bear else ("Bull case stronger" if len(bull)>len(bear) else "Bear case stronger" if len(bear)>len(bull) else "Balanced — bull and bear equal")
    if veto: verdict="RISK VETO — no position, regardless of debate outcome"
    return {"bull": bull, "bear": bear, "veto": veto, "veto_reason": veto_reason, "verdict": verdict}

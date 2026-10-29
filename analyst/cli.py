"""CLI: python -m analyst.cli demo  -> runs the full pipeline on demo data, prints the report.
No network, no key, no install beyond Python 3.10+."""
import argparse
import sys

from .pipeline import run
from .report import render

DEMO = {"as_of": "2026-10-28", "company_type": "stable", "price": 100.0,
        "prices": [100 + i*0.5 + (i % 5) for i in range(60)],
        "market_prices": [(100 + i*0.5 + (i % 5))*10 + (i % 3) for i in range(60)],
        "fundamentals": {"revenue": 1000, "net_income": 120, "equity": 800, "assets": 1500, "debt": 300, "current_assets": 400, "current_liabilities": 200, "operating_cash_flow": 150, "roa": 0.08, "leverage": 0.375, "current_ratio": 2.0, "shares_outstanding": 100, "gross_margin": 0.4, "asset_turnover": 0.67},
        "previous_fundamentals": {"roa": 0.06, "leverage": 0.45, "current_ratio": 1.8, "shares_outstanding": 100, "gross_margin": 0.38, "asset_turnover": 0.60},
        "news_text": "Strong growth and record profit beat expectations, expansion continues",
        "valuation_inputs": {"dcf": 110, "ev_ebitda": 105, "pe": 95}}
# Second worked example, same pipeline/audit/veto machinery, different inputs.
# DEMO data only — NOT a real company, NOT real financials. Deliberately
# contrasting with DEMO: company_type "cyclical" (EV/EBITDA-led weights),
# weak Piotroski inputs, a negative valuation gap, and a price series that
# repeatedly drops 12% (100 -> 88 -> 100 ...) so 5% VaR is 12% and the Risk
# Manager vetoes, where the smooth DEMO series (VaR ~3.2%) does not.
# Max drawdown here is only -12%, so the veto is driven by VaR alone.
DEMO_CYCLICAL = {"as_of": "2026-10-28", "company_type": "cyclical", "price": 100.0,
        "prices": [100.0 if i % 2 == 0 else 88.0 for i in range(60)],
        "market_prices": [1000.0 if i % 2 == 0 else 880.0 for i in range(60)],
        "fundamentals": {"revenue": 1000, "net_income": -50, "equity": 800, "assets": 1500, "debt": 600, "current_assets": 300, "current_liabilities": 300, "operating_cash_flow": -20, "roa": -0.0333, "leverage": 0.75, "current_ratio": 1.0, "shares_outstanding": 110, "gross_margin": 0.30, "asset_turnover": 0.67},
        "previous_fundamentals": {"roa": 0.02, "leverage": 0.60, "current_ratio": 1.2, "shares_outstanding": 100, "gross_margin": 0.35, "asset_turnover": 0.70},
        "news_text": "Loss widens as demand falls, downgrade follows weak quarter",
        "valuation_inputs": {"dcf": 70, "ev_ebitda": 80, "pe": 60}}
def main(argv=None):
    p = argparse.ArgumentParser(prog="financial-research-analyst-agent")
    p.add_argument("cmd", choices=["demo", "demo2"])
    args = p.parse_args(argv)
    if args.cmd == "demo":
        print(render(run(DEMO), "Demo Company — Research Report (demo data, not a real company)"))
    elif args.cmd == "demo2":
        print(render(run(DEMO_CYCLICAL), "Demo Cyclical Company — Research Report (demo data, not a real company)"))
    return 0
if __name__ == "__main__": sys.exit(main())

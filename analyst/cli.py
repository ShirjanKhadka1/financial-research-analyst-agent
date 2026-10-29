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
def main(argv=None):
    p = argparse.ArgumentParser(prog="financial-research-analyst-agent")
    p.add_argument("cmd", choices=["demo"])
    args = p.parse_args(argv)
    if args.cmd == "demo":
        print(render(run(DEMO), "Demo Company — Research Report (demo data, not a real company)"))
    return 0
if __name__ == "__main__": sys.exit(main())

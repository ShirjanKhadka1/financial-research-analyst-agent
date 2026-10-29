"""Run the second worked example through the SAME pipeline as demo_run.py
and save the report. Usage: python examples/second_run.py

DEMO data only — not a real company, not real financials. See
analyst/cli.py (DEMO_CYCLICAL) for how its inputs differ from DEMO and
why its Risk Veto outcome differs. Research only, no recommendation.
"""
import sys

sys.path.insert(0, ".")

from analyst.cli import DEMO_CYCLICAL
from analyst.pipeline import run
from analyst.report import render

if __name__ == "__main__":
    report = render(run(DEMO_CYCLICAL), "Demo Cyclical Company — Research Report (demo data, not a real company)")
    with open("examples/second_report.md", "w") as f:
        f.write(report)
    print(report)

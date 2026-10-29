"""Run the demo pipeline and save the report. Usage: python examples/demo_run.py"""
import sys

sys.path.insert(0, ".")

from analyst.cli import DEMO
from analyst.pipeline import run
from analyst.report import render

if __name__ == "__main__":
    report = render(run(DEMO), "Demo Company — Research Report (demo data, not a real company)")
    with open("examples/demo_report.md", "w") as f:
        f.write(report)
    print(report)

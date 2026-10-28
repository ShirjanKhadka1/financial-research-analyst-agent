"""financial-research-analyst-agent: deterministic, zero-dependency research pipeline.

No LLM, no API key, no trade. Every number is computed here, in this
package, from data the user supplies (CSV, Yahoo, World Bank) — so the
report is auditable, reproducible, and costs $0.
"""
from . import audit, debate, fundamental, pipeline, report, risk, sentiment, technical, valuation
__all__ = ["audit", "debate", "fundamental", "pipeline", "report", "risk", "sentiment", "technical", "valuation"]

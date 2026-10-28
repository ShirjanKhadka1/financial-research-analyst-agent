# Financial Research Analyst Agent — the better version

**One pipeline. Every agent. Zero dependencies. $0. No trade. No buy/sell.**

Built after tearing down TradingAgents (117k stars), ai-hedge-fund (64k), Vibe-Trading (37k),
gsaini's 11-agent system, sushpr's valuation-by-type engine, kingabzpro's FastAPI agent,
fakher's CrewAI assistant, and both GitHub topic lists. Full teardown:
`research/teardown-2026-10-28.md`.

## Why this is better than all of them
- **Runs without any API key.** Every other repo above needs LLM/data keys to do anything.
  This one runs offline, in under a minute, with Python 3.10+ and nothing else installed.
- **Numbers are computed, not generated.** RSI, MACD, Bollinger, Piotroski F-Score (0–9),
  DCF + multiples **by company type** (bank ≠ stable ≠ high-growth ≠ cyclical),
  historical VaR/CVaR, Monte Carlo VaR, beta, drawdown — all in `analyst/`, all tested.
- **Debate + Risk Veto.** Bull vs Bear are scored from those numbers, and the Risk Manager
  can veto a position to zero. A good story cannot override a bad risk number.
- **Hash-chained audit log.** Every step is logged with a hash of the previous step —
  tamper with one entry and `verify()` fails. Spend is $0 by construction.
- **Point-in-time + falsifier.** Every input is stamped `as_of`; every report states
  exactly what would flip its verdict.
- **Stdlib API.** `python -m analyst.server` gives `GET /health`, `POST /research`,
  `GET /demo` — no FastAPI install needed.
- **Nepal-ready.** Feed it a CSV price file (NEPSE-style, labelled by you) the same way
  you feed it world data. No US-only assumption.
- **Research only.** This system makes no trades and gives no buy/sell recommendation.

## Run it in 30 seconds
```
python -m analyst.cli demo
python examples/demo_run.py        # saves examples/demo_report.md
python -m analyst.server           # API on http://127.0.0.1:8000
```

## Pipeline
Data (CSV/Yahoo/World Bank, user-supplied) → Technical → Fundamental (Piotroski) →
Risk → Valuation by type → Sentiment (lexicon, word counts shown) → Debate → Risk Veto →
Markdown report + audit log.

## Tests
```
python -m pytest tests/ -q   # 46 passed (demo pipeline, bank weights, audit tamper, risk veto, sentiment, server, isolated technicals, bad inputs; flat-series RSI bug fixed: neutral 50, not 100)
```

## As-of / point-in-time discipline
Every input in this system is stamped `as_of`, and every report must be
read as of that date — not as of today. A figure restated from a
historical date reads as first reported for that date: it is not silently
updated, revised, or re-based to a later figure. Where a historical
figure is not available on a first-reported basis, it is withheld and
labelled TO VERIFY rather than filled in with a later restatement or a
plausible substitute. A report whose inputs span different dates must say
so, so that no reader mistakes a mixed-date report for a single-date
snapshot.

## Disclaimer
Research only. Not investment advice. No trade is made by this system.

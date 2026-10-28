# Good First Issues

Small, well-scoped tasks a new contributor can pick up. This is a list, not
a promise: no maintainer response time is promised, and no GitHub issue has
been created for these items. Open an issue first and ask to be assigned
before starting, so two people do not do the same task.

## 1. Clarify the simulated-VaR docstring in `analyst/risk.py`

`monte_carlo_var` is the simulated (Monte Carlo) VaR function, but its
docstring does not yet state in plain words what it simulates: the
distribution it draws from, the horizon and number of paths, the seed and
reproducibility, and that the result is a simulation under stated
assumptions — not a prediction of future loss. Rewrite only the docstring
(no behaviour change, no signature change) so a reader can tell, without
reading the code, exactly what the number means and what would change it.

Acceptance: docstring only; all existing tests still pass
(`python -m pytest tests/ -q`); no new claim about accuracy is introduced.

## House rules

Research only, not investment advice; never a buy/sell recommendation.
No credentials, no private data, no paywalled scraping.

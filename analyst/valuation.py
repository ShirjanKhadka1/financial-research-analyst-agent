"""Valuation by company type — the one idea every other repo gets wrong when
it applies a single model to every company (sushpr's insight, made deterministic).

Types: 'bank' (P/B + P/E, never DCF on equity the same way), 'stable',
'high_growth', 'cyclical' (EV/EBITDA-led). Weights are stated, not hidden.
DCF uses the same convention as the toolkit: terminal FCF is the first
year AFTER the forecast, and k must exceed g.
"""
def dcf_value(fcf_forecast, terminal_fcf, k, g):
    if k<=g: raise ValueError("discount rate k must exceed terminal growth g")
    pv=sum(f/((1+k)**(i+1)) for i,f in enumerate(fcf_forecast))
    tv=terminal_fcf/(k-g); pv_tv=tv/((1+k)**len(fcf_forecast))
    return pv+pv_tv
def multiple_value(metric, multiple):
    if metric is None or multiple is None: return None
    return metric*multiple
WEIGHTS={
    "stable": {"dcf":0.50,"ev_ebitda":0.30,"pe":0.20},
    "high_growth": {"revenue":0.60,"dcf":0.40},
    "bank": {"pb":0.60,"pe":0.40},
    "cyclical": {"ev_ebitda":0.50,"dcf":0.30,"pe":0.20},
}
def blended_value(company_type, values):
    """values: dict model->value (None = unavailable). Re-weights over available models."""
    if company_type not in WEIGHTS: raise ValueError(f"unknown company_type {company_type}; use one of {sorted(WEIGHTS)}")
    w=WEIGHTS[company_type]; avail={m:v for m,v in values.items() if v is not None and m in w}
    if not avail: return None
    tot=sum(w[m] for m in avail)
    return sum(values[m]*w[m]/tot for m in avail)

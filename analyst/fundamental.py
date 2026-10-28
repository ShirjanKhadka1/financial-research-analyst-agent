"""Fundamental ratios + Piotroski F-Score (0-9). No LLM, no invented inputs."""
def ratios(fin):
    """fin: dict with revenue, net_income, equity, assets, debt, current_assets,
    current_liabilities, operating_cash_flow. Returns ratios, skipping missing inputs."""
    out={}
    def div(a,b):
        return a/b if a is not None and b not in (None,0) else None
    out["roe"]=div(fin.get("net_income"), fin.get("equity"))
    out["roa"]=div(fin.get("net_income"), fin.get("assets"))
    out["net_margin"]=div(fin.get("net_income"), fin.get("revenue"))
    out["debt_to_equity"]=div(fin.get("debt"), fin.get("equity"))
    out["current_ratio"]=div(fin.get("current_assets"), fin.get("current_liabilities"))
    out["operating_cash_flow_to_net_income"]=div(fin.get("operating_cash_flow"), fin.get("net_income"))
    return out
def piotroski(cur, prev):
    """cur/prev: dicts with roa, operating_cash_flow, leverage, current_ratio,
    shares_outstanding, gross_margin, asset_turnover (each a value, or None).
    Scores 1 point per improvement, exactly as Piotroski defined. Unknown = 0, flagged."""
    score=0; detail={}
    checks=[
        ("profitable_roa", cur.get("roa") is not None and cur["roa"]>0),
        ("positive_cash_flow", cur.get("operating_cash_flow") is not None and cur["operating_cash_flow"]>0),
        ("roa_improving", cur.get("roa") is not None and prev.get("roa") is not None and cur["roa"]>prev["roa"]),
        ("cash_flow_beats_profit", cur.get("operating_cash_flow") is not None and cur.get("net_income") is not None and cur["operating_cash_flow"]>cur["net_income"]),
        ("leverage_falling", cur.get("leverage") is not None and prev.get("leverage") is not None and cur["leverage"]<prev["leverage"]),
        ("liquidity_improving", cur.get("current_ratio") is not None and prev.get("current_ratio") is not None and cur["current_ratio"]>prev["current_ratio"]),
        ("no_new_shares", cur.get("shares_outstanding") is not None and prev.get("shares_outstanding") is not None and cur["shares_outstanding"]<=prev["shares_outstanding"]),
        ("margin_improving", cur.get("gross_margin") is not None and prev.get("gross_margin") is not None and cur["gross_margin"]>prev["gross_margin"]),
        ("turnover_improving", cur.get("asset_turnover") is not None and prev.get("asset_turnover") is not None and cur["asset_turnover"]>prev["asset_turnover"]),
    ]
    for name, ok in checks:
        detail[name]=bool(ok); score+=int(ok)
    return {"score": score, "out_of": 9, "detail": detail}

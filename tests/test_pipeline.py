from analyst import audit, valuation
from analyst.cli import DEMO
from analyst.pipeline import run


def test_demo_pipeline_runs_and_audits():
    r = run(DEMO)
    assert r["audit_valid"] and r["audit_entries"] >= 6
    assert r["piotroski"]["score"] >= 7  # demo fundamentals are strong on every check
    assert r["valuation"]["blended_value"] is not None
    assert "verdict" in r["debate"]
def test_valuation_by_type_bank_never_uses_dcf_weight():
    v = valuation.blended_value("bank", {"pb": 100, "pe": 120, "dcf": 999})
    assert abs(v - (100*0.6+120*0.4)) < 1e-9
def test_audit_chain_breaks_on_tamper():
    log = audit.AuditLog(); log.add("a", {"x": 1}); log.entries[0]["detail"] = {"x": 2}
    assert not log.verify()
def test_risk_veto_fires():
    from analyst.debate import debate
    d = debate({"rsi": 50, "piotroski_score": 9, "var_5pct": 0.20, "max_drawdown": -0.1, "valuation_gap": 0.5})
    assert d["veto"] and "RISK VETO" in d["verdict"]

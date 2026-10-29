"""Second worked example (DEMO_CYCLICAL): same pipeline, audit and veto
machinery as DEMO, different inputs, different veto outcome.

DEMO data only — DEMO_CYCLICAL is not a real company and its numbers
are not real financials. Nothing here is a buy/sell recommendation.
"""
import copy

from analyst import audit
from analyst.cli import DEMO, DEMO_CYCLICAL
from analyst.pipeline import run
from analyst.report import render


def test_second_example_runs_end_to_end():
    r = run(DEMO_CYCLICAL)
    assert r["audit_valid"] and r["audit_entries"] == run(DEMO)["audit_entries"]
    assert r["company_type"] == "cyclical"
    assert r["piotroski"]["score"] == 1  # weak demo fundamentals: 1/9
    assert r["valuation"]["blended_value"] == 73.0  # 0.5*80 + 0.3*70 + 0.2*60
    assert abs(r["valuation"]["gap_vs_price"] - (-0.27)) < 1e-9
    assert r["sentiment"]["score"] == -1.0
    assert "RISK VETO" in r["debate"]["verdict"]
    rendered = render(r, "Demo Cyclical Company — Research Report (demo data, not a real company)")
    assert "demo data, not a real company" in rendered
    assert "RISK VETO" in rendered
    assert "buy" not in rendered.lower().replace("not investment advice", "")


def test_second_example_audit_trail_is_its_own_and_tamper_evident():
    # pipeline.run() exposes validity/count, not entries, so the
    # tamper-evidence of the second example's own trail is shown on
    # the same AuditLog machinery with its own distinctive payloads.
    log = audit.AuditLog()
    log.add("input_received", {"as_of": DEMO_CYCLICAL["as_of"], "company_type": DEMO_CYCLICAL["company_type"], "n_prices": len(DEMO_CYCLICAL["prices"])})
    second = run(DEMO_CYCLICAL)
    log.add("risk", second["risk"])
    assert log.verify()
    # Its trail differs from DEMO's: different company type and VaR.
    demo_log = audit.AuditLog()
    demo_log.add("input_received", {"as_of": DEMO["as_of"], "company_type": DEMO["company_type"], "n_prices": len(DEMO["prices"])})
    demo_log.add("risk", run(DEMO)["risk"])
    assert log.entries[0]["detail"] != demo_log.entries[0]["detail"]
    assert log.entries[1]["detail"] != demo_log.entries[1]["detail"]
    # Tampering with the second trail breaks it, exactly as with DEMO.
    log.entries[1]["detail"] = dict(log.entries[1]["detail"], var_5pct=0.01)
    assert not log.verify()


def test_veto_differs_and_is_driven_by_second_example_inputs():
    first, second = run(DEMO), run(DEMO_CYCLICAL)
    assert first["debate"]["veto"] is False
    assert first["risk"]["var_5pct"] <= 0.10
    assert second["debate"]["veto"] is True
    assert second["risk"]["var_5pct"] == 0.12  # repeated 100 -> 88 drops
    assert second["risk"]["max_drawdown"] == -0.12  # above the -40% drawdown trigger
    assert "VaR" in (second["debate"]["veto_reason"] or "")
    # Not rigged to the example: keep every second-example input except
    # the price series, swap in DEMO's smooth series, and the veto clears.
    smoothed = copy.deepcopy(DEMO_CYCLICAL)
    smoothed["prices"] = DEMO["prices"]
    smoothed["market_prices"] = DEMO["market_prices"]
    assert run(smoothed)["debate"]["veto"] is False

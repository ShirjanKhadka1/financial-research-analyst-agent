"""Bad-input rejection — every guard the pipeline claims, pinned at its
boundary. Stdlib only, offline. Lenient boundaries (blended value with
no available model -> None, empty sentiment -> 0.0) are asserted as
lenient, not as rejections, so the test states which side each boundary
falls on. No pipeline behaviour is changed by this file.
"""
import pytest

from analyst import risk, technical, valuation
from analyst.cli import DEMO
from analyst.debate import debate
from analyst.pipeline import run


def _demo_with(**overrides):
    data = dict(DEMO)
    data.update(overrides)
    return data


# --- Valuation guards ----------------------------------------------------

def test_valuation_rejects_unknown_company_type():
    with pytest.raises(ValueError, match="unknown company_type"):
        valuation.blended_value("mystery", {"pe": 10})


def test_valuation_bank_ignores_dcf_even_when_supplied():
    # The by-type guard: a bank blend uses P/B + P/E only; a DCF value
    # of 999 must not move the result at all.
    assert valuation.blended_value(
        "bank", {"pb": 100, "pe": 120, "dcf": 999}) == pytest.approx(
            100 * 0.6 + 120 * 0.4)


def test_valuation_reweights_over_available_models_only():
    # Stable weights are dcf 0.50 / ev_ebitda 0.30 / pe 0.20; with only
    # DCF available the weight renormalises to 1.0, not 0.50.
    assert valuation.blended_value("stable", {"dcf": 110}) == 110.0


def test_valuation_no_available_model_is_none_not_zero():
    assert valuation.blended_value("stable", {"dcf": None}) is None
    assert valuation.blended_value("stable", {}) is None


def test_dcf_rejects_k_not_above_g():
    with pytest.raises(ValueError, match="k must exceed"):
        valuation.dcf_value([10], 100, 0.05, 0.05)
    with pytest.raises(ValueError, match="k must exceed"):
        valuation.dcf_value([10], 100, 0.04, 0.05)


# --- Indicator / risk guards ----------------------------------------------

def test_indicators_reject_short_series():
    with pytest.raises(ValueError):
        technical.sma([1, 2], 20)
    with pytest.raises(ValueError):
        technical.ema([1, 2], 20)
    with pytest.raises(ValueError):
        technical.rsi([100.0] * 10, 14)
    with pytest.raises(ValueError):
        technical.macd([100.0] * 10)
    with pytest.raises(ValueError):
        technical.bollinger([100.0] * 10)


def test_risk_rejects_too_few_prices_and_mismatched_beta():
    with pytest.raises(ValueError):
        risk.returns_from_prices([100.0])
    with pytest.raises(ValueError):
        risk.beta([0.01, 0.02], [0.01])
    with pytest.raises(ValueError):
        risk.beta([0.01], [0.01])


# --- Pipeline-level rejection ----------------------------------------------

def test_pipeline_rejects_missing_prices():
    with pytest.raises(KeyError):
        run({"company_type": "stable"})


def test_pipeline_rejects_empty_prices():
    with pytest.raises(ValueError):
        run(_demo_with(prices=[]))


def test_pipeline_rejects_unknown_company_type():
    with pytest.raises(ValueError, match="unknown company_type"):
        run(_demo_with(company_type="mystery"))


def test_pipeline_accepts_demo_unchanged():
    # Guard test: the rejection cases above must not break the happy path.
    result = run(DEMO)
    assert result["audit_valid"] is True
    assert result["valuation"]["blended_value"] is not None


# --- Risk Veto boundaries (strict >, not >=) -------------------------------

def test_veto_fires_above_thresholds():
    assert debate({"rsi": 50, "piotroski_score": 9, "var_5pct": 0.11,
                   "max_drawdown": -0.1, "valuation_gap": 0.5})["veto"]
    assert debate({"rsi": 50, "piotroski_score": 9, "var_5pct": 0.05,
                   "max_drawdown": -0.41, "valuation_gap": 0.5})["veto"]


def test_veto_does_not_fire_exactly_at_thresholds():
    base = {"rsi": 50, "piotroski_score": 9, "valuation_gap": 0.5}
    assert not debate({**base, "var_5pct": 0.10,
                       "max_drawdown": -0.1})["veto"]
    assert not debate({**base, "var_5pct": 0.05,
                       "max_drawdown": -0.40})["veto"]

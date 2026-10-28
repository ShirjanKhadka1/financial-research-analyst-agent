"""Isolated indicator tests — one indicator at a time, on hand-computed
series, so a pipeline failure can be traced to the indicator that broke.
Stdlib only, offline.
"""
import pytest

from analyst import technical


def test_sma_known_values():
    # Mean of the last n prices only; earlier prices do not leak in.
    assert technical.sma([1, 2, 3, 4, 5], 3) == 4.0
    assert technical.sma([10, 20, 30], 3) == 20.0


def test_sma_rejects_too_few_prices_and_bad_window():
    with pytest.raises(ValueError):
        technical.sma([1, 2], 5)
    with pytest.raises(ValueError):
        technical.sma([1, 2, 3], 0)


def test_ema_seed_is_sma_of_first_window():
    assert technical.ema([10, 20, 30], 3) == pytest.approx(20.0)


def test_ema_rejects_too_few_prices():
    with pytest.raises(ValueError):
        technical.ema([1, 2], 3)


def test_rsi_all_gains_is_100_all_losses_is_0():
    assert technical.rsi([100 + i for i in range(20)]) == 100.0
    assert technical.rsi([100 - i for i in range(20)]) == 0.0


def test_rsi_flat_series_is_50_by_convention():
    # KNOWN-FAILING case, reported not fixed (see slice report): a flat
    # series has no gains AND no losses (ag == al == 0), so the neutral
    # reading is 50 — the same convention the scanner repo uses. The
    # current code returns 100.0 here because its `al == 0` branch
    # cannot tell "all gains" from "no movement", and 100 then feeds
    # the debate as an "overbought" bear point on a series that did
    # not move at all. Behaviour is deliberately left unchanged.
    assert technical.rsi([50.0] * 20) == 50.0


def test_rsi_rejects_too_few_prices():
    with pytest.raises(ValueError):
        technical.rsi([100, 101], 14)


def test_macd_rejects_too_few_prices():
    with pytest.raises(ValueError):
        technical.macd([100.0] * 10)


def test_macd_rising_series_is_positive():
    result = technical.macd([100 + i for i in range(60)])
    assert result["macd"] > 0
    assert result["signal"] is not None and result["signal"] > 0


def test_bollinger_flat_series_bands_equal_price():
    result = technical.bollinger([50.0] * 20)
    assert result == {"middle": 50.0, "upper": 50.0, "lower": 50.0,
                      "bandwidth": 0.0}


def test_bollinger_known_values():
    closes = list(range(1, 21))  # mean 10.5
    result = technical.bollinger(closes, 20, 2.0)
    assert result["middle"] == pytest.approx(10.5)
    assert result["upper"] > result["middle"] > result["lower"]


def test_bollinger_rejects_too_few_prices():
    with pytest.raises(ValueError):
        technical.bollinger([100.0] * 5)

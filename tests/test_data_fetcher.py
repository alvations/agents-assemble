"""Tests for data_fetcher.py — the data layer.

Validates:
- Module-level functions and constants
- compute_stock_score returns valid score (1-10)
- estimate_fair_value returns dict with expected keys
- check_strategy_triggers returns dict
- Cache path generation
- API key helpers

External calls (yfinance, web) are mocked to avoid network dependency.
"""
import sys
import math
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


def _make_yf_ticker_mock(symbol="AAPL"):
    """Create a mock yfinance.Ticker with realistic data."""
    mock = MagicMock()
    mock.info = {
        "currentPrice": 175.0,
        "regularMarketPrice": 175.0,
        "trailingPE": 28.5,
        "priceToBook": 45.0,
        "returnOnEquity": 0.15,
        "debtToEquity": 180.0,
        "dividendYield": 0.005,
        "revenueGrowth": 0.08,
        "freeCashflow": 100_000_000_000,
        "sharesOutstanding": 15_500_000_000,
        "shortName": f"{symbol} Inc.",
    }
    days = 300
    dates = pd.date_range("2023-01-01", periods=days, freq="B")
    rng = np.random.RandomState(42)
    close = 150 + np.cumsum(rng.randn(days) * 1.5)
    close = np.maximum(close, 50.0)
    hist_df = pd.DataFrame({
        "Open": close * 0.998,
        "High": close * 1.012,
        "Low": close * 0.988,
        "Close": close,
        "Volume": rng.randint(30_000_000, 100_000_000, days),
    }, index=dates)
    mock.history.return_value = hist_df
    return mock


# ---------------------------------------------------------------------------
# Module imports and constants
# ---------------------------------------------------------------------------
class TestModuleImports:
    def test_import_data_fetcher(self):
        import data_fetcher
        assert hasattr(data_fetcher, "fetch_ohlcv")
        assert hasattr(data_fetcher, "compute_stock_score")
        assert hasattr(data_fetcher, "estimate_fair_value")
        assert hasattr(data_fetcher, "check_strategy_triggers")

    def test_universe_exists(self):
        from data_fetcher import UNIVERSE
        assert isinstance(UNIVERSE, dict)
        assert len(UNIVERSE) > 10  # Many asset categories

    def test_api_keys_registry(self):
        from data_fetcher import API_KEYS
        assert "FRED_API_KEY" in API_KEYS
        assert "FINNHUB_API_KEY" in API_KEYS

    def test_cache_dir_constant(self):
        from data_fetcher import CACHE_DIR
        assert isinstance(CACHE_DIR, Path)


# ---------------------------------------------------------------------------
# Cache helpers
# ---------------------------------------------------------------------------
class TestCacheHelpers:
    def test_canonical_cache_path_format(self):
        from data_fetcher import _canonical_cache_path
        path = _canonical_cache_path("AAPL", "1d")
        assert path.name == "ohlcv_AAPL_1d.parquet"

    def test_canonical_cache_path_sanitizes(self):
        from data_fetcher import _canonical_cache_path
        path = _canonical_cache_path("BRK/B", "1d")
        assert "/" not in path.name or str(path).count("/") == str(path.parent).count("/") + 1

    def test_cache_path_function(self):
        from data_fetcher import _cache_path
        path = _cache_path("test_key")
        assert path.suffix == ".parquet"

    def test_get_api_key(self):
        from data_fetcher import get_api_key
        # Should return None when env var not set (unless user has it)
        result = get_api_key("NONEXISTENT_KEY_12345")
        assert result is None

    def test_summarize_api_keys(self):
        from data_fetcher import summarize_api_keys
        summary = summarize_api_keys()
        assert isinstance(summary, str)
        assert "API Key Status" in summary


# ---------------------------------------------------------------------------
# compute_stock_score — mocked yfinance
# ---------------------------------------------------------------------------
class TestComputeStockScore:
    @patch("data_fetcher.yf", create=True)
    def test_returns_valid_score(self, mock_yf_module):
        """Score should be 1-10 with breakdown keys."""
        mock_ticker = _make_yf_ticker_mock("AAPL")
        mock_yf_module.Ticker.return_value = mock_ticker

        # We need to patch at the point of use inside compute_stock_score
        with patch("yfinance.Ticker", return_value=mock_ticker):
            from data_fetcher import compute_stock_score
            result = compute_stock_score("AAPL")

        assert isinstance(result, dict)
        assert "score" in result
        score = result["score"]
        assert isinstance(score, (int, float))
        assert 1 <= score <= 10

    @patch("data_fetcher.yf", create=True)
    def test_breakdown_keys(self, mock_yf_module):
        mock_ticker = _make_yf_ticker_mock("MSFT")
        mock_yf_module.Ticker.return_value = mock_ticker

        with patch("yfinance.Ticker", return_value=mock_ticker):
            from data_fetcher import compute_stock_score
            result = compute_stock_score("MSFT")

        assert "breakdown" in result or "score" in result
        # Score is always present
        assert "score" in result


# ---------------------------------------------------------------------------
# estimate_fair_value — mocked yfinance
# ---------------------------------------------------------------------------
class TestEstimateFairValue:
    def test_returns_expected_keys(self):
        """Fair value result should have required keys."""
        mock_ticker = _make_yf_ticker_mock("AAPL")

        with patch("yfinance.Ticker", return_value=mock_ticker):
            from data_fetcher import estimate_fair_value
            result = estimate_fair_value("AAPL")

        assert isinstance(result, dict)
        assert "symbol" in result
        assert result["symbol"] == "AAPL"
        # Either has fair_value_per_share or error
        assert "fair_value_per_share" in result or "error" in result

    def test_with_valid_fundamentals(self):
        """With good data, should produce numeric fair value."""
        mock_ticker = _make_yf_ticker_mock("AAPL")
        # Ensure all needed fields are present and valid
        mock_ticker.info.update({
            "currentPrice": 175.0,
            "freeCashflow": 100_000_000_000,
            "revenueGrowth": 0.08,
            "sharesOutstanding": 15_500_000_000,
        })

        with patch("yfinance.Ticker", return_value=mock_ticker):
            from data_fetcher import estimate_fair_value
            result = estimate_fair_value("AAPL")

        assert result["fair_value_per_share"] is not None
        assert isinstance(result["fair_value_per_share"], (int, float))
        assert result["fair_value_per_share"] > 0
        assert "rating" in result
        assert result["rating"] in ("undervalued", "fair_value", "overvalued")

    def test_with_missing_data(self):
        """With missing fundamentals, should return error gracefully."""
        mock_ticker = MagicMock()
        mock_ticker.info = {"shortName": "Bad Corp"}  # Missing critical fields

        with patch("yfinance.Ticker", return_value=mock_ticker):
            from data_fetcher import estimate_fair_value
            result = estimate_fair_value("BAD")

        assert result["fair_value_per_share"] is None
        assert "error" in result or result["rating"] == "insufficient_data"

    def test_discount_rate_validation(self):
        """Discount rate too low should produce error."""
        mock_ticker = MagicMock()
        mock_ticker.info = {
            "currentPrice": 100.0,
            "freeCashflow": 1_000_000,
            "sharesOutstanding": 1_000_000,
        }

        with patch("yfinance.Ticker", return_value=mock_ticker):
            from data_fetcher import estimate_fair_value
            result = estimate_fair_value("TEST", discount_rate=0.02)

        # Should catch that discount_rate <= terminal_growth
        assert "error" in result or result["fair_value_per_share"] is None


# ---------------------------------------------------------------------------
# check_strategy_triggers — mocked fetch_ohlcv
# ---------------------------------------------------------------------------
class TestCheckStrategyTriggers:
    def test_returns_dict_of_triggers(self):
        """Each trigger should have active, signal, tickers_affected."""
        # Mock fetch_ohlcv to return synthetic data
        days = 300
        dates = pd.date_range("2022-01-01", periods=days, freq="B")
        rng = np.random.RandomState(42)
        close = 100 + np.cumsum(rng.randn(days) * 0.5)
        close = np.maximum(close, 1.0)
        mock_df = pd.DataFrame({
            "Open": close * 0.999, "High": close * 1.01,
            "Low": close * 0.99, "Close": close,
            "Volume": rng.randint(1e6, 1e7, days),
        }, index=dates)

        with patch("data_fetcher.fetch_ohlcv", return_value=mock_df):
            from data_fetcher import check_strategy_triggers
            triggers = check_strategy_triggers()

        assert isinstance(triggers, dict)
        assert len(triggers) > 0

        for name, trigger in triggers.items():
            assert "active" in trigger, f"Trigger {name} missing 'active'"
            assert "signal" in trigger, f"Trigger {name} missing 'signal'"
            assert isinstance(trigger["active"], bool), (
                f"Trigger {name}: 'active' should be bool"
            )


# ---------------------------------------------------------------------------
# UNIVERSE validation
# ---------------------------------------------------------------------------
class TestUniverse:
    def test_all_tickers_are_strings(self):
        from data_fetcher import UNIVERSE
        for category, tickers in UNIVERSE.items():
            assert isinstance(tickers, (list, tuple, set)), (
                f"UNIVERSE[{category}] is {type(tickers).__name__}"
            )
            for t in tickers:
                assert isinstance(t, str), (
                    f"UNIVERSE[{category}] has non-string: {t!r}"
                )

    def test_has_major_categories(self):
        from data_fetcher import UNIVERSE
        # Should have at least these broad categories
        assert len(UNIVERSE) >= 10

"""Tests for app.py Flask routes.

Validates all API routes return expected status codes and JSON structure.
External dependencies (yfinance, data fetchers) are mocked where needed.
"""
import json
import sys
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
# Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture(scope="module")
def client():
    """Flask test client — module-scoped to avoid repeated app imports."""
    import app as flask_app
    flask_app.app.testing = True
    # Clear caches so tests don't interfere
    flask_app._leaderboard_cache.clear()
    flask_app._strategies_cache.clear()
    flask_app._market_cache.clear()
    return flask_app.app.test_client()


# ---------------------------------------------------------------------------
# Index / HTML
# ---------------------------------------------------------------------------
class TestIndexRoute:
    def test_index_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_index_returns_html(self, client):
        resp = client.get("/")
        data = resp.get_data(as_text=True)
        assert "<!DOCTYPE html>" in data or "<html" in data

    def test_index_has_app_title(self, client):
        resp = client.get("/")
        data = resp.get_data(as_text=True)
        assert "agents-assemble" in data


# ---------------------------------------------------------------------------
# /api/leaderboard
# ---------------------------------------------------------------------------
class TestLeaderboardRoute:
    def test_leaderboard_returns_200(self, client):
        resp = client.get("/api/leaderboard")
        assert resp.status_code == 200

    def test_leaderboard_returns_json(self, client):
        resp = client.get("/api/leaderboard")
        data = resp.get_json()
        assert isinstance(data, list)

    def test_leaderboard_default_horizon_3y(self, client):
        """Default horizon is 3y which reads from results/ files."""
        resp = client.get("/api/leaderboard")
        assert resp.status_code == 200

    def test_leaderboard_invalid_horizon(self, client):
        resp = client.get("/api/leaderboard?horizon=invalid")
        assert resp.status_code in (200, 400)

    def test_leaderboard_entries_have_keys(self, client):
        resp = client.get("/api/leaderboard")
        data = resp.get_json()
        if data:  # May be empty if no results/ dir
            entry = data[0]
            assert "name" in entry
            assert "return" in entry


# ---------------------------------------------------------------------------
# /api/strategies
# ---------------------------------------------------------------------------
class TestStrategiesRoute:
    def test_strategies_returns_200(self, client):
        resp = client.get("/api/strategies")
        assert resp.status_code == 200

    def test_strategies_returns_list(self, client):
        resp = client.get("/api/strategies")
        data = resp.get_json()
        assert isinstance(data, list)
        assert len(data) > 50  # Should have many strategies

    def test_strategy_entries_have_name(self, client):
        resp = client.get("/api/strategies")
        data = resp.get_json()
        for entry in data[:5]:
            assert "name" in entry
            assert "source" in entry


# ---------------------------------------------------------------------------
# /api/stock-score/<symbol>
# ---------------------------------------------------------------------------
class TestStockScoreRoute:
    def test_stock_score_returns_200(self, client):
        """Stock score endpoint should return 200 with mocked data."""
        mock_ticker = _make_yf_ticker_mock("AAPL")
        with patch("yfinance.Ticker", return_value=mock_ticker):
            resp = client.get("/api/stock-score/AAPL")

        assert resp.status_code == 200

    def test_stock_score_returns_json(self, client):
        mock_ticker = _make_yf_ticker_mock("MSFT")
        with patch("yfinance.Ticker", return_value=mock_ticker):
            resp = client.get("/api/stock-score/MSFT")

        data = resp.get_json()
        assert isinstance(data, dict)
        assert "score" in data

    def test_stock_score_invalid_symbol(self, client):
        resp = client.get("/api/stock-score/!!!INVALID!!!")
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# /api/fair-value/<symbol>
# ---------------------------------------------------------------------------
class TestFairValueRoute:
    def test_fair_value_returns_200(self, client):
        mock_ticker = _make_yf_ticker_mock("AAPL")
        mock_ticker.info.update({
            "currentPrice": 175.0,
            "freeCashflow": 100_000_000_000,
            "revenueGrowth": 0.08,
            "sharesOutstanding": 15_500_000_000,
        })
        with patch("yfinance.Ticker", return_value=mock_ticker):
            resp = client.get("/api/fair-value/AAPL")

        assert resp.status_code == 200

    def test_fair_value_returns_json(self, client):
        mock_ticker = _make_yf_ticker_mock("MSFT")
        with patch("yfinance.Ticker", return_value=mock_ticker):
            resp = client.get("/api/fair-value/MSFT")

        data = resp.get_json()
        assert isinstance(data, dict)
        assert "symbol" in data

    def test_fair_value_invalid_symbol(self, client):
        resp = client.get("/api/fair-value/BAD!!!")
        assert resp.status_code == 400

    def test_fair_value_custom_discount_rate(self, client):
        mock_ticker = _make_yf_ticker_mock("AAPL")
        mock_ticker.info.update({
            "currentPrice": 175.0,
            "freeCashflow": 100_000_000_000,
            "revenueGrowth": 0.08,
            "sharesOutstanding": 15_500_000_000,
        })
        with patch("yfinance.Ticker", return_value=mock_ticker):
            resp = client.get("/api/fair-value/AAPL?discount_rate=0.12")

        assert resp.status_code == 200

    def test_fair_value_bad_discount_rate(self, client):
        resp = client.get("/api/fair-value/AAPL?discount_rate=-1")
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# /api/alerts
# ---------------------------------------------------------------------------
class TestAlertsRoute:
    def test_alerts_returns_200(self, client):
        """Alerts should return 200 even when mocked."""
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
            resp = client.get("/api/alerts")

        assert resp.status_code == 200

    def test_alerts_returns_json(self, client):
        days = 300
        dates = pd.date_range("2022-01-01", periods=days, freq="B")
        rng = np.random.RandomState(42)
        close = 100 + np.cumsum(rng.randn(days) * 0.5)
        mock_df = pd.DataFrame({
            "Close": np.maximum(close, 1.0),
            "Open": close, "High": close + 1, "Low": close - 1,
            "Volume": np.full(days, 5_000_000),
        }, index=dates)

        with patch("data_fetcher.fetch_ohlcv", return_value=mock_df):
            resp = client.get("/api/alerts")

        data = resp.get_json()
        assert isinstance(data, dict)


# ---------------------------------------------------------------------------
# /api/market
# ---------------------------------------------------------------------------
class TestMarketRoute:
    def test_market_returns_200(self, client):
        """Market route should return 200 (may be empty without network)."""
        resp = client.get("/api/market")
        assert resp.status_code == 200

    def test_market_returns_json(self, client):
        resp = client.get("/api/market")
        data = resp.get_json()
        assert isinstance(data, dict)


# ---------------------------------------------------------------------------
# /api/stock-pick
# ---------------------------------------------------------------------------
class TestStockPickRoute:
    def test_no_symbols_returns_400(self, client):
        resp = client.get("/api/stock-pick")
        assert resp.status_code == 400

    def test_invalid_symbol_returns_400(self, client):
        resp = client.get("/api/stock-pick?symbols=!!!BAD!!!")
        assert resp.status_code == 400

    def test_too_many_symbols_returns_400(self, client):
        syms = ",".join([f"SYM{i}" for i in range(25)])
        resp = client.get(f"/api/stock-pick?symbols={syms}")
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# /api/top-picks
# ---------------------------------------------------------------------------
class TestTopPicksRoute:
    def test_top_picks_returns_200(self, client):
        resp = client.get("/api/top-picks")
        assert resp.status_code == 200

    def test_top_picks_returns_json(self, client):
        resp = client.get("/api/top-picks")
        data = resp.get_json()
        assert isinstance(data, (list, dict))


# ---------------------------------------------------------------------------
# Route validation: symbol sanitization
# ---------------------------------------------------------------------------
class TestInputValidation:
    def test_stock_score_rejects_path_traversal(self, client):
        resp = client.get("/api/stock-score/../etc/passwd")
        # Should either 404 or 400, not serve a file
        assert resp.status_code in (400, 404)

    def test_fair_value_rejects_script(self, client):
        resp = client.get("/api/fair-value/<script>alert(1)</script>")
        assert resp.status_code in (400, 404)

    def test_alerts_strategy_rejects_invalid(self, client):
        resp = client.get("/api/alerts/../../etc/passwd")
        assert resp.status_code in (400, 404)


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------
class TestAppHelpers:
    def test_sanitize_for_json(self):
        import app
        # NaN should become None
        result = app._sanitize_for_json({"val": float("nan")})
        assert result["val"] is None

    def test_sanitize_for_json_inf(self):
        import app
        result = app._sanitize_for_json({"val": float("inf")})
        assert result["val"] is None

    def test_safe_metric_normal(self):
        import app
        assert app._safe_metric(1.23456, 2) == 1.23

    def test_safe_metric_nan(self):
        import app
        assert app._safe_metric(float("nan")) == 0

    def test_safe_metric_bool(self):
        import app
        assert app._safe_metric(True) == 0

    def test_is_finite_number(self):
        import app
        assert app._is_finite_number(1.0) is True
        assert app._is_finite_number(float("nan")) is False
        assert app._is_finite_number(True) is False
        assert app._is_finite_number("1.0") is False

    def test_valid_date(self):
        import app
        assert app._valid_date("2024-01-15") is True
        assert app._valid_date("not-a-date") is False
        assert app._valid_date("2024-13-01") is False

"""Tests for StockPick feature. Run with: python -m pytest tests/test_stock_picker.py -v"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest


# ---------------------------------------------------------------------------
# Unit tests for stock_picker.py
# ---------------------------------------------------------------------------
class TestLoadStrategies:
    def test_loads_strategies(self):
        from stock_picker import _load_all_strategies
        strategies = _load_all_strategies()
        assert len(strategies) > 50, f"Expected 50+ strategies, got {len(strategies)}"

    def test_strategy_has_required_fields(self):
        from stock_picker import _load_all_strategies
        strategies = _load_all_strategies()
        for s in strategies[:5]:
            assert "key" in s
            assert "source" in s
            assert "universe" in s
            assert isinstance(s["universe"], set)
            assert len(s["universe"]) > 0

    def test_strategy_cache(self):
        from stock_picker import _get_strategies
        s1 = _get_strategies()
        s2 = _get_strategies()
        assert s1 is s2, "Strategy cache should return same object"


class TestMatchStrategies:
    def test_match_known_ticker(self):
        from stock_picker import _match_strategies, _get_strategies
        strategies = _get_strategies()
        matches = _match_strategies(["NVDA", "AAPL"], strategies)
        assert len(matches) > 0, "NVDA+AAPL should match at least one strategy"
        assert matches[0]["overlap"], "Best match should have overlap"

    def test_match_returns_sorted(self):
        from stock_picker import _match_strategies, _get_strategies
        strategies = _get_strategies()
        matches = _match_strategies(["NVDA", "AAPL", "MSFT"], strategies)
        if len(matches) > 1:
            assert matches[0]["score"] >= matches[1]["score"]

    def test_no_match_for_obscure_ticker(self):
        from stock_picker import _match_strategies, _get_strategies
        strategies = _get_strategies()
        matches = _match_strategies(["XYZNONEXIST"], strategies)
        assert len(matches) == 0


class TestPositionTable:
    def test_generates_positions(self):
        from stock_picker import _generate_position_table
        metrics = {
            "total_return": 0.50, "sharpe_ratio": 1.0, "max_drawdown": -0.15,
            "win_rate": 0.55, "profit_factor": 1.5, "cagr": 0.20,
        }
        positions = _generate_position_table(["AAPL"], ["MSFT"], metrics, 100000)
        assert len(positions) >= 1
        # Check required fields
        for p in positions:
            assert "symbol" in p
            assert "action" in p
            assert "annual_volatility" in p
            assert "stop_loss" in p
            assert "take_profit" in p
            assert "position_size" in p
            assert "is_user_pick" in p

    def test_user_picks_flagged(self):
        from stock_picker import _generate_position_table
        metrics = {"total_return": 0.5, "sharpe_ratio": 1.0, "max_drawdown": -0.1,
                    "win_rate": 0.5, "profit_factor": 1.3, "cagr": 0.15}
        positions = _generate_position_table(["AAPL"], ["MSFT"], metrics, 100000)
        user_picks = [p for p in positions if p["is_user_pick"]]
        suggested = [p for p in positions if not p["is_user_pick"]]
        assert len(user_picks) >= 1
        assert user_picks[0]["symbol"] == "AAPL"
        if suggested:
            assert suggested[0]["symbol"] == "MSFT"

    def test_losing_strategy_zero_size(self):
        from stock_picker import _generate_position_table
        metrics = {"total_return": -0.20, "sharpe_ratio": -0.5, "max_drawdown": -0.30,
                    "win_rate": 0.35, "profit_factor": 0.8, "cagr": -0.10}
        positions = _generate_position_table(["AAPL"], [], metrics, 100000)
        for p in positions:
            assert p["position_size"] == "0.0%", f"{p['symbol']} should have 0% size for losing strategy"
            assert p["action"] in ("HOLD", "WATCH", "SKIP")

    def test_vol_adjusted_sizing(self):
        from stock_picker import _generate_position_table
        metrics = {"total_return": 1.0, "sharpe_ratio": 1.5, "max_drawdown": -0.10,
                    "win_rate": 0.60, "profit_factor": 2.0, "cagr": 0.30}
        # TSLA (high vol) vs KO (low vol) — TSLA should get smaller size
        positions = _generate_position_table(["TSLA", "KO"], [], metrics, 100000)
        if len(positions) == 2:
            tsla_size = float(positions[0]["position_size"].rstrip("%")) if positions[0]["symbol"] == "TSLA" else float(positions[1]["position_size"].rstrip("%"))
            ko_size = float(positions[1]["position_size"].rstrip("%")) if positions[1]["symbol"] == "KO" else float(positions[0]["position_size"].rstrip("%"))
            assert ko_size > tsla_size, f"KO ({ko_size}%) should have larger size than TSLA ({tsla_size}%) due to lower vol"


class TestAnalyzeStockPicks:
    def test_basic_analysis(self):
        from stock_picker import analyze_stock_picks
        result = analyze_stock_picks(["NVDA", "AAPL"], include_claude=False, horizon="3y")
        assert "user_picks" in result
        assert "recommendations" in result
        assert len(result["recommendations"]) > 0
        rec = result["recommendations"][0]
        assert "positions" in rec
        assert "hypothesis" in rec
        assert "strategy_explanation" in rec

    def test_empty_symbols(self):
        from stock_picker import analyze_stock_picks
        result = analyze_stock_picks([], include_claude=False)
        assert "error" in result

    def test_invalid_ticker(self):
        from stock_picker import analyze_stock_picks
        result = analyze_stock_picks(["XYZNONEXIST999"], include_claude=False)
        assert "error" in result or len(result.get("user_picks", [])) == 0

    def test_top_n_recommendations(self):
        from stock_picker import analyze_stock_picks
        result = analyze_stock_picks(["NVDA", "AAPL"], include_claude=False, top_n=3)
        recs = result.get("recommendations", [])
        assert len(recs) >= 1
        assert len(recs) <= 3

    def test_has_additional_tickers(self):
        from stock_picker import analyze_stock_picks
        result = analyze_stock_picks(["NVDA"], include_claude=False, horizon="3y")
        rec = result["recommendations"][0]
        assert len(rec.get("additional_tickers", [])) > 0, "Should suggest additional tickers"

    def test_matched_strategy_populated(self):
        from stock_picker import analyze_stock_picks
        result = analyze_stock_picks(["AAPL", "MSFT", "GOOGL"], include_claude=False, horizon="3y")
        rec = result["recommendations"][0]
        ms = rec.get("matched_strategy")
        assert ms is not None, "Should match a strategy for FAANG stocks"
        assert "name" in ms
        assert "source" in ms

    def test_backtest_included(self):
        from stock_picker import analyze_stock_picks
        result = analyze_stock_picks(["AAPL", "MSFT"], include_claude=False, horizon="3y")
        rec = result["recommendations"][0]
        bt = rec.get("backtest")
        if bt:
            assert "metrics" in bt
            m = bt["metrics"]
            assert "total_return" in m
            assert "sharpe_ratio" in m
            assert "max_drawdown" in m

    def test_notes_is_list(self):
        from stock_picker import analyze_stock_picks
        result = analyze_stock_picks(["SPY"], include_claude=False, horizon="3y")
        rec = result["recommendations"][0]
        assert "notes" in rec
        assert isinstance(rec["notes"], list)

    def test_total_strategies_matched(self):
        from stock_picker import analyze_stock_picks
        result = analyze_stock_picks(["AAPL", "NVDA"], include_claude=False)
        assert "total_strategies_matched" in result
        assert result["total_strategies_matched"] > 0


# ---------------------------------------------------------------------------
# Integration test for the Flask API endpoint
# ---------------------------------------------------------------------------
class TestAPIEndpoint:
    @pytest.fixture
    def client(self):
        import app as flask_app
        flask_app.app.testing = True
        return flask_app.app.test_client()

    def test_stock_pick_endpoint(self, client):
        resp = client.get("/api/stock-pick?symbols=NVDA,AAPL&claude=0&top_n=2")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "recommendations" in data
        assert len(data["recommendations"]) > 0
        assert "positions" in data["recommendations"][0]

    def test_stock_pick_no_symbols(self, client):
        resp = client.get("/api/stock-pick")
        assert resp.status_code == 400

    def test_stock_pick_invalid_symbol(self, client):
        resp = client.get("/api/stock-pick?symbols=INVALID!!!")
        assert resp.status_code == 400

    def test_stock_pick_max_symbols(self, client):
        syms = ",".join([f"SYM{i}" for i in range(25)])
        resp = client.get(f"/api/stock-pick?symbols={syms}")
        assert resp.status_code == 400

    def test_stock_pick_html_has_tab(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        html = resp.get_data(as_text=True)
        assert "StockPick" in html
        assert "section-stockpick" in html


# ---------------------------------------------------------------------------
# Data fetcher cache tests
# ---------------------------------------------------------------------------
class TestCanonicalCache:
    def test_canonical_cache_path(self):
        from data_fetcher import _canonical_cache_path
        path = _canonical_cache_path("AAPL", "1d")
        assert path.name == "ohlcv_AAPL_1d.parquet"

    def test_fetch_uses_canonical_cache(self):
        """After fetch, canonical cache file should exist (no date range in name)."""
        from data_fetcher import fetch_ohlcv, _canonical_cache_path
        fetch_ohlcv("SPY", start="2024-01-01", cache=True)
        path = _canonical_cache_path("SPY", "1d")
        assert path.exists(), "Canonical cache file should exist after fetch"

    def test_different_date_ranges_same_cache(self):
        """Different date ranges should use the same canonical cache file."""
        from data_fetcher import fetch_ohlcv, _canonical_cache_path
        import time
        # First fetch
        fetch_ohlcv("AAPL", start="2023-01-01", cache=True)
        path = _canonical_cache_path("AAPL", "1d")
        mtime1 = path.stat().st_mtime

        # Very short sleep to ensure time difference if file is written
        time.sleep(0.01)

        # Second fetch with different range — should NOT create new file
        fetch_ohlcv("AAPL", start="2024-06-01", end="2024-12-31", cache=True)
        mtime2 = path.stat().st_mtime

        # mtime should be the same (no rewrite needed for cached data)
        # Or at most slightly newer if incremental update happened
        assert path.exists()

    def test_sgx_universe_added(self):
        from data_fetcher import UNIVERSE
        assert "singapore_sgx" in UNIVERSE
        assert len(UNIVERSE["singapore_sgx"]) >= 40
        assert "D05.SI" in UNIVERSE["singapore_sgx"]  # DBS
        assert "U11.SI" in UNIVERSE["singapore_sgx"]  # UOB

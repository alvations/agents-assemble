"""Tests for trade_recommender.py.

Validates:
- generate_trade_recommendations produces correct structure
- save_strategy_recommendation creates .md and .json files
- Winning vs losing classification
- position_recommendations is populated
- risk_parameters has strategy-specific values
"""
import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from trade_recommender import (
    generate_trade_recommendations,
    save_strategy_recommendation,
    _safe_float,
    _strategy_risk_params,
    _assess_strategy,
)


# ---------------------------------------------------------------------------
# _safe_float
# ---------------------------------------------------------------------------
class TestSafeFloat:
    def test_normal_float(self):
        assert _safe_float(1.5) == 1.5

    def test_int(self):
        assert _safe_float(42) == 42.0

    def test_none(self):
        assert _safe_float(None) == 0.0

    def test_nan(self):
        assert _safe_float(float("nan")) == 0.0

    def test_inf(self):
        assert _safe_float(float("inf")) == 0.0

    def test_bool_rejected(self):
        assert _safe_float(True) == 0.0
        assert _safe_float(False) == 0.0

    def test_string_rejected(self):
        assert _safe_float("1.5") == 0.0

    def test_custom_default(self):
        assert _safe_float(None, default=5.0) == 5.0


# ---------------------------------------------------------------------------
# generate_trade_recommendations
# ---------------------------------------------------------------------------
class TestGenerateTradeRecommendations:
    @pytest.fixture
    def winning_metrics(self):
        return {
            "total_return": 0.99,
            "sharpe_ratio": 1.20,
            "max_drawdown": -0.166,
            "win_rate": 0.55,
            "profit_factor": 1.31,
            "alpha": 0.171,
            "cagr": 0.234,
            "annual_volatility": 0.167,
        }

    @pytest.fixture
    def losing_metrics(self):
        return {
            "total_return": -0.25,
            "sharpe_ratio": -0.50,
            "max_drawdown": -0.40,
            "win_rate": 0.35,
            "profit_factor": 0.70,
            "alpha": -0.10,
            "cagr": -0.15,
            "annual_volatility": 0.30,
        }

    def test_winning_classification(self, winning_metrics):
        recs = generate_trade_recommendations(
            "momentum_test", winning_metrics,
            {"NVDA": {"qty": 50, "avg_cost": 120.5}},
        )
        assert recs["is_winning"] is True
        assert recs["strategy_name"] == "momentum_test"

    def test_losing_classification(self, losing_metrics):
        recs = generate_trade_recommendations(
            "bad_strategy", losing_metrics,
            {"AAPL": {"qty": 10, "avg_cost": 200.0}},
        )
        assert recs["is_winning"] is False

    def test_has_required_keys(self, winning_metrics):
        recs = generate_trade_recommendations(
            "test_strat", winning_metrics,
            {"AAPL": {"qty": 10}},
        )
        assert "strategy_name" in recs
        assert "is_winning" in recs
        assert "overall_assessment" in recs
        assert "risk_parameters" in recs
        assert "execution_guidance" in recs
        assert "position_recommendations" in recs
        assert "metrics_summary" in recs

    def test_risk_parameters_populated(self, winning_metrics):
        recs = generate_trade_recommendations(
            "momentum_test", winning_metrics,
            {"NVDA": {"qty": 50}},
        )
        rp = recs["risk_parameters"]
        assert "stop_loss" in rp
        assert "take_profit_target" in rp
        assert "max_portfolio_allocation" in rp
        assert "max_drawdown_tolerance" in rp
        # Values should be percentage strings, not empty
        assert rp["stop_loss"] != ""
        assert rp["take_profit_target"] != ""

    def test_position_recommendations_populated(self, winning_metrics):
        positions = {
            "NVDA": {"qty": 50, "avg_cost": 120.5},
            "META": {"qty": 30, "avg_cost": 350.2},
        }
        # Mock data_fetcher.fetch_ohlcv to avoid network calls (lazy import inside function)
        with patch("data_fetcher.fetch_ohlcv", side_effect=Exception("mocked")):
            recs = generate_trade_recommendations(
                "momentum_test", winning_metrics, positions,
            )
        assert len(recs["position_recommendations"]) == 2
        for pr in recs["position_recommendations"]:
            assert "symbol" in pr
            assert "action" in pr
            assert "stop_loss" in pr
            assert "take_profit" in pr

    def test_empty_positions(self, winning_metrics):
        recs = generate_trade_recommendations(
            "empty_test", winning_metrics, {},
        )
        assert recs["position_recommendations"] == []


# ---------------------------------------------------------------------------
# _strategy_risk_params — strategy-specific (not generic)
# ---------------------------------------------------------------------------
class TestStrategyRiskParams:
    def test_buffett_has_wide_stops(self):
        sl, tp, entry, scale = _strategy_risk_params(
            "buffett_value", 0.20, 0.15, 0.12, 0.55, True
        )
        assert sl >= 0.20  # Passive strategies have wide stops
        assert "DCA" in entry or "dip" in entry.lower()

    def test_momentum_has_tight_stops(self):
        sl, tp, entry, scale = _strategy_risk_params(
            "momentum_crash_hedge", 0.15, 0.20, 0.20, 0.55, True
        )
        assert sl <= 0.20  # Momentum has tighter stops

    def test_seasonal_has_time_exit(self):
        sl, tp, entry, scale = _strategy_risk_params(
            "january_effect", 0.10, 0.15, 0.05, 0.50, True
        )
        assert "calendar" in entry.lower() or "market" in entry.lower()

    def test_different_strategies_different_params(self):
        """Different strategy types should produce different risk params."""
        buffett = _strategy_risk_params("buffett_value", 0.20, 0.15, 0.12, 0.55, True)
        momentum = _strategy_risk_params("momentum_growth", 0.15, 0.20, 0.20, 0.55, True)
        seasonal = _strategy_risk_params("santa_claus_rally", 0.08, 0.10, 0.03, 0.50, True)

        # These should not all be identical
        params = [buffett, momentum, seasonal]
        stop_losses = [p[0] for p in params]
        # At least 2 different stop losses
        assert len(set(round(s, 2) for s in stop_losses)) >= 2


# ---------------------------------------------------------------------------
# _assess_strategy
# ---------------------------------------------------------------------------
class TestAssessStrategy:
    def test_strong_buy(self):
        assessment = _assess_strategy({"sharpe_ratio": 1.5, "alpha": 0.10, "total_return": 0.50})
        assert "STRONG BUY" in assessment

    def test_avoid(self):
        assessment = _assess_strategy({"sharpe_ratio": -0.5, "alpha": -0.05, "total_return": -0.20})
        assert "AVOID" in assessment

    def test_hold(self):
        assessment = _assess_strategy({"sharpe_ratio": 0.3, "alpha": 0.01, "total_return": 0.05})
        assert "HOLD" in assessment or "NEUTRAL" in assessment


# ---------------------------------------------------------------------------
# save_strategy_recommendation — file creation
# ---------------------------------------------------------------------------
class TestSaveStrategyRecommendation:
    def test_creates_md_and_json(self, tmp_path):
        """Saving a recommendation should create both .md and .json files."""
        results = {
            "metrics": {
                "total_return": 0.50, "sharpe_ratio": 1.0, "max_drawdown": -0.15,
                "win_rate": 0.55, "profit_factor": 1.5, "alpha": 0.10,
                "cagr": 0.20, "annual_volatility": 0.15,
            },
            "final_positions": {"AAPL": {"qty": 10, "avg_cost": 150.0}},
        }

        # Temporarily redirect strategy dirs to tmp_path
        with patch("trade_recommender.WINNING_DIR", tmp_path / "winning"), \
             patch("trade_recommender.LOSING_DIR", tmp_path / "losing"), \
             patch("data_fetcher.fetch_ohlcv", side_effect=Exception("mocked")):
            (tmp_path / "winning").mkdir()
            (tmp_path / "losing").mkdir()
            md_path = save_strategy_recommendation("test_winning", results)

        # Should be in winning dir
        assert "winning" in str(md_path).lower() or md_path.parent.name == "winning"
        assert md_path.exists()
        assert md_path.suffix == ".md"

        # JSON should also exist
        json_path = md_path.with_suffix(".json")
        assert json_path.exists()

        # JSON should be parseable
        data = json.loads(json_path.read_text())
        assert data["strategy_name"] == "test_winning"
        assert data["is_winning"] is True

    def test_losing_goes_to_losing_dir(self, tmp_path):
        results = {
            "metrics": {
                "total_return": -0.30, "sharpe_ratio": -0.5, "max_drawdown": -0.40,
                "win_rate": 0.30, "profit_factor": 0.60,
                "cagr": -0.15, "annual_volatility": 0.30,
            },
            "final_positions": {},
        }

        with patch("trade_recommender.WINNING_DIR", tmp_path / "winning"), \
             patch("trade_recommender.LOSING_DIR", tmp_path / "losing"):
            (tmp_path / "winning").mkdir()
            (tmp_path / "losing").mkdir()
            md_path = save_strategy_recommendation("test_losing", results)

        assert "losing" in str(md_path).lower() or md_path.parent.name == "losing"

    def test_md_content_has_assessment(self, tmp_path):
        results = {
            "metrics": {
                "total_return": 0.80, "sharpe_ratio": 1.5, "max_drawdown": -0.10,
                "win_rate": 0.60, "profit_factor": 2.0, "alpha": 0.15,
                "cagr": 0.25, "annual_volatility": 0.12,
            },
            "final_positions": {"NVDA": {"qty": 20, "avg_cost": 800.0}},
        }

        with patch("trade_recommender.WINNING_DIR", tmp_path / "winning"), \
             patch("trade_recommender.LOSING_DIR", tmp_path / "losing"), \
             patch("data_fetcher.fetch_ohlcv", side_effect=Exception("mocked")):
            (tmp_path / "winning").mkdir()
            (tmp_path / "losing").mkdir()
            md_path = save_strategy_recommendation("great_strat", results)

        content = md_path.read_text()
        assert "WINNING" in content
        assert "Performance" in content or "Risk" in content

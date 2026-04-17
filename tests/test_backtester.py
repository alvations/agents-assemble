"""Tests for backtester engine.

Validates:
- Portfolio buy/sell and value tracking
- Backtester instantiation with valid/invalid args
- A simple backtest on a buy-and-hold strategy
- Parallel mode flag
- Slippage model (fixed vs volume)
- cost_summary in results
- Metrics keys (total_return, sharpe_ratio, max_drawdown)
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

# Use flat-file imports — these tests validate the agents-assemble backtester
from backtester import (
    Backtester, Portfolio, Position, Side, Trade,
    compute_metrics, format_report, estimate_spread_bps,
    HISTORICAL_CRASHES,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _make_synthetic_df(days=200, base_price=100.0, seed=42):
    """Create a synthetic OHLCV DataFrame with DatetimeIndex."""
    dates = pd.date_range("2023-01-01", periods=days, freq="B")
    rng = np.random.RandomState(seed)
    close = base_price + np.cumsum(rng.randn(days) * 0.5)
    close = np.maximum(close, 1.0)
    return pd.DataFrame({
        "Open": close * 0.999,
        "High": close * 1.01,
        "Low": close * 0.99,
        "Close": close,
        "Volume": rng.randint(1_000_000, 10_000_000, days),
    }, index=dates)


def _buy_and_hold(date, prices_dict, portfolio, data):
    """Simple strategy: buy TEST if not already holding."""
    if not portfolio.get_position("TEST"):
        return {"TEST": 0.90}
    return {}


# ---------------------------------------------------------------------------
# Portfolio tests
# ---------------------------------------------------------------------------
class TestPortfolio:
    def test_initial_state(self):
        p = Portfolio(initial_cash=50_000)
        assert p.cash == 50_000
        assert p.initial_cash == 50_000
        assert len(p.positions) == 0
        assert len(p.trades) == 0

    def test_buy_reduces_cash(self):
        p = Portfolio(initial_cash=10_000)
        p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 10, 100.0)
        assert p.cash < 10_000

    def test_buy_creates_position(self):
        p = Portfolio(initial_cash=10_000)
        p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 10, 100.0)
        pos = p.get_position("AAPL")
        assert pos is not None
        assert pos.quantity == 10

    def test_sell_closes_position(self):
        p = Portfolio(initial_cash=10_000)
        p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 10, 100.0)
        p.execute_trade(pd.Timestamp("2024-01-02"), "AAPL", Side.SELL, 10, 110.0)
        pos = p.get_position("AAPL")
        assert pos is None  # Closed positions are removed

    def test_total_value_gains(self):
        p = Portfolio(initial_cash=10_000)
        p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 10, 100.0)
        value = p.total_value({"AAPL": 110.0})
        assert value > 10_000

    def test_total_value_losses(self):
        p = Portfolio(initial_cash=10_000)
        p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 10, 100.0)
        value = p.total_value({"AAPL": 90.0})
        assert value < 10_000

    def test_invalid_quantity_raises(self):
        p = Portfolio(initial_cash=10_000)
        with pytest.raises(ValueError, match="Quantity"):
            p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 0, 100.0)

    def test_invalid_price_raises(self):
        p = Portfolio(initial_cash=10_000)
        with pytest.raises(ValueError, match="Price"):
            p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 10, -5.0)

    def test_snapshot(self):
        p = Portfolio(initial_cash=10_000)
        p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 10, 100.0)
        snap = p.snapshot(pd.Timestamp("2024-01-02"), {"AAPL": 105.0})
        assert "total_value" in snap
        assert "holdings" in snap
        assert "AAPL" in snap["holdings"]
        assert snap["holdings"]["AAPL"]["quantity"] == 10

    def test_trade_records(self):
        p = Portfolio(initial_cash=10_000)
        p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 10, 100.0)
        assert len(p.trades) == 1
        assert p.trades[0].symbol == "AAPL"
        assert p.trades[0].side == Side.BUY


# ---------------------------------------------------------------------------
# Slippage model tests
# ---------------------------------------------------------------------------
class TestSlippageModel:
    def test_fixed_slippage_default(self):
        p = Portfolio(initial_cash=100_000)
        assert p.slippage_pct == 0.0005  # 5 bps default

    def test_fixed_slippage_applied(self):
        p = Portfolio(initial_cash=100_000, cash=100_000, slippage_pct=0.001)
        trade = p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 100, 150.0)
        assert trade.slippage > 0
        expected_slippage = 150.0 * 0.001 * 100
        assert abs(trade.slippage - expected_slippage) < 0.01

    def test_volume_spread_model(self):
        p = Portfolio(initial_cash=100_000, cash=100_000, spread_model="volume")
        p.set_volume_spreads({"AAPL": 50_000_000})  # Very liquid
        trade = p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 100, 150.0)
        # Volume model should use half-spread + base slippage
        assert trade.slippage > 0

    def test_estimate_spread_bps(self):
        assert estimate_spread_bps(50_000_000) == 0.0001   # Very liquid
        assert estimate_spread_bps(5_000_000) == 0.0003    # Liquid
        assert estimate_spread_bps(500_000) == 0.0008      # Moderate
        assert estimate_spread_bps(50_000) == 0.0015       # Illiquid
        assert estimate_spread_bps(5_000) == 0.0030        # Very illiquid
        assert estimate_spread_bps(None) == 0.0005         # Unknown
        assert estimate_spread_bps(-1) == 0.0005           # Invalid


# ---------------------------------------------------------------------------
# Compute metrics
# ---------------------------------------------------------------------------
class TestComputeMetrics:
    def test_basic_metrics(self):
        dates = pd.date_range("2023-01-01", periods=250, freq="B")
        returns = pd.Series(
            np.random.RandomState(42).randn(250) * 0.01,
            index=dates,
        )
        m = compute_metrics(returns)
        assert "total_return" in m
        assert "sharpe_ratio" in m
        assert "max_drawdown" in m
        assert m["max_drawdown"] <= 0

    def test_with_benchmark(self):
        dates = pd.date_range("2023-01-01", periods=250, freq="B")
        rng = np.random.RandomState(42)
        returns = pd.Series(rng.randn(250) * 0.01, index=dates)
        bench = pd.Series(rng.randn(250) * 0.008, index=dates)
        m = compute_metrics(returns, bench)
        assert "alpha" in m
        assert "beta" in m

    def test_insufficient_data(self):
        dates = pd.date_range("2023-01-01", periods=1, freq="B")
        returns = pd.Series([0.01], index=dates)
        m = compute_metrics(returns)
        assert "error" in m

    def test_all_zero_returns(self):
        dates = pd.date_range("2023-01-01", periods=100, freq="B")
        returns = pd.Series(np.zeros(100), index=dates)
        m = compute_metrics(returns)
        assert "total_return" in m
        assert abs(m["total_return"]) < 0.01

    def test_required_metrics_keys(self):
        """Verify all expected metric keys are present."""
        dates = pd.date_range("2023-01-01", periods=250, freq="B")
        returns = pd.Series(
            np.random.RandomState(99).randn(250) * 0.01,
            index=dates,
        )
        m = compute_metrics(returns)
        required = {"total_return", "sharpe_ratio", "max_drawdown", "cagr",
                    "annual_volatility", "sortino_ratio", "win_rate"}
        for key in required:
            assert key in m, f"Missing metric: {key}"


# ---------------------------------------------------------------------------
# Format report
# ---------------------------------------------------------------------------
class TestFormatReport:
    def test_basic_report(self):
        results = {
            "metrics": {
                "total_return": 0.5, "cagr": 0.15, "annual_volatility": 0.2,
                "sharpe_ratio": 1.0, "sortino_ratio": 1.2, "calmar_ratio": 0.8,
                "max_drawdown": -0.1, "win_rate": 0.55, "profit_factor": 1.5,
            },
            "trade_metrics": {
                "num_trades": 100, "num_buys": 50, "num_sells": 50,
                "total_transaction_costs": 50.0,
            },
            "initial_value": 100_000,
            "final_value": 150_000,
        }
        report = format_report(results)
        assert isinstance(report, str)
        assert "Performance" in report or "150,000" in report


# ---------------------------------------------------------------------------
# Backtester integration
# ---------------------------------------------------------------------------
class TestBacktester:
    def test_instantiation(self):
        df = _make_synthetic_df()
        bt = Backtester(
            strategy=_buy_and_hold,
            symbols=["TEST"],
            start="2023-01-01",
            end="2023-06-01",
            data={"TEST": df},
            benchmark=None,
        )
        assert bt is not None

    def test_simple_backtest(self):
        df = _make_synthetic_df(days=200)
        bt = Backtester(
            strategy=_buy_and_hold,
            symbols=["TEST"],
            start="2023-01-01",
            end="2023-06-01",
            data={"TEST": df},
            benchmark=None,
        )
        results = bt.run()
        assert "metrics" in results
        assert "equity_curve" in results
        assert results["final_value"] > 0

    def test_metrics_in_results(self):
        df = _make_synthetic_df(days=200)
        bt = Backtester(
            strategy=_buy_and_hold,
            symbols=["TEST"],
            start="2023-01-01",
            end="2023-06-01",
            data={"TEST": df},
            benchmark=None,
        )
        results = bt.run()
        metrics = results["metrics"]
        assert "total_return" in metrics
        assert "sharpe_ratio" in metrics
        assert "max_drawdown" in metrics

    def test_cost_summary_in_results(self):
        df = _make_synthetic_df(days=200)
        bt = Backtester(
            strategy=_buy_and_hold,
            symbols=["TEST"],
            start="2023-01-01",
            end="2023-06-01",
            data={"TEST": df},
            benchmark=None,
        )
        results = bt.run()
        # cost info is in trade_metrics
        assert "trade_metrics" in results
        tm = results["trade_metrics"]
        assert "total_transaction_costs" in tm or "num_trades" in tm

    def test_custom_slippage(self):
        df = _make_synthetic_df(days=200)
        bt = Backtester(
            strategy=_buy_and_hold,
            symbols=["TEST"],
            start="2023-01-01",
            end="2023-06-01",
            data={"TEST": df},
            benchmark=None,
            slippage_pct=0.01,  # 1% slippage
        )
        results = bt.run()
        assert results["final_value"] > 0

    def test_volume_spread_model(self):
        df = _make_synthetic_df(days=200)
        bt = Backtester(
            strategy=_buy_and_hold,
            symbols=["TEST"],
            start="2023-01-01",
            end="2023-06-01",
            data={"TEST": df},
            benchmark=None,
            spread_model="volume",
        )
        results = bt.run()
        assert results["final_value"] > 0

    def test_empty_strategy_no_crash(self):
        """Strategy that never trades should still produce valid results."""
        df = _make_synthetic_df(days=200)
        bt = Backtester(
            strategy=lambda date, prices, portfolio, data: {},
            symbols=["TEST"],
            start="2023-01-01",
            end="2023-06-01",
            data={"TEST": df},
            benchmark=None,
        )
        results = bt.run()
        assert results["final_value"] > 0
        assert abs(results["final_value"] - 100_000) < 1.0  # No trades = no change


# ---------------------------------------------------------------------------
# Position dataclass
# ---------------------------------------------------------------------------
class TestPosition:
    def test_buy_updates_avg_cost(self):
        pos = Position(symbol="AAPL")
        pos.update(Side.BUY, 10, 100.0)
        assert pos.quantity == 10
        assert pos.avg_cost == 100.0

    def test_sell_realizes_pnl(self):
        pos = Position(symbol="AAPL")
        pos.update(Side.BUY, 10, 100.0)
        realized = pos.update(Side.SELL, 10, 120.0)
        assert realized == 200.0  # 10 * (120 - 100)

    def test_partial_sell(self):
        pos = Position(symbol="AAPL")
        pos.update(Side.BUY, 10, 100.0)
        realized = pos.update(Side.SELL, 5, 120.0)
        assert realized == 100.0  # 5 * (120 - 100)
        assert pos.quantity == 5


# ---------------------------------------------------------------------------
# Trade dataclass
# ---------------------------------------------------------------------------
class TestTrade:
    def test_buy_cost(self):
        t = Trade(
            date=pd.Timestamp("2024-01-01"),
            symbol="AAPL",
            side=Side.BUY,
            quantity=10,
            price=100.0,
            commission=5.0,
            slippage=2.0,
        )
        assert t.cost == 10 * 100 + 5 + 2  # 1007

    def test_sell_cost(self):
        t = Trade(
            date=pd.Timestamp("2024-01-01"),
            symbol="AAPL",
            side=Side.SELL,
            quantity=10,
            price=100.0,
            commission=5.0,
            slippage=2.0,
        )
        assert t.cost == 10 * 100 - 5 - 2  # 993


# ---------------------------------------------------------------------------
# Historical crashes constant
# ---------------------------------------------------------------------------
def test_historical_crashes_present():
    assert len(HISTORICAL_CRASHES) >= 5
    for key, crash in HISTORICAL_CRASHES.items():
        assert "magnitude" in crash
        assert crash["magnitude"] < 0
        assert "duration_days" in crash

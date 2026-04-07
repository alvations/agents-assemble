"""Tests for backtester engine. Run with: python -m pytest tests/"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from backtester import Backtester, Portfolio, Trade, Side, compute_metrics, format_report


def test_portfolio_buy_sell():
    p = Portfolio(initial_cash=10000, cash=10000)
    p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 10, 100.0)
    assert p.cash < 10000
    pos = p.get_position("AAPL")
    assert pos is not None
    assert pos.quantity == 10
    p.execute_trade(pd.Timestamp("2024-01-02"), "AAPL", Side.SELL, 10, 110.0)
    pos2 = p.get_position("AAPL")
    assert pos2 is None or pos2.quantity == 0


def test_portfolio_total_value():
    p = Portfolio(initial_cash=10000, cash=10000)
    p.execute_trade(pd.Timestamp("2024-01-01"), "AAPL", Side.BUY, 10, 100.0)
    value = p.total_value({"AAPL": 110.0})
    assert value > 10000  # Should have gained


def test_compute_metrics_basic():
    returns = pd.Series([0.01, -0.005, 0.02, -0.01, 0.015] * 50)
    m = compute_metrics(returns)
    assert "total_return" in m
    assert "sharpe_ratio" in m
    assert "max_drawdown" in m
    assert m["max_drawdown"] <= 0


def test_compute_metrics_with_benchmark():
    returns = pd.Series([0.01, -0.005, 0.02] * 100)
    bench = pd.Series([0.005, 0.003, -0.002] * 100)
    m = compute_metrics(returns, bench)
    assert "alpha" in m
    assert "beta" in m


def test_format_report():
    results = {
        "metrics": {"total_return": 0.5, "cagr": 0.15, "annual_volatility": 0.2,
                     "sharpe_ratio": 1.0, "sortino_ratio": 1.2, "calmar_ratio": 0.8,
                     "max_drawdown": -0.1, "win_rate": 0.55, "profit_factor": 1.5},
        "trade_metrics": {"num_trades": 100, "num_buys": 50, "num_sells": 50,
                          "total_transaction_costs": 50.0},
        "initial_value": 100000,
        "final_value": 150000,
    }
    report = format_report(results)
    assert "Performance" in report
    assert "150,000" in report


def test_backtester_simple():
    """Test backtester with synthetic data."""
    dates = pd.date_range("2023-01-01", periods=100, freq="B")
    prices = 100 + np.cumsum(np.random.randn(100) * 0.5)
    df = pd.DataFrame({
        "Open": prices, "High": prices + 1, "Low": prices - 1,
        "Close": prices, "Volume": np.random.randint(1e6, 1e7, 100),
    }, index=dates)

    def buy_and_hold(date, prices_dict, portfolio, data):
        if not portfolio.get_position("TEST"):
            return {"TEST": 0.90}
        return {}

    bt = Backtester(
        strategy=buy_and_hold,
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


if __name__ == "__main__":
    test_portfolio_buy_sell()
    test_portfolio_total_value()
    test_compute_metrics_basic()
    test_compute_metrics_with_benchmark()
    test_format_report()
    test_backtester_simple()
    print("All backtester tests passed!")

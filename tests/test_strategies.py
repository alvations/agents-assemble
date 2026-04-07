"""Tests for all strategies. Run with: python -m pytest tests/"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pandas as pd
import numpy as np
from personas import ALL_PERSONAS, get_persona
from famous_investors import FAMOUS_INVESTORS, get_famous_investor
from theme_strategies import THEME_STRATEGIES, get_theme_strategy
from recession_strategies import RECESSION_STRATEGIES, get_recession_strategy
from unconventional_strategies import UNCONVENTIONAL_STRATEGIES, get_unconventional_strategy
from research_strategies import RESEARCH_STRATEGIES, get_research_strategy
from math_strategies import MATH_STRATEGIES, get_math_strategy
from hedge_fund_strategies import HEDGE_FUND_STRATEGIES, get_hedge_fund_strategy


def _make_mock_data(symbols, days=300):
    """Create synthetic price data for testing strategies without network calls."""
    dates = pd.date_range("2023-01-01", periods=days, freq="B")
    data = {}
    prices_today = {}
    for sym in symbols:
        base = 100 + hash(sym) % 100
        close = base + np.cumsum(np.random.RandomState(hash(sym) % 2**31).randn(days) * 0.5)
        close = np.maximum(close, 1)  # No negative prices
        df = pd.DataFrame({
            "Open": close * 0.999, "High": close * 1.01,
            "Low": close * 0.99, "Close": close,
            "Volume": np.random.randint(1e6, 1e7, days),
        }, index=dates)
        # Add indicators
        df["sma_20"] = df["Close"].rolling(20).mean()
        df["sma_50"] = df["Close"].rolling(50).mean()
        df["sma_200"] = df["Close"].rolling(200).mean()
        df["ema_12"] = df["Close"].ewm(span=12).mean()
        df["ema_26"] = df["Close"].ewm(span=26).mean()
        df["macd"] = df["ema_12"] - df["ema_26"]
        df["macd_signal"] = df["macd"].ewm(span=9).mean()
        delta = df["Close"].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss.replace(0, np.nan)
        df["rsi_14"] = 100 - (100 / (1 + rs))
        sma20 = df["Close"].rolling(20).mean()
        std20 = df["Close"].rolling(20).std()
        df["bb_upper"] = sma20 + 2 * std20
        df["bb_lower"] = sma20 - 2 * std20
        tr = pd.concat([df["High"] - df["Low"],
                         (df["High"] - df["Close"].shift(1)).abs(),
                         (df["Low"] - df["Close"].shift(1)).abs()], axis=1).max(axis=1)
        df["atr_14"] = tr.rolling(14).mean()
        df["daily_return"] = df["Close"].pct_change()
        df["vol_20"] = df["daily_return"].rolling(20).std()
        df["volume_sma_20"] = df["Volume"].rolling(20).mean()
        data[sym] = df
        prices_today[sym] = float(close[-1])
    return data, prices_today, dates[-1]


def _get_all_registries():
    return [
        ("generic", ALL_PERSONAS, get_persona),
        ("famous", FAMOUS_INVESTORS, get_famous_investor),
        ("theme", THEME_STRATEGIES, get_theme_strategy),
        ("recession", RECESSION_STRATEGIES, get_recession_strategy),
        ("unconventional", UNCONVENTIONAL_STRATEGIES, get_unconventional_strategy),
        ("research", RESEARCH_STRATEGIES, get_research_strategy),
        ("math", MATH_STRATEGIES, get_math_strategy),
        ("hedge_fund", HEDGE_FUND_STRATEGIES, get_hedge_fund_strategy),
    ]


def test_all_strategies_instantiate():
    """Every strategy can be created with valid config."""
    for cat, registry, getter in _get_all_registries():
        for key in registry:
            persona = getter(key)
            assert persona.config.name, f"{cat}/{key} has no name"
            assert persona.config.universe, f"{cat}/{key} has empty universe"
            assert persona.config.max_positions > 0
            assert 0 < persona.config.max_position_size <= 1


def test_all_strategies_generate_signals():
    """Every strategy can generate signals without crashing."""
    from backtester import Portfolio
    portfolio = Portfolio(initial_cash=100000, cash=100000)

    for cat, registry, getter in _get_all_registries():
        for key in registry:
            persona = getter(key)
            symbols = persona.config.universe[:10]  # Limit for speed
            data, prices, date = _make_mock_data(symbols)
            try:
                weights = persona.generate_signals(date, prices, portfolio, data)
                assert isinstance(weights, dict), f"{cat}/{key} returned {type(weights)}"
                for sym, w in weights.items():
                    assert isinstance(w, (int, float)), f"{cat}/{key} weight for {sym} is {type(w)}"
            except Exception as e:
                raise AssertionError(f"{cat}/{key} crashed: {e}")


def test_strategy_weights_reasonable():
    """Strategy weights should be between 0 and 1."""
    from backtester import Portfolio
    portfolio = Portfolio(initial_cash=100000, cash=100000)

    for cat, registry, getter in _get_all_registries():
        for key in registry:
            persona = getter(key)
            symbols = persona.config.universe[:10]
            data, prices, date = _make_mock_data(symbols)
            weights = persona.generate_signals(date, prices, portfolio, data)
            for sym, w in weights.items():
                assert -0.01 <= w <= 1.01, f"{cat}/{key}: {sym} weight {w} out of range"


if __name__ == "__main__":
    print("Testing strategy instantiation...")
    test_all_strategies_instantiate()
    print(f"  PASS: all strategies instantiate")

    print("Testing signal generation...")
    test_all_strategies_generate_signals()
    print(f"  PASS: all strategies generate valid signals")

    print("Testing weight ranges...")
    test_strategy_weights_reasonable()
    print(f"  PASS: all weights in valid range")

    print("\nAll strategy tests passed!")

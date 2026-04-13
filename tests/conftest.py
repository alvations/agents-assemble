"""Shared fixtures for agents-assemble test suite."""
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import pytest

# Ensure the project root is on sys.path so flat imports work
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# Strategy registry helpers
# ---------------------------------------------------------------------------
ALL_STRATEGY_MODULES = [
    ("personas", "ALL_PERSONAS", "get_persona"),
    ("famous_investors", "FAMOUS_INVESTORS", "get_famous_investor"),
    ("theme_strategies", "THEME_STRATEGIES", "get_theme_strategy"),
    ("recession_strategies", "RECESSION_STRATEGIES", "get_recession_strategy"),
    ("unconventional_strategies", "UNCONVENTIONAL_STRATEGIES", "get_unconventional_strategy"),
    ("research_strategies", "RESEARCH_STRATEGIES", "get_research_strategy"),
    ("math_strategies", "MATH_STRATEGIES", "get_math_strategy"),
    ("hedge_fund_strategies", "HEDGE_FUND_STRATEGIES", "get_hedge_fund_strategy"),
    ("news_event_strategies", "NEWS_EVENT_STRATEGIES", "get_news_event_strategy"),
    ("political_strategies", "POLITICAL_STRATEGIES", "get_political_strategy"),
    ("portfolio_strategies", "PORTFOLIO_STRATEGIES", "get_portfolio_strategy"),
    ("crisis_commodity_strategies", "CRISIS_COMMODITY_STRATEGIES", "get_crisis_commodity_strategy"),
    ("williams_seasonal_strategies", "WILLIAMS_SEASONAL_STRATEGIES", "get_williams_seasonal_strategy"),
    ("gap_strategies", "GAP_STRATEGIES", "get_gap_strategy"),
    ("strategy_orchestrator", "ORCHESTRATOR_STRATEGIES", "get_orchestrated_strategy"),
]


def _load_all_registries():
    """Load all strategy registries. Returns list of (category, registry_dict, getter_fn)."""
    results = []
    for mod_name, reg_attr, getter_attr in ALL_STRATEGY_MODULES:
        mod = __import__(mod_name)
        registry = getattr(mod, reg_attr)
        getter = getattr(mod, getter_attr)
        results.append((mod_name, registry, getter))
    return results


@pytest.fixture(scope="session")
def all_registries():
    """All strategy registries loaded once per test session."""
    return _load_all_registries()


# ---------------------------------------------------------------------------
# Synthetic market data
# ---------------------------------------------------------------------------
def make_mock_data(symbols, days=300, seed=42):
    """Create synthetic OHLCV + indicators for testing without network calls."""
    dates = pd.date_range("2023-01-01", periods=days, freq="B")
    data = {}
    prices_today = {}
    for sym in symbols:
        rng = np.random.RandomState(hash(sym) % 2**31 + seed)
        base = 100 + hash(sym) % 100
        close = base + np.cumsum(rng.randn(days) * 0.5)
        close = np.maximum(close, 1.0)
        df = pd.DataFrame({
            "Open": close * 0.999,
            "High": close * 1.01,
            "Low": close * 0.99,
            "Close": close,
            "Volume": rng.randint(1_000_000, 10_000_000, days),
        }, index=dates)
        # Technical indicators that strategies expect
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
        tr = pd.concat([
            df["High"] - df["Low"],
            (df["High"] - df["Close"].shift(1)).abs(),
            (df["Low"] - df["Close"].shift(1)).abs(),
        ], axis=1).max(axis=1)
        df["atr_14"] = tr.rolling(14).mean()
        df["daily_return"] = df["Close"].pct_change()
        df["vol_20"] = df["daily_return"].rolling(20).std()
        df["volume_sma_20"] = df["Volume"].rolling(20).mean()
        data[sym] = df
        prices_today[sym] = float(close[-1])
    return data, prices_today, dates[-1]


@pytest.fixture(scope="session")
def mock_market_data():
    """Session-scoped synthetic data for common tickers."""
    symbols = ["AAPL", "MSFT", "GOOGL", "NVDA", "SPY", "QQQ", "TLT", "GLD"]
    return make_mock_data(symbols)


@pytest.fixture
def mock_portfolio():
    """Fresh portfolio for each test."""
    from backtester import Portfolio
    return Portfolio(initial_cash=100_000, cash=100_000)


# ---------------------------------------------------------------------------
# Flask test client
# ---------------------------------------------------------------------------
@pytest.fixture(scope="session")
def flask_client():
    """Flask test client with mocked external dependencies."""
    import app as flask_app
    flask_app.app.testing = True
    return flask_app.app.test_client()


# ---------------------------------------------------------------------------
# yfinance mock
# ---------------------------------------------------------------------------
def make_yf_ticker_mock(symbol="AAPL"):
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

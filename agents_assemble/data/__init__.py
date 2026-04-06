"""Data fetching and market data access."""
from agents_assemble.data.fetcher import (
    fetch_ohlcv, fetch_multiple_ohlcv, fetch_fundamentals,
    fetch_fred_series, fetch_yield_curve, get_universe, UNIVERSE,
    scan_52_week_lows, scan_volatile_stocks,
    fetch_dividends, fetch_earnings, fetch_options_chain,
    fetch_sector_performance, fetch_market_breadth,
    summarize_api_keys,
)

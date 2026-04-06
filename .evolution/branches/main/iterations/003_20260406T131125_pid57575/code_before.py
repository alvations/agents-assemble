"""Market data fetching module for agents-assemble.

Provides unified access to free and premium market data sources for
stocks, ETFs, bonds, and other publicly tradable instruments on
Robinhood/Public.com.

Free sources: yfinance (OHLCV, fundamentals), FRED (macro/bonds)
Premium sources (API key required): Alpha Vantage, Polygon.io, Quandl,
    IEX Cloud, Finnhub, News API
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import requests

# ---------------------------------------------------------------------------
# Cache setup
# ---------------------------------------------------------------------------
CACHE_DIR = Path(__file__).parent / ".cache"
CACHE_DIR.mkdir(exist_ok=True)

# ---------------------------------------------------------------------------
# API key registry — users set these as env vars
# ---------------------------------------------------------------------------
API_KEYS = {
    "ALPHA_VANTAGE_KEY": {
        "desc": "Alpha Vantage — real-time quotes, fundamentals, forex, crypto",
        "url": "https://www.alphavantage.co/support/#api-key",
        "free_tier": "5 calls/min, 500 calls/day",
    },
    "POLYGON_API_KEY": {
        "desc": "Polygon.io — tick-level data, options, forex",
        "url": "https://polygon.io/pricing",
        "free_tier": "5 calls/min, delayed data",
    },
    "QUANDL_API_KEY": {
        "desc": "Nasdaq Data Link (Quandl) — alternative data, futures, economics",
        "url": "https://data.nasdaq.com/sign-up",
        "free_tier": "50 calls/day for free datasets",
    },
    "IEX_CLOUD_KEY": {
        "desc": "IEX Cloud — real-time US equity data, stats, earnings",
        "url": "https://iexcloud.io/pricing/",
        "free_tier": "Deprecated free tier, pay-as-you-go now",
    },
    "FINNHUB_API_KEY": {
        "desc": "Finnhub — real-time stock prices, news, social sentiment",
        "url": "https://finnhub.io/register",
        "free_tier": "60 calls/min",
    },
    "NEWS_API_KEY": {
        "desc": "NewsAPI — financial news headlines for sentiment analysis",
        "url": "https://newsapi.org/register",
        "free_tier": "100 requests/day, 1 month old articles",
    },
    "FRED_API_KEY": {
        "desc": "FRED (Federal Reserve) — macro data, yield curves, rates",
        "url": "https://fred.stlouisfed.org/docs/api/api_key.html",
        "free_tier": "Unlimited (free registration required)",
    },
}


def get_api_key(name: str) -> Optional[str]:
    """Get API key from environment."""
    return os.environ.get(name)


def summarize_api_keys() -> str:
    """Print summary of all API keys and their status."""
    lines = ["=== API Key Status ==="]
    for key, info in API_KEYS.items():
        status = "SET" if get_api_key(key) else "NOT SET"
        lines.append(f"\n{key}: [{status}]")
        lines.append(f"  {info['desc']}")
        lines.append(f"  Free tier: {info['free_tier']}")
        lines.append(f"  Get key: {info['url']}")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Caching helpers
# ---------------------------------------------------------------------------
def _cache_path(key: str) -> Path:
    safe = key.replace("/", "_").replace(":", "_").replace(" ", "_")
    return CACHE_DIR / f"{safe}.parquet"


def _cache_get(key: str, max_age_hours: float = 12) -> Optional[pd.DataFrame]:
    path = _cache_path(key)
    if path.exists():
        age = time.time() - path.stat().st_mtime
        if age < max_age_hours * 3600:
            try:
                return pd.read_parquet(path)
            except Exception:
                pass
    return None


def _cache_set(key: str, df: pd.DataFrame) -> None:
    try:
        df.to_parquet(_cache_path(key))
    except Exception:
        pass


# ---------------------------------------------------------------------------
# FREE DATA: yfinance
# ---------------------------------------------------------------------------
def fetch_ohlcv(
    symbol: str,
    start: str = "2020-01-01",
    end: Optional[str] = None,
    interval: str = "1d",
    cache: bool = True,
) -> pd.DataFrame:
    """Fetch OHLCV data for a stock/ETF/index via yfinance.

    Args:
        symbol: Ticker symbol (e.g., 'AAPL', 'SPY', 'BND')
        start: Start date 'YYYY-MM-DD'
        end: End date (default: today)
        interval: '1d', '1wk', '1mo', '5m', '15m', '1h'
        cache: Use local cache

    Returns:
        DataFrame with columns: Open, High, Low, Close, Volume, Adj Close
    """
    import yfinance as yf

    end = end or datetime.now().strftime("%Y-%m-%d")
    cache_key = f"ohlcv_{symbol}_{start}_{end}_{interval}"

    if cache:
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start, end=end, interval=interval)

    if df.empty:
        raise ValueError(f"No data returned for {symbol}")

    if cache:
        _cache_set(cache_key, df)

    return df


def fetch_multiple_ohlcv(
    symbols: List[str],
    start: str = "2020-01-01",
    end: Optional[str] = None,
    interval: str = "1d",
) -> Dict[str, pd.DataFrame]:
    """Fetch OHLCV for multiple symbols. Falls back to individual downloads on failure."""
    import yfinance as yf

    end = end or datetime.now().strftime("%Y-%m-%d")
    results = {}

    # Check cache first to avoid unnecessary network calls
    uncached = []
    for sym in symbols:
        cache_key = f"ohlcv_{sym}_{start}_{end}_{interval}"
        cached = _cache_get(cache_key)
        if cached is not None:
            results[sym] = cached
        else:
            uncached.append(sym)

    if not uncached:
        return results

    # Try batch download for uncached symbols
    try:
        data = yf.download(uncached, start=start, end=end, interval=interval, group_by="ticker")
        if len(uncached) == 1:
            if not data.empty:
                results[uncached[0]] = data
                _cache_set(f"ohlcv_{uncached[0]}_{start}_{end}_{interval}", data)
        else:
            for sym in uncached:
                try:
                    df = data[sym].dropna(how="all")
                    if not df.empty:
                        results[sym] = df
                        _cache_set(f"ohlcv_{sym}_{start}_{end}_{interval}", df)
                except (KeyError, AttributeError):
                    pass
    except Exception:
        pass

    # Fallback: individually fetch any symbols still missing after batch
    missing = [s for s in uncached if s not in results]
    for sym in missing:
        try:
            df = fetch_ohlcv(sym, start=start, end=end, interval=interval, cache=True)
            if not df.empty:
                results[sym] = df
        except Exception:
            pass

    return results


def fetch_fundamentals(symbol: str) -> Dict[str, Any]:
    """Fetch fundamental data for a stock via yfinance.

    Returns dict with: pe_ratio, pb_ratio, dividend_yield, market_cap,
    revenue, earnings, debt_to_equity, roe, free_cash_flow, etc.
    """
    import yfinance as yf

    ticker = yf.Ticker(symbol)
    info = ticker.info

    return {
        "symbol": symbol,
        "name": info.get("longName", ""),
        "sector": info.get("sector", ""),
        "industry": info.get("industry", ""),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "forward_pe": info.get("forwardPE"),
        "pb_ratio": info.get("priceToBook"),
        "ps_ratio": info.get("priceToSalesTrailing12Months"),
        "dividend_yield": info.get("dividendYield"),
        "payout_ratio": info.get("payoutRatio"),
        "debt_to_equity": info.get("debtToEquity"),
        "roe": info.get("returnOnEquity"),
        "roa": info.get("returnOnAssets"),
        "revenue": info.get("totalRevenue"),
        "earnings": info.get("netIncomeToCommon"),
        "free_cash_flow": info.get("freeCashflow"),
        "operating_margins": info.get("operatingMargins"),
        "profit_margins": info.get("profitMargins"),
        "beta": info.get("beta"),
        "52w_high": info.get("fiftyTwoWeekHigh"),
        "52w_low": info.get("fiftyTwoWeekLow"),
        "50d_avg": info.get("fiftyDayAverage"),
        "200d_avg": info.get("twoHundredDayAverage"),
        "avg_volume": info.get("averageVolume"),
        "shares_outstanding": info.get("sharesOutstanding"),
        "institutional_holders_pct": info.get("heldPercentInstitutions"),
    }


def fetch_earnings(symbol: str) -> pd.DataFrame:
    """Fetch quarterly earnings history."""
    import yfinance as yf

    ticker = yf.Ticker(symbol)
    return ticker.quarterly_earnings


def fetch_dividends(symbol: str) -> pd.Series:
    """Fetch dividend history."""
    import yfinance as yf

    ticker = yf.Ticker(symbol)
    return ticker.dividends


def fetch_options_chain(symbol: str, expiry: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    """Fetch options chain (calls and puts)."""
    import yfinance as yf

    ticker = yf.Ticker(symbol)
    if expiry:
        chain = ticker.option_chain(expiry)
    else:
        expirations = ticker.options
        if not expirations:
            return {"calls": pd.DataFrame(), "puts": pd.DataFrame()}
        chain = ticker.option_chain(expirations[0])

    return {"calls": chain.calls, "puts": chain.puts}


# ---------------------------------------------------------------------------
# FREE DATA: FRED (Federal Reserve Economic Data)
# ---------------------------------------------------------------------------
FRED_BASE = "https://api.stlouisfed.org/fred"

# Key FRED series for trading
FRED_SERIES = {
    "DGS10": "10-Year Treasury Yield",
    "DGS2": "2-Year Treasury Yield",
    "DGS30": "30-Year Treasury Yield",
    "DGS5": "5-Year Treasury Yield",
    "FEDFUNDS": "Federal Funds Rate",
    "T10Y2Y": "10Y-2Y Treasury Spread (yield curve)",
    "T10Y3M": "10Y-3M Treasury Spread",
    "VIXCLS": "VIX (CBOE Volatility Index)",
    "DTWEXBGS": "Trade-Weighted Dollar Index",
    "CPIAUCSL": "CPI (inflation)",
    "UNRATE": "Unemployment Rate",
    "GDP": "Gross Domestic Product",
    "UMCSENT": "Consumer Sentiment",
    "BAMLH0A0HYM2": "High Yield Bond Spread (ICE BofA)",
    "BAMLC0A4CBBB": "BBB Corporate Bond Spread",
    "MORTGAGE30US": "30-Year Mortgage Rate",
}


def fetch_fred_series(
    series_id: str,
    start: str = "2020-01-01",
    end: Optional[str] = None,
    api_key: Optional[str] = None,
    cache: bool = True,
) -> pd.DataFrame:
    """Fetch a FRED series. Works without API key for basic access.

    Returns DataFrame with 'date' index and 'value' column.
    """
    api_key = api_key or get_api_key("FRED_API_KEY")

    end = end or datetime.now().strftime("%Y-%m-%d")
    cache_key = f"fred_{series_id}_{start}_{end}"

    if cache:
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

    if api_key:
        url = f"{FRED_BASE}/series/observations"
        params = {
            "series_id": series_id,
            "api_key": api_key,
            "file_type": "json",
            "observation_start": start,
            "observation_end": end,
        }
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()["observations"]
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df[["date", "value"]].dropna().set_index("date")
    else:
        # Fallback: scrape FRED CSV (no key needed)
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={start}&coed={end}"
        try:
            df = pd.read_csv(url, parse_dates=["DATE"], index_col="DATE")
            df.index.name = "date"
            df.columns = ["value"]
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df.dropna()
        except Exception:
            raise ValueError(f"Could not fetch FRED series {series_id}. Set FRED_API_KEY for reliable access.")

    if cache:
        _cache_set(cache_key, df)
    return df


def fetch_yield_curve(date: Optional[str] = None) -> Dict[str, float]:
    """Fetch US Treasury yield curve for a given date."""
    maturities = {"DGS1MO": "1M", "DGS3MO": "3M", "DGS6MO": "6M",
                  "DGS1": "1Y", "DGS2": "2Y", "DGS3": "3Y", "DGS5": "5Y",
                  "DGS7": "7Y", "DGS10": "10Y", "DGS20": "20Y", "DGS30": "30Y"}

    curve = {}
    if date:
        dt = datetime.strptime(date, "%Y-%m-%d")
        start = (dt - timedelta(days=365)).strftime("%Y-%m-%d")
    else:
        start = "2024-01-01"
    for series_id, label in maturities.items():
        try:
            df = fetch_fred_series(series_id, start=start)
            if not df.empty:
                if date:
                    idx = pd.to_datetime(date)
                    nearest = df.index[df.index.get_indexer([idx], method="nearest")[0]]
                    curve[label] = float(df.loc[nearest, "value"])
                else:
                    curve[label] = float(df.iloc[-1]["value"])
        except Exception:
            pass

    return curve


# ---------------------------------------------------------------------------
# PREMIUM DATA: Alpha Vantage
# ---------------------------------------------------------------------------
def fetch_alpha_vantage(
    symbol: str,
    function: str = "TIME_SERIES_DAILY_ADJUSTED",
    outputsize: str = "full",
) -> pd.DataFrame:
    """Fetch data from Alpha Vantage (requires ALPHA_VANTAGE_KEY)."""
    key = get_api_key("ALPHA_VANTAGE_KEY")
    if not key:
        raise ValueError("Set ALPHA_VANTAGE_KEY env var. Get free key: https://www.alphavantage.co/support/#api-key")

    url = "https://www.alphavantage.co/query"
    params = {"function": function, "symbol": symbol, "apikey": key, "outputsize": outputsize}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    # Parse time series data
    ts_key = [k for k in data.keys() if "Time Series" in k]
    if not ts_key:
        raise ValueError(f"Unexpected response: {list(data.keys())}")

    ts = data[ts_key[0]]
    df = pd.DataFrame.from_dict(ts, orient="index")
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


# ---------------------------------------------------------------------------
# PREMIUM DATA: Polygon.io
# ---------------------------------------------------------------------------
def fetch_polygon_bars(
    symbol: str,
    start: str = "2020-01-01",
    end: Optional[str] = None,
    timespan: str = "day",
) -> pd.DataFrame:
    """Fetch bars from Polygon.io (requires POLYGON_API_KEY)."""
    key = get_api_key("POLYGON_API_KEY")
    if not key:
        raise ValueError("Set POLYGON_API_KEY env var. Get key: https://polygon.io/pricing")

    end = end or datetime.now().strftime("%Y-%m-%d")
    url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/{timespan}/{start}/{end}"
    params = {"apiKey": key, "limit": 50000, "sort": "asc"}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    if "results" not in data:
        raise ValueError(f"No results for {symbol}")

    df = pd.DataFrame(data["results"])
    df["date"] = pd.to_datetime(df["t"], unit="ms")
    df = df.rename(columns={"o": "Open", "h": "High", "l": "Low", "c": "Close", "v": "Volume"})
    df = df.set_index("date")[["Open", "High", "Low", "Close", "Volume"]]

    return df


# ---------------------------------------------------------------------------
# PREMIUM DATA: Finnhub (sentiment/news)
# ---------------------------------------------------------------------------
def fetch_finnhub_sentiment(symbol: str) -> Dict[str, Any]:
    """Fetch social sentiment from Finnhub (requires FINNHUB_API_KEY)."""
    key = get_api_key("FINNHUB_API_KEY")
    if not key:
        raise ValueError("Set FINNHUB_API_KEY env var. Get key: https://finnhub.io/register")

    url = "https://finnhub.io/api/v1/stock/social-sentiment"
    params = {"symbol": symbol, "token": key}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


def fetch_finnhub_news(
    symbol: str, from_date: Optional[str] = None, to_date: Optional[str] = None
) -> List[Dict]:
    """Fetch company news from Finnhub."""
    key = get_api_key("FINNHUB_API_KEY")
    if not key:
        raise ValueError("Set FINNHUB_API_KEY env var")

    to_date = to_date or datetime.now().strftime("%Y-%m-%d")
    from_date = from_date or (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")

    url = "https://finnhub.io/api/v1/company-news"
    params = {"symbol": symbol, "from": from_date, "to": to_date, "token": key}
    resp = requests.get(url, params=params, timeout=30)
    resp.raise_for_status()
    return resp.json()


# ---------------------------------------------------------------------------
# Screening / universe helpers
# ---------------------------------------------------------------------------
# Popular instruments available on Robinhood / Public.com
UNIVERSE = {
    "mega_cap": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "JPM", "V"],
    "growth": ["PLTR", "SNOW", "CRWD", "DDOG", "NET", "SHOP", "SQ", "ROKU", "ENPH", "MELI"],
    "value": ["BRK-B", "JPM", "JNJ", "PG", "KO", "PEP", "MRK", "CVX", "XOM", "IBM"],
    "dividend": ["JNJ", "PG", "KO", "PEP", "MMM", "T", "VZ", "MO", "ABBV", "O"],
    "meme": ["GME", "AMC", "BBBY", "BB", "PLTR", "SOFI", "WISH", "CLOV", "HOOD", "RIVN"],
    "etf_broad": ["SPY", "QQQ", "IWM", "DIA", "VTI", "VOO"],
    "etf_sector": ["XLF", "XLK", "XLE", "XLV", "XLI", "XLP", "XLU", "XLRE", "XLC", "XLB"],
    "etf_bond": ["BND", "TLT", "IEF", "SHY", "LQD", "HYG", "AGG", "TIP", "VCSH", "VCIT"],
    "etf_international": ["EEM", "VEA", "VWO", "EFA", "IEMG"],
    "crypto_adjacent": ["COIN", "MARA", "RIOT", "MSTR", "SQ"],
}


def get_universe(category: str = "mega_cap") -> List[str]:
    """Get a list of tickers for a given category."""
    return UNIVERSE.get(category, UNIVERSE["mega_cap"])


def screen_by_fundamentals(
    symbols: List[str],
    min_market_cap: Optional[float] = None,
    max_pe: Optional[float] = None,
    min_dividend_yield: Optional[float] = None,
    max_debt_to_equity: Optional[float] = None,
) -> List[Dict[str, Any]]:
    """Screen stocks by fundamental criteria."""
    results = []
    for sym in symbols:
        try:
            f = fetch_fundamentals(sym)
            if min_market_cap is not None and (f["market_cap"] or 0) < min_market_cap:
                continue
            if max_pe is not None and f["pe_ratio"] and f["pe_ratio"] > max_pe:
                continue
            if min_dividend_yield is not None and (f["dividend_yield"] or 0) < min_dividend_yield:
                continue
            if max_debt_to_equity is not None and f["debt_to_equity"] and f["debt_to_equity"] > max_debt_to_equity:
                continue
            results.append(f)
        except Exception:
            pass
    return results


# ---------------------------------------------------------------------------
# Convenience: multi-asset data bundle
# ---------------------------------------------------------------------------
def fetch_asset_bundle(
    symbols: List[str],
    start: str = "2020-01-01",
    end: Optional[str] = None,
    include_fundamentals: bool = False,
) -> Dict[str, Any]:
    """Fetch a complete data bundle for backtesting.

    Returns: {symbol: {"ohlcv": DataFrame, "fundamentals": dict (optional)}}
    """
    ohlcv_data = fetch_multiple_ohlcv(symbols, start=start, end=end)
    bundle = {}
    for sym in symbols:
        entry: Dict[str, Any] = {}
        if sym in ohlcv_data:
            entry["ohlcv"] = ohlcv_data[sym]
        if include_fundamentals:
            try:
                entry["fundamentals"] = fetch_fundamentals(sym)
            except Exception:
                entry["fundamentals"] = {}
        if entry:
            bundle[sym] = entry

    return bundle


if __name__ == "__main__":
    print(summarize_api_keys())
    print("\n=== Testing AAPL OHLCV fetch ===")
    df = fetch_ohlcv("AAPL", start="2024-01-01")
    print(f"Fetched {len(df)} rows for AAPL")
    print(df.tail())

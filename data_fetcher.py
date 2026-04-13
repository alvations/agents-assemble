"""Market data fetching module for agents-assemble.

Provides unified access to free and premium market data sources for
stocks, ETFs, bonds, and other publicly tradable instruments on
Robinhood/Public.com.

Free sources: yfinance (OHLCV, fundamentals), FRED (macro/bonds)
Premium sources (API key required): Alpha Vantage, Polygon.io, Quandl,
    IEX Cloud, Finnhub, News API
"""

from __future__ import annotations

import os
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import math

import pandas as pd
import requests

_SQRT_252 = math.sqrt(252)

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
    "NOAA_CDO_TOKEN": {
        "desc": "NOAA Climate Data Online — weather, temperature, precipitation",
        "url": "https://www.ncdc.noaa.gov/cdo-web/token",
        "free_tier": "5 req/sec, 10,000 req/day (free registration)",
    },
}


def get_api_key(name: str) -> str | None:
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


def _canonical_cache_path(symbol: str, interval: str = "1d") -> Path:
    """One file per ticker+interval — no date range in filename."""
    safe = symbol.replace("/", "_").replace(":", "_")
    return CACHE_DIR / f"ohlcv_{safe}_{interval}.parquet"


def _cache_get(key: str, max_age_hours: float = 12) -> pd.DataFrame | None:
    path = _cache_path(key)
    try:
        age = time.time() - path.stat().st_mtime
        if age < max_age_hours * 3600:
            return pd.read_parquet(path)
    except FileNotFoundError:
        return None
    except Exception:
        try:
            path.unlink()
        except OSError:
            pass
    return None


def _cache_set(key: str, df: pd.DataFrame) -> None:
    tmp = None
    try:
        CACHE_DIR.mkdir(exist_ok=True)
        path = _cache_path(key)
        tmp = path.with_suffix(".parquet.tmp")
        df.to_parquet(tmp)
        tmp.replace(path)  # atomic on POSIX
    except Exception:
        try:
            if tmp is not None:
                tmp.unlink(missing_ok=True)
        except Exception:
            pass


def _canonical_cache_read(symbol: str, interval: str = "1d") -> pd.DataFrame | None:
    """Read the canonical (one-per-ticker) cache file.

    Always returns tz-naive index so callers don't need to strip it.
    """
    path = _canonical_cache_path(symbol, interval)
    try:
        if path.exists():
            df = pd.read_parquet(path)
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)
            return df
    except Exception:
        try:
            path.unlink()
        except OSError:
            pass
    return None


def _canonical_cache_write(symbol: str, df: pd.DataFrame, interval: str = "1d") -> None:
    """Write/overwrite the canonical cache file for a ticker."""
    CACHE_DIR.mkdir(exist_ok=True)
    path = _canonical_cache_path(symbol, interval)
    tmp = path.with_suffix(".parquet.tmp")
    try:
        df.to_parquet(tmp)
        tmp.replace(path)
    except Exception:
        try:
            tmp.unlink(missing_ok=True)
        except Exception:
            pass


def migrate_cache() -> dict[str, int]:
    """Migrate old date-range cache files into canonical per-ticker files.

    Merges all ohlcv_{SYM}_{start}_{end}_{interval}.parquet files into
    one ohlcv_{SYM}_{interval}.parquet per ticker, then deletes the old files.
    Returns counts of files migrated and removed.
    """
    import re

    if not CACHE_DIR.exists():
        return {"migrated": 0, "removed": 0}

    # Find old-format files: ohlcv_SYM_YYYY-MM-DD_YYYY-MM-DD_1d.parquet
    old_pattern = re.compile(
        r"^ohlcv_(.+?)_(\d{4}-\d{2}-\d{2})_(\d{4}-\d{2}-\d{2})_(\w+)\.parquet$"
    )

    # Group old files by (symbol, interval)
    groups: dict[tuple[str, str], list[Path]] = {}
    for f in CACHE_DIR.iterdir():
        m = old_pattern.match(f.name)
        if m:
            sym, _, _, interval = m.groups()
            groups.setdefault((sym, interval), []).append(f)

    migrated = 0
    removed = 0
    for (sym, interval), files in groups.items():
        # Read and merge all old files for this ticker
        frames = []
        for f in files:
            try:
                df = pd.read_parquet(f)
                if df.index.tz is not None:
                    df.index = df.index.tz_localize(None)
                frames.append(df)
            except Exception:
                pass

        if frames:
            merged = pd.concat(frames)
            merged = merged[~merged.index.duplicated(keep="last")]
            merged = merged.sort_index()

            # Also merge with existing canonical file if present
            existing = _canonical_cache_read(sym, interval)
            if existing is not None and not existing.empty:
                merged = pd.concat([existing, merged])
                merged = merged[~merged.index.duplicated(keep="last")]
                merged = merged.sort_index()

            _canonical_cache_write(sym, merged, interval)
            migrated += 1

        # Remove old files
        for f in files:
            try:
                f.unlink()
                removed += 1
            except OSError:
                pass

    return {"migrated": migrated, "removed": removed}


def refresh_cache(max_age_days: int = 1) -> dict[str, int]:
    """Incrementally update all cached tickers that are older than max_age_days.

    Call daily (or weekly with max_age_days=7) to keep cache fresh.
    Only downloads missing days — not full re-download.

    Returns counts of tickers updated and skipped.
    """
    import re

    if not CACHE_DIR.exists():
        return {"updated": 0, "skipped": 0, "failed": 0}

    canonical = re.compile(r"^ohlcv_(.+?)_([\w]+)\.parquet$")
    old_format = re.compile(r"\d{4}-\d{2}-\d{2}")
    today = pd.Timestamp(datetime.now().strftime("%Y-%m-%d"))
    updated = 0
    skipped = 0
    failed = 0

    files = sorted(CACHE_DIR.iterdir())
    for f in files:
        m = canonical.match(f.name)
        if not m:
            continue
        sym, interval = m.groups()
        # Skip old-format files (ohlcv_SYM_YYYY-MM-DD_YYYY-MM-DD_interval)
        if old_format.search(sym):
            continue
        # Skip intraday
        if interval not in ("1d", "1wk", "1mo"):
            continue

        try:
            df = pd.read_parquet(f)
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)
            if df.empty:
                continue

            cached_max = df.index.max()
            if cached_max >= today - timedelta(days=max_age_days):
                skipped += 1
                continue

            # Fetch only missing days
            fetch_ohlcv(sym, start=df.index.min().strftime("%Y-%m-%d"), interval=interval, cache=True)
            updated += 1
        except Exception:
            failed += 1

    return {"updated": updated, "skipped": skipped, "failed": failed}


# ---------------------------------------------------------------------------
# FREE DATA: yfinance
# ---------------------------------------------------------------------------
def fetch_ohlcv(
    symbol: str,
    start: str = "2020-01-01",
    end: str | None = None,
    interval: str = "1d",
    cache: bool = True,
) -> pd.DataFrame:
    """Fetch OHLCV data for a stock/ETF/index via yfinance.

    Uses ONE canonical cache file per ticker+interval (no date range in key).
    On cache hit, checks if we need to fetch newer data and appends incrementally.
    Returns only the requested [start, end] slice.

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
    intraday = interval in ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h")

    # Intraday: use old per-request cache (short TTL, yfinance limits history)
    if intraday:
        cache_key = f"ohlcv_{symbol}_{start}_{end}_{interval}"
        if cache:
            cached = _cache_get(cache_key, max_age_hours=0.5)
            if cached is not None:
                return cached
        ticker = yf.Ticker(symbol)
        df = ticker.history(start=start, end=end, interval=interval)
        if df.empty:
            raise ValueError(f"No data returned for {symbol}")
        if "Close" in df.columns:
            df = df.dropna(subset=["Close"])
            if df.empty:
                raise ValueError(f"No valid price data for {symbol} (all Close values NaN)")
        if cache:
            _cache_set(cache_key, df)
        return df

    # Daily/weekly/monthly: canonical per-ticker cache with incremental updates
    req_start = pd.Timestamp(start)
    req_end = pd.Timestamp(end)
    cached_df = _canonical_cache_read(symbol, interval) if cache else None

    need_fetch = True
    fetch_start = start
    fetch_end = end

    if cached_df is not None and not cached_df.empty:
        cached_min = cached_df.index.min()
        cached_max = cached_df.index.max()
        today = pd.Timestamp(datetime.now().strftime("%Y-%m-%d"))

        # Check if cached data fully covers the request
        covers_start = cached_min <= req_start
        covers_end = cached_max >= req_end - timedelta(days=3)  # 3-day grace for weekends
        is_fresh = cached_max >= today - timedelta(days=1)  # Has yesterday's data

        if covers_start and covers_end:
            # Cache covers both start and end — no fetch needed for this range
            # Only fetch new data if cache is stale AND end is "today"
            if is_fresh or req_end <= cached_max:
                need_fetch = False
            else:
                # Cache covers range but we want newer data too
                new_start = (cached_max + timedelta(days=1)).strftime("%Y-%m-%d")
                new_end = today.strftime("%Y-%m-%d")
                if pd.Timestamp(new_start) < pd.Timestamp(new_end):
                    fetch_start = new_start
                    fetch_end = new_end
                else:
                    need_fetch = False
        elif covers_start and not covers_end:
            # Covers start but not end — fetch only the gap
            new_start = (cached_max + timedelta(days=1)).strftime("%Y-%m-%d")
            if pd.Timestamp(new_start) < req_end:
                fetch_start = new_start
                fetch_end = end
            else:
                # cached_max is past req_end — no fetch needed
                need_fetch = False
        elif not covers_start and covers_end:
            # Need earlier data only
            fetch_start = start
            fetch_end = (cached_min - timedelta(days=1)).strftime("%Y-%m-%d")
            if pd.Timestamp(fetch_start) >= pd.Timestamp(fetch_end):
                need_fetch = False
        else:
            # Need both earlier and newer — full refetch
            fetch_start = start
            fetch_end = end

    if need_fetch:
        try:
            ticker = yf.Ticker(symbol)
            df_new = ticker.history(start=fetch_start, end=fetch_end, interval=interval)
        except Exception:
            df_new = pd.DataFrame()

        if not df_new.empty:
            if df_new.index.tz is not None:
                df_new.index = df_new.index.tz_localize(None)
            if "Close" in df_new.columns:
                df_new = df_new.dropna(subset=["Close"])

        # Merge with cached data
        if cached_df is not None and not cached_df.empty and not df_new.empty:
            merged = pd.concat([cached_df, df_new])
            merged = merged[~merged.index.duplicated(keep="last")]
            merged = merged.sort_index()
            cached_df = merged
        elif not df_new.empty:
            cached_df = df_new
        # else: keep whatever cached_df we had (may be None)

        # Write merged data back to canonical cache (only if we got new data)
        if cache and not df_new.empty and cached_df is not None and not cached_df.empty:
            _canonical_cache_write(symbol, cached_df, interval)

    if cached_df is None or cached_df.empty:
        raise ValueError(f"No data returned for {symbol}")

    # Slice to requested range
    result = cached_df.loc[
        (cached_df.index >= req_start) & (cached_df.index <= req_end)
    ]

    if result.empty:
        raise ValueError(f"No data for {symbol} in range {start} to {end}")

    return result


def fetch_multiple_ohlcv(
    symbols: list[str],
    start: str = "2020-01-01",
    end: str | None = None,
    interval: str = "1d",
) -> dict[str, pd.DataFrame]:
    """Fetch OHLCV for multiple symbols using canonical per-ticker cache.

    Each symbol goes through fetch_ohlcv which handles incremental updates.
    For symbols with no cache at all, does a batch yf.download to save time.
    """
    import yfinance as yf

    end = end or datetime.now().strftime("%Y-%m-%d")
    intraday = interval in ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h")
    results = {}

    # For daily data: check which symbols already have fresh canonical cache
    need_any_fetch = []
    if not intraday:
        today = pd.Timestamp(datetime.now().strftime("%Y-%m-%d"))
        req_start = pd.Timestamp(start)
        req_end = pd.Timestamp(end)

        for sym in symbols:
            cached = _canonical_cache_read(sym, interval)
            if cached is not None and not cached.empty:
                cached_min = cached.index.min()
                cached_max = cached.index.max()
                covers_start = cached_min <= req_start
                is_fresh = cached_max >= today - timedelta(days=1)

                if covers_start and is_fresh:
                    # Slice and use directly — no fetch needed
                    sliced = cached.loc[
                        (cached.index >= req_start) & (cached.index <= req_end)
                    ]
                    if not sliced.empty:
                        results[sym] = sliced
                        continue

            need_any_fetch.append(sym)
    else:
        need_any_fetch = list(symbols)

    if not need_any_fetch:
        return results

    # Batch fetch uncached symbols — each goes through fetch_ohlcv
    # which handles canonical caching internally
    for sym in need_any_fetch:
        try:
            df = fetch_ohlcv(sym, start=start, end=end, interval=interval, cache=True)
            if not df.empty:
                results[sym] = df
        except Exception:
            pass

    return results


def fetch_fundamentals(symbol: str) -> dict[str, Any]:
    """Fetch fundamental data for a stock via yfinance.

    Returns dict with: pe_ratio, pb_ratio, dividend_yield, market_cap,
    revenue, earnings, debt_to_equity, roe, free_cash_flow, etc.
    """
    import yfinance as yf

    ticker = yf.Ticker(symbol)
    info = ticker.info

    result = {
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
    # yfinance .info can return NaN or Infinity for numeric fields;
    # sanitize to None so downstream `is not None` checks work correctly
    return {k: (None if isinstance(v, float) and not math.isfinite(v) else v)
            for k, v in result.items()}


def fetch_earnings(symbol: str) -> pd.DataFrame:
    """Fetch quarterly earnings history."""
    import yfinance as yf

    ticker = yf.Ticker(symbol)
    result = ticker.quarterly_earnings
    if result is None:
        return pd.DataFrame()
    return result


def fetch_dividends(symbol: str) -> pd.Series:
    """Fetch dividend history."""
    import yfinance as yf

    ticker = yf.Ticker(symbol)
    return ticker.dividends


def fetch_options_chain(symbol: str, expiry: str | None = None) -> dict[str, pd.DataFrame]:
    """Fetch options chain (calls and puts)."""
    import yfinance as yf

    empty = {"calls": pd.DataFrame(), "puts": pd.DataFrame()}
    try:
        ticker = yf.Ticker(symbol)
        if expiry:
            chain = ticker.option_chain(expiry)
        else:
            expirations = ticker.options
            if not expirations:
                return empty
            chain = ticker.option_chain(expirations[0])
        return {"calls": chain.calls, "puts": chain.puts}
    except Exception:
        return empty


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
    end: str | None = None,
    api_key: str | None = None,
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
        body = resp.json()
        if "error_message" in body:
            raise ValueError(f"FRED API error for {series_id}: {body['error_message']}")
        if "observations" not in body:
            raise ValueError(f"FRED API unexpected response for {series_id}: {list(body.keys())}")
        data = body["observations"]
        if not data:
            return pd.DataFrame({"value": pd.Series([], dtype=float)}, index=pd.DatetimeIndex([], name="date"))
        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"])
        df["value"] = pd.to_numeric(df["value"], errors="coerce")
        df = df[["date", "value"]].dropna().set_index("date")
    else:
        # Fallback: scrape FRED CSV (no key needed)
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={start}&coed={end}"
        try:
            from io import StringIO
            resp = requests.get(url, timeout=30)
            resp.raise_for_status()
            df = pd.read_csv(StringIO(resp.text), parse_dates=["DATE"], index_col="DATE")
            df.index.name = "date"
            df.columns = ["value"]
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            df = df.dropna()
        except Exception as e:
            raise ValueError(f"Could not fetch FRED series {series_id}. Set FRED_API_KEY for reliable access.") from e

    if cache and not df.empty:
        _cache_set(cache_key, df)
    return df


def fetch_yield_curve(date: str | None = None) -> dict[str, float]:
    """Fetch US Treasury yield curve for a given date."""
    from concurrent.futures import ThreadPoolExecutor

    maturities = {"DGS1MO": "1M", "DGS3MO": "3M", "DGS6MO": "6M",
                  "DGS1": "1Y", "DGS2": "2Y", "DGS3": "3Y", "DGS5": "5Y",
                  "DGS7": "7Y", "DGS10": "10Y", "DGS20": "20Y", "DGS30": "30Y"}

    if date:
        dt = datetime.strptime(date, "%Y-%m-%d")
        start = (dt - timedelta(days=365)).strftime("%Y-%m-%d")
        end = (dt + timedelta(days=15)).strftime("%Y-%m-%d")
    else:
        start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        end = None

    def _fetch_one(item: tuple[str, str]) -> tuple[str, float] | None:
        series_id, label = item
        try:
            df = fetch_fred_series(series_id, start=start, end=end)
            if df.empty:
                return None
            if date:
                idx = pd.to_datetime(date)
                pos = df.index.get_indexer([idx], method="pad")[0]
                if pos == -1:
                    return None
                nearest = df.index[pos]
                if abs((nearest - idx).days) > 10:
                    return None
                val = df.loc[nearest, "value"]
                if isinstance(val, pd.Series):
                    val = val.iloc[-1]
            else:
                val = df.iloc[-1]["value"]
            if pd.isna(val):
                return None
            return (label, float(val))
        except Exception:
            return None

    curve = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        for result in executor.map(_fetch_one, maturities.items()):
            if result is not None:
                curve[result[0]] = result[1]

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

    # Detect rate-limit or invalid-key responses
    if "Note" in data:
        raise ValueError(f"Alpha Vantage rate limit hit: {data['Note']}")
    if "Error Message" in data:
        raise ValueError(f"Alpha Vantage error: {data['Error Message']}")
    if "Information" in data:
        raise ValueError(f"Alpha Vantage API error: {data['Information']}")

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
    end: str | None = None,
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
def fetch_finnhub_sentiment(symbol: str) -> dict[str, Any]:
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
    symbol: str, from_date: str | None = None, to_date: str | None = None
) -> list[dict]:
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
# FREE DATA: SEC EDGAR (insider trades, filings)
# ---------------------------------------------------------------------------
SEC_EDGAR_BASE = "https://efts.sec.gov/LATEST"
SEC_HEADERS = {"User-Agent": "agents-assemble research@example.com"}


def fetch_insider_trades(symbol: str, limit: int = 50) -> list[dict[str, Any]]:
    """Fetch recent insider trades from SEC EDGAR full-text search.

    Returns list of dicts with: name, title, date, transaction_type, shares, price
    Note: This uses the free EDGAR full-text search API.
    """
    # Use EDGAR company search for CIK lookup
    startdt = (datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d")
    url = f"https://efts.sec.gov/LATEST/search-index?q=%22{symbol}%22&dateRange=custom&startdt={startdt}&forms=4"
    try:
        resp = requests.get(url, headers=SEC_HEADERS, timeout=30)
        if resp.status_code == 200:
            return resp.json().get("hits", {}).get("hits", [])[:limit]
    except Exception:
        pass
    return []


def fetch_sec_filings(
    symbol: str,
    filing_type: str = "10-K",
    limit: int = 10,
) -> list[dict[str, Any]]:
    """Fetch SEC filings metadata via EDGAR full-text search."""
    url = f"{SEC_EDGAR_BASE}/search-index"
    params = {
        "q": f'"{symbol}"',
        "forms": filing_type,
        "dateRange": "custom",
        "startdt": "2020-01-01",
    }
    try:
        resp = requests.get(url, params=params, headers=SEC_HEADERS, timeout=30)
        if resp.status_code == 200:
            return resp.json().get("hits", {}).get("hits", [])[:limit]
    except Exception:
        pass
    return []




# ---------------------------------------------------------------------------
# FREE DATA: RSS News (Yahoo Finance + Google News -- no API key needed)
# ---------------------------------------------------------------------------
def _parse_rss_xml(xml_text: str) -> list[dict[str, str]]:
    """Parse RSS XML into list of dicts with title/link/pubDate/description/source."""
    import xml.etree.ElementTree as ET

    items: list[dict[str, str]] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items

    for item in root.iter("item"):
        entry: dict[str, str] = {}
        title_el = item.find("title")
        if title_el is not None and title_el.text:
            entry["title"] = title_el.text.strip()
        link_el = item.find("link")
        if link_el is not None and link_el.text:
            entry["link"] = link_el.text.strip()
        pub_el = item.find("pubDate")
        if pub_el is not None and pub_el.text:
            entry["pubDate"] = pub_el.text.strip()
        desc_el = item.find("description")
        if desc_el is not None and desc_el.text:
            entry["description"] = desc_el.text.strip()
        source_el = item.find("source")
        if source_el is not None and source_el.text:
            entry["source"] = source_el.text.strip()
        if entry.get("title"):
            items.append(entry)
    return items


def fetch_yahoo_rss_news(symbol: str, max_items: int = 20) -> list[dict[str, Any]]:
    """Fetch news headlines from Yahoo Finance RSS feed (free, no API key).

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        max_items: Maximum number of items to return

    Returns:
        List of dicts with: title, link, published, description, source
    """
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "agents-assemble/1.0"})
        if resp.status_code != 200:
            return []
        raw_items = _parse_rss_xml(resp.text)
        results = []
        for item in raw_items[:max_items]:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "published": item.get("pubDate", ""),
                "description": item.get("description", ""),
                "source": "yahoo_finance",
            })
        return results
    except Exception:
        return []


def fetch_google_news_rss(
    symbol: str, max_items: int = 20, topic: str = "stock"
) -> list[dict[str, Any]]:
    """Fetch news headlines from Google News RSS feed (free, no API key).

    Searches Google News for "<symbol> <topic>" and returns RSS results.

    Args:
        symbol: Ticker symbol or company name (e.g. 'AAPL', 'Apple')
        max_items: Maximum number of items to return
        topic: Additional search term (default: 'stock')

    Returns:
        List of dicts with: title, link, published, description, source
    """
    from urllib.parse import quote

    query = quote(f"{symbol} {topic}")
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "agents-assemble/1.0"})
        if resp.status_code != 200:
            return []
        raw_items = _parse_rss_xml(resp.text)
        results = []
        for item in raw_items[:max_items]:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "published": item.get("pubDate", ""),
                "description": item.get("description", ""),
                "source": item.get("source", "google_news"),
            })
        return results
    except Exception:
        return []


def fetch_news_rss(
    symbol: str, max_items: int = 30, sources: list[str] | None = None
) -> list[dict[str, Any]]:
    """Unified RSS news fetcher -- pulls from Yahoo Finance + Google News.

    Free, no API key needed. Deduplicates by title.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        max_items: Maximum total items to return
        sources: List of sources to use. Options: 'yahoo', 'google'.
                 Default: both.

    Returns:
        List of dicts with: title, link, published, description, source
    """
    if sources is None:
        sources = ["yahoo", "google"]

    all_items: list[dict[str, Any]] = []

    if "yahoo" in sources:
        all_items.extend(fetch_yahoo_rss_news(symbol, max_items=max_items))

    if "google" in sources:
        all_items.extend(fetch_google_news_rss(symbol, max_items=max_items))

    # Deduplicate by normalized title
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in all_items:
        key = item["title"].lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(item)

    return unique[:max_items]


# ---------------------------------------------------------------------------
# FREE DATA: SEC EDGAR 8-K filings (material events -- no API key)
# ---------------------------------------------------------------------------
def _get_cik_for_symbol(symbol: str) -> str | None:
    """Look up SEC CIK number for a ticker symbol via EDGAR company tickers JSON."""
    cache_file = CACHE_DIR / "sec_company_tickers.json"
    import json

    # Cache the tickers file (~2MB, changes rarely)
    tickers_data = None
    if cache_file.exists():
        age_hours = (time.time() - cache_file.stat().st_mtime) / 3600
        if age_hours < 24:
            try:
                tickers_data = json.loads(cache_file.read_text())
            except Exception:
                pass

    if tickers_data is None:
        try:
            resp = requests.get(
                "https://www.sec.gov/files/company_tickers.json",
                headers=SEC_HEADERS,
                timeout=15,
            )
            if resp.status_code == 200:
                tickers_data = resp.json()
                cache_file.write_text(json.dumps(tickers_data))
        except Exception:
            return None

    if tickers_data is None:
        return None

    sym_upper = symbol.upper()
    for entry in tickers_data.values():
        if entry.get("ticker", "").upper() == sym_upper:
            cik = str(entry.get("cik_str", ""))
            return cik.zfill(10)  # Pad to 10 digits
    return None


def fetch_sec_8k_filings(
    symbol: str, limit: int = 20, days_back: int = 90
) -> list[dict[str, Any]]:
    """Fetch recent 8-K filings (material events) from SEC EDGAR.

    8-K filings report major events: earnings, acquisitions, executive changes,
    debt issuance, bankruptcy, etc. These are the most time-sensitive SEC filings
    and often move stock prices.

    Free, no API key needed. Requires User-Agent header with email.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        limit: Maximum number of filings to return
        days_back: How far back to search (default: 90 days)

    Returns:
        List of dicts with: form_type, filed_date, accession_number,
        primary_document, description, url
    """
    cik = _get_cik_for_symbol(symbol)
    if not cik:
        return []

    # Use EDGAR submissions API (free, no key)
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    try:
        resp = requests.get(url, headers=SEC_HEADERS, timeout=15)
        if resp.status_code != 200:
            return []
        data = resp.json()
    except Exception:
        return []

    recent = data.get("filings", {}).get("recent", {})
    if not recent:
        return []

    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])
    descriptions = recent.get("primaryDocDescription", [])

    cutoff = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    results = []

    for i in range(min(len(forms), len(dates), len(accessions))):
        form = forms[i] if i < len(forms) else ""
        if not form.startswith("8-K"):
            continue
        filed = dates[i] if i < len(dates) else ""
        if filed < cutoff:
            continue

        acc = accessions[i] if i < len(accessions) else ""
        acc_no_dash = acc.replace("-", "")
        doc = primary_docs[i] if i < len(primary_docs) else ""
        desc = descriptions[i] if i < len(descriptions) else ""

        filing_url = ""
        if doc:
            filing_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{cik.lstrip('0')}/{acc_no_dash}/{doc}"
            )

        results.append({
            "form_type": form,
            "filed_date": filed,
            "accession_number": acc,
            "primary_document": doc,
            "description": desc,
            "url": filing_url,
            "source": "sec_edgar",
        })

        if len(results) >= limit:
            break

    return results


# ---------------------------------------------------------------------------
# FREE DATA: Reddit sentiment (read-only JSON, no API key)
# ---------------------------------------------------------------------------
_REDDIT_HEADERS = {"User-Agent": "agents-assemble/1.0 (financial research)"}

_FINANCE_SUBREDDITS = [
    "wallstreetbets",
    "stocks",
    "investing",
    "options",
    "SecurityAnalysis",
]


def fetch_reddit_posts(
    symbol: str,
    subreddits: list[str] | None = None,
    max_per_sub: int = 10,
    sort: str = "new",
) -> list[dict[str, Any]]:
    """Fetch Reddit posts mentioning a ticker from financial subreddits.

    Uses Reddit's public JSON endpoint (no API key needed).
    Appends .json to subreddit search URL.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        subreddits: List of subreddit names. Default: WSB, stocks, investing, etc.
        max_per_sub: Max posts per subreddit
        sort: Sort order: 'new', 'hot', 'top', 'relevance'

    Returns:
        List of dicts with: title, body, score, num_comments, created_utc,
        subreddit, url, source
    """
    if subreddits is None:
        subreddits = _FINANCE_SUBREDDITS

    all_posts: list[dict[str, Any]] = []

    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/search.json"
        params = {
            "q": f"${symbol} OR {symbol}",
            "restrict_sr": "on",
            "sort": sort,
            "t": "week",
            "limit": max_per_sub,
        }
        try:
            resp = requests.get(
                url, params=params, headers=_REDDIT_HEADERS, timeout=15
            )
            if resp.status_code != 200:
                continue
            data = resp.json()
            children = data.get("data", {}).get("children", [])
            for child in children:
                post = child.get("data", {})
                all_posts.append({
                    "title": post.get("title", ""),
                    "body": (post.get("selftext", "") or "")[:500],
                    "score": post.get("score", 0),
                    "num_comments": post.get("num_comments", 0),
                    "created_utc": post.get("created_utc", 0),
                    "subreddit": post.get("subreddit", sub),
                    "url": f"https://reddit.com{post.get('permalink', '')}",
                    "source": "reddit",
                })
        except Exception:
            continue

    all_posts.sort(key=lambda x: x.get("score", 0), reverse=True)
    return all_posts


def fetch_reddit_sentiment(symbol: str) -> dict[str, Any]:
    """Estimate Reddit sentiment for a ticker from financial subreddits.

    Uses keyword-based sentiment scoring on post titles/bodies.
    No API key needed -- uses Reddit's public JSON endpoints.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')

    Returns:
        Dict with: symbol, total_mentions, avg_score, avg_comments,
        sentiment_score (-1 to 1), sentiment_label, top_posts, subreddit_breakdown
    """
    posts = fetch_reddit_posts(symbol, max_per_sub=25)

    if not posts:
        return {
            "symbol": symbol,
            "total_mentions": 0,
            "sentiment_score": 0.0,
            "sentiment_label": "neutral",
            "avg_score": 0,
            "avg_comments": 0,
            "top_posts": [],
            "subreddit_breakdown": {},
        }

    bullish_words = {
        "buy", "calls", "long", "moon", "rocket", "bullish", "undervalued",
        "breakout", "squeeze", "yolo", "diamond", "hands", "tendies",
        "gamma", "rip", "surge", "rally", "beat", "upgrade", "upside",
        "strong", "growth", "outperform", "accumulate", "conviction",
    }
    bearish_words = {
        "sell", "puts", "short", "bear", "crash", "dump", "overvalued",
        "bubble", "rug", "pull", "tank", "drop", "miss", "downgrade",
        "weak", "decline", "underperform", "avoid", "risk", "bag",
        "holder", "loss", "dead", "falling", "knife", "recession",
    }

    scores = []
    sub_counts: dict[str, int] = {}

    for post in posts:
        text = f"{post['title']} {post['body']}".lower()
        bull_count = sum(1 for w in bullish_words if w in text)
        bear_count = sum(1 for w in bearish_words if w in text)
        total_kw = bull_count + bear_count
        if total_kw > 0:
            sentiment = (bull_count - bear_count) / total_kw
        else:
            sentiment = 0.0
        weight = 1 + math.log1p(max(post.get("score", 0), 0))
        scores.append(sentiment * weight)

        sub = post.get("subreddit", "unknown")
        sub_counts[sub] = sub_counts.get(sub, 0) + 1

    avg_sentiment = sum(scores) / len(scores) if scores else 0.0
    avg_sentiment = max(-1.0, min(1.0, avg_sentiment))

    if avg_sentiment > 0.15:
        label = "bullish"
    elif avg_sentiment < -0.15:
        label = "bearish"
    else:
        label = "neutral"

    avg_score = sum(p.get("score", 0) for p in posts) / len(posts) if posts else 0
    avg_comments = (
        sum(p.get("num_comments", 0) for p in posts) / len(posts) if posts else 0
    )

    return {
        "symbol": symbol,
        "total_mentions": len(posts),
        "sentiment_score": round(avg_sentiment, 3),
        "sentiment_label": label,
        "avg_score": round(avg_score, 1),
        "avg_comments": round(avg_comments, 1),
        "top_posts": [
            {"title": p["title"], "score": p["score"], "subreddit": p["subreddit"]}
            for p in posts[:5]
        ],
        "subreddit_breakdown": sub_counts,
    }


# ---------------------------------------------------------------------------
# FREE DATA: StockTwits social sentiment (no API key needed)
# ---------------------------------------------------------------------------
def fetch_stocktwits_sentiment(
    symbol: str, max_messages: int = 30
) -> dict[str, Any]:
    """Fetch StockTwits sentiment for a ticker (free, no API key).

    StockTwits is a social network for traders. Users tag messages as
    Bullish/Bearish, providing crowd-sourced sentiment data.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        max_messages: Max messages to analyze (API returns up to 30)

    Returns:
        Dict with: symbol, total_messages, bullish_count, bearish_count,
        sentiment_ratio, sentiment_label, sample_messages
    """
    url = f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return {
                "symbol": symbol, "total_messages": 0,
                "sentiment_label": "unavailable",
            }
        data = resp.json()
    except Exception:
        return {
            "symbol": symbol, "total_messages": 0,
            "sentiment_label": "unavailable",
        }

    messages = data.get("messages", [])[:max_messages]
    if not messages:
        return {"symbol": symbol, "total_messages": 0, "sentiment_label": "neutral"}

    bullish = 0
    bearish = 0
    samples = []

    for msg in messages:
        sentiment = msg.get("entities", {}).get("sentiment", {})
        if isinstance(sentiment, dict):
            basic = sentiment.get("basic", "")
        else:
            basic = ""

        if basic == "Bullish":
            bullish += 1
        elif basic == "Bearish":
            bearish += 1

        if len(samples) < 5:
            samples.append({
                "body": (msg.get("body", "") or "")[:200],
                "sentiment": basic or "neutral",
                "created_at": msg.get("created_at", ""),
            })

    total_tagged = bullish + bearish
    ratio = bullish / total_tagged if total_tagged > 0 else 0.5

    if ratio > 0.6:
        label = "bullish"
    elif ratio < 0.4:
        label = "bearish"
    else:
        label = "neutral"

    return {
        "symbol": symbol,
        "total_messages": len(messages),
        "bullish_count": bullish,
        "bearish_count": bearish,
        "sentiment_ratio": round(ratio, 3),
        "sentiment_label": label,
        "sample_messages": samples,
    }


# ---------------------------------------------------------------------------
# AGGREGATORS: Unified news + sentiment across all free sources
# ---------------------------------------------------------------------------
def fetch_all_news(
    symbol: str,
    sources: list[str] | None = None,
    max_items: int = 50,
) -> list[dict[str, Any]]:
    """Fetch news from ALL available free sources, deduplicated.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        sources: List of sources. Options: 'yahoo_rss', 'google_rss',
                 'yfinance', 'finnhub', 'reddit', 'sec_8k'.
                 Default: all free sources (yfinance + RSS + SEC).
        max_items: Maximum total items

    Returns:
        List of dicts with: title, link, published, description, source
    """
    if sources is None:
        sources = ["yahoo_rss", "google_rss", "yfinance", "sec_8k"]
        if get_api_key("FINNHUB_API_KEY"):
            sources.append("finnhub")

    all_items: list[dict[str, Any]] = []

    if "yahoo_rss" in sources:
        all_items.extend(fetch_yahoo_rss_news(symbol, max_items=20))

    if "google_rss" in sources:
        all_items.extend(fetch_google_news_rss(symbol, max_items=20))

    if "yfinance" in sources:
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            for n in (ticker.news or [])[:20]:
                ts = n.get("providerPublishTime", 0)
                pub = ""
                if ts and ts > 946684800:
                    try:
                        pub = datetime.fromtimestamp(ts, tz=timezone.utc).strftime(
                            "%a, %d %b %Y %H:%M:%S +0000"
                        )
                    except Exception:
                        pass
                all_items.append({
                    "title": n.get("title", ""),
                    "link": n.get("link", ""),
                    "published": pub,
                    "description": "",
                    "source": "yfinance",
                })
        except Exception:
            pass

    if "finnhub" in sources:
        try:
            news = fetch_finnhub_news(symbol)
            for n in news[:20]:
                ts = n.get("datetime", 0)
                pub = ""
                if ts and ts > 946684800:
                    try:
                        pub = datetime.fromtimestamp(ts, tz=timezone.utc).strftime(
                            "%a, %d %b %Y %H:%M:%S +0000"
                        )
                    except Exception:
                        pass
                all_items.append({
                    "title": n.get("headline", ""),
                    "link": n.get("url", ""),
                    "published": pub,
                    "description": n.get("summary", ""),
                    "source": "finnhub",
                })
        except Exception:
            pass

    if "reddit" in sources:
        posts = fetch_reddit_posts(symbol, max_per_sub=5)
        for p in posts[:15]:
            ts = p.get("created_utc", 0)
            pub = ""
            if ts:
                try:
                    pub = datetime.fromtimestamp(ts, tz=timezone.utc).strftime(
                        "%a, %d %b %Y %H:%M:%S +0000"
                    )
                except Exception:
                    pass
            all_items.append({
                "title": p.get("title", ""),
                "link": p.get("url", ""),
                "published": pub,
                "description": p.get("body", "")[:200],
                "source": f"reddit/{p.get('subreddit', '')}",
            })

    if "sec_8k" in sources:
        filings = fetch_sec_8k_filings(symbol, limit=10)
        for f in filings:
            all_items.append({
                "title": f"8-K Filing: {f.get('description', 'Material Event')}",
                "link": f.get("url", ""),
                "published": f.get("filed_date", ""),
                "description": f"SEC 8-K filed {f.get('filed_date', '')}",
                "source": "sec_edgar",
            })

    # Deduplicate by normalized title
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in all_items:
        key = item.get("title", "").lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(item)

    return unique[:max_items]


def fetch_aggregate_sentiment(symbol: str) -> dict[str, Any]:
    """Aggregate sentiment across all available free sources.

    Combines: Reddit sentiment, StockTwits sentiment, Finnhub social sentiment
    (if API key set), and basic news headline sentiment.

    Args:
        symbol: Ticker symbol

    Returns:
        Dict with: symbol, overall_sentiment (-1 to 1), overall_label,
        sources (per-source sentiment breakdown), news_count
    """
    sources_data: dict[str, dict[str, Any]] = {}
    weighted_scores: list[tuple[float, float]] = []  # (score, weight)

    # Reddit sentiment (weight: 1.0)
    try:
        reddit = fetch_reddit_sentiment(symbol)
        if reddit.get("total_mentions", 0) > 0:
            sources_data["reddit"] = {
                "sentiment_score": reddit["sentiment_score"],
                "sentiment_label": reddit["sentiment_label"],
                "mentions": reddit["total_mentions"],
            }
            weighted_scores.append((reddit["sentiment_score"], 1.0))
    except Exception:
        pass

    # StockTwits sentiment (weight: 1.5 -- tagged sentiment is more reliable)
    try:
        st = fetch_stocktwits_sentiment(symbol)
        if (st.get("total_messages", 0) > 0
                and st.get("sentiment_label") != "unavailable"):
            st_score = (st.get("sentiment_ratio", 0.5) - 0.5) * 2
            sources_data["stocktwits"] = {
                "sentiment_score": round(st_score, 3),
                "sentiment_label": st["sentiment_label"],
                "messages": st["total_messages"],
                "bullish": st.get("bullish_count", 0),
                "bearish": st.get("bearish_count", 0),
            }
            weighted_scores.append((st_score, 1.5))
    except Exception:
        pass

    # Finnhub social sentiment (weight: 1.0)
    fh_key = get_api_key("FINNHUB_API_KEY")
    if fh_key:
        try:
            fh = fetch_finnhub_sentiment(symbol)
            if fh:
                reddit_data = fh.get("reddit", [])
                if reddit_data:
                    latest = (
                        reddit_data[-1] if isinstance(reddit_data, list) else {}
                    )
                    pos = latest.get("positiveMention", 0)
                    neg = latest.get("negativeMention", 0)
                    total_m = pos + neg
                    if total_m > 0:
                        fh_score = (pos - neg) / total_m
                        sources_data["finnhub"] = {
                            "sentiment_score": round(fh_score, 3),
                            "positive_mentions": pos,
                            "negative_mentions": neg,
                        }
                        weighted_scores.append((fh_score, 1.0))
        except Exception:
            pass

    # News headline sentiment (weight: 0.5 -- basic keyword approach)
    try:
        news = fetch_news_rss(symbol, max_items=20)
        if news:
            positive = {
                "beat", "surge", "rally", "upgrade", "buy", "growth",
                "profit", "record", "strong", "outperform", "raise",
                "bullish", "gain", "up", "positive", "exceed", "above",
            }
            negative = {
                "miss", "crash", "decline", "downgrade", "sell", "loss",
                "weak", "cut", "bearish", "drop", "below", "warning",
                "risk", "concern", "fear", "negative", "layoff", "recall",
            }
            bull = 0
            bear = 0
            for n in news:
                title = n.get("title", "").lower()
                bull += sum(1 for w in positive if w in title)
                bear += sum(1 for w in negative if w in title)
            total_kw = bull + bear
            if total_kw > 0:
                news_score = (bull - bear) / total_kw
                sources_data["news_headlines"] = {
                    "sentiment_score": round(news_score, 3),
                    "articles_analyzed": len(news),
                    "positive_signals": bull,
                    "negative_signals": bear,
                }
                weighted_scores.append((news_score, 0.5))
    except Exception:
        pass

    # Calculate weighted average
    if weighted_scores:
        total_weight = sum(w for _, w in weighted_scores)
        overall = sum(s * w for s, w in weighted_scores) / total_weight
        overall = max(-1.0, min(1.0, overall))
    else:
        overall = 0.0

    if overall > 0.15:
        label = "bullish"
    elif overall < -0.15:
        label = "bearish"
    else:
        label = "neutral"

    return {
        "symbol": symbol,
        "overall_sentiment": round(overall, 3),
        "overall_label": label,
        "sources": sources_data,
        "news_count": sum(
            v.get("mentions", 0) + v.get("messages", 0)
            + v.get("articles_analyzed", 0)
            + v.get("positive_mentions", 0) + v.get("negative_mentions", 0)
            for v in sources_data.values()
        ),
    }


# ---------------------------------------------------------------------------
# FREE DATA: Market events calendar (FRED releases)
# ---------------------------------------------------------------------------
def fetch_market_events(days_ahead: int = 14) -> list[dict[str, Any]]:
    """Fetch upcoming economic data releases from FRED.

    Requires FRED_API_KEY env var (free registration at fred.stlouisfed.org).
    Falls back to a static calendar of major recurring events if no key.

    Args:
        days_ahead: Number of days to look ahead

    Returns:
        List of dicts with: name, date, description, source
    """
    fred_key = get_api_key("FRED_API_KEY")

    if fred_key:
        today = datetime.now().strftime("%Y-%m-%d")
        end = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        url = "https://api.stlouisfed.org/fred/releases/dates"
        params = {
            "api_key": fred_key,
            "file_type": "json",
            "realtime_start": today,
            "realtime_end": end,
            "include_release_dates_with_no_data": "false",
        }
        try:
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                events = []
                for release in data.get("release_dates", []):
                    events.append({
                        "name": (
                            f"FRED Release #{release.get('release_id', '?')}"
                        ),
                        "date": release.get("date", ""),
                        "description": release.get(
                            "release_name", "Economic data release"
                        ),
                        "source": "fred",
                    })
                return events
        except Exception:
            pass

    # Fallback: static calendar of major recurring US economic events
    now = datetime.now()
    events = []
    major_events = [
        ("FOMC Rate Decision", "Federal Reserve interest rate decision",
         [1, 3, 5, 6, 7, 9, 11, 12]),
        ("CPI Report", "Consumer Price Index -- inflation measure",
         list(range(1, 13))),
        ("Jobs Report (NFP)", "Non-Farm Payrolls -- first Friday of month",
         list(range(1, 13))),
        ("GDP Report", "Gross Domestic Product -- quarterly",
         [1, 4, 7, 10]),
        ("PCE Price Index",
         "Personal Consumption Expenditures -- Fed preferred inflation gauge",
         list(range(1, 13))),
        ("ISM Manufacturing",
         "ISM Manufacturing PMI -- first business day of month",
         list(range(1, 13))),
        ("Retail Sales", "Monthly retail sales data",
         list(range(1, 13))),
        ("Housing Starts", "New residential construction",
         list(range(1, 13))),
    ]
    for name, desc, months in major_events:
        for m in months:
            if m == now.month:
                event_date = now + timedelta(days=7)
            else:
                event_date = now.replace(month=m, day=15)
                # If date is in the past, try next year (handles Dec→Jan boundary)
                if event_date < now:
                    try:
                        event_date = event_date.replace(year=now.year + 1)
                    except (ValueError, OverflowError):
                        continue
            try:
                delta = (event_date - now).days
                if 0 <= delta <= days_ahead:
                    events.append({
                        "name": name,
                        "date": event_date.strftime("%Y-%m-%d"),
                        "description": desc,
                        "source": "static_calendar",
                    })
            except (ValueError, OverflowError):
                pass

    return sorted(events, key=lambda x: x.get("date", ""))


# ---------------------------------------------------------------------------
# FREE DATA: Earnings calendar and analyst estimates (yfinance)
# ---------------------------------------------------------------------------
def fetch_earnings_calendar(symbol: str) -> dict[str, Any]:
    """Fetch upcoming and past earnings dates + surprise data."""
    import yfinance as yf
    ticker = yf.Ticker(symbol)
    result = {
        "symbol": symbol,
        "earnings_dates": [],
        "quarterly_earnings": None,
    }
    try:
        cal = ticker.earnings_dates
        if cal is not None and not cal.empty:
            result["earnings_dates"] = [
                {"date": str(idx), **{col: (None if pd.isna(row[col]) else row[col]) for col in cal.columns}}
                for idx, row in cal.head(8).iterrows()
            ]
    except Exception:
        pass
    try:
        qe = ticker.quarterly_earnings
        if qe is not None and not qe.empty:
            result["quarterly_earnings"] = qe.to_dict()
    except Exception:
        pass
    return result


def fetch_analyst_recommendations(symbol: str) -> pd.DataFrame:
    """Fetch analyst recommendation history."""
    import yfinance as yf
    ticker = yf.Ticker(symbol)
    try:
        recs = ticker.recommendations
        if recs is not None and not recs.empty:
            return recs
    except Exception:
        pass
    return pd.DataFrame()


def fetch_institutional_holders(symbol: str) -> pd.DataFrame:
    """Fetch top institutional holders."""
    import yfinance as yf
    ticker = yf.Ticker(symbol)
    try:
        holders = ticker.institutional_holders
        if holders is not None and not holders.empty:
            return holders
    except Exception:
        pass
    return pd.DataFrame()


# ---------------------------------------------------------------------------
# FREE DATA: Sector / market breadth
# ---------------------------------------------------------------------------
def fetch_sector_performance(period: str = "1mo") -> dict[str, float]:
    """Fetch sector ETF performance over a period.

    Args:
        period: '1d', '5d', '1mo', '3mo', '6mo', '1y'

    Returns: {sector_name: return_pct}
    """
    import yfinance as yf
    sectors = {
        "Technology": "XLK", "Financials": "XLF", "Energy": "XLE",
        "Healthcare": "XLV", "Industrials": "XLI", "Consumer Staples": "XLP",
        "Utilities": "XLU", "Real Estate": "XLRE", "Communications": "XLC",
        "Materials": "XLB", "Consumer Disc": "XLY",
    }
    results = {}
    etf_list = list(sectors.values())
    etf_to_name = {etf: name for name, etf in sectors.items()}

    # Batch download all sector ETFs in one HTTP call
    try:
        data = yf.download(etf_list, period=period, group_by="ticker", progress=False)
        for etf in etf_list:
            try:
                hist = data[etf].dropna(how="all")
                if "Close" in hist.columns:
                    hist = hist.dropna(subset=["Close"])
                if len(hist) < 2:
                    continue
                first_close = hist["Close"].iloc[0]
                last_close = hist["Close"].iloc[-1]
                if (not pd.isna(first_close) and first_close > 0
                        and not pd.isna(last_close)):
                    results[etf_to_name[etf]] = float((last_close / first_close) - 1)
            except (KeyError, AttributeError):
                pass
    except Exception:
        pass

    # Fallback: individually fetch any sectors still missing
    for name, etf in sectors.items():
        if name in results:
            continue
        try:
            ticker = yf.Ticker(etf)
            hist = ticker.history(period=period)
            if not hist.empty and len(hist) > 1:
                first_close = hist["Close"].iloc[0]
                last_close = hist["Close"].iloc[-1]
                if (first_close is not None and not pd.isna(first_close) and first_close > 0
                        and last_close is not None and not pd.isna(last_close)):
                    results[name] = float((last_close / first_close) - 1)
        except Exception:
            pass
    return results


def fetch_market_breadth() -> dict[str, Any]:
    """Fetch market breadth indicators using major ETFs as proxies."""
    import yfinance as yf
    etfs = ["SPY", "QQQ", "IWM", "DIA", "VTI"]
    breadth = {}

    # Batch download all ETFs in one HTTP call
    fetched: dict[str, pd.DataFrame] = {}
    try:
        data = yf.download(etfs, period="3mo", group_by="ticker", progress=False)
        for sym in etfs:
            try:
                df = data[sym].dropna(how="all")
                if "Close" in df.columns:
                    df = df.dropna(subset=["Close"])
                if not df.empty:
                    fetched[sym] = df
            except (KeyError, AttributeError):
                pass
    except Exception:
        pass

    # Fallback: individually fetch any ETFs missing from batch
    for sym in etfs:
        if sym in fetched:
            continue
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period="3mo")
            if not hist.empty:
                fetched[sym] = hist
        except Exception:
            pass

    for sym in etfs:
        hist = fetched.get(sym)
        if hist is None:
            continue
        try:
            close = hist["Close"]
            sma20 = close.rolling(20).mean()
            valid_sma = sma20.notna()
            above_sma = (close[valid_sma] > sma20[valid_sma]).sum() / valid_sma.sum() if valid_sma.sum() > 0 else 0
            last_close = close.iloc[-1]
            if pd.isna(last_close):
                continue
            recent = close.iloc[-22:] if len(close) > 22 else close
            first_close = recent.iloc[0] if len(recent) > 1 else None
            ret_1m = (last_close / first_close - 1) if first_close is not None and not pd.isna(first_close) and first_close > 0 else 0
            breadth[sym] = {
                "pct_above_sma20": float(above_sma),
                "return_1m": float(ret_1m),
                "current_price": float(last_close),
            }
        except Exception:
            pass
    return breadth


# ---------------------------------------------------------------------------
# Screening / universe helpers
# ---------------------------------------------------------------------------
# Popular instruments available on Robinhood / Public.com / Tiger Brokers / IBKR
UNIVERSE = {
    # US Equities
    "mega_cap": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "BRK-B", "JPM", "V"],
    "growth": ["PLTR", "SNOW", "CRWD", "DDOG", "NET", "SHOP", "SQ", "ROKU", "ENPH", "MELI"],
    "value": ["BRK-B", "JPM", "JNJ", "PG", "KO", "PEP", "MRK", "CVX", "XOM", "IBM"],
    "dividend": ["JNJ", "PG", "KO", "PEP", "MMM", "T", "VZ", "MO", "ABBV", "O"],
    "meme": ["GME", "AMC", "PLTR", "SOFI", "HOOD", "RIVN", "LCID", "NIO", "BBAI"],
    # US ETFs
    "etf_broad": ["SPY", "QQQ", "IWM", "DIA", "VTI", "VOO"],
    "etf_sector": ["XLF", "XLK", "XLE", "XLV", "XLI", "XLP", "XLU", "XLRE", "XLC", "XLB"],
    "etf_bond": ["BND", "TLT", "IEF", "SHY", "LQD", "HYG", "AGG", "TIP", "VCSH", "VCIT"],
    "etf_international": ["EEM", "VEA", "VWO", "EFA", "IEMG"],
    "etf_commodity": ["GLD", "SLV", "USO", "UNG", "DBA", "WEAT", "COPX"],
    "crypto_adjacent": ["COIN", "MARA", "RIOT", "MSTR"],
    # China / HK ADRs (tradeable on US exchanges, Tiger Brokers, IBKR)
    # China ADRs — comprehensive (100+)
    "china_adr": [
        "BABA", "JD", "PDD", "NIO", "XPEV", "LI", "BIDU", "TME", "BILI", "FUTU",
        "NTES", "IQ", "WB", "ZTO", "VNET", "YMM", "DOYU", "HUYA", "GDS",
        "HTHT", "TCOM", "EDU", "TAL", "MNSO", "LEGN", "ZLAB", "RLX",
        "JOYY", "QFIN", "FINV", "SOHU", "DQ", "JKS", "SOL", "TIGR",
        "KC", "VIPS", "LU", "BEKE", "CAN", "NOAH", "EH", "NIU",
        "HSAI", "NAAS", "TUYA", "ZK", "DADA", "PUYI", "LX",
        "FLX", "FANH", "SY", "IMAB", "ZEPP", "ZH", "XNET",
        "TC", "MF", "XYF", "QSG", "FENG", "PT", "UCL", "WIMI",
    ],
    "china_etf": ["FXI", "MCHI", "KWEB", "GXC", "ASHR", "CQQQ", "CNXT"],
    # Japan ADRs
    "japan_adr": [
        "TM", "SONY", "MUFG", "SMFG", "NMR", "HMC", "NTDOY",
        "MSBHF", "TKOMY", "FANUY", "DNZOY", "SHECY", "RKUNY",
    ],
    "japan_etf": ["EWJ", "DXJ", "BBJP", "HEWJ"],
    # Hong Kong / Singapore
    "hk_etf": ["EWH", "FLHK"],
    "singapore_etf": ["EWS"],
    "singapore_sgx": [
        # Banks & Financials
        "D05.SI", "U11.SI", "O39.SI",  # DBS, UOB, OCBC
        "S68.SI", "BN4.SI", "G07.SI",  # SGX, Keppel, Great Eastern
        # REITs (SGX is REIT capital of Asia)
        "A17U.SI", "N2IU.SI", "C38U.SI",  # CapitaLand Ascendas, Mapletree Pan Asia, CapitaLand Integrated
        "ME8U.SI", "M44U.SI", "BUOU.SI",  # Mapletree Industrial, Mapletree Logistics, Frasers Logistics
        "J69U.SI", "T82U.SI", "SK6U.SI",  # Frasers Centrepoint, Suntec REIT, Parkway Life
        "N2HU.SI", "HMN.SI", "AJBU.SI",   # Mapletree US, CapitaLand China Trust, Keppel DC REIT (data centres)
        "A68U.SI", "J36.SI",               # CDL Hospitality, Jardine Matheson
        # Telco & Tech
        "Z74.SI", "CC3.SI", "S63.SI",  # SingTel, StarHub, ST Engineering
        "S58.SI", "BN2.SI",            # SATS, Nanofilm
        # Consumer & Healthcare
        "F34.SI", "Y92.SI", "OV8.SI",  # Wilmar, Thai Bev, Sheng Siong
        "C52.SI", "U96.SI", "S51.SI",  # ComfortDelGro, Sembcorp Industries, Seatrium
        "H78.SI", "V03.SI",            # Hongkong Land, Venture Corp
        # Property & Conglomerates
        "C09.SI", "U14.SI", "C31.SI",  # City Developments, UOL Group, CapitaLand Investment
        "CY6U.SI", "TQ5.SI",           # CapSpring, Frasers Property
        # Industrials & Offshore
        "BS6.SI", "AWX.SI", "S56.SI",  # YZJ Shipbuilding, AEM Holdings, SembMarine
        "BLA.SI", "EB5.SI",            # Bumitama Agri, First Resources
        # Small/Mid Cap (popular retail plays)
        "5CP.SI", "Z25.SI", "Q0F.SI",  # Silverlake Axis, Yanlord Land, iFast Corp
        "AIY.SI", "A30.SI",            # iX Biopharma, Centurion Corp
    ],
    # Europe ADRs — comprehensive by country
    "europe_uk": [
        "SHEL", "BP", "HSBC", "AZN", "GSK", "UL", "DEO", "BCS", "LYG",
        "RIO", "WPP", "VOD", "BTI", "NGG", "SNN", "SN", "BUD",
    ],
    "europe_germany": [
        "SAP", "DB", "BAYRY", "BASFY", "SIFY", "DTEGY",
    ],
    "europe_netherlands": ["ASML", "ING", "PHG", "STLA", "NXP", "NXPI"],
    "europe_france": ["TTE", "SNY", "DANOY", "BNPQF"],
    "europe_switzerland": ["NVS", "RHHBY", "UBS", "LOGI", "ABBNY"],
    "europe_nordic": ["NVO", "SPOT", "NOK", "ERIC", "NHYDY", "EQNR"],
    "europe_spain_italy": ["SAN", "BBVA", "TEF", "RACE", "ENEL"],
    "europe_all": [
        "SAP", "ASML", "NVO", "AZN", "SHEL", "TTE", "UL", "DEO", "BP", "HSBC",
        "GSK", "BCS", "LYG", "DB", "SAN", "BBVA", "ING", "PHG", "SPOT", "NOK",
        "ERIC", "ABBNY", "NVS", "UBS", "LOGI", "STM", "NXPI", "RIO", "VOD",
        "BTI", "NGG", "SNY", "EQNR", "NHYDY", "RACE", "STLA", "BUD",
    ],
    "europe_etf": ["VGK", "EZU", "EWG", "EWU", "EWQ", "EWI", "EWP", "IEUR", "HEDJ"],
    # Latin America — comprehensive
    "latam_brazil": [
        "VALE", "PBR", "ITUB", "BSBR", "ABEV", "BBD", "ERJ",
        "SBS", "CBD", "GGB", "SID", "CIG", "BRFS", "VTEX", "NU",
    ],
    "latam_mexico": ["AMX", "KOF", "FMX", "BSMX", "OMAB", "PAC"],
    "latam_argentina": ["GGAL", "YPF", "BMA", "LOMA", "SUPV", "GLOB"],
    "latam_chile_colombia_peru": ["SQM", "BCH", "CIB", "BVN", "CREG"],
    "latam_all": [
        "MELI", "NU", "VALE", "PBR", "ITUB", "BSBR", "SQM", "GGAL",
        "STNE", "PAGS", "ABEV", "ERJ", "VTEX", "DLO", "AMX", "KOF",
        "FMX", "YPF", "BMA", "GLOB", "BCH", "CIB", "BVN",
        "BBD", "GGB", "SID", "BRFS", "SBS", "CIG", "LOMA",
    ],
    "latam_etf": ["EWZ", "EWW", "ILF", "ARGT", "ECH"],
    # India ADRs
    "india_adr": [
        "INFY", "WIT", "IBN", "HDB", "RDY", "WNS", "MMYT", "SIFY",
    ],
    "india_etf": ["INDA", "SMIN", "EPI", "NDIA", "INDL"],
    # Korea / Taiwan
    "korea_adr": ["LPL", "KB", "SHG", "PKX"],
    "taiwan_adr": ["TSM", "UMC", "ASX", "CAMT", "IMOS"],
    "asia_etf": ["AAXJ", "EWT", "EWY", "EWA", "EWJ", "VPL", "IPAC"],
    # Australia ADRs
    "australia_adr": ["BHP", "RIO", "JHX", "WBD"],
    # Africa / Middle East ADRs
    "africa_adr": ["GOLD", "HMY", "AU", "SBSW", "SSRM", "MTN"],
    "middle_east_adr": ["MBLY", "CYBR", "MNDY", "WIX", "GLBE", "CEVA"],
    # Southeast Asia
    "se_asia_adr": ["SE", "GRAB"],
    # Commodities (via ETFs/stocks)
    "commodities": ["GLD", "SLV", "USO", "UNG", "DBA", "WEAT", "COPX", "CPER",
                     "FCX", "NEM", "GOLD", "BHP", "RIO", "VALE"],
    # REITs
    "reits": ["O", "AMT", "PLD", "EQIX", "SPG", "DLR", "VNQ", "XLRE"],
    # Small caps (Russell 2000 components, IWM)
    "small_cap": ["SMCI", "CELH", "CAVA", "DUOL", "RELY", "CWAN", "FTNT",
                   "LULU", "DECK", "EXAS", "HUBS", "SAIA", "RCL", "BURL"],
    "small_cap_etf": ["IWM", "IWO", "IWN", "SCHA", "VB", "VTWO"],
    # Mid caps
    "mid_cap": ["ZS", "PANW", "OKTA", "VEEV", "TEAM", "WIX", "ZM",
                "NXPI", "MCHP", "SWKS", "QRVO", "ON", "ENTG", "LRCX"],
    "mid_cap_etf": ["MDY", "IJH", "VO", "IVOO"],
    # Micro/nano caps (very small, high vol — Tiger/IBKR only)
    "micro_cap": ["IONQ", "RGTI", "QUBT", "SOUN", "IREN", "APLD",
                   "GSAT", "OPEN", "DNA", "MNDY", "BRZE", "GTLB"],
    # Penny stocks / speculative (very high risk, available on most platforms)
    "speculative": ["ASTS", "LUNR", "RKLB", "JOBY", "LILM", "EVTL",
                     "MVST", "LAZR", "LIDR", "OUST"],
    # Penny / under $5 stocks (EXTREME risk, momentum-only, small positions)
    "penny_momentum": ["LAC", "KULR", "OPTT", "LODE", "EDIT", "CDXS",
                        "GSAT", "DNA", "OPEN", "WISH"],
    # Sector themes (missing categories)
    "fintech_payments": ["SQ", "PYPL", "AFRM", "UPST", "SOFI", "COIN", "HOOD", "NU", "STNE"],
    "cybersecurity": ["CRWD", "PANW", "ZS", "FTNT", "S", "CYBR", "RPD", "TENB"],
    "gaming_esports": ["EA", "TTWO", "RBLX", "U", "DKNG", "PENN"],
    "water_agriculture": ["AWK", "WTRG", "ADM", "CF", "MOS", "NTR", "DE", "CTVA"],
    "nuclear_energy": ["CCJ", "LEU", "NNE", "OKLO", "SMR"],
    "quantum_computing": ["IONQ", "RGTI", "QUBT"],
    "cannabis": ["TLRY", "CGC", "ACB", "MO", "STZ"],
    "space": ["RKLB", "ASTS", "LUNR", "BA", "LMT", "NOC"],
    "ev_full": ["TSLA", "RIVN", "LCID", "NIO", "XPEV", "LI", "GM", "F", "TM", "HMC"],
    # 2026 Emerging Themes
    "robotics_autonomous": [
        "ISRG", "INTC", "NVDA", "TER", "CGNX", "AZTA", "IRBT",
        "BOTZ", "ROBO",  # Robotics ETFs
        "GOOGL", "TSLA", "GM", "F",  # Autonomous vehicles
        "ABBNY", "FANUY",  # Industrial automation
    ],
    "glp1_obesity": [
        "LLY", "NVO", "AMGN", "VKTX",  # GLP-1 leaders
        "PFE", "ABBV", "JNJ", "MRK",  # Big pharma with pipelines
        "HIMS", "PLNT", "PTON",  # Beneficiaries (telehealth, fitness)
    ],
    "space_economy": [
        "RKLB", "ASTS", "LUNR", "BA", "LMT", "NOC",
        "PLTR", "IRDM", "VSAT",
        "ARKX",  # Space ETF
    ],
    # Frontier / underexplored markets
    "frontier_etf": ["VNM", "EIDO", "FM", "FRN"],
    # Copper / uranium / lithium (commodity supercycle plays)
    "copper_uranium_lithium": [
        "SCCO", "COPX", "FCX",  # Copper
        "URA", "CCJ", "UUUU", "NXE",  # Uranium
        "LIT", "ALB", "SQM",  # Lithium
    ],
    # Recent IPOs with momentum
    "recent_ipos": ["ARM", "VRT", "RDDT", "BIRK", "CART"],
    # Short squeeze candidates (high short interest, March 2026)
    "short_squeeze": [
        "HTZ", "GRPN", "HIMS", "AI", "SOUN", "LCID", "RXRX",
        "BYND", "ENVX", "NVAX", "MARA", "BBAI", "VKTX", "PLUG", "RUN",
    ],
    # 2026 YTD winners (energy crisis + geopolitical)
    "etf_2026_winners": ["BWET", "XOP", "XES", "WGMI", "BKCH", "ITA"],
    # Uranium expanded (nuclear renaissance, 2B lb deficit)
    "uranium_expanded": ["URA", "URNM", "CCJ", "UUUU", "DNN", "NXE", "LEU"],
    # Oil services (Iran crisis beneficiaries)
    "oil_services": ["OXY", "DVN", "HAL", "SLB", "BKR"],
    # Precious metals expanded
    "precious_metals": ["GLD", "SLV", "GDX", "GDXJ", "NEM", "GOLD", "AEM", "PAAS", "WPM"],
    # Data center infrastructure (AI capex beneficiaries)
    "data_centers": ["VRT", "EQIX", "DLR", "AMT", "DELL", "HPE", "SMCI"],
    # Semiconductor comprehensive (2026: $1T global market, +25% YoY)
    "semiconductor": [
        "NVDA", "AMD", "AVGO", "ASML", "TSM", "INTC", "QCOM", "TXN",
        "MRVL", "MU", "ADI", "NXPI", "ARM", "ON", "LRCX", "AMAT",
        "KLAC", "SNPS", "CDNS", "MCHP", "SWKS", "QRVO",
        "SMH", "SOXX",  # Semiconductor ETFs
    ],
    # Small cap value (from research — AVUV 13.23% annualized since 2019)
    "small_cap_value_etf": ["AVUV", "DFSV", "VBR", "IWC", "FDM"],
    "small_cap_picks": ["GRC", "UCTT", "WTTR", "EVLV", "WWW"],
    # Mid cap picks (S&P 400 EPS growth +19.6% for 2026)
    "mid_cap_picks": ["CRSP", "IRDM", "ERAS", "AXTI"],
    "mid_cap_active_etf": ["SMAP", "HWSM", "NBSM", "SPMD"],
    # Contrarian / fallen angels (2026 rebound candidates)
    "contrarian_2026": ["FMC", "CZR", "CLX", "CMCSA", "AAP", "HRL", "UPS",
                         "BA", "INTC", "PFE", "ENPH", "LUV"],
    # Activist targets (Elliott, Trian, Starboard campaigns)
    "activist_targets": ["NCLH", "WEN", "TRIP", "TXN", "LUV"],
    # Nuclear SMR (OKLO +700% in 12 months)
    "nuclear_smr": ["OKLO", "LEU", "BWXT", "SMR", "NNE"],
    # Defense niche (beyond LMT/NOC)
    "defense_niche": ["KTOS", "KRMN", "BWXT"],
    # Gold streaming (leveraged gold exposure, lower risk than miners)
    "gold_streaming": ["WPM", "RGLD", "EQX", "FNV"],
    # Midstream energy (pipeline income plays)
    "midstream_energy": ["HESM", "WES", "MPLX", "ET", "EPD"],
    # Agriculture / food security
    "agriculture": ["ADM", "CF", "MOS", "NTR", "DE", "CTVA", "FMC",
                     "DBA", "WEAT", "CORN", "MOO"],
    # Gaming / entertainment
    "gaming_entertainment": ["NTDOY", "EA", "TTWO", "RBLX", "U", "DKNG",
                              "DIS", "NFLX", "WBD", "PARA", "CMCSA"],
    # LatAm expanded (from research)
    "latam_expanded": ["COPA", "ARCO", "TV", "LOMA", "CRESY"],
    # Dividend Aristocrats (25+ years consecutive increases, S&P 500)
    "dividend_aristocrats": [
        "JNJ", "PG", "KO", "PEP", "ABBV", "MRK", "MMM", "ABT", "CL", "EMR",
        "GPC", "ADM", "ADP", "AFL", "APD", "BDX", "BEN", "CAH", "CB", "CTAS",
        "CVX", "DOV", "ECL", "ED", "GD", "GWW", "HRL", "ITW", "KMB", "LOW",
        "MCD", "NDSN", "NEE", "NUE", "PH", "PPG", "ROP", "SHW", "SYY", "TGT",
        "TROW", "WMT", "XOM", "T", "VZ", "IBM", "O",
    ],
    # Dividend Kings (50+ years)
    "dividend_kings": [
        "JNJ", "PG", "KO", "CL", "EMR", "GPC", "DOV", "PH", "GWW",
        "MMM", "ABT", "ADM", "BDX", "ITW", "KMB", "LOW", "NUE", "PPG",
        "SWK", "SYY", "TGT",
    ],
    # Global diversified — comprehensive (top picks from each region)
    "global_diversified": [
        # US mega cap
        "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "JPM", "V",
        # Europe
        "SAP", "ASML", "NVO", "AZN", "SHEL", "UL", "NVS", "SPOT", "ABBNY",
        # Japan
        "TM", "SONY", "MUFG",
        # China
        "BABA", "PDD", "JD", "BIDU", "NIO",
        # India
        "INFY", "IBN", "HDB",
        # SE Asia
        "SE", "GRAB", "TSM",
        # LatAm
        "MELI", "NU", "VALE", "PBR", "AMX",
        # Australia / Africa
        "BHP", "RIO", "GOLD",
        # Regional ETFs
        "SPY", "EFA", "EEM", "VWO", "INDA", "EWJ", "EWZ",
    ],
}


def get_universe(category: str = "mega_cap") -> list[str]:
    """Get a list of tickers for a given category."""
    return list(UNIVERSE.get(category, UNIVERSE["mega_cap"]))


def _all_universe_symbols() -> list[str]:
    """Return sorted list of all unique symbols across every UNIVERSE category."""
    return list(_ALL_UNIVERSE_SYMBOLS)


_ALL_UNIVERSE_SYMBOLS: list[str] = sorted({s for syms in UNIVERSE.values() for s in syms})


def scan_52_week_lows(
    universe: list[str] | None = None,
    max_results: int = 20,
) -> list[dict[str, Any]]:
    """Scan for stocks near their 52-week lows (live data).

    Returns list of {symbol, price, 52w_low, 52w_high, pct_from_low, pct_from_high}
    sorted by proximity to 52w low.
    """
    import yfinance as yf

    if universe is None:
        universe = _all_universe_symbols()

    # Batch download 1-year history (1 HTTP call) instead of N individual
    # yf.Ticker.info calls which each make a separate request.
    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

    fetched: dict[str, pd.DataFrame] = {}
    if len(universe) > 1:
        try:
            data = yf.download(universe, start=start, end=end, group_by="ticker", progress=False)
            for sym in universe:
                try:
                    df = data[sym].dropna(how="all")
                    if "Close" in df.columns:
                        df = df.dropna(subset=["Close"])
                    if not df.empty:
                        fetched[sym] = df
                except (KeyError, AttributeError):
                    pass
        except Exception:
            pass

    # Fallback: individually fetch symbols missing from batch
    for sym in universe:
        if sym in fetched:
            continue
        try:
            df = fetch_ohlcv(sym, start=start, end=end)
            if not df.empty:
                fetched[sym] = df
        except Exception:
            pass

    results = []
    for sym in universe:
        hist = fetched.get(sym)
        if hist is None or "Close" not in hist.columns:
            continue
        close = hist["Close"]
        if len(close) < 20:
            continue
        price = close.iloc[-1]
        if pd.isna(price) or price <= 0:
            continue
        low_52 = float(close.min())
        high_52 = float(close.max())
        if low_52 <= 0 or high_52 <= 0:
            continue

        pct_from_low = (price - low_52) / low_52
        pct_from_high = (price - high_52) / high_52
        results.append({
            "symbol": sym,
            "price": float(price),
            "52w_low": low_52,
            "52w_high": high_52,
            "pct_from_low": float(pct_from_low),
            "pct_from_high": float(pct_from_high),
            "range_position": float((price - low_52) / (high_52 - low_52)) if high_52 > low_52 else 0.5,
        })

    results.sort(key=lambda x: x["pct_from_low"])
    return results[:max_results]


def scan_volatile_stocks(
    universe: list[str] | None = None,
    period: str = "3mo",
    min_vol: float = 0.03,
    max_results: int = 20,
) -> list[dict[str, Any]]:
    """Scan for most volatile stocks (live data).

    Returns list sorted by daily volatility (highest first).
    """
    import yfinance as yf

    if universe is None:
        universe = _all_universe_symbols()

    # Batch download all symbols in one HTTP call instead of N individual calls
    fetched: dict[str, pd.DataFrame] = {}
    if len(universe) > 1:
        try:
            data = yf.download(universe, period=period, group_by="ticker", progress=False)
            for sym in universe:
                try:
                    df = data[sym].dropna(how="all")
                    if "Close" in df.columns:
                        df = df.dropna(subset=["Close"])
                    if not df.empty:
                        fetched[sym] = df
                except (KeyError, AttributeError):
                    pass
        except Exception:
            pass

    # Fallback: individually fetch symbols not in batch
    for sym in universe:
        if sym in fetched:
            continue
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period=period)
            if not hist.empty:
                fetched[sym] = hist
        except Exception:
            pass

    results = []
    for sym in universe:
        hist = fetched.get(sym)
        if hist is None or "Close" not in hist.columns or len(hist) < 20:
            continue
        try:
            close = hist["Close"]
            last_close = close.iloc[-1]
            if pd.isna(last_close):
                continue
            daily_vol = close.pct_change().std()
            if pd.isna(daily_vol) or daily_vol < min_vol:
                continue
            avg_vol = hist["Volume"].mean() if "Volume" in hist.columns else 0.0
            results.append({
                "symbol": sym,
                "daily_vol": float(daily_vol),
                "annual_vol": float(daily_vol * _SQRT_252),
                "avg_volume": float(avg_vol) if not pd.isna(avg_vol) else 0.0,
                "price": float(last_close),
            })
        except Exception:
            pass

    results.sort(key=lambda x: x["daily_vol"], reverse=True)
    return results[:max_results]


def discover_universe_from_etf(
    etf_symbol: str,
    max_holdings: int = 20,
) -> list[str]:
    """Discover stock universe from an ETF's top holdings (live data).

    Useful for building universes from sector/theme ETFs.
    """
    raise NotImplementedError(
        f"discover_universe_from_etf('{etf_symbol}') is not implemented. "
        "Use get_universe() with a category instead."
    )


def screen_by_fundamentals(
    symbols: list[str],
    min_market_cap: float | None = None,
    max_pe: float | None = None,
    min_dividend_yield: float | None = None,
    max_debt_to_equity: float | None = None,
) -> list[dict[str, Any]]:
    """Screen stocks by fundamental criteria."""
    from concurrent.futures import ThreadPoolExecutor

    def _valid(v: Any) -> bool:
        """Check if a fundamental value is present and numeric (not None/NaN)."""
        return v is not None and not (isinstance(v, float) and v != v)

    def _fetch_one(sym: str) -> dict[str, Any] | None:
        try:
            return fetch_fundamentals(sym)
        except Exception:
            return None

    # Fetch fundamentals in parallel (each is a separate HTTP call)
    fundamentals: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=8) as executor:
        for sym, f in zip(symbols, executor.map(_fetch_one, symbols)):
            if f is not None:
                fundamentals[sym] = f

    results = []
    for sym in symbols:
        f = fundamentals.get(sym)
        if f is None:
            continue
        if min_market_cap is not None:
            if not _valid(f["market_cap"]) or f["market_cap"] < min_market_cap:
                continue
        if max_pe is not None:
            if not _valid(f["pe_ratio"]) or f["pe_ratio"] > max_pe:
                continue
        if min_dividend_yield is not None:
            if not _valid(f["dividend_yield"]) or f["dividend_yield"] < min_dividend_yield:
                continue
        if max_debt_to_equity is not None:
            if not _valid(f["debt_to_equity"]) or f["debt_to_equity"] > max_debt_to_equity:
                continue
        results.append(f)
    return results


# ===========================================================================
# ALTERNATIVE DATA: Free non-traditional signals
# ===========================================================================

# ---------------------------------------------------------------------------
# ALT DATA: Google Trends (pytrends — free, no key)
# ---------------------------------------------------------------------------
def fetch_google_trends(
    keywords: list[str],
    timeframe: str = "today 3-m",
    geo: str = "",
    cache: bool = True,
) -> pd.DataFrame:
    """Fetch Google Trends interest-over-time for keywords.

    Uses the pytrends library (pip install pytrends). No API key needed.

    Args:
        keywords: Up to 5 search terms (Google Trends limit).
        timeframe: Time range. Options:
            'now 1-H'  (past hour), 'now 4-H'  (past 4 hours),
            'now 1-d'  (past day),  'now 7-d'  (past 7 days),
            'today 1-m' (past 30 days), 'today 3-m' (past 90 days),
            'today 12-m' (past 12 months),
            'YYYY-MM-DD YYYY-MM-DD' (custom range, daily if <9mo, weekly otherwise)
        geo: Country code ('' = worldwide, 'US', 'GB', 'CN', etc.)
        cache: Use cached results (12h TTL).

    Returns:
        DataFrame with DatetimeIndex and one column per keyword (0-100 scale),
        plus 'isPartial' column. Empty DataFrame on failure.

    Trading signal: Rising search interest for a brand/product → demand growth.
        Compare current vs 30-day-ago interest for momentum.
    Sectors: Consumer retail, tech adoption, pharma awareness, travel demand.
    """
    cache_key = f"gtrends_{'_'.join(keywords)}_{timeframe}_{geo}"
    if cache:
        cached = _cache_get(cache_key, max_age_hours=12)
        if cached is not None:
            return cached

    try:
        from pytrends.request import TrendReq
    except ImportError:
        raise ImportError(
            "pytrends is required: pip install pytrends\n"
            "For better rate limiting: pip install pytrends-modern"
        )

    try:
        # Initialize — avoid passing retry params that may break on older urllib3
        pytrends = TrendReq(hl="en-US", tz=360)
        pytrends.build_payload(keywords[:5], cat=0, timeframe=timeframe, geo=geo)
        df = pytrends.interest_over_time()

        if df is not None and not df.empty:
            if cache:
                _cache_set(cache_key, df)
            return df
    except Exception:
        pass

    return pd.DataFrame()


def fetch_google_trends_related(
    keyword: str,
    timeframe: str = "today 3-m",
    geo: str = "",
) -> dict[str, pd.DataFrame]:
    """Fetch related queries and topics for a keyword from Google Trends.

    Returns dict with keys 'rising' and 'top', each a DataFrame.
    Useful for discovering emerging trends and related stock plays.
    """
    try:
        from pytrends.request import TrendReq
    except ImportError:
        raise ImportError("pytrends is required: pip install pytrends")

    try:
        pytrends = TrendReq(hl="en-US", tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=geo)
        related = pytrends.related_queries()
        result = {}
        if keyword in related:
            for key in ("top", "rising"):
                val = related[keyword].get(key)
                result[key] = val if val is not None else pd.DataFrame()
        return result
    except Exception:
        return {"top": pd.DataFrame(), "rising": pd.DataFrame()}


# ---------------------------------------------------------------------------
# ALT DATA: TSA Checkpoint Passenger Data (free, no key)
# ---------------------------------------------------------------------------
def fetch_tsa_checkpoint(cache: bool = True) -> pd.DataFrame:
    """Fetch daily TSA checkpoint passenger data from tsa.gov.

    Scrapes the HTML table at https://www.tsa.gov/travel/passenger-volumes.
    Updated Mon-Fri by 9am. No API key needed.

    NOTE: TSA uses Akamai CDN protection which may block programmatic access.
    If blocked, use fetch_air_travel_index() as a FRED-based fallback.

    Returns:
        DataFrame with DatetimeIndex and columns for current year and
        comparison years. Empty DataFrame on failure.

    Trading signal: Compare current traveler counts to prior year.
        Sustained growth → bullish airlines/travel. Sharp drops → bearish.
    Sectors: Airlines (DAL, UAL, LUV, AAL), hotels (MAR, HLT, H),
        travel platforms (BKNG, EXPE, ABNB), airports.
    """
    cache_key = "tsa_checkpoint_current"
    if cache:
        cached = _cache_get(cache_key, max_age_hours=12)
        if cached is not None:
            return cached

    url = "https://www.tsa.gov/travel/passenger-volumes"
    try:
        # TSA blocks default User-Agent; use a browser-like header
        from io import StringIO

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
            "Accept-Language": "en-US,en;q=0.9",
        }
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        tables = pd.read_html(StringIO(resp.text), header=0)
        if not tables:
            return pd.DataFrame()

        df = tables[0]
        # First column is the date
        date_col = df.columns[0]
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        df = df.dropna(subset=[date_col])
        df = df.set_index(date_col)
        df.index.name = "date"

        # Convert numeric columns
        for col in df.columns:
            df[col] = pd.to_numeric(
                df[col].astype(str).str.replace(",", ""), errors="coerce"
            )

        df = df.sort_index()

        if cache and not df.empty:
            _cache_set(cache_key, df)
        return df
    except Exception:
        return pd.DataFrame()


def fetch_air_travel_index(
    start: str = "2020-01-01",
    cache: bool = True,
) -> pd.DataFrame:
    """Fetch air travel indicators from FRED (always accessible fallback for TSA data).

    Returns DataFrame with monthly airline load factor and freight transport index.
    These are reliable proxies for air travel demand when TSA.gov is blocked.

    FRED Series:
        LOADFACTOR — Airline industry domestic load factor (% seats filled)
        TSIFRGHT — Transportation Services Index: Freight

    No API key needed (uses FRED CSV fallback).

    Trading signal: Rising load factor = strong travel demand, bullish airlines.
        Load factor > 85% = capacity constraints, pricing power.
    """
    cache_key = f"air_travel_index_{start}"
    if cache:
        cached = _cache_get(cache_key, max_age_hours=24)
        if cached is not None:
            return cached

    from io import StringIO

    series_map = {
        "LOADFACTOR": "airline_load_factor_pct",
        "TSIFRGHT": "freight_transport_index",
    }

    frames = []
    for series_id, col_name in series_map.items():
        url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}&cosd={start}"
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                df = pd.read_csv(StringIO(resp.text), parse_dates=["DATE"])
                df = df.rename(columns={"DATE": "date", series_id: col_name})
                df = df.set_index("date")
                df[col_name] = pd.to_numeric(df[col_name], errors="coerce")
                frames.append(df)
        except Exception:
            pass

    if not frames:
        return pd.DataFrame()

    result = pd.concat(frames, axis=1)
    result.index.name = "date"
    result = result.dropna(how="all").sort_index()

    if cache and not result.empty:
        _cache_set(cache_key, result)
    return result


def fetch_tsa_yoy_change(cache: bool = True) -> pd.DataFrame:
    """Compute year-over-year change in TSA passenger volumes.

    Falls back to air travel index if TSA direct scraping is blocked.
    Returns DataFrame with yoy_change column.
    """
    df = fetch_tsa_checkpoint(cache=cache)
    if not df.empty and len(df.columns) >= 2:
        current_col = df.columns[0]
        prior_col = df.columns[1]
        result = pd.DataFrame({
            "current": df[current_col],
            "prior_year": df[prior_col],
        })
        result["yoy_change"] = (
            (result["current"] - result["prior_year"]) / result["prior_year"]
        )
        result["yoy_change"] = result["yoy_change"].replace(
            [float("inf"), float("-inf")], float("nan")
        )
        return result.dropna()

    # Fallback: use FRED load factor for YoY comparison
    air = fetch_air_travel_index(
        start=(datetime.now() - timedelta(days=730)).strftime("%Y-%m-%d"),
        cache=cache,
    )
    if air.empty or "airline_load_factor_pct" not in air.columns:
        return pd.DataFrame()

    lf = air[["airline_load_factor_pct"]].dropna()
    lf["prior_year"] = lf["airline_load_factor_pct"].shift(12)
    lf["yoy_change"] = (lf["airline_load_factor_pct"] - lf["prior_year"]) / lf["prior_year"]
    return lf.dropna()


# ---------------------------------------------------------------------------
# ALT DATA: NOAA Climate Data (free, token required)
# ---------------------------------------------------------------------------
NOAA_CDO_BASE = "https://www.ncei.noaa.gov/cdo-web/api/v2"


def fetch_noaa_weather(
    dataset: str = "GHCND",
    station_id: str = "GHCND:USW00094728",
    start: str | None = None,
    end: str | None = None,
    data_types: list[str] | None = None,
    token: str | None = None,
    cache: bool = True,
) -> pd.DataFrame:
    """Fetch weather data from NOAA Climate Data Online API.

    Requires a free token from https://www.ncdc.noaa.gov/cdo-web/token.
    Set NOAA_CDO_TOKEN env var or pass token directly.

    Args:
        dataset: Dataset ID. Common: 'GHCND' (daily), 'GSOM' (monthly).
        station_id: Weather station. Default: Central Park, NYC.
            Find stations at: https://www.ncdc.noaa.gov/cdo-web/datatools/findstation
        start: Start date 'YYYY-MM-DD' (default: 1 year ago).
        end: End date 'YYYY-MM-DD' (default: today).
        data_types: List of data type IDs to fetch. Common GHCND types:
            TMAX (max temp, tenths of C), TMIN (min temp), TAVG (avg temp),
            PRCP (precipitation, tenths of mm), SNOW (snowfall, mm),
            AWND (avg wind speed, tenths of m/s).
        token: NOAA CDO API token (or set NOAA_CDO_TOKEN env var).
        cache: Cache results for 12 hours.

    Returns:
        DataFrame with DatetimeIndex and one column per data type.

    Trading signal: Extreme weather events → energy demand spikes, crop damage.
        Mild winters → lower nat gas demand (UNG). Heat waves → higher electricity.
    Sectors: Energy (XLE, UNG, USO), agriculture (DBA, WEAT), utilities, insurance.
    """
    token = token or get_api_key("NOAA_CDO_TOKEN")
    if not token:
        raise ValueError(
            "NOAA CDO token required. Get free token: https://www.ncdc.noaa.gov/cdo-web/token\n"
            "Set NOAA_CDO_TOKEN env var."
        )

    end = end or datetime.now().strftime("%Y-%m-%d")
    start = start or (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

    cache_key = f"noaa_{dataset}_{station_id}_{start}_{end}"
    if cache:
        cached = _cache_get(cache_key, max_age_hours=12)
        if cached is not None:
            return cached

    headers = {"token": token}
    params: dict[str, Any] = {
        "datasetid": dataset,
        "stationid": station_id,
        "startdate": start,
        "enddate": end,
        "limit": 1000,
        "units": "metric",
    }
    if data_types:
        params["datatypeid"] = ",".join(data_types)

    all_records: list[dict] = []
    offset = 1
    for _ in range(20):  # Max 20 pages to avoid infinite loop
        params["offset"] = offset
        try:
            resp = requests.get(
                f"{NOAA_CDO_BASE}/data", headers=headers, params=params, timeout=30
            )
            resp.raise_for_status()
            body = resp.json()
            results = body.get("results", [])
            if not results:
                break
            all_records.extend(results)
            metadata = body.get("metadata", {}).get("resultset", {})
            total = metadata.get("count", 0)
            if offset + len(results) > total:
                break
            offset += len(results)
            time.sleep(0.25)  # Respect 5 req/sec limit
        except Exception:
            break

    if not all_records:
        return pd.DataFrame()

    df = pd.DataFrame(all_records)
    df["date"] = pd.to_datetime(df["date"])

    # Pivot so each data type is a column
    if "datatype" in df.columns and "value" in df.columns:
        pivoted = df.pivot_table(
            index="date", columns="datatype", values="value", aggfunc="first"
        )
        pivoted.index.name = "date"
        if cache and not pivoted.empty:
            _cache_set(cache_key, pivoted)
        return pivoted

    return pd.DataFrame()


# Common NOAA weather stations for major US cities
NOAA_STATIONS = {
    "NYC": "GHCND:USW00094728",       # Central Park
    "LAX": "GHCND:USW00023174",       # LA International Airport
    "ORD": "GHCND:USW00094846",       # Chicago O'Hare
    "DFW": "GHCND:USW00003927",       # Dallas/Fort Worth
    "ATL": "GHCND:USW00013874",       # Atlanta Hartsfield
    "MIA": "GHCND:USW00012839",       # Miami International
    "SEA": "GHCND:USW00024233",       # Seattle-Tacoma
    "DEN": "GHCND:USW00003017",       # Denver International
    "IAH": "GHCND:USW00012960",       # Houston Intercontinental
    "BOS": "GHCND:USW00014739",       # Boston Logan
}


# ---------------------------------------------------------------------------
# ALT DATA: Steam Player Counts (free, no key)
# ---------------------------------------------------------------------------
# Major game App IDs on Steam (for tracking gaming engagement)
STEAM_GAME_IDS = {
    "CS2": 730,              # Counter-Strike 2 (Valve)
    "Dota2": 570,            # Dota 2 (Valve)
    "PUBG": 578080,          # PUBG (Krafton)
    "Apex": 1172470,         # Apex Legends (EA)
    "GTA5": 271590,          # GTA V (TTWO)
    "Elden_Ring": 1245620,   # Elden Ring (Bandai Namco)
    "Rust": 252490,          # Rust (Facepunch)
    "TF2": 440,              # Team Fortress 2 (Valve)
    "Civ6": 289070,          # Civilization VI (TTWO)
    "Destiny2": 1085660,     # Destiny 2 (Bungie/Sony)
    "Baldurs_Gate3": 1086940,  # BG3 (Hasbro/Larian)
    "Palworld": 1623730,     # Palworld
    "Helldivers2": 553850,   # Helldivers 2 (Sony)
    "Path_of_Exile2": 2694490,  # PoE 2 (Tencent/GGG)
}

# Map game publishers to stock tickers
STEAM_GAME_TICKERS = {
    "CS2": None,        # Valve (private)
    "Dota2": None,      # Valve (private)
    "PUBG": None,       # Krafton (Korean-listed)
    "Apex": "EA",       # Electronic Arts
    "GTA5": "TTWO",     # Take-Two Interactive
    "Elden_Ring": None,  # Bandai Namco (Japanese-listed)
    "Rust": None,       # Facepunch (private)
    "TF2": None,        # Valve (private)
    "Civ6": "TTWO",     # Take-Two Interactive
    "Destiny2": "SONY", # Bungie owned by Sony
    "Baldurs_Gate3": "HAS",  # Hasbro (D&D IP owner)
    "Palworld": None,   # Pocketpair (private)
    "Helldivers2": "SONY",  # Sony
    "Path_of_Exile2": None,  # Tencent/GGG
}


def fetch_steam_player_count(app_id: int) -> int | None:
    """Fetch current player count for a Steam game.

    No API key needed. Free endpoint.

    Args:
        app_id: Steam application ID (e.g., 730 for CS2).

    Returns:
        Current number of players, or None on failure.
    """
    url = f"https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
    try:
        resp = requests.get(url, params={"appid": app_id}, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", {}).get("player_count")
    except Exception:
        return None


def fetch_steam_all_players(cache: bool = True) -> dict[str, int]:
    """Fetch current player counts for all tracked Steam games.

    No API key needed. Returns {game_name: player_count}.

    Trading signal: Aggregate Steam players = overall gaming engagement.
        Compare week-over-week. Rising = bullish gaming sector.
        Track specific games for publisher stock signals (EA, TTWO, SONY).
    Sectors: Gaming (EA, TTWO, RBLX, SONY, NTDOY), GPU demand (NVDA, AMD).
    """
    cache_key = "steam_players_all"
    if cache:
        cached = _cache_get(cache_key, max_age_hours=1)
        if cached is not None:
            return cached.to_dict().get("players", {})

    results = {}
    for name, app_id in STEAM_GAME_IDS.items():
        count = fetch_steam_player_count(app_id)
        if count is not None:
            results[name] = count
        time.sleep(0.1)  # Be polite

    if cache and results:
        df = pd.DataFrame({"players": results})
        _cache_set(cache_key, df)

    return results


def fetch_steam_gaming_index(cache: bool = True) -> dict[str, Any]:
    """Compute a gaming engagement index from Steam player data.

    Returns dict with total players, per-ticker aggregation, and
    comparison to help assess gaming sector health.
    """
    players = fetch_steam_all_players(cache=cache)
    if not players:
        return {"total_players": 0, "by_ticker": {}, "games": {}}

    total = sum(players.values())

    # Aggregate by stock ticker
    by_ticker: dict[str, int] = {}
    for game, count in players.items():
        ticker = STEAM_GAME_TICKERS.get(game)
        if ticker:
            by_ticker[ticker] = by_ticker.get(ticker, 0) + count

    return {
        "total_players": total,
        "by_ticker": by_ticker,
        "games": players,
        "timestamp": datetime.now().isoformat(),
    }


# ---------------------------------------------------------------------------
# ALT DATA: DeFi Llama — TVL & Protocol Data (free, no key)
# ---------------------------------------------------------------------------
DEFILLAMA_BASE = "https://api.llama.fi"


def fetch_defi_tvl_all(cache: bool = True) -> pd.DataFrame:
    """Fetch current TVL for all DeFi protocols from DeFi Llama.

    Free API, no key needed. Returns DataFrame with protocol name, chain,
    TVL, and 24h/7d changes.

    Trading signal: Total DeFi TVL = crypto risk appetite indicator.
        Rising TVL = bullish crypto. Rapid TVL decline = potential contagion.
    Sectors: Crypto (COIN, MARA, RIOT, MSTR), DeFi tokens.
    """
    cache_key = "defillama_protocols"
    if cache:
        cached = _cache_get(cache_key, max_age_hours=4)
        if cached is not None:
            return cached

    try:
        resp = requests.get(f"{DEFILLAMA_BASE}/protocols", timeout=30)
        resp.raise_for_status()
        protocols = resp.json()

        rows = []
        for p in protocols:
            rows.append({
                "name": p.get("name", ""),
                "symbol": p.get("symbol", ""),
                "chain": p.get("chain", ""),
                "tvl": p.get("tvl", 0),
                "change_1d": p.get("change_1d", 0),
                "change_7d": p.get("change_7d", 0),
                "category": p.get("category", ""),
                "chains": ",".join(p.get("chains", [])),
            })

        df = pd.DataFrame(rows)
        if cache and not df.empty:
            _cache_set(cache_key, df)
        return df
    except Exception:
        return pd.DataFrame()


def fetch_defi_chain_tvl(chain: str = "Ethereum", cache: bool = True) -> pd.DataFrame:
    """Fetch historical TVL for a specific blockchain from DeFi Llama.

    Args:
        chain: Chain name (Ethereum, BSC, Solana, Avalanche, Polygon, etc.)

    Returns:
        DataFrame with DatetimeIndex and 'tvl' column.
    """
    cache_key = f"defillama_chain_{chain}"
    if cache:
        cached = _cache_get(cache_key, max_age_hours=12)
        if cached is not None:
            return cached

    try:
        resp = requests.get(
            f"{DEFILLAMA_BASE}/v2/historicalChainTvl/{chain}", timeout=30
        )
        resp.raise_for_status()
        data = resp.json()

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"], unit="s")
        df = df.set_index("date")
        df.index.name = "date"

        if cache and not df.empty:
            _cache_set(cache_key, df)
        return df
    except Exception:
        return pd.DataFrame()


def fetch_defi_total_tvl(cache: bool = True) -> pd.DataFrame:
    """Fetch historical total DeFi TVL across all chains.

    Returns DataFrame with DatetimeIndex and 'tvl' column.
    Great for crypto market health dashboard.
    """
    cache_key = "defillama_total_tvl"
    if cache:
        cached = _cache_get(cache_key, max_age_hours=12)
        if cached is not None:
            return cached

    try:
        resp = requests.get(
            f"{DEFILLAMA_BASE}/v2/historicalChainTvl", timeout=30
        )
        resp.raise_for_status()
        data = resp.json()

        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)
        df["date"] = pd.to_datetime(df["date"], unit="s")
        df = df.set_index("date")
        df.index.name = "date"

        if cache and not df.empty:
            _cache_set(cache_key, df)
        return df
    except Exception:
        return pd.DataFrame()


# ---------------------------------------------------------------------------
# ALT DATA: Reddit/WSB Sentiment — ApeWisdom (free, no key)
# ---------------------------------------------------------------------------
def fetch_reddit_trending_stocks(
    filter_name: str = "all-stocks",
    pages: int = 1,
    cache: bool = True,
) -> pd.DataFrame:
    """Fetch trending stock mentions from Reddit via ApeWisdom API.

    Free API, no key needed. Tracks mentions across r/wallstreetbets,
    r/stocks, r/investing, and other finance subreddits.

    Args:
        filter_name: Filter type. Options:
            'all-stocks' — all stock-focused subreddits
            'all-crypto' — crypto subreddits
            'wallstreetbets' — WSB only
            'stocks' — r/stocks only
            'investing' — r/investing only
        pages: Number of pages (100 results per page).
        cache: Cache results for 1 hour.

    Returns:
        DataFrame with columns: rank, ticker, name, mentions, upvotes,
        rank_24h_ago, mentions_24h_ago.

    Trading signal: Spike in mentions = retail attention. High upvotes/mention
        ratio = strong conviction. Compare rank_24h_ago for momentum.
    Sectors: Meme stocks, small/mid caps, whatever Reddit is excited about.
    """
    cache_key = f"reddit_trending_{filter_name}_p{pages}"
    if cache:
        cached = _cache_get(cache_key, max_age_hours=1)
        if cached is not None:
            return cached

    all_results = []
    for page in range(1, pages + 1):
        try:
            url = f"https://apewisdom.io/api/v1.0/filter/{filter_name}/page/{page}"
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            results = data.get("results", [])
            if not results:
                break
            all_results.extend(results)
            time.sleep(0.5)  # Be polite
        except Exception:
            break

    if not all_results:
        return pd.DataFrame()

    df = pd.DataFrame(all_results)
    # Keep useful columns
    keep_cols = ["rank", "ticker", "name", "mentions", "upvotes",
                 "rank_24h_ago", "mentions_24h_ago"]
    available = [c for c in keep_cols if c in df.columns]
    df = df[available]

    if cache and not df.empty:
        _cache_set(cache_key, df)
    return df


def fetch_reddit_stock_sentiment(ticker: str) -> dict[str, Any]:
    """Get Reddit sentiment summary for a specific stock ticker.

    Searches current trending data for the ticker.
    Returns dict with mentions, rank, upvotes, and 24h changes.
    """
    df = fetch_reddit_trending_stocks(filter_name="all-stocks", pages=3)
    if df.empty:
        return {"ticker": ticker, "found": False}

    match = df[df["ticker"].str.upper() == ticker.upper()]
    if match.empty:
        return {"ticker": ticker, "found": False, "note": "Not in top 300 trending"}

    row = match.iloc[0].to_dict()
    row["found"] = True
    return row


# ---------------------------------------------------------------------------
# ALT DATA: OpenSky Network — Flight Tracking (free, no key for anonymous)
# ---------------------------------------------------------------------------
OPENSKY_BASE = "https://opensky-network.org/api"


def fetch_opensky_flights(
    airport: str,
    direction: str = "departure",
    hours_back: int = 24,
) -> list[dict[str, Any]]:
    """Fetch recent flights from/to an airport via OpenSky Network.

    Free API (anonymous: 400 credits/day). No key needed.

    Args:
        airport: ICAO airport code (e.g., 'KJFK', 'KLAX', 'EGLL', 'RJTT').
        direction: 'departure' or 'arrival'.
        hours_back: Look back this many hours (max 48 for anonymous).

    Returns:
        List of flight dicts with icao24, callsign, departure/arrival airports,
        and timestamps.

    Trading signal: Flight counts at major airports = air travel demand proxy.
    Sectors: Airlines, travel, aerospace.
    """
    end_ts = int(time.time())
    begin_ts = end_ts - (hours_back * 3600)

    endpoint = "departure" if direction == "departure" else "arrival"
    url = f"{OPENSKY_BASE}/flights/{endpoint}"
    params = {"airport": airport, "begin": begin_ts, "end": end_ts}

    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return []


# Common ICAO airport codes for tracking
AIRPORTS = {
    "JFK": "KJFK", "LAX": "KLAX", "ORD": "KORD", "ATL": "KATL",
    "DFW": "KDFW", "SFO": "KSFO", "MIA": "KMIA", "SEA": "KSEA",
    "LHR": "EGLL", "CDG": "LFPG", "FRA": "EDDF", "NRT": "RJAA",
    "HND": "RJTT", "PEK": "ZBAA", "SIN": "WSSS", "DXB": "OMDB",
}


# ---------------------------------------------------------------------------
# Convenience: multi-asset data bundle
# ---------------------------------------------------------------------------
def fetch_asset_bundle(
    symbols: list[str],
    start: str = "2020-01-01",
    end: str | None = None,
    include_fundamentals: bool = False,
) -> dict[str, Any]:
    """Fetch a complete data bundle for backtesting.

    Returns: {symbol: {"ohlcv": DataFrame, "fundamentals": dict (optional)}}
    """
    ohlcv_data = fetch_multiple_ohlcv(symbols, start=start, end=end)
    bundle = {}
    for sym in symbols:
        if sym not in ohlcv_data:
            continue
        entry: dict[str, Any] = {"ohlcv": ohlcv_data[sym]}
        if include_fundamentals:
            try:
                entry["fundamentals"] = fetch_fundamentals(sym)
            except Exception:
                entry["fundamentals"] = {}
        bundle[sym] = entry

    return bundle


# ---------------------------------------------------------------------------
# Per-Stock Composite Score (like TipRanks Smart Score)
# ---------------------------------------------------------------------------
def compute_stock_score(symbol: str) -> dict[str, Any]:
    """Compute a 1-10 composite score for a stock.

    Combines fundamental, technical, and momentum factors into a single
    integer score inspired by TipRanks Smart Score / Seeking Alpha Quant.

    Returns dict with: score (1-10), breakdown (sub-scores), raw data used.
    """
    import yfinance as yf

    ticker = yf.Ticker(symbol)
    info = ticker.info

    # --- Fundamental score (0-10 scale, will be weighted) ---
    fund_points = 0.0
    fund_max = 0.0
    fund_details = {}

    pe = info.get("trailingPE")
    if isinstance(pe, (int, float)) and math.isfinite(pe) and pe > 0:
        fund_max += 2.0
        # PE < 15 is cheap, 15-25 is fair, >25 is expensive
        if pe < 15:
            fund_points += 2.0
        elif pe < 25:
            fund_points += 1.0
        else:
            fund_points += 0.0
        fund_details["pe_ratio"] = round(pe, 2)

    pb = info.get("priceToBook")
    if isinstance(pb, (int, float)) and math.isfinite(pb) and pb > 0:
        fund_max += 1.5
        if pb < 1.5:
            fund_points += 1.5
        elif pb < 3.0:
            fund_points += 0.75
        else:
            fund_points += 0.0
        fund_details["pb_ratio"] = round(pb, 2)

    roe = info.get("returnOnEquity")
    if isinstance(roe, (int, float)) and math.isfinite(roe):
        fund_max += 2.0
        if roe > 0.20:
            fund_points += 2.0
        elif roe > 0.10:
            fund_points += 1.0
        elif roe > 0:
            fund_points += 0.5
        fund_details["roe"] = round(roe, 4)

    de = info.get("debtToEquity")
    if isinstance(de, (int, float)) and math.isfinite(de):
        fund_max += 1.5
        if de < 50:
            fund_points += 1.5
        elif de < 100:
            fund_points += 0.75
        else:
            fund_points += 0.0
        fund_details["debt_to_equity"] = round(de, 2)

    div_yield = info.get("dividendYield")
    if isinstance(div_yield, (int, float)) and math.isfinite(div_yield):
        fund_max += 1.0
        if div_yield > 0.03:
            fund_points += 1.0
        elif div_yield > 0.01:
            fund_points += 0.5
        fund_details["dividend_yield"] = round(div_yield, 4)

    rev_growth = info.get("revenueGrowth")
    if isinstance(rev_growth, (int, float)) and math.isfinite(rev_growth):
        fund_max += 2.0
        if rev_growth > 0.20:
            fund_points += 2.0
        elif rev_growth > 0.10:
            fund_points += 1.5
        elif rev_growth > 0.0:
            fund_points += 0.75
        fund_details["revenue_growth"] = round(rev_growth, 4)

    fundamental_score = (fund_points / fund_max * 10) if fund_max > 0 else 5.0

    # --- Technical score (0-10 scale) ---
    tech_points = 0.0
    tech_max = 0.0
    tech_details = {}

    try:
        hist = ticker.history(period="1y")
        if not hist.empty and len(hist) >= 50:
            close = hist["Close"]
            current_price = float(close.iloc[-1])

            # SMA200: price above = bullish
            if len(close) >= 200:
                sma200 = float(close.rolling(200).mean().iloc[-1])
                tech_max += 3.0
                if current_price > sma200:
                    tech_points += 3.0
                elif current_price > sma200 * 0.95:
                    tech_points += 1.5
                tech_details["sma200"] = round(sma200, 2)
                tech_details["above_sma200"] = current_price > sma200

            # RSI: 30-70 is healthy, oversold/overbought are penalized
            delta = close.diff()
            gain = delta.where(delta > 0, 0.0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0.0)).rolling(14).mean()
            rs = gain.iloc[-1] / loss.iloc[-1] if loss.iloc[-1] != 0 else 0
            rsi = 100 - (100 / (1 + rs)) if rs > 0 else 50
            tech_max += 3.0
            if 30 <= rsi <= 70:
                tech_points += 3.0
            elif 20 <= rsi <= 80:
                tech_points += 1.5
            else:
                tech_points += 0.0
            tech_details["rsi_14"] = round(rsi, 2)

            # MACD: positive = bullish
            if len(close) >= 35:
                ema12 = close.ewm(span=12, adjust=False).mean()
                ema26 = close.ewm(span=26, adjust=False).mean()
                macd_line = float((ema12 - ema26).iloc[-1])
                signal_line = float((ema12 - ema26).ewm(span=9, adjust=False).mean().iloc[-1])
                tech_max += 4.0
                if macd_line > signal_line and macd_line > 0:
                    tech_points += 4.0
                elif macd_line > signal_line:
                    tech_points += 2.0
                elif macd_line > 0:
                    tech_points += 1.0
                tech_details["macd"] = round(macd_line, 4)
                tech_details["macd_signal"] = round(signal_line, 4)
                tech_details["macd_bullish"] = macd_line > signal_line

            tech_details["current_price"] = round(current_price, 2)
    except Exception:
        pass

    technical_score = (tech_points / tech_max * 10) if tech_max > 0 else 5.0

    # --- Momentum score (0-10 scale): 3-month return vs SPY ---
    momentum_score = 5.0
    momentum_details = {}
    try:
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
        stock_hist = fetch_ohlcv(symbol, start=start_date, end=end_date)
        spy_hist = fetch_ohlcv("SPY", start=start_date, end=end_date)

        if not stock_hist.empty and not spy_hist.empty and len(stock_hist) > 5:
            stock_ret = float(stock_hist["Close"].iloc[-1] / stock_hist["Close"].iloc[0] - 1)
            spy_ret = float(spy_hist["Close"].iloc[-1] / spy_hist["Close"].iloc[0] - 1)
            relative = stock_ret - spy_ret

            if relative > 0.10:
                momentum_score = 10.0
            elif relative > 0.05:
                momentum_score = 8.0
            elif relative > 0.0:
                momentum_score = 6.5
            elif relative > -0.05:
                momentum_score = 4.0
            elif relative > -0.10:
                momentum_score = 2.5
            else:
                momentum_score = 1.0

            momentum_details["stock_3m_return"] = round(stock_ret, 4)
            momentum_details["spy_3m_return"] = round(spy_ret, 4)
            momentum_details["relative_strength"] = round(relative, 4)
    except Exception:
        pass

    # --- Combine into 1-10 composite ---
    # Weights: fundamentals 40%, technical 35%, momentum 25%
    raw_score = (fundamental_score * 0.40
                 + technical_score * 0.35
                 + momentum_score * 0.25)
    composite = max(1, min(10, round(raw_score)))

    return {
        "symbol": symbol,
        "score": composite,
        "raw_score": round(raw_score, 2),
        "breakdown": {
            "fundamental": round(fundamental_score, 2),
            "technical": round(technical_score, 2),
            "momentum": round(momentum_score, 2),
        },
        "weights": {
            "fundamental": 0.40,
            "technical": 0.35,
            "momentum": 0.25,
        },
        "details": {
            "fundamental": fund_details,
            "technical": tech_details,
            "momentum": momentum_details,
        },
    }


# ---------------------------------------------------------------------------
# Fair Value / DCF Estimator (like Morningstar Stars)
# ---------------------------------------------------------------------------
def estimate_fair_value(symbol: str, discount_rate: float = 0.10,
                        projection_years: int = 5) -> dict[str, Any]:
    """Estimate intrinsic fair value per share using a simple DCF model.

    Uses yfinance fundamentals: freeCashflow, revenueGrowth, sharesOutstanding.
    Discount rate defaults to 10% (typical equity cost of capital).

    Returns dict with: fair_value_per_share, current_price,
    discount_or_premium_pct, rating (undervalued/fair/overvalued), inputs used.
    """
    import yfinance as yf

    ticker = yf.Ticker(symbol)
    info = ticker.info

    current_price = info.get("currentPrice") or info.get("regularMarketPrice")
    fcf = info.get("freeCashflow")
    revenue_growth = info.get("revenueGrowth")
    shares = info.get("sharesOutstanding")

    errors = []
    if not isinstance(current_price, (int, float)) or current_price <= 0:
        errors.append("current_price unavailable")
    if not isinstance(fcf, (int, float)) or fcf <= 0:
        errors.append("freeCashflow unavailable or negative")
    if not isinstance(shares, (int, float)) or shares <= 0:
        errors.append("sharesOutstanding unavailable")

    if errors:
        return {
            "symbol": symbol,
            "error": "Insufficient data for DCF",
            "missing": errors,
            "current_price": current_price if isinstance(current_price, (int, float)) else None,
            "fair_value_per_share": None,
            "discount_or_premium_pct": None,
            "rating": "insufficient_data",
        }

    # Default growth rate: use revenueGrowth if available, else conservative 5%
    if isinstance(revenue_growth, (int, float)) and math.isfinite(revenue_growth):
        growth_rate = max(0.0, min(revenue_growth, 0.30))  # Cap at 30%
    else:
        growth_rate = 0.05
        revenue_growth = None

    # Terminal growth rate (long-term GDP-ish)
    terminal_growth = 0.025

    # Project FCF forward and discount back
    projected_fcf = []
    pv_sum = 0.0
    for year in range(1, projection_years + 1):
        future_fcf = fcf * ((1 + growth_rate) ** year)
        pv = future_fcf / ((1 + discount_rate) ** year)
        pv_sum += pv
        projected_fcf.append({
            "year": year,
            "fcf": round(future_fcf),
            "present_value": round(pv),
        })

    # Terminal value (Gordon Growth Model)
    terminal_fcf = fcf * ((1 + growth_rate) ** projection_years) * (1 + terminal_growth)
    terminal_value = terminal_fcf / (discount_rate - terminal_growth)
    pv_terminal = terminal_value / ((1 + discount_rate) ** projection_years)

    total_value = pv_sum + pv_terminal
    fair_value_per_share = total_value / shares

    # Rating
    if current_price <= 0:
        discount_pct = 0.0
        rating = "insufficient_data"
    else:
        discount_pct = (fair_value_per_share - current_price) / current_price * 100
        if discount_pct > 20:
            rating = "undervalued"
        elif discount_pct > -10:
            rating = "fair_value"
        else:
            rating = "overvalued"

    return {
        "symbol": symbol,
        "fair_value_per_share": round(fair_value_per_share, 2),
        "current_price": round(current_price, 2),
        "discount_or_premium_pct": round(discount_pct, 2),
        "rating": rating,
        "inputs": {
            "free_cash_flow": fcf,
            "growth_rate": round(growth_rate, 4),
            "revenue_growth_raw": round(revenue_growth, 4) if revenue_growth is not None else None,
            "terminal_growth": terminal_growth,
            "discount_rate": discount_rate,
            "shares_outstanding": shares,
            "projection_years": projection_years,
        },
        "projected_fcf": projected_fcf,
        "terminal_value": round(pv_terminal),
        "total_enterprise_value": round(total_value),
    }


# ---------------------------------------------------------------------------
# Alert System: Strategy Trigger Checks
# ---------------------------------------------------------------------------
def check_strategy_triggers() -> dict[str, dict[str, Any]]:
    """Check which of our strategy triggers are currently active.

    Mirrors the actual strategy signal logic from unconventional_strategies.py
    but only checks the current state (no backtesting). Uses live price data
    and SMA calculations to determine if a trigger condition is met.

    Returns dict of {strategy_name: {active, signal, tickers_affected, details}}.
    """
    triggers = {}

    # Helper: get current price and SMA200 for a symbol
    def _get_sma_status(sym: str, sma_days: int = 200) -> dict[str, Any] | None:
        try:
            needed_days = sma_days + 50  # buffer for weekends/holidays
            start = (datetime.now() - timedelta(days=int(needed_days * 1.6))).strftime("%Y-%m-%d")
            df = fetch_ohlcv(sym, start=start)
            if df.empty or len(df) < sma_days:
                return None
            close = df["Close"]
            current = float(close.iloc[-1])
            sma = float(close.rolling(sma_days).mean().iloc[-1])
            return {
                "symbol": sym,
                "current_price": round(current, 2),
                "sma200": round(sma, 2),
                "below_sma200": current < sma,
                "above_sma200": current > sma,
                "distance_pct": round((current / sma - 1) * 100, 2),
            }
        except Exception:
            return None

    # --- 1. Oil Down Tech Up ---
    # Trigger: >=2 of [XLE, XOP, OIH] below SMA200
    energy_symbols = ["XLE", "XOP", "OIH"]
    energy_statuses = {}
    energy_weak = 0
    for sym in energy_symbols:
        status = _get_sma_status(sym)
        if status:
            energy_statuses[sym] = status
            if status["below_sma200"]:
                energy_weak += 1

    triggers["oil_down_tech_up"] = {
        "active": energy_weak >= 2,
        "signal": "Energy sector weak -- capital rotating to tech" if energy_weak >= 2
                  else "Energy sector stable -- no rotation signal",
        "tickers_affected": [s for s, st in energy_statuses.items() if st["below_sma200"]],
        "details": energy_statuses,
        "threshold": ">=2 of XLE/XOP/OIH below SMA200",
    }

    # --- 2. VIX Spike Buyback ---
    # Trigger: VXX > 1.3x its SMA200
    vxx_status = _get_sma_status("VXX")
    vix_active = False
    vix_signal = "VXX data unavailable"
    if vxx_status:
        vix_active = vxx_status["current_price"] > vxx_status["sma200"] * 1.3
        if vix_active:
            vix_signal = f"VXX at {vxx_status['current_price']} > 1.3x SMA200 ({vxx_status['sma200']}) -- fear spike, buy cash-rich buyback stocks"
        else:
            vix_signal = f"VXX at {vxx_status['current_price']} vs SMA200 {vxx_status['sma200']} -- no fear spike"

    triggers["vix_spike_buyback"] = {
        "active": vix_active,
        "signal": vix_signal,
        "tickers_affected": ["VXX"] if vix_active else [],
        "details": {"VXX": vxx_status} if vxx_status else {},
        "threshold": "VXX > 1.3x SMA200",
    }

    # --- 3. Job Loss Tech Boom ---
    # Trigger: >=2 of [MAN, RHI, ASGN, ADP] below SMA200
    staffing_symbols = ["MAN", "RHI", "ASGN", "ADP"]
    staffing_statuses = {}
    staffing_weak = 0
    for sym in staffing_symbols:
        status = _get_sma_status(sym)
        if status:
            staffing_statuses[sym] = status
            if status["below_sma200"]:
                staffing_weak += 1

    triggers["job_loss_tech_boom"] = {
        "active": staffing_weak >= 2,
        "signal": "Staffing stocks weak -- automation/tech adoption accelerating" if staffing_weak >= 2
                  else "Staffing sector stable -- no automation signal",
        "tickers_affected": [s for s, st in staffing_statuses.items() if st["below_sma200"]],
        "details": staffing_statuses,
        "threshold": ">=2 of MAN/RHI/ASGN/ADP below SMA200",
    }

    # --- 4. Wealth Barometer ---
    # Trigger: >=1 of [DLTR, DG] below SMA200 AND COST above SMA200
    dollar_symbols = ["DLTR", "DG"]
    dollar_statuses = {}
    dollar_weak = 0
    for sym in dollar_symbols:
        status = _get_sma_status(sym)
        if status:
            dollar_statuses[sym] = status
            if status["below_sma200"]:
                dollar_weak += 1

    cost_status = _get_sma_status("COST")
    cost_strong = False
    if cost_status:
        dollar_statuses["COST"] = cost_status
        cost_strong = cost_status["above_sma200"]

    wealth_active = dollar_weak >= 1 and cost_strong
    if wealth_active:
        wealth_signal = "K-shaped economy: dollar stores weak, Costco strong -- long quality/luxury"
    elif dollar_weak >= 1:
        wealth_signal = "Dollar stores weak but Costco also weak -- broad consumer stress"
    else:
        wealth_signal = "Dollar stores stable -- no K-shape signal"

    triggers["wealth_barometer"] = {
        "active": wealth_active,
        "signal": wealth_signal,
        "tickers_affected": [s for s, st in dollar_statuses.items()
                             if (s in ("DLTR", "DG") and st["below_sma200"])
                             or (s == "COST" and st["above_sma200"] and dollar_weak >= 1)],
        "details": dollar_statuses,
        "threshold": ">=1 of DLTR/DG below SMA200 AND COST above SMA200",
    }

    return triggers


if __name__ == "__main__":
    print(summarize_api_keys())
    print("\n=== Testing AAPL OHLCV fetch ===")
    df = fetch_ohlcv("AAPL", start="2024-01-01")
    print(f"Fetched {len(df)} rows for AAPL")
    print(df.tail())

    # --- Alternative data tests ---
    print("\n=== Alternative Data Sources ===")

    print("\n--- Steam Player Counts ---")
    try:
        steam = fetch_steam_all_players(cache=False)
        for game, count in sorted(steam.items(), key=lambda x: -x[1])[:5]:
            print(f"  {game}: {count:,} players")
        idx = fetch_steam_gaming_index(cache=False)
        print(f"  Total: {idx['total_players']:,} | By ticker: {idx['by_ticker']}")
    except Exception as e:
        print(f"  Steam error: {e}")

    print("\n--- Reddit Trending Stocks (ApeWisdom) ---")
    try:
        reddit = fetch_reddit_trending_stocks(pages=1, cache=False)
        if not reddit.empty:
            print(reddit.head(10).to_string(index=False))
    except Exception as e:
        print(f"  Reddit error: {e}")

    print("\n--- DeFi Llama Total TVL ---")
    try:
        tvl = fetch_defi_total_tvl(cache=False)
        if not tvl.empty:
            print(f"  Latest TVL: ${tvl.iloc[-1]['tvl']:,.0f}")
            print(f"  Data range: {tvl.index[0].date()} to {tvl.index[-1].date()}")
    except Exception as e:
        print(f"  DeFi Llama error: {e}")

    print("\n--- TSA Checkpoint Data ---")
    try:
        tsa = fetch_tsa_checkpoint(cache=False)
        if not tsa.empty:
            print(f"  Columns: {list(tsa.columns)}")
            print(f"  Latest: {tsa.index[-1].date()} — {tsa.iloc[-1].to_dict()}")
    except Exception as e:
        print(f"  TSA error: {e}")

    print("\n--- Google Trends (requires pytrends) ---")
    try:
        gt = fetch_google_trends(["NVDA", "TSLA"], timeframe="today 3-m", cache=False)
        if not gt.empty:
            print(f"  Fetched {len(gt)} data points for NVDA, TSLA trends")
            print(gt.tail(5))
    except ImportError:
        print("  pytrends not installed (pip install pytrends)")
    except Exception as e:
        print(f"  Google Trends error: {e}")

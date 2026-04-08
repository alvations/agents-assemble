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
from datetime import datetime, timedelta
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
        # Intraday data goes stale within minutes; 12h TTL would serve
        # morning data all day.  Use 30min TTL for sub-daily intervals.
        intraday = interval in ("1m", "2m", "5m", "15m", "30m", "60m", "90m", "1h")
        cached = _cache_get(cache_key, max_age_hours=0.5 if intraday else 12)
        if cached is not None:
            return cached

    ticker = yf.Ticker(symbol)
    df = ticker.history(start=start, end=end, interval=interval)

    if df.empty:
        raise ValueError(f"No data returned for {symbol}")

    # Drop rows where Close is NaN (e.g., delisted/suspended tickers)
    if "Close" in df.columns:
        df = df.dropna(subset=["Close"])
        if df.empty:
            raise ValueError(f"No valid price data for {symbol} (all Close values NaN)")

    if cache:
        _cache_set(cache_key, df)

    return df


def fetch_multiple_ohlcv(
    symbols: list[str],
    start: str = "2020-01-01",
    end: str | None = None,
    interval: str = "1d",
) -> dict[str, pd.DataFrame]:
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

    # Try batch download for uncached symbols (only when >1, since
    # yf.download with a single-element list + group_by="ticker" returns
    # multi-level columns inconsistent with fetch_ohlcv's Ticker.history())
    if len(uncached) > 1:
        try:
            data = yf.download(uncached, start=start, end=end, interval=interval, group_by="ticker", progress=False)
            for sym in uncached:
                try:
                    df = data[sym].dropna(how="all")
                    if "Close" in df.columns:
                        df = df.dropna(subset=["Close"])
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


def fetch_fundamentals(symbol: str) -> dict[str, Any]:
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
                pos = df.index.get_indexer([idx], method="nearest")[0]
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
                {"date": str(idx), **{col: row[col] for col in cal.columns}}
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
        if hist is None or len(hist) < 20:
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
    def _valid(v: Any) -> bool:
        """Check if a fundamental value is present and numeric (not None/NaN)."""
        return v is not None and not (isinstance(v, float) and v != v)

    results = []
    for sym in symbols:
        try:
            f = fetch_fundamentals(sym)
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
        except Exception:
            pass
    return results


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


if __name__ == "__main__":
    print(summarize_api_keys())
    print("\n=== Testing AAPL OHLCV fetch ===")
    df = fetch_ohlcv("AAPL", start="2024-01-01")
    print(f"Fetched {len(df)} rows for AAPL")
    print(df.tail())

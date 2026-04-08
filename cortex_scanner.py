"""Cortex AI Custom Scanner — natural language stock screening.

Users describe what they want in plain English, and the scanner
translates it into technical filters and returns matching stocks.

Usage:
    from cortex_scanner import CortexScanner
    scanner = CortexScanner()
    results = scanner.scan("stocks with RSI below 30 and price above SMA200")
    results = scanner.scan("high dividend yield above 4% in S&P 500")
    results = scanner.scan("tech stocks making new 52-week highs")

Works without any API keys — uses yfinance + our data_fetcher.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

from data_fetcher import fetch_ohlcv, UNIVERSE


# ---------------------------------------------------------------------------
# Natural language parser
# ---------------------------------------------------------------------------
FILTER_PATTERNS = {
    # RSI filters
    r"rsi\s*(?:below|under|<)\s*(\d+)": lambda m, d: d.get("rsi_14", 50) < float(m.group(1)),
    r"rsi\s*(?:above|over|>)\s*(\d+)": lambda m, d: d.get("rsi_14", 50) > float(m.group(1)),
    r"oversold": lambda m, d: d.get("rsi_14", 50) < 30,
    r"overbought": lambda m, d: d.get("rsi_14", 50) > 70,

    # Price vs SMA
    r"(?:price\s*)?above\s*sma\s*200": lambda m, d: d["price"] > d.get("sma_200", 0) if d.get("sma_200") else False,
    r"(?:price\s*)?below\s*sma\s*200": lambda m, d: d["price"] < d.get("sma_200", float("inf")) if d.get("sma_200") else False,
    r"(?:price\s*)?above\s*sma\s*50": lambda m, d: d["price"] > d.get("sma_50", 0) if d.get("sma_50") else False,
    r"golden\s*cross": lambda m, d: d.get("sma_50", 0) > d.get("sma_200", float("inf")) if d.get("sma_200") else False,
    r"death\s*cross": lambda m, d: d.get("sma_50", float("inf")) < d.get("sma_200", 0) if d.get("sma_200") else False,

    # 52-week
    r"(?:new\s*)?52.?week\s*high": lambda m, d: d.get("near_52w_high", False),
    r"near\s*52.?week\s*low": lambda m, d: d.get("near_52w_low", False),

    # Volume
    r"high\s*volume": lambda m, d: d.get("vol_ratio", 1) > 1.5,
    r"volume\s*spike": lambda m, d: d.get("vol_ratio", 1) > 2.0,

    # MACD
    r"macd\s*(?:bullish|positive|above)": lambda m, d: d.get("macd", 0) > d.get("macd_signal", 0) if d.get("macd") is not None else False,
    r"macd\s*(?:bearish|negative|below)": lambda m, d: d.get("macd", 0) < d.get("macd_signal", 0) if d.get("macd") is not None else False,

    # Momentum
    r"momentum": lambda m, d: d["price"] > d.get("sma_50", 0) and d.get("sma_50", 0) > d.get("sma_200", 0) if d.get("sma_200") else False,
    r"uptrend": lambda m, d: d["price"] > d.get("sma_50", 0) if d.get("sma_50") else False,
    r"downtrend": lambda m, d: d["price"] < d.get("sma_50", float("inf")) if d.get("sma_50") else False,

    # Volatility
    r"low\s*vol": lambda m, d: d.get("annual_vol", 0.20) < 0.20,
    r"high\s*vol": lambda m, d: d.get("annual_vol", 0.20) > 0.35,
}

UNIVERSE_PATTERNS = {
    r"s&?p\s*500|large\s*cap|mega\s*cap|blue\s*chip": "mega_cap",
    r"tech|technology|software": "mega_cap",  # Mostly tech in mega_cap
    r"small\s*cap": "small_cap",
    r"mid\s*cap": "mid_cap",
    r"dividend": "dividend_aristocrats",
    r"energy|oil": "commodities",
    r"china|chinese": "china_adr",
    r"biotech|pharma": "glp1_obesity",
    r"crypto": "crypto_adjacent",
    r"defense|military": "defense_niche",
    r"semiconductor|chip": "semiconductor",
    r"gold|silver|precious": "precious_metals",
}


class CortexScanner:
    """Natural language stock screener."""

    def scan(self, query: str, max_results: int = 20) -> List[Dict[str, Any]]:
        """Scan stocks matching a natural language query.

        Examples:
            "stocks with RSI below 30 and price above SMA200"
            "tech stocks in uptrend with high volume"
            "oversold dividend stocks"
            "small cap stocks making new 52-week highs"
        """
        query_lower = query.lower()

        # Determine universe
        universe_syms = self._pick_universe(query_lower)

        # Parse filters
        filters = self._parse_filters(query_lower)

        # Screen
        results = []
        for sym in universe_syms[:50]:  # Limit for speed
            try:
                data = self._get_stock_data(sym)
                if data is None:
                    continue

                # Apply all filters
                passes = True
                for filt in filters:
                    try:
                        if not filt(data):
                            passes = False
                            break
                    except (TypeError, KeyError):
                        passes = False
                        break

                if passes:
                    results.append(data)
            except Exception:
                pass

        results.sort(key=lambda x: x.get("rsi_14", 50))
        return results[:max_results]

    def _pick_universe(self, query: str) -> List[str]:
        for pattern, cat in UNIVERSE_PATTERNS.items():
            if re.search(pattern, query):
                return UNIVERSE.get(cat, UNIVERSE["mega_cap"])
        # Default: combine mega + growth + value
        return list(set(UNIVERSE["mega_cap"] + UNIVERSE["growth"] + UNIVERSE["value"]))

    def _parse_filters(self, query: str) -> list:
        filters = []
        for pattern, fn in FILTER_PATTERNS.items():
            match = re.search(pattern, query)
            if match:
                filters.append(lambda d, m=match, f=fn: f(m, d))
        if not filters:
            # Default: show uptrending stocks
            filters.append(lambda d: d["price"] > d.get("sma_50", 0) if d.get("sma_50") else True)
        return filters

    def _get_stock_data(self, symbol: str) -> Optional[Dict]:
        try:
            df = fetch_ohlcv(symbol, start="2024-01-01", cache=True)
            if df.empty or len(df) < 20:
                return None
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)

            close = df["Close"]
            price = float(close.iloc[-1])
            high_252 = float(df["High"].tail(252).max()) if len(df) >= 252 else float(df["High"].max())
            low_252 = float(df["Low"].tail(252).min()) if len(df) >= 252 else float(df["Low"].min())

            # Indicators
            sma50 = float(close.rolling(50).mean().iloc[-1]) if len(close) >= 50 else None
            sma200 = float(close.rolling(200).mean().iloc[-1]) if len(close) >= 200 else None
            delta = close.diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss.replace(0, np.nan)
            rsi_series = 100 - (100 / (1 + rs))
            rsi = float(rsi_series.iloc[-1]) if not pd.isna(rsi_series.iloc[-1]) else 50

            ema12 = close.ewm(span=12).mean()
            ema26 = close.ewm(span=26).mean()
            macd = float((ema12 - ema26).iloc[-1])
            macd_signal = float((ema12 - ema26).ewm(span=9).mean().iloc[-1])

            vol_20 = float(close.pct_change().tail(20).std())
            vol_avg = float(df["Volume"].rolling(20).mean().iloc[-1]) if "Volume" in df.columns else 0
            vol_ratio = float(df["Volume"].iloc[-1] / vol_avg) if vol_avg > 0 else 1

            return {
                "symbol": symbol,
                "price": price,
                "sma_50": sma50,
                "sma_200": sma200,
                "rsi_14": rsi,
                "macd": macd,
                "macd_signal": macd_signal,
                "annual_vol": vol_20 * (252 ** 0.5),
                "vol_ratio": vol_ratio,
                "52w_high": high_252,
                "52w_low": low_252,
                "near_52w_high": price >= high_252 * 0.95,
                "near_52w_low": price <= low_252 * 1.05,
                "pct_from_high": (price - high_252) / high_252,
                "pct_from_low": (price - low_252) / low_252,
                "tradingview": f"https://www.tradingview.com/chart/?symbol={symbol}",
            }
        except Exception:
            return None


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "oversold stocks above SMA200"
    scanner = CortexScanner()
    print(f"\n  Cortex Scan: \"{query}\"\n")
    results = scanner.scan(query)
    print(f"  {'Symbol':>6s} | {'Price':>8s} | {'RSI':>5s} | {'vs SMA50':>8s} | {'vs 52wH':>8s} | {'Vol':>5s}")
    print(f"  {'-'*55}")
    for r in results:
        sma50_pct = f"{(r['price']/r['sma_50']-1)*100:+.1f}%" if r.get("sma_50") else "N/A"
        high_pct = f"{r['pct_from_high']*100:+.1f}%"
        print(f"  {r['symbol']:>6s} | ${r['price']:>7.2f} | {r['rsi_14']:>4.0f} | {sma50_pct:>8s} | {high_pct:>8s} | {r['annual_vol']*100:.0f}%")
    print(f"\n  {len(results)} stocks found")

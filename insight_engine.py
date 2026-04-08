"""Insight Engine Custom Scanner — Claude-powered natural language stock screening.

Uses claude_code_client to interpret natural language queries into
technical screening criteria, then scans the universe for matches.

Usage:
    from insight_engine import InsightEngine
    scanner = InsightEngine()

    # Claude interprets your query and screens stocks
    results = scanner.scan("find me oversold tech stocks that are still above their 200-day average")
    results = scanner.scan("which energy stocks have the best momentum right now?")
    results = scanner.scan("show me cheap dividend stocks with low volatility")

    # Also works without Claude (falls back to keyword matching)
    results = scanner.scan("RSI below 30 above SMA200", use_claude=False)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
import math

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from data_fetcher import fetch_ohlcv, UNIVERSE


class InsightEngine:
    """AI-powered stock screener using Claude + technical data."""

    def __init__(self):
        self._claude = None

    def _get_claude(self):
        if self._claude is None:
            try:
                from claude_code_client import ClaudeClient
                self._claude = ClaudeClient()
            except Exception:
                self._claude = False  # Mark as unavailable
        return self._claude if self._claude else None

    def scan(self, query: str, universe: str = "auto", max_results: int = 20,
             use_claude: bool = True) -> dict:
        """Scan stocks using natural language.

        1. If use_claude=True: Claude interprets the query into screening criteria
        2. Fetches data for the appropriate universe
        3. Screens and ranks results
        4. Returns structured results with live price links

        Returns:
            Dict with 'query', 'interpretation', 'criteria', 'results', 'count'
        """
        # Step 1: Interpret query (Claude or fallback)
        if use_claude:
            interpretation = self._claude_interpret(query)
        else:
            interpretation = self._keyword_interpret(query)

        if not interpretation:
            interpretation = self._keyword_interpret(query)

        # Step 2: Pick universe
        symbols = self._pick_universe(query, universe)

        # Step 3: Screen stocks
        results = []
        for sym in symbols[:60]:  # Limit for speed
            try:
                data = self._get_stock_data(sym)
                if data and self._passes_criteria(data, interpretation.get("criteria", {})):
                    data["match_reason"] = interpretation.get("description", query)
                    results.append(data)
            except Exception:
                pass

        # Step 4: Rank by the interpretation's sort key
        sort_key = interpretation.get("sort_by", "rsi_14")
        sort_asc = interpretation.get("sort_ascending", True)
        results.sort(key=lambda x: x.get(sort_key, 0), reverse=not sort_asc)

        return {
            "query": query,
            "interpretation": interpretation.get("description", ""),
            "criteria": interpretation.get("criteria", {}),
            "results": results[:max_results],
            "count": len(results),
            "universe_scanned": len(symbols),
        }

    # ----- Claude interpretation -----

    def _claude_interpret(self, query: str) -> dict | None:
        """Use Claude to interpret a natural language screening query."""
        claude = self._get_claude()
        if not claude:
            return None

        prompt = f"""You are a stock screening assistant. Interpret this query into technical screening criteria.

Query: "{query}"

Return ONLY a JSON object (no other text) with these fields:
{{
    "description": "one-line description of what user wants",
    "universe": "mega_cap|small_cap|dividend|energy|tech|china|all",
    "criteria": {{
        "rsi_max": null or number (e.g. 30 for oversold),
        "rsi_min": null or number (e.g. 70 for overbought),
        "above_sma200": true/false/null,
        "above_sma50": true/false/null,
        "golden_cross": true/false/null,
        "min_vol_ratio": null or number (e.g. 1.5 for high volume),
        "macd_bullish": true/false/null,
        "near_52w_high": true/false/null,
        "near_52w_low": true/false/null,
        "max_annual_vol": null or number (e.g. 0.20 for low vol),
        "min_annual_vol": null or number
    }},
    "sort_by": "rsi_14|price|annual_vol|vol_ratio|pct_from_high",
    "sort_ascending": true/false
}}"""

        try:
            result = claude.ask(prompt)
            text = result.text.strip()
            # Extract JSON from response
            json_match = re.search(r'\{[\s\S]*\}', text)
            if json_match:
                return json.loads(json_match.group())
        except Exception:
            pass
        return None

    # ----- Keyword fallback interpretation -----

    def _keyword_interpret(self, query: str) -> dict:
        q = query.lower()
        criteria = {}
        description = query

        if any(w in q for w in ["oversold", "rsi below", "rsi under"]):
            m = re.search(r"rsi\s*(?:below|under|<)\s*(\d+)", q)
            criteria["rsi_max"] = int(m.group(1)) if m else 30

        if any(w in q for w in ["overbought", "rsi above", "rsi over"]):
            m = re.search(r"rsi\s*(?:above|over|>)\s*(\d+)", q)
            criteria["rsi_min"] = int(m.group(1)) if m else 70

        if "above sma200" in q or "above 200" in q:
            criteria["above_sma200"] = True
        if "below sma200" in q or "below 200" in q:
            criteria["above_sma200"] = False

        if "above sma50" in q or "uptrend" in q or "momentum" in q:
            criteria["above_sma50"] = True

        if "golden cross" in q:
            criteria["golden_cross"] = True

        if "high volume" in q or "volume spike" in q:
            criteria["min_vol_ratio"] = 1.5

        if "52 week high" in q or "52w high" in q or "new high" in q:
            criteria["near_52w_high"] = True
        if "52 week low" in q or "52w low" in q:
            criteria["near_52w_low"] = True

        if "low vol" in q:
            criteria["max_annual_vol"] = 0.20
        if "high vol" in q:
            criteria["min_annual_vol"] = 0.35

        if "macd bullish" in q or "macd positive" in q:
            criteria["macd_bullish"] = True

        sort_by = "rsi_14"
        sort_asc = True
        if "momentum" in q or "uptrend" in q:
            sort_by = "pct_from_high"
            sort_asc = False
        if "volume" in q:
            sort_by = "vol_ratio"
            sort_asc = False
        elif "vol" in q:
            sort_by = "annual_vol"
            sort_asc = "low" in q

        return {
            "description": description,
            "criteria": criteria,
            "sort_by": sort_by,
            "sort_ascending": sort_asc,
        }

    # ----- Screening logic -----

    def _passes_criteria(self, data: dict, criteria: dict) -> bool:
        if not criteria:
            return True
        for key, val in criteria.items():
            if val is None:
                continue
            if key == "rsi_max" and data.get("rsi_14", 50) > val:
                return False
            if key == "rsi_min" and data.get("rsi_14", 50) < val:
                return False
            if key == "above_sma200" and val:
                if data.get("sma_200") is None or data["price"] <= data["sma_200"]:
                    return False
            if key == "above_sma200" and not val:
                if data.get("sma_200") is not None and data["price"] > data["sma_200"]:
                    return False
            if key == "above_sma50" and val:
                if data.get("sma_50") is None or data["price"] <= data["sma_50"]:
                    return False
            if key == "golden_cross" and val:
                if data.get("sma_50") is None or data.get("sma_200") is None or data["sma_50"] <= data["sma_200"]:
                    return False
            if key == "min_vol_ratio" and data.get("vol_ratio", 1) < val:
                return False
            if key == "macd_bullish" and val:
                if data.get("macd") is None or data["macd"] <= data.get("macd_signal", 0):
                    return False
            if key == "near_52w_high" and val and not data.get("near_52w_high"):
                return False
            if key == "near_52w_low" and val and not data.get("near_52w_low"):
                return False
            if key == "max_annual_vol" and data.get("annual_vol", 0.20) > val:
                return False
            if key == "min_annual_vol" and data.get("annual_vol", 0.20) < val:
                return False
        return True

    def _pick_universe(self, query: str, universe: str) -> list[str]:
        if universe != "auto":
            if universe not in UNIVERSE:
                raise ValueError(f"Unknown universe '{universe}'. Available: {sorted(UNIVERSE.keys())}")
            return UNIVERSE[universe]

        q = query.lower()
        for pattern, cat in [
            (r"s&?p|large|mega|blue.chip", "mega_cap"),
            (r"small.cap", "small_cap"), (r"mid.cap", "mid_cap"),
            (r"tech|software", "semiconductor"),
            (r"dividend", "dividend_aristocrats"),
            (r"energy|oil", "commodities"),
            (r"china|chinese", "china_adr"),
            (r"biotech|pharma", "glp1_obesity"),
            (r"crypto", "crypto_adjacent"),
            (r"defense", "defense_niche"),
            (r"gold|silver", "precious_metals"),
        ]:
            if re.search(pattern, q):
                return UNIVERSE.get(cat, UNIVERSE["mega_cap"])

        return list(dict.fromkeys(UNIVERSE["mega_cap"] + UNIVERSE["growth"] + UNIVERSE["value"] +
                                   UNIVERSE["dividend"]))

    def _get_stock_data(self, symbol: str) -> dict | None:
        try:
            df = fetch_ohlcv(symbol, start="2024-01-01", cache=True)
            if df.empty or len(df) < 20:
                return None
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)

            close = df["Close"]
            price = float(close.iloc[-1])
            df_52w = df.iloc[-252:]
            high_252 = df_52w["High"].max()
            low_252 = df_52w["Low"].min()
            if pd.isna(high_252) or pd.isna(low_252):
                return None
            high_252 = float(high_252)
            low_252 = float(low_252)

            sma50 = float(close.iloc[-50:].mean()) if len(close) >= 50 else None
            sma200 = float(close.iloc[-200:].mean()) if len(close) >= 200 else None
            if sma50 is not None and pd.isna(sma50):
                sma50 = None
            if sma200 is not None and pd.isna(sma200):
                sma200 = None

            delta = close.diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss.replace(0, float("nan"))
            rsi = float((100 - (100 / (1 + rs))).iloc[-1])
            if pd.isna(rsi):
                rsi = 50

            ema12 = close.ewm(span=12).mean()
            ema26 = close.ewm(span=26).mean()
            macd = float((ema12 - ema26).iloc[-1])
            macd_signal = float((ema12 - ema26).ewm(span=9).mean().iloc[-1])

            vol_20 = close.pct_change().tail(20).std()
            if pd.isna(vol_20):
                vol_20 = 0.0
            else:
                vol_20 = float(vol_20)
            vol_avg = df["Volume"].rolling(20).mean().iloc[-1]
            if pd.isna(vol_avg) or vol_avg <= 0:
                vol_ratio = 1.0
            else:
                vol_ratio = float(df["Volume"].iloc[-1] / vol_avg)

            return {
                "symbol": symbol,
                "price": price,
                "sma_50": sma50,
                "sma_200": sma200,
                "rsi_14": rsi,
                "macd": macd,
                "macd_signal": macd_signal,
                "annual_vol": vol_20 * math.sqrt(252),
                "vol_ratio": vol_ratio,
                "52w_high": high_252,
                "52w_low": low_252,
                "near_52w_high": price >= high_252 * 0.95,
                "near_52w_low": price <= low_252 * 1.05,
                "pct_from_high": (price - high_252) / high_252 if high_252 > 0 else 0.0,
                "tradingview": f"https://www.tradingview.com/chart/?symbol={symbol}",
                "yahoo": f"https://finance.yahoo.com/quote/{symbol}/",
            }
        except Exception:
            return None


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) or "oversold stocks above SMA200"
    scanner = InsightEngine()
    print(f"\n  Insight Engine Scan: \"{query}\"\n")
    result = scanner.scan(query)
    print(f"  Interpretation: {result['interpretation']}")
    print(f"  Criteria: {result['criteria']}")
    print(f"  Found: {result['count']} / {result['universe_scanned']} scanned\n")
    print(f"  {'Symbol':>6s} | {'Price':>8s} | {'RSI':>5s} | {'vs SMA50':>8s} | {'vs 52wH':>8s} | {'Vol':>5s}")
    print(f"  {'-'*55}")
    for r in result["results"]:
        sma50_pct = f"{(r['price']/r['sma_50']-1)*100:+.1f}%" if r.get("sma_50") else "N/A"
        print(f"  {r['symbol']:>6s} | ${r['price']:>7.2f} | {r['rsi_14']:>4.0f} | {sma50_pct:>8s} | {r['pct_from_high']*100:+.1f}% | {r['annual_vol']*100:.0f}%")

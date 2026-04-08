"""FlowRadar — unusual volume and flow detection.

Scans for stocks with unusual volume activity that may indicate
institutional buying/selling or options activity.

Usage:
    from flow_radar import FlowRadar
    radar = FlowRadar()
    alerts = radar.scan_volume_spikes()
    alerts = radar.scan_momentum_shifts()
"""

from __future__ import annotations
import sys
from pathlib import Path
from typing import Any, Dict, List
import numpy as np, pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from data_fetcher import fetch_ohlcv, UNIVERSE

class FlowRadar:
    """Detect unusual market flow patterns."""

    def scan_volume_spikes(self, universe: str = "mega_cap", threshold: float = 2.5) -> List[Dict]:
        """Find stocks with volume > threshold * 20-day average."""
        symbols = UNIVERSE.get(universe, UNIVERSE["mega_cap"])
        alerts = []
        for sym in symbols:
            try:
                df = fetch_ohlcv(sym, start="2024-10-01", cache=True)
                if len(df) < 25: continue
                if df.index.tz is not None: df.index = df.index.tz_localize(None)
                vol_avg = float(df["Volume"].rolling(20).mean().iloc[-1])
                vol_today = float(df["Volume"].iloc[-1])
                ratio = vol_today / vol_avg if vol_avg > 0 else 1
                if ratio > threshold:
                    ret = float(df["Close"].pct_change().iloc[-1])
                    alerts.append({
                        "symbol": sym, "volume_ratio": round(ratio, 1),
                        "direction": "UP" if ret > 0.01 else "DOWN" if ret < -0.01 else "FLAT",
                        "daily_return": round(ret * 100, 1),
                        "signal": "ACCUMULATION" if ret > 0 and ratio > 3 else "DISTRIBUTION" if ret < 0 and ratio > 3 else "UNUSUAL",
                        "tradingview": f"https://www.tradingview.com/chart/?symbol={sym}",
                    })
            except: pass
        alerts.sort(key=lambda x: x["volume_ratio"], reverse=True)
        return alerts

    def scan_momentum_shifts(self, universe: str = "mega_cap") -> List[Dict]:
        """Find stocks where MACD just crossed (momentum shift)."""
        symbols = UNIVERSE.get(universe, UNIVERSE["mega_cap"])
        shifts = []
        for sym in symbols:
            try:
                df = fetch_ohlcv(sym, start="2024-06-01", cache=True)
                if len(df) < 30: continue
                if df.index.tz is not None: df.index = df.index.tz_localize(None)
                c = df["Close"]
                macd = c.ewm(span=12).mean() - c.ewm(span=26).mean()
                sig = macd.ewm(span=9).mean()
                if macd.iloc[-1] > sig.iloc[-1] and macd.iloc[-2] <= sig.iloc[-2]:
                    shifts.append({"symbol": sym, "signal": "BULLISH_CROSS", "macd": round(float(macd.iloc[-1]), 3),
                                   "tradingview": f"https://www.tradingview.com/chart/?symbol={sym}"})
                elif macd.iloc[-1] < sig.iloc[-1] and macd.iloc[-2] >= sig.iloc[-2]:
                    shifts.append({"symbol": sym, "signal": "BEARISH_CROSS", "macd": round(float(macd.iloc[-1]), 3),
                                   "tradingview": f"https://www.tradingview.com/chart/?symbol={sym}"})
            except: pass
        return shifts

    def scan_all(self) -> Dict[str, List]:
        return {
            "volume_spikes": self.scan_volume_spikes(),
            "momentum_shifts": self.scan_momentum_shifts(),
        }

if __name__ == "__main__":
    r = FlowRadar()
    print("=== Volume Spikes ===")
    for a in r.scan_volume_spikes()[:5]:
        print(f"  {a['symbol']:>6s} | {a['volume_ratio']:.1f}x vol | {a['direction']} {a['daily_return']:+.1f}% | {a['signal']}")
    print("\n=== Momentum Shifts ===")
    for s in r.scan_momentum_shifts()[:5]:
        print(f"  {s['symbol']:>6s} | {s['signal']}")

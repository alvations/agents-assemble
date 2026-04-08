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
import math
from datetime import datetime, timedelta
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
from data_fetcher import fetch_ohlcv, UNIVERSE

class FlowRadar:
    """Detect unusual market flow patterns."""

    def scan_volume_spikes(self, universe: str = "mega_cap", threshold: float = 2.5) -> list[dict]:
        """Find stocks with volume > threshold * 20-day average."""
        symbols = UNIVERSE.get(universe, UNIVERSE["mega_cap"])
        alerts = []
        for sym in symbols:
            try:
                start = (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d")
                df = fetch_ohlcv(sym, start=start, cache=True)
                if len(df) < 25: continue
                if df.index.tz is not None: df.index = df.index.tz_localize(None)
                vol_avg = float(df["Volume"].rolling(20).mean().iloc[-1])
                vol_today = float(df["Volume"].iloc[-1])
                if not math.isfinite(vol_avg) or not math.isfinite(vol_today) or vol_avg <= 0:
                    continue
                ratio = vol_today / vol_avg
                if ratio > threshold:
                    ret = float(df["Close"].pct_change().iloc[-1])
                    if not math.isfinite(ret):
                        continue
                    alerts.append({
                        "symbol": sym, "volume_ratio": round(ratio, 1),
                        "direction": "UP" if ret > 0.01 else "DOWN" if ret < -0.01 else "FLAT",
                        "daily_return": round(ret * 100, 1),
                        "signal": "ACCUMULATION" if ret > 0 and ratio > 3 else "DISTRIBUTION" if ret < 0 and ratio > 3 else "UNUSUAL",
                        "tradingview": f"https://www.tradingview.com/chart/?symbol={sym}",
                    })
            except Exception: pass
        alerts.sort(key=lambda x: x["volume_ratio"], reverse=True)
        return alerts

    def scan_momentum_shifts(self, universe: str = "mega_cap") -> list[dict]:
        """Find stocks where MACD just crossed (momentum shift)."""
        symbols = UNIVERSE.get(universe, UNIVERSE["mega_cap"])
        shifts = []
        for sym in symbols:
            try:
                start = (datetime.now() - timedelta(days=120)).strftime("%Y-%m-%d")
                df = fetch_ohlcv(sym, start=start, cache=True)
                if len(df) < 30: continue
                if df.index.tz is not None: df.index = df.index.tz_localize(None)
                c = df["Close"]
                macd = c.ewm(span=12).mean() - c.ewm(span=26).mean()
                sig = macd.ewm(span=9).mean()
                m_cur, m_prev = float(macd.iloc[-1]), float(macd.iloc[-2])
                s_cur, s_prev = float(sig.iloc[-1]), float(sig.iloc[-2])
                if not all(math.isfinite(v) for v in (m_cur, m_prev, s_cur, s_prev)):
                    continue
                if m_cur > s_cur and m_prev <= s_prev:
                    shifts.append({"symbol": sym, "signal": "BULLISH_CROSS", "macd": round(m_cur, 3),
                                   "tradingview": f"https://www.tradingview.com/chart/?symbol={sym}"})
                elif m_cur < s_cur and m_prev >= s_prev:
                    shifts.append({"symbol": sym, "signal": "BEARISH_CROSS", "macd": round(m_cur, 3),
                                   "tradingview": f"https://www.tradingview.com/chart/?symbol={sym}"})
            except Exception: pass
        return shifts

    def scan_all(self) -> dict[str, list]:
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

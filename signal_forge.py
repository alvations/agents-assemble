"""SignalForge — AI-powered custom indicator and signal builder.

Users describe a trading signal in natural language, Claude generates
the code, and SignalForge backtests it immediately.

Usage:
    from signal_forge import SignalForge
    forge = SignalForge()
    result = forge.build("buy when RSI crosses below 20 and MACD turns positive")
    result = forge.build("sell when price drops 5% from 20-day high")
"""

from __future__ import annotations
import sys, json, re
from pathlib import Path
from typing import Any, Dict, List, Optional
import numpy as np, pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))
from data_fetcher import fetch_ohlcv

class SignalForge:
    """Build and backtest custom signals from natural language."""

    BUILTIN_SIGNALS = {
        "rsi_oversold": {"desc": "Buy when RSI(14) < 20", "buy": lambda d,i: d["rsi"].iloc[i] < 20, "sell": lambda d,i: d["rsi"].iloc[i] > 60},
        "macd_cross": {"desc": "Buy when MACD crosses above signal", "buy": lambda d,i: d["macd"].iloc[i] > d["signal"].iloc[i] and d["macd"].iloc[i-1] <= d["signal"].iloc[i-1], "sell": lambda d,i: d["macd"].iloc[i] < d["signal"].iloc[i]},
        "golden_cross": {"desc": "Buy when SMA50 crosses above SMA200", "buy": lambda d,i: d["sma50"].iloc[i] > d["sma200"].iloc[i] and d["sma50"].iloc[i-1] <= d["sma200"].iloc[i-1], "sell": lambda d,i: d["sma50"].iloc[i] < d["sma200"].iloc[i]},
        "bb_bounce": {"desc": "Buy when price touches lower Bollinger Band", "buy": lambda d,i: d["close"].iloc[i] <= d["bb_lower"].iloc[i], "sell": lambda d,i: d["close"].iloc[i] >= d["sma20"].iloc[i]},
        "volume_breakout": {"desc": "Buy on 2x volume + 2% up move", "buy": lambda d,i: d["vol_ratio"].iloc[i] > 2 and d["ret"].iloc[i] > 0.02, "sell": lambda d,i: d["rsi"].iloc[i] > 75},
    }

    def build(self, description: str, symbol: str = "SPY", start: str = "2020-01-01") -> Dict[str, Any]:
        """Build a signal from description, backtest it, return results."""
        # Try Claude first
        signal = self._claude_build(description)
        if not signal:
            signal = self._match_builtin(description)

        if not signal:
            return {"error": f"Could not interpret: {description}", "available": list(self.BUILTIN_SIGNALS.keys())}

        # Backtest
        return self._backtest_signal(signal, symbol, start)

    def _claude_build(self, description: str) -> Optional[Dict]:
        try:
            from claude_code_client import ClaudeClient
            client = ClaudeClient()
            prompt = f"""Create a trading signal from this description: "{description}"

Return ONLY a JSON with: {{"name": "signal_name", "buy_condition": "python expression using: close, sma20, sma50, sma200, rsi, macd, signal, bb_upper, bb_lower, vol_ratio, ret", "sell_condition": "python expression"}}

Variables available: close (price), sma20/50/200, rsi (0-100), macd, signal (macd signal line), bb_upper/bb_lower, vol_ratio (volume/20d avg), ret (daily return)."""

            result = client.ask(prompt)
            match = re.search(r'\{[\s\S]*\}', result.text)
            if match:
                parsed = json.loads(match.group())
                return {"name": parsed.get("name", "custom"), "desc": description,
                        "buy_expr": parsed.get("buy_condition", ""), "sell_expr": parsed.get("sell_condition", "")}
        except Exception:
            pass
        return None

    def _match_builtin(self, description: str) -> Optional[Dict]:
        d = description.lower()
        for name, sig in self.BUILTIN_SIGNALS.items():
            keywords = name.replace("_", " ").split()
            if any(k in d for k in keywords):
                return {"name": name, "desc": sig["desc"], "builtin": name}
        return None

    def _backtest_signal(self, signal: Dict, symbol: str, start: str) -> Dict:
        df = fetch_ohlcv(symbol, start=start)
        if df.index.tz is not None: df.index = df.index.tz_localize(None)
        if len(df) < 50: return {"error": "Insufficient data"}

        c = df["Close"]
        data = pd.DataFrame({
            "close": c, "sma20": c.rolling(20).mean(), "sma50": c.rolling(50).mean(),
            "sma200": c.rolling(200).mean(), "ret": c.pct_change(),
            "vol_ratio": df["Volume"] / df["Volume"].rolling(20).mean(),
        })
        delta = c.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        data["rsi"] = 100 - (100 / (1 + gain / loss.replace(0, np.nan)))
        ema12, ema26 = c.ewm(span=12).mean(), c.ewm(span=26).mean()
        data["macd"] = ema12 - ema26
        data["signal"] = data["macd"].ewm(span=9).mean()
        std20 = c.rolling(20).std()
        data["bb_upper"] = data["sma20"] + 2 * std20
        data["bb_lower"] = data["sma20"] - 2 * std20

        trades = []
        position = None

        if "builtin" in signal:
            buy_fn = self.BUILTIN_SIGNALS[signal["builtin"]]["buy"]
            sell_fn = self.BUILTIN_SIGNALS[signal["builtin"]]["sell"]
        elif "buy_expr" in signal:
            buy_fn = lambda d, i, expr=signal["buy_expr"]: eval(expr, {k: d[k].iloc[i] for k in d.columns if not pd.isna(d[k].iloc[i])})
            sell_fn = lambda d, i, expr=signal["sell_expr"]: eval(expr, {k: d[k].iloc[i] for k in d.columns if not pd.isna(d[k].iloc[i])})
        else:
            return {"error": "No signal logic"}

        for i in range(201, len(data)):
            try:
                if position is None and buy_fn(data, i):
                    position = float(c.iloc[i])
                elif position is not None and sell_fn(data, i):
                    trades.append(float(c.iloc[i]) / position - 1)
                    position = None
            except: pass

        if position: trades.append(float(c.iloc[-1]) / position - 1)
        if not trades: return {"signal": signal["name"], "trades": 0, "note": "No signals triggered"}

        winners = [t for t in trades if t > 0]
        losers = [t for t in trades if t < 0]
        return {
            "signal": signal["name"], "description": signal.get("desc", ""),
            "symbol": symbol, "period": f"{start} → now",
            "trades": len(trades), "win_rate": len(winners)/len(trades),
            "avg_return": float(np.mean(trades)),
            "total_return": float(np.prod([1+t for t in trades]) - 1),
            "best": float(max(trades)), "worst": float(min(trades)),
            "profit_factor": abs(sum(winners)/sum(losers)) if losers else float("inf"),
        }

    def list_signals(self) -> List[Dict]:
        return [{"name": k, "description": v["desc"]} for k, v in self.BUILTIN_SIGNALS.items()]

if __name__ == "__main__":
    f = SignalForge()
    print("Built-in signals:", [s["name"] for s in f.list_signals()])
    r = f.build("RSI oversold bounce", symbol="SPY")
    print(json.dumps(r, indent=2, default=str))

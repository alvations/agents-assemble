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
import sys, json, math, re
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))
from data_fetcher import fetch_ohlcv

class SignalForge:
    """Build and backtest custom signals from natural language."""

    _UNSAFE = re.compile(r'__|\bimport\b|\bexec\b|\beval\b|\bcompile\b|\bopen\b|\bgetattr\b|\bsetattr\b|\bdelattr\b|\bglobals\b|\blocals\b|\bos\b|\bsys\b')
    _SAFE_GLOBALS = {"__builtins__": {}, "abs": abs, "min": min, "max": max, "round": round,
                     "sum": sum, "len": len, "int": int, "float": float, "bool": bool}

    BUILTIN_SIGNALS = {
        "rsi_oversold": {"desc": "Buy when RSI(14) < 20", "buy": lambda d,i: d["rsi"].iloc[i] < 20, "sell": lambda d,i: d["rsi"].iloc[i] > 60},
        "macd_cross": {"desc": "Buy when MACD crosses above signal", "buy": lambda d,i: d["macd"].iloc[i] > d["signal"].iloc[i] and d["macd"].iloc[i-1] <= d["signal"].iloc[i-1], "sell": lambda d,i: d["macd"].iloc[i] < d["signal"].iloc[i]},
        "golden_cross": {"desc": "Buy when SMA50 crosses above SMA200", "buy": lambda d,i: d["sma50"].iloc[i] > d["sma200"].iloc[i] and d["sma50"].iloc[i-1] <= d["sma200"].iloc[i-1], "sell": lambda d,i: d["sma50"].iloc[i] < d["sma200"].iloc[i]},
        "bb_bounce": {"desc": "Buy when price touches lower Bollinger Band", "buy": lambda d,i: d["close"].iloc[i] <= d["bb_lower"].iloc[i], "sell": lambda d,i: d["close"].iloc[i] >= d["sma20"].iloc[i]},
        "volume_breakout": {"desc": "Buy on 2x volume + 2% up move", "buy": lambda d,i: d["vol_ratio"].iloc[i] > 2 and d["ret"].iloc[i] > 0.02, "sell": lambda d,i: d["rsi"].iloc[i] > 75},
    }

    def build(self, description: str, symbol: str = "SPY", start: str = "2020-01-01") -> dict:
        """Build a signal from description, backtest it, return results."""
        # Try Claude first
        signal = self._claude_build(description)
        if not signal:
            signal = self._match_builtin(description)

        if not signal:
            return {"error": f"Could not interpret: {description}", "available": list(self.BUILTIN_SIGNALS.keys())}

        # Backtest
        return self._backtest_signal(signal, symbol, start)

    def _claude_build(self, description: str) -> dict | None:
        try:
            from claude_code_client import ClaudeClient
            client = ClaudeClient()
            prompt = f"""Create a trading signal from this description: "{description}"

Return ONLY a JSON with: {{"name": "signal_name", "buy_condition": "python expression using: close, sma20, sma50, sma200, rsi, macd, signal, bb_upper, bb_lower, vol_ratio, ret", "sell_condition": "python expression"}}

Variables available: close (price), sma20/50/200, rsi (0-100), macd, signal (macd signal line), bb_upper/bb_lower, vol_ratio (volume/20d avg), ret (daily return)."""

            result = client.ask(prompt)
            match = re.search(r'\{[\s\S]*\}', result.text)
            if match:
                parsed = json.loads(match.group().strip())
                return {"name": parsed.get("name", "custom"), "desc": description,
                        "buy_expr": parsed.get("buy_condition", ""), "sell_expr": parsed.get("sell_condition", "")}
        except Exception:
            pass
        return None

    def _match_builtin(self, description: str) -> dict | None:
        words = set(re.findall(r'[a-z0-9]+', description.lower()))
        best, best_count = None, 0
        for name, sig in self.BUILTIN_SIGNALS.items():
            keywords = name.split("_")
            if all(k in words for k in keywords) and len(keywords) > best_count:
                best = {"name": name, "desc": sig["desc"], "builtin": name}
                best_count = len(keywords)
        return best

    def _backtest_signal(self, signal: dict, symbol: str, start: str) -> dict:
        try:
            df = fetch_ohlcv(symbol, start=start)
        except Exception as e:
            return {"error": f"Failed to fetch data for {symbol}: {e}"}
        if df.index.tz is not None: df.index = df.index.tz_localize(None)
        if len(df) < 200: return {"error": "Insufficient data (need 200+ rows for SMA200)"}

        c = df["Close"]
        data = pd.DataFrame({
            "close": c, "sma20": c.rolling(20).mean(), "sma50": c.rolling(50).mean(),
            "sma200": c.rolling(200).mean(), "ret": c.pct_change(),
            "vol_ratio": df["Volume"] / df["Volume"].rolling(20).mean().replace(0, float("nan")),
        })
        delta = c.diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss.replace(0, float("nan"))
        rsi = 100 - (100 / (1 + rs))
        data["rsi"] = rsi.where(loss > 0, pd.Series(float("nan"), index=c.index).where(gain <= 0, 100.0))
        ema12, ema26 = c.ewm(span=12).mean(), c.ewm(span=26).mean()
        data["macd"] = ema12 - ema26
        data["signal"] = data["macd"].ewm(span=9).mean()
        std20 = c.rolling(20).std()
        data["bb_upper"] = data["sma20"] + 2 * std20
        data["bb_lower"] = data["sma20"] - 2 * std20

        trades = []
        position = None
        errors = 0

        if "builtin" in signal:
            buy_fn = self.BUILTIN_SIGNALS[signal["builtin"]]["buy"]
            sell_fn = self.BUILTIN_SIGNALS[signal["builtin"]]["sell"]
        elif "buy_expr" in signal:
            buy_expr, sell_expr = signal["buy_expr"].strip(), signal["sell_expr"].strip()
            if not buy_expr or not sell_expr:
                return {"error": "Empty buy or sell expression", "signal": signal.get("name", "custom")}
            for expr_name, expr in [("buy", buy_expr), ("sell", sell_expr)]:
                if self._UNSAFE.search(expr):
                    return {"error": f"Unsafe pattern in {expr_name} expression", "signal": signal.get("name", "custom")}
            sg = self._SAFE_GLOBALS
            vals = {k: data[k].values for k in data.columns}
            buy_fn = lambda d, i, expr=buy_expr, v=vals: eval(expr, sg, {k: float(v[k][i]) for k in v})
            sell_fn = lambda d, i, expr=sell_expr, v=vals: eval(expr, sg, {k: float(v[k][i]) for k in v})
        else:
            return {"error": "No signal logic"}

        close_arr = c.values
        for i in range(200, len(data)):
            price = float(close_arr[i])
            if price != price:  # NaN guard
                continue
            try:
                if position is None and buy_fn(data, i):
                    position = price
                elif position is not None and sell_fn(data, i):
                    trades.append(price / position - 1)
                    position = None
            except Exception:
                errors += 1

        if position is not None:
            last = float(close_arr[-1])
            if last == last:  # NaN guard
                trades.append(last / position - 1)
        trades = [t for t in trades if t == t]  # filter NaN
        if not trades:
            result = {"signal": signal["name"], "trades": 0, "note": "No signals triggered"}
            if errors: result["eval_errors"] = errors
            return result

        winners = [t for t in trades if t > 0]
        losers = [t for t in trades if t < 0]
        return {
            "signal": signal["name"], "description": signal.get("desc", ""),
            "symbol": symbol, "period": f"{start} → now",
            "trades": len(trades), "win_rate": len(winners)/len(trades),
            "avg_return": sum(trades) / len(trades),
            "total_return": math.prod(1 + t for t in trades) - 1,
            "best": float(max(trades)), "worst": float(min(trades)),
            "profit_factor": abs(sum(winners)/sum(losers)) if losers else None,
            **({"eval_errors": errors} if errors else {}),
        }

    def list_signals(self) -> list[dict]:
        return [{"name": k, "description": v["desc"]} for k, v in self.BUILTIN_SIGNALS.items()]

if __name__ == "__main__":
    f = SignalForge()
    print("Built-in signals:", [s["name"] for s in f.list_signals()])
    r = f.build("RSI oversold bounce", symbol="SPY")
    def _sanitize(obj):
        if isinstance(obj, dict):
            return {k: _sanitize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [_sanitize(v) for v in obj]
        if isinstance(obj, float) and not math.isfinite(obj):
            return None
        return obj
    print(json.dumps(_sanitize(r), indent=2, default=str))

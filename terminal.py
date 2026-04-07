"""Mini Bloomberg Terminal — visualization and dashboard for agents-assemble.

Generates charts, dashboards, and reports as PNG images + markdown.
Designed to emulate key Bloomberg terminal features using free data.

Features:
    1. Equity chart with indicators (price, SMA, volume, RSI, MACD)
    2. Strategy equity curve comparison
    3. Leaderboard heatmap (strategies x horizons)
    4. Sector performance treemap
    5. Portfolio allocation pie chart
    6. Catalyst event timeline
    7. Risk/return scatter plot
    8. Correlation matrix
    9. Drawdown chart
    10. Auto-trade signal dashboard (integrates with public_trader)

Usage:
    from terminal import Terminal
    t = Terminal()
    t.equity_chart("NVDA")                   # Single stock chart
    t.strategy_comparison(["momentum", "ai_revolution"])  # Compare strategies
    t.leaderboard_heatmap()                  # Full leaderboard
    t.generate_dashboard("NVDA")             # Full Bloomberg-style dashboard
"""

from __future__ import annotations

import os
import sys
from datetime import datetime
from pathlib import Path
import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

# Lazy import matplotlib to avoid issues in headless environments
def _get_plt():
    import matplotlib
    matplotlib.use("Agg")  # Non-interactive backend
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    return plt, mdates

CHARTS_DIR = Path(__file__).parent / "charts"
CHARTS_DIR.mkdir(exist_ok=True)


class Terminal:
    """Mini Bloomberg Terminal for agents-assemble."""

    def __init__(self, output_dir: str | None = None):
        self.output_dir = Path(output_dir or str(CHARTS_DIR))
        self.output_dir.mkdir(parents=True, exist_ok=True)

    # ----- 1. Equity Chart (GP command) -----

    def equity_chart(
        self, symbol: str, start: str = "2024-01-01", end: str | None = None,
        show_volume: bool = True, show_rsi: bool = True, show_macd: bool = True,
    ) -> Path:
        """Bloomberg GP-style equity chart with indicators."""
        plt, mdates = _get_plt()
        from data_fetcher import fetch_ohlcv

        df = fetch_ohlcv(symbol, start=start, end=end)
        if df.index.tz is not None:
            df.index = df.index.tz_localize(None)

        close = df["Close"]
        sma20 = close.rolling(20).mean()
        sma50 = close.rolling(50).mean()
        sma200 = close.rolling(200).mean()

        n_panels = 1 + show_volume + show_rsi + show_macd
        ratios = [3] + ([1] if show_volume else []) + ([1] if show_rsi else []) + ([1.2] if show_macd else [])

        fig, axes = plt.subplots(n_panels, 1, figsize=(14, 3 * n_panels),
                                  gridspec_kw={"height_ratios": ratios}, sharex=True)
        if n_panels == 1:
            axes = [axes]
        fig.patch.set_facecolor("#1a1a2e")

        # Price panel
        ax = axes[0]
        ax.set_facecolor("#1a1a2e")
        ax.plot(close.index, close, color="#00ff88", linewidth=1.2, label="Price")
        ax.plot(sma20.index, sma20, color="#ffaa00", linewidth=0.7, alpha=0.7, label="SMA20")
        ax.plot(sma50.index, sma50, color="#ff4444", linewidth=0.7, alpha=0.7, label="SMA50")
        if len(close) > 200:
            ax.plot(sma200.index, sma200, color="#4488ff", linewidth=0.7, alpha=0.7, label="SMA200")
        ax.fill_between(close.index, close, close.min(), alpha=0.1, color="#00ff88")
        ax.set_ylabel("Price ($)", color="white", fontsize=9)
        ax.legend(loc="upper left", fontsize=7, facecolor="#1a1a2e", edgecolor="#333",
                  labelcolor="white")
        ax.tick_params(colors="white", labelsize=8)
        ax.grid(True, alpha=0.15, color="white")
        ax.set_title(f"  {symbol}  |  {close.iloc[-1]:.2f}  |  "
                     f"{(close.iloc[-1]/close.iloc[0]-1)*100:+.1f}%  |  "
                     f"{start} → {df.index[-1].strftime('%Y-%m-%d')}",
                     color="#00ff88", fontsize=12, loc="left", fontweight="bold")

        panel = 1

        # Volume panel
        if show_volume:
            ax = axes[panel]; panel += 1
            ax.set_facecolor("#1a1a2e")
            colors = ["#00ff88" if c >= o else "#ff4444"
                      for c, o in zip(df["Close"], df["Open"])]
            ax.bar(df.index, df["Volume"], color=colors, alpha=0.6, width=0.8)
            ax.set_ylabel("Vol", color="white", fontsize=8)
            ax.tick_params(colors="white", labelsize=7)
            ax.grid(True, alpha=0.1, color="white")

        # RSI panel
        if show_rsi:
            ax = axes[panel]; panel += 1
            delta = close.diff()
            gain = delta.where(delta > 0, 0).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss.replace(0, float('nan'))
            rsi = 100 - (100 / (1 + rs))
            ax.set_facecolor("#1a1a2e")
            ax.plot(rsi.index, rsi, color="#ffaa00", linewidth=1)
            ax.axhline(70, color="#ff4444", linewidth=0.5, linestyle="--", alpha=0.5)
            ax.axhline(30, color="#00ff88", linewidth=0.5, linestyle="--", alpha=0.5)
            ax.fill_between(rsi.index, rsi, 70, where=rsi > 70, color="#ff4444", alpha=0.2)
            ax.fill_between(rsi.index, rsi, 30, where=rsi < 30, color="#00ff88", alpha=0.2)
            ax.set_ylabel("RSI", color="white", fontsize=8)
            ax.set_ylim(0, 100)
            ax.tick_params(colors="white", labelsize=7)
            ax.grid(True, alpha=0.1, color="white")

        # MACD panel
        if show_macd:
            ax = axes[panel]; panel += 1
            ema12 = close.ewm(span=12).mean()
            ema26 = close.ewm(span=26).mean()
            macd = ema12 - ema26
            signal = macd.ewm(span=9).mean()
            hist = macd - signal
            ax.set_facecolor("#1a1a2e")
            ax.plot(macd.index, macd, color="#00aaff", linewidth=0.8, label="MACD")
            ax.plot(signal.index, signal, color="#ff8800", linewidth=0.8, label="Signal")
            colors = ["#00ff88" if h >= 0 else "#ff4444" for h in hist]
            ax.bar(hist.index, hist, color=colors, alpha=0.5, width=0.8)
            ax.set_ylabel("MACD", color="white", fontsize=8)
            ax.legend(loc="upper left", fontsize=6, facecolor="#1a1a2e",
                      edgecolor="#333", labelcolor="white")
            ax.tick_params(colors="white", labelsize=7)
            ax.grid(True, alpha=0.1, color="white")

        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
        plt.tight_layout()
        path = self.output_dir / f"{symbol}_chart.png"
        fig.savefig(path, dpi=150, facecolor="#1a1a2e", bbox_inches="tight")
        plt.close(fig)
        return path

    # ----- 2. Strategy Equity Curve Comparison -----

    def strategy_comparison(
        self, strategies: list[str], start: str = "2022-01-01", end: str = "2024-12-31",
    ) -> Path:
        """Compare equity curves of multiple strategies."""
        plt, mdates = _get_plt()
        from run_multi_horizon import run_single, _get_all_strategies

        all_strats = _get_all_strategies()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8),
                                        gridspec_kw={"height_ratios": [3, 1]})
        fig.patch.set_facecolor("#1a1a2e")

        results = {}
        for name in strategies:
            strat_info = next((s for s in all_strats if s["key"] == name), None)
            if not strat_info:
                continue
            r = run_single(strat_info, "3y", start, end, verbose=False)
            if r["status"] == "success":
                results[name] = r["metrics"]

        # Bar chart of returns + Sharpe
        if results:
            names = list(results.keys())
            returns = [results[n].get("total_return", 0) * 100 for n in names]
            sharpes = [results[n].get("sharpe_ratio", 0) for n in names]
            max_dds = [results[n].get("max_drawdown", 0) * 100 for n in names]

            colors = ["#00ff88" if r > 0 else "#ff4444" for r in returns]

            ax1.set_facecolor("#1a1a2e")
            bars = ax1.bar(names, returns, color=colors, alpha=0.8, edgecolor="#333")
            for bar, sharpe in zip(bars, sharpes):
                ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                         f"S:{sharpe:.2f}", ha="center", color="white", fontsize=8)
            ax1.set_ylabel("Total Return (%)", color="white")
            ax1.set_title(f"Strategy Comparison | {start} → {end}", color="#00ff88",
                          fontsize=12, fontweight="bold")
            ax1.tick_params(colors="white", labelsize=8)
            ax1.axhline(0, color="white", linewidth=0.5, alpha=0.3)
            ax1.grid(True, axis="y", alpha=0.15, color="white")

            ax2.set_facecolor("#1a1a2e")
            ax2.bar(names, max_dds, color="#ff4444", alpha=0.6, edgecolor="#333")
            ax2.set_ylabel("Max Drawdown (%)", color="white")
            ax2.tick_params(colors="white", labelsize=8)
            ax2.grid(True, axis="y", alpha=0.15, color="white")

        for ax in [ax1, ax2]:
            plt.setp(ax.get_xticklabels(), rotation=30, ha="right")

        plt.tight_layout()
        path = self.output_dir / "strategy_comparison.png"
        fig.savefig(path, dpi=150, facecolor="#1a1a2e", bbox_inches="tight")
        plt.close(fig)
        return path

    # ----- 3. Leaderboard Heatmap -----

    def leaderboard_heatmap(self, top_n: int = 15) -> Path:
        """Heatmap of top strategies across horizons."""
        plt, _ = _get_plt()
        from run_multi_horizon import run_single, _get_all_strategies

        all_strats = _get_all_strategies()
        now = pd.Timestamp.now()
        end_date = now.strftime("%Y-%m-%d")
        horizons = {
            "3m": ((now - pd.DateOffset(months=3)).strftime("%Y-%m-%d"), end_date),
            "6m": ((now - pd.DateOffset(months=6)).strftime("%Y-%m-%d"), end_date),
            "1y": ((now - pd.DateOffset(years=1)).strftime("%Y-%m-%d"), end_date),
            "3y": ((now - pd.DateOffset(years=3)).strftime("%Y-%m-%d"), end_date),
        }

        # Collect data for top strategies
        data = {}
        for strat_info in all_strats[:top_n * 2]:
            name = strat_info["key"]
            row = {}
            for h_name, (start, end) in horizons.items():
                r = run_single(strat_info, h_name, start, end, verbose=False)
                if r["status"] == "success":
                    row[h_name] = r["metrics"].get("total_return", 0) * 100
            if row:
                data[name] = row

        if not data:
            return self.output_dir / "empty.png"

        df = pd.DataFrame(data).T.fillna(0)
        # Sort by 3Y return
        if "3y" in df.columns:
            df = df.sort_values("3y", ascending=False).head(top_n)

        fig, ax = plt.subplots(figsize=(10, max(6, top_n * 0.4)))
        fig.patch.set_facecolor("#1a1a2e")
        ax.set_facecolor("#1a1a2e")

        im = ax.imshow(df.values, aspect="auto", cmap="RdYlGn",
                        vmin=-50, vmax=150)
        ax.set_xticks(range(len(df.columns)))
        ax.set_xticklabels(df.columns, color="white", fontsize=9)
        ax.set_yticks(range(len(df.index)))
        ax.set_yticklabels(df.index, color="white", fontsize=8)

        for i in range(len(df.index)):
            for j in range(len(df.columns)):
                val = df.values[i, j]
                color = "white" if abs(val) > 50 else "black"
                ax.text(j, i, f"{val:.0f}%", ha="center", va="center",
                        color=color, fontsize=7, fontweight="bold")

        ax.set_title("Strategy Returns Heatmap (%)", color="#00ff88",
                      fontsize=12, fontweight="bold")
        plt.colorbar(im, ax=ax, label="Return (%)", shrink=0.8)
        plt.tight_layout()

        path = self.output_dir / "leaderboard_heatmap.png"
        fig.savefig(path, dpi=150, facecolor="#1a1a2e", bbox_inches="tight")
        plt.close(fig)
        return path

    # ----- 4. Risk/Return Scatter -----

    def risk_return_scatter(self, horizon: str = "3y") -> Path:
        """Risk vs return scatter plot for all strategies."""
        plt, _ = _get_plt()
        from run_multi_horizon import run_single, _get_all_strategies

        now = pd.Timestamp.now()
        end_str = now.strftime("%Y-%m-%d")
        offset_map = {"1y": 1, "3y": 3, "5y": 5}
        years = offset_map.get(horizon, 3)
        start = (now - pd.DateOffset(years=years)).strftime("%Y-%m-%d")
        end = end_str

        points = []
        for strat_info in _get_all_strategies():
            r = run_single(strat_info, horizon, start, end, verbose=False)
            if r["status"] == "success":
                m = r["metrics"]
                points.append({
                    "name": strat_info["key"],
                    "source": strat_info["source"],
                    "return": m.get("total_return", 0) * 100,
                    "vol": m.get("annual_volatility", 0) * 100,
                    "sharpe": m.get("sharpe_ratio", 0),
                    "max_dd": m.get("max_drawdown", 0) * 100,
                })

        if not points:
            return self.output_dir / "empty.png"

        fig, ax = plt.subplots(figsize=(14, 9))
        fig.patch.set_facecolor("#1a1a2e")
        ax.set_facecolor("#1a1a2e")

        source_colors = {
            "generic": "#00ff88", "famous": "#ffaa00", "theme": "#ff4488",
            "research": "#4488ff", "unconventional": "#aa44ff", "math": "#ff8844",
            "recession": "#888888", "hedge_fund": "#44ffaa", "news_event": "#ff44aa",
            "political": "#44aaff", "portfolio": "#aaff44", "crisis": "#ff8888",
        }

        for p in points:
            color = source_colors.get(p["source"], "#ffffff")
            size = max(20, min(200, abs(p["sharpe"]) * 80))
            ax.scatter(p["vol"], p["return"], c=color, s=size, alpha=0.7,
                       edgecolors="white", linewidths=0.5)
            if abs(p["return"]) > 80 or p["sharpe"] > 1.0:
                ax.annotate(p["name"], (p["vol"], p["return"]),
                            color="white", fontsize=6, alpha=0.8,
                            xytext=(5, 5), textcoords="offset points")

        ax.axhline(0, color="white", linewidth=0.3, alpha=0.3)
        ax.set_xlabel("Annual Volatility (%)", color="white", fontsize=10)
        ax.set_ylabel(f"Total Return (%) — {horizon}", color="white", fontsize=10)
        ax.set_title(f"Risk/Return Scatter | {horizon} | Size = |Sharpe|",
                     color="#00ff88", fontsize=12, fontweight="bold")
        ax.tick_params(colors="white")
        ax.grid(True, alpha=0.15, color="white")

        # Legend for sources
        for src, color in list(source_colors.items())[:6]:
            ax.scatter([], [], c=color, label=src, s=40)
        ax.legend(loc="upper left", fontsize=7, facecolor="#1a1a2e",
                  edgecolor="#333", labelcolor="white")

        plt.tight_layout()
        path = self.output_dir / f"risk_return_{horizon}.png"
        fig.savefig(path, dpi=150, facecolor="#1a1a2e", bbox_inches="tight")
        plt.close(fig)
        return path

    # ----- 5. Catalyst Event Timeline -----

    def catalyst_timeline(self, symbol: str) -> Path:
        """Bloomberg-style event timeline for a ticker."""
        plt, mdates = _get_plt()
        from catalyst_analyzer import CatalystAnalyzer

        analyzer = CatalystAnalyzer(symbol)
        patterns = analyzer.analyze_historical_patterns()
        df = analyzer._get_price_data()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 7),
                                        gridspec_kw={"height_ratios": [3, 1]})
        fig.patch.set_facecolor("#1a1a2e")

        # Price with event markers
        ax1.set_facecolor("#1a1a2e")
        ax1.plot(df.index, df["Close"], color="#00ff88", linewidth=1)

        events = patterns.get("events", [])
        for e in events:
            date = pd.Timestamp(e["date"])
            color = "#00ff88" if e["direction"] == "up" else "#ff4444"
            try:
                idx = df.index.get_indexer([date], method="nearest")[0]
                if idx < 0:
                    continue
                price = df["Close"].iloc[idx]
                marker = "^" if e["direction"] == "up" else "v"
                ax1.scatter(date, price, c=color, marker=marker, s=60, zorder=5, alpha=0.8)
            except (IndexError, KeyError):
                pass

        ax1.set_ylabel("Price ($)", color="white", fontsize=9)
        ax1.set_title(f"  {symbol} — Catalyst Event Timeline", color="#00ff88",
                      fontsize=12, fontweight="bold", loc="left")
        ax1.tick_params(colors="white", labelsize=8)
        ax1.grid(True, alpha=0.15, color="white")

        # Sell-horizon returns for up events
        ax2.set_facecolor("#1a1a2e")
        if "after_up" in patterns:
            horizons_data = patterns["after_up"]
            h_names = sorted(horizons_data.keys(), key=lambda x: int(x.replace("d", "")))
            avg_rets = [horizons_data[h]["avg_return"] * 100 for h in h_names]
            win_rates = [horizons_data[h].get("win_rate", 0) * 100 for h in h_names]
            colors = ["#00ff88" if r > 0 else "#ff4444" for r in avg_rets]
            x = range(len(h_names))
            ax2.bar(x, avg_rets, color=colors, alpha=0.7)
            ax2.set_xticks(x)
            ax2.set_xticklabels(h_names, color="white", fontsize=8)
            for i, (r, w) in enumerate(zip(avg_rets, win_rates)):
                ax2.text(i, r + 0.2, f"{w:.0f}%w", ha="center", color="white", fontsize=7)
            ax2.set_ylabel("Avg Return (%)", color="white", fontsize=9)
            ax2.set_title("  Post-Event Returns by Sell Horizon (UP events)",
                          color="#ffaa00", fontsize=10, loc="left")
        ax2.tick_params(colors="white", labelsize=8)
        ax2.axhline(0, color="white", linewidth=0.3, alpha=0.3)
        ax2.grid(True, axis="y", alpha=0.15, color="white")

        plt.tight_layout()
        path = self.output_dir / f"{symbol}_catalyst_timeline.png"
        fig.savefig(path, dpi=150, facecolor="#1a1a2e", bbox_inches="tight")
        plt.close(fig)
        return path

    # ----- 6. Sector Performance -----

    def sector_performance(self) -> Path:
        """Sector ETF performance bar chart."""
        plt, _ = _get_plt()
        from data_fetcher import fetch_ohlcv

        sectors = {
            "Tech": "XLK", "Finance": "XLF", "Energy": "XLE", "Health": "XLV",
            "Industry": "XLI", "Staples": "XLP", "Utility": "XLU",
            "RealEst": "XLRE", "Comms": "XLC", "Matls": "XLB", "DiscCon": "XLY",
        }

        ytd_start = f"{datetime.now().year}-01-01"
        rets = {}
        for name, etf in sectors.items():
            try:
                df = fetch_ohlcv(etf, start=ytd_start, cache=True)
                if len(df) > 5:
                    rets[name] = (df["Close"].iloc[-1] / df["Close"].iloc[0] - 1) * 100
            except Exception:
                pass

        if not rets:
            return self.output_dir / "empty.png"

        sorted_items = sorted(rets.items(), key=lambda x: x[1], reverse=True)
        names = [x[0] for x in sorted_items]
        values = [x[1] for x in sorted_items]
        colors = ["#00ff88" if v > 0 else "#ff4444" for v in values]

        fig, ax = plt.subplots(figsize=(12, 6))
        fig.patch.set_facecolor("#1a1a2e")
        ax.set_facecolor("#1a1a2e")

        bars = ax.barh(names, values, color=colors, alpha=0.8, edgecolor="#333")
        for bar, val in zip(bars, values):
            ax.text(val + (1 if val > 0 else -1), bar.get_y() + bar.get_height()/2,
                    f"{val:+.1f}%", va="center", color="white", fontsize=9)

        ax.axvline(0, color="white", linewidth=0.5, alpha=0.3)
        ax.set_xlabel("YTD Return (%)", color="white")
        ax.set_title("Sector Performance (YTD)", color="#00ff88",
                     fontsize=12, fontweight="bold")
        ax.tick_params(colors="white")
        ax.grid(True, axis="x", alpha=0.15, color="white")
        ax.invert_yaxis()

        plt.tight_layout()
        path = self.output_dir / "sector_performance.png"
        fig.savefig(path, dpi=150, facecolor="#1a1a2e", bbox_inches="tight")
        plt.close(fig)
        return path

    # ----- 7. Full Dashboard -----

    def generate_dashboard(self, symbol: str = "NVDA") -> list[Path]:
        """Generate full Bloomberg-style dashboard for a symbol."""
        paths = []
        print(f"Generating dashboard for {symbol}...")

        print("  [1/5] Equity chart...")
        paths.append(self.equity_chart(symbol))

        print("  [2/5] Catalyst timeline...")
        paths.append(self.catalyst_timeline(symbol))

        print("  [3/5] Sector performance...")
        paths.append(self.sector_performance())

        print("  [4/5] Strategy comparison...")
        top5 = ["concentrate_winners", "momentum", "momentum_crash_hedge",
                "ai_revolution", "nancy_pelosi"]
        paths.append(self.strategy_comparison(top5))

        print("  [5/5] Risk/return scatter...")
        paths.append(self.risk_return_scatter("3y"))

        print(f"\n  Dashboard saved to: {self.output_dir}/")
        for p in paths:
            print(f"    {p.name}")

        return paths


if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else "NVDA"
    t = Terminal()
    t.generate_dashboard(symbol)

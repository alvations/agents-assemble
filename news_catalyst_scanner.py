"""News-driven catalyst scanner and short-horizon backtester.

Given a ticker (e.g., "NTDOY"), this tool:
1. Pulls recent news via free APIs (Finnhub, NewsAPI) or yfinance
2. Identifies potential catalysts (product launches, earnings, M&A)
3. Analyzes historical price/volume patterns around news events
4. Produces short-horizon (<1Y) backtest results

Usage:
    python news_catalyst_scanner.py NTDOY
    python news_catalyst_scanner.py DIS --horizon 3m
    python news_catalyst_scanner.py TTWO --analyze-events

For enhanced results, set API keys:
    FINNHUB_API_KEY — real-time news + sentiment
    NEWS_API_KEY — broader news coverage
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import math

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

from data_fetcher import fetch_ohlcv, get_api_key


# ---------------------------------------------------------------------------
# News fetching (free + premium)
# ---------------------------------------------------------------------------
def fetch_news_yfinance(symbol: str, max_items: int = 20) -> list[dict]:
    """Fetch news from yfinance (free, no API key needed)."""
    import yfinance as yf
    ticker = yf.Ticker(symbol)
    try:
        news = ticker.news
        if news:
            return [
                {
                    "title": n.get("title", ""),
                    "date": datetime.fromtimestamp(n.get("providerPublishTime", 0)).strftime("%Y-%m-%d"),
                    "source": n.get("publisher", ""),
                    "url": n.get("link", ""),
                    "type": _classify_headline(n.get("title", "")),
                }
                for n in news[:max_items]
            ]
    except Exception:
        pass
    return []


def fetch_news_finnhub(symbol: str, days_back: int = 30) -> list[dict]:
    """Fetch company news from Finnhub (requires FINNHUB_API_KEY)."""
    import requests
    key = get_api_key("FINNHUB_API_KEY")
    if not key:
        return []

    end = datetime.now().strftime("%Y-%m-%d")
    start = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    url = "https://finnhub.io/api/v1/company-news"
    try:
        resp = requests.get(url, params={"symbol": symbol, "from": start, "to": end, "token": key}, timeout=15)
        if resp.status_code == 200:
            return [
                {
                    "title": n.get("headline", ""),
                    "date": datetime.fromtimestamp(n.get("datetime", 0)).strftime("%Y-%m-%d"),
                    "source": n.get("source", ""),
                    "url": n.get("url", ""),
                    "type": _classify_headline(n.get("headline", "")),
                    "sentiment": n.get("sentiment", None),
                }
                for n in resp.json()[:30]
            ]
    except Exception:
        pass
    return []


def _classify_headline(title: str) -> str:
    """Classify a news headline into catalyst type."""
    t = title.lower()
    if any(w in t for w in ["launch", "release", "unveil", "announce", "debut", "premiere"]):
        return "product_launch"
    if any(w in t for w in ["earnings", "revenue", "profit", "beat", "miss", "guidance"]):
        return "earnings"
    if any(w in t for w in ["acquire", "merger", "buyout", "deal", "takeover"]):
        return "ma"
    if any(w in t for w in ["upgrade", "downgrade", "target", "rating", "analyst"]):
        return "analyst"
    if any(w in t for w in ["fda", "approval", "trial", "patent"]):
        return "regulatory"
    if any(w in t for w in ["dividend", "buyback", "repurchase", "split"]):
        return "capital_return"
    return "general"


# ---------------------------------------------------------------------------
# Event analysis (price/volume patterns around news)
# ---------------------------------------------------------------------------
def analyze_event_patterns(
    symbol: str,
    start: str = "2023-01-01",
    end: str | None = None,
    volume_threshold: float = 2.0,
    return_threshold: float = 0.03,
    df: pd.DataFrame | None = None,
) -> dict:
    """Analyze historical price/volume patterns that look like news events.

    Detects "event days" = days with unusual volume (>2x average) AND
    significant price move (>3%). Analyzes what happens before and after.

    Returns:
        Dict with event_days, pre_event_drift, post_event_drift, etc.
    """
    if df is None:
        df = fetch_ohlcv(symbol, start=start, end=end)
    if df.empty or len(df) < 50:
        return {"error": f"Insufficient data for {symbol}"}

    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    close = df["Close"]
    volume = df["Volume"]
    daily_ret = close.pct_change()
    vol_avg = volume.rolling(20).mean()
    vol_ratio = volume / vol_avg

    # Find event days: unusual volume + significant move
    events = []
    for i in range(25, len(df) - 20):
        if vol_ratio.iloc[i] > volume_threshold and abs(daily_ret.iloc[i]) > return_threshold:
            date = df.index[i]
            ret = daily_ret.iloc[i]
            direction = "up" if ret > 0 else "down"

            # Pre-event: 5 days before
            pre_ret = close.iloc[i] / close.iloc[i - 5] - 1
            # Post-event: 5, 10, 20 days after (full windows guaranteed by loop bound)
            post_5 = close.iloc[i + 5] / close.iloc[i] - 1
            post_10 = close.iloc[i + 10] / close.iloc[i] - 1
            post_20 = close.iloc[i + 20] / close.iloc[i] - 1

            events.append({
                "date": str(date.date()),
                "return": float(ret),
                "volume_ratio": float(vol_ratio.iloc[i]),
                "direction": direction,
                "pre_5d_return": float(pre_ret),
                "post_5d_return": float(post_5),
                "post_10d_return": float(post_10),
                "post_20d_return": float(post_20),
            })

    if not events:
        return {"symbol": symbol, "events": [], "summary": "No significant events detected"}

    # Aggregate patterns
    up_events = [e for e in events if e["direction"] == "up"]
    down_events = [e for e in events if e["direction"] == "down"]

    summary = {
        "symbol": symbol,
        "total_events": len(events),
        "up_events": len(up_events),
        "down_events": len(down_events),
    }

    if up_events:
        n_up = len(up_events)
        summary["after_up_event"] = {
            "avg_post_5d": sum(e["post_5d_return"] for e in up_events) / n_up,
            "avg_post_10d": sum(e["post_10d_return"] for e in up_events) / n_up,
            "avg_post_20d": sum(e["post_20d_return"] for e in up_events) / n_up,
            "win_rate_5d": sum(1 for e in up_events if e["post_5d_return"] > 0) / n_up,
        }

    if down_events:
        n_down = len(down_events)
        summary["after_down_event"] = {
            "avg_post_5d": sum(e["post_5d_return"] for e in down_events) / n_down,
            "avg_post_10d": sum(e["post_10d_return"] for e in down_events) / n_down,
            "avg_post_20d": sum(e["post_20d_return"] for e in down_events) / n_down,
            "bounce_rate_5d": sum(1 for e in down_events if e["post_5d_return"] > 0) / n_down,
        }

    summary["events"] = events[:20]  # Limit for display
    return summary


# ---------------------------------------------------------------------------
# Short-horizon backtest based on event patterns
# ---------------------------------------------------------------------------
def event_driven_backtest(
    symbol: str,
    start: str = "2022-01-01",
    end: str | None = None,
    strategy: str = "buy_spike",  # buy_spike, buy_dip, momentum
    holding_days: int = 10,
    df: pd.DataFrame | None = None,
) -> dict:
    """Backtest an event-driven strategy on a single stock.

    Strategies:
    - buy_spike: Buy after >3% up-day on 2x volume, hold N days
    - buy_dip: Buy after >3% down-day on 2x volume (mean reversion), hold N days
    - momentum: Buy after >2% up on 1.5x volume, sell when RSI > 70

    Returns: performance metrics
    """
    if df is None:
        df = fetch_ohlcv(symbol, start=start, end=end)
    if df.empty or len(df) < 50:
        return {"error": f"Insufficient data for {symbol}"}

    if df.index.tz is not None:
        df.index = df.index.tz_localize(None)

    close = df["Close"]
    volume = df["Volume"]
    daily_ret = close.pct_change()
    vol_avg = volume.rolling(20).mean()
    vol_ratio = volume / vol_avg

    # RSI for momentum strategy exit
    if strategy == "momentum":
        delta = close.diff()
        gain = delta.clip(lower=0).rolling(14).mean()
        loss = (-delta.clip(upper=0)).rolling(14).mean()
        rsi = 100 - (100 / (1 + gain / loss))

    # Track trades
    trades = []
    position = None  # (entry_date, entry_price, entry_idx)

    for i in range(20, len(df)):
        price = close.iloc[i]
        ret = daily_ret.iloc[i] if not pd.isna(daily_ret.iloc[i]) else 0
        vr = vol_ratio.iloc[i] if not pd.isna(vol_ratio.iloc[i]) else 1

        # Check exit
        if position is not None:
            days_held = i - position[2]
            rsi_exit = (strategy == "momentum" and days_held >= 2
                        and not pd.isna(rsi.iloc[i]) and rsi.iloc[i] > 70)
            if days_held >= holding_days or rsi_exit:
                exit_ret = price / position[1] - 1
                trades.append({
                    "entry": str(df.index[position[2]].date()),
                    "exit": str(df.index[i].date()),
                    "return": float(exit_ret),
                    "days": days_held,
                })
                position = None

        # Check entry
        if position is None:
            if strategy == "buy_spike" and ret > 0.03 and vr > 2.0:
                position = (df.index[i], price, i)
            elif strategy == "buy_dip" and ret < -0.03 and vr > 2.0:
                position = (df.index[i], price, i)
            elif strategy == "momentum" and ret > 0.02 and vr > 1.5:
                position = (df.index[i], price, i)

    # Close any remaining position
    if position is not None:
        exit_ret = close.iloc[-1] / position[1] - 1
        trades.append({
            "entry": str(df.index[position[2]].date()),
            "exit": str(df.index[-1].date()),
            "return": float(exit_ret),
            "days": len(df) - 1 - position[2],
        })

    if not trades:
        return {"symbol": symbol, "strategy": strategy, "trades": 0, "note": "No events triggered"}

    returns = [t["return"] for t in trades]
    winners = [r for r in returns if r > 0]
    losers = [r for r in returns if r < 0]
    sum_winners = sum(winners)
    sum_losers = sum(losers)

    return {
        "symbol": symbol,
        "strategy": strategy,
        "holding_days": holding_days,
        "total_trades": len(trades),
        "win_rate": len(winners) / len(trades),
        "avg_return": sum(returns) / len(returns),
        "total_return": math.prod(1 + r for r in returns) - 1,
        "best_trade": max(returns),
        "worst_trade": min(returns),
        "avg_winner": sum_winners / len(winners) if winners else 0,
        "avg_loser": sum_losers / len(losers) if losers else 0,
        "profit_factor": abs(sum_winners / sum_losers) if sum_losers else (None if sum_winners else 0.0),
        "trades": trades[-10:],  # Last 10 trades
    }


# ---------------------------------------------------------------------------
# Full scanner: news + events + backtest
# ---------------------------------------------------------------------------
def scan_ticker(symbol: str, horizons: list[str] | None = None, start: str = "2022-01-01") -> dict:
    """Full catalyst scan for a ticker.

    1. Fetch news (yfinance + Finnhub if available)
    2. Analyze historical event patterns
    3. Run event-driven backtests (buy_spike, buy_dip, momentum)
    """
    if horizons is None:
        horizons = ["3m", "6m", "1y"]

    print(f"\n{'='*60}")
    print(f"  Catalyst Scan: {symbol}")
    print(f"{'='*60}")

    # 1. Recent news
    print("\n  Fetching news...")
    news = fetch_news_yfinance(symbol)
    finnhub_news = fetch_news_finnhub(symbol)
    all_news = news + finnhub_news
    print(f"  Found {len(all_news)} news items")
    for n in all_news[:5]:
        print(f"    [{n['type']}] {n['date']} — {n['title'][:70]}")

    # Fetch OHLCV once for all downstream analysis
    ohlcv = fetch_ohlcv(symbol, start=start)

    # 2. Event pattern analysis
    print("\n  Analyzing historical event patterns...")
    patterns = analyze_event_patterns(symbol, start=start, df=ohlcv)
    if "total_events" in patterns:
        print(f"  Found {patterns['total_events']} significant events "
              f"({patterns['up_events']} up, {patterns['down_events']} down)")
        if "after_up_event" in patterns:
            au = patterns["after_up_event"]
            print(f"  After UP events: +{au['avg_post_5d']:.1%} (5d), "
                  f"+{au['avg_post_10d']:.1%} (10d), +{au['avg_post_20d']:.1%} (20d)")
        if "after_down_event" in patterns:
            ad = patterns["after_down_event"]
            print(f"  After DOWN events: {ad['avg_post_5d']:+.1%} (5d), "
                  f"{ad['avg_post_10d']:+.1%} (10d), {ad['avg_post_20d']:+.1%} (20d)")

    # 3. Event-driven backtests
    print("\n  Running event-driven backtests...")
    backtest_results = {}
    for strat in ["buy_spike", "buy_dip", "momentum"]:
        for hold in [5, 10, 20]:
            result = event_driven_backtest(symbol, start=start, strategy=strat, holding_days=hold, df=ohlcv)
            key = f"{strat}_{hold}d"
            backtest_results[key] = result
            if result.get("total_trades", 0) > 0:
                print(f"  {key:20s} | Trades: {result['total_trades']:3d} | "
                      f"Win: {result['win_rate']:.0%} | "
                      f"Avg: {result['avg_return']:+.1%} | "
                      f"Total: {result['total_return']:+.1%}")

    return {
        "symbol": symbol,
        "news": all_news[:10],
        "event_patterns": patterns,
        "backtests": backtest_results,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="News catalyst scanner + short-horizon backtester")
    parser.add_argument("symbol", help="Ticker symbol (e.g., NTDOY, DIS, TTWO)")
    parser.add_argument("--start", default="2022-01-01", help="Backtest start date")
    args = parser.parse_args()

    results = scan_ticker(args.symbol, start=args.start)

    # Save results
    out_dir = Path(__file__).parent / "knowledge" / "catalyst_scans"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M")
    out_path = out_dir / f"{args.symbol}_{ts}.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    print(f"\n  Results saved to: {out_path}")


if __name__ == "__main__":
    main()

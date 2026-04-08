"""StockPicker — AI-powered stock pick analyzer for agents-assemble.

Given user-selected tickers, this engine:
1. Fetches data (adding to cache/universe if new)
2. Matches stocks to best-fit strategies from our 90+ backtested strategies
3. Runs a fresh backtest with those stocks
4. Generates vol-adjusted position recommendations
5. Suggests additional similar tickers that strengthen the strategy
6. Sends results to Claude for AI commentary
7. Returns everything for the GUI

This is a CORE feature — after Leaderboard and Trade tabs.
"""

from __future__ import annotations

import json
import math
import sys
import time
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))


# ---------------------------------------------------------------------------
# Strategy registry — load ALL strategy modules
# ---------------------------------------------------------------------------
def _load_all_strategies() -> list[dict[str, Any]]:
    """Load every strategy from every module, with universe info."""
    strategies = []

    def _add(keys, getter, source):
        for key in keys:
            try:
                persona = getter(key)
                strategies.append({
                    "key": key,
                    "source": source,
                    "getter": getter,
                    "persona": persona,
                    "universe": set(persona.config.universe),
                    "name": persona.config.name,
                    "description": persona.config.description,
                })
            except Exception:
                pass

    try:
        from personas import get_persona, ALL_PERSONAS
        _add(ALL_PERSONAS, get_persona, "generic")
    except Exception:
        pass
    try:
        from famous_investors import get_famous_investor, FAMOUS_INVESTORS
        _add(FAMOUS_INVESTORS, get_famous_investor, "famous")
    except Exception:
        pass
    try:
        from theme_strategies import get_theme_strategy, THEME_STRATEGIES
        _add(THEME_STRATEGIES, get_theme_strategy, "theme")
    except Exception:
        pass
    try:
        from recession_strategies import get_recession_strategy, RECESSION_STRATEGIES
        _add(RECESSION_STRATEGIES, get_recession_strategy, "recession")
    except Exception:
        pass
    try:
        from unconventional_strategies import get_unconventional_strategy, UNCONVENTIONAL_STRATEGIES
        _add(UNCONVENTIONAL_STRATEGIES, get_unconventional_strategy, "unconventional")
    except Exception:
        pass
    try:
        from research_strategies import get_research_strategy, RESEARCH_STRATEGIES
        _add(RESEARCH_STRATEGIES, get_research_strategy, "research")
    except Exception:
        pass
    try:
        from math_strategies import get_math_strategy, MATH_STRATEGIES
        _add(MATH_STRATEGIES, get_math_strategy, "math")
    except Exception:
        pass
    try:
        from political_strategies import get_political_strategy, POLITICAL_STRATEGIES
        _add(POLITICAL_STRATEGIES, get_political_strategy, "political")
    except Exception:
        pass
    try:
        from hedge_fund_strategies import get_hedge_fund_strategy, HEDGE_FUND_STRATEGIES
        _add(HEDGE_FUND_STRATEGIES, get_hedge_fund_strategy, "hedge_fund")
    except Exception:
        pass
    try:
        from news_event_strategies import get_news_event_strategy, NEWS_EVENT_STRATEGIES
        _add(NEWS_EVENT_STRATEGIES, get_news_event_strategy, "news_event")
    except Exception:
        pass
    try:
        from portfolio_strategies import get_portfolio_strategy, PORTFOLIO_STRATEGIES
        _add(PORTFOLIO_STRATEGIES, get_portfolio_strategy, "portfolio")
    except Exception:
        pass
    try:
        from crisis_commodity_strategies import get_crisis_commodity_strategy, CRISIS_COMMODITY_STRATEGIES
        _add(CRISIS_COMMODITY_STRATEGIES, get_crisis_commodity_strategy, "crisis")
    except Exception:
        pass
    try:
        from williams_seasonal_strategies import get_williams_seasonal_strategy, WILLIAMS_SEASONAL_STRATEGIES
        _add(WILLIAMS_SEASONAL_STRATEGIES, get_williams_seasonal_strategy, "williams_seasonal")
    except Exception:
        pass

    return strategies


# Cache the strategy registry (expensive to load)
_STRATEGY_CACHE: list[dict] | None = None


def _get_strategies() -> list[dict]:
    global _STRATEGY_CACHE
    if _STRATEGY_CACHE is None:
        _STRATEGY_CACHE = _load_all_strategies()
    return _STRATEGY_CACHE


# ---------------------------------------------------------------------------
# Stock info fetcher
# ---------------------------------------------------------------------------
def _get_stock_info(symbol: str) -> dict[str, Any]:
    """Get basic info for a stock — sector, industry, market cap, etc."""
    try:
        import yfinance as yf
        ticker = yf.Ticker(symbol)
        info = ticker.info
        return {
            "symbol": symbol,
            "name": info.get("longName", info.get("shortName", symbol)),
            "sector": info.get("sector", "Unknown"),
            "industry": info.get("industry", "Unknown"),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE"),
            "dividend_yield": info.get("dividendYield"),
            "beta": info.get("beta"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
        }
    except Exception:
        return {"symbol": symbol, "name": symbol, "sector": "Unknown", "industry": "Unknown"}


def _find_similar_tickers(symbol: str, stock_info: dict, all_strategies: list[dict], limit: int = 5) -> list[str]:
    """Find similar tickers from our universe based on sector/industry overlap."""
    sector = stock_info.get("sector", "")
    industry = stock_info.get("industry", "")

    # Collect all tickers from strategies that contain this symbol or similar sector
    candidates: dict[str, int] = {}  # ticker -> score
    for strat in all_strategies:
        universe = strat["universe"]
        if symbol in universe:
            # Tickers from same strategy = highly relevant
            for t in universe:
                if t != symbol:
                    candidates[t] = candidates.get(t, 0) + 3

    # Also find tickers from same sector/industry across all strategies
    if sector and sector != "Unknown":
        try:
            import yfinance as yf
            all_tickers = set()
            for strat in all_strategies:
                all_tickers.update(strat["universe"])

            for t in list(all_tickers)[:100]:  # Limit to avoid too many API calls
                try:
                    from data_fetcher import _canonical_cache_read
                    # Only check tickers we already have cached (no extra downloads)
                    cached = _canonical_cache_read(t)
                    if cached is not None:
                        info = yf.Ticker(t).info
                        if info.get("sector") == sector:
                            candidates[t] = candidates.get(t, 0) + 2
                            if info.get("industry") == industry:
                                candidates[t] = candidates.get(t, 0) + 2
                except Exception:
                    pass
        except Exception:
            pass

    # Sort by relevance score, return top N
    ranked = sorted(candidates.items(), key=lambda x: -x[1])
    return [t for t, _ in ranked[:limit] if t != symbol]


# ---------------------------------------------------------------------------
# Strategy matching
# ---------------------------------------------------------------------------
def _match_strategies(
    symbols: list[str],
    all_strategies: list[dict],
) -> list[dict]:
    """Find strategies that best match the user's stock picks.

    Scoring:
    - Direct universe overlap (stock is in strategy's universe)
    - Sector affinity (strategy focuses on same sector)
    - Historical performance of strategy
    """
    scored = []
    symbol_set = set(symbols)

    for strat in all_strategies:
        overlap = symbol_set & strat["universe"]
        if not overlap:
            continue
        # Score = overlap count + bonus for high overlap ratio
        overlap_ratio = len(overlap) / len(symbol_set)
        score = len(overlap) * 10 + overlap_ratio * 20
        scored.append({
            "key": strat["key"],
            "source": strat["source"],
            "name": strat["name"],
            "description": strat["description"],
            "getter": strat["getter"],
            "overlap": list(overlap),
            "overlap_ratio": overlap_ratio,
            "universe": list(strat["universe"]),
            "score": score,
        })

    # Sort by score
    scored.sort(key=lambda x: -x["score"])
    return scored


# ---------------------------------------------------------------------------
# Run backtest for matched strategy with user's tickers
# ---------------------------------------------------------------------------
def _run_backtest_for_pick(
    strategy_info: dict,
    extra_symbols: list[str],
    horizon: str = "3y",
) -> dict[str, Any]:
    """Run a backtest for the matched strategy."""
    from backtester import Backtester

    HORIZONS = {
        "1y": ("2024-01-01", "2024-12-31"),
        "3y": ("2022-01-01", "2024-12-31"),
        "5y": ("2020-01-01", "2024-12-31"),
    }
    start, end = HORIZONS.get(horizon, HORIZONS["3y"])

    try:
        persona = strategy_info["getter"](strategy_info["key"])
        # Use the strategy's full universe (includes user's picks if they overlap)
        symbols = persona.config.universe

        bt = Backtester(
            strategy=persona,
            symbols=symbols,
            start=start,
            end=end,
            initial_cash=100_000,
            benchmark="SPY",
            rebalance_frequency=persona.config.rebalance_frequency,
        )
        results = bt.run()
        return {
            "status": "success",
            "metrics": results["metrics"],
            "trade_metrics": results.get("trade_metrics", {}),
            "final_positions": results.get("final_positions", {}),
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


# ---------------------------------------------------------------------------
# Vol-adjusted position recommendations
# ---------------------------------------------------------------------------
def _safe_float(val, default=0.0):
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        f = float(val)
        return f if math.isfinite(f) else default
    return default


def _generate_position_table(
    user_symbols: list[str],
    additional_symbols: list[str],
    metrics: dict,
    portfolio_amount: float = 100_000,
) -> list[dict]:
    """Generate vol-adjusted position table for user + recommended tickers."""
    from data_fetcher import fetch_ohlcv

    total_ret = _safe_float(metrics.get("total_return"), 0.0)
    sharpe = _safe_float(metrics.get("sharpe_ratio"), 0.0)
    is_winning = total_ret > 0 and sharpe > 0
    max_dd = abs(_safe_float(metrics.get("max_drawdown"), 0.20))
    win_rate = _safe_float(metrics.get("win_rate"), 0.5)
    profit_factor = _safe_float(metrics.get("profit_factor"), 1.0)
    cagr = _safe_float(metrics.get("cagr"), 0.10)

    # Kelly fraction
    if profit_factor > 1 and win_rate > 0 and is_winning:
        avg_wl = profit_factor * (1 - win_rate) / win_rate if win_rate < 1 else 1
        kelly = win_rate - (1 - win_rate) / avg_wl if avg_wl > 0 else 0
        kelly = max(0.02, min(kelly, 0.25))
    else:
        kelly = 0.0

    base_stop = max(min(max_dd * 1.2, 0.25), 0.02)
    base_target = max(cagr * 0.5, 0.05)

    all_symbols = list(user_symbols) + [s for s in additional_symbols if s not in user_symbols]
    positions = []

    for sym in all_symbols:
        is_user_pick = sym in user_symbols
        try:
            df = fetch_ohlcv(sym, start="2024-06-01", cache=True)
            if len(df) < 20:
                continue
            last_price = float(df["Close"].iloc[-1])
            daily_vol = float(df["Close"].pct_change().std())
            ann_vol = daily_vol * (252 ** 0.5)

            # Vol-adjusted sizing
            vol_ratio = max(0.5, min(3.0, daily_vol / 0.015))
            adj_stop = min(base_stop * vol_ratio, 0.40)
            adj_target = max(base_target * vol_ratio, 0.03)
            adj_size = kelly / vol_ratio if is_winning else 0.0

            # If strategy is losing, user picks get size=0
            if not is_winning:
                adj_size = 0.0

            # Cap any single position at 20%
            adj_size = min(adj_size, 0.20)

            note = ""
            action = "BUY"
            if not is_winning:
                action = "HOLD"
                note = "Strategy underperforms — paper trade first"
            elif adj_size < 0.01:
                adj_size = 0.0
                action = "WATCH"
                note = "Too volatile for meaningful position"

            positions.append({
                "symbol": sym,
                "is_user_pick": is_user_pick,
                "action": action,
                "last_price": last_price,
                "annual_volatility": f"{ann_vol:.0%}",
                "entry_rule": "Limit 0.5% below market" if ann_vol < 0.30 else "Market order (volatile)",
                "stop_loss": f"{adj_stop:.1%} below entry",
                "take_profit": f"{adj_target:.1%} above entry",
                "position_size": f"{adj_size:.1%}",
                "position_dollars": f"${adj_size * portfolio_amount:,.0f}" if adj_size > 0 else "$0",
                "trailing_stop": f"{adj_stop * 0.7:.1%} trailing after {adj_target * 0.4:.1%} gain",
                "note": note,
                "tradingview_url": f"https://www.tradingview.com/chart/?symbol={sym}",
                "yahoo_url": f"https://finance.yahoo.com/quote/{sym}/",
            })
        except Exception:
            positions.append({
                "symbol": sym,
                "is_user_pick": is_user_pick,
                "action": "SKIP",
                "last_price": 0,
                "annual_volatility": "N/A",
                "entry_rule": "N/A",
                "stop_loss": "N/A",
                "take_profit": "N/A",
                "position_size": "0.0%",
                "position_dollars": "$0",
                "trailing_stop": "N/A",
                "note": "Could not fetch data",
                "tradingview_url": "",
                "yahoo_url": "",
            })

    return positions


# ---------------------------------------------------------------------------
# Claude AI commentary
# ---------------------------------------------------------------------------
def _get_claude_commentary(
    user_symbols: list[str],
    matched_strategy: dict | None,
    backtest_metrics: dict | None,
    positions: list[dict],
    stock_infos: list[dict],
) -> str:
    """Ask Claude to analyze the stock pick and strategy match."""
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
        from claude_code_client import ClaudeClient
        client = ClaudeClient(max_tokens=1500)
    except Exception:
        return "Claude AI analysis unavailable — claude_code_client not found."

    # Build a concise prompt
    picks_str = ", ".join(user_symbols)
    strat_name = matched_strategy["name"] if matched_strategy else "None"
    strat_desc = matched_strategy["description"] if matched_strategy else "N/A"

    metrics_str = "N/A"
    if backtest_metrics:
        ret = _safe_float(backtest_metrics.get("total_return"), 0)
        sharpe = _safe_float(backtest_metrics.get("sharpe_ratio"), 0)
        max_dd = _safe_float(backtest_metrics.get("max_drawdown"), 0)
        alpha = _safe_float(backtest_metrics.get("alpha"), 0)
        win_rate = _safe_float(backtest_metrics.get("win_rate"), 0)
        metrics_str = (
            f"Return: {ret:.1%}, Sharpe: {sharpe:.2f}, MaxDD: {max_dd:.1%}, "
            f"Alpha: {alpha:.1%}, Win Rate: {win_rate:.0%}"
        )

    # Stock info summary
    info_lines = []
    for info in stock_infos[:5]:
        name = info.get("name", info["symbol"])
        sector = info.get("sector", "?")
        pe = info.get("pe_ratio")
        pe_str = f", P/E: {pe:.1f}" if pe else ""
        info_lines.append(f"  {info['symbol']}: {name} ({sector}{pe_str})")
    info_str = "\n".join(info_lines)

    # Position summary
    pos_lines = []
    for p in positions[:8]:
        tag = "[USER PICK]" if p["is_user_pick"] else "[RECOMMENDED]"
        pos_lines.append(f"  {p['symbol']} {tag}: {p['action']} | Size: {p['position_size']} | Vol: {p['annual_volatility']}")
    pos_str = "\n".join(pos_lines)

    prompt = f"""You are a trading analyst for agents-assemble. A user picked these stocks: {picks_str}

Our system matched them to strategy: "{strat_name}" — {strat_desc}

Backtest results (3Y): {metrics_str}

Stock fundamentals:
{info_str}

Position recommendations:
{pos_str}

Give a SHORT (150 words max) analysis:
1. Is this a good pick combination? Why or why not?
2. What's the thesis/edge of the matched strategy?
3. Any risks or concerns?
4. One concrete actionable tip.

Be direct. Use plain language. No disclaimers — we already show those on the GUI."""

    try:
        result = client.ask(prompt)
        if isinstance(result, dict):
            text = result.get("result", result.get("text", ""))
        else:
            text = str(result)
        # Clean up — remove any system prefix
        if text and len(text) > 10:
            return text.strip()
    except Exception as e:
        return f"Claude analysis unavailable: {str(e)[:100]}"

    return "Claude analysis unavailable."


# ---------------------------------------------------------------------------
# Build one recommendation set for a given strategy match
# ---------------------------------------------------------------------------
def _build_recommendation(
    match: dict,
    valid_symbols: list[str],
    stock_infos: list[dict],
    all_strategies: list[dict],
    portfolio_amount: float,
    horizon: str,
    include_claude: bool,
) -> dict[str, Any]:
    """Build a complete recommendation for one strategy match."""
    # Run backtest
    backtest_result = _run_backtest_for_pick(match, valid_symbols, horizon)
    backtest_metrics = None
    if backtest_result.get("status") == "success":
        backtest_metrics = backtest_result["metrics"]

    # Additional tickers from strategy
    additional_tickers = [t for t in match["universe"] if t not in valid_symbols][:8]

    # Position table
    positions = _generate_position_table(
        valid_symbols, additional_tickers, backtest_metrics or {}, portfolio_amount,
    )

    # Hypothesis and explanation
    notes = []
    overlap = match.get("overlap", [])
    overlap_pct = match.get("overlap_ratio", 0)
    strategy_explanation = (
        f"Your picks matched **{match['name']}** ({match['source']}) — "
        f"{match['description']}. "
        f"{len(overlap)}/{len(valid_symbols)} of your picks are in this strategy's universe "
        f"({overlap_pct:.0%} overlap)."
    )
    hypothesis = (
        f"This strategy was backtested over {horizon} with {len(match['universe'])} stocks. "
    )
    if backtest_metrics:
        ret = _safe_float(backtest_metrics.get("total_return"), 0)
        sharpe = _safe_float(backtest_metrics.get("sharpe_ratio"), 0)
        max_dd = _safe_float(backtest_metrics.get("max_drawdown"), 0)
        hypothesis += f"Results: {ret:.1%} return, {sharpe:.2f} Sharpe, {max_dd:.1%} max drawdown. "
        if sharpe > 1.0:
            hypothesis += "This is an EXCELLENT risk-adjusted performer."
        elif sharpe > 0.5:
            hypothesis += "This is a GOOD strategy with acceptable risk."
        elif sharpe > 0:
            hypothesis += "This strategy is marginally positive — use as diversifier only."
        else:
            hypothesis += "This strategy UNDERPERFORMS — proceed with caution."
            notes.append("Strategy has negative or zero Sharpe — consider paper trading first")
        if ret < 0:
            notes.append("Negative total return — your picks may be in a losing strategy pattern")
    else:
        hypothesis += "Backtest could not be completed."

    # Check for meh picks
    meh_picks = [p["symbol"] for p in positions if p["is_user_pick"] and p["position_size"] == "0.0%"]
    if meh_picks:
        notes.append(
            f"Tickers {', '.join(meh_picks)} have 0% allocation — "
            f"the matched strategy doesn't support profitable positioning for these. "
            f"They may be too volatile, in a downtrend, or lack an identifiable edge."
        )

    # Claude commentary (only for primary recommendation to save API calls)
    claude_analysis = ""
    if include_claude:
        claude_analysis = _get_claude_commentary(
            valid_symbols, match, backtest_metrics, positions, stock_infos
        )

    return {
        "matched_strategy": {
            "key": match["key"],
            "source": match["source"],
            "name": match["name"],
            "description": match["description"],
            "overlap": match.get("overlap", []),
            "overlap_ratio": match.get("overlap_ratio", 0),
            "universe_size": len(match["universe"]),
        },
        "backtest": {
            "horizon": horizon,
            "metrics": {
                k: round(v, 4) if isinstance(v, float) else v
                for k, v in (backtest_metrics or {}).items()
            },
            "trade_metrics": backtest_result.get("trade_metrics", {}) if backtest_result else {},
        } if backtest_metrics else None,
        "positions": positions,
        "additional_tickers": additional_tickers,
        "hypothesis": hypothesis,
        "strategy_explanation": strategy_explanation,
        "notes": notes,
        "claude_analysis": claude_analysis,
    }


# ---------------------------------------------------------------------------
# Main entry point — analyze user stock picks
# ---------------------------------------------------------------------------
def analyze_stock_picks(
    symbols: list[str],
    portfolio_amount: float = 100_000,
    horizon: str = "3y",
    include_claude: bool = True,
    top_n: int = 5,
) -> dict[str, Any]:
    """Analyze user's stock picks and return top N strategy recommendations.

    Args:
        symbols: List of ticker symbols (e.g. ["NVDA", "AAPL"])
        portfolio_amount: Portfolio size in dollars
        horizon: Backtest horizon ("1y", "3y", "5y")
        include_claude: Whether to get Claude AI commentary
        top_n: Number of strategy recommendations to return (default 5)

    Returns:
        {
            "user_picks": [...],
            "stock_info": [...],
            "recommendations": [{...}, {...}, ...],  # top N strategies
            "total_strategies_matched": int,
            "generated_at": "...",
        }
    """
    symbols = [s.upper().strip() for s in symbols if s.strip()]
    if not symbols:
        return {"error": "No symbols provided"}

    all_strategies = _get_strategies()

    # Step 1: Fetch data for all user symbols (adds to canonical cache)
    from data_fetcher import fetch_ohlcv
    stock_infos = []
    valid_symbols = []
    for sym in symbols:
        try:
            df = fetch_ohlcv(sym, start="2015-01-01", cache=True)
            if len(df) > 20:
                valid_symbols.append(sym)
                info = _get_stock_info(sym)
                stock_infos.append(info)
        except Exception:
            stock_infos.append({
                "symbol": sym, "name": sym,
                "sector": "Unknown", "industry": "Unknown",
                "error": "Could not fetch data — may be delisted or invalid ticker",
            })

    if not valid_symbols:
        return {
            "error": "None of the provided tickers have valid market data",
            "user_picks": symbols,
            "stock_info": stock_infos,
        }

    # Step 2: Match to strategies
    matches = _match_strategies(valid_symbols, all_strategies)

    # Step 3: If no direct match, try sector-based matching
    if not matches:
        sectors = {info.get("sector") for info in stock_infos if info.get("sector", "Unknown") != "Unknown"}
        sector_matches = []
        for strat in all_strategies:
            for t in list(strat["universe"])[:5]:
                try:
                    import yfinance as yf
                    t_info = yf.Ticker(t).info
                    if t_info.get("sector") in sectors:
                        sector_matches.append({
                            "key": strat["key"],
                            "source": strat["source"],
                            "name": strat["name"],
                            "description": strat["description"],
                            "getter": strat["getter"],
                            "overlap": [],
                            "overlap_ratio": 0.0,
                            "universe": list(strat["universe"]),
                            "score": 5,
                        })
                        break
                except Exception:
                    pass
        matches = sector_matches

    total_matched = len(matches)

    # Step 4: Build recommendations for top N matches
    recommendations = []
    for i, match in enumerate(matches[:top_n]):
        # Only ask Claude for the first recommendation (saves API cost)
        use_claude = include_claude and i == 0
        rec = _build_recommendation(
            match, valid_symbols, stock_infos, all_strategies,
            portfolio_amount, horizon, use_claude,
        )
        recommendations.append(rec)

    # If no matches at all, build a generic "no match" recommendation
    if not recommendations:
        additional = []
        for info in stock_infos[:2]:
            similar = _find_similar_tickers(info["symbol"], info, all_strategies, limit=4)
            additional.extend(similar)
        additional = list(dict.fromkeys(additional))[:8]
        positions = _generate_position_table(valid_symbols, additional, {}, portfolio_amount)
        recommendations.append({
            "matched_strategy": None,
            "backtest": None,
            "positions": positions,
            "additional_tickers": additional,
            "hypothesis": "No direct strategy match. Recommendations based on volatility analysis.",
            "strategy_explanation": (
                "Your stock picks don't directly match any of our 90+ backtested strategies. "
                "Consider the suggested tickers to build a more diversified position."
            ),
            "notes": ["No strategy match — recommendations are conservative (paper trade first)"],
            "claude_analysis": "",
        })

    return {
        "user_picks": valid_symbols,
        "invalid_picks": [s for s in symbols if s not in valid_symbols],
        "stock_info": stock_infos,
        "recommendations": recommendations,
        "total_strategies_matched": total_matched,
        "generated_at": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import sys
    symbols = sys.argv[1:] if len(sys.argv) > 1 else ["NVDA", "AAPL", "MSFT"]
    print(f"Analyzing: {symbols}")
    result = analyze_stock_picks(symbols, include_claude=False, top_n=3)
    print(f"Matched {result.get('total_strategies_matched', 0)} strategies, showing top {len(result.get('recommendations', []))}")
    for i, rec in enumerate(result.get("recommendations", [])):
        ms = rec.get("matched_strategy")
        name = ms["name"] if ms else "No Match"
        bt = rec.get("backtest")
        if bt and bt.get("metrics"):
            m = bt["metrics"]
            print(f"  [{i+1}] {name}: Ret={m.get('total_return',0):.1%} Sharpe={m.get('sharpe_ratio',0):.2f} DD={m.get('max_drawdown',0):.1%}")
        else:
            print(f"  [{i+1}] {name}: No backtest")
    print(json.dumps(result, indent=2, default=str))

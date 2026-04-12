"""Trade recommendation generator for agents-assemble.

Generates actionable trade recommendations from backtest results:
- Entry price and limit price
- Stop-loss and take-profit targets
- Position sizing
- Timing guidance
- Saves winning strategies to strategy/winning/
- Saves losing strategies to strategy/losing/
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import math

import pandas as pd


def _safe_float(val: Any, default: float = 0.0) -> float:
    """Coerce a value to float, returning default if non-numeric."""
    if isinstance(val, (int, float)) and not isinstance(val, bool):
        f = float(val)
        if math.isfinite(f):
            return f
    return default


def _strategy_risk_params(name: str, max_dd: float, vol: float, cagr: float, win_rate: float, is_winning: bool):
    """Generate strategy-SPECIFIC stop loss, take profit, entry style, and scaling.

    NOT a one-size-fits-all formula. Different strategy types need fundamentally
    different risk management.
    """
    n = name.lower()

    # --- PASSIVE / BUY-AND-HOLD: wide stops, rebalance-based exits ---
    if any(x in n for x in ["buffett", "bogle", "permanent_portfolio", "all_weather", "dividend_growth", "quality_dividend", "boring_compounder"]):
        sl = max(max_dd * 1.5, 0.25)  # Very wide — these recover from drawdowns
        tp = max(cagr * 1.0, 0.15)    # Full year's CAGR as target
        entry = "limit: DCA monthly regardless of price. Add more on 10%+ dips."
        scale = "Equal monthly contributions. Never try to time entry."
        return sl, tp, entry, scale

    # --- INCOME / DIVIDEND: no price stop, dividend-based exit ---
    if any(x in n for x in ["dividend", "income", "muni_bond", "midstream", "toll_road", "insurance_float", "high_yield_reit"]):
        sl = max(max_dd * 1.3, 0.20)  # Wide — income stocks recover
        tp = max(cagr * 0.8, 0.08)    # Modest — you hold for income not gains
        entry = "limit: Buy on ex-dividend date dips or when yield exceeds 5-year average."
        scale = "Build position over 4-6 weeks. Reinvest all dividends."
        return sl, tp, entry, scale

    # --- MOMENTUM / GROWTH: tight trailing stops ---
    if any(x in n for x in ["momentum", "ai_token", "ai_revolution", "concentrate", "subscription", "growth"]):
        sl = max(min(max_dd * 0.8, 0.18), 0.08)  # Tight — momentum reversal = exit fast
        tp = max(cagr * 0.6, 0.12)                 # Partial profit at 60% of annual
        entry = "limit: Buy on RSI pullback to 40-50 in confirmed uptrend. Never chase."
        scale = "Enter 50% initial, add 25% on first pullback, final 25% on trend confirmation."
        return sl, tp, entry, scale

    # --- URANIUM / COMMODITY CYCLE: very wide stops, cycle-aware ---
    if any(x in n for x in ["uranium", "commodity", "shipping", "tanker", "rare_earth"]):
        sl = max(min(max_dd * 1.5, 0.45), 0.20)  # Extremely wide — 50% drawdowns are normal
        tp = max(cagr * 0.7, 0.15)                 # Decent target — cycles spike hard
        entry = "limit: Buy on golden cross (SMA50 > SMA200). These are CYCLE trades — timing matters."
        scale = "Enter 30% at signal, add 30% on confirmation, hold 40% for cycle peak."
        return sl, tp, entry, scale

    # --- DEFENSE / POLICY: wide stops, event-driven ---
    if any(x in n for x in ["defense", "wartime", "policy_catalyst", "election", "presidential"]):
        sl = max(min(max_dd * 1.0, 0.20), 0.10)  # Moderate — policy doesn't reverse overnight
        tp = max(cagr * 0.5, 0.10)                 # Steady gains, not explosive
        entry = "limit: Buy on policy announcement day or day after. Backlogs are locked — dips are gifts."
        scale = "Enter 60% immediately on catalyst, add 40% if pullback within 2 weeks."
        return sl, tp, entry, scale

    # --- SEASONAL / CALENDAR: time-based exits, not price ---
    if any(x in n for x in ["january", "santa_claus", "triple_witching", "seasonal", "sell_in_may", "turn_of_month"]):
        sl = 0.08  # Tight — short holding period
        tp = max(cagr * 0.3, 0.03)  # Small — these are short-duration trades
        entry = "market: Enter on calendar date. Timing IS the strategy — don't wait for better price."
        scale = "Full position on entry date. Exit on exit date. No scaling needed."
        return sl, tp, entry, scale

    # --- INVERSE / SIGNAL: trigger-based, different from normal ---
    if any(x in n for x in ["oil_down", "job_loss", "wealth_barometer", "bonds_down", "dollar_weak", "vix_spike", "crisis_alpha", "retail_crash", "crypto_crash"]):
        sl = max(min(max_dd * 0.9, 0.15), 0.05)  # Moderate-tight — signal reversal = exit
        tp = max(cagr * 0.5, 0.08)                 # Capture the rotation, don't overstay
        entry = "market: Enter immediately when trigger fires. Speed matters more than price."
        scale = "Full position at trigger. No scaling — the signal is binary."
        return sl, tp, entry, scale

    # --- VALUE / CONTRARIAN: patient entry, wide stops ---
    if any(x in n for x in ["value", "graham", "deep", "contrarian", "fallen", "beaten", "dcf", "patent_cliff", "constellation"]):
        sl = max(min(max_dd * 1.2, 0.30), 0.12)  # Wide — value takes time
        tp = max(cagr * 0.8, 0.10)                 # Patient target
        entry = "limit: Buy below SMA200 or at RSI < 35. Value = patience. Don't rush."
        scale = "Enter in 3 tranches over 4-6 weeks as price confirms bottom."
        return sl, tp, entry, scale

    # --- HEDGE / DEFENSIVE: insurance, different rules ---
    if any(x in n for x in ["gold", "treasury", "defensive", "stagnation", "permanent", "safe", "hedge", "domino"]):
        sl = 0.15  # Moderate — hedges shouldn't lose much
        tp = max(cagr * 0.4, 0.05)  # Low — you hold these for protection not profit
        entry = "limit: Always hold some. Add more when SPY breaks below SMA200."
        scale = "Maintain 5-15% allocation. Add during fear, trim during euphoria."
        return sl, tp, entry, scale

    # --- AI BOOM CYCLE: specific exit logic ---
    if any(x in n for x in ["ai_infrastructure", "ai_application", "ai_adopter", "picks_and_shovels", "late_cycle_bubble"]):
        sl = max(min(max_dd * 0.9, 0.20), 0.10)
        tp = max(cagr * 0.5, 0.10)
        entry = "limit: Buy when NVDA above SMA50 (demand signal). Don't buy if NVDA below SMA200."
        scale = "Enter 40% initial, add on NVDA pullback to SMA50, full position on confirmation."
        return sl, tp, entry, scale

    # --- ORCHESTRATOR: auto-managed ---
    if any(x in n for x in ["regime", "orchestrator", "adaptive", "conservative"]):
        sl = max_dd * 1.0
        tp = cagr * 0.5
        entry = "market: Auto-managed. No manual entry needed — strategy self-adjusts weekly."
        scale = "Set it and forget it. Review quarterly."
        return sl, tp, entry, scale

    # --- REGIONAL: country-specific ---
    if any(x in n for x in ["singapore", "japan", "korean", "china", "uk_european", "latam", "emerging"]):
        sl = max(min(max_dd * 1.1, 0.25), 0.10)
        tp = max(cagr * 0.6, 0.08)
        entry = "limit: Buy when local market index is above SMA200. FX matters — check currency trend."
        scale = "Enter in 3 tranches over 2-4 weeks. Currency hedging optional."
        return sl, tp, entry, scale

    # --- PAIRS / STAT ARB: spread-based ---
    if any(x in n for x in ["pairs", "arb", "cointegration", "zscore"]):
        sl = 0.10  # Tight — if spread widens further, thesis is wrong
        tp = 0.05  # Small — you capture mean reversion, not trends
        entry = "limit: Enter when Z-score exceeds 2.0. Exit when Z returns to 0."
        scale = "Full position at entry. No scaling — it's a convergence trade."
        return sl, tp, entry, scale

    # --- DEFAULT: use metrics-based formula (only for truly unmatched strategies) ---
    sl = max(min(max_dd * 1.0, 0.25), 0.05)
    tp = max(cagr * 0.5, 0.05)
    entry = "limit: Buy 0.5% below market in uptrend." if vol < 0.20 else "market: Use market orders for volatile names."
    scale = "Enter in 3 tranches over 1-2 weeks."
    return sl, tp, entry, scale


STRATEGY_DIR = Path(__file__).parent / "strategy"
WINNING_DIR = STRATEGY_DIR / "winning"
LOSING_DIR = STRATEGY_DIR / "losing"


def _ensure_dirs():
    WINNING_DIR.mkdir(parents=True, exist_ok=True)
    LOSING_DIR.mkdir(parents=True, exist_ok=True)


def generate_trade_recommendations(
    name: str,
    metrics: dict[str, float],
    final_positions: dict[str, Any],
    equity_curve: pd.Series | None = None,
    persona_config: dict | None = None,
) -> dict[str, Any]:
    """Generate actionable trade recommendations from a strategy.

    Returns:
        Dict with strategy assessment, individual trade recs, and risk params.
    """
    total_ret = _safe_float(metrics.get("total_return"), 0.0)
    sharpe = _safe_float(metrics.get("sharpe_ratio"), 0.0)
    is_winning = total_ret > 0 and sharpe > 0

    # Risk parameters based on strategy performance
    max_dd = abs(_safe_float(metrics.get("max_drawdown"), 0.20))
    vol = _safe_float(metrics.get("annual_volatility"), 0.15)

    # Position sizing via Kelly criterion (simplified)
    win_rate = _safe_float(metrics.get("win_rate"), 0.5)
    profit_factor = _safe_float(metrics.get("profit_factor"), 1.0)
    if profit_factor > 1 and win_rate > 0 and is_winning:
        avg_win_loss_ratio = profit_factor * (1 - win_rate) / win_rate if win_rate < 1 else 1
        kelly_fraction = win_rate - (1 - win_rate) / avg_win_loss_ratio if avg_win_loss_ratio > 0 else 0
        kelly_fraction = max(0.02, min(kelly_fraction, 0.25))  # Floor at 2%, cap at 25%
    else:
        kelly_fraction = 0.0

    # Strategy-specific risk parameters (not generic formulas)
    cagr = _safe_float(metrics.get("cagr"), 0.10)
    stop_loss_pct, take_profit_pct, entry_style, scaling_advice = _strategy_risk_params(
        name, max_dd, vol, cagr, win_rate, is_winning
    )

    recs = {
        "strategy_name": name,
        "is_winning": is_winning,
        "generated_at": datetime.now().isoformat(),
        "overall_assessment": _assess_strategy(metrics),
        "risk_parameters": {
            "max_portfolio_allocation": f"{kelly_fraction:.1%}",
            "stop_loss": f"{stop_loss_pct:.1%}",
            "take_profit_target": f"{take_profit_pct:.1%}",
            "max_drawdown_tolerance": f"{max_dd:.1%}",
            "rebalance_frequency": persona_config.get("rebalance_frequency", "weekly") if persona_config else "weekly",
        },
        "execution_guidance": {
            "order_type": entry_style.split(":")[0] if ":" in entry_style else entry_style,
            "limit_offset": entry_style,
            "timing": _timing_guidance(metrics, name),
            "scaling": scaling_advice,
        },
        "position_recommendations": [],
        "metrics_summary": {
            "total_return": f"{total_ret:.2%}",
            "sharpe_ratio": f"{sharpe:.2f}",
            "max_drawdown": f"{_safe_float(metrics.get('max_drawdown'), 0.0):.2%}",
            "win_rate": f"{win_rate:.2%}",
            "alpha": f"{metrics['alpha']:.2%}" if isinstance(metrics.get('alpha'), (int, float)) and not isinstance(metrics.get('alpha'), bool) else "N/A",
        },
    }

    # Generate per-position recommendations with vol-adjusted risk
    vol_data = {}
    if final_positions:
        # Compute per-stock volatility from price data if available
        try:
            from data_fetcher import fetch_ohlcv
            for sym in list(final_positions.keys())[:15]:
                try:
                    df = fetch_ohlcv(sym, start="2024-06-01", cache=True)
                    if len(df) > 20:
                        vol_data[sym] = float(df["Close"].pct_change().std())
                except Exception:
                    pass
        except Exception:
            pass

        for sym, pos_info in final_positions.items():
            rec = _generate_position_rec(sym, pos_info, stop_loss_pct, take_profit_pct, kelly_fraction, vol_data)
            recs["position_recommendations"].append(rec)

    return recs


def _assess_strategy(metrics: dict[str, float]) -> str:
    """Generate overall strategy assessment."""
    sharpe = _safe_float(metrics.get("sharpe_ratio"), 0.0)
    alpha = _safe_float(metrics.get("alpha"), 0.0)
    total_ret = _safe_float(metrics.get("total_return"), 0.0)

    if sharpe > 1.0 and alpha > 0.05:
        return "STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence."
    elif sharpe > 0.5 and total_ret > 0.20:
        return "BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes."
    elif sharpe > 0 and total_ret > 0:
        return "HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy."
    elif sharpe <= 0 and total_ret < 0:
        return "AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign."
    else:
        return "NEUTRAL — Mixed signals. Paper trade before committing capital."


def _timing_guidance(metrics: dict[str, float], name: str = "") -> str:
    """Generate timing guidance. Three types only:

    1. SAFE TO BUY — invest anytime, risk managed by position sizing
    2. WAIT FOR SIGNAL — only invest when trigger fires
    3. ALWAYS ACTIVE — auto-managed, no timing needed
    """
    n = name.lower()

    # --- WAIT FOR SIGNAL: inverse/event strategies that need a trigger ---
    if "v_shape" in n:
        return "WAIT FOR SIGNAL: Only enter after a major crash (-15%+) when market starts recovering. Exit at take profit."
    if "retail_crash" in n:
        return "WAIT FOR SIGNAL: Only enter when retail sector is collapsing. Long e-commerce names. Exit when retail stabilizes."
    if "crypto" in n and ("crash" in n or "tradfi" in n):
        return "WAIT FOR SIGNAL: Only enter when crypto is crashing hard (-20%+). Long traditional banks. Exit when crypto stabilizes."
    if "oil_down" in n:
        return "WAIT FOR SIGNAL: Only enter when oil/energy is crashing. Long tech stocks that benefit from lower costs. Exit when energy recovers."
    if "dollar_weak" in n:
        return "WAIT FOR SIGNAL: Only enter when US dollar is weakening. Long emerging markets + gold. Exit when dollar strengthens."
    if "domino" in n and "nvidia" in n:
        return "WAIT FOR SIGNAL: Hold AI stocks normally. Switch to defensive ONLY when supply chain companies start breaking down."
    if "l_shape" in n or "stagnation" in n:
        return "WAIT FOR SIGNAL: Go max defensive ONLY during prolonged market downturn (3+ months). Otherwise hold small gold/bond insurance."
    if any(x in n for x in ["pairs", "arb", "reversion", "zscore", "cointegration"]):
        return "WAIT FOR SIGNAL: Only enter when price spread between paired stocks reaches extreme levels. Exit when spread normalizes."

    # --- ALWAYS ACTIVE: auto-managed ---
    if "regime" in n or "orchestrator" in n:
        return "ALWAYS ACTIVE: Auto-managed. Switches between growth and defensive weekly based on market conditions. No user timing needed."
    if "seasonal" in n or "sell_in_may" in n:
        return "ALWAYS ACTIVE: Calendar-based. Stocks Nov-Apr, bonds May-Oct. Just rebalance twice a year."

    # --- SAFE TO BUY: everything else. Risk managed by position sizing. ---
    # Only add specific timing note for strategies where it really matters
    if "job_loss" in n or "unemployment" in n:
        return "SAFE TO BUY. Even better: add more when hiring slows (staffing companies declining) — that's when companies accelerate automation spending."
    if "bonds_down" in n or "yield_curve" in n:
        return "SAFE TO BUY. Even better: add more when interest rates are rising — banks earn wider margins on loans."
    if "k_shape" in n or "wealth_barometer" in n:
        return "SAFE TO BUY. Even better: add more when discount retailers (Dollar Tree) are struggling — signals money flowing to premium brands."
    if "vix" in n and "buyback" in n:
        return "SAFE TO BUY. Even better: add more during market panic — these cash-rich companies buy back their own stock at discount prices."
    if "vix" in n or ("crisis" in n and "alpha" in n):
        return "SAFE TO BUY as portfolio insurance. Add more during market selloffs — fear creates the best prices in quality names."
    if "chain" in n and "nvidia" in n:
        return "SAFE TO BUY. Important: exit ALL positions if any company in the AI supply chain starts collapsing — domino risk."

    # For everything else: SAFE TO BUY, risk is managed by position sizing already
    return "SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically."


def _generate_position_rec(
    symbol: str,
    pos_info: dict[str, Any],
    base_stop_pct: float,
    base_target_pct: float,
    base_size_pct: float,
    vol_data: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Generate per-position recommendation with VOL-ADJUSTED risk.

    Each stock gets different stop/target/size based on its realized volatility:
    - High vol stocks (TSLA, NVDA): wider stop, smaller size
    - Low vol stocks (KO, PG): tighter stop, larger size
    """
    qty = _safe_float(pos_info.get("qty"), 0.0)
    action = "BUY" if qty > 0 else "SELL" if qty < 0 else "FLAT"

    tv_chart = f"https://www.tradingview.com/chart/?symbol={symbol}"
    yahoo_url = f"https://finance.yahoo.com/quote/{symbol}/"

    # Per-position vol-adjusted risk
    stock_vol = (vol_data or {}).get(symbol, 0.02)  # daily vol, default 2%
    ann_vol = stock_vol * (252 ** 0.5)
    # Scale: if stock vol is 2x average, stop is 2x wider, size is 0.5x
    vol_ratio = max(0.5, min(3.0, stock_vol / 0.015))  # Normalize to 1.5% baseline
    adj_stop = min(base_stop_pct * vol_ratio, 0.40)  # Cap at 40%
    adj_target = max(base_target_pct * vol_ratio, 0.03)  # Floor at 3%
    adj_size = base_size_pct / vol_ratio  # Inverse vol sizing

    return {
        "symbol": symbol,
        "action": action,
        "current_position": qty,
        "annual_volatility": f"{ann_vol:.0%}",
        "entry_rule": f"Limit 0.5% below market" if ann_vol < 0.30 else "Market order (volatile)",
        "stop_loss": f"{adj_stop:.1%} below entry",
        "take_profit": f"{adj_target:.1%} above entry",
        "position_size": f"{adj_size:.1%} of portfolio",
        "trailing_stop": f"{adj_stop * 0.7:.1%} trailing after {adj_target * 0.4:.1%} gain",
        "tradingview_url": tv_chart,
        "yahoo_url": yahoo_url,
    }


def save_strategy_recommendation(
    name: str,
    results: dict[str, Any],
    persona_config: dict | None = None,
    description: str = "",
    hypothesis: str = "",
) -> Path:
    """Save strategy recommendation to winning/ or losing/ directory."""
    _ensure_dirs()

    metrics = results.get("metrics", {})
    final_positions = results.get("final_positions", {})
    equity_curve = results.get("equity_curve")

    recs = generate_trade_recommendations(
        name, metrics, final_positions, equity_curve, persona_config
    )

    # Determine winning or losing
    is_winning = recs["is_winning"]
    target_dir = WINNING_DIR if is_winning else LOSING_DIR
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save as markdown for readability
    md_lines = [
        f"# {'WINNING' if is_winning else 'LOSING'} Strategy: {name}",
    ]
    if description:
        md_lines.append(f"\n> **What it does:** {description}")
    if hypothesis:
        md_lines.append(f">\n> **Hypothesis:** {hypothesis}")
    md_lines.extend([
        f"\n**Generated:** {recs['generated_at']}",
        f"**Assessment:** {recs['overall_assessment']}",
        "",
        "## Performance Summary",
    ])
    for k, v in recs["metrics_summary"].items():
        md_lines.append(f"- **{k}:** {v}")

    md_lines.extend(["", "## Risk Parameters"])
    for k, v in recs["risk_parameters"].items():
        md_lines.append(f"- **{k}:** {v}")

    md_lines.extend(["", "## Execution Guidance"])
    for k, v in recs["execution_guidance"].items():
        md_lines.append(f"- **{k}:** {v}")

    if recs["position_recommendations"]:
        md_lines.extend([
            "", "## Positions — Vol-Adjusted Risk (per-stock sizing)", "",
            "*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*", "",
            "| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |",
            "|--------|--------|-----|-------|-----------|-------------|------|------------|",
        ])
        for rec in recs["position_recommendations"]:
            sym = rec["symbol"]
            tv = f"[Chart](https://www.tradingview.com/chart/?symbol={sym})"
            yf = f"[Yahoo](https://finance.yahoo.com/quote/{sym}/)"
            vol_str = rec.get("annual_volatility", "?")
            md_lines.append(
                f"| **{sym}** | {rec['action']} | {vol_str} | {rec['entry_rule']} | "
                f"{rec['stop_loss']} | {rec['take_profit']} | "
                f"{rec['position_size']} | {tv} / {yf} |"
            )
        md_lines.extend([
            "",
            "> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.",
            "> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.",
            "> Click Live Price links for current market price. Apply % rules to calculate exact levels.",
            "",
        ])

    if not is_winning:
        md_lines.extend([
            "## Lessons Learned",
            "",
            "This strategy lost money. Key issues:",
            f"- Sharpe ratio: {_safe_float(metrics.get('sharpe_ratio'), 0.0):.2f} (target > 0.5)",
            f"- Max drawdown: {_safe_float(metrics.get('max_drawdown'), 0.0):.2%} (target > -20%)",
            f"- Alpha: {_safe_float(metrics.get('alpha'), 0.0):.2%} (target > 0%)" if isinstance(metrics.get('alpha'), (int, float)) and not isinstance(metrics.get('alpha'), bool) else "- Alpha: N/A (target > 0%)",
            "",
            "**DO NOT REPEAT** these patterns without fundamental strategy changes.",
        ])

    safe_name = name
    for ch in ('/', '\\', ':', '*', '?', '"', '<', '>', '|'):
        safe_name = safe_name.replace(ch, '_')
    safe_name = safe_name.replace("..", "_").lstrip(".")
    md_path = target_dir / f"{safe_name}_{timestamp}.md"
    md_path.write_text("\n".join(md_lines))

    # Also save raw JSON
    json_path = target_dir / f"{safe_name}_{timestamp}.json"
    json_path.write_text(json.dumps(recs, indent=2, default=str))

    return md_path


def save_all_recommendations(all_results: list[dict[str, Any]]) -> dict[str, Path]:
    """Save recommendations for all strategy results."""
    _ensure_dirs()
    paths = {}
    for r in all_results:
        if r.get("status") != "success":
            continue
        name = r["name"]
        path = save_strategy_recommendation(name, r, r.get("persona_config"))
        paths[name] = path
    return paths


if __name__ == "__main__":
    # Test with sample data
    sample_results = {
        "metrics": {
            "total_return": 0.99, "sharpe_ratio": 1.20, "max_drawdown": -0.166,
            "win_rate": 0.37, "profit_factor": 1.31, "alpha": 0.171,
            "cagr": 0.234, "annual_volatility": 0.167,
        },
        "final_positions": {
            "NVDA": {"qty": 50, "avg_cost": 120.5},
            "META": {"qty": 30, "avg_cost": 350.2},
        },
    }
    path = save_strategy_recommendation("momentum_test", sample_results)
    print(f"Saved to: {path}")
    print(path.read_text())

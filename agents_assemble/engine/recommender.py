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


STRATEGY_DIR = Path(__file__).resolve().parent.parent.parent / "strategy"
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

    # Stop-loss based on historical drawdown (floored at 2% to avoid noise-triggered exits)
    stop_loss_pct = max(min(max_dd * 1.2, 0.25), 0.02)

    # Take-profit based on CAGR and vol
    cagr = _safe_float(metrics.get("cagr"), 0.10)
    take_profit_pct = max(cagr * 0.5, 0.05)  # Half of annual return per position

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
            "order_type": "limit" if vol < 0.20 else "market",
            "limit_offset": "0.5% below current price for buys" if vol < 0.20 else "use market orders in volatile names",
            "timing": _timing_guidance(metrics),
            "scaling": "Enter in 3 tranches over 1-2 weeks to average in",
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
            from agents_assemble.data.fetcher import fetch_ohlcv
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


def _timing_guidance(metrics: dict[str, float]) -> str:
    """Generate timing guidance based on strategy characteristics."""
    vol = _safe_float(metrics.get("annual_volatility"), 0.15)
    win_rate = _safe_float(metrics.get("win_rate"), 0.5)

    if vol > 0.25:
        return "Wait for VIX spike > 25 to enter (buy fear). Avoid entering in low-vol complacency."
    elif win_rate < 0.40:
        return "Strategy has low win rate — enter only on strong setup days. Be patient."
    else:
        return "Enter on any weekly rebalance day. No specific timing edge detected."


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

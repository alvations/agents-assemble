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
    if profit_factor > 1 and win_rate > 0:
        avg_win_loss_ratio = profit_factor * (1 - win_rate) / win_rate if win_rate < 1 else 1
        kelly_fraction = win_rate - (1 - win_rate) / avg_win_loss_ratio if avg_win_loss_ratio > 0 else 0
        kelly_fraction = max(0, min(kelly_fraction, 0.25))  # Cap at 25%
    else:
        kelly_fraction = 0.05  # Minimum

    # Stop-loss based on historical drawdown
    stop_loss_pct = min(max_dd * 1.2, 0.25)  # 120% of historical max DD, capped at 25%

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
            "alpha": f"{metrics.get('alpha', 0):.2%}" if isinstance(metrics.get('alpha'), (int, float)) else "N/A",
        },
    }

    # Generate individual position recommendations
    if final_positions:
        for sym, pos_info in final_positions.items():
            rec = _generate_position_rec(sym, pos_info, stop_loss_pct, take_profit_pct, kelly_fraction)
            recs["position_recommendations"].append(rec)

    return recs


def _assess_strategy(metrics: dict[str, float]) -> str:
    """Generate overall strategy assessment."""
    sharpe = _safe_float(metrics.get("sharpe_ratio"), 0.0)
    alpha = _safe_float(metrics.get("alpha"), 0.0)
    max_dd = _safe_float(metrics.get("max_drawdown"), 0.0)
    total_ret = _safe_float(metrics.get("total_return"), 0.0)

    if sharpe > 1.0 and alpha > 0.05:
        return "STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence."
    elif sharpe > 0.5 and total_ret > 0.20:
        return "BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes."
    elif sharpe > 0 and total_ret > 0:
        return "HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy."
    elif sharpe < 0 and total_ret < 0:
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
    stop_loss_pct: float,
    take_profit_pct: float,
    position_size_pct: float,
) -> dict[str, Any]:
    """Generate recommendation for a single position."""
    avg_cost = _safe_float(pos_info.get("avg_cost"), 0.0)
    qty = _safe_float(pos_info.get("qty"), 0.0)

    if qty > 0:
        action = "BUY"
    elif qty < 0:
        action = "SELL"
    else:
        action = "FLAT"

    if avg_cost > 0 and qty != 0:
        if qty > 0:
            stop_price = avg_cost * (1 - stop_loss_pct)
            target_price = avg_cost * (1 + take_profit_pct)
            stop_label = "below"
            target_label = "above"
            limit_price = avg_cost * 0.995
            limit_desc = "0.5% below avg cost"
        else:
            stop_price = avg_cost * (1 + stop_loss_pct)
            target_price = avg_cost * (1 - take_profit_pct)
            stop_label = "above"
            target_label = "below"
            limit_price = avg_cost * 1.005
            limit_desc = "0.5% above avg cost"
        entry_info = {
            "limit_price": f"${limit_price:.2f} ({limit_desc})",
            "market_price": "Use market order if volatile",
        }
        stop_str = f"${stop_price:.2f} ({stop_loss_pct:.1%} {stop_label} entry)"
        target_str = f"${target_price:.2f} ({take_profit_pct:.1%} {target_label} entry)"
    else:
        entry_info = {"limit_price": "N/A (no cost basis)", "market_price": "N/A"}
        stop_str = "N/A (no cost basis)"
        target_str = "N/A (no cost basis)"

    return {
        "symbol": symbol,
        "action": action,
        "current_position": qty,
        "avg_cost_basis": f"${avg_cost:.2f}" if avg_cost > 0 else "N/A",
        "recommended_entry": entry_info,
        "stop_loss": stop_str,
        "take_profit": target_str,
        "position_size": f"{position_size_pct:.1%} of portfolio",
        "trailing_stop": f"{stop_loss_pct * 0.8:.1%} trailing stop after {take_profit_pct * 0.5:.1%} gain",
    }


def save_strategy_recommendation(
    name: str,
    results: dict[str, Any],
    persona_config: dict | None = None,
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
        f"**Generated:** {recs['generated_at']}",
        f"**Assessment:** {recs['overall_assessment']}",
        "",
        "## Performance Summary",
    ]
    for k, v in recs["metrics_summary"].items():
        md_lines.append(f"- **{k}:** {v}")

    md_lines.extend(["", "## Risk Parameters"])
    for k, v in recs["risk_parameters"].items():
        md_lines.append(f"- **{k}:** {v}")

    md_lines.extend(["", "## Execution Guidance"])
    for k, v in recs["execution_guidance"].items():
        md_lines.append(f"- **{k}:** {v}")

    if recs["position_recommendations"]:
        md_lines.extend(["", "## Position Recommendations", ""])
        for rec in recs["position_recommendations"]:
            md_lines.append(f"### {rec['symbol']} — {rec['action']}")
            md_lines.append(f"- Entry limit: {rec['recommended_entry']['limit_price']}")
            md_lines.append(f"- Stop-loss: {rec['stop_loss']}")
            md_lines.append(f"- Take-profit: {rec['take_profit']}")
            md_lines.append(f"- Position size: {rec['position_size']}")
            md_lines.append(f"- Trailing stop: {rec['trailing_stop']}")
            md_lines.append("")

    if not is_winning:
        md_lines.extend([
            "## Lessons Learned",
            "",
            "This strategy lost money. Key issues:",
            f"- Sharpe ratio: {_safe_float(metrics.get('sharpe_ratio'), 0.0):.2f} (target > 0.5)",
            f"- Max drawdown: {_safe_float(metrics.get('max_drawdown'), 0.0):.2%} (target > -20%)",
            f"- Alpha: {_safe_float(metrics.get('alpha'), 0.0):.2%} (target > 0%)" if isinstance(metrics.get('alpha'), (int, float)) else "- Alpha: N/A (target > 0%)",
            "",
            "**DO NOT REPEAT** these patterns without fundamental strategy changes.",
        ])

    md_path = target_dir / f"{name}_{timestamp}.md"
    md_path.write_text("\n".join(md_lines))

    # Also save raw JSON
    json_path = target_dir / f"{name}_{timestamp}.json"
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
        path = save_strategy_recommendation(name, r)
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

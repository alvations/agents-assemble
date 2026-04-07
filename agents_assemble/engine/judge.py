"""Hypothesis judge for agents-assemble.

Analyzes backtest results, identifies weaknesses in trading strategies,
suggests parameter tuning, and ranks strategies for deployment.

Can optionally use Claude (via claude_code_client) for deeper analysis.
"""

from __future__ import annotations

import math
from datetime import datetime
from pathlib import Path
from typing import Any


KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"


# ---------------------------------------------------------------------------
# Scoring rubric
# ---------------------------------------------------------------------------
METRICS_WEIGHTS = {
    "sharpe_ratio": 0.25,
    "sortino_ratio": 0.15,
    "total_return": 0.15,
    "max_drawdown": 0.15,  # Inverted — less negative is better
    "alpha": 0.15,
    "win_rate": 0.05,
    "profit_factor": 0.05,
    "calmar_ratio": 0.05,
}

# Benchmark thresholds for grading
GRADE_THRESHOLDS = {
    "sharpe_ratio": {"A": 1.5, "B": 1.0, "C": 0.5, "D": 0.0, "F": -999},
    "sortino_ratio": {"A": 2.0, "B": 1.2, "C": 0.5, "D": 0.0, "F": -999},
    "total_return": {"A": 0.50, "B": 0.25, "C": 0.10, "D": 0.0, "F": -999},
    "max_drawdown": {"A": -0.05, "B": -0.10, "C": -0.20, "D": -0.30, "F": -999},
    "alpha": {"A": 0.10, "B": 0.05, "C": 0.0, "D": -0.05, "F": -999},
    "win_rate": {"A": 0.55, "B": 0.50, "C": 0.45, "D": 0.40, "F": 0.0},
    "calmar_ratio": {"A": 2.0, "B": 1.0, "C": 0.5, "D": 0.0, "F": -999},
    "profit_factor": {"A": 2.0, "B": 1.5, "C": 1.1, "D": 1.0, "F": 0.0},
}

GRADE_SCORES = {"A": 100, "B": 80, "C": 60, "D": 40, "F": 20}

# Default values for missing metrics — 0 is misleading for some metrics
# (e.g., max_drawdown=0 means "no drawdown" which would falsely grade as A)
_METRIC_MISSING_DEFAULTS = {
    "max_drawdown": -1.0,
}


def _safe_float(value: Any) -> float:
    """Coerce a value to float, returning NaN for non-numeric types."""
    if isinstance(value, bool):
        return float("nan")
    if isinstance(value, (int, float)):
        return float(value)
    return float("nan")


def grade_metric(metric: str, value: float) -> str:
    """Grade a single metric value."""
    value = _safe_float(value)
    if not math.isfinite(value):
        return "F"
    thresholds = GRADE_THRESHOLDS.get(metric)
    if thresholds is None:
        return "F"
    for grade in ["A", "B", "C", "D"]:
        if value >= thresholds[grade]:
            return grade
    return "F"


def compute_composite_score(metrics: dict[str, float]) -> float:
    """Compute weighted composite score (0-100)."""
    score = 0.0
    for metric, weight in METRICS_WEIGHTS.items():
        value = metrics.get(metric, _METRIC_MISSING_DEFAULTS.get(metric, 0))
        grade = grade_metric(metric, value)
        score += GRADE_SCORES[grade] * weight
    return score


# ---------------------------------------------------------------------------
# Diagnosis engine
# ---------------------------------------------------------------------------
def diagnose_strategy(
    name: str,
    metrics: dict[str, float],
    trade_metrics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Diagnose a strategy's strengths and weaknesses.

    Returns:
        Dict with grades, diagnosis, and improvement suggestions.
    """
    grades = {}
    for metric in METRICS_WEIGHTS:
        value = metrics.get(metric, _METRIC_MISSING_DEFAULTS.get(metric, 0))
        grades[metric] = {
            "value": _safe_float(value),
            "grade": grade_metric(metric, value),
        }

    # Compute composite directly from already-graded values (avoids re-grading)
    composite = sum(
        GRADE_SCORES[grades[m]["grade"]] * w for m, w in METRICS_WEIGHTS.items()
    )

    # Identify strengths and weaknesses
    strengths = []
    weaknesses = []
    suggestions = []

    for metric, info in grades.items():
        if not math.isfinite(info["value"]):
            continue
        if info["grade"] in ("A", "B"):
            strengths.append(f"{metric}: {info['value']:.4f} ({info['grade']})")
        elif info["grade"] in ("D", "F"):
            weaknesses.append(f"{metric}: {info['value']:.4f} ({info['grade']})")

    # Strategy-specific suggestions (use same defaults as scoring, NaN-safe)
    sharpe = _safe_float(metrics.get("sharpe_ratio"))
    max_dd = _safe_float(metrics.get("max_drawdown"))
    win_rate = _safe_float(metrics.get("win_rate"))
    alpha = _safe_float(metrics.get("alpha"))
    total_ret = _safe_float(metrics.get("total_return"))
    num_trades = _safe_float(trade_metrics.get("num_trades", 0)) if trade_metrics else 0

    if max_dd < -0.25:
        suggestions.append("Add trailing stop-loss (e.g., 15-20% from peak) to limit drawdowns")
        suggestions.append("Consider position sizing via Kelly criterion or vol-targeting")

    if win_rate < 0.40:
        suggestions.append("Low win rate — ensure winners are large enough (check profit factor)")
        suggestions.append("Consider tighter entry criteria or waiting for confirmation signals")

    if sharpe < 0 and total_ret < 0:
        suggestions.append("Strategy is destroying capital — consider inverting signals or switching regime")
        suggestions.append("Add regime detection (trending vs mean-reverting market filter)")

    if sharpe > 0 and alpha < 0:
        suggestions.append("Positive returns but negative alpha — strategy just follows market beta")
        suggestions.append("Reduce market exposure or add hedging (inverse ETF position in downtrends)")

    if num_trades > 500:
        suggestions.append("High trade count increases transaction costs — consider longer holding periods")
        suggestions.append("Increase rebalance frequency threshold or add minimum holding period")

    if num_trades < 20:
        suggestions.append("Very few trades — strategy may be too selective, missing opportunities")
        suggestions.append("Relax entry criteria or expand the universe of tradeable instruments")

    if sharpe > 1.0 and max_dd > -0.15:
        suggestions.append("Strong strategy! Consider scaling up position sizes gradually")
        suggestions.append("Test on different time periods to confirm robustness (2020, 2018-2019)")

    if not suggestions:
        suggestions.append("Strategy is performing adequately — focus on robustness testing across market regimes")

    return {
        "name": name,
        "composite_score": composite,
        "overall_grade": "A" if composite >= 85 else "B" if composite >= 70 else "C" if composite >= 55 else "D" if composite >= 40 else "F",
        "grades": grades,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "suggestions": suggestions,
    }


# ---------------------------------------------------------------------------
# Ranking and comparison
# ---------------------------------------------------------------------------
def rank_strategies(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Rank multiple strategy results by composite score."""
    ranked = []
    for r in results:
        if r.get("status") != "success" or "metrics" not in r:
            continue
        diagnosis = diagnose_strategy(
            r["name"], r["metrics"], r.get("trade_metrics")
        )
        ranked.append({
            "name": r["name"],
            "composite_score": diagnosis["composite_score"],
            "overall_grade": diagnosis["overall_grade"],
            "sharpe": _safe_float(r["metrics"].get("sharpe_ratio")),
            "alpha": _safe_float(r["metrics"].get("alpha")),
            "max_dd": _safe_float(r["metrics"].get("max_drawdown")),
            "total_return": _safe_float(r["metrics"].get("total_return")),
            "diagnosis": diagnosis,
        })

    # Use _safe_float to ensure NaN doesn't break sort (NaN sorts to bottom)
    ranked.sort(
        key=lambda x: (x["composite_score"], x["sharpe"] if math.isfinite(x["sharpe"]) else -999),
        reverse=True,
    )

    # Assign ranks
    for i, r in enumerate(ranked):
        r["rank"] = i + 1

    return ranked


def generate_judge_report(results: list[dict[str, Any]]) -> str:
    """Generate a comprehensive judge report."""
    ranked = rank_strategies(results)

    lines = [
        "# Strategy Judge Report",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Strategies evaluated:** {len(ranked)}",
        "",
        "## Rankings",
        "",
        "| Rank | Strategy | Score | Grade | Sharpe | Alpha | Max DD | Return |",
        "|------|----------|-------|-------|--------|-------|--------|--------|",
    ]

    def _fmt(val: float, fmt: str) -> str:
        return format(val, fmt) if math.isfinite(val) else "N/A"

    for r in ranked:
        lines.append(
            f"| {r['rank']} | {r['name']} | {r['composite_score']:.0f} | "
            f"{r['overall_grade']} | {_fmt(r['sharpe'], '.2f')} | "
            f"{_fmt(r['alpha'], '.2%')} | "
            f"{_fmt(r['max_dd'], '.1%')} | {_fmt(r['total_return'], '.1%')} |"
        )

    # Detail for each strategy
    for r in ranked:
        d = r["diagnosis"]
        lines.extend([
            f"\n## #{r['rank']} {r['name']} (Score: {d['composite_score']:.0f}, Grade: {d['overall_grade']})",
            "",
        ])
        if d["strengths"]:
            lines.append("**Strengths:**")
            for s in d["strengths"]:
                lines.append(f"- {s}")

        if d["weaknesses"]:
            lines.append("\n**Weaknesses:**")
            for w in d["weaknesses"]:
                lines.append(f"- {w}")

        lines.append("\n**Improvement Suggestions:**")
        for s in d["suggestions"]:
            lines.append(f"- {s}")

    # Deployment recommendation
    lines.extend([
        "\n## Deployment Recommendation",
        "",
    ])

    if ranked:
        best = ranked[0]
        if best["composite_score"] >= 70:
            lines.append(f"**Deploy:** {best['name']} (Score: {best['composite_score']:.0f})")
            lines.append(f"Start with small position sizes (25% of intended) for live validation.")
        else:
            lines.append("**No strategy meets deployment threshold (Score >= 70).**")
            lines.append("Continue iterating on strategy design and parameter tuning.")

        if len(ranked) >= 3:
            lines.append(f"\n**Ensemble candidate:** Combine top 3: "
                         f"{', '.join(r['name'] for r in ranked[:3])}")

    return "\n".join(lines)


def save_judge_report(results: list[dict[str, Any]]) -> Path:
    """Generate and save the judge report."""
    report = generate_judge_report(results)
    kb_dir = KNOWLEDGE_DIR / "judge_reports"
    kb_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = kb_dir / f"judge_report_{timestamp}.md"
    path.write_text(report)
    return path


# ---------------------------------------------------------------------------
# Parameter tuning suggestions
# ---------------------------------------------------------------------------
def suggest_parameter_tuning(
    name: str,
    metrics: dict[str, float],
    persona_config: dict[str, Any] | None = None,
) -> list[dict[str, str]]:
    """Suggest specific parameter changes based on performance."""
    suggestions = []
    sharpe = _safe_float(metrics.get("sharpe_ratio"))
    max_dd = _safe_float(metrics.get("max_drawdown"))
    win_rate = _safe_float(metrics.get("win_rate"))
    vol = _safe_float(metrics.get("annual_volatility"))

    if max_dd < -0.20:
        suggestions.append({
            "parameter": "max_position_size",
            "current": "0.20-0.30",
            "suggested": "0.10-0.15",
            "reason": f"Max drawdown {max_dd:.1%} is too severe. Smaller positions reduce concentration risk."
        })
        suggestions.append({
            "parameter": "stop_loss",
            "current": "None",
            "suggested": "0.15 (15% trailing stop)",
            "reason": "Add stop-loss to automatically exit losing positions before they compound."
        })

    if vol > 0.25:
        suggestions.append({
            "parameter": "rebalance_frequency",
            "current": "daily/weekly",
            "suggested": "monthly",
            "reason": f"Annual vol {vol:.1%} is high. Less frequent rebalancing reduces whipsaw losses."
        })

    if win_rate < 0.35:
        suggestions.append({
            "parameter": "entry_threshold",
            "current": "current RSI/BB levels",
            "suggested": "Tighten RSI to < 25 for buy, > 80 for sell",
            "reason": f"Win rate {win_rate:.1%} is low. More selective entries improve hit rate."
        })

    if sharpe > 0.8:
        suggestions.append({
            "parameter": "max_positions",
            "current": "8-10",
            "suggested": "6-8 (concentrate in winners)",
            "reason": f"Good Sharpe {sharpe:.2f} — concentrating in fewer high-conviction picks may increase returns."
        })

    return suggestions


if __name__ == "__main__":
    # Test with sample metrics
    sample = {
        "sharpe_ratio": 1.10,
        "sortino_ratio": 1.65,
        "total_return": 0.87,
        "max_drawdown": -0.16,
        "alpha": 0.146,
        "win_rate": 0.37,
        "profit_factor": 1.31,
        "calmar_ratio": 1.45,
        "annual_volatility": 0.17,
    }
    d = diagnose_strategy("momentum_test", sample, {"num_trades": 700})
    print(f"Composite Score: {d['composite_score']:.0f} ({d['overall_grade']})")
    print(f"\nStrengths: {d['strengths']}")
    print(f"\nWeaknesses: {d['weaknesses']}")
    print(f"\nSuggestions: {d['suggestions']}")

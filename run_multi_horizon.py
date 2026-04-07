"""Multi-horizon hypothesis testing for agents-assemble.

Tests every strategy across 1Y, 3Y, 5Y, and 10Y horizons.
Saves comprehensive comparison to knowledge/ and LEADERBOARD.md.

Usage:
    python run_multi_horizon.py                        # All strategies, all horizons
    python run_multi_horizon.py --persona momentum     # One strategy
    python run_multi_horizon.py --horizon 3y           # One horizon
    python run_multi_horizon.py --category research    # One category
"""

from __future__ import annotations

import argparse
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))

from backtester import Backtester, format_report
from personas import get_persona, ALL_PERSONAS
from famous_investors import get_famous_investor, FAMOUS_INVESTORS
from theme_strategies import get_theme_strategy, THEME_STRATEGIES
from recession_strategies import get_recession_strategy, RECESSION_STRATEGIES
from unconventional_strategies import get_unconventional_strategy, UNCONVENTIONAL_STRATEGIES
from research_strategies import get_research_strategy, RESEARCH_STRATEGIES
from math_strategies import get_math_strategy, MATH_STRATEGIES

KNOWLEDGE_DIR = Path(__file__).parent / "knowledge"
RESULTS_DIR = Path(__file__).parent / "results"

# ---------------------------------------------------------------------------
# Time horizons
# ---------------------------------------------------------------------------
HORIZONS = {
    "1y": ("2024-01-01", "2024-12-31"),
    "3y": ("2022-01-01", "2024-12-31"),
    "5y": ("2020-01-01", "2024-12-31"),
    "10y": ("2015-01-01", "2024-12-31"),
}

# Short horizons — backtester pre-loads 1 year of data for indicator warmup
SHORT_HORIZONS = {
    "1w": ("2024-12-23", "2024-12-31"),
    "2w": ("2024-12-16", "2024-12-31"),
    "1m": ("2024-12-01", "2024-12-31"),
    "3m": ("2024-10-01", "2024-12-31"),
    "6m": ("2024-07-01", "2024-12-31"),
}

ALL_HORIZONS = {**SHORT_HORIZONS, **HORIZONS}

# ---------------------------------------------------------------------------
# All strategy sources
# ---------------------------------------------------------------------------
def _get_all_strategies() -> List[Dict[str, Any]]:
    """Get flat list of all strategies with their source info."""
    strategies = []
    for key in ALL_PERSONAS:
        strategies.append({"key": key, "source": "generic", "getter": get_persona})
    for key in FAMOUS_INVESTORS:
        strategies.append({"key": key, "source": "famous", "getter": get_famous_investor})
    for key in THEME_STRATEGIES:
        strategies.append({"key": key, "source": "theme", "getter": get_theme_strategy})
    for key in RECESSION_STRATEGIES:
        strategies.append({"key": key, "source": "recession", "getter": get_recession_strategy})
    for key in UNCONVENTIONAL_STRATEGIES:
        strategies.append({"key": key, "source": "unconventional", "getter": get_unconventional_strategy})
    for key in RESEARCH_STRATEGIES:
        strategies.append({"key": key, "source": "research", "getter": get_research_strategy})
    for key in MATH_STRATEGIES:
        strategies.append({"key": key, "source": "math", "getter": get_math_strategy})
    return strategies


def run_single(strategy_info: Dict, horizon_name: str, start: str, end: str,
               verbose: bool = False) -> Dict[str, Any]:
    """Run a single strategy on a single horizon."""
    key = strategy_info["key"]
    try:
        persona = strategy_info["getter"](key)
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
        m = results["metrics"]

        if verbose:
            print(f"  {key:35s} | {horizon_name} | Ret: {m.get('total_return', 0):>7.1%} | "
                  f"Sharpe: {m.get('sharpe_ratio', 0):>6.2f} | MaxDD: {m.get('max_drawdown', 0):>7.1%}")

        return {
            "key": key,
            "source": strategy_info["source"],
            "horizon": horizon_name,
            "status": "success",
            "metrics": m,
            "trade_metrics": results.get("trade_metrics", {}),
            "final_positions": results.get("final_positions", {}),
        }
    except Exception as e:
        if verbose:
            print(f"  {key:35s} | {horizon_name} | ERROR: {str(e)[:50]}")
        return {
            "key": key,
            "source": strategy_info["source"],
            "horizon": horizon_name,
            "status": "error",
            "error": str(e),
        }


def run_multi_horizon(
    strategies: Optional[List[Dict]] = None,
    horizons: Optional[Dict[str, tuple]] = None,
    verbose: bool = True,
) -> pd.DataFrame:
    """Run all strategies across all horizons. Returns DataFrame of results."""
    if strategies is None:
        strategies = _get_all_strategies()
    if horizons is None:
        horizons = HORIZONS

    all_results = []
    total = len(strategies) * len(horizons)
    done = 0

    for horizon_name, (start, end) in horizons.items():
        if verbose:
            print(f"\n{'='*60}")
            print(f"  Horizon: {horizon_name} ({start} to {end})")
            print(f"{'='*60}")

        for strat in strategies:
            result = run_single(strat, horizon_name, start, end, verbose=verbose)
            all_results.append(result)
            done += 1

            if verbose and done % 10 == 0:
                print(f"  ... {done}/{total} complete")

    # Build results DataFrame
    rows = []
    for r in all_results:
        if r["status"] == "success":
            m = r["metrics"]
            rows.append({
                "strategy": r["key"],
                "source": r["source"],
                "horizon": r["horizon"],
                "total_return": m.get("total_return", 0),
                "cagr": m.get("cagr", 0),
                "sharpe": m.get("sharpe_ratio", 0),
                "sortino": m.get("sortino_ratio", 0),
                "max_drawdown": m.get("max_drawdown", 0),
                "alpha": m.get("alpha", None),
                "beta": m.get("beta", None),
                "win_rate": m.get("win_rate", 0),
                "num_trades": r.get("trade_metrics", {}).get("num_trades", 0),
            })
        else:
            rows.append({
                "strategy": r["key"],
                "source": r["source"],
                "horizon": r["horizon"],
                "total_return": None,
                "cagr": None,
                "sharpe": None,
                "sortino": None,
                "max_drawdown": None,
                "alpha": None,
                "beta": None,
                "win_rate": None,
                "num_trades": None,
                "error": r.get("error", ""),
            })

    df = pd.DataFrame(rows)
    return df


def save_multi_horizon_report(df: pd.DataFrame) -> Path:
    """Save multi-horizon comparison report."""
    kb_dir = KNOWLEDGE_DIR / "multi_horizon"
    kb_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save raw CSV
    csv_path = kb_dir / f"results_{timestamp}.csv"
    df.to_csv(csv_path, index=False)

    # Generate markdown report
    lines = [
        "# Multi-Horizon Backtest Results",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
    ]

    successes = df[df["total_return"].notna()]

    for horizon in ALL_HORIZONS:
        h_data = successes[successes["horizon"] == horizon].sort_values("sharpe", ascending=False)
        if h_data.empty:
            continue

        start, end = HORIZONS[horizon]
        lines.append(f"\n## {horizon.upper()} ({start} to {end})")
        lines.append("")
        lines.append("| Rank | Strategy | Source | Return | Sharpe | Max DD | Alpha |")
        lines.append("|------|----------|--------|--------|--------|--------|-------|")

        for rank, (_, row) in enumerate(h_data.head(15).iterrows(), 1):
            alpha = f"{row['alpha']:.1%}" if pd.notna(row.get('alpha')) else "N/A"
            lines.append(
                f"| {rank} | {row['strategy']} | {row['source']} | "
                f"{row['total_return']:.1%} | {row['sharpe']:.2f} | "
                f"{row['max_drawdown']:.1%} | {alpha} |"
            )

    # Cross-horizon consistency (strategies that rank well across ALL horizons)
    lines.append("\n## Cross-Horizon Consistency")
    lines.append("Strategies ranked by average Sharpe across all horizons:")
    lines.append("")

    avg_sharpe = successes.groupby("strategy")["sharpe"].mean().sort_values(ascending=False)
    std_sharpe = successes.groupby("strategy")["sharpe"].std().fillna(0)

    lines.append("| Strategy | Avg Sharpe | Std Sharpe | Consistent? |")
    lines.append("|----------|-----------|-----------|-------------|")
    for strat in avg_sharpe.head(15).index:
        avg = avg_sharpe[strat]
        std = std_sharpe.get(strat, 0)
        consistent = "YES" if avg > 0.3 and std < 0.5 else "MIXED" if avg > 0 else "NO"
        lines.append(f"| {strat} | {avg:.2f} | {std:.2f} | {consistent} |")

    md_path = kb_dir / f"report_{timestamp}.md"
    md_path.write_text("\n".join(lines))

    return md_path


def main():
    parser = argparse.ArgumentParser(description="Multi-horizon backtest runner")
    parser.add_argument("--persona", "-p", help="Run only this strategy")
    parser.add_argument("--category", "-c", help="Run only this category (generic/famous/theme/recession/unconventional/research/math)")
    parser.add_argument("--horizon", help="Run only this horizon (1w/2w/1m/3m/6m/1y/3y/5y/10y)")
    parser.add_argument("--short", action="store_true", help="Include short horizons (1w/2w/1m/3m/6m)")
    parser.add_argument("--all-horizons", action="store_true", help="Run ALL horizons (short + long)")
    parser.add_argument("--quiet", "-q", action="store_true")
    args = parser.parse_args()

    strategies = _get_all_strategies()
    if args.all_horizons:
        horizons = ALL_HORIZONS
    elif args.short:
        horizons = SHORT_HORIZONS
    else:
        horizons = HORIZONS

    if args.persona:
        strategies = [s for s in strategies if s["key"] == args.persona]
        if not strategies:
            parser.error(f"Unknown strategy: {args.persona}")
    if args.category:
        strategies = [s for s in strategies if s["source"] == args.category]
        if not strategies:
            parser.error(f"Unknown category: {args.category}")
    if args.horizon:
        if args.horizon not in ALL_HORIZONS:
            parser.error(f"Unknown horizon: {args.horizon!r}. Choose from: {', '.join(ALL_HORIZONS)}")
        horizons = {args.horizon: ALL_HORIZONS[args.horizon]}

    print(f"Running {len(strategies)} strategies x {len(horizons)} horizons = {len(strategies) * len(horizons)} backtests")

    df = run_multi_horizon(strategies, horizons, verbose=not args.quiet)
    report_path = save_multi_horizon_report(df)

    successes = df[df["total_return"].notna()]
    errors = df[df["total_return"].isna()]
    print(f"\nDone: {len(successes)} succeeded, {len(errors)} failed")
    print(f"Report: {report_path}")


if __name__ == "__main__":
    main()
# Short horizons: 1w/2w/1m/3m/6m now supported

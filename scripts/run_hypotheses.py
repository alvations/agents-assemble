"""Hypothesis testing runner for agents-assemble.

Runs each persona's strategy through the backtester, compares results,
and saves all findings to the knowledge base.

Usage:
    python run_hypotheses.py                    # Run all personas
    python run_hypotheses.py --persona buffett  # Run one persona
    python run_hypotheses.py --start 2022-01-01 --end 2024-12-31
"""

from __future__ import annotations

import argparse
import json
import sys
import traceback
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

# Support both installed package and flat-file imports
_REPO_ROOT = Path(__file__).parent.parent  # repo root (parent of scripts/)
sys.path.insert(0, str(_REPO_ROOT))

try:
    from agents_assemble.engine.backtester import Backtester, format_report, save_results
    from agents_assemble.strategies.generic import ALL_PERSONAS, get_persona, list_personas
    from agents_assemble.strategies.famous import FAMOUS_INVESTORS, get_famous_investor, list_famous_investors
    from agents_assemble.strategies.themes import THEME_STRATEGIES, get_theme_strategy, list_theme_strategies
    from agents_assemble.strategies.recession import RECESSION_STRATEGIES, get_recession_strategy
    from agents_assemble.engine.recommender import save_strategy_recommendation
except ImportError:
    from backtester import Backtester, format_report, save_results
    from personas import ALL_PERSONAS, get_persona, list_personas
    from famous_investors import FAMOUS_INVESTORS, get_famous_investor, list_famous_investors
    from theme_strategies import THEME_STRATEGIES, get_theme_strategy, list_theme_strategies
    from recession_strategies import RECESSION_STRATEGIES, get_recession_strategy
    from trade_recommender import save_strategy_recommendation

try:
    from agents_assemble.strategies.unconventional import UNCONVENTIONAL_STRATEGIES, get_unconventional_strategy
except ImportError:
    try:
        from unconventional_strategies import UNCONVENTIONAL_STRATEGIES, get_unconventional_strategy
    except ImportError:
        UNCONVENTIONAL_STRATEGIES = {}
        def get_unconventional_strategy(name, **kw): raise ImportError("unconventional_strategies not available")


# ---------------------------------------------------------------------------
# Knowledge base
# ---------------------------------------------------------------------------
KNOWLEDGE_DIR = _REPO_ROOT / "knowledge"
RESULTS_DIR = _REPO_ROOT / "results"


def save_to_knowledge(name: str, content: str, category: str = "hypothesis") -> Path:
    """Save a finding to the knowledge base."""
    kb_dir = KNOWLEDGE_DIR / category
    kb_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = kb_dir / f"{name}_{timestamp}.md"
    path.write_text(content)
    return path


def save_result_json(name: str, data: Dict[str, Any]) -> Path:
    """Save backtest results as JSON."""
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = RESULTS_DIR / f"{name}_{timestamp}.json"
    # Serialize carefully
    serializable = {}
    for k, v in data.items():
        if isinstance(v, pd.Series):
            serializable[k] = {str(idx): float(val) for idx, val in v.items()}
        elif isinstance(v, pd.DataFrame):
            serializable[k] = v.to_dict()
        elif isinstance(v, list):
            serializable[k] = str(v)[:2000]  # Truncate large lists
        elif isinstance(v, dict):
            serializable[k] = {str(kk): vv for kk, vv in v.items()
                                if isinstance(vv, (int, float, str, bool, type(None)))}
        else:
            try:
                json.dumps(v)
                serializable[k] = v
            except (TypeError, ValueError):
                serializable[k] = str(v)[:500]
    path.write_text(json.dumps(serializable, indent=2, default=str))
    return path


# ---------------------------------------------------------------------------
# Hypothesis definitions
# ---------------------------------------------------------------------------
HYPOTHESES = [
    {
        "name": "buffett_value_beats_spy",
        "persona": "buffett_value",
        "hypothesis": "Buffett-style value investing in blue chips outperforms SPY on a risk-adjusted basis over 3+ years",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "momentum_tech_leaders",
        "persona": "momentum",
        "hypothesis": "Momentum strategy in tech leaders captures trends while limiting drawdowns via MACD exits",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "meme_stocks_2021_2024",
        "persona": "meme_stock",
        "hypothesis": "Meme stock volume-spike strategy generates high returns but with extreme volatility",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "dividend_aristocrats_stability",
        "persona": "dividend",
        "hypothesis": "Dividend investing provides stable returns with low drawdowns vs SPY",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "quant_mean_reversion",
        "persona": "quant",
        "hypothesis": "Mean-reversion (buy BB lower + low RSI) generates alpha in large caps",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "fixed_income_duration",
        "persona": "fixed_income",
        "hypothesis": "Dynamic duration management via bond ETF trends beats static bond allocation (BND) during rate hike cycle",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "growth_disruption",
        "persona": "growth",
        "hypothesis": "Buying dips in disruptive growth stocks during uptrends outperforms, but with high volatility",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "sector_rotation_outperforms",
        "persona": "sector_rotation",
        "hypothesis": "Rotating into top-momentum sector ETFs outperforms broad market SPY",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "pairs_relative_value",
        "persona": "pairs",
        "hypothesis": "Pairs trading correlated stocks (XOM/CVX, KO/PEP, etc.) generates market-neutral alpha",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "ensemble_consensus",
        "persona": "ensemble",
        "hypothesis": "Multi-strategy consensus (momentum+value+growth+dividend) beats any single strategy on risk-adjusted basis",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    # === Famous Investors ===
    {
        "name": "peter_lynch_garp",
        "persona": "peter_lynch",
        "persona_source": "famous",
        "hypothesis": "Peter Lynch GARP: moderate momentum consumer stocks with low vol outperform",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "ray_dalio_all_weather",
        "persona": "ray_dalio",
        "persona_source": "famous",
        "hypothesis": "Dalio All-Weather risk parity (stocks+bonds+gold+commodities) provides stable returns in any regime",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "george_soros_reflexivity",
        "persona": "george_soros",
        "persona_source": "famous",
        "hypothesis": "Soros reflexivity: concentrated macro momentum bets capture accelerating trends",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "michael_burry_contrarian",
        "persona": "michael_burry",
        "persona_source": "famous",
        "hypothesis": "Burry contrarian: buying capitulation in beaten-down large caps generates deep value alpha",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "jim_simons_quant",
        "persona": "jim_simons",
        "persona_source": "famous",
        "hypothesis": "Simons multi-factor quant: combining mean-reversion + momentum + trend + BB generates consistent alpha",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "carl_icahn_activist",
        "persona": "carl_icahn",
        "persona_source": "famous",
        "hypothesis": "Icahn activist value: concentrated deep-discount large caps showing recovery outperform",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "masayoshi_son_vision",
        "persona": "masayoshi_son",
        "persona_source": "famous",
        "hypothesis": "Son Vision Fund: concentrated high-conviction tech platform bets capture outsized returns",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "li_ka_shing_infrastructure",
        "persona": "li_ka_shing",
        "persona_source": "famous",
        "hypothesis": "Li Ka-shing: patient infrastructure/utility value provides stable income with low drawdowns",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "sawiris_em_industrials",
        "persona": "nassef_sawiris",
        "persona_source": "famous",
        "hypothesis": "Sawiris: emerging market industrial value (materials, mining) outperforms during commodity cycles",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "lemann_consumer_brands",
        "persona": "jorge_paulo_lemann",
        "persona_source": "famous",
        "hypothesis": "Lemann 3G: buying dominant consumer brands on pullbacks compounds steadily",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "alwaleed_crisis_buying",
        "persona": "prince_alwaleed",
        "persona_source": "famous",
        "hypothesis": "Alwaleed: buying iconic blue-chip brands during crises generates recovery alpha",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "howard_marks_contrarian",
        "persona": "howard_marks",
        "persona_source": "famous",
        "hypothesis": "Marks second-level thinking: buying quality during market panic outperforms on risk-adjusted basis",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "support_resistance_commodities",
        "persona": "support_resistance",
        "persona_source": "famous",
        "hypothesis": "Support/resistance breakout on commodity ETFs captures trend reversals with defined risk",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    # === Theme Strategies ===
    {
        "name": "ai_revolution_2022_2024",
        "persona": "ai_revolution",
        "persona_source": "theme",
        "hypothesis": "AI infrastructure and applications companies outperform during the AI boom",
        "start": "2022-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "defense_geopolitics",
        "persona": "defense_aerospace",
        "persona_source": "theme",
        "hypothesis": "Defense/aerospace/cyber stocks benefit from sustained geopolitical tension",
        "start": "2022-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "biotech_innovation",
        "persona": "biotech_breakout",
        "persona_source": "theme",
        "hypothesis": "Diversified biotech basket with momentum filtering outperforms XBI",
        "start": "2022-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "china_tech_recovery",
        "persona": "china_tech_rebound",
        "persona_source": "theme",
        "hypothesis": "China tech ADRs recover from regulatory crackdown creating deep value opportunity",
        "start": "2022-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "small_cap_deep_value",
        "persona": "small_cap_value",
        "persona_source": "theme",
        "hypothesis": "Small cap deep value (oversold + volume) captures mean-reversion alpha",
        "start": "2022-01-01",
        "end": "2024-12-31",
    },
    # === Recession Strategies ===
    {
        "name": "recession_detector_adaptive",
        "persona": "recession_detector",
        "persona_source": "recession",
        "hypothesis": "Regime-switching strategy detects recession and shifts to defensive, preserving capital",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "treasury_safe_haven",
        "persona": "treasury_safe",
        "persona_source": "recession",
        "hypothesis": "Flight to quality (long-duration bonds + gold) outperforms during market stress",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "defensive_rotation_recession",
        "persona": "defensive_rotation",
        "persona_source": "recession",
        "hypothesis": "Rotating to staples/utilities/healthcare during recession signals beats holding SPY",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "gold_bug_hedge",
        "persona": "gold_bug",
        "persona_source": "recession",
        "hypothesis": "Gold and precious metals provide portfolio protection during recession/inflation",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    # === Unconventional Strategies ===
    {
        "name": "sell_in_may_seasonal",
        "persona": "sell_in_may",
        "persona_source": "unconventional",
        "hypothesis": "Sell in May: stocks Nov-Apr, bonds May-Oct captures seasonal alpha",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "turn_of_month_effect",
        "persona": "turn_of_month",
        "persona_source": "unconventional",
        "hypothesis": "Turn-of-month effect: last 3 + first 3 days capture cash flow driven returns",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "vix_buy_fear",
        "persona": "vix_mean_reversion",
        "persona_source": "unconventional",
        "hypothesis": "Buying stocks when VIX spikes (vol proxy > 30) captures mean-reversion premium",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "dogs_of_dow_contrarian",
        "persona": "dogs_of_dow",
        "persona_source": "unconventional",
        "hypothesis": "Dogs of Dow: worst-performing blue chips revert to mean, outperforming equally-weighted Dow",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "quality_factor_low_vol",
        "persona": "quality_factor",
        "persona_source": "unconventional",
        "hypothesis": "Quality factor (low vol + uptrend) generates stable returns with minimal drawdowns",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
    {
        "name": "tail_risk_crash_buying",
        "persona": "tail_risk_harvest",
        "persona_source": "unconventional",
        "hypothesis": "Buying quality stocks after >3% single-day drops captures overreaction mean-reversion",
        "start": "2021-01-01",
        "end": "2024-12-31",
    },
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
def run_hypothesis(hyp: Dict[str, Any], verbose: bool = True) -> Dict[str, Any]:
    """Run a single hypothesis test."""
    name = hyp["name"]
    persona_key = hyp["persona"]

    if verbose:
        print(f"\n{'=' * 60}")
        print(f"  Testing: {name}")
        print(f"  Hypothesis: {hyp['hypothesis']}")
        print(f"  Period: {hyp['start']} to {hyp['end']}")
        print(f"{'=' * 60}")

    source = hyp.get("persona_source", "builtin")
    if source == "famous":
        persona = get_famous_investor(persona_key)
    elif source == "theme":
        persona = get_theme_strategy(persona_key)
    elif source == "recession":
        persona = get_recession_strategy(persona_key)
    elif source == "unconventional":
        persona = get_unconventional_strategy(persona_key)
    else:
        persona = get_persona(persona_key)
    symbols = persona.config.universe

    bt = Backtester(
        strategy=persona,
        symbols=symbols,
        start=hyp["start"],
        end=hyp["end"],
        initial_cash=100_000,
        benchmark="SPY",
        rebalance_frequency=persona.config.rebalance_frequency,
    )

    try:
        results = bt.run()
        report = format_report(results, f"{persona.config.name}: {hyp['hypothesis'][:60]}")

        if verbose:
            print(report)

        # Determine if hypothesis is supported
        m = results["metrics"]
        verdict_lines = [f"# Hypothesis: {hyp['hypothesis']}", ""]
        verdict_lines.append(f"**Persona:** {persona.config.name}")
        verdict_lines.append(f"**Period:** {hyp['start']} to {hyp['end']}")
        verdict_lines.append(f"**Universe:** {', '.join(symbols)}")
        verdict_lines.append("")
        verdict_lines.append("## Results")
        verdict_lines.append(f"- Total Return: {m.get('total_return', 0):.2%}")
        verdict_lines.append(f"- CAGR: {m.get('cagr', 0):.2%}")
        verdict_lines.append(f"- Sharpe: {m.get('sharpe_ratio', 0):.2f}")
        verdict_lines.append(f"- Max Drawdown: {m.get('max_drawdown', 0):.2%}")
        verdict_lines.append(f"- Win Rate: {m.get('win_rate', 0):.2%}")

        if "benchmark_total_return" in m:
            verdict_lines.append(f"- Benchmark Return: {m.get('benchmark_total_return', 0):.2%}")
            verdict_lines.append(f"- Alpha: {m.get('alpha', 0):.2%}")
            verdict_lines.append(f"- Beta: {m.get('beta', 0):.2f}")

        # Verdict
        sharpe = m.get("sharpe_ratio", 0)
        alpha = m.get("alpha", 0)
        max_dd = m.get("max_drawdown", 0)

        if sharpe > 0.5 and alpha > 0:
            verdict = "SUPPORTED - Strategy shows positive alpha and decent risk-adjusted returns"
        elif sharpe > 0 and alpha > -0.05:
            verdict = "PARTIALLY SUPPORTED - Positive returns but limited alpha over benchmark"
        else:
            verdict = "NOT SUPPORTED - Strategy underperforms benchmark on risk-adjusted basis"

        verdict_lines.append(f"\n## Verdict\n**{verdict}**")
        verdict_lines.append(f"\n## Key Observations")

        if max_dd < -0.30:
            verdict_lines.append(f"- WARNING: Severe drawdown of {max_dd:.1%}")
        if m.get("win_rate", 0) > 0.55:
            verdict_lines.append(f"- Good win rate of {m.get('win_rate', 0):.1%}")

        num_trades = results.get("trade_metrics", {}).get("num_trades", 0)
        verdict_lines.append(f"- Total trades: {num_trades}")

        finding = "\n".join(verdict_lines)
        save_to_knowledge(name, finding, "hypothesis_results")
        save_result_json(name, {"metrics": m, "trade_metrics": results.get("trade_metrics", {})})

        # Save trade recommendations (winning/losing)
        try:
            save_strategy_recommendation(
                name, results,
                persona_config={
                    "rebalance_frequency": persona.config.rebalance_frequency,
                    "risk_tolerance": persona.config.risk_tolerance,
                }
            )
        except Exception:
            pass

        return {
            "name": name,
            "status": "success",
            "verdict": verdict,
            "metrics": m,
            "report": report,
            "final_positions": results.get("final_positions", {}),
        }

    except Exception as e:
        error_msg = f"# FAILED: {name}\n\nError: {e}\n\n```\n{traceback.format_exc()}\n```"
        save_to_knowledge(name, error_msg, "failures")

        if verbose:
            print(f"  ERROR: {e}")

        return {
            "name": name,
            "status": "error",
            "error": str(e),
        }


def run_all(
    start: str = "2021-01-01",
    end: str = "2024-12-31",
    personas_filter: Optional[List[str]] = None,
    verbose: bool = True,
) -> List[Dict[str, Any]]:
    """Run all hypothesis tests and generate summary."""
    hypotheses = [dict(h) for h in HYPOTHESES]

    if personas_filter:
        hypotheses = [h for h in hypotheses if h["persona"] in personas_filter]

    # Override dates if specified
    for h in hypotheses:
        h["start"] = start
        h["end"] = end

    all_results = []
    for hyp in hypotheses:
        result = run_hypothesis(hyp, verbose=verbose)
        all_results.append(result)

    # Generate summary
    summary_lines = ["# Hypothesis Testing Summary", ""]
    summary_lines.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    summary_lines.append(f"**Period:** {start} to {end}")
    summary_lines.append(f"**Hypotheses tested:** {len(all_results)}")
    summary_lines.append("")
    summary_lines.append("| Persona | Total Return | Sharpe | Max DD | Alpha | Verdict |")
    summary_lines.append("|---------|-------------|--------|--------|-------|---------|")

    for r in all_results:
        if r["status"] == "success":
            m = r["metrics"]
            alpha = m.get('alpha')
            alpha_str = f"{alpha:.1%}" if isinstance(alpha, (int, float)) else "N/A"
            summary_lines.append(
                f"| {r['name']} | {m.get('total_return', 0):.1%} | "
                f"{m.get('sharpe_ratio', 0):.2f} | {m.get('max_drawdown', 0):.1%} | "
                f"{alpha_str} | {r['verdict'][:30]}... |"
            )
        else:
            summary_lines.append(f"| {r['name']} | ERROR | - | - | - | {r['error'][:30]} |")

    summary = "\n".join(summary_lines)
    save_to_knowledge("summary", summary, "hypothesis_results")

    if verbose:
        print(f"\n\n{'=' * 60}")
        print(summary)

    return all_results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Run trading hypothesis backtests")
    parser.add_argument("--persona", "-p", help="Run only this persona")
    parser.add_argument("--start", "-s", default="2021-01-01", help="Start date")
    parser.add_argument("--end", "-e", default="2024-12-31", help="End date")
    parser.add_argument("--quiet", "-q", action="store_true", help="Less output")
    parser.add_argument("--list", "-l", action="store_true", help="List personas")
    args = parser.parse_args()

    if args.list:
        print("  Builtin Personas:")
        for p in list_personas():
            print(f"    {p['key']:20s} | {p['name']:25s} | {p['description']}")
        print("\n  Famous Investors:")
        for p in list_famous_investors():
            print(f"    {p['key']:20s} | {p['name']:25s} | {p['description']}")
        print("\n  Theme Strategies:")
        for p in list_theme_strategies():
            print(f"    {p['key']:20s} | {p['name']:25s} | {p['description']}")
        print("\n  Recession Strategies:")
        for key, strat in RECESSION_STRATEGIES.items():
            print(f"    {key:20s} | {strat.config.name:25s} | {strat.config.description}")
        return

    filter_list = [args.persona] if args.persona else None
    results = run_all(
        start=args.start,
        end=args.end,
        personas_filter=filter_list,
        verbose=not args.quiet,
    )

    successes = sum(1 for r in results if r["status"] == "success")
    failures = sum(1 for r in results if r["status"] == "error")
    print(f"\nDone: {successes} succeeded, {failures} failed")


if __name__ == "__main__":
    main()

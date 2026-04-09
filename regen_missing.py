"""Regenerate missing strategy files one at a time, commit+push after each.

Usage: python3 regen_missing.py
"""
import json, os, re, subprocess, sys, time
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from backtester import Backtester
from trade_recommender import save_strategy_recommendation

# Import ALL strategy modules
from personas import get_persona, ALL_PERSONAS
from famous_investors import get_famous_investor, FAMOUS_INVESTORS
from theme_strategies import get_theme_strategy, THEME_STRATEGIES
from recession_strategies import get_recession_strategy, RECESSION_STRATEGIES
from unconventional_strategies import get_unconventional_strategy, UNCONVENTIONAL_STRATEGIES
from research_strategies import get_research_strategy, RESEARCH_STRATEGIES
from math_strategies import get_math_strategy, MATH_STRATEGIES
from political_strategies import get_political_strategy, POLITICAL_STRATEGIES
from hedge_fund_strategies import get_hedge_fund_strategy, HEDGE_FUND_STRATEGIES
from news_event_strategies import get_news_event_strategy, NEWS_EVENT_STRATEGIES
from portfolio_strategies import get_portfolio_strategy, PORTFOLIO_STRATEGIES
from crisis_commodity_strategies import get_crisis_commodity_strategy, CRISIS_COMMODITY_STRATEGIES
from williams_seasonal_strategies import get_williams_seasonal_strategy, WILLIAMS_SEASONAL_STRATEGIES

ALL = []
for k in ALL_PERSONAS: ALL.append((k, get_persona, "generic"))
for k in FAMOUS_INVESTORS: ALL.append((k, get_famous_investor, "famous"))
for k in THEME_STRATEGIES: ALL.append((k, get_theme_strategy, "theme"))
for k in RECESSION_STRATEGIES: ALL.append((k, get_recession_strategy, "recession"))
for k in UNCONVENTIONAL_STRATEGIES: ALL.append((k, get_unconventional_strategy, "unconventional"))
for k in RESEARCH_STRATEGIES: ALL.append((k, get_research_strategy, "research"))
for k in MATH_STRATEGIES: ALL.append((k, get_math_strategy, "math"))
for k in POLITICAL_STRATEGIES: ALL.append((k, get_political_strategy, "political"))
for k in HEDGE_FUND_STRATEGIES: ALL.append((k, get_hedge_fund_strategy, "hedge_fund"))
for k in NEWS_EVENT_STRATEGIES: ALL.append((k, get_news_event_strategy, "news_event"))
for k in PORTFOLIO_STRATEGIES: ALL.append((k, get_portfolio_strategy, "portfolio"))
for k in CRISIS_COMMODITY_STRATEGIES: ALL.append((k, get_crisis_commodity_strategy, "crisis"))
for k in WILLIAMS_SEASONAL_STRATEGIES: ALL.append((k, get_williams_seasonal_strategy, "williams_seasonal"))

# Find what's missing
results_dir = Path("results")
results_dir.mkdir(exist_ok=True)
DATE_FULL = re.compile(r"_\d{8}_\d{6}$")
DATE_SUFFIX = re.compile(r"_\d{4}(-\d{2}(-\d{2})?)?$")
existing = set()
for f in results_dir.glob("*.json"):
    base = DATE_FULL.sub("", f.stem)
    base = DATE_SUFFIX.sub("", base)
    existing.add(base)

missing = [(k, g, s) for k, g, s in ALL if k not in existing]
print(f"Total: {len(ALL)} strategies, {len(existing)} have results, {len(missing)} to backtest")

for i, (key, getter, source) in enumerate(missing):
    print(f"\n[{i+1}/{len(missing)}] Backtesting {key}...", flush=True)
    try:
        persona = getter(key)
        bt = Backtester(
            strategy=persona,
            symbols=persona.config.universe,
            start="2022-01-01",
            end="2024-12-31",
            initial_cash=100_000,
            benchmark="SPY",
            rebalance_frequency=persona.config.rebalance_frequency,
        )
        results = bt.run()
        m = results["metrics"]

        # Save result JSON
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        result_data = {
            "metrics": m,
            "trade_metrics": results.get("trade_metrics", {}),
            "final_positions": results.get("final_positions", {}),
            "source": source,
            "description": persona.config.description,
        }
        result_path = results_dir / f"{key}_{ts}.json"
        result_path.write_text(json.dumps(result_data, indent=2, default=str))

        # Save strategy recommendation
        save_strategy_recommendation(
            key, results,
            description=persona.config.description,
            hypothesis=f"{persona.config.name} strategy backtested 3Y (2022-2024)",
        )

        ret = m.get("total_return", 0)
        sharpe = m.get("sharpe_ratio", 0)
        dd = m.get("max_drawdown", 0)
        tag = "WIN" if ret > 0 and sharpe > 0 else "LOSE"
        print(f"  [{tag}] {key:35s} Ret={ret:>7.1%} Sharpe={sharpe:.2f} DD={dd:.1%}", flush=True)

        # Git add + commit + push
        subprocess.run(["git", "add", "results/", "strategy/winning/", "strategy/losing/"], cwd=str(Path(__file__).parent))
        subprocess.run(
            ["git", "commit", "-m", f"Add {key} strategy ({tag}): {ret:.1%} ret, {sharpe:.2f} sharpe\n\nCo-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"],
            cwd=str(Path(__file__).parent),
        )
        subprocess.run(["git", "push"], cwd=str(Path(__file__).parent))
        print(f"  Committed and pushed {key}", flush=True)

    except Exception as e:
        print(f"  [ERR] {key}: {str(e)[:80]}", flush=True)

print(f"\nDone! Check strategy/winning/ and strategy/losing/")

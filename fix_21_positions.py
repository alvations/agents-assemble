"""Fix all 21 strategies with empty position_recommendations.

Runs a 3Y backtest (2023-2025) for each, then saves recommendation files
with REAL final_positions.
"""

import sys
import os
import json
import glob
import traceback
from datetime import datetime
from pathlib import Path

# Ensure we can import from the project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from personas import ALL_PERSONAS
from famous_investors import FAMOUS_INVESTORS
from theme_strategies import THEME_STRATEGIES
from portfolio_strategies import PORTFOLIO_STRATEGIES
from unconventional_strategies import UNCONVENTIONAL_STRATEGIES
from research_strategies import RESEARCH_STRATEGIES
from math_strategies import MATH_STRATEGIES
from hedge_fund_strategies import HEDGE_FUND_STRATEGIES
from williams_seasonal_strategies import WILLIAMS_SEASONAL_STRATEGIES
from backtester import Backtester
from trade_recommender import save_strategy_recommendation


# Map each broken strategy to its registry
STRATEGY_REGISTRY = {
    'covered_call_income': PORTFOLIO_STRATEGIES,
    'cross_asset_carry': RESEARCH_STRATEGIES,
    'ensemble': ALL_PERSONAS,
    'fixed_income': ALL_PERSONAS,
    'howard_marks': FAMOUS_INVESTORS,
    'insider_buying_acceleration': UNCONVENTIONAL_STRATEGIES,
    'insider_buying_real': UNCONVENTIONAL_STRATEGIES,
    'low_vol_quality': RESEARCH_STRATEGIES,
    'managed_futures_proxy': HEDGE_FUND_STRATEGIES,
    'quant': ALL_PERSONAS,
    'all_weather_modern': PORTFOLIO_STRATEGIES,
    'benjamin_graham': FAMOUS_INVESTORS,
    'dollar_cycle_rotation': UNCONVENTIONAL_STRATEGIES,
    'dual_momentum_global': PORTFOLIO_STRATEGIES,
    'infrastructure_reshoring': THEME_STRATEGIES,
    'leveraged_trend_tactical': UNCONVENTIONAL_STRATEGIES,
    'multi_factor_combined': RESEARCH_STRATEGIES,
    'preferred_equity_income': PORTFOLIO_STRATEGIES,
    'prince_alwaleed': FAMOUS_INVESTORS,
    'tax_harvest_rotation': PORTFOLIO_STRATEGIES,
    'vix_fear_buy': WILLIAMS_SEASONAL_STRATEGIES,
}


def run_backtest_and_save(name, registry):
    """Run 3Y backtest and save recommendation for a single strategy."""
    print(f"\n{'='*60}")
    print(f"  Processing: {name}")
    print(f"{'='*60}")

    # Instantiate
    persona_cls = registry[name]
    persona = persona_cls()
    universe = persona.config.universe
    rebal = persona.config.rebalance_frequency
    desc = persona.config.description

    print(f"  Universe: {len(universe)} symbols")
    print(f"  Rebalance: {rebal}")

    # Run backtest
    bt = Backtester(
        strategy=persona,
        symbols=universe,
        start='2023-01-01',
        end='2025-12-31',
        initial_cash=100_000,
        benchmark='SPY',
        rebalance_frequency=rebal,
    )
    result = bt.run()

    final_pos = result.get('final_positions', {})
    metrics = result.get('metrics', {})
    total_ret = metrics.get('total_return', 0)
    sharpe = metrics.get('sharpe_ratio', 0)

    print(f"  Result: {len(final_pos)} positions, "
          f"ret={total_ret:.2%}, sharpe={sharpe:.2f}")

    if not final_pos:
        print(f"  WARNING: No final_positions even after backtest!")

    # Save recommendation
    md_path = save_strategy_recommendation(
        name=name,
        results=result,
        persona_config={
            'rebalance_frequency': rebal,
        },
        description=desc,
    )
    print(f"  Saved: {md_path}")

    # Verify the new files have positions
    json_path = str(md_path).replace('.md', '.json')
    with open(json_path) as f:
        data = json.load(f)
    n_recs = len(data.get('position_recommendations', []))
    print(f"  Verification: {n_recs} position_recommendations in JSON")

    # Check MD has position table
    md_text = Path(md_path).read_text()
    has_table = '| Symbol | Action |' in md_text
    print(f"  MD has position table: {has_table}")

    return {
        'name': name,
        'n_positions': len(final_pos),
        'n_recommendations': n_recs,
        'total_return': total_ret,
        'sharpe': sharpe,
        'md_path': str(md_path),
        'has_table': has_table,
    }


def main():
    results = []
    failures = []

    for name, registry in STRATEGY_REGISTRY.items():
        try:
            info = run_backtest_and_save(name, registry)
            results.append(info)
        except Exception as e:
            print(f"\n  FAILED: {name}: {e}")
            traceback.print_exc()
            failures.append({'name': name, 'error': str(e)})

    # Summary
    print(f"\n\n{'='*60}")
    print(f"  SUMMARY")
    print(f"{'='*60}")
    print(f"  Successful: {len(results)}/{len(STRATEGY_REGISTRY)}")
    print(f"  Failed: {len(failures)}")

    for r in results:
        status = 'OK' if r['has_table'] and r['n_recommendations'] > 0 else 'EMPTY!'
        print(f"  [{status}] {r['name']}: {r['n_recommendations']} positions, "
              f"ret={r['total_return']:.2%}, sharpe={r['sharpe']:.2f}")

    if failures:
        print(f"\n  FAILURES:")
        for f in failures:
            print(f"    {f['name']}: {f['error']}")

    # Final verification across all 21
    print(f"\n\n{'='*60}")
    print(f"  FINAL VERIFICATION")
    print(f"{'='*60}")
    all_names = list(STRATEGY_REGISTRY.keys())
    for name in all_names:
        files = sorted(
            glob.glob(f'strategy/winning/{name}_*.json') +
            glob.glob(f'strategy/losing/{name}_*.json')
        )
        if files:
            latest = files[-1]
            with open(latest) as fh:
                data = json.load(fh)
            recs = data.get('position_recommendations', [])
            print(f"  {name}: {len(recs)} positions (latest: {os.path.basename(latest)})")
        else:
            print(f"  {name}: NO FILES FOUND!")


if __name__ == '__main__':
    main()

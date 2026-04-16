#!/usr/bin/env python3
"""Backtest 10 new boring-but-proven strategies on all 28 rolling windows."""
import sys, json, os, traceback
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backtester import Backtester

STRATEGIES = [
    # Unconventional (4)
    'waste_monopoly_compounder', 'death_care_demographics',
    'pawn_counter_cyclical', 'long_term_loser_rebound',
    # Portfolio (3)
    'self_storage_reit', 'closed_end_fund_discount', 'canadian_aristocrat_income',
    # Research (3)
    'buyback_yield_systematic', 'gross_profitability_value', 'accruals_quality',
]

WINDOWS = {
    '1Y_2015': ('2015-01-01','2015-12-31'), '1Y_2016': ('2016-01-01','2016-12-31'),
    '1Y_2017': ('2017-01-01','2017-12-31'), '1Y_2018': ('2018-01-01','2018-12-31'),
    '1Y_2019': ('2019-01-01','2019-12-31'), '1Y_2020': ('2020-01-01','2020-12-31'),
    '1Y_2021': ('2021-01-01','2021-12-31'), '1Y_2022': ('2022-01-01','2022-12-31'),
    '1Y_2023': ('2023-01-01','2023-12-31'), '1Y_2024': ('2024-01-01','2024-12-31'),
    '1Y_2025': ('2025-01-01','2025-12-31'),
    '3Y_2015_2017': ('2015-01-01','2017-12-31'), '3Y_2016_2018': ('2016-01-01','2018-12-31'),
    '3Y_2017_2019': ('2017-01-01','2019-12-31'), '3Y_2018_2020': ('2018-01-01','2020-12-31'),
    '3Y_2019_2021': ('2019-01-01','2021-12-31'), '3Y_2020_2022': ('2020-01-01','2022-12-31'),
    '3Y_2021_2023': ('2021-01-01','2023-12-31'), '3Y_2022_2024': ('2022-01-01','2024-12-31'),
    '3Y_2023_2025': ('2023-01-01','2025-12-31'),
    '5Y_2015_2019': ('2015-01-01','2019-12-31'), '5Y_2016_2020': ('2016-01-01','2020-12-31'),
    '5Y_2017_2021': ('2017-01-01','2021-12-31'), '5Y_2018_2022': ('2018-01-01','2022-12-31'),
    '5Y_2019_2023': ('2019-01-01','2023-12-31'), '5Y_2020_2024': ('2020-01-01','2024-12-31'),
    '5Y_2021_2025': ('2021-01-01','2025-12-31'),
    '10Y_2015_2024': ('2015-01-01','2024-12-31'),
}

LB_WINDOWS = ['1Y_2022','1Y_2023','1Y_2024','1Y_2025','3Y_2022_2024','3Y_2023_2025']

def get_strategy_class(name):
    """Find and return strategy class by name."""
    modules = [
        ('unconventional_strategies', 'UNCONVENTIONAL_STRATEGIES'),
        ('portfolio_strategies', 'PORTFOLIO_STRATEGIES'),
        ('research_strategies', 'RESEARCH_STRATEGIES'),
    ]
    for mod_name, dict_name in modules:
        try:
            mod = __import__(mod_name)
            registry = getattr(mod, dict_name, {})
            if name in registry:
                return registry[name]
        except Exception:
            continue
    return None

def main():
    # Load existing MW data
    mw_files = sorted([f for f in os.listdir('results') if f.startswith('_multi_window_full_')])
    mw_path = f'results/{mw_files[-1]}' if mw_files else None
    mw_data = {}
    if mw_path:
        with open(mw_path) as f:
            mw_data = json.load(f)

    total = len(STRATEGIES)
    for idx, name in enumerate(STRATEGIES, 1):
        print(f'\n[{idx}/{total}] Backtesting {name}...', flush=True)
        cls = get_strategy_class(name)
        if cls is None:
            print(f'  SKIP — class not found')
            continue

        try:
            persona = cls()
        except Exception as e:
            print(f'  SKIP — instantiation failed: {e}')
            continue

        symbols = persona.config.universe if hasattr(persona, 'config') else persona.universe
        rebal = persona.config.rebalance_frequency if hasattr(persona, 'config') else 'monthly'

        window_results = {}
        for wname, (start, end) in WINDOWS.items():
            try:
                bt = Backtester(
                    strategy=persona, symbols=symbols,
                    start=start, end=end,
                    initial_cash=100_000, benchmark='SPY',
                    rebalance_frequency=rebal,
                )
                result = bt.run()
                m = result.get('metrics', {})
                sh = m.get('sharpe_ratio', 0)
                if sh != sh:  # NaN check
                    sh = 0
                window_results[wname] = {
                    'ret': round(m.get('total_return', 0), 4),
                    'sh': round(sh, 2),
                    'dd': round(m.get('max_drawdown', 0), 4),
                }
                print(f'    {wname:20s} ret={window_results[wname]["ret"]:>7.1%} sh={sh:>5.2f}', flush=True)
            except Exception as e:
                window_results[wname] = {'ret': 0, 'sh': 0, 'dd': 0}
                print(f'    {wname:20s} ERROR: {str(e)[:60]}', flush=True)

        # Compute composites
        all_sh = [w['sh'] for w in window_results.values()]
        all_ret = [w['ret'] for w in window_results.values()]
        all_dd = [abs(w['dd']) for w in window_results.values()]

        consistency = sum(1 for s in all_sh if s > 0) / len(all_sh) if all_sh else 0
        avg_ret = sum(all_ret) / len(all_ret) if all_ret else 0
        avg_dd = sum(all_dd) / len(all_dd) if all_dd else 0
        hodl_composite = round(avg_ret * consistency * (1 - avg_dd), 4)

        # LB composite (6 windows)
        lb_sh = [window_results[w]['sh'] for w in LB_WINDOWS if w in window_results]
        lb_ret = [window_results[w]['ret'] for w in LB_WINDOWS if w in window_results]
        lb_dd = [abs(window_results[w]['dd']) for w in LB_WINDOWS if w in window_results]
        lb_con = sum(1 for s in lb_sh if s > 0) / len(lb_sh) if lb_sh else 0
        lb_avg_ret = sum(lb_ret) / len(lb_ret) if lb_ret else 0
        lb_avg_dd = sum(lb_dd) / len(lb_dd) if lb_dd else 0
        lb_composite = round(lb_avg_ret * lb_con * (1 - lb_avg_dd), 4)

        # Determine source category
        src_map = {
            'waste_monopoly_compounder': 'unconventional',
            'death_care_demographics': 'unconventional',
            'pawn_counter_cyclical': 'unconventional',
            'long_term_loser_rebound': 'unconventional',
            'self_storage_reit': 'portfolio',
            'closed_end_fund_discount': 'portfolio',
            'canadian_aristocrat_income': 'portfolio',
            'buyback_yield_systematic': 'research',
            'gross_profitability_value': 'research',
            'accruals_quality': 'research',
        }

        best_3y = window_results.get('3Y_2023_2025', window_results.get('3Y_2022_2024', {}))
        is_winning = best_3y.get('sh', 0) > 0

        mw_data[name] = {
            'src': src_map.get(name, 'boring10'),
            'desc': persona.config.description,
            'w': window_results,
            'consistency': round(consistency, 2),
            'composite': lb_composite,
            'hodl_composite': hodl_composite,
        }

        verdict = 'W' if is_winning else 'L'
        print(f'  {verdict} {name:40s} LB={lb_composite:.2f} HODL={hodl_composite:.4f} con={consistency:.0%}', flush=True)

        # Save individual result
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        ind_result = {
            'metrics': {
                'total_return': best_3y.get('ret', 0),
                'sharpe_ratio': best_3y.get('sh', 0),
                'max_drawdown': best_3y.get('dd', 0),
            },
            'final_positions': {},
            'rolling_windows': window_results,
            'source': 'boring10_backtest',
        }
        with open(f'results/{name}_{ts}.json', 'w') as f:
            json.dump(ind_result, f, indent=2, default=str)

    # Save updated MW
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    mw_out = f'results/_multi_window_full_{ts}.json'
    with open(mw_out, 'w') as f:
        json.dump(mw_data, f, indent=2, default=str)
    print(f'\nDONE: {total}/{total}, total MW: {len(mw_data)}')
    print(f'Saved: {mw_out}')

if __name__ == '__main__':
    main()

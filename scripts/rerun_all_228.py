#!/usr/bin/env python3
"""Rerun ALL 228 strategies on all 28 rolling windows with dividend-adjusted prices."""
import sys, json, os, traceback
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from bespoke import Backtester
except ImportError:
    from backtester import Backtester

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

def get_all_strategies():
    """Load ALL strategies from ALL registries."""
    modules = [
        ('personas', 'ALL_PERSONAS'),
        ('famous_investors', 'FAMOUS_INVESTORS'),
        ('theme_strategies', 'THEME_STRATEGIES'),
        ('portfolio_strategies', 'PORTFOLIO_STRATEGIES'),
        ('recession_strategies', 'RECESSION_STRATEGIES'),
        ('unconventional_strategies', 'UNCONVENTIONAL_STRATEGIES'),
        ('research_strategies', 'RESEARCH_STRATEGIES'),
        ('math_strategies', 'MATH_STRATEGIES'),
        ('hedge_fund_strategies', 'HEDGE_FUND_STRATEGIES'),
        ('crisis_commodity_strategies', 'CRISIS_COMMODITY_STRATEGIES'),
        ('williams_seasonal_strategies', 'WILLIAMS_SEASONAL_STRATEGIES'),
        ('news_event_strategies', 'NEWS_EVENT_STRATEGIES'),
        ('political_strategies', 'POLITICAL_STRATEGIES'),
        ('strategy_orchestrator', 'ORCHESTRATOR_STRATEGIES'),
    ]
    all_strats = {}
    for mod_name, dict_name in modules:
        try:
            mod = __import__(mod_name)
            registry = getattr(mod, dict_name, {})
            for key, cls in registry.items():
                src = mod_name.replace('_strategies', '').replace('_investors', '')
                all_strats[key] = (cls, src)
        except Exception as e:
            print(f'  WARN: could not load {mod_name}.{dict_name}: {e}')
    return all_strats

def main():
    all_strats = get_all_strategies()
    total = len(all_strats)
    print(f'Found {total} strategies across all registries')
    
    # Load existing MW to preserve desc fields
    import glob
    mw_files = sorted(glob.glob('results/_multi_window_full_*.json'))
    old_mw = {}
    if mw_files:
        with open(mw_files[-1]) as f:
            old_mw = json.load(f)

    mw_data = {}
    for idx, (name, (cls, src)) in enumerate(sorted(all_strats.items()), 1):
        print(f'\n[{idx}/{total}] {name} ({src})...', flush=True)
        try:
            persona = cls()
        except Exception as e:
            print(f'  SKIP — init failed: {e}')
            continue

        symbols = persona.config.universe if hasattr(persona, 'config') else getattr(persona, 'universe', [])
        rebal = persona.config.rebalance_frequency if hasattr(persona, 'config') else 'monthly'
        if not symbols:
            print(f'  SKIP — no universe')
            continue

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
                if sh != sh: sh = 0  # NaN
                ret = m.get('total_return', 0)
                if ret != ret: ret = 0
                dd = m.get('max_drawdown', 0)
                if dd != dd: dd = 0
                window_results[wname] = {
                    'ret': round(ret, 4),
                    'sh': round(sh, 2),
                    'dd': round(dd, 4),
                }
            except Exception:
                window_results[wname] = {'ret': 0, 'sh': 0, 'dd': 0}

        # Composites
        all_sh = [w['sh'] for w in window_results.values()]
        all_ret = [w['ret'] for w in window_results.values()]
        all_dd = [abs(w['dd']) for w in window_results.values()]
        
        consistency = sum(1 for s in all_sh if s > 0) / len(all_sh) if all_sh else 0
        avg_ret = sum(all_ret) / len(all_ret) if all_ret else 0
        avg_dd = sum(all_dd) / len(all_dd) if all_dd else 0
        hodl_composite = round(avg_ret * consistency * (1 - avg_dd), 4)

        lb_sh = [window_results[w]['sh'] for w in LB_WINDOWS if w in window_results]
        lb_ret = [window_results[w]['ret'] for w in LB_WINDOWS if w in window_results]
        lb_dd = [abs(window_results[w]['dd']) for w in LB_WINDOWS if w in window_results]
        lb_con = sum(1 for s in lb_sh if s > 0) / len(lb_sh) if lb_sh else 0
        lb_avg_ret = sum(lb_ret) / len(lb_ret) if lb_ret else 0
        lb_avg_dd = sum(lb_dd) / len(lb_dd) if lb_dd else 0
        lb_composite = round(lb_avg_ret * lb_con * (1 - lb_avg_dd), 4)

        mw_data[name] = {
            'src': src.replace('personas', 'generic').replace('famous', 'famous'),
            'desc': old_mw.get(name, {}).get('desc', ''),
            'w': window_results,
            'consistency': round(consistency, 2),
            'composite': lb_composite,
            'hodl_composite': hodl_composite,
        }

        verdict = 'W' if hodl_composite > 0 and consistency > 0.5 else 'L'
        print(f'  {verdict} LB={lb_composite:.3f} HODL={hodl_composite:.4f} con={consistency:.0%}', flush=True)

        # Save individual result JSON
        best_3y = window_results.get('3Y_2023_2025', window_results.get('3Y_2022_2024', {}))
        ind_ts = datetime.now().strftime('%Y%m%d_%H%M%S')
        ind_result = {
            'metrics': {
                'total_return': best_3y.get('ret', 0),
                'sharpe_ratio': best_3y.get('sh', 0),
                'max_drawdown': best_3y.get('dd', 0),
            },
            'final_positions': {},
            'rolling_windows': window_results,
            'source': src,
            'description': old_mw.get(name, {}).get('desc', ''),
            'backtest_date': ind_ts,
            'dividend_adjusted': True,
        }
        with open(f'results/{name}_{ind_ts}.json', 'w') as f:
            json.dump(ind_result, f, indent=2, default=str)

    # Save MW
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    out = f'results/_multi_window_full_{ts}.json'
    with open(out, 'w') as f:
        json.dump(mw_data, f, indent=2, default=str)
    print(f'\nDONE: {len(mw_data)}/{total} strategies')
    print(f'Saved: {out}')

if __name__ == '__main__':
    main()

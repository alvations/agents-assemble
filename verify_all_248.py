#!/usr/bin/env python3
"""Verify ALL 248 strategies: fresh 3Y backtest vs stored MW data."""
import sys, json, glob, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backtester import Backtester

def get_all_strategies():
    modules = [
        ('personas', 'ALL_PERSONAS'), ('famous_investors', 'FAMOUS_INVESTORS'),
        ('theme_strategies', 'THEME_STRATEGIES'), ('portfolio_strategies', 'PORTFOLIO_STRATEGIES'),
        ('recession_strategies', 'RECESSION_STRATEGIES'), ('unconventional_strategies', 'UNCONVENTIONAL_STRATEGIES'),
        ('research_strategies', 'RESEARCH_STRATEGIES'), ('math_strategies', 'MATH_STRATEGIES'),
        ('hedge_fund_strategies', 'HEDGE_FUND_STRATEGIES'), ('crisis_commodity_strategies', 'CRISIS_COMMODITY_STRATEGIES'),
        ('williams_seasonal_strategies', 'WILLIAMS_SEASONAL_STRATEGIES'),
        ('news_event_strategies', 'NEWS_EVENT_STRATEGIES'), ('political_strategies', 'POLITICAL_STRATEGIES'),
        ('strategy_orchestrator', 'ORCHESTRATOR_STRATEGIES'),
    ]
    all_strats = {}
    for mod_name, dict_name in modules:
        try:
            mod = __import__(mod_name)
            registry = getattr(mod, dict_name, {})
            for key, cls in registry.items():
                all_strats[key] = cls
        except Exception as e:
            print(f"WARN: {mod_name}: {e}")
    return all_strats

def main():
    mw_files = sorted(glob.glob('results/_multi_window_full_*.json'))
    with open(mw_files[-1]) as f:
        mw = json.load(f)
    
    all_strats = get_all_strategies()
    print(f"MW: {len(mw)} strategies, Registries: {len(all_strats)} strategies")
    
    # Check MW strategies that aren't in registries
    missing_code = [n for n in mw if n not in all_strats]
    if missing_code:
        print(f"\nIn MW but NOT in code registries: {missing_code}")
    
    # Check registry strategies not in MW
    missing_mw = [n for n in all_strats if n not in mw]
    if missing_mw:
        print(f"\nIn code but NOT in MW: {missing_mw}")
    
    ok = 0
    diff = 0
    errors = 0
    no_positions = 0
    total = len(mw)
    
    print(f"\nVerifying {total} strategies (fresh 3Y backtest each)...\n")
    
    for idx, name in enumerate(sorted(mw.keys()), 1):
        mw_ret = mw[name].get('w', {}).get('3Y_2023_2025', {}).get('ret', 0)
        
        if name not in all_strats:
            print(f"[{idx}/{total}] SKIP {name} — not in registries")
            errors += 1
            continue
        
        try:
            persona = all_strats[name]()
            symbols = persona.config.universe if hasattr(persona, 'config') else persona.universe
            rebal = persona.config.rebalance_frequency if hasattr(persona, 'config') else 'monthly'
            
            bt = Backtester(
                strategy=persona, symbols=symbols,
                start='2023-01-01', end='2025-12-31',
                initial_cash=100_000, benchmark='SPY',
                rebalance_frequency=rebal,
            )
            result = bt.run()
            fresh_ret = result['metrics']['total_return']
            fresh_pos = len(result.get('final_positions', {}))
            
            delta = abs(fresh_ret - mw_ret)
            match = delta < 0.05
            
            if not match:
                print(f"[{idx}/{total}] DIFF {name}: MW={mw_ret:.1%} fresh={fresh_ret:.1%} delta={delta:.1%} pos={fresh_pos}")
                diff += 1
            else:
                ok += 1
            
            if fresh_pos == 0:
                print(f"[{idx}/{total}] NO_POS {name}: backtest returned 0 positions")
                no_positions += 1
                
        except Exception as e:
            print(f"[{idx}/{total}] ERROR {name}: {e}")
            errors += 1
    
    print(f"\n{'='*60}")
    print(f"RESULTS: {ok} OK, {diff} DIFF, {errors} ERROR, {no_positions} NO_POS")
    print(f"Total: {total}")
    print(f"Pass rate: {ok}/{total} ({ok/total*100:.1f}%)")
    if diff > 0:
        print(f"\nDIFF strategies need investigation — MW data doesn't match fresh backtest")

if __name__ == '__main__':
    main()

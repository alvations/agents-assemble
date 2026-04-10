#!/bin/bash
# Post-evolution validation: run after self_evolve.py completes
# Ensures changes don't break existing functionality

set -e
cd "$(dirname "$0")"

echo "=== Post-Evolution Validation ==="
echo ""

# 1. Syntax check ALL Python files
echo "[1/6] Syntax check..."
FAIL=0
for f in backtester.py data_fetcher.py app.py trade_recommender.py stock_picker.py strategy_orchestrator.py; do
    if ! python3 -c "import ast; ast.parse(open('$f').read())" 2>/dev/null; then
        echo "  FAIL: $f"
        FAIL=1
    fi
done
for f in personas.py famous_investors.py theme_strategies.py unconventional_strategies.py portfolio_strategies.py recession_strategies.py research_strategies.py math_strategies.py political_strategies.py hedge_fund_strategies.py news_event_strategies.py crisis_commodity_strategies.py williams_seasonal_strategies.py; do
    if ! python3 -c "import ast; ast.parse(open('$f').read())" 2>/dev/null; then
        echo "  FAIL: $f"
        FAIL=1
    fi
done
[ $FAIL -eq 0 ] && echo "  ALL PASS" || exit 1

# 2. Import check — can all modules load?
echo "[2/6] Import check..."
python3 -c "
import sys; sys.path.insert(0, '.')
modules = ['backtester', 'data_fetcher', 'trade_recommender', 'stock_picker', 'strategy_orchestrator',
           'personas', 'famous_investors', 'theme_strategies', 'unconventional_strategies',
           'portfolio_strategies', 'recession_strategies', 'research_strategies', 'math_strategies',
           'political_strategies', 'hedge_fund_strategies', 'news_event_strategies',
           'crisis_commodity_strategies', 'williams_seasonal_strategies']
for m in modules:
    try:
        __import__(m)
    except Exception as e:
        print(f'  FAIL: {m}: {e}')
        exit(1)
print('  ALL PASS')
"

# 3. Strategy count — should be >= 187
echo "[3/6] Strategy count check..."
python3 -c "
import sys; sys.path.insert(0, '.')
t = 0
for m, n in [('theme_strategies','THEME_STRATEGIES'),('unconventional_strategies','UNCONVENTIONAL_STRATEGIES'),('portfolio_strategies','PORTFOLIO_STRATEGIES'),('crisis_commodity_strategies','CRISIS_COMMODITY_STRATEGIES'),('hedge_fund_strategies','HEDGE_FUND_STRATEGIES'),('news_event_strategies','NEWS_EVENT_STRATEGIES'),('recession_strategies','RECESSION_STRATEGIES'),('math_strategies','MATH_STRATEGIES'),('political_strategies','POLITICAL_STRATEGIES'),('williams_seasonal_strategies','WILLIAMS_SEASONAL_STRATEGIES'),('personas','ALL_PERSONAS'),('famous_investors','FAMOUS_INVESTORS'),('strategy_orchestrator','ORCHESTRATOR_STRATEGIES')]:
    try:
        mod = __import__(m); d = getattr(mod, n); t += len(d)
    except: pass
if t < 187:
    print(f'  FAIL: only {t} strategies (expected >= 187)')
    exit(1)
print(f'  PASS: {t} strategies')
"

# 4. Quick backtest — can the backtester still run?
echo "[4/6] Quick backtest..."
python3 -c "
import sys; sys.path.insert(0, '.')
from backtester import Backtester
from personas import get_persona
p = get_persona('momentum')
bt = Backtester(strategy=p, symbols=['AAPL','MSFT'], start='2024-06-01', end='2024-12-31', initial_cash=100000, benchmark='SPY', rebalance_frequency='weekly')
r = bt.run()
m = r['metrics']
if 'total_return' not in m or 'sharpe_ratio' not in m:
    print('  FAIL: missing metrics')
    exit(1)
print(f'  PASS: ret={m[\"total_return\"]:.1%} sharpe={m[\"sharpe_ratio\"]:.2f}')
" 2>/dev/null

# 5. Data fetcher — can it still fetch?
echo "[5/6] Data fetcher check..."
python3 -c "
import sys; sys.path.insert(0, '.')
from data_fetcher import fetch_ohlcv
df = fetch_ohlcv('AAPL', start='2024-01-01', cache=True)
if len(df) < 100:
    print(f'  FAIL: only {len(df)} rows')
    exit(1)
print(f'  PASS: {len(df)} rows')
" 2>/dev/null

# 6. App routes — are all API endpoints registered?
echo "[6/6] App route check..."
python3 -c "
import sys; sys.path.insert(0, '.')
import app
rules = [r.rule for r in app.app.url_map.iter_rules()]
required = ['/', '/api/leaderboard', '/api/strategies', '/api/market', '/api/scan/<symbol>',
            '/api/catalyst/<symbol>', '/api/chart/<symbol>', '/api/trade-plan/<strategy>',
            '/api/stock-pick']
missing = [r for r in required if r not in rules]
if missing:
    print(f'  FAIL: missing routes: {missing}')
    exit(1)
print(f'  PASS: {len(rules)} routes registered')
"

echo ""
echo "=== ALL VALIDATION PASSED ==="

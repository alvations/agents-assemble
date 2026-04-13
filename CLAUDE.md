# agents-assemble

Trading agents and algorithms for publicly tradable instruments on Robinhood, Public.com, Tiger Brokers, IBKR, eToro, IG.

## Architecture

```
agents-assemble/
  agents_assemble/                # Python package (pip install -e .)
    data/fetcher.py               — Market data (yfinance, FRED, SEC, premium)
    engine/backtester.py          — Event-driven backtesting engine
    engine/judge.py               — Strategy grading, ranking, diagnosis
    engine/recommender.py         — Trade recommendation generator
    strategies/generic.py         — 10 built-in personas
    strategies/famous.py          — 13 famous investor personas
    strategies/themes.py          — 11 theme-based strategies
    strategies/recession.py       — 4 recession strategies + regime detector
    strategies/unconventional.py  — 6 unconventional strategies
    strategies/research.py        — 10 research-backed strategies
    strategies/math.py            — 5 math-driven strategies
    strategies/hedge_fund.py      — 2 hedge fund-inspired strategies

  # Flat source files (for self-evolution)
  backtester.py, personas.py, famous_investors.py, theme_strategies.py,
  recession_strategies.py, unconventional_strategies.py, research_strategies.py,
  math_strategies.py, hedge_fund_strategies.py, data_fetcher.py, judge.py,
  trade_recommender.py

  # Runners
  run_hypotheses.py               — Single-horizon hypothesis runner
  run_multi_horizon.py            — Multi-horizon (1Y/3Y/5Y/10Y) runner
  sync_package.py                 — Sync flat files → package after evolution

  # Data & Results
  knowledge/                      — Research findings, results, failures
  results/                        — Backtest result JSON files
  strategy/winning/               — Winning trade recommendations
  strategy/losing/                — Losing strategies (don't repeat!)
  LEADERBOARD.md                  — Definitive multi-horizon rankings
```

## 214 Strategies (15 categories)

| Category | Count | File |
|----------|-------|------|
| Unconventional | 45 | unconventional_strategies.py |
| Themes | 42 | theme_strategies.py |
| Famous Investors | 20 | famous_investors.py |
| Portfolio | 17 | portfolio_strategies.py |
| Crisis/Commodity | 12 | crisis_commodity_strategies.py |
| Williams Seasonal | 12 | williams_seasonal_strategies.py |
| News/Event | 10 | news_event_strategies.py |
| Recession | 10 | recession_strategies.py |
| Generic | 10 | personas.py |
| Research | 10 | research_strategies.py |
| Political | 9 | political_strategies.py |
| Math | 8 | math_strategies.py |
| Hedge Fund | 7 | hedge_fund_strategies.py |
| Orchestrator | 2 | strategy_orchestrator.py |

## Universe

61 categories, 451 unique tickers spanning:
US (mega/small/mid/micro), China (65 ADRs), Europe (37 by country),
Japan (13), India (8), Korea/Taiwan (9), LatAm (30), Australia (4),
Africa (6), Middle East (6), SE Asia (2), Dividend Aristocrats (47),
Dividend Kings (21), sector themes (fintech, cybersecurity, gaming,
water, nuclear, quantum, cannabis, space, EV).

## Self-Evolution

CRITICAL: Use PYTHONPATH when evolving files that import from each other:
```bash
cd agents-assemble
PYTHONPATH=$(pwd) python3 ../self_evolve.py <file>.py -n 3 --verbose --resume
python3 sync_package.py  # After evolution, sync to package
```

## Key Findings

- **ALWAYS backtest** — never trust any strategy blindly
- **Test 4 horizons** — 1Y, 3Y, 5Y, 10Y (a 3Y winner may be a 10Y loser)
- **Momentum Crash-Hedged is MOST CONSISTENT** — >0.7 Sharpe on all 4 horizons
- **Bond fallback fails in rate hike cycles** — use gold/cash as third option
- **Factor ETF rotation doesn't work** — ETFs too correlated with SPY
- **Insider buying proxy** — distance from 52-week high is #1 predictor
- See knowledge/failures_log.md for strategies NOT to repeat

## API Keys (env vars, optional)

- `FRED_API_KEY` — Macro data (free registration)
- `FINNHUB_API_KEY` — Social sentiment, insider trades (60/min free)
- `ALPHA_VANTAGE_KEY` — Real-time quotes (5/min free)
- `POLYGON_API_KEY` — Tick data (5/min free, delayed)
- `NEWS_API_KEY` — Financial news (100/day free)

## Research-to-Strategy Pipeline (MUST CHECK BEFORE ANY WORK)

**Before self-evolving or doing any other work, agents MUST:**

1. Check `knowledge/research_queue.md` for pending strategies
2. If any items are marked `[ ]` (not implemented), implement them FIRST
3. Follow the process in that file: implement → backtest → save → update leaderboard → commit

**The pipeline:**
```
Research Agent discovers gaps → knowledge/research_queue.md → Strategy Agent implements →
Backtester validates → trade_recommender saves to strategy/{winning,losing}/ →
LEADERBOARD.md updated → git commit + push
```

**Key files:**
- `knowledge/research_queue.md` — Source of truth for pending strategy research
- `stock_picker.py` — StockPick feature (core GUI: AI strategy matcher)
- `regen_missing.py` — Batch backtest + commit script for missing strategies
- `sync_package.py` — MUST run after editing any strategy file

**Rules:**
- NEVER delete strategy files before replacements are ready
- Strategy files are versioned with timestamps — keep latest, remove old duplicates
- Cache is canonical per-ticker (`ohlcv_AAPL_1d.parquet`) — no date range in filename
- Every strategy MUST have both .md and .json in strategy/winning/ or strategy/losing/
- Every strategy JSON MUST have `position_recommendations` populated (not empty)
- `while True` loops in generate_signals MUST have max iteration cap (use `for _ in range(5)`)

## Trading Philosophy: Patient, Thesis-Driven Fund

**This is NOT a day-trading operation.** It is a patient, thesis-driven fund that
makes 20-30 trades per YEAR, not per day.

### Core Rules
- Trade LESS, not more. A great fund makes 20-30 trades per YEAR.
- Each position has a THESIS (why we believe this will work over 1-5 years).
- Each position has predetermined take profit, stop loss, and exit criteria SET AT ENTRY.
- The daily loop mostly MONITORS and WAITS. It rarely trades.
- Pre-market research identifies OPPORTUNITIES, not daily trades.

### Key Files
- `daily_trader.py` — PatientDailyTrader (default) + HorizonDailyTrader (legacy)
- `research_parser.py` — Parse pre-market research, score opportunities (0-100)
- `circuit_breaker.py` — Emergency stop system (GREEN/YELLOW/RED)
- `risk_manager.py` — Pre-trade risk checks + cost estimation
- `trading_log.py` — Trade and P&L logging
- `public_trader.py` — Public.com API execution

### Daily Loop (PatientDailyTrader)
```
Morning:
  1. Check circuit breakers (is anything in emergency?)
  2. Check existing positions — has any hit take profit or stop loss?
     → If yes: execute the PLANNED exit (not a panic sell)
  3. Parse pre-market research for NEW opportunities
     → Only act if score > 70 (HIGH_CONVICTION_THRESHOLD)
     → Most days: no new trades (this is correct behavior)
  4. Log everything

NOT every day:
  5. Quarterly: rebalance core (10Y) positions
  6. Monthly: review strategic (3Y) positions
  7. Weekly: check tactical (1Y) positions
  8. Only on signal: opportunistic bucket
```

### Opportunity Scoring (research_parser.py)
```
+20: Multiple strategy triggers agree
+20: Thesis aligns with 3Y+ trend (not just a 1-day move)
+15: Risk/reward ratio > 3:1
+15: Strategy has >80% consistency in rolling windows
+10: Pre-market research explicitly highlights this opportunity
+10: Position fits within a horizon bucket that has room
+10: No correlation > 0.7 with existing positions
Threshold: only trade if score > 70
```

### Position Plans (set at entry, not changed daily)
```python
position_plan = {
    'symbol': 'XOM', 'entry_date': '2026-04-13', 'entry_price': 104.50,
    'thesis': 'Hormuz blockade → oil above $100 for 6+ months.',
    'horizon': '1Y',
    'take_profit': 125.40,   # +20% — set at entry, don't change
    'stop_loss': 88.83,      # -15% — set at entry, don't change
    'exit_trigger': 'Hormuz reopens fully OR oil drops below $70 for 30 days',
    'review_date': '2026-07-13',
    'max_position_pct': 0.05,
}
```

### Key Metrics
- Trade frequency: 2-3 per month (not per day)
- Average hold period: 6-18 months
- Win rate matters more than trade count
- Sharpe on REALIZED trades, not just positions

### Running
```bash
# Patient daily run (default — mostly does nothing)
python daily_trader.py

# Check only TP/SL exits
python daily_trader.py --check-exits

# Portfolio summary
python daily_trader.py --summary

# Legacy horizon-rebalance mode
python daily_trader.py --horizon-mode

# Parse pre-market research
python research_parser.py
```

## Quick Start

```bash
pip install -e .

# Run all strategies on 3-year horizon
python run_multi_horizon.py --horizon 3y

# Run single strategy
python run_multi_horizon.py --persona momentum_crash_hedge

# Run all strategies in a category
python run_multi_horizon.py --category research
```

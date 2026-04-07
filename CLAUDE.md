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

## 59 Strategies (8 categories)

| Category | Count | Top Performer | Avg Sharpe |
|----------|-------|--------------|-----------|
| Generic | 10 | Momentum (1.08) | — |
| Famous Investors | 13 | Masayoshi Son (0.87) | — |
| Themes | 11 | AI Revolution (0.94) | — |
| Recession | 4 | Defensive Rotation (0.59) | — |
| Unconventional | 6 | Quality Factor (0.20) | — |
| Research | 10 | Momentum Crash-Hedged (1.05) | — |
| Math | 5 | Kelly Optimal (0.67) | — |
| Hedge Fund | 2 | Healthcare+Asia (0.81) | — |

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

# agents-assemble

Trading agents and algorithms for publicly tradable instruments. **99 strategies**, 580 tickers, backtested across 9 horizons (1W to 10Y).

**Platforms:** Robinhood, Public.com, Tiger Brokers, IBKR, eToro, IG

> **Start here:**
> - **[LEADERBOARD.md](LEADERBOARD.md)** — Full rankings with Return + Sharpe + Max DD
> - **[strategy/winning/](strategy/winning/)** — Trade recommendations for winning strategies (entry, stop-loss, take-profit)
> - **[strategy/losing/](strategy/losing/)** — Strategies that failed (don't repeat these)
> - **[TRADING.md](TRADING.md)** — How to execute trades via Public.com API
> - **[knowledge/](knowledge/)** — 42 research files with backtested findings

## Top 5 Strategies (Return + Sharpe + Max DD)

| Rank | Strategy | 3Y Return | 3Y Sharpe | 3Y Max DD | 10Y Return |
|------|----------|-----------|-----------|-----------|-----------|
| 1 | **AI Revolution** | **183.6%** | **1.41** | -22.0% | 783% |
| 2 | **Concentrate Winners** | **135.6%** | **1.28** | -18.0% | 818% |
| 3 | **Momentum** | **135.0%** | **1.36** | -17.9% | 570% |
| 4 | **Momentum Crash-Hedged** | **117.1%** | **1.26** | -20.8% | 743% |
| 5 | **GLP-1 Obesity** | **80.7%** | **0.92** | -12.5% | — |

**NEW:** Williams %R(2) on SPY: 77% win rate, +96% 10Y, invested only 22% of the time → [LEADERBOARD.md](LEADERBOARD.md)

## Quick Start

```bash
pip install -e .

# Run all strategies on 3-year horizon
python run_multi_horizon.py --horizon 3y

# Run single strategy
python run_multi_horizon.py --persona concentrate_winners

# Run all strategies in a category
python run_multi_horizon.py --category research

# Test suite (99/99 should pass)
python tests/test_strategies.py
```

## Top 5 Strategies — 3Y (Return + Sharpe + Max DD)

| Rank | Strategy | 3Y Return | 3Y Sharpe | 3Y Max DD | Trade Rec |
|------|----------|-----------|-----------|-----------|-----------|
| 1 | **AI Revolution** | **183.6%** | **1.41** | -22.0% | [View](strategy/winning/) |
| 2 | **Concentrate Winners** | **135.6%** | **1.28** | -18.0% | [View](strategy/winning/) |
| 3 | **Momentum** | **135.0%** | **1.36** | -17.9% | [View](strategy/winning/) |
| 4 | **Momentum Crash-Hedged** | **117.1%** | **1.26** | -20.8% | [View](strategy/winning/) |
| 5 | **GLP-1 Obesity** | **80.7%** | **0.92** | -12.5% | [View](strategy/winning/) |

See **[LEADERBOARD.md](LEADERBOARD.md)** for all 99 strategies with full rankings.

## 99 Strategies Across 13 Categories

| Category | Count | Best Performer |
|----------|-------|---------------|
| Famous Investors | 20 | Ackman (1.22 Sharpe), Druckenmiller, Cathie Wood, BRK, Graham |
| Themes | 12 | AI Revolution (1.41 Sharpe), GLP-1, Robotics, Defense |
| Generic | 10 | Momentum (1.36 Sharpe), Concentrate Winners (1.28) |
| Research | 9 | Momentum Crash-Hedged (1.26 Sharpe) |
| Unconventional | 8 | Short Seller Dip Buy (+59.5%, 0.89 Sharpe) |
| Williams/Seasonal | 8 | Energy Seasonal (+39.7%), Williams %R (77% win SPY) |
| Political/Billionaire | 7 | Nancy Pelosi (1.39 Sharpe), Ken Griffin, Dan Loeb |
| Portfolio | 6 | Barbell (2.05 Sharpe 1Y), Core-Satellite |
| Crisis/Commodity | 5 | Geopolitical Crisis, Agriculture, Small Cap Value |
| Recession | 4 | Defensive Rotation (regime-switching) |
| News/Event | 3 | Earnings Drift (lowest DD: -3.6% 5Y) |
| Hedge Fund | 2 | Healthcare+Asia (0.82 Sharpe) |
| Math | 5 | Kelly Criterion (0.67 avg Sharpe) |
| Math | 5 | Kelly Optimal (0.67) |
| Hedge Fund | 2 | Healthcare+Asia (0.81) |
| News/Event | 3 | Earnings Surprise Drift (lowest DD: -3.6% 5Y) |

## Universe: 510 Tickers, 71 Categories

- **US:** mega/mid/small/micro cap, Dividend Aristocrats (47), Dividend Kings (21)
- **China:** 65 ADRs (BABA, JD, PDD, NIO, etc.)
- **Europe:** 37 ADRs by country (UK, Germany, France, Nordic, etc.)
- **Japan:** 13 ADRs (TM, SONY, MUFG, etc.)
- **India:** 8 ADRs + ETFs (INFY, IBN, HDB, INDA)
- **LatAm:** 30 (Brazil, Mexico, Argentina, Chile)
- **Africa/ME:** 12 (GOLD, HMY, CYBR, WIX, etc.)
- **Sectors:** fintech, cybersecurity, gaming, nuclear, quantum, cannabis, space, EV
- **Themes:** AI, GLP-1/obesity, robotics, data centers, semiconductors (24)
- **Commodities:** gold, silver, copper, uranium, lithium, agriculture

## Project Structure

```
agents-assemble/
  agents_assemble/              # Python package
    data/fetcher.py             # Market data (yfinance, FRED, SEC, premium APIs)
    engine/backtester.py        # Event-driven backtesting engine
    engine/judge.py             # Strategy grading and ranking
    engine/recommender.py       # Trade recommendations with entry/exit/stops
    strategies/                 # All strategy implementations
      generic.py, famous.py, themes.py, recession.py,
      unconventional.py, research.py, math.py, hedge_fund.py

  run_hypotheses.py             # Single-horizon backtest runner
  run_multi_horizon.py          # Multi-horizon (1Y/3Y/5Y/10Y) runner
  test_strategies.py            # Test suite (63/63 pass)
  sync_package.py               # Sync flat files → package after evolution

  LEADERBOARD.md                # Definitive strategy rankings
  CLAUDE.md                     # Development guide
  knowledge/                    # Research findings, failures log
  results/                      # Backtest JSON results
  strategy/winning/             # Trade recs for winning strategies
  strategy/losing/              # Failed strategies (don't repeat)
  .evolution/                   # Self-evolution history
```

## Key Findings

- **Always backtest** — never trust any strategy blindly
- **Test 4 horizons** — 1Y, 3Y, 5Y, 10Y (a 3Y winner may be a 10Y loser)
- **Concentration beats diversification** — top 3-5 stocks outperform equal-weight
- **Vol-scaling prevents crashes** — Momentum Crash-Hedged >0.7 Sharpe all horizons
- **Bond fallback fails in rate hikes** — use gold/cash as third option
- See `knowledge/failures_log.md` for strategies NOT to repeat

## API Keys (optional, set as env vars)

| Key | Source | Free Tier |
|-----|--------|-----------|
| `FRED_API_KEY` | FRED macro data | Unlimited |
| `FINNHUB_API_KEY` | Social sentiment, insider trades | 60 calls/min |
| `ALPHA_VANTAGE_KEY` | Real-time quotes | 5 calls/min |
| `POLYGON_API_KEY` | Tick data | 5 calls/min (delayed) |
| `NEWS_API_KEY` | Financial news headlines | 100/day |

## Tax Note (K-1 Warning)

Some commodity ETFs (USO, UNG, DBA) issue K-1 forms instead of 1099-DIV.
See `knowledge/tax_k1_warning.md` for safe alternatives.

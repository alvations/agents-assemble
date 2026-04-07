# agents-assemble

Trading agents and algorithms for publicly tradable instruments. Backtested across multiple time horizons with 63 strategies, 510 tickers, and comprehensive research.

**Platforms:** Robinhood, Public.com, Tiger Brokers, IBKR, eToro, IG

## Quick Start

```bash
pip install -e .

# Run all strategies on 3-year horizon
python run_multi_horizon.py --horizon 3y

# Run single strategy
python run_multi_horizon.py --persona concentrate_winners

# Run all strategies in a category
python run_multi_horizon.py --category research

# Test suite (63/63 should pass)
python test_strategies.py
```

## Top 5 Strategies (Cross-Horizon Consistency)

| Rank | Strategy | Avg Sharpe | 3Y Return | 10Y Return |
|------|----------|-----------|-----------|-----------|
| **1** | **Concentrate Winners** | **1.11** | 135.6% | 817.5% |
| 2 | Momentum | 1.08 | 135.0% | 570.0% |
| 3 | Momentum Crash-Hedged | 1.05 | 117.1% | 743.0% |
| 4 | AI Revolution | 0.94 | 183.6% | 783.3% |
| 5 | Masayoshi Son | 0.87 | 90.8% | 1068.3% |

See [LEADERBOARD.md](LEADERBOARD.md) for full rankings of all 66 strategies.

## 66 Strategies Across 9 Categories

| Category | Count | Best Performer |
|----------|-------|---------------|
| Generic | 10 | Momentum (1.08 avg Sharpe) |
| Famous Investors | 13 | Masayoshi Son (0.87) |
| Themes | 12 | AI Revolution (0.94) |
| Recession | 4 | Defensive Rotation (0.59) |
| Unconventional | 8 | Concentrate Winners (1.11) |
| Research | 9 | Momentum Crash-Hedged (1.05) |
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

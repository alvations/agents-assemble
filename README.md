# agents-assemble

Trading agents and algorithms for publicly tradable instruments. **99 strategies** (55 winning, 44 losing), 630+ tickers, backtested across 9 horizons (1W to 10Y).

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

## StockPick — AI Strategy Matcher (Core Feature)

Pick any stocks. We match them to our best backtested strategy, show vol-adjusted position sizing, suggest additional tickers, and get Claude AI's opinion.

**GUI:** Open `http://localhost:8888` → click **StockPick** tab

**Python API:**
```python
from stock_picker import analyze_stock_picks

# Analyze your picks — returns top 5 matching strategies
result = analyze_stock_picks(
    ["NVDA", "AAPL", "TSLA"],
    portfolio_amount=100_000,
    horizon="3y",       # "1y", "3y", or "5y"
    top_n=5,            # Number of strategy recommendations
    include_claude=True, # Get Claude AI commentary
)

# result["recommendations"] is a list of N strategy matches, each with:
for rec in result["recommendations"]:
    strat = rec["matched_strategy"]     # Strategy name, source, overlap
    bt = rec["backtest"]["metrics"]     # Return, Sharpe, MaxDD, Alpha
    positions = rec["positions"]        # Vol-adjusted position table
    # Each position: symbol, action, vol, entry, stop, target, size, $amount
    # User picks are highlighted; additional tickers are suggested
    print(rec["hypothesis"])            # Backtested evidence
    print(rec["claude_analysis"])       # Claude AI opinion
```

**How it works:**
1. Enter tickers (any stock — if not in our universe, we fetch and cache it)
2. System matches against 90+ backtested strategies by universe overlap
3. Runs fresh backtest on the matched strategy
4. Generates vol-adjusted positions: high-vol stocks (TSLA) get wider stops + smaller size; low-vol stocks (KO) get tighter stops + larger size
5. If your picks are weak, size = 0% with an explanation note
6. Claude AI reviews the whole thing
7. **Re-roll:** GUI shows 5 strategies in a carousel — click Next/Re-roll to cycle through shuffled alternatives

**Example output (NVDA, AAPL, TSLA → Momentum Trader):**

| | Symbol | Action | Vol | Stop Loss | Take Profit | Size |
|---|--------|--------|-----|-----------|-------------|------|
| YOUR PICK | NVDA | BUY | 49% | 16.8% | 6.7% | 3.3% |
| YOUR PICK | AAPL | BUY | 29% | 10.6% | 4.2% | 5.6% |
| YOUR PICK | TSLA | BUY | 62% | 21.1% | 8.5% | 2.6% |
| SUGGESTED | GOOGL | BUY | 30% | 10.9% | 4.3% | 5.4% |
| SUGGESTED | AMZN | BUY | 33% | 12.0% | 4.8% | 4.9% |

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

## Universe: 630+ Tickers, 72 Categories

- **US:** mega/mid/small/micro cap, Dividend Aristocrats (47), Dividend Kings (21)
- **China:** 65 ADRs (BABA, JD, PDD, NIO, etc.)
- **Europe:** 37 ADRs by country (UK, Germany, France, Nordic, etc.)
- **Japan:** 13 ADRs (TM, SONY, MUFG, etc.)
- **India:** 8 ADRs + ETFs (INFY, IBN, HDB, INDA)
- **Singapore (SGX):** 50+ stocks (DBS, UOB, OCBC, CapitaLand REITs, SingTel, Wilmar, ST Eng)
- **LatAm:** 30 (Brazil, Mexico, Argentina, Chile)
- **Africa/ME:** 12 (GOLD, HMY, CYBR, WIX, etc.)
- **Sectors:** fintech, cybersecurity, gaming, nuclear, quantum, cannabis, space, EV
- **Themes:** AI, GLP-1/obesity, robotics, data centers, semiconductors (24)
- **Commodities:** gold, silver, copper, uranium, lithium, agriculture
- **Dynamic:** StockPick automatically adds any new ticker to cache on first use

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

  stock_picker.py               # StockPick: AI strategy matcher (core feature)
  run_hypotheses.py             # Single-horizon backtest runner
  run_multi_horizon.py          # Multi-horizon (1Y/3Y/5Y/10Y) runner
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

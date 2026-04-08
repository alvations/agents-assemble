# Gap, Rotation, Breakout, Sentiment & Earnings Gap Strategies

Research date: 2026-04-06. All rules are codeable.

---

## 1. Gap Fill Strategy (SPY/ES)

**Core finding:** Small gaps fill reliably; large gaps do not.

| Gap Size | Bullish Fill % | Bearish Fill % |
|----------|---------------|----------------|
| >0.1%    | 59%           | 61%            |
| >0.5%    | 43%           | 42%            |
| >1.0%    | 28%           | 33%            |

**Codeable rules (SPY gap-down fade):**
- Entry: SPY gaps down -0.15% to -0.6% at open AND yesterday `(close-low)/(high-low) < 0.25`
- Target: 75% of gap size filled
- Stop: exit at close if target not hit (no hard stop)
- Backtest (2010-2012): 110 trades, **89% win rate**, avg +0.19%/trade
- Enhanced filter: if yesterday's close is 2%+ below 10d MA, avg return rises to +0.185%
- Best day: Friday shows strongest equity curve
- Ticker: SPY or ES futures

**Expected annual return:** ~15-20% (high-frequency, small per-trade)

---

## 2. Sector ETF Momentum Rotation (Monthly)

**Core finding:** Top-3 sector momentum beats S&P 500 by ~4%/yr.

**Codeable rules:**
- Universe: XLB, XLC, XLE, XLF, XLI, XLK, XLP, XLRE, XLU, XLV, XLY (11 SPDR sectors)
- Rank all by 3-month total return (use 12-month as alternative)
- Buy top 3, equal-weight (33.3% each)
- Rebalance: last trading day of each month
- Hold: 1 month, then re-rank
- Backtest (1928-2009 equivalent data): **CAGR 13.94%**, Sharpe 0.54, max DD -46%
- Outperforms buy-and-hold in ~70% of years
- 3-month lookback variant: **CAGR 11.5%**, max DD -32% (better risk-adjusted)

**Simpler 3-ETF version:** SPY/TLT/EEM, buy best 3-month performer monthly. CAGR 11.5%, max DD -32%.

---

## 3. 52-Week High Breakout Strategy

**Core finding:** Stocks near 52-week highs continue higher, especially with volume + fundamentals.

**Codeable rules:**
- Screen: stock closes at new 52-week high
- Volume filter: today's volume > 150% of 20-day avg volume
- Fundamental filter: Piotroski F-Score > 7 (or simpler: above 50d AND 200d MA)
- Entry: buy at close on breakout day
- Exit: 2-day RSI > 99 OR after 75 trading days OR close below 200d MA
- Backtest: **0.65%/month** (7.8% annualized) for pure 52-week-high momentum
- With volume+fundamentals: **+23.7% over 90 days** (vs 8.3% without fundamentals)
- Breakout with 150%+ volume: continues higher **72% of the time**, avg +11.4% over 31 trading days
- Universe: S&P 100 or S&P 500 stocks
- Position size: 25% per trade, max 4 positions

**Key insight:** Short holds (5-10 days) show negative returns. Must hold 30+ days.

---

## 4. Put-Call Ratio Contrarian Strategy

**Core finding:** Extreme fear readings are decent buy signals; extreme greed is a weak sell signal.

**Codeable rules:**
- Data source: CBOE equity put-call ratio (daily)
- Buy signal: 10-day MA of PCR > 1.2 (extreme fear) -> go long SPY
- Sell/caution signal: 10-day MA of PCR < 0.6 (extreme greed) -> reduce exposure
- Alternative threshold: single-day PCR spike > 3.0 (rare panic)
- Hold: 115 days from signal for best results -> avg +6.36%/trade
- Shorter holds (5-30 days) show diminished but positive returns
- Win rate: not formally reported; researchers consider it "not impressive" standalone
- Better as a filter/overlay than primary signal
- Ticker: SPY or QQQ for execution

**Practical use:** Combine with other strategies -- when PCR > 1.2, increase position sizes on other long signals by 25-50%. Not a standalone system.

---

## 5. Earnings Gap Continuation (Gap-and-Go)

**Core finding:** Large earnings gaps with massive volume tend to continue; small gaps tend to fill.

**Codeable rules:**
- Screen: stock gaps up 4%+ at open after earnings release
- Volume filter: premarket volume > 3x 20-day average (for large caps); > 5x for small caps
- Catalyst: confirmed earnings beat (EPS surprise > 0%)
- Entry: buy at open if gap holds first 5 minutes (price stays above prior close + 3%)
- Exit option A (day trade): sell at close same day
- Exit option B (swing): hold 3-5 days with trailing stop at gap-fill level
- Fill rate reality: 80%+ of small gaps fill by noon; large (4%+) gaps fill only 28-33%
- Expected win rate: ~60-70% for qualified setups (4%+ gap, volume confirmed)
- Key stat from April 2025: SPY gapped +3.5%, then fell -4.9% from open (large index gaps are unreliable; single stocks with earnings catalysts are better)

**Tickers to scan:** Focus on individual stocks with earnings, NOT index ETFs. Use finviz screener for gap-ups > 4% with earnings catalyst.

---

## Strategy Comparison Summary

| Strategy | Win Rate | Avg Return/Trade | Hold Period | Complexity |
|----------|----------|-----------------|-------------|------------|
| Gap Fill (SPY) | 89% | +0.19% | 1 day | Low |
| Sector Rotation | ~70% yr | +11.5% CAGR | 1 month | Low |
| 52-Week Breakout | 72% | +11.4%/31d | 30-75 days | Medium |
| Put-Call Contrarian | ~55% est | +6.36%/115d | 115 days | Low |
| Earnings Gap-and-Go | 60-70% | +2-5%/trade | 1-5 days | High |

## Sources

- [QuantifiedStrategies: Gap Fill](https://www.quantifiedstrategies.com/gap-fill-trading-strategies/)
- [QuantifiedStrategies: 52-Week High](https://www.quantifiedstrategies.com/52-week-high-strategy/)
- [QuantifiedStrategies: Put-Call Ratio](https://www.quantifiedstrategies.com/put-call-ratio-backtest-strategy/)
- [QuantifiedStrategies: ETF Rotation](https://www.quantifiedstrategies.com/etf-rotation-strategy/)
- [QuantifiedStrategies: Unfilled Gaps](https://www.quantifiedstrategies.com/unfilled-gap-trading-strategies/)
- [Quantpedia: Sector Momentum](https://quantpedia.com/strategies/sector-momentum-rotational-system)
- [Kavout: 52-Week High Momentum](https://www.kavout.com/market-lens/mastering-the-52-week-high-momentum-strategy-a-practical-guide-for-investors)
- [Trade That Swing: SPY Gap Stats](https://tradethatswing.com/sp-500-spy-es-gap-fill-strategy-and-statistics/)
- [George & Hwang: 52-Week High Paper](https://www.bauer.uh.edu/tgeorge/papers/gh4-paper.pdf)
- [Swastika: 52-Week Breakout 2026](https://www.swastika.co.in/blog/52-week-high-breakout-strategy-in-2026-how-traders-spot-momentum-stocks-should-you-buy-them)

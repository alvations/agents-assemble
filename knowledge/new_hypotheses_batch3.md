# Calendar & Seasonal Trading Hypotheses (Batch 3)

Research date: 2026-04-06

---

## Hypothesis 1: January Effect Small-Cap Tax-Loss Harvesting Reversal

### Thesis
Tax-loss harvesting in December forces institutional and retail selling of beaten-down small caps. In late December through January, buying pressure returns as investors redeploy capital. AQR data shows small stocks outperform large stocks by 2.1% in January on average (1926-2017). In January 2026, IWM surged ~9% YTD as capital rotated away from mega-cap tech ("AI fatigue") into domestic small-cap value.

### Caveats
- The effect has weakened significantly post-2000 and is declining for Russell indices
- January 2024 saw small caps FALL -3.89%, lagging large caps by 528 bps
- Timing has shifted earlier: the move often starts mid-December, not January 1
- November and December have actually been the most profitable months for small caps (1979-2024)

### Tickers
- **Long:** IWM (Russell 2000 ETF), IJR (S&P SmallCap 600, requires earnings = higher quality), VB (Vanguard Small-Cap), SCHA (Schwab Small-Cap), SPSM (SPDR S&P 600 Small Cap)
- **Micro-cap tilt (stronger effect):** IWC (iShares Micro-Cap), EWMC (Invesco S&P SmallCap 600 Equal Weight)
- **Leveraged (aggressive):** TNA (Direxion Small Cap Bull 3X)

### Entry/Exit Logic
1. **Entry:** Buy at close on December 15 (or the Monday of the 3rd week of December)
2. **Position:** Equal-weight IJR + IWM (IJR preferred for quality screen)
3. **Exit:** Sell at close on January 31 (or first trading day of February)
4. **Stop-loss:** -5% from entry (small caps can gap down hard)
5. **Filter:** Only enter if Russell 2000 is down >5% from its 52-week high in December (suggests tax-loss selling has occurred)

### Expected Horizon
6-7 weeks (mid-December to end of January)

### Expected Alpha
+2-4% over SPY in a typical year; 0% or negative in years when large caps are in a strong momentum regime

### Confidence
MEDIUM-LOW. The anomaly is well-documented but weakening. The quality filter (IJR over IWM) and December pre-positioning improve odds.

---

## Hypothesis 2: OPEX Week Bullish Drift (Monthly Options Expiration)

### Thesis
The week of monthly options expiration (3rd Friday of each month) shows above-average S&P 500 returns due to dealer hedging flows. Market makers delta-hedging large option positions create systematic buying pressure during the week. Backtest shows 2% CAGR from holding only during OPEX weeks (~18% of trading days). However, OPEX Friday itself is historically negative (compounded returns of -23.55%, win rate 51.4%).

### Key Finding
March is the strongest OPEX month by far (+1.09% average). July and January are the weakest. The effect exists because hedge rebalancing by option market makers in the most actively traded names creates predictable buying flow.

### Tickers
- **Primary:** SPY (S&P 500 ETF), QQQ (Nasdaq 100)
- **Leveraged (aggressive):** SPXL (S&P 500 Bull 3X), TQQQ (Nasdaq 100 Bull 3X)
- **Volatility play:** Sell VIX puts or buy short-dated VIX call spreads to fade the volatility suppression

### Entry/Exit Logic
1. **Entry:** Buy SPY at Monday open of OPEX week (the week containing the 3rd Friday)
2. **Exit:** Sell at Thursday close (day BEFORE expiration Friday)
3. **DO NOT hold through Friday** -- OPEX day itself averages -0.77% loss
4. **Monthly filter:** Prioritize March OPEX (strongest month). Avoid July and January
5. **Position size:** Standard (no leverage unless strong conviction)

### 2026 OPEX Calendar (Monthly Expiration Fridays)
Jan 16, Feb 20, Mar 20, Apr 17, May 15, Jun 18 (Thu, Juneteenth), Jul 17, Aug 21, Sep 18, Oct 16, Nov 20, Dec 18

### Expected Horizon
4 days per trade (Monday open to Thursday close), 12 times per year

### Expected Alpha
+0.35% per trade average, 61% win rate. Exiting Thursday instead of Friday improves to +0.55% average, 65% win rate. Annualized ~4.2% with only 18% time in market.

### Confidence
MEDIUM-HIGH. Mechanistic explanation (dealer hedging) is sound. Effect is consistent across decades. Exit-before-Friday rule is critical.

---

## Hypothesis 3: Pre-FOMC Announcement Drift

### Thesis
The S&P 500 has averaged +49 bps in the 24 hours before FOMC announcements since 1994. A NY Fed study found ~80% of the annual US equity premium was earned in just the 24 hours before the 8 yearly FOMC meetings. The mechanism: uncertainty resolution + risk premium compression as the announcement approaches. Buying SPY 48 hours before and selling at close of announcement day yields ~0.5% per trade (vs 0.08% for random 2-day periods).

### Caveats
- The drift has weakened significantly after 2015 (post-publication decay)
- Works best in high-uncertainty environments (high VIX)
- Post-meeting performance is poor -- do NOT hold after the announcement
- Bitcoin shows the opposite: "sell the news" in 7 of 8 FOMC meetings in 2025

### Tickers
- **Primary:** SPY, QQQ
- **Leveraged:** SPXL (3x S&P), TQQQ (3x Nasdaq). Backtest shows 8-9% CAGR with 3x leveraged ETFs despite trading only 5% of days (Sharpe ~0.6)
- **Bonds (inverse play):** TLT rallies if dovish; sell TLT if hawkish expected
- **Gold:** GLD tends to rally pre-FOMC on uncertainty

### Entry/Exit Logic
1. **Entry:** Buy SPY at close, 2 trading days before FOMC announcement
2. **Exit:** Sell at close on FOMC announcement day (statement + press conference day)
3. **DO NOT hold overnight after the announcement** -- post-FOMC returns are negative
4. **VIX filter:** Only enter if VIX > 18 (the drift is strongest in high-uncertainty periods)
5. **Rate expectations filter:** Check CME FedWatch. If market assigns >90% probability to a specific outcome, the drift is smaller (less uncertainty to resolve)

### 2026 FOMC Meeting Schedule (Announcement Days)
Jan 28, Mar 18*, Apr 29, Jun 17*, Jul 29, Sep 16*, Oct 28, Dec 9*
(*with Summary of Economic Projections / dot plot -- higher volatility)

### Expected Horizon
2-day holding period, 8 times per year

### Expected Alpha
+0.5% per trade average. With 3x leverage: ~1.5% per trade. Annual contribution: ~4% (unleveraged), ~12% (3x leveraged). Sharpe ratio historically >1.0 (pre-2015), ~0.5-0.6 post-2015.

### Confidence
MEDIUM. The academic evidence is among the strongest of any calendar anomaly. However, post-publication decay is real. The VIX filter helps select for the trades most likely to work.

---

## Hypothesis 4: Post-Earnings Announcement Drift (PEAD)

### Thesis
Stocks that beat earnings estimates continue to drift upward for 60 trading days (~one quarter) after the announcement. Stocks that miss continue to drift downward. This is one of the most robust anomalies in finance (Ball & Brown, 1968). A long-short portfolio based on Standardized Unexpected Earnings (SUE) deciles generates 5.1% abnormal returns over 3 months (~20% annualized). Zacks ESP (Earnings Surprise Prediction) combined with Zacks Rank >= 3 produces positive surprises 70% of the time with 28.3% average annual returns in a 10-year backtest.

### Key Nuance
The drift is strongest for small caps with low analyst coverage (information takes longer to be priced in). Enter on Day 2 after announcement to avoid initial volatility spike.

### Tickers (Implementation Vehicles)
- **Broad exposure:** PRF (Invesco FTSE RAFI US 1000 -- value-weighted, captures drift), SPHQ (S&P 500 Quality)
- **Earnings-focused ETFs:** EPRF (Innovator S&P 500 Power Buffer), PQDI (Principal Spectrum Tax-Advantaged Dividend Active)
- **Individual stock screener approach (preferred):**
  - Screen for: actual EPS > consensus estimate by > 1 standard deviation (top SUE decile)
  - Focus on: S&P 500 and Russell 2000 names with < 10 analyst coverage
  - Current Q1 2026 earnings season mega-caps reporting: AMZN (Apr 23), GOOGL (Apr 28), META (Apr 29), AAPL (Apr 30)

### Entry/Exit Logic
1. **Screen:** After each earnings report, compute SUE = (Actual EPS - Consensus EPS) / Std Dev of past surprises
2. **Entry:** Buy at open on Day 2 after earnings (T+2) if SUE is in top quintile AND revenue also beat estimates
3. **Exit:** Hold for 60 trading days (one calendar quarter), then sell
4. **Short side (optional):** Short stocks in bottom SUE quintile (missed by > 1 std dev) on T+2, cover after 60 days
5. **Position sizing:** Equal-weight portfolio of 10-20 names per earnings season
6. **Stop-loss:** -8% from entry (earnings misses can cascade)

### Earnings Season Calendar 2026
- Q4 2025 reports: January-February 2026
- Q1 2026 reports: April-May 2026 (CURRENT)
- Q2 2026 reports: July-August 2026
- Q3 2026 reports: October-November 2026

### Expected Horizon
60 trading days per position; new positions entered 4x/year during earnings seasons

### Expected Alpha
+2.6% to +9.4% per quarter (long-only, top SUE quintile). Long-short: ~5.1% per quarter. Declining in recent years due to faster information processing, but still statistically significant.

### Confidence
HIGH. Most academically robust anomaly on this list. Survives out-of-sample, international markets, and multiple time periods. The T+2 entry and quality filters are critical for implementation.

---

## Hypothesis 5: Triple Witching Week Volatility Fade

### Thesis
Triple witching (simultaneous expiration of stock options, index options, and index futures) occurs on the 3rd Friday of March, June, September, and December. The week leading up shows elevated but suppressed volatility (gamma pinning), followed by violent moves on Friday as ~$5 trillion in contracts expire. Key stats: triple witching days show median S&P 500 return of -0.36% (vs +0.10% normal days), only 25% win rate, and daily range expands 7%. However, buying Monday and selling Thursday before the witching Friday yields +0.55% average, 65% win rate over 128 trades.

### Mechanism
Before expiration, positive gamma from large option positions suppresses volatility (market makers buy dips, sell rallies). At expiration, gamma collapses toward zero, removing the stabilizing force. In negative gamma, market makers amplify moves (sell into falls, buy into rallies). This creates predictable pre/post patterns.

### Tickers
- **Long (Mon-Thu of witching week):** SPY, QQQ
- **Volatility play (post-witching):** Buy VIX calls or UVXY on Thursday before witching Friday to capture the volatility expansion
- **Short vol (during witching week Mon-Thu):** Sell SPX straddles or iron condors as gamma pinning suppresses movement
- **Rebalancing beneficiary:** Watch stocks being added/removed from S&P 500 index during March and September rebalances (which coincide with witching)

### Entry/Exit Logic

**Strategy A: Equity Long (Monday-Thursday)**
1. **Entry:** Buy SPY at open on Monday of triple witching week
2. **Exit:** Sell at close on Thursday
3. **DO NOT hold through Friday** -- the witching day itself averages -0.52%
4. **Expected return:** +0.55% per trade, 65% win rate

**Strategy B: Volatility Expansion (Post-Witching)**
1. **Entry:** Buy VIX calls (1-2 weeks out, slightly OTM) at Thursday close
2. **Exit:** Sell Monday/Tuesday of the following week after gamma unpin causes volatility spike
3. **Risk:** Limited to premium paid

**Strategy C: Short Vol During Pinning (Mon-Wed)**
1. **Entry:** Sell SPX iron condors (5-10 delta wings) on Monday of witching week
2. **Exit:** Close at Wednesday close or Thursday open (before gamma collapse begins)
3. **Risk:** Defined by iron condor structure

### 2026 Triple Witching Dates
March 20, June 19, September 18, December 18

### Expected Horizon
4 days per trade (Monday-Thursday), 4 times per year

### Expected Alpha
Strategy A: +0.55% per trade, ~2.2% annually from 4 trades. Strategy B: Variable, depends on post-witching volatility expansion. Strategy C: Collect ~1-2% of notional per trade from theta decay during gamma pinning.

### Confidence
MEDIUM-HIGH. The mechanical explanation (gamma pinning and unpin) is well-understood by options market makers. The Monday-Thursday long strategy has strong backtested evidence (128 trades, 65% win rate). The key edge is avoiding Friday.

---

## Combined Calendar Strategy: Optimal Trading Calendar 2026

### Stacking Multiple Effects

When multiple calendar anomalies overlap, the expected edge compounds:

| Date Range | Events Overlapping | Expected Edge |
|---|---|---|
| Mar 16-19, 2026 | OPEX week + Triple Witching + FOMC (Mar 18) | **Triple stack**: Pre-FOMC drift + OPEX bullish week + witching pinning |
| Jun 15-18, 2026 | OPEX week + Triple Witching + FOMC (Jun 17) | **Triple stack** |
| Sep 14-17, 2026 | OPEX week + Triple Witching + FOMC (Sep 16) | **Triple stack** |
| Dec 7-9, 2026 | FOMC meeting + pre-January-effect positioning | **Double stack**: FOMC drift + early January effect rotation into small caps |
| Apr 27-29, 2026 | FOMC (Apr 29) + peak earnings season | **Double stack**: FOMC drift + PEAD opportunities from mega-cap earnings |

### Implementation Priority

1. **Highest conviction:** PEAD (Hypothesis 4) -- strongest academic backing, most robust
2. **Best risk/reward:** OPEX Monday-Thursday (Hypothesis 2) -- mechanical edge, frequent
3. **Most alpha per trade:** Pre-FOMC drift (Hypothesis 3) -- but only 8 trades/year
4. **Best combined event:** Triple Witching Monday-Thursday (Hypothesis 5) -- 4x/year, strong win rate
5. **Most speculative:** January Effect (Hypothesis 1) -- weakening, but still works in risk-off years

---

## Sources

### January Effect
- [2026 January Effect: Small-Caps Dethrone Magnificent 7](https://markets.financialcontent.com/stocks/article/marketminute-2026-3-3-the-2026-january-effect-small-caps-dethrone-the-magnificent-7-in-historic-market-rotation)
- [January Effect Still Work? Historical Data - EBC](https://www.ebc.com/forex/does-the-january-effect-still-work-what-historical-data-shows)
- [Invesco: January Effect and Stock Performance](https://www.invesco.com/us/en/insights/january-effect-stock-performance.html)
- [Quantpedia: January Effect in Stocks](https://quantpedia.com/strategies/january-effect-in-stocks)
- [Nasdaq: How to Play January Effect With Small-Cap ETFs](https://www.nasdaq.com/articles/how-play-january-effect-small-cap-etfs)
- [Seeking Alpha: January Effect Small or Large Caps](https://seekingalpha.com/article/4746332-january-effect-small-or-large-caps)

### OPEX Week
- [Quantified Strategies: Options Expiration Week Effect (Backtest)](https://www.quantifiedstrategies.com/the-option-expiration-week-effect/)
- [Quantpedia: Option-Expiration Week Effect](https://quantpedia.com/strategies/option-expiration-week-effect)
- [MenthorQ: OPEX Guide](https://menthorq.com/guide/option-expiration-week/)
- [Quantified Strategies: Day Before OPEX Day](https://www.quantifiedstrategies.com/what-has-happened-the-day-before-opex-day/)
- [Macroption: Options Expiration Calendar 2026](https://www.macroption.com/options-expiration-calendar/)

### FOMC Pre-Announcement Drift
- [NY Fed Staff Report: Pre-FOMC Announcement Drift](https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr512.pdf)
- [Quantified Strategies: FOMC Meeting Trading Strategy Backtest](https://www.quantifiedstrategies.com/fomc-meeting-trading-strategy/)
- [Taylor & Francis: Pre-FOMC Drift Short-Lived or Long-Lasting](https://www.tandfonline.com/doi/full/10.1080/00036846.2024.2322573)
- [NIH/PMC: Disappearing Pre-FOMC Announcement Drift](https://pmc.ncbi.nlm.nih.gov/articles/PMC7525326/)
- [Quantpedia: FOMC Meeting Effect in Stocks](https://quantpedia.com/strategies/federal-open-market-committee-meeting-effect-in-stocks)
- [Federal Reserve: 2026 FOMC Calendar](https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm)

### Post-Earnings Announcement Drift (PEAD)
- [Wikipedia: Post-Earnings-Announcement Drift](https://en.wikipedia.org/wiki/Post%E2%80%93earnings-announcement_drift)
- [Quantpedia: Post-Earnings Announcement Effect](https://quantpedia.com/strategies/post-earnings-announcement-effect)
- [Analyzing Alpha: PEAD](https://analyzingalpha.com/post-earnings-announcement-drift)
- [Zacks: Earnings Surprise Predictions](https://www.zacks.com/earnings/earnings-surprise-predictions/)
- [Philadelphia Fed: PEAD.txt Using Text](https://www.philadelphiafed.org/-/media/frbp/assets/working-papers/2021/wp21-07.pdf)

### Triple Witching
- [Quantified Strategies: Quadruple Witching Backtest](https://www.quantifiedstrategies.com/quadruple-witching/)
- [Kavout: Why March 20 2026 Triple Witching Matters](https://www.kavout.com/market-lens/what-is-triple-witching-and-why-does-march-20-2026-matter)
- [Benzinga: S&P 500 Triple Witching 25% Win Rate](https://www.benzinga.com/etfs/broad-u-s-equity-etfs/26/03/51320368/sp-500-braces-for-triple-witching-as-financials-signal-deeper-correction-index-closed-up-only-25-of-the-time-in-last-5-years)
- [Option Alpha: Triple Witching Dates 2026](https://optionalpha.com/learn/triple-witching)
- [MenthorQ: Triple Witching and Market Volatility Guide](https://menthorq.com/guide/triple-witching-and-market-volatility/)

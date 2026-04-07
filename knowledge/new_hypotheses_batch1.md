# Trading Hypotheses Batch 1 -- Event-Driven & Corporate Action Strategies

Generated: 2026-04-06

---

## Hypothesis 1: IPO Lockup Expiration Short

**Thesis:** Stocks of recently-IPO'd companies experience statistically significant declines (1-3% average, up to 10-80% for overvalued names) around lockup expiration dates as insiders dump shares. VC-backed firms show the worst declines (-1.6% to -2.6% cumulative abnormal return in the -2 to +2 day window). The 2025-2026 IPO class has been especially brutal -- Bloomberg documented a "negative feedback loop" where beaten-down IPOs face further selling pressure as lockups expire on stocks already trading well below IPO price.

**Research basis:**
- Ofek & Richardson (2000): average 1-3% decline at lockup expiry
- VC-backed firms: CAR of -1.6% to -2.6% in 5-day event window
- Figma (FIG): crashed 81% from highs before full lockup expiry, with staggered releases through June 2026
- StubHub (STUB): plunged 12.4% on lockup day (March 16, 2026) compounded by earnings miss
- Klarna (KLAR): 335M shares (90% of outstanding) became eligible March 9, 2026; stock was trading 65% below IPO price

**Specific tickers & dates:**
| Ticker | Company | Lockup Event | Notes |
|--------|---------|-------------|-------|
| FIG | Figma | Staggered through June 2026; final VC release ~Aug 31, 2026 | 54% of shares in extended lockup. Stock already ~80% below ATH. Watch for selling waves each quarter. |
| KLAR | Klarna | Expired March 9, 2026 (335M shares / 90% of float) | Continued selling pressure likely for weeks post-expiry. Monitor volume for exhaustion. |
| STUB | StubHub | Expired March 16, 2026 | Already plunged 12.4%. JPM downgraded to neutral, PT slashed to $10 from $22. Potential dead-cat bounce trade. |

**Entry/exit logic:**
- **Short entry:** 5-7 trading days before lockup expiry date. Confirm with rising short interest and high insider share overhang (>50% of float locked).
- **Position sizing:** 2-3% of portfolio per position. Use options (put spreads) for defined risk.
- **Exit (cover short):** 3-5 days after lockup date, or when volume normalizes to pre-event average.
- **Alternative (long after flush):** If stock drops >15% on lockup week AND has strong fundamentals, buy 10-15 days post-expiry for recovery bounce. Use 52-week low as stop.
- **Key filter:** Best results on VC-backed names where insider ownership >40% and stock has appreciated significantly since IPO (insiders motivated to sell).
- **Avoid:** Shorting if stock is already deeply below IPO price (selling may be lighter as insiders hope for recovery).

**Data sources:** MarketBeat lockup calendar, IPOScoop.com, Briefing.com IPO lockups calendar.

**Expected horizon:** 2-4 weeks around each lockup date.

---

## Hypothesis 2: Earnings Whisper Number Fade/Chase

**Thesis:** The Earnings Whisper number (the market's real expectation, distinct from Wall Street consensus) is a more reliable predictor of post-earnings stock moves than the consensus estimate. Since 1998, stocks that beat the whisper number closed higher 60% of the time with an average +1.8% gain. Critically, stocks that beat consensus but MISS the whisper number declined 55% of the time (avg -0.3%). The whisper number has been closer to actual EPS than consensus 70% of the time. This creates a systematic edge: trade the whisper, not the consensus.

**Research basis:**
- EarningsWhispers.com historical data (since 1998): beat whisper = +1.8% avg, 60% hit rate
- Beat consensus but miss whisper = -0.3% avg, down 55% of time
- Whisper number closer to actual earnings than consensus 70% of the time
- Goldman Sachs research: only 56% of earnings straddles profit (avg profit 2%), so directional trades off whispers outperform straddles

**Strategy variants:**

### Variant A: Pre-Earnings Directional (Whisper Beat Expected)
- **Setup:** Stock has whisper number ABOVE consensus AND positive Earnings Whisper Score
- **Entry:** Buy shares or OTM call (2-3 weeks to expiry) 1-2 days before earnings
- **Exit:** Sell within first 30 min of post-earnings trading
- **Stop:** Pre-define max loss at option premium paid

### Variant B: Whisper Miss Fade (Consensus Beat, Whisper Miss)
- **Setup:** Company likely to beat consensus but whisper number is materially higher than consensus (gap >5%)
- **Entry:** Buy puts or short shares on the day of earnings release, after confirmation of whisper miss
- **Exit:** Hold 1-3 days for post-earnings drift continuation
- **Stop:** If stock rises >2% above earnings-day close

### Variant C: Post-Earnings Announcement Drift (PEAD)
- **Setup:** Stock beats whisper AND has low analyst coverage (<5 analysts) or is small/mid-cap
- **Entry:** Buy on day after earnings if stock gaps up
- **Exit:** Hold 20-60 trading days (PEAD persists longest in low-coverage names)
- **Key research:** PEAD largely disappeared from large-caps by 2006 but persists in small-caps with low analyst coverage

**Data sources:** earningswhispers.com ($5/mo), thewhispernumber.com (free).

**Expected horizon:** 1 day (Variant A), 1-3 days (Variant B), 20-60 days (Variant C).

---

## Hypothesis 3: Stock Split Announcement Anticipation & Post-Split Rally

**Thesis:** Stock splits remain a reliable short-term catalyst. Companies that announce splits are typically strong performers with confident management -- the announcement itself signals management belief in continued appreciation. The strategy is to identify high-probability split candidates BEFORE announcements and hold through the post-announcement pop. Booking Holdings (BKNG) just completed a historic 25-for-1 split on April 2, 2026, creating fresh market attention on "who's next."

**Research basis:**
- Stock split announcements historically produce 2-5% short-term pops
- Booking Holdings 25-for-1 split executed April 2, 2026 (from ~$4,117 to ~$165)
- Companies split to improve retail accessibility -- typically at $500-$2000+ price points
- Strongest candidates: high price, no prior split history, strong growth, management incentive

**Specific tickers (split candidates for 2026):**
| Ticker | Company | Share Price (approx) | Split Likelihood | Notes |
|--------|---------|---------------------|-----------------|-------|
| MELI | MercadoLibre | ~$1,960 | HIGH | Never split since 2007 IPO. Highest-priced major growth stock without split history. Revenue up 39% YoY. Analyst consensus PT $2,733 (strong buy). 10-for-1 or 20-for-1 likely. |
| COST | Costco | ~$1,000+ | MODERATE-HIGH | Once a company crosses $1,000, it lands on split radar. Up 130% over 5 years. Last split was 2000. |
| AZO | AutoZone | ~$3,500+ | MODERATE | Perennially high price, never split since 1994. Management historically resistant but peer pressure mounting post-BKNG. |
| META | Meta Platforms | ~$650-700 | MODERATE | Never split. Approaching $700/share. Would generate massive retail interest. |

**Entry/exit logic:**
- **Entry (anticipation):** Buy shares in MELI, COST as core holdings now. These are quality companies regardless of split.
- **Entry (announcement pop):** If a split is announced, momentum traders pile in for 2-4 weeks. Buy on announcement day if you don't already own.
- **Exit:** Sell 50% of position on split execution date (the news becomes "sell the event"). Hold remainder as long-term position.
- **Stop:** Standard 8-10% trailing stop. A split thesis failure (no announcement) doesn't invalidate the quality thesis.
- **Key risk:** Split candidates remain speculative. Buy only companies you'd own regardless of split.

**Expected horizon:** 1-6 months (waiting for announcement); 2-4 weeks (post-announcement momentum).

---

## Hypothesis 4: Corporate Buyback Announcement Alpha

**Thesis:** Companies announcing large buyback programs outperform peers. Research shows +1.4% abnormal return on announcement day, +12.1% excess return over 4 years (up to 23.6% controlling for size/value), and the S&P 500 Buyback Index has outperformed the S&P 500 by 3x since 2000 (1,000% vs 310% total return). The signal is strongest when: (a) buyback is large relative to market cap (>3%), (b) company is undervalued (high book-to-market), and (c) an accelerated share repurchase (ASR) is included (signals urgency). S&P 500 companies spent ~$1 trillion on buybacks in 2025.

**Research basis:**
- Announcement abnormal return: +1.4% (event study, 882 OMR announcements)
- Long-term outperformance: +12.1% over 4 years (broad), +23.6% size/BM-adjusted, +45.3% for undervaluation-motivated buybacks
- S&P 500 Buyback Index: +1,000% since 2000 vs S&P 500 +310%
- Post-2002 weakening: 2002-2006 subsample showed only +2.35% 3-year BHAR (not significant) -- quality filtering is essential
- MSCI: buyback gap between DM and EM is persistent contributor to DM outperformance

**Specific tickers (major 2026 buyback announcements):**
| Ticker | Company | Buyback Size | % of Mkt Cap | ASR? | Notes |
|--------|---------|-------------|-------------|------|-------|
| NOW | ServiceNow | $5B new + $1.4B remaining = $6.4B | ~6.1% | YES ($2B ASR) | Stock down 34-45% in early 2026. Wall Street says "buy now." Buyback at depressed levels = strong signal. |
| WDC | Western Digital | $4B new + $484M remaining = $4.5B | ~4.1% | No | Insiders also buying (cluster signal). Strong 2025 run, adding buyback firepower. |
| PEP | PepsiCo | $10B new program | ~4.3% | No | Up 19% in 2026 already. Turnaround narrative. Classic defensive + buyback combo. |
| AAPL | Apple | $100B (largest in US history) | ~3% | Ongoing | Perennial buyback king. $23.6B in Q1 FY2025 alone. |
| GOOG | Alphabet | $70B program | ~3.5% | No | Consistent $70B annual authorization. |
| META | Meta | $50B expansion ($80B total auth) | ~5% | No | Already spent $8B in Q3 2025 alone. Aggressive capital return. |

**Entry/exit logic:**
- **Primary strategy (announcement chase):** Buy within 1-2 days of new buyback announcement. Best edge: buyback >3% of market cap AND stock is below 52-week high (undervaluation signal).
- **Quality filter (critical):** Only buy if company has: (a) positive free cash flow, (b) low debt/equity, (c) not using debt to fund buybacks. Avoid companies buying back stock while issuing shares (net issuance positive = fake buyback).
- **Best current setup:** NOW -- stock down 45%, $6.4B buyback (6.1% of cap), includes $2B ASR, Wall Street consensus "buy." This is textbook: large buyback + depressed stock + accelerated execution.
- **Exit:** Hold 6-12 months. The buyback provides ongoing price support as company executes purchases.
- **Stop:** 15% below entry (companies rarely announce large buybacks and then see persistent declines unless fundamentals deteriorate).

**Expected horizon:** 1-5 days (announcement pop), 6-12 months (buyback execution tailwind).

---

## Hypothesis 5: Insider Cluster Buying

**Thesis:** When 3+ corporate insiders (CEO, CFO, directors) buy stock in open-market transactions within a 30-60 day window, the stock outperforms the market by ~7% over the following year (Journal of Finance). Cluster buys dramatically reduce false positive rates vs. single-insider purchases. The signal is strongest when: (a) purchases are large relative to insider's existing holdings, (b) senior leadership (not just directors), (c) buying occurs near 52-week lows or after sharp declines, and (d) accompanied by a catalyst (spinoff, restructuring, turnaround).

**Research basis:**
- Journal of Finance: stocks with heavy insider buying outperform by ~7% over 12 months
- Cluster buys (3+ insiders) sharply increase hit rate
- Consumer staples spinoff insiders: average +112% return before completion
- Key: isolated insider purchases lack predictive value; coordinated buying demonstrates genuine conviction

**Specific tickers with recent cluster buying (Q1 2026):**
| Ticker | Company | Cluster Details | Price at Buy | Analyst PT | Implied Upside |
|--------|---------|----------------|-------------|-----------|---------------|
| LOAR | Loar Holdings | 3 insiders bought 98,800 shares ($6.46M) in March 2026 near 52-week low | ~$65-67 | $94.50 (median), $106.78 (high) | ~42-60% |
| AHCO | AdaptHealth | 3 insiders bought >$20M in shares in March 2026 | -- | $13.25 (consensus Buy) | Significant (50% Strong Buy, 50% Buy) |
| WEX | WEX Inc. | Multiple C-suite insiders bought in coordinated cluster | ~$149 | $165.09 (consensus) | ~11% |
| CEVA | CEVA Inc. | CEO + CFO + director all bought after Feb 17 earnings call (Feb 19-23) | ~$18-20 | $33.13 (consensus), $40 high | ~65-100% |
| NKE | Nike | Listed in Insider Monkey top 10 large-cap insider buys 2026 | -- | 60% bullish analyst ratings | Turnaround play |
| CHRW | C.H. Robinson | 4 insiders bought 3,042 shares ($501K) in Feb 2026 | ~$165 | -- | Transport/logistics value |
| PHIN | Phinia | Cluster of insider buys post-BorgWarner spinoff | -- | -- | Historical precedent: "stock doubled within months" |

**Entry/exit logic:**
- **Entry:** Buy within 5-10 trading days of identifying a cluster buy event (3+ insiders, within 60 days). Use OpenInsider.com or insider-monitor.com for real-time alerts.
- **Position sizing:** 2-4% of portfolio per position. Concentrate on highest-conviction clusters (CEO + CFO involved, large purchase size relative to compensation).
- **Best current setups:**
  - **LOAR:** 3 insiders, $6.46M total, near 52-week low, 42-60% upside to analyst targets. Goldman Sachs has Buy rating with $98 PT.
  - **CEVA:** CEO + CFO + director all buying immediately after earnings call. Consensus PT implies 65-100% upside. Small-cap semiconductor with high insider ownership.
  - **AHCO:** $20M+ in insider buys is unusually large. All-buy analyst consensus. Healthcare services turnaround.
- **Exit:** Hold 6-12 months (aligned with the research showing 7% annual outperformance). Take partial profits at analyst consensus PT.
- **Stop:** 15-20% below insider purchase price (if insiders are wrong, cut losses). Re-evaluate if a second cluster of SELLING appears.
- **Key filter:** Ignore director-only buys of <$100K. Focus on operational insiders (CEO, CFO, COO) making purchases >$500K.

**Data sources:** OpenInsider.com (free, real-time), insider-monitor.com (cluster alerts), InsiderFinance.io, SEC EDGAR Form 4 filings.

**Expected horizon:** 6-12 months.

---

## Summary: Priority Ranking

| Rank | Hypothesis | Edge Quality | Ease of Execution | Best Ticker Now |
|------|-----------|-------------|-------------------|----------------|
| 1 | Insider Cluster Buying | HIGH (academic + practitioner evidence) | EASY (free data, clear signals) | LOAR, CEVA, AHCO |
| 2 | Buyback Announcement Alpha | HIGH (deep academic evidence, S&P Buyback Index track record) | EASY (public announcements) | NOW, WDC, PEP |
| 3 | IPO Lockup Expiration Short | MODERATE-HIGH (consistent research, recent examples) | MODERATE (need lockup calendar, short selling or puts) | FIG (June/Aug 2026 releases) |
| 4 | Stock Split Anticipation | MODERATE (speculative until announced) | EASY (buy quality stocks at high prices) | MELI, COST |
| 5 | Earnings Whisper Trading | MODERATE (good data, but IV crush risk on options) | MODERATE (requires whisper data subscription, fast execution) | Check earningswhispers.com weekly |

---

## Sources

- [Earnings Whispers](https://www.earningswhispers.com/)
- [The Whisper Number](https://thewhispernumber.com/)
- [OpenInsider - Latest Cluster Buys](http://openinsider.com/latest-cluster-buys)
- [Insider Monkey - 10 Large-Cap Stocks with Insider Buying 2026](https://www.insidermonkey.com/blog/10-large-cap-stocks-with-insider-buying-in-2026-1728256/)
- [Follow The Money: Insider Clusters (Yahoo Finance)](https://finance.yahoo.com/news/money-insider-clusters-signal-conviction-204011459.html)
- [3 Massive Buybacks That Map the Market's Mood in 2026 (Yahoo Finance)](https://finance.yahoo.com/news/3-massive-buybacks-map-market-183800713.html)
- [5 Stocks Using Buybacks to Drive Serious Upside Into 2026 (Yahoo Finance)](https://finance.yahoo.com/news/5-stocks-using-buybacks-drive-222700328.html)
- [MSCI: Every Share Counts - Impact of Buybacks on Markets](https://www.msci.com/research-and-insights/blog-post/every-share-counts-the-impact-of-buybacks-on-markets)
- [S&P Capital IQ: Buying Outperformance - Share Repurchase Announcements](https://www.spglobal.com/content/dam/spglobal/mi/en/documents/general/Buying_Outperformance_Do_Share_Repurchase_Announcements_Lead_to_Higher_Returns.pdf)
- [Figma IPO Collapse (InvestorPlace)](https://investorplace.com/dailylive/2026/02/why-figma-stock-crashed-81-the-ipo-mechanics-retail-never-saw-coming-2/)
- [StubHub Plunges Amid Lockup Expiration (Sportico)](https://www.sportico.com/business/finance/2026/stubhub-stock-plunges-q4-earnings-lockup-expiration-1234886442/)
- [Klarna Lock-Up Expiration Mechanics](https://investors.klarna.com/News--Events/news/news-details/2026/Klarna-Group-Plc-clarifies-mechanics-of-March-9-lock-up-expiration-2026-fmB3oS8vW-/default.aspx)
- [Beaten Down IPOs Face Negative Feedback Loop (Bloomberg)](https://www.bloomberg.com/news/articles/2026-03-09/beaten-down-ipos-face-negative-feedback-loop-after-lock-ups)
- [Stock Split Candidates 2026 (24/7 Wall St)](https://247wallst.com/investing/2025/12/31/these-are-the-3-stock-split-candidates-heading-into-2026/)
- [5 Stock Splits That Could Happen in 2026 (Nasdaq)](https://www.nasdaq.com/articles/5-stock-splits-could-happen-2026)
- [After Booking Stock Split, Who's Next? (24/7 Wall St)](https://247wallst.com/investing/2026/02/20/after-historic-booking-stock-split-whos-next/)
- [Booking Holdings 25-for-1 Split (StockTitan)](https://www.stocktitan.net/sec-filings/BKNG/8-k-booking-holdings-inc-reports-material-event-e738c601b9d7.html)
- [ServiceNow $5B Buyback (Investor Relations)](https://investor.servicenow.com/news/news-details/2026/ServiceNow-Reports-Fourth-Quarter-and-Full-Year-2025-Financial-Results-Board-of-Directors-Authorizes-Additional-5B-for-Share-Repurchase-Program/default.aspx)
- [ServiceNow Has Fallen 45%, Wall Street Says Buy Now (24/7 Wall St)](https://247wallst.com/investing/2026/04/01/servicenow-has-fallen-45-wall-street-says-buy-now/)
- [Western Digital $4B Buyback (WD Newsroom)](https://www.westerndigital.com/company/newsroom/press-releases/2026/2026-02-03-western-digital-authorizes-additional-4billion-dollars-of-share-repurchases)
- [Loar Holdings Insider Cluster Buying (HoldingsChannel)](https://www.holdingschannel.com/article/202603/loar-holdings-insider-cluster-buying-signals-confidence-after-recent-LOAR03172026cluster.htm/)
- [CEVA Insider Cluster Buying (Fintool)](https://fintool.com/news/ceva-insider-cluster-buying)
- [AdaptHealth Insider Cluster Buying (HoldingsChannel)](https://www.holdingschannel.com/article/202603/insider-cluster-buying-at-adapthealth-signals-confidence-in-ahco-shares-AHCO03162026cluster.htm/)
- [WEX Insider Buying Cluster (Yahoo Finance)](https://finance.yahoo.com/news/wex-insider-buying-cluster-highlights-101146160.html)
- [MarketBeat IPO Lockup Expirations](https://www.marketbeat.com/ipos/lockup-expirations/)
- [IPO Lockup Research (SMU)](https://ink.library.smu.edu.sg/context/etd_coll/article/1521/viewcontent/IPO_performance_and_trading_around_lock_up_expiration.pdf)
- [Post-Earnings Announcement Drift (Quantpedia)](https://quantpedia.com/strategies/post-earnings-announcement-effect/)
- [Options Strategies for Earnings Season 2026 (OptionStrading.org)](https://www.optionstrading.org/blog/options-strategies-earnings-season/)

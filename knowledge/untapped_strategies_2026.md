# Untapped Trading Strategies 2026 -- New Angles

Research date: April 6, 2026. Web-sourced, not yet backtested.

---

## 1. Pairs Trading -- Cointegrated Pairs (Statistical Arbitrage)

**Classic pairs (Engle-Granger confirmed historically):**
- XOM/CVX (energy majors, correlation >0.92)
- KO/PEP (consumer staples, >30yr cointegration)
- EWA/EWC (Australia/Canada commodity ETFs)
- SPY/IVV (identical index, micro-arb)
- XLF/XLU (counter-cyclical sector pair for regime shifts)
- GOOGL/META, V/MA, GS/MS, HD/LOW

**ETF pairs (2025 Springer research, 30 pairs tested 2000-2024):**
- Lowering z-score threshold from 2.0 to 1.5 increased Sharpe but raised drawdowns.
- Portfolio of 45 pairs: 15% annualized return, Sharpe 1.43 (after costs).

**Rules:** Enter when z-score of spread > 2.0 (or 1.5 aggressive). Exit at z-score 0. Stop at z-score 3.5. Re-test cointegration quarterly (Johansen test preferred over Engle-Granger). Holding period: 5-20 trading days. Historical win rate: ~60-65% per trade.

**NEW vs existing:** Our pairs_trading_research.md already covers these tickers. The new angle is the ETF-based approach (EWA/EWC, XLF/XLU) and the z-score threshold research.

---

## 2. Tax-Loss Harvesting / January Effect Rebound

**Concept:** Stocks hammered by December tax-loss selling rebound in January as selling pressure ends and the 30-day wash-sale window expires.

**2025-2026 specific tickers beaten down in Dec 2025:**
- NCNO (nCino) -- sold off, expected rebound
- GLBE (Global-e Online) -- sold off, expected rebound
- GTLB (GitLab) -- sold off, expected rebound
- IOT (Samsara) -- sold off, expected rebound
- TTD (The Trade Desk) -- down 70% YTD in 2025
- NKE (Nike) -- down 39% in 2025
- FI (Fiserv) -- down 66% in 2025
- FRSH (Freshworks), CERT (Certara) -- tax-loss recovery plays

**Rules:** Buy first week of January. Hold 4-8 weeks (through wash-sale window expiry). Target small/mid caps with >30% prior-year decline and no fundamental deterioration. Historical January effect: small caps outperform large caps by 1-5% in January (Quantified Strategies backtest).

**Win rate:** January effect has worked in ~65-70% of years historically, but weakening as more capital exploits it.

**Timing for 2026:** This window has passed (we are in April). Queue for December 2026 screening.

---

## 3. Dividend Capture Strategy

**Concept:** Buy before ex-dividend date, collect dividend, sell on/after ex-date.

**High-yield targets for capture (current as of April 2026):**
- AGNC -- 15.34% yield, $0.12/month, ex-div ~end of month, pay ~10th of next month
- O (Realty Income) -- 5.3% yield, monthly payer, 134th consecutive increase
- MAIN (Main Street Capital) -- ~6-7% yield, monthly payer
- MO (Altria) -- ~8% yield, quarterly
- T (AT&T) -- ~5% yield, quarterly

**Rules:** Buy 2-3 days before ex-date. Sell on ex-date or day after. Use 5-EMA/15-EMA crossover + RSI for timing. Stop-loss at 2%. Position size: max 1% account risk per trade. Holding period: 1-5 days.

**Critical warning:** Stock typically drops by ~dividend amount on ex-date. Net profit per trade is small. Dividends held <61 days taxed as ordinary income. Transaction costs can eat profits. Historical win rate on pure capture: ~50-55% (barely profitable after costs).

**Better variant:** Combine with technical oversold bounce -- only capture dividends on stocks that are also RSI <30 near ex-date.

---

## 4. Merger Arbitrage -- Current Deals (April 2026)

**Active deals with spreads:**

| Target | Acquirer | Deal Price | Spread | Expected Close |
|--------|----------|-----------|--------|---------------|
| WBD (Warner Bros Discovery) | PARA (Paramount Skydance) | $31.00/share cash | ~14% ($3.86/share) | Q3 2026 (Sept 30) |
| CNTA (Centessa Pharma) | LLY (Eli Lilly) | $38.00 + up to $9 CVR | Small (stock near $40) | Q3 2026 |
| NSC (Norfolk Southern) | UNP (Union Pacific) | ~$85B total deal | Wide (regulatory risk) | 2027+ (filed April 30) |

**WBD detail:** Shareholder vote April 23, 2026. Ticking fee of $0.25/share/quarter if not closed by Sept 30. Bloomberg called the spread "mispriced" on March 27. Annualized return ~25% if closed on time.

**Rules:** Buy target stock at current price, collect spread to deal price at close. For stock deals, hedge by shorting acquirer in correct ratio. Size positions based on deal-break probability (WBD: moderate regulatory risk, ~75-80% implied probability). Stop: exit if deal breaks. Holding period: weeks to months.

**Historical win rate for announced deals:** ~85-90% close successfully. Annualized returns: 5-15% (higher for riskier deals).

**ETF alternative:** MNA (IQ Merger Arbitrage ETF), MRGR, ARBR -- diversified merger arb exposure.

---

## 5. Closed-End Fund (CEF) Discount to NAV

**Concept:** Buy CEFs trading at deep discounts to NAV. Profit from discount narrowing + distribution yield.

**Current opportunities (April 2026):**
- HQH (Tekla Healthcare Investors) -- >9% discount, 15%+ distribution
- TYG (Tortoise Energy Infrastructure) -- 7.15% discount
- ADX (Adams Diversified Equity) -- 6.6% discount, oldest NYSE-listed
- GDL (GDL Fund) -- persistent discount since 2007 (value trap warning)
- BST (BlackRock Science & Technology Trust) -- historically trades discount/premium

**Rules:** Buy when discount exceeds 3-year average discount by >1 standard deviation. Sell when discount narrows to average or flips to premium. Prioritize CEFs with activist pressure, tender offers, or conversion catalysts. Avoid "perma-discount" funds (GDL-type). Holding period: 3-12 months.

**Yield kicker:** An 8% NAV distribution = 10% yield when bought at 20% discount.

**Screening tools:** CEFData.com, CEFA.com premium/discount reports, CEF Channel screener.

**Historical alpha:** Academic studies show buying deepest-discount quintile and selling premium quintile generates 4-6% annual alpha. Win rate: ~60% when using mean-reversion of discount.

---

## 6. Biotech PDUFA Binary Events

**Concept:** Trade binary FDA approval/rejection decisions on known dates.

**April 2026 PDUFA calendar (confirmed):**
- NVS (Novartis) -- KESIMPTA supplement, April 1 -- MS indication (low risk, supplement)
- RCKT (Rocket Pharma) -- RP-L201, April 2 -- LAD-I gene therapy (high risk/reward)
- DNLI (Denali Therapeutics) -- Tivi, April 5 -- neurological disorder
- CORT (Corcept Therapeutics) -- CORT118335, April 9 -- Alzheimer's psychosis
- ROIV (Roivant Sciences) -- RVT-2001, April 9 -- Alzheimer's disease
- BMRN (BioMarin Pharma) -- NDA, April 1 -- unspecified
- LLY (Eli Lilly) -- Orforglipron, April 2026 -- obesity (blockbuster potential)

**Volume of catalysts:** April has 152 PDUFA events, May 133, June 193, July 129.

**Rules:** For long-only: buy 2-5 days before PDUFA if Phase 3 data was strong. For hedged: buy stock + put (defined risk). For pure volatility: buy straddle 1-2 weeks before PDUFA, sell on decision day. Position size: max 2% of portfolio per binary event. Never hold >3 PDUFA bets simultaneously.

**Historical stats:** Approval rates vary by indication (~70-85% for drugs with strong Phase 3). Approved drugs average +10-30% pop. Rejected drugs average -30-60% drop. Straddle strategy win rate: ~55% (IV expansion priced in).

**Screening:** biopharmcatalyst.com, catalystalert.io, fdatracker.com for live calendars.

---

## Priority Ranking for Implementation

1. **Merger Arb (WBD)** -- Highest conviction, 14% spread, known timeline, April 23 vote imminent
2. **CEF Discount** -- Steady alpha, lower risk, screener-friendly, combinable with yield
3. **Biotech PDUFA** -- High reward but need per-event research; LLY/Orforglipron is the big one
4. **Pairs Trading ETFs** -- Extend existing infra with EWA/EWC, XLF/XLU pairs
5. **January Effect** -- Queue for December 2026 (window passed)
6. **Dividend Capture** -- Marginal after costs; only worthwhile combined with oversold bounce

---

Sources:
- [Springer: Cointegration-based pairs trading with ETFs](https://link.springer.com/article/10.1057/s41260-025-00416-0)
- [Quantified Strategies: January Effect Backtest](https://www.quantifiedstrategies.com/january-effect-in-stocks/)
- [Yahoo Finance: January Effect 2026 Beaten-Down Stocks](https://finance.yahoo.com/news/january-effect-2026-4-beaten-165700495.html)
- [AInvest: January Snap-Back Tax-Loss Recovery Plays 2026](https://www.ainvest.com/news/january-snap-tax-loss-recovery-plays-2026-2512/)
- [AlphaExCapital: Ex-Dividend Date Strategy](https://www.alphaexcapital.com/stocks/stock-investing-strategies/free-cash-flow-and-dividends/ex-dividend-date-strategy/)
- [Dividend.com: Dividend Capture Guide](https://www.dividend.com/dividend-education/dividend-capture-strategy-the-best-guide-on-the-web/)
- [AGNC Dividend Data](https://www.marketbeat.com/stocks/NASDAQ/AGNC/dividend/)
- [AllianceBernstein: Merger Arbitrage Riding the Wave into 2026](https://www.alliancebernstein.com/americas/en/institutions/insights/investment-insights/merger-arbitrage-riding-the-wave-into-2026.html)
- [Bloomberg: Mispriced WBD Deal Spread](https://www.bloomberg.com/news/articles/2026-03-27/-mispriced-warner-bros-deal-spread-creates-windfall-potential)
- [WBD Shareholder Vote Date](https://www.prnewswire.com/news-releases/warner-bros-discovery-sets-shareholder-meeting-date-of-april-23-2026-to-approve-transaction-with-paramount-skydance-302726244.html)
- [Paramount $81B Bid for WBD](https://www.hedgeco.net/news/04/2026/paramounts-81-billion-bid-for-warner-bros-signals-a-new-era-for-event-driven-investing.html)
- [LLY-CNTA Acquisition](https://investor.lilly.com/news-releases/news-release-details/lilly-acquire-centessa-pharmaceuticals-advance-treatments-sleep)
- [UNP-NSC Merger Application](https://www.axios.com/pro/supply-chain-deals/2026/02/18/union-pacific-norfolk-southern-revised-merger-application-april)
- [Fidelity: CEF Discounts and Premiums](https://www.fidelity.com/learning-center/investment-products/closed-end-funds/discounts-and-premiums)
- [Sure Dividend: 2026 CEF List](https://www.suredividend.com/closed-end-funds-list/)
- [CatalystAlert: April 2026 PDUFA](https://catalystalert.io/pdufa/april-2026)
- [BioPharmCatalyst: FDA Calendar](https://www.biopharmcatalyst.com/calendars/fda-calendar)
- [InsideArbitrage: Merger Arbitrage Tool](https://www.insidearbitrage.com/merger-arbitrage/)
- [Seeking Alpha: Tax-Loss Harvesting Stocks](https://seekingalpha.com/article/4853516-tax-loss-harvesting-selling-downgraded-stocks-before-2026)
- [Trade Ideas: 5 Tax-Loss Harvesting Trades](https://www.trade-ideas.com/2025/12/26/reset-your-portfolio-with-tax-loss-harvesting-the-5-trades-to-make-before-january-1st/)

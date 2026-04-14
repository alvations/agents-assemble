# Paper Trading Log

**Started:** 2026-04-14
**Account:** Public.com Brokerage (5LO16569)
**Mode:** Paper / Dry Run (no live trades until user approves)

## Account Snapshot (2026-04-14)

| Item | Value |
|------|-------|
| HESAY | 9 shares @ $207.10 = $1,863.90 (PROTECTED) |
| Cash | $841.60 |
| Jiko T-bill | $1,240.70 (OFF LIMITS) |
| Buying power | $841.60 |
| Total | ~$3,946 |

## Rules
- NEVER sell HESAY
- NEVER touch yield/T-bill account
- NEVER transfer funds (user does it)
- Paper trade only until user approves live
- $5,000 additional funding expected ~2026-04-21

## Daily Paper Trades

### 2026-04-14 (Day 1)

**Pre-market research:** Iran deal talks, S&P reversal to 6886, VIX 18, JPM earnings miss

**Opportunities scored:**
| Symbol | Score | Thesis | Action |
|--------|-------|--------|--------|
| JPM | 72 | Bank earnings (missed, but sector watch) | WAIT — need WFC/C + PPI first |
| TSM | 72 | TSMC Thursday earnings, revenue $35.7B known | WATCH — enter after earnings if guidance strong |
| KOSPI | 69 | Korean semis +2.74%, export surge | NO — can't trade KOSPI directly |
| WFC | 67 | Bank earnings today | WAIT — earnings not out yet |
| EPD/ET/WMB | 61 | Energy midstream, elevated post-war | WATCH — thesis weakening as Iran deal talks |

**Paper trades placed:** NONE
**Reason:** Buying power $841.60 too small for proper positions. Waiting for $5K funding.
**Paper P&L:** $0.00

---


## Selected Strategies for Paper Trading

**Portfolio: $5,841.60 ($841.60 now + $5,000 incoming)**
**Style: Wait for triggers, don't chase. Most days = 0 trades.**

### Strategy Picks (5 strategies, diverse themes)

| # | Strategy | Comp | Con | Theme | Entry Trigger |
|---|----------|------|-----|-------|--------------|
| 1 | **core_satellite** | 0.61 | 89% | Broad market + alpha | SPY above SMA50 + satellite names (AVGO, LLY, AMZN) showing momentum |
| 2 | **momentum** | 0.45 | 96% | Classic factor | Buy top RSI names above SMA50, cut below SMA50 |
| 3 | **uranium_renaissance** | 0.48 | 71% | Structural supply deficit | CCJ/URA above SMA50, nuclear sentiment positive |
| 4 | **gross_profitability_value** | 0.64 HODL | 96% | Quality boring compounders | V/MA/COST/MCD below fair value (RSI < 50) |
| 5 | **drawdown_severity_rotation** | 0.17 | 79% | Regime hedge | Shifts SPY→GLD→TLT→SHY based on drawdown depth |

### Allocation Plan (when $5K arrives)

| Strategy | Allocation | $ Amount | Max Positions |
|----------|-----------|----------|--------------|
| core_satellite | 25% | $1,460 | 3-4 tickers |
| momentum | 20% | $1,168 | 2-3 tickers |
| uranium_renaissance | 15% | $876 | 2 tickers |
| gross_profitability_value | 15% | $876 | 2 tickers |
| drawdown_severity_rotation | 10% | $584 | 1-2 tickers |
| **Cash reserve** | **15%** | **$876** | For opportunistic |

### Entry Rules (WAIT for these, don't force)

**core_satellite:** Enter when SPY is above SMA50 AND at least 2 satellite names (AVGO, LLY, AMZN, MSFT) show RSI > 50 + above SMA50. Current status: CHECK DAILY.

**momentum:** Enter the 2-3 names with highest 3-month momentum that are above SMA50. Recheck weekly. Cut any name that drops below SMA50.

**uranium_renaissance:** Enter CCJ + URA when both above SMA50. Thesis: nuclear demand is structural (AI data centers need baseload power). NOT affected by Iran deal.

**gross_profitability_value:** Enter V + COST (or MA + MCD) on pullbacks. Wait for RSI < 45 on any of them. These are buy-the-dip quality names.

**drawdown_severity_rotation:** Always on. Start with SPY/QQQ heavy (normal regime, VIX 18). Auto-shifts to GLD/TLT if drawdown deepens.

### Daily Tracking Format

Each day I will log:
1. Strategy triggers checked (fired / not fired)
2. Paper entries/exits with prices and reasons
3. Paper P&L (running total)
4. End-of-week summary every Friday


### Why These 5 Strategies (Selection Rationale)

**1. core_satellite (25% allocation)**
*What it does:* Holds a core index position (SPY) for broad market exposure, plus "satellite" high-conviction picks (AVGO, LLY, AMZN, MSFT) for alpha. GLD and XLE for diversification.
*Why picked:* #1 ranked standalone strategy (0.61 composite). The core SPY position means we're never fully out of the market. Satellites add upside without betting the farm. 89% consistency across 28 windows — it works in most regimes.
*Entry trigger:* SPY above SMA50 (bull regime confirmed) + at least 2 satellites showing momentum (RSI > 50, above SMA50).
*Risk:* If broad market corrects, SPY drags the portfolio. Mitigated by GLD allocation within the strategy.

**2. momentum (20% allocation)**
*What it does:* Buys the stocks with strongest recent price momentum (3-6 month returns). Cuts losers fast (below SMA50 = exit). Classic academic factor with decades of evidence.
*Why picked:* 96% consistency — positive Sharpe in 27 of 28 windows. Works in almost every market environment except sharp reversals. Current regime (tech rally, VIX 18) is ideal for momentum.
*Entry trigger:* Buy top 2-3 names by 3-month return that are above SMA50. Currently: NVDA, AVGO, META, CRM are candidates. Rebalance weekly.
*Risk:* Momentum crashes (sudden reversal like Mar 2020). This is why we have drawdown_severity_rotation as a hedge.

**3. uranium_renaissance (15% allocation)**
*What it does:* Holds uranium miners and nuclear energy companies (CCJ, URA, LEU, UUUU, OKLO). Thesis: structural uranium supply deficit — mines take 10+ years to build, demand surging from AI data centers needing 24/7 nuclear baseload power.
*Why picked:* Completely uncorrelated to tech/AI. Our other picks are tech-heavy, so uranium provides genuine diversification. The thesis is structural (not cyclical) — Iran deal doesn't affect nuclear power demand. 71% consistency is our lowest, but HODL composite 0.42 is strong.
*Entry trigger:* CCJ and URA both above SMA50. Nuclear sentiment positive (check for new reactor announcements, utility contracts).
*Risk:* Uranium price can be volatile. Small-cap miners (DNN, UEC) are especially volatile. Mitigated by sticking to CCJ + URA (larger, more liquid).

**4. gross_profitability_value (15% allocation)**
*What it does:* Buys companies with the highest gross profit margins relative to their assets — the Novy-Marx quality factor. Universe: V, MA, COST, MCD, SBUX, YUM, AAPL. These are boring, cash-generative monopolies.
*Why picked:* 96% consistency AND 0.64 HODL composite — the best "boring compounder" in our platform. These companies grow earnings through recessions. Visa and Mastercard are literal toll booths on every transaction. McDonald's and Costco have pricing power. Academic evidence for this factor spans 30+ years across 17 countries.
*Entry trigger:* Buy on pullbacks — wait for RSI < 45 on V, MA, COST, or MCD. Don't chase all-time highs.
*Risk:* These are expensive stocks (high P/E). If rates spike, multiples compress. But earnings power is real, so drawdowns recover.

**5. drawdown_severity_rotation (10% allocation)**
*What it does:* Shifts between SPY/QQQ (equities), TLT (bonds), GLD (gold), and SHY (cash) based on how deep the S&P 500 drawdown is from its 52-week high. Normal market = 80% equities. Drawdown 10-20% = shift to gold/bonds. Drawdown > 20% = mostly gold/cash.
*Why picked:* This is our HEDGE. If the market crashes, this strategy automatically rotates to safety. We need this because our other 4 picks are equity-heavy. In the 3Y backtest, max drawdown was only -8.2% while the market fell -30%. It won't make us rich, but it protects capital.
*Entry trigger:* Always on. Currently in "normal" mode (SPY/QQQ heavy, VIX 18, no drawdown). Will auto-shift if conditions deteriorate.
*Risk:* In a slow grind-down (no sharp crash), the rotation may be too slow. Also, bonds and equities can fall together (like 2022). GLD is the true safe haven here.


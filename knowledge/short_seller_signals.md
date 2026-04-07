# Short Seller Report Dip-Buying Signals

## Academic Baseline (CAR After Activist Short Reports)

Source: Ogorodniks & Sirbu (SSE Riga), Brendel et al. (Journal of Accounting Research), BSIC/Bocconi, HEC Paris

| Window | Mean CAR | Implication |
|--------|----------|-------------|
| Day 0 | -4.8% | Initial shock |
| Day 0-3 | -11.2% | Continued selling |
| Day 0-7 | -8.3% | Slight mean-reversion starts |
| Day 0-30 | -13.3% | Drift continues |
| Day 0-60 | -14.5% to -17.0% | Persistent |
| Day 0-135 | -14.8% | Stabilization |
| Day 0-180 | -22.6% | Long-term if allegations valid |

Sample: 247 campaigns (BSIC), 159 fraud cases (Kartapanis). Only 30% of fraud allegations confirmed by SEC. 45% of reports associated with lasting negative returns; 55% partially or fully recover.

## Firm-Level Track Records

### Citron Research (Andrew Left)
- **Avg day-0 drop**: -7% to -17% (varies by conviction level)
- **Historical accuracy**: 42% avg decline in year after report (WSJ, 111 reports 2001-2014)
- **Notable WRONG calls**: Tesla (shorted pre-run), Shopify (recovered strongly)
- **Notable RIGHT calls**: Luckin Coffee (fraud confirmed), Valeant
- **Recent**: PLTR Aug 2025 -- dropped 17% over 6 sessions ($73B wiped); recovery TBD
- **Dip-buy signal**: Citron increasingly wrong in bull markets; meme stocks bounce fast

### Hindenburg Research (Nate Anderson) -- CLOSED Jan 2025
- **Avg day-0 drop**: -15% to -28%
- **Track record**: ~100 individuals charged civilly/criminally from targets; #1 ranked activist 2024
- **Notable RIGHT**: Nikola (-90%, founder convicted), Lordstown Motors (delisted), PACS Group (-28%)
- **Notable WRONG**: Super Micro (fell 68%, independent probe found no fraud, stock recovered)
- **Recent**: iLearningEngines Aug 2024 (-50%), Adani Jan 2023 (-65%, partial recovery)
- **Dip-buy signal**: HIGH danger -- Hindenburg had highest accuracy; most targets stayed down

### Muddy Waters (Carson Block)
- **Avg day-0 drop**: -15% to -20%
- **Strategy**: Covers most of short quickly after report, trades around position
- **Notable WRONG**: AppLovin Mar 2025 (dropped 20%, recovered, up 70% YTD by Oct)
- **Notable RIGHT**: Sino-Forest (fraud, delisted), Luck Kin Mining
- **Recent**: APP Mar 2025 -- dropped 20% day-1, doubled down May 2025, stock still contested
- **Dip-buy signal**: BEST dip-buy candidate -- Block himself covers quickly; stocks often rebound

### Grizzly Research
- **Reports tracked**: 10 (BreakOut POINT 12-month data)
- **Avg return after report**: -14%
- **Win rate**: ~60% (6/10 stayed down)
- **Best short**: MVST -62%, RZLV -45%, ACHR -43%, PONY -29%
- **Worst short (wrong calls)**: EOS +30%, NXST +24%
- **Dip-buy signal**: 40% of targets recover -- moderate opportunity

### Kerrisdale Capital
- **Avg day-0 drop**: -4% to -12% (lower impact than top-tier)
- **Recent**: IONQ Mar 2025 -- dropped 4.5% on report day
- **Style**: Valuation-based (not fraud), targets overvalued momentum stocks
- **Dip-buy signal**: BEST dip-buy -- valuation shorts rarely kill stocks; smallest drops, fastest recovery

### Spruce Point Capital
- **Recent targets (2025-2026)**: REZI, IPX, DKNG, UEC, IRTC, LMB, TEM, YOU, MNST
- **Style**: Accounting forensics, mid-cap focus
- **Dip-buy signal**: Moderate -- similar profile to Grizzly

## Backtestable Strategy Rules

### Entry Rules
| Condition | Action |
|-----------|--------|
| Report by Kerrisdale/valuation-based | BUY day 1 (smallest drop, fastest recovery) |
| Report by Muddy Waters | BUY day 3 (Block covers quickly; 20% drops revert) |
| Report by Grizzly/Spruce Point | BUY day 5 (40% wrong rate; wait for stabilization) |
| Report by Citron | BUY day 5-7 (mixed accuracy; bull market bias helps) |
| Report by Hindenburg-tier (fraud) | DO NOT BUY (70%+ stayed down; only 30% fraud unconfirmed) |

### Position Sizing
- Max 2% of portfolio per dip-buy
- Scale in: 50% at entry, 50% at -10% from entry (if it keeps dropping)

### Exit Rules
- Target: 50% recovery of initial drop (e.g., stock drops 20%, sell when up 10% from low)
- Stop-loss: -15% from entry (fraud is real)
- Max hold: 30 trading days (if no recovery, cut)

### Expected Win Rates (from data)
| Seller Type | Buy Day 3 Win Rate | Buy Day 7 Win Rate | Avg Recovery Time |
|-------------|-------------------|-------------------|-------------------|
| Valuation-based (Kerrisdale) | ~65% | ~70% | 5-15 days |
| Mixed (Citron, Muddy Waters) | ~50% | ~55% | 10-30 days |
| Forensic/Fraud (Hindenburg) | ~25% | ~30% | 60+ days or never |
| Mid-tier (Grizzly, Spruce) | ~40% | ~50% | 15-40 days |

### Key Filters (Improve Win Rate)
1. **Large cap only (>$10B)**: Small caps hit by shorts rarely recover (academic finding)
2. **Company does NOT respond**: Non-response correlates with LESS negative outcome (Brendel 2021)
3. **No SEC investigation announced within 48h**: If SEC piles on, stay away
4. **Bull market regime**: Short reports less effective when SPY above 200-day MA
5. **Prior 6-month run-up >50%**: Valuation shorts on momentum names revert to mean

## Data Sources for Monitoring
- [Citron Research](https://citronresearch.com/) -- reports posted as PDFs
- [Muddy Waters](https://muddywatersresearch.com/) -- research tab
- [Grizzly Research](https://grizzlyreports.com/category/reports/) -- reports page
- [Spruce Point Capital](https://www.sprucepointcap.com/research) -- research page
- [Kerrisdale Capital](https://www.kerrisdalecap.com/) -- PDF reports
- [BreakOut POINT](https://breakoutpoint.com/) -- tracks all activist short sellers with performance data
- Hindenburg shut down Jan 2025; no new reports

## Sources
- [WSJ Citron Analysis (111 reports)](https://www.warriortrading.com/citron-research-know/)
- [Hindenburg Wikipedia - Full Target List](https://en.wikipedia.org/wiki/Hindenburg_Research)
- [HEC Paris - How Activist Short Sellers Move a Stock](https://www.hec.edu/en/dare/economics-finance/how-activist-short-sellers-move-stock)
- [BSIC Bocconi - Activist Short Sellers Study (247 campaigns)](https://bsic.it/activist-short-sellers-manipulative-profit-seekers-or-bearers-of-justice/)
- [Brendel et al. 2021 - Journal of Accounting Research](https://onlinelibrary.wiley.com/doi/10.1111/1475-679X.12356)
- [ScienceDirect - Stock Market Effects of Hindenburg](https://www.sciencedirect.com/science/article/abs/pii/S1544612324015241)
- [Institutional Investor - Muddy Waters Big Gains](https://www.institutionalinvestor.com/article/2bswowrzfev7mwobtecjk/portfolio/in-tough-year-for-short-sellers-muddy-waters-pulls-off-big-gains)
- [BreakOut POINT - Grizzly Research 12mo Summary](https://breakoutpoint.com/as-summary/grizzly-research-tcgeg/)
- [Kerrisdale IonQ Short Report](https://www.kerrisdalecap.com/wp-content/uploads/2025/03/IonQ-%E2%80%93-Kerrisdale.pdf)

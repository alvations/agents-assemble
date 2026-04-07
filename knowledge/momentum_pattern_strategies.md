# Momentum & Pattern Trading Strategies -- Codeable Rules

## 1. Minervini SEPA / VCP

**Performance:** 220% avg annual return over 5.5 years; 334.8% in 2021 US Investing Championship.

### Trend Template (all 8 must pass):
1. Price > 150-day MA AND Price > 200-day MA
2. 150-day MA > 200-day MA
3. 200-day MA slope positive for >= 1 month (prefer 4-5 months)
4. 50-day MA > 150-day MA AND 50-day MA > 200-day MA
5. Price > 50-day MA
6. Price >= 1.25 * 52-week low (at least 25% above)
7. Price >= 0.75 * 52-week high (within 25% of high)
8. RS rank >= 70 (prefer >= 90)

### VCP Entry:
- 2-4 contractions, each ~50% shallower than previous (e.g., 25% -> 12% -> 6%)
- Volume declines at each contraction low
- **Buy:** breakout above pivot (high of last contraction) on volume >= 1.5x 50-day avg volume
- **Stop:** 5-8% below entry (absolute max 10%)
- **Universe:** US stocks > $10, avg volume > 200K shares/day
- **Hold:** until 50-day MA break or trailing stop

---

## 2. O'Neil CAN SLIM

**Caveat:** Portfolio123 backtest of full screen over 15 years showed -6% avg per stock held 6 months. The technical entry timing (cup-with-handle breakout) is critical -- screening alone is not enough.

### Quantitative Screen:
- **C:** Quarterly EPS growth >= 25% YoY (both latest and prior quarter)
- **A:** Annual EPS growth >= 25% each of last 3 years
- ROE >= 17%
- Current quarter profit margin > TTM profit margin
- **L:** 52-week price performance in top 15% of market; price closer to 52-week high than low
- **I:** >= 20 institutional holders; institutional holder count increasing YoY; not in top 50 most-held
- **S:** Price >= $15; no OTC/foreign stocks
- **M:** Only buy when market in confirmed uptrend (S&P 500 above 50-day MA, no distribution days cluster)

### Entry/Exit:
- **Buy:** breakout from cup-with-handle base (min 7 weeks), price crosses pivot point on volume >= 1.5x average
- **Stop loss:** 7-8% below buy point, no exceptions
- **Hold:** sell at 20-25% gain or on breakdown below 50-day MA

---

## 3. Candlestick Patterns (Backtested on SPY, 1993-2024)

**Key finding:** Bearish patterns often work as *bullish* signals (mean-reversion). Combined top-10 patterns: 10.6% CAGR, 72% win rate, 35% time invested.

| Pattern | Trades | Avg Gain | Win Rate | Profit Factor | CAGR |
|---------|--------|----------|----------|---------------|------|
| Bearish Engulfing (buy signal!) | 296 | 0.53% | 71% | 2.5 | 5.0% |
| Three Outside Down (buy signal!) | 112 | 0.70% | 78% | 2.6 | 2.3% |
| Bullish Harami | 306 | 0.33% | 76% | 1.65 | 3.1% |

### Codeable Rules (mean-reversion on SPY):
- **Entry:** Buy at close when bearish engulfing pattern detected (today's open > yesterday's close AND today's close < yesterday's open AND today's body engulfs yesterday's body)
- **Exit:** Sell when today's close > yesterday's high
- **Avg hold:** ~5 trading days
- **Avoid:** Tweezer tops/bottoms (50% loss rate, 1.07 reward/risk)

---

## 4. Academic 12-1 Month Momentum (S&P 500, 2006-2024)

**Source:** Kumar (2026), SSRN #5367656.

| Metric | Value |
|--------|-------|
| Net annualized return (long-short) | -2.79% |
| Annualized volatility | 20.66% |
| Sharpe ratio | -0.23 |
| Max drawdown | -81% |
| Long leg only | +7.9% annualized |
| Short leg only | -9.1% annualized |

### Codeable Implementation:
- **Signal:** Rank all S&P 500 stocks by cumulative return months t-12 to t-2 (skip most recent month)
- **Long:** Top decile; **Short:** Bottom decile
- **Rebalance:** Monthly
- **Verdict:** Long-only momentum still works (+7.9%); long-short is broken by catastrophic short-leg crashes. Use long-only with market regime filter.
- **ETFs:** MTUM (iShares MSCI USA Momentum Factor), QMOM (Alpha Architect)

---

## 5. Trend Following / Managed Futures ETFs

| ETF | Expense | 2021 | 2022 | CAGR (inception) | Sharpe | Equity Correlation |
|-----|---------|------|------|-------------------|--------|--------------------|
| DBMF | 0.85% | +11.4% | +23.1% | +9.35% | 1.87 | -0.40 |
| KMLM | 0.92% | +7.1% | +44.8% | ~10% | 1.77 | -0.27 |
| CTA | 0.75% | N/A | launched 2022 | ~5% | N/A | negative |

### Strategy Logic (KMLM replication):
- **Assets:** Futures on equities, bonds, currencies, commodities (25+ markets)
- **Signal:** Price > 12-month SMA = long; Price < 12-month SMA = short (or flat)
- **Position sizing:** Inverse volatility (target equal risk contribution)
- **Rebalance:** Monthly
- **Key value:** Negative equity correlation; massive gains in 2022 crash year
- **Best use:** 10-20% portfolio allocation for crisis alpha

---

## 6. Larry Williams %R Short-Term Strategy

**Backtested on SPY (inception-present): 81% win rate, 11.9% CAGR, 22% time invested.**

### Exact Rules:
```
Williams_%R = ((Highest_High_2d - Close) / (Highest_High_2d - Lowest_Low_2d)) * -100
# Lookback period: 2 days (not default 14)

Entry: Buy at CLOSE when Williams_%R < -90
Exit:  Sell at CLOSE when (Close > Yesterday_High) OR (Williams_%R > -30)
```

| Metric | SPY | QQQ |
|--------|-----|-----|
| CAGR | 11.9% | 13.4% |
| Buy & Hold | 10.3% | 9.9% |
| Win Rate | 78% | 78% |
| Total Trades | 598 | 251 |
| Avg Gain/Trade | 0.6% | ~0.8% |
| Max Drawdown | 17% | 20.5% |
| Profit Factor | 2.2 | 3.2 |
| Time Invested | 22% | 14% |
| Risk-Adj Return | 52% | ~95% |

**Best years:** 2008: +98.9%, 2020: +43.3%, 2022: +15.7% (thrives in volatility).

---

## Priority for Backtesting Implementation

1. **Williams %R (2-day)** -- Simplest to code, strongest backtested edge, works on SPY/QQQ
2. **Candlestick mean-reversion** -- Bearish engulfing as buy signal on SPY, 5-day hold
3. **Minervini Trend Template** -- 8-point stock screener, combine with volume breakout
4. **Trend following SMA crossover** -- Multi-asset futures, monthly rebalance
5. **Long-only momentum** -- 12-1 month ranking, top decile, monthly rebalance via MTUM
6. **CAN SLIM** -- Most complex, needs fundamental data feed, entry timing critical

Sources:
- [Minervini VCP Guide - FinerMarketPoints](https://www.finermarketpoints.com/post/what-is-a-vcp-pattern-mark-minervini-s-volatility-contraction-pattern-explained)
- [Minervini SEPA Blueprint - TradingMomentum](https://tradingmomentum.substack.com/p/the-minervini-blueprint-the-sepa)
- [CAN SLIM Guide - Portfolio123](https://blog.portfolio123.com/a-stock-pickers-guide-to-william-oneils-can-slim-system/)
- [CAN SLIM - EarningSpike](https://www.earningspike.com/canslim-method)
- [75 Candlestick Patterns Backtest - QuantifiedStrategies](https://www.quantifiedstrategies.com/the-complete-backtest-of-all-75-candlestick-patterns/)
- [3 Bullish Patterns That Work - QuantifiedStrategies](https://www.quantifiedstrategies.com/3-bullish-candlestick-patterns-that-work/)
- [12-1 Momentum Study - SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5367656)
- [Managed Futures ETF Comparison - PicturePerfectPortfolios](https://pictureperfectportfolios.com/whats-the-best-managed-futures-etf-dbmf-vs-kmlm-vs-cta/)
- [Williams %R Strategy 81% Win Rate - QuantifiedStrategies](https://www.quantifiedstrategies.com/williams-r-trading-strategy/)
- [Williams %R - StockCharts](https://chartschool.stockcharts.com/table-of-contents/technical-indicators-and-overlays/technical-indicators/williams-r)
- [Trend Following - ReturnStacked](https://www.returnstacked.com/managed-futures-trend-following/)

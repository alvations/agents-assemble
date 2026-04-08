# More Winning Trading Strategies (Backtested)

## 1. RSI(2) Mean Reversion (Larry Connors)

**Rules:** Buy SPY when 2-period RSI < 10 AND price > 200-day SMA. Sell when RSI(2) > 80 OR price crosses above 5-day SMA.

**Backtested results (SPY, 1993-present):**
- CAGR: 6.8-9% (depending on exit rule)
- Win rate: 76%
- Max drawdown: 15-34% (tighter exits = lower drawdown)
- Avg gain per trade: 0.5-0.95%
- Time invested: 18-28%
- Risk-adjusted return: ~37% (9% / 0.28 time invested)

**Tickers:** SPY, QQQ, broad market ETFs. Works best on indices, not individual stocks.

Sources: [QuantifiedStrategies RSI-2](https://www.quantifiedstrategies.com/rsi-2-strategy/), [Connors RSI](https://www.quantifiedstrategies.com/connors-rsi/)

---

## 2. Golden Cross / Death Cross (50/200 SMA)

**Rules:** Buy when 50-day SMA crosses above 200-day SMA (golden cross). Sell when 50-day crosses below 200-day (death cross). Hold until opposite signal.

**Backtested results (S&P 500, 1960-2025):**
- CAGR: 6.8% (vs 7.2% buy-and-hold)
- Win rate: 79%
- Max drawdown: -33% (vs -56% buy-and-hold)
- Only 33 trades in 66 years (~0.5/year)
- Avg gain per trade: 15.8%
- Time invested: 70%
- Risk-adjusted return: 9.6%

**Verdict:** Slightly lower raw returns than buy-and-hold, but cuts max drawdown nearly in half. A risk-management overlay, not an alpha generator.

**Tickers:** S&P 500 / SPY only. More whipsaws on individual stocks.

Sources: [QuantifiedStrategies Golden Cross](https://www.quantifiedstrategies.com/golden-cross-trading-strategy/)

---

## 3. Buy Extreme Fear (VIX > 30)

**Rules:** Buy SPY when VIX crosses above 30. Hold for 3 weeks to 12 months depending on variant. Do NOT buy when VIX > 50 (that signals worse ahead).

**Backtested results (1990-2026):**
- VIX > 30: 81.5% win rate over 3 weeks, median gain +4.62%
- VIX > 35: 93.3% win rate over 3 months, median gain +11.56%
- VIX > 40: 100% win rate over 12 months, median gain +40%
- VIX > 50: WARNING -- 66.7% probability of NEGATIVE returns over 3 weeks
- Sweet spot: VIX 30-40 range
- Time invested: ~13% (rare signals)
- Risk-adjusted return: ~44%

**Tickers:** SPY, QQQ. The signal is about broad market fear, so trade indices.

Sources: [FXEmpire VIX Analysis](https://www.fxempire.com/forecasts/article/sp-500-forecast-vix-above-30-could-signal-a-tactical-buying-opportunity-1589696), [QuantifiedStrategies VIX](https://www.quantifiedstrategies.com/using-vix-to-trade-spy-and-sp-500/)

---

## 4. Dual Momentum (Gary Antonacci)

**Rules:** Monthly rebalancing. Compare 12-month returns of US stocks (SPY), international stocks (EFA), and T-bills. Hold whichever of SPY/EFA has higher momentum AND positive absolute momentum. If neither is positive, hold bonds (AGG). ~1.5 trades/year.

**Backtested results (1974-2025):**
- CAGR: 6.75% (vs 9.2% S&P 500)
- Max drawdown: -30% (vs -55% S&P 500)
- Correlation to S&P 500: 0.50
- Only ~1.5 trades per year (minimal costs)
- Significantly better risk-adjusted returns than S&P 500
- Weakness: Misses fast V-shaped recoveries (e.g., March 2020 rebound)

**Tickers:** SPY, EFA (international), AGG (bonds). Three-fund rotation.

Sources: [QuantifiedStrategies Dual Momentum](https://www.quantifiedstrategies.com/dual-momentum-trading-strategy/), [TuringTrader](https://www.turingtrader.com/portfolios/antonacci-dual-momentum/)

---

## 5. Overnight Return Anomaly (Buy Close, Sell Open)

**Rules:** Buy at market close (3:59 PM ET). Sell at market open (9:31 AM ET). Repeat daily.

**Backtested results (Q3 2020 - Q3 2025):**

| Ticker | Overnight (Close-to-Open) | Intraday (Open-to-Close) |
|--------|--------------------------|--------------------------|
| SPY    | +47.1%                   | +29.9%                   |
| QQQ    | +53.5%                   | +30.3%                   |
| IWP (Mid Growth) | +60.7%          | +5.1%                    |
| IWO (Small Growth)| +74.7%         | -23.4%                   |

QQQ 1999-2024: 92.58% of ALL gains came from overnight sessions (426.86 of 460.9 points).

**Critical caveat:** Transaction costs destroy the edge. A 20-year backtest showed fees consumed ~25% of capital. Bid-ask spreads at open/close plus slippage make this nearly impossible to profit from in practice. The anomaly is real but NOT tradeable for retail.

**Tickers:** QQQ and small-cap growth ETFs show the largest overnight edge.

Sources: [Overnight Anomaly Dissection](https://medium.com/@ejcacciatore/a-dissection-of-market-returns-the-overnight-anomaly-and-the-call-for-a-24-5-rhythm-995309847fea), [Overnight Returns Analysis](https://www.vatsalpandya.com/blog/overnight-returns-stock-market-anomaly), [Alpha Architect](https://alphaarchitect.com/trading-costs-wipe-out-the-overnight-return-anomaly/)

---

## Strategy Ranking by Practicality

| Strategy | Risk-Adj Return | Tradeable? | Frequency |
|----------|----------------|------------|-----------|
| VIX > 30 Buy | ~44% | Yes (rare) | ~2-4x/year |
| RSI(2) Mean Reversion | ~37% | Yes | ~15-20x/year |
| Golden Cross | 9.6% | Yes (slow) | ~0.5x/year |
| Dual Momentum | Better than S&P | Yes (monthly) | ~1.5x/year |
| Overnight Anomaly | Theoretical only | NO (costs kill it) | Daily |

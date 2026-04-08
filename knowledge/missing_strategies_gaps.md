# Missing Strategies: Research Findings

## 1. Mean Reversion ETF Cointegration (Stat Arb)

**Rules:** Find ETF pairs with Engle-Granger cointegration (p<0.05). Compute spread z-score using rolling hedge ratio from OLS regression. Enter long/short when z-score exceeds +/-2.0. Exit when z-score reverts to 0. Common pairs: EWA/EWC, GLD/SLV, SPY/IWM, XLF/XLK.

**Results:** 2025 study of 30 ETF pairs (2000-2024): z-score threshold of 2.0 yielded Sharpe 0.28 and 1% total profit (conservative). Bollinger-based variant on cointegrated pair: Sharpe 2.7, 97% win rate over 13 years. EWA/EWC simple strategy: Sharpe 0.69, 135 trades over 17 years. Best-case: 15% annual return, Sharpe 1.43 across 45 pairs. Key risk: cointegration breaks down during regime changes.

**Sources:** [Springer 2025 study](https://link.springer.com/article/10.1057/s41260-025-00416-0), [QuantStart SPY/IWM](https://www.quantstart.com/articles/Backtesting-An-Intraday-Mean-Reversion-Pairs-Strategy-Between-SPY-And-IWM/)

## 2. ADX Trend Strength Filter

**Rules:** Compute 14-period ADX with DI+/DI-. Strategy A (standalone): Buy when DI+ crosses above DI-, sell on reverse cross. Strategy B (filter): Only take trend entries when ADX > 25-30, confirming strong trend. Optimal: 35-day DI period, 15-day ADX breakout.

**Results:** DI crossover on S&P 500: CAGR 5.4%, profit factor 1.7, 55% market exposure. ADX as filter on SPY: CAGR 7%, profit factor 2.4, only 15% market exposure, max drawdown 19% (vs 55% buy-and-hold). Win rate ~47% standalone. Best use: filter for other strategies, not standalone signal. ADX alone underperforms buy-and-hold (3% vs 10% CAGR).

**Sources:** [QuantifiedStrategies ADX](https://www.quantifiedstrategies.com/adx-trading-strategy/), [MindMathMoney ADX Guide](https://www.mindmathmoney.com/articles/adx-indicator-trading-strategy-the-complete-guide-to-finding-trends-like-a-pro)

## 3. Ichimoku Cloud System

**Rules:** Default settings (9/26/52). Buy when price closes above the cloud (Kumo). Sell when price closes below the cloud. Optional: require Chikou Span above price for confirmation. Tenkan/Kijun cross for early entry.

**Results:** 15,024 trades across 30 DJ-30 stocks over 20 years: 10% win rate, underperformed buy-and-hold 90% of the time. S&P 500 backtest: CAGR 5.2% vs 6.9% buy-and-hold, invested 63% of time. One bright spot: Bitcoin CAGR 78% vs 60% buy-and-hold. Verdict: poor for stocks, may work for trending crypto. Reduces drawdowns but sacrifices returns.

**Sources:** [LiberatedStockTrader 15K trades](https://www.liberatedstocktrader.com/ichimoku-cloud/), [QuantifiedStrategies Ichimoku](https://www.quantifiedstrategies.com/ichimoku-strategy/)

## 4. Fibonacci Retracement Levels

**Rules:** Identify swing high/low. Draw Fibonacci levels (23.6%, 38.2%, 50%, 61.8%). Enter long at 50-61.8% retracement with confirming candle pattern (pin bar, engulfing). Stop below 100% level. Targets at 100%, 161.8%, 261.8% extension.

**Results:** Backtested across 102 stocks: accurate only 37% of the time. AAPL-specific: 30% win rate. Cannot be rigorously systematized -- rules are too subjective for automated backtesting. Academic research: passive buy-and-hold outperforms active Fibonacci trading. No credible evidence prices respect Fibonacci ratios. Verdict: avoid as standalone strategy.

**Sources:** [LiberatedStockTrader Fibonacci Myth](https://www.liberatedstocktrader.com/how-to-use-fibonacci-retracement/), [QuantifiedStrategies Fibonacci](https://www.quantifiedstrategies.com/fibonacci-trading-strategy/)

## 5. Market Breadth / Advance-Decline

**Rules:** Zweig Breadth Thrust: compute 10-day EMA of (advances / (advances + declines)) on NYSE. Signal fires when ratio surges from below 0.40 to above 0.615 within 10 days. Buy S&P 500 on signal. Hold 6-12 months.

**Results:** 19 post-WWII signals: 100% win rate over 6- and 12-month horizons. Average 12-month forward return: 23.4%. Combined with another indicator: 266 trades, 77% win rate, profit factor 2.55, max drawdown 23%. Caveat: extremely rare signal (fewer than 30 times since 1970s), so small sample size. Best use: confirmation of major bull market initiation, not frequent trading.

**Sources:** [QuantifiedStrategies Zweig](https://www.quantifiedstrategies.com/zweig-breadth-thrust-indicator-strategy/), [OptionsTrading IQ](https://optionstradingiq.com/zweig-breadth-thrust-signal/)

---

**Bottom line:** ETF cointegration and ADX-as-filter are implementable with solid risk-adjusted returns. Zweig Breadth Thrust is rare but near-perfect historically. Ichimoku and Fibonacci backtest poorly for stocks -- skip or use only as secondary confirmation.

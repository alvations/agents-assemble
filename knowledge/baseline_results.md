# Baseline Backtest Results (2022-01-01 to 2024-12-31)

## Summary

Tested 7 trading personas against SPY benchmark. $100K initial capital.

## Winners (positive alpha)

### 1. Momentum Trader (BEST)
- Total Return: 87.1% | CAGR: 23.4%
- Sharpe: 1.10 | Sortino: 1.65
- Max Drawdown: -16.1% | Alpha: +14.6%
- 700 trades, weekly rebalance
- Strategy: MACD + SMA alignment on tech leaders

### 2. Growth Investor
- Total Return: 49.4% | CAGR: 14.4%
- Sharpe: 0.62 | Sortino: 0.70
- Max Drawdown: -17.6% | Alpha: +5.6%
- 410 trades, weekly rebalance
- Strategy: Dip-buying in disruptive growth stocks during uptrends

## Neutral (positive return, slight negative alpha)

### 3. Buffett Value
- Total Return: 25.6% | CAGR: 8.0%
- Sharpe: 0.77 | Max DD: -6.0% | Alpha: -0.9%
- Best risk-adjusted (lowest drawdown), but missed bull market alpha
- Very low beta (0.07) — nearly market-neutral

### 4. Dividend Investor
- Total Return: 19.7% | CAGR: 6.2%
- Sharpe: 0.30 | Max DD: -10.1% | Alpha: -2.6%
- Stable but underperformed in bull market

## Losers (negative return or deep negative alpha)

### 5. Quant Mean Reversion
- Total Return: -1.2% | Sharpe: -0.83 | Alpha: -9.2%
- Mean reversion struggled in trending market (2022-2024)

### 6. Fixed Income Duration
- Total Return: -2.8% | Sharpe: -0.80 | Alpha: -9.8%
- Bond ETFs suffered during rate hike cycle (expected)

### 7. Meme Stock Trader
- Total Return: -13.3% | Sharpe: -0.04 | Max DD: -43.6%
- Worst performer. Post-meme bubble (2022+) was brutal

## Key Insights

1. **Momentum + trend-following dominated** this period (tech bull run 2023-2024)
2. **Buffett value had best risk-adjusted return** (Sharpe 0.77, only -6% DD) but low alpha
3. **Mean reversion failed** in a trending market — needs regime detection
4. **Fixed income needs yield curve data** from FRED to work properly (currently price-only)
5. **Meme stocks need social sentiment data** (Finnhub API) to time entries better

## Improvement Ideas for Self-Evolution

- Add regime detection (trending vs mean-reverting) to quant strategy
- Add FRED yield curve data to fixed income strategy
- Add position sizing via Kelly criterion or risk parity
- Add stop-loss/trailing-stop to all strategies
- Combine best personas into an ensemble strategy
- Add transaction cost sensitivity analysis

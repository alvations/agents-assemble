# Signal-Based Strategy Results (2026-04-10)

## New Strategies Tested (28 rolling windows each)

### WINNERS
- **sentiment_reversal**: HODL 0.84, 96% consistency, +808% 10Y
  - Thesis: buy extreme fear (VXX >1.5x SMA200), sell complacency
  - Why it works: Fear creates the best prices. VIX spikes are temporary, recoveries are permanent.
  
- **breadth_divergence**: HODL 0.62, 96% consistency, +407% 10Y
  - Thesis: go defensive when QQQ outperforms RSP (narrow breadth = top-heavy market)
  - Why it works: Narrow leadership precedes corrections. When only 5 stocks hold up the index, the rest will drag it down.

### MODERATE
- **institutional_flow**: HODL 0.25, 82% consistency, +159% 10Y
  - Thesis: follow institutional accumulation patterns (steady price + volume)
  - Why moderate: proxy signals (price/volume) only partially capture actual institutional flows. Real 13F data would improve this.

### FAILED
- **insider_buying_acceleration**: HODL 0.00, 0% consistency, +6% 10Y
  - Thesis: buy when insiders buy (proxied by price near 52-week low + volume spike)
  - Why it failed: price proxies DON'T reliably indicate insider buying. Need actual SEC Form 4 data in real-time.
  - Lesson: DON'T proxy insider trading with price action. The edge IS the information asymmetry — without actual insider data, there's no edge.

## New Technical Indicators Added
- VWAP (20-day), OBV, Stochastic (%K/%D), Williams %R, Ichimoku Cloud, ROC (12), CCI (20)
- Available to all strategies via _get_indicators()
- Dividend/split adjustment fixed: backtester now uses Adj Close

## Key Insight
The strategies that work use MARKET-WIDE signals (VIX for sentiment, breadth for market health). 
The strategy that failed tried to use INDIVIDUAL stock signals (insider proxies per stock).
Market-wide signals are more robust because they reflect aggregate behavior, not noisy individual data.

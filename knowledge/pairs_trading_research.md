# Pairs Trading / Statistical Arbitrage Research (2025)

## Key Findings

### Performance
- Top 20 pairs: 1.44% monthly excess return (~11% annualized)
- After transaction costs (81 bps/trade): 113-225 bps per 6-month period
- Consumer Discretionary: strongest risk-adjusted performance (1.08% monthly excess)
- Retailing: fastest mean-reversion, highest trade frequency

### Methods (ranked by robustness)
1. **Cointegration-based** (most robust): identifies long-term equilibrium, handles non-stationary prices
2. **Distance-based** (simplest): trades deviations from historical correlation
3. **Kalman filter + ML regime**: dynamic hedge estimation, adapts to regime changes

### 2025 Reality Check
- Profitability is WEAKER than historical (more competition)
- Highly dependent on market regime
- Transaction costs matter significantly
- Need longer holding periods than before

### Best Sector Pairs to Test
- Consumer Discretionary: XLY vs individual retail stocks
- Retailing: AMZN vs WMT, TGT vs COST, HD vs LOW
- Tech: GOOGL vs META, AAPL vs MSFT, NVDA vs AMD
- Financials: JPM vs BAC, V vs MA, GS vs MS
- Energy: XOM vs CVX, COP vs EOG

### Our Existing Pairs Strategy
Currently uses 7 pairs (XOM/CVX, KO/PEP, etc.). Performance:
- 3Y: 41.0%, 0.62 Sharpe
- Need to expand to more pairs and test cointegration-based approach

Sources:
- [Gatev et al. (Wharton)](http://stat.wharton.upenn.edu/~steele/Courses/434/434Context/PairsTrading/PairsTradingGGR.pdf)
- [7 Innovative Pairs Trading 2025](https://chartswatcher.com/pages/blog/7-innovative-pairs-trading-strategies-for-2025)
- [Modern Pairs Trading: What Still Works](https://blog.harbourfronts.com/2026/01/26/modern-pairs-trading-what-still-works-and-why/)

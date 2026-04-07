# Strategy Research — 2026-04-07

## Academic Findings (2024-2025)

### Factor Investing (proven academic factors)
1. **Value**: Low P/E, P/B stocks outperform over long horizons
2. **Momentum**: 12-1 month returns predict future returns (Jegadeesh & Titman)
3. **Quality**: High profitability + low leverage + stable earnings (AQR QMJ)
4. **Size**: Small caps outperform large caps (Fama-French SMB)
5. **Low Volatility**: Low-vol stocks outperform on risk-adjusted basis (anomaly)
6. **Dividend Yield**: High dividend stocks provide steady returns

### Smart Beta ETFs (accessible to retail)
- Value: VTV, VLUE, RPV
- Momentum: MTUM, PDP
- Quality: QUAL, SPHQ
- Low Vol: SPLV, USMV
- Size: IWM, VB
- Multi-factor: GSLC, LRGF

### Advanced Strategies from Recent Research
7. **Regime-Adaptive Ensemble**: Combine ML + technical + sentiment (Sharpe 3.64-5.10 in 2022-2023)
8. **Cross-Sectional Momentum**: Rank stocks by 12-1 month returns, long top decile, short bottom
9. **Earnings Momentum**: Buy after positive earnings surprise, sell after negative
10. **Insider Trading Following**: Track Form 4 filings, follow cluster buys
11. **Options-Implied Volatility Skew**: High put skew → bearish sentiment → contrarian buy
12. **Correlation Breakdown**: When stock-stock correlations spike, rotate to uncorrelated assets

### Strategies to Implement
- [x] Quality Factor (already implemented)
- [ ] Multi-Factor Smart Beta (combine value + momentum + quality)
- [ ] Earnings Momentum (post-earnings drift)
- [ ] Low Volatility Anomaly (buy lowest-vol quintile)
- [ ] Dual Momentum (absolute + relative momentum, Antonacci)
- [ ] Risk Parity with Momentum Overlay (Dalio + trend following)

## Multi-Horizon Testing Requirement
Must test all strategies on: 1Y, 3Y, 5Y, 10Y horizons.

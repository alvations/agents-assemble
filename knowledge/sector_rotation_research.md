# Sector Rotation Research (2025)

## Key Performance Data
- Faber: outperformed buy-and-hold 70% of the time since 1920s
- $10K in 2000 → $135K by 2024 vs $62K S&P 500 (2.2x better)
- Fidelity: +3.6% annual alpha over 15 years
- Uses 12-month momentum ranking of sector ETFs

## Why Our Existing Strategy Underperforms (0.33 Sharpe)
1. Uses SMA20 for momentum — too short-term, whipsaw
2. Faber uses 12-month momentum (SMA200 proxy) — more stable
3. Need absolute momentum filter (only invest if sector > 0%)
4. Missing trend validation (require SMA50 > SMA200)

## Faber's Approach (proven)
1. Rank 10 sector ETFs by 12-month momentum
2. Select top 3 sectors
3. Apply absolute momentum filter: only invest if above SMA200
4. If none above SMA200 → go to bonds (TLT/IEF)
5. Rebalance monthly

## Action Items
- [ ] Implement Faber's exact sector rotation methodology
- [ ] Use 12-month (SMA200) momentum, not SMA20
- [ ] Add absolute momentum filter
- [ ] Test across 1Y/3Y/5Y/10Y

Sources:
- [Quantpedia Sector Momentum](https://quantpedia.com/strategies/sector-momentum-rotational-system)
- [Faber's Sector Rotation (StockCharts)](https://chartschool.stockcharts.com/table-of-contents/trading-strategies-and-models/trading-strategies/fabers-sector-rotation-trading-strategy)
- [Fidelity study referenced](https://beaconinvesting.com/the-power-of-sector-rotation/)

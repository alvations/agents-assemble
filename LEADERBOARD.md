# Strategy Leaderboard

**Last Updated:** 2026-04-07 05:30 UTC
**Horizons:** 1Y (2024), 3Y (2022-2024), 5Y (2020-2024), 10Y (2015-2024)
**Initial Capital:** $100,000 | **Slippage:** 10 bps | **Commission:** $0
**Benchmark:** SPY | **Total strategies:** 44+ across 6 categories

## Cross-Horizon Consistency Ranking (THE definitive ranking)

Sorted by average Sharpe ratio across all 4 horizons. This is the most reliable way to evaluate a strategy — a high Sharpe on one period could be luck.

| Rank | Strategy | Category | Avg Sharpe | 1Y | 3Y | 5Y | 10Y | 10Y Return | Consistent? |
|------|----------|----------|-----------|------|------|------|------|-----------|-------------|
| 1 | **Momentum** | Generic | **1.08** | 1.49 | 1.36 | 0.60 | 0.86 | 570% | YES |
| 2 | **Momentum Crash-Hedged** | Research | **1.05** | 1.18 | 1.26 | 0.72 | 1.05 | 743% | **MOST CONSISTENT** |
| 3 | **AI Revolution** | Theme | **0.94** | 0.55 | 1.41 | 0.85 | 0.95 | 783% | YES |
| 4 | **Masayoshi Son** | Famous | **0.87** | 1.19 | 0.77 | 0.62 | 0.90 | 1068% | YES |
| 5 | **Defensive Rotation** | Recession | 0.59 | 0.88 | 0.33 | 0.60 | 0.57 | 212% | YES |
| 6 | Mean-Variance | Research | 0.53 | 0.12 | 0.40 | 0.88 | 0.71 | 206% | MIXED |
| 7 | Global Rotation | Research | 0.51 | -0.27 | 1.00 | 0.61 | 0.71 | 257% | MIXED |
| 8 | Small Cap Value | Theme | 0.50 | 1.25 | 1.10 | -0.12 | -0.25 | -3% | NO (recent only) |
| 9 | Dual Momentum | Research | 0.34 | 0.14 | 0.47 | 0.55 | 0.21 | 80% | MIXED |
| 10 | Multi-Factor Smart Beta | Research | 0.32 | -0.68 | 0.54 | 0.74 | 0.70 | 253% | MIXED |

## Highest Absolute Returns (10Y)

| Strategy | 10Y Return | 10Y Sharpe | 10Y Max DD |
|----------|-----------|-----------|-----------|
| Masayoshi Son | 1068% | 0.90 | -53.8% |
| AI Revolution | 783% | 0.95 | -30.2% |
| Momentum Crash-Hedged | 743% | 1.05 | -25.1% |
| Momentum | 570% | 0.86 | -35.3% |
| Global Rotation | 257% | 0.71 | -26.1% |
| Multi-Factor Smart Beta | 253% | 0.70 | -24.2% |
| Quality Factor | 230% | 0.68 | -25.8% |

## Best Risk-Adjusted (Lowest Max Drawdown)

| Strategy | 10Y Return | 10Y Max DD | 10Y Sharpe |
|----------|-----------|-----------|-----------|
| Mean-Variance | 206% | **-15.6%** | 0.71 |
| Low Vol Anomaly | 52% | -12.7% | 0.07 |
| Momentum Crash-Hedged | 743% | -25.1% | 1.05 |
| Multi-Factor Smart Beta | 253% | -24.2% | 0.70 |
| Quality Factor | 230% | -25.8% | 0.68 |

## Losing Strategies (avoid)

| Strategy | Avg Sharpe | Why It Failed |
|----------|-----------|---------------|
| Carl Icahn | -0.46 | Deep value needs patience > 10Y, 2022 crushed financials |
| Prince Alwaleed | -0.27 | Too selective, crisis buying rare in bull markets |
| Dogs of Dow | -0.00 | Contrarian works 3Y+ but terrible short-term |
| Low Vol Anomaly | 0.07 | Works in theory but missed tech rally entirely |
| Small Cap Value | 0.50 (1Y/3Y only) | Great recent, terrible 5Y/10Y (COVID crash destroyed it) |

## Recommended Deployable Portfolio

| Component | Strategy | Weight | Role | Avg Sharpe |
|-----------|----------|--------|------|-----------|
| Core | Momentum Crash-Hedged | 40% | Consistent alpha, vol-scaled | 1.05 |
| Growth | AI Revolution | 30% | Capture tech megatrend | 0.94 |
| Hedge | Defensive Rotation | 20% | Recession protection | 0.59 |
| Diversifier | Global Rotation | 10% | International exposure | 0.51 |

## Methodology

- All backtests use yfinance daily OHLCV data
- 44+ strategies across 6 categories: generic, famous investors, themes, recession, unconventional, research
- Universe: 500+ tickers across 40+ categories (US, Europe, Japan, China, India, LatAm, Africa, Middle East, SE Asia)
- Indicators: SMA20/50/200, MACD, RSI14, Bollinger Bands, ATR14, vol_20
- Self-evolved 20+ iterations across all modules (~$15 total API cost)

## How to Reproduce

```bash
cd agents-assemble
# Single strategy, all horizons
python run_multi_horizon.py --persona momentum_crash_hedge

# All strategies in a category
python run_multi_horizon.py --category research

# Everything
python run_multi_horizon.py
```

## Results Files

All raw results are in `results/` as JSON. Multi-horizon reports in `knowledge/multi_horizon/`.
Trade recommendations (entry/exit/stop-loss) in `strategy/winning/` and `strategy/losing/`.

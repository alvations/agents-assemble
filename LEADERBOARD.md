# Strategy Leaderboard

**Last Updated:** 2026-04-07 10:35 UTC
**Horizons Tested:** 1Y (2024), 3Y (2022-2024), 5Y (2020-2024), 10Y (2015-2024)
**Initial Capital:** $100,000 | **Slippage:** 10 bps | **Commission:** $0
**Benchmark:** SPY | **Total Strategies:** 63 | **Total Tickers:** 510

## NEW #1: Concentrate Winners (1.11 avg Sharpe!)

| Horizon | Return | Sharpe | Max DD |
|---------|--------|--------|--------|
| 1Y | 28.9% | 1.50 | -6.5% |
| 3Y | 135.6% | 1.28 | -18.0% |
| 5Y | 132.8% | 0.74 | -28.1% |
| 10Y | **817.5%** | 0.92 | -28.3% |
| **Avg** | — | **1.11** | — |

## Cross-Horizon Consistency (Avg Sharpe across 1Y/3Y/5Y/10Y)

| Rank | Strategy | Category | 1Y | 3Y | 5Y | 10Y | **Avg Sharpe** |
|------|----------|----------|----|----|----|----|-----------|
| **1** | **Concentrate Winners** | Unconventional | **1.50** | **1.28** | 0.74 | 0.92 | **1.11** |
| 2 | Momentum | Generic | 1.49 | 1.36 | 0.60 | 0.86 | **1.08** |
| 3 | Momentum Crash-Hedged | Research | 1.18 | 1.26 | 0.72 | 1.05 | **1.05** |
| 4 | AI Revolution | Theme | 0.55 | 1.41 | 0.85 | 0.95 | **0.94** |
| 5 | Masayoshi Son | Famous | 1.19 | 0.77 | 0.62 | 0.90 | **0.87** |
| 6 | Healthcare+Asia | Hedge Fund | 0.88 | 0.80 | 0.94 | 0.61 | **0.81** |
| 6 | Pairs Trading | Generic | 0.87 | 0.62 | 1.03 | 0.72 | **0.81** |
| 8 | Kelly Optimal | Math | 0.06 | 0.72 | 0.95 | 0.96 | **0.67** |
| 9 | Defensive Rotation | Recession | 0.88 | 0.33 | 0.60 | 0.57 | **0.59** |
| 10 | Global Rotation | Research | -0.27 | 1.00 | 0.61 | 0.71 | **0.51** |

## Definitive 3Y Rankings (2022-2024)

| Rank | Strategy | Category | 3Y Return | 3Y Sharpe | 3Y Max DD |
|------|----------|----------|-----------|-----------|-----------|
| 1 | **AI Revolution** | Theme | **183.6%** | **1.41** | -22.0% |
| 2 | **Momentum** | Generic | **135.0%** | **1.36** | -17.9% |
| 3 | **Concentrate Winners** | Unconventional | **135.6%** | **1.28** | -18.0% |
| 4 | **Momentum Crash-Hedged** | Research | **117.1%** | **1.26** | -20.8% |
| 5 | Small Cap Value | Theme | 56.1% | **1.10** | **-4.6%** |
| 6 | Prince Alwaleed | Famous | 44.5% | **1.02** | -9.5% |
| 7 | Global Rotation | Research | 52.4% | **1.00** | -8.1% |
| 8 | Defense & Aerospace | Theme | **92.9%** | 0.64 | -46.1% |
| 9 | **GLP-1 Obesity** | Theme | **80.7%** | **0.92** | -12.5% |
| 10 | Masayoshi Son | Famous | **90.8%** | 0.77 | -28.1% |

## 10Y Absolute Returns

| Strategy | 10Y Return | 10Y Sharpe |
|----------|-----------|-----------|
| Masayoshi Son | 1068% | 0.90 |
| **Concentrate Winners** | **817%** | **0.92** |
| AI Revolution | 783% | 0.95 |
| Momentum Crash-Hedged | 743% | 1.05 |
| Momentum | 570% | 0.86 |

## New Strategies Added (2026-04-07)

| Strategy | Type | 3Y Sharpe | Status |
|----------|------|-----------|--------|
| **Concentrate Winners** | Unconventional | **1.28** | **NEW #1!** |
| GLP-1 Obesity | Theme | 0.92 | Winner |
| Robotics/Autonomous | Theme | 0.40 | Moderate |
| Dividend Aristocrat Momentum | Unconventional | -0.46 | Failed |

## Failed Strategies (see knowledge/failures_log.md)

Factor ETF Rotation, Faber Sector Rotation, Sell in May, Z-Score MR,
ERC, Dividend Aristocrat Momentum. Don't repeat without fundamental changes.

## Recommended Portfolio

| Component | Strategy | Weight | Role | Sharpe |
|-----------|----------|--------|------|--------|
| Core | Concentrate Winners | 30% | Maximum alpha | 1.11 |
| Hedged Core | Momentum Crash-Hedged | 25% | Consistent, vol-scaled | 1.05 |
| Growth | AI Revolution | 20% | Tech megatrend | 0.94 |
| Health | GLP-1 Obesity | 10% | Pharma theme | 0.92 |
| Hedge | Defensive Rotation | 15% | Recession protection | 0.59 |

## Library Stats

- **63 strategies** across 8 categories
- **510 unique tickers** across 71 categories
- **50+ self-evolution iterations**
- **55+ commits**
- Trade recommendations in `strategy/winning/` and `strategy/losing/`

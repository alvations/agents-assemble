# Strategy Leaderboard

**Last Updated:** 2026-04-07 06:20 UTC
**Horizons Tested:** 1Y (2024), 3Y (2022-2024), 5Y (2020-2024), 10Y (2015-2024)
**Initial Capital:** $100,000 | **Slippage:** 10 bps | **Commission:** $0
**Benchmark:** SPY | **Total Strategies:** 61 | **Total Tickers:** 510

## Definitive 3Y Rankings (2022-01-01 to 2024-12-31)

All 61 strategies backtested on identical 3-year period.

| Rank | Strategy | Category | 3Y Return | 3Y Sharpe | 3Y Max DD |
|------|----------|----------|-----------|-----------|-----------|
| 1 | **AI Revolution** | Theme | **183.6%** | **1.41** | -22.0% |
| 2 | **Momentum** | Generic | **135.0%** | **1.36** | -17.9% |
| 3 | **Momentum Crash-Hedged** | Research | **117.1%** | **1.26** | -20.8% |
| 4 | **Small Cap Value** | Theme | 56.1% | **1.10** | **-4.6%** |
| 5 | Prince Alwaleed | Famous | 44.5% | **1.02** | -9.5% |
| 6 | Global Rotation | Research | 52.4% | **1.00** | -8.1% |
| 7 | **GLP-1 Obesity** | Theme | **80.7%** | **0.92** | -12.5% |
| 8 | Defense & Aerospace | Theme | **92.9%** | 0.64 | -46.1% |
| 9 | Healthcare + Asia | Hedge Fund | 61.5% | 0.82 | -16.0% |
| 10 | Buffett Value | Generic | 27.0% | 0.81 | -7.5% |
| 11 | Masayoshi Son | Famous | **90.8%** | 0.77 | -28.1% |
| 12 | George Soros | Famous | 56.9% | 0.77 | -23.7% |
| 13 | Kelly Optimal | Math | 49.1% | 0.72 | -14.6% |
| 14 | Crypto Ecosystem | Theme | **90.4%** | 0.67 | -31.7% |
| 15 | Quality Factor | Unconventional | 31.9% | 0.70 | -8.9% |

## Cross-Horizon Consistency (Avg Sharpe across 1Y/3Y/5Y/10Y)

| Rank | Strategy | 1Y | 3Y | 5Y | 10Y | **Avg Sharpe** |
|------|----------|----|----|----|----|-----------|
| 1 | **Momentum** | 1.49 | 1.36 | 0.60 | 0.86 | **1.08** |
| 2 | **Momentum Crash-Hedged** | 1.18 | 1.26 | 0.72 | 1.05 | **1.05** |
| 3 | **AI Revolution** | 0.55 | 1.41 | 0.85 | 0.95 | **0.94** |
| 4 | **Masayoshi Son** | 1.19 | 0.77 | 0.62 | 0.90 | **0.87** |
| 5 | **Healthcare+Asia** | 0.88 | 0.80 | 0.94 | 0.61 | **0.81** |
| 5 | **Pairs Trading** | 0.87 | 0.62 | 1.03 | 0.72 | **0.81** |

## Failed Strategies (don't repeat — see knowledge/failures_log.md)

| Strategy | Avg Sharpe | Why Failed |
|----------|-----------|------------|
| Factor ETF Rotation | -0.07 | ETFs too correlated with SPY |
| Faber Sector Rotation | 0.09 | Bond fallback failed in rate hikes |
| Sell in May | -0.16 | Calendar effects too weak |
| Z-Score Reversion | -1.42 (3Y) | Too few signals in bull market |
| Equal Risk Contribution | -0.59 (3Y) | TLT drag in 2022 |

## Recommended Portfolio

| Component | Strategy | Weight | Role | Sharpe |
|-----------|----------|--------|------|--------|
| Core | Momentum Crash-Hedged | 35% | Consistent alpha | 1.05 |
| Growth | AI Revolution | 25% | Tech megatrend | 0.94 |
| Health | GLP-1 Obesity | 15% | Pharma theme | 0.92 |
| Hedge | Defensive Rotation | 15% | Recession protection | 0.59 |
| Intl | Global Rotation | 10% | Geographic diversification | 0.51 |

## Library Summary

- **61 strategies** across 8 categories
- **510 unique tickers** across 71 categories
- **20+ knowledge files** with research, results, failures
- **45+ self-evolution iterations** across all modules
- **51 commits** since project start

## How to Run

```bash
pip install -e .

# All strategies, all horizons
python run_multi_horizon.py

# Single strategy
python run_multi_horizon.py --persona momentum_crash_hedge

# Category
python run_multi_horizon.py --category research

# Test suite
python test_strategies.py
```

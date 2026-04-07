# Strategy Leaderboard

**Last Updated:** 2026-04-07 12:30 UTC
**Horizons:** 1W / 2W / 1M / 3M / 6M / 1Y / 3Y / 5Y / 10Y (9 horizons)
**Initial Capital:** $100,000 | **Slippage:** 10 bps | **Commission:** $0
**Total Strategies:** 91 | **Total Tickers:** 580 | **Categories:** 12

> **Note:** All rankings show Return + Sharpe + Max Drawdown together.
> Individual metrics alone are deceptive.

## Top 15 Strategies — 3Y (2022-01-01 to 2024-12-31)

| Rank | Strategy | Category | 3Y Return | 3Y Sharpe | 3Y Max DD |
|------|----------|----------|-----------|-----------|-----------|
| 1 | **AI Revolution** | Theme | **183.6%** | **1.41** | -22.0% |
| 2 | **Concentrate Winners** | Unconventional | **135.6%** | **1.28** | -18.0% |
| 3 | **Momentum** | Generic | **135.0%** | **1.36** | -17.9% |
| 4 | **Momentum Crash-Hedged** | Research | **117.1%** | **1.26** | -20.8% |
| 5 | **Defense & Aerospace** | Theme | **92.9%** | 0.64 | -46.1% |
| 6 | Masayoshi Son | Famous | **90.8%** | 0.77 | -28.1% |
| 7 | Crypto Ecosystem | Theme | **90.4%** | 0.67 | -31.7% |
| 8 | **GLP-1 Obesity** | Theme | **80.7%** | **0.92** | -12.5% |
| 9 | Ackman (Pershing) | Famous | 76.1% | **1.22** | -12.1% |
| 10 | Druckenmiller | Famous/Political | 69.0% | 0.85 | -24.5% |
| 11 | Healthcare + Asia | Hedge Fund | 61.5% | 0.82 | -16.0% |
| 12 | BlackRock 2026 | Famous | 58.6% | **1.24** | -7.0% |
| 13 | George Soros | Famous | 56.9% | 0.77 | -23.7% |
| 14 | **Small Cap Value** | Theme | 56.1% | **1.10** | **-4.6%** |
| 15 | Growth Disruption | Generic | 55.7% | 0.65 | -20.6% |

## Cross-Horizon Consistency (Avg Sharpe across 1Y/3Y/5Y/10Y)

| Rank | Strategy | 1Y Return/Sharpe | 3Y Return/Sharpe | 5Y Return/Sharpe | 10Y Return/Sharpe | Avg Sharpe |
|------|----------|-----------------|-----------------|-----------------|------------------|-----------|
| 1 | **Concentrate Winners** | 28.9% / 1.50 | 135.6% / 1.28 | 132.8% / 0.74 | 817.5% / 0.92 | **1.11** |
| 2 | Momentum | 23.6% / 1.49 | 135.0% / 1.36 | 99.0% / 0.60 | 570.0% / 0.86 | **1.08** |
| 3 | Mom Crash-Hedged | 18.2% / 1.18 | 117.1% / 1.26 | 115.6% / 0.72 | 743.0% / 1.05 | **1.05** |
| 4 | AI Revolution | 11.1% / 0.55 | 183.6% / 1.41 | 178.5% / 0.85 | 783.3% / 0.95 | **0.94** |
| 5 | Nancy Pelosi | — / 0.42 | — / 1.39 | — / — | — / — | **0.91** |

## Best Portfolio Strategies (hedged)

| Strategy | 3M Return/Sharpe | 1Y Return/Sharpe | 3Y Return/Sharpe |
|----------|-----------------|-----------------|-----------------|
| **Barbell** | — / 1.78 | — / **2.05** | — / **0.91** |
| Core-Satellite | — / **2.24** | — / 1.75 | — / 0.66 |
| Staples-Hedged Growth | — / 0.46 | — / 1.80 | — / 0.81 |
| Adaptive Ensemble | — / 1.70 | — / 1.71 | — / 0.73 |

## Political / Billionaire Strategies

| Strategy | 1Y Return/Sharpe | 3Y Return/Sharpe |
|----------|-----------------|-----------------|
| **Nancy Pelosi** | — / 0.42 | — / **1.39** |
| Dan Loeb | — / 0.62 | — / 1.00 |
| Ken Griffin | — / 0.30 | — / 1.06 |
| David Tepper | — / -0.25 | — / 1.11 |

## Catalyst Scanner Top Findings (event-driven)

| Ticker | Strategy | Win Rate | Total Return |
|--------|----------|----------|-------------|
| SMCI | buy_spike_14d | 88% | **+1647%** |
| TAL | momentum_20d | 65% | +660% |
| PLTR | momentum_30d | 68% | +873% |
| AVGO | momentum_30d | 65% | +279% |
| AMD | buy_spike_30d | 78% | +208% |
| TSLA | momentum_20d | 62% | +201% |
| MELI | buy_dip_20d | 64% | +143% |
| LLY | momentum_20d | 67% | +139% |

## Failed Strategies (don't repeat)

| Strategy | 3Y Return | 3Y Sharpe | 3Y Max DD | Why Failed |
|----------|-----------|-----------|-----------|------------|
| Factor ETF Rotation | 24.2% | 0.39 | -9.5% | ETFs too correlated |
| Faber Sector Rotation | -2.7% | -0.30 | -28.7% | Bonds failed in rate hikes |
| Sell in May | — | -0.16 | — | Calendar effects too weak |
| All-Weather Modern | — | -0.84 | — | TLT drag |
| Div Aristocrat Momentum | -0.2% | -0.46 | -15.1% | Aristocrats lagged tech |

## Library Summary

- **91 strategies** across 12 categories
- **580 tickers** across 88 universe categories
- **9 horizons**: 1W, 2W, 1M, 3M, 6M, 1Y, 3Y, 5Y, 10Y
- **Tools**: terminal.py, catalyst_analyzer.py, news_catalyst_scanner.py, public_trader.py
- **92+ commits** on GitHub

```bash
# Run any strategy on any horizon
python run_multi_horizon.py --persona concentrate_winners --horizon 3y

# Scan a ticker for catalyst patterns
python catalyst_analyzer.py NVDA

# Generate Bloomberg-style charts
python terminal.py NVDA

# Full backtest suite
python run_multi_horizon.py --all-horizons --category research
```

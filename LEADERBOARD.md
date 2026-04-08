# Strategy Leaderboard

**Last Updated:** 2026-04-07 23:00 UTC
**Horizons:** 1W / 2W / 1M / 3M / 6M / 1Y / 3Y / 5Y / 10Y
**Initial Capital:** $100,000 | **Slippage:** 10 bps | **Commission:** $0
**Total Strategies:** 91 coded + 10 backtested | **Tickers:** 580 | **Categories:** 12

> All rankings show Return + Sharpe + Max Drawdown together.

## Top 15 Strategies — 3Y (2022-2024)

| Rank | Strategy | Category | 3Y Return | 3Y Sharpe | 3Y Max DD |
|------|----------|----------|-----------|-----------|-----------|
| 1 | **AI Revolution** | Theme | **183.6%** | **1.41** | -22.0% |
| 2 | **Concentrate Winners** | Unconventional | **135.6%** | **1.28** | -18.0% |
| 3 | **Momentum** | Generic | **135.0%** | **1.36** | -17.9% |
| 4 | **Momentum Crash-Hedged** | Research | **117.1%** | **1.26** | -20.8% |
| 5 | Defense & Aerospace | Theme | 92.9% | 0.64 | -46.1% |
| 6 | Masayoshi Son | Famous | 90.8% | 0.77 | -28.1% |
| 7 | Crypto Ecosystem | Theme | 90.4% | 0.67 | -31.7% |
| 8 | **GLP-1 Obesity** | Theme | **80.7%** | **0.92** | -12.5% |
| 9 | Ackman (Pershing) | Famous | 76.1% | **1.22** | -12.1% |
| 10 | Druckenmiller | Political | 69.0% | 0.85 | -24.5% |
| 11 | Healthcare + Asia | Hedge Fund | 61.5% | 0.82 | -16.0% |
| 12 | **BlackRock 2026** | Famous | 58.6% | **1.24** | -7.0% |
| 13 | Small Cap Value | Theme | 56.1% | **1.10** | **-4.6%** |
| 14 | Growth Disruption | Generic | 55.7% | 0.65 | -20.6% |
| 15 | Global Rotation | Research | 52.4% | 1.00 | -8.1% |

## NEW: Williams %R(2) Strategy (CODED — williams_seasonal_strategies.py)

| Ticker | 3Y Return | 3Y Win% | 10Y Return | 10Y Win% | 10Y PF |
|--------|-----------|---------|------------|----------|--------|
| **SPY** | +41.6% | **80%** | +95.9% | **77%** | 2.9 |
| **QQQ** | +56.6% | **79%** | +144.7% | **78%** | 2.7 |
| **NVDA** | +132.4% | 69% | **+815.5%** | 71% | 2.8 |
| **MSFT** | +36.3% | 66% | **+413.9%** | **75%** | **3.8** |
| **META** | +78.6% | 72% | **+334.6%** | **76%** | 3.0 |
| **AAPL** | +43.5% | 73% | **+328.1%** | 71% | **3.9** |

*Invested only ~22% of the time. Buy when %R(2) < -90 AND price > SMA200. Exit when close > prev day high.*

## NEW: Seasonal Energy (Sep→Apr)

| Ticker | 10Y Trades | 10Y Win% | 10Y Return |
|--------|-----------|----------|------------|
| **CVX** | 11 | **82%** | **+244.5%** |
| **XOM** | 11 | **73%** | **+203.6%** |
| XLE | 11 | 73% | +126.1% |

## NEW: Catalyst Scanner Top Discoveries

| Ticker | Strategy | Win% | Return | PF | Category |
|--------|----------|------|--------|-----|----------|
| SMCI | buy_spike_14d | 88% | **+1647%** | — | AI Servers |
| PLTR | momentum_30d | 68% | **+873%** | — | AI Software |
| HOOD | momentum_20d | 62% | **+499%** | 4.1 | Retail/Crypto |
| ORN | buy_spike_20d | **80%** | **+402%** | **7.0** | Infrastructure |
| STRL | momentum_20d | 71% | +269% | 4.5 | Breakout |
| OKLO | buy_spike_10d | 71% | +362% | 4.1 | Nuclear SMR |
| MARA | momentum_10d | 65% | +231% | 2.7 | Crypto Mining |
| LEU | buy_dip_10d | **78%** | +179% | **34.1** | Nuclear |
| AVGO | momentum_30d | 65% | +279% | 6.3 | AI Silicon |

## Portfolio Strategies (hedged)

| Strategy | 3M Return/Sharpe | 1Y Return/Sharpe | 3Y Return/Sharpe |
|----------|-----------------|-----------------|-----------------|
| **Barbell** | — / 1.78 | — / **2.05** | — / **0.91** |
| Core-Satellite | — / **2.24** | — / 1.75 | — / 0.66 |
| Staples-Hedged Growth | — / 0.46 | — / 1.80 | — / 0.81 |

## Short Seller Dip-Buy (contrarian)

| Ticker | Hold | Win% | Return | Verdict |
|--------|------|------|--------|---------|
| **MSTR** | 14d | 67% | **+226%** | Shorts wrong on BTC |
| **HOOD** | 20d | **80%** | **+168%** | Retail boom |
| **SMCI** | 10d | 71% | **+141%** | AI demand > short thesis |
| LCID | 3d | 29% | -14% | Shorts were RIGHT |

## Failed Strategies (don't repeat)

| Strategy | Return | Sharpe | Why |
|----------|--------|--------|-----|
| Factor ETF Rotation | +24% | 0.39 | ETFs too correlated |
| Faber Sector Rotation | -3% | -0.30 | Bonds failed in rate hikes |
| Sell in May | +2% | -0.16 | Calendar too weak |
| All-Weather Modern | — | -0.84 | TLT drag |
| Dividend Aristocrat Momentum | -0.2% | -0.46 | Aristocrats lagged tech |
| Overnight Anomaly | — | — | Transaction costs destroy edge |

## Research Findings Summary

| Topic | Key Finding | Source |
|-------|------------|--------|
| Williams %R(2) | 78% win, 11.9% CAGR on SPY | Connors Research |
| Energy Seasonal | CVX 82% win Sep→Apr | 10Y backtest |
| Minervini SEPA | 220% avg annual, 8 precise rules | US Investing Championship |
| VIX > 30 Buy | 81.5% win at 3 weeks | Historical analysis |
| Short Seller Dip | Kerrisdale best (65-70% win), Hindenburg worst (25-30%) | Academic + empirical |
| Gap Fill SPY | 89% win, +0.19%/trade | Backtested |
| 52-Week High | 72% continuation, +11.4% / 31 days | Backtested |
| Midterm Year | Oct low → Nov-Apr +16.4% (strongest 6 months) | Historical cycles |
| Nuclear/AI Power | OKLO +700%, LEU only US HALEU | Sector research |
| Merger Arb | WBD $27→$31, 14% spread, vote April 23 | Live deal |

## How to Use

```bash
# Web GUI
python app.py  # → http://localhost:8888

# Scan any ticker
python catalyst_analyzer.py NVDA

# Backtest strategies
python run_multi_horizon.py --persona momentum_crash_hedge --horizon 3y

# Generate trade plan
python public_trader.py momentum_crash_hedge

# Bloomberg-style charts
python terminal.py NVDA
```

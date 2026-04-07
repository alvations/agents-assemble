# Strategy Leaderboard

**Last Updated:** 2026-04-07 00:30 UTC
**Backtest Period:** 2022-01-01 to 2024-12-31 (3 years)
**Initial Capital:** $100,000
**Benchmark:** SPY (28.66% total return over period)
**Slippage:** 10 bps per trade | **Commission:** $0 (Robinhood-style)

## Top 10 Strategies by Sharpe Ratio

| Rank | Strategy | Type | Return | CAGR | Sharpe | Sortino | Max DD | Alpha | Win Rate | Trades | Result File |
|------|----------|------|--------|------|--------|---------|--------|-------|----------|--------|-------------|
| 1 | AI Revolution | Theme | 183.6% | ~41% | 1.41 | — | -22.0% | — | — | — | [results/ai_revolution_2022_2024_*.json](results/) |
| 2 | Momentum Tech Leaders | Generic | 99.0% | 23.4% | 1.20 | 1.65 | -16.6% | +17.1% | 37.4% | 700 | [results/momentum_tech_leaders_*.json](results/) |
| 3 | Small Cap Deep Value | Theme | 56.1% | ~16% | 1.10 | — | -4.6% | — | — | — | [results/small_cap_deep_value_*.json](results/) |
| 4 | Prince Alwaleed (Crisis) | Famous | 39.0% | ~12% | 0.90 | — | -9.5% | +2.9% | — | — | [results/alwaleed_crisis_buying_*.json](results/) |
| 5 | Masayoshi Son (Vision) | Famous | 81.2% | ~22% | 0.82 | — | -18.8% | +13.3% | — | — | [results/masayoshi_son_vision_*.json](results/) |
| 6 | Buffett Value | Generic | 25.6% | 8.0% | 0.77 | 0.95 | -6.0% | -0.9% | 29.0% | 68 | [results/buffett_value_beats_spy_*.json](results/) |
| 7 | Defense & Aerospace | Theme | 92.9% | ~25% | 0.64 | — | -46.1% | — | — | — | [results/defense_geopolitics_*.json](results/) |
| 8 | Defensive Rotation | Recession | 60.7% | ~17% | 0.65 | — | -18.5% | — | — | — | [results/defensive_rotation_recession_*.json](results/) |
| 9 | Carl Icahn (Activist) | Famous | 31.1% | ~9% | 0.65 | — | -5.6% | +0.7% | — | — | [results/carl_icahn_activist_*.json](results/) |
| 10 | Growth Disruption | Generic | 49.4% | 14.4% | 0.62 | 0.88 | -17.6% | +5.6% | 33.3% | 410 | [results/growth_disruption_*.json](results/) |

## Losing Strategies (avoid repeating)

| Rank | Strategy | Type | Return | Sharpe | Max DD | Why It Failed |
|------|----------|------|--------|--------|--------|---------------|
| 28 | Howard Marks Contrarian | Famous | -1.8% | -1.85 | -6.2% | Too selective, market kept trending up |
| 29 | Treasury Safe Haven | Recession | -11.0% | -0.92 | -22.4% | 2022 rate hikes crushed bonds |
| 30 | Quant Mean Reversion | Generic | -1.3% | -0.83 | -11.0% | Mean reversion failed in trending market |
| 31 | S/R Commodity | Famous | -11.8% | -0.80 | -23.8% | Commodities whipsawed, no clear trend |
| 32 | Meme Stock | Generic | -13.3% | -0.04 | -43.6% | Post-bubble destruction, 2022+ was brutal |

## Unconventional Strategies (NEW)

| Rank | Strategy | Type | Return | Sharpe | Max DD | Notes |
|------|----------|------|--------|--------|--------|-------|
| 1 | Quality Factor | Unconventional | 31.9% | 0.70 | -8.9% | Low vol + uptrend = quality |
| 2 | Dogs of the Dow | Unconventional | 33.1% | 0.54 | -8.3% | Contrarian: buy worst performers |
| 3 | Tail Risk Harvest | Unconventional | 9.2% | -0.14 | -5.1% | Buy after >3% crashes, lowest DD |
| 4 | Turn of Month | Unconventional | 7.4% | -0.11 | -11.5% | Calendar effect too weak |
| 5 | VIX Mean Reversion | Unconventional | 5.0% | -0.11 | -22.2% | 2022 rate hikes broke it |
| 6 | Sell in May | Unconventional | 2.2% | -0.16 | -24.2% | Missed 2023 summer rally |

## Strategy Categories

### Best by Category
- **Best Overall Return:** AI Revolution (183.6%)
- **Best Risk-Adjusted:** Small Cap Deep Value (1.10 Sharpe, -4.6% DD)
- **Best Famous Investor:** Masayoshi Son (81.2%, 0.82 Sharpe)
- **Best Recession Hedge:** Defensive Rotation (60.7%, 0.65 Sharpe)
- **Lowest Drawdown:** Small Cap Deep Value (-4.6%)
- **Highest Alpha vs SPY:** Momentum (+17.1% alpha)
- **Best Unconventional:** Quality Factor (0.70 Sharpe, -8.9% DD)

### Recommended Portfolio Blend
| Component | Strategy | Weight | Role |
|-----------|----------|--------|------|
| Growth Engine | AI Revolution | 40% | Capture tech megatrend |
| Value Anchor | Small Cap Value | 30% | Low-vol alpha capture |
| Recession Hedge | Defensive Rotation | 30% | Downside protection |

## Methodology
- All backtests use yfinance daily OHLCV data
- Technical indicators: SMA20/50/200, MACD, RSI14, Bollinger Bands, ATR14
- Strategies are callable: `strategy(date, prices, portfolio, data) -> {symbol: weight}`
- Rebalancing varies by strategy (daily/weekly/monthly)
- Results saved in `results/` as JSON, trade recs in `strategy/winning/` and `strategy/losing/`

## How to Reproduce
```bash
cd agents-assemble
python run_hypotheses.py --start 2022-01-01 --end 2024-12-31
```

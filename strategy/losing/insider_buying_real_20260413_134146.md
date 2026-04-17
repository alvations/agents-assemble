# LOSING Strategy: insider_buying_real

> **What it does:** ALL 4 signals must confirm: volume surge + near 52w low + stabilization + RSI recovery
>
> **Hypothesis:** Insider Buying Real Signal — gap audit strategy

**Generated:** 2026-04-13T13:41:45.114511
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 0.59%
- **sharpe_ratio:** -6.92
- **max_drawdown:** -0.71%
- **win_rate:** 10.12%
- **alpha:** -22.93%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 5.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 0.7%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy 0.5% below market in uptrend.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **AAPL** | FLAT | 29% | Limit 0.5% below market | 6.0% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **MSFT** | FLAT | 24% | Limit 0.5% below market | 5.1% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **GOOGL** | FLAT | 30% | Limit 0.5% below market | 6.3% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **JPM** | FLAT | 25% | Limit 0.5% below market | 5.3% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **BAC** | FLAT | 26% | Limit 0.5% below market | 5.4% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BAC) / [Yahoo](https://finance.yahoo.com/quote/BAC/) |
| **WFC** | FLAT | 31% | Market order (volatile) | 6.4% below entry | 6.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WFC) / [Yahoo](https://finance.yahoo.com/quote/WFC/) |
| **JNJ** | FLAT | 18% | Limit 0.5% below market | 3.7% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **PFE** | FLAT | 25% | Limit 0.5% below market | 5.1% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PFE) / [Yahoo](https://finance.yahoo.com/quote/PFE/) |
| **UNH** | FLAT | 43% | Market order (volatile) | 9.0% below entry | 9.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UNH) / [Yahoo](https://finance.yahoo.com/quote/UNH/) |
| **XOM** | FLAT | 24% | Limit 0.5% below market | 4.9% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **CVX** | FLAT | 23% | Limit 0.5% below market | 4.9% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CVX) / [Yahoo](https://finance.yahoo.com/quote/CVX/) |
| **HD** | FLAT | 23% | Limit 0.5% below market | 4.8% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HD) / [Yahoo](https://finance.yahoo.com/quote/HD/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -6.92 (target > 0.5)
- Max drawdown: -0.71% (target > -20%)
- Alpha: -22.93% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 2.0% |
| **Avg 5Y Sharpe** | -0.62 |
| **Avg 5Y Max DD** | -12.1% |
| **10Y Return (2015-2024)** | 8.2% |
| **10Y Sharpe** | -0.51 |
| **10Y Max DD** | -15.4% |
| **HODL Composite** | 0.01 |
| **Windows Tested** | 28 |
| **Consistency** | 18% |

### How to Use This Strategy Passively

**Weak long-term profile.** Not recommended for passive buy-and-hold. May still work as a tactical or hedged position — see main body.

</details>

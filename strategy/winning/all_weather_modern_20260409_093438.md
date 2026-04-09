# WINNING Strategy: all_weather_modern

> **What it does:** Updated Dalio All-Weather: reduced bonds, added TIPS + crypto exposure
>
> **Hypothesis:** All-Weather Modern (2026) — composite: 0.01, consistency: 25%

**Generated:** 2026-04-09T09:34:38.271552
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 13.85%
- **sharpe_ratio:** 0.15
- **max_drawdown:** -2.69%
- **win_rate:** 55.39%
- **alpha:** -18.70%

## Risk Parameters
- **max_portfolio_allocation:** 11.5%
- **stop_loss:** 3.2%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 2.7%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SHY** | BUY | 2% | Limit 0.5% below market | 1.6% below entry | 3.0% above entry | 23.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **TIP** | BUY | 4% | Limit 0.5% below market | 1.6% below entry | 3.0% above entry | 23.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TIP) / [Yahoo](https://finance.yahoo.com/quote/TIP/) |
| **IEF** | BUY | 6% | Limit 0.5% below market | 1.6% below entry | 3.0% above entry | 23.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEF) / [Yahoo](https://finance.yahoo.com/quote/IEF/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 3.1% below entry | 4.8% above entry | 11.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **VEA** | BUY | 35% | Market order (volatile) | 4.8% below entry | 7.4% above entry | 7.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VEA) / [Yahoo](https://finance.yahoo.com/quote/VEA/) |
| **VTI** | BUY | 17% | Limit 0.5% below market | 2.3% below entry | 3.6% above entry | 15.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VTI) / [Yahoo](https://finance.yahoo.com/quote/VTI/) |
| **XLE** | BUY | 23% | Limit 0.5% below market | 3.1% below entry | 4.8% above entry | 12.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 7.5% |
| **Avg 5Y Sharpe** | -0.94 |
| **Avg 5Y Max DD** | -6.1% |
| **10Y Return (2015-2024)** | 13.9% |
| **10Y Sharpe** | -0.96 |
| **10Y Max DD** | -8.0% |
| **HODL Composite** | 0.01 |
| **Windows Tested** | 28 |
| **Consistency** | 14% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>

# LOSING Strategy: bond_duration_trade

> **What it does:** Yield curve regime: long duration in flattening, short duration in steepening
>
> **Hypothesis:** Bond Duration Trade — gap audit strategy

**Generated:** 2026-04-13T13:38:16.615094
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -5.18%
- **sharpe_ratio:** -1.00
- **max_drawdown:** -10.18%
- **win_rate:** 53.26%
- **alpha:** -24.90%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 10.2%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 10.2%
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
| **IEF** | BUY | 6% | Limit 0.5% below market | 5.1% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEF) / [Yahoo](https://finance.yahoo.com/quote/IEF/) |
| **TIP** | BUY | 4% | Limit 0.5% below market | 5.1% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TIP) / [Yahoo](https://finance.yahoo.com/quote/TIP/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 5.1% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **BIL** | BUY | 0% | Limit 0.5% below market | 5.1% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BIL) / [Yahoo](https://finance.yahoo.com/quote/BIL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -1.00 (target > 0.5)
- Max drawdown: -10.18% (target > -20%)
- Alpha: -24.90% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 5.9% |
| **Avg 5Y Sharpe** | -0.47 |
| **Avg 5Y Max DD** | -11.9% |
| **10Y Return (2015-2024)** | 3.0% |
| **10Y Sharpe** | -0.59 |
| **10Y Max DD** | -15.3% |
| **HODL Composite** | 0.01 |
| **Windows Tested** | 28 |
| **Consistency** | 21% |

### How to Use This Strategy Passively

**Weak long-term profile.** Not recommended for passive buy-and-hold. May still work as a tactical or hedged position — see main body.

</details>

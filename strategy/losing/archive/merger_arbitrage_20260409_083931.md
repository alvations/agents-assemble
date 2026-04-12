# LOSING Strategy: merger_arbitrage

> **What it does:** M&A deal spread capture: buy targets at discount to deal price
>
> **Hypothesis:** Merger Arbitrage (M&A Spread) — consistency: 0% across 6 windows

**Generated:** 2026-04-09T08:39:31.799576
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -8.27%
- **sharpe_ratio:** -2.22
- **max_drawdown:** -8.27%
- **win_rate:** 18.51%
- **alpha:** -25.98%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 9.9%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 8.3%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** WAIT FOR SIGNAL: Only enter when price spread between paired stocks reaches extreme levels. Exit when spread normalizes.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **IEX** | BUY | 27% | Limit 0.5% below market | 11.2% below entry | 5.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEX) / [Yahoo](https://finance.yahoo.com/quote/IEX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -2.22 (target > 0.5)
- Max drawdown: -8.27% (target > -20%)
- Alpha: -25.98% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 1.4% |
| **Avg 5Y Sharpe** | -1.3 |
| **Avg 5Y Max DD** | -8.9% |
| **10Y Return (2015-2024)** | -0.8% |
| **10Y Sharpe** | -1.24 |
| **10Y Max DD** | -12.7% |
| **HODL Composite** | 0.0 |
| **Windows Tested** | 28 |
| **Consistency** | 10% |

### How to Use This Strategy Passively

This strategy is **NOT recommended for passive investing**. It has low consistency across time periods or negative long-term returns.

**If you still want exposure:** Limit to 5% of your portfolio maximum. Use the strategy orchestrator (conservative_regime) instead for passive allocation.

</details>

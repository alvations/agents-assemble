# LOSING Strategy: cointegration_pairs

> **What it does:** Long laggard in cointegrated pairs when spread Z > 2
>
> **Hypothesis:** Cointegration Pairs Trading 3Y

**Generated:** 2026-04-08T16:18:26.835157
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -6.87%
- **sharpe_ratio:** -1.36
- **max_drawdown:** -14.04%
- **win_rate:** 49.20%
- **alpha:** -11.02%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 16.8%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 14.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Enter on any weekly rebalance day. No specific timing edge detected.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **BAC** | BUY | 26% | Limit 0.5% below market | 18.2% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BAC) / [Yahoo](https://finance.yahoo.com/quote/BAC/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -1.36 (target > 0.5)
- Max drawdown: -14.04% (target > -20%)
- Alpha: -11.02% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
# LOSING Strategy: zscore_reversion

> **What it does:** Buy at Z < -2 (statistically oversold), sell at Z > 0
>
> **Hypothesis:** Z-Score Mean Reversion 3Y

**Generated:** 2026-04-08T14:16:27.544105
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 0.62%
- **sharpe_ratio:** -0.58
- **max_drawdown:** -5.61%
- **win_rate:** 41.62%
- **alpha:** -8.46%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 6.7%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 5.6%
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
| **XOM** | BUY | 23% | Limit 0.5% below market | 6.6% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.58 (target > 0.5)
- Max drawdown: -5.61% (target > -20%)
- Alpha: -8.46% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
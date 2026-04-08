# LOSING Strategy: tail_risk_harvest

> **What it does:** Buy quality names after sharp single-day drops, capture mean-reversion
>
> **Hypothesis:** Tail Risk Harvest (Buy Crashes) 3Y

**Generated:** 2026-04-08T15:54:55.343121
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -0.16%
- **sharpe_ratio:** -0.38
- **max_drawdown:** -16.87%
- **win_rate:** 40.29%
- **alpha:** -8.72%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 20.2%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 16.9%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Enter on any weekly rebalance day. No specific timing edge detected.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in
## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.38 (target > 0.5)
- Max drawdown: -16.87% (target > -20%)
- Alpha: -8.72% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
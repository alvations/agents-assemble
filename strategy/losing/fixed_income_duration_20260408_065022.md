# LOSING Strategy: fixed_income_duration

**Generated:** 2026-04-08T06:50:22.414268
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -2.48%
- **sharpe_ratio:** -0.79
- **max_drawdown:** -7.37%
- **win_rate:** 49.67%
- **alpha:** -9.66%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 8.8%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 7.4%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Enter on any weekly rebalance day. No specific timing edge detected.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in
## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.79 (target > 0.5)
- Max drawdown: -7.37% (target > -20%)
- Alpha: -9.66% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
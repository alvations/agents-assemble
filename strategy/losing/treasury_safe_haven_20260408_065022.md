# LOSING Strategy: treasury_safe_haven

**Generated:** 2026-04-08T06:50:22.555662
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -10.95%
- **sharpe_ratio:** -0.92
- **max_drawdown:** -22.38%
- **win_rate:** 48.85%
- **alpha:** N/A

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 22.4%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Enter on any weekly rebalance day. No specific timing edge detected.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in
## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.92 (target > 0.5)
- Max drawdown: -22.38% (target > -20%)
- Alpha: N/A (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
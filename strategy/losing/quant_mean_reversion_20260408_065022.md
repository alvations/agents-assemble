# LOSING Strategy: quant_mean_reversion

**Generated:** 2026-04-08T06:50:22.508600
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -1.28%
- **sharpe_ratio:** -0.83
- **max_drawdown:** -10.97%
- **win_rate:** 25.57%
- **alpha:** -9.26%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 13.2%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 11.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Strategy has low win rate — enter only on strong setup days. Be patient.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in
## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.83 (target > 0.5)
- Max drawdown: -10.97% (target > -20%)
- Alpha: -9.26% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
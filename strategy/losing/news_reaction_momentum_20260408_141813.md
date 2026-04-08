# LOSING Strategy: news_reaction_momentum

> **What it does:** Buy unusual volume + positive price moves (news proxy)
>
> **Hypothesis:** News Reaction Momentum 3Y

**Generated:** 2026-04-08T14:18:13.708340
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -0.38%
- **sharpe_ratio:** -0.61
- **max_drawdown:** -11.68%
- **win_rate:** 8.91%
- **alpha:** -8.79%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 14.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 11.7%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Strategy has low win rate — enter only on strong setup days. Be patient.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in
## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.61 (target > 0.5)
- Max drawdown: -11.68% (target > -20%)
- Alpha: -8.79% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
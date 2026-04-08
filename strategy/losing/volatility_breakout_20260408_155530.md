# LOSING Strategy: volatility_breakout

> **What it does:** Donchian breakout with ATR position sizing (Turtle Trading)
>
> **Hypothesis:** Volatility Breakout (Turtle) 3Y

**Generated:** 2026-04-08T15:55:30.236231
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -1.31%
- **sharpe_ratio:** -1.79
- **max_drawdown:** -5.31%
- **win_rate:** 17.55%
- **alpha:** -9.10%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 6.4%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 5.3%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Strategy has low win rate — enter only on strong setup days. Be patient.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in
## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -1.79 (target > 0.5)
- Max drawdown: -5.31% (target > -20%)
- Alpha: -9.10% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
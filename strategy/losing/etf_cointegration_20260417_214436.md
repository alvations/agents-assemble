# LOSING Strategy: etf_cointegration

> **What it does:** Mean reversion on cointegrated ETF pairs via z-score spread trading

**Generated:** 2026-04-17T21:44:36.688939
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 0.00%
- **sharpe_ratio:** 0.00
- **max_drawdown:** 0.00%
- **win_rate:** 0.00%
- **alpha:** -65.44%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 10.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 0.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Enter when Z-score exceeds 2.0. Exit when Z returns to 0.
- **timing:** WAIT FOR SIGNAL: Only enter when price spread between paired stocks reaches extreme levels. Exit when spread normalizes.
- **scaling:** Full position at entry. No scaling — it's a convergence trade.
## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: 0.00 (target > 0.5)
- Max drawdown: 0.00% (target > -20%)
- Alpha: -65.44% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
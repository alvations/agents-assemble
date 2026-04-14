# LOSING Strategy: insider_buying_acceleration

> **What it does:** Detect insider accumulation via price/volume proxies: 52-week low bounce, oversold uptrend, volume spike

**Generated:** 2026-04-14T07:23:08.802613
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 0.19%
- **sharpe_ratio:** -1.02
- **max_drawdown:** -4.37%
- **win_rate:** 20.94%
- **alpha:** -65.38%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 5.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 4.4%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy 0.5% below market in uptrend.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks.
## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -1.02 (target > 0.5)
- Max drawdown: -4.37% (target > -20%)
- Alpha: -65.38% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
# LOSING Strategy: treasury_safe_haven
**Generated:** 2026-04-06T09:49:25.953631
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -10.95%
- **sharpe_ratio:** -0.92
- **max_drawdown:** -22.38%
- **win_rate:** 48.85%
- **alpha:** N/A

## Risk Parameters
- **max_portfolio_allocation:** 5.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 22.4%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Enter on any weekly rebalance day. No specific timing edge detected.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Position Recommendations

### SHY — BUY
- Entry limit: $77.05 (0.5% below avg cost)
- Stop-loss: $58.08 (25.0% below entry)
- Take-profit: $81.31 (5.0% above entry)
- Position size: 5.0% of portfolio
- Trailing stop: 20.0% trailing stop after 2.5% gain

### IEF — BUY
- Entry limit: $88.17 (0.5% below avg cost)
- Stop-loss: $66.46 (25.0% below entry)
- Take-profit: $93.04 (5.0% above entry)
- Position size: 5.0% of portfolio
- Trailing stop: 20.0% trailing stop after 2.5% gain

### TLT — BUY
- Entry limit: $87.37 (0.5% below avg cost)
- Stop-loss: $65.86 (25.0% below entry)
- Take-profit: $92.20 (5.0% above entry)
- Position size: 5.0% of portfolio
- Trailing stop: 20.0% trailing stop after 2.5% gain

### GLD — BUY
- Entry limit: $223.35 (0.5% below avg cost)
- Stop-loss: $168.35 (25.0% below entry)
- Take-profit: $235.69 (5.0% above entry)
- Position size: 5.0% of portfolio
- Trailing stop: 20.0% trailing stop after 2.5% gain

### TIP — BUY
- Entry limit: $104.12 (0.5% below avg cost)
- Stop-loss: $78.48 (25.0% below entry)
- Take-profit: $109.88 (5.0% above entry)
- Position size: 5.0% of portfolio
- Trailing stop: 20.0% trailing stop after 2.5% gain

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.92 (target > 0.5)
- Max drawdown: -22.38% (target > -20%)
- Alpha: 0.00% if available (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
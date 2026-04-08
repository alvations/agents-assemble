# LOSING Strategy: williams_percent_r

> **What it does:** Buy %R<-90 above SMA200, exit close>prev high. 77% win SPY, 22% invested
>
> **Hypothesis:** Williams %R(2) Mean Reversion 3Y

**Generated:** 2026-04-08T14:19:21.098494
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 5.11%
- **sharpe_ratio:** -0.38
- **max_drawdown:** -5.90%
- **win_rate:** 19.28%
- **alpha:** -6.98%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 7.1%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 5.9%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Strategy has low win rate — enter only on strong setup days. Be patient.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **NVDA** | BUY | 49% | Market order (volatile) | 14.5% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.38 (target > 0.5)
- Max drawdown: -5.90% (target > -20%)
- Alpha: -6.98% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
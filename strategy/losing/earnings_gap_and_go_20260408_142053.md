# LOSING Strategy: earnings_gap_and_go

> **What it does:** Buy 4%+ gap-up on 3x volume (earnings proxy). 60-70% win, hold 1-5d
>
> **Hypothesis:** Earnings Gap-and-Go 3Y

**Generated:** 2026-04-08T14:20:52.995806
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 7.91%
- **sharpe_ratio:** -0.21
- **max_drawdown:** -7.98%
- **win_rate:** 26.33%
- **alpha:** -6.08%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 9.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 8.0%
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
| **PLTR** | BUY | 64% | Market order (volatile) | 25.5% below entry | 13.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PLTR) / [Yahoo](https://finance.yahoo.com/quote/PLTR/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.21 (target > 0.5)
- Max drawdown: -7.98% (target > -20%)
- Alpha: -6.08% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
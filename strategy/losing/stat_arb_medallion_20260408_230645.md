# LOSING Strategy: stat_arb_medallion

> **What it does:** Short-term mean reversion across sector pairs, Renaissance-inspired
>
> **Hypothesis:** Stat Arb (Medallion-style) 4Y (2022-2025)

**Generated:** 2026-04-08T23:06:45.408201
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 13.82%
- **sharpe_ratio:** -0.14
- **max_drawdown:** -3.80%
- **win_rate:** 47.90%
- **alpha:** -7.57%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 4.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 3.8%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Enter on any weekly rebalance day. Monitor SMA200 for trend confirmation.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **PG** | BUY | 18% | Limit 0.5% below market | 3.5% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PG) / [Yahoo](https://finance.yahoo.com/quote/PG/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.14 (target > 0.5)
- Max drawdown: -3.80% (target > -20%)
- Alpha: -7.57% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
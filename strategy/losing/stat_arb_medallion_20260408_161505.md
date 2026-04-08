# LOSING Strategy: stat_arb_medallion

> **What it does:** Short-term mean reversion across sector pairs, Renaissance-inspired
>
> **Hypothesis:** Stat Arb (Medallion-style) 3Y

**Generated:** 2026-04-08T16:15:05.743238
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 8.72%
- **sharpe_ratio:** -0.28
- **max_drawdown:** -3.80%
- **win_rate:** 46.41%
- **alpha:** -5.83%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 4.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 3.8%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Enter on any weekly rebalance day. No specific timing edge detected.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **JNJ** | BUY | 18% | Limit 0.5% below market | 3.4% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.28 (target > 0.5)
- Max drawdown: -3.80% (target > -20%)
- Alpha: -5.83% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
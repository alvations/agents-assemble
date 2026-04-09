# WINNING Strategy: fifty_two_week_breakout

> **What it does:** Buy new 52-week highs on 1.5x volume. 72% continuation, +11.4%/31d
>
> **Hypothesis:** 52-Week High Breakout — composite: 0.14, consistency: 83%

**Generated:** 2026-04-09T09:36:53.951319
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 14.93%
- **sharpe_ratio:** 0.22
- **max_drawdown:** -3.64%
- **win_rate:** 44.74%
- **alpha:** -18.37%

## Risk Parameters
- **max_portfolio_allocation:** 10.8%
- **stop_loss:** 4.4%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 3.6%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 5.5% below entry | 6.3% above entry | 8.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

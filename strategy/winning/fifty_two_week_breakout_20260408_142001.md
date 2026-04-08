# WINNING Strategy: fifty_two_week_breakout

> **What it does:** Buy new 52-week highs on 1.5x volume. 72% continuation, +11.4%/31d
>
> **Hypothesis:** 52-Week High Breakout 3Y

**Generated:** 2026-04-08T14:20:01.748486
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 15.14%
- **sharpe_ratio:** 0.24
- **max_drawdown:** -2.13%
- **win_rate:** 45.61%
- **alpha:** -3.83%

## Risk Parameters
- **max_portfolio_allocation:** 10.9%
- **stop_loss:** 2.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 2.1%
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
| **AAPL** | BUY | 29% | Limit 0.5% below market | 3.1% below entry | 6.0% above entry | 9.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

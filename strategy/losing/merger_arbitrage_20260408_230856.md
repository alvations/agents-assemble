# LOSING Strategy: merger_arbitrage

> **What it does:** M&A deal spread capture: buy targets at discount to deal price
>
> **Hypothesis:** Merger Arbitrage (M&A Spread) 4Y (2022-2025)

**Generated:** 2026-04-08T23:08:56.118837
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -9.98%
- **sharpe_ratio:** -2.42
- **max_drawdown:** -9.98%
- **win_rate:** 15.17%
- **alpha:** -13.47%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 12.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 10.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When spread Z-score > 1.5 (divergence starting). STRONG BUY: When Z-score > 2.0 — statistical mean reversion at extreme levels.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **IEX** | BUY | 27% | Limit 0.5% below market | 13.5% below entry | 5.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEX) / [Yahoo](https://finance.yahoo.com/quote/IEX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -2.42 (target > 0.5)
- Max drawdown: -9.98% (target > -20%)
- Alpha: -13.47% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
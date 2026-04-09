# LOSING Strategy: cointegration_pairs

> **What it does:** Long laggard in cointegrated pairs when spread Z > 2
>
> **Hypothesis:** Cointegration Pairs Trading 4Y (2022-2025)

**Generated:** 2026-04-08T23:11:29.038963
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -3.48%
- **sharpe_ratio:** -1.07
- **max_drawdown:** -14.04%
- **win_rate:** 48.20%
- **alpha:** -11.75%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 16.8%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 14.0%
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
| **UPS** | BUY | 30% | Market order (volatile) | 21.2% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UPS) / [Yahoo](https://finance.yahoo.com/quote/UPS/) |
| **PG** | BUY | 18% | Limit 0.5% below market | 13.0% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PG) / [Yahoo](https://finance.yahoo.com/quote/PG/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -1.07 (target > 0.5)
- Max drawdown: -14.04% (target > -20%)
- Alpha: -11.75% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
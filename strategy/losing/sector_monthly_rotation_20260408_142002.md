# LOSING Strategy: sector_monthly_rotation

> **What it does:** Top 3 of 11 sector ETFs by 3-month momentum. 13.94% CAGR
>
> **Hypothesis:** Sector Monthly Rotation 3Y

**Generated:** 2026-04-08T14:20:02.806560
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 6.86%
- **sharpe_ratio:** -0.05
- **max_drawdown:** -24.10%
- **win_rate:** 49.47%
- **alpha:** -6.42%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 24.1%
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
| **XLF** | BUY | 18% | Limit 0.5% below market | 18.9% below entry | 3.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLF) / [Yahoo](https://finance.yahoo.com/quote/XLF/) |
| **XLY** | BUY | 23% | Limit 0.5% below market | 23.7% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLY) / [Yahoo](https://finance.yahoo.com/quote/XLY/) |
| **XLC** | BUY | 17% | Limit 0.5% below market | 17.8% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLC) / [Yahoo](https://finance.yahoo.com/quote/XLC/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.05 (target > 0.5)
- Max drawdown: -24.10% (target > -20%)
- Alpha: -6.42% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
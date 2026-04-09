# WINNING Strategy: sector_monthly_rotation

> **What it does:** Top 3 of 11 sector ETFs by 3-month momentum. 13.94% CAGR
>
> **Hypothesis:** Sector Monthly Rotation — consistency: 83% across 6 windows

**Generated:** 2026-04-09T08:40:18.882085
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 45.33%
- **sharpe_ratio:** 0.74
- **max_drawdown:** -13.20%
- **win_rate:** 52.06%
- **alpha:** -9.81%

## Risk Parameters
- **max_portfolio_allocation:** 8.8%
- **stop_loss:** 15.8%
- **take_profit_target:** 6.7%
- **max_drawdown_tolerance:** 13.2%
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
| **XLV** | BUY | 15% | Limit 0.5% below market | 10.2% below entry | 4.3% above entry | 13.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLV) / [Yahoo](https://finance.yahoo.com/quote/XLV/) |
| **XLP** | BUY | 13% | Limit 0.5% below market | 8.6% below entry | 3.6% above entry | 16.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLP) / [Yahoo](https://finance.yahoo.com/quote/XLP/) |
| **XLE** | BUY | 23% | Limit 0.5% below market | 15.1% below entry | 6.4% above entry | 9.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

# WINNING Strategy: systematic_sector_rotation

> **What it does:** Rank 11 GICS sectors by 3-month relative strength vs SPY, long top 3
>
> **Hypothesis:** Systematic Sector Rotation — gap audit strategy

**Generated:** 2026-04-13T13:37:01.036557
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 24.65%
- **sharpe_ratio:** 0.33
- **max_drawdown:** -17.21%
- **win_rate:** 53.26%
- **alpha:** -15.48%

## Risk Parameters
- **max_portfolio_allocation:** 5.5%
- **stop_loss:** 17.2%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 17.2%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy 0.5% below market in uptrend.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **XLK** | BUY | 26% | Limit 0.5% below market | 18.9% below entry | 5.5% above entry | 5.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLK) / [Yahoo](https://finance.yahoo.com/quote/XLK/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 9.1% below entry | 3.0% above entry | 10.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **IEF** | BUY | 6% | Limit 0.5% below market | 8.6% below entry | 3.0% above entry | 11.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEF) / [Yahoo](https://finance.yahoo.com/quote/IEF/) |
| **XLV** | BUY | 15% | Limit 0.5% below market | 11.1% below entry | 3.2% above entry | 8.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLV) / [Yahoo](https://finance.yahoo.com/quote/XLV/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

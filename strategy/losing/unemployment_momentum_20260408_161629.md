# LOSING Strategy: unemployment_momentum

> **What it does:** Staffing stock weakness as unemployment proxy, rotate to defensives
>
> **Hypothesis:** Unemployment Claims Momentum 3Y

**Generated:** 2026-04-08T16:16:29.255382
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -11.38%
- **sharpe_ratio:** -0.66
- **max_drawdown:** -25.01%
- **win_rate:** 52.26%
- **alpha:** -12.62%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 25.0%
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
| **SPY** | BUY | 17% | Limit 0.5% below market | 17.9% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 13.2% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **XLP** | BUY | 13% | Limit 0.5% below market | 13.5% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLP) / [Yahoo](https://finance.yahoo.com/quote/XLP/) |
| **XLV** | BUY | 15% | Limit 0.5% below market | 16.1% below entry | 3.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLV) / [Yahoo](https://finance.yahoo.com/quote/XLV/) |
| **XLU** | BUY | 16% | Limit 0.5% below market | 16.5% below entry | 3.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLU) / [Yahoo](https://finance.yahoo.com/quote/XLU/) |
| **IEF** | BUY | 6% | Limit 0.5% below market | 12.5% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEF) / [Yahoo](https://finance.yahoo.com/quote/IEF/) |
| **VNQ** | BUY | 15% | Limit 0.5% below market | 15.8% below entry | 3.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VNQ) / [Yahoo](https://finance.yahoo.com/quote/VNQ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.66 (target > 0.5)
- Max drawdown: -25.01% (target > -20%)
- Alpha: -12.62% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
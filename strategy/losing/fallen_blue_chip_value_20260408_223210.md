# LOSING Strategy: fallen_blue_chip_value

> **What it does:** Once-great blue chips at deep discounts: turnaround catalysts + dividend income
>
> **Hypothesis:** Fallen Blue Chip Value 3Y

**Generated:** 2026-04-08T22:32:09.955023
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -14.37%
- **sharpe_ratio:** -0.54
- **max_drawdown:** -25.59%
- **win_rate:** 48.01%
- **alpha:** -13.72%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 25.6%
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
| **MDT** | BUY | 20% | Limit 0.5% below market | 21.3% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MDT) / [Yahoo](https://finance.yahoo.com/quote/MDT/) |
| **WMT** | BUY | 23% | Limit 0.5% below market | 24.4% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WMT) / [Yahoo](https://finance.yahoo.com/quote/WMT/) |
| **PFE** | BUY | 25% | Limit 0.5% below market | 25.8% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PFE) / [Yahoo](https://finance.yahoo.com/quote/PFE/) |
| **INTC** | BUY | 64% | Market order (volatile) | 40.0% below entry | 13.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=INTC) / [Yahoo](https://finance.yahoo.com/quote/INTC/) |
| **TGT** | BUY | 36% | Market order (volatile) | 37.7% below entry | 7.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TGT) / [Yahoo](https://finance.yahoo.com/quote/TGT/) |
| **NKE** | BUY | 40% | Market order (volatile) | 40.0% below entry | 8.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NKE) / [Yahoo](https://finance.yahoo.com/quote/NKE/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.54 (target > 0.5)
- Max drawdown: -25.59% (target > -20%)
- Alpha: -13.72% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
# LOSING Strategy: commodity_supercycle

> **What it does:** Ride multi-commodity momentum when commodities outperform stocks
>
> **Hypothesis:** Commodity Supercycle

**Generated:** 2026-04-12T18:43:44.418439
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -8.15%
- **sharpe_ratio:** -0.59
- **max_drawdown:** -22.61%
- **win_rate:** 51.26%
- **alpha:** -25.93%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 22.6%
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
| **DJP** | BUY | 17% | Limit 0.5% below market | 18.3% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DJP) / [Yahoo](https://finance.yahoo.com/quote/DJP/) |
| **SCCO** | BUY | 43% | Market order (volatile) | 40.0% below entry | 9.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCCO) / [Yahoo](https://finance.yahoo.com/quote/SCCO/) |
| **MOO** | BUY | 16% | Limit 0.5% below market | 16.6% below entry | 3.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MOO) / [Yahoo](https://finance.yahoo.com/quote/MOO/) |
| **NTR** | BUY | 29% | Limit 0.5% below market | 30.6% below entry | 6.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NTR) / [Yahoo](https://finance.yahoo.com/quote/NTR/) |
| **XME** | BUY | 32% | Market order (volatile) | 34.0% below entry | 6.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XME) / [Yahoo](https://finance.yahoo.com/quote/XME/) |
| **SLV** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SLV) / [Yahoo](https://finance.yahoo.com/quote/SLV/) |
| **COPX** | BUY | 39% | Market order (volatile) | 40.0% below entry | 8.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=COPX) / [Yahoo](https://finance.yahoo.com/quote/COPX/) |
| **GSG** | BUY | 20% | Limit 0.5% below market | 20.8% below entry | 4.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GSG) / [Yahoo](https://finance.yahoo.com/quote/GSG/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **FCX** | BUY | 45% | Market order (volatile) | 40.0% below entry | 9.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=FCX) / [Yahoo](https://finance.yahoo.com/quote/FCX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.59 (target > 0.5)
- Max drawdown: -22.61% (target > -20%)
- Alpha: -25.93% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
# LOSING Strategy: all_weather_modern

> **What it does:** Updated Dalio All-Weather: reduced bonds, added TIPS + crypto exposure
>
> **Hypothesis:** All-Weather Modern (2026) 3Y

**Generated:** 2026-04-08T14:18:36.475628
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 2.12%
- **sharpe_ratio:** -0.84
- **max_drawdown:** -7.15%
- **win_rate:** 50.53%
- **alpha:** -7.96%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 8.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 7.2%
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
| **SHY** | BUY | 2% | Limit 0.5% below market | 4.3% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **TIP** | BUY | 4% | Limit 0.5% below market | 4.3% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TIP) / [Yahoo](https://finance.yahoo.com/quote/TIP/) |
| **VTI** | BUY | 17% | Limit 0.5% below market | 6.2% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VTI) / [Yahoo](https://finance.yahoo.com/quote/VTI/) |
| **XLE** | BUY | 23% | Limit 0.5% below market | 8.2% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |
| **IEF** | BUY | 6% | Limit 0.5% below market | 4.3% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEF) / [Yahoo](https://finance.yahoo.com/quote/IEF/) |
| **COIN** | BUY | 79% | Market order (volatile) | 25.7% below entry | 15.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=COIN) / [Yahoo](https://finance.yahoo.com/quote/COIN/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 4.5% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.84 (target > 0.5)
- Max drawdown: -7.15% (target > -20%)
- Alpha: -7.96% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
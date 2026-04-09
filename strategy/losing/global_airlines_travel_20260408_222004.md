# LOSING Strategy: global_airlines_travel

> **What it does:** Airlines and OTAs: DAL, UAL, BKNG, ABNB — post-pandemic travel demand
>
> **Hypothesis:** Global Airlines & Travel 3Y

**Generated:** 2026-04-08T22:20:03.202656
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -29.54%
- **sharpe_ratio:** -0.70
- **max_drawdown:** -52.47%
- **win_rate:** 49.47%
- **alpha:** -19.72%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 52.5%
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
| **EXPE** | BUY | 45% | Market order (volatile) | 40.0% below entry | 9.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EXPE) / [Yahoo](https://finance.yahoo.com/quote/EXPE/) |
| **JBLU** | BUY | 69% | Market order (volatile) | 40.0% below entry | 14.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JBLU) / [Yahoo](https://finance.yahoo.com/quote/JBLU/) |
| **UAL** | BUY | 53% | Market order (volatile) | 40.0% below entry | 11.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UAL) / [Yahoo](https://finance.yahoo.com/quote/UAL/) |
| **BKNG** | BUY | 30% | Market order (volatile) | 31.6% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BKNG) / [Yahoo](https://finance.yahoo.com/quote/BKNG/) |
| **LUV** | BUY | 42% | Market order (volatile) | 40.0% below entry | 8.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LUV) / [Yahoo](https://finance.yahoo.com/quote/LUV/) |
| **ABNB** | BUY | 36% | Market order (volatile) | 38.2% below entry | 7.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ABNB) / [Yahoo](https://finance.yahoo.com/quote/ABNB/) |
| **TCOM** | BUY | 44% | Market order (volatile) | 40.0% below entry | 9.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TCOM) / [Yahoo](https://finance.yahoo.com/quote/TCOM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.70 (target > 0.5)
- Max drawdown: -52.47% (target > -20%)
- Alpha: -19.72% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
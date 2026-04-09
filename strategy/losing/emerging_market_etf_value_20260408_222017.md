# LOSING Strategy: emerging_market_etf_value

> **What it does:** EM country ETFs at value prices: Vietnam, Korea, India, Taiwan, Singapore
>
> **Hypothesis:** Emerging Market ETF Value 3Y

**Generated:** 2026-04-08T22:20:17.023015
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -7.87%
- **sharpe_ratio:** -0.48
- **max_drawdown:** -22.39%
- **win_rate:** 48.67%
- **alpha:** -11.37%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 22.4%
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
| **VNM** | BUY | 27% | Limit 0.5% below market | 28.0% below entry | 5.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VNM) / [Yahoo](https://finance.yahoo.com/quote/VNM/) |
| **EPI** | BUY | 16% | Limit 0.5% below market | 17.2% below entry | 3.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EPI) / [Yahoo](https://finance.yahoo.com/quote/EPI/) |
| **INDA** | BUY | 15% | Limit 0.5% below market | 15.9% below entry | 3.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=INDA) / [Yahoo](https://finance.yahoo.com/quote/INDA/) |
| **EWY** | BUY | 32% | Market order (volatile) | 33.2% below entry | 6.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EWY) / [Yahoo](https://finance.yahoo.com/quote/EWY/) |
| **EWS** | BUY | 18% | Limit 0.5% below market | 18.6% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EWS) / [Yahoo](https://finance.yahoo.com/quote/EWS/) |
| **EEM** | BUY | 19% | Limit 0.5% below market | 19.6% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EEM) / [Yahoo](https://finance.yahoo.com/quote/EEM/) |
| **NU** | BUY | 44% | Market order (volatile) | 40.0% below entry | 9.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NU) / [Yahoo](https://finance.yahoo.com/quote/NU/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.48 (target > 0.5)
- Max drawdown: -22.39% (target > -20%)
- Alpha: -11.37% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
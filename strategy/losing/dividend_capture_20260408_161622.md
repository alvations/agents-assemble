# LOSING Strategy: dividend_capture

> **What it does:** Dividend capture: hold high-yield low-vol stocks, harvest dividends
>
> **Hypothesis:** Dividend Capture (Ex-Date) 3Y

**Generated:** 2026-04-08T16:16:21.911551
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -16.13%
- **sharpe_ratio:** -0.91
- **max_drawdown:** -27.31%
- **win_rate:** 48.67%
- **alpha:** -14.38%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 27.3%
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
| **JNJ** | FLAT | 18% | Limit 0.5% below market | 18.6% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **PG** | FLAT | 18% | Limit 0.5% below market | 19.3% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PG) / [Yahoo](https://finance.yahoo.com/quote/PG/) |
| **KO** | FLAT | 16% | Limit 0.5% below market | 17.2% below entry | 3.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KO) / [Yahoo](https://finance.yahoo.com/quote/KO/) |
| **PEP** | FLAT | 21% | Limit 0.5% below market | 21.7% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PEP) / [Yahoo](https://finance.yahoo.com/quote/PEP/) |
| **MCD** | FLAT | 18% | Limit 0.5% below market | 19.0% below entry | 3.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MCD) / [Yahoo](https://finance.yahoo.com/quote/MCD/) |
| **MMM** | FLAT | 49% | Market order (volatile) | 40.0% below entry | 10.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MMM) / [Yahoo](https://finance.yahoo.com/quote/MMM/) |
| **ABT** | FLAT | 22% | Limit 0.5% below market | 23.0% below entry | 4.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ABT) / [Yahoo](https://finance.yahoo.com/quote/ABT/) |
| **XOM** | FLAT | 23% | Limit 0.5% below market | 24.5% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **CVX** | FLAT | 23% | Limit 0.5% below market | 24.4% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CVX) / [Yahoo](https://finance.yahoo.com/quote/CVX/) |
| **IBM** | FLAT | 30% | Market order (volatile) | 31.9% below entry | 6.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IBM) / [Yahoo](https://finance.yahoo.com/quote/IBM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.91 (target > 0.5)
- Max drawdown: -27.31% (target > -20%)
- Alpha: -14.38% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
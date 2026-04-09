# LOSING Strategy: dividend_capture

> **What it does:** Dividend capture: hold high-yield low-vol stocks, harvest dividends
>
> **Hypothesis:** Dividend Capture (Ex-Date) — consistency: 17% across 6 windows

**Generated:** 2026-04-09T08:39:32.626074
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -0.75%
- **sharpe_ratio:** -0.40
- **max_drawdown:** -14.52%
- **win_rate:** 49.53%
- **alpha:** -23.38%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 17.4%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 14.5%
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
| **JNJ** | BUY | 18% | Limit 0.5% below market | 13.0% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **KO** | BUY | 16% | Limit 0.5% below market | 12.0% below entry | 3.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KO) / [Yahoo](https://finance.yahoo.com/quote/KO/) |
| **SCHD** | BUY | 14% | Limit 0.5% below market | 10.3% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCHD) / [Yahoo](https://finance.yahoo.com/quote/SCHD/) |
| **VYM** | BUY | 14% | Limit 0.5% below market | 10.1% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VYM) / [Yahoo](https://finance.yahoo.com/quote/VYM/) |
| **HDV** | BUY | 12% | Limit 0.5% below market | 8.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HDV) / [Yahoo](https://finance.yahoo.com/quote/HDV/) |
| **IBM** | BUY | 30% | Market order (volatile) | 22.2% below entry | 6.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IBM) / [Yahoo](https://finance.yahoo.com/quote/IBM/) |
| **MCD** | BUY | 18% | Limit 0.5% below market | 13.2% below entry | 3.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MCD) / [Yahoo](https://finance.yahoo.com/quote/MCD/) |
| **XOM** | BUY | 24% | Limit 0.5% below market | 17.2% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **VZ** | BUY | 22% | Limit 0.5% below market | 16.4% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VZ) / [Yahoo](https://finance.yahoo.com/quote/VZ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.40 (target > 0.5)
- Max drawdown: -14.52% (target > -20%)
- Alpha: -23.38% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
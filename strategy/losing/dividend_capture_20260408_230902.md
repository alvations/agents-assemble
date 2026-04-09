# LOSING Strategy: dividend_capture

> **What it does:** Dividend capture: hold high-yield low-vol stocks, harvest dividends
>
> **Hypothesis:** Dividend Capture (Ex-Date) 4Y (2022-2025)

**Generated:** 2026-04-08T23:09:02.244122
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -13.78%
- **sharpe_ratio:** -0.69
- **max_drawdown:** -27.31%
- **win_rate:** 49.20%
- **alpha:** -14.52%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 27.3%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: Always hold for income (DCA on rebalance). STRONG BUY: On price dip to SMA200 — yield expands, lock in higher income rate.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **JNJ** | BUY | 18% | Limit 0.5% below market | 18.6% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **KO** | BUY | 16% | Limit 0.5% below market | 17.2% below entry | 3.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KO) / [Yahoo](https://finance.yahoo.com/quote/KO/) |
| **MCD** | BUY | 18% | Limit 0.5% below market | 19.0% below entry | 3.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MCD) / [Yahoo](https://finance.yahoo.com/quote/MCD/) |
| **SCHD** | BUY | 14% | Limit 0.5% below market | 14.8% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCHD) / [Yahoo](https://finance.yahoo.com/quote/SCHD/) |
| **VYM** | BUY | 14% | Limit 0.5% below market | 14.4% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VYM) / [Yahoo](https://finance.yahoo.com/quote/VYM/) |
| **VZ** | BUY | 22% | Limit 0.5% below market | 23.5% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VZ) / [Yahoo](https://finance.yahoo.com/quote/VZ/) |
| **HDV** | BUY | 12% | Limit 0.5% below market | 12.5% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HDV) / [Yahoo](https://finance.yahoo.com/quote/HDV/) |
| **IBM** | BUY | 30% | Market order (volatile) | 31.9% below entry | 6.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IBM) / [Yahoo](https://finance.yahoo.com/quote/IBM/) |
| **XOM** | BUY | 23% | Limit 0.5% below market | 24.5% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.69 (target > 0.5)
- Max drawdown: -27.31% (target > -20%)
- Alpha: -14.52% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
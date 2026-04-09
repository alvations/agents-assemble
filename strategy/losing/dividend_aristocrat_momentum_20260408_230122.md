# LOSING Strategy: dividend_aristocrat_momentum

> **What it does:** Quality dividends + momentum: only buy Aristocrats in uptrends
>
> **Hypothesis:** Dividend Aristocrat Momentum 4Y (2022-2025)

**Generated:** 2026-04-08T23:01:22.785750
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -3.14%
- **sharpe_ratio:** -0.38
- **max_drawdown:** -15.48%
- **win_rate:** 51.40%
- **alpha:** -11.66%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 18.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 15.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When trend leaders above SMA50 > SMA200 (golden cross). STRONG BUY: On RSI pullback to 40-55 in confirmed uptrend — ride the trend, don't fight it.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **ECL** | BUY | 20% | Limit 0.5% below market | 15.8% below entry | 4.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ECL) / [Yahoo](https://finance.yahoo.com/quote/ECL/) |
| **WMT** | BUY | 23% | Limit 0.5% below market | 18.1% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WMT) / [Yahoo](https://finance.yahoo.com/quote/WMT/) |
| **XOM** | BUY | 23% | Limit 0.5% below market | 18.2% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **PEP** | BUY | 21% | Limit 0.5% below market | 16.2% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PEP) / [Yahoo](https://finance.yahoo.com/quote/PEP/) |
| **JNJ** | BUY | 18% | Limit 0.5% below market | 13.9% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **MRK** | BUY | 27% | Limit 0.5% below market | 21.3% below entry | 5.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MRK) / [Yahoo](https://finance.yahoo.com/quote/MRK/) |
| **MCD** | BUY | 18% | Limit 0.5% below market | 14.1% below entry | 3.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MCD) / [Yahoo](https://finance.yahoo.com/quote/MCD/) |
| **NEE** | BUY | 26% | Limit 0.5% below market | 20.6% below entry | 5.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NEE) / [Yahoo](https://finance.yahoo.com/quote/NEE/) |
| **EMR** | BUY | 31% | Market order (volatile) | 23.9% below entry | 6.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EMR) / [Yahoo](https://finance.yahoo.com/quote/EMR/) |
| **LOW** | BUY | 25% | Limit 0.5% below market | 19.2% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LOW) / [Yahoo](https://finance.yahoo.com/quote/LOW/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.38 (target > 0.5)
- Max drawdown: -15.48% (target > -20%)
- Alpha: -11.66% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
# LOSING Strategy: earnings_surprise_drift

> **What it does:** PEAD proxy: buy after >3% gap-up on 2x volume, ride drift 20-60 days
>
> **Hypothesis:** Earnings Surprise Drift — composite: 0.00, consistency: 0%

**Generated:** 2026-04-09T09:35:24.677080
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 7.40%
- **sharpe_ratio:** -0.53
- **max_drawdown:** -2.61%
- **win_rate:** 7.86%
- **alpha:** -20.71%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 3.1%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 2.6%
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
| **AAPL** | FLAT | 29% | Limit 0.5% below market | 3.8% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **MSFT** | FLAT | 24% | Limit 0.5% below market | 3.2% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **NVDA** | FLAT | 49% | Market order (volatile) | 6.4% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **GOOGL** | FLAT | 30% | Limit 0.5% below market | 3.9% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | FLAT | 33% | Market order (volatile) | 4.3% below entry | 6.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **META** | FLAT | 36% | Market order (volatile) | 4.8% below entry | 7.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **TSLA** | FLAT | 62% | Market order (volatile) | 8.2% below entry | 13.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TSLA) / [Yahoo](https://finance.yahoo.com/quote/TSLA/) |
| **JPM** | FLAT | 26% | Limit 0.5% below market | 3.4% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **V** | FLAT | 22% | Limit 0.5% below market | 2.9% below entry | 4.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |
| **UNH** | FLAT | 43% | Market order (volatile) | 5.7% below entry | 9.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UNH) / [Yahoo](https://finance.yahoo.com/quote/UNH/) |
| **LLY** | FLAT | 38% | Market order (volatile) | 5.0% below entry | 8.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LLY) / [Yahoo](https://finance.yahoo.com/quote/LLY/) |
| **AVGO** | FLAT | 55% | Market order (volatile) | 7.2% below entry | 11.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AVGO) / [Yahoo](https://finance.yahoo.com/quote/AVGO/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.53 (target > 0.5)
- Max drawdown: -2.61% (target > -20%)
- Alpha: -20.71% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
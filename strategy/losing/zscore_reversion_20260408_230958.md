# LOSING Strategy: zscore_reversion

> **What it does:** Buy at Z < -2 (statistically oversold), sell at Z > 0
>
> **Hypothesis:** Z-Score Mean Reversion 4Y (2022-2025)

**Generated:** 2026-04-08T23:09:58.174383
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 7.27%
- **sharpe_ratio:** -0.28
- **max_drawdown:** -5.61%
- **win_rate:** 45.01%
- **alpha:** -9.09%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 6.7%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 5.6%
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
| **AAPL** | FLAT | 29% | Limit 0.5% below market | 8.1% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **MSFT** | FLAT | 24% | Limit 0.5% below market | 6.9% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **GOOGL** | FLAT | 30% | Limit 0.5% below market | 8.4% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | FLAT | 33% | Market order (volatile) | 9.2% below entry | 6.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **NVDA** | FLAT | 49% | Market order (volatile) | 13.8% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **META** | FLAT | 36% | Market order (volatile) | 10.2% below entry | 7.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **JPM** | FLAT | 25% | Limit 0.5% below market | 7.2% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **V** | FLAT | 22% | Limit 0.5% below market | 6.1% below entry | 4.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |
| **UNH** | FLAT | 43% | Market order (volatile) | 12.2% below entry | 9.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UNH) / [Yahoo](https://finance.yahoo.com/quote/UNH/) |
| **JNJ** | FLAT | 18% | Limit 0.5% below market | 5.0% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **PG** | FLAT | 18% | Limit 0.5% below market | 5.2% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PG) / [Yahoo](https://finance.yahoo.com/quote/PG/) |
| **KO** | FLAT | 16% | Limit 0.5% below market | 4.6% below entry | 3.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KO) / [Yahoo](https://finance.yahoo.com/quote/KO/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.28 (target > 0.5)
- Max drawdown: -5.61% (target > -20%)
- Alpha: -9.09% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
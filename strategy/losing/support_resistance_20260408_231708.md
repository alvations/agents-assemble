# LOSING Strategy: support_resistance

> **What it does:** Breakout trading on commodity ETFs with defined S/R levels and ATR stops
>
> **Hypothesis:** Support/Resistance Commodity 4Y (2022-2025)

**Generated:** 2026-04-08T23:17:08.096094
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 4.37%
- **sharpe_ratio:** -0.10
- **max_drawdown:** -32.28%
- **win_rate:** 47.90%
- **alpha:** -9.79%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 32.3%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When holdings above SMA200 on weekly rebalance. STRONG BUY: On RSI pullback to 35-50 in confirmed uptrend — buy the dip in quality.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **XLE** | BUY | 23% | Limit 0.5% below market | 23.8% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **CPER** | BUY | 31% | Market order (volatile) | 33.0% below entry | 6.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CPER) / [Yahoo](https://finance.yahoo.com/quote/CPER/) |
| **SLV** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SLV) / [Yahoo](https://finance.yahoo.com/quote/SLV/) |
| **NEM** | BUY | 41% | Market order (volatile) | 40.0% below entry | 8.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NEM) / [Yahoo](https://finance.yahoo.com/quote/NEM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.10 (target > 0.5)
- Max drawdown: -32.28% (target > -20%)
- Alpha: -9.79% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
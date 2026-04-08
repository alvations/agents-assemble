# LOSING Strategy: support_resistance

> **What it does:** Breakout trading on commodity ETFs with defined S/R levels and ATR stops
>
> **Hypothesis:** Support/Resistance Commodity 3Y

**Generated:** 2026-04-08T15:54:18.910803
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 0.21%
- **sharpe_ratio:** -0.17
- **max_drawdown:** -32.28%
- **win_rate:** 46.01%
- **alpha:** -8.59%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 32.3%
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
| **DBA** | BUY | 13% | Limit 0.5% below market | 13.9% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DBA) / [Yahoo](https://finance.yahoo.com/quote/DBA/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **UNG** | BUY | 62% | Market order (volatile) | 40.0% below entry | 13.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UNG) / [Yahoo](https://finance.yahoo.com/quote/UNG/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.17 (target > 0.5)
- Max drawdown: -32.28% (target > -20%)
- Alpha: -8.59% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
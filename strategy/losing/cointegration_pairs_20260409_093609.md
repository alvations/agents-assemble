# LOSING Strategy: cointegration_pairs

> **What it does:** Long laggard in cointegrated pairs when spread Z > 2
>
> **Hypothesis:** Cointegration Pairs Trading — composite: 0.00, consistency: 8%

**Generated:** 2026-04-09T09:36:09.200695
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 6.21%
- **sharpe_ratio:** -0.47
- **max_drawdown:** -6.16%
- **win_rate:** 48.60%
- **alpha:** -21.09%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 7.4%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 6.2%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** WAIT FOR SIGNAL: Only enter when price spread between paired stocks reaches extreme levels. Exit when spread normalizes.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **UPS** | BUY | 30% | Market order (volatile) | 9.3% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UPS) / [Yahoo](https://finance.yahoo.com/quote/UPS/) |
| **PG** | BUY | 18% | Limit 0.5% below market | 5.7% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PG) / [Yahoo](https://finance.yahoo.com/quote/PG/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.47 (target > 0.5)
- Max drawdown: -6.16% (target > -20%)
- Alpha: -21.09% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
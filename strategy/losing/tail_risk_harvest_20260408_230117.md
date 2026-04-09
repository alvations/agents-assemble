# LOSING Strategy: tail_risk_harvest

> **What it does:** Buy quality names after sharp single-day drops, capture mean-reversion
>
> **Hypothesis:** Tail Risk Harvest (Buy Crashes) 4Y (2022-2025)

**Generated:** 2026-04-08T23:01:17.212272
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 0.44%
- **sharpe_ratio:** -0.37
- **max_drawdown:** -16.87%
- **win_rate:** 41.62%
- **alpha:** -10.76%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 20.2%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 16.9%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Enter on any weekly rebalance day. Monitor SMA200 for trend confirmation.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **NVDA** | BUY | 49% | Market order (volatile) | 40.0% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 25.4% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.37 (target > 0.5)
- Max drawdown: -16.87% (target > -20%)
- Alpha: -10.76% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
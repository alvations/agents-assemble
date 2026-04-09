# LOSING Strategy: patent_cliff_pharma

> **What it does:** BMY 7x earnings, PFE post-COVID: market overprices patent cliffs by 2-3x
>
> **Hypothesis:** Patent Cliff Pharma Value — consistency: 50% across 6 windows

**Generated:** 2026-04-09T08:38:30.063127
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 10.05%
- **sharpe_ratio:** -0.01
- **max_drawdown:** -14.10%
- **win_rate:** 51.40%
- **alpha:** -19.87%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 16.9%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 14.1%
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
| **TAK** | BUY | 20% | Limit 0.5% below market | 14.0% below entry | 4.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TAK) / [Yahoo](https://finance.yahoo.com/quote/TAK/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.01 (target > 0.5)
- Max drawdown: -14.10% (target > -20%)
- Alpha: -19.87% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
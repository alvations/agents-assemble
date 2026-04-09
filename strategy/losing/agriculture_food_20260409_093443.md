# LOSING Strategy: agriculture_food

> **What it does:** Fertilizer + agriculture: food crisis beneficiaries
>
> **Hypothesis:** Agriculture & Food Security — composite: 0.06, consistency: 50%

**Generated:** 2026-04-09T09:34:43.369123
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -34.94%
- **sharpe_ratio:** -1.51
- **max_drawdown:** -36.31%
- **win_rate:** 46.74%
- **alpha:** -36.52%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 36.3%
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
| **DBA** | BUY | 13% | Limit 0.5% below market | 13.9% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DBA) / [Yahoo](https://finance.yahoo.com/quote/DBA/) |
| **NTR** | BUY | 29% | Limit 0.5% below market | 30.6% below entry | 6.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NTR) / [Yahoo](https://finance.yahoo.com/quote/NTR/) |
| **MOO** | BUY | 16% | Limit 0.5% below market | 16.6% below entry | 3.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MOO) / [Yahoo](https://finance.yahoo.com/quote/MOO/) |
| **CTVA** | BUY | 25% | Limit 0.5% below market | 26.3% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CTVA) / [Yahoo](https://finance.yahoo.com/quote/CTVA/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -1.51 (target > 0.5)
- Max drawdown: -36.31% (target > -20%)
- Alpha: -36.52% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
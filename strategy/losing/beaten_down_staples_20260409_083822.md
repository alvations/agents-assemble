# LOSING Strategy: beaten_down_staples

> **What it does:** Consumer staples oversold on GLP-1 fears — buy the overreaction, collect dividends
>
> **Hypothesis:** Beaten Down Staples (GLP-1 Fear) — consistency: 50% across 6 windows

**Generated:** 2026-04-09T08:38:22.386685
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 3.24%
- **sharpe_ratio:** -0.24
- **max_drawdown:** -11.61%
- **win_rate:** 48.60%
- **alpha:** -22.06%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 13.9%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 11.6%
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
| **DPZ** | BUY | 28% | Limit 0.5% below market | 16.6% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DPZ) / [Yahoo](https://finance.yahoo.com/quote/DPZ/) |
| **HRL** | BUY | 24% | Limit 0.5% below market | 14.3% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HRL) / [Yahoo](https://finance.yahoo.com/quote/HRL/) |
| **SJM** | BUY | 28% | Limit 0.5% below market | 16.2% below entry | 5.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SJM) / [Yahoo](https://finance.yahoo.com/quote/SJM/) |
| **CPB** | BUY | 27% | Limit 0.5% below market | 16.0% below entry | 5.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CPB) / [Yahoo](https://finance.yahoo.com/quote/CPB/) |
| **CAG** | BUY | 26% | Limit 0.5% below market | 15.1% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CAG) / [Yahoo](https://finance.yahoo.com/quote/CAG/) |
| **MDLZ** | BUY | 22% | Limit 0.5% below market | 12.6% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MDLZ) / [Yahoo](https://finance.yahoo.com/quote/MDLZ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.24 (target > 0.5)
- Max drawdown: -11.61% (target > -20%)
- Alpha: -22.06% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
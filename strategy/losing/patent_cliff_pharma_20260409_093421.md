# LOSING Strategy: patent_cliff_pharma

> **What it does:** BMY 7x earnings, PFE post-COVID: market overprices patent cliffs by 2-3x
>
> **Hypothesis:** Patent Cliff Pharma Value — composite: 0.17, consistency: 75%

**Generated:** 2026-04-09T09:34:21.137589
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
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 46.1% |
| **Avg 5Y Sharpe** | 0.33 |
| **Avg 5Y Max DD** | -16.2% |
| **10Y Return (2015-2024)** | 84.0% |
| **10Y Sharpe** | 0.23 |
| **10Y Max DD** | -16.8% |
| **HODL Composite** | 0.27 |
| **Windows Tested** | 28 |
| **Consistency** | 78% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Trim winners that are up 50%+ to lock in gains
- **Stop loss:** Exit if drawdown exceeds 25% — the strategy may not recover quickly
- **Time limit:** If flat (< 5% return) after 12 months, reassess whether the thesis still holds

</details>

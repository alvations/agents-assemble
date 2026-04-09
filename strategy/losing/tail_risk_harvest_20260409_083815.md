# LOSING Strategy: tail_risk_harvest

> **What it does:** Buy quality names after sharp single-day drops, capture mean-reversion
>
> **Hypothesis:** Tail Risk Harvest (Buy Crashes) — consistency: 33% across 6 windows

**Generated:** 2026-04-09T08:38:15.113783
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 10.73%
- **sharpe_ratio:** -0.03
- **max_drawdown:** -12.12%
- **win_rate:** 39.28%
- **alpha:** -19.66%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 14.5%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 12.1%
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
| **NVDA** | BUY | 49% | Market order (volatile) | 29.7% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 18.3% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.03 (target > 0.5)
- Max drawdown: -12.12% (target > -20%)
- Alpha: -19.66% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 45.7% |
| **Avg 5Y Sharpe** | 0.32 |
| **Avg 5Y Max DD** | -20.0% |
| **10Y Return (2015-2024)** | 90.4% |
| **10Y Sharpe** | 0.28 |
| **10Y Max DD** | -21.7% |
| **HODL Composite** | 0.24 |
| **Windows Tested** | 28 |
| **Consistency** | 67% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Trim 25% at +80%. Rebalance quarterly.
- **Stop loss:** Stop loss at -25% from entry.
- **Exit rule:** Exit if strategy thesis no longer holds.

</details>

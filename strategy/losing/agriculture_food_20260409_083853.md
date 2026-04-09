# LOSING Strategy: agriculture_food

> **What it does:** Fertilizer + agriculture: food crisis beneficiaries
>
> **Hypothesis:** Agriculture & Food Security — consistency: 17% across 6 windows

**Generated:** 2026-04-09T08:38:53.093083
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
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 45.6% |
| **Avg 5Y Sharpe** | 0.25 |
| **Avg 5Y Max DD** | -32.6% |
| **10Y Return (2015-2024)** | 36.5% |
| **10Y Sharpe** | 0.01 |
| **10Y Max DD** | -42.6% |
| **HODL Composite** | 0.11 |
| **Windows Tested** | 28 |
| **Consistency** | 53% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -49% drawdown to return 36% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit only on FUNDAMENTAL deterioration: dividend cuts, moat erosion, management fraud, or regulatory destruction of business model. Price drops alone are NOT exit signals for passive investors.

</details>

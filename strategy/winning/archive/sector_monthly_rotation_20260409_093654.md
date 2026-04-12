# WINNING Strategy: sector_monthly_rotation

> **What it does:** Top 3 of 11 sector ETFs by 3-month momentum. 13.94% CAGR
>
> **Hypothesis:** Sector Monthly Rotation — composite: 0.08, consistency: 67%

**Generated:** 2026-04-09T09:36:54.302329
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 45.33%
- **sharpe_ratio:** 0.74
- **max_drawdown:** -13.20%
- **win_rate:** 52.06%
- **alpha:** -9.81%

## Risk Parameters
- **max_portfolio_allocation:** 8.8%
- **stop_loss:** 15.8%
- **take_profit_target:** 6.7%
- **max_drawdown_tolerance:** 13.2%
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
| **XLV** | BUY | 15% | Limit 0.5% below market | 10.2% below entry | 4.3% above entry | 13.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLV) / [Yahoo](https://finance.yahoo.com/quote/XLV/) |
| **XLP** | BUY | 13% | Limit 0.5% below market | 8.6% below entry | 3.6% above entry | 16.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLP) / [Yahoo](https://finance.yahoo.com/quote/XLP/) |
| **XLE** | BUY | 23% | Limit 0.5% below market | 15.1% below entry | 6.4% above entry | 9.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 13.0% |
| **Avg 5Y Sharpe** | -0.06 |
| **Avg 5Y Max DD** | -23.9% |
| **10Y Return (2015-2024)** | 17.1% |
| **10Y Sharpe** | -0.11 |
| **10Y Max DD** | -27.6% |
| **HODL Composite** | 0.04 |
| **Windows Tested** | 28 |
| **Consistency** | 50% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -28% drawdown to return 17% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit individual ETFs only if they close or change methodology. The rotation framework, not individual ETFs, is the strategy.

</details>

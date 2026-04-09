# WINNING Strategy: dollar_weak_em_strong

> **What it does:** USD weakens → EM stocks + commodities + gold outperform. Inverse dollar-to-EM signal.
>
> **Hypothesis:** Dollar Weak → EM Strong (Currency Rotation) — composite: 0.12, consistency: 58%

**Generated:** 2026-04-09T09:34:28.777033
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 36.75%
- **sharpe_ratio:** 0.85
- **max_drawdown:** -13.03%
- **win_rate:** 57.52%
- **alpha:** -12.09%

## Risk Parameters
- **max_portfolio_allocation:** 14.1%
- **stop_loss:** 15.6%
- **take_profit_target:** 5.5%
- **max_drawdown_tolerance:** 13.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** WAIT FOR SIGNAL: Only enter when US dollar is weakening. Long emerging markets + gold. Exit when dollar strengthens.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **GLD** | BUY | 23% | Limit 0.5% below market | 15.1% below entry | 5.3% above entry | 14.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **EEM** | BUY | 19% | Limit 0.5% below market | 12.5% below entry | 4.4% above entry | 17.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EEM) / [Yahoo](https://finance.yahoo.com/quote/EEM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 58.5% |
| **Avg 5Y Sharpe** | 0.53 |
| **Avg 5Y Max DD** | -11.3% |
| **10Y Return (2015-2024)** | 142.9% |
| **10Y Sharpe** | 0.53 |
| **10Y Max DD** | -13.0% |
| **HODL Composite** | 0.4 |
| **Windows Tested** | 28 |
| **Consistency** | 71% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -13% drawdown to return 143% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit EM/gold overweight when US dollar (UUP) recovers above SMA200. Dollar strength kills EM trade.

</details>

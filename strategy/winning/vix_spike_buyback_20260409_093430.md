# WINNING Strategy: vix_spike_buyback

> **What it does:** Fear spikes → buy companies with massive buyback programs. They buy themselves cheap in panics.
>
> **Hypothesis:** VIX Spike → Cash-Rich Buyback — composite: 0.17, consistency: 83%

**Generated:** 2026-04-09T09:34:30.364495
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 48.72%
- **sharpe_ratio:** 1.14
- **max_drawdown:** -6.88%
- **win_rate:** 56.19%
- **alpha:** -8.93%

## Risk Parameters
- **max_portfolio_allocation:** 19.6%
- **stop_loss:** 8.3%
- **take_profit_target:** 7.1%
- **max_drawdown_tolerance:** 6.9%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** SAFE TO BUY. Even better: add more during market panic — these cash-rich companies buy back their own stock at discount prices.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **AAPL** | BUY | 29% | Limit 0.5% below market | 10.0% below entry | 8.6% above entry | 16.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 10.4% below entry | 8.9% above entry | 15.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **META** | BUY | 36% | Market order (volatile) | 12.6% below entry | 10.8% above entry | 12.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **V** | BUY | 22% | Limit 0.5% below market | 7.5% below entry | 6.5% above entry | 21.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 39.2% |
| **Avg 5Y Sharpe** | 0.32 |
| **Avg 5Y Max DD** | -17.3% |
| **10Y Return (2015-2024)** | 89.8% |
| **10Y Sharpe** | 0.29 |
| **10Y Max DD** | -20.5% |
| **HODL Composite** | 0.32 |
| **Windows Tested** | 28 |
| **Consistency** | 89% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Take profit:** Trim 25% at +80%. Rebalance quarterly.
- **Stop loss:** Stop loss at -25% from entry.
- **Exit rule:** Exit if strategy thesis no longer holds.

</details>

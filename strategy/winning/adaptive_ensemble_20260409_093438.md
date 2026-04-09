# WINNING Strategy: adaptive_ensemble

> **What it does:** Regime-switching: momentum in bulls, defensive in bears, quality in transitions
>
> **Hypothesis:** Adaptive Ensemble — composite: 0.42, consistency: 92%

**Generated:** 2026-04-09T09:34:38.800720
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 84.05%
- **sharpe_ratio:** 1.22
- **max_drawdown:** -13.24%
- **win_rate:** 56.72%
- **alpha:** -0.50%

## Risk Parameters
- **max_portfolio_allocation:** 12.9%
- **stop_loss:** 15.9%
- **take_profit_target:** 11.3%
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
| **GLD** | BUY | 23% | Limit 0.5% below market | 15.3% below entry | 10.9% above entry | 13.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 7.9% below entry | 5.7% above entry | 25.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **VIG** | BUY | 14% | Limit 0.5% below market | 9.2% below entry | 6.5% above entry | 22.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VIG) / [Yahoo](https://finance.yahoo.com/quote/VIG/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 14.5% below entry | 10.3% above entry | 14.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 32.5% below entry | 23.1% above entry | 6.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 16.3% below entry | 11.6% above entry | 12.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 21.8% below entry | 15.5% above entry | 9.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 101.2% |
| **Avg 5Y Sharpe** | 0.81 |
| **Avg 5Y Max DD** | -20.2% |
| **10Y Return (2015-2024)** | 317.2% |
| **10Y Sharpe** | 0.85 |
| **10Y Max DD** | -24.8% |
| **HODL Composite** | 0.92 |
| **Windows Tested** | 28 |
| **Consistency** | 89% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -25% drawdown to return 317% over the long term. Stopping out would have locked in losses.
- **Exit rule:** This strategy returned 317% over 10 years despite -25% max drawdown. Exit if the ensemble model underperforms SPY for 3 consecutive years — the multi-strategy blend has stopped adding value.

</details>

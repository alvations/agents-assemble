# WINNING Strategy: dynamic_ensemble

> **What it does:** Multi-strategy ensemble weighted by rolling Sharpe ratio
>
> **Hypothesis:** Dynamic Ensemble — composite: 0.32, consistency: 92%

**Generated:** 2026-04-09T09:34:59.858523
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 49.08%
- **sharpe_ratio:** 0.88
- **max_drawdown:** -10.87%
- **win_rate:** 55.13%
- **alpha:** -8.84%

## Risk Parameters
- **max_portfolio_allocation:** 11.0%
- **stop_loss:** 13.0%
- **take_profit_target:** 7.1%
- **max_drawdown_tolerance:** 10.9%
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
| **JPM** | BUY | 26% | Limit 0.5% below market | 14.0% below entry | 7.7% above entry | 10.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **V** | BUY | 22% | Limit 0.5% below market | 11.9% below entry | 6.5% above entry | 12.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |
| **ABBV** | BUY | 26% | Limit 0.5% below market | 14.5% below entry | 7.9% above entry | 9.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ABBV) / [Yahoo](https://finance.yahoo.com/quote/ABBV/) |
| **MRK** | BUY | 27% | Limit 0.5% below market | 15.0% below entry | 8.2% above entry | 9.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MRK) / [Yahoo](https://finance.yahoo.com/quote/MRK/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 12.6% below entry | 6.9% above entry | 11.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 17.9% below entry | 9.8% above entry | 8.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **XOM** | BUY | 24% | Limit 0.5% below market | 12.9% below entry | 7.1% above entry | 11.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 15.7% below entry | 8.6% above entry | 9.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 26.7% below entry | 14.6% above entry | 5.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 9.4% below entry | 5.1% above entry | 15.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 16.4% below entry | 9.0% above entry | 8.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 11.9% below entry | 6.5% above entry | 12.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 94.4% |
| **Avg 5Y Sharpe** | 0.71 |
| **Avg 5Y Max DD** | -18.7% |
| **10Y Return (2015-2024)** | 248.2% |
| **10Y Sharpe** | 0.69 |
| **10Y Max DD** | -20.3% |
| **HODL Composite** | 0.81 |
| **Windows Tested** | 28 |
| **Consistency** | 92% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -20% drawdown to return 248% over the long term. Stopping out would have locked in losses.
- **Exit rule:** This strategy returned 248% over 10 years despite -20% max drawdown. Exit if the dynamic allocation model shows negative alpha vs equal-weight for 4 consecutive quarters.

</details>

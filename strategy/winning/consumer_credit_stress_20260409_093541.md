# WINNING Strategy: consumer_credit_stress

> **What it does:** Consumer discretionary vs staples ratio as credit stress indicator
>
> **Hypothesis:** Consumer Credit Stress (Subprime Proxy) — composite: 0.13, consistency: 67%

**Generated:** 2026-04-09T09:35:41.317398
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 32.35%
- **sharpe_ratio:** 0.51
- **max_drawdown:** -16.72%
- **win_rate:** 53.66%
- **alpha:** -13.30%

## Risk Parameters
- **max_portfolio_allocation:** 7.2%
- **stop_loss:** 20.1%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 16.7%
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
| **TLT** | BUY | 13% | Limit 0.5% below market | 10.6% below entry | 3.0% above entry | 13.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 19.3% below entry | 4.8% above entry | 7.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 14.4% below entry | 3.6% above entry | 10.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 18.3% below entry | 4.6% above entry | 7.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **XLY** | BUY | 23% | Limit 0.5% below market | 19.1% below entry | 4.8% above entry | 7.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLY) / [Yahoo](https://finance.yahoo.com/quote/XLY/) |
| **KRE** | BUY | 29% | Limit 0.5% below market | 24.2% below entry | 6.0% above entry | 5.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KRE) / [Yahoo](https://finance.yahoo.com/quote/KRE/) |
| **HYG** | BUY | 5% | Limit 0.5% below market | 10.0% below entry | 3.0% above entry | 14.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HYG) / [Yahoo](https://finance.yahoo.com/quote/HYG/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 46.1% |
| **Avg 5Y Sharpe** | 0.37 |
| **Avg 5Y Max DD** | -20.9% |
| **10Y Return (2015-2024)** | 124.1% |
| **10Y Sharpe** | 0.42 |
| **10Y Max DD** | -23.1% |
| **HODL Composite** | 0.34 |
| **Windows Tested** | 28 |
| **Consistency** | 78% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -23% drawdown to return 124% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit only on FUNDAMENTAL deterioration: dividend cuts, moat erosion, management fraud, or regulatory destruction of business model. Price drops alone are NOT exit signals for passive investors.

</details>

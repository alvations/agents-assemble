# LOSING Strategy: global_consumer_staples

> **What it does:** Global pricing power: Unilever, Nestle, P&G, KO, Deere — income + stability
>
> **Hypothesis:** Global Consumer Staples — consistency: 17% across 6 windows

**Generated:** 2026-04-09T08:37:51.257669
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -3.24%
- **sharpe_ratio:** -0.40
- **max_drawdown:** -16.63%
- **win_rate:** 49.27%
- **alpha:** -24.23%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 20.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 16.6%
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
| **COST** | BUY | 20% | Limit 0.5% below market | 17.1% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=COST) / [Yahoo](https://finance.yahoo.com/quote/COST/) |
| **MKC** | BUY | 25% | Limit 0.5% below market | 21.0% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MKC) / [Yahoo](https://finance.yahoo.com/quote/MKC/) |
| **KO** | BUY | 16% | Limit 0.5% below market | 13.7% below entry | 3.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KO) / [Yahoo](https://finance.yahoo.com/quote/KO/) |
| **CL** | BUY | 21% | Limit 0.5% below market | 17.3% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CL) / [Yahoo](https://finance.yahoo.com/quote/CL/) |
| **UL** | BUY | 20% | Limit 0.5% below market | 16.7% below entry | 4.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UL) / [Yahoo](https://finance.yahoo.com/quote/UL/) |
| **PG** | BUY | 18% | Limit 0.5% below market | 15.5% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PG) / [Yahoo](https://finance.yahoo.com/quote/PG/) |
| **DE** | BUY | 29% | Limit 0.5% below market | 24.1% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DE) / [Yahoo](https://finance.yahoo.com/quote/DE/) |
| **NVO** | BUY | 49% | Market order (volatile) | 40.0% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVO) / [Yahoo](https://finance.yahoo.com/quote/NVO/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.40 (target > 0.5)
- Max drawdown: -16.63% (target > -20%)
- Alpha: -24.23% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 49.2% |
| **Avg 5Y Sharpe** | 0.37 |
| **Avg 5Y Max DD** | -18.8% |
| **10Y Return (2015-2024)** | 101.1% |
| **10Y Sharpe** | 0.33 |
| **10Y Max DD** | -20.8% |
| **HODL Composite** | 0.28 |
| **Windows Tested** | 28 |
| **Consistency** | 71% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -21% drawdown to return 101% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit only on FUNDAMENTAL deterioration: dividend cuts, moat erosion, management fraud, or regulatory destruction of business model. Price drops alone are NOT exit signals for passive investors.

</details>

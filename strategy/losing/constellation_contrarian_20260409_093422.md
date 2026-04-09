# LOSING Strategy: constellation_contrarian

> **What it does:** STZ 49.8% DCF discount, EFX 34%, NKE permanent moat — most mispriced wide-moat stocks
>
> **Hypothesis:** Constellation Contrarian (Max DCF Discount) — composite: 0.00, consistency: 33%

**Generated:** 2026-04-09T09:34:22.316834
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -1.87%
- **sharpe_ratio:** -0.19
- **max_drawdown:** -26.51%
- **win_rate:** 48.87%
- **alpha:** -23.76%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 26.5%
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
| **STZ** | BUY | 29% | Limit 0.5% below market | 30.6% below entry | 6.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=STZ) / [Yahoo](https://finance.yahoo.com/quote/STZ/) |
| **SAM** | BUY | 31% | Market order (volatile) | 33.0% below entry | 6.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SAM) / [Yahoo](https://finance.yahoo.com/quote/SAM/) |
| **DEO** | BUY | 29% | Limit 0.5% below market | 30.4% below entry | 6.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DEO) / [Yahoo](https://finance.yahoo.com/quote/DEO/) |
| **NKE** | BUY | 40% | Market order (volatile) | 40.0% below entry | 8.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NKE) / [Yahoo](https://finance.yahoo.com/quote/NKE/) |
| **LULU** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LULU) / [Yahoo](https://finance.yahoo.com/quote/LULU/) |
| **EFX** | BUY | 35% | Market order (volatile) | 36.3% below entry | 7.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EFX) / [Yahoo](https://finance.yahoo.com/quote/EFX/) |
| **PVH** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PVH) / [Yahoo](https://finance.yahoo.com/quote/PVH/) |
| **MNST** | BUY | 24% | Limit 0.5% below market | 25.6% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MNST) / [Yahoo](https://finance.yahoo.com/quote/MNST/) |
| **BUD** | BUY | 24% | Limit 0.5% below market | 25.0% below entry | 5.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BUD) / [Yahoo](https://finance.yahoo.com/quote/BUD/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.19 (target > 0.5)
- Max drawdown: -26.51% (target > -20%)
- Alpha: -23.76% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 33.5% |
| **Avg 5Y Sharpe** | 0.18 |
| **Avg 5Y Max DD** | -35.9% |
| **10Y Return (2015-2024)** | 62.7% |
| **10Y Sharpe** | 0.14 |
| **10Y Max DD** | -40.3% |
| **HODL Composite** | 0.13 |
| **Windows Tested** | 28 |
| **Consistency** | 60% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -40% drawdown to return 63% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit if Modelo loses #1 US beer market share position (currently #1). The turnaround thesis depends on the beer business momentum.

</details>

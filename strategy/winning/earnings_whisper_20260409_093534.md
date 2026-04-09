# WINNING Strategy: earnings_whisper

> **What it does:** Pre-earnings drift: accumulation patterns predict positive surprises
>
> **Hypothesis:** Earnings Whisper (Pre-Drift) — composite: 0.01, consistency: 33%

**Generated:** 2026-04-09T09:35:34.033585
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 29.61%
- **sharpe_ratio:** 0.45
- **max_drawdown:** -10.26%
- **win_rate:** 51.80%
- **alpha:** -14.07%

## Risk Parameters
- **max_portfolio_allocation:** 6.9%
- **stop_loss:** 12.3%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 10.3%
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
| **META** | BUY | 36% | Market order (volatile) | 18.7% below entry | 7.6% above entry | 4.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **JPM** | BUY | 26% | Limit 0.5% below market | 13.2% below entry | 5.4% above entry | 6.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **CRM** | BUY | 33% | Market order (volatile) | 17.2% below entry | 7.0% above entry | 5.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CRM) / [Yahoo](https://finance.yahoo.com/quote/CRM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 24.3% |
| **Avg 5Y Sharpe** | 0.09 |
| **Avg 5Y Max DD** | -22.1% |
| **10Y Return (2015-2024)** | 59.2% |
| **10Y Sharpe** | 0.12 |
| **10Y Max DD** | -28.8% |
| **HODL Composite** | 0.14 |
| **Windows Tested** | 28 |
| **Consistency** | 64% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -29% drawdown to return 59% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit only on FUNDAMENTAL deterioration: dividend cuts, moat erosion, management fraud, or regulatory destruction of business model. Price drops alone are NOT exit signals for passive investors.

</details>

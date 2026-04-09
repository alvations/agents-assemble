# WINNING Strategy: market_making_momentum

> **What it does:** Multi-factor momentum + short-term mean-reversion entry, Citadel-inspired
>
> **Hypothesis:** Market-Making Momentum (Citadel-style) — consistency: 67% across 6 windows

**Generated:** 2026-04-09T08:39:17.037624
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 11.84%
- **sharpe_ratio:** 0.04
- **max_drawdown:** -13.98%
- **win_rate:** 51.93%
- **alpha:** -19.32%

## Risk Parameters
- **max_portfolio_allocation:** 3.3%
- **stop_loss:** 16.8%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 14.0%
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
| **ABBV** | BUY | 26% | Limit 0.5% below market | 18.6% below entry | 5.5% above entry | 2.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ABBV) / [Yahoo](https://finance.yahoo.com/quote/ABBV/) |
| **JPM** | BUY | 26% | Limit 0.5% below market | 18.0% below entry | 5.4% above entry | 3.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **XOM** | BUY | 24% | Limit 0.5% below market | 16.6% below entry | 4.9% above entry | 3.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **GS** | BUY | 31% | Market order (volatile) | 22.1% below entry | 6.6% above entry | 2.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GS) / [Yahoo](https://finance.yahoo.com/quote/GS/) |
| **TSLA** | BUY | 62% | Market order (volatile) | 40.0% below entry | 13.1% above entry | 1.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TSLA) / [Yahoo](https://finance.yahoo.com/quote/TSLA/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 34.3% below entry | 10.2% above entry | 1.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **CVX** | BUY | 23% | Limit 0.5% below market | 16.5% below entry | 4.9% above entry | 3.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CVX) / [Yahoo](https://finance.yahoo.com/quote/CVX/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 12.1% below entry | 3.6% above entry | 4.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 21.1% below entry | 6.3% above entry | 2.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 30.2% |
| **Avg 5Y Sharpe** | 0.15 |
| **Avg 5Y Max DD** | -21.9% |
| **10Y Return (2015-2024)** | 65.3% |
| **10Y Sharpe** | 0.15 |
| **10Y Max DD** | -23.4% |
| **HODL Composite** | 0.15 |
| **Windows Tested** | 28 |
| **Consistency** | 60% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Rebalance when any position exceeds 2x its target weight. Trim back to target, redeploy to underweight positions.
- **Stop loss:** NO price-based stop loss. This strategy recovered from -23% drawdown to return 65% over the long term. Stopping out would have locked in losses.
- **Exit rule:** Exit only on FUNDAMENTAL deterioration: dividend cuts, moat erosion, management fraud, or regulatory destruction of business model. Price drops alone are NOT exit signals for passive investors.

</details>

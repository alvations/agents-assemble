# WINNING Strategy: staples_hedged_growth

> **What it does:** Growth core + consumer staples/dividend hedge + gold/bond buffer
>
> **Hypothesis:** Staples-Hedged Growth — composite: 0.39, consistency: 92%

**Generated:** 2026-04-09T09:34:37.553361
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 87.77%
- **sharpe_ratio:** 1.64
- **max_drawdown:** -9.99%
- **win_rate:** 56.72%
- **alpha:** 0.33%

## Risk Parameters
- **max_portfolio_allocation:** 17.3%
- **stop_loss:** 12.0%
- **take_profit_target:** 11.7%
- **max_drawdown_tolerance:** 10.0%
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
| **GLD** | BUY | 23% | Limit 0.5% below market | 11.6% below entry | 11.3% above entry | 17.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 6.0% below entry | 5.9% above entry | 34.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 24.5% below entry | 24.0% above entry | 8.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 14.4% below entry | 14.1% above entry | 14.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **XLP** | BUY | 13% | Limit 0.5% below market | 6.5% below entry | 6.4% above entry | 31.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLP) / [Yahoo](https://finance.yahoo.com/quote/XLP/) |
| **PG** | BUY | 18% | Limit 0.5% below market | 9.3% below entry | 9.1% above entry | 22.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PG) / [Yahoo](https://finance.yahoo.com/quote/PG/) |
| **KO** | BUY | 16% | Limit 0.5% below market | 8.2% below entry | 8.1% above entry | 25.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KO) / [Yahoo](https://finance.yahoo.com/quote/KO/) |
| **WMT** | BUY | 23% | Limit 0.5% below market | 11.8% below entry | 11.5% above entry | 17.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WMT) / [Yahoo](https://finance.yahoo.com/quote/WMT/) |
| **COST** | BUY | 20% | Limit 0.5% below market | 10.3% below entry | 10.1% above entry | 20.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=COST) / [Yahoo](https://finance.yahoo.com/quote/COST/) |
| **PEP** | BUY | 21% | Limit 0.5% below market | 10.4% below entry | 10.2% above entry | 19.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PEP) / [Yahoo](https://finance.yahoo.com/quote/PEP/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 15.1% below entry | 14.8% above entry | 13.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 16.5% below entry | 16.1% above entry | 12.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **META** | BUY | 36% | Market order (volatile) | 18.2% below entry | 17.8% above entry | 11.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 103.2% |
| **Avg 5Y Sharpe** | 0.9 |
| **Avg 5Y Max DD** | -18.5% |
| **10Y Return (2015-2024)** | 319.2% |
| **10Y Sharpe** | 0.94 |
| **10Y Max DD** | -21.6% |
| **HODL Composite** | 0.99 |
| **Windows Tested** | 28 |
| **Consistency** | 92% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Exit rule:** Exit if growth rate turns negative for 2+ quarters. Trim winners at +100%. Cut losers at -30%.

</details>

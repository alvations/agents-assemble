# WINNING Strategy: yield_curve_inversion

> **What it does:** TLT/SHY ratio proxy for yield curve: go defensive on flattening
>
> **Hypothesis:** Yield Curve Inversion Signal — composite: 0.25, consistency: 92%

**Generated:** 2026-04-09T09:35:40.872866
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 65.81%
- **sharpe_ratio:** 1.20
- **max_drawdown:** -13.45%
- **win_rate:** 55.79%
- **alpha:** -4.70%

## Risk Parameters
- **max_portfolio_allocation:** 13.5%
- **stop_loss:** 16.1%
- **take_profit_target:** 9.2%
- **max_drawdown_tolerance:** 13.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** SAFE TO BUY. Even better: add more when interest rates are rising — banks earn wider margins on loans.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SPY** | BUY | 17% | Limit 0.5% below market | 11.6% below entry | 6.6% above entry | 18.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 8.5% below entry | 4.9% above entry | 25.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 15.6% below entry | 8.9% above entry | 14.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **IEF** | BUY | 6% | Limit 0.5% below market | 8.1% below entry | 4.6% above entry | 27.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IEF) / [Yahoo](https://finance.yahoo.com/quote/IEF/) |
| **XLP** | BUY | 13% | Limit 0.5% below market | 8.8% below entry | 5.0% above entry | 25.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLP) / [Yahoo](https://finance.yahoo.com/quote/XLP/) |
| **XLV** | BUY | 15% | Limit 0.5% below market | 10.4% below entry | 5.9% above entry | 21.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLV) / [Yahoo](https://finance.yahoo.com/quote/XLV/) |
| **XLU** | BUY | 16% | Limit 0.5% below market | 10.6% below entry | 6.1% above entry | 20.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLU) / [Yahoo](https://finance.yahoo.com/quote/XLU/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 54.3% |
| **Avg 5Y Sharpe** | 0.49 |
| **Avg 5Y Max DD** | -17.6% |
| **10Y Return (2015-2024)** | 105.3% |
| **10Y Sharpe** | 0.36 |
| **10Y Max DD** | -21.0% |
| **HODL Composite** | 0.35 |
| **Windows Tested** | 28 |
| **Consistency** | 82% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Take profit:** Trim 25% at +80%. Rebalance quarterly.
- **Stop loss:** Stop loss at -25% from entry.
- **Exit rule:** Exit if strategy thesis no longer holds.

</details>

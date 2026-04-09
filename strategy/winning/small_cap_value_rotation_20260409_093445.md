# WINNING Strategy: small_cap_value_rotation

> **What it does:** Small caps at 50-year cheap: AVUV + momentum picks, 18% YTD 2026
>
> **Hypothesis:** Small Cap Value Rotation — composite: 0.14, consistency: 67%

**Generated:** 2026-04-09T09:34:45.358427
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 22.17%
- **sharpe_ratio:** 0.25
- **max_drawdown:** -27.46%
- **win_rate:** 50.60%
- **alpha:** -16.20%

## Risk Parameters
- **max_portfolio_allocation:** 4.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 27.5%
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
| **DECK** | BUY | 50% | Market order (volatile) | 40.0% below entry | 10.4% above entry | 1.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DECK) / [Yahoo](https://finance.yahoo.com/quote/DECK/) |
| **AVUV** | BUY | 23% | Limit 0.5% below market | 23.7% below entry | 4.7% above entry | 4.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AVUV) / [Yahoo](https://finance.yahoo.com/quote/AVUV/) |
| **DFSV** | BUY | 22% | Limit 0.5% below market | 23.5% below entry | 4.7% above entry | 4.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DFSV) / [Yahoo](https://finance.yahoo.com/quote/DFSV/) |
| **VBR** | BUY | 19% | Limit 0.5% below market | 20.1% below entry | 4.0% above entry | 4.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VBR) / [Yahoo](https://finance.yahoo.com/quote/VBR/) |
| **SAIA** | BUY | 57% | Market order (volatile) | 40.0% below entry | 12.0% above entry | 1.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SAIA) / [Yahoo](https://finance.yahoo.com/quote/SAIA/) |
| **GRC** | BUY | 30% | Market order (volatile) | 32.0% below entry | 6.4% above entry | 3.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GRC) / [Yahoo](https://finance.yahoo.com/quote/GRC/) |
| **IWM** | BUY | 22% | Limit 0.5% below market | 23.4% below entry | 4.7% above entry | 4.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWM) / [Yahoo](https://finance.yahoo.com/quote/IWM/) |
| **IWN** | BUY | 21% | Limit 0.5% below market | 22.4% below entry | 4.5% above entry | 4.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWN) / [Yahoo](https://finance.yahoo.com/quote/IWN/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 98.6% |
| **Avg 5Y Sharpe** | 0.59 |
| **Avg 5Y Max DD** | -31.7% |
| **10Y Return (2015-2024)** | 188.0% |
| **10Y Sharpe** | 0.47 |
| **10Y Max DD** | -37.9% |
| **HODL Composite** | 0.52 |
| **Windows Tested** | 28 |
| **Consistency** | 78% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Take profit:** If any single position doubles (+100%), trim half and let the rest ride
- **Stop loss:** If the overall strategy drawdown exceeds 40%, reduce all positions by 50%
- **Full exit:** If 3+ positions hit their individual stop losses within the same month, exit entirely and reassess

</details>

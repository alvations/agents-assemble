# WINNING Strategy: credit_spread_trade

> **What it does:** Rotate high yield vs investment grade based on credit spread regime
>
> **Hypothesis:** Credit Spread Trade — gap audit strategy

**Generated:** 2026-04-13T13:38:29.895466
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 13.53%
- **sharpe_ratio:** 0.09
- **max_drawdown:** -4.87%
- **win_rate:** 52.60%
- **alpha:** -18.79%

## Risk Parameters
- **max_portfolio_allocation:** 7.5%
- **stop_loss:** 5.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 4.9%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy 0.5% below market in uptrend.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks.

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **HYG** | BUY | 5% | Limit 0.5% below market | 2.5% below entry | 3.0% above entry | 15.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HYG) / [Yahoo](https://finance.yahoo.com/quote/HYG/) |
| **JNK** | BUY | 5% | Limit 0.5% below market | 2.5% below entry | 3.0% above entry | 15.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNK) / [Yahoo](https://finance.yahoo.com/quote/JNK/) |
| **VCIT** | BUY | 5% | Limit 0.5% below market | 2.5% below entry | 3.0% above entry | 15.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VCIT) / [Yahoo](https://finance.yahoo.com/quote/VCIT/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 9.4% |
| **Avg 5Y Sharpe** | -0.37 |
| **Avg 5Y Max DD** | -14.2% |
| **10Y Return (2015-2024)** | 15.5% |
| **10Y Sharpe** | -0.45 |
| **10Y Max DD** | -17.9% |
| **HODL Composite** | 0.02 |
| **Windows Tested** | 28 |
| **Consistency** | 32% |

### How to Use This Strategy Passively

**Weak long-term profile.** Not recommended for passive buy-and-hold. May still work as a tactical or hedged position — see main body.

</details>

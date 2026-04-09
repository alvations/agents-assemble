# WINNING Strategy: barbell_portfolio

> **What it does:** Short bonds + long bonds + growth equities — skip the middle
>
> **Hypothesis:** Barbell Portfolio — consistency: 100% across 6 windows

**Generated:** 2026-04-09T08:38:44.323965
**Assessment:** STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

## Performance Summary
- **total_return:** 163.72%
- **sharpe_ratio:** 1.90
- **max_drawdown:** -12.08%
- **win_rate:** 56.99%
- **alpha:** 15.18%

## Risk Parameters
- **max_portfolio_allocation:** 17.5%
- **stop_loss:** 14.5%
- **take_profit_target:** 19.2%
- **max_drawdown_tolerance:** 12.1%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** WAIT FOR SIGNAL: Only enter when price spread between paired stocks reaches extreme levels. Exit when spread normalizes.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SHY** | BUY | 2% | Limit 0.5% below market | 7.2% below entry | 9.6% above entry | 35.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 7.7% below entry | 10.1% above entry | 33.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 29.6% below entry | 39.2% above entry | 8.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 14.0% below entry | 18.5% above entry | 18.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 14.8% below entry | 19.6% above entry | 17.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 18.3% below entry | 24.1% above entry | 13.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 19.9% below entry | 26.3% above entry | 12.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 161.0% |
| **Avg 5Y Sharpe** | 1.1 |
| **Avg 5Y Max DD** | -25.4% |
| **10Y Return (2015-2024)** | 682.6% |
| **10Y Sharpe** | 1.22 |
| **10Y Max DD** | -30.7% |
| **HODL Composite** | 1.88 |
| **Windows Tested** | 28 |
| **Consistency** | 96% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Take profit:** Rebalance when either end drifts >10% from target. Dont let offense OR defense dominate.
- **Stop loss:** No stop loss on the portfolio level. Individual positions: -30% triggers review, not automatic exit.
- **Exit rule:** Never fully exit — barbell is designed to work in ALL environments. Adjust the ratio, dont abandon it.

</details>

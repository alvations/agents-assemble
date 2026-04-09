# WINNING Strategy: conservative_regime

> **What it does:** 70% regime-adaptive + 30% permanent defense (GLD/SHY/SCHD). Lower DD, steadier returns.
>
> **Hypothesis:** Conservative Regime Orchestrator — consistency: 100% across 6 windows

**Generated:** 2026-04-09T08:41:03.197386
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 103.23%
- **sharpe_ratio:** 1.65
- **max_drawdown:** -13.53%
- **win_rate:** 57.52%
- **alpha:** 3.64%

## Risk Parameters
- **max_portfolio_allocation:** 16.9%
- **stop_loss:** 16.2%
- **take_profit_target:** 13.4%
- **max_drawdown_tolerance:** 13.5%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** ALWAYS ACTIVE: Auto-managed. Switches between growth and defensive weekly based on market conditions. No user timing needed.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **GLD** | BUY | 23% | Limit 0.5% below market | 15.7% below entry | 12.9% above entry | 17.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 8.1% below entry | 6.7% above entry | 33.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **SCHD** | BUY | 14% | Limit 0.5% below market | 9.6% below entry | 7.9% above entry | 28.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCHD) / [Yahoo](https://finance.yahoo.com/quote/SCHD/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 33.2% below entry | 27.4% above entry | 8.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **CRM** | BUY | 33% | Market order (volatile) | 22.7% below entry | 18.7% above entry | 12.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CRM) / [Yahoo](https://finance.yahoo.com/quote/CRM/) |
| **EPD** | BUY | 17% | Limit 0.5% below market | 11.7% below entry | 9.7% above entry | 23.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EPD) / [Yahoo](https://finance.yahoo.com/quote/EPD/) |
| **ET** | BUY | 23% | Limit 0.5% below market | 15.7% below entry | 12.9% above entry | 17.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ET) / [Yahoo](https://finance.yahoo.com/quote/ET/) |
| **MPLX** | BUY | 18% | Limit 0.5% below market | 12.4% below entry | 10.3% above entry | 22.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MPLX) / [Yahoo](https://finance.yahoo.com/quote/MPLX/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 16.6% below entry | 13.7% above entry | 16.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 19.6% below entry | 16.1% above entry | 14.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 20.4% below entry | 16.9% above entry | 13.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 128.0% |
| **Avg 5Y Sharpe** | 0.93 |
| **Avg 5Y Max DD** | -23.3% |
| **10Y Return (2015-2024)** | 445.0% |
| **10Y Sharpe** | 1.01 |
| **10Y Max DD** | -26.0% |
| **HODL Composite** | 1.22 |
| **Windows Tested** | 28 |
| **Consistency** | 89% |

### How to Use This Strategy Passively

This strategy is **suitable for passive investing**. It has shown consistent returns across multiple time horizons.

**Entry:** Buy the recommended positions at any time. Use the position sizes above as your target allocation.

**Rebalance:** Check quarterly. If any position has drifted more than 5% from target, rebalance back.

**Exit rules:**
- **Exit rule:** Never exit — this auto-manages. Check quarterly that the regime detection is working correctly.

</details>

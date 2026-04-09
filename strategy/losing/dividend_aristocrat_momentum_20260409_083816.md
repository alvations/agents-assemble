# LOSING Strategy: dividend_aristocrat_momentum

> **What it does:** Quality dividends + momentum: only buy Aristocrats in uptrends
>
> **Hypothesis:** Dividend Aristocrat Momentum — consistency: 33% across 6 windows

**Generated:** 2026-04-09T08:38:15.930627
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -5.13%
- **sharpe_ratio:** -0.53
- **max_drawdown:** -15.46%
- **win_rate:** 50.73%
- **alpha:** -24.88%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 18.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 15.5%
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
| **JNJ** | BUY | 18% | Limit 0.5% below market | 13.8% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **NEE** | BUY | 26% | Limit 0.5% below market | 20.5% below entry | 5.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NEE) / [Yahoo](https://finance.yahoo.com/quote/NEE/) |
| **MRK** | BUY | 27% | Limit 0.5% below market | 21.3% below entry | 5.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MRK) / [Yahoo](https://finance.yahoo.com/quote/MRK/) |
| **EMR** | BUY | 31% | Market order (volatile) | 24.1% below entry | 6.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EMR) / [Yahoo](https://finance.yahoo.com/quote/EMR/) |
| **LOW** | BUY | 25% | Limit 0.5% below market | 19.4% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LOW) / [Yahoo](https://finance.yahoo.com/quote/LOW/) |
| **XOM** | BUY | 24% | Limit 0.5% below market | 18.4% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **ECL** | BUY | 20% | Limit 0.5% below market | 15.9% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ECL) / [Yahoo](https://finance.yahoo.com/quote/ECL/) |
| **PEP** | BUY | 21% | Limit 0.5% below market | 16.1% below entry | 4.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PEP) / [Yahoo](https://finance.yahoo.com/quote/PEP/) |
| **WMT** | BUY | 23% | Limit 0.5% below market | 18.2% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WMT) / [Yahoo](https://finance.yahoo.com/quote/WMT/) |
| **MCD** | BUY | 18% | Limit 0.5% below market | 14.1% below entry | 3.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MCD) / [Yahoo](https://finance.yahoo.com/quote/MCD/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.53 (target > 0.5)
- Max drawdown: -15.46% (target > -20%)
- Alpha: -24.88% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 49.1% |
| **Avg 5Y Sharpe** | 0.39 |
| **Avg 5Y Max DD** | -15.2% |
| **10Y Return (2015-2024)** | 75.9% |
| **10Y Sharpe** | 0.21 |
| **10Y Max DD** | -15.5% |
| **HODL Composite** | 0.23 |
| **Windows Tested** | 28 |
| **Consistency** | 67% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Trim 25% of any position that doubles. Reinvest the proceeds into the lowest-yielding holding to rebalance.
- **Stop loss:** No price-based stop loss. Only exit if dividend is CUT (not just frozen). A 30% price drop with maintained dividend = higher yield = buy more.
- **Exit rule:** Full exit only if company cuts dividend AND debt-to-equity exceeds 2x (financial distress, not just a bad quarter).

</details>

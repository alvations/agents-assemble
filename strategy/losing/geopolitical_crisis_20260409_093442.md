# LOSING Strategy: geopolitical_crisis

> **What it does:** War/crisis beneficiaries: energy + defense spike when vol rises
>
> **Hypothesis:** Geopolitical Crisis Alpha — composite: 0.05, consistency: 50%

**Generated:** 2026-04-09T09:34:42.566464
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 0.08%
- **sharpe_ratio:** -0.34
- **max_drawdown:** -21.37%
- **win_rate:** 51.80%
- **alpha:** -23.10%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 21.4%
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
| **NOC** | BUY | 26% | Limit 0.5% below market | 26.9% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NOC) / [Yahoo](https://finance.yahoo.com/quote/NOC/) |
| **HAL** | BUY | 39% | Market order (volatile) | 40.0% below entry | 8.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HAL) / [Yahoo](https://finance.yahoo.com/quote/HAL/) |
| **RTX** | BUY | 25% | Limit 0.5% below market | 26.2% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=RTX) / [Yahoo](https://finance.yahoo.com/quote/RTX/) |
| **ITA** | BUY | 21% | Limit 0.5% below market | 22.5% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ITA) / [Yahoo](https://finance.yahoo.com/quote/ITA/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SLV** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SLV) / [Yahoo](https://finance.yahoo.com/quote/SLV/) |
| **XLE** | BUY | 23% | Limit 0.5% below market | 23.9% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |
| **DVN** | BUY | 37% | Market order (volatile) | 38.6% below entry | 7.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DVN) / [Yahoo](https://finance.yahoo.com/quote/DVN/) |
| **LMT** | BUY | 25% | Limit 0.5% below market | 26.3% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LMT) / [Yahoo](https://finance.yahoo.com/quote/LMT/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.34 (target > 0.5)
- Max drawdown: -21.37% (target > -20%)
- Alpha: -23.10% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 21.6% |
| **Avg 5Y Sharpe** | 0.08 |
| **Avg 5Y Max DD** | -29.7% |
| **10Y Return (2015-2024)** | 26.2% |
| **10Y Sharpe** | -0.03 |
| **10Y Max DD** | -32.1% |
| **HODL Composite** | 0.08 |
| **Windows Tested** | 28 |
| **Consistency** | 60% |

### How to Use This Strategy Passively

This strategy has **moderate long-term potential** but requires more active monitoring than a pure passive approach.

**Entry:** Wait for a pullback before entering. Buy in 3 tranches over 2-4 weeks to average your entry price.

**Rebalance:** Check monthly. This strategy is more volatile and needs closer attention.

**Exit rules:**
- **Take profit:** Trim winners that are up 50%+ to lock in gains
- **Stop loss:** Exit if drawdown exceeds 25% — the strategy may not recover quickly
- **Time limit:** If flat (< 5% return) after 12 months, reassess whether the thesis still holds

</details>

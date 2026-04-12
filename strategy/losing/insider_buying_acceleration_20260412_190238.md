# LOSING Strategy: insider_buying_acceleration

> **What it does:** Detect insider accumulation via price/volume proxies: 52-week low bounce, oversold uptrend, volume spike
>
> **Hypothesis:** Insider Buying Acceleration

**Generated:** 2026-04-12T19:02:37.443547
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 1.71%
- **sharpe_ratio:** -1.95
- **max_drawdown:** -2.95%
- **win_rate:** 16.64%
- **alpha:** -22.56%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 5.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 3.0%
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
| **AAPL** | FLAT | 29% | Limit 0.5% below market | 6.0% below entry | 6.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **MSFT** | FLAT | 24% | Limit 0.5% below market | 5.1% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **GOOGL** | FLAT | 30% | Limit 0.5% below market | 6.3% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **JPM** | FLAT | 25% | Limit 0.5% below market | 5.3% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **BAC** | FLAT | 26% | Limit 0.5% below market | 5.4% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BAC) / [Yahoo](https://finance.yahoo.com/quote/BAC/) |
| **WFC** | FLAT | 31% | Market order (volatile) | 6.4% below entry | 6.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WFC) / [Yahoo](https://finance.yahoo.com/quote/WFC/) |
| **GS** | FLAT | 31% | Market order (volatile) | 6.6% below entry | 6.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GS) / [Yahoo](https://finance.yahoo.com/quote/GS/) |
| **JNJ** | FLAT | 18% | Limit 0.5% below market | 3.7% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **PFE** | FLAT | 25% | Limit 0.5% below market | 5.1% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PFE) / [Yahoo](https://finance.yahoo.com/quote/PFE/) |
| **UNH** | FLAT | 43% | Market order (volatile) | 9.0% below entry | 9.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UNH) / [Yahoo](https://finance.yahoo.com/quote/UNH/) |
| **XOM** | FLAT | 24% | Limit 0.5% below market | 4.9% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **CVX** | FLAT | 23% | Limit 0.5% below market | 4.9% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CVX) / [Yahoo](https://finance.yahoo.com/quote/CVX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -1.95 (target > 0.5)
- Max drawdown: -2.95% (target > -20%)
- Alpha: -22.56% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 2.7% |
| **Avg 5Y Sharpe** | -1.07 |
| **10Y Return** | 6.3% |
| **10Y Sharpe** | -0.95 |
| **HODL Composite** | 0.0 |
| **Consistency** | 0% |
| **Suitable for passive** | No |

This strategy is **NOT recommended for passive investing**.

- **Take profit:** Take profit at +50%. This strategy is inconsistent — capture gains when available.
- **Stop loss:** Reduce position by 50% at -25% drawdown. Consistency is only 0%.
- **Exit rule:** Review annually. Exit if strategy underperforms its benchmark for 3 consecutive years.

</details>

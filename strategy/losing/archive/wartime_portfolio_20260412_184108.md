# LOSING Strategy: wartime_portfolio

> **What it does:** Anti-fragile: defense + energy + gold. Outperforms 8.5% during conflicts
>
> **Hypothesis:** Wartime Portfolio

**Generated:** 2026-04-12T18:41:06.566044
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 2.89%
- **sharpe_ratio:** -0.41
- **max_drawdown:** -10.25%
- **win_rate:** 53.13%
- **alpha:** -22.17%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 12.3%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 10.2%
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
| **DBA** | BUY | 13% | Limit 0.5% below market | 6.8% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DBA) / [Yahoo](https://finance.yahoo.com/quote/DBA/) |
| **XOM** | BUY | 24% | Limit 0.5% below market | 12.2% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **XLE** | BUY | 23% | Limit 0.5% below market | 11.7% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLE) / [Yahoo](https://finance.yahoo.com/quote/XLE/) |
| **DVN** | BUY | 37% | Market order (volatile) | 19.0% below entry | 7.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DVN) / [Yahoo](https://finance.yahoo.com/quote/DVN/) |
| **LHX** | BUY | 23% | Limit 0.5% below market | 11.9% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LHX) / [Yahoo](https://finance.yahoo.com/quote/LHX/) |
| **ITA** | BUY | 21% | Limit 0.5% below market | 11.0% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ITA) / [Yahoo](https://finance.yahoo.com/quote/ITA/) |
| **LMT** | BUY | 25% | Limit 0.5% below market | 12.9% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LMT) / [Yahoo](https://finance.yahoo.com/quote/LMT/) |
| **NOC** | BUY | 26% | Limit 0.5% below market | 13.2% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NOC) / [Yahoo](https://finance.yahoo.com/quote/NOC/) |
| **SLV** | BUY | 46% | Market order (volatile) | 23.9% below entry | 9.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SLV) / [Yahoo](https://finance.yahoo.com/quote/SLV/) |
| **RTX** | BUY | 25% | Limit 0.5% below market | 12.8% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=RTX) / [Yahoo](https://finance.yahoo.com/quote/RTX/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 11.8% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.41 (target > 0.5)
- Max drawdown: -10.25% (target > -20%)
- Alpha: -22.17% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
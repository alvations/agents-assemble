# WINNING Strategy: late_cycle_bubble_hedge

> **What it does:** 1999 detector: rotate to value when AI speculation gets frothy
>
> **Hypothesis:** Late-Cycle Bubble Hedge

**Generated:** 2026-04-12T18:50:01.795919
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 46.49%
- **sharpe_ratio:** 0.94
- **max_drawdown:** -10.50%
- **win_rate:** 54.19%
- **alpha:** -9.51%

## Risk Parameters
- **max_portfolio_allocation:** 10.8%
- **stop_loss:** 12.6%
- **take_profit_target:** 6.8%
- **max_drawdown_tolerance:** 10.5%
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
| **MSFT** | BUY | 24% | Limit 0.5% below market | 12.9% below entry | 7.0% above entry | 10.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 17.4% below entry | 9.4% above entry | 7.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 15.8% below entry | 8.6% above entry | 8.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **JNJ** | BUY | 18% | Limit 0.5% below market | 9.4% below entry | 5.1% above entry | 14.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 15.1% below entry | 8.2% above entry | 9.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **PEP** | BUY | 21% | Limit 0.5% below market | 10.9% below entry | 5.9% above entry | 12.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PEP) / [Yahoo](https://finance.yahoo.com/quote/PEP/) |
| **KO** | BUY | 16% | Limit 0.5% below market | 8.7% below entry | 4.7% above entry | 15.7% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KO) / [Yahoo](https://finance.yahoo.com/quote/KO/) |
| **MRK** | BUY | 27% | Limit 0.5% below market | 14.5% below entry | 7.8% above entry | 9.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MRK) / [Yahoo](https://finance.yahoo.com/quote/MRK/) |
| **BRK-B** | BUY | 18% | Limit 0.5% below market | 9.3% below entry | 5.0% above entry | 14.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BRK-B) / [Yahoo](https://finance.yahoo.com/quote/BRK-B/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

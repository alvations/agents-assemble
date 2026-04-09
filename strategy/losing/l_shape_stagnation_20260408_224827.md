# LOSING Strategy: l_shape_stagnation

> **What it does:** Persistent crash with no recovery (Japan 1990s). Gold + utilities + short bonds + dividends only.
>
> **Hypothesis:** L-Shape Stagnation Hedge (Worst Case)

**Generated:** 2026-04-08T22:48:27.468588
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 0.00%
- **sharpe_ratio:** 0.00
- **max_drawdown:** 0.00%
- **win_rate:** 0.00%
- **alpha:** -8.66%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 2.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 0.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Strategy has low win rate — enter only on strong setup days. Be patient.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SPY** | FLAT | 17% | Limit 0.5% below market | 1.4% below entry | 3.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **GLD** | FLAT | 23% | Limit 0.5% below market | 1.9% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **IAU** | FLAT | 23% | Limit 0.5% below market | 1.9% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IAU) / [Yahoo](https://finance.yahoo.com/quote/IAU/) |
| **XLU** | FLAT | 16% | Limit 0.5% below market | 1.3% below entry | 3.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XLU) / [Yahoo](https://finance.yahoo.com/quote/XLU/) |
| **SHY** | FLAT | 2% | Limit 0.5% below market | 1.0% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **BIL** | FLAT | 0% | Limit 0.5% below market | 1.0% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BIL) / [Yahoo](https://finance.yahoo.com/quote/BIL/) |
| **SCHD** | FLAT | 14% | Limit 0.5% below market | 1.2% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCHD) / [Yahoo](https://finance.yahoo.com/quote/SCHD/) |
| **JNJ** | FLAT | 18% | Limit 0.5% below market | 1.5% below entry | 3.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **PG** | FLAT | 18% | Limit 0.5% below market | 1.5% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PG) / [Yahoo](https://finance.yahoo.com/quote/PG/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: 0.00 (target > 0.5)
- Max drawdown: 0.00% (target > -20%)
- Alpha: -8.66% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
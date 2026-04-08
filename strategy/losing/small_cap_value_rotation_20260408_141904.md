# LOSING Strategy: small_cap_value_rotation

> **What it does:** Small caps at 50-year cheap: AVUV + momentum picks, 18% YTD 2026
>
> **Hypothesis:** Small Cap Value Rotation 3Y

**Generated:** 2026-04-08T14:19:04.731971
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 3.60%
- **sharpe_ratio:** -0.06
- **max_drawdown:** -22.29%
- **win_rate:** 49.87%
- **alpha:** -7.47%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 22.3%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Enter on any weekly rebalance day. No specific timing edge detected.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **WTTR** | BUY | 48% | Market order (volatile) | 40.0% below entry | 10.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WTTR) / [Yahoo](https://finance.yahoo.com/quote/WTTR/) |
| **LULU** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LULU) / [Yahoo](https://finance.yahoo.com/quote/LULU/) |
| **DECK** | BUY | 49% | Market order (volatile) | 40.0% below entry | 10.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DECK) / [Yahoo](https://finance.yahoo.com/quote/DECK/) |
| **EVLV** | BUY | 74% | Market order (volatile) | 40.0% below entry | 15.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EVLV) / [Yahoo](https://finance.yahoo.com/quote/EVLV/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.06 (target > 0.5)
- Max drawdown: -22.29% (target > -20%)
- Alpha: -7.47% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
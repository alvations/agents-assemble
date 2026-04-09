# LOSING Strategy: constellation_contrarian

> **What it does:** STZ 49.8% DCF discount, EFX 34%, NKE permanent moat — most mispriced wide-moat stocks
>
> **Hypothesis:** Constellation Contrarian (Max DCF Discount) 4Y (2022-2025)

**Generated:** 2026-04-08T23:02:46.034785
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -13.54%
- **sharpe_ratio:** -0.29
- **max_drawdown:** -26.62%
- **win_rate:** 48.70%
- **alpha:** -14.45%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 26.6%
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
| **STZ** | BUY | 29% | Limit 0.5% below market | 30.5% below entry | 6.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=STZ) / [Yahoo](https://finance.yahoo.com/quote/STZ/) |
| **LULU** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LULU) / [Yahoo](https://finance.yahoo.com/quote/LULU/) |
| **PVH** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PVH) / [Yahoo](https://finance.yahoo.com/quote/PVH/) |
| **BUD** | BUY | 24% | Limit 0.5% below market | 24.8% below entry | 5.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BUD) / [Yahoo](https://finance.yahoo.com/quote/BUD/) |
| **SAM** | BUY | 31% | Market order (volatile) | 33.1% below entry | 6.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SAM) / [Yahoo](https://finance.yahoo.com/quote/SAM/) |
| **MNST** | BUY | 24% | Limit 0.5% below market | 25.5% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MNST) / [Yahoo](https://finance.yahoo.com/quote/MNST/) |
| **DEO** | BUY | 29% | Limit 0.5% below market | 30.3% below entry | 6.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DEO) / [Yahoo](https://finance.yahoo.com/quote/DEO/) |
| **NKE** | BUY | 40% | Market order (volatile) | 40.0% below entry | 8.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NKE) / [Yahoo](https://finance.yahoo.com/quote/NKE/) |
| **EFX** | BUY | 35% | Market order (volatile) | 36.4% below entry | 7.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EFX) / [Yahoo](https://finance.yahoo.com/quote/EFX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.29 (target > 0.5)
- Max drawdown: -26.62% (target > -20%)
- Alpha: -14.45% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
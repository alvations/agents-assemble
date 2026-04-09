# LOSING Strategy: constellation_contrarian

> **What it does:** STZ 49.8% DCF discount, EFX 34%, NKE permanent moat — most mispriced wide-moat stocks
>
> **Hypothesis:** Constellation Contrarian (Max DCF Discount) 3Y

**Generated:** 2026-04-08T22:09:51.359091
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -3.30%
- **sharpe_ratio:** -0.17
- **max_drawdown:** -24.93%
- **win_rate:** 49.47%
- **alpha:** -9.78%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 24.9%
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
| **PVH** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PVH) / [Yahoo](https://finance.yahoo.com/quote/PVH/) |
| **BUD** | BUY | 24% | Limit 0.5% below market | 24.8% below entry | 5.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BUD) / [Yahoo](https://finance.yahoo.com/quote/BUD/) |
| **TAP** | BUY | 26% | Limit 0.5% below market | 27.2% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TAP) / [Yahoo](https://finance.yahoo.com/quote/TAP/) |
| **SAM** | BUY | 31% | Market order (volatile) | 33.1% below entry | 6.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SAM) / [Yahoo](https://finance.yahoo.com/quote/SAM/) |
| **MNST** | BUY | 24% | Limit 0.5% below market | 25.5% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MNST) / [Yahoo](https://finance.yahoo.com/quote/MNST/) |
| **DEO** | BUY | 29% | Limit 0.5% below market | 30.3% below entry | 6.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DEO) / [Yahoo](https://finance.yahoo.com/quote/DEO/) |
| **HAS** | BUY | 32% | Market order (volatile) | 33.7% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HAS) / [Yahoo](https://finance.yahoo.com/quote/HAS/) |
| **NKE** | BUY | 40% | Market order (volatile) | 40.0% below entry | 8.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NKE) / [Yahoo](https://finance.yahoo.com/quote/NKE/) |
| **EFX** | BUY | 35% | Market order (volatile) | 36.4% below entry | 7.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EFX) / [Yahoo](https://finance.yahoo.com/quote/EFX/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.17 (target > 0.5)
- Max drawdown: -24.93% (target > -20%)
- Alpha: -9.78% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
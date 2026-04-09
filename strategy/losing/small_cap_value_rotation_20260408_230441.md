# LOSING Strategy: small_cap_value_rotation

> **What it does:** Small caps at 50-year cheap: AVUV + momentum picks, 18% YTD 2026
>
> **Hypothesis:** Small Cap Value Rotation 4Y (2022-2025)

**Generated:** 2026-04-08T23:04:41.431366
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -3.85%
- **sharpe_ratio:** -0.16
- **max_drawdown:** -27.41%
- **win_rate:** 48.60%
- **alpha:** -11.85%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 27.4%
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
| **AVUV** | BUY | 23% | Limit 0.5% below market | 23.7% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AVUV) / [Yahoo](https://finance.yahoo.com/quote/AVUV/) |
| **VBR** | BUY | 19% | Limit 0.5% below market | 20.1% below entry | 4.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VBR) / [Yahoo](https://finance.yahoo.com/quote/VBR/) |
| **IWN** | BUY | 21% | Limit 0.5% below market | 22.3% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWN) / [Yahoo](https://finance.yahoo.com/quote/IWN/) |
| **SAIA** | BUY | 57% | Market order (volatile) | 40.0% below entry | 12.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SAIA) / [Yahoo](https://finance.yahoo.com/quote/SAIA/) |
| **IWM** | BUY | 22% | Limit 0.5% below market | 23.3% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IWM) / [Yahoo](https://finance.yahoo.com/quote/IWM/) |
| **DFSV** | BUY | 22% | Limit 0.5% below market | 23.5% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DFSV) / [Yahoo](https://finance.yahoo.com/quote/DFSV/) |
| **DECK** | BUY | 49% | Market order (volatile) | 40.0% below entry | 10.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=DECK) / [Yahoo](https://finance.yahoo.com/quote/DECK/) |
| **GRC** | BUY | 30% | Market order (volatile) | 31.7% below entry | 6.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GRC) / [Yahoo](https://finance.yahoo.com/quote/GRC/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.16 (target > 0.5)
- Max drawdown: -27.41% (target > -20%)
- Alpha: -11.85% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
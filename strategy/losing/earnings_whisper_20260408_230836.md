# LOSING Strategy: earnings_whisper

> **What it does:** Pre-earnings drift: accumulation patterns predict positive surprises
>
> **Hypothesis:** Earnings Whisper (Pre-Drift) 4Y (2022-2025)

**Generated:** 2026-04-08T23:08:36.656730
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 2.44%
- **sharpe_ratio:** -0.20
- **max_drawdown:** -23.60%
- **win_rate:** 46.31%
- **alpha:** -10.26%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 23.6%
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
| **META** | BUY | 36% | Market order (volatile) | 37.8% below entry | 7.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **JPM** | BUY | 25% | Limit 0.5% below market | 26.7% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **CRM** | BUY | 33% | Market order (volatile) | 34.9% below entry | 7.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CRM) / [Yahoo](https://finance.yahoo.com/quote/CRM/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.20 (target > 0.5)
- Max drawdown: -23.60% (target > -20%)
- Alpha: -10.26% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
# LOSING Strategy: crypto_crash_tradfi

> **What it does:** Crypto collapse drives capital to traditional banks, brokers, asset managers.
>
> **Hypothesis:** Crypto Crash → TradFi Flight

**Generated:** 2026-04-08T22:42:57.244387
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 4.00%
- **sharpe_ratio:** -0.17
- **max_drawdown:** -17.51%
- **win_rate:** 54.92%
- **alpha:** -7.34%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 21.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 17.5%
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
| **JPM** | BUY | 25% | Limit 0.5% below market | 22.4% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **BLK** | BUY | 26% | Limit 0.5% below market | 22.6% below entry | 5.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BLK) / [Yahoo](https://finance.yahoo.com/quote/BLK/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.17 (target > 0.5)
- Max drawdown: -17.51% (target > -20%)
- Alpha: -7.34% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
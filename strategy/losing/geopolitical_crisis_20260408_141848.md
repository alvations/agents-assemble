# LOSING Strategy: geopolitical_crisis

> **What it does:** War/crisis beneficiaries: energy + defense spike when vol rises
>
> **Hypothesis:** Geopolitical Crisis Alpha 3Y

**Generated:** 2026-04-08T14:18:48.368607
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -1.35%
- **sharpe_ratio:** -0.22
- **max_drawdown:** -28.09%
- **win_rate:** 50.66%
- **alpha:** -9.11%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 28.1%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** TRIGGER: Enter when VIX spikes >25 (VXX >1.3x SMA200). Buy fear in quality names.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SLV** | BUY | 46% | Market order (volatile) | 40.0% below entry | 9.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SLV) / [Yahoo](https://finance.yahoo.com/quote/SLV/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.22 (target > 0.5)
- Max drawdown: -28.09% (target > -20%)
- Alpha: -9.11% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
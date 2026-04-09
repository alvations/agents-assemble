# WINNING Strategy: vix_mean_reversion

> **What it does:** Buy aggressively when volatility spikes, reduce when complacent
>
> **Hypothesis:** VIX Mean Reversion (Buy Fear) — composite: 0.11, consistency: 67%

**Generated:** 2026-04-09T09:33:53.930592
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 56.21%
- **sharpe_ratio:** 1.06
- **max_drawdown:** -10.64%
- **win_rate:** 55.93%
- **alpha:** -7.04%

## Risk Parameters
- **max_portfolio_allocation:** 13.6%
- **stop_loss:** 12.8%
- **take_profit_target:** 8.0%
- **max_drawdown_tolerance:** 10.6%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** WAIT FOR SIGNAL: Only enter when price spread between paired stocks reaches extreme levels. Exit when spread normalizes.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SPY** | BUY | 17% | Limit 0.5% below market | 9.2% below entry | 5.8% above entry | 18.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 11.6% below entry | 7.3% above entry | 14.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 6.7% below entry | 4.2% above entry | 25.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 12.3% below entry | 7.8% above entry | 14.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

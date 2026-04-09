# LOSING Strategy: nvidia_domino_hedge

> **What it does:** Profit when NVIDIA financing chain breaks: inverse ETFs + safe havens + vol, scaled by supply chain stress
>
> **Hypothesis:** NVIDIA Domino Hedge (Supply Chain Collapse) — consistency: 0% across 6 windows

**Generated:** 2026-04-09T08:38:41.606472
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -13.67%
- **sharpe_ratio:** -0.83
- **max_drawdown:** -16.27%
- **win_rate:** 47.94%
- **alpha:** -27.93%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 19.5%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 16.3%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** WAIT FOR SIGNAL: Hold AI stocks normally. Switch to defensive ONLY when supply chain companies start breaking down.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **GLD** | BUY | 23% | Limit 0.5% below market | 18.8% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SQQQ** | BUY | 65% | Market order (volatile) | 40.0% below entry | 13.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SQQQ) / [Yahoo](https://finance.yahoo.com/quote/SQQQ/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 10.3% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **UVXY** | BUY | 122% | Market order (volatile) | 40.0% below entry | 15.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UVXY) / [Yahoo](https://finance.yahoo.com/quote/UVXY/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 9.8% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.83 (target > 0.5)
- Max drawdown: -16.27% (target > -20%)
- Alpha: -27.93% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
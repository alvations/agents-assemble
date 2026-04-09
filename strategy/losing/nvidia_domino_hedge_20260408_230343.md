# LOSING Strategy: nvidia_domino_hedge

> **What it does:** Profit when NVIDIA financing chain breaks: inverse ETFs + safe havens + vol, scaled by supply chain stress
>
> **Hypothesis:** NVIDIA Domino Hedge (Supply Chain Collapse) 4Y (2022-2025)

**Generated:** 2026-04-08T23:03:43.517878
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -19.41%
- **sharpe_ratio:** -0.93
- **max_drawdown:** -20.72%
- **win_rate:** 49.40%
- **alpha:** -16.13%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 24.9%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 20.7%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** TRIGGER: Enter hedge when supply chain canaries (SMCI, AMKR, KLIC) break below SMA200 with volume spike.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.0% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SQQQ** | BUY | 64% | Market order (volatile) | 40.0% below entry | 13.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SQQQ) / [Yahoo](https://finance.yahoo.com/quote/SQQQ/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 13.1% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 12.4% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **UVXY** | BUY | 122% | Market order (volatile) | 40.0% below entry | 15.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UVXY) / [Yahoo](https://finance.yahoo.com/quote/UVXY/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.93 (target > 0.5)
- Max drawdown: -20.72% (target > -20%)
- Alpha: -16.13% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
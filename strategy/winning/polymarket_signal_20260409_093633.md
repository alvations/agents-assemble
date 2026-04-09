# WINNING Strategy: polymarket_signal

> **What it does:** Political uncertainty→defensive, stability→risk-on (Polymarket proxy)
>
> **Hypothesis:** Polymarket Signal (Uncertainty Proxy) — composite: 0.19, consistency: 92%

**Generated:** 2026-04-09T09:36:33.640974
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 41.38%
- **sharpe_ratio:** 0.86
- **max_drawdown:** -11.44%
- **win_rate:** 57.26%
- **alpha:** -10.85%

## Risk Parameters
- **max_portfolio_allocation:** 11.1%
- **stop_loss:** 13.7%
- **take_profit_target:** 6.1%
- **max_drawdown_tolerance:** 11.4%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **TLT** | BUY | 13% | Limit 0.5% below market | 7.2% below entry | 3.2% above entry | 21.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 13.2% below entry | 5.9% above entry | 11.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 9.9% below entry | 4.4% above entry | 15.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 12.5% below entry | 5.6% above entry | 12.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

# WINNING Strategy: short_seller_dip_buy

> **What it does:** Buy >5% drops on 3x volume (short report proxy). MSTR +226%, HOOD +168%
>
> **Hypothesis:** Short Seller Dip Buy 3Y

**Generated:** 2026-04-08T14:21:23.803207
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 58.58%
- **sharpe_ratio:** 0.87
- **max_drawdown:** -11.38%
- **win_rate:** 51.20%
- **alpha:** 8.01%

## Risk Parameters
- **max_portfolio_allocation:** 10.9%
- **stop_loss:** 13.7%
- **take_profit_target:** 8.3%
- **max_drawdown_tolerance:** 11.4%
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
| **AI** | BUY | 65% | Market order (volatile) | 37.2% below entry | 22.7% above entry | 4.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AI) / [Yahoo](https://finance.yahoo.com/quote/AI/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

# WINNING Strategy: short_seller_dip_buy

> **What it does:** Buy >5% drops on 3x volume (short report proxy). MSTR +226%, HOOD +168%
>
> **Hypothesis:** Short Seller Dip Buy 4Y (2022-2025)

**Generated:** 2026-04-08T23:15:11.464422
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 64.87%
- **sharpe_ratio:** 0.68
- **max_drawdown:** -11.38%
- **win_rate:** 50.80%
- **alpha:** 2.49%

## Risk Parameters
- **max_portfolio_allocation:** 9.0%
- **stop_loss:** 13.7%
- **take_profit_target:** 6.7%
- **max_drawdown_tolerance:** 11.4%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When holdings above SMA200 on weekly rebalance. STRONG BUY: On RSI pullback to 35-50 in confirmed uptrend — buy the dip in quality.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **META** | BUY | 36% | Market order (volatile) | 20.6% below entry | 10.1% above entry | 6.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

# WINNING Strategy: market_making_momentum

> **What it does:** Multi-factor momentum + short-term mean-reversion entry, Citadel-inspired
>
> **Hypothesis:** Market-Making Momentum (Citadel-style) — composite: 0.07, consistency: 58%

**Generated:** 2026-04-09T09:35:13.467121
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 11.84%
- **sharpe_ratio:** 0.04
- **max_drawdown:** -13.98%
- **win_rate:** 51.93%
- **alpha:** -19.32%

## Risk Parameters
- **max_portfolio_allocation:** 3.3%
- **stop_loss:** 16.8%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 14.0%
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
| **ABBV** | BUY | 26% | Limit 0.5% below market | 18.6% below entry | 5.5% above entry | 2.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ABBV) / [Yahoo](https://finance.yahoo.com/quote/ABBV/) |
| **JPM** | BUY | 26% | Limit 0.5% below market | 18.0% below entry | 5.4% above entry | 3.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **XOM** | BUY | 24% | Limit 0.5% below market | 16.6% below entry | 4.9% above entry | 3.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **GS** | BUY | 31% | Market order (volatile) | 22.1% below entry | 6.6% above entry | 2.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GS) / [Yahoo](https://finance.yahoo.com/quote/GS/) |
| **TSLA** | BUY | 62% | Market order (volatile) | 40.0% below entry | 13.1% above entry | 1.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TSLA) / [Yahoo](https://finance.yahoo.com/quote/TSLA/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 34.3% below entry | 10.2% above entry | 1.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **CVX** | BUY | 23% | Limit 0.5% below market | 16.5% below entry | 4.9% above entry | 3.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CVX) / [Yahoo](https://finance.yahoo.com/quote/CVX/) |
| **SPY** | BUY | 17% | Limit 0.5% below market | 12.1% below entry | 3.6% above entry | 4.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPY) / [Yahoo](https://finance.yahoo.com/quote/SPY/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 21.1% below entry | 6.3% above entry | 2.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

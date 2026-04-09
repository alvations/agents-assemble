# WINNING Strategy: vix_spike_buyback

> **What it does:** Fear spikes → buy companies with massive buyback programs. They buy themselves cheap in panics.
>
> **Hypothesis:** VIX Spike → Cash-Rich Buyback 4Y (2022-2025)

**Generated:** 2026-04-08T23:03:32.366375
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 35.09%
- **sharpe_ratio:** 0.46
- **max_drawdown:** -11.42%
- **win_rate:** 53.49%
- **alpha:** -3.04%

## Risk Parameters
- **max_portfolio_allocation:** 10.3%
- **stop_loss:** 13.7%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 11.4%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** BUY: When cash-rich companies (AAPL, GOOGL, META) are above SMA200. STRONG BUY: When VIX spikes >25 and RSI < 40 — buy the fear, these companies buy themselves back.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **AAPL** | BUY | 29% | Limit 0.5% below market | 16.5% below entry | 6.0% above entry | 8.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 17.2% below entry | 6.3% above entry | 8.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **META** | BUY | 36% | Market order (volatile) | 20.7% below entry | 7.6% above entry | 6.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **V** | BUY | 22% | Limit 0.5% below market | 12.5% below entry | 4.6% above entry | 11.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

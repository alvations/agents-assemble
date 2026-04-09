# WINNING Strategy: vix_spike_buyback

> **What it does:** Fear spikes → buy companies with massive buyback programs. They buy themselves cheap in panics.
>
> **Hypothesis:** VIX Spike → Cash-Rich Buyback

**Generated:** 2026-04-08T22:42:53.954357
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 16.44%
- **sharpe_ratio:** 0.21
- **max_drawdown:** -11.42%
- **win_rate:** 53.99%
- **alpha:** -3.44%

## Risk Parameters
- **max_portfolio_allocation:** 7.4%
- **stop_loss:** 13.7%
- **take_profit_target:** 5.0%
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
| **AAPL** | BUY | 29% | Limit 0.5% below market | 16.5% below entry | 6.0% above entry | 6.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 17.2% below entry | 6.3% above entry | 5.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **META** | BUY | 36% | Market order (volatile) | 20.7% below entry | 7.6% above entry | 4.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **V** | BUY | 22% | Limit 0.5% below market | 12.5% below entry | 4.6% above entry | 8.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

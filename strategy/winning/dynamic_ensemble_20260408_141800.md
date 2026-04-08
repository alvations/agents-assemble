# WINNING Strategy: dynamic_ensemble

> **What it does:** Multi-strategy ensemble weighted by rolling Sharpe ratio
>
> **Hypothesis:** Dynamic Ensemble 3Y

**Generated:** 2026-04-08T14:18:00.492809
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 17.35%
- **sharpe_ratio:** 0.18
- **max_drawdown:** -16.28%
- **win_rate:** 52.53%
- **alpha:** -3.17%

## Risk Parameters
- **max_portfolio_allocation:** 4.2%
- **stop_loss:** 19.5%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 16.3%
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
| **MSFT** | BUY | 24% | Limit 0.5% below market | 20.0% below entry | 5.1% above entry | 4.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **WMT** | BUY | 23% | Limit 0.5% below market | 19.1% below entry | 4.9% above entry | 4.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WMT) / [Yahoo](https://finance.yahoo.com/quote/WMT/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 17.8% below entry | 4.5% above entry | 4.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **AAPL** | BUY | 29% | Limit 0.5% below market | 23.5% below entry | 6.0% above entry | 3.5% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AAPL) / [Yahoo](https://finance.yahoo.com/quote/AAPL/) |
| **META** | BUY | 36% | Market order (volatile) | 29.5% below entry | 7.6% above entry | 2.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=META) / [Yahoo](https://finance.yahoo.com/quote/META/) |
| **JPM** | BUY | 25% | Limit 0.5% below market | 20.9% below entry | 5.3% above entry | 3.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **JNJ** | BUY | 18% | Limit 0.5% below market | 14.6% below entry | 3.7% above entry | 5.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JNJ) / [Yahoo](https://finance.yahoo.com/quote/JNJ/) |
| **MA** | BUY | 22% | Limit 0.5% below market | 17.7% below entry | 4.5% above entry | 4.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MA) / [Yahoo](https://finance.yahoo.com/quote/MA/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 24.5% below entry | 6.3% above entry | 3.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 26.8% below entry | 6.9% above entry | 3.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |
| **V** | BUY | 22% | Limit 0.5% below market | 17.8% below entry | 4.6% above entry | 4.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=V) / [Yahoo](https://finance.yahoo.com/quote/V/) |
| **TSLA** | BUY | 62% | Market order (volatile) | 40.0% below entry | 13.1% above entry | 1.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TSLA) / [Yahoo](https://finance.yahoo.com/quote/TSLA/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

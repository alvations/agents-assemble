# LOSING Strategy: merger_arbitrage

> **What it does:** M&A deal spread capture: buy targets at discount to deal price
>
> **Hypothesis:** Merger Arbitrage (M&A Spread) 3Y

**Generated:** 2026-04-08T16:16:15.513060
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -1.65%
- **sharpe_ratio:** -1.77
- **max_drawdown:** -5.24%
- **win_rate:** 12.25%
- **alpha:** -9.36%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 6.3%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 5.2%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Strategy has low win rate — enter only on strong setup days. Be patient.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **ATVI** | FLAT | 32% | Market order (volatile) | 8.4% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ATVI) / [Yahoo](https://finance.yahoo.com/quote/ATVI/) |
| **VMW** | FLAT | 32% | Market order (volatile) | 8.4% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VMW) / [Yahoo](https://finance.yahoo.com/quote/VMW/) |
| **SPLK** | FLAT | 32% | Market order (volatile) | 8.4% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPLK) / [Yahoo](https://finance.yahoo.com/quote/SPLK/) |
| **FORG** | FLAT | 32% | Market order (volatile) | 8.4% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=FORG) / [Yahoo](https://finance.yahoo.com/quote/FORG/) |
| **COUP** | FLAT | 32% | Market order (volatile) | 8.4% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=COUP) / [Yahoo](https://finance.yahoo.com/quote/COUP/) |
| **SGEN** | FLAT | 32% | Market order (volatile) | 8.4% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SGEN) / [Yahoo](https://finance.yahoo.com/quote/SGEN/) |
| **ALNY** | FLAT | 49% | Market order (volatile) | 12.8% below entry | 10.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ALNY) / [Yahoo](https://finance.yahoo.com/quote/ALNY/) |
| **BMRN** | FLAT | 34% | Market order (volatile) | 9.0% below entry | 7.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BMRN) / [Yahoo](https://finance.yahoo.com/quote/BMRN/) |
| **HZNP** | FLAT | 32% | Market order (volatile) | 8.4% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HZNP) / [Yahoo](https://finance.yahoo.com/quote/HZNP/) |
| **IONS** | FLAT | 46% | Market order (volatile) | 12.2% below entry | 9.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=IONS) / [Yahoo](https://finance.yahoo.com/quote/IONS/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -1.77 (target > 0.5)
- Max drawdown: -5.24% (target > -20%)
- Alpha: -9.36% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
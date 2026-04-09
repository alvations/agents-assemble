# LOSING Strategy: boring_compounder

> **What it does:** Quiet compounders in boring industries: pool supply, uniforms, fasteners, packaging
>
> **Hypothesis:** Boring Compounder 20% Club 3Y

**Generated:** 2026-04-08T22:00:17.462008
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 3.12%
- **sharpe_ratio:** -0.11
- **max_drawdown:** -30.24%
- **win_rate:** 51.33%
- **alpha:** -7.63%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 30.2%
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
| **POOL** | BUY | 33% | Market order (volatile) | 34.5% below entry | 6.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=POOL) / [Yahoo](https://finance.yahoo.com/quote/POOL/) |
| **FAST** | BUY | 25% | Limit 0.5% below market | 25.9% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=FAST) / [Yahoo](https://finance.yahoo.com/quote/FAST/) |
| **WSO** | BUY | 32% | Market order (volatile) | 33.3% below entry | 6.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=WSO) / [Yahoo](https://finance.yahoo.com/quote/WSO/) |
| **ODFL** | BUY | 39% | Market order (volatile) | 40.0% below entry | 8.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ODFL) / [Yahoo](https://finance.yahoo.com/quote/ODFL/) |
| **CTAS** | BUY | 23% | Limit 0.5% below market | 23.7% below entry | 4.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CTAS) / [Yahoo](https://finance.yahoo.com/quote/CTAS/) |
| **TDY** | BUY | 24% | Limit 0.5% below market | 24.8% below entry | 5.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TDY) / [Yahoo](https://finance.yahoo.com/quote/TDY/) |
| **MORN** | BUY | 27% | Limit 0.5% below market | 28.8% below entry | 5.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MORN) / [Yahoo](https://finance.yahoo.com/quote/MORN/) |
| **ROP** | BUY | 23% | Limit 0.5% below market | 23.9% below entry | 4.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ROP) / [Yahoo](https://finance.yahoo.com/quote/ROP/) |
| **CLH** | BUY | 28% | Limit 0.5% below market | 29.2% below entry | 5.8% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CLH) / [Yahoo](https://finance.yahoo.com/quote/CLH/) |
| **LII** | BUY | 34% | Market order (volatile) | 35.5% below entry | 7.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LII) / [Yahoo](https://finance.yahoo.com/quote/LII/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.11 (target > 0.5)
- Max drawdown: -30.24% (target > -20%)
- Alpha: -7.63% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
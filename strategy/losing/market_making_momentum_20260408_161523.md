# LOSING Strategy: market_making_momentum

> **What it does:** Multi-factor momentum + short-term mean-reversion entry, Citadel-inspired
>
> **Hypothesis:** Market-Making Momentum (Citadel-style) 3Y

**Generated:** 2026-04-08T16:15:23.187255
**Assessment:** NEUTRAL — Mixed signals. Paper trade before committing capital.

## Performance Summary
- **total_return:** 1.84%
- **sharpe_ratio:** -0.21
- **max_drawdown:** -16.77%
- **win_rate:** 50.53%
- **alpha:** -8.05%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 20.1%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 16.8%
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
| **UNH** | BUY | 43% | Market order (volatile) | 36.5% below entry | 9.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=UNH) / [Yahoo](https://finance.yahoo.com/quote/UNH/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 18.3% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **LLY** | BUY | 38% | Market order (volatile) | 32.3% below entry | 8.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LLY) / [Yahoo](https://finance.yahoo.com/quote/LLY/) |
| **XOM** | BUY | 23% | Limit 0.5% below market | 19.7% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=XOM) / [Yahoo](https://finance.yahoo.com/quote/XOM/) |
| **JPM** | BUY | 25% | Limit 0.5% below market | 21.5% below entry | 5.3% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **GS** | BUY | 31% | Market order (volatile) | 26.4% below entry | 6.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GS) / [Yahoo](https://finance.yahoo.com/quote/GS/) |
| **MA** | BUY | 22% | Limit 0.5% below market | 18.2% below entry | 4.5% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MA) / [Yahoo](https://finance.yahoo.com/quote/MA/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 27.6% below entry | 6.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.21 (target > 0.5)
- Max drawdown: -16.77% (target > -20%)
- Alpha: -8.05% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
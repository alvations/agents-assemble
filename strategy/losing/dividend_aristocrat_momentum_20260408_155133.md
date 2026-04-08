# LOSING Strategy: dividend_aristocrat_momentum

> **What it does:** Quality dividends + momentum: only buy Aristocrats in uptrends
>
> **Hypothesis:** Dividend Aristocrat Momentum 3Y

**Generated:** 2026-04-08T15:51:32.335679
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -0.80%
- **sharpe_ratio:** -0.33
- **max_drawdown:** -15.48%
- **win_rate:** 51.99%
- **alpha:** -8.93%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 18.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 15.5%
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
| **SHW** | BUY | 24% | Limit 0.5% below market | 18.8% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHW) / [Yahoo](https://finance.yahoo.com/quote/SHW/) |
| **ABT** | BUY | 22% | Limit 0.5% below market | 17.1% below entry | 4.6% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ABT) / [Yahoo](https://finance.yahoo.com/quote/ABT/) |
| **ADP** | BUY | 20% | Limit 0.5% below market | 15.6% below entry | 4.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ADP) / [Yahoo](https://finance.yahoo.com/quote/ADP/) |
| **AFL** | BUY | 20% | Limit 0.5% below market | 15.6% below entry | 4.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AFL) / [Yahoo](https://finance.yahoo.com/quote/AFL/) |
| **CVX** | BUY | 23% | Limit 0.5% below market | 18.1% below entry | 4.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=CVX) / [Yahoo](https://finance.yahoo.com/quote/CVX/) |
| **ITW** | BUY | 21% | Limit 0.5% below market | 16.4% below entry | 4.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=ITW) / [Yahoo](https://finance.yahoo.com/quote/ITW/) |
| **KMB** | BUY | 24% | Limit 0.5% below market | 18.9% below entry | 5.1% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=KMB) / [Yahoo](https://finance.yahoo.com/quote/KMB/) |
| **PG** | BUY | 18% | Limit 0.5% below market | 14.3% below entry | 3.9% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=PG) / [Yahoo](https://finance.yahoo.com/quote/PG/) |
| **SYY** | BUY | 25% | Limit 0.5% below market | 19.2% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SYY) / [Yahoo](https://finance.yahoo.com/quote/SYY/) |
| **APD** | BUY | 27% | Limit 0.5% below market | 21.0% below entry | 5.7% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=APD) / [Yahoo](https://finance.yahoo.com/quote/APD/) |
| **EMR** | BUY | 31% | Market order (volatile) | 23.9% below entry | 6.4% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=EMR) / [Yahoo](https://finance.yahoo.com/quote/EMR/) |
| **LOW** | BUY | 25% | Limit 0.5% below market | 19.2% below entry | 5.2% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LOW) / [Yahoo](https://finance.yahoo.com/quote/LOW/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.33 (target > 0.5)
- Max drawdown: -15.48% (target > -20%)
- Alpha: -8.93% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
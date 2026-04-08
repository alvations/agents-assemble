# WINNING Strategy: barbell_portfolio

> **What it does:** Short bonds + long bonds + growth equities — skip the middle
>
> **Hypothesis:** Barbell Portfolio 3Y

**Generated:** 2026-04-08T14:18:34.818622
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 65.64%
- **sharpe_ratio:** 0.89
- **max_drawdown:** -27.61%
- **win_rate:** 52.66%
- **alpha:** 9.72%

## Risk Parameters
- **max_portfolio_allocation:** 9.1%
- **stop_loss:** 25.0%
- **take_profit_target:** 9.2%
- **max_drawdown_tolerance:** 27.6%
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
| **SHY** | BUY | 2% | Limit 0.5% below market | 12.5% below entry | 4.6% above entry | 18.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 13.2% below entry | 4.9% above entry | 17.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 40.0% below entry | 18.8% above entry | 4.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 8.9% above entry | 9.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 25.6% below entry | 9.4% above entry | 8.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 31.4% below entry | 11.5% above entry | 7.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 34.3% below entry | 12.6% above entry | 6.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

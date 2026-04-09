# WINNING Strategy: barbell_portfolio

> **What it does:** Short bonds + long bonds + growth equities — skip the middle
>
> **Hypothesis:** Barbell Portfolio 4Y (2022-2025)

**Generated:** 2026-04-08T23:04:02.829002
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 102.23%
- **sharpe_ratio:** 0.96
- **max_drawdown:** -27.61%
- **win_rate:** 54.19%
- **alpha:** 8.44%

## Risk Parameters
- **max_portfolio_allocation:** 10.1%
- **stop_loss:** 25.0%
- **take_profit_target:** 9.7%
- **max_drawdown_tolerance:** 27.6%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** Enter on any weekly rebalance day. Monitor SMA200 for trend confirmation.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **SHY** | BUY | 2% | Limit 0.5% below market | 12.5% below entry | 4.8% above entry | 20.1% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 13.2% below entry | 5.1% above entry | 19.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 40.0% below entry | 19.7% above entry | 4.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **GLD** | BUY | 23% | Limit 0.5% below market | 24.1% below entry | 9.3% above entry | 10.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 25.6% below entry | 9.9% above entry | 9.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **GOOGL** | BUY | 30% | Limit 0.5% below market | 31.4% below entry | 12.1% above entry | 8.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GOOGL) / [Yahoo](https://finance.yahoo.com/quote/GOOGL/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 34.3% below entry | 13.2% above entry | 7.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

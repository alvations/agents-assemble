# WINNING Strategy: adaptive_ensemble

> **What it does:** Regime-switching: momentum in bulls, defensive in bears, quality in transitions
>
> **Hypothesis:** Adaptive Ensemble — consistency: 100% across 6 windows

**Generated:** 2026-04-09T08:38:45.678981
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 84.05%
- **sharpe_ratio:** 1.22
- **max_drawdown:** -13.24%
- **win_rate:** 56.72%
- **alpha:** -0.50%

## Risk Parameters
- **max_portfolio_allocation:** 12.9%
- **stop_loss:** 15.9%
- **take_profit_target:** 11.3%
- **max_drawdown_tolerance:** 13.2%
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
| **GLD** | BUY | 23% | Limit 0.5% below market | 15.3% below entry | 10.9% above entry | 13.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GLD) / [Yahoo](https://finance.yahoo.com/quote/GLD/) |
| **SHY** | BUY | 2% | Limit 0.5% below market | 7.9% below entry | 5.7% above entry | 25.8% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SHY) / [Yahoo](https://finance.yahoo.com/quote/SHY/) |
| **VIG** | BUY | 14% | Limit 0.5% below market | 9.2% below entry | 6.5% above entry | 22.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VIG) / [Yahoo](https://finance.yahoo.com/quote/VIG/) |
| **QQQ** | BUY | 22% | Limit 0.5% below market | 14.5% below entry | 10.3% above entry | 14.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=QQQ) / [Yahoo](https://finance.yahoo.com/quote/QQQ/) |
| **NVDA** | BUY | 49% | Market order (volatile) | 32.5% below entry | 23.1% above entry | 6.3% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=NVDA) / [Yahoo](https://finance.yahoo.com/quote/NVDA/) |
| **MSFT** | BUY | 24% | Limit 0.5% below market | 16.3% below entry | 11.6% above entry | 12.6% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=MSFT) / [Yahoo](https://finance.yahoo.com/quote/MSFT/) |
| **AMZN** | BUY | 33% | Market order (volatile) | 21.8% below entry | 15.5% above entry | 9.4% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AMZN) / [Yahoo](https://finance.yahoo.com/quote/AMZN/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

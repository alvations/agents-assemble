# LOSING Strategy: bond_fixed_income

> **What it does:** Diversified bonds: duration ladder + credit spectrum + EM, 3-5% yield target
>
> **Hypothesis:** Bond & Fixed Income Portfolio 3Y

**Generated:** 2026-04-08T22:20:25.788682
**Assessment:** AVOID — Strategy is destroying capital. Do NOT deploy. Needs fundamental redesign.

## Performance Summary
- **total_return:** -7.49%
- **sharpe_ratio:** -0.77
- **max_drawdown:** -19.46%
- **win_rate:** 49.87%
- **alpha:** -11.23%

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 23.3%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 19.5%
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
| **TLT** | BUY | 13% | Limit 0.5% below market | 12.3% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |
| **LQD** | BUY | 7% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=LQD) / [Yahoo](https://finance.yahoo.com/quote/LQD/) |
| **HYG** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=HYG) / [Yahoo](https://finance.yahoo.com/quote/HYG/) |
| **VWOB** | BUY | 6% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VWOB) / [Yahoo](https://finance.yahoo.com/quote/VWOB/) |
| **SCHI** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SCHI) / [Yahoo](https://finance.yahoo.com/quote/SCHI/) |
| **VTEB** | BUY | 4% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=VTEB) / [Yahoo](https://finance.yahoo.com/quote/VTEB/) |
| **AGG** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=AGG) / [Yahoo](https://finance.yahoo.com/quote/AGG/) |
| **BND** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=BND) / [Yahoo](https://finance.yahoo.com/quote/BND/) |
| **FBND** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=FBND) / [Yahoo](https://finance.yahoo.com/quote/FBND/) |
| **SPBO** | BUY | 5% | Limit 0.5% below market | 11.7% below entry | 3.0% above entry | 0.0% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=SPBO) / [Yahoo](https://finance.yahoo.com/quote/SPBO/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

## Lessons Learned

This strategy lost money. Key issues:
- Sharpe ratio: -0.77 (target > 0.5)
- Max drawdown: -19.46% (target > -20%)
- Alpha: -11.23% (target > 0%)

**DO NOT REPEAT** these patterns without fundamental strategy changes.
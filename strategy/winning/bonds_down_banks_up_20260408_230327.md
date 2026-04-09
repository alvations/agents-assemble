# WINNING Strategy: bonds_down_banks_up

> **What it does:** Rising rates crush bonds but boost banks (wider NIM) + insurance (float income). TLT↓ = XLF↑.
>
> **Hypothesis:** Bonds Down → Banks Up (Rate Rotation) 4Y (2022-2025)

**Generated:** 2026-04-08T23:03:27.936532
**Assessment:** HOLD — Positive but underwhelming returns. Use as diversifier, not primary strategy.

## Performance Summary
- **total_return:** 20.23%
- **sharpe_ratio:** 0.12
- **max_drawdown:** -29.00%
- **win_rate:** 53.69%
- **alpha:** -6.14%

## Risk Parameters
- **max_portfolio_allocation:** 4.2%
- **stop_loss:** 25.0%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 29.0%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** 0.5% below current price for buys
- **timing:** TRIGGER: Enter when TLT breaks below SMA200 (rates rising). Exit when bonds recover.
- **scaling:** Enter in 3 tranches over 1-2 weeks to average in

## Positions — Vol-Adjusted Risk (per-stock sizing)

*Each position has different stop/target/size based on its volatility. Higher vol = wider stop + smaller size.*

| Symbol | Action | Vol | Entry | Stop Loss | Take Profit | Size | Live Price |
|--------|--------|-----|-------|-----------|-------------|------|------------|
| **JPM** | BUY | 25% | Limit 0.5% below market | 26.7% below entry | 5.3% above entry | 3.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=JPM) / [Yahoo](https://finance.yahoo.com/quote/JPM/) |
| **GS** | BUY | 31% | Market order (volatile) | 32.7% below entry | 6.5% above entry | 3.2% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=GS) / [Yahoo](https://finance.yahoo.com/quote/GS/) |
| **TLT** | BUY | 13% | Limit 0.5% below market | 13.2% below entry | 3.0% above entry | 7.9% of portfolio | [Chart](https://www.tradingview.com/chart/?symbol=TLT) / [Yahoo](https://finance.yahoo.com/quote/TLT/) |

> **Vol-adjusted sizing:** Volatile stocks (TSLA, NVDA) get wider stops + smaller positions.
> Stable stocks (KO, PG) get tighter stops + larger positions. This is proper risk management.
> Click Live Price links for current market price. Apply % rules to calculate exact levels.

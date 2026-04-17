# WINNING Strategy: tax_harvest_rotation

> ⚠ **Stale data:** This strategy is no longer in the active backtest universe. Numbers below reflect an earlier run under the prior flat-averaged composite formula. Re-run `scripts/update_strategy_composites.py` after adding the strategy back to the registry.

**Generated:** 2026-04-13T18:32:38.801797
**Assessment:** BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

## Performance Summary
- **total_return:** 86.97%
- **sharpe_ratio:** 1.22
- **max_drawdown:** -18.57%
- **win_rate:** 50.00%
- **alpha:** N/A

## Risk Parameters
- **max_portfolio_allocation:** 0.0%
- **stop_loss:** 18.6%
- **take_profit_target:** 5.0%
- **max_drawdown_tolerance:** 18.6%
- **rebalance_frequency:** weekly

## Execution Guidance
- **order_type:** limit
- **limit_offset:** limit: Buy 0.5% below market in uptrend.
- **timing:** SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.
- **scaling:** Enter in 3 tranches over 1-2 weeks.

<details>
<summary>For passive investors (buy and hold)</summary>

### Long-Horizon Performance

| Metric | Value |
|--------|-------|
| **Avg 5Y Return** | 95.4% |
| **Avg 5Y Sharpe** | 0.62 |
| **Avg 5Y Max DD** | -27.5% |
| **10Y Return (2015-2024)** | 241.2% |
| **10Y Sharpe** | 0.58 |
| **10Y Max DD** | -29.6% |
| **HODL Composite** | 0.40 |
| **Windows Tested** | 28 |
| **Consistency** | 93% |

### How to Use This Strategy Passively

This strategy has decent long-term performance. **Consider allocating 5-10% of portfolio.** Rebalance quarterly. Use the strategy orchestrator for regime-aware allocation.

</details>

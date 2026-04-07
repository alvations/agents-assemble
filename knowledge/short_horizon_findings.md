# Short Horizon (<1Y) Strategy Findings

## Key Finding: 13F-Based Strategies Don't Work Short-Term

Tested Ackman, Druckenmiller, Cathie Wood, Momentum Crash-Hedged, and
Concentrate Winners on 1M, 3M, 6M horizons. Most returned 0% because:

1. **SMA200 needs 200 trading days** — on a 1-3 month backtest, there's
   no SMA200 data to generate signals
2. **Monthly rebalancing** — on 1M horizon, only 1 rebalance happens
3. **13F filings are quarterly** — by definition lagged, not intraday

## Which Strategies Work at Each Horizon

| Horizon | Best Strategy Type | Why |
|---------|-------------------|-----|
| Intraday | News Reaction, Volume spikes | Requires real-time data |
| 1 week | Not backtestable with daily data | Need intraday bars |
| 1 month | Crisis Alpha (daily signals) | Uses daily return + vol |
| 3 months | Dual Momentum, Quality Factor | Uses SMA50 only |
| 6 months | Most strategies start working | SMA200 kicks in |
| 1-3 years | Momentum, Concentrate Winners | Sweet spot |
| 5-10 years | Kelly, Multi-Factor, Global Rotation | Long-term compounding |

## Strategies That SHOULD Work Short-Term (need separate backtester)
- News Reaction Momentum (daily signals via volume spikes)
- Earnings Surprise Drift (event-driven, daily)
- Crisis Alpha (daily vol monitoring)
- Tail Risk Harvest (daily crash detection)

## Recommendation
For <1Y horizons, use strategies with SMA20/SMA50 signals, not SMA200.
Or use event-driven strategies (news, earnings, volume spikes).

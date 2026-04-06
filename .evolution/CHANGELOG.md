# Evolution Changelog

## [2026-04-06T13:07:11.938870+00:00] Branch: main | Run: 20260406T130441_pid56839 | Iter 1 | $0.3981
### backtester.py
All edits pass syntax validation. Here's what was changed:

- **Fixed `Position.update` short position handling**: BUY on a short position now correctly computes realized P&L when covering, and SELL on an existing short now blends avg_cost instead of incorrectly computing phantom P&L. Both branches handle position flips (short→long, long→short) and full closes properly.
- **Fixed Sortino ratio calculation**: Replaced incorrect `std()` of only negative returns with the standard downside deviation

## [2026-04-06T13:09:38.502606+00:00] Branch: main | Run: 20260406T130441_pid56839 | Iter 2 | $0.4508
### backtester.py
All edits pass syntax validation. Here's what was changed:

- **Fixed `_rebalance` leaking short positions**: Positions not in target weights are now properly closed regardless of direction — short positions get bought back (BUY), not just long positions sold.
- **Fixed benchmark CAGR using wrong time span**: `bench_cagr` now uses `aligned_n_years` (from the aligned overlap period), and alpha compares portfolio vs benchmark CAGR over the same aligned window, preventing systematic misstatement wh

## [2026-04-06T13:11:17.106397+00:00] Branch: main | Run: 20260406T130441_pid56839 | Iter 3 | $0.3461
### backtester.py
All edits pass syntax validation. Here's what was changed:

- **Fixed information ratio numerator**: Used `port_aligned_cagr` instead of full-period `cagr`, making it consistent with the aligned-window alpha fix from iteration 2.
- **Fixed `_rebalance` sell qty cap for short positions**: The cap `min(qty, abs(current_pos.quantity))` now only applies when the position is long (`current_pos.quantity > 0`), allowing short positions to be increased via additional sells.
- **Fixed missing equity curv

## [2026-04-06T13:13:15.452499+00:00] Branch: main | Run: 20260406T131125_pid57575 | Iter 1 | $0.3467
### data_fetcher.py
Syntax is valid. Here's a summary of the changes:

- **Fixed `fetch_yield_curve` ignoring pre-2024 dates** — The hardcoded `start="2024-01-01"` meant calling `fetch_yield_curve(date="2023-06-15")` would silently return wrong data. Now dynamically adjusts start date based on the requested date.
- **Removed dead `not df.empty` guard in `fetch_ohlcv`** — Line 155 was unreachable since line 152-153 already raises `ValueError` on empty data.
- **Fixed `screen_by_fundamentals` filter checks** — Change

## [2026-04-06T13:14:59.436927+00:00] Branch: main | Run: 20260406T131125_pid57575 | Iter 2 | $0.4125
### data_fetcher.py
Syntax is valid. Here's a summary of the changes:

- **Fixed `fetch_yield_curve` for arbitrary historical dates** — Instead of the incomplete `"2020-01-01"` / `"2024-01-01"` conditional, now computes start as 1 year before the requested date, so any date (e.g., "2015-06-15") will be in range.
- **Fixed `fetch_fred_series` CSV fallback index name mismatch** — API path produced index `"date"`, CSV fallback produced `"DATE"`. Now normalizes to `"date"` so downstream code works consistently regardle

## [2026-04-06T13:16:50.859300+00:00] Branch: main | Run: 20260406T131125_pid57575 | Iter 3 | $0.3844
### data_fetcher.py
Syntax is valid. Here's a summary of the changes:

- **Fixed `fetch_multiple_ohlcv` single-symbol batch inconsistency** — `yf.download([sym], group_by="ticker")` produces multi-level columns unlike `Ticker.history()`. Now skips batch for single symbols and falls through to the individual `fetch_ohlcv` fallback path, ensuring consistent DataFrame structure.
- **Fixed `fetch_yield_curve(date=None)` stale hardcoded start** — Replaced `"2024-01-01"` with dynamic `(now - 90 days)` so the function sta

## [2026-04-06T13:18:24.840830+00:00] Branch: main | Run: 20260406T131655_pid58052 | Iter 1 | $0.3234
### personas.py
All edits pass syntax validation. Summary of changes:

- **Fix `_get_indicator` silent wrong-answer bug**: `get_indexer` can return -1 (empty index, NaT); `df.iloc[-1]` would silently return the last row. Now returns `None` when idx is -1.
- **Fix `QuantStrategist` candidate ranking**: candidates were sliced `[:max_positions]` in iteration order, not by score. Added `sort(key=score, reverse=True)` so the best mean-reversion signals are selected.
- **Fix `GrowthInvestor` truthiness check on RSI**

## [2026-04-06T13:20:04.929723+00:00] Branch: main | Run: 20260406T131655_pid58052 | Iter 2 | $0.3540
### personas.py
All edits pass syntax validation. Summary of changes:

- **Fix `QuantStrategist` vol-weighted sizing denominator**: `total_inv_vol` was computed over ALL candidates but only top N were allocated — diluting weights. Now computed only over the top N slice.
- **Fix `MemeStockTrader` exit signal overwritten by buy**: A breakout (vol_ratio > 3, price > sma20) with RSI > 80 could score for buy AND trigger exit, with the buy overwriting the exit weight. Restructured as `elif` so exit conditions take pr

## [2026-04-06T13:22:02.502734+00:00] Branch: main | Run: 20260406T131655_pid58052 | Iter 3 | $0.4277
### personas.py
All edits pass syntax validation. Summary of changes:

- **Remove dead `sma50` fetch in `BuffettValue`**: `sma_50` was fetched on every symbol but never used — wasted indicator lookup removed.
- **Fix `DividendInvestor` RSI truthiness bug**: `if rsi and rsi < 40` → `if rsi is not None and rsi < 40` — RSI of exactly 0.0 would have skipped the oversold bonus due to falsy float.
- **Fix `FixedIncomeStrat` TIP RSI truthiness bug**: Same pattern — `if tlt_rsi and tlt_rsi < 30` → `if tlt_rsi is not No

## [2026-04-06T13:31:11.186567+00:00] Branch: main | Run: 20260406T132815_pid59005 | Iter 4 | $0.4994
### backtester.py
All edits pass syntax validation. Here's what was changed:

- **Fixed phantom equity drops from missing data**: When using a union date index, days where a symbol had no price data excluded that position's value from `total_value`, creating false drawdowns and inflated volatility. Now carries forward last-known prices so positions are always valued consistently.
- **Fixed `_rebalance` executing buys before sells**: Previously, iteration order determined trade execution, so a buy could fail the c

## [2026-04-06T13:42:37.328408+00:00] Branch: main | Run: 20260406T132815_pid59005 | Iter 5 | $1.3981
### backtester.py
All edits pass syntax validation. Here's what was changed:

- **Removed sell qty cap in `_rebalance`**: The `min(qty, int(current_pos.quantity))` cap prevented strategies from flipping long-to-short in a single rebalance. Since `Position.update` handles flips correctly and the cap is mathematically redundant for non-negative target weights, removing it fixes the bug.
- **Recompute total value after sells**: Buy quantities are now computed from post-sell portfolio value instead of stale pre-sell 


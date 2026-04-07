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

## [2026-04-06T13:54:18.755315+00:00] Branch: main | Run: 20260406T132815_pid59005 | Iter 6 | $1.3470
### backtester.py
All edits pass syntax validation. Here's what was changed:

- **Pre-computed close prices DataFrame for performance**: Replaced the set-based date union construction and per-date per-symbol `.loc` lookups with a single `pd.DataFrame` of close prices, sorted and forward-filled via `.ffill()`. This eliminates O(n_dates × n_symbols) individual index lookups and the manual `last_known_prices` accumulator, replacing them with a one-time vectorized operation.
- **Simplified simulation loop**: Removed 

## [2026-04-06T13:54:44.710825+00:00] Branch: main | Run: 20260406T135045_pid60422 | Iter 3 | $0.3888
### run_hypotheses.py
Syntax is clean. Here's what I changed:

- **Fixed global state mutation** — `run_all` now shallow-copies `HYPOTHESES` dicts before overwriting `start`/`end`, so repeated calls with different dates don't corrupt the module-level data.
- **Fixed alpha formatting in summary table** — Alpha was printed as a raw float (e.g., `0.053`) instead of formatted as `5.3%`. Now properly formats as percentage when numeric, falls back to `"N/A"` when missing.
- **Fixed `--list` showing only builtin personas** 

## [2026-04-06T14:11:50.712719+00:00] Branch: main | Run: 20260406T140930_pid62145 | Iter 1 | $0.3446
### recession_strategies.py
Syntax is clean. Here's what I changed:

- **Fixed truthiness bugs in `detect_recession_regime`**: Changed 5 checks from `if val:` to `if val is not None:` — RSI of 0 or vol of 0.0 were incorrectly treated as missing data, skipping the signal entirely
- **Fixed same bug in `GoldBug.generate_signals`**: `gld_sma50 and gld_sma200 and gld_price` → explicit `is not None` checks
- **Fixed misleading comment**: `# 3+ signals` → `# majority of available signals` since the threshold is 50% of *available

## [2026-04-06T14:18:35.923169+00:00] Branch: main | Run: 20260406T140930_pid62145 | Iter 2 | $0.9846
### recession_strategies.py
Syntax is clean. Here's what I changed:

- **Eliminated redundant SPY lookups in `detect_recession_regime`**: `spy_sma200` was fetched twice (signals 1 and 2), and `"SPY" in data` was checked 3 separate times. All 5 SPY indicators are now fetched once upfront.
- **Added staleness guard to `_safe_get`**: The nearest-date fallback via `get_indexer(method="nearest")` could return arbitrarily old data (months/years stale). Now rejects data more than 10 days from the requested date.
- **Fixed NaN bug

## [2026-04-06T14:21:05.830296+00:00] Branch: main | Run: 20260406T140930_pid62145 | Iter 3 | $0.4433
### recession_strategies.py
Syntax is clean. Here's what I changed:

- **Filtered `RecessionDetector.generate_signals` returns by `prices`**: Both branches now return `{k: v for k, v in weights.items() if k in prices}`, matching the pattern used by `DefensiveRotation` and `GoldBug` — prevents returning weights for symbols the backtester can't trade
- **Filtered `TreasurySafe.generate_signals` returns by `prices`**: All three branches (recession/mixed/clear) now filter the same way — same consistency fix
- **Fixed duplicate

## [2026-04-06T14:22:04.935353+00:00] Branch: main | Run: 20260406T142016_pid62900 | Iter 1 | $0.3531
### judge.py
Syntax is valid. Summary of changes:

- **Removed dead imports**: `json`, `numpy`, `pandas`, and `Tuple` were imported but never used; replaced with `math` (needed for NaN/inf check)
- **Fixed NaN/inf bug in `grade_metric`**: Added `math.isfinite()` guard — metrics producing `NaN` (e.g., Sharpe when vol=0) or `inf` (e.g., profit_factor with zero losses) now correctly grade as "F" instead of silently getting wrong grades
- **Extracted `GRADE_SCORES` to module-level constant**: Was being recreated

## [2026-04-06T14:24:05.275230+00:00] Branch: main | Run: 20260406T142016_pid62900 | Iter 2 | $0.4465
### judge.py
Syntax is valid. Summary of changes:

- **Fixed `grade_metric` for unknown metrics**: Returns "F" instead of silently grading as "A" when a metric isn't in `GRADE_THRESHOLDS` (the old `{}.get(grade, -999)` fallback meant any value passed all thresholds)
- **Fixed missing `max_drawdown` false-A bug**: Added `_METRIC_MISSING_DEFAULTS` so missing `max_drawdown` defaults to -1.0 (grade "F") instead of 0 (grade "A" — "no drawdown")
- **Cleaned up empty report sections**: "Strengths:" and "Weaknesses:

## [2026-04-06T14:25:47.123105+00:00] Branch: main | Run: 20260406T142016_pid62900 | Iter 3 | $0.3586
### judge.py
All tests pass. Summary of changes:

- **Fixed crash on `None`/non-numeric metric values**: Added `_safe_float()` helper; `grade_metric` now returns "F" for `None`, strings, etc. instead of raising `TypeError`
- **Eliminated duplicate grading in `diagnose_strategy`**: Composite score is now computed directly from already-graded values instead of calling `compute_composite_score` which re-grades every metric
- **Fixed inconsistent missing-metric defaults in suggestion logic**: `diagnose_strategy`

## [2026-04-07T08:53:17.596650+00:00] Branch: main | Run: 20260407T085049_pid33764 | Iter 1 | $0.6318
### famous_investors.py
All edits pass syntax check. Summary of changes:

- **Removed unused imports**: `dataclass`, `field`, `Any`, `Dict`, `numpy` — none were referenced in the file
- **Removed dead variable** in `PeterLynch.generate_signals`: `ret` (daily_return) was fetched but never used
- **Removed dead variable** in `NassefSawiris.generate_signals`: `sma50` was fetched but never used
- **Fixed `HowardMarks` buy/exit conflict**: The risk control exit (`price < sma200 * 0.80`) was checked *after* candidates were a

## [2026-04-07T08:55:58.851191+00:00] Branch: main | Run: 20260407T085049_pid33764 | Iter 2 | $0.5898
### famous_investors.py
All edits pass syntax check. Summary of changes:

- **Removed unused `import pandas as pd`** and **`from typing import List, Optional`** — neither is referenced anywhere in the file
- **Modernized type hints** — replaced `Optional[List[str]]` with `list[str] | None` across all 13 classes (already guarded by `from __future__ import annotations`)
- **Removed dead variable `vol`** in `GeorgeSoros.generate_signals` — fetched via `_get_indicator` but never used in any computation or check
- **Removed

## [2026-04-07T08:58:51.009893+00:00] Branch: main | Run: 20260407T085049_pid33764 | Iter 3 | $0.7566
### famous_investors.py
All edits pass syntax check. Summary of changes:

- **Removed dead variable `sma50`** in `CarlIcahn.generate_signals` — fetched via `_get_indicator` but never referenced in the method body
- **Fixed division-by-zero in `PeterLynch`** — added `sma50 > 0` guard before `abs(price - sma50) / sma50` (line 98)
- **Fixed division-by-zero in `JorgePauloLemann`** — added `sma50 > 0` guard with fallback to `1.0` (which skips the proximity bonus) when computing `proximity` (line 824)
- **Fixed division-by-

## [2026-04-07T09:09:58.947502+00:00] Branch: main | Run: 20260407T090350_pid35770 | Iter 1 | $0.2574
### research_strategies.py
Syntax is valid. Summary of changes:

- **Bug fix (LowVolAnomaly line 234)**: Changed `max(n, self.config.max_positions)` → `min(n, self.config.max_positions)`. The old code always selected at least 15 stocks (75% of a 20-stock universe), completely defeating the bottom-quintile selection that is the core of the strategy.
- **Bug fix (DualMomentum line 71)**: Changed truthiness checks (`efa_price and efa_sma200`) to explicit `is not None` checks. A price of `0.0` would have been incorrectly trea

## [2026-04-07T09:17:01.496265+00:00] Branch: main | Run: 20260407T090350_pid35770 | Iter 2 | $0.3824
### research_strategies.py
All edits pass syntax validation. Summary of changes:

- **Bug fix (MultiFactorSmartBeta lines 142, 145, 148, 155)**: Changed truthiness checks on `sma50`, `sma200`, `rsi` to proper `is not None` checks or removed redundant guards. A 0.0 value would have incorrectly skipped momentum/quality scoring — same bug class fixed in iteration 1 for DualMomentum.
- **Bug fix (RiskParityMomentum line 383)**: Changed `if sma50 and` → `if sma50 is not None and` to prevent 0.0 values from bypassing the moment

## [2026-04-07T09:18:31.969963+00:00] Branch: main | Run: 20260407T090350_pid35770 | Iter 3 | $0.3429
### research_strategies.py
All edits pass syntax validation. Summary of changes:

- **Bug fix (LowVolAnomaly line 223)**: Changed `if sma200 and` → `if sma200 is not None and` — a 0.0 SMA200 value would skip the downtrend filter, allowing broken-trend stocks into the low-vol portfolio. Same bug class fixed in iterations 1-2.
- **Bug fix (GlobalRotation line 535)**: Changed `if vol and vol > 0:` → `if vol is not None and vol > 0:` — explicit None check for consistency and correctness.
- **Bug fix (GlobalRotation line 540)*

## [2026-04-07T09:20:49.659659+00:00] Branch: main | Run: 20260407T091902_pid38331 | Iter 1 | $0.4585
### unconventional_strategies.py
All changes pass syntax check. Summary:

- **Removed unused imports** `Dict` and `Any` — dead code cleanup
- **Filtered `SellInMayGoAway` and `TurnOfMonth` signals by `prices`** — these were the only two strategies returning hard-coded symbol dicts without checking if the symbols exist in the price data, which could cause downstream issues in the backtester
- **Fixed `TailRiskHarvest` exit/crash-buy conflict** — moved exit check before crash-buy check with `continue`, so a position marked for ex


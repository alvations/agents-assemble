# Backtest Results Archive

## File Structure

```
results/
  _multi_window_full_YYYYMMDD_HHMMSS.json   # Canonical MW snapshots (ALL strategies, ALL 28 windows)
  {strategy_name}_YYYYMMDD_HHMMSS.json       # Individual strategy results (latest 3Y window + rolling windows)
  README.md                                   # This file
```

## Multi-Window (MW) Files

Each MW JSON contains ALL strategies backtested across ALL 28 rolling windows. These are the **source of truth** for leaderboard generation.

**Schema per strategy:**
```json
{
  "strategy_name": {
    "src": "category (theme, unconventional, portfolio, etc.)",
    "desc": "strategy description",
    "w": {
      "1Y_2015": {"ret": 0.1234, "sh": 0.56, "dd": -0.0789},
      "1Y_2016": {...},
      "3Y_2015_2017": {...},
      "5Y_2015_2019": {...},
      "10Y_2015_2024": {...}
    },
    "consistency": 0.79,
    "composite": 0.085,
    "hodl_composite": 0.138
  }
}
```

**Windows:** 28 total
- 1Y: 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025 (11)
- 3Y: 2015-2017 through 2023-2025 (9)
- 5Y: 2015-2019 through 2021-2025 (7)
- 10Y: 2015-2024 (1)

**Composites:**
- `composite` = LB composite (6 windows 2022-2025): `Avg Return × Consistency × (1 - Avg |MaxDD|)`
- `hodl_composite` = HODL composite (all 28 windows): same formula
- `consistency` = % of windows with positive Sharpe (0-1 scale)

## Individual Result Files

Per-strategy JSON with full metrics from the latest backtest run.

**Schema:**
```json
{
  "metrics": {
    "total_return": 0.2465,
    "cagr": 0.0765,
    "annual_volatility": 0.1346,
    "sharpe_ratio": 0.3255,
    "sortino_ratio": 0.4445,
    "calmar_ratio": 0.4445,
    "max_drawdown": -0.1721,
    "win_rate": 0.5326,
    "profit_factor": 1.1153
  },
  "final_positions": {"AAPL": {"qty": 50, "avg_cost": 170.5}, ...},
  "rolling_windows": {"1Y_2015": {...}, ...},
  "source": "category"
}
```

## How to Use

### Load latest MW data
```python
import json, glob
mw_files = sorted(glob.glob('results/_multi_window_full_*.json'))
with open(mw_files[-1]) as f:
    mw = json.load(f)
print(f'{len(mw)} strategies')
```

### Compare two MW snapshots (before/after)
```python
with open(mw_files[-2]) as f: old = json.load(f)
with open(mw_files[-1]) as f: new = json.load(f)
for name in new:
    if name in old:
        delta = new[name]['hodl_composite'] - old[name]['hodl_composite']
        if abs(delta) > 0.01:
            print(f'{name}: {old[name]["hodl_composite"]:.3f} -> {new[name]["hodl_composite"]:.3f} ({delta:+.3f})')
```

### Add a new strategy to MW
```python
mw['new_strategy_name'] = {
    'src': 'category',
    'desc': 'what it does',
    'w': window_results,  # dict of 28 windows
    'consistency': 0.85,
    'composite': 0.15,
    'hodl_composite': 0.25,
}
```

### Rebuild leaderboards from MW
```bash
python3 rebuild_leaderboards.py  # auto-detects latest MW file
```

## Naming Convention

- MW files: `_multi_window_full_YYYYMMDD_HHMMSS.json` (underscore prefix = canonical)
- Individual: `{strategy_name}_YYYYMMDD_HHMMSS.json`
- All timestamps are local time at generation

## History

| Date | MW File | Strategies | Notes |
|------|---------|-----------|-------|
| 2026-04-09 | _090034 | 173 | Initial multi-horizon run |
| 2026-04-09 | _101742, _104126 | 195, 204 | Added more strategies |
| 2026-04-10 | _193648 | 204 | Rerun with fixes |
| 2026-04-12 | _185020 | 204 | Full 28-window rerun |
| 2026-04-13 | _134146 | 214 | +10 gap audit strategies |
| 2026-04-13 | _183206 | 224 | +10 new (fixed + gap) |
| 2026-04-13 | _190236 | 227 | +3 AI ecosystem |
| 2026-04-13 | _191533 | 228 | +1 open source AI |
| 2026-04-13 | (running) | 237+ | Full div-adjusted rerun + boring strategies |

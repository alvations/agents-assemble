# Evolution Round 1 Results (2026-04-06)

## Changes Made

### backtester.py (3 iterations, $1.20)
- Fixed Position.update() for proper short/long flips
- Fixed Sortino ratio calculation (proper downside deviation)
- Fixed alpha calculation using aligned period lengths
- RSI edge cases (all-up = 100, flat = 50)
- Cash check includes slippage before buying
- Short position closing in rebalance
- Info ratio uses aligned CAGR

### data_fetcher.py (3 iterations, $1.14)
- Cache-first lookup in fetch_multiple_ohlcv (avoids re-downloading)
- Single-symbol yf.download workaround (use Ticker.history instead)
- FRED CSV index name normalization
- Alpha Vantage rate-limit/error detection
- Yield curve date range fix (uses relative window)
- screen_by_fundamentals: `is not None` checks for 0-value filters

### personas.py (3 iterations, $1.11)
- get_indexer -1 check in _get_indicator
- Meme stock: exit signal takes priority over buy signals
- Dividend: rank + top-N selection (was equal-weighting all)
- Quant: sort + slice before vol-weighting (was vol-weighting ALL then slicing)
- Fixed income: filter weights to tradeable symbols only, cap at max_position_size
- Momentum: RSI/100 tiebreaker for same discrete trend_score
- Growth: removed redundant `rsi and` check

## Performance Comparison (2022-01-01 to 2024-12-31)

| Persona | Before | After | Change |
|---------|--------|-------|--------|
| Momentum | 87.1% (1.10 Sharpe) | 99.0% (1.20 Sharpe) | +12% return, +0.10 Sharpe |
| Growth | 49.4% (0.62) | 49.4% (0.62) | No change (cached data) |
| Buffett | 25.6% (0.77) | 25.6% (0.77) | Same |
| Dividend | 19.7% (0.30) | 18.3% (0.25) | Slight decrease (ranking change) |
| Quant MR | -1.2% (-0.83) | -1.3% (-0.83) | Same |
| Fixed Inc | -2.8% (-0.80) | -2.5% (-0.79) | Slight improvement |
| Meme | -13.3% (-0.04) | -16.3% (-0.12) | Worse (exit priority fix) |

## Key Takeaways
1. Momentum strategy improved most (+12% return) from RSI tiebreaker
2. Meme strategy worse — exit-first logic is correct but more conservative
3. Fixed income slightly better with position cap enforcement
4. Total evolution cost: $3.45

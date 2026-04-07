# Math Strategy Multi-Horizon Results (2026-04-07)

## Kelly Criterion Optimal — THE best math strategy

| Horizon | Return | Sharpe | Max DD |
|---------|--------|--------|--------|
| 1Y (2024) | -1.1% | -0.44 | -10.3% |
| 3Y (2022-2024) | 36.3% | 0.63 | -10.3% |
| 5Y (2020-2024) | 80.1% | 0.71 | -16.8% |
| 10Y (2015-2024) | 217.4% | 0.72 | -16.9% |

**Avg Sharpe (3Y/5Y/10Y):** 0.69

**Key insight:** Kelly sizing works for long-term investing. Weak short-term
because Kelly fraction estimate from 60-day window is noisy on 1Y. Over 5-10Y,
the law of large numbers makes the win rate and payoff ratio estimates more stable.

**Why it works:** Instead of equal-weighting positions, Kelly sizes each position
proportional to its edge (win_rate * payoff - loss_rate) / payoff. Higher-confidence
bets get larger allocations. Half-Kelly provides safety margin.

## Other Math Strategies (3Y only)
- Z-Score Reversion: 0.5% / -1.42 Sharpe — fails because Z<-2 events are rare in uptrend
- Hurst Regime: 13.2% / 0.07 — autocorrelation proxy too noisy for regime detection
- Volatility Breakout: 5.0% / -0.32 — BB breakouts don't capture Turtle-style trends
- ERC: -8.8% / -0.59 — TLT drag during rate hikes killed this

## Lessons
1. Position sizing (Kelly) matters more than signal generation
2. Statistical mean reversion (Z-score) needs more frequent signals to work
3. Autocorrelation is a poor Hurst estimator — need R/S analysis
4. Turtle-style breakouts need true Donchian channels, not BB approximation

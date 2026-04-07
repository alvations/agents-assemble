# Strategy Failures Log

Record of strategies that failed so we don't repeat them.

## Factor ETF Rotation (2026-04-07)
- **Strategy:** Rotate between MTUM, QUAL, VLUE, SPLV, IWM based on momentum
- **Result:** -0.07 avg Sharpe across 1Y/3Y/5Y/10Y
- **Why it failed:** Factor ETFs don't have enough cross-sectional dispersion to
  make rotation profitable. They're all highly correlated (0.85+) with SPY.
  Individual stocks have much more dispersion → better for momentum rotation.
- **Lesson:** Don't rotate between correlated ETFs. Use individual stocks or
  truly uncorrelated asset classes (stocks vs bonds vs gold vs commodities).

## Z-Score Mean Reversion (2026-04-07)
- **Strategy:** Buy at Z < -2, sell at Z > 0 (60-day window)
- **Result:** 0.5% / -1.42 Sharpe on 3Y
- **Why it failed:** Z < -2 events are extremely rare in a bull market.
  Only triggers maybe 5-10 times per year per stock.
- **Lesson:** Statistical signals need higher frequency. Use Z < -1.5 or
  shorter window (20 days instead of 60) for more signals.

## Equal Risk Contribution (2026-04-07)
- **Strategy:** Inverse-vol weighting across asset classes with momentum filter
- **Result:** -8.8% / -0.59 Sharpe on 3Y
- **Why it failed:** TLT (long bonds) dragged portfolio during 2022 rate hikes.
  Risk parity overweighted bonds because they had lower vol.
- **Lesson:** Pure inverse-vol weighting without regime awareness is dangerous.
  Need to exclude falling asset classes entirely, not just underweight them.

## Sell in May (2026-04-07)
- **Strategy:** Stocks Nov-Apr, bonds May-Oct
- **Result:** 2.2% / -0.16 Sharpe on 3Y
- **Why it failed:** Summer 2023 rally was massive (AI boom). Seasonal
  effects too weak to overcome strong fundamental trends.
- **Lesson:** Calendar effects are dominated by macro/fundamental trends.
  Use only as a minor tilt, never as primary signal.

## Self-Evolution Import Failures
- Files importing from other flat files MUST have PYTHONPATH set
- famous_investors.py and theme_strategies.py failed 3+3 = 6 evolution
  iterations ($3+ wasted) before discovering the PYTHONPATH fix
- **Fix:** PYTHONPATH=/path/to/agents-assemble python3 ../self_evolve.py file.py

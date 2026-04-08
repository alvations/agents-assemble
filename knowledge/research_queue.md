# Research Queue — Strategies Pending Implementation

This file tracks strategies discovered by research agents that need to be:
1. Implemented in Python (BasePersona pattern)
2. Backtested on 3Y horizon
3. Added to strategy/winning/ or strategy/losing/
4. Updated in LEADERBOARD.md

**Any agent working on this repo should check this file first.**

## Status: 2026-04-08

### Implemented (need backtest + strategy files)
- [x] stat_arb_medallion (hedge_fund) — Renaissance-style stat arb with mean reversion
- [x] risk_parity (hedge_fund) — Bridgewater-style inverse-vol weighting
- [x] market_making_momentum (hedge_fund) — Citadel-style short-term momentum + vol
- [x] growth_concentration (hedge_fund) — Tiger Global high-conviction growth
- [x] activist_distressed (hedge_fund) — Elliott-style deep value + activist catalyst
- [x] fda_catalyst (news_event) — Biotech FDA approval/rejection plays
- [x] earnings_whisper (news_event) — Pre-earnings drift momentum
- [x] merger_arbitrage (news_event) — M&A announced deal spread capture
- [x] dividend_capture (news_event) — Ex-date dividend trading
- [x] yield_curve_inversion (recession) — Trade based on yield curve inversion/steepening via TLT/SHY ratio
- [x] consumer_credit_stress (recession) — Consumer credit deterioration signal
- [x] unemployment_momentum (recession) — Jobless claims trend-following

### Pending Implementation
(none — all current research has been implemented and backtested)

### Completed 2026-04-08 batch 2
- [x] rare_earth_minerals (crisis_commodity) — -1.8% ret, LOSE
- [x] water_scarcity (crisis_commodity) — -19.8% ret, LOSE
- [x] shipping_freight_cycle (crisis_commodity) — +24.2% ret, WIN
- [x] entropy_regime (math) — +10.7% ret, LOSE (negative Sharpe)
- [x] cointegration_pairs (math) — -6.9% ret, LOSE
- [x] optimal_stopping (math) — -34.0% ret, LOSE

## Process for Converting Research to Strategies

1. Check this file for pending items
2. Implement in the appropriate `*_strategies.py` file using BasePersona pattern
3. Add key to module's registry dict (e.g., RECESSION_STRATEGIES)
4. Run: `python3 -c "import ast; ast.parse(open('file.py').read())"` to verify syntax
5. Run: `python3 sync_package.py` to sync to package
6. Backtest: use Backtester with start='2022-01-01', end='2024-12-31'
7. Save: use save_strategy_recommendation() for strategy/winning/ or strategy/losing/
8. Update LEADERBOARD.md
9. Commit and push
10. Mark item as [x] in this file

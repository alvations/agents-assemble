# agents-assemble

Trading agents and algorithms for publicly tradable instruments on Robinhood / Public.com.

## Architecture

```
agents-assemble/
  data_fetcher.py      — Market data fetching (yfinance, FRED, SEC EDGAR, premium APIs)
  backtester.py        — Event-driven backtesting engine with metrics
  personas.py          — 10 trader persona strategies
  run_hypotheses.py    — Hypothesis testing runner (10 hypotheses)
  judge.py             — Strategy judge: grades, ranks, suggests improvements
  knowledge/           — Saved findings, judge reports, evolution results
  results/             — Backtest result JSON files
  .cache/              — Parquet data cache
  .evolution/          — Self-evolution history
```

## Key design decisions

- **No local data storage** — pull live from yfinance/FRED unless caching for repeated backtests
- **Strategy = callable(date, prices, portfolio, data) -> {symbol: weight}** — all personas share this interface
- **Free data first** — yfinance + FRED CSV work without API keys. Premium sources need env vars.
- **Backtester normalizes tz** — yfinance returns tz-aware, we strip to tz-naive for consistent indexing
- **Union date index** — backtester uses union of all symbols' dates (not intersection) so partial data works

## 10 Personas (ranked by judge score, 2022-2024 backtest)

1. **Momentum** (B, 79) — MACD + SMA alignment on tech leaders. 99% return, 1.20 Sharpe.
2. **Growth** (C, 64) — Dip-buying disruptive stocks in uptrends. 49% return.
3. **Pairs** (C, 64) — Relative value between correlated stocks. 41% return.
4. **Buffett Value** (C, 62) — Deep value, SMA200 discount + RSI. Low DD (-6%).
5. **Dividend** (D, 50) — Equal-weight dividend aristocrats. Stable but no alpha.
6. **Ensemble** (F, 39) — Consensus of momentum+value+growth+dividend. Too conservative.
7. **Sector Rotation** (F, 33) — Rotate into strongest sector ETFs. Needs work.
8. **Fixed Income** (F, 32) — Bond duration via ETF trends. Hurt by rate hikes.
9. **Quant MR** (F, 26) — Mean-reversion (BB+RSI). Failed in trending market.
10. **Meme Stock** (F, 21) — Volume spike dip-buying. Post-bubble wreckage.

## Self-evolution

Uses `self_evolve.py` from parent directory. Each module can be evolved independently:

```bash
cd /Users/alvas/jean-claude
python3 self_evolve.py agents-assemble/backtester.py -n 3 --verbose
python3 self_evolve.py agents-assemble/personas.py -n 3 --verbose
python3 self_evolve.py agents-assemble/data_fetcher.py -n 3 --verbose
```

## API keys (env vars)

- `FRED_API_KEY` — FRED macro data (free registration)
- `FINNHUB_API_KEY` — Social sentiment, news (60 calls/min free)
- `ALPHA_VANTAGE_KEY` — Real-time quotes (5 calls/min free)
- `POLYGON_API_KEY` — Tick data (5 calls/min free, delayed)
- `NEWS_API_KEY` — Financial news headlines (100/day free)

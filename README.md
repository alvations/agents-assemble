# agents-assemble

Trading agents and algorithms for publicly tradable instruments (stocks, ETFs, bonds) on Robinhood / Public.com.

## Architecture

```
agents-assemble/
  data_fetcher.py      — Market data (yfinance, FRED, premium APIs)
  backtester.py        — Event-driven backtesting engine
  personas.py          — 7 trader persona strategies
  run_hypotheses.py    — Hypothesis testing runner
  knowledge/           — Saved findings and research
  results/             — Backtest result JSON files
  .cache/              — Data cache (parquet)
```

## Personas

| Persona | Style | Risk | Rebalance |
|---------|-------|------|-----------|
| Buffett Value | Deep value, buy-and-hold blue chips | Low | Monthly |
| Momentum | Trend-following tech leaders | High | Weekly |
| Meme Stock | Volume spikes, dip buys, YOLO | Very High | Daily |
| Dividend | Dividend aristocrats, compound forever | Very Low | Monthly |
| Quant | Mean-reversion, Bollinger/RSI | Medium | Daily |
| Fixed Income | Bond duration/credit via ETFs | Low | Weekly |
| Growth | Disruptive innovation dip-buying | High | Weekly |

## Quick start

```bash
# Run all hypothesis backtests
python run_hypotheses.py

# Run single persona
python run_hypotheses.py --persona buffett_value

# Custom date range
python run_hypotheses.py --start 2022-01-01 --end 2024-06-30

# Self-evolve the library
cd ..
python self_evolve.py agents-assemble/ -n 3 --verbose
```

## Data sources

### Free (no API key needed)
- **yfinance**: OHLCV, fundamentals, dividends, options
- **FRED CSV**: Treasury yields, macro data (limited)

### Free with API key
- **FRED API**: Full macro/bond data (`FRED_API_KEY`)
- **Finnhub**: Social sentiment, news (`FINNHUB_API_KEY`)
- **Alpha Vantage**: Real-time quotes (`ALPHA_VANTAGE_KEY`)

### Premium
- **Polygon.io**: Tick data, options (`POLYGON_API_KEY`)
- **IEX Cloud**: Real-time US equities (`IEX_CLOUD_KEY`)

Run `python data_fetcher.py` to see API key status.

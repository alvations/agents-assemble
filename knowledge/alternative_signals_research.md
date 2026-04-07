# Alternative Trading Signals Research (2026)

## Signals We Can't Currently Backtest (need premium data)

### 1. Congressional Trading (STOCK Act disclosures)
- Congress members' portfolios consistently outperform market
- 45-day disclosure delay limits edge but still profitable
- Tools: unusualwhales.com, tradercongress.com, quiverquant.com
- **Need:** QUIVER_API_KEY or web scraping

### 2. 13F Filings (Hedge Fund Holdings)
- Quarterly disclosure of positions by managers with $100M+ AUM
- When short interest increases + hedge fund ownership decreases → bearish
- Significant forecasting power for out-of-sample returns
- **Need:** SEC EDGAR API + parsing (free but complex)

### 3. Dark Pool Activity
- Large institutional trades executed away from public exchanges
- High dark pool volume in a stock can signal accumulation/distribution
- Detectable after execution via FINRA ADF data
- **Need:** FINRA or premium data feed

### 4. Options Flow (Unusual Activity)
- Large options purchases (especially calls) can signal informed trading
- "Smart money" tends to use options before major moves
- **Need:** CBOE data or options analytics API

## Signals We CAN Proxy Without Premium Data
- **Short interest proxy:** High volatility + price decline + volume spike
  (already captured by our Meme Stock + Tail Risk strategies)
- **Congressional copycat:** Buy stocks held by multiple institutions
  (proxy: buy the most popular Dividend Aristocrats + mega caps)
- **13F proxy:** Follow ETF inflows/outflows (available via yfinance)

## Action Items
- [ ] When FINNHUB_API_KEY is set: add insider trading + social sentiment
- [ ] When user adds SEC EDGAR parsing: add 13F-based strategy
- [ ] Consider web scraping tradercongress.com for congressional data

Sources:
- [ScienceDirect: Short selling + 13F](https://www.sciencedirect.com/science/article/abs/pii/S0304405X16301520)
- [Unusual Whales Institutions](https://unusualwhales.com/institutions)
- [TraderCongress](https://tradercongress.com/)

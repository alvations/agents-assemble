# Alternative Data Sources for Trading Signals

Research date: 2026-04-08. All sources verified for programmatic access.

---

## 1. Satellite & Geospatial Data

### NASA VIIRS Nighttime Lights (FREE)
- **What**: Satellite imagery of nighttime light intensity. Proxy for economic activity, urbanization, industrial output.
- **API/Access**: NASA Earthdata (https://www.earthdata.nasa.gov/topics/human-dimensions/nighttime-lights). Free Earthdata login required. Black Marble product from LAADS DAAC.
- **Also**: Earth Observation Group at Colorado School of Mines (https://eogdata.mines.edu/products/vnl/) — CC BY 4.0 license.
- **Rate limits**: No API rate limits; bulk download.
- **Signal**: Regional economic growth/decline. Compare YoY light intensity for countries/regions to predict emerging market ETFs.
- **Sectors**: Emerging markets (EEM, VWO, FXI), infrastructure, real estate.
- **Verdict**: FREE, high-value for macro signals, but requires image processing (not trivial to automate for daily trading).

### OpenSky Network — Flight Tracking (FREE)
- **What**: Real-time ADS-B flight data. Track global air traffic volume as economic activity indicator.
- **API**: `https://opensky-network.org/api/states/all` (anonymous: 400 credits/day, 10s resolution). Also `/flights/all`, `/flights/arrival`, `/flights/departure`.
- **Rate limits**: Anonymous: 400 API credits/day, 10s resolution. Registered: 4000 credits/day, 5s resolution.
- **Signal**: Airport departure/arrival counts = air travel demand. Correlates with airline revenue, business travel, tourism.
- **Sectors**: Airlines (DAL, UAL, LUV, AAL), travel (BKNG, EXPE, ABNB), aerospace (BA, RTX).
- **Verdict**: FREE, immediately usable. Count flights at major hub airports weekly.

### AIS Ship Tracking (FREE/FREEMIUM)
- **AISHub** (https://www.aishub.net): Free AIS data exchange. Requires contributing your own AIS data.
- **aisstream.io** (https://aisstream.io): Free real-time WebSocket API for ship tracking.
- **Signal**: Global shipping volume = trade flow indicator. Track container ships at major ports.
- **Sectors**: Shipping (ZIM, SBLK, DAC), global trade ETFs, commodities.
- **Verdict**: aisstream.io is FREE and real-time. Good for shipping/commodity plays.

---

## 2. Web Traffic & Search Data

### Google Trends via pytrends (FREE)
- **What**: Search interest over time for any keyword. Demand/awareness proxy.
- **Library**: `pip install pytrends` (unofficial). Also `pytrends-modern` for better rate limiting.
- **Rate limits**: ~1 request/2 seconds before throttling. Add `time.sleep(2)` between calls. Max ~1400 requests before hard rate limit.
- **Signal**: Rising search interest in a brand/product = demand growth. Declining interest = revenue warning.
- **Sectors**: Consumer (retail, restaurants), tech (app adoption), pharma (drug awareness).
- **Example**: "iPhone 16" search spike before AAPL earnings. "Ozempic" searches correlated with LLY/NVO stock.
- **Verdict**: FREE, immediately usable. IMPLEMENTED in data_fetcher.py.

### SimilarWeb (PAID, limited free)
- **What**: Website traffic data as revenue proxy.
- **API**: Paid plans only (https://developers.similarweb.com). Chrome extension gives limited free data.
- **Verdict**: NOT FEASIBLE for programmatic free use.

---

## 3. Social & Sentiment Data

### Reddit/WSB Sentiment — ApeWisdom (FREE)
- **What**: Stock mention counts and sentiment from r/wallstreetbets, r/stocks, r/investing, r/CryptoCurrency.
- **API**: `https://apewisdom.io/api/v1.0/filter/{filter}/page/{page}`. Filters: `all-stocks`, `all-crypto`, `wallstreetbets`, `stocks`, etc.
- **Rate limits**: Not documented, but public API. 100 results per page.
- **Response**: `{rank, ticker, name, mentions, upvotes, rank_24h_ago, mentions_24h_ago}`
- **Signal**: Spike in mentions = retail attention. Contrarian: fade extreme hype. Momentum: ride early mentions.
- **Sectors**: Meme stocks, crypto-adjacent, small/mid caps with retail following.
- **Verdict**: FREE, no key needed. IMPLEMENTED in data_fetcher.py.

### Reddit/WSB — Tradestie (FREE)
- **What**: Top 50 stocks discussed on r/wallstreetbets with sentiment.
- **API**: `https://tradestie.com/api/v1/apps/reddit`
- **Response**: `{no_of_comments, sentiment, sentiment_score, ticker}`
- **Verdict**: FREE, no key needed. Simple endpoint.

### Glassdoor / Indeed Job Postings (SCRAPING REQUIRED)
- **What**: Company hiring velocity as growth proxy.
- **Access**: JobSpy library (https://github.com/speedyapply/JobSpy) scrapes LinkedIn, Indeed, Glassdoor. Indeed has no rate limits; LinkedIn rate limits at ~10 pages.
- **Signal**: Rapid hiring = growth phase. Hiring freeze/layoffs = contraction.
- **Verdict**: Free via scraping, but fragile. NOT implemented (anti-bot risk).

---

## 4. Government & Public Data (ALL FREE)

### TSA Checkpoint Passenger Data (FREE)
- **What**: Daily count of travelers screened at TSA checkpoints. Updated Mon-Fri by 9am.
- **URL**: `https://www.tsa.gov/travel/passenger-volumes` (HTML table, scrapeable with pandas.read_html).
- **Signal**: Air travel recovery/growth indicator. Compare to prior year same day.
- **Sectors**: Airlines (DAL, UAL, LUV, AAL, JBLU), airports, hotels (MAR, HLT, H), travel platforms (BKNG, EXPE).
- **Verdict**: FREE, no key needed. IMPLEMENTED in data_fetcher.py.

### NOAA Climate Data (FREE)
- **What**: Historical weather, temperature, precipitation, storm data.
- **API**: `https://www.ncei.noaa.gov/cdo-web/api/v2/{endpoint}`. Token required (free: https://www.ncdc.noaa.gov/cdo-web/token).
- **Rate limits**: 5 requests/second, 10,000 requests/day.
- **Signal**: Extreme weather = energy demand spikes, crop damage, insurance claims. Mild winters = lower nat gas demand.
- **Sectors**: Energy (XLE, UNG, USO), agriculture (DBA, WEAT, ADM, CF, MOS), insurance, utilities.
- **Verdict**: FREE with registration. IMPLEMENTED in data_fetcher.py.

### USDA Quick Stats — Agriculture Data (FREE)
- **What**: Crop production, acreage, livestock, prices for all US agriculture.
- **API**: `https://quickstats.nass.usda.gov/api/` (free key required: https://quickstats.nass.usda.gov/api/).
- **Rate limits**: 50,000 records per query.
- **Signal**: Crop report surprises move corn, soy, wheat futures. Livestock data impacts protein stocks.
- **Sectors**: Agriculture commodities (WEAT, CORN, SOYB), ag companies (ADM, CF, MOS, NTR, DE).
- **Verdict**: FREE, key required. Not implemented yet (requires USDA key signup).

### BLS Employment Data (FREE)
- **What**: Employment by sector, unemployment rate, wages, CPI.
- **API**: `https://api.bls.gov/publicAPI/v2/timeseries/data/` (v1 no key, v2 free key for higher limits).
- **Rate limits**: v1: 25 queries/day, 10 years, 25 series. v2: 500 queries/day, 20 years, 50 series.
- **Signal**: Sector employment trends = sector rotation signal. Rising wages = inflation pressure.
- **Sectors**: Sector ETFs (XLF, XLK, XLE, etc.), broad market (SPY), bonds (TLT).
- **Verdict**: FREE, no key for basic use. Not implemented yet.

### Census Construction Spending (FREE)
- **What**: Monthly value of construction (residential, commercial, public).
- **API**: `https://api.census.gov/data/` (free, no key needed for some endpoints).
- **Signal**: Construction spending trends = real estate and infrastructure demand.
- **Sectors**: Homebuilders (DHI, LEN, PHM), REITs (VNQ, O), materials (MLM, VMC).
- **Verdict**: FREE. Not implemented yet.

### EPA Environmental Data (FREE)
- **What**: Air quality, emissions, pollution permits.
- **API**: Envirofacts API (https://www.epa.gov/enviro/envirofacts-data-service-api). AQS API for air quality.
- **Signal**: Industrial pollution permits = expansion/contraction of manufacturing.
- **Verdict**: FREE but niche. Not implemented.

### FCC Spectrum Auctions (FREE)
- **What**: Spectrum auction results and wireless licenses.
- **Data**: https://www.fcc.gov/auctions-summary, https://auctiondata.fcc.gov/
- **Signal**: Spectrum spending = telecom capex commitment. High bids = competitive market.
- **Sectors**: Telecom (T, VZ, TMUS), tower REITs (AMT, CCI).
- **Verdict**: FREE but infrequent (auctions happen periodically). Not implemented.

---

## 5. Crypto & DeFi On-Chain Data

### DeFi Llama (FREE, no key)
- **What**: Total Value Locked (TVL) across 7000+ DeFi protocols on 500+ chains.
- **API**: `https://api.llama.fi/protocols` (all protocols), `/protocol/{slug}` (historical), `/tvl/{protocol}` (current), `/v2/chains` (all chains), `/v2/historicalChainTvl` (historical by chain).
- **Rate limits**: None documented for free tier. Reasonable usage expected.
- **Signal**: TVL growth = DeFi adoption, risk appetite. TVL decline = capital flight.
- **Sectors**: Crypto (COIN, MARA, RIOT, MSTR), DeFi tokens, blockchain infrastructure.
- **Verdict**: FREE, no key, excellent data. IMPLEMENTED in data_fetcher.py.

### Glassnode (FREE TIER)
- **What**: Bitcoin/Ethereum on-chain metrics (800+ metrics).
- **API**: `https://api.glassnode.com/v1/metrics/{category}/{metric}`. Free tier = Tier 1 metrics at daily resolution.
- **Free metrics**: Active addresses, transaction count, exchange flows, SOPR, NVT ratio.
- **Signal**: Exchange inflows = sell pressure. HODLer accumulation = bullish. NVT ratio = valuation.
- **Sectors**: Bitcoin (MSTR, MARA, RIOT), crypto ETFs, COIN.
- **Verdict**: FREE TIER available (registration required). Not implemented yet (needs API key).

### Etherscan (FREE TIER)
- **What**: Ethereum blockchain transactions, gas prices, token transfers.
- **API**: `https://api.etherscan.io/api`. Free: 5 calls/second, 100K calls/day.
- **Signal**: Gas price spikes = network congestion = high DeFi activity. Transaction volume trends.
- **Sectors**: Ethereum ecosystem, DeFi tokens, COIN.
- **Verdict**: FREE TIER (key required). Not implemented yet.

---

## 6. Retail & Consumer Proxy Data

### Steam Player Counts (FREE, no key)
- **What**: Current player counts for any Steam game.
- **API**: `https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={app_id}` (no key needed).
- **Key App IDs**: 730 (CS2), 570 (Dota 2), 440 (TF2), 252490 (Rust), 271590 (GTA V), 1245620 (Elden Ring), 1172470 (Apex Legends), 578080 (PUBG).
- **Signal**: Player engagement trends = gaming company health. New game launches spike player counts.
- **Sectors**: Gaming (EA, TTWO, RBLX), Valve (private), gaming ETFs, GPU demand (NVDA, AMD).
- **Verdict**: FREE, no key needed. IMPLEMENTED in data_fetcher.py.

### Box Office Data (FREE)
- **What**: Daily/weekly/monthly domestic and worldwide box office grosses.
- **Library**: `pip install boxoffice-api` (scrapes Box Office Mojo).
- **Also**: OMDb API (https://www.omdbapi.com/) — 1000 requests/day free with key.
- **Signal**: Box office performance = studio revenue. Weekend #1 = positive catalyst for parent company.
- **Sectors**: Entertainment (DIS, WBD, PARA, CMCSA/NBCU, NFLX, AMC).
- **Verdict**: FREE via scraping library. Not fully implemented (library may be fragile).

### Amazon Best Sellers (SCRAPING)
- **What**: Hourly updated bestseller rankings across product categories.
- **Signal**: Product demand velocity, brand momentum.
- **Verdict**: Requires scraping infrastructure. NOT implemented.

### Twitch Viewership (FREE API)
- **What**: Live stream viewer counts by game/streamer.
- **API**: Official Twitch API (https://dev.twitch.tv/docs/api/) — OAuth2 required, but free.
- **Signal**: Gaming engagement trends, esports popularity.
- **Sectors**: Gaming/streaming (AMZN/Twitch), game publishers.
- **Verdict**: FREE with OAuth registration. Not implemented yet.

---

## Implementation Summary

| Source | Free? | Key Required? | Implemented? | Signal Quality |
|--------|-------|---------------|-------------|----------------|
| Google Trends (pytrends) | YES | No | YES | High |
| TSA Checkpoint | YES | No | YES | High |
| NOAA Weather | YES | Yes (free) | YES | Medium |
| Steam Player Counts | YES | No | YES | Medium |
| DeFi Llama TVL | YES | No | YES | High (crypto) |
| Reddit/WSB (ApeWisdom) | YES | No | YES | Medium |
| OpenSky Flights | YES | No | Partial | Medium |
| BLS Employment | YES | No/Free key | No | High |
| USDA Agriculture | YES | Free key | No | High (commodities) |
| Glassnode On-Chain | Free tier | Yes | No | High (crypto) |
| Etherscan | Free tier | Yes | No | Medium (crypto) |
| Census Construction | YES | No | No | Medium |
| VIIRS Nighttime Lights | YES | Free login | No | High (macro, complex) |
| AIS Ship Tracking | YES | No | No | Medium |
| SimilarWeb | No | Paid | No | High (if paid) |
| Job Postings | Scraping | No | No | High (fragile) |

---

## Recommended Priority for Implementation

1. **Google Trends** (done) — Highest signal-to-effort ratio
2. **TSA Checkpoint** (done) — Clean leading indicator for travel sector
3. **DeFi Llama** (done) — Best free crypto alternative data
4. **Reddit Sentiment** (done) — Retail attention tracker
5. **Steam Players** (done) — Gaming sector proxy
6. **NOAA Weather** (done) — Agriculture/energy weather signals
7. **BLS Employment** (next) — Sector rotation signals
8. **USDA Agriculture** (next) — Commodity trading signals
9. **OpenSky Flights** (next) — International travel/trade flows
10. **Glassnode** (needs key) — On-chain crypto signals

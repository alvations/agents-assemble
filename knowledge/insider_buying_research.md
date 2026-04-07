# Insider Buying Research (2024-2025)

## Performance Data
- Harvard study: stocks with significant insider buying outperform by +6% annually over 3 years
- Cluster buys (multiple insiders buying within short timeframe) are strongest signal
- Transactions after >10% price appreciation: 6.3% cumulative abnormal return
- Distance from 52-week high is #1 predictor (36% of feature importance)

## Implementability in Our Framework
- CANNOT access live SEC Form 4 data for backtesting (need premium API)
- CAN proxy using 52-week high distance (already in our universe via scan_52_week_lows)
- Our Burry + Icahn contrarian strategies already partially capture this signal
- Small cap deep value strategy also captures oversold + volume spike (insider cluster proxy)

## API Keys Needed for Full Implementation
- SEC EDGAR (free but rate-limited): bulk Form 4 filings
- Finnhub (FINNHUB_API_KEY): insider transactions endpoint
- OpenInsider.com: free web scraping possible but fragile

## Proxy Strategy (no API needed)
Combine: price near 52-week low + above SMA200 + volume spike
This captures similar dynamics to insider cluster buying.
Our existing tail_risk_harvest + michael_burry strategies are closest.

Sources:
- [Harvard insider buying study](https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2014/04/9919.pdf)
- [ArXiv: Insider Purchase Signals in Microcap](https://arxiv.org/html/2602.06198)
- [ScienceDirect: Insider filings as trading signals](https://www.sciencedirect.com/science/article/pii/S1544612324015435)

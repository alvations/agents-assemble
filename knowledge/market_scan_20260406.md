# Market Scan: April 2026 — Tickers for Backtesting

## 1. Best Performing ETFs YTD 2026

Energy dominates on Iran/Hormuz crisis (Brent $60 -> $118). Broad market down (VOO -4.4%).

| ETF | Theme | YTD Return |
|-----|-------|-----------|
| BWET | Tanker Shipping | +411% |
| XOP | Oil & Gas E&P | +44.6% |
| XES | Oil & Gas Equipment | +42.3% |
| XLE | Energy Select | +37.9% |
| VXX | Volatility (VIX futures) | +34.9% |
| WGMI | Bitcoin Mining | +33.4% |
| DRNZ | Drones | +33.1% |
| MEME | Meme Stocks | +31.9% |
| BKCH | Blockchain | +29.8% |
| EWY | South Korea (memory chips) | +26.5% |
| ITA | Aerospace & Defense | +9.8% |
| GLD | Gold | +5.8% |
| EWJ | Japan | +5.1% |

**Backtest tickers:** BWET, XOP, XES, XLE, VXX, WGMI, DRNZ, MEME, BKCH, EWY, ITA, GLD, EWJ, VOO, VTI

## 2. New Academic Anomalies (2025-2026)

- **Crowding factor**: Most-crowded stocks deliver +0.54% monthly alpha; least-crowded -0.90%. Crowding = new predictive signal.
- **Sentiment-conditioned factors**: Momentum/low-vol win after high sentiment + low VIX. Quality wins after low sentiment + high VIX.
- **Anomaly decay**: Most of the "factor zoo" (100+ anomalies) have disappeared in the modern era. Momentum, low-risk, and quality survive.
- **Hedge fund factor model**: 9-factor model with 5 anomaly-based factors outperforms existing models.

**Backtest tickers (factor ETFs):** MTUM (momentum), QUAL (quality), USMV (low vol), VLUE (value), SIZE (small cap), SPY (benchmark)

## 3. Most Shorted Stocks — Squeeze Candidates

Top 20 by short interest % of float (as of March 2026):

| Ticker | Short % | Sector |
|--------|---------|--------|
| HTZ | 48.35% | Transportation |
| GRPN | 46.31% | Retail |
| BETR | 46.27% | Financial |
| HIMS | 41.09% | Healthcare |
| AI | 37.19% | Software |
| IOVA | 36.69% | Biotech |
| SOUN | 34.02% | AI/IT Services |
| LCID | 33.81% | EV/Autos |
| RXRX | 33.24% | Biotech |
| BYND | 31.76% | Food |
| ENVX | 31.66% | Energy Storage |
| NVAX | 31.41% | Biotech |
| MARA | 30.70% | Crypto Mining |
| SPHR | 29.63% | Entertainment |
| BBAI | 28.24% | AI/IT Services |
| SERV | 28.00% | Robotics |
| VKTX | 27.01% | Biotech (GLP-1) |
| PLUG | 24.05% | Renewable Energy |
| KSS | 23.88% | Department Stores |
| RUN | 24.83% | Solar |

**Backtest tickers:** HTZ, GRPN, HIMS, AI, SOUN, LCID, RXRX, BYND, ENVX, NVAX, MARA, SPHR, BBAI, VKTX, PLUG, KSS, RUN

## 4. Commodity Supercycle Plays

**Copper** — Linchpin of energy transition + AI data centers. Up ~40% in 2025 (best since 2009). Tight supply deepening.
- Tickers: COPX (copper miners ETF), FCX (Freeport-McMoRan), SCCO (Southern Copper), TECK (Teck Resources)

**Gold** — Re-monetization thesis. Central bank accumulation. Geopolitical safe haven.
- Tickers: GLD (gold ETF), GDX (gold miners), NEM (Newmont), GOLD (Barrick), AEM (Agnico Eagle)

**Uranium** — Goldman projects 2B lb cumulative deficit over 20 years. Nuclear renaissance + AI power demand.
- Tickers: URA (uranium ETF), URNM (uranium miners ETF), CCJ (Cameco), UUUU (Energy Fuels), DNN (Denison)

**Lithium** — Oversupplied near-term but green transition demand long-term. Prices well below 2022 peak.
- Tickers: LIT (lithium ETF), ALB (Albemarle), SQM (Sociedad Quimica), LTHM/LAC (Lithium Americas)

**Oil** — Iran crisis driving prices. Tanker/services plays outperforming.
- Tickers: XLE, XOP, XES, BWET, OXY (Occidental), DVN (Devon Energy), HAL (Halliburton)

**Silver** — Retail traders' top pick for 2026. Industrial + monetary demand.
- Tickers: SLV (silver ETF), PAAS (Pan American Silver), WPM (Wheaton Precious Metals)

## All Unique Tickers (yfinance-ready)

```python
ETF_WINNERS = ["BWET", "XOP", "XES", "XLE", "VXX", "WGMI", "DRNZ", "MEME", "BKCH", "EWY", "ITA", "GLD", "EWJ"]
FACTOR_ETFS = ["MTUM", "QUAL", "USMV", "VLUE", "SIZE", "SPY"]
SHORT_SQUEEZE = ["HTZ", "GRPN", "HIMS", "AI", "SOUN", "LCID", "RXRX", "BYND", "ENVX", "NVAX", "MARA", "SPHR", "BBAI", "VKTX", "PLUG", "KSS", "RUN"]
COPPER = ["COPX", "FCX", "SCCO", "TECK"]
GOLD = ["GLD", "GDX", "NEM", "GOLD", "AEM"]
URANIUM = ["URA", "URNM", "CCJ", "UUUU", "DNN"]
LITHIUM = ["LIT", "ALB", "SQM", "LAC"]
OIL = ["XLE", "XOP", "XES", "BWET", "OXY", "DVN", "HAL"]
SILVER = ["SLV", "PAAS", "WPM"]
```

## Sources

- [Best-Performing ETFs to Start 2026 — Yahoo Finance](https://finance.yahoo.com/news/best-performing-etfs-start-2026-140000302.html)
- [Best Performing ETFs of 2026 — ETF.com](https://www.etf.com/sections/features/best-performing-etfs-2026)
- [Stock Market Anomalies in the Modern Era — ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S154461232501904X)
- [Crowded Spaces and Anomalies — ScienceDirect](https://www.sciencedirect.com/science/article/pii/S0378426625001992)
- [Anomalies as New Hedge Fund Factors — JFQA](https://jfqa.org/2025/01/25/anomalies-as-new-hedge-fund-factors/)
- [16 Short Squeeze Candidates — Schaeffer's Research](https://www.schaeffersresearch.com/content/analysis/2026/02/26/16-stocks-that-are-short-squeeze-candidates)
- [Most Shorted Stocks — HighShortInterest.com](https://www.highshortinterest.com/)
- [Commodity Supercycle 2026 — Guild Investment](https://guildinvestment.substack.com/p/2026-commodities-outlook-when-the)
- [Uranium Outlook 2026 — Sprott ETFs](https://sprottetfs.com/insights/uranium-outlook-2026/)
- [Copper Outlook 2026 — Mining.com](https://www.mining.com/coppers-tight-supply-and-tariff-risks-set-for-a-volatile-2026/)
- [Commodity Supercycle — AInvest](https://www.ainvest.com/news/commodity-supercycle-copper-lithium-aluminum-buys-gold-2026-2512/)

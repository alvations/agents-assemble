# agents-assemble

Trading agents and algorithms for publicly tradable instruments. **253 strategies**, 720+ tickers, ranked by Composite Score across 28 rolling windows (2015-2025).

**Platforms:** Robinhood, Public.com, Tiger Brokers, IBKR, eToro, IG

> **Start here:**
> - **[LEADERBOARD.md](LEADERBOARD.md)** — Rankings by Composite Score (253 strategies, components collapsed)
> - **[strategy/winning/](strategy/winning/)** — Trade recommendations for winning strategies (entry, stop-loss, take-profit)
> - **[strategy/losing/](strategy/losing/)** — Strategies that failed (don't repeat these)
> - **[TRIGGERS.md](TRIGGERS.md)** — Plain-English guide to all trading signals and when to act
> - **[TRADING.md](TRADING.md)** — How to execute trades via Public.com API
> - **[knowledge/](knowledge/)** — 70+ research files with backtested findings
>
> **Pre-Market Research: [Weekly Roundup Apr 18](knowledge/premarket-research/20260418_weekly.md) — Hormuz reopened, oil -19%, S&P 7,126 ATH, Nasdaq 13-day streak, banks sweep earnings

## Top 5 Strategies (by Composite Score, 6 windows 2022-2025)

| Rank | Strategy | Composite | 3Y Return | 3Y Sharpe | Consistency | Type |
|------|----------|-----------|-----------|-----------|-------------|------|
| 1 | **Core Satellite** | **0.75** | 255.4% | 0.87 | 83% | Core index + satellite alpha positions |
| 2 | **Uranium Renaissance** | **0.60** | 353.1% | 1.27 | 83% | Structural uranium supply deficit (UUUU, CCJ, LEU) |
| 3 | **Momentum** | **0.57** | 218.6% | 1.58 | 83% | Classic momentum factor |
| 4 | **AI Mega Ecosystem** | **0.57** | 247.3% | 1.54 | 83% | 41-ticker AI combined (6 sub-strategies collapsed) |
| 5 | **Concentrate Winners** | **0.51** | 177.6% | 1.28 | 83% | Top-conviction holdings only, no diversification drag |

See **[LEADERBOARD.md](LEADERBOARD.md)** for all 253 strategies with full rankings and formula details.

## Quick Start

```bash
pip install -e .

# Launch web GUI
python app.py
# Open http://localhost:8888

# Run all 253 strategies on 4-year horizon
python run_multi_horizon.py --horizon 3y

# Run single strategy
python run_multi_horizon.py --persona ai_token_economy

# Run all 253 strategies in a category
python run_multi_horizon.py --category unconventional
```

## StockPick — AI Strategy Matcher (Core Feature)

Pick any stocks. We match them to our best backtested strategy, show vol-adjusted position sizing, suggest additional tickers, and get Claude AI's opinion.

**GUI:** Open `http://localhost:8888` → click **StockPick** tab

**Python API:**
```python
from stock_picker import analyze_stock_picks

result = analyze_stock_picks(
    ["NVDA", "AAPL", "TSLA"],
    portfolio_amount=100_000,
    horizon="3y",
    top_n=5,
    include_claude=True,
)

for rec in result["recommendations"]:
    strat = rec["matched_strategy"]
    bt = rec["backtest"]["metrics"]
    positions = rec["positions"]
    print(rec["hypothesis"])
    print(rec["claude_analysis"])
```

**How it works:**
1. Enter tickers (any stock — if not in our universe, we fetch and cache it)
2. System matches against 253 backtested strategies by universe overlap
3. Runs fresh backtest on the matched strategy
4. Generates vol-adjusted positions: high-vol stocks get wider stops + smaller size
5. If your picks are weak, size = 0% with an explanation note
6. Claude AI reviews the whole thing
7. **Re-roll:** GUI shows 253 strategies in a carousel with shuffle

## Strategy Orchestrator — Regime-Adaptive Meta-Strategy

```python
from strategy_orchestrator import get_orchestrated_strategy

# Auto-detects bull/bear/rotation/crisis/K-shape regime
strategy = get_orchestrated_strategy("conservative_regime")
# 70% regime-adaptive + 30% permanent defense (GLD/SHY/SCHD)
# Result: +70.0% return, 1.17 Sharpe, -16.7% max DD
```

Detects regime weekly from: SPY trend, VIX level, dollar stores vs luxury (K-shape), energy vs tech divergence, bond trend. Activates appropriate sub-strategies per regime.

## 253 Strategies Across 14 Categories

| Category | Count | Top Performer |
|----------|-------|---------------|
| Unconventional | 52 | AI Token Economy (0.81 composite), Warflation Hedge, Waste Monopoly |
| Themes | 51 | AI Infra Picks & Shovels (0.57), Anthropic Ecosystem, Infrastructure Reshoring |
| Portfolio | 26 | Core-Satellite (0.61), Drawdown Severity Rotation, Covered Call Income |
| Famous Investors | 20 | David Tepper, Prince Alwaleed, Stanley Druckenmiller |
| Research | 16 | Gross Profitability Value (0.64 HODL), Cross-Asset Carry, Low Vol Quality |
| Crisis/Commodity | 12 | Product Tanker Shipping, Crisis Rotation, Commodity Supercycle |
| Williams/Seasonal | 12 | Energy Seasonal, Short Seller Dip Buy, Triple Witching |
| News/Event | 11 | FOMC Announcement, Crisis Alpha, IPO Lockup Expiry |
| Generic | 10 | Momentum, Concentrate Winners, Value |
| Recession | 10 | Recession Detector, K-Shape Economy, V-Shape Recovery |
| Political | 9 | Nancy Pelosi, Election Cycle Rotation, Polymarket Signal |
| Math | 9 | Kelly Optimal, Z-Score Reversion, Mean-Variance Optimal |
| Hedge Fund | 8 | Managed Futures Proxy, Growth Concentration, Stat Arb |
| Orchestrator | 2 | Conservative Regime (1.17 Sharpe) |

### Inverse Correlation Strategies (regime-activated)

| Strategy | Trigger | What It Does |
|----------|---------|-------------|
| Oil Down → Tech Up | XLE breaks SMA200 | Rotate to tech (AAPL, MSFT, CRM) |
| Job Loss → Tech Boom | MAN/RHI/ADP break SMA200 | Long automation (CRM, NOW, NVDA) |
| Wealth Barometer | DLTR/DG break SMA200 | Long Costco + luxury (K-shape) |
| Bonds Down → Banks Up | TLT breaks SMA200 | Long banks + insurance |
| VIX Spike → Buyback | VXX > 1.3x SMA200 | Buy cash-rich companies at fear prices |
| Mag7 Domino Hedge | Supply chain canaries break | Rotate to defensives (XLP, GLD, TLT) |

## Universe: 720+ Tickers

- **US:** mega/mid/small/micro cap, Dividend Aristocrats, Dividend Kings
- **China:** 65+ ADRs (BABA, JD, PDD, NIO, CPNG, etc.)
- **Europe:** 40+ ADRs (UK, Germany, France, Nordic, Spain, Italy)
- **Japan:** 15+ ADRs (TM, SONY, MUFG, Makita, trading houses)
- **Korea:** 8+ ADRs (Samsung, SK Telecom, Kookmin, Shinhan, POSCO, Coupang, Hyundai)
- **India:** 8+ ADRs + ETFs (INFY, IBN, HDB, INDA, EPI)
- **Singapore (SGX):** 50+ stocks (DBS, UOB, OCBC, CapitaLand REITs, SingTel, Haw Par)
- **LatAm:** 30+ (Brazil, Mexico, Argentina, Chile, Colombia)
- **Sectors:** AI infrastructure, cybersecurity, gaming, nuclear/uranium, cannabis, EVs, shipping
- **Commodities:** gold, silver, copper, uranium, lithium, rare earth, agriculture
- **Alternative:** Billboard monopolies, specialty insurance, midstream pipelines, muni bonds
- **Dynamic:** StockPick automatically adds any new ticker to cache on first use

## Data Sources (25+)

| Source | Type | API Key Required |
|--------|------|-----------------|
| yfinance | OHLCV, fundamentals | None |
| Yahoo Finance RSS | News headlines | None |
| Google News RSS | Aggregated news | None |
| SEC EDGAR | 8-K filings, insider trades | None |
| Reddit (WSB, stocks) | Sentiment, trending | None |
| StockTwits | Crowd sentiment | None |
| Google Trends | Search interest | None |
| Steam | Gaming player counts | None |
| DeFi Llama | Crypto TVL | None |
| OpenSky | Flight tracking | None |
| FRED | Macro data, rates | Free: `FRED_API_KEY` |
| Finnhub | Social sentiment, insiders | Free: `FINNHUB_API_KEY` (60/min) |
| Alpha Vantage | Real-time quotes | Free: `ALPHA_VANTAGE_KEY` (5/min) |
| NOAA | Weather data | Free: `NOAA_TOKEN` |

## Project Structure

```
agents-assemble/
  # Core engine
  app.py                        # Web GUI at localhost:8888
  backtester.py                 # Event-driven backtester
  data_fetcher.py               # Market data + 25 alternative sources
  stock_picker.py               # StockPick: AI strategy matcher
  strategy_orchestrator.py      # Regime detection + strategy activation
  trade_recommender.py          # Vol-adjusted trade recommendations
  run_multi_horizon.py          # Multi-horizon backtest runner

  # Strategy files (13 modules, 253 strategies)
  personas.py, famous_investors.py, theme_strategies.py, ...

  # Scripts & tools
  scripts/                      # Backtest runners, leaderboard rebuild, verification
  tools/                        # Experimental: catalyst analyzer, signal forge, etc.

  # Tests
  tests/                        # pytest suite

  # Data (do not reorganize)
  LEADERBOARD.md                # Strategy rankings (253, components collapsed)
  knowledge/                    # 70+ research files
  results/                      # Backtest JSON results + MW snapshots
  strategy/winning/             # Trade recs for winning strategies
  strategy/losing/              # Failed strategies (don't repeat)
```

## Key Findings

- **AI compute demand (NVDA momentum) is the strongest signal** — +248% in 4 years
- **Inverse correlations beat direct plays** — job loss → tech boom, oil crash → tech rotation
- **Regime orchestration improves Sharpe** — conservative orchestrator has 1.17 Sharpe
- **Boring monopolies compound quietly** — insurance float, toll booths, railroads
- **Supply chain risk is real** — NVIDIA's $110B financing book echoes Cisco 2000
- **Always backtest** — 72+ of 253 strategies lost money despite sounding good
- See `knowledge/` for detailed findings

## Tax Note (K-1 Warning)

Some commodity ETFs (USO, UNG, DBA) and MLPs (EPD, ET) issue K-1 forms instead of 1099-DIV.
See `knowledge/tax_k1_warning.md` for safe alternatives.

---

**Disclaimer:** Not financial advice. All content is AI-generated and may contain errors. Past performance does not predict future results. See [full disclaimer](knowledge/DISCLAIMER.md).

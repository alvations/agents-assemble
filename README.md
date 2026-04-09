# agents-assemble

Trading agents and algorithms for publicly tradable instruments. **173 strategies** (113 winning, 98 losing), 720+ tickers, backtested on 4Y horizon (2022-2025).

**Platforms:** Robinhood, Public.com, Tiger Brokers, IBKR, eToro, IG

> **Start here:**
> - **[LEADERBOARD.md](LEADERBOARD.md)** — Full rankings with Return + Sharpe + Max DD
> - **[strategy/winning/](strategy/winning/)** — Trade recommendations for winning strategies (entry, stop-loss, take-profit)
> - **[strategy/losing/](strategy/losing/)** — Strategies that failed (don't repeat these)
> - **[TRIGGERS.md](TRIGGERS.md)** — Plain-English guide to all trading signals and when to act
> - **[TRADING.md](TRADING.md)** — How to execute trades via Public.com API
> - **[knowledge/](knowledge/)** — 54 research files with backtested findings

## Top 5 Strategies (4Y: 2022-2025)

| Rank | Strategy | 4Y Return | Sharpe | Max DD | Type |
|------|----------|-----------|--------|--------|------|
| 1 | **AI Token Economy** | **248.4%** | **1.12** | -28.7% | NVDA compute demand proxy → AI infra stack |
| 2 | **Uranium Renaissance** | **156.9%** | **0.67** | -51.4% | Structural uranium supply deficit (UUUU, CCJ, LEU) |
| 3 | **Midstream Toll Road** | **112.5%** | **0.86** | -19.9% | Pipeline fee-based income (EPD, ET, MPLX) |
| 4 | **David Tepper** | **108.2%** | **0.82** | -16.2% | Appaloosa macro + high-conviction growth |
| 5 | **UK European Banking** | **103.1%** | **0.83** | -23.6% | NatWest, HSBC, UBS value recovery |

**Regime Orchestrator:** Conservative version: +70.0%, 1.17 Sharpe, -16.7% DD — auto-switches between bull/bear/rotation/crisis/K-shape.

See **[LEADERBOARD.md](LEADERBOARD.md)** for all 173 strategies with full rankings.

## Quick Start

```bash
pip install -e .

# Launch web GUI
python app.py
# Open http://localhost:8888

# Run all strategies on 4-year horizon
python run_multi_horizon.py --horizon 3y

# Run single strategy
python run_multi_horizon.py --persona ai_token_economy

# Run all strategies in a category
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
2. System matches against 173 backtested strategies by universe overlap
3. Runs fresh backtest on the matched strategy
4. Generates vol-adjusted positions: high-vol stocks get wider stops + smaller size
5. If your picks are weak, size = 0% with an explanation note
6. Claude AI reviews the whole thing
7. **Re-roll:** GUI shows 5 strategies in a carousel with shuffle

## Strategy Orchestrator — Regime-Adaptive Meta-Strategy

```python
from strategy_orchestrator import get_orchestrated_strategy

# Auto-detects bull/bear/rotation/crisis/K-shape regime
strategy = get_orchestrated_strategy("conservative_regime")
# 70% regime-adaptive + 30% permanent defense (GLD/SHY/SCHD)
# Result: +70.0% return, 1.17 Sharpe, -16.7% max DD
```

Detects regime weekly from: SPY trend, VIX level, dollar stores vs luxury (K-shape), energy vs tech divergence, bond trend. Activates appropriate sub-strategies per regime.

## 173 Strategies Across 15 Categories

| Category | Count | Top Performer (4Y) |
|----------|-------|---------------------|
| Unconventional | 39 | AI Token Economy (+248%), Midstream Toll Road (+112%) |
| Themes | 37 | Uranium Renaissance (+157%), Subscription Monopoly (+81%) |
| Famous Investors | 20 | David Tepper (+108%), Druckenmiller (+97%) |
| Recession | 10 | K-Shape Economy, V-Shape Recovery, L-Shape Stagnation |
| Generic | 10 | Momentum (+85%), Concentrate Winners (+78%) |
| Portfolio | 9 | Barbell, Core-Satellite, Dividend Aristocrat Blue Chips |
| Crisis/Commodity | 9 | Product Tanker Shipping (+93%), Shipping Freight Cycle |
| Math | 8 | Cointegration Pairs, Entropy Regime, Optimal Stopping |
| Williams/Seasonal | 8 | Energy Seasonal, Short Seller Dip Buy (+65%) |
| Hedge Fund | 7 | Growth Concentration (+45%), Stat Arb Medallion |
| News/Event | 7 | FDA Catalyst, Earnings Whisper, Merger Arbitrage |
| Political | 7 | Nancy Pelosi, GOP Trading, Polymarket Signal |
| Orchestrator | 2 | Conservative Regime (+70%, 1.17 Sharpe) |

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
- **Japan:** 15+ ADRs (TM, SONY, MUFG, Makita, sogo shoshas)
- **Korea:** Chaebols (Samsung, SK Telecom, Kookmin, Shinhan, POSCO)
- **India:** ADRs + ETFs (INFY, IBN, HDB, INDA, EPI)
- **Singapore (SGX):** 50+ stocks (DBS, UOB, OCBC, CapitaLand REITs, SingTel, Haw Par)
- **LatAm:** 30+ (Brazil, Mexico, Argentina, Chile, Colombia)
- **Sectors:** AI infrastructure, cybersecurity, gaming, nuclear/uranium, cannabis, EVs, shipping
- **Commodities:** gold, silver, copper, uranium, lithium, rare earth, agriculture
- **Alternative:** Billboard monopolies, specialty insurance, midstream pipelines, muni bonds
- **Dynamic:** StockPick automatically adds any new ticker to cache on first use

## Data Sources (25+)

| Source | Type | API Key |
|--------|------|---------|
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
| FRED | Macro data, rates | Free key |
| Finnhub | Social sentiment, insiders | Free key |
| Alpha Vantage | Real-time quotes | Free key |

## Project Structure

```
agents-assemble/
  agents_assemble/              # Python package (pip install -e .)
    data/fetcher.py             # Market data + 25 alternative data sources
    engine/backtester.py        # Event-driven backtester + predictions + black swan sim
    engine/judge.py             # Strategy grading and ranking
    engine/recommender.py       # Trade recommendations with vol-adjusted sizing
    strategies/                 # All strategy implementations (13 modules)

  strategy_orchestrator.py      # Meta-strategy: regime detection + strategy activation
  stock_picker.py               # StockPick: AI strategy matcher (core GUI feature)
  app.py                        # Web GUI at localhost:8888
  run_multi_horizon.py          # Multi-horizon backtest runner
  sync_package.py               # Sync flat files → package after evolution

  LEADERBOARD.md                # Definitive strategy rankings (173 strategies)
  TRADING.md                    # Public.com API execution guide
  knowledge/                    # 54 research files (NVDA supply chain, alt data, etc.)
  results/                      # Backtest JSON results
  strategy/winning/             # Trade recs for winning strategies
  strategy/losing/              # Failed strategies (don't repeat)
```

## Key Findings

- **AI compute demand (NVDA momentum) is the strongest signal** — +248% in 4 years
- **Inverse correlations beat direct plays** — job loss → tech boom, oil crash → tech rotation
- **Regime orchestration improves Sharpe** — conservative orchestrator has 1.17 Sharpe
- **Boring monopolies compound quietly** — insurance float, toll booths, railroads
- **Supply chain risk is real** — NVIDIA's $110B financing book echoes Cisco 2000
- **Always backtest** — 72 of 173 strategies lost money despite sounding good
- See `knowledge/` for detailed findings

## API Keys (optional, set as env vars)

| Key | Source | Free Tier |
|-----|--------|-----------|
| `FRED_API_KEY` | FRED macro data | Unlimited |
| `FINNHUB_API_KEY` | Social sentiment, insider trades | 60 calls/min |
| `ALPHA_VANTAGE_KEY` | Real-time quotes | 5 calls/min |
| `NOAA_TOKEN` | Weather data | Free registration |

## Tax Note (K-1 Warning)

Some commodity ETFs (USO, UNG, DBA) and MLPs (EPD, ET) issue K-1 forms instead of 1099-DIV.
See `knowledge/tax_k1_warning.md` for safe alternatives.

---

**Disclaimer:** This is not financial advice. Past performance does not predict future results. Trade at your own risk. See [LEADERBOARD.md](LEADERBOARD.md) for full disclaimer.

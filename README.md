# agents-assemble

Trading agents and algorithms for publicly tradable instruments. **183 strategies**, 720+ tickers, ranked by Composite Score across 12 rolling windows (2020-2025).

**Platforms:** Robinhood, Public.com, Tiger Brokers, IBKR, eToro, IG

> **Start here:**
> - **[LEADERBOARD.md](LEADERBOARD.md)** — Rankings by Composite Score (Avg Return × Consistency × Drawdown Protection)
> - **[strategy/winning/](strategy/winning/)** — Trade recommendations for winning strategies (entry, stop-loss, take-profit)
> - **[strategy/losing/](strategy/losing/)** — Strategies that failed (don't repeat these)
> - **[TRIGGERS.md](TRIGGERS.md)** — Plain-English guide to all trading signals and when to act
> - **[TRADING.md](TRADING.md)** — How to execute trades via Public.com API
> - **[knowledge/](knowledge/)** — 54+ research files with backtested findings
>
> **Pre-Market Research (2026-04-10):** [knowledge/premarket-research/20260410.md](knowledge/premarket-research/20260410.md) — CPI release day, tariff escalation, market selloff

## Top 5 Strategies (by Composite Score, 2020-2025)

| Rank | Strategy | Composite | Consistency | Avg Return | Type |
|------|----------|-----------|-------------|------------|------|
| 1 | **AI Token Economy** | **1.10** | 92% | +156% avg | NVDA compute demand proxy → AI infra stack |
| 2 | **Uranium Renaissance** | **0.74** | 92% | +134% avg | Structural uranium supply deficit (UUUU, CCJ, LEU) |
| 3 | **Concentrate Winners** | **0.62** | 92% | +89% avg | Top 3-5 stocks outperform equal-weight |
| 4 | **AI Revolution** | **0.53** | 92% | +79% avg | Broad AI theme (NVDA, AVGO, CRM, SNOW) |
| 5 | **David Tepper** | **0.52** | 100% | +65% avg | Appaloosa macro — positive Sharpe in ALL 12 windows |

See **[LEADERBOARD.md](LEADERBOARD.md)** for all 183 strategies with full rankings and formula details.

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

## 175 Strategies Across 13 Categories

| Category | Count | Top Performer |
|----------|-------|---------------|
| Unconventional | 41 | AI Token Economy (1.10 composite), Warflation Hedge, Defense Budget Floor |
| Themes | 37 | Uranium Renaissance (0.74 composite), Subscription Monopoly |
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

## Tax Note (K-1 Warning)

Some commodity ETFs (USO, UNG, DBA) and MLPs (EPD, ET) issue K-1 forms instead of 1099-DIV.
See `knowledge/tax_k1_warning.md` for safe alternatives.

---

**Disclaimer:** This is not financial advice. Past performance does not predict future results. Trade at your own risk. See [full disclaimer](knowledge/DISCLAIMER.md).

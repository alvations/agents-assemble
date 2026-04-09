# AI Token Growth Signals — How to Track Compute Demand

## Direct Proxies (what we use in ai_token_economy strategy)
- **NVDA revenue growth** = most direct proxy for industry-wide AI compute spend
- **SMCI server shipments** = physical AI server deployment rate
- **VRT (Vertiv) orders** = data center cooling demand = new capacity being built
- **EQIX/DLR leasing** = data center space absorption rate

## How to Get AI Token Growth Data

### Free / Public Sources
1. **Quarterly earnings calls** — NVDA, MSFT (Azure AI), GOOGL (Cloud AI), AMZN (Bedrock)
   report AI revenue/growth directly. Parse from SEC 10-Q filings.
2. **Similarweb traffic to api.openai.com, claude.ai** — web traffic as usage proxy
3. **GitHub Copilot adoption** — MSFT reports subscriber numbers quarterly
4. **Hugging Face model downloads** — public API, tracks open-source AI adoption
5. **MLPerf benchmark submissions** — indicates which companies are scaling inference
6. **Electricity consumption data** — EIA reports power usage by data center regions
   (Northern Virginia, Oregon, Iowa = major data center hubs)
7. **Google Trends** for "ChatGPT", "Claude", "AI API" — consumer awareness proxy

### Paid / Alternative Data
- **SemiAnalysis** ($1K/yr) — detailed GPU shipment tracking, hyperscaler capex
- **New Street Research** — semiconductor supply chain intelligence
- **TrendForce** — DRAM/NAND pricing (HBM demand for AI = price premium)
- **Dell'Oro Group** — data center capex forecasting

### Our Strategy's Approach
We use NVDA as the "token spend index" — when NVDA is in a strong uptrend
(SMA50 > SMA200, MACD positive), it means AI compute demand is accelerating.
This signal boosts allocation to the entire AI infrastructure stack.

Result: **+216.6% return, 1.43 Sharpe** on 3Y backtest (2022-2024).
This captured the AI infrastructure buildout from ChatGPT launch through 2024.

## Future Enhancement
- Add quarterly NVDA revenue growth rate as a signal multiplier
- Track HBM (High Bandwidth Memory) pricing via MU earnings
- Monitor power utility contracts in data center regions
- Cross-reference with cloud provider capex guidance

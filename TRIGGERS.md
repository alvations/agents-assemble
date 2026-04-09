# Trading Triggers Guide

This page explains the signals used by our **WAIT FOR SIGNAL** and **signal-enhanced** strategies. If a strategy says "WAIT FOR SIGNAL" or "Even better: add more when...", refer to this guide for what to watch.

## What Are These Signals?

Our strategies monitor market conditions automatically. Some strategies work best when specific conditions are met. Think of these like traffic lights:

- **Green light** = conditions are met, strategy is active
- **Red light** = conditions not met, strategy sits in cash (or holds small position)

You don't need to calculate anything yourself — the backtester handles this. But knowing the signals helps you understand WHY a strategy is buying or selling.

---

## Inverse Correlation Triggers

These strategies profit when one sector's pain becomes another's gain.

### Oil Crash → Tech Boom
**What to watch:** Energy stocks (ExxonMobil, Chevron) dropping significantly  
**Why it works:** When oil crashes, tech companies get lower costs (data centers, shipping). Money also rotates from energy funds to growth funds.  
**Strategies:** `oil_down_tech_up`  
**How to check:** Look at XLE (Energy ETF) — is it in a sustained decline?

<details>
<summary>Technical details (for advanced users)</summary>

- **Entry signal:** XLE and XOP both below their 200-day simple moving average (SMA200)
- **Exit signal:** XLE recovers above SMA200
- **Indicators used:** SMA50, SMA200, RSI14, MACD
- **Target stocks:** AAPL, MSFT, GOOGL, AMZN, META, CRM, NOW
- **Position sizing:** Score-weighted by trend strength. Max 12% per position.
</details>

### Job Losses → Automation Boom
**What to watch:** Staffing companies (ManpowerGroup, Robert Half, ADP) declining  
**Why it works:** When companies cut staff, they invest in software/AI to replace workers. Salesforce, ServiceNow, and AI companies benefit.  
**Strategies:** `job_loss_tech_boom`  
**How to check:** Are staffing company stocks dropping while tech/SaaS stocks are rising?

<details>
<summary>Technical details (for advanced users)</summary>

- **Entry signal:** 2+ of MAN, RHI, ASGN, ADP below their SMA200
- **Exit signal:** Staffing stocks recover above SMA200
- **Indicators used:** SMA50, SMA200, RSI14, MACD, MACD Signal
- **Target stocks:** CRM, NOW, WDAY, INTU, ADBE, PANW, NVDA, PATH
- **Position sizing:** Score-weighted. Concentrated in strongest momentum names.
</details>

### Dollar Stores Struggling → Luxury Winning (K-Shape Economy)
**What to watch:** Dollar Tree, Dollar General stocks declining while Costco stays strong  
**Why it works:** When lower-income consumers struggle, it signals a "K-shaped" economy where wealthy consumers are fine. Premium brands outperform.  
**Strategies:** `k_shape_economy`, `wealth_barometer`  
**How to check:** Compare Dollar Tree stock vs Costco stock. If Dollar Tree is falling and Costco isn't, K-shape is active.

<details>
<summary>Technical details (for advanced users)</summary>

- **Entry signal:** DLTR or DG below SMA200 AND COST above SMA200
- **Exit signal:** Dollar stores recover OR luxury breaks down
- **Indicators used:** SMA50, SMA200, RSI14
- **Target stocks:** COST, LVMUY, AAPL, AMZN, UNH, BX, LULU, RH
- **Position sizing:** Score-weighted by trend. Max 12% per position.
</details>

### Rising Interest Rates → Banks Profit
**What to watch:** Bond prices falling (TLT declining)  
**Why it works:** When interest rates rise, banks earn more on loans (wider "net interest margin"). Insurance companies also earn more on their investment float.  
**Strategies:** `bonds_down_banks_up`, `yield_curve_inversion`  
**How to check:** Are bond ETFs (TLT, AGG) declining? That means rates are rising → good for banks.

<details>
<summary>Technical details (for advanced users)</summary>

- **Entry signal:** TLT below SMA200 (rates rising)
- **Exit signal:** TLT recovers above SMA200 (rates falling)
- **Target stocks:** JPM, BAC, WFC, C, GS, PGR, ALL, CB, MET, SCHW, MS
- **Position sizing:** Score-weighted by SMA50/200 trend + RSI.
</details>

### Weak Dollar → Emerging Markets Rise
**What to watch:** US Dollar Index declining  
**Why it works:** When the dollar weakens, emerging market currencies strengthen, making their exports cheaper and their debt easier to service.  
**Strategies:** `dollar_weak_em_strong`  
**How to check:** Is UUP (Dollar ETF) declining? That's good for international stocks.

### Market Panic → Buy Buyback Kings
**What to watch:** VIX (fear index) spiking above 25  
**Why it works:** Cash-rich companies like Apple and Google buy back their own stock during panics, creating a price floor. You're buying alongside them.  
**Strategies:** `vix_spike_buyback`, `crisis_alpha`  
**How to check:** Is the news talking about market fear/panic? VIX > 25 = elevated fear.

### Crypto Crash → Traditional Finance
**What to watch:** Bitcoin/crypto prices crashing hard (-20%+)  
**Why it works:** When crypto crashes, some investors move money back to traditional banks and brokerages.  
**Strategies:** `crypto_crash_tradfi`  
**How to check:** Is Coinbase (COIN) stock crashing? Are crypto headlines negative?

---

## Crash Recovery Triggers

### V-Shape Recovery
**What to watch:** Market drops 15%+ then starts bouncing back sharply  
**Why it works:** After sudden shocks (like COVID), high-risk stocks bounce hardest. Getting in early on the recovery = biggest gains.  
**Strategies:** `v_shape_recovery`  
**When to enter:** Only AFTER you see the market start recovering from a major crash. Not during the crash.

### L-Shape Stagnation (Worst Case Hedge)
**What to watch:** Market stays down for 3+ months with no recovery  
**Why it works:** This is insurance for a Japan 1990s-style prolonged downturn. Hold gold + short-term bonds + utilities.  
**Strategies:** `l_shape_stagnation`  
**When to enter:** Only when the market has been declining for months with no sign of recovery.

---

## Supply Chain Triggers

### NVIDIA Domino Effect
**What to watch:** AI supply chain companies (SMCI, AMKR, chip packagers) breaking down  
**Why it works:** NVIDIA depends on dozens of smaller suppliers. If suppliers start failing, it's an early warning that NVIDIA's growth could stall.  
**Strategies:** `nvidia_domino_hedge`, `nvidia_chain_diversified`  
**When to act:** If 2+ supply chain companies start declining sharply, reduce AI stock positions and move to defensive.

---

## Statistical Triggers

### Pairs Trading (Mean Reversion)
**What to watch:** Two historically correlated stocks diverge significantly  
**Why it works:** Stocks like Coca-Cola/Pepsi or Visa/Mastercard normally move together. When they diverge, they tend to snap back.  
**Strategies:** `cointegration_pairs`, `zscore_reversion`  
**When to enter:** When the price ratio between paired stocks reaches extreme levels (2+ standard deviations).

---

## How Position Sizes Handle Risk

For **SAFE TO BUY** strategies, you don't need to time the market. The position sizing already handles risk:

- **High volatility stocks** (like TSLA, NVDA) automatically get **smaller positions**
- **Low volatility stocks** (like PG, JNJ) automatically get **larger positions**
- **Stop losses and take profits** are set per-position based on each stock's volatility
- **Maximum allocation** caps prevent any single stock from dominating

This means you can invest in any SAFE TO BUY strategy at any time — the sizing protects you.

---

*See [LEADERBOARD.md](LEADERBOARD.md) for strategy rankings. See individual strategy files in [strategy/winning/](strategy/winning/) for specific position recommendations.*

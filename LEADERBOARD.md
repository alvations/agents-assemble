# LEADERBOARD

**253 strategies** (247 ranked + 6 components collapsed under combined strategies).

## Ranking Formula

```
Composite = Avg Return x Consistency x (1 - Avg |Max Drawdown|)
```

**Windows:** 1Y (2022-2025) + 3Y (2022-2024, 2023-2025) = 6

Return and drawdown are **horizon-weighted**: the 1Y group and 3Y group each contribute 50% to the averages, so 4 one-year windows cannot drown out 2 three-year windows.

## How to Read This

| Metric | What It Means | Good | Bad |
|--------|--------------|------|-----|
| **Return** | Total cumulative return | >50% | <0% |
| **Sharpe** | Risk-adjusted return | >1.0 | <0 |
| **Max DD** | Worst peak-to-trough drop | >-15% | <-30% |
| **Composite** | Return x consistency x safety | >0.3 | <0 |
| **Consistency** | % of 6 windows with positive Sharpe | 100% | <50% |

---

## Top 10 Strategies

### #1 [core_satellite](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/core_satellite_20260412_190248.md)

| 3Y Return | 3Y Sharpe | 3Y Max DD | Positions | Consistency | Avg Return | Composite |
|-----------|-----------|-----------|-----------|------------|------------|-----------|
| **255.4%** | **0.87** | -11.6% | 6 | 83% | 108.1% | **0.75** |

> BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

Risk: Stop loss 11.6% | Take profit 13.8% | Max allocation 16.5%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2022 | -10.0% | -0.80 | -15.6% |
| 1Y_2023 | 13.9% | 0.89 | -7.8% |
| 1Y_2024 | 141.0% | 1.19 | -9.2% |
| 1Y_2025 | 29.5% | 1.72 | -11.6% |
| 3Y_2022_2024 | 89.7% | 0.50 | -34.2% |
| 3Y_2023_2025 | 255.4% | 0.87 | -11.6% |
</details>

### #2 [uranium_renaissance](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/uranium_renaissance_20260412_190203.md)

| 3Y Return | 3Y Sharpe | 3Y Max DD | Positions | Consistency | Avg Return | Composite |
|-----------|-----------|-----------|-----------|------------|------------|-----------|
| **353.1%** | **1.27** | -37.4% | 8 | 83% | 115.3% | **0.60** |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 45.0% | Take profit 45.2% | Max allocation 11.3%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2022 | -40.9% | -1.31 | -46.6% |
| 1Y_2023 | 29.8% | 1.02 | -18.7% |
| 1Y_2024 | 75.1% | 1.37 | -21.3% |
| 1Y_2025 | 91.2% | 1.36 | -37.4% |
| 3Y_2022_2024 | 30.6% | 0.32 | -51.0% |
| 3Y_2023_2025 | 353.1% | 1.27 | -37.4% |
</details>

### #3 [momentum](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/momentum_20260412_190553.md)

| 3Y Return | 3Y Sharpe | 3Y Max DD | Positions | Consistency | Avg Return | Composite |
|-----------|-----------|-----------|-----------|------------|------------|-----------|
| **218.6%** | **1.58** | -29.5% | 5 | 83% | 93.0% | **0.57** |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 18.0% | Take profit 24.5% | Max allocation 12.5%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2022 | -28.8% | -1.63 | -30.7% |
| 1Y_2023 | 74.9% | 2.26 | -14.4% |
| 1Y_2024 | 56.0% | 1.91 | -12.4% |
| 1Y_2025 | 16.4% | 0.59 | -28.8% |
| 3Y_2022_2024 | 93.9% | 0.90 | -30.7% |
| 3Y_2023_2025 | 218.6% | 1.58 | -29.5% |
</details>

### #4 [ai_mega_ecosystem](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_mega_ecosystem_20260414_063940.md)

| 3Y Return | 3Y Sharpe | 3Y Max DD | Positions | Consistency | Avg Return | Composite |
|-----------|-----------|-----------|-----------|------------|------------|-----------|
| **247.3%** | **1.54** | -31.8% | 40 | 83% | 97.0% | **0.57** |

> BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

Risk: Stop loss 25.0% | Take profit 25.8% | Max allocation 14.6%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2022 | -33.0% | -1.24 | -39.1% |
| 1Y_2023 | 81.1% | 2.65 | -8.3% |
| 1Y_2024 | 48.4% | 1.50 | -18.1% |
| 1Y_2025 | 28.1% | 0.83 | -31.8% |
| 3Y_2022_2024 | 78.2% | 0.70 | -39.1% |
| 3Y_2023_2025 | 247.3% | 1.54 | -31.8% |
</details>

### #5 [concentrate_winners](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/concentrate_winners_20260412_190150.md)

| 3Y Return | 3Y Sharpe | 3Y Max DD | Positions | Consistency | Avg Return | Composite |
|-----------|-----------|-----------|-----------|------------|------------|-----------|
| **177.6%** | **1.28** | -29.6% | 5 | 83% | 80.8% | **0.51** |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 18.0% | Take profit 22.0% | Max allocation 10.8%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2022 | -22.6% | -1.92 | -24.3% |
| 1Y_2023 | 60.6% | 1.93 | -16.4% |
| 1Y_2024 | 55.0% | 1.63 | -17.5% |
| 1Y_2025 | 12.8% | 0.43 | -29.6% |
| 3Y_2022_2024 | 92.7% | 0.91 | -24.3% |
| 3Y_2023_2025 | 177.6% | 1.28 | -29.6% |
</details>

### #6 [yield_curve_inversion](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/yield_curve_inversion_20260412_190427.md)

| 3Y Return | 3Y Sharpe | 3Y Max DD | Positions | Consistency | Avg Return | Composite |
|-----------|-----------|-----------|-----------|------------|------------|-----------|
| **172.7%** | **0.76** | -13.5% | 7 | 83% | 71.5% | **0.49** |

> BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

Risk: Stop loss 13.5% | Take profit 9.2% | Max allocation 13.5%

Timing: SAFE TO BUY. Even better: add more when interest rates are rising — banks earn wider margins on loans.

<details>
<summary>Rolling window breakdown</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2022 | -15.4% | -1.05 | -20.9% |
| 1Y_2023 | 17.4% | 1.44 | -5.6% |
| 1Y_2024 | 97.2% | 1.04 | -6.7% |
| 1Y_2025 | 18.4% | 1.03 | -13.4% |
| 3Y_2022_2024 | 54.7% | 0.39 | -34.8% |
| 3Y_2023_2025 | 172.7% | 0.76 | -13.5% |
</details>

### #7 [recession_detector](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/recession_detector_20260412_190423.md)

| 3Y Return | 3Y Sharpe | 3Y Max DD | Positions | Consistency | Avg Return | Composite |
|-----------|-----------|-----------|-----------|------------|------------|-----------|
| **142.8%** | **0.69** | -14.1% | 5 | 83% | 69.5% | **0.49** |

> BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

Risk: Stop loss 14.3% | Take profit 7.9% | Max allocation 11.6%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2022 | -20.7% | -1.66 | -24.1% |
| 1Y_2023 | 11.3% | 0.79 | -7.2% |
| 1Y_2024 | 108.3% | 1.11 | -6.5% |
| 1Y_2025 | 5.2% | 0.16 | -14.0% |
| 3Y_2022_2024 | 83.2% | 0.49 | -24.1% |
| 3Y_2023_2025 | 142.8% | 0.69 | -14.1% |
</details>

### #8 [ipo_lockup_expiry](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ipo_lockup_expiry_20260412_190422.md)

| 3Y Return | 3Y Sharpe | 3Y Max DD | Positions | Consistency | Avg Return | Composite |
|-----------|-----------|-----------|-----------|------------|------------|-----------|
| **162.8%** | **1.18** | -22.1% | 2 | 83% | 72.1% | **0.46** |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 22.7% | Take profit 16.7% | Max allocation 9.5%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2022 | -24.1% | -1.23 | -26.6% |
| 1Y_2023 | 41.9% | 1.28 | -22.0% |
| 1Y_2024 | 70.9% | 1.98 | -12.6% |
| 1Y_2025 | 13.5% | 0.46 | -22.1% |
| 3Y_2022_2024 | 74.6% | 0.69 | -27.7% |
| 3Y_2023_2025 | 162.8% | 1.18 | -22.1% |
</details>

### #9 [david_tepper](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/david_tepper_20260412_190511.md)

| 3Y Return | 3Y Sharpe | 3Y Max DD | Positions | Consistency | Avg Return | Composite |
|-----------|-----------|-----------|-----------|------------|------------|-----------|
| **93.9%** | **1.22** | -18.4% | 6 | 100% | 54.5% | **0.45** |

> BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

Risk: Stop loss 18.4% | Take profit 12.1% | Max allocation 11.7%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2022 | 7.2% | 0.25 | -21.1% |
| 1Y_2023 | 16.9% | 0.82 | -12.8% |
| 1Y_2024 | 44.4% | 2.01 | -11.1% |
| 1Y_2025 | 15.6% | 0.80 | -18.3% |
| 3Y_2022_2024 | 82.0% | 0.85 | -21.1% |
| 3Y_2023_2025 | 93.9% | 1.22 | -18.4% |
</details>

### #10 [sentiment_reversal](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/sentiment_reversal_20260412_190240.md)

| 3Y Return | 3Y Sharpe | 3Y Max DD | Positions | Consistency | Avg Return | Composite |
|-----------|-----------|-----------|-----------|------------|------------|-----------|
| **179.2%** | **1.22** | -25.8% | 15 | 83% | 72.0% | **0.44** |

> BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

Risk: Stop loss 25.0% | Take profit 13.9% | Max allocation 12.1%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2022 | -36.7% | -1.01 | -38.8% |
| 1Y_2023 | 45.8% | 2.55 | -6.4% |
| 1Y_2024 | 84.6% | 1.66 | -7.7% |
| 1Y_2025 | 3.8% | 0.12 | -25.8% |
| 3Y_2022_2024 | 59.9% | 0.50 | -41.4% |
| 3Y_2023_2025 | 179.2% | 1.22 | -25.8% |
</details>

---

## Full Rankings (247 Ranked + 6 Components)

| # | Strategy | 3Y Ret | 3Y Sharpe | 3Y DD | Pos | Consistency | Avg Ret | Composite |
|---|----------|--------|-----------|-------|-----|------------|---------|-----------|
| 1 | [**core_satellite**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/core_satellite_20260412_190248.md) | 255.4% | 0.87 | -11.6% | 6 | 83% | 108.1% | **0.75** |
| 2 | [**uranium_renaissance**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/uranium_renaissance_20260412_190203.md) | 353.1% | 1.27 | -37.4% | 8 | 83% | 115.3% | **0.6** |
| 3 | [**momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/momentum_20260412_190553.md) | 218.6% | 1.58 | -29.5% | 5 | 83% | 93.0% | **0.57** |
| 4 | [**ai_mega_ecosystem**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_mega_ecosystem_20260414_063940.md) **[combined]** | 247.3% | 1.54 | -31.8% | 40 | 83% | 97.0% | **0.57** |
| ↳ | [ai_token_economy](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_token_economy_20260412_190218.md) | 342.5% | 1.65 | -28.5% | 9 | 83% | 164.8% | **1.05** |
| ↳ | [ai_infra_picks_shovels](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_infra_picks_shovels_20260413_190736.md) | 329.1% | 1.56 | -38.9% | 18 | 83% | 129.2% | **0.72** |
| ↳ | [anthropic_ecosystem](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/anthropic_ecosystem_20260413_190600.md) | 302.3% | 1.78 | -31.7% | 16 | 83% | 115.7% | **0.68** |
| ↳ | [openai_ecosystem](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/openai_ecosystem_20260413_190648.md) | 246.1% | 1.55 | -31.7% | 17 | 83% | 99.5% | **0.59** |
| ↳ | [ai_revolution](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_revolution_20260412_190016.md) | 214.6% | 1.37 | -27.0% | 8 | 83% | 96.6% | **0.59** |
| ↳ | [open_source_ai_ecosystem](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/open_source_ai_ecosystem_20260413_191458.md) | 232.6% | 1.57 | -26.8% | ? | 83% | 81.6% | 0.47 |
| 5 | [**concentrate_winners**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/concentrate_winners_20260412_190150.md) | 177.6% | 1.28 | -29.6% | 5 | 83% | 80.8% | **0.51** |
| 6 | [**yield_curve_inversion**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/yield_curve_inversion_20260412_190427.md) | 172.7% | 0.76 | -13.5% | 7 | 83% | 71.5% | **0.49** |
| 7 | [**recession_detector**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/recession_detector_20260412_190423.md) | 142.8% | 0.69 | -14.1% | 5 | 83% | 69.5% | **0.49** |
| 8 | [**ipo_lockup_expiry**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ipo_lockup_expiry_20260412_190422.md) | 162.8% | 1.18 | -22.1% | 2 | 83% | 72.1% | **0.46** |
| 9 | [**david_tepper**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/david_tepper_20260412_190511.md) | 93.9% | 1.22 | -18.4% | 6 | 100% | 54.5% | **0.45** |
| 10 | [**sentiment_reversal**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/sentiment_reversal_20260412_190240.md) | 179.2% | 1.22 | -25.8% | 15 | 83% | 72.0% | **0.44** |
| 11 | [**crisis_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/crisis_rotation_20260412_190325.md) | 140.9% | 0.84 | -13.6% | 5 | 83% | 62.1% | 0.44 |
| 12 | [**stanley_druckenmiller**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/stanley_druckenmiller_20260412_190636.md) | 161.7% | 1.62 | -21.2% | 9 | 83% | 65.8% | 0.44 |
| 13 | [**crisis_alpha**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/crisis_alpha_20260412_190401.md) | 174.9% | 0.71 | -11.5% | 4 | 83% | 65.5% | 0.43 |
| 14 | [**presidential_cycle**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/presidential_cycle_20260412_190551.md) | 111.8% | 1.02 | -9.2% | 5 | 83% | 55.2% | 0.41 |
| 15 | [**late_cycle_bubble_hedge**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/late_cycle_bubble_hedge_20260412_190130.md) | 126.0% | 1.40 | -18.3% | 8 | 83% | 59.0% | 0.41 |
| 16 | [**mag7_domino_hedge**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/mag7_domino_hedge_20260412_190123.md) | 177.2% | 1.57 | -23.2% | 16 | 83% | 66.0% | 0.41 |
| 17 | [**barbell_portfolio**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/barbell_portfolio_20260412_190245.md) | 144.8% | 1.63 | -12.1% | 7 | 83% | 59.0% | 0.41 |
| 18 | [**triple_witching_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/triple_witching_momentum_20260412_190550.md) | 141.0% | 0.68 | -8.0% | 5 | 83% | 57.8% | 0.41 |
| 19 | [**multi_factor_smart_beta**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/multi_factor_smart_beta_20260408_141543.md) | 81.6% | 1.23 | -10.9% | 12 | 100% | 46.0% | 0.41 |
| 20 | [**equal_weight_sp500**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/equal_weight_sp500_20260412_190303.md) | 124.8% | 1.72 | -14.6% | 16 | 83% | 57.2% | 0.41 |
| 21 | [**midstream_toll_road**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/midstream_toll_road_20260412_190208.md) | 76.0% | 0.99 | -16.4% | 7 | 83% | 56.7% | 0.4 |
| 22 | [**momentum_crash_hedge**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/momentum_crash_hedge_20260408_141550.md) | 122.8% | 1.20 | -20.7% | 10 | 83% | 56.9% | 0.38 |
| 23 | [**nancy_pelosi**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nancy_pelosi_20260412_190506.md) | 117.5% | 1.51 | -13.7% | 6 | 83% | 53.7% | 0.38 |
| 24 | [**vix_mean_reversion**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/vix_mean_reversion_20260412_190132.md) | 137.3% | 0.83 | -10.6% | 4 | 83% | 54.0% | 0.38 |
| 25 | [**nvidia_chain_diversified**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nvidia_chain_diversified_20260412_190231.md) | 152.2% | 1.37 | -18.9% | 3 | 83% | 55.7% | 0.37 |
| 26 | [**breadth_divergence**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/breadth_divergence_20260412_190243.md) | 113.1% | 1.17 | -14.4% | 7 | 83% | 51.6% | 0.37 |
| 27 | [**consumer_credit_stress**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/consumer_credit_stress_20260412_190428.md) | 119.6% | 0.67 | -16.7% | 7 | 67% | 64.9% | 0.37 |
| 28 | [**gop_trading**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/gop_trading_20260412_190508.md) | 102.6% | 1.30 | -11.7% | 9 | 83% | 50.2% | 0.36 |
| 29 | [**uk_european_banking**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/uk_european_banking_20260412_190110.md) | 91.3% | 1.35 | -14.5% | 5 | 100% | 42.6% | 0.36 |
| 30 | [**polymarket_signal**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/polymarket_signal_20260412_190510.md) | 112.4% | 0.73 | -11.3% | 4 | 83% | 49.7% | 0.35 |
| 31 | [**prince_alwaleed**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/prince_alwaleed_20260414_072438.md) | 98.8% | 1.49 | -12.3% | 0 | 83% | 48.3% | 0.35 |
| 32 | [**george_soros**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/george_soros_20260412_190616.md) | 111.1% | 1.40 | -13.3% | 5 | 67% | 60.7% | 0.35 |
| 33 | [**contrastive_pairs**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/contrastive_pairs_20260412_190046.md) | 125.2% | 1.25 | -25.1% | 10 | 83% | 52.0% | 0.34 |
| 34 | [**conservative_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/conservative_regime_20260412_190649.md) | 89.9% | 1.24 | -13.4% | 11 | 83% | 45.8% | 0.33 |
| 35 | [**pawn_counter_cyclical**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/pawn_counter_cyclical_20260413_194617.md) | 57.9% | 1.00 | -8.5% | 0 | 100% | 36.0% | 0.33 |
| 36 | [**fomc_announcement**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/fomc_announcement_20260412_190416.md) | 108.2% | 0.72 | -5.2% | 5 | 83% | 44.3% | 0.32 |
| 37 | [**bill_ackman**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/bill_ackman_20260412_190634.md) | 100.0% | 1.33 | -14.8% | 7 | 83% | 45.1% | 0.32 |
| 38 | [**santa_claus_rally**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/santa_claus_rally_20260412_190549.md) | 110.3% | 1.00 | -6.2% | 8 | 83% | 43.8% | 0.32 |
| 39 | [**semiconductor_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/semiconductor_value_20260412_190043.md) | 152.3% | 1.06 | -33.7% | 10 | 83% | 55.4% | 0.32 |
| 40 | [**policy_catalyst**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/policy_catalyst_20260412_190517.md) | 64.3% | 0.86 | -24.1% | 10 | 100% | 37.6% | 0.31 |
| 41 | [**robotics_autonomous**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/robotics_autonomous_20260412_190041.md) | 99.8% | 1.16 | -18.4% | 8 | 83% | 44.4% | 0.31 |
| 42 | [**nfp_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nfp_momentum_20260412_190418.md) | 100.2% | 0.68 | -7.9% | 4 | 83% | 42.6% | 0.31 |
| 43 | [**magic_formula**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/magic_formula_20260412_190302.md) | 83.1% | 1.10 | -11.9% | 14 | 83% | 40.8% | 0.3 |
| 44 | [**short_seller_dip_buy**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/short_seller_dip_buy_20260412_190547.md) | 75.7% | 1.06 | -11.4% | 1 | 83% | 39.9% | 0.3 |
| 45 | [**blackrock_2026**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/blackrock_2026_20260412_190639.md) | 97.8% | 1.20 | -11.8% | 8 | 83% | 41.5% | 0.3 |
| 46 | [**ai_infrastructure_layer**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_infrastructure_layer_20260412_190125.md) | 106.8% | 1.04 | -22.7% | 11 | 67% | 53.9% | 0.29 |
| 47 | [**bipartisan_consensus**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/bipartisan_consensus_20260412_190509.md) | 75.9% | 1.15 | -11.8% | 9 | 83% | 39.0% | 0.29 |
| 48 | [**specialty_insurance**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/specialty_insurance_20260412_190201.md) | 57.9% | 0.65 | -18.3% | 3 | 100% | 34.0% | 0.29 |
| 49 | [**masayoshi_son**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/masayoshi_son_20260412_190625.md) | 164.2% | 1.04 | -28.7% | 4 | 83% | 53.0% | 0.29 |
| 50 | [**singapore_alpha**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/singapore_alpha_20260412_190108.md) | 50.7% | 0.80 | -10.6% | 9 | 100% | 32.4% | 0.29 |
| 51 | [**dogs_of_dow**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dogs_of_dow_20260412_190135.md) | 100.1% | 1.17 | -14.7% | 10 | 83% | 41.5% | 0.28 |
| 52 | [**infrastructure_reshoring**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/infrastructure_reshoring_20260414_072409.md) | 84.9% | 0.96 | -22.5% | 0 | 83% | 42.4% | 0.28 |
| 53 | [**defense_budget_floor**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defense_budget_floor_20260412_190235.md) | 64.2% | 1.05 | -11.5% | 8 | 100% | 30.6% | 0.27 |
| 54 | [**unemployment_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/unemployment_momentum_20260412_190430.md) | 104.2% | 0.62 | -10.5% | 8 | 67% | 47.7% | 0.27 |
| 55 | [**ken_griffin**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ken_griffin_20260412_190512.md) | 126.8% | 1.38 | -16.3% | 6 | 83% | 42.5% | 0.27 |
| 56 | [**defense_aerospace**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defense_aerospace_20260412_190020.md) | 114.0% | 0.71 | -49.4% | 9 | 83% | 50.4% | 0.27 |
| 57 | [**market_making_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/market_making_momentum_20260412_190348.md) | 81.1% | 0.69 | -9.7% | 9 | 67% | 44.7% | 0.26 |
| 58 | [**product_tanker_shipping**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/product_tanker_shipping_20260412_190321.md) | 11.4% | 0.08 | -25.2% | 8 | 83% | 39.4% | 0.26 |
| 59 | [**leveraged_trend_tactical**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/leveraged_trend_tactical_20260414_072412.md) | 82.3% | 1.07 | -16.2% | 0 | 83% | 36.2% | 0.25 |
| 60 | [**jim_simons**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/jim_simons_20260412_190622.md) | 76.4% | 1.24 | -12.9% | 12 | 83% | 34.9% | 0.25 |
| 61 | [**vix_fear_buy**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/vix_fear_buy_20260414_072443.md) | 73.2% | 0.74 | -9.1% | 0 | 83% | 32.8% | 0.25 |
| 62 | [**mean_variance_optimal**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/mean_variance_optimal_20260408_141555.md) | 74.4% | 1.36 | -12.2% | 12 | 83% | 32.9% | 0.25 |
| 63 | [**kelly_optimal**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/kelly_optimal_20260412_190435.md) | 80.7% | 1.13 | -15.2% | 9 | 83% | 34.5% | 0.24 |
| 64 | [**crypto_ecosystem**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/crypto_ecosystem_20260412_190035.md) | 60.9% | 0.56 | -27.3% | 10 | 67% | 45.6% | 0.24 |
| 65 | [**job_loss_tech_boom**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/job_loss_tech_boom_20260412_190220.md) | 87.4% | 0.89 | -33.0% | 8 | 67% | 46.8% | 0.24 |
| 66 | [**reshoring_industrial**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/reshoring_industrial_20260412_190051.md) | 64.2% | 0.81 | -20.8% | 11 | 83% | 33.7% | 0.24 |
| 67 | [**defensive_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defensive_rotation_20260412_190425.md) | 95.2% | 0.58 | -21.0% | 6 | 50% | 55.6% | 0.23 |
| 68 | [**adaptive_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/adaptive_regime_20260412_190647.md) | 75.2% | 1.02 | -16.7% | 10 | 67% | 40.7% | 0.23 |
| 69 | [**drawdown_severity_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/drawdown_severity_rotation_20260414_073950.md) | 76.4% | 0.78 | -8.2% | ? | 83% | 31.4% | 0.23 |
| 70 | [**entropy_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/entropy_regime_20260412_190453.md) | 77.1% | 1.42 | -8.5% | 9 | 83% | 30.9% | 0.23 |
| 71 | [**growth_concentration**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/growth_concentration_20260412_190350.md) | 79.6% | 0.75 | -22.6% | 5 | 83% | 35.1% | 0.23 |
| 72 | [**humanoid_robotics_supply_chain**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/humanoid_robotics_supply_chain_20260415_220651.md) | 104.6% | 0.99 | -26.5% | 11 | 83% | 37.7% | 0.23 |
| 73 | [**dynamic_ensemble**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dynamic_ensemble_20260412_190337.md) | 67.2% | 1.10 | -10.7% | 12 | 83% | 30.7% | 0.23 |
| 74 | [**biotech_breakout**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/biotech_breakout_20260412_190023.md) | 48.1% | 0.64 | -18.3% | 12 | 100% | 26.8% | 0.23 |
| 75 | [**japan_industrial_finance**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/japan_industrial_finance_20260413_141458.md) | 77.8% | 0.93 | -17.0% | 6 | 83% | 33.5% | 0.23 |
| 76 | [**oil_down_tech_up**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/oil_down_tech_up_20260412_190221.md) | 66.9% | 0.99 | -27.2% | 3 | 67% | 39.6% | 0.22 |
| 77 | [**global_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/global_rotation_20260408_141600.md) | 84.3% | 1.20 | -18.3% | 7 | 83% | 32.9% | 0.22 |
| 78 | [**dan_loeb**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dan_loeb_20260412_190513.md) | 75.0% | 1.05 | -15.3% | 3 | 67% | 37.8% | 0.22 |
| 79 | [**latam_growth**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/latam_growth_20260412_190028.md) | 72.1% | 0.88 | -17.9% | 8 | 83% | 32.0% | 0.21 |
| 80 | [**howard_marks**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/howard_marks_20260414_072247.md) | 48.5% | 0.83 | -7.5% | 0 | 83% | 27.2% | 0.21 |
| 81 | [**pre_ipo_innovation_funds**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/pre_ipo_innovation_funds_20260415_220709.md) | 164.4% | 0.87 | -53.9% | 5 | 83% | 49.1% | 0.21 |
| 82 | [**gross_profitability_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/gross_profitability_value_20260413_194626.md) | 65.8% | 0.91 | -15.7% | 0 | 83% | 29.5% | 0.21 |
| 83 | [**buffett_hodl**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/buffett_hodl_20260412_190258.md) | 60.9% | 0.99 | -16.0% | 13 | 83% | 28.9% | 0.2 |
| 84 | [**subscription_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/subscription_monopoly_20260412_190044.md) | 59.9% | 0.78 | -20.1% | 2 | 67% | 36.0% | 0.2 |
| 85 | [**global_financial_infra**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/global_financial_infra_20260412_190049.md) | 61.3% | 1.00 | -19.7% | 12 | 83% | 28.9% | 0.2 |
| 86 | [**sell_in_may**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/sell_in_may_20260412_190131.md) | 126.1% | 0.54 | -18.6% | 2 | 50% | 51.8% | 0.2 |
| 87 | [**cathie_wood**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/cathie_wood_20260412_190638.md) | 64.0% | 0.66 | -25.6% | 5 | 67% | 35.4% | 0.19 |
| 88 | [**buffett_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/buffett_value_20260412_190551.md) | 43.4% | 1.17 | -7.6% | 2 | 83% | 23.1% | 0.18 |
| 89 | [**esg_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/esg_momentum_20260413_134755.md) | 67.8% | 1.05 | -17.3% | 8 | 83% | 25.3% | 0.18 |
| 90 | [**japanese_sogo_shosha**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/japanese_sogo_shosha_20260412_190642.md) | 49.9% | 0.70 | -15.8% | 4 | 83% | 25.2% | 0.17 |
| 91 | [**insurance_float**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/insurance_float_20260412_190158.md) | 43.0% | 0.70 | -9.5% | 7 | 83% | 23.1% | 0.17 |
| 92 | [**rideshare_mobility**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/rideshare_mobility_20260412_190115.md) | 52.3% | 0.75 | -13.2% | 4 | 83% | 24.3% | 0.17 |
| 93 | [**quality_factor**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/quality_factor_20260412_190137.md) | 53.9% | 0.92 | -12.1% | 8 | 67% | 28.0% | 0.17 |
| 94 | [**small_cap_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/small_cap_value_20260412_190032.md) | 24.2% | 0.44 | -8.3% | 12 | 100% | 17.5% | 0.16 |
| 95 | [**utility_infra_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/utility_infra_income_20260413_141457.md) | 38.2% | 0.71 | -13.3% | 8 | 83% | 22.3% | 0.16 |
| 96 | [**gold_bug**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/gold_bug_20260412_190426.md) | 105.2% | 1.20 | -17.4% | 4 | 50% | 38.8% | 0.16 |
| 97 | [**china_adr_deep_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/china_adr_deep_value_20260412_190056.md) | 29.6% | 0.43 | -12.6% | 5 | 100% | 19.2% | 0.16 |
| 98 | [**vix_spike_buyback**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/vix_spike_buyback_20260412_190225.md) | 47.9% | 1.12 | -6.8% | 4 | 83% | 20.3% | 0.16 |
| 99 | [**covered_call_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/covered_call_income_20260414_080112.md) | 44.9% | 0.85 | -14.1% | 0 | 83% | 20.6% | 0.15 |
| 100 | [**infrastructure_boom**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/infrastructure_boom_20260412_190029.md) | 37.8% | 0.57 | -12.5% | 10 | 83% | 20.5% | 0.15 |
| 101 | [**bogle_three_fund**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/bogle_three_fund_20260412_190258.md) | 55.5% | 1.09 | -12.0% | 3 | 83% | 20.5% | 0.15 |
| 102 | [**staples_hedged_growth**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/staples_hedged_growth_20260412_190245.md) | 47.6% | 1.02 | -9.9% | 13 | 83% | 19.6% | 0.14 |
| 103 | [**berkshire_holdings**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/berkshire_holdings_20260412_190641.md) | 47.5% | 0.81 | -12.6% | 10 | 83% | 20.2% | 0.14 |
| 104 | [**waste_monopoly_compounder**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/waste_monopoly_compounder_20260413_194614.md) | 45.3% | 0.71 | -13.5% | 0 | 67% | 24.2% | 0.14 |
| 105 | [**healthcare_asia_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/healthcare_asia_momentum_20260412_190332.md) | 48.2% | 0.68 | -21.2% | 12 | 67% | 25.2% | 0.14 |
| 106 | [**williams_percent_r**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/williams_percent_r_20260412_190521.md) | 35.5% | 1.14 | -4.4% | 6 | 83% | 17.2% | 0.14 |
| 107 | [**glp1_obesity**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/glp1_obesity_20260412_190039.md) | 37.6% | 0.49 | -17.7% | 8 | 67% | 24.1% | 0.14 |
| 108 | [**dividend**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dividend_20260412_190558.md) | 30.5% | 0.53 | -8.5% | 11 | 83% | 17.9% | 0.13 |
| 109 | [**dividend_growth_compounding**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dividend_growth_compounding_20260412_190300.md) | 28.0% | 0.47 | -9.7% | 13 | 83% | 17.7% | 0.13 |
| 110 | [**pairs**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/pairs_20260412_190606.md) | 35.0% | 0.90 | -8.1% | 8 | 83% | 15.7% | 0.12 |
| 111 | [**faber_sector_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/faber_sector_rotation_20260408_141604.md) | 35.3% | 0.52 | -17.1% | 3 | 83% | 16.8% | 0.12 |
| 112 | [**peter_lynch**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/peter_lynch_20260412_190614.md) | 42.0% | 0.59 | -17.1% | 4 | 67% | 20.7% | 0.12 |
| 113 | [**nvidia_supply_chain**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nvidia_supply_chain_20260412_190117.md) | 75.3% | 0.78 | -26.9% | 8 | 67% | 22.6% | 0.12 |
| 114 | [**growth**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/growth_20260412_190604.md) | 53.3% | 0.54 | -35.9% | 3 | 67% | 23.8% | 0.12 |
| 115 | [**toll_booth_economy**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/toll_booth_economy_20260412_190156.md) | 38.2% | 0.62 | -14.1% | 5 | 83% | 15.3% | 0.11 |
| 116 | [**closed_end_fund_discount**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/closed_end_fund_discount_20260413_194620.md) | 42.5% | 0.90 | -14.8% | 0 | 83% | 15.7% | 0.11 |
| 117 | [**january_barometer**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/january_barometer_20260412_190548.md) | 67.0% | 1.11 | -11.5% | 6 | 67% | 19.6% | 0.11 |
| 118 | [**quality_dividend_aristocrats**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/quality_dividend_aristocrats_20260412_190306.md) | 30.4% | 0.51 | -11.1% | 12 | 83% | 14.8% | 0.11 |
| 119 | [**income_shield**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/income_shield_20260412_190251.md) | 30.7% | 0.65 | -7.7% | 12 | 83% | 14.3% | 0.11 |
| 120 | [**dividend_aristocrat_blue_chips**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dividend_aristocrat_blue_chips_20260412_190256.md) | 24.9% | 0.36 | -11.8% | 14 | 83% | 14.7% | 0.11 |
| 121 | [**long_term_loser_rebound**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/long_term_loser_rebound_20260413_194618.md) | 35.1% | 0.51 | -18.7% | 0 | 83% | 15.2% | 0.11 |
| 122 | [**gig_economy_saas**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/gig_economy_saas_20260412_190112.md) | 55.6% | 0.59 | -22.9% | 4 | 67% | 20.7% | 0.11 |
| 123 | [**energy_seasonal**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/energy_seasonal_20260412_190522.md) | 6.7% | -0.08 | -19.6% | 5 | 67% | 19.0% | 0.1 |
| 124 | [**volatility_breakout**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/volatility_breakout_20260412_190450.md) | 35.0% | 0.37 | -4.2% | 12 | 50% | 21.8% | 0.1 |
| 125 | [**warflation_hedge**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/warflation_hedge_20260412_190233.md) | 17.1% | 0.19 | -12.1% | 10 | 67% | 17.7% | 0.1 |
| 126 | [**accruals_quality**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/accruals_quality_20260413_194628.md) | 30.4% | 0.62 | -8.2% | 0 | 83% | 13.8% | 0.1 |
| 127 | [**shipping_freight_cycle**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/shipping_freight_cycle_20260412_190320.md) | 32.7% | 0.46 | -19.4% | 8 | 67% | 18.4% | 0.1 |
| 128 | [**rare_earth_minerals**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/rare_earth_minerals_20260412_190316.md) | 65.9% | 0.78 | -15.4% | 8 | 50% | 24.1% | 0.1 |
| 129 | [**permanent_portfolio**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/permanent_portfolio_20260412_190259.md) | 46.5% | 1.22 | -7.8% | 4 | 67% | 16.9% | 0.1 |
| 130 | [**sector_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/sector_rotation_20260412_190605.md) | 15.1% | 0.13 | -15.7% | 4 | 83% | 13.9% | 0.1 |
| 131 | [**risk_parity**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/risk_parity_20260412_190344.md) | 44.7% | 0.74 | -7.9% | 8 | 67% | 16.6% | 0.1 |
| 132 | [**sector_monthly_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/sector_monthly_rotation_20260412_190531.md) | 47.6% | 0.78 | -13.0% | 3 | 67% | 17.1% | 0.1 |
| 133 | [**multi_factor_combined**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/multi_factor_combined_20260414_072429.md) | 31.7% | 0.56 | -12.0% | 0 | 83% | 13.0% | 0.09 |
| 134 | [**stat_arb_medallion**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/stat_arb_medallion_20260412_190343.md) | 17.3% | 0.34 | -3.5% | 1 | 83% | 11.3% | 0.09 |
| 135 | [**telecom_equipment_5g**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/telecom_equipment_5g_20260412_190111.md) | 50.5% | 0.64 | -15.4% | 6 | 67% | 15.9% | 0.09 |
| 136 | [**defense_prime_contractors**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defense_prime_contractors_20260413_141459.md) | 19.7% | 0.23 | -16.6% | 8 | 67% | 15.5% | 0.09 |
| 137 | [**earnings_whisper**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/earnings_whisper_20260412_190409.md) | 42.2% | 0.70 | -8.5% | 3 | 67% | 14.6% | 0.08 |
| 138 | [**dollar_cycle_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dollar_cycle_rotation_20260414_072403.md) | 17.5% | 0.25 | -9.2% | 0 | 83% | 10.9% | 0.08 |
| 139 | [**systematic_sector_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/systematic_sector_rotation_20260413_134751.md) | 26.1% | 0.36 | -17.6% | 4 | 83% | 11.7% | 0.08 |
| 140 | [**nassef_sawiris**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nassef_sawiris_20260412_190627.md) | 16.4% | 0.15 | -23.1% | 1 | 67% | 14.6% | 0.08 |
| 141 | [**wealth_barometer**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/wealth_barometer_20260412_190227.md) | 26.7% | 0.37 | -22.4% | 3 | 67% | 14.2% | 0.08 |
| 142 | [**institutional_flow**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/institutional_flow_20260412_190242.md) | 27.8% | 0.42 | -11.6% | 10 | 67% | 13.4% | 0.08 |
| 143 | [**ai_adopters_not_builders**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_adopters_not_builders_20260412_190128.md) | 47.3% | 0.91 | -13.0% | 5 | 50% | 17.6% | 0.08 |
| 144 | [**dollar_weak_em_strong**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dollar_weak_em_strong_20260412_190222.md) | 37.7% | 0.88 | -12.8% | 2 | 50% | 16.1% | 0.07 |
| 145 | [**global_pharma_pipeline**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/global_pharma_pipeline_20260412_190107.md) | 38.8% | 0.58 | -17.2% | 7 | 50% | 16.7% | 0.07 |
| 146 | [**retail_deep_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/retail_deep_value_20260412_190212.md) | 31.0% | 0.36 | -25.1% | 3 | 67% | 13.4% | 0.07 |
| 147 | [**fifty_two_week_breakout**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/fifty_two_week_breakout_20260412_190531.md) | 15.9% | 0.27 | -3.6% | 1 | 67% | 10.3% | 0.07 |
| 148 | [**buyback_yield_systematic**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/buyback_yield_systematic_20260413_194623.md) | 25.1% | 0.66 | -5.5% | 0 | 67% | 10.6% | 0.07 |
| 149 | [**ray_dalio**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ray_dalio_20260412_190615.md) | 31.0% | 0.69 | -7.9% | 5 | 67% | 10.6% | 0.06 |
| 150 | [**patent_cliff_pharma**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/patent_cliff_pharma_20260412_190207.md) | 12.4% | 0.05 | -13.8% | 1 | 67% | 10.2% | 0.06 |
| 151 | [**adaptive_ensemble**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/adaptive_ensemble_20260412_190247.md) | 31.2% | 0.48 | -13.2% | 7 | 67% | 10.7% | 0.06 |
| 152 | [**korean_chaebols**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/korean_chaebols_20260412_190114.md) | 41.1% | 0.53 | -23.2% | 7 | 50% | 15.2% | 0.06 |
| 153 | [**factor_etf_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/factor_etf_rotation_20260408_141602.md) | 41.5% | 0.67 | -14.3% | 3 | 67% | 10.9% | 0.06 |
| 154 | [**gaming_catalyst**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/gaming_catalyst_20260412_190310.md) | 24.1% | 0.29 | -23.0% | 4 | 67% | 11.0% | 0.06 |
| 155 | [**news_media_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/news_media_monopoly_20260412_190211.md) | 47.3% | 0.70 | -17.6% | 2 | 67% | 11.0% | 0.06 |
| 156 | [**small_cap_value_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/small_cap_value_rotation_20260412_190312.md) | 26.9% | 0.32 | -27.1% | 8 | 67% | 11.0% | 0.06 |
| 157 | [**picks_and_shovels_ai**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/picks_and_shovels_ai_20260412_190131.md) | 39.9% | 0.51 | -19.3% | 5 | 50% | 13.7% | 0.06 |
| 158 | [**high_yield_reit_bdc**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/high_yield_reit_bdc_20260412_190254.md) | 28.9% | 0.50 | -14.8% | 9 | 67% | 10.2% | 0.06 |
| 159 | [**bonds_down_banks_up**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/bonds_down_banks_up_20260412_190223.md) | 36.7% | 0.56 | -20.0% | 3 | 50% | 13.7% | 0.06 |
| 160 | [**risk_parity_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/risk_parity_momentum_20260408_141553.md) | 32.5% | 0.64 | -9.5% | 3 | 67% | 9.6% | 0.06 |
| 161 | [**benjamin_graham**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/benjamin_graham_20260414_073107.md) | 27.4% | 0.60 | -9.3% | 0 | 50% | 12.2% | 0.05 |
| 162 | [**dual_momentum_global**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dual_momentum_global_20260414_072404.md) | 37.3% | 0.56 | -14.3% | 0 | 67% | 9.7% | 0.05 |
| 163 | [**hidden_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/hidden_monopoly_20260412_190152.md) | 35.5% | 0.54 | -14.4% | 6 | 50% | 12.8% | 0.05 |
| 164 | [**k_shape_economy**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/k_shape_economy_20260412_190432.md) | 14.9% | 0.11 | -24.9% | 3 | 67% | 9.7% | 0.05 |
| 165 | [**global_airlines_travel**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/global_airlines_travel_20260412_190058.md) | 65.0% | 0.74 | -20.5% | 8 | 67% | 11.7% | 0.05 |
| 166 | [**v_shape_recovery**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/v_shape_recovery_20260412_190431.md) | 63.9% | 1.03 | -11.7% | 1 | 50% | 13.6% | 0.05 |
| 167 | [**carl_icahn**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/carl_icahn_20260412_190623.md) | 19.9% | 0.36 | -5.8% | 12 | 50% | 11.2% | 0.05 |
| 168 | [**ensemble**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ensemble_20260414_072231.md) | 19.1% | 0.41 | -5.9% | 0 | 67% | 7.9% | 0.05 |
| 169 | [**boring_compounder**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/boring_compounder_20260412_190159.md) | 37.6% | 0.55 | -20.0% | 3 | 50% | 12.1% | 0.05 |
| 170 | [**dual_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dual_momentum_20260408_141539.md) | 36.8% | 0.55 | -14.3% | 1 | 67% | 8.6% | 0.05 |
| 171 | [**election_cycle_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/election_cycle_rotation_20260412_190514.md) | 26.3% | 0.51 | -7.2% | 4 | 50% | 10.4% | 0.05 |
| 172 | [**emerging_market_etf_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/emerging_market_etf_value_20260412_190105.md) | 40.9% | 0.67 | -21.2% | 6 | 50% | 11.3% | 0.05 |
| 173 | [**support_resistance**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/support_resistance_20260412_190633.md) | 6.9% | -0.04 | -26.1% | 6 | 67% | 8.5% | 0.04 |
| 174 | [**equal_risk_contrib**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/equal_risk_contrib_20260412_190451.md) | 38.2% | 0.88 | -7.1% | 7 | 67% | 7.6% | 0.04 |
| 175 | [**retail_crash_ecommerce**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/retail_crash_ecommerce_20260412_190224.md) | 51.1% | 0.76 | -20.5% | 2 | 67% | 8.5% | 0.04 |
| 176 | [**billboard_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/billboard_monopoly_20260412_190200.md) | 39.0% | 0.48 | -22.3% | 4 | 50% | 10.3% | 0.04 |
| 177 | [**all_weather_passive**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/all_weather_passive_20260412_190304.md) | 28.3% | 0.55 | -10.4% | 5 | 67% | 6.7% | 0.04 |
| 178 | [**canadian_aristocrat_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/canadian_aristocrat_income_20260413_194622.md) | 29.5% | 0.53 | -13.4% | 0 | 50% | 9.1% | 0.04 |
| 179 | [**mag7_hidden_suppliers**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/mag7_hidden_suppliers_20260412_190119.md) | 49.4% | 0.57 | -32.7% | 9 | 50% | 10.0% | 0.04 |
| 180 | [**activist_distressed**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/activist_distressed_20260412_190353.md) | 8.3% | -0.06 | -20.7% | 12 | 50% | 8.0% | 0.03 |
| 181 | [**cloud_cyber_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/cloud_cyber_value_20260412_190056.md) | 46.8% | 0.47 | -29.3% | 5 | 50% | 9.7% | 0.03 |
| 182 | [**li_ka_shing**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/li_ka_shing_20260412_190626.md) | 16.9% | 0.18 | -17.1% | 5 | 50% | 7.6% | 0.03 |
| 183 | [**insider_buying_real**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/insider_buying_real_20260414_072327.md) | 19.4% | 0.28 | -4.4% | 0 | 50% | 6.7% | 0.03 |
| 184 | [**serial_acquirer**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/serial_acquirer_20260412_190206.md) | 24.4% | 0.33 | -15.7% | 5 | 33% | 10.6% | 0.03 |
| 185 | [**beaten_down_staples**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/beaten_down_staples_20260412_190157.md) | 4.1% | -0.22 | -11.5% | 6 | 50% | 6.9% | 0.03 |
| 186 | [**all_weather_modern**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/all_weather_modern_20260414_072353.md) | 16.2% | 0.36 | -2.7% | 0 | 50% | 6.4% | 0.03 |
| 187 | [**aging_population**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/aging_population_20260412_190037.md) | 24.0% | 0.32 | -13.2% | 7 | 33% | 10.1% | 0.03 |
| 188 | [**l_shape_stagnation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/l_shape_stagnation_20260412_190432.md) | 13.9% | 0.10 | -7.1% | 3 | 50% | 6.4% | 0.03 |
| 189 | [**jorge_paulo_lemann**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/jorge_paulo_lemann_20260412_190628.md) | 19.8% | 0.30 | -6.6% | 1 | 50% | 6.4% | 0.03 |
| 190 | [**economic_indicators**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/economic_indicators_20260412_190215.md) | 15.9% | 0.16 | -9.7% | 4 | 50% | 6.4% | 0.03 |
| 191 | [**quant**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/quant_20260414_072349.md) | 19.7% | 0.26 | -11.6% | 0 | 50% | 6.4% | 0.03 |
| 192 | [**earnings_gap_and_go**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/earnings_gap_and_go_20260412_190542.md) | 15.9% | 0.23 | -4.6% | 12 | 33% | 7.5% | 0.02 |
| 193 | [**news_reaction_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/news_reaction_momentum_20260412_190356.md) | 14.5% | 0.13 | -5.7% | 12 | 50% | 5.1% | 0.02 |
| 194 | [**dcf_deep_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dcf_deep_value_20260412_190155.md) | 8.0% | -0.03 | -14.5% | 10 | 50% | 5.4% | 0.02 |
| 195 | [**contrarian_fallen_angels**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/contrarian_fallen_angels_20260412_190313.md) | 13.6% | 0.09 | -19.7% | 4 | 50% | 5.3% | 0.02 |
| 196 | [**southeast_asia_growth**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/southeast_asia_growth_20260413_134756.md) | 16.1% | 0.17 | -14.8% | 4 | 50% | 4.8% | 0.02 |
| 197 | [**crypto_crash_tradfi**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/crypto_crash_tradfi_20260412_190226.md) | 12.1% | 0.02 | -14.3% | 2 | 50% | 4.8% | 0.02 |
| 198 | [**preferred_equity_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/preferred_equity_income_20260414_072431.md) | 16.0% | 0.21 | -7.9% | 0 | 50% | 4.5% | 0.02 |
| 199 | [**volatility_premium**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/volatility_premium_20260413_134754.md) | 11.6% | -0.01 | -6.7% | 3 | 33% | 6.1% | 0.02 |
| 200 | [**fallen_blue_chip_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/fallen_blue_chip_value_20260412_190214.md) | 26.3% | 0.36 | -11.4% | 2 | 50% | 4.5% | 0.02 |
| 201 | [**water_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/water_monopoly_20260412_190053.md) | 20.1% | 0.23 | -15.6% | 6 | 67% | 3.4% | 0.02 |
| 202 | [**regulated_data**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/regulated_data_20260412_190054.md) | 11.7% | 0.03 | -13.0% | 3 | 50% | 4.1% | 0.02 |
| 203 | [**cross_asset_carry**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/cross_asset_carry_20260414_080125.md) | 17.8% | 0.31 | -7.5% | 0 | 50% | 3.6% | 0.02 |
| 204 | [**geopolitical_crisis**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/geopolitical_crisis_20260412_190308.md) | 4.1% | -0.21 | -18.6% | 9 | 33% | 5.8% | 0.02 |
| 205 | [**wartime_portfolio**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/wartime_portfolio_20260412_190324.md) | 4.5% | -0.32 | -11.0% | 11 | 50% | 3.6% | 0.02 |
| 206 | [**managed_futures_proxy**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/managed_futures_proxy_20260414_072332.md) | 2.3% | -0.61 | -7.0% | 0 | 33% | 5.0% | 0.02 |
| 207 | [**china_tech_rebound**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/china_tech_rebound_20260412_190025.md) | 10.1% | 0.10 | -29.4% | 4 | 67% | 3.3% | 0.02 |
| 208 | [**ai_application_survivors**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/ai_application_survivors_20260412_190127.md) | 6.0% | -0.17 | -18.3% | 1 | 33% | 5.2% | 0.02 |
| 209 | [**treasury_safe**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/treasury_safe_20260412_190424.md) | 19.4% | 0.32 | -9.9% | 5 | 50% | 3.2% | 0.01 |
| 210 | [**credit_spread_trade**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/credit_spread_trade_20260413_134753.md) | 14.9% | 0.18 | -4.6% | 3 | 50% | 2.7% | 0.01 |
| 211 | [**bond_fixed_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/bond_fixed_income_20260412_190252.md) | 16.6% | 0.22 | -8.5% | 10 | 50% | 2.4% | 0.01 |
| 212 | [**hurst_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/hurst_regime_20260412_190443.md) | 11.1% | -0.10 | -4.2% | 1 | 33% | 3.4% | 0.01 |
| 213 | [**zscore_reversion**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/zscore_reversion_20260412_190439.md) | 10.4% | -0.09 | -4.9% | 12 | 17% | 5.1% | 0.01 |
| 214 | [**global_consumer_staples**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/global_consumer_staples_20260412_190104.md) | -2.8% | -0.39 | -16.4% | 8 | 33% | 2.7% | 0.01 |
| 215 | [**low_vol_anomaly**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/low_vol_anomaly_20260408_141547.md) | 5.4% | -0.43 | -7.0% | 5 | 17% | 4.5% | 0.01 |
| 216 | [**tail_risk_harvest**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/tail_risk_harvest_20260412_190145.md) | 11.5% | -0.01 | -11.4% | 2 | 33% | 2.3% | 0.01 |
| 217 | [**fallen_luxury**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/fallen_luxury_20260412_190204.md) | -1.1% | -0.16 | -29.6% | 3 | 33% | 2.5% | 0.01 |
| 218 | [**muni_bond_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/muni_bond_income_20260412_190205.md) | 11.5% | -0.03 | -7.2% | 6 | 33% | 2.1% | 0.01 |
| 219 | [**death_care_demographics**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/death_care_demographics_20260413_194615.md) | 10.4% | 0.04 | -18.1% | 0 | 33% | 2.0% | 0.01 |
| 220 | [**cointegration_pairs**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/cointegration_pairs_20260412_190456.md) | 8.8% | -0.26 | -5.6% | 2 | 33% | 1.1% | 0.0 |
| 221 | [**africa_frontier**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/africa_frontier_20260413_134756.md) | 10.7% | 0.01 | -20.5% | 4 | 33% | 1.2% | 0.0 |
| 222 | [**spinoff_alpha**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/spinoff_alpha_20260413_134754.md) | 8.8% | -0.08 | -10.9% | 7 | 17% | 2.0% | 0.0 |
| 223 | [**commodity_supercycle**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/commodity_supercycle_20260412_190326.md) | -4.5% | -0.47 | -21.0% | 10 | 33% | 1.1% | 0.0 |
| 224 | [**fda_catalyst**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/fda_catalyst_20260412_190405.md) | 9.6% | -0.04 | -14.6% | 8 | 33% | 1.0% | 0.0 |
| 225 | [**bond_duration_trade**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/bond_duration_trade_20260413_134753.md) | -4.1% | -0.94 | -10.0% | 4 | 0% | -5.2% | 0.0 |
| 226 | [**earnings_surprise_drift**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/earnings_surprise_drift_20260412_190401.md) | 9.7% | -0.30 | -1.5% | 12 | 0% | 4.9% | 0.0 |
| 227 | [**fixed_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/fixed_income_20260414_072237.md) | 6.0% | -0.29 | -6.2% | 0 | 0% | -1.4% | 0.0 |
| 228 | [**gap_fill_spy**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/gap_fill_spy_20260412_190522.md) | -14.0% | -1.61 | -15.7% | 1 | 0% | -8.5% | 0.0 |
| 229 | [**insider_buying_acceleration**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/insider_buying_acceleration_20260414_073120.md) | 0.2% | -1.02 | -4.4% | 0 | 0% | -0.3% | 0.0 |
| 230 | [**meme_stock**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/meme_stock_20260412_190556.md) | -20.0% | -0.49 | -33.9% | 12 | 0% | -19.0% | 0.0 |
| 231 | [**merger_arbitrage**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/merger_arbitrage_20260412_190413.md) | -6.9% | -2.07 | -6.9% | 1 | 0% | -4.0% | 0.0 |
| 232 | [**nvidia_domino_hedge**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/nvidia_domino_hedge_20260412_190229.md) | -12.7% | -0.80 | -15.9% | 5 | 0% | -9.9% | 0.0 |
| 233 | [**optimal_stopping**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/optimal_stopping_20260412_190505.md) | -6.5% | -0.69 | -14.5% | 4 | 0% | -10.6% | 0.0 |
| 234 | [**water_scarcity**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/water_scarcity_20260412_190317.md) | -8.3% | -0.76 | -14.1% | 4 | 0% | -9.6% | 0.0 |
| 235 | [**adx_trend_filter**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/adx_trend_filter_20260417_214317.md) | 0.0% | -inf | 0.0% | ? | 0% | 0.0% | 0.0 |
| 236 | [**etf_cointegration**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/etf_cointegration_20260417_214436.md) | 0.0% | -inf | 0.0% | ? | 0% | 0.0% | 0.0 |
| 237 | [**constellation_contrarian**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/constellation_contrarian_20260412_190210.md) | 0.9% | -0.13 | -25.9% | 9 | 17% | -0.6% | -0.0 |
| 238 | [**low_vol_quality**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/low_vol_quality_20260414_072331.md) | 1.3% | -1.35 | -5.7% | 0 | 17% | -0.5% | -0.0 |
| 239 | [**dividend_aristocrat_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dividend_aristocrat_momentum_20260412_190147.md) | -3.8% | -0.49 | -15.3% | 10 | 33% | -0.7% | -0.0 |
| 240 | [**michael_burry**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/michael_burry_20260412_190618.md) | 7.5% | -0.18 | -8.0% | 12 | 33% | -2.2% | -0.01 |
| 241 | [**dividend_capture**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dividend_capture_20260412_190415.md) | 3.6% | -0.24 | -13.6% | 9 | 33% | -3.2% | -0.01 |
| 242 | [**self_storage_reit**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/self_storage_reit_20260413_194619.md) | -2.7% | -0.21 | -24.6% | 0 | 17% | -9.0% | -0.01 |
| 243 | [**clean_energy**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/clean_energy_20260412_190017.md) | -3.1% | -0.13 | -43.4% | 5 | 17% | -16.2% | -0.02 |
| 244 | [**agriculture_food**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/agriculture_food_20260412_190309.md) | -32.8% | -1.42 | -34.2% | 4 | 17% | -16.9% | -0.02 |
| 245 | [**turn_of_month**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/turn_of_month_20260412_190131.md) | -11.2% | -0.99 | -20.9% | 2 | 33% | -11.0% | -0.03 |
| 246 | [**cannabis_alt_consumer**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/cannabis_alt_consumer_20260412_190213.md) | 12.1% | 0.22 | -57.4% | 2 | 67% | -9.9% | -0.03 |
| 247 | [**genomics_revolution**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/genomics_revolution_20260415_220615.md) | 1.3% | 0.08 | -44.4% | 11 | 50% | -18.0% | -0.05 |

*Updated: 2026-04-17 21:49*

---

## Disclaimer

This content is for **educational and research purposes only**. It is **not financial advice**.

- **AI-GENERATED CONTENT.** All rankings, analyses, research reports, and recommendations in this repository have been generated by large language models and automated systems. AI-generated content may contain errors, inaccuracies, hallucinated facts, incorrect dates, or fabricated statistics. Users must independently verify all information before relying on it for any purpose.
- Past performance does not guarantee future results.
- Backtests use historical data and may not reflect real-world conditions (liquidity, slippage, market impact).
- All strategies tested with simulated capital. No real money was used or is at risk.
- Consult a qualified financial advisor before making investment decisions.
- The authors and contributors accept no responsibility for financial losses from using this information.
- Securities mentioned are not buy/sell recommendations. Do your own due diligence.
- Trading involves substantial risk of loss. Only invest what you can afford to lose.

By using this information, you acknowledge that you understand and accept these risks and that AI-generated content requires independent verification.

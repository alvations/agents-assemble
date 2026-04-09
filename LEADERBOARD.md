# LEADERBOARD

**175 strategies** ranked by **Composite Score** (horizon-weighted, 2020-2025).

## Ranking Formula

```
Composite = Horizon_Avg_Return x Consistency x (1 - Horizon_Avg_Drawdown)
```

Horizon averages are computed **per horizon first** (1Y, 3Y, 5Y) then averaged equally.
This prevents short-term windows from dominating the score.

| Factor | What It Measures |
|--------|-----------------|
| **Horizon Avg Return** | Equal-weighted average of (Avg 1Y + Avg 3Y + Avg 5Y) returns |
| **Consistency** | % of ALL windows where Sharpe > 0 |
| **Drawdown Penalty** | Equal-weighted average drawdown across horizons |

## How to Read This

| Metric | What It Means | Good | Bad |
|--------|--------------|------|-----|
| **Return** | Total cumulative return | >50% | <0% |
| **Sharpe** | Risk-adjusted return | >1.0 | <0 |
| **Max DD** | Worst peak-to-trough drop | >-15% | <-30% |
| **Composite** | Overall score (return x consistency x safety) | >0.5 | <0 |
| **Consistency** | % of windows with positive Sharpe | 100% | <50% |

A high return with terrible Sharpe is gambling. A 3Y winner that loses on 5Y is a fluke.

---

## Top 10 Strategies

### #1 [ai_token_economy](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_token_economy_20260409_093426.md)

| Composite | Consistency | Avg 1Y | Avg 3Y | Avg 5Y | 3Y Sharpe | Positions |
|-----------|------------|--------|--------|--------|-----------|-----------|
| **1.53** | **92%** | 44% | 184% | 439% | 1.64 | 9 |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 25.0% | Take profit 31.8% | Max allocation 15.3%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown (12 windows)</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2020 | 33.4% | 1.0 | -24.2% |
| 1Y_2021 | 40.5% | 1.64 | -16.8% |
| 1Y_2022 | -19.6% | -1.3 | -25.3% |
| 1Y_2023 | 107.5% | 2.92 | -8.9% |
| 1Y_2024 | 93.7% | 2.01 | -20.6% |
| 1Y_2025 | 7.0% | 0.26 | -28.7% |
| 3Y_2020_2022 | 49.0% | 0.52 | -26.0% |
| 3Y_2021_2023 | 134.5% | 1.26 | -26.0% |
| 3Y_2022_2024 | 216.3% | 1.43 | -25.3% |
| 3Y_2023_2025 | 335.2% | 1.64 | -28.7% |
| 5Y_2020_2024 | 486.3% | 1.34 | -26.0% |
| 5Y_2021_2025 | 391.9% | 1.19 | -28.7% |
</details>

### #2 [uranium_renaissance](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/uranium_renaissance_20260409_093418.md)

| Composite | Consistency | Avg 1Y | Avg 3Y | Avg 5Y | 3Y Sharpe | Positions |
|-----------|------------|--------|--------|--------|-----------|-----------|
| **0.96** | **92%** | 53% | 132% | 384% | 1.25 | 8 |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 25.0% | Take profit 32.3% | Max allocation 11.3%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown (12 windows)</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2020 | 75.4% | 1.7 | -20.5% |
| 1Y_2021 | 89.4% | 1.33 | -27.4% |
| 1Y_2022 | -41.2% | -1.33 | -46.9% |
| 1Y_2023 | 28.9% | 0.99 | -18.9% |
| 1Y_2024 | 73.9% | 1.36 | -21.3% |
| 1Y_2025 | 89.8% | 1.35 | -37.4% |
| 3Y_2020_2022 | 104.7% | 0.67 | -52.3% |
| 3Y_2021_2023 | 51.4% | 0.45 | -56.4% |
| 3Y_2022_2024 | 28.1% | 0.3 | -51.4% |
| 3Y_2023_2025 | 343.6% | 1.25 | -37.4% |
| 5Y_2020_2024 | 346.4% | 0.83 | -56.4% |
| 5Y_2021_2025 | 421.0% | 0.86 | -56.4% |
</details>

### #3 [concentrate_winners](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/concentrate_winners_20260409_093412.md)

| Composite | Consistency | Avg 1Y | Avg 3Y | Avg 5Y | 3Y Sharpe | Positions |
|-----------|------------|--------|--------|--------|-----------|-----------|
| **0.83** | **92%** | 38% | 91% | 240% | 1.18 | 5 |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 25.0% | Take profit 18.3% | Max allocation 10.8%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown (12 windows)</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2020 | 116.7% | 2.09 | -27.0% |
| 1Y_2021 | 14.4% | 0.57 | -12.8% |
| 1Y_2022 | -23.1% | -1.96 | -24.7% |
| 1Y_2023 | 53.1% | 1.74 | -17.0% |
| 1Y_2024 | 55.6% | 1.66 | -18.0% |
| 1Y_2025 | 10.8% | 0.37 | -29.7% |
| 3Y_2020_2022 | 93.2% | 0.81 | -28.1% |
| 3Y_2021_2023 | 39.1% | 0.45 | -28.1% |
| 3Y_2022_2024 | 78.8% | 0.8 | -24.7% |
| 3Y_2023_2025 | 154.1% | 1.18 | -29.7% |
| 5Y_2020_2024 | 348.8% | 1.13 | -28.1% |
| 5Y_2021_2025 | 131.2% | 0.67 | -29.7% |
</details>

### #4 [david_tepper](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/david_tepper_20260409_093634.md)

| Composite | Consistency | Avg 1Y | Avg 3Y | Avg 5Y | 3Y Sharpe | Positions |
|-----------|------------|--------|--------|--------|-----------|-----------|
| **0.71** | **100%** | 25% | 73% | 168% | 1.19 | 6 |

> BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

Risk: Stop loss 22.1% | Take profit 12.1% | Max allocation 11.7%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown (12 windows)</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2020 | 54.1% | 1.6 | -23.7% |
| 1Y_2021 | 11.1% | 0.46 | -8.9% |
| 1Y_2022 | 6.7% | 0.23 | -21.2% |
| 1Y_2023 | 16.4% | 0.79 | -13.1% |
| 1Y_2024 | 43.8% | 1.98 | -11.2% |
| 1Y_2025 | 15.1% | 0.77 | -18.4% |
| 3Y_2020_2022 | 79.8% | 0.75 | -23.7% |
| 3Y_2021_2023 | 41.8% | 0.46 | -21.2% |
| 3Y_2022_2024 | 79.7% | 0.83 | -21.2% |
| 3Y_2023_2025 | 91.5% | 1.19 | -18.4% |
| 5Y_2020_2024 | 202.6% | 0.93 | -23.7% |
| 5Y_2021_2025 | 133.1% | 0.76 | -21.2% |
</details>

### #5 [ai_revolution](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_revolution_20260409_093318.md)

| Composite | Consistency | Avg 1Y | Avg 3Y | Avg 5Y | 3Y Sharpe | Positions |
|-----------|------------|--------|--------|--------|-----------|-----------|
| **0.71** | **92%** | 30% | 89% | 208% | 1.21 | 8 |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 25.0% | Take profit 19.8% | Max allocation 10.6%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown (12 windows)</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2020 | 47.1% | 1.49 | -18.0% |
| 1Y_2021 | 30.4% | 1.17 | -10.0% |
| 1Y_2022 | -28.8% | -1.81 | -34.0% |
| 1Y_2023 | 71.6% | 2.05 | -13.8% |
| 1Y_2024 | 52.0% | 1.43 | -21.9% |
| 1Y_2025 | 5.0% | 0.17 | -27.3% |
| 3Y_2020_2022 | 38.6% | 0.42 | -34.2% |
| 3Y_2021_2023 | 63.9% | 0.67 | -34.2% |
| 3Y_2022_2024 | 83.3% | 0.76 | -34.0% |
| 3Y_2023_2025 | 170.9% | 1.21 | -27.4% |
| 5Y_2020_2024 | 256.3% | 0.99 | -34.2% |
| 5Y_2021_2025 | 158.7% | 0.73 | -34.2% |
</details>

### #6 [barbell_portfolio](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/barbell_portfolio_20260409_093437.md)

| Composite | Consistency | Avg 1Y | Avg 3Y | Avg 5Y | 3Y Sharpe | Positions |
|-----------|------------|--------|--------|--------|-----------|-----------|
| **0.63** | **92%** | 25% | 76% | 165% | 1.9 | 7 |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 14.5% | Take profit 19.2% | Max allocation 17.5%

Timing: WAIT FOR SIGNAL: Only enter when price spread between paired stocks reaches extreme levels. Exit when spread normalizes.

<details>
<summary>Rolling window breakdown (12 windows)</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2020 | 26.4% | 1.32 | -10.8% |
| 1Y_2021 | 28.9% | 1.54 | -7.8% |
| 1Y_2022 | -23.7% | -1.98 | -27.6% |
| 1Y_2023 | 53.9% | 2.54 | -8.3% |
| 1Y_2024 | 42.1% | 1.98 | -11.3% |
| 1Y_2025 | 21.4% | 1.17 | -12.0% |
| 3Y_2020_2022 | 23.9% | 0.29 | -30.7% |
| 3Y_2021_2023 | 52.0% | 0.73 | -30.7% |
| 3Y_2022_2024 | 65.6% | 0.89 | -27.6% |
| 3Y_2023_2025 | 163.7% | 1.9 | -12.1% |
| 5Y_2020_2024 | 169.0% | 1.09 | -30.7% |
| 5Y_2021_2025 | 160.5% | 1.07 | -30.7% |
</details>

### #7 [conservative_regime](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/conservative_regime_20260409_093754.md)

| Composite | Consistency | Avg 1Y | Avg 3Y | Avg 5Y | 3Y Sharpe | Positions |
|-----------|------------|--------|--------|--------|-----------|-----------|
| **0.62** | **92%** | 21% | 70% | 157% | 1.65 | 11 |

> BUY — Good returns with acceptable risk. Consider deploying with moderate position sizes.

Risk: Stop loss 16.2% | Take profit 13.4% | Max allocation 16.9%

Timing: ALWAYS ACTIVE: Auto-managed. Switches between growth and defensive weekly based on market conditions. No user timing needed.

<details>
<summary>Rolling window breakdown (12 windows)</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2020 | 15.9% | 0.56 | -26.0% |
| 1Y_2021 | 32.7% | 1.86 | -5.5% |
| 1Y_2022 | -7.5% | -0.88 | -16.7% |
| 1Y_2023 | 32.5% | 2.17 | -5.2% |
| 1Y_2024 | 39.8% | 2.3 | -8.0% |
| 1Y_2025 | 10.4% | 0.55 | -13.6% |
| 3Y_2020_2022 | 42.5% | 0.53 | -26.0% |
| 3Y_2021_2023 | 64.3% | 1.07 | -17.2% |
| 3Y_2022_2024 | 70.0% | 1.17 | -16.7% |
| 3Y_2023_2025 | 103.2% | 1.65 | -13.5% |
| 5Y_2020_2024 | 161.9% | 1.04 | -26.0% |
| 5Y_2021_2025 | 152.0% | 1.21 | -17.2% |
</details>

### #8 [momentum](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/momentum_20260409_093714.md)

| Composite | Consistency | Avg 1Y | Avg 3Y | Avg 5Y | 3Y Sharpe | Positions |
|-----------|------------|--------|--------|--------|-----------|-----------|
| **0.61** | **92%** | 33% | 77% | 176% | 1.42 | 5 |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 25.0% | Take profit 20.4% | Max allocation 12.5%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown (12 windows)</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2020 | 90.7% | 2.28 | -18.9% |
| 1Y_2021 | 4.8% | 0.13 | -15.9% |
| 1Y_2022 | -29.6% | -1.68 | -31.4% |
| 1Y_2023 | 57.5% | 1.94 | -17.9% |
| 1Y_2024 | 56.9% | 1.96 | -12.6% |
| 1Y_2025 | 14.9% | 0.54 | -28.9% |
| 3Y_2020_2022 | 40.4% | 0.43 | -35.4% |
| 3Y_2021_2023 | 19.2% | 0.2 | -35.4% |
| 3Y_2022_2024 | 71.0% | 0.74 | -31.4% |
| 3Y_2023_2025 | 178.1% | 1.42 | -29.8% |
| 5Y_2020_2024 | 241.6% | 1.01 | -35.4% |
| 5Y_2021_2025 | 110.7% | 0.61 | -35.4% |
</details>

### #9 [masayoshi_son](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/masayoshi_son_20260409_093739.md)

| Composite | Consistency | Avg 1Y | Avg 3Y | Avg 5Y | 3Y Sharpe | Positions |
|-----------|------------|--------|--------|--------|-----------|-----------|
| **0.59** | **92%** | 41% | 78% | 222% | 1.06 | 4 |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 25.0% | Take profit 19.5% | Max allocation 9.7%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown (12 windows)</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2020 | 99.1% | 1.73 | -34.1% |
| 1Y_2021 | 63.6% | 1.76 | -18.1% |
| 1Y_2022 | -44.9% | -2.33 | -46.8% |
| 1Y_2023 | 50.9% | 1.26 | -28.2% |
| 1Y_2024 | 51.8% | 1.33 | -20.5% |
| 1Y_2025 | 24.6% | 0.76 | -28.7% |
| 3Y_2020_2022 | 84.8% | 0.66 | -52.1% |
| 3Y_2021_2023 | 40.2% | 0.4 | -53.8% |
| 3Y_2022_2024 | 18.2% | 0.21 | -48.8% |
| 3Y_2023_2025 | 167.5% | 1.06 | -28.7% |
| 5Y_2020_2024 | 296.3% | 0.88 | -53.8% |
| 5Y_2021_2025 | 148.4% | 0.62 | -53.8% |
</details>

### #10 [nancy_pelosi](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nancy_pelosi_20260409_093631.md)

| Composite | Consistency | Avg 1Y | Avg 3Y | Avg 5Y | 3Y Sharpe | Positions |
|-----------|------------|--------|--------|--------|-----------|-----------|
| **0.59** | **92%** | 22% | 67% | 147% | 1.52 | 6 |

> STRONG BUY — Excellent risk-adjusted returns with significant alpha. Deploy with confidence.

Risk: Stop loss 16.4% | Take profit 15.0% | Max allocation 14.7%

Timing: SAFE TO BUY. Position sizes are already risk-adjusted by volatility — higher vol stocks get smaller positions automatically.

<details>
<summary>Rolling window breakdown (12 windows)</summary>

| Window | Return | Sharpe | Max DD |
|--------|--------|--------|--------|
| 1Y_2020 | 30.1% | 1.0 | -20.7% |
| 1Y_2021 | 25.9% | 1.27 | -6.4% |
| 1Y_2022 | -16.3% | -1.43 | -20.7% |
| 1Y_2023 | 44.8% | 2.26 | -9.3% |
| 1Y_2024 | 35.4% | 1.68 | -10.2% |
| 1Y_2025 | 13.7% | 0.7 | -13.6% |
| 3Y_2020_2022 | 35.5% | 0.42 | -21.6% |
| 3Y_2021_2023 | 53.6% | 0.76 | -21.6% |
| 3Y_2022_2024 | 61.4% | 0.86 | -20.7% |
| 3Y_2023_2025 | 118.8% | 1.52 | -13.7% |
| 5Y_2020_2024 | 161.5% | 0.94 | -21.6% |
| 5Y_2021_2025 | 132.1% | 0.92 | -21.6% |
</details>

---

## Full Rankings (175 Strategies)

| # | Strategy | Composite | Consistency | Avg 1Y | Avg 3Y | Avg 5Y | 3Y Sharpe | Pos |
|---|----------|-----------|------------|--------|--------|--------|-----------|-----|
| 1 | [**ai_token_economy**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_token_economy_20260409_093426.md) | 1.53 | 92% | 44% | 184% | 439% | 1.64 | 9 |
| 2 | [**uranium_renaissance**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/uranium_renaissance_20260409_093418.md) | 0.96 | 92% | 53% | 132% | 384% | 1.25 | 8 |
| 3 | [**concentrate_winners**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/concentrate_winners_20260409_093412.md) | 0.83 | 92% | 38% | 91% | 240% | 1.18 | 5 |
| 4 | [**david_tepper**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/david_tepper_20260409_093634.md) | 0.71 | 100% | 25% | 73% | 168% | 1.19 | 6 |
| 5 | [**ai_revolution**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_revolution_20260409_093318.md) | 0.71 | 92% | 30% | 89% | 208% | 1.21 | 8 |
| 6 | [**barbell_portfolio**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/barbell_portfolio_20260409_093437.md) | 0.63 | 92% | 25% | 76% | 165% | 1.9 | 7 |
| 7 | [**conservative_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/conservative_regime_20260409_093754.md) | 0.62 | 92% | 21% | 70% | 157% | 1.65 | 11 |
| 8 | [**momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/momentum_20260409_093714.md) | 0.61 | 92% | 33% | 77% | 176% | 1.42 | 5 |
| 9 | [**masayoshi_son**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/masayoshi_son_20260409_093739.md) | 0.59 | 92% | 41% | 78% | 222% | 1.06 | 4 |
| 10 | [**nancy_pelosi**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nancy_pelosi_20260409_093631.md) | 0.59 | 92% | 22% | 67% | 147% | 1.52 | 6 |
| 11 | [**midstream_toll_road**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/midstream_toll_road_20260409_093421.md) | 0.59 | 83% | 19% | 83% | 177% | 0.98 | 7 |
| 12 | [**mag7_domino_hedge**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/mag7_domino_hedge_20260409_093353.md) | 0.54 | 92% | 31% | 69% | 161% | 1.51 | 16 |
| 13 | [**adaptive_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/adaptive_regime_20260409_093752.md) | 0.54 | 83% | 20% | 69% | 156% | 1.34 | 10 |
| 14 | [**crypto_ecosystem**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/crypto_ecosystem_20260409_093330.md) | 0.53 | 83% | 21% | 73% | 153% | 0.45 | 10 |
| 15 | [**subscription_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/subscription_monopoly_20260408_220452.md) | 0.52 | 83% | 22% | 64% | 142% | 0.75 | 10 |
| 16 | [**robotics_autonomous**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/robotics_autonomous_20260409_093333.md) | 0.52 | 92% | 24% | 59% | 127% | 1.1 | 8 |
| 17 | [**core_satellite**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/core_satellite_20260409_093439.md) | 0.51 | 92% | 20% | 55% | 120% | 1.64 | 6 |
| 18 | [**reshoring_industrial**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/reshoring_industrial_20260409_093338.md) | 0.47 | 92% | 17% | 56% | 116% | 0.77 | 11 |
| 19 | [**dan_loeb**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dan_loeb_20260409_093636.md) | 0.45 | 83% | 19% | 52% | 120% | 1.05 | 3 |
| 20 | [**stanley_druckenmiller**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/stanley_druckenmiller_20260409_093746.md) | 0.44 | 83% | 26% | 63% | 129% | 1.66 | 9 |
| 21 | [**semiconductor_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/semiconductor_value_20260408_220448.md) | 0.43 | 92% | 25% | 63% | 130% | 1.03 | 10 |
| 22 | [**bipartisan_consensus**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/bipartisan_consensus_20260409_093633.md) | 0.43 | 92% | 16% | 46% | 100% | 1.06 | 9 |
| 23 | [**kelly_optimal**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/kelly_optimal_20260409_093546.md) | 0.42 | 92% | 19% | 49% | 106% | 1.15 | 9 |
| 24 | [**adaptive_ensemble**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/adaptive_ensemble_20260409_093438.md) | 0.42 | 92% | 16% | 49% | 106% | 1.22 | 7 |
| 25 | [**job_loss_tech_boom**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/job_loss_tech_boom_20260409_093427.md) | 0.41 | 83% | 21% | 58% | 121% | 0.86 | 8 |
| 26 | [**contrastive_pairs**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/contrastive_pairs_20260408_220455.md) | 0.41 | 92% | 19% | 53% | 113% | 1.2 | 10 |
| 27 | [**uk_european_banking**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/uk_european_banking_20260409_093346.md) | 0.41 | 100% | 18% | 47% | 100% | 1.27 | 5 |
| 28 | [**specialty_insurance**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/specialty_insurance_20260409_093417.md) | 0.4 | 100% | 13% | 43% | 85% | 0.64 | 3 |
| 29 | [**ken_griffin**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ken_griffin_20260409_093635.md) | 0.39 | 92% | 23% | 46% | 111% | 1.34 | 6 |
| 30 | [**staples_hedged_growth**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/staples_hedged_growth_20260409_093437.md) | 0.39 | 92% | 16% | 47% | 90% | 1.64 | 13 |
| 31 | [**rare_earth_minerals**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/rare_earth_minerals_20260408_161751.md) | 0.39 | 75% | 26% | 51% | 108% | 0.74 | 10 |
| 32 | [**oil_down_tech_up**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/oil_down_tech_up_20260409_093428.md) | 0.37 | 83% | 15% | 48% | 96% | 0.97 | 3 |
| 33 | [**growth_concentration**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/growth_concentration_20260409_093514.md) | 0.36 | 83% | 28% | 48% | 110% | 0.76 | 5 |
| 34 | [**george_soros**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/george_soros_20260409_093733.md) | 0.36 | 75% | 20% | 49% | 110% | 1.17 | 5 |
| 35 | [**gop_trading**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/gop_trading_20260409_093632.md) | 0.35 | 92% | 14% | 44% | 90% | 1.26 | 9 |
| 36 | [**bill_ackman**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/bill_ackman_20260409_093745.md) | 0.33 | 83% | 15% | 45% | 88% | 1.28 | 7 |
| 37 | [**dynamic_ensemble**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dynamic_ensemble_20260409_093459.md) | 0.32 | 92% | 15% | 33% | 74% | 0.88 | 12 |
| 38 | [**singapore_alpha**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/singapore_alpha_20260409_093345.md) | 0.31 | 92% | 12% | 41% | 69% | 0.8 | 9 |
| 39 | [**short_seller_dip_buy**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/short_seller_dip_buy_20260409_093712.md) | 0.3 | 83% | 9% | 42% | 77% | 1.05 | 1 |
| 40 | [**warflation_hedge**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/warflation_hedge_20260409_093436.md) | 0.29 | 83% | 10% | 38% | 73% | 0.15 | 10 |
| 41 | [**energy_seasonal**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/energy_seasonal_20260409_093642.md) | 0.29 | 75% | 13% | 53% | 99% | -0.1 | 5 |
| 42 | [**biotech_breakout**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/biotech_breakout_20260409_093322.md) | 0.29 | 100% | 10% | 33% | 63% | 0.58 | 12 |
| 43 | [**jim_simons**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/jim_simons_20260409_093738.md) | 0.29 | 92% | 13% | 31% | 71% | 0.94 | 12 |
| 44 | [**defensive_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defensive_rotation_20260409_093540.md) | 0.28 | 83% | 12% | 37% | 79% | 0.68 | 6 |
| 45 | [**healthcare_asia_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/healthcare_asia_momentum_20260409_093454.md) | 0.28 | 83% | 16% | 33% | 79% | 0.6 | 12 |
| 46 | [**utility_infra_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/utility_infra_income_20260409_093343.md) | 0.27 | 92% | 11% | 31% | 65% | 0.69 | 8 |
| 47 | [**buffett_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/buffett_value_20260409_093712.md) | 0.27 | 83% | 11% | 39% | 68% | 1.51 | 2 |
| 48 | [**shipping_freight_cycle**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/shipping_freight_cycle_20260409_093449.md) | 0.26 | 83% | 11% | 33% | 71% | 0.39 | 8 |
| 49 | [**dividend**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dividend_20260409_093716.md) | 0.25 | 92% | 9% | 29% | 61% | 0.51 | 11 |
| 50 | [**yield_curve_inversion**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/yield_curve_inversion_20260409_093540.md) | 0.25 | 92% | 12% | 29% | 57% | 1.2 | 7 |
| 51 | [**cathie_wood**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/cathie_wood_20260409_093748.md) | 0.25 | 75% | 14% | 35% | 79% | 0.62 | 5 |
| 52 | [**dividend_aristocrat_blue_chips**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dividend_aristocrat_blue_chips_20260409_093441.md) | 0.24 | 92% | 10% | 28% | 59% | 0.36 | 14 |
| 53 | [**blackrock_2026**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/blackrock_2026_20260409_093749.md) | 0.24 | 92% | 12% | 29% | 58% | 1.22 | 8 |
| 54 | [**dogs_of_dow**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dogs_of_dow_20260408_155136.md) | 0.24 | 92% | 12% | 33% | 61% | 1.04 | 10 |
| 55 | [**quality_factor**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/quality_factor_20260409_093356.md) | 0.24 | 83% | 11% | 29% | 63% | 0.69 | 8 |
| 56 | [**nvidia_supply_chain**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/nvidia_supply_chain_20260408_225113.md) | 0.23 | 83% | 18% | 29% | 65% | 0.74 | 4 |
| 57 | [**pairs**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/pairs_20260409_093723.md) | 0.23 | 92% | 9% | 26% | 52% | 1.02 | 8 |
| 58 | [**infrastructure_boom**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/infrastructure_boom_20260409_093326.md) | 0.23 | 92% | 9% | 27% | 58% | 0.55 | 10 |
| 59 | [**insurance_float**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/insurance_float_20260409_093415.md) | 0.22 | 83% | 9% | 27% | 57% | 0.69 | 7 |
| 60 | [**recession_detector**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/recession_detector_20260409_093539.md) | 0.22 | 92% | 11% | 25% | 55% | 1.04 | 5 |
| 61 | [**nvidia_chain_diversified**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nvidia_chain_diversified_20260409_093435.md) | 0.22 | 67% | 19% | 40% | 75% | 1.28 | 3 |
| 62 | [**defense_budget_floor**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defense_budget_floor_20260409_093436.md) | 0.22 | 83% | 10% | 28% | 52% | 1.01 | 8 |
| 63 | [**berkshire_holdings**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/berkshire_holdings_20260409_093750.md) | 0.22 | 92% | 10% | 26% | 55% | 0.72 | 10 |
| 64 | [**japanese_sogo_shosha**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/japanese_sogo_shosha_20260409_093750.md) | 0.21 | 92% | 9% | 28% | 50% | 0.68 | 4 |
| 65 | [**sector_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/sector_rotation_20260409_093722.md) | 0.2 | 83% | 9% | 26% | 50% | -0.08 | 4 |
| 66 | [**polymarket_signal**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/polymarket_signal_20260409_093633.md) | 0.19 | 92% | 9% | 20% | 44% | 0.86 | 4 |
| 67 | [**boring_compounder**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/boring_compounder_20260408_230207.md) | 0.19 | 75% | 14% | 26% | 59% | 0.54 | 3 |
| 68 | [**defense_aerospace**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defense_aerospace_20260409_093320.md) | 0.19 | 75% | 13% | 42% | 69% | 0.7 | 9 |
| 69 | [**global_financial_infra**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/global_financial_infra_20260408_220459.md) | 0.18 | 75% | 9% | 26% | 55% | 0.96 | 10 |
| 70 | [**income_shield**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/income_shield_20260408_141844.md) | 0.18 | 92% | 7% | 21% | 44% | 0.63 | 11 |
| 71 | [**japan_industrial_finance**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/japan_industrial_finance_20260409_093343.md) | 0.18 | 75% | 10% | 29% | 52% | 0.91 | 6 |
| 72 | [**product_tanker_shipping**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/product_tanker_shipping_20260409_093450.md) | 0.17 | 75% | 8% | 44% | 43% | 0.04 | 8 |
| 73 | [**patent_cliff_pharma**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/patent_cliff_pharma_20260409_093421.md) | 0.17 | 75% | 9% | 25% | 44% | -0.01 | 1 |
| 74 | [**vix_spike_buyback**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/vix_spike_buyback_20260409_093430.md) | 0.17 | 83% | 8% | 21% | 40% | 1.14 | 4 |
| 75 | [**aging_population**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/aging_population_20260408_155019.md) | 0.16 | 67% | 10% | 26% | 54% | 0.3 | 12 |
| 76 | [**k_shape_economy**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/k_shape_economy_20260408_230922.md) | 0.16 | 83% | 8% | 20% | 47% | 0.04 | 3 |
| 77 | [**beaten_down_staples**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/beaten_down_staples_20260409_093415.md) | 0.16 | 75% | 7% | 24% | 45% | -0.24 | 6 |
| 78 | [**latam_growth**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/latam_growth_20260409_093325.md) | 0.16 | 83% | 11% | 26% | 40% | 0.78 | 8 |
| 79 | [**entropy_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/entropy_regime_20260408_161814.md) | 0.15 | 75% | 11% | 19% | 43% | 1.2 | 7 |
| 80 | [**hidden_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/hidden_monopoly_20260408_230144.md) | 0.15 | 75% | 10% | 21% | 47% | 0.52 | 6 |
| 81 | [**fallen_luxury**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/fallen_luxury_20260409_093419.md) | 0.15 | 67% | 10% | 30% | 51% | -0.19 | 3 |
| 82 | [**small_cap_value_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/small_cap_value_rotation_20260408_230441.md) | 0.14 | 67% | 16% | 22% | 53% | 0.25 | 8 |
| 83 | [**gig_economy_saas**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/gig_economy_saas_20260409_093347.md) | 0.14 | 75% | 16% | 19% | 50% | 0.55 | 4 |
| 84 | [**fifty_two_week_breakout**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/fifty_two_week_breakout_20260409_093653.md) | 0.14 | 83% | 6% | 17% | 30% | 0.22 | 1 |
| 85 | [**gold_bug**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/gold_bug_20260408_155231.md) | 0.14 | 57% | 17% | 24% | 50% | 1.13 | 4 |
| 86 | [**glp1_obesity**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/glp1_obesity_20260409_093332.md) | 0.14 | 67% | 6% | 24% | 44% | 0.44 | 8 |
| 87 | [**nassef_sawiris**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nassef_sawiris_20260409_093740.md) | 0.13 | 75% | 6% | 25% | 36% | 0.14 | 1 |
| 88 | [**telecom_equipment_5g**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/telecom_equipment_5g_20260408_223146.md) | 0.13 | 75% | 10% | 16% | 38% | 0.59 | 4 |
| 89 | [**toll_booth_economy**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/toll_booth_economy_20260409_093414.md) | 0.13 | 83% | 7% | 16% | 36% | 0.61 | 5 |
| 90 | [**mag7_hidden_suppliers**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/mag7_hidden_suppliers_20260408_225932.md) | 0.13 | 75% | 17% | 19% | 41% | 0.53 | 9 |
| 91 | [**consumer_credit_stress**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/consumer_credit_stress_20260409_093541.md) | 0.13 | 67% | 7% | 19% | 44% | 0.51 | 7 |
| 92 | [**regulated_data**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/regulated_data_20260408_225826.md) | 0.12 | 75% | 7% | 16% | 37% | 0.01 | 3 |
| 93 | [**dollar_weak_em_strong**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dollar_weak_em_strong_20260408_223948.md) | 0.12 | 57% | 11% | 20% | 41% | 0.85 | 2 |
| 94 | [**billboard_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/billboard_monopoly_20260408_220423.md) | 0.12 | 67% | 13% | 15% | 46% | 0.47 | 7 |
| 95 | [**bonds_down_banks_up**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/bonds_down_banks_up_20260408_223953.md) | 0.12 | 67% | 10% | 16% | 44% | 0.51 | 10 |
| 96 | [**global_pharma_pipeline**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/global_pharma_pipeline_20260408_222020.md) | 0.11 | 75% | 7% | 18% | 31% | 0.55 | 6 |
| 97 | [**vix_mean_reversion**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/vix_mean_reversion_20260408_155501.md) | 0.11 | 67% | 9% | 17% | 37% | 1.06 | 5 |
| 98 | [**defense_prime_contractors**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defense_prime_contractors_20260409_093343.md) | 0.11 | 67% | 7% | 21% | 36% | 0.21 | 8 |
| 99 | [**korean_chaebols**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/korean_chaebols_20260408_223153.md) | 0.1 | 75% | 9% | 18% | 30% | 0.48 | 7 |
| 100 | [**growth**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/growth_20260409_093721.md) | 0.1 | 67% | 12% | 17% | 42% | 0.47 | 3 |
| 101 | [**prince_alwaleed**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/prince_alwaleed_20260409_093741.md) | 0.09 | 57% | 6% | 23% | 32% | 1.04 | 2 |
| 102 | [**high_yield_reit_bdc**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/high_yield_reit_bdc_20260408_223216.md) | 0.09 | 75% | 6% | 13% | 27% | 0.49 | 10 |
| 103 | [**peter_lynch**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/peter_lynch_20260408_231617.md) | 0.09 | 67% | 6% | 12% | 30% | 0.28 | 4 |
| 104 | [**li_ka_shing**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/li_ka_shing_20260408_231646.md) | 0.08 | 67% | 6% | 12% | 27% | 0.16 | 5 |
| 105 | [**sector_monthly_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/sector_monthly_rotation_20260408_142002.md) | 0.08 | 67% | 7% | 12% | 28% | 0.74 | 3 |
| 106 | [**retail_deep_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/retail_deep_value_20260409_093423.md) | 0.08 | 67% | 5% | 16% | 32% | 0.32 | 3 |
| 107 | [**china_adr_deep_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/china_adr_deep_value_20260409_093341.md) | 0.08 | 92% | 5% | 14% | 19% | 0.41 | 5 |
| 108 | [**global_consumer_staples**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/global_consumer_staples_20260409_093344.md) | 0.08 | 50% | 5% | 18% | 30% | -0.4 | 8 |
| 109 | [**support_resistance**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/support_resistance_20260409_093745.md) | 0.07 | 67% | 6% | 12% | 26% | -0.39 | 6 |
| 110 | [**williams_percent_r**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/williams_percent_r_20260408_231254.md) | 0.07 | 57% | 6% | 10% | 22% | 0.37 | 6 |
| 111 | [**market_making_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/market_making_momentum_20260408_230709.md) | 0.07 | 57% | 6% | 10% | 27% | 0.04 | 9 |
| 112 | [**ray_dalio**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/ray_dalio_20260408_155403.md) | 0.07 | 67% | 6% | 10% | 21% | 0.68 | 5 |
| 113 | [**stat_arb_medallion**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/stat_arb_medallion_20260409_093508.md) | 0.07 | 57% | 4% | 11% | 21% | -0.14 | 1 |
| 114 | [**small_cap_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/small_cap_value_20260409_093328.md) | 0.06 | 67% | 1% | 14% | 20% | 0.39 | 12 |
| 115 | [**water_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/water_monopoly_20260408_225824.md) | 0.06 | 75% | 6% | 6% | 21% | 0.22 | 6 |
| 116 | [**wealth_barometer**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/wealth_barometer_20260408_230338.md) | 0.06 | 57% | 3% | 11% | 24% | 0.35 | 3 |
| 117 | [**cloud_cyber_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/cloud_cyber_value_20260408_225839.md) | 0.06 | 57% | 14% | 7% | 27% | 0.43 | 5 |
| 118 | [**economic_indicators**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/economic_indicators_20260408_230308.md) | 0.06 | 57% | 5% | 10% | 20% | 0.12 | 4 |
| 119 | [**agriculture_food**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/agriculture_food_20260409_093443.md) | 0.06 | 50% | 7% | 20% | 22% | -1.51 | 4 |
| 120 | [**dcf_deep_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dcf_deep_value_20260409_093414.md) | 0.05 | 50% | 5% | 11% | 23% | -0.09 | 10 |
| 121 | [**geopolitical_crisis**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/geopolitical_crisis_20260409_093442.md) | 0.05 | 50% | 5% | 10% | 22% | -0.34 | 9 |
| 122 | [**carl_icahn**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/carl_icahn_20260409_093738.md) | 0.04 | 42% | 3% | 13% | 20% | 0.39 | 12 |
| 123 | [**dividend_aristocrat_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dividend_aristocrat_momentum_20260409_093409.md) | 0.04 | 42% | 6% | 9% | 22% | -0.53 | 10 |
| 124 | [**l_shape_stagnation**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/l_shape_stagnation_20260408_230923.md) | 0.04 | 42% | 5% | 10% | 20% | 0.23 | 3 |
| 125 | [**gaming_catalyst**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/gaming_catalyst_20260408_141859.md) | 0.04 | 50% | 8% | 10% | 14% | 0.22 | 7 |
| 126 | [**crisis_alpha**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/crisis_alpha_20260408_230758.md) | 0.04 | 57% | 6% | 6% | 17% | 1.04 | 4 |
| 127 | [**tail_risk_harvest**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/tail_risk_harvest_20260409_093407.md) | 0.04 | 42% | 5% | 8% | 22% | -0.03 | 2 |
| 128 | [**risk_parity**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/risk_parity_20260408_230646.md) | 0.04 | 50% | 5% | 7% | 17% | 0.62 | 8 |
| 129 | [**activist_distressed**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/activist_distressed_20260409_093515.md) | 0.04 | 50% | 1% | 14% | 15% | -0.07 | 12 |
| 130 | [**serial_acquirer**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/serial_acquirer_20260408_230230.md) | 0.04 | 42% | 4% | 12% | 18% | 0.32 | 5 |
| 131 | [**crypto_crash_tradfi**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/crypto_crash_tradfi_20260408_230335.md) | 0.04 | 50% | 3% | 7% | 16% | 0.01 | 2 |
| 132 | [**sell_in_may**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/sell_in_may_20260408_225937.md) | 0.04 | 50% | 4% | 7% | 18% | 0.38 | 2 |
| 133 | [**unemployment_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/unemployment_momentum_20260408_230914.md) | 0.04 | 50% | 6% | 4% | 17% | 0.34 | 8 |
| 134 | [**jorge_paulo_lemann**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/jorge_paulo_lemann_20260408_231652.md) | 0.03 | 42% | 4% | 6% | 17% | 0.25 | 1 |
| 135 | [**turn_of_month**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/turn_of_month_20260409_093353.md) | 0.02 | 42% | 3% | 9% | 8% | -0.59 | 2 |
| 136 | [**hurst_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/hurst_regime_20260408_231017.md) | 0.02 | 33% | 3% | 7% | 13% | 0.4 | 1 |
| 137 | [**equal_risk_contrib**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/equal_risk_contrib_20260408_231103.md) | 0.02 | 42% | 6% | 1% | 8% | 0.76 | 7 |
| 138 | [**rideshare_mobility**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/rideshare_mobility_20260409_093348.md) | 0.01 | 33% | 3% | 7% | 5% | 0.69 | 4 |
| 139 | [**news_media_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/news_media_monopoly_20260408_230249.md) | 0.01 | 33% | 6% | 2% | 7% | 0.64 | 2 |
| 140 | [**contrarian_fallen_angels**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/contrarian_fallen_angels_20260408_230444.md) | 0.01 | 33% | 1% | 5% | 7% | 0.06 | 4 |
| 141 | [**earnings_gap_and_go**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/earnings_gap_and_go_20260408_231447.md) | 0.01 | 17% | 2% | 7% | 12% | 0.19 | 12 |
| 142 | [**earnings_whisper**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/earnings_whisper_20260408_230836.md) | 0.01 | 33% | 4% | 2% | 6% | 0.45 | 3 |
| 143 | [**emerging_market_etf_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/emerging_market_etf_value_20260408_225858.md) | 0.01 | 33% | 3% | 3% | 5% | 0.58 | 6 |
| 144 | [**all_weather_modern**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/all_weather_modern_20260408_230405.md) | 0.01 | 25% | 2% | 3% | 6% | 0.15 | 7 |
| 145 | [**benjamin_graham**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/benjamin_graham_20260409_093751.md) | 0.01 | 17% | 1% | 7% | 8% | -1.03 | 12 |
| 146 | [**howard_marks**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/howard_marks_20260409_093742.md) | 0.01 | 17% | 1% | 4% | 8% | -1.77 | 12 |
| 147 | [**zscore_reversion**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/zscore_reversion_20260409_093550.md) | 0.01 | 17% | 1% | 3% | 7% | -0.18 | 12 |
| 148 | [**constellation_contrarian**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/constellation_contrarian_20260409_093422.md) | 0.0 | 33% | 1% | 1% | 1% | -0.19 | 9 |
| 149 | [**china_tech_rebound**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/china_tech_rebound_20260408_225721.md) | 0.0 | 50% | 7% | -2% | -3% | 0.03 | 4 |
| 150 | [**vix_fear_buy**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/vix_fear_buy_20260409_093712.md) | 0.0 | 8% | 1% | 2% | 4% | -0.11 | 3 |
| 151 | [**quant**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/quant_20260409_093720.md) | 0.0 | 17% | 2% | -1% | 2% | -1.03 | 12 |
| 152 | [**cointegration_pairs**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/cointegration_pairs_20260409_093609.md) | 0.0 | 8% | 1% | -1% | 4% | -0.47 | 2 |
| 153 | [**news_reaction_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/news_reaction_momentum_20260409_093518.md) | 0.0 | 8% | 0% | 0% | 1% | -0.09 | 12 |
| 154 | [**treasury_safe**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/treasury_safe_20260408_230904.md) | 0.0 | 33% | 2% | -2% | 0% | 0.42 | 5 |
| 155 | [**nvidia_domino_hedge**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/nvidia_domino_hedge_20260409_093432.md) | -0.0 | 0% | -5% | -16% | -25% | -0.83 | 5 |
| 156 | [**earnings_surprise_drift**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/earnings_surprise_drift_20260409_093524.md) | 0.0 | 0% | 1% | 3% | 6% | -0.53 | 12 |
| 157 | [**merger_arbitrage**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/merger_arbitrage_20260409_093538.md) | -0.0 | 0% | -2% | -7% | -11% | -2.22 | 1 |
| 158 | [**volatility_breakout**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/volatility_breakout_20260409_093602.md) | -0.0 | 0% | 0% | -1% | -1% | -1.73 | 12 |
| 159 | [**optimal_stopping**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/optimal_stopping_20260409_093630.md) | -0.0 | 0% | -15% | -37% | -55% | -1.43 | 4 |
| 160 | [**ensemble**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/ensemble_20260409_093731.md) | -0.0 | 0% | 0% | 0% | 0% | -4.46 | 12 |
| 161 | [**muni_bond_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/muni_bond_income_20260409_093419.md) | -0.0 | 8% | 1% | -2% | 0% | -0.07 | 6 |
| 162 | [**retail_crash_ecommerce**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/retail_crash_ecommerce_20260408_230330.md) | -0.0 | 50% | 7% | -5% | -2% | 0.74 | 2 |
| 163 | [**bond_fixed_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/bond_fixed_income_20260408_230417.md) | -0.0 | 33% | 1% | -3% | -2% | 0.21 | 10 |
| 164 | [**v_shape_recovery**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/v_shape_recovery_20260408_230916.md) | -0.0 | 33% | 6% | -5% | -4% | 0.97 | 1 |
| 165 | [**fixed_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/fixed_income_20260409_093720.md) | -0.0 | 8% | 0% | -6% | -7% | -0.4 | 5 |
| 166 | [**fallen_blue_chip_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/fallen_blue_chip_value_20260408_230304.md) | -0.01 | 17% | 0% | -7% | -8% | 0.29 | 2 |
| 167 | [**dividend_capture**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dividend_capture_20260409_093539.md) | -0.01 | 25% | 0% | -7% | -4% | -0.4 | 9 |
| 168 | [**water_scarcity**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/water_scarcity_20260409_093447.md) | -0.01 | 17% | 0% | -9% | -8% | -0.79 | 4 |
| 169 | [**gap_fill_spy**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/gap_fill_spy_20260409_093642.md) | -0.01 | 8% | -4% | -14% | -22% | -1.57 | 1 |
| 170 | [**meme_stock**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/meme_stock_20260409_093716.md) | -0.01 | 8% | -5% | -22% | -28% | -0.53 | 12 |
| 171 | [**michael_burry**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/michael_burry_20260409_093734.md) | -0.01 | 25% | -2% | -6% | -11% | -0.03 | 12 |
| 172 | [**fda_catalyst**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/fda_catalyst_20260409_093529.md) | -0.01 | 25% | -2% | -10% | -11% | -0.28 | 8 |
| 173 | [**clean_energy**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/clean_energy_20260409_093320.md) | -0.02 | 17% | 1% | -29% | -42% | -0.18 | 5 |
| 174 | [**global_airlines_travel**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/global_airlines_travel_20260408_225844.md) | -0.02 | 42% | 1% | -12% | -18% | 0.67 | 8 |
| 175 | [**cannabis_alt_consumer**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/cannabis_alt_consumer_20260408_230259.md) | -0.05 | 42% | -8% | -35% | -53% | 0.2 | 2 |

*Updated: 2026-04-09 09:38*

---

## Disclaimer

This leaderboard is for **educational and research purposes only**. It is **not financial advice**.

- Past performance does not guarantee future results.
- Backtests use historical data and may not reflect real-world conditions.
- All strategies tested with simulated capital. No real money was used.
- Consult a qualified financial advisor before making investment decisions.
- The authors accept no responsibility for financial losses from using this information.
- Securities mentioned are not buy/sell recommendations. Do your own due diligence.
- Trading involves substantial risk of loss. Only invest what you can afford to lose.

By using this information, you acknowledge and accept these risks.
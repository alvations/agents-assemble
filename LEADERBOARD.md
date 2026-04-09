# LEADERBOARD

**175 strategies** ranked by **Composite Score** across 12 rolling windows (2020-2025).

## Ranking Formula

```
Composite Score = Avg Return x Consistency x (1 - Avg |Max Drawdown|)
```

| Factor | What It Measures |
|--------|-----------------|
| **Avg Return** | Average total return across all 12 test windows |
| **Consistency** | % of windows where strategy made risk-adjusted profit (Sharpe > 0) |
| **Drawdown Penalty** | Bigger crashes = lower score |

**Windows:** 1Y (2020-2025, 6 windows) + 3Y (4 windows) + 5Y (2 windows) = 12 total

## How to Read This

| Metric | What It Means | Good | Bad |
|--------|--------------|------|-----|
| **Return** | Total cumulative return over the period | >50% | <0% |
| **Sharpe** | Return per unit of risk. Higher = better risk-adjusted | >1.0 | <0 |
| **Max DD** | Worst peak-to-trough drop during the period | >-15% | <-30% |
| **Win Rate** | % of trading days that were profitable | >55% | <40% |
| **Positions** | Number of stocks held at end of backtest | varies | 0 = exited all |
| **Composite** | Overall score combining return, consistency, and drawdown protection | >0.5 | <0 |
| **Consistency** | % of rolling windows where strategy had positive Sharpe | 100% | <50% |

Always look at Return + Sharpe + Max DD **together**. A high return with terrible Sharpe is gambling.

---

## Top 10 Strategies

### #1 [ai_token_economy](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_token_economy_20260409_083837.md)

| Composite | Consistency | Avg Return | 3Y Return | 3Y Sharpe | 3Y Max DD | Positions |
|-----------|------------|------------|-----------|-----------|-----------|-----------|
| **1.1** | **92%** | 156.3% | 335.2% | 1.64 | -28.7% | 9 |

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

### #2 [uranium_renaissance](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/uranium_renaissance_20260409_083826.md)

| Composite | Consistency | Avg Return | 3Y Return | 3Y Sharpe | 3Y Max DD | Positions |
|-----------|------------|------------|-----------|-----------|-----------|-----------|
| **0.74** | **92%** | 134.3% | 343.6% | 1.25 | -37.4% | 8 |

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

### #3 [concentrate_winners](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/concentrate_winners_20260409_083818.md)

| Composite | Consistency | Avg Return | 3Y Return | 3Y Sharpe | 3Y Max DD | Positions |
|-----------|------------|------------|-----------|-----------|-----------|-----------|
| **0.62** | **92%** | 89.4% | 154.1% | 1.18 | -29.7% | 5 |

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

### #4 [ai_revolution](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_revolution_20260409_083715.md)

| Composite | Consistency | Avg Return | 3Y Return | 3Y Sharpe | 3Y Max DD | Positions |
|-----------|------------|------------|-----------|-----------|-----------|-----------|
| **0.53** | **92%** | 79.1% | 170.9% | 1.21 | -27.4% | 8 |

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

### #5 [david_tepper](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/david_tepper_20260409_084004.md)

| Composite | Consistency | Avg Return | 3Y Return | 3Y Sharpe | 3Y Max DD | Positions |
|-----------|------------|------------|-----------|-----------|-----------|-----------|
| **0.52** | **100%** | 64.6% | 91.5% | 1.19 | -18.4% | 6 |

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

### #6 [barbell_portfolio](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/barbell_portfolio_20260409_083844.md)

| Composite | Consistency | Avg Return | 3Y Return | 3Y Sharpe | 3Y Max DD | Positions |
|-----------|------------|------------|-----------|-----------|-----------|-----------|
| **0.48** | **92%** | 65.3% | 163.7% | 1.9 | -12.1% | 7 |

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

### #7 [momentum](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/momentum_20260409_084034.md)

| Composite | Consistency | Avg Return | 3Y Return | 3Y Sharpe | 3Y Max DD | Positions |
|-----------|------------|------------|-----------|-----------|-----------|-----------|
| **0.48** | **92%** | 71.3% | 178.1% | 1.42 | -29.8% | 5 |

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

### #8 [masayoshi_son](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/masayoshi_son_20260409_084051.md)

| Composite | Consistency | Avg Return | 3Y Return | 3Y Sharpe | 3Y Max DD | Positions |
|-----------|------------|------------|-----------|-----------|-----------|-----------|
| **0.47** | **92%** | 83.4% | 167.5% | 1.06 | -28.7% | 4 |

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

### #9 [conservative_regime](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/conservative_regime_20260409_084103.md)

| Composite | Consistency | Avg Return | 3Y Return | 3Y Sharpe | 3Y Max DD | Positions |
|-----------|------------|------------|-----------|-----------|-----------|-----------|
| **0.46** | **92%** | 59.8% | 103.2% | 1.65 | -13.5% | 11 |

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

### #10 [nancy_pelosi](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nancy_pelosi_20260409_084002.md)

| Composite | Consistency | Avg Return | 3Y Return | 3Y Sharpe | 3Y Max DD | Positions |
|-----------|------------|------------|-----------|-----------|-----------|-----------|
| **0.44** | **92%** | 58.1% | 118.8% | 1.52 | -13.7% | 6 |

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

| # | Strategy | Composite | Consistency | Avg Ret | 3Y Ret | 3Y Sharpe | Pos |
|---|----------|-----------|------------|---------|--------|-----------|-----|
| 1 | [**ai_token_economy**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_token_economy_20260409_083837.md) | 1.1 | 92% | 156.3% | 335.2% | 1.64 | 9 |
| 2 | [**uranium_renaissance**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/uranium_renaissance_20260409_083826.md) | 0.74 | 92% | 134.3% | 343.6% | 1.25 | 8 |
| 3 | [**concentrate_winners**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/concentrate_winners_20260409_083818.md) | 0.62 | 92% | 89.4% | 154.1% | 1.18 | 5 |
| 4 | [**ai_revolution**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ai_revolution_20260409_083715.md) | 0.53 | 92% | 79.1% | 170.9% | 1.21 | 8 |
| 5 | [**david_tepper**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/david_tepper_20260409_084004.md) | 0.52 | 100% | 64.6% | 91.5% | 1.19 | 6 |
| 6 | [**barbell_portfolio**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/barbell_portfolio_20260409_083844.md) | 0.48 | 92% | 65.3% | 163.7% | 1.9 | 7 |
| 7 | [**momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/momentum_20260409_084034.md) | 0.48 | 92% | 71.3% | 178.1% | 1.42 | 5 |
| 8 | [**masayoshi_son**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/masayoshi_son_20260409_084051.md) | 0.47 | 92% | 83.4% | 167.5% | 1.06 | 4 |
| 9 | [**conservative_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/conservative_regime_20260409_084103.md) | 0.46 | 92% | 59.8% | 103.2% | 1.65 | 11 |
| 10 | [**nancy_pelosi**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nancy_pelosi_20260409_084002.md) | 0.44 | 92% | 58.1% | 118.8% | 1.52 | 6 |
| 11 | [**midstream_toll_road**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/midstream_toll_road_20260409_083831.md) | 0.43 | 83% | 66.7% | 74.8% | 0.98 | 7 |
| 12 | [**mag7_domino_hedge**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/mag7_domino_hedge_20260409_083805.md) | 0.43 | 92% | 65.5% | 154.3% | 1.51 | 16 |
| 13 | [**adaptive_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/adaptive_regime_20260409_084102.md) | 0.4 | 83% | 59.4% | 97.9% | 1.34 | 10 |
| 14 | [**robotics_autonomous**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/robotics_autonomous_20260409_083734.md) | 0.4 | 92% | 52.7% | 93.5% | 1.1 | 8 |
| 15 | [**crypto_ecosystem**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/crypto_ecosystem_20260409_083730.md) | 0.39 | 83% | 60.6% | 46.8% | 0.45 | 10 |
| 16 | [**subscription_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/subscription_monopoly_20260408_220452.md) | 0.39 | 83% | 56.1% | 57.2% | 0.75 | 10 |
| 17 | [**core_satellite**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/core_satellite_20260409_083846.md) | 0.38 | 92% | 48.4% | 107.1% | 1.64 | 6 |
| 18 | [**stanley_druckenmiller**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/stanley_druckenmiller_20260409_084057.md) | 0.35 | 83% | 55.9% | 164.0% | 1.66 | 9 |
| 19 | [**reshoring_industrial**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/reshoring_industrial_20260409_083742.md) | 0.35 | 92% | 46.1% | 60.9% | 0.77 | 11 |
| 20 | [**semiconductor_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/semiconductor_value_20260408_220448.md) | 0.34 | 92% | 55.0% | 145.8% | 1.03 | 10 |
| 21 | [**dan_loeb**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dan_loeb_20260409_084005.md) | 0.33 | 83% | 46.9% | 75.0% | 1.05 | 3 |
| 22 | [**kelly_optimal**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/kelly_optimal_20260409_083939.md) | 0.33 | 92% | 43.4% | 82.9% | 1.15 | 9 |
| 23 | [**bipartisan_consensus**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/bipartisan_consensus_20260409_084003.md) | 0.32 | 92% | 39.9% | 56.0% | 1.06 | 9 |
| 24 | [**uk_european_banking**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/uk_european_banking_20260409_083756.md) | 0.32 | 100% | 41.4% | 84.7% | 1.27 | 5 |
| 25 | [**adaptive_ensemble**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/adaptive_ensemble_20260409_083845.md) | 0.32 | 92% | 42.0% | 84.0% | 1.22 | 7 |
| 26 | [**contrastive_pairs**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/contrastive_pairs_20260408_220455.md) | 0.32 | 92% | 46.3% | 117.8% | 1.2 | 10 |
| 27 | [**job_loss_tech_boom**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/job_loss_tech_boom_20260409_083838.md) | 0.32 | 83% | 50.0% | 83.7% | 0.86 | 8 |
| 28 | [**ken_griffin**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/ken_griffin_20260409_084005.md) | 0.31 | 92% | 45.4% | 118.8% | 1.34 | 6 |
| 29 | [**staples_hedged_growth**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/staples_hedged_growth_20260409_083844.md) | 0.3 | 92% | 38.8% | 87.8% | 1.64 | 13 |
| 30 | [**rare_earth_minerals**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/rare_earth_minerals_20260408_161751.md) | 0.3 | 75% | 47.9% | 62.3% | 0.74 | 10 |
| 31 | [**specialty_insurance**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/specialty_insurance_20260409_083825.md) | 0.3 | 100% | 35.1% | 56.9% | 0.64 | 3 |
| 32 | [**growth_concentration**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/growth_concentration_20260409_083918.md) | 0.29 | 83% | 48.0% | 79.9% | 0.76 | 5 |
| 33 | [**oil_down_tech_up**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/oil_down_tech_up_20260409_083838.md) | 0.28 | 83% | 39.7% | 54.5% | 0.97 | 3 |
| 34 | [**george_soros**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/george_soros_20260409_084046.md) | 0.28 | 75% | 45.0% | 83.5% | 1.17 | 5 |
| 35 | [**gop_trading**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/gop_trading_20260409_084002.md) | 0.27 | 92% | 36.5% | 73.0% | 1.26 | 9 |
| 36 | [**bill_ackman**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/bill_ackman_20260409_084056.md) | 0.25 | 83% | 37.4% | 96.8% | 1.28 | 7 |
| 37 | [**dynamic_ensemble**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dynamic_ensemble_20260409_083908.md) | 0.24 | 92% | 30.7% | 49.1% | 0.88 | 12 |
| 38 | [**singapore_alpha**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/singapore_alpha_20260409_083755.md) | 0.24 | 92% | 31.0% | 50.4% | 0.8 | 9 |
| 39 | [**energy_seasonal**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/energy_seasonal_20260409_084008.md) | 0.23 | 75% | 40.8% | 6.0% | -0.1 | 5 |
| 40 | [**short_seller_dip_buy**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/short_seller_dip_buy_20260409_084033.md) | 0.23 | 83% | 31.5% | 75.4% | 1.05 | 1 |
| 41 | [**jim_simons**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/jim_simons_20260409_084050.md) | 0.22 | 92% | 28.7% | 46.6% | 0.94 | 12 |
| 42 | [**biotech_breakout**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/biotech_breakout_20260409_083720.md) | 0.22 | 100% | 26.8% | 43.4% | 0.58 | 12 |
| 43 | [**warflation_hedge**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/warflation_hedge_20260409_090630.md) | 0.22 | 83% | 29.8% | 15.7% | 0.15 | 10 |
| 44 | [**healthcare_asia_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/healthcare_asia_momentum_20260409_083906.md) | 0.21 | 83% | 32.2% | 42.8% | 0.6 | 12 |
| 45 | [**defensive_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defensive_rotation_20260409_083933.md) | 0.21 | 83% | 31.7% | 41.8% | 0.68 | 6 |
| 46 | [**utility_infra_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/utility_infra_income_20260409_083749.md) | 0.21 | 92% | 26.5% | 37.4% | 0.69 | 8 |
| 47 | [**buffett_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/buffett_value_20260409_084033.md) | 0.21 | 83% | 29.6% | 55.6% | 1.51 | 2 |
| 48 | [**yield_curve_inversion**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/yield_curve_inversion_20260409_083934.md) | 0.2 | 92% | 25.3% | 65.8% | 1.2 | 7 |
| 49 | [**shipping_freight_cycle**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/shipping_freight_cycle_20260409_083901.md) | 0.19 | 83% | 28.3% | 29.0% | 0.39 | 8 |
| 50 | [**dividend**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dividend_20260409_084036.md) | 0.19 | 92% | 24.5% | 29.8% | 0.51 | 11 |
| 51 | [**dogs_of_dow**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dogs_of_dow_20260408_155136.md) | 0.19 | 92% | 26.9% | 73.0% | 1.04 | 10 |
| 52 | [**blackrock_2026**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/blackrock_2026_20260409_084059.md) | 0.19 | 92% | 25.1% | 67.9% | 1.22 | 8 |
| 53 | [**nvidia_supply_chain**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/nvidia_supply_chain_20260408_225113.md) | 0.19 | 83% | 29.2% | 70.5% | 0.74 | 4 |
| 54 | [**cathie_wood**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/cathie_wood_20260409_084059.md) | 0.19 | 75% | 31.9% | 59.5% | 0.62 | 5 |
| 55 | [**dividend_aristocrat_blue_chips**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/dividend_aristocrat_blue_chips_20260409_083851.md) | 0.18 | 92% | 24.0% | 24.6% | 0.36 | 14 |
| 56 | [**nvidia_chain_diversified**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nvidia_chain_diversified_20260409_083843.md) | 0.18 | 67% | 35.5% | 138.9% | 1.28 | 3 |
| 57 | [**quality_factor**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/quality_factor_20260409_083808.md) | 0.18 | 83% | 25.7% | 36.4% | 0.69 | 8 |
| 58 | [**pairs**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/pairs_20260409_084040.md) | 0.18 | 92% | 21.8% | 38.4% | 1.02 | 8 |
| 59 | [**recession_detector**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/recession_detector_20260409_083933.md) | 0.18 | 92% | 23.1% | 54.9% | 1.04 | 5 |
| 60 | [**infrastructure_boom**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/infrastructure_boom_20260409_083725.md) | 0.17 | 92% | 23.2% | 36.6% | 0.55 | 10 |
| 61 | [**defense_budget_floor**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defense_budget_floor_20260409_090631.md) | 0.17 | 83% | 23.1% | 61.7% | 1.01 | 8 |
| 62 | [**berkshire_holdings**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/berkshire_holdings_20260409_084100.md) | 0.17 | 92% | 22.5% | 42.9% | 0.72 | 10 |
| 63 | [**insurance_float**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/insurance_float_20260409_083823.md) | 0.17 | 83% | 22.8% | 42.5% | 0.69 | 7 |
| 64 | [**japanese_sogo_shosha**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/japanese_sogo_shosha_20260409_084100.md) | 0.16 | 92% | 22.1% | 48.9% | 0.68 | 4 |
| 65 | [**defense_aerospace**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defense_aerospace_20260409_083718.md) | 0.15 | 75% | 31.7% | 111.0% | 0.7 | 9 |
| 66 | [**sector_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/sector_rotation_20260409_084040.md) | 0.15 | 83% | 21.2% | 7.7% | -0.08 | 4 |
| 67 | [**boring_compounder**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/boring_compounder_20260408_230207.md) | 0.15 | 75% | 25.7% | 36.9% | 0.54 | 3 |
| 68 | [**polymarket_signal**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/polymarket_signal_20260409_084003.md) | 0.14 | 92% | 18.4% | 41.4% | 0.86 | 4 |
| 69 | [**product_tanker_shipping**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/product_tanker_shipping_20260409_083903.md) | 0.14 | 75% | 25.6% | 9.0% | 0.04 | 8 |
| 70 | [**income_shield**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/income_shield_20260408_141844.md) | 0.14 | 92% | 17.9% | 30.1% | 0.63 | 11 |
| 71 | [**japan_industrial_finance**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/japan_industrial_finance_20260409_083750.md) | 0.14 | 75% | 23.4% | 76.3% | 0.91 | 6 |
| 72 | [**global_financial_infra**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/global_financial_infra_20260408_220459.md) | 0.14 | 75% | 22.1% | 58.7% | 0.96 | 10 |
| 73 | [**patent_cliff_pharma**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/patent_cliff_pharma_20260409_083830.md) | 0.13 | 75% | 20.2% | 10.1% | -0.01 | 1 |
| 74 | [**latam_growth**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/latam_growth_20260409_083723.md) | 0.13 | 83% | 21.0% | 63.0% | 0.78 | 8 |
| 75 | [**vix_spike_buyback**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/vix_spike_buyback_20260409_083840.md) | 0.13 | 83% | 17.8% | 48.7% | 1.14 | 4 |
| 76 | [**aging_population**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/aging_population_20260408_155019.md) | 0.13 | 67% | 22.6% | 22.9% | 0.3 | 12 |
| 77 | [**beaten_down_staples**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/beaten_down_staples_20260409_083822.md) | 0.12 | 75% | 18.9% | 3.2% | -0.24 | 6 |
| 78 | [**entropy_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/entropy_regime_20260408_161814.md) | 0.12 | 75% | 19.1% | 56.4% | 1.2 | 7 |
| 79 | [**k_shape_economy**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/k_shape_economy_20260408_230922.md) | 0.12 | 83% | 18.2% | 11.3% | 0.04 | 3 |
| 80 | [**small_cap_value_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/small_cap_value_rotation_20260408_230441.md) | 0.12 | 67% | 24.4% | 22.2% | 0.25 | 8 |
| 81 | [**gig_economy_saas**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/gig_economy_saas_20260409_083758.md) | 0.12 | 75% | 22.5% | 52.0% | 0.55 | 4 |
| 82 | [**fallen_luxury**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/fallen_luxury_20260409_083827.md) | 0.12 | 67% | 23.5% | -2.9% | -0.19 | 3 |
| 83 | [**hidden_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/hidden_monopoly_20260408_230144.md) | 0.12 | 75% | 19.6% | 34.3% | 0.52 | 6 |
| 84 | [**gold_bug**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/gold_bug_20260408_155231.md) | 0.12 | 57% | 24.8% | 94.4% | 1.13 | 4 |
| 85 | [**mag7_hidden_suppliers**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/mag7_hidden_suppliers_20260408_225932.md) | 0.11 | 75% | 21.6% | 46.2% | 0.53 | 9 |
| 86 | [**fifty_two_week_breakout**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/fifty_two_week_breakout_20260409_084018.md) | 0.11 | 83% | 13.4% | 14.9% | 0.22 | 1 |
| 87 | [**nassef_sawiris**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/nassef_sawiris_20260409_084052.md) | 0.11 | 75% | 17.2% | 15.6% | 0.14 | 1 |
| 88 | [**glp1_obesity**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/glp1_obesity_20260409_083732.md) | 0.1 | 67% | 18.2% | 34.2% | 0.44 | 8 |
| 89 | [**telecom_equipment_5g**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/telecom_equipment_5g_20260408_223146.md) | 0.1 | 75% | 16.6% | 46.8% | 0.59 | 4 |
| 90 | [**toll_booth_economy**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/toll_booth_economy_20260409_083822.md) | 0.1 | 83% | 14.9% | 37.6% | 0.61 | 5 |
| 91 | [**dollar_weak_em_strong**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dollar_weak_em_strong_20260408_223948.md) | 0.1 | 57% | 18.7% | 36.8% | 0.85 | 2 |
| 92 | [**billboard_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/billboard_monopoly_20260408_220423.md) | 0.1 | 67% | 18.9% | 38.1% | 0.47 | 7 |
| 93 | [**regulated_data**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/regulated_data_20260408_225826.md) | 0.1 | 75% | 15.1% | 11.1% | 0.01 | 3 |
| 94 | [**consumer_credit_stress**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/consumer_credit_stress_20260409_083935.md) | 0.09 | 67% | 16.9% | 32.4% | 0.51 | 7 |
| 95 | [**bonds_down_banks_up**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/bonds_down_banks_up_20260408_223953.md) | 0.09 | 67% | 17.6% | 34.0% | 0.51 | 10 |
| 96 | [**vix_mean_reversion**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/vix_mean_reversion_20260408_155501.md) | 0.09 | 67% | 16.7% | 56.2% | 1.06 | 5 |
| 97 | [**global_pharma_pipeline**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/global_pharma_pipeline_20260408_222020.md) | 0.09 | 75% | 14.8% | 37.2% | 0.55 | 6 |
| 98 | [**defense_prime_contractors**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/defense_prime_contractors_20260409_083751.md) | 0.09 | 67% | 16.5% | 18.9% | 0.21 | 8 |
| 99 | [**korean_chaebols**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/korean_chaebols_20260408_223153.md) | 0.09 | 75% | 15.7% | 37.5% | 0.48 | 7 |
| 100 | [**growth**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/growth_20260409_084039.md) | 0.08 | 67% | 18.7% | 46.0% | 0.47 | 3 |
| 101 | [**prince_alwaleed**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/prince_alwaleed_20260409_084053.md) | 0.07 | 57% | 15.8% | 46.5% | 1.04 | 2 |
| 102 | [**china_adr_deep_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/china_adr_deep_value_20260409_083746.md) | 0.07 | 92% | 10.3% | 28.2% | 0.41 | 5 |
| 103 | [**high_yield_reit_bdc**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/high_yield_reit_bdc_20260408_223216.md) | 0.07 | 75% | 11.9% | 28.5% | 0.49 | 10 |
| 104 | [**sector_monthly_rotation**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/sector_monthly_rotation_20260408_142002.md) | 0.07 | 67% | 12.1% | 45.3% | 0.74 | 3 |
| 105 | [**peter_lynch**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/peter_lynch_20260408_231617.md) | 0.07 | 67% | 11.8% | 21.4% | 0.28 | 4 |
| 106 | [**li_ka_shing**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/li_ka_shing_20260408_231646.md) | 0.07 | 67% | 11.3% | 16.1% | 0.16 | 5 |
| 107 | [**retail_deep_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/retail_deep_value_20260409_083834.md) | 0.06 | 67% | 13.2% | 27.9% | 0.32 | 3 |
| 108 | [**support_resistance**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/support_resistance_20260409_084055.md) | 0.06 | 67% | 11.3% | -8.3% | -0.39 | 6 |
| 109 | [**global_consumer_staples**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/global_consumer_staples_20260409_083752.md) | 0.06 | 50% | 13.6% | -3.2% | -0.4 | 8 |
| 110 | [**ray_dalio**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/ray_dalio_20260408_155403.md) | 0.06 | 67% | 9.5% | 30.8% | 0.68 | 5 |
| 111 | [**williams_percent_r**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/williams_percent_r_20260408_231254.md) | 0.05 | 57% | 9.9% | 18.9% | 0.37 | 6 |
| 112 | [**cloud_cyber_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/cloud_cyber_value_20260408_225839.md) | 0.05 | 57% | 14.1% | 42.9% | 0.43 | 5 |
| 113 | [**market_making_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/market_making_momentum_20260408_230709.md) | 0.05 | 57% | 10.8% | 11.8% | 0.04 | 9 |
| 114 | [**stat_arb_medallion**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/stat_arb_medallion_20260409_083913.md) | 0.05 | 57% | 9.4% | 10.2% | -0.14 | 1 |
| 115 | [**agriculture_food**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/agriculture_food_20260409_083853.md) | 0.05 | 50% | 14.1% | -34.9% | -1.51 | 4 |
| 116 | [**water_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/water_monopoly_20260408_225824.md) | 0.05 | 75% | 8.4% | 19.6% | 0.22 | 6 |
| 117 | [**small_cap_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/small_cap_value_20260409_083728.md) | 0.05 | 67% | 8.4% | 22.6% | 0.39 | 12 |
| 118 | [**wealth_barometer**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/wealth_barometer_20260408_230338.md) | 0.04 | 57% | 9.4% | 25.9% | 0.35 | 3 |
| 119 | [**economic_indicators**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/economic_indicators_20260408_230308.md) | 0.04 | 57% | 8.9% | 14.6% | 0.12 | 4 |
| 120 | [**dcf_deep_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dcf_deep_value_20260409_083821.md) | 0.04 | 50% | 9.8% | 5.1% | -0.09 | 10 |
| 121 | [**gaming_catalyst**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/gaming_catalyst_20260408_141859.md) | 0.04 | 50% | 9.5% | 20.3% | 0.22 | 7 |
| 122 | [**geopolitical_crisis**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/geopolitical_crisis_20260409_083852.md) | 0.04 | 50% | 9.6% | 0.1% | -0.34 | 9 |
| 123 | [**crisis_alpha**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/crisis_alpha_20260408_230758.md) | 0.04 | 57% | 8.1% | 55.6% | 1.04 | 4 |
| 124 | [**dividend_aristocrat_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dividend_aristocrat_momentum_20260409_083816.md) | 0.04 | 42% | 9.6% | -5.1% | -0.53 | 10 |
| 125 | [**carl_icahn**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/carl_icahn_20260409_084050.md) | 0.04 | 42% | 9.2% | 20.2% | 0.39 | 12 |
| 126 | [**l_shape_stagnation**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/l_shape_stagnation_20260408_230923.md) | 0.03 | 42% | 8.8% | 14.8% | 0.23 | 3 |
| 127 | [**risk_parity**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/risk_parity_20260408_230646.md) | 0.03 | 50% | 7.4% | 25.9% | 0.62 | 8 |
| 128 | [**tail_risk_harvest**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/tail_risk_harvest_20260409_083815.md) | 0.03 | 42% | 9.0% | 10.7% | -0.03 | 2 |
| 129 | [**serial_acquirer**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/serial_acquirer_20260408_230230.md) | 0.03 | 42% | 9.1% | 23.5% | 0.32 | 5 |
| 130 | [**activist_distressed**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/activist_distressed_20260409_083919.md) | 0.03 | 50% | 7.6% | 7.9% | -0.07 | 12 |
| 131 | [**sell_in_may**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/sell_in_may_20260408_225937.md) | 0.03 | 50% | 7.4% | 27.5% | 0.38 | 2 |
| 132 | [**crypto_crash_tradfi**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/crypto_crash_tradfi_20260408_230335.md) | 0.03 | 50% | 6.6% | 11.6% | 0.01 | 2 |
| 133 | [**unemployment_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/unemployment_momentum_20260408_230914.md) | 0.03 | 50% | 7.1% | 21.5% | 0.34 | 8 |
| 134 | [**jorge_paulo_lemann**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/jorge_paulo_lemann_20260408_231652.md) | 0.02 | 42% | 6.8% | 18.4% | 0.25 | 1 |
| 135 | [**turn_of_month**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/turn_of_month_20260409_083805.md) | 0.02 | 42% | 5.5% | -3.9% | -0.59 | 2 |
| 136 | [**hurst_regime**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/hurst_regime_20260408_231017.md) | 0.02 | 33% | 5.8% | 18.1% | 0.4 | 1 |
| 137 | [**equal_risk_contrib**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/equal_risk_contrib_20260408_231103.md) | 0.02 | 42% | 4.6% | 34.6% | 0.76 | 7 |
| 138 | [**news_media_monopoly**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/news_media_monopoly_20260408_230249.md) | 0.01 | 33% | 5.1% | 43.6% | 0.64 | 2 |
| 139 | [**rideshare_mobility**](https://github.com/alvations/agents-assemble/blob/main/strategy/winning/rideshare_mobility_20260409_083759.md) | 0.01 | 33% | 4.6% | 48.3% | 0.69 | 4 |
| 140 | [**earnings_whisper**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/earnings_whisper_20260408_230836.md) | 0.01 | 33% | 3.5% | 29.6% | 0.45 | 3 |
| 141 | [**emerging_market_etf_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/emerging_market_etf_value_20260408_225858.md) | 0.01 | 33% | 3.5% | 36.5% | 0.58 | 6 |
| 142 | [**earnings_gap_and_go**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/earnings_gap_and_go_20260408_231447.md) | 0.01 | 17% | 5.6% | 15.0% | 0.19 | 12 |
| 143 | [**contrarian_fallen_angels**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/contrarian_fallen_angels_20260408_230444.md) | 0.01 | 33% | 3.2% | 12.7% | 0.06 | 4 |
| 144 | [**all_weather_modern**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/all_weather_modern_20260408_230405.md) | 0.01 | 25% | 3.0% | 13.9% | 0.15 | 7 |
| 145 | [**benjamin_graham**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/benjamin_graham_20260409_084101.md) | 0.01 | 17% | 4.3% | 3.1% | -1.03 | 12 |
| 146 | [**china_tech_rebound**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/china_tech_rebound_20260408_225721.md) | 0.01 | 50% | 2.2% | 4.1% | 0.03 | 4 |
| 147 | [**howard_marks**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/howard_marks_20260409_084053.md) | 0.01 | 17% | 3.2% | -3.4% | -1.77 | 12 |
| 148 | [**zscore_reversion**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/zscore_reversion_20260409_083942.md) | 0.0 | 17% | 2.8% | 8.5% | -0.18 | 12 |
| 149 | [**retail_crash_ecommerce**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/retail_crash_ecommerce_20260408_230330.md) | 0.0 | 50% | 1.3% | 50.1% | 0.74 | 2 |
| 150 | [**constellation_contrarian**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/constellation_contrarian_20260409_083832.md) | 0.0 | 33% | 1.3% | -1.9% | -0.19 | 9 |
| 151 | [**quant**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/quant_20260409_084038.md) | 0.0 | 17% | 1.0% | -3.6% | -1.03 | 12 |
| 152 | [**vix_fear_buy**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/vix_fear_buy_20260409_084033.md) | 0.0 | 8% | 2.1% | 9.0% | -0.11 | 3 |
| 153 | [**treasury_safe**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/treasury_safe_20260408_230904.md) | 0.0 | 33% | 0.4% | 20.0% | 0.42 | 5 |
| 154 | [**v_shape_recovery**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/v_shape_recovery_20260408_230916.md) | 0.0 | 33% | 0.4% | 50.7% | 0.97 | 1 |
| 155 | [**cointegration_pairs**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/cointegration_pairs_20260409_083954.md) | 0.0 | 8% | 0.7% | 6.2% | -0.47 | 2 |
| 156 | [**news_reaction_momentum**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/news_reaction_momentum_20260409_083921.md) | 0.0 | 8% | 0.2% | 10.4% | -0.09 | 12 |
| 157 | [**nvidia_domino_hedge**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/nvidia_domino_hedge_20260409_083841.md) | -0.0 | 0% | -12.2% | -13.7% | -0.83 | 5 |
| 158 | [**earnings_surprise_drift**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/earnings_surprise_drift_20260409_083924.md) | 0.0 | 0% | 2.4% | 7.4% | -0.53 | 12 |
| 159 | [**merger_arbitrage**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/merger_arbitrage_20260409_083931.md) | -0.0 | 0% | -5.2% | -8.3% | -2.22 | 1 |
| 160 | [**volatility_breakout**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/volatility_breakout_20260409_083950.md) | -0.0 | 0% | -0.6% | -1.3% | -1.73 | 12 |
| 161 | [**optimal_stopping**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/optimal_stopping_20260409_084001.md) | -0.0 | 0% | -28.9% | -24.7% | -1.43 | 4 |
| 162 | [**ensemble**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/ensemble_20260409_084045.md) | -0.0 | 0% | -0.2% | 0.2% | -4.46 | 12 |
| 163 | [**muni_bond_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/muni_bond_income_20260409_083828.md) | -0.0 | 8% | -0.1% | 11.0% | -0.07 | 6 |
| 164 | [**bond_fixed_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/bond_fixed_income_20260408_230417.md) | -0.0 | 33% | -0.5% | 16.5% | 0.21 | 10 |
| 165 | [**fixed_income**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/fixed_income_20260409_084038.md) | -0.0 | 8% | -3.1% | 4.1% | -0.4 | 5 |
| 166 | [**fallen_blue_chip_value**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/fallen_blue_chip_value_20260408_230304.md) | -0.01 | 17% | -3.8% | 22.9% | 0.29 | 2 |
| 167 | [**dividend_capture**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/dividend_capture_20260409_083933.md) | -0.01 | 25% | -2.8% | -0.8% | -0.4 | 9 |
| 168 | [**water_scarcity**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/water_scarcity_20260409_083859.md) | -0.01 | 17% | -4.2% | -9.0% | -0.79 | 4 |
| 169 | [**gap_fill_spy**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/gap_fill_spy_20260409_084009.md) | -0.01 | 8% | -10.2% | -14.8% | -1.57 | 1 |
| 170 | [**meme_stock**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/meme_stock_20260409_084036.md) | -0.01 | 8% | -14.3% | -22.0% | -0.53 | 12 |
| 171 | [**michael_burry**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/michael_burry_20260409_084047.md) | -0.01 | 25% | -5.2% | 10.7% | -0.03 | 12 |
| 172 | [**fda_catalyst**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/fda_catalyst_20260409_083926.md) | -0.01 | 25% | -6.0% | 2.3% | -0.28 | 8 |
| 173 | [**clean_energy**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/clean_energy_20260409_083716.md) | -0.02 | 17% | -16.0% | -6.2% | -0.18 | 5 |
| 174 | [**global_airlines_travel**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/global_airlines_travel_20260408_225844.md) | -0.02 | 42% | -6.6% | 58.6% | 0.67 | 8 |
| 175 | [**cannabis_alt_consumer**](https://github.com/alvations/agents-assemble/blob/main/strategy/losing/cannabis_alt_consumer_20260408_230259.md) | -0.04 | 42% | -24.7% | 9.8% | 0.2 | 2 |

*Updated: 2026-04-09 09:09*

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
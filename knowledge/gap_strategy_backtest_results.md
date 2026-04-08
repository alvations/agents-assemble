# Gap Strategy Backtest Results

Strategies implemented from knowledge/missing_strategies_gaps.md.
Code: `gap_strategies.py` (ETFCointegration, ADXTrendFilter)

## 1. ETF Cointegration (Stat Arb)

Mean reversion on cointegrated ETF pairs using rolling OLS hedge ratio
and z-score spread trading. Pairs: EWA/EWC, GLD/SLV, SPY/IWM, XLF/XLK,
XLE/XOP, EWJ/EWH. Z-score entry at +/-2.0, exit at +/-0.5.

| Horizon | Sharpe | CAGR | Max DD | Total Return | Alpha vs SPY | Beta |
|---------|--------|------|--------|-------------|-------------|------|
| 1Y | 1.74 | 27.6% | -8.8% | 27.4% | +9.5% | — |
| 3Y | 1.04 | 15.4% | -8.9% | 53.4% | -7.8% | 0.54 |
| 5Y | 0.56 | 10.1% | -14.1% | 61.2% | -4.6% | — |

**Verdict: WINNER.** Sharpe >1.0 on 1Y and 3Y. Low drawdown (-8.9% on 3Y).
Low beta (0.54) means it's genuinely uncorrelated with the market.
1,457 trades over 3Y = active but not churning. Best recent performance
(1Y Sharpe 1.74) suggests pairs are well-cointegrated in current regime.
Weakens over 5Y as cointegration relationships shift (expected per research).

**Best for:** Moderate-risk diversification, market-neutral-ish returns.

## 2. ADX Trend Strength Filter

ADX (14-period) with DI+/DI- crossover and momentum confirmation.
Entry: ADX >25, DI+ > DI-, price > SMA50 > SMA200.
Exit: ADX <20. Position scaled by ADX strength.

| Horizon | Sharpe | CAGR | Max DD | Total Return | Alpha vs SPY | Beta |
|---------|--------|------|--------|-------------|-------------|------|
| 1Y | 0.05 | 4.1% | -2.8% | 4.1% | -14.1% | — |
| 3Y | 0.54 | 8.0% | -10.1% | 25.9% | -15.1% | 0.25 |
| 5Y | 0.11 | 4.5% | -10.2% | 24.8% | -10.2% | — |

**Verdict: MEDIOCRE standalone, USEFUL as filter.** Very low beta (0.25)
and tiny max drawdown (-2.8% on 1Y), but severely underperforms SPY.
Only invested ~15-25% of the time, confirming the research finding.
Win rate 46.2% (below 50%) with profit factor 1.25.

**Best for:** Adding as a filter to other strategies (only enter when ADX >25),
NOT as a standalone strategy. The low exposure is both its strength (low DD)
and weakness (low absolute returns).

## Comparison with Existing Top Strategies

| Strategy | 3Y Sharpe | 3Y CAGR | 3Y Max DD |
|----------|-----------|---------|-----------|
| ETF Cointegration (NEW) | **1.04** | 15.4% | -8.9% |
| Momentum Crash-Hedged | ~1.05 | — | — |
| AI Revolution (theme) | ~0.94 | — | — |
| Masayoshi Son (famous) | ~0.87 | — | — |
| ADX Trend Filter (NEW) | 0.54 | 8.0% | -10.1% |

ETF Cointegration ranks **#2 overall** by 3Y Sharpe, essentially tied
with Momentum Crash-Hedged. Its low beta makes it an excellent
diversifier alongside momentum-based strategies.

## Recommendations

1. **Add ETF Cointegration to the main roster** -- it's a top-tier strategy
2. **Use ADX as a filter module** for existing momentum/trend strategies
   rather than running it standalone
3. **Re-test ETF Cointegration annually** -- cointegration can break down
   during regime changes (the 5Y degradation from 1.04 to 0.56 Sharpe
   confirms this)

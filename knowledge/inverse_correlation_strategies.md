# Inverse Correlation Strategies — Findings

## Strategies Implemented & Backtested (3Y 2022-2024)

### Winners
| Strategy | Return | Sharpe | Inverse Signal |
|----------|--------|--------|----------------|
| ai_token_economy | +216.6% | 1.43 | NVDA momentum → AI infra stack |
| oil_down_tech_up | +55.0% | 1.11 | XLE drops → tech rotation |
| job_loss_tech_boom | +56.3% | 0.61 | Staffing (MAN/RHI/ADP) weak → SaaS/AI boom |
| vix_spike_buyback | +16.4% | 0.21 | VIX spikes → cash-rich buyback machines |

### Losers
| Strategy | Return | Sharpe | Why It Failed |
|----------|--------|--------|---------------|
| dollar_weak_em_strong | +8.9% | -0.11 | USD was STRONG 2022-2024, signal rarely triggered |
| bonds_down_banks_up | +4.0% | -0.14 | Banks underperformed despite rate hikes (SVB crisis) |
| retail_crash_ecommerce | -19.9% | -0.28 | E-commerce crashed harder than retail in 2022 |
| crypto_crash_tradfi | +4.0% | -0.17 | TradFi didn't benefit from crypto crash |

## Key Insight
The STRONGEST inverse correlations are:
1. **Employment → Automation** (staffing weak = tech strong)
2. **Energy → Tech** (oil crash = lower costs + rotation)
3. **AI leader → AI supply chain** (NVDA momentum = infrastructure boom)

The WEAKEST (or regime-dependent):
1. Dollar-EM correlation broke in 2022-2023 (both dropped)
2. Crypto-TradFi rotation didn't materialize (both risk assets)
3. Retail-ecommerce correlation flipped (both crashed in 2022)

## Lesson
Inverse correlations work best when the mechanism is STRUCTURAL (jobs→automation),
not just portfolio rotation (crypto→tradfi). The ADP/staffing signal is particularly
powerful because it measures a real economic variable (employment) not just price action.

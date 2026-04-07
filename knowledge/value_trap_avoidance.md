# Value Trap Avoidance Research

## Piotroski F-Score (0-9) — Buy >= 7, Avoid <= 3
- Profitability (4 pts): positive ROA, positive CFO, ROA improvement, accruals
- Leverage (3 pts): decreased debt, improved current ratio, no dilution
- Efficiency (2 pts): improved gross margin, improved asset turnover
- F >= 7 among low P/B stocks: +7.5% annual outperformance

## Altman Z-Score — Safe > 2.99, Distress < 1.81
- Z = 1.2*(WC/TA) + 1.4*(RE/TA) + 3.3*(EBIT/TA) + 0.6*(MktCap/TL) + 1.0*(Rev/TA)
- Z < 1.81 = bankruptcy risk = value trap

## Combined Filter
Reject value candidates if: F-Score <= 3 OR Z-Score < 1.81 OR negative FCF 2+ quarters

## Note: Can't implement without fundamental data beyond yfinance .info
Our current proxy: use SMA200 as quality filter (broken stocks below SMA200 * 0.85 excluded)

## Momentum Research Key Findings
- 12-1 momentum still works but weakened in US large caps (crowding)
- Residual momentum (pure stock-specific) is more persistent, less crash-prone
- Cross-asset momentum works across stocks/bonds/commodities/currencies
- Managed momentum: scale by inverse realized vol (Barroso-Santa-Clara 2015)
- Our Momentum Crash-Hedged already implements vol-scaling = managed momentum
- Key signal: ret_12_2 = price[t-1] / price[t-12] - 1 (skip recent month)

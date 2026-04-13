# Research Queue — Strategies Pending Implementation

This file tracks strategies discovered by research agents that need to be:
1. Implemented in Python (BasePersona pattern)
2. Backtested on 3Y horizon
3. Added to strategy/winning/ or strategy/losing/
4. Updated in LEADERBOARD.md

**Any agent working on this repo should check this file first.**

## Status: 2026-04-13

### Implemented (need backtest + strategy files)
- [x] stat_arb_medallion (hedge_fund) — Renaissance-style stat arb with mean reversion
- [x] risk_parity (hedge_fund) — Bridgewater-style inverse-vol weighting
- [x] market_making_momentum (hedge_fund) — Citadel-style short-term momentum + vol
- [x] growth_concentration (hedge_fund) — Tiger Global high-conviction growth
- [x] activist_distressed (hedge_fund) — Elliott-style deep value + activist catalyst
- [x] fda_catalyst (news_event) — Biotech FDA approval/rejection plays
- [x] earnings_whisper (news_event) — Pre-earnings drift momentum
- [x] merger_arbitrage (news_event) — M&A announced deal spread capture
- [x] dividend_capture (news_event) — Ex-date dividend trading
- [x] yield_curve_inversion (recession) — Trade based on yield curve inversion/steepening via TLT/SHY ratio
- [x] consumer_credit_stress (recession) — Consumer credit deterioration signal
- [x] unemployment_momentum (recession) — Jobless claims trend-following

### Pending Implementation — User Ticker Requests (2026-04-08)
User requested strategies incorporating these tickers. Group into thematic strategies:

- [x] **Utility & Infrastructure Income**: SO, D, DUK, PPL, EQIX, PG, COST, TMUS, SCHW — `utility_infra_income` (theme)
- [x] **Japan Industrial ADR**: MKTAY (Makita), construction ADRs, NMR (Nomura), SMFG, MUFG — `japan_industrial_finance` (theme)
- [x] **Global Bond & Fixed Income**: FBND, SPBO, SCHI, VWOB, VTEB — `bond_fixed_income` (portfolio)
- [x] **News & Media Monopoly**: NYT, CMCSA (Comcast), WBD — `news_media_monopoly` (unconventional)
- [x] **Defense Prime Contractors**: LMT, NOC, RTX, BA, BAESY — `defense_prime_contractors` (theme)
- [x] **Global Consumer Brands**: UL, MKC, DE, NVO, PG, COST, EL — `global_consumer_staples` (theme)
- [x] **Emerging Market Value**: NU, VNM, EWY, EWS, EPI — `emerging_market_etf_value` (theme)
- [x] **Pharma & Biotech Pipeline**: RHHBY (Roche), MRK, BAYRY (Bayer), NVS, UBS — `global_pharma_pipeline` (theme)
- [x] **Singapore Heritage Consumer**: H02.SI (Haw Par/Tiger Balm), F34.SI (Wilmar), Y92.SI (Thai Bev) — combined with Singapore REITs into `singapore_alpha` (theme)
- [x] **Product Tanker Shipping**: TRMD (TORM), FRO (Frontline), STNG (Scorpio), INSW (International Seaways) — `product_tanker_shipping` (crisis_commodity)
- [x] **UK & European Banking Value**: NWG (NatWest), BARC (Barclays), HSBC, UBS, BNPQF, DB — `uk_european_banking` (theme)
- [x] **Retail Deep Value**: KSS (Kohl's), M (Macy's), JWN (Nordstrom), DDS (Dillard's), BURL — `retail_deep_value` (unconventional)
- [x] **Telecom Equipment & 5G**: ERIC (Ericsson), NOK (Nokia), QCOM, MRVL, KEYS — `telecom_equipment_5g` (theme)
- [x] **Gig Economy & SaaS Disruptors**: UPWK (Upwork), FVRR (Fiverr), TOST (Toast), RKLB (Rocket Lab) — `gig_economy_saas` (theme)
- [x] **Cannabis & Alt Consumer**: TLRY (Tilray), CGC (Canopy), MJ ETF — `cannabis_alt_consumer` (unconventional)
- [x] **Cloud & Cybersecurity Value**: NET, DDOG, SNOW, CRWD, CRM, ZS, S (SentinelOne) — `cloud_cyber_value` (theme)
- [x] **Airlines & Travel Recovery**: DAL, LUV, UAL, C6L.SI (SIA), RKUNY (ANA), TCOM, BKNG — `global_airlines_travel` (theme)
- [x] **Korean Chaebols & Fintech**: CPNG (Coupang), SKM (SK Telecom), SSNLF (Samsung), KB (Kookmin), SHG (Shinhan), PKX (POSCO) — `korean_chaebols` (theme)
- [x] **Fallen Blue Chip Value**: PFE (Pfizer), INTC (Intel), WMT (Walmart), SBUX (Starbucks), NKE (Nike), CSCO (Cisco), VZ (Verizon), TGT (Target) — `fallen_blue_chip_value` (unconventional)
- [x] **Rideshare & Mobility**: UBER, LYFT, GRAB, DASH (DoorDash) — `rideshare_mobility` (theme)
- [x] **High-Yield REIT & BDC Income**: O (Realty Income), AGNC, ARMOUR (ARR), ORC (Orchid), NLY (Annaly), DX (Dynex), PSEC (Prospect), MAIN (Main Street), HTGC (Horizon), STAG, ARCC (Ares Capital), EFC (Ellington), PNNT (PennantPark) — combined with Real Estate Tech into `high_yield_reit_bdc` (portfolio)
- [x] **Singapore REITs**: A17U.SI (CapitaLand Ascendas), N2IU.SI (Mapletree Pan Asia), C38U.SI (CapitaLand Integrated), ME8U.SI, AJBU.SI (Keppel DC REIT) — combined with Singapore Heritage into `singapore_alpha` (theme)
- [x] **Real Estate Tech**: Z (Zillow), RDFN (Redfin) — combined with High-Yield REIT into `high_yield_reit_bdc` (portfolio)
- [x] **Dividend Aristocrat Blue Chips**: MO (Altria), PM (Philip Morris), MMM (3M), UPS, FDX, F (Ford), KHC (Kraft), JNJ, ENB (Enbridge), ABBV, XOM (Exxon), SCHD (Schwab Dividend ETF) — `dividend_aristocrat_blue_chips` (portfolio)

### Completed 2026-04-08 batch 2
- [x] rare_earth_minerals (crisis_commodity) — -1.8% ret, LOSE
- [x] water_scarcity (crisis_commodity) — -19.8% ret, LOSE
- [x] shipping_freight_cycle (crisis_commodity) — +24.2% ret, WIN
- [x] entropy_regime (math) — +10.7% ret, LOSE (negative Sharpe)
- [x] cointegration_pairs (math) — -6.9% ret, LOSE
- [x] optimal_stopping (math) — -34.0% ret, LOSE

## Process for Converting Research to Strategies

1. Check this file for pending items
2. Implement in the appropriate `*_strategies.py` file using BasePersona pattern
3. Add key to module's registry dict (e.g., RECESSION_STRATEGIES)
4. Run: `python3 -c "import ast; ast.parse(open('file.py').read())"` to verify syntax
5. Run: `python3 sync_package.py` to sync to package
6. Backtest: use Backtester with start='2022-01-01', end='2024-12-31'
7. Save: use save_strategy_recommendation() for strategy/winning/ or strategy/losing/
8. Update LEADERBOARD.md
9. Commit and push
10. Mark item as [x] in this file

# NVIDIA Supply Chain Research: Non-Megacap Peripheral Suppliers

Research date: 2026-04-08

## Thesis

Everyone buys NVDA directly. But NVIDIA's GPUs require an entire ecosystem of
smaller, less-followed companies for packaging, testing, materials, cooling, and
power delivery. These companies have significant NVIDIA/AI revenue exposure but
trade at a fraction of NVDA's multiple. Supply chain multiplier effect: a 20%
increase in NVDA GPU shipments can mean 30-50% revenue growth for a substrate or
packaging company with 40%+ exposure.

## Selected Universe (14 tickers, all US-tradable)

### Chip Packaging & OSAT

| Ticker | Company | Mkt Cap | Role in NVDA Supply Chain | AI/Semi Exposure |
|--------|---------|---------|--------------------------|-----------------|
| AMKR | Amkor Technology | ~$12B | #2 OSAT globally. Advanced packaging (CoWoS, fan-out) for NVDA GPUs. Building $1.6B Vietnam facility for multi-chip HBM packages. Expanding CoWoS assembly in Arizona. | ~35-40% AI/HPC |
| ASX | ASE Technology (ADR) | ~$20B | #1 OSAT globally (35%+ share). CoWoS packaging partner for TSMC/NVDA. Packaging and testing services. | ~30% advanced packaging |
| KLIC | Kulicke & Soffa | ~$3.4B | Wire bonding, wedge bonding, and advanced packaging equipment. Critical for semiconductor assembly. Small cap, pure-play packaging equipment. | ~25-30% advanced packaging |

### Semiconductor Test Equipment

| Ticker | Company | Mkt Cap | Role in NVDA Supply Chain | AI/Semi Exposure |
|--------|---------|---------|--------------------------|-----------------|
| COHU | Cohu | ~$1.7B | Automated test equipment (ATE) for chip testing. Smallest pure-play ATE company. Growing AI/HPC test exposure. | ~20-25% AI chip testing |
| FORM | FormFactor | ~$7.2B | Probe cards for wafer-level testing. Critical for HBM memory testing and advanced node verification. Shares returned 67% in 3 months. | ~40% AI/HBM testing |
| ONTO | Onto Innovation | ~$10.7B | Process control and lithography for advanced packaging. Inspection/metrology for CoWoS and 3D packaging. | ~35% advanced packaging |

### Semiconductor Chemicals & Materials

| Ticker | Company | Mkt Cap | Role in NVDA Supply Chain | AI/Semi Exposure |
|--------|---------|---------|--------------------------|-----------------|
| ENTG | Entegris | ~$17.7B | Filters, chemicals, CMP slurries, specialty materials for all leading-edge fabs. Every TSMC wafer that makes NVDA chips touches Entegris materials. | ~50-60% leading-edge semi |

### Power Delivery

| Ticker | Company | Mkt Cap | Role in NVDA Supply Chain | AI/Semi Exposure |
|--------|---------|---------|--------------------------|-----------------|
| MPWR | Monolithic Power Systems | ~$30B | DC-DC power management ICs for AI GPU server racks. Direct supplier to NVDA ecosystem for voltage regulators. | ~40% AI/data center |

### PCB & Substrate

| Ticker | Company | Mkt Cap | Role in NVDA Supply Chain | AI/Semi Exposure |
|--------|---------|---------|--------------------------|-----------------|
| TTMI | TTM Technologies | ~$5B | High-layer-count PCBs for AI servers and networking. Supplies boards for GPU server chassis. | ~25-30% AI/data center |

### Data Center Cooling

| Ticker | Company | Mkt Cap | Role in NVDA Supply Chain | AI/Semi Exposure |
|--------|---------|---------|--------------------------|-----------------|
| MOD | Modine Manufacturing | ~$12B | Liquid cooling for data centers. DC sales grew 119% to $644M in FY2025. Projecting 50-70% annual growth. Hyperscale customer wins. | ~45% data center cooling |
| NVT | nVent Electric | ~$18B | High-density power distribution units (IPDUs) for AI workloads. Direct NVIDIA collaboration. 117K sq ft facility expansion for NVDA racks. | ~30% data center power/cooling |

### Rare Earth & Strategic Materials

| Ticker | Company | Mkt Cap | Role in NVDA Supply Chain | AI/Semi Exposure |
|--------|---------|---------|--------------------------|-----------------|
| MP | MP Materials | ~$9B | Rare earth magnets (NdPr) for motors in cooling fans, robotic arms, data center infrastructure. $400M US government strategic partnership. | ~15-20% electronics/AI adjacent |

### ABF Substrate (Japan ADRs)

| Ticker | Company | Mkt Cap | Role in NVDA Supply Chain | AI/Semi Exposure |
|--------|---------|---------|--------------------------|-----------------|
| AJINY | Ajinomoto (ADR) | ~$28B | Invented ABF (Ajinomoto Build-up Film). Monopoly supplier of the insulating film used in ALL high-end GPU substrates. Every NVDA GPU package uses ABF. | ~15-20% (ABF is small % of total Ajinomoto revenue, but monopoly) |
| IBIDY | Ibiden (ADR) | ~$14B | #2 ABF substrate manufacturer (19% market share). Supplies IC substrates directly for GPU packaging. | ~60-70% semiconductor substrates |

## Companies Researched But NOT Included

| Company | Ticker | Reason Excluded |
|---------|--------|----------------|
| Teradyne | TER | ATE leader but $18B+ market cap, well-covered by analysts |
| Advantest | ATEYY | ATE monopolist but $130B market cap -- megacap, not "hidden" |
| Vertiv | VRT | Data center cooling leader but $66B market cap -- too large |
| Schneider Electric | SBGSY | $120B+ market cap -- megacap |
| ON Semiconductor | ON | $25B+ market cap, well-covered |
| Vishay Intertechnology | VSH | ~$3B but low AI-specific exposure (<10%) |
| Micron | MU | HBM maker but $100B+ market cap -- megacap |
| Linde / Air Products | LIN/APD | Industrial gas for fabs but mega cap, low semi-specific exposure |
| Lasertec | LSRCY | EUV photomask inspection monopoly but low US ADR liquidity |
| Shinko Electric | SHEGF | ABF substrate but very low US OTC liquidity |
| Resonac Holdings | RSKCF | NCF/underfill materials but low US OTC liquidity |
| Lynas Rare Earths | LYSCF | Rare earth but Australian, low US liquidity |

## Key Supply Chain Dynamics (2025-2026)

1. **CoWoS bottleneck**: Demand 670K wafers in 2025, targeting 1M in 2026. TSMC has 95%+ utilization. NVDA securing 70%+ of TSMC's advanced packaging capacity.

2. **HBM memory fully booked**: SK Hynix and Micron HBM capacity sold out through 2026. HBM stacking requires advanced packaging equipment from KLIC, test from FORM/COHU.

3. **ABF substrate shortage**: $4.9B market in 2025, growing to $9.5B by 2033 (10.6% CAGR). Ajinomoto has monopoly on ABF film. Top 5 substrate makers (Unimicron, Ibiden, AT&S, Nan Ya PCB, Shinko) control 74% of market.

4. **Data center cooling inflection**: AI racks draw 40-100kW (vs 10-15kW traditional). Liquid cooling now required. Modine DC sales +119% YoY. nVent has direct NVDA partnership.

5. **Advanced packaging market**: Expected to exceed 51% of total semiconductor packaging for first time in 2025. Growing at 10.6% CAGR to $78.6B by 2028.

## Strategy Signal

- **Primary**: NVDA momentum (SMA50 > SMA200 = supply chain demand is strong)
- **Secondary**: Individual stock trend + RSI + MACD + volume
- **Edge case**: When NVDA is strong but a supply chain name is oversold (RSI < 35), that is highest conviction (lagging supply chain = buying opportunity)
- **Risk management**: Hard exit below SMA200 * 0.80 or RSI > 80

## Implementation

Strategy class: `NvidiaSupplyChain` in `theme_strategies.py`
Registry key: `nvidia_supply_chain`

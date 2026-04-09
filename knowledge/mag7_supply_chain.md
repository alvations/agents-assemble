# Magnificent 7 Supply Chain Deep Map & Domino-Collapse Analysis

Research date: 2026-04-08

## Executive Summary

The Magnificent 7 (AAPL, MSFT, GOOGL, AMZN, META, NVDA, TSLA) share a deeply
interconnected supply chain with critical single points of failure concentrated
in a handful of Japanese, Korean, and Taiwanese companies. A disruption at any
of these chokepoints cascades through ALL Mag7 simultaneously.

The most dangerous domino: **TSMC + ASML + Ajinomoto ABF** -- if any one of
these fails, every Mag7 company is impacted within weeks.

---

## Per-Company Supply Chain Maps

### 1. APPLE (AAPL)

**Critical single-supplier dependencies:**
- **TSMC** -- Sole manufacturer of A-series / M-series chips (3nm/2nm). No alternative fab exists at these nodes
- **Samsung Display** -- ~120M iPhone OLED panels in 2026. After BOE production crisis (late 2025), Samsung has exclusive iPhone Fold supply until 2029-2030
- **Corning (GLW)** -- Exclusive Gorilla Glass supplier since 2007. $2.5B deal for all iPhone/Watch cover glass
- **Broadcom (AVGO)** -- Wi-Fi, Bluetooth, NFC chips across entire Apple ecosystem
- **Sony (SONY)** -- CMOS image sensors (dominant supplier for iPhone cameras)

**Hidden material dependencies:**
- Ajinomoto ABF substrate film (chip packaging)
- Shin-Etsu (SHECY) silicon wafers for TSMC fabs
- Murata (MRAAY) -- up to 1000 MLCCs per iPhone
- Rare earth magnets (China controls 60%+ of processing)

**Customer concentration (downstream dominos):**
- Foxconn/Hon Hai -- ~70% of iPhone assembly
- App Store ecosystem -- millions of developers depend on Apple platform

### 2. MICROSOFT (MSFT)

**Critical single-supplier dependencies:**
- **TSMC** -- Fabricates custom Azure Maia AI chips, Cobalt ARM CPUs (via 3nm process)
- **NVIDIA** -- Primary GPU supplier for Azure AI cloud infrastructure
- **Marvell (MRVL) / Broadcom (AVGO)** -- Custom ASIC design partners for Azure chips (MSFT negotiating switch from Marvell to Broadcom)
- **ARM Holdings (ARM)** -- Architecture license for custom Cobalt CPUs

**Hidden material dependencies:**
- Ajinomoto ABF, Shin-Etsu wafers, Entegris chemicals (through TSMC)
- Transformer equipment (2-4 year lead times) for data center power

**Customer concentration (downstream):**
- Enterprise world runs on Azure/Office 365/Teams
- CoreWeave and other AI startups depend on Azure capacity

### 3. ALPHABET/GOOGLE (GOOGL)

**Critical single-supplier dependencies:**
- **Broadcom (AVGO)** -- TPU co-design partner through 2031 deal. Broadcom converts Google's architecture into manufacturable ASICs
- **TSMC** -- Fabricates TPUs and all Google custom silicon
- **Samsung** -- DRAM/NAND for data centers
- **SK Hynix (HXSCF)** -- HBM memory for AI accelerators

**Hidden material dependencies:**
- Ajinomoto ABF for TPU packaging
- Corning (GLW) fiber optic for data center interconnects
- MediaTek partnership (2026+) to reduce Broadcom dependence

**Customer concentration (downstream):**
- Anthropic ($3.5 GW TPU capacity from 2027)
- YouTube/Search advertising -- 80%+ of Google revenue
- Cloud customers (SAP, Deutsche Bank, etc.)

### 4. AMAZON (AMZN)

**Critical single-supplier dependencies:**
- **TSMC** -- Fabricates Graviton CPUs, Trainium AI chips, Inferentia chips (all designed by Annapurna Labs)
- **NVIDIA** -- GPU supplier for AWS AI instances (EC2 P5, etc.)
- **ARM Holdings (ARM)** -- Architecture for Graviton processors
- **Intel** -- Legacy x86 instances still substantial

**Hidden material dependencies:**
- Ajinomoto ABF, Shin-Etsu wafers (through TSMC)
- Corning fiber optic (data center interconnects)
- Transformer/switchgear supply chain (power infrastructure)

**Customer concentration (downstream):**
- AWS is the backbone for Netflix, Airbnb, thousands of startups
- 33% of global cloud market

### 5. META (META)

**Critical single-supplier dependencies:**
- **NVIDIA** -- Primary GPU supplier for AI training (Llama models, recommendation engines)
- **TSMC** -- Fabricates Meta's custom MTIA AI chips
- **Corning (GLW)** -- $6B fiber optic deal through 2030 for AI data centers
- **Power utilities** -- Entergy Louisiana deal; $60-65B capex in 2025 mostly AI infrastructure

**Hidden material dependencies:**
- Transformers (2-4 year lead times, critical bottleneck)
- SK Hynix/Samsung HBM memory for GPU clusters
- Ajinomoto ABF, Entegris chemicals (through TSMC/NVIDIA)

**Customer concentration (downstream):**
- 3.9B monthly active users across apps
- Advertising ecosystem (97% of revenue)

### 6. NVIDIA (NVDA)

**Critical single-supplier dependencies:**
- **TSMC** -- Sole manufacturer of H100/H200/B100/B200 GPUs. CoWoS packaging ONLY in Taiwan
- **SK Hynix (HXSCF)** -- 62% of HBM market, NVIDIA's primary HBM supplier (sold out through 2026)
- **Samsung** -- Secondary HBM supplier (17% share, catching up with HBM4)
- **Micron (MU)** -- Third HBM supplier (21% share)

**Hidden material dependencies:**
- **Ajinomoto (AJINY)** -- 95%+ monopoly on ABF substrate film for GPU packaging
- **Ibiden (IBIDY)** -- Only manufacturer supplying AI server IC substrates to NVIDIA
- **Amkor (AMKR) / ASE (ASX)** -- Advanced packaging (OSAT) partners
- **Entegris (ENTG)** -- Ultra-pure chemicals, CMP slurries for TSMC fabs
- **Monolithic Power (MPWR)** -- DC-DC power for AI GPU server racks

**Customer concentration (downstream):**
- CoreWeave: 67% revenue from Microsoft, massive NVIDIA-financed GPU debt ($29.8B total debt)
- NVIDIA vendor financing exposure ~$110B, ~2.8x larger than what sank Lucent
- Hyperscalers (MSFT, GOOGL, AMZN, META) collectively 60%+ of revenue

### 7. TESLA (TSLA)

**Critical single-supplier dependencies:**
- **CATL** -- #1 global battery maker, supplies LFP cells for Model 3/Y (China)
- **Panasonic** -- NCA battery cells for US-made vehicles, long-term partner
- **LG Energy Solution** -- Third battery supplier
- **TSMC** -- Fabricates Tesla FSD (Full Self-Driving) chips
- **Samsung SDI** -- Battery cells for certain models

**Hidden material dependencies:**
- **Cobalt** -- 75% from DRC (politically volatile). Tesla shifting to LFP to reduce exposure
- **Lithium** -- Albemarle, SQM, Ganfeng Lithium (concentrated in Chile/Australia/China)
- **Rare earth magnets** -- China controls 60%+ processing. Ford shut plants for 3 weeks in 2025 due to China export ban
- **NVIDIA** -- Supplies chips for Dojo training supercomputer

**Customer concentration (downstream):**
- Consumer demand (no single customer concentration)
- But EV market increasingly competitive (BYD, legacy auto)

---

## Shared Dependencies (Domino Risk Matrix)

### Tier 1: Universal Single Points of Failure (ALL Mag7)

| Supplier | What They Supply | Mag7 Exposed | Monopoly Level |
|----------|-----------------|--------------|----------------|
| **TSMC (TSM)** | Advanced chip fabrication (3nm/2nm) | ALL 7 | ~71% foundry market, 90%+ cutting-edge |
| **ASML (ASML)** | EUV lithography machines | ALL 7 (via TSMC) | 100% monopoly on EUV |
| **Ajinomoto (AJINY)** | ABF substrate film | ALL 7 (via chip packaging) | 95%+ monopoly |
| **Shin-Etsu (SHECY)** | Silicon wafers | ALL 7 (via all fabs) | ~30% share (#1), 90% with SUMCO |
| **Murata (MRAAY)** | MLCCs (capacitors) | ALL 7 (every device) | ~40% global MLCC share (#1) |

### Tier 2: Critical Oligopoly Chokepoints (5+ Mag7)

| Supplier | What They Supply | Mag7 Exposed | Market Position |
|----------|-----------------|--------------|-----------------|
| **SK Hynix (HXSCF)** | HBM memory | NVDA, GOOGL, MSFT, META, AMZN | 62% HBM share |
| **Corning (GLW)** | Gorilla Glass + fiber optic | AAPL, META, GOOGL, AMZN, MSFT | Dominant in both |
| **Entegris (ENTG)** | Ultra-pure chemicals/filters | ALL 7 (via fabs) | Critical for all advanced nodes |
| **ARM (ARM)** | CPU architecture | AAPL, AMZN, MSFT, GOOGL, NVDA | Dominant mobile/server |
| **Broadcom (AVGO)** | Custom ASICs, networking | GOOGL, MSFT, AAPL, META | #1 custom AI chip partner |

### Tier 3: Hidden Critical Suppliers (4+ Mag7)

| Supplier | What They Supply | Mag7 Exposed | Why Hidden |
|----------|-----------------|--------------|------------|
| **Ibiden (IBIDY)** | ABF substrates for NVIDIA | NVDA + all GPU users | Japanese B2B, low coverage |
| **Lasertec (LSRCY)** | EUV mask inspection | ALL 7 (via TSMC) | 100% monopoly, only company |
| **Disco Corp (DSCOY)** | Wafer dicing/grinding | ALL 7 (via all fabs) | 70%+ market share |
| **Tokyo Electron (TOELY)** | Etch/deposition equipment | ALL 7 (via fabs) | #1 in Asia, 43% revenue from China |
| **Hamamatsu Photonics** | Photon detectors, EUV sources | ALL 7 (via ASML) | Deep in ASML supply chain |
| **SUMCO (SUOPY)** | Silicon wafers (#2) | ALL 7 (via all fabs) | 30% share, duopoly with Shin-Etsu |

### Tier 4: Power & Infrastructure (Emerging Bottleneck)

| Supplier Category | Constraint | Mag7 Exposed |
|-------------------|-----------|--------------|
| **Transformer OEMs** | 2-4 year lead times | MSFT, GOOGL, AMZN, META |
| **Power utilities** | Grid capacity insufficient | All hyperscalers |
| **Electrical components (China)** | Switchgear, batteries | All data center builders |

---

## Domino Collapse Scenarios

### Scenario 1: TSMC Disruption (Taiwan earthquake/conflict)
- **Immediate impact**: ALL Mag7 lose chip supply within 4-8 weeks
- **No alternative**: Samsung/Intel fabs 2+ generations behind at advanced nodes
- **Cascading**: NVDA GPUs stop shipping -> AI training halts -> cloud revenue drops -> hyperscaler capex crashes
- **Duration**: 12-24 months minimum to partially recover

### Scenario 2: HBM Memory Crisis (SK Hynix disruption)
- **Immediate impact**: NVIDIA GPU production halts (62% of HBM from SK Hynix)
- **Secondary**: Samsung/Micron cannot absorb demand for 6-12 months
- **Cascading**: AI training capacity freezes -> hyperscaler revenue guidance cut -> Mag7 broad selloff

### Scenario 3: ABF Substrate Shortage (Ajinomoto/Ibiden)
- **Immediate impact**: ALL advanced chip packaging stops
- **Hidden risk**: Market doesn't understand this dependency until it breaks
- **Cascading**: GPU, CPU, mobile chip production all halt simultaneously

### Scenario 4: Rare Earth Export Ban (China retaliation)
- **Immediate impact**: Magnets, capacitor materials, battery materials restricted
- **Real precedent**: Ford shut plants for 3 weeks in 2025 from China export controls
- **Cascading**: AAPL (iPhones), TSLA (motors/batteries), all electronics manufacturing

### Scenario 5: Power Grid Failure
- **Half of planned US data center builds delayed/canceled** due to power constraints
- **Cascading**: AI capex guidance cut -> NVDA demand miss -> semiconductor selloff

---

## Trading Strategy Implications

### Strategy 1: Hidden Suppliers (Long)
The "picks and shovels" companies that ALL Mag7 depend on but are under-followed:
- AJINY, SHECY, MRAAY, ENTG, LSRCY, DSCOY, TOELY, IBIDY, SUOPY
- Plus: GLW, AMKR, ASX, MPWR, HXSCF
- Thesis: If Mag7 spend $320B+ on AI capex, these suppliers capture guaranteed revenue

### Strategy 2: Domino Hedge (Defensive Rotation)
Monitor supply chain stress signals:
- If TSMC, ASML, or key supply chain names break below SMA200 with volume spike -> early warning
- Rotate from Mag7/QQQ exposure into defensive (XLP, XLU, GLD, TLT)
- Supply chain breaks BEFORE consumer-facing companies react

---

## Key Ticker Reference

| Company | Ticker | Exchange | Role |
|---------|--------|----------|------|
| TSMC | TSM | NYSE | Chip fabrication monopoly |
| ASML | ASML | NASDAQ | EUV lithography monopoly |
| Ajinomoto | AJINY | OTC | ABF substrate monopoly (95%+) |
| Shin-Etsu Chemical | SHECY | OTC | #1 silicon wafer maker |
| SUMCO | SUOPY | OTC | #2 silicon wafer maker |
| Murata Manufacturing | MRAAY | OTC | #1 MLCC capacitor maker |
| Ibiden | IBIDY | OTC | ABF substrate for NVIDIA |
| Lasertec | LSRCY | OTC | EUV mask inspection monopoly |
| Disco Corp | DSCOY | OTC | Wafer dicing 70%+ share |
| Tokyo Electron | TOELY | OTC | Etch/deposition equipment |
| Hamamatsu Photonics | HPHTF | OTC | Photon detectors for EUV |
| Entegris | ENTG | NASDAQ | Ultra-pure chemicals for fabs |
| Corning | GLW | NYSE | Glass + fiber optic |
| SK Hynix | HXSCF | OTC | #1 HBM memory (62%) |
| Amkor Technology | AMKR | NASDAQ | Advanced packaging OSAT |
| ASE Technology | ASX | NYSE | #1 OSAT globally |
| Monolithic Power | MPWR | NASDAQ | Power delivery for AI GPUs |
| Broadcom | AVGO | NASDAQ | Custom ASICs, networking |
| ARM Holdings | ARM | NASDAQ | CPU architecture IP |

Sources:
- TSMC 71% foundry market share (Q3 2025)
- Ajinomoto 95%+ ABF monopoly (Palliser Capital activist report)
- SK Hynix 62% HBM share, sold out through 2026
- Lasertec 100% EUV mask inspection (sub-5nm)
- NVIDIA vendor financing ~$110B, 2.8x Lucent ratio
- CoreWeave $29.8B total debt, 67% revenue from Microsoft
- Meta $6B Corning fiber deal, $60-65B AI capex 2025
- Half of US data center builds delayed/canceled due to power
- Samsung Display exclusive iPhone Fold supply until 2029-2030
- Disco Corp 70%+ wafer dicing market share
- China rare earth export ban caused Ford plant shutdowns (2025)

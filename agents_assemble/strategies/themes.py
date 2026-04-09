"""Theme-based trading strategies for agents-assemble.

These personas trade based on macro themes and megatrends rather than
individual investor philosophies. Each theme targets a specific sector
thesis with its own universe and timing signals.

Themes:
    1. AIRevolution              — AI/ML infrastructure and applications
    2. CleanEnergy               — Renewables, EVs, batteries, grid
    3. DefenseAerospace          — Defense contractors, space, cybersecurity
    4. BiotechBreakout           — Biotech/pharma innovation and FDA catalysts
    5. ChinaTechRebound          — China tech ADRs recovery play
    6. LatAmGrowth               — Latin American growth (fintech, commodities)
    7. InfrastructureBoom        — Infrastructure spending (bridges, 5G, data centers)
    8. SmallCapValue             — Small cap deep value (IWM universe)
    9. CryptoEcosystem           — Crypto-adjacent public companies
    10. AgingPopulation          — Healthcare, senior living, pharma for aging demographics
    11. GLP1Obesity              — GLP-1 / weight loss drug megatrend
    12. RoboticsAutonomous       — Humanoid robots + autonomous vehicles
    + SemiconductorValue         — Semi picks-and-shovels at value
    + SubscriptionMonopoly       — Sticky subscription moats
    + ContrastivePairs           — Long value side of hype sectors
    + GlobalFinancialInfra       — Financial infrastructure monopolies
    + ReshoringIndustrial        — US reshoring beneficiaries
    + WaterMonopoly              — Water utility monopolies
    + RegulatedData              — Regulated data monopolies
    + ChinaADRDeepValue          — China ADR deep value
    + CloudCyberValue            — Cloud & cybersecurity value entries
    + GlobalAirlinesTravel       — Airlines & travel recovery / momentum
    + UtilityInfraIncome         — Utility & infrastructure income
    + JapanIndustrialFinance     — Japan industrial & finance reform
    + DefensePrimeContractors    — Defense prime contractors (NATO spend)
    + GlobalConsumerStaples      — Global consumer staples income
    + EmergingMarketETFValue     — Emerging market ETF value
    + GlobalPharmaPipeline       — Global pharma pipeline value
    + SingaporeAlpha             — Singapore heritage consumer + REITs
    + UKEuropeanBanking          — UK & European bank deep value
    + TelecomEquipment5G         — 5G equipment & infrastructure
    + GigEconomySaaSDisruptors   — Gig economy + SaaS growth disruptors
    + KoreanChaebols             — Korean chaebol conglomerates + fintech
    + RideshareMobility          — Rideshare & mobility platforms
    + NvidiaSupplyChain          — NVIDIA peripheral supply chain (non-megacap)
"""

from __future__ import annotations


def _is_missing(v):
    """Check if value is None or NaN."""
    return v is None or v != v

from agents_assemble.strategies.generic import BasePersona, PersonaConfig


# ---------------------------------------------------------------------------
# 1. AI Revolution
# ---------------------------------------------------------------------------
class AIRevolution(BasePersona):
    """AI/ML megatrend strategy.

    Thesis: AI is a generational shift. Companies building AI infrastructure
    (GPUs, cloud, data centers) and AI applications will outperform.

    Signals: Buy on trend alignment (SMA50 > SMA200), momentum.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="AI Revolution",
            description="AI megatrend: GPUs, cloud, data centers, AI applications",
            risk_tolerance=0.8,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NVDA", "AMD", "AVGO", "MRVL", "ARM",  # AI chips
                "MSFT", "GOOGL", "AMZN", "META",  # AI cloud/apps
                "PLTR", "AI", "PATH", "SNOW",  # AI software
                "SMH", "SOXX",  # Semiconductor ETFs
                "SMCI", "DELL", "HPE",  # AI servers
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]

            if any(v is None for v in [sma50, sma200, rsi]):
                continue

            # Thesis broken
            if price < sma200 * 0.90:
                weights[sym] = 0.0
                continue
            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0
            if price > sma50 > sma200:
                score += 3.0  # Full trend alignment
            elif price > sma50:
                score += 1.5
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if 40 < rsi < 75:
                score += 0.5

            if score > 2:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 2. Clean Energy
# ---------------------------------------------------------------------------
class CleanEnergy(BasePersona):
    """Clean energy / green transition strategy.

    Thesis: Global energy transition to renewables creates multi-decade growth.
    Buy solar, wind, EV, battery, and grid companies.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Clean Energy Transition",
            description="Renewables, EVs, batteries: buy the green transition",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "ENPH", "SEDG", "FSLR", "RUN",  # Solar
                "TSLA", "RIVN", "LCID", "NIO", "LI", "XPEV",  # EVs
                "ALB", "LTHM", "SQM",  # Lithium/batteries
                "NEE", "AES", "BEP",  # Utilities/renewables
                "ICLN", "TAN", "QCLN",  # Clean energy ETFs
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if any(v is None for v in [sma50, rsi]):
                continue

            # Broken trend: >15% below SMA200 (clean energy is volatile)
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            # Buy dips in uptrend or recovery from oversold
            if sma200 is not None and price > sma200 and rsi < 55:
                score = 2.0
                if sma50 > 0 and abs(price - sma50) / sma50 < 0.05:
                    score += 1.0  # Near SMA50 support
                scored.append((sym, score))
            elif rsi < 30:
                scored.append((sym, 1.5))  # Oversold bounce
            elif rsi > 80:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 3. Defense & Aerospace
# ---------------------------------------------------------------------------
class DefenseAerospace(BasePersona):
    """Defense, aerospace, and cybersecurity strategy.

    Thesis: Geopolitical tensions drive sustained defense spending.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Defense & Aerospace",
            description="Defense spending boom: contractors, space, cybersecurity",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "LMT", "RTX", "NOC", "GD", "BA", "LHX",  # Defense
                "PLTR", "CRWD", "PANW", "ZS", "FTNT",  # Cybersecurity
                "RKLB", "ASTS", "LUNR",  # Space
                "ITA", "XAR",  # Defense ETFs
                "HII", "TDG", "HWM",  # Niche defense
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            if sma200 is None:
                continue

            # Defense stocks tend to be stable — buy near SMA200
            # Broken trend: >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            if discount > -0.10 and (rsi is None or rsi < 65):
                score = max(discount + 0.10, 0.01) + 0.3
                candidates.append((sym, score))
            elif rsi is not None and rsi > 80:
                weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 4. Biotech Breakout
# ---------------------------------------------------------------------------
class BiotechBreakout(BasePersona):
    """Biotech innovation and catalyst strategy.

    Thesis: Biotech has binary outcomes — buy diversified basket,
    overweight momentum leaders, cut losers fast.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Biotech Breakout",
            description="Biotech innovation: diversified basket, momentum leaders, cut losers",
            risk_tolerance=0.8,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                "MRNA", "REGN", "VRTX", "GILD", "BIIB",  # Large biotech
                "SGEN", "ALNY", "IONS", "BMRN",  # Mid biotech
                "XBI", "IBB", "BBH",  # Biotech ETFs
                "ISRG", "DXCM", "HIMS",  # MedTech
                "LLY", "ABBV", "MRK",  # Big pharma with biotech pipelines
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "vol_20"], date)
            sma50, sma200 = inds["sma_50"], inds["sma_200"]
            rsi, vol = inds["rsi_14"], inds["vol_20"]
            if any(v is None for v in [sma50, rsi]):
                continue

            # Cut losers fast (biotech-specific)
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            score = 0.0
            if price > sma50:
                score += 1.5
            if sma200 is not None and sma50 > sma200:
                score += 1.0
            if 35 < rsi < 70:
                score += 0.5
            # Prefer lower-vol names (less binary risk)
            if vol is not None and vol < 0.03:
                score += 0.5

            if score > 1.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 5. China Tech Rebound
# ---------------------------------------------------------------------------
class ChinaTechRebound(BasePersona):
    """China tech ADR recovery strategy.

    Thesis: China tech crackdown created deep value. Recovery plays in
    BABA, JD, PDD etc when regulation stabilizes.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="China Tech Rebound",
            description="China tech ADR recovery: deep value after regulatory crackdown",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "BABA", "JD", "PDD", "BIDU", "NIO", "XPEV", "LI",
                "TME", "BILI", "NTES", "IQ", "WB",
                "KWEB", "MCHI", "FXI",  # China ETFs
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if any(v is None for v in [sma50, rsi]):
                continue

            # Recovery signal: price crossing above SMA50
            if price > sma50 and rsi < 60:
                score = 2.0
                if sma200 is not None and price > sma200:
                    score += 1.5  # Full recovery
                scored.append((sym, score))
            elif rsi < 25:
                scored.append((sym, 1.5))  # Deep oversold bounce
            elif rsi > 75:
                weights[sym] = 0.0  # Take profits

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 6. LatAm Growth
# ---------------------------------------------------------------------------
class LatAmGrowth(BasePersona):
    """Latin American growth strategy.

    Thesis: LatAm fintech, e-commerce, and commodity exporters benefit
    from structural digitization and commodity supercycle.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="LatAm Growth",
            description="Latin American fintech, e-commerce, commodities growth",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "MELI", "NU", "STNE", "PAGS",  # Fintech/e-commerce
                "VALE", "PBR", "ITUB", "BSBR",  # Brazilian blue chips
                "SQM", "GGAL",  # Chile/Argentina
                "EWZ", "EWW", "ILF",  # LatAm ETFs
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if any(v is None for v in [sma50, rsi]):
                continue

            # Broken trend: >15% below SMA200 (LatAm stocks can freefall)
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            if price > sma50 and rsi < 65:
                score = 1.5
                if sma200 is not None and price > sma200:
                    score += 1.0
                scored.append((sym, score))
            elif rsi < 30:
                scored.append((sym, 1.0))
            elif rsi > 75:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 7. Infrastructure Boom
# ---------------------------------------------------------------------------
class InfrastructureBoom(BasePersona):
    """Infrastructure spending megatrend.

    Thesis: IIJA + CHIPS Act + global infra spending creates multi-year
    tailwind for construction, 5G, data centers.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Infrastructure Boom",
            description="Infrastructure spending: construction, 5G, data centers, utilities",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "CAT", "DE", "VMC", "MLM",  # Construction/materials
                "AMT", "CCI", "EQIX", "DLR",  # Towers/data centers
                "T", "VZ", "TMUS",  # Telecom/5G
                "NEE", "DUK", "SO",  # Utilities
                "PAVE", "IFRA",  # Infrastructure ETFs
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            if sma200 is None:
                continue

            # Broken trend: >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            if rsi is not None and rsi > 70:
                weights[sym] = 0.0
            elif discount > -0.10:
                score = max(discount + 0.10, 0.01) + 0.3
                if rsi is not None and rsi < 40:
                    score += 0.2
                candidates.append((sym, score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 8. Small Cap Deep Value
# ---------------------------------------------------------------------------
class SmallCapValue(BasePersona):
    """Small cap deep value strategy.

    Thesis: Small caps are inefficiently priced. Buy deeply oversold
    small caps with volume confirmation for mean-reversion.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Small Cap Deep Value",
            description="Small cap inefficiency: buy deeply oversold with volume spikes",
            risk_tolerance=0.7,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                "SMCI", "CELH", "CAVA", "DUOL", "RELY", "CWAN",
                "HUBS", "SAIA", "RCL", "BURL", "DECK", "LULU",
                "EXAS", "FTNT", "MTDR", "CEIX",
                "IWM", "IWO", "SCHA",  # Small cap ETFs
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["bb_lower", "rsi_14", "Volume", "volume_sma_20"], date)
            bb_lower, rsi = inds["bb_lower"], inds["rsi_14"]
            volume, vol_avg = inds["Volume"], inds["volume_sma_20"]
            if rsi is None:
                continue

            # Deep value: oversold + volume spike
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if rsi < 30 and vol_ratio > 1.5:
                score = (30 - rsi) / 30 * 3 + min(vol_ratio, 3.0)
                scored.append((sym, score))
            elif bb_lower is not None and price < bb_lower and rsi < 35 and vol_ratio > 0.5:
                score = 2.0
                scored.append((sym, score))
            elif rsi > 80:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 9. Crypto Ecosystem
# ---------------------------------------------------------------------------
class CryptoEcosystem(BasePersona):
    """Crypto-adjacent public companies strategy.

    Thesis: Crypto adoption creates value for miners, exchanges,
    and companies with BTC on balance sheet.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Crypto Ecosystem",
            description="Crypto-adjacent: miners, exchanges, BTC treasury companies",
            risk_tolerance=0.9,
            max_position_size=0.20,
            max_positions=6,
            rebalance_frequency="daily",
            universe=universe or [
                "COIN", "MARA", "RIOT", "CLSK",  # Mining/exchange
                "MSTR", "HUT",  # BTC treasury
                "SQ", "PYPL",  # Payment + crypto
                "BITO", "IBIT",  # Bitcoin ETFs
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_20", "sma_50", "rsi_14", "Volume", "volume_sma_20"], date)
            sma20, sma50, rsi = inds["sma_20"], inds["sma_50"], inds["rsi_14"]
            volume, vol_avg = inds["Volume"], inds["volume_sma_20"]
            if any(v is None for v in [sma20, rsi]):
                continue

            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1

            # Crypto is momentum-driven — ride breakouts
            if price > sma20 and rsi < 75 and vol_ratio > 1.2:
                score = 2.0 + min(vol_ratio, 5.0)
                if sma50 is not None and price > sma50:
                    score += 1.0
                scored.append((sym, score))
            elif rsi > 85:
                weights[sym] = 0.0
            elif rsi < 20 and vol_ratio > 2:
                scored.append((sym, 3.0))  # Capitulation buy

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            total_score = sum(s for _, s in top)
            cap = self.config.max_position_size
            for sym, score in top:
                weights[sym] = min((score / total_score) * 0.90, cap)
            # Iteratively redistribute clipped excess until fully allocated
            for _ in range(10):
                total_w = sum(weights[sym] for sym, _ in top)
                if total_w >= 0.899 or total_w <= 0:
                    break
                uncapped = [(sym, s) for sym, s in top if weights[sym] < cap - 1e-9]
                if not uncapped:
                    break
                uncapped_w = sum(weights[sym] for sym, _ in uncapped)
                if uncapped_w <= 0:
                    break
                surplus = 0.90 - total_w
                for sym, _ in uncapped:
                    weights[sym] = min(weights[sym] + surplus * weights[sym] / uncapped_w, cap)
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 10. Aging Population
# ---------------------------------------------------------------------------
class AgingPopulation(BasePersona):
    """Aging population demographic megatrend.

    Thesis: Global aging drives demand for healthcare, senior living,
    pharmaceuticals, and medical devices.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Aging Population",
            description="Demographic megatrend: healthcare, pharma, senior care",
            risk_tolerance=0.3,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "UNH", "HUM", "CI", "ELV",  # Health insurance
                "JNJ", "PFE", "MRK", "LLY", "ABBV",  # Big pharma
                "ISRG", "SYK", "MDT", "ABT",  # Medical devices
                "XLV", "VHT",  # Healthcare ETFs
                "WELL", "VTR",  # Senior housing REITs
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            if sma200 is None:
                continue

            # Broken trend: >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            # Defensive: buy near or below SMA200
            if rsi is not None and rsi > 70:
                weights[sym] = 0.0
            elif discount > -0.10:
                score = max(discount + 0.10, 0.01) + 0.3
                if rsi is not None and rsi < 40:
                    score += 0.1
                candidates.append((sym, score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 11. GLP-1 / Obesity Revolution
# ---------------------------------------------------------------------------
class GLP1Obesity(BasePersona):
    """GLP-1 / weight loss drug megatrend.

    2026: $73-87B market, LLY past $1T. Oral pills coming.
    30M Americans on GLP-1 by 2030.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="GLP-1 / Obesity Revolution",
            description="Weight loss drug megatrend: $73-87B market, LLY/NVO leaders",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "LLY", "NVO", "AMGN", "VKTX",
                "PFE", "ABBV", "JNJ", "MRK",
                "HIMS", "PLNT",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if any(v is None for v in [sma50, rsi]):
                continue
            if sma200 is not None and price < sma200 * 0.90:
                weights[sym] = 0.0
                continue
            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if 35 < rsi < 75:
                score += 0.5
            if score >= 2.0:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 12. Robotics & Autonomous Vehicles
# ---------------------------------------------------------------------------
class RoboticsAutonomous(BasePersona):
    """Robotics and autonomous vehicles megatrend.

    CES 2026: humanoid robots commercially viable, Level 4 autonomy.
    Global robotics market > $200B by decade end.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Robotics & Autonomous",
            description="Humanoid robots + autonomous vehicles: $200B market by 2030",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "ISRG", "NVDA", "INTC", "TER", "CGNX",
                "GOOGL", "TSLA", "GM",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]
            if any(v is None for v in [sma50, rsi]):
                continue
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue
            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if 40 < rsi < 75:
                score += 0.5
            if score >= 2.5:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# 13. Semiconductor Value (not AI hype — supply chain deep value)
# ---------------------------------------------------------------------------
class SemiconductorValue(BasePersona):
    """Buy the semiconductor PICKS AND SHOVELS at value prices, not AI hype.

    Everyone chases NVDA. Smart money buys the companies NVDA depends on:
    TSMC (makes the chips), ASML (makes the machines that make the chips),
    memory companies at cyclical lows (WDC, MU), and equipment companies (LRCX, KLAC).

    Edge: Semi cycles are predictable — buy at low RSI when inventory clears.
    Memory is a commodity cycle: oversupply → crash → consolidation → undersupply → boom.
    Equipment companies have 80%+ recurring service revenue nobody prices in.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Semiconductor Value (Picks & Shovels)",
            description="Semi supply chain at value prices: TSMC, ASML, memory at cyclical lows, equipment recurring revenue",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "TSM",    # TSMC — makes 90% of advanced chips
                "ASML",   # ASML — monopoly on EUV lithography
                "AVGO",   # Broadcom — custom AI chips + VMware
                "SSNLF",  # Samsung (OTC) — memory + foundry
                "WDC",    # Western Digital — NAND flash, cyclical low
                "MU",     # Micron — DRAM/NAND, HBM for AI
                "LRCX",   # Lam Research — etch equipment
                "KLAC",   # KLA Corp — inspection equipment
                "AMAT",   # Applied Materials — deposition equipment
                "CRSR",   # Corsair Gaming — peripherals, undervalued
                "ON",     # ON Semi — auto/industrial chips
                "MRVL",   # Marvell — data center networking
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # VALUE: buy below SMA200 (cyclical low)
            if price < sma200 * 0.90:
                score += 3.0  # Deep cyclical discount
            elif price < sma200:
                score += 1.5
            # Also ride uptrends (secular growth)
            elif price > sma200 and sma50 is not None and sma50 > sma200:
                score += 1.5
            # RSI value zone
            if rsi < 35:
                score += 2.5  # Max fear in semis = best entry
            elif rsi < 50:
                score += 1.0
            # MACD reversal
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if score >= 2.5:
                scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 14. Subscription Monopoly (Recurring Revenue Moats)
# ---------------------------------------------------------------------------
class SubscriptionMonopoly(BasePersona):
    """Companies with sticky subscriptions that customers never cancel.

    CRM (Salesforce): once your sales team is on it, switching cost is enormous.
    ADP: every company's payroll — 40M employees processed, never switches.
    NFLX: 260M subscribers, content moat deepening.
    SPOT: 600M users, podcasts + music + audiobooks ecosystem.
    ADBE: every designer/marketer on Creative Cloud.

    Edge: Subscription = predictable revenue + negative churn (upselling).
    These trade at high multiples but actually DESERVE it because cash flow
    visibility is 95%+. Buy dips — they always recover.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Subscription Monopoly (Recurring Revenue)",
            description="Sticky subscriptions nobody cancels: CRM, ADP, NFLX, SPOT — predictable cash flow machines",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "CRM",    # Salesforce — enterprise CRM monopoly
                "ADP",    # Automatic Data Processing — payroll monopoly
                "NFLX",   # Netflix — content + scale moat
                "SPOT",   # Spotify — audio ecosystem
                "ADBE",   # Adobe — Creative Cloud lock-in
                "INTU",   # Intuit — TurboTax + QuickBooks (tax monopoly)
                "HRB",    # H&R Block — tax prep for masses
                "VEEV",   # Veeva Systems — pharma CRM monopoly
                "HUBS",   # HubSpot — SMB marketing automation
                "ZM",     # Zoom — enterprise video (sticky post-COVID)
                "PANW",   # Palo Alto — cybersecurity subscription pivot
                "FTNT",   # Fortinet — network security subscriptions
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "vol_20"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Uptrend = growing subscribers
            if price > sma200:
                score += 2.0
            if sma50 is not None and price > sma50:
                score += 1.0
            # Buy pullbacks (subscriptions = reliable recovery)
            if 30 < rsi < 45 and price > sma200:
                score += 2.5
            elif 45 <= rsi < 60:
                score += 1.0
            # Low vol preferred (stable subscription base)
            vol = inds["vol_20"]
            if vol is not None and not _is_missing(vol) and vol < 0.020:
                score += 0.5
            if score >= 3:
                scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 15. Contrastive Pairs (Long Value vs Short Hype within same sector)
# ---------------------------------------------------------------------------
class ContrastivePairs(BasePersona):
    """Long the cheap, short the expensive within the same theme.

    Within every hot sector, there's a value stock and a hype stock.
    This strategy goes long the undervalued one and avoids/shorts the overvalued one.
    Since we can't short in our backtester, we just concentrate in the VALUE side
    of each pair and avoid the hype side entirely.

    Pairs: WDC (value) vs NVDA (hype), HRB (value) vs SNOW (hype),
    ADP (value) vs WDAY (hype), NFLX (value) vs ROKU (hype).

    Edge: Mean reversion within sectors. The value side catches up.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Contrastive Pairs (Value Side of Hype Sectors)",
            description="Long the cheap stock in every hot sector: WDC not NVDA, HRB not SNOW, ADP not WDAY",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Semi value (not NVDA)
                "WDC", "MU", "ON",
                # Tax/payroll value (not cloud hype)
                "HRB", "ADP", "PAYX",
                # Streaming value (not money-burners)
                "NFLX", "WBD",
                # Enterprise value (not overpriced SaaS)
                "ORCL", "IBM",
                # Fintech value (not speculative)
                "FISV", "FIS",
                # Hardware value (not meme)
                "HPQ", "DELL",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # VALUE signal: below SMA200 or recently recovered
            if price < sma200:
                score += 2.0  # In value zone
                if rsi < 40:
                    score += 2.0  # Deep value
            # Momentum recovery signal
            if price > sma200:
                score += 1.0
            if sma50 is not None and price > sma50 > sma200:
                score += 1.5  # Breaking out of value zone
            # MACD reversal from below
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if 40 < rsi < 65:
                score += 0.5
            if score >= 2.5:
                scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 16. Global Financial Infrastructure
# ---------------------------------------------------------------------------
class GlobalFinancialInfra(BasePersona):
    """Payment rails + global banks + trading houses = backbone of world finance.

    Combines US payment monopolies (V, MA, AXP), US mega-banks (JPM, GS, BK),
    Japanese trading houses (Marubeni/MRBEY, Mitsubishi/MITSY),
    and Singapore banks (D05.SI, U11.SI, O39.SI).

    Edge: Cross-geography diversification with correlated upside (global growth)
    but uncorrelated downside (different regulatory/economic cycles).
    Singapore banks yield 5%+ with pristine asset quality. Japanese sogo shoshas
    trade at book value with 15%+ ROE. US payments grow with global digitization.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Global Financial Infrastructure",
            description="Payment rails + mega-banks + Japanese trading houses + Singapore banks — backbone of world finance",
            risk_tolerance=0.5,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                # US payment monopolies
                "V", "MA", "AXP",
                # US mega-banks
                "JPM", "GS", "BK",
                # Capital One (consumer credit cycle play)
                "COF",
                # Japanese sogo shoshas (Buffett-approved)
                "MRBEY",  # Marubeni
                "MITSY",  # Mitsubishi Corp
                "ITOCY",  # Itochu
                # Singapore banks (5%+ dividend, AAA country)
                "D05.SI",  # DBS
                "U11.SI",  # UOB
                "O39.SI",  # OCBC
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Uptrend
            if price > sma200:
                score += 2.0
            if sma50 is not None and price > sma50:
                score += 1.0
            # Buy dips in financials (they recover with rate cycles)
            if 30 < rsi < 50 and price > sma200:
                score += 2.0
            elif 50 <= rsi < 65:
                score += 0.5
            # MACD momentum
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            if score >= 3:
                scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 17. Reshoring Industrial Renaissance — 2% implemented, 98% orders pending
# ---------------------------------------------------------------------------
class ReshoringIndustrial(BasePersona):
    """US reshoring + CHIPS Act + IRA = multi-decade industrial capex.

    Only 2% of manufacturers have FULLY reshored — 98% of orders pending.
    ETN picks-and-shovels for electrification, NUE domestic steel at premium,
    CAT 19% earnings growth, URI rents equipment to build every factory.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Reshoring Industrial Renaissance",
            description="CHIPS Act + IRA + reshoring: 2% implemented, 98% of orders still coming. ETN, CAT, NUE, URI.",
            risk_tolerance=0.5, max_position_size=0.10, max_positions=12, rebalance_frequency="weekly",
            universe=universe or ["ETN", "EMR", "ROK", "AME", "GE", "CAT", "NUE", "STLD", "RS", "TT", "GNRC", "VMC", "MLM", "URI"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi): continue
            price = prices[sym]
            score = 0.0
            if price > sma200: score += 2.0
            if sma50 is not None and sma50 > sma200: score += 1.5
            if 40 < rsi < 55: score += 1.5
            macd, ms = inds["macd"], inds["macd_signal"]
            if macd is not None and ms is not None and macd > ms: score += 1.0
            if score >= 3: scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        if scored:
            total = sum(s for _, s in scored[:self.config.max_positions])
            for sym, sc in scored[:self.config.max_positions]:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 18. Water Infrastructure Monopoly — $45B mandated EPA spending
# ---------------------------------------------------------------------------
class WaterMonopoly(BasePersona):
    """Regulated water monopolies with zero competition. You can't choose your water provider.

    EPA lead pipe mandate = $45B MUST be spent, utilities MUST be made whole via rate hikes.
    AWK 10% below fair value. WTRG unanimous Strong Buy +25% upside.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Water Infrastructure Monopoly",
            description="Regulated water monopolies: $45B EPA mandate, AWK below fair value, 8-9% rate base growth guaranteed",
            risk_tolerance=0.3, max_position_size=0.15, max_positions=8, rebalance_frequency="monthly",
            universe=universe or ["AWK", "WTRG", "WTR", "SJW", "XYL", "WTS", "FELE", "PNR", "ECL"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi): continue
            price = prices[sym]
            score = 1.0  # Always some allocation (utility income)
            if price > sma200: score += 2.0
            sma50 = inds["sma_50"]
            if sma50 is not None and price > sma50: score += 0.5
            if 30 < rsi < 45: score += 2.0
            elif rsi < 30: score += 2.5  # Rare panic = gift
            elif 45 <= rsi < 60: score += 0.5
            if score >= 3: scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        if scored:
            total = sum(s for _, s in scored[:self.config.max_positions])
            for sym, sc in scored[:self.config.max_positions]:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 19. Regulated Data Infrastructure — SPGI 31.9% DCF upside
# ---------------------------------------------------------------------------
class RegulatedData(BasePersona):
    """Data monopolies REQUIRED by regulation. 85-95% subscription, 100%+ NRR.

    VRSK: sole insurance actuarial data provider. SPGI/MCO: required by Basel III.
    MSCI indexes determine $15T+ in fund allocations. Arms dealers of finance.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Regulated Data Infrastructure",
            description="VRSK/SPGI/MSCI: regulatory-required data monopolies, 85-95% subscription, 100%+ NRR",
            risk_tolerance=0.4, max_position_size=0.12, max_positions=10, rebalance_frequency="monthly",
            universe=universe or ["VRSK", "FDS", "MSCI", "SPGI", "MCO", "TRI", "NDAQ", "MORN", "DNB", "ENV"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "vol_20"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi): continue
            price = prices[sym]
            score = 0.0
            if price > sma200: score += 2.0
            if sma50 is not None and sma50 > sma200: score += 1.5
            if 35 < rsi < 50 and price > sma200: score += 2.0
            elif 50 <= rsi < 65: score += 1.0
            vol = inds["vol_20"]
            if vol is not None and not _is_missing(vol) and vol < 0.015: score += 1.0
            if score >= 4: scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        if scored:
            total = sum(s for _, s in scored[:self.config.max_positions])
            for sym, sc in scored[:self.config.max_positions]:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 20. China ADR Deep Value — JD/PDD 9x P/E
# ---------------------------------------------------------------------------
class ChinaADRDeepValue(BasePersona):
    """Chinese ADRs at lowest valuations in history. Delisting fear resolved.

    JD 9x P/E, PDD 9.4x forward. BABA dominant e-commerce + cloud below intrinsic.
    Government pivoted to stimulus. Geopolitical fear = persistent mispricing.
    MAX POSITION SIZE SMALL due to tail risk.
    """
    def __init__(self, universe=None):
        config = PersonaConfig(
            name="China ADR Deep Value",
            description="JD/PDD 9x P/E, BABA below intrinsic — delisting resolved, stimulus pivot, geopolitical discount",
            risk_tolerance=0.6, max_position_size=0.08, max_positions=10, rebalance_frequency="weekly",
            universe=universe or ["BABA", "JD", "PDD", "BIDU", "NIO", "XPEV", "LI", "VIPS", "BILI", "TME", "ZTO", "YUMC", "TCOM", "MNSO"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices: continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "volume_sma_20"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi): continue
            price = prices[sym]
            score = 0.0
            if price < sma200 * 0.85: score += 3.0
            elif price < sma200: score += 1.5
            if rsi < 35: score += 2.0
            elif rsi < 45: score += 1.0
            macd, ms = inds["macd"], inds["macd_signal"]
            if macd is not None and ms is not None and macd > ms: score += 1.5
            vol_sma = inds["volume_sma_20"]
            if vol_sma is not None and not _is_missing(vol_sma) and sym in data:
                try:
                    cv = data[sym].loc[:date, "Volume"].iloc[-1]
                    if cv > vol_sma * 2.0: score += 1.5
                except Exception: pass
            if score >= 4: scored.append((sym, score))
        scored.sort(key=lambda x: -x[1])
        if scored:
            total = sum(s for _, s in scored[:self.config.max_positions])
            for sym, sc in scored[:self.config.max_positions]:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# Cloud & Cybersecurity Value
# ---------------------------------------------------------------------------
class CloudCyberValue(BasePersona):
    """Cloud and cybersecurity value strategy.

    Thesis: Cloud infrastructure and cybersecurity are non-discretionary spend.
    Companies like Cloudflare, Datadog, CrowdStrike have durable moats via
    network effects and switching costs. Buy on pullbacks to SMA200 with
    MACD reversal for value entries in secular growth names.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Cloud & Cybersecurity Value",
            description="Cloud/cyber non-discretionary spend: buy dips in Cloudflare, Datadog, CrowdStrike, Palo Alto",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NET", "DDOG", "SNOW", "CRWD",  # Cloud/observability
                "PANW", "FTNT", "ZS", "S",  # Cybersecurity
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "vol_20"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]

            if any(_is_missing(v) for v in [sma200, rsi]):
                continue

            # Broken trend: >15% below SMA200 (growth names can gap down)
            if price < sma200 * 0.85:
                weights[sym] = 0.0
                continue
            if rsi > 80:
                weights[sym] = 0.0
                continue

            score = 0.0
            # Value entry: below SMA200 with low RSI
            if price < sma200 and rsi < 45:
                score += 2.5  # Below long-term avg = value zone
            # Uptrend confirmation
            if sma50 is not None and price > sma50 > sma200:
                score += 2.0
            elif sma50 is not None and price > sma50:
                score += 1.0
            # MACD reversal (key signal for value entry timing)
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5
            # Not overbought
            if 30 < rsi < 65:
                score += 0.5

            if score >= 2.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Global Airlines & Travel
# ---------------------------------------------------------------------------
class GlobalAirlinesTravel(BasePersona):
    """Global airlines and travel recovery / momentum strategy.

    Thesis: Post-pandemic travel demand is structural. Airlines are cyclical
    but international travel (BKNG, TCOM) has durable pricing power.
    Buy on pullbacks using SMA200 support with golden cross confirmation.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Global Airlines & Travel",
            description="Airlines and OTAs: DAL, UAL, BKNG, ABNB — post-pandemic travel demand",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "DAL", "LUV", "UAL", "JBLU",  # US airlines
                "BKNG", "ABNB", "EXPE",  # OTAs / travel platforms
                "TCOM",  # Trip.com (China/Asia travel)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "bb_lower"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]
            bb_lower = inds["bb_lower"]

            if any(_is_missing(v) for v in [sma50, rsi]):
                continue

            # Airlines are cyclical — cut at >20% below SMA200
            if sma200 is not None and price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            if rsi > 78:
                weights[sym] = 0.0
                continue

            score = 0.0
            # Golden cross: strong momentum signal for cyclicals
            if sma200 is not None and sma50 > sma200 and price > sma50:
                score += 3.0
            elif price > sma50:
                score += 1.5
            # Pullback entry near Bollinger lower band
            if bb_lower is not None and not _is_missing(bb_lower) and price < bb_lower * 1.03:
                score += 1.5
            # MACD confirmation
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            # RSI sweet spot
            if 30 < rsi < 60:
                score += 0.5

            if score >= 2.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Utility & Infrastructure Income
# ---------------------------------------------------------------------------
class UtilityInfraIncome(BasePersona):
    """Utility and infrastructure income strategy.

    Thesis: Regulated utilities, data center REITs, and defensive consumer
    names provide steady income with inflation-linked pricing.
    Always maintain some allocation; buy more on dips below SMA200.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Utility & Infrastructure Income",
            description="Utilities, data centers, telecom: steady income, buy dips for yield",
            risk_tolerance=0.2,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "SO", "D", "DUK", "PPL",  # Regulated utilities
                "EQIX",  # Data center REIT
                "TMUS",  # T-Mobile (telecom)
                "COST",  # Costco (defensive consumer)
                "SCHW",  # Schwab (financial infrastructure)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14", "sma_50"], date)
            sma200, rsi, sma50 = inds["sma_200"], inds["rsi_14"], inds["sma_50"]
            if _is_missing(sma200):
                continue

            # Income: always some allocation (base weight)
            base_weight = 0.08
            # Buy more on dips below SMA200
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            if discount > 0.05:
                # 5%+ below SMA200 = accumulate aggressively
                score = 2.0 + discount * 5
                if rsi is not None and rsi < 35:
                    score += 1.0
                candidates.append((sym, score, 0.12))
            elif discount > -0.05:
                # Near SMA200 = normal income allocation
                score = 1.5
                if rsi is not None and rsi < 45:
                    score += 0.5
                candidates.append((sym, score, base_weight))
            elif discount > -0.15:
                # Up to 15% above SMA200 = reduced but still hold for income
                candidates.append((sym, 1.0, 0.06))
            # More than 15% above SMA200 and RSI overbought = trim
            elif rsi is not None and rsi > 75:
                weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        for sym, _, wt in top:
            weights[sym] = min(wt, self.config.max_position_size)
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Japan Industrial & Finance
# ---------------------------------------------------------------------------
class JapanIndustrialFinance(BasePersona):
    """Japan industrial and financial sector strategy.

    Thesis: Japan's corporate governance reform (TSE push for ROE > 8%)
    is unlocking value in keiretsu conglomerates and megabanks.
    Buy ADRs of quality Japanese industrials and financials on dips.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Japan Industrial & Finance",
            description="Japan governance reform: Toyota, Sony, Nomura, MUFG, trading houses",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "MKTAY", "NMR", "SMFG", "MUFG",  # Finance / industrial
                "ITOCY", "MITSY",  # Trading houses (Buffett favorites)
                "TM", "SONY",  # Consumer / auto
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]

            if any(_is_missing(v) for v in [sma200, rsi]):
                continue

            # Japan ADRs can be volatile — cut at >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue

            score = 0.0
            # Value entry: below SMA200 with low RSI (governance reform unlocks value)
            if price < sma200 and rsi < 45:
                score += 2.5
            # Uptrend = reform thesis working
            if sma50 is not None and price > sma50 > sma200:
                score += 2.0
            elif sma50 is not None and price > sma50:
                score += 1.0
            # MACD reversal
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            # Not overbought
            if 30 < rsi < 65:
                score += 0.5
            # Deep oversold = contrarian buy
            if rsi < 30:
                score += 1.5

            if score >= 2.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Defense Prime Contractors
# ---------------------------------------------------------------------------
class DefensePrimeContractors(BasePersona):
    """Defense prime contractors focused strategy.

    Thesis: NATO 2%+ GDP spending targets, geopolitical tensions, and
    long-duration defense contracts create predictable revenue streams.
    Primes have cost-plus contracts = guaranteed margins.
    Buy on value dips, hold for steady compounding.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Defense Prime Contractors",
            description="NATO spending boom: LMT, NOC, RTX, BAE, GD — cost-plus contracts = guaranteed margins",
            risk_tolerance=0.3,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "LMT", "NOC", "RTX", "BAESY",  # Top primes
                "GD", "HII", "LHX", "LDOS",  # Second tier primes
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14", "sma_50", "vol_20"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            sma50, vol = inds["sma_50"], inds["vol_20"]
            if _is_missing(sma200):
                continue

            # Defense primes are stable — cut only at >15% below SMA200
            if price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            score = 0.0

            # Value: buy near or below SMA200
            if discount > 0:
                score += 2.0 + discount * 5  # More discount = higher score
            elif discount > -0.10:
                score += 1.0

            # Low RSI = oversold (defense rarely stays oversold)
            if rsi is not None and rsi < 40:
                score += 1.5
            elif rsi is not None and rsi < 55:
                score += 0.5
            elif rsi is not None and rsi > 75:
                weights[sym] = 0.0
                continue

            # Low vol bonus (stable defense contractor = good)
            if vol is not None and not _is_missing(vol) and vol < 0.015:
                score += 0.5

            if score >= 1.5:
                candidates.append((sym, score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Global Consumer Staples
# ---------------------------------------------------------------------------
class GlobalConsumerStaples(BasePersona):
    """Global consumer staples strategy.

    Thesis: Global staples (Unilever, Nestle, P&G, KO) have pricing power
    across economic cycles. Buy for income and stability — always maintain
    some allocation, accumulate on dips.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Global Consumer Staples",
            description="Global pricing power: Unilever, Nestle, P&G, KO, Deere — income + stability",
            risk_tolerance=0.2,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "UL", "MKC", "DE", "NVO",  # International staples/health
                "PG", "KO", "NSRGY", "COST",  # US/global staples
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14", "sma_50"], date)
            sma200, rsi, sma50 = inds["sma_200"], inds["rsi_14"], inds["sma_50"]
            if _is_missing(sma200):
                continue

            # Income strategy: always hold some, buy more on dips
            base_weight = 0.08
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            if discount > 0.05:
                # >5% below SMA200: accumulate (staples always recover)
                wt = 0.13
                score = 2.5
                if rsi is not None and rsi < 35:
                    score += 1.0
                    wt = 0.15
                candidates.append((sym, score, wt))
            elif discount > -0.05:
                # Near SMA200: normal income allocation
                score = 1.5
                if rsi is not None and rsi < 45:
                    score += 0.5
                candidates.append((sym, score, base_weight))
            elif discount > -0.12:
                # Moderate uptrend: smaller allocation
                candidates.append((sym, 1.0, 0.06))
            else:
                # Extended above SMA200 + overbought: trim
                if rsi is not None and rsi > 75:
                    weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        for sym, _, wt in top:
            weights[sym] = min(wt, self.config.max_position_size)
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Emerging Market ETF Value
# ---------------------------------------------------------------------------
class EmergingMarketETFValue(BasePersona):
    """Emerging market ETF value strategy.

    Thesis: EM equities are structurally undervalued vs DM. Country ETFs
    (Vietnam, Korea, Singapore, India, Taiwan) provide diversified EM
    exposure. Buy when RSI is low and price is below SMA200 for value entries.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Emerging Market ETF Value",
            description="EM country ETFs at value prices: Vietnam, Korea, India, Taiwan, Singapore",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NU", "VNM", "EWY", "EWS",  # LatAm fintech, Vietnam, Korea, Singapore
                "EPI", "INDA", "EEM", "EWT",  # India, broad EM, Taiwan
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]

            if any(_is_missing(v) for v in [sma200, rsi]):
                continue

            # EM can freefall — cut at >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue
            if rsi > 78:
                weights[sym] = 0.0
                continue

            score = 0.0
            # Value: below SMA200 with low RSI
            if price < sma200 and rsi < 40:
                score += 3.0  # Deep EM value
            elif price < sma200 and rsi < 55:
                score += 2.0
            # Momentum recovery: above SMA200 with golden cross
            if sma50 is not None and price > sma50 > sma200:
                score += 2.0
            elif sma50 is not None and price > sma50:
                score += 1.0
            # MACD reversal = turning point
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0
            # Deep oversold bounce
            if rsi < 25:
                score += 1.5

            if score >= 2.0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Global Pharma Pipeline
# ---------------------------------------------------------------------------
class GlobalPharmaPipeline(BasePersona):
    """Global pharma pipeline strategy.

    Thesis: Big pharma companies with deep pipelines (Roche, AstraZeneca,
    Merck, GSK, Takeda) trade at value multiples despite having
    blockbuster drugs in late-stage trials. Buy on patent cliff fears.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Global Pharma Pipeline",
            description="Global pharma at value: Roche, AZN, MRK, GSK, TAK — deep pipelines, patent cliff fears",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "RHHBY", "MRK", "BAYRY", "NVS",  # Global pharma
                "AZN", "GSK", "TAK", "SNY",  # EU/Japan pharma
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "bb_lower"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            macd, macd_sig = inds["macd"], inds["macd_signal"]
            bb_lower = inds["bb_lower"]

            if any(_is_missing(v) for v in [sma200, rsi]):
                continue

            # Pharma can gap on FDA news — cut at >20% below SMA200
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue

            score = 0.0
            # Value: below SMA200 (patent cliff fears = opportunity)
            if price < sma200 * 0.90:
                score += 3.0
            elif price < sma200:
                score += 2.0
            # RSI oversold (pharma recovers when pipeline delivers)
            if rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0
            # MACD reversal = pipeline catalyst turning sentiment
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5
            # Bollinger lower = statistical extreme
            if bb_lower is not None and not _is_missing(bb_lower) and price < bb_lower * 1.02:
                score += 1.0
            # Also buy uptrending pharma (pipeline thesis confirmed)
            if sma50 is not None and price > sma50 > sma200:
                score += 1.5
            elif rsi > 75:
                weights[sym] = 0.0
                continue

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            weights.setdefault(sym, 0.0)
        return weights


# ---------------------------------------------------------------------------
# Singapore Alpha (Heritage Consumer + REITs combined)
# ---------------------------------------------------------------------------
class SingaporeAlpha(BasePersona):
    """Singapore equities: heritage consumer brands + REITs.

    Thesis: Singapore is a AAA-rated financial hub with world-class
    governance. Heritage consumer brands (Haw Par/Tiger Balm, Wilmar
    International, Thai Beverage) are cash-generative with regional
    distribution. Singapore REITs (S-REITs) offer 4-6% yields backed
    by prime commercial real estate in Asia's most transparent market.
    Combined, they offer income + growth from Singapore's structural
    advantages: rule of law, low tax, regional HQ status.

    Signal: Income-oriented — buy on dips below SMA200 for yield,
    hold in uptrend for total return.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Singapore Alpha",
            description="Singapore heritage consumer + REITs: AAA-rated income + growth",
            risk_tolerance=0.3,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                # Heritage consumer brands
                "H02.SI",   # Haw Par Corporation (Tiger Balm, healthcare)
                "F34.SI",   # Wilmar International (world's largest palm oil)
                "Y92.SI",   # Thai Beverage (Chang Beer, spirits, regional)
                # Singapore REITs (S-REITs)
                "A17U.SI",  # CapitaLand Ascendas REIT (industrial, data centers)
                "N2IU.SI",  # Mapletree Pan Asia Commercial Trust
                "C38U.SI",  # CapitaLand Integrated Commercial Trust
                "ME8U.SI",  # Mapletree Industrial Trust
                "AJBU.SI",  # Keppel DC REIT (data center REIT)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14"], date)
            sma200, sma50, rsi = inds["sma_200"], inds["sma_50"], inds["rsi_14"]
            if _is_missing(sma200):
                continue

            # Income strategy: always maintain allocation, buy dips
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            if discount > 0.05:
                # 5%+ below SMA200 = accumulate (yield pickup)
                score = 2.5 + discount * 5
                if rsi is not None and rsi < 35:
                    score += 1.0
                candidates.append((sym, score, 0.13))
            elif discount > -0.05:
                # Near SMA200 = normal income allocation
                score = 1.5
                if rsi is not None and rsi < 45:
                    score += 0.5
                candidates.append((sym, score, 0.10))
            elif discount > -0.15:
                # Moderately above SMA200 = hold for income
                candidates.append((sym, 1.0, 0.08))
            else:
                # >15% above SMA200 and RSI overbought = trim
                if rsi is not None and rsi > 75:
                    weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        for sym, _, wt in top:
            weights[sym] = min(wt, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# UK & European Banking Value
# ---------------------------------------------------------------------------
class UKEuropeanBanking(BasePersona):
    """UK and European banking value strategy.

    Thesis: European banks trade at 0.5-0.8x book value vs US banks
    at 1.2-1.5x despite improving ROE from higher rates. NatWest,
    Barclays, HSBC benefit from UK rate normalization. UBS (post-CS
    integration) is the world's largest wealth manager. BNP Paribas
    and Deutsche Bank are restructuring successfully. Dividend yields
    of 4-7% provide downside cushion.

    Signal: Deep value + MACD reversal. Buy when below book (SMA200
    proxy) with momentum confirmation. Sell on overbought.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="UK & European Banking Value",
            description="European bank deep value: 0.5-0.8x book, 4-7% yield, rate normalization",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NWG",    # NatWest Group (UK retail/commercial bank)
                "BARC",   # Barclays (UK investment + retail bank)
                "HSBC",   # HSBC Holdings (global, Asia-focused)
                "UBS",    # UBS Group (wealth management leader post-CS)
                "BNPQF",  # BNP Paribas (France, largest eurozone bank)
                "DB",     # Deutsche Bank (German restructuring play)
                "LYG",    # Lloyds Banking Group (UK mortgage leader)
                "ING",    # ING Group (Netherlands digital banking)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "bb_lower"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            bb_low = inds["bb_lower"]

            if _is_missing(sma200) or _is_missing(rsi):
                continue

            score = 0.0

            # Value: banks below SMA200 = below "book value" proxy
            if price < sma200 * 0.92:
                score += 3.0
            elif price < sma200:
                score += 1.5

            # RSI oversold = peak pessimism on European banks
            if rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0

            # MACD bullish crossover = turnaround signal
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5

            # Bollinger lower band = statistical extreme
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 1.0

            # Momentum confirmation for established uptrend
            if sma50 is not None and price > sma50 > sma200:
                score += 2.0
            elif sma50 is not None and price > sma50:
                score += 1.0

            # Overbought: take profits (banks are cyclical)
            if rsi > 75:
                weights[sym] = 0.0
                continue

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# Telecom Equipment & 5G
# ---------------------------------------------------------------------------
class TelecomEquipment5G(BasePersona):
    """Telecom equipment and 5G infrastructure strategy.

    Thesis: 5G capex cycle is multi-year ($1.7T global spend by 2030).
    Equipment vendors (Ericsson, Nokia) have oligopoly with Huawei
    restricted from Western markets. Qualcomm dominates 5G modems.
    Marvell provides custom silicon for 5G base stations. Keysight
    is the picks-and-shovels play (test equipment for every 5G rollout).
    Secular tailwind from AI requiring low-latency 5G edge networks.

    Signal: Momentum in equipment names. Buy uptrend + MACD bullish.
    Sell on overbought or trend breakdown.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Telecom Equipment & 5G",
            description="5G infrastructure: equipment oligopoly + semiconductor + test & measurement",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "ERIC",   # Ericsson (5G RAN leader, Huawei displacement)
                "NOK",    # Nokia (5G equipment + submarine cables)
                "QCOM",   # Qualcomm (5G modem monopoly + licensing)
                "MRVL",   # Marvell Technology (5G custom silicon)
                "KEYS",   # Keysight Technologies (5G test equipment)
                "ANET",   # Arista Networks (data center + 5G backhaul)
                "LITE",   # Lumentum (optical components for 5G)
                "VIAV",   # Viavi Solutions (network test + assurance)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal",
                 "Volume", "volume_sma_20"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if _is_missing(sma50) or _is_missing(rsi):
                continue

            # Exit: overbought (take profits)
            if rsi > 80:
                weights[sym] = 0.0
                continue

            # Exit: broken trend
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Uptrend: golden cross
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5

            # MACD bullish = capex cycle accelerating
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Volume confirmation (carrier orders = institutional buying)
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.3:
                score += 0.5

            # RSI healthy range
            if 35 < rsi < 70:
                score += 0.5

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# Gig Economy & SaaS Disruptors
# ---------------------------------------------------------------------------
class GigEconomySaaSDisruptors(BasePersona):
    """Gig economy platforms and SaaS disruptors strategy.

    Thesis: The gig economy is restructuring labor markets globally.
    Upwork and Fiverr connect 100M+ freelancers with enterprises.
    Toast is replacing legacy restaurant POS with cloud-native SaaS.
    Rocket Lab is disrupting SpaceX with small-launch dominance.
    These names trade at growth discounts after 2022 selloff but are
    approaching profitability / already profitable. Revenue growth
    25-50% with expanding margins = re-rating potential.

    Signal: Growth momentum. Buy on uptrend + volume. Sell overbought.
    Higher risk tolerance for these high-beta names.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Gig Economy & SaaS Disruptors",
            description="Gig platforms + SaaS disruptors: growth at reasonable price, high beta",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "UPWK",   # Upwork (freelance marketplace leader)
                "FVRR",   # Fiverr (gig economy marketplace)
                "TOST",   # Toast (restaurant SaaS / fintech)
                "RKLB",   # Rocket Lab (small-launch space disruptor)
                "DDOG",   # Datadog (observability SaaS)
                "NET",    # Cloudflare (edge computing / CDN)
                "CFLT",   # Confluent (data streaming SaaS)
                "HUBS",   # HubSpot (marketing SaaS)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal",
                 "Volume", "volume_sma_20"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if _is_missing(sma50) or _is_missing(rsi):
                continue

            # Exit: overbought growth names (take profits aggressively)
            if rsi > 78:
                weights[sym] = 0.0
                continue

            # Exit: structural breakdown
            if sma200 is not None and price < sma200 * 0.75:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Growth momentum: strong uptrend
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
                # Extra for breakout momentum
                if sma200 > 0:
                    pct_above = (price - sma200) / sma200
                    score += min(pct_above * 2, 1.5)
            elif price > sma50:
                score += 1.5

            # MACD bullish = earnings acceleration
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Volume surge (institutional accumulation)
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.5:
                score += 1.0
            elif vol_ratio > 1.2:
                score += 0.5

            # RSI in healthy momentum zone
            if 40 < rsi < 70:
                score += 0.5

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# Korean Chaebols & Fintech
# ---------------------------------------------------------------------------
class KoreanChaebols(BasePersona):
    """Korean chaebol conglomerates and fintech strategy.

    Thesis: Korean chaebols are global leaders trading at "Korea discount"
    (30-50% vs global peers) due to governance concerns. Reforms underway:
    Korea Value-Up Program (2024) follows Japan's TSE model. Coupang is
    Korea's Amazon (dominant e-commerce + logistics). Samsung (SSNLF) is
    the world's largest semiconductor manufacturer. KB Financial and
    Shinhan are top banks with 5%+ dividend yields. POSCO is the world's
    most efficient steelmaker + battery materials play.

    Signal: Value + momentum. Buy Korea discount names in uptrend.
    MACD reversal for turnaround signals.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Korean Chaebols & Fintech",
            description="Korea discount value: chaebols + fintech, governance reform catalyst",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "CPNG",   # Coupang (Korea's Amazon, dominant e-commerce)
                "SKM",    # SK Telecom (5G leader + AI investments)
                "SSNLF",  # Samsung Electronics (memory + foundry)
                "KB",     # KB Financial Group (Korea's largest bank)
                "SHG",    # Shinhan Financial (premium Korean bank)
                "PKX",    # POSCO Holdings (steel + battery materials)
                "LPL",    # LG Display (OLED technology leader)
                "EWY",    # iShares MSCI South Korea ETF (broad exposure)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal", "bb_lower"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            bb_low = inds["bb_lower"]

            if _is_missing(sma200) or _is_missing(rsi):
                continue

            score = 0.0

            # Korea discount: buy below SMA200 (value entry)
            if price < sma200 * 0.92:
                score += 2.5
            elif price < sma200:
                score += 1.5

            # Also buy momentum (governance reform re-rating)
            if sma50 is not None and price > sma50 > sma200:
                score += 2.5
            elif sma50 is not None and price > sma50:
                score += 1.0

            # RSI oversold = Korea sentiment trough
            if rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0

            # MACD bullish crossover = reform momentum building
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Bollinger lower band extreme
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 0.5

            # Overbought: take profits (Korea rallies are sharp but short)
            if rsi > 75:
                weights[sym] = 0.0
                continue

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# Rideshare & Mobility
# ---------------------------------------------------------------------------
class RideshareMobility(BasePersona):
    """Rideshare and mobility platform strategy.

    Thesis: Rideshare is a winner-take-most market. Uber is the global
    leader (150M+ monthly active users, 37 countries). Lyft is the #2
    US player approaching sustained profitability. Grab is the SE Asia
    super-app (rideshare + food + payments). DoorDash dominates US food
    delivery with 65%+ market share. All four have crossed the
    profitability inflection point with expanding margins. Network
    effects + autonomous driving optionality = long runway.

    Signal: Growth momentum. Buy on uptrend + volume confirmation.
    Sell on overbought or breakdown.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Rideshare & Mobility",
            description="Mobility platforms: rideshare + delivery, profitability inflection",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "UBER",   # Uber Technologies (global rideshare + delivery leader)
                "LYFT",   # Lyft (US #2 rideshare, margin expansion)
                "GRAB",   # Grab Holdings (SE Asia super-app)
                "DASH",   # DoorDash (US food delivery dominant)
                "ABNB",   # Airbnb (mobility-adjacent: travel platform)
                "TCOM",   # Trip.com (China travel + mobility)
                "BKNG",   # Booking Holdings (global travel platform)
                "CPRT",   # Copart (vehicle remarketing — mobility value chain)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(
                data, sym,
                ["sma_50", "sma_200", "rsi_14", "macd", "macd_signal",
                 "Volume", "volume_sma_20"],
                date,
            )
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            macd = inds["macd"]
            macd_sig = inds["macd_signal"]
            volume = inds["Volume"]
            vol_avg = inds["volume_sma_20"]

            if _is_missing(sma50) or _is_missing(rsi):
                continue

            # Exit: overbought
            if rsi > 78:
                weights[sym] = 0.0
                continue

            # Exit: broken below SMA200
            if sma200 is not None and price < sma200 * 0.80:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Growth momentum: strong uptrend
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5

            # MACD bullish = earnings momentum
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.0

            # Volume confirmation
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.3:
                score += 0.5

            # RSI healthy range
            if 35 < rsi < 70:
                score += 0.5

            # Dip-buy: oversold mobility names
            if rsi < 35 and sma200 is not None and price > sma200 * 0.90:
                score += 1.5

            if score >= 2.5:
                scored.append((sym, score))

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


THEME_STRATEGIES = {
    "ai_revolution": AIRevolution,
    "clean_energy": CleanEnergy,
    "defense_aerospace": DefenseAerospace,
    "biotech_breakout": BiotechBreakout,
    "china_tech_rebound": ChinaTechRebound,
    "latam_growth": LatAmGrowth,
    "infrastructure_boom": InfrastructureBoom,
    "small_cap_value": SmallCapValue,
    "crypto_ecosystem": CryptoEcosystem,
    "aging_population": AgingPopulation,
    "glp1_obesity": GLP1Obesity,
    "robotics_autonomous": RoboticsAutonomous,
    "semiconductor_value": SemiconductorValue,
    "subscription_monopoly": SubscriptionMonopoly,
    "contrastive_pairs": ContrastivePairs,
    "global_financial_infra": GlobalFinancialInfra,
    "reshoring_industrial": ReshoringIndustrial,
    "water_monopoly": WaterMonopoly,
    "regulated_data": RegulatedData,
    "china_adr_deep_value": ChinaADRDeepValue,
    "cloud_cyber_value": CloudCyberValue,
    "global_airlines_travel": GlobalAirlinesTravel,
    "utility_infra_income": UtilityInfraIncome,
    "japan_industrial_finance": JapanIndustrialFinance,
    "defense_prime_contractors": DefensePrimeContractors,
    "global_consumer_staples": GlobalConsumerStaples,
    "emerging_market_etf_value": EmergingMarketETFValue,
    "global_pharma_pipeline": GlobalPharmaPipeline,
    "singapore_alpha": SingaporeAlpha,
    "uk_european_banking": UKEuropeanBanking,
    "telecom_equipment_5g": TelecomEquipment5G,
    "gig_economy_saas": GigEconomySaaSDisruptors,
    "korean_chaebols": KoreanChaebols,
    "rideshare_mobility": RideshareMobility,
}


def get_theme_strategy(name: str, **kwargs) -> BasePersona:
    cls = THEME_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown theme: {name}. Available: {list(THEME_STRATEGIES.keys())}")
    return cls(**kwargs)


def list_theme_strategies():
    result = []
    for key, cls in THEME_STRATEGIES.items():
        instance = cls()
        result.append({
            "key": key,
            "name": instance.config.name,
            "description": instance.config.description,
        })
    return result


if __name__ == "__main__":
    print("=== Theme-Based Strategies ===\n")
    for p in list_theme_strategies():
        print(f"  {p['key']:25s} | {p['name']:30s} | {p['description']}")

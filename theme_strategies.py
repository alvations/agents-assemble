"""Theme-based trading strategies for agents-assemble.

These personas trade based on macro themes and megatrends rather than
individual investor philosophies. Each theme targets a specific sector
thesis with its own universe and timing signals.

Themes:
    1. AIRevolution      — AI/ML infrastructure and applications
    2. CleanEnergy       — Renewables, EVs, batteries, grid
    3. DefenseAerospace  — Defense contractors, space, cybersecurity
    4. BiotechBreakout   — Biotech/pharma innovation and FDA catalysts
    5. ChinaTechRebound  — China tech ADRs recovery play
    6. LatAmGrowth       — Latin American growth (fintech, commodities)
    7. InfrastructureBoom — Infrastructure spending (bridges, 5G, data centers)
    8. SmallCapValue     — Small cap deep value (IWM universe)
    9. CryptoEcosystem   — Crypto-adjacent public companies
    10. AgingPopulation  — Healthcare, senior living, pharma for aging demographics
    11. GLP1Obesity      — GLP-1 / weight loss drug megatrend
    12. RoboticsAutonomous — Humanoid robots + autonomous vehicles
"""

from __future__ import annotations

from personas import BasePersona, PersonaConfig


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
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            macd = self._get_indicator(data, sym, "macd", date)
            macd_sig = self._get_indicator(data, sym, "macd_signal", date)

            if any(v is None for v in [sma50, sma200, rsi]):
                continue

            # Thesis broken
            if price < sma200 * 0.90:
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
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
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
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
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
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            vol = self._get_indicator(data, sym, "vol_20", date)
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
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
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
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            if any(v is None for v in [sma50, rsi]):
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
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
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
            bb_lower = self._get_indicator(data, sym, "bb_lower", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            volume = self._get_indicator(data, sym, "Volume", date)
            vol_avg = self._get_indicator(data, sym, "volume_sma_20", date)
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
            sma20 = self._get_indicator(data, sym, "sma_20", date)
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            volume = self._get_indicator(data, sym, "Volume", date)
            vol_avg = self._get_indicator(data, sym, "volume_sma_20", date)
            if any(v is None for v in [sma20, rsi]):
                continue

            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1

            # Crypto is momentum-driven — ride breakouts
            if price > sma20 and rsi < 75 and vol_ratio > 1.2:
                score = 2.0 + vol_ratio
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
            for sym, score in top:
                weights[sym] = min((score / total_score) * 0.90, self.config.max_position_size)
            # Redistribute clipped excess so total allocation reaches 90%
            total_w = sum(weights[sym] for sym, _ in top)
            if 0 < total_w < 0.90:
                for sym, _ in top:
                    weights[sym] = min(weights[sym] * 0.90 / total_w, self.config.max_position_size)
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
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
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
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            if any(v is None for v in [sma50, rsi]):
                continue
            if sma200 is not None and price < sma200 * 0.90:
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
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            macd = self._get_indicator(data, sym, "macd", date)
            macd_sig = self._get_indicator(data, sym, "macd_signal", date)
            if any(v is None for v in [sma50, rsi]):
                continue
            if sma200 is not None and price < sma200 * 0.85:
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

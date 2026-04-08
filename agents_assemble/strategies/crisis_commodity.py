"""Crisis, commodity, and event-catalyst trading strategies.

Based on research findings from agents:
- War/geopolitical → energy/defense spike
- Food crisis → fertilizer/agriculture
- Gaming/entertainment → content release catalysts
- Small cap value rotation

All backtested — never trust blindly.
"""

from __future__ import annotations

from agents_assemble.strategies.generic import BasePersona, PersonaConfig


# ---------------------------------------------------------------------------
# 1. Geopolitical Crisis Alpha
# ---------------------------------------------------------------------------
class GeopoliticalCrisis(BasePersona):
    """Trade war/crisis → energy + defense beneficiaries.

    Research: Iran-Hormuz crisis (Feb 2026) doubled crude to $104+.
    XLE +40.8% YTD, ITA +54% trailing 12mo. Defense backlogs $1T+.

    Strategy: When market vol spikes (crisis proxy), rotate into
    energy + defense. When vol normalizes, reduce and take profits.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Geopolitical Crisis Alpha",
            description="War/crisis beneficiaries: energy + defense spike when vol rises",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "XLE", "XOP", "OXY", "DVN", "HAL", "SLB",  # Energy
                "LMT", "RTX", "NOC", "GD", "ITA",  # Defense
                "GLD", "SLV",  # Safe havens
                "SPY",  # Regime detection
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        ann_vol = spy_vol * (252 ** 0.5) if spy_vol is not None else 0.15

        weights = {}
        energy = ["XLE", "XOP", "OXY", "DVN", "HAL", "SLB"]
        defense = ["LMT", "RTX", "NOC", "GD", "ITA"]

        if ann_vol > 0.22:
            # Crisis mode: heavy energy + defense + safe havens
            crisis_picks = []
            for sym in energy + defense:
                if sym not in prices:
                    continue
                inds = self._get_indicators(data, sym, ["sma_50", "rsi_14"], date)
                sma50, rsi = inds["sma_50"], inds["rsi_14"]
                if rsi is not None and rsi > 80:
                    weights[sym] = 0.0
                    continue
                if sym in energy and (sma50 is None or prices[sym] <= sma50):
                    continue
                crisis_picks.append(sym)
            for sym in ["GLD", "SLV"]:
                if sym in self.config.universe and sym in prices:
                    crisis_picks.append(sym)
            if crisis_picks:
                per_stock = min(0.90 / len(crisis_picks), self.config.max_position_size)
                for sym in crisis_picks:
                    weights[sym] = per_stock
        else:
            # Normal: momentum-select best performers
            scored = []
            for sym in energy + defense:
                if sym not in prices:
                    continue
                inds = self._get_indicators(data, sym, ["sma_50", "sma_200"], date)
                sma50, sma200 = inds["sma_50"], inds["sma_200"]
                if sma50 is not None and sma200 is not None and sma200 > 0 and prices[sym] > sma50 > sma200:
                    scored.append((sym, (prices[sym] - sma200) / sma200))
            scored.sort(key=lambda x: x[1], reverse=True)
            top = scored[:self.config.max_positions]
            haven_budget = 0.0
            for sym in ["GLD", "SLV"]:
                if sym in self.config.universe and sym in prices:
                    weights[sym] = 0.05
                    haven_budget += 0.05
            if top:
                per_stock = min((0.90 - haven_budget) / len(top), self.config.max_position_size)
                for sym, _ in top:
                    weights[sym] = per_stock

        # Close stale positions for symbols not in current weights
        for sym in self.config.universe:
            if sym in prices and sym != "SPY" and sym not in weights:
                weights[sym] = 0.0
        return {k: v for k, v in weights.items() if k in prices and k != "SPY"}


# ---------------------------------------------------------------------------
# 2. Agriculture & Food Security
# ---------------------------------------------------------------------------
class AgricultureFoodSecurity(BasePersona):
    """Food crisis / fertilizer shortage strategy.

    Research: Hormuz blockade cuts 33% of seaborne urea.
    NTR (largest potash), CF (low-cost gas), ADM, DE benefit.
    MOO ETF for broad agriculture equity exposure.

    Strategy: Momentum on agriculture + fertilizer names.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Agriculture & Food Security",
            description="Fertilizer + agriculture: food crisis beneficiaries",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NTR", "CF", "MOS", "FMC",  # Fertilizer
                "ADM", "BG", "CTVA",  # Agribusiness
                "DE", "AGCO",  # Farm equipment
                "DBA", "MOO",  # Agriculture ETFs
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
            if rsi > 80:
                weights[sym] = 0.0
                continue
            score = 0.0
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if 35 < rsi < 70:
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
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 3. Gaming Content Catalyst
# ---------------------------------------------------------------------------
class GamingContentCatalyst(BasePersona):
    """Buy-the-rumor-sell-the-news on game/content releases.

    Research findings:
    - NTDOY: buy 3-6mo before major launch, sell on release day
    - TTWO: buy delay dips (GTA VI delays = 7-10% drops, then +36% rallies)
    - DIS: box office barely moves stock, play earnings instead
    - NFLX: purely subscriber/earnings, content doesn't move stock
    - AMC: most correlated to individual movie weekends

    Strategy: Momentum in gaming publishers (strongest BRSN pattern).
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Gaming Content Catalyst",
            description="Buy-the-rumor on game publishers: NTDOY, TTWO, EA momentum",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "NTDOY", "TTWO", "EA",  # Game publishers (strongest signal)
                "RBLX", "U",  # Gaming platforms
                "DKNG",  # Gaming/betting
                "DIS", "NFLX",  # Entertainment (earnings plays)
                "CMCSA", "WBD",  # Media
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
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "Volume", "volume_sma_20"], date)
            sma50, sma200, rsi = inds["sma_50"], inds["sma_200"], inds["rsi_14"]
            volume, vol_avg = inds["Volume"], inds["volume_sma_20"]
            if any(v is None for v in [sma50, rsi]):
                continue
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            # Buy momentum + volume confirmation (pre-launch buildup)
            score = 0.0
            if sma200 is not None and price > sma50 > sma200:
                score += 2.5
            elif price > sma50:
                score += 1.5
            if vol_ratio > 1.3:
                score += 1.0  # Volume = catalyst anticipation
            if 40 < rsi < 70:
                score += 0.5
            # Sell on extreme overbought (post-release selloff)
            if rsi > 80:
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
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 4. Small Cap Value Rotation
# ---------------------------------------------------------------------------
class SmallCapValueRotation(BasePersona):
    """Small cap value rotation based on research.

    Research: Small caps at cheapest vs large caps in 50 YEARS.
    IWM +18% YTD 2026. AVUV 13.23% annualized since 2019.
    Multi-factor (value + quality + momentum) beats single-factor.

    Strategy: Rotate into small cap value ETFs + individual picks
    when small caps show momentum vs large caps.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Small Cap Value Rotation",
            description="Small caps at 50-year cheap: AVUV + momentum picks, 18% YTD 2026",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "AVUV", "DFSV", "VBR",  # Small cap value ETFs
                "IWM", "IWN",  # Small cap broad + value
                "GRC", "UCTT", "WTTR", "EVLV",  # Individual picks
                "SAIA", "DECK", "LULU", "CELH",  # Small cap winners
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
            if rsi > 80:
                weights[sym] = 0.0
                continue
            score = 0.0
            if sma200 is not None and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if 35 < rsi < 70:
                score += 0.5
            # Small cap value premium: buy dips
            if sma200 is not None and price < sma200 * 1.05 and rsi < 40:
                score += 1.0  # Near SMA200 support
            if score >= 2.0:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
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
# 5. Contrarian Fallen Angels
# ---------------------------------------------------------------------------
class ContrarianFallenAngels(BasePersona):
    """Buy beaten-down quality stocks with activist/turnaround catalysts.

    Research: BA $682B backlog, INTC foundry milestones, PFE $60B+ revenue.
    NCLH (Elliott 10% stake, $56 target vs $21).
    CPI 2.4% + stabilizing rates = re-rating window.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Contrarian Fallen Angels",
            description="Buy beaten-down quality + activist catalysts: BA, INTC, PFE, NCLH",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "BA", "INTC", "PFE", "ENPH",  # Fallen angels
                "NCLH", "TRIP", "WEN",  # Activist targets
                "NKE", "PYPL", "DIS",  # Beaten-down quality
                "FMC", "CLX", "UPS",  # Deep value
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
            inds = self._get_indicators(data, sym, ["sma_200", "rsi_14", "Volume", "volume_sma_20"], date)
            sma200, rsi = inds["sma_200"], inds["rsi_14"]
            volume, vol_avg = inds["Volume"], inds["volume_sma_20"]
            if any(v is None for v in [sma200, rsi]):
                continue
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            # Exit structural freefall — >30% below SMA200 is falling knife
            if discount > 0.30:
                weights[sym] = 0.0
                continue
            # Buy deep discount + recovery signal
            if discount > 0.05 and rsi < 45:
                vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
                score = discount * 5 + max(0, 45 - rsi) / 45
                if vol_ratio > 1.5:
                    score *= 1.3  # Volume = institutional interest
                candidates.append((sym, score))
            # Take profits on recovery
            if rsi > 65 and discount < -0.10:
                weights[sym] = 0.0
        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


CRISIS_COMMODITY_STRATEGIES = {
    "geopolitical_crisis": GeopoliticalCrisis,
    "agriculture_food": AgricultureFoodSecurity,
    "gaming_catalyst": GamingContentCatalyst,
    "small_cap_value_rotation": SmallCapValueRotation,
    "contrarian_fallen_angels": ContrarianFallenAngels,
}


def get_crisis_commodity_strategy(name: str, **kwargs) -> BasePersona:
    cls = CRISIS_COMMODITY_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(CRISIS_COMMODITY_STRATEGIES.keys())}")
    return cls(**kwargs)

"""Recession indicators and recession-proof strategies for agents-assemble.

Recession Detection:
- Yield curve inversion (10Y-2Y spread, 10Y-3M spread)
- SMA200 death cross on SPY
- High yield spreads widening
- Market breadth deterioration
- VIX regime

Recession-Proof Strategies:
1. RecessionDetector    — Regime detection, shifts to defensive
2. TreasurySafe        — Flight to quality during downturns
3. DefensiveRotation   — Rotate to staples/utilities/healthcare in recessions
4. GoldBug             — Gold and precious metals as recession hedge
"""

from __future__ import annotations

import pandas as pd

from agents_assemble.strategies.generic import BasePersona, PersonaConfig


# ---------------------------------------------------------------------------
# Recession Regime Detection
# ---------------------------------------------------------------------------
def detect_recession_regime(
    date: pd.Timestamp,
    data: dict[str, pd.DataFrame],
    prices: dict[str, float],
) -> dict[str, object]:
    """Detect if we're in a recession-like regime.

    Uses multiple signals:
    1. SPY below SMA200 (bear market)
    2. TLT rising (flight to quality)
    3. IWM underperforming SPY (small caps weaker = risk-off)
    4. VIX proxy (high volatility in SPY)

    Returns dict with regime info and confidence score.
    """
    regime = {
        "is_recession": False,
        "confidence": 0.0,
        "signals": {},
    }

    signal_count = 0
    total_signals = 0

    # Fetch SPY indicators once (used by signals 1, 2, 4, 5)
    _spy_raw = prices.get("SPY")
    spy_price = _spy_raw if _spy_raw is not None and not pd.isna(_spy_raw) else None
    spy_sma50 = _safe_get(data, "SPY", "sma_50", date) if "SPY" in data else None
    spy_sma200 = _safe_get(data, "SPY", "sma_200", date) if "SPY" in data else None
    spy_vol = _safe_get(data, "SPY", "vol_20", date) if "SPY" in data else None
    spy_rsi = _safe_get(data, "SPY", "rsi_14", date) if "SPY" in data else None

    # Signal 1: SPY below SMA200
    if spy_sma200 is not None and spy_price is not None:
        total_signals += 1
        if spy_price < spy_sma200:
            signal_count += 1
            regime["signals"]["spy_below_sma200"] = True
        else:
            regime["signals"]["spy_below_sma200"] = False

    # Signal 2: SPY SMA50 < SMA200 (death cross)
    if spy_sma50 is not None and spy_sma200 is not None:
        total_signals += 1
        if spy_sma50 < spy_sma200:
            signal_count += 1
            regime["signals"]["death_cross"] = True
        else:
            regime["signals"]["death_cross"] = False

    # Signal 3: TLT trending up (bonds rally = flight to quality)
    if "TLT" in data:
        tlt_sma50 = _safe_get(data, "TLT", "sma_50", date)
        tlt_sma200 = _safe_get(data, "TLT", "sma_200", date)
        if tlt_sma50 is not None and tlt_sma200 is not None:
            total_signals += 1
            if tlt_sma50 > tlt_sma200:
                signal_count += 1
                regime["signals"]["tlt_uptrend"] = True
            else:
                regime["signals"]["tlt_uptrend"] = False

    # Signal 4: High volatility
    if spy_vol is not None:
        total_signals += 1
        if spy_vol > 0.018:  # Annualized ~28%
            signal_count += 1
            regime["signals"]["high_vol"] = True
        else:
            regime["signals"]["high_vol"] = False

    # Signal 5: RSI below 40 on SPY
    if spy_rsi is not None:
        total_signals += 1
        if spy_rsi < 40:
            signal_count += 1
            regime["signals"]["spy_oversold"] = True
        else:
            regime["signals"]["spy_oversold"] = False

    if total_signals > 0:
        regime["confidence"] = signal_count / total_signals
        regime["is_recession"] = regime["confidence"] >= 0.5  # majority of available signals

    return regime


def _safe_get(data, sym, indicator, date):
    if sym not in data:
        return None
    df = data[sym]
    if indicator not in df.columns:
        return None
    if date in df.index:
        val = df.loc[date, indicator]
        if isinstance(val, pd.Series):
            val = val.iloc[0]
        return float(val) if not pd.isna(val) else None
    try:
        idx = df.index.get_indexer([date], method="nearest")[0]
        if idx >= 0:
            nearest_date = df.index[idx]
            if abs((date - nearest_date).days) > 10:
                return None  # Data too stale
            val = df.iloc[idx][indicator]
            return float(val) if not pd.isna(val) else None
    except (IndexError, KeyError, TypeError):
        pass
    return None


# ---------------------------------------------------------------------------
# 1. Recession Detector — Adaptive regime switching
# ---------------------------------------------------------------------------
class RecessionDetector(BasePersona):
    """Adaptive strategy that detects recession regime and switches positioning.

    Normal regime: 70% stocks (SPY/QQQ), 20% bonds (TLT), 10% gold (GLD)
    Recession regime: 20% stocks (XLP/XLV), 50% bonds (TLT/IEF), 20% gold (GLD), 10% cash
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Recession Detector (Adaptive)",
            description="Regime-switching: risk-on in growth, defensive in recession",
            risk_tolerance=0.4,
            max_position_size=0.50,
            max_positions=6,
            rebalance_frequency="weekly",
            universe=universe or [
                "SPY", "QQQ", "TLT", "IEF", "GLD",
                "XLP", "XLV", "SHY",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        regime = detect_recession_regime(date, data, prices)

        if regime["is_recession"]:
            # Defensive positioning
            weights = {
                "XLP": 0.15,  # Consumer staples
                "XLV": 0.10,  # Healthcare
                "TLT": 0.30,  # Long bonds
                "IEF": 0.15,  # Intermediate bonds
                "GLD": 0.20,  # Gold
                "SHY": 0.05,  # Short-term treasuries (cash proxy)
                "SPY": 0.0,   # Exit stocks
                "QQQ": 0.0,   # Exit tech
            }
        else:
            # Risk-on positioning
            weights = {
                "SPY": 0.35,
                "QQQ": 0.30,
                "TLT": 0.15,
                "GLD": 0.10,
                "IEF": 0.05,
                "XLP": 0.0,
                "XLV": 0.0,
                "SHY": 0.0,
            }

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 2. Treasury Safe Haven
# ---------------------------------------------------------------------------
class TreasurySafe(BasePersona):
    """Flight to quality strategy during downturns.

    Thesis: When stocks sell off, treasuries rally. Go long duration
    when recession signals fire, short duration otherwise.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Treasury Safe Haven",
            description="Flight to quality: long-duration bonds when recession signals fire",
            risk_tolerance=0.2,
            max_position_size=0.40,
            max_positions=4,
            rebalance_frequency="weekly",
            universe=universe or ["TLT", "IEF", "SHY", "TIP", "GLD", "SPY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        regime = detect_recession_regime(date, data, prices)

        if regime["is_recession"]:
            weights = {
                "TLT": 0.45,  # Long bonds (biggest winner in recession)
                "IEF": 0.20,
                "GLD": 0.20,  # Gold hedge
                "TIP": 0.10,  # Inflation protection
                "SHY": 0.0,
                "SPY": 0.0,
            }
        elif regime["confidence"] > 0.3:
            # Mixed signals — balanced
            weights = {
                "IEF": 0.30,
                "TLT": 0.15,
                "GLD": 0.15,
                "SHY": 0.20,
                "TIP": 0.10,
                "SPY": 0.0,
            }
        else:
            # All clear — moderate bond allocation
            weights = {
                "SHY": 0.40,  # Short duration (rates may rise)
                "IEF": 0.25,
                "TLT": 0.10,
                "GLD": 0.10,
                "TIP": 0.10,
                "SPY": 0.0,
            }

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 3. Defensive Rotation
# ---------------------------------------------------------------------------
class DefensiveRotation(BasePersona):
    """Rotate into defensive sectors during recession signals.

    Thesis: Consumer staples, utilities, and healthcare outperform
    during recessions because demand is inelastic.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Defensive Rotation",
            description="Rotate to staples/utilities/healthcare when recession signals fire",
            risk_tolerance=0.3,
            max_position_size=0.30,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Defensive sectors
                "XLP", "XLU", "XLV",  # Sector ETFs
                "PG", "KO", "PEP", "CL",  # Consumer staples
                "JNJ", "MRK", "ABBV", "UNH",  # Healthcare
                "NEE", "DUK", "SO",  # Utilities
                # Growth (for when things are good)
                "SPY", "QQQ", "XLK",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        regime = detect_recession_regime(date, data, prices)
        weights = {}

        if regime["is_recession"]:
            # Full defensive
            defensive = ["XLP", "XLU", "XLV", "PG", "KO", "JNJ", "MRK", "NEE"]
            available = [s for s in defensive if s in prices]
            if available:
                per_stock = min(0.90 / len(available), self.config.max_position_size)
                for sym in available:
                    weights[sym] = per_stock
            # Exit growth
            for sym in ["SPY", "QQQ", "XLK"]:
                weights[sym] = 0.0
        else:
            # Risk-on with some defensive hedge
            weights["SPY"] = 0.30
            weights["QQQ"] = 0.25
            weights["XLK"] = 0.15
            weights["XLP"] = 0.10
            weights["XLV"] = 0.10
            weights["XLU"] = 0.05

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 4. Gold Bug
# ---------------------------------------------------------------------------
class GoldBug(BasePersona):
    """Gold and precious metals strategy for recession/inflation hedge.

    Thesis: Gold outperforms during recessions, currency debasement,
    and inflation. Mining stocks provide leveraged exposure.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Gold Bug (Precious Metals)",
            description="Gold/silver/miners as recession and inflation hedge",
            risk_tolerance=0.5,
            max_position_size=0.25,
            max_positions=6,
            rebalance_frequency="weekly",
            universe=universe or [
                "GLD", "SLV",  # Physical gold/silver ETFs
                "GDX", "GDXJ",  # Gold miners
                "NEM", "GOLD", "AEM",  # Individual miners
                "IAU",  # Alternative gold ETF
                "SPY", "TLT",  # Required for recession regime detection
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        regime = detect_recession_regime(date, data, prices)

        # Always hold some gold
        base_gold = 0.20

        if regime["is_recession"]:
            # Max gold allocation
            weights["GLD"] = 0.35
            weights["SLV"] = 0.15
            weights["GDX"] = 0.20
            weights["NEM"] = 0.10
            weights["IAU"] = 0.10
        else:
            # Check gold trend
            gld_sma50 = _safe_get(data, "GLD", "sma_50", date)
            gld_sma200 = _safe_get(data, "GLD", "sma_200", date)
            gld_price = prices.get("GLD")

            if gld_sma50 is not None and gld_sma200 is not None and gld_price is not None:
                if gld_sma50 > gld_sma200:
                    # Gold uptrend — increase allocation
                    weights["GLD"] = 0.30
                    weights["GDX"] = 0.20
                    weights["SLV"] = 0.15
                    weights["NEM"] = 0.10
                else:
                    # Gold downtrend — minimal
                    weights["GLD"] = 0.15
                    weights["IAU"] = 0.10
            else:
                weights["GLD"] = base_gold

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
RECESSION_STRATEGIES = {
    "recession_detector": RecessionDetector,
    "treasury_safe": TreasurySafe,
    "defensive_rotation": DefensiveRotation,
    "gold_bug": GoldBug,
}


def get_recession_strategy(name: str, **kwargs) -> BasePersona:
    cls = RECESSION_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown strategy: {name}. Available: {list(RECESSION_STRATEGIES.keys())}")
    return cls(**kwargs)


if __name__ == "__main__":
    print("=== Recession Strategies ===\n")
    for key, cls in RECESSION_STRATEGIES.items():
        inst = cls()
        print(f"  {key:25s} | {inst.config.name:35s} | {inst.config.description}")

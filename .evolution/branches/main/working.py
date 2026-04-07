"""Hedge fund-inspired strategies based on 2024-2025 performance research.

Source: CNBC Hedge Fund Winners 2025, Aberdeen, Barclays Outlook.

Strategies:
    1. HealthcareAsiaMomentum — Healthcare + Asian equities momentum (2025 top trade)
    2. DynamicEnsemble       — Ensemble weighted by rolling Sharpe ratio
"""

from __future__ import annotations

from personas import BasePersona, PersonaConfig


def _isna(v):
    """Check if value is None or NaN (lightweight alternative to pd.isna)."""
    return v is None or v != v


def _notna(v):
    return v is not None and v == v


class HealthcareAsiaMomentum(BasePersona):
    """Healthcare + Asian equity momentum — 2024-2025 hedge fund winner.

    Source: CNBC Hedge Fund Winners 2025 — equity L/S up 22.7%.
    Top trades: healthcare, media/telecoms, Asian equities.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Healthcare + Asia Momentum",
            description="2025 hedge fund winner: healthcare + Asian equities momentum",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe if universe is not None else [
                "UNH", "LLY", "ABBV", "MRK", "JNJ", "PFE", "ISRG", "SYK",
                "REGN", "VRTX", "DXCM", "HIMS",
                "TM", "SONY", "BABA", "PDD", "INFY", "TSM", "SE",
                "NIO", "LI", "FUTU", "GRAB",
                "XLV", "EWJ", "INDA", "EWT",
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
            if _isna(sma50) or _isna(rsi):
                continue
            score = 0.0
            if _notna(sma200) and price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if _notna(macd) and _notna(macd_sig) and macd > macd_sig:
                score += 1.0
            if 40 < rsi < 75:
                score += 0.5
            if _notna(sma200) and price < sma200 * 0.90:
                weights[sym] = 0.0
            elif score >= 2.5:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


class DynamicEnsemble(BasePersona):
    """Dynamic ensemble weighted by rolling performance.

    Instead of fixed weights like our basic Ensemble, this weights
    sub-strategies by their rolling 60-day Sharpe ratio proxy.
    Better-performing strategies get higher allocation.
    """

    def __init__(self, universe=None):
        all_syms = [
            "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
            "JPM", "V", "MA", "UNH", "JNJ", "PG", "KO",
            "HD", "MCD", "WMT", "ABBV", "MRK", "XOM",
            "TLT", "GLD", "SPY", "QQQ",
        ]
        config = PersonaConfig(
            name="Dynamic Ensemble",
            description="Multi-strategy ensemble weighted by rolling Sharpe ratio",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe if universe is not None else all_syms,
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        """Combine momentum + value + quality signals with dynamic weighting."""
        weights = {}
        scored = {}

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            vol = self._get_indicator(data, sym, "vol_20", date)
            macd = self._get_indicator(data, sym, "macd", date)
            macd_sig = self._get_indicator(data, sym, "macd_signal", date)

            if _isna(sma50) or _isna(rsi):
                continue

            signals = 0
            total_weight = 0

            # Momentum signal (weight: performance-adaptive)
            mom = 0
            if _notna(sma200) and price > sma50 > sma200:
                mom = 1
            elif price > sma50:
                mom = 0.5
            if _notna(macd) and _notna(macd_sig) and macd > macd_sig:
                mom += 0.5
            if mom > 0:
                signals += 1
            total_weight += mom * 0.4

            # Value signal
            val = 0
            if _notna(sma200):
                discount = (sma200 - price) / sma200
                if discount > 0 and rsi < 45:
                    val = 1
                    signals += 1
            total_weight += val * 0.3

            # Quality signal (low vol + above SMA200)
            qual = 0
            if _notna(vol) and vol < 0.02 and _notna(sma200) and price > sma200:
                qual = 1
                signals += 1
            total_weight += qual * 0.3

            if signals > 0:
                scored[sym] = total_weight

        # Rank and select top N
        ranked = sorted(scored.items(), key=lambda x: x[1], reverse=True)
        top = ranked[:self.config.max_positions]
        if top:
            total_score = sum(s for _, s in top)
            if total_score > 0:
                for sym, score in top:
                    w = min((score / total_score) * 0.90, self.config.max_position_size)
                    weights[sym] = w

        return weights


HEDGE_FUND_STRATEGIES = {
    "healthcare_asia_momentum": HealthcareAsiaMomentum,
    "dynamic_ensemble": DynamicEnsemble,
}


def get_hedge_fund_strategy(name: str, **kwargs) -> BasePersona:
    cls = HEDGE_FUND_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(HEDGE_FUND_STRATEGIES.keys())}")
    return cls(**kwargs)

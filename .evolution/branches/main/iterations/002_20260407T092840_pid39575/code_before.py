"""Mathematically-driven trading strategies for agents-assemble.

These strategies use specific mathematical techniques beyond simple
moving averages. Each is grounded in a specific mathematical concept.

Strategies:
    1. KellyOptimal        — Kelly criterion position sizing with momentum
    2. ZScoreReversion     — Statistical Z-score mean reversion
    3. HurstExponent       — Regime detection via Hurst exponent proxy
    4. VolatilityBreakout  — Donchian channel breakouts scaled by ATR
    5. EqualRiskContrib    — Equal risk contribution (ERC) portfolio
"""

from __future__ import annotations

from typing import List, Optional

import numpy as np
import pandas as pd

from personas import BasePersona, PersonaConfig


# ---------------------------------------------------------------------------
# 1. Kelly Criterion Optimal Sizing
# ---------------------------------------------------------------------------
class KellyOptimal(BasePersona):
    """Kelly criterion position sizing with momentum signal.

    Source: Kelly (1956) "A New Interpretation of Information Rate"

    f* = (p*b - q) / b
    where p = win probability, q = 1-p, b = win/loss ratio

    We estimate p and b from rolling 60-day returns, then use
    fractional Kelly (half-Kelly) for safety.
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Kelly Criterion Optimal",
            description="Position sizing via Kelly criterion from rolling win rate and payoff ratio",
            risk_tolerance=0.5,
            max_position_size=0.20,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "UNH", "HD", "MCD", "PG",
                "SPY", "QQQ",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue

            df = data[sym]
            if "daily_return" not in df.columns or date not in df.index:
                continue

            # Get rolling 60-day returns window
            loc = df.index.get_loc(date)
            if loc < 60:
                continue
            window = df["daily_return"].iloc[loc-60:loc+1].dropna()
            if len(window) < 30:
                continue

            # Estimate Kelly parameters
            wins = window[window > 0]
            losses = window[window < 0]
            if len(wins) == 0 or len(losses) == 0:
                continue

            p = len(wins) / len(window)  # Win probability
            avg_win = wins.mean()
            avg_loss = abs(losses.mean())
            b = avg_win / avg_loss if avg_loss > 0 else 1  # Payoff ratio

            q = 1 - p
            kelly = (p * b - q) / b if b > 0 else 0

            # Half-Kelly for safety
            half_kelly = max(0, kelly * 0.5)

            # Only invest if Kelly > 0 and momentum is positive
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            price = prices[sym]
            if half_kelly > 0.01 and sma50 and price > sma50:
                candidates.append((sym, half_kelly))

        # Normalize weights
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            top = candidates[:self.config.max_positions]
            total_kelly = sum(k for _, k in top)
            if total_kelly > 0.95:
                scale = 0.95 / total_kelly
            else:
                scale = 1.0
            for sym, k in top:
                weights[sym] = min(k * scale, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# 2. Z-Score Mean Reversion
# ---------------------------------------------------------------------------
class ZScoreReversion(BasePersona):
    """Statistical Z-score based mean reversion.

    Buy when a stock's price is >2 standard deviations below its
    60-day mean (Z < -2). Sell when it reverts to Z > 0.

    This is more rigorous than simple RSI — it uses actual
    statistical significance thresholds.
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Z-Score Mean Reversion",
            description="Buy at Z < -2 (statistically oversold), sell at Z > 0",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "UNH", "JNJ", "PG", "KO",
                "HD", "MCD", "WMT", "XOM", "CVX", "BAC",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue

            df = data[sym]
            if "Close" not in df.columns or date not in df.index:
                continue

            loc = df.index.get_loc(date)
            if loc < 60:
                continue

            window = df["Close"].iloc[loc-60:loc+1]
            if len(window) < 30:
                continue

            mean = window.mean()
            std = window.std()
            if not (std > 0):
                continue

            price = prices[sym]
            z_score = (price - mean) / std

            # Buy signal: Z < -2 (statistically significant oversold)
            if z_score < -2.0:
                # Score by how extreme the Z is
                score = abs(z_score) - 2.0
                sma200 = self._get_indicator(data, sym, "sma_200", date)
                # Only if not in structural downtrend
                if sma200 and price > sma200 * 0.85:
                    candidates.append((sym, score))

            # Exit: Z > 0 (reverted to mean)
            elif z_score > 0.5:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 3. Hurst Exponent Regime Detection
# ---------------------------------------------------------------------------
class HurstExponent(BasePersona):
    """Regime detection using Hurst exponent proxy.

    H > 0.5: trending (use momentum)
    H < 0.5: mean-reverting (use mean reversion)
    H = 0.5: random walk (stay out)

    We estimate H from the autocorrelation of returns as a fast proxy.
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Hurst Regime Detector",
            description="Adaptive: momentum when trending, mean-reversion when reverting",
            risk_tolerance=0.5,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "UNH", "JNJ", "PG", "KO",
                "HD", "MCD", "WMT", "SPY", "QQQ",
            ],
        )
        super().__init__(config)

    def _estimate_hurst(self, returns: pd.Series) -> float:
        """Estimate Hurst exponent from autocorrelation proxy."""
        if len(returns) < 20:
            return 0.5  # Unknown → random walk
        # Use lag-1 autocorrelation as quick Hurst proxy
        # H ≈ 0.5 + autocorr/2
        autocorr = returns.autocorr(lag=1)
        if pd.isna(autocorr):
            return 0.5
        return 0.5 + autocorr / 2

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        mom_candidates = []
        mr_candidates = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue

            df = data[sym]
            if "daily_return" not in df.columns or date not in df.index:
                continue

            loc = df.index.get_loc(date)
            if loc < 60:
                continue

            returns = df["daily_return"].iloc[loc-60:loc+1].dropna()
            hurst = self._estimate_hurst(returns)

            price = prices[sym]
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            bb_lower = self._get_indicator(data, sym, "bb_lower", date)

            if any(v is None for v in [sma50, rsi]):
                continue

            if hurst > 0.55:
                # Trending regime → use momentum
                if price > sma50 and rsi < 75:
                    score = hurst * 2
                    if sma200 and sma50 > sma200:
                        score += 1
                    mom_candidates.append((sym, score))
            elif hurst < 0.45:
                # Mean-reverting regime → buy oversold
                if rsi < 30 and bb_lower and price < bb_lower:
                    score = (0.5 - hurst) * 5
                    mr_candidates.append((sym, score))
            # 0.45-0.55 → random walk, stay out

        # Combine both signal types
        all_candidates = mom_candidates + mr_candidates
        all_candidates.sort(key=lambda x: x[1], reverse=True)
        top = all_candidates[:self.config.max_positions]

        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 4. Volatility Breakout (Donchian + ATR)
# ---------------------------------------------------------------------------
class VolatilityBreakout(BasePersona):
    """Volatility breakout: Donchian channel breakout scaled by ATR.

    Source: Turtle Trading system (Richard Dennis, 1983)

    Buy when price breaks above the 20-day high (Donchian upper).
    Position size = risk budget / ATR (risk-normalize position).
    Exit when price breaks below 10-day low.

    We approximate Donchian with BB upper and use ATR for sizing.
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Volatility Breakout (Turtle)",
            description="Donchian breakout with ATR position sizing (Turtle Trading)",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
                "GLD", "TLT", "XLE", "SPY", "QQQ",
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
            bb_upper = self._get_indicator(data, sym, "bb_upper", date)
            bb_lower = self._get_indicator(data, sym, "bb_lower", date)
            atr = self._get_indicator(data, sym, "atr_14", date)
            sma20 = self._get_indicator(data, sym, "sma_20", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)

            if any(v is None for v in [bb_upper, atr, sma20]):
                continue

            # Breakout: price above BB upper (Donchian proxy)
            if price > bb_upper and rsi and rsi < 80:
                # ATR-scaled scoring (lower ATR = stronger breakout signal)
                if atr > 0:
                    atr_pct = atr / price
                    score = 3.0 / max(atr_pct * 100, 0.5)  # Inverse of ATR %
                    scored.append((sym, score, atr))

            # Exit: price below SMA20 (simplified Donchian lower)
            elif price < sma20 and bb_lower and price < bb_lower:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            risk_per_position = 0.02  # 2% of portfolio per position
            for sym, score, atr in top:
                if atr > 0:
                    # w = risk_budget * price / ATR (total_value cancels out)
                    w = min(risk_per_position * prices[sym] / atr,
                            self.config.max_position_size)
                    weights[sym] = w

        return weights


# ---------------------------------------------------------------------------
# 5. Equal Risk Contribution (ERC)
# ---------------------------------------------------------------------------
class EqualRiskContrib(BasePersona):
    """Equal Risk Contribution portfolio.

    Source: Maillard, Roncalli, Teiletche (2010)

    Each asset contributes equally to portfolio risk.
    Weight_i proportional to 1 / (sigma_i * sum(1/sigma_j))

    Combined with a momentum filter to avoid investing in downtrending assets.
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Equal Risk Contribution (ERC)",
            description="Each asset contributes equal risk, with momentum filter",
            risk_tolerance=0.4,
            max_position_size=0.25,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "SPY", "QQQ", "IWM",  # US equities
                "EFA", "EEM",          # International
                "TLT", "IEF",         # Bonds
                "GLD",                  # Gold
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        eligible = []

        for sym in self.config.universe:
            if sym not in prices:
                continue

            vol = self._get_indicator(data, sym, "vol_20", date)
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            price = prices[sym]

            if vol is None or vol <= 0:
                continue

            # Momentum filter: only include assets above SMA50
            if sma50 and price > sma50:
                eligible.append((sym, vol))

        if not eligible:
            # Everything bearish → defensive allocation from available universe
            fallback = {"TLT": 0.50, "IEF": 0.30, "GLD": 0.10}
            available = {s: w for s, w in fallback.items() if s in self.config.universe}
            if available:
                return available
            return {}

        # ERC: weight inversely proportional to vol
        total_inv_vol = sum(1 / v for _, v in eligible)
        for sym, vol in eligible:
            w = (1 / vol) / total_inv_vol * 0.90
            weights[sym] = min(w, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
MATH_STRATEGIES = {
    "kelly_optimal": KellyOptimal,
    "zscore_reversion": ZScoreReversion,
    "hurst_regime": HurstExponent,
    "volatility_breakout": VolatilityBreakout,
    "equal_risk_contrib": EqualRiskContrib,
}


def get_math_strategy(name: str, **kwargs) -> BasePersona:
    cls = MATH_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(MATH_STRATEGIES.keys())}")
    return cls(**kwargs)


if __name__ == "__main__":
    print("=== Math-Driven Strategies ===\n")
    for key, cls in MATH_STRATEGIES.items():
        inst = cls()
        print(f"  {key:25s} | {inst.config.name:35s} | {inst.config.description}")

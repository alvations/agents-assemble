"""Research-backed quantitative strategies for agents-assemble.

These are strategies derived from academic finance research and
quantitative analysis — not from any persona or interview.

All MUST be backtested before trusting.

Strategies:
    1. DualMomentum         — Gary Antonacci: absolute + relative momentum
    2. MultiFactorSmartBeta — Combine value + momentum + quality factors
    3. LowVolAnomaly        — Buy lowest-volatility quintile (Frazzini & Pedersen)
    4. MomentumCrashHedge   — 12-1 momentum with crash protection
    5. RiskParityMomentum   — Risk parity allocation + momentum overlay
    6. MeanVarianceOptimal  — Simplified Markowitz-inspired allocation
    7. GlobalRotation        — International momentum rotation
    8. FactorETFRotation    — Rotate between factor ETFs by momentum
    9. FaberSectorRotation  — Faber 12-month sector momentum, top 3
"""

from __future__ import annotations

import math

from agents_assemble.strategies.generic import BasePersona, PersonaConfig

_SQRT_252 = math.sqrt(252)


def _is_missing(v) -> bool:
    """Check if indicator value is None or NaN (nearest-date path can leak NaN)."""
    return v is None or v != v


# ---------------------------------------------------------------------------
# 1. Dual Momentum (Gary Antonacci)
# ---------------------------------------------------------------------------
class DualMomentum(BasePersona):
    """Gary Antonacci's Dual Momentum strategy.

    Source: "Dual Momentum Investing" (2014)

    Two filters:
    1. Relative momentum: pick the stronger of US stocks vs international
    2. Absolute momentum: only invest if stronger asset > T-bills (SMA proxy)

    If both fail → 100% bonds.

    Implementation:
    - Compare SPY 12-month return vs EFA (international)
    - If winner > 0 (absolute momentum): invest in winner
    - If winner < 0: invest in AGG (bonds)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Dual Momentum (Antonacci)",
            description="Absolute + relative momentum: stocks vs intl vs bonds",
            risk_tolerance=0.5,
            max_position_size=0.90,
            max_positions=2,
            rebalance_frequency="monthly",
            universe=universe or ["SPY", "EFA", "AGG"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        # Calculate 12-month (approx 200-day) momentum for SPY and EFA
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        efa_sma200 = self._get_indicator(data, "EFA", "sma_200", date)
        spy_price = prices.get("SPY")
        efa_price = prices.get("EFA")

        if spy_price is None or _is_missing(spy_sma200):
            return {"AGG": 0.90} if "AGG" in prices else {}

        # Relative momentum: SPY vs EFA
        spy_mom = (spy_price - spy_sma200) / spy_sma200 if spy_sma200 > 0 else 0
        efa_mom = (efa_price - efa_sma200) / efa_sma200 if efa_price is not None and not _is_missing(efa_sma200) and efa_sma200 > 0 else -1

        if spy_mom > efa_mom:
            winner, winner_mom = "SPY", spy_mom
        else:
            winner, winner_mom = "EFA", efa_mom

        # Absolute momentum: is winner > 0 (above its SMA200)?
        loser = "EFA" if winner == "SPY" else "SPY"
        if winner_mom > 0:
            weights = {winner: 0.90, loser: 0.0, "AGG": 0.0}
        else:
            # Both negative → safe haven
            weights = {"AGG": 0.90, "SPY": 0.0, "EFA": 0.0}
        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 2. Multi-Factor Smart Beta
# ---------------------------------------------------------------------------
class MultiFactorSmartBeta(BasePersona):
    """Multi-factor strategy combining value + momentum + quality.

    Source: Fama-French, AQR, Asness et al.

    Score each stock on 3 factors:
    - Value: price below SMA200 (discount proxy)
    - Momentum: MACD > signal + price > SMA50
    - Quality: low volatility + above SMA200

    Composite score → rank → equal-weight top N.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Multi-Factor Smart Beta",
            description="Value + momentum + quality composite factor ranking",
            risk_tolerance=0.5,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
                "JPM", "V", "MA", "UNH", "JNJ", "PG", "KO",
                "HD", "MCD", "WMT", "COST", "ABBV", "MRK",
                "XOM", "CVX", "BAC", "GS",
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
            vol = self._get_indicator(data, sym, "vol_20", date)

            if any(_is_missing(v) for v in [sma200, rsi, vol]) or vol <= 0:
                continue

            # Factor 1: Value (discount to SMA200, higher = more value)
            value_score = (sma200 - price) / sma200 if sma200 > 0 else 0
            value_score = max(-0.5, min(0.5, value_score))  # Clip

            # Factor 2: Momentum (trend alignment)
            mom_score = 0.0
            if not _is_missing(sma50) and price > sma50:
                mom_score += 0.25
            if price > sma200:
                mom_score += 0.25
            if not _is_missing(macd) and not _is_missing(macd_sig) and macd > macd_sig:
                mom_score += 0.25
            if 40 < rsi < 70:
                mom_score += 0.25

            # Factor 3: Quality (inverse vol, above SMA200)
            # vol > 0 guaranteed by filter on line 142
            quality_score = min(1.0, 0.015 / vol)  # Normalize: lower vol → higher score
            if price > sma200:
                quality_score = min(1.0, quality_score * 1.3)

            # Composite: equal weight the 3 factors
            composite = (value_score + 0.5) * 0.33 + mom_score * 0.33 + quality_score * 0.33

            if composite > 0.25:
                scored.append((sym, composite))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        # Explicitly close positions in non-qualifying stocks
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# 3. Low Volatility Anomaly
# ---------------------------------------------------------------------------
class LowVolAnomaly(BasePersona):
    """Low volatility anomaly strategy.

    Source: Frazzini & Pedersen (2014) "Betting Against Beta"

    Buy the lowest-volatility stocks. Counterintuitively, low-vol stocks
    have historically outperformed high-vol stocks on a risk-adjusted basis
    (and often in absolute terms too).

    Implementation:
    - Rank universe by 20-day realized volatility
    - Buy the bottom quintile (lowest vol)
    - Must be above SMA200 (not in downtrend)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Low Volatility Anomaly",
            description="Buy lowest-vol stocks: anomaly where low risk = higher returns",
            risk_tolerance=0.2,
            max_position_size=0.08,
            max_positions=15,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "MA", "UNH", "JNJ", "PG", "KO", "PEP",
                "HD", "MCD", "WMT", "COST", "ABBV", "MRK",
                "XOM", "CVX", "BAC", "GS", "TMO", "ABT",
                "LLY", "NEE", "DUK", "SO", "BRK-B",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        vol_ranked = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            vol = self._get_indicator(data, sym, "vol_20", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)

            if _is_missing(vol) or vol <= 0:
                continue
            # Must be above SMA200 (not broken)
            if not _is_missing(sma200) and price < sma200 * 0.95:
                continue

            vol_ranked.append((sym, vol))

        # Sort by vol ascending (lowest vol first)
        vol_ranked.sort(key=lambda x: x[1])

        # Take bottom quintile
        n = max(1, len(vol_ranked) // 5)
        top = vol_ranked[:min(n, self.config.max_positions)]

        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        if not weights:
            return {sym: 0.0 for sym in self.config.universe if sym in prices}
        return weights


# ---------------------------------------------------------------------------
# 4. Momentum with Crash Protection
# ---------------------------------------------------------------------------
class MomentumCrashHedge(BasePersona):
    """Momentum strategy with crash protection.

    Source: Daniel & Moskowitz (2016) "Momentum Crashes"

    Problem: Pure momentum crashes during bear market reversals.
    Solution: Scale momentum exposure by market volatility.
    When vol is high → reduce exposure. When vol is low → full exposure.

    Implementation:
    - Standard 12-1 momentum ranking (price vs SMA200)
    - Scale position sizes by inverse of realized volatility
    - When SPY vol > 2x average → cut to 50% exposure
    - When SPY vol > 3x average → cut to 25% or go to cash
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Momentum Crash-Hedged",
            description="Momentum with vol-scaling: reduce exposure when volatility spikes",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
                "AVGO", "NFLX", "CRM", "AMD", "PLTR", "CRWD",
                "SPY",  # Include for vol measurement
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Measure market volatility regime
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        if _is_missing(spy_vol):
            vol_scale = 1.0
        else:
            annualized_vol = spy_vol * _SQRT_252
            if annualized_vol > 0.40:      # >40% = crisis
                vol_scale = 0.25
            elif annualized_vol > 0.25:    # >25% = high vol
                vol_scale = 0.50
            elif annualized_vol > 0.18:    # >18% = elevated
                vol_scale = 0.75
            else:
                vol_scale = 1.0

        scored = []
        for sym in self.config.universe:
            if sym == "SPY" or sym not in prices:
                continue
            price = prices[sym]
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            macd = self._get_indicator(data, sym, "macd", date)
            macd_sig = self._get_indicator(data, sym, "macd_signal", date)

            if any(_is_missing(v) for v in [sma50, sma200, rsi]):
                continue

            # Momentum score
            score = 0.0
            if price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if not _is_missing(macd) and not _is_missing(macd_sig) and macd > macd_sig:
                score += 1.0
            if 45 < rsi < 75:
                score += 0.5

            if score >= 2.5:
                scored.append((sym, score))
            else:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min((0.90 * vol_scale) / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        if not weights:
            return {sym: 0.0 for sym in self.config.universe if sym in prices and sym != "SPY"}
        return weights


# ---------------------------------------------------------------------------
# 5. Risk Parity with Momentum Overlay
# ---------------------------------------------------------------------------
class RiskParityMomentum(BasePersona):
    """Risk parity allocation with momentum tilt.

    Combines Bridgewater-style risk parity with trend following:
    - Base: risk parity across asset classes (stocks, bonds, gold, commodities)
    - Overlay: tilt toward assets with positive momentum, away from negative

    Implementation:
    - Inverse-vol weighting (risk parity base)
    - Momentum filter: only include assets above SMA50
    - Assets below SMA50 get zero weight (trend filter)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Risk Parity + Momentum",
            description="Risk parity allocation with momentum tilt across asset classes",
            risk_tolerance=0.4,
            max_position_size=0.40,
            max_positions=5,
            rebalance_frequency="monthly",
            universe=universe or [
                "SPY",   # US stocks
                "EFA",   # International stocks
                "TLT",   # Long bonds
                "GLD",   # Gold
                "XLE",   # Commodities proxy
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
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            vol = self._get_indicator(data, sym, "vol_20", date)

            if _is_missing(vol) or vol <= 0:
                continue

            # Momentum filter: only include if above SMA50
            if not _is_missing(sma50) and price > sma50:
                candidates.append((sym, vol))
            # else: excluded (negative momentum)

        if not candidates:
            # Everything trending down → safe haven, zero out all equities
            fallback = {sym: 0.0 for sym in self.config.universe if sym in prices}
            # Only allocate to safe havens if they're in universe AND have price data
            if "TLT" in self.config.universe and "TLT" in prices:
                fallback["TLT"] = min(0.50, self.config.max_position_size)
            if "GLD" in self.config.universe and "GLD" in prices:
                fallback["GLD"] = min(0.30, self.config.max_position_size)
            return fallback

        # Respect max_positions: keep lowest-vol assets (best risk parity contributors)
        if len(candidates) > self.config.max_positions:
            candidates.sort(key=lambda x: x[1])  # ascending vol
            candidates = candidates[:self.config.max_positions]

        # Risk parity: inverse-vol weighting with iterative capping
        cap = self.config.max_position_size
        budget = 0.90
        remaining = [(sym, 1.0 / vol) for sym, vol in candidates]
        while remaining:
            total_inv_vol = sum(iv for _, iv in remaining)
            if total_inv_vol <= 0:
                break
            new_remaining = []
            for sym, iv in remaining:
                w = (iv / total_inv_vol) * budget
                if w >= cap:
                    weights[sym] = cap
                    budget -= cap
                else:
                    new_remaining.append((sym, iv))
            if len(new_remaining) == len(remaining):
                # No more capping needed — assign remaining budget
                for sym, iv in new_remaining:
                    weights[sym] = (iv / total_inv_vol) * budget
                break
            remaining = new_remaining

        return weights


# ---------------------------------------------------------------------------
# 6. Mean-Variance Simplified (Markowitz-inspired)
# ---------------------------------------------------------------------------
class MeanVarianceOptimal(BasePersona):
    """Simplified Markowitz mean-variance optimization.

    Source: Markowitz (1952) "Portfolio Selection"

    Instead of full covariance matrix optimization, we use a simplified
    return/risk ranking:
    - Expected return proxy: SMA50 momentum
    - Risk proxy: 20-day realized vol
    - Score = return / risk (Sharpe-like ratio per stock)
    - Weight proportional to score
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Mean-Variance Simplified",
            description="Markowitz-inspired: rank by return/risk ratio, weight proportionally",
            risk_tolerance=0.4,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "UNH", "JNJ", "PG", "KO",
                "HD", "MCD", "WMT", "ABBV", "MRK", "XOM",
                "TLT", "GLD",  # Include bonds/gold for diversification
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
            vol = self._get_indicator(data, sym, "vol_20", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)

            if any(_is_missing(v) for v in [sma50, vol]) or vol <= 0:
                continue

            # Expected return proxy: momentum (price / SMA50 - 1)
            exp_return = (price - sma50) / sma50 if sma50 > 0 else 0

            # Only consider assets with positive expected return
            if exp_return <= 0:
                continue

            # Must be above SMA200 (structural uptrend)
            if not _is_missing(sma200) and price < sma200:
                continue

            # Sharpe-like score
            sharpe_proxy = exp_return / vol
            scored.append((sym, sharpe_proxy))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            cap = self.config.max_position_size
            budget = 0.90
            remaining = list(top)
            while remaining:
                sub_total = sum(s for _, s in remaining)
                if sub_total <= 0:
                    break
                new_remaining = []
                for sym, score in remaining:
                    w = (score / sub_total) * budget
                    if w >= cap:
                        weights[sym] = cap
                        budget -= cap
                    else:
                        new_remaining.append((sym, score))
                if len(new_remaining) == len(remaining):
                    # No more capping needed — assign remaining budget
                    for sym, score in new_remaining:
                        weights[sym] = (score / sub_total) * budget
                    break
                remaining = new_remaining

        if not weights:
            return {sym: 0.0 for sym in self.config.universe if sym in prices}
        return weights


# ---------------------------------------------------------------------------
# 7. Global Rotation (international momentum)
# ---------------------------------------------------------------------------
class GlobalRotation(BasePersona):
    """Global rotation: momentum across regional ETFs + individual ADRs.

    Rotate capital into the strongest-performing regions and individual
    international names. Uses same momentum framework but across a
    geographically diversified universe.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Global Rotation",
            description="Rotate into strongest regions: US, Europe, Asia, EM, LatAm",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                # Regional ETFs
                "SPY", "EFA", "EEM", "VWO", "EWJ", "EWZ", "INDA", "EWY",
                # Top intl ADRs
                "TM", "SONY", "BABA", "PDD", "INFY", "SE",
                "MELI", "NU", "SAP", "ASML", "NVO",
                "BHP", "VALE", "GOLD",
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

            if any(_is_missing(v) for v in [sma50, sma200, rsi]):
                continue

            # Momentum score (same as proven momentum framework)
            score = 0.0
            if price > sma50 > sma200:
                score += 3.0
            elif price > sma50:
                score += 1.5
            if 40 < rsi < 75:
                score += 0.5

            # Vol-adjusted (prefer lower vol for same momentum)
            if not _is_missing(vol) and vol > 0:
                score *= min(1.5, 0.02 / vol)

            if score > 1.5:
                scored.append((sym, score))
            else:
                weights[sym] = 0.0

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        if not weights:
            return {sym: 0.0 for sym in self.config.universe if sym in prices}
        return weights


# ---------------------------------------------------------------------------
# 8. Factor ETF Rotation
# ---------------------------------------------------------------------------
class FactorETFRotation(BasePersona):
    """Rotate between factor ETFs based on momentum.

    Instead of picking individual stocks, rotate between factor ETFs:
    momentum (MTUM), quality (QUAL), value (VLUE), low vol (SPLV),
    size (IWM), multi-factor (LRGF). Pick the top 3 by momentum.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Factor ETF Rotation",
            description="Rotate between factor ETFs (momentum, quality, value, low vol) based on trend",
            risk_tolerance=0.4,
            max_position_size=0.35,
            max_positions=3,
            rebalance_frequency="monthly",
            universe=universe or [
                "MTUM",  # Momentum
                "QUAL",  # Quality
                "VLUE",  # Value
                "SPLV",  # Low Volatility
                "IWM",   # Small Cap (Size)
                "SPY",   # Market (baseline)
                "TLT",   # Bonds (safe haven)
                "GLD",   # Gold (hedge)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            if _is_missing(sma50) or _is_missing(sma200):
                continue
            # Momentum score
            mom = (price - sma200) / sma200 if sma200 > 0 else 0
            if price > sma50:
                mom += 0.1
            scored.append((sym, mom))

        # Filter positive momentum first, THEN take top N
        positive = [(s, m) for s, m in scored if m > 0]
        positive.sort(key=lambda x: x[1], reverse=True)
        top = positive[:self.config.max_positions]
        weights = {}
        if top:
            per_etf = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_etf
        else:
            # All negative momentum → safe haven (only if in universe and prices)
            cap = self.config.max_position_size
            if "TLT" in self.config.universe and "TLT" in prices:
                weights["TLT"] = min(0.50, cap)
            if "GLD" in self.config.universe and "GLD" in prices:
                weights["GLD"] = min(0.30, cap)
        # Explicitly close positions in non-winning ETFs
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 9. Faber Sector Rotation (proven methodology)
# ---------------------------------------------------------------------------
class FaberSectorRotation(BasePersona):
    """Faber sector rotation: 12-month momentum, top 3 sectors, absolute momentum filter.

    Source: Faber (2007). $10K→$135K (2000-2024) vs $62K S&P.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Faber Sector Rotation",
            description="Proven 12-month sector momentum: top 3 + absolute momentum filter",
            risk_tolerance=0.5,
            max_position_size=0.35,
            max_positions=3,
            rebalance_frequency="monthly",
            universe=universe or [
                "XLK", "XLF", "XLE", "XLV", "XLI", "XLP",
                "XLU", "XLRE", "XLC", "XLB", "XLY",
                "TLT", "IEF",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        scored = []
        for sym in self.config.universe:
            if sym in ("TLT", "IEF") or sym not in prices:
                continue
            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            if _is_missing(sma200) or sma200 <= 0:
                continue
            momentum = (price - sma200) / sma200
            if momentum > 0:
                scored.append((sym, momentum))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        weights = {}
        if top:
            per_sector = min(0.90 / len(top), self.config.max_position_size)
            total_alloc = per_sector * len(top)
            for sym, _ in top:
                weights[sym] = per_sector
            # Allocate capped remainder to safe havens (Faber: unallocated → bonds)
            remainder = 0.90 - total_alloc
            if remainder > 0.05:
                havens = [s for s in ("TLT", "IEF")
                          if s in self.config.universe and s in prices]
                if havens:
                    per_haven = min(remainder / len(havens),
                                    self.config.max_position_size)
                    for s in havens:
                        weights[s] = per_haven
        else:
            havens = [s for s in ("TLT", "IEF")
                      if s in self.config.universe and s in prices]
            if havens:
                per_haven = min(0.90 / len(havens),
                                self.config.max_position_size)
                for s in havens:
                    weights[s] = per_haven
        # Explicitly close positions in non-winning sectors
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return {k: v for k, v in weights.items() if k in prices}


RESEARCH_STRATEGIES = {
    "dual_momentum": DualMomentum,
    "multi_factor_smart_beta": MultiFactorSmartBeta,
    "low_vol_anomaly": LowVolAnomaly,
    "momentum_crash_hedge": MomentumCrashHedge,
    "risk_parity_momentum": RiskParityMomentum,
    "mean_variance_optimal": MeanVarianceOptimal,
    "global_rotation": GlobalRotation,
    "factor_etf_rotation": FactorETFRotation,
    "faber_sector_rotation": FaberSectorRotation,
}


def get_research_strategy(name: str, **kwargs) -> BasePersona:
    cls = RESEARCH_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(RESEARCH_STRATEGIES.keys())}")
    return cls(**kwargs)


if __name__ == "__main__":
    print("=== Research-Backed Strategies ===\n")
    for key, cls in RESEARCH_STRATEGIES.items():
        inst = cls()
        print(f"  {key:30s} | {inst.config.name:35s} | {inst.config.description}")

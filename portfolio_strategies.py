"""Combined portfolio strategies with hedging for agents-assemble.

These are PORTFOLIO-LEVEL strategies that combine multiple asset classes
(equities, bonds, commodities, defensive sectors) with explicit hedging.

Strategies:
    1. StaplesHedgedGrowth  — Growth core + staples/dividend hedge
    2. BarbellPortfolio     — Short-duration bonds + long-duration bonds + equities
    3. AllWeatherModern     — Updated Dalio All-Weather with 2026 adjustments
    4. AdaptiveEnsemble     — Regime-aware ensemble that shifts between strategies
    5. CoreSatellite        — 60% passive core + 40% active satellite
    6. IncomeShield         — High-dividend stocks + bond income for downside protection
"""

from __future__ import annotations

from typing import Dict, List, Optional

import numpy as np

from personas import BasePersona, PersonaConfig


# ---------------------------------------------------------------------------
# 1. Staples-Hedged Growth
# ---------------------------------------------------------------------------
class StaplesHedgedGrowth(BasePersona):
    """Growth stocks hedged with consumer staples and dividends.

    Core: 60% in momentum/growth (top tech)
    Hedge: 25% in staples (XLP, PG, KO, WMT) — low beta, steady income
    Buffer: 15% in gold/bonds — crisis protection

    When growth is strong (SMA50>SMA200 on SPY): full growth allocation.
    When growth weakens: shift to 40% staples, 30% bonds/gold.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Staples-Hedged Growth",
            description="Growth core + consumer staples/dividend hedge + gold/bond buffer",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                # Growth core
                "NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META",
                # Staples hedge
                "XLP", "PG", "KO", "WMT", "COST", "PEP",
                # Bond/gold buffer
                "TLT", "GLD", "SHY",
                # SPY for regime detection
                "SPY",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        # Detect growth regime via SPY
        spy_sma50 = self._get_indicator(data, "SPY", "sma_50", date)
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        spy_price = prices.get("SPY")

        growth_mode = True
        if spy_sma50 and spy_sma200 and spy_price:
            if spy_price < spy_sma200 or spy_sma50 < spy_sma200:
                growth_mode = False

        weights = {}
        growth = ["NVDA", "MSFT", "AAPL", "GOOGL", "AMZN", "META"]
        staples = ["XLP", "PG", "KO", "WMT", "COST", "PEP"]
        safe = ["TLT", "GLD", "SHY"]

        if growth_mode:
            # Risk-on: 60% growth, 25% staples, 15% buffer
            for sym in growth:
                if sym in prices:
                    rsi = self._get_indicator(data, sym, "rsi_14", date)
                    sma50 = self._get_indicator(data, sym, "sma_50", date)
                    if sma50 and prices[sym] > sma50 and (rsi is None or rsi < 75):
                        weights[sym] = 0.10
            for sym in staples:
                if sym in prices:
                    weights[sym] = 0.04
            weights["GLD"] = 0.05
            weights["SHY"] = 0.05
        else:
            # Risk-off: 20% growth, 40% staples, 30% safe, 10% cash
            for sym in growth[:3]:
                if sym in prices:
                    weights[sym] = 0.07
            for sym in staples:
                if sym in prices:
                    weights[sym] = 0.07
            weights["TLT"] = 0.12
            weights["GLD"] = 0.10
            weights["SHY"] = 0.08

        return {k: v for k, v in weights.items() if k in prices and k != "SPY"}


# ---------------------------------------------------------------------------
# 2. Barbell Portfolio
# ---------------------------------------------------------------------------
class BarbellPortfolio(BasePersona):
    """Barbell strategy: short-duration + long-duration + equities.

    Source: BlackRock barbell positioning for volatility.

    Barbell: concentrate in extremes, avoid the middle.
    - Short-duration bonds (SHY): stability, low vol
    - Long-duration bonds (TLT): convexity, crisis protection
    - High-growth equities: maximum upside

    Skip intermediate bonds — they have worst risk/reward.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Barbell Portfolio",
            description="Short bonds + long bonds + growth equities — skip the middle",
            risk_tolerance=0.5,
            max_position_size=0.25,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "SHY", "TLT",  # Bond barbell
                "NVDA", "MSFT", "GOOGL", "AMZN",  # Growth equities
                "GLD",  # Gold alternative
                "SPY",  # Regime detection
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        ann_vol = spy_vol * (252 ** 0.5) if spy_vol else 0.15

        if ann_vol > 0.25:
            # High vol: heavy bonds + gold
            return {"SHY": 0.30, "TLT": 0.25, "GLD": 0.20,
                    "NVDA": 0.05, "MSFT": 0.05}
        elif ann_vol < 0.12:
            # Low vol: heavy equities
            return {"NVDA": 0.20, "MSFT": 0.15, "GOOGL": 0.15, "AMZN": 0.15,
                    "SHY": 0.10, "TLT": 0.10, "GLD": 0.05}
        else:
            # Normal: balanced barbell
            return {"SHY": 0.20, "TLT": 0.15, "GLD": 0.10,
                    "NVDA": 0.15, "MSFT": 0.10, "GOOGL": 0.10, "AMZN": 0.10}


# ---------------------------------------------------------------------------
# 3. All-Weather Modern (2026 update)
# ---------------------------------------------------------------------------
class AllWeatherModern(BasePersona):
    """Updated All-Weather portfolio for 2026 environment.

    Classic Dalio: 30% stocks, 40% long bonds, 15% intermediate, 7.5% gold, 7.5% commodities.

    2026 adjustments:
    - Reduce long bonds (TLT) — rate uncertainty
    - Add TIPS for inflation protection
    - Add crypto-adjacent for diversification
    - Use momentum tilt within each sleeve
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="All-Weather Modern (2026)",
            description="Updated Dalio All-Weather: reduced bonds, added TIPS + crypto exposure",
            risk_tolerance=0.3,
            max_position_size=0.25,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "VTI", "VEA",  # Stocks (US + intl)
                "TLT", "IEF", "TIP", "SHY",  # Bonds (duration ladder + TIPS)
                "GLD",  # Gold
                "XLE",  # Commodities proxy
                "COIN",  # Crypto proxy (small allocation)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        # Risk parity: weight by inverse vol
        vols = {}
        for sym in self.config.universe:
            if sym not in prices:
                continue
            vol = self._get_indicator(data, sym, "vol_20", date)
            if vol and vol > 0:
                vols[sym] = vol

        if not vols:
            return {"VTI": 0.25, "TLT": 0.20, "IEF": 0.15, "GLD": 0.10, "TIP": 0.10, "SHY": 0.10}

        # Momentum filter: only include assets above SMA50
        filtered = {}
        for sym, vol in vols.items():
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            price = prices[sym]
            if sma50 and price > sma50:
                filtered[sym] = vol
            elif sym in ("SHY", "TIP"):
                filtered[sym] = vol  # Always include short bonds + TIPS

        if not filtered:
            filtered = vols

        total_inv = sum(1/v for v in filtered.values())
        for sym, vol in filtered.items():
            w = (1/vol) / total_inv * 0.90
            weights[sym] = min(w, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# 4. Adaptive Ensemble
# ---------------------------------------------------------------------------
class AdaptiveEnsemble(BasePersona):
    """Regime-aware ensemble that shifts between strategy types.

    Bull (SPY > SMA200, vol low): 70% momentum, 20% growth, 10% bonds
    Bear (SPY < SMA200, vol high): 20% defensive, 40% bonds, 30% gold, 10% staples
    Transition: 40% quality, 30% dividend, 20% bonds, 10% gold

    This is a META-strategy that allocates between asset classes
    based on market regime, not individual stock signals.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Adaptive Ensemble",
            description="Regime-switching: momentum in bulls, defensive in bears, quality in transitions",
            risk_tolerance=0.5,
            max_position_size=0.20,
            max_positions=10,
            rebalance_frequency="weekly",
            universe=universe or [
                # Momentum/growth sleeve
                "QQQ", "NVDA", "MSFT", "AMZN",
                # Defensive/staples sleeve
                "XLP", "XLV", "XLU",
                # Dividend/quality sleeve
                "VIG", "SCHD", "DVY",
                # Bonds
                "TLT", "IEF", "SHY",
                # Gold
                "GLD",
                # Regime detection
                "SPY",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        spy_sma200 = self._get_indicator(data, "SPY", "sma_200", date)
        spy_sma50 = self._get_indicator(data, "SPY", "sma_50", date)
        spy_price = prices.get("SPY")
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        spy_rsi = self._get_indicator(data, "SPY", "rsi_14", date)

        # Determine regime
        if spy_sma200 and spy_price and spy_sma50:
            ann_vol = spy_vol * (252 ** 0.5) if spy_vol else 0.15
            if spy_price > spy_sma50 > spy_sma200 and ann_vol < 0.20:
                regime = "bull"
            elif spy_price < spy_sma200 or ann_vol > 0.28:
                regime = "bear"
            else:
                regime = "transition"
        else:
            regime = "transition"

        if regime == "bull":
            return {
                "QQQ": 0.25, "NVDA": 0.15, "MSFT": 0.15, "AMZN": 0.15,
                "VIG": 0.10, "GLD": 0.05, "SHY": 0.05,
            }
        elif regime == "bear":
            return {
                "TLT": 0.20, "IEF": 0.15, "SHY": 0.10,
                "GLD": 0.20,
                "XLP": 0.10, "XLV": 0.10, "XLU": 0.05,
                "QQQ": 0.0, "NVDA": 0.0,
            }
        else:  # transition
            return {
                "VIG": 0.15, "SCHD": 0.10, "DVY": 0.05,
                "XLP": 0.10, "XLV": 0.10,
                "TLT": 0.10, "IEF": 0.10,
                "GLD": 0.10,
                "QQQ": 0.10,
            }

    def _filter_tradeable(self, weights, prices):
        return {k: v for k, v in weights.items() if k in prices and k != "SPY"}


# ---------------------------------------------------------------------------
# 5. Core-Satellite Portfolio
# ---------------------------------------------------------------------------
class CoreSatellite(BasePersona):
    """60% passive core + 40% active satellite.

    Core (60%): SPY/VTI + BND/AGG — boring, cheap, always-on
    Satellite (40%): Momentum + thematic + contrarian — active alpha

    Satellite changes based on momentum signals.
    Core stays constant.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Core-Satellite Portfolio",
            description="60% passive core (SPY+BND) + 40% active satellite (momentum+themes)",
            risk_tolerance=0.4,
            max_position_size=0.30,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "SPY", "BND",  # Core
                "NVDA", "AVGO", "LLY", "PLTR", "AMZN", "MSFT",  # Satellite: momentum
                "GLD", "XLE",  # Satellite: alternatives
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        # Core: always on
        weights["SPY"] = 0.40
        weights["BND"] = 0.20

        # Satellite: momentum-filtered
        satellite_candidates = []
        for sym in ["NVDA", "AVGO", "LLY", "PLTR", "GLD", "XLE"]:
            if sym not in prices:
                continue
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            price = prices[sym]
            if sma50 and price > sma50 and (rsi is None or rsi < 75):
                satellite_candidates.append(sym)

        if satellite_candidates:
            per_sat = 0.35 / len(satellite_candidates)
            for sym in satellite_candidates:
                weights[sym] = min(per_sat, 0.12)
        else:
            weights["GLD"] = 0.20
            weights["SPY"] = 0.50  # Increase core if no satellites

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 6. Income Shield
# ---------------------------------------------------------------------------
class IncomeShield(BasePersona):
    """High-dividend equities + bond income for downside protection.

    Combines dividend aristocrats, high-yield bond ETFs, and REITs
    for maximum income generation with lower drawdowns.

    Target: 4-5% yield, max drawdown < 15%.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Income Shield",
            description="High-dividend + bond income: 4-5% yield target, low drawdown",
            risk_tolerance=0.2,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                # High-dividend stocks
                "VIG", "SCHD", "DVY", "HDV",
                # Dividend aristocrats
                "JNJ", "PG", "KO", "ABBV", "XOM", "CVX", "MMM",
                # Bond income
                "BND", "LQD", "HYG", "TIP",
                # REITs
                "VNQ", "O",
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
            # Income: buy near or below SMA200, hold steady
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            if discount > -0.10:
                score = max(discount + 0.10, 0.01) + 0.3
                if rsi and rsi < 45:
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
# 7. Bond & Fixed Income Portfolio
# ---------------------------------------------------------------------------
class BondFixedIncome(BasePersona):
    """Diversified bond and fixed income portfolio.

    Thesis: Bonds provide income, diversification, and crisis protection.
    Allocate across duration ladder (short to long), credit spectrum
    (investment grade to high yield), and geography (US + EM).
    Shift duration based on volatility regime.

    Target: 3-5% yield, max drawdown < 8%.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Bond & Fixed Income Portfolio",
            description="Diversified bonds: duration ladder + credit spectrum + EM, 3-5% yield target",
            risk_tolerance=0.15,
            max_position_size=0.20,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "FBND", "SPBO",  # Core bond / corporate
                "SCHI",  # Intermediate corporate
                "VWOB",  # EM sovereign bonds
                "VTEB",  # Tax-exempt munis
                "AGG", "BND",  # Broad US aggregate
                "TLT",  # Long-duration treasuries
                "HYG",  # High yield corporate
                "LQD",  # Investment grade corporate
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        # Use AGG volatility as regime indicator
        agg_vol = self._get_indicator(data, "AGG", "vol_20", date)
        agg_rsi = self._get_indicator(data, "AGG", "rsi_14", date)

        if agg_vol is not None:
            ann_vol = agg_vol * (252 ** 0.5)
        else:
            ann_vol = 0.05  # Default bond vol assumption

        if ann_vol > 0.10:
            # High bond vol: shorten duration, reduce credit risk
            # Overweight short-duration and high-quality
            weights["FBND"] = 0.15
            weights["SPBO"] = 0.10
            weights["SCHI"] = 0.10
            weights["AGG"] = 0.15
            weights["BND"] = 0.15
            weights["VTEB"] = 0.10
            weights["TLT"] = 0.05  # Reduce long duration
            weights["HYG"] = 0.05  # Reduce credit risk
            weights["LQD"] = 0.10
            weights["VWOB"] = 0.05  # Reduce EM exposure
        elif ann_vol < 0.04:
            # Very low vol: extend duration for yield, add credit
            weights["TLT"] = 0.15
            weights["HYG"] = 0.12
            weights["LQD"] = 0.15
            weights["VWOB"] = 0.12
            weights["SCHI"] = 0.10
            weights["VTEB"] = 0.10
            weights["AGG"] = 0.08
            weights["BND"] = 0.08
            weights["FBND"] = 0.05
            weights["SPBO"] = 0.05
        else:
            # Normal vol: balanced allocation
            weights["AGG"] = 0.12
            weights["BND"] = 0.12
            weights["LQD"] = 0.12
            weights["FBND"] = 0.10
            weights["SCHI"] = 0.10
            weights["VTEB"] = 0.10
            weights["TLT"] = 0.10
            weights["VWOB"] = 0.08
            weights["HYG"] = 0.08
            weights["SPBO"] = 0.08

        # Oversold bonds = accumulate (income strategy always buys dips)
        if agg_rsi is not None and agg_rsi < 30:
            # Boost allocation across the board on bond selloff
            for sym in weights:
                weights[sym] = min(weights[sym] * 1.1, self.config.max_position_size)

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 8. High-Yield REIT, BDC & Real Estate Income
# ---------------------------------------------------------------------------
class HighYieldREITBDCIncome(BasePersona):
    """High-yield REIT, BDC, and real estate income strategy.

    Thesis: REITs and BDCs provide 6-12% dividend yields with monthly
    or quarterly distributions. Realty Income (O) is the "Monthly
    Dividend Company" with 30+ years of increases. AGNC and NLY are
    agency mortgage REITs yielding 12-15% (interest rate sensitive).
    MAIN and HTGC are BDCs lending to middle-market companies at 10%+
    yields. ARCC (Ares Capital) is the largest BDC by AUM.
    STAG Industrial is a logistics/e-commerce REIT beneficiary.
    Zillow and Redfin provide real estate tech exposure as a growth
    kicker alongside the income core.

    Target: 6-8% yield portfolio, max drawdown < 20%.

    Signal: Income-oriented. Buy on dips below SMA200 for yield
    accumulation. Hold in uptrend for total return. Trim overbought.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="High-Yield REIT, BDC & Real Estate",
            description="REITs + BDCs + RE tech: 6-8% yield, monthly income, dip accumulation",
            risk_tolerance=0.3,
            max_position_size=0.10,
            max_positions=14,
            rebalance_frequency="monthly",
            universe=universe or [
                # Equity REITs
                "O",      # Realty Income (monthly dividend, net lease)
                "STAG",   # STAG Industrial (logistics / e-commerce REIT)
                # Mortgage REITs (high yield, rate sensitive)
                "AGNC",   # AGNC Investment (agency MBS, 12-15% yield)
                "ARR",    # ARMOUR Residential (agency MBS REIT)
                "NLY",    # Annaly Capital (largest mortgage REIT)
                "DX",     # Dynex Capital (agency + non-agency MBS)
                # BDCs (Business Development Companies)
                "MAIN",   # Main Street Capital (premium BDC, internal)
                "HTGC",   # Horizon Technology Finance (venture lending)
                "ARCC",   # Ares Capital (largest BDC by AUM)
                # Real Estate Tech (growth kicker)
                "Z",      # Zillow Group (RE marketplace + tech)
                "RDFN",   # Redfin (discount brokerage + tech)
                # Broad REIT exposure
                "VNQ",    # Vanguard Real Estate ETF (diversified)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        # Classify tickers by type for different allocation logic
        income_core = {"O", "STAG", "MAIN", "ARCC", "VNQ"}
        mortgage_reits = {"AGNC", "ARR", "NLY", "DX"}
        bdcs = {"HTGC"}
        growth = {"Z", "RDFN"}

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14"], date)
            sma200, sma50, rsi = inds["sma_200"], inds["sma_50"], inds["rsi_14"]

            if sma200 is None or (sma200 != sma200):
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            if sym in income_core:
                # Income core: always allocate, buy dips aggressively
                if discount > 0.08:
                    score = 3.0 + discount * 5
                    candidates.append((sym, score, 0.10))
                elif discount > -0.05:
                    candidates.append((sym, 2.0, 0.08))
                elif discount > -0.15:
                    candidates.append((sym, 1.0, 0.06))
                elif rsi is not None and rsi > 78:
                    weights[sym] = 0.0

            elif sym in mortgage_reits:
                # Mortgage REITs: yield-seekers, very rate sensitive
                # Buy on oversold, trim on overbought
                if rsi is not None and rsi < 35 and discount > 0:
                    candidates.append((sym, 2.5 + discount * 3, 0.08))
                elif rsi is not None and rsi < 50 and discount > -0.05:
                    candidates.append((sym, 1.5, 0.06))
                elif rsi is not None and rsi > 75:
                    weights[sym] = 0.0
                else:
                    candidates.append((sym, 1.0, 0.05))

            elif sym in bdcs:
                # BDCs: steady income, accumulate on dips
                if discount > 0.05:
                    candidates.append((sym, 2.5, 0.08))
                elif discount > -0.10:
                    candidates.append((sym, 1.5, 0.06))
                elif rsi is not None and rsi > 75:
                    weights[sym] = 0.0

            elif sym in growth:
                # RE tech: momentum-driven growth kicker
                if sma50 is not None and price > sma50 and (rsi is None or rsi < 75):
                    score = 1.5
                    if sma200 is not None and price > sma50 > sma200:
                        score = 2.5
                    candidates.append((sym, score, 0.06))
                elif rsi is not None and rsi > 78:
                    weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        for sym, _, wt in top:
            weights[sym] = min(wt, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 9. Dividend Aristocrat Blue Chips
# ---------------------------------------------------------------------------
class DividendAristocratBlueChips(BasePersona):
    """Dividend aristocrat blue chip income portfolio.

    Thesis: Dividend aristocrats have raised dividends 25+ consecutive
    years — proof of business quality and capital discipline. Altria (MO)
    yields 8%+ with pricing power. Philip Morris (PM) is the global
    tobacco leader with IQOS growth. 3M (MMM) is restructuring post-
    litigation. UPS/FDX are logistics duopoly. JNJ is the healthcare
    conglomerate gold standard. Enbridge (ENB) is North America's
    largest pipeline operator (6%+ yield). ABBV (AbbVie) has the best
    pharma pipeline. XOM generates $50B+ operating cash flow.
    SCHD ETF provides diversified dividend exposure.

    Signal: Income accumulation. Buy on dips below SMA200 (yield
    pickup). Inverse volatility weighting for stability. Trim
    overbought to lock in capital gains.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Dividend Aristocrat Blue Chips",
            description="25+ year dividend growers: 4-8% yield, income + capital appreciation",
            risk_tolerance=0.2,
            max_position_size=0.10,
            max_positions=14,
            rebalance_frequency="monthly",
            universe=universe or [
                "MO",     # Altria (8%+ yield, pricing power)
                "PM",     # Philip Morris International (IQOS growth + 5% yield)
                "MMM",    # 3M (restructuring, 65yr dividend streak)
                "UPS",    # UPS (logistics duopoly, 4%+ yield)
                "FDX",    # FedEx (logistics duopoly, restructuring)
                "KHC",    # Kraft Heinz (consumer staples, 4%+ yield)
                "JNJ",    # Johnson & Johnson (healthcare gold standard)
                "PG",     # Procter & Gamble (69yr dividend streak)
                "KO",     # Coca-Cola (62yr dividend streak)
                "PEP",    # PepsiCo (52yr dividend streak)
                "ENB",    # Enbridge (pipeline, 6%+ yield)
                "ABBV",   # AbbVie (pharma pipeline + 4% yield)
                "XOM",    # Exxon Mobil (energy cash machine)
                "SCHD",   # Schwab US Dividend Equity ETF (diversified)
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
            inds = self._get_indicators(data, sym, ["sma_200", "sma_50", "rsi_14", "vol_20"], date)
            sma200, sma50, rsi, vol20 = inds["sma_200"], inds["sma_50"], inds["rsi_14"], inds["vol_20"]

            if sma200 is None or (sma200 != sma200):
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            # Income: always maintain some allocation (aristocrats are core)
            base_weight = 0.06
            score = 1.0

            # Buy dips below SMA200 (yield pickup on aristocrats)
            if discount > 0.10:
                score = 3.0 + discount * 5
                base_weight = 0.10
            elif discount > 0.03:
                score = 2.0
                base_weight = 0.08
            elif discount > -0.05:
                score = 1.5
                base_weight = 0.07
            elif discount > -0.15:
                score = 1.0
                base_weight = 0.05

            # RSI bonus for oversold aristocrats
            if rsi is not None and rsi < 35:
                score += 1.5
            elif rsi is not None and rsi < 45:
                score += 0.5

            # Overbought aristocrats: trim (not sell — they're income)
            if rsi is not None and rsi > 78 and discount < -0.15:
                base_weight = 0.03

            # Low vol bonus (stable dividend payers = more allocation)
            if vol20 is not None and vol20 < 0.015:
                score += 0.5

            candidates.append((sym, score, base_weight))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        total_weight = sum(wt for _, _, wt in top)
        # Scale to ~95% invested
        scale = 0.95 / total_weight if total_weight > 0 else 1.0
        for sym, _, wt in top:
            scaled = min(wt * scale, self.config.max_position_size)
            weights[sym] = scaled
        return weights


PORTFOLIO_STRATEGIES = {
    "staples_hedged_growth": StaplesHedgedGrowth,
    "barbell_portfolio": BarbellPortfolio,
    "all_weather_modern": AllWeatherModern,
    "adaptive_ensemble": AdaptiveEnsemble,
    "core_satellite": CoreSatellite,
    "income_shield": IncomeShield,
    "bond_fixed_income": BondFixedIncome,
    "high_yield_reit_bdc": HighYieldREITBDCIncome,
    "dividend_aristocrat_blue_chips": DividendAristocratBlueChips,
}


def get_portfolio_strategy(name: str, **kwargs) -> BasePersona:
    cls = PORTFOLIO_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(PORTFOLIO_STRATEGIES.keys())}")
    return cls(**kwargs)

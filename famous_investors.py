"""Famous investor personas for agents-assemble.

Real investor strategies based on documented approaches. Each persona
implements the actual strategy the investor is known for, with citations
to their documented methodology.

DISCLAIMER: These are educational backtests based on publicly documented
investment philosophies. They are NOT investment advice. Past performance
does not predict future results. The actual investors may have changed
their strategies or used non-public information.

Personas:
    1. PeterLynch     — "Buy what you know", PEG ratio, growth at reasonable price
    2. RayDalio       — All-Weather portfolio, risk parity, macro regime
    3. GeorgeSoros    — Reflexivity theory, macro momentum, currency/bond bets
    4. MichaelBurry   — Deep value contrarian, distressed assets, short overbought
    5. JimSimons      — Pure quant: mean-reversion + momentum factor combination
    6. CarlIcahn      — Activist value: undervalued large caps with catalysts
    7. MasayoshiSon   — Vision Fund: high-conviction tech platform bets
    8. LiKaShing      — Infrastructure/utility value, steady cash flows
    9. NassefSawiris  — Emerging market industrials, materials, global value
   10. JorgePauloLemann — 3G Capital: consumer brand dominance
   11. PrinceAlwaleed — Global blue-chip contrarian, crisis buying
   12. HowardMarks    — Oaktree: second-level thinking, buy quality in panic
   13. SupportResistanceCommodity — Breakout trading on commodity ETFs
"""

from __future__ import annotations

from personas import BasePersona, PersonaConfig


# ---------------------------------------------------------------------------
# 1. Peter Lynch — Growth at a Reasonable Price (GARP)
# ---------------------------------------------------------------------------
class PeterLynch(BasePersona):
    """Peter Lynch strategy — "Buy what you know", GARP.

    Source: "One Up on Wall Street" (1989), "Beating the Street" (1993)

    Key principles:
    - PEG ratio < 1.0 (P/E divided by earnings growth rate) = undervalued
    - Companies with consistent earnings growth
    - Avoid "hot" stocks with extreme momentum
    - Classify: slow growers, stalwarts, fast growers, cyclicals, turnarounds
    - "Invest in what you know" — favor consumer-facing companies

    Implementation (price-based proxy since we lack real-time PEG):
    - Buy stocks with moderate momentum (not extreme) near SMA50 support
    - Prefer stocks with low volatility relative to returns (proxy for GARP)
    - Avoid overbought (RSI > 75) and extremely volatile names
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Peter Lynch (GARP)",
            description="Growth at reasonable price: moderate momentum, low vol, buy what you know",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="monthly",
            # Consumer-facing + consistent growers Lynch would recognize
            universe=universe or [
                "AAPL", "COST", "WMT", "HD", "NKE", "SBUX", "MCD",
                "PG", "JNJ", "DIS", "AMZN", "GOOGL", "V", "MA",
                "UNH", "MSFT", "PEP", "KO", "TGT", "LOW",
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
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            vol20 = self._get_indicator(data, sym, "vol_20", date)

            if any(v is None for v in [sma50, sma200, rsi, vol20]):
                continue

            # GARP filter: moderate growth, not overheated
            if rsi > 75:
                weights[sym] = 0.0  # Avoid hot stocks
                continue

            if price < sma200 * 0.85:
                continue  # Avoid broken stocks

            # Score: return-to-volatility ratio (proxy for PEG concept)
            momentum = (price - sma200) / sma200 if sma200 > 0 else 0
            vol_adj = vol20 if vol20 > 0.005 else 0.005

            # GARP score: moderate momentum + low volatility = best
            if 0 < momentum < 0.30 and rsi < 65:
                garp_score = momentum / vol_adj  # Return per unit of risk
                # Bonus if near SMA50 support (buying on pullback)
                if sma50 > 0 and abs(price - sma50) / sma50 < 0.03:
                    garp_score *= 1.3
                candidates.append((sym, garp_score))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]

        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 2. Ray Dalio — All Weather / Risk Parity
# ---------------------------------------------------------------------------
class RayDalio(BasePersona):
    """Ray Dalio All-Weather portfolio + risk parity.

    Source: "Principles" (2017), Bridgewater research papers

    Key principles:
    - Balance risk across 4 macro environments:
      1. Rising growth (stocks, commodities)
      2. Falling growth (long-term bonds)
      3. Rising inflation (commodities, TIPS)
      4. Falling inflation (stocks, bonds)
    - Risk parity: weight inversely to volatility
    - Classic All-Weather: 30% stocks, 40% long-term bonds,
      15% intermediate bonds, 7.5% gold, 7.5% commodities

    Implementation:
    - Use ETF proxies: VTI (stocks), TLT (long bonds), IEF (intermediate),
      GLD (gold), DBC/GSG (commodities proxy via energy ETFs)
    - Adjust weights based on realized volatility (risk parity)
    """

    ASSET_TARGETS = {
        "VTI": 0.30,   # US total market
        "TLT": 0.40,   # Long-term treasuries
        "IEF": 0.15,   # Intermediate treasuries
        "GLD": 0.075,  # Gold
        "XLE": 0.075,  # Energy (commodity proxy available on Robinhood)
    }

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Ray Dalio (All-Weather)",
            description="Risk parity: balance across growth/inflation regimes via ETFs",
            risk_tolerance=0.3,
            max_position_size=0.45,
            max_positions=5,
            rebalance_frequency="monthly",
            universe=universe or list(self.ASSET_TARGETS.keys()),
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        vols = {}

        for sym in self.config.universe:
            if sym not in prices:
                continue
            vol = self._get_indicator(data, sym, "vol_20", date)
            if vol is not None and vol > 0:
                vols[sym] = vol

        if not vols:
            # Fallback to static All-Weather
            return {sym: w for sym, w in self.ASSET_TARGETS.items() if sym in prices}

        # Risk parity: weight inversely proportional to volatility
        total_inv_vol = sum(1 / v for v in vols.values())
        for sym, vol in vols.items():
            inv_vol = 1 / vol
            risk_parity_w = inv_vol / total_inv_vol

            # Blend risk parity with Dalio's target weights
            target = self.ASSET_TARGETS.get(sym, 0.10)
            blended = 0.6 * risk_parity_w + 0.4 * target  # 60% risk parity, 40% strategic

            weights[sym] = min(blended, self.config.max_position_size)

        # Normalize to ~95% invested (All-Weather should be near-fully invested)
        total = sum(weights.values())
        if total > 0 and abs(total - 0.95) > 0.01:
            scale = 0.95 / total
            weights = {k: min(v * scale, self.config.max_position_size) for k, v in weights.items()}

        return weights


# ---------------------------------------------------------------------------
# 3. George Soros — Reflexivity / Macro Momentum
# ---------------------------------------------------------------------------
class GeorgeSoros(BasePersona):
    """George Soros reflexivity and macro momentum strategy.

    Source: "The Alchemy of Finance" (1987), Soros Fund Management history

    Key principles:
    - Reflexivity: market participants' biases can reinforce trends
    - "Find the trend whose premise is false, and bet against it"
    - But also: ride trends aggressively when they're accelerating
    - Heavy use of leverage (we use position concentration instead)
    - Famous for: breaking the Bank of England (GBP short), tech bets

    Implementation:
    - Strong momentum: buy assets breaking to new highs with volume
    - Contrarian on extremes: fade when RSI > 85 or < 15
    - Concentrated bets (fewer positions, larger sizes)
    - Mix of equities and bond/currency ETFs for macro bets
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="George Soros (Reflexivity)",
            description="Macro momentum: ride reflexive trends, concentrate bets, fade extremes",
            risk_tolerance=0.9,
            max_position_size=0.30,
            max_positions=5,
            rebalance_frequency="weekly",
            universe=universe or [
                "SPY", "QQQ", "TLT", "GLD", "EEM",
                "XLE", "XLF", "AAPL", "NVDA", "MSFT",
                "TSLA", "META", "GOOGL", "AMZN",
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
            macd = self._get_indicator(data, sym, "macd", date)
            macd_sig = self._get_indicator(data, sym, "macd_signal", date)
            volume = self._get_indicator(data, sym, "Volume", date)
            vol_avg = self._get_indicator(data, sym, "volume_sma_20", date)

            if any(v is None for v in [sma20, sma50, rsi, macd, macd_sig]):
                continue

            # Extreme contrarian: fade if RSI > 85 (exhaustion)
            if rsi > 85:
                weights[sym] = 0.0
                continue

            # Reflexive momentum: accelerating trend with volume confirmation
            trend_strength = 0.0
            if price > sma20 > sma50:
                trend_strength += 2.0
            elif price > sma20:
                trend_strength += 1.0

            if macd > macd_sig and macd > 0:
                trend_strength += 1.0

            # Volume confirmation (Soros loves conviction)
            if volume and vol_avg and vol_avg > 0:
                vol_ratio = volume / vol_avg
                if vol_ratio > 1.5:
                    trend_strength += 1.0

            if trend_strength >= 3:
                scored.append((sym, trend_strength))

        # Concentrated: take only top 5, heavy weights
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            total_score = sum(s for _, s in top)
            for sym, score in top:
                weights[sym] = (score / total_score) * 0.95
            # Post-clip normalization: redistribute freed allocation
            clipped = {s: min(w, self.config.max_position_size) for s, w in weights.items() if w > 0}
            clip_total = sum(clipped.values())
            if clip_total > 0 and clip_total < 0.90:
                scale = 0.95 / clip_total
                clipped = {s: min(w * scale, self.config.max_position_size) for s, w in clipped.items()}
            weights.update(clipped)

        return weights


# ---------------------------------------------------------------------------
# 4. Michael Burry — Deep Value Contrarian
# ---------------------------------------------------------------------------
class MichaelBurry(BasePersona):
    """Michael Burry deep value contrarian strategy.

    Source: "The Big Short" documented approach, Scion Capital letters

    Key principles:
    - Deep value: buy when everyone else is selling
    - Contrarian: go against market consensus
    - Focus on tangible book value and cash flows
    - Willing to hold losing positions for years
    - Famous for: subprime short, water investments, GameStop early

    Implementation:
    - Buy deeply oversold stocks (RSI < 25, price well below SMA200)
    - Prefer high-volume selloffs (capitulation = opportunity)
    - Very patient: monthly rebalancing, let positions work
    - Avoid momentum — specifically buy what's hated
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Michael Burry (Contrarian)",
            description="Deep value contrarian: buy capitulation, bet against consensus",
            risk_tolerance=0.6,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="monthly",
            # Mix of beaten-down sectors and individual names
            universe=universe or [
                "AAPL", "GOOGL", "META", "AMZN", "CVX", "XOM",
                "JNJ", "PFE", "BAC", "C", "GS", "WFC",
                "INTC", "IBM", "T", "VZ", "DIS", "PYPL",
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
            bb_lower = self._get_indicator(data, sym, "bb_lower", date)
            volume = self._get_indicator(data, sym, "Volume", date)
            vol_avg = self._get_indicator(data, sym, "volume_sma_20", date)

            if any(v is None for v in [sma200, rsi]):
                continue

            # Deep value: significant discount to SMA200
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            if discount > 0.10 and rsi < 35:
                # Capitulation score: deeper discount + more oversold + high volume
                score = discount * 10 + (35 - rsi) / 35
                if volume and vol_avg and vol_avg > 0:
                    vol_ratio = volume / vol_avg
                    if vol_ratio > 2:
                        score *= 1.5  # Volume capitulation bonus

                candidates.append((sym, score))

            # Also buy if at Bollinger lower band + deeply oversold
            elif bb_lower is not None and price < bb_lower and rsi < 25:
                score = (bb_lower - price) / bb_lower * 10 + 0.5
                candidates.append((sym, score))

            # Take profits on recovery (Burry takes profits)
            if rsi > 70 and discount < -0.15:
                weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]

        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 5. Jim Simons — Pure Quant (Factor Combination)
# ---------------------------------------------------------------------------
class JimSimons(BasePersona):
    """Jim Simons / Renaissance Technologies quant factor strategy.

    Source: "The Man Who Solved the Market" (2019), RenTech known approach

    Key principles:
    - Pure systematic, no discretion
    - Combine multiple weak signals into strong composite
    - Mean-reversion on short timeframes + momentum on medium timeframes
    - Risk management: diversify across many positions
    - Trade frequently, capture small edges consistently

    Implementation:
    - Composite factor: momentum (medium-term) + mean-reversion (short-term)
    - RSI mean-reversion: buy oversold, sell overbought
    - MACD momentum: trend confirmation
    - Volatility-adjusted position sizing
    - Daily rebalancing, many positions
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Jim Simons (Quant Factors)",
            description="Pure systematic: multi-factor composite, vol-weighted, daily rebalance",
            risk_tolerance=0.5,
            max_position_size=0.10,
            max_positions=15,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA",
                "JPM", "BAC", "GS", "XOM", "CVX", "JNJ", "PG",
                "KO", "WMT", "HD", "V", "MA", "UNH",
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
            macd = self._get_indicator(data, sym, "macd", date)
            macd_sig = self._get_indicator(data, sym, "macd_signal", date)
            bb_upper = self._get_indicator(data, sym, "bb_upper", date)
            bb_lower = self._get_indicator(data, sym, "bb_lower", date)
            vol = self._get_indicator(data, sym, "vol_20", date)

            if any(v is None for v in [sma20, sma50, rsi, macd, macd_sig, vol]):
                continue

            # Factor 1: Mean-reversion (RSI z-score)
            rsi_z = (rsi - 50) / 25  # Normalize RSI to roughly [-2, 2]
            mr_signal = -rsi_z  # Buy oversold, sell overbought

            # Factor 2: Momentum (MACD relative to signal)
            macd_diff = macd - macd_sig
            # Normalize by price level
            mom_signal = macd_diff / price * 1000 if price > 0 else 0

            # Factor 3: Trend (price vs SMAs)
            trend_signal = 0.0
            if price > sma20:
                trend_signal += 0.5
            if sma20 > sma50:
                trend_signal += 0.5

            # Factor 4: Bollinger band position
            if bb_upper is not None and bb_lower is not None and bb_upper != bb_lower:
                bb_pos = (price - bb_lower) / (bb_upper - bb_lower)
                bb_signal = 1 - 2 * bb_pos  # -1 at upper, +1 at lower
            else:
                bb_signal = 0

            # Composite: weighted combination
            composite = (
                0.30 * mr_signal +      # Mean reversion
                0.25 * mom_signal +      # Momentum
                0.25 * trend_signal +    # Trend
                0.20 * bb_signal         # Bollinger
            )

            if composite > 0.1:
                scored.append((sym, composite, vol))
            elif composite < -0.3:
                weights[sym] = 0.0  # Exit negative composite

        # Vol-weighted sizing
        if scored:
            scored.sort(key=lambda x: x[1], reverse=True)
            top = scored[:self.config.max_positions]
            total_inv_vol = sum(1 / max(v, 0.005) for _, _, v in top)
            for sym, score, vol in top:
                inv_vol = 1 / max(vol, 0.005)
                raw_w = (inv_vol / total_inv_vol) * 0.90
                weights[sym] = min(raw_w, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# 6. Carl Icahn — Activist Value
# ---------------------------------------------------------------------------
class CarlIcahn(BasePersona):
    """Carl Icahn activist value strategy.

    Source: Icahn Enterprises 13F filings, public letters

    Key principles:
    - Buy undervalued large caps with catalysts
    - Target companies with poor management (proxy for: beaten down)
    - Concentrated portfolio (5-8 positions)
    - Patient: hold for years if needed
    - Takes large positions to influence (we buy dips)

    Implementation:
    - Buy large caps that are deeply discounted (>20% below SMA200)
    - Prefer those starting to recover (RSI turning up from <30)
    - Concentrated positions, patient monthly rebalance
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Carl Icahn (Activist Value)",
            description="Concentrated deep value: buy beaten-down large caps showing recovery",
            risk_tolerance=0.5,
            max_position_size=0.25,
            max_positions=6,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "META", "AMZN", "GOOGL",
                "XOM", "CVX", "OXY", "DVN",
                "JPM", "BAC", "C", "GS",
                "PFE", "BMY", "ABBV",
                "DIS", "NFLX", "T",
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

            if any(v is None for v in [sma200, rsi]):
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            # Deep value + recovery signal
            if discount > 0.15 and rsi < 45:
                # Recovery bonus: RSI rising from very oversold
                recovery = max(0, rsi - 20) / 25  # Higher when recovering from <20
                score = discount * 5 + recovery
                candidates.append((sym, score))

            # Take profits at fair value
            if discount < -0.10 and rsi > 65:
                weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]

        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 7. Masayoshi Son — Vision Fund style (high-conviction tech bets)
# ---------------------------------------------------------------------------
class MasayoshiSon(BasePersona):
    """Masayoshi Son / SoftBank Vision Fund strategy.

    Source: SoftBank Vision Fund public portfolio, Son's documented approach

    Key principles (adapted for public markets):
    - Bet big on technology platform companies
    - "300-year vision" — extreme long-term conviction
    - Concentrated in disruptive tech at any price
    - Accept high volatility for potential massive returns
    - Famous for: early Alibaba bet, WeWork, ARM

    Implementation:
    - Buy tech leaders showing strong momentum (price > SMA50)
    - Very concentrated: top 5 highest-momentum tech names
    - Hold through volatility (wide stop at SMA200)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Masayoshi Son (Vision Fund)",
            description="High-conviction tech platform bets: concentrated, momentum-driven",
            risk_tolerance=0.95,
            max_position_size=0.25,
            max_positions=5,
            rebalance_frequency="monthly",
            universe=universe or [
                "NVDA", "TSLA", "AMZN", "GOOGL", "META", "MSFT",
                "AAPL", "CRM", "SHOP", "SQ", "PLTR", "COIN",
                "ARM", "SNOW", "DDOG", "NET",
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

            if any(v is None for v in [sma50, sma200]):
                continue

            # Exit if thesis broken (below SMA200)
            if price < sma200 * 0.90:
                weights[sym] = 0.0
                continue

            # Score by momentum strength
            if price > sma50:
                momentum = (price - sma50) / sma50
                score = momentum * 10
                if sma50 > sma200:
                    score += 2  # Trend alignment bonus
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.95 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 8. Li Ka-shing — Asian conglomerate / infrastructure value
# ---------------------------------------------------------------------------
class LiKaShing(BasePersona):
    """Li Ka-shing (CK Hutchison) infrastructure value strategy.

    Source: CK Hutchison portfolio, documented approach in HK business press

    Key principles:
    - Infrastructure and utility assets for steady cash flows
    - Value orientation: buy assets others overlook
    - Geographic diversification (we use international ETFs)
    - Real estate, ports, telecom, utilities
    - Very patient: decades-long holding periods

    Implementation:
    - Utility, infrastructure, and REIT ETFs + blue chips
    - Buy when trading below SMA200 (value)
    - Very low turnover, focus on yield
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Li Ka-shing (Infrastructure Value)",
            description="Patient infrastructure/utility value: steady cash flows, geographic diversity",
            risk_tolerance=0.2,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "XLU", "XLRE", "VNQ", "O", "AMT", "PLD",
                "NEE", "DUK", "SO", "T", "VZ",
                "EEM", "VEA", "EFA",  # International exposure
                "BND", "TIP",  # Fixed income stability
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

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            # Buy steady assets on discount
            if discount >= 0:  # At or below SMA200
                score = max(discount, 0.01)
                if rsi is not None and rsi < 40:
                    score += 0.1
                candidates.append((sym, score + 0.3))  # Base ensures we hold

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 9. Nassef Sawiris — Emerging markets conglomerate value
# ---------------------------------------------------------------------------
class NassefSawiris(BasePersona):
    """Nassef Sawiris (OCI, Orascom) emerging markets value strategy.

    Source: Sawiris family public investments (Adidas, LafargeHolcim, OCI)

    Key principles:
    - Value investing in global industrials and materials
    - Emerging market exposure through multinational companies
    - Concentrated positions in undervalued blue chips
    - Focus on construction, materials, chemicals, fertilizers

    Implementation:
    - Industrial, materials, and EM-exposed blue chips
    - Buy on deep discount to SMA200 + RSI recovery
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Nassef Sawiris (EM Industrials)",
            description="Emerging market industrials: materials, construction, global value",
            risk_tolerance=0.5,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "XLB", "XLI", "EEM", "VWO",  # Sectors + EM ETFs
                "NUE", "FCX", "VALE", "BHP",  # Materials/mining
                "CAT", "DE",  # Industrials
                "DOW", "LIN",  # Chemicals
                "NKE", "ADDYY",  # Consumer (Sawiris owns Adidas stake)
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
            if any(v is None for v in [sma200, rsi]):
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0
            if discount > 0.05 and rsi < 45:
                score = discount * 5 + (45 - rsi) / 45
                candidates.append((sym, score))
            elif rsi > 70 and discount < -0.15:
                weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 10. Jorge Paulo Lemann — Brazilian 3G Capital style
# ---------------------------------------------------------------------------
class JorgePauloLemann(BasePersona):
    """Jorge Paulo Lemann / 3G Capital strategy.

    Source: 3G Capital public portfolio (AB InBev, Kraft Heinz, Burger King/RBI)

    Key principles:
    - Buy dominant consumer brands at reasonable prices
    - Focus on cost-cutting and operational efficiency (proxy: buy dips)
    - Very concentrated in consumer staples and restaurants
    - Long-term hold, patient entry on weakness

    Implementation:
    - Consumer staples + restaurant/fast-food chains
    - Buy on pullback to SMA50 with moderate RSI
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Jorge Paulo Lemann (3G Capital)",
            description="Consumer brand dominance: buy great brands on weakness, concentrate",
            risk_tolerance=0.3,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "KO", "PEP", "MCD", "QSR", "YUM", "SBUX",
                "PG", "KHC", "BUD", "DEO", "UL", "CL",
                "WMT", "COST", "TGT",
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
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            if any(v is None for v in [sma50, sma200, rsi]):
                continue

            # Buy great brands on pullback
            if price > sma200 and rsi < 50:
                proximity = abs(price - sma50) / sma50 if sma50 > 0 else 1.0
                if proximity < 0.05:  # Near SMA50 support
                    score = 2.0 + (50 - rsi) / 50
                    candidates.append((sym, score))
                elif price > sma50:
                    candidates.append((sym, 1.0))

            if rsi > 75:
                weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 11. Prince Alwaleed bin Talal — Middle Eastern tech/finance investor
# ---------------------------------------------------------------------------
class PrinceAlwaleed(BasePersona):
    """Prince Alwaleed bin Talal (Kingdom Holding) strategy.

    Source: Kingdom Holding public portfolio, Bloomberg filings

    Key principles:
    - Global blue-chip investor (Citigroup, Twitter, Four Seasons)
    - Mix of US tech + financials + luxury hospitality
    - Buy iconic brands during crises at distressed prices
    - Famous for: early Citigroup investment, Twitter pre-IPO

    Implementation:
    - US financials + tech giants + luxury consumer
    - Contrarian: buy on crisis (deep RSI + volume spike)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Prince Alwaleed (Kingdom Holding)",
            description="Global blue-chip contrarian: buy iconic brands during crises",
            risk_tolerance=0.5,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "C", "JPM", "BAC", "GS",  # Financials (Citigroup focus)
                "AAPL", "MSFT", "GOOGL", "META",  # Tech giants
                "LVMUY", "MAR", "HLT",  # Luxury/hospitality
                "DIS", "NFLX",  # Entertainment
                "V", "MA",  # Payment networks
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
            volume = self._get_indicator(data, sym, "Volume", date)
            vol_avg = self._get_indicator(data, sym, "volume_sma_20", date)
            if any(v is None for v in [sma200, rsi]):
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            # Crisis buying: deep discount + oversold + high volume
            if discount > 0.10 and rsi < 35:
                score = discount * 8
                if volume and vol_avg and vol_avg > 0 and volume / vol_avg > 2:
                    score *= 1.5  # Crisis volume
                candidates.append((sym, score))
            # Also accumulate blue chips on moderate dips
            elif discount > 0 and rsi < 45:
                candidates.append((sym, discount * 3))
            elif rsi > 70 and discount < -0.15:
                weights[sym] = 0.0

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 12. Howard Marks — Oaktree Capital distressed/contrarian
# ---------------------------------------------------------------------------
class HowardMarks(BasePersona):
    """Howard Marks / Oaktree Capital contrarian strategy.

    Source: "The Most Important Thing" (2011), Oaktree memos

    Key principles:
    - "Second-level thinking" — go against consensus when it's wrong
    - Buy when others are fearful (high VIX, oversold markets)
    - Focus on credit quality cycle (we proxy with HY spread behavior)
    - Risk control is #1 — avoid losing money
    - "You can't predict, you can prepare"

    Implementation:
    - Buy beaten-down quality stocks when VIX proxy (vol) is high
    - Prefer names with low vol that are temporarily oversold
    - Very conservative position sizing
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Howard Marks (Oaktree Contrarian)",
            description="Second-level thinking: buy quality when others panic, control risk",
            risk_tolerance=0.3,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "JNJ", "PG", "KO",
                "JPM", "V", "UNH", "HD",
                "BRK-B", "ABBV", "MRK", "PFE",
                "HYG", "LQD", "BND",  # Credit proxies
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        # Check if market is in fear mode (proxy: broad vol)
        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)
        if spy_vol is None:
            # Fallback: use first available universe symbol's vol
            for _sym in self.config.universe:
                spy_vol = self._get_indicator(data, _sym, "vol_20", date)
                if spy_vol is not None:
                    break
        fear_mode = spy_vol is not None and spy_vol > 0.02  # High daily vol

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            vol = self._get_indicator(data, sym, "vol_20", date)
            if any(v is None for v in [sma200, rsi]):
                continue

            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            # Risk control: exit if thesis breaking (>20% below SMA200)
            if price < sma200 * 0.80:
                weights[sym] = 0.0
                continue

            # Second-level thinking: buy when others panic
            if fear_mode and discount > 0.05 and rsi < 40:
                # Prefer low-vol names (quality) that are temporarily oversold
                vol_penalty = vol if vol is not None else 0.02
                quality_score = (1 / max(vol_penalty, 0.005)) * discount
                candidates.append((sym, quality_score))
            elif not fear_mode and discount > 0.15 and rsi < 30:
                # Even in calm markets, buy extreme fear in individual names
                candidates.append((sym, discount * 3))

        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 13. Support/Resistance Commodity Trader
# ---------------------------------------------------------------------------
class SupportResistanceCommodity(BasePersona):
    """Support/resistance breakout strategy for commodity ETFs.

    Key principles:
    - Identify support (SMA200, recent lows) and resistance (recent highs, BB upper)
    - Buy breakouts above resistance with volume confirmation
    - Short/exit breakdowns below support
    - ATR-based stop-losses for defined risk
    - Commodities trend well due to supply/demand cycles

    Implementation:
    - Commodity ETFs: gold (GLD), oil (USO/XLE), agriculture (DBA), metals (SLV)
    - Buy: Price breaks above BB upper + RSI 55-75 + volume > 1.5x avg
    - Sell: Price breaks below BB lower or SMA200
    - Position size based on ATR (wider ATR = smaller position)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Support/Resistance Commodity",
            description="Breakout trading on commodity ETFs with defined S/R levels and ATR stops",
            risk_tolerance=0.6,
            max_position_size=0.20,
            max_positions=6,
            rebalance_frequency="daily",
            universe=universe or [
                "GLD", "SLV", "XLE", "XOP",  # Gold, Silver, Energy
                "XLB", "DBA", "WEAT",  # Materials, Agriculture
                "UNG", "COPX", "CPER",  # Nat gas, Copper
                "FCX", "NEM", "GOLD",  # Mining stocks
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
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            sma50 = self._get_indicator(data, sym, "sma_50", date)
            bb_upper = self._get_indicator(data, sym, "bb_upper", date)
            bb_lower = self._get_indicator(data, sym, "bb_lower", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            atr = self._get_indicator(data, sym, "atr_14", date)
            volume = self._get_indicator(data, sym, "Volume", date)
            vol_avg = self._get_indicator(data, sym, "volume_sma_20", date)

            if any(v is None for v in [sma200, bb_upper, bb_lower, rsi]):
                continue

            # Breakdown below support — EXIT
            if price < bb_lower and rsi < 30:
                weights[sym] = 0.0
                continue
            if price < sma200 * 0.95:
                weights[sym] = 0.0
                continue

            # Breakout above resistance — BUY
            vol_ratio = volume / vol_avg if volume and vol_avg and vol_avg > 0 else 1
            if price > bb_upper and 55 < rsi < 80 and vol_ratio > 1.3:
                # Breakout with volume confirmation
                score = 3.0 + vol_ratio
                # ATR-based sizing: wider ATR = smaller position (risk normalization)
                if atr is not None and atr > 0:
                    atr_pct = atr / price
                    score *= (0.02 / max(atr_pct, 0.005))  # Prefer low-ATR breakouts
                scored.append((sym, score))

            # Bounce off support — BUY (support test)
            elif sma50 is not None and sma50 > 0 and abs(price - sma50) / sma50 < 0.02 and rsi < 45:
                score = 1.5
                if vol_ratio > 1.2:
                    score += 0.5
                scored.append((sym, score))

            # Trending above both MAs — HOLD/accumulate
            elif sma50 is not None and price > sma50 > sma200 and rsi < 70:
                scored.append((sym, 1.0))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            total_score = sum(s for _, s in top)
            for sym, score in top:
                weights[sym] = (score / total_score) * 0.90
            # Post-clip normalization: redistribute freed allocation
            clipped = {s: min(w, self.config.max_position_size) for s, w in weights.items() if w > 0}
            clip_total = sum(clipped.values())
            if clip_total > 0 and clip_total < 0.85:
                scale = 0.90 / clip_total
                clipped = {s: min(w * scale, self.config.max_position_size) for s, w in clipped.items()}
            weights.update(clipped)

        return weights


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
FAMOUS_INVESTORS = {
    "peter_lynch": PeterLynch,
    "ray_dalio": RayDalio,
    "george_soros": GeorgeSoros,
    "michael_burry": MichaelBurry,
    "jim_simons": JimSimons,
    "carl_icahn": CarlIcahn,
    "masayoshi_son": MasayoshiSon,
    "li_ka_shing": LiKaShing,
    "nassef_sawiris": NassefSawiris,
    "jorge_paulo_lemann": JorgePauloLemann,
    "prince_alwaleed": PrinceAlwaleed,
    "howard_marks": HowardMarks,
    "support_resistance": SupportResistanceCommodity,
}


def get_famous_investor(name: str, **kwargs) -> BasePersona:
    cls = FAMOUS_INVESTORS.get(name)
    if cls is None:
        raise ValueError(f"Unknown investor: {name}. Available: {list(FAMOUS_INVESTORS.keys())}")
    return cls(**kwargs)


def list_famous_investors():
    result = []
    for key, cls in FAMOUS_INVESTORS.items():
        instance = cls()
        result.append({
            "key": key,
            "name": instance.config.name,
            "description": instance.config.description,
        })
    return result


if __name__ == "__main__":
    print("=== Famous Investor Personas ===\n")
    for p in list_famous_investors():
        print(f"  {p['key']:20s} | {p['name']:30s} | {p['description']}")

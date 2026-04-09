"""Unconventional and less obvious trading strategies for agents-assemble.

These go beyond the standard momentum/value playbook into more
creative and contrarian approaches.

Strategies:
    1. SellInMayGoAway    — Seasonal "sell in May" calendar effect
    2. TurnOfMonth        — End-of-month/start-of-month buying window
    3. VIXMeanReversion   — Buy stocks when VIX spikes (fear = opportunity)
    4. DogsOfTheDow       — Buy worst performers yearly (contrarian)
    5. QualityFactor      — Low vol + high profitability + low leverage
    6. TailRiskHarvest    — Sell premium (proxy: buy after sharp drops)
"""

from __future__ import annotations


_SQRT_252 = 252 ** 0.5


def _is_missing(v):
    """Check if value is None or NaN."""
    return v is None or v != v


from personas import BasePersona, PersonaConfig


# ---------------------------------------------------------------------------
# 1. Sell in May and Go Away (Halloween Effect)
# ---------------------------------------------------------------------------
class SellInMayGoAway(BasePersona):
    """Seasonal calendar strategy: "Sell in May and go away."

    Historical evidence: Nov-Apr returns >> May-Oct returns.
    Source: Bouman & Jacobsen (2002) "The Halloween Indicator"

    Implementation:
    - Nov 1 to Apr 30: 100% in SPY/QQQ
    - May 1 to Oct 31: Move to bonds (TLT/IEF) or cash (SHY)
    - Simple but historically robust across many markets
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Sell in May (Halloween Effect)",
            description="Seasonal: stocks Nov-Apr, bonds May-Oct",
            risk_tolerance=0.4,
            max_position_size=0.50,
            max_positions=4,
            rebalance_frequency="monthly",
            universe=universe or ["SPY", "QQQ", "TLT", "IEF", "SHY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        month = date.month

        if month >= 11 or month <= 4:
            # "Winter" = stocks
            raw = {
                "SPY": 0.50,
                "QQQ": 0.40,
                "TLT": 0.0,
                "IEF": 0.0,
                "SHY": 0.0,
            }
        else:
            # "Summer" = bonds/cash
            raw = {
                "SPY": 0.0,
                "QQQ": 0.0,
                "TLT": 0.30,
                "IEF": 0.30,
                "SHY": 0.30,
            }
        return {k: v for k, v in raw.items() if k in prices}


# ---------------------------------------------------------------------------
# 2. Turn of Month Effect
# ---------------------------------------------------------------------------
class TurnOfMonth(BasePersona):
    """Turn-of-month buying window.

    Research shows the last 3 trading days + first 3 trading days of
    each month account for most of the monthly return due to cash flows
    (pension funds, paychecks, portfolio rebalancing).

    Source: Ariel (1987), Lakonishok & Smidt (1988)

    Implementation:
    - Buy SPY/QQQ on day 26+ of month and hold through day 3 of next month
    - Move to SHY/cash for the rest of the month
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Turn of Month Effect",
            description="Buy last 3 + first 3 days of month, cash otherwise",
            risk_tolerance=0.3,
            max_position_size=0.50,
            max_positions=3,
            rebalance_frequency="daily",
            universe=universe or ["SPY", "QQQ", "SHY"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        day = date.day

        if day >= 26 or day <= 3:
            # Turn of month window — be in stocks
            raw = {
                "SPY": 0.50,
                "QQQ": 0.40,
                "SHY": 0.0,
            }
        else:
            # Mid-month — park in short-term treasuries
            raw = {
                "SPY": 0.0,
                "QQQ": 0.0,
                "SHY": 0.90,
            }
        return {k: v for k, v in raw.items() if k in prices}


# ---------------------------------------------------------------------------
# 3. VIX Mean Reversion (Buy the Fear)
# ---------------------------------------------------------------------------
class VIXMeanReversion(BasePersona):
    """Buy stocks when VIX spikes (fear = opportunity).

    Research: VIX mean-reverts. Spikes above 30 are historically
    followed by strong equity returns (Whaley 2000).

    Implementation (using SPY volatility as VIX proxy since we don't
    have VIX directly):
    - When realized vol spikes > 2x 60-day average → aggressively buy
    - When vol is low → normal allocation
    - When vol is extremely low → reduce (complacency risk)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="VIX Mean Reversion (Buy Fear)",
            description="Buy aggressively when volatility spikes, reduce when complacent",
            risk_tolerance=0.6,
            max_position_size=0.35,
            max_positions=5,
            rebalance_frequency="daily",
            universe=universe or [
                "SPY", "QQQ", "IWM",  # Broad market
                "TLT", "GLD",  # Safe havens
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        spy_vol = self._get_indicator(data, "SPY", "vol_20", date)

        if _is_missing(spy_vol):
            fallback = {"SPY": 0.30, "QQQ": 0.20, "TLT": 0.20, "GLD": 0.10}
            return {k: v for k, v in fallback.items() if k in prices}

        # Estimate VIX from realized vol (rough: annualized * 100)
        implied_vix = spy_vol * _SQRT_252 * 100

        if implied_vix > 30:
            # High fear — BUY aggressively (VIX will mean-revert)
            weights["SPY"] = 0.40
            weights["QQQ"] = 0.30
            weights["IWM"] = 0.20
            weights["TLT"] = 0.0
            weights["GLD"] = 0.0
        elif implied_vix > 20:
            # Moderate fear — balanced
            weights["SPY"] = 0.30
            weights["QQQ"] = 0.20
            weights["TLT"] = 0.15
            weights["GLD"] = 0.10
            weights["IWM"] = 0.10
        elif implied_vix < 12:
            # Very low vol — complacency, reduce and hedge
            weights["SPY"] = 0.15
            weights["QQQ"] = 0.10
            weights["TLT"] = 0.25
            weights["GLD"] = 0.20
            weights["IWM"] = 0.0
        else:
            # Normal vol
            weights["SPY"] = 0.25
            weights["QQQ"] = 0.20
            weights["TLT"] = 0.15
            weights["GLD"] = 0.10
            weights["IWM"] = 0.10

        return {k: v for k, v in weights.items() if k in prices}


# ---------------------------------------------------------------------------
# 4. Dogs of the Dow (Contrarian Yearly)
# ---------------------------------------------------------------------------
class DogsOfTheDow(BasePersona):
    """Dogs of the Dow contrarian strategy.

    Source: Michael O'Higgins, "Beating the Dow" (1991)

    Buy the 10 highest-yielding Dow stocks at start of year.
    Proxy: buy the worst-performing stocks (highest discount to SMA200)
    from blue-chip universe at each rebalance, equal weight.
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Dogs of the Dow (Contrarian)",
            description="Buy worst-performing blue chips yearly, contrarian equal-weight",
            risk_tolerance=0.4,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            # Dow 30 components (approximate)
            universe=universe or [
                "AAPL", "MSFT", "AMZN", "UNH", "GS", "HD", "MCD",
                "V", "CRM", "DIS", "NKE", "BA", "CAT", "JPM",
                "IBM", "JNJ", "KO", "PG", "WMT", "MRK",
                "MMM", "CVX", "DOW", "INTC", "VZ",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        discount_scores = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            if _is_missing(sma200) or sma200 <= 0:
                continue

            discount = (sma200 - price) / sma200
            discount_scores.append((sym, discount))

        # Sort by discount (highest = furthest below SMA200 = "dogs")
        discount_scores.sort(key=lambda x: x[1], reverse=True)

        # Take the 10 "worst" performers (highest discount = most beaten down)
        dogs = discount_scores[:self.config.max_positions]

        if dogs:
            per_stock = min(0.90 / len(dogs), self.config.max_position_size)
            for sym, _ in dogs:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 5. Quality Factor (Buffett + Quant Hybrid)
# ---------------------------------------------------------------------------
class QualityFactor(BasePersona):
    """Quality factor: low volatility + strong trend = quality.

    Source: AQR "Quality Minus Junk" (Asness, Frazzini, Pedersen 2019)

    Buy stocks that are:
    - Low volatility (stable earnings proxy)
    - Above SMA200 (quality doesn't break down)
    - Not overbought (RSI < 70)
    - Moderate momentum (not hot, not cold)
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Quality Factor (Low Vol + Trend)",
            description="Buy low-vol stocks in uptrends — quality minus junk",
            risk_tolerance=0.3,
            max_position_size=0.10,
            max_positions=15,
            rebalance_frequency="monthly",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "JNJ", "PG", "KO", "PEP",
                "V", "MA", "UNH", "HD", "MCD", "COST", "ABT",
                "LLY", "TMO", "ACN", "AVGO", "TXN", "LIN",
                "BRK-B", "WMT", "NEE", "DUK",
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
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            vol = self._get_indicator(data, sym, "vol_20", date)
            sma50 = self._get_indicator(data, sym, "sma_50", date)

            if any(_is_missing(v) for v in [sma200, rsi, vol]):
                continue

            # Quality filters
            if price < sma200:
                continue  # Must be above long-term trend
            if rsi > 70:
                continue  # Not overbought
            if vol > 0.025:
                continue  # Not too volatile (daily vol < 2.5%)

            # Score: inverse of volatility * trend alignment
            trend_bonus = 1.0
            if sma50 is not None and price > sma50:
                trend_bonus = 1.3

            quality_score = (1 / max(vol, 0.005)) * trend_bonus
            scored.append((sym, quality_score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 6. Tail Risk Harvest (Buy After Sharp Drops)
# ---------------------------------------------------------------------------
class TailRiskHarvest(BasePersona):
    """Buy after sharp single-day drops in quality names.

    Research: Large single-day drops in blue chips tend to
    mean-revert over 5-20 trading days (overreaction effect).

    Implementation:
    - Track daily returns
    - Buy when a quality stock drops > 3% in a day with high volume
    - Hold for ~20 trading days, then re-evaluate
    """

    def __init__(self, universe: list[str] | None = None):
        config = PersonaConfig(
            name="Tail Risk Harvest (Buy Crashes)",
            description="Buy quality names after sharp single-day drops, capture mean-reversion",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META",
                "JPM", "V", "MA", "UNH", "JNJ", "PG",
                "HD", "MCD", "KO", "WMT",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        crash_buys = []

        for sym in self.config.universe:
            if sym not in prices:
                continue
            price = prices[sym]
            daily_ret = self._get_indicator(data, sym, "daily_return", date)
            sma200 = self._get_indicator(data, sym, "sma_200", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            volume = self._get_indicator(data, sym, "Volume", date)
            vol_avg = self._get_indicator(data, sym, "volume_sma_20", date)

            if _is_missing(daily_ret):
                continue

            # Exit recovered positions (RSI > 60 = recovered from crash)
            if rsi is not None and rsi > 65 and sma200 is not None and price > sma200:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                    continue  # Don't consider for crash buy

            # Crash buy signal: sharp drop + above SMA200 (still quality)
            if daily_ret < -0.03:  # > 3% drop
                vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
                if sma200 is not None and price > sma200 * 0.90:
                    # Quality + crash = buy
                    score = abs(daily_ret) * 10
                    if vol_ratio > 2:
                        score *= 1.5  # Panic selling = better opportunity
                    crash_buys.append((sym, score))

        crash_buys.sort(key=lambda x: x[1], reverse=True)
        top = crash_buys[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------
# ---------------------------------------------------------------------------
# 7. Dividend Aristocrat Momentum
# ---------------------------------------------------------------------------
class DividendAristocratMomentum(BasePersona):
    """Combine Dividend Aristocrats with momentum filtering.

    Thesis: Aristocrats provide quality (25+ years of div growth).
    Momentum filter selects the ones trending up. This avoids
    the "value trap" problem of pure dividend investing.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Dividend Aristocrat Momentum",
            description="Quality dividends + momentum: only buy Aristocrats in uptrends",
            risk_tolerance=0.3,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "JNJ", "PG", "KO", "PEP", "ABBV", "MRK", "ABT", "CL",
                "EMR", "ADP", "AFL", "APD", "CVX", "ECL", "GD", "ITW",
                "KMB", "LOW", "MCD", "NEE", "PPG", "SHW", "SYY", "TGT",
                "WMT", "XOM",
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
            if any(v is None for v in [sma50, sma200, rsi]):
                continue
            # Must be in uptrend (momentum filter)
            if price < sma200:
                continue
            # Score by trend strength
            score = 0.0
            if price > sma50 > sma200:
                score += 2.0
            elif price > sma50:
                score += 1.0
            if 35 < rsi < 65:
                score += 0.5  # Prefer not overbought
            # Bonus for being near SMA50 (buy on pullback in uptrend)
            if sma50 and abs(price - sma50) / sma50 < 0.03:
                score += 0.5
            if score > 1.0:
                scored.append((sym, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        return weights


# ---------------------------------------------------------------------------
# 8. Concentration in Winners
# ---------------------------------------------------------------------------
class ConcentrateWinners(BasePersona):
    """Let winners run, cut losers — extreme concentration.

    Thesis: A few stocks drive most market returns. Instead of
    diversifying equally, concentrate in the top 3-5 strongest
    momentum stocks. Higher risk but potentially higher returns.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Concentrate in Winners",
            description="Extreme concentration: top 3-5 strongest momentum stocks only",
            risk_tolerance=0.9,
            max_position_size=0.30,
            max_positions=5,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
                "AVGO", "LLY", "V", "MA", "UNH", "JPM", "HD",
                "NFLX", "CRM", "AMD", "PLTR", "CRWD",
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
            # Only the strongest momentum
            score = 0.0
            if price > sma50 > sma200:
                score += 3.0
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5
            if 50 < rsi < 80:
                score += 1.0
            # Momentum magnitude
            mom = (price - sma200) / sma200 if sma200 > 0 else 0
            score += mom * 5  # Weight by how far above SMA200
            if score >= 4:
                scored.append((sym, score))
            elif sma200 and price < sma200 * 0.95:
                weights[sym] = 0.0
        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            # Score-weighted allocation (more to strongest)
            total_score = sum(s for _, s in top)
            for sym, score in top:
                w = min((score / total_score) * 0.95, self.config.max_position_size)
                weights[sym] = w
        return weights


# ---------------------------------------------------------------------------
# 9. Hidden Monopoly Compounders — boring businesses with pricing power
# ---------------------------------------------------------------------------
class HiddenMonopoly(BasePersona):
    """Invest in companies with natural monopolies or duopolies in boring industries.

    These businesses have massive moats but get zero media attention:
    - Credit ratings (MCO, SPGI) — literally impossible to compete
    - Data monopolies (VRSK, ICE, MSCI) — mission-critical, no switching
    - Waste management (WM, RSG) — local monopolies, inflation-linked pricing
    - Railroads (CSX, NSC) — physically impossible to build competing rail
    - Elevator/HVAC installed base (OTIS, CARR, TT) — service contracts = recurring

    Edge: These compound intrinsic value 12-18% annually but trade at lower
    multiples than tech because they're "boring." The market systematically
    underprices predictability.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Hidden Monopoly Compounders",
            description="Natural monopolies in boring industries: credit ratings, data, waste, rail, HVAC",
            risk_tolerance=0.4,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                # Credit ratings duopoly
                "SPGI", "MCO",
                # Data/analytics monopolies
                "VRSK", "ICE", "MSCI", "FDS",
                # Waste monopolies
                "WM", "RSG",
                # Railroad monopolies
                "CSX", "NSC",
                # Installed-base HVAC/elevator
                "OTIS", "CARR", "TT",
                # Industrial distribution
                "FAST", "CTAS",
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
            vol = inds["vol_20"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Long-term uptrend (compounding)
            if price > sma200:
                score += 2.0
            if sma50 is not None and price > sma50:
                score += 1.0
            # Buy on pullbacks (RSI dip in uptrend = gift)
            if 30 < rsi < 50 and price > sma200:
                score += 2.0  # Pullback in uptrend = best entry
            elif 50 <= rsi < 65:
                score += 1.0
            # Low vol = stable compounder (good)
            if vol is not None and not _is_missing(vol) and vol < 0.015:
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
# 10. DCF Deep Value — stocks trading 30%+ below intrinsic value
# ---------------------------------------------------------------------------
class DCFDeepValue(BasePersona):
    """Buy mid/large caps trading far below DCF intrinsic value.

    Uses price-to-FCF and distance-from-highs as proxies for DCF discount
    (we can't compute DCF in real-time, but beaten-down FCF machines are
    statistically the same set).

    Universe: companies with high FCF yield that have sold off.
    Edge: Market overreacts to short-term earnings misses in high-FCF companies.
    The FCF keeps compounding even when the stock price doesn't.

    Includes: healthcare post-patent, consumer staples GLP-1 fear selloff,
    energy with massive buybacks, beaten-down industrials.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="DCF Deep Value (High FCF Discount)",
            description="Mid/large caps trading 30%+ below intrinsic value — high FCF, beaten-down prices",
            risk_tolerance=0.5,
            max_position_size=0.10,
            max_positions=15,
            rebalance_frequency="weekly",
            universe=universe or [
                # Consumer staples beaten down (GLP-1 fear overreaction)
                "MDLZ", "CAG", "SJM", "HRL", "CPB",
                # Healthcare FCF machines
                "DHR", "WAT", "ZTS", "IDXX",
                # Insurance float compounders
                "ALL", "PGR", "MKL", "CINF",
                # Payment infrastructure (depressed vs growth)
                "FIS", "GPN", "FISV",
                # Industrial FCF
                "DOV", "ROP", "TDY",
                # Boring but profitable
                "WST", "ODFL",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
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
            price = prices[sym]
            score = 0.0

            # Deep value: price significantly below SMA200 = potential DCF discount
            if price < sma200 * 0.90:
                score += 3.0  # >10% below long-term avg = deep value
            elif price < sma200:
                score += 1.5

            # RSI oversold = maximum pessimism
            if rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0

            # MACD turning up = reversal starting
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 1.5

            # Near lower Bollinger = statistical extreme
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 1.0

            # Only buy if there's actual value signal (not just trending down)
            if score >= 3.0:
                scored.append((sym, score))
            elif price > sma200:
                # Exited value zone — reduce or exit
                weights[sym] = 0.0

        scored.sort(key=lambda x: -x[1])
        top = scored[:self.config.max_positions]
        if top:
            total = sum(s for _, s in top)
            for sym, sc in top:
                weights[sym] = min((sc / total) * 0.95, self.config.max_position_size)
        return weights


# ---------------------------------------------------------------------------
# 11. Toll Booth Economy — companies that tax every transaction
# ---------------------------------------------------------------------------
class TollBoothEconomy(BasePersona):
    """Invest in companies that sit on critical infrastructure and collect fees.

    These are the "toll booths" of the modern economy:
    - Every credit card swipe: V, MA
    - Every stock trade: ICE, CME, NDAQ
    - Every insurance policy: SPGI, MCO rate it
    - Every building needs HVAC: OTIS, CARR
    - Every package shipped: ODFL, CHRW

    Edge: Transaction volumes grow with GDP. These companies have near-zero
    marginal cost per transaction. Revenue scales infinitely.
    Unlike tech, they don't need to reinvent themselves every 3 years.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Toll Booth Economy",
            description="Companies that tax every transaction: payments, exchanges, ratings, logistics",
            risk_tolerance=0.4,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                # Payment toll booths
                "V", "MA", "FISV", "GPN",
                # Exchange toll booths
                "ICE", "CME", "NDAQ",
                # Ratings toll booths
                "SPGI", "MCO",
                # Logistics toll booths
                "ODFL", "CHRW",
                # Testing/compliance toll booths
                "A", "VRSK",
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
            vol = inds["vol_20"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Uptrend = growing transaction volumes
            if price > sma200:
                score += 2.0
            if sma50 is not None and sma50 > sma200:
                score += 1.0  # Golden cross
            # Not overextended
            if 40 < rsi < 70:
                score += 1.0
            # Low vol = stable toll collector (exactly what we want)
            if vol is not None and not _is_missing(vol) and vol < 0.018:
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
# 12. Beaten Down Staples (GLP-1 Fear Overreaction)
# ---------------------------------------------------------------------------
class BeatenDownStaples(BasePersona):
    """Buy consumer staples crushed by GLP-1/Ozempic weight-loss drug fears.

    The market sold off snack, soda, fast food, and packaged food companies
    on fears that GLP-1 drugs will reduce calorie consumption. But:
    - GLP-1 penetration is <5% of population even in 2026
    - These companies have pricing power and adapt product lines
    - Dividend yields are now at 10-year highs
    - FCF is still growing

    Edge: Classic overreaction. The selloff priced in 100% GLP-1 adoption
    when real adoption is <5%. Buy the fear, collect the dividends.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Beaten Down Staples (GLP-1 Fear)",
            description="Consumer staples oversold on GLP-1 fears — buy the overreaction, collect dividends",
            risk_tolerance=0.3,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                # Snack/packaged food (hit hardest by GLP-1 fear)
                "MDLZ", "CAG", "SJM", "HRL", "CPB",
                # Soda (Pepsi/Coke hit by weight loss fears)
                "PEP", "KO",
                # Fast food/restaurants
                "MCD", "YUM", "DPZ",
                # Grocery/consumer
                "KR", "SYY",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14", "bb_lower"], date)
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            bb_low = inds["bb_lower"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Below SMA200 = fear territory (where we want to buy)
            if price < sma200 * 0.95:
                score += 3.0  # Deep discount to trend
            elif price < sma200:
                score += 1.5
            # RSI oversold = maximum fear
            if rsi < 35:
                score += 2.0
            elif rsi < 45:
                score += 1.0
            # Near Bollinger lower = statistical extreme
            if bb_low is not None and not _is_missing(bb_low) and price < bb_low * 1.02:
                score += 1.0
            # Recovery signal: if above SMA200, hold with momentum
            if price > sma200 and rsi > 50:
                score += 1.5

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
# 13. Insurance Float Compounders
# ---------------------------------------------------------------------------
class InsuranceFloat(BasePersona):
    """Invest in insurance companies that compound via float investing.

    Insurance companies collect premiums upfront and pay claims later.
    The "float" — premiums collected but not yet paid out — is essentially
    free leverage that they invest. Berkshire Hathaway pioneered this.

    Edge: Float grows with premiums (inflation-linked). Combined ratios <100%
    mean they're paid to hold your money. Market treats them as boring financials
    but they're actually leveraged investment vehicles.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Insurance Float Compounders",
            description="Insurance companies with massive float: paid to hold money, compound via investing",
            risk_tolerance=0.4,
            max_position_size=0.12,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "BRK-B",  # Berkshire Hathaway (the OG float compounder)
                "PGR",    # Progressive (auto insurance, 96% combined ratio)
                "ALL",    # Allstate
                "CB",     # Chubb (global, very profitable)
                "MKL",    # Markel (mini-Berkshire)
                "CINF",   # Cincinnati Financial (50+ year dividend growth)
                "AFL",    # Aflac (supplemental insurance, massive float)
                "WRB",    # Berkley (specialty insurance)
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []
        for sym in self.config.universe:
            if sym not in prices:
                continue
            inds = self._get_indicators(data, sym, ["sma_50", "sma_200", "rsi_14"], date)
            sma50 = inds["sma_50"]
            sma200 = inds["sma_200"]
            rsi = inds["rsi_14"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Uptrend = growing premiums + float
            if price > sma200:
                score += 2.0
            if sma50 is not None and price > sma50:
                score += 1.0
            # Buy dips in uptrend
            if 35 < rsi < 50 and price > sma200:
                score += 2.0
            elif 50 <= rsi < 65:
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
# 14. Boring Compounder 20% Club
# ---------------------------------------------------------------------------
class BoringCompounder(BasePersona):
    """Companies growing intrinsic value 15-20% annually in boring industries.

    These never make CNBC, never go viral on Reddit, never get mentioned
    by Cathie Wood. They just quietly compound wealth:
    - POOL: only national pool supply distributor
    - ODFL: best-in-class LTL freight (98% on-time)
    - CTAS: uniform rental monopoly
    - WST: pharmaceutical packaging (every vial needs a stopper)
    - ROP: vertical market software roll-up
    - FAST: industrial fastener distribution

    Edge: Boring = under-owned by retail = less volatile = better Sharpe.
    Institutional ownership is high but passive flows dominate, meaning
    mispricings persist longer.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Boring Compounder 20% Club",
            description="Quiet compounders in boring industries: pool supply, uniforms, fasteners, packaging",
            risk_tolerance=0.3,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="monthly",
            universe=universe or [
                "POOL",  # Pool supply distribution monopoly
                "ODFL",  # Best LTL freight carrier
                "CTAS",  # Uniform rental
                "WST",   # Pharma packaging
                "ROP",   # Vertical software roll-up
                "FAST",  # Industrial fasteners
                "TDY",   # Defense/instrumentation
                "IDXX",  # Veterinary diagnostics monopoly
                "CLH",   # Hazardous waste (Clean Harbors)
                "LII",   # HVAC (Lennox)
                "WSO",   # HVAC distribution (Watsco)
                "MORN",  # Morningstar (investment research monopoly)
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
            vol = inds["vol_20"]
            if _is_missing(sma200) or _is_missing(rsi):
                continue
            price = prices[sym]
            score = 0.0
            # Must be in uptrend (compounders trend up)
            if price > sma200:
                score += 2.0
            else:
                continue  # Don't buy broken compounders
            if sma50 is not None and price > sma50:
                score += 1.0
            # Buy pullbacks aggressively (these always recover)
            if 30 < rsi < 45:
                score += 2.5  # Deep pullback in compounder = best entry
            elif 45 <= rsi < 60:
                score += 1.0
            # Low vol = stable compounder
            if vol is not None and not _is_missing(vol) and vol < 0.015:
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


UNCONVENTIONAL_STRATEGIES = {
    "sell_in_may": SellInMayGoAway,
    "turn_of_month": TurnOfMonth,
    "vix_mean_reversion": VIXMeanReversion,
    "dogs_of_dow": DogsOfTheDow,
    "quality_factor": QualityFactor,
    "tail_risk_harvest": TailRiskHarvest,
    "dividend_aristocrat_momentum": DividendAristocratMomentum,
    "concentrate_winners": ConcentrateWinners,
    "hidden_monopoly": HiddenMonopoly,
    "dcf_deep_value": DCFDeepValue,
    "toll_booth_economy": TollBoothEconomy,
    "beaten_down_staples": BeatenDownStaples,
    "insurance_float": InsuranceFloat,
    "boring_compounder": BoringCompounder,
}


def get_unconventional_strategy(name: str, **kwargs) -> BasePersona:
    cls = UNCONVENTIONAL_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(UNCONVENTIONAL_STRATEGIES.keys())}")
    return cls(**kwargs)


if __name__ == "__main__":
    print("=== Unconventional Strategies ===\n")
    for key, cls in UNCONVENTIONAL_STRATEGIES.items():
        inst = cls()
        print(f"  {key:25s} | {inst.config.name:35s} | {inst.config.description}")

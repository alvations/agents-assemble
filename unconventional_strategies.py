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
                "MMM", "CVX", "DOW", "INTC", "VZ", "WBA",
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
            if sma200 is None or sma200 <= 0:
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

            if daily_ret is None:
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
UNCONVENTIONAL_STRATEGIES = {
    "sell_in_may": SellInMayGoAway,
    "turn_of_month": TurnOfMonth,
    "vix_mean_reversion": VIXMeanReversion,
    "dogs_of_dow": DogsOfTheDow,
    "quality_factor": QualityFactor,
    "tail_risk_harvest": TailRiskHarvest,
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

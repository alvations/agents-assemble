"""News and event-driven trading strategies for agents-assemble.

These strategies proxy news/event impact through price and volume
signals, since we don't have real-time news APIs by default.

When FINNHUB_API_KEY or NEWS_API_KEY is set, these can be enhanced
with actual sentiment data.

Strategies:
    1. NewsReactionMomentum — Buy stocks with unusual volume + price moves
    2. EarningsSurpriseDrift — Buy after big up-days (earnings proxy)
    3. CrisisAlpha — Go defensive when broad market drops sharply
"""

from __future__ import annotations

from agents_assemble.strategies.generic import BasePersona, PersonaConfig


class NewsReactionMomentum(BasePersona):
    """Buy stocks showing unusual volume + positive price action.

    Proxy for news-driven momentum: when a stock has >2x average
    volume AND positive return, it likely received positive news.
    Ride the momentum for ~5-20 days.

    This captures earnings beats, FDA approvals, contract wins,
    analyst upgrades — any event that drives volume + price.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="News Reaction Momentum",
            description="Buy unusual volume + positive price moves (news proxy)",
            risk_tolerance=0.7,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
                "JPM", "V", "UNH", "LLY", "AVGO", "HD", "MCD",
                "CRM", "AMD", "NFLX", "PLTR", "CRWD", "COIN",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        scored = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue
            price = prices[sym]
            ind = self._get_indicators(data, sym,
                ["daily_return", "Volume", "volume_sma_20", "sma_50", "rsi_14"], date)
            daily_ret = ind["daily_return"]
            volume = ind["Volume"]
            vol_avg = ind["volume_sma_20"]
            sma50 = ind["sma_50"]
            rsi = ind["rsi_14"]

            if daily_ret is None or volume is None or vol_avg is None:
                continue

            vol_ratio = volume / vol_avg if vol_avg > 0 else 1

            # Exit: RSI overbought after news run (checked first — priority over buy)
            if rsi is not None and rsi > 80:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                continue

            # News reaction signal: volume spike + positive move
            if vol_ratio > 2.0 and daily_ret > 0.01:
                score = vol_ratio * daily_ret * 100
                # Must be in reasonable trend (not broken stock)
                if sma50 is not None and price > sma50 * 0.90:
                    scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]
        if top:
            per_stock = min(0.85 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock
        for sym in self.config.universe:
            if sym in prices and sym not in weights:
                weights[sym] = 0.0
        return weights


class EarningsSurpriseDrift(BasePersona):
    """Post-earnings announcement drift (PEAD) proxy.

    Academic anomaly: stocks that gap up on earnings continue drifting
    up for 60+ days. We proxy this with large single-day moves (>3%)
    on high volume (>2x average).

    Source: Ball & Brown (1968), Bernard & Thomas (1989)
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Earnings Surprise Drift",
            description="PEAD proxy: buy after >3% gap-up on 2x volume, ride drift 20-60 days",
            risk_tolerance=0.6,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
                "JPM", "V", "UNH", "LLY", "AVGO", "HD", "MCD",
                "CRM", "AMD", "NFLX", "PG", "JNJ", "MRK",
                "ABBV", "KO", "PEP", "WMT", "COST",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        candidates = []

        for sym in self.config.universe:
            if sym not in prices or sym not in data:
                continue
            price = prices[sym]
            ind = self._get_indicators(data, sym,
                ["daily_return", "Volume", "volume_sma_20", "sma_200"], date)
            daily_ret = ind["daily_return"]
            volume = ind["Volume"]
            vol_avg = ind["volume_sma_20"]
            sma200 = ind["sma_200"]

            if daily_ret is None or volume is None or vol_avg is None:
                continue

            vol_ratio = volume / vol_avg if vol_avg > 0 else 1

            # Broken-trend exit (checked first — priority over buy)
            if sma200 is not None and price < sma200 * 0.90:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                continue

            # Negative surprise: sell on big down + volume
            if daily_ret < -0.05 and vol_ratio > 2.0:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                continue

            # Earnings surprise proxy: >3% move on >2x volume
            if daily_ret > 0.03 and vol_ratio > 2.0:
                score = daily_ret * vol_ratio
                # Must be above SMA200 (quality filter)
                if sma200 is not None and price > sma200 * 0.95:
                    candidates.append((sym, score))

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


class CrisisAlpha(BasePersona):
    """Go defensive when market drops sharply (crisis detection).

    When SPY drops >2% in a day OR >5% in a week, shift to
    defensive assets (bonds, gold, cash). Return to stocks
    when volatility normalizes.

    This captures "black swan" events, geopolitical crises,
    and market panics.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Crisis Alpha",
            description="Auto-defensive on sharp market drops, return when vol normalizes",
            risk_tolerance=0.3,
            max_position_size=0.40,
            max_positions=5,
            rebalance_frequency="daily",
            universe=universe or [
                "SPY", "QQQ", "TLT", "GLD", "SHY",
            ],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        spy_ind = self._get_indicators(data, "SPY",
            ["daily_return", "vol_20", "rsi_14"], date) if "SPY" in data else {}
        spy_ret = spy_ind.get("daily_return")
        spy_vol = spy_ind.get("vol_20")
        spy_rsi = spy_ind.get("rsi_14")

        # Crisis detection
        is_crisis = False
        if spy_ret is not None and spy_ret < -0.02:
            is_crisis = True  # >2% single-day drop
        if spy_vol is not None and spy_vol > 0.025:
            is_crisis = True  # High realized vol (annualized ~40%)
        if spy_rsi is not None and spy_rsi < 25:
            is_crisis = True  # Extremely oversold
        # 5-day cumulative loss (weekly return proxy)
        if not is_crisis and "SPY" in data and "Close" in data["SPY"].columns:
            try:
                loc = int(data["SPY"].index.get_loc(date))
                if loc >= 5:
                    close_5d = data["SPY"]["Close"].iloc[loc - 5]
                    if close_5d > 0:
                        ret_5d = data["SPY"]["Close"].iloc[loc] / close_5d - 1
                        if ret_5d < -0.05:
                            is_crisis = True  # >5% weekly drop
            except (KeyError, TypeError, ValueError):
                pass

        universe_set = set(self.config.universe)
        if is_crisis:
            raw = {
                "TLT": 0.35,
                "GLD": 0.30,
                "SHY": 0.25,
                "SPY": 0.0,
                "QQQ": 0.0,
            }
        else:
            # Normal: 70/30 stocks/bonds
            raw = {
                "SPY": 0.40,
                "QQQ": 0.30,
                "TLT": 0.10,
                "GLD": 0.10,
                "SHY": 0.0,
            }
        result = {k: v for k, v in raw.items() if k in prices and k in universe_set}
        # Scale positive weights to recover budget lost from filtered symbols
        total_pos = sum(v for v in result.values() if v > 0)
        raw_pos = sum(v for v in raw.values() if v > 0)
        if 0 < total_pos < raw_pos:
            scale = raw_pos / total_pos
            result = {k: min(v * scale, self.config.max_position_size) if v > 0 else v
                      for k, v in result.items()}
        for sym in self.config.universe:
            if sym in prices and sym not in result:
                result[sym] = 0.0
        return result


NEWS_EVENT_STRATEGIES = {
    "news_reaction_momentum": NewsReactionMomentum,
    "earnings_surprise_drift": EarningsSurpriseDrift,
    "crisis_alpha": CrisisAlpha,
}


def get_news_event_strategy(name: str, **kwargs) -> BasePersona:
    cls = NEWS_EVENT_STRATEGIES.get(name)
    if cls is None:
        raise ValueError(f"Unknown: {name}. Available: {list(NEWS_EVENT_STRATEGIES.keys())}")
    return cls(**kwargs)


if __name__ == "__main__":
    print("=== News/Event-Driven Strategies ===\n")
    for key, cls in NEWS_EVENT_STRATEGIES.items():
        inst = cls()
        print(f"  {key:30s} | {inst.config.name:35s} | {inst.config.description}")

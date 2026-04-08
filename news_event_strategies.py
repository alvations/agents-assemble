"""News and event-driven trading strategies for agents-assemble.

These strategies proxy news/event impact through price and volume
signals, since we don't have real-time news APIs by default.

When FINNHUB_API_KEY or NEWS_API_KEY is set, these can be enhanced
with actual sentiment data.

Strategies:
    1. NewsReactionMomentum — Buy stocks with unusual volume + price moves
    2. EarningsSurpriseDrift — Buy after big up-days (earnings proxy)
    3. CrisisAlpha — Go defensive when broad market drops sharply
    4. FDACatalyst — Biotech FDA approval/rejection event plays
    5. EarningsWhisper — Pre-earnings drift (buy before earnings, sell after)
    6. MergerArbitrage — Announced M&A deal spread capture
    7. DividendCapture — Ex-dividend date trading for yield harvesting
"""

from __future__ import annotations

from personas import BasePersona, PersonaConfig


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


# ---------------------------------------------------------------------------
# 4. FDA Catalyst (Biotech event plays)
# ---------------------------------------------------------------------------
class FDACatalyst(BasePersona):
    """Biotech FDA approval/rejection event-driven strategy.

    Hypothesis: Biotech stocks exhibit extreme volatility around FDA
    binary events (PDUFA dates). We proxy catalysts via volume spikes
    + positive price action in biotech names. Academic evidence shows
    biotech stocks drift upward in the 30 days pre-PDUFA and gap on
    the event. We ride momentum in confirmed winners and cut losers.

    Source: Ovtchinnikov & McTier (2016) show +3.5% average pre-PDUFA
    drift. Huang et al. (2020) document post-approval drift of +8%
    over 60 days for novel drugs.

    Signal: Volume spike (>2.5x average) + positive return in biotech
    names = FDA catalyst proxy. Strong uptrend = phase 3 anticipation.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="FDA Catalyst (Biotech Events)",
            description="Biotech FDA event plays: volume spike + momentum in pharma/biotech",
            risk_tolerance=0.7,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="daily",
            universe=universe or [
                # Large-cap biotech (FDA pipeline-driven)
                "AMGN", "GILD", "REGN", "VRTX", "MRNA", "BIIB",
                # Mid-cap biotech (higher event sensitivity)
                "SGEN", "BMRN", "ALNY", "INCY",
                # Pharma (steady pipeline)
                "LLY", "ABBV", "MRK", "PFE", "JNJ",
                # Biotech ETF (for sector-wide moves)
                "XBI", "IBB",
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
                ["daily_return", "Volume", "volume_sma_20", "sma_50",
                 "sma_200", "rsi_14", "atr_14"], date)
            daily_ret = ind["daily_return"]
            volume = ind["Volume"]
            vol_avg = ind["volume_sma_20"]
            sma50 = ind["sma_50"]
            sma200 = ind["sma_200"]
            rsi = ind["rsi_14"]
            atr = ind["atr_14"]

            if daily_ret is None or volume is None or vol_avg is None or rsi is None:
                continue

            vol_ratio = volume / vol_avg if vol_avg > 0 else 1

            # Exit: overbought post-catalyst (take profits)
            if rsi > 82:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                continue

            # Exit: crashed below SMA200 (failed trial / rejection)
            if sma200 is not None and price < sma200 * 0.85:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Primary signal: volume spike + positive move (FDA catalyst proxy)
            if vol_ratio > 2.5 and daily_ret > 0.02:
                score += vol_ratio * daily_ret * 50

            # Secondary: strong uptrend (pre-PDUFA accumulation)
            if sma50 is not None and sma200 is not None and price > sma50 > sma200:
                score += 2.0
            elif sma50 is not None and price > sma50:
                score += 1.0

            # RSI in healthy range
            if 35 < rsi < 70:
                score += 0.5

            if score >= 2.5:
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


# ---------------------------------------------------------------------------
# 5. Earnings Whisper (Pre-Earnings Drift)
# ---------------------------------------------------------------------------
class EarningsWhisper(BasePersona):
    """Pre-earnings announcement drift strategy.

    Hypothesis: Stocks that have been trending up on above-average
    volume in the 10-20 days before earnings tend to beat estimates
    (smart money positioning). This is the "whisper" signal -- informed
    traders accumulate before the announcement.

    Source: Christophe, Ferri & Angel (2004) "Short-selling prior to
    earnings announcements". Barber et al. (2001) show retail buys
    predict positive surprises. The pre-earnings drift is 1-3% on
    average for positive whisper signals.

    Signal: Sustained uptrend (price > SMA20 > SMA50) + rising volume
    + RSI 50-70 (accumulation zone, not overbought). Exit after the
    post-earnings gap (RSI > 75 or volume spike + reversal).
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Earnings Whisper (Pre-Drift)",
            description="Pre-earnings drift: accumulation patterns predict positive surprises",
            risk_tolerance=0.6,
            max_position_size=0.10,
            max_positions=12,
            rebalance_frequency="daily",
            universe=universe or [
                # Mega-cap (most liquid, best whisper signal)
                "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA",
                # High-beta earnings movers
                "CRM", "AMD", "NFLX", "SHOP", "SNOW",
                # Financial (clear earnings beats)
                "JPM", "GS", "V", "MA",
                # Consumer (guidance-driven)
                "HD", "MCD", "NKE", "SBUX",
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
                ["sma_20", "sma_50", "rsi_14", "Volume", "volume_sma_20",
                 "macd", "macd_signal", "daily_return"], date)
            sma20 = ind["sma_20"]
            sma50 = ind["sma_50"]
            rsi = ind["rsi_14"]
            volume = ind["Volume"]
            vol_avg = ind["volume_sma_20"]
            macd = ind["macd"]
            macd_sig = ind["macd_signal"]
            daily_ret = ind["daily_return"]

            if any(v is None for v in [sma20, sma50, rsi]):
                continue

            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1

            # Exit: post-earnings pop exhaustion
            if rsi > 78:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0:
                    weights[sym] = 0.0
                continue

            # Exit: negative surprise (big drop + volume)
            if daily_ret is not None and daily_ret < -0.04 and vol_ratio > 2.0:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Whisper signal: price > SMA20 > SMA50 (orderly accumulation)
            if price > sma20 > sma50:
                score += 2.5
            elif price > sma20:
                score += 1.0

            # Rising volume (smart money accumulating)
            if vol_ratio > 1.2 and vol_ratio < 3.0:
                score += 1.0  # Elevated but not spike (spike = event already happened)

            # MACD bullish
            if macd is not None and macd_sig is not None and macd > macd_sig:
                score += 0.5

            # Ideal RSI zone: 50-70 (accumulation, not overbought)
            if 50 < rsi < 70:
                score += 1.0
            elif 40 < rsi < 50:
                score += 0.5

            if score >= 3.5:
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


# ---------------------------------------------------------------------------
# 6. Merger Arbitrage (M&A Spread)
# ---------------------------------------------------------------------------
class MergerArbitrage(BasePersona):
    """M&A merger arbitrage spread capture strategy.

    Hypothesis: When an acquisition is announced, the target trades at
    a discount to the deal price (the "spread") reflecting completion
    risk. This spread typically narrows as the deal progresses.
    Historically spreads are 3-8% annualized for announced deals.

    We proxy announced deals via: (1) stock trading within 5-15% of
    recent high with very low volatility (deal "floor"), (2) volume
    spike on initial announcement, (3) subsequent low-vol trading
    (spread compression). The strategy buys targets showing this
    pattern and exits when the spread closes (price near SMA20).

    Source: Mitchell & Pulvino (2001) show merger arb returns ~4%
    above risk-free with 0.5 beta. Baker & Savasoglu (2002) confirm
    the spread as compensation for deal break risk.
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Merger Arbitrage (M&A Spread)",
            description="M&A deal spread capture: buy targets at discount to deal price",
            risk_tolerance=0.3,
            max_position_size=0.12,
            max_positions=10,
            rebalance_frequency="daily",
            universe=universe or [
                # Large-cap frequent M&A targets / acquirers
                "ATVI", "VMW", "SPLK", "FORG", "COUP",
                # Pharma (frequent M&A)
                "SGEN", "ALNY", "BMRN", "HZNP", "IONS",
                # Tech M&A
                "NUAN", "TWLO", "ZEN", "FIVN", "QLYS",
                # Industrial / consumer
                "IR", "ROK", "IEX", "POOL",
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
                ["sma_20", "sma_50", "rsi_14", "vol_20", "atr_14",
                 "bb_upper", "bb_lower", "Volume", "volume_sma_20"], date)
            sma20 = ind["sma_20"]
            sma50 = ind["sma_50"]
            rsi = ind["rsi_14"]
            vol20 = ind["vol_20"]
            atr = ind["atr_14"]
            bb_upper = ind["bb_upper"]
            bb_lower = ind["bb_lower"]
            volume = ind["Volume"]
            vol_avg = ind["volume_sma_20"]

            if any(v is None for v in [sma20, rsi, vol20]):
                continue

            score = 0.0

            # M&A target proxy: low volatility + price near a ceiling
            # (deal price acts as ceiling, creating tight Bollinger bands)
            if vol20 < 0.012:  # Very low daily vol (annualized ~19%)
                score += 2.0
            elif vol20 < 0.018:
                score += 1.0

            # Tight Bollinger bandwidth (deal floor/ceiling compression)
            if bb_upper is not None and bb_lower is not None and bb_lower > 0:
                bandwidth = (bb_upper - bb_lower) / bb_lower
                if bandwidth < 0.05:
                    score += 1.5  # Very tight bands = M&A spread

            # Price near SMA20 (stable around deal price)
            if sma20 > 0:
                deviation = abs(price - sma20) / sma20
                if deviation < 0.02:
                    score += 1.0

            # RSI near 50 (neutral = deal spread equilibrium)
            if 40 < rsi < 60:
                score += 0.5

            # Volume was elevated recently (deal announcement aftermath)
            vol_ratio = volume / vol_avg if volume is not None and vol_avg is not None and vol_avg > 0 else 1
            if vol_ratio > 1.3:
                score += 0.5

            # Exit: deal break signal (sudden vol spike + price drop)
            if vol20 > 0.03 and rsi < 30:
                weights[sym] = 0.0
                continue

            if score >= 3.5:
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


# ---------------------------------------------------------------------------
# 7. Dividend Capture (Ex-Date Trading)
# ---------------------------------------------------------------------------
class DividendCapture(BasePersona):
    """Dividend capture / ex-date trading strategy.

    Hypothesis: Buy high-dividend stocks shortly before the ex-date
    to capture the dividend, then sell after. The stock drops by the
    dividend amount on ex-date but often recovers within days.
    We proxy this by holding high-yield, low-vol dividend payers
    in uptrends -- the same stocks institutional dividend capture
    funds target.

    Source: Kalay & Michaely (2000) show ex-date price drops average
    only 75-85% of the dividend (tax clientele effect), leaving a
    net gain. Cloyd et al. (2006) document institutional dividend
    capture yielding 2-4% annualized excess.

    Signal: Low volatility + above SMA50 + healthy RSI in known
    high-yield names (Dividend Aristocrats and high-yield ETFs).
    """

    def __init__(self, universe=None):
        config = PersonaConfig(
            name="Dividend Capture (Ex-Date)",
            description="Dividend capture: hold high-yield low-vol stocks, harvest dividends",
            risk_tolerance=0.3,
            max_position_size=0.12,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or [
                # Dividend Aristocrats (25+ years of increases)
                "JNJ", "PG", "KO", "PEP", "MCD", "MMM", "ABT",
                "XOM", "CVX", "IBM", "T", "VZ",
                # High-yield ETFs
                "SCHD", "VYM", "HDV",
                # REITs (high yield)
                "O", "VICI", "NNN",
                # Utilities (stable dividends)
                "NEE", "DUK", "SO",
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
            ind = self._get_indicators(data, sym,
                ["sma_50", "sma_200", "rsi_14", "vol_20", "atr_14"], date)
            sma50 = ind["sma_50"]
            sma200 = ind["sma_200"]
            rsi = ind["rsi_14"]
            vol20 = ind["vol_20"]
            atr = ind["atr_14"]

            if any(v is None for v in [sma50, rsi]):
                continue

            score = 0.0

            # Must be in uptrend (dividend stocks in downtrend = value trap)
            if sma200 is not None and price > sma50 > sma200:
                score += 2.5
            elif price > sma50:
                score += 1.5
            else:
                continue  # Skip downtrending dividend stocks

            # Low volatility preferred (stable dividend payers)
            if vol20 is not None:
                if vol20 < 0.012:
                    score += 2.0  # Very stable
                elif vol20 < 0.018:
                    score += 1.0
                elif vol20 > 0.03:
                    continue  # Too volatile for dividend capture

            # RSI in healthy range (not overbought)
            if 30 < rsi < 65:
                score += 1.0
            elif rsi > 75:
                weights[sym] = 0.0
                continue

            # Low ATR relative to price (tight trading range = stable)
            if atr is not None and price > 0:
                atr_pct = atr / price
                if atr_pct < 0.015:
                    score += 0.5

            if score >= 3.5:
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


NEWS_EVENT_STRATEGIES = {
    "news_reaction_momentum": NewsReactionMomentum,
    "earnings_surprise_drift": EarningsSurpriseDrift,
    "crisis_alpha": CrisisAlpha,
    "fda_catalyst": FDACatalyst,
    "earnings_whisper": EarningsWhisper,
    "merger_arbitrage": MergerArbitrage,
    "dividend_capture": DividendCapture,
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

"""Trading persona agents for agents-assemble.

Each persona implements a trading strategy inspired by a famous trader archetype.
All personas return target portfolio weights via a common interface compatible
with the Backtester.

Personas:
    1. BuffettValue       — Warren Buffett / Benjamin Graham value investing
    2. MomentumTrader     — Trend-following momentum (Druckenmiller style)
    3. MemeStockTrader    — Social sentiment / meme stock (WSB / Reddit style)
    4. DividendInvestor   — Dividend growth (old-school income investing)
    5. QuantStrategist    — Statistical arbitrage / mean reversion (Renaissance style)
    6. FixedIncomeStrat   — Bond / yield curve strategies (PIMCO style)
    7. GrowthInvestor     — Cathie Wood / ARK style high-growth disruptors
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import pandas as pd


# ---------------------------------------------------------------------------
# Base persona
# ---------------------------------------------------------------------------
@dataclass
class PersonaConfig:
    """Configuration for a trading persona."""
    name: str
    description: str
    risk_tolerance: float = 0.5       # 0 = conservative, 1 = aggressive
    max_position_size: float = 0.25   # Max weight per position
    max_positions: int = 10
    rebalance_frequency: str = "monthly"  # daily, weekly, monthly
    universe: List[str] = field(default_factory=list)


class BasePersona(ABC):
    """Base class for all trading personas."""

    def __init__(self, config: PersonaConfig):
        self.config = config

    @abstractmethod
    def generate_signals(
        self, date: pd.Timestamp, prices: Dict[str, float],
        portfolio: Any, data: Dict[str, pd.DataFrame]
    ) -> Dict[str, float]:
        """Generate target weights for each symbol.

        Returns: {symbol: weight} where weight is 0-1 (fraction of portfolio)
        """
        ...

    def __call__(self, date, prices, portfolio, data):
        """Make persona callable as a strategy function."""
        return self.generate_signals(date, prices, portfolio, data)

    def _get_indicator(self, data: Dict[str, pd.DataFrame], symbol: str,
                       indicator: str, date: pd.Timestamp) -> Optional[float]:
        """Safely get an indicator value for a symbol at a date."""
        if symbol not in data:
            return None
        df = data[symbol]
        if indicator not in df.columns:
            return None
        if date not in df.index:
            # Try nearest date
            try:
                idx = df.index.get_indexer([date], method="nearest")[0]
                if idx == -1:
                    return None
                val = df.iloc[idx][indicator]
                if pd.isna(val):
                    return None
                return float(val)
            except (IndexError, KeyError):
                return None
        val = df.loc[date, indicator]
        if pd.isna(val):
            return None
        return float(val)


# ---------------------------------------------------------------------------
# 1. Buffett Value Investor
# ---------------------------------------------------------------------------
class BuffettValue(BasePersona):
    """Warren Buffett / Benjamin Graham style value investing.

    Philosophy:
    - Buy wonderful companies at fair prices
    - Low P/E, low P/B, strong moat indicators
    - Use SMA200 as a margin-of-safety filter
    - Concentrate in high-conviction picks
    - Hold for the long term, low turnover

    Signals:
    - BUY: Price below SMA200 AND RSI < 40 (unloved + below long-term avg)
    - HOLD: Price within 10% of SMA200
    - SELL: RSI > 75 (overheated)
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Buffett Value",
            description="Deep value investing: buy great companies when they're cheap",
            risk_tolerance=0.3,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="monthly",
            universe=universe or [
                "BRK-B", "AAPL", "KO", "JNJ", "PG", "JPM", "BAC",
                "CVX", "XOM", "MRK", "ABBV", "V", "MA", "AXP",
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

            if sma200 is None or rsi is None:
                continue

            # Value score: how far below SMA200 (discount to intrinsic value proxy)
            discount = (sma200 - price) / sma200 if sma200 > 0 else 0

            # Only buy if trading below long-term average and not overbought
            if discount > 0.0 and rsi < 50:
                score = discount * (50 - rsi) / 50  # Combine discount + RSI
                candidates.append((sym, score))
            elif rsi > 75:
                # Sell overheated positions
                weights[sym] = 0.0

        # Rank by value score, take top N
        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]

        if top:
            # Equal weight among top picks, capped at max_position_size
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, score in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 2. Momentum Trader
# ---------------------------------------------------------------------------
class MomentumTrader(BasePersona):
    """Trend-following momentum strategy (Druckenmiller / O'Neil style).

    Philosophy:
    - Buy strength, sell weakness
    - Follow the trend — "the trend is your friend"
    - Use MACD crossovers and moving average alignment
    - Cut losses quickly, let winners run

    Signals:
    - BUY: MACD > signal AND price > SMA50 > SMA200 (uptrend alignment)
    - SELL: MACD < signal AND price < SMA50 (momentum breakdown)
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Momentum Trader",
            description="Trend-following: buy strength, cut losers fast",
            risk_tolerance=0.7,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "AAPL", "MSFT", "NVDA", "META", "GOOGL", "AMZN", "TSLA",
                "AVGO", "NFLX", "CRM", "AMD", "PLTR", "CRWD", "SNOW",
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
            macd = self._get_indicator(data, sym, "macd", date)
            macd_sig = self._get_indicator(data, sym, "macd_signal", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)

            if any(v is None for v in [sma50, sma200, macd, macd_sig, rsi]):
                continue

            # Trend alignment score
            trend_score = 0.0
            if price > sma50:
                trend_score += 1
            if sma50 > sma200:
                trend_score += 1
            if macd > macd_sig:
                trend_score += 1
            if rsi > 50 and rsi < 80:  # Momentum but not overbought
                trend_score += 1

            if trend_score >= 3:
                # Use RSI/100 as tiebreaker for same discrete trend_score
                scored.append((sym, trend_score + rsi / 100))
            elif trend_score <= 1:
                weights[sym] = 0.0  # Exit weak positions

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 3. Meme Stock Trader
# ---------------------------------------------------------------------------
class MemeStockTrader(BasePersona):
    """Social sentiment / meme stock trading (WSB / Reddit style).

    Philosophy:
    - High volume surges signal retail interest
    - RSI extremes as entry points (contrarian on dips, momentum on breakouts)
    - Short squeeze candidates: high short interest + volume spike
    - YOLO concentrated positions

    Signals:
    - BUY: Volume > 2x average AND RSI recovering from <30 (dip buy)
          OR Volume > 3x average AND price breaking above SMA20 (breakout)
    - SELL: RSI > 80 OR price drops below SMA20
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Meme Stock Trader",
            description="YOLO: volume spikes, dip buys, short squeezes",
            risk_tolerance=0.95,
            max_position_size=0.30,
            max_positions=5,
            rebalance_frequency="daily",
            universe=universe or [
                "GME", "AMC", "PLTR", "SOFI", "HOOD", "RIVN",
                "COIN", "MARA", "RIOT", "MSTR", "TSLA", "NVDA",
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
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            sma20 = self._get_indicator(data, sym, "sma_20", date)
            volume = self._get_indicator(data, sym, "Volume", date)
            vol_avg = self._get_indicator(data, sym, "volume_sma_20", date)

            if any(v is None for v in [rsi, sma20, volume, vol_avg]):
                continue

            vol_ratio = volume / vol_avg if vol_avg > 0 else 1

            score = 0.0

            # Dip buy: volume spike + oversold
            if vol_ratio > 2 and rsi < 35:
                score = 3.0 + vol_ratio

            # Breakout: massive volume + price above SMA20
            elif vol_ratio > 3 and price > sma20:
                score = 2.0 + vol_ratio

            # Moderate interest
            elif vol_ratio > 1.5 and rsi < 45 and price > sma20:
                score = 1.0 + vol_ratio

            # Exit overheated (takes priority over buy signals)
            if rsi > 80 or (price < sma20 and rsi > 60):
                weights[sym] = 0.0
            elif score > 0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            total_score = sum(s for _, s in top)
            for sym, score in top:
                w = min((score / total_score) * 0.90, self.config.max_position_size)
                weights[sym] = w

        return weights


# ---------------------------------------------------------------------------
# 4. Dividend Investor
# ---------------------------------------------------------------------------
class DividendInvestor(BasePersona):
    """Old-school dividend growth investing.

    Philosophy:
    - Buy companies with long dividend histories (Dividend Aristocrats)
    - Focus on dividend yield + growth rate
    - Reinvest dividends (compounding)
    - Very low turnover — buy and hold forever
    - Use price dips as accumulation opportunities

    Signals:
    - BUY: Price near or below SMA200 (accumulate on weakness)
    - HOLD: Always (unless dividend cut)
    - Rarely SELL: Only if price >30% above SMA200 (take some off table)
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Dividend Investor",
            description="Buy and hold dividend aristocrats, compound forever",
            risk_tolerance=0.2,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="monthly",
            universe=universe or [
                "JNJ", "PG", "KO", "PEP", "MMM", "T", "VZ",
                "MO", "ABBV", "O", "XOM", "CVX", "IBM", "HD",
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

            # Accumulate on dips, hold otherwise
            if discount > -0.10:  # Within 10% of or below SMA200
                # Score: prefer deeper discounts
                score = max(0, discount + 0.10)
                if rsi is not None and rsi < 40:
                    score += 0.1  # Bonus for oversold
                candidates.append((sym, score + 0.5))  # Base score ensures we hold
            elif discount < -0.30:
                # Way above SMA200 — trim
                weights[sym] = 0.05  # Keep small position

        # Rank by score, take top max_positions, equal weight
        candidates.sort(key=lambda x: x[1], reverse=True)
        top = candidates[:self.config.max_positions]
        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 5. Quant Strategist
# ---------------------------------------------------------------------------
class QuantStrategist(BasePersona):
    """Statistical/quantitative mean-reversion strategy (Renaissance style).

    Philosophy:
    - Markets are mostly efficient but mean-revert on short timescales
    - Use Bollinger Bands and RSI for mean-reversion signals
    - Volatility-weighted position sizing
    - High turnover, many small bets

    Signals:
    - BUY: Price below lower Bollinger Band AND RSI < 30
    - SELL: Price above upper Bollinger Band AND RSI > 70
    - Size inversely proportional to volatility
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Quant Strategist",
            description="Mean-reversion: buy oversold, sell overbought, size by vol",
            risk_tolerance=0.6,
            max_position_size=0.15,
            max_positions=10,
            rebalance_frequency="daily",
            universe=universe or [
                "AAPL", "MSFT", "GOOGL", "AMZN", "JPM", "BAC", "GS",
                "XOM", "CVX", "JNJ", "PG", "KO", "WMT", "HD",
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
            bb_upper = self._get_indicator(data, sym, "bb_upper", date)
            bb_lower = self._get_indicator(data, sym, "bb_lower", date)
            rsi = self._get_indicator(data, sym, "rsi_14", date)
            vol = self._get_indicator(data, sym, "vol_20", date)
            sma20 = self._get_indicator(data, sym, "sma_20", date)

            if any(v is None for v in [bb_upper, bb_lower, rsi, vol, sma20]):
                continue

            # Mean reversion score
            if price < bb_lower and rsi < 35:
                # Oversold — buy signal
                z_score = (sma20 - price) / (vol * price) if vol > 0 else 0
                inv_vol = 1.0 / max(vol, 0.005)  # Size inversely to vol
                score = z_score * inv_vol
                candidates.append((sym, max(score, 0.1), vol))

            elif price > bb_upper and rsi > 70:
                # Overbought — close position
                weights[sym] = 0.0

        # Vol-weighted sizing
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            top = candidates[:self.config.max_positions]
            total_inv_vol = sum(1 / max(v, 0.005) for _, _, v in top)
            for sym, score, vol in top:
                inv_vol = 1 / max(vol, 0.005)
                raw_w = (inv_vol / total_inv_vol) * 0.85
                weights[sym] = min(raw_w, self.config.max_position_size)

        return weights


# ---------------------------------------------------------------------------
# 6. Fixed Income Strategist
# ---------------------------------------------------------------------------
class FixedIncomeStrat(BasePersona):
    """Bond / yield curve strategy (PIMCO / Gundlach style).

    Philosophy:
    - Use bond ETFs as instruments (TLT, IEF, SHY, LQD, HYG, TIP)
    - Duration management based on yield curve signals
    - Go long duration when curve inverts (recession signal → rates will fall)
    - Go short duration when curve steepens
    - Credit spread trades: HYG vs LQD based on risk appetite

    Signals (using price action of bond ETFs as proxy):
    - Long TLT when SMA50 > SMA200 (bond uptrend = rates falling)
    - Long SHY when TLT trending down (flight to short duration)
    - Long HYG when RSI recovering and momentum positive (risk-on)
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Fixed Income Strategist",
            description="Bond duration/credit strategies via ETFs",
            risk_tolerance=0.3,
            max_position_size=0.35,
            max_positions=5,
            rebalance_frequency="weekly",
            universe=universe or ["TLT", "IEF", "SHY", "LQD", "HYG", "TIP", "BND", "AGG"],
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}
        tradeable = set(prices.keys())

        # Assess TLT trend (long-term bonds)
        tlt_sma50 = self._get_indicator(data, "TLT", "sma_50", date)
        tlt_sma200 = self._get_indicator(data, "TLT", "sma_200", date)
        tlt_price = prices.get("TLT")
        tlt_rsi = self._get_indicator(data, "TLT", "rsi_14", date)

        # Assess HYG (high yield = risk appetite)
        hyg_macd = self._get_indicator(data, "HYG", "macd", date)
        hyg_sig = self._get_indicator(data, "HYG", "macd_signal", date)
        hyg_rsi = self._get_indicator(data, "HYG", "rsi_14", date)

        # Duration allocation
        if tlt_sma50 is not None and tlt_sma200 is not None and tlt_price is not None:
            if tlt_sma50 > tlt_sma200:
                # Bond uptrend — rates falling, go long duration
                weights["TLT"] = 0.35
                weights["IEF"] = 0.20
                weights["SHY"] = 0.10
            elif tlt_price < tlt_sma50:
                # Rates rising — shorten duration
                weights["SHY"] = 0.35
                weights["IEF"] = 0.20
                weights["TLT"] = 0.05
            else:
                # Neutral — barbell
                weights["TLT"] = 0.15
                weights["SHY"] = 0.25
                weights["IEF"] = 0.15

        # Credit allocation
        if hyg_macd is not None and hyg_sig is not None:
            if hyg_macd > hyg_sig and hyg_rsi is not None and hyg_rsi > 40:
                # Risk-on: prefer high yield
                weights["HYG"] = 0.15
                weights["LQD"] = 0.10
            else:
                # Risk-off: prefer investment grade
                weights["LQD"] = 0.20
                weights["HYG"] = 0.0

        # Inflation protection
        if tlt_rsi is not None and tlt_rsi < 30:
            weights["TIP"] = 0.10  # Inflation hedge when bonds oversold

        # Only return weights for symbols that are actually tradeable, capped by config
        cap = self.config.max_position_size
        return {sym: min(w, cap) for sym, w in weights.items() if sym in tradeable}


# ---------------------------------------------------------------------------
# 7. Growth Investor
# ---------------------------------------------------------------------------
class GrowthInvestor(BasePersona):
    """Cathie Wood / ARK style growth & disruption investing.

    Philosophy:
    - Invest in disruptive innovation
    - High growth > current profitability
    - Buy on dips in high-conviction names
    - Willing to hold through volatility
    - Concentrated portfolio

    Signals:
    - BUY: Price near SMA50 support + RSI 35-55 (buying the dip in uptrend)
    - HOLD: Price > SMA50
    - SELL: Price breaks below SMA200 (thesis broken)
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Growth Investor",
            description="Disruptive innovation: high growth, buy dips in uptrends",
            risk_tolerance=0.8,
            max_position_size=0.20,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or [
                "TSLA", "PLTR", "COIN", "SHOP", "SQ", "ROKU", "CRWD",
                "DDOG", "NET", "SNOW", "ENPH", "MELI", "SE", "RBLX",
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

            # Thesis broken — full exit
            if price < sma200 * 0.95:
                weights[sym] = 0.0
                continue

            score = 0.0

            # Buy the dip in uptrend
            if price > sma200 and 30 < rsi < 55:
                proximity_to_sma50 = abs(price - sma50) / sma50 if sma50 > 0 else 1.0
                if proximity_to_sma50 < 0.05:  # Near SMA50 support
                    score = 3.0
                elif price > sma50:
                    score = 2.0
                else:
                    score = 1.0

                if macd is not None and macd_sig is not None and macd > macd_sig:
                    score += 1.0

            if score > 0:
                scored.append((sym, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            per_stock = min(0.90 / len(top), self.config.max_position_size)
            for sym, _ in top:
                weights[sym] = per_stock

        return weights


# ---------------------------------------------------------------------------
# 8. Sector Rotation Strategist
# ---------------------------------------------------------------------------
class SectorRotation(BasePersona):
    """Sector rotation strategy — rotate into strongest sectors.

    Philosophy:
    - Different sectors lead at different economic cycle stages
    - Momentum in sector ETFs predicts continued outperformance
    - Overweight top 3 sectors, underweight bottom 3
    - Weekly rotation to capture sector trends

    Signals:
    - Rank sectors by 1-month momentum (price / SMA20)
    - Go long top 3 sectors with momentum > 1
    - Exit sectors with momentum < 0.97 (below SMA20 by 3%)
    """

    def __init__(self, universe: Optional[List[str]] = None):
        config = PersonaConfig(
            name="Sector Rotation",
            description="Rotate into strongest sector ETFs, fade weakest",
            risk_tolerance=0.5,
            max_position_size=0.25,
            max_positions=4,
            rebalance_frequency="weekly",
            universe=universe or [
                "XLK", "XLF", "XLE", "XLV", "XLI", "XLP", "XLU",
                "XLRE", "XLC", "XLB", "XLY",
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

            if sma20 is None or sma50 is None:
                continue

            # Momentum score: how far above SMA20
            momentum = price / sma20 if sma20 > 0 else 1.0
            trend = 1.0 if price > sma50 else 0.0

            if momentum > 1.0:
                score = momentum + trend
                if rsi is not None and 40 < rsi < 75:
                    score += 0.2  # Bonus for healthy RSI
                scored.append((sym, score))
            elif momentum < 0.97:
                weights[sym] = 0.0  # Exit weak sectors

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:self.config.max_positions]

        if top:
            total_score = sum(s for _, s in top)
            for sym, score in top:
                w = min((score / total_score) * 0.90, self.config.max_position_size)
                weights[sym] = w

        return weights


# ---------------------------------------------------------------------------
# 9. Pairs / Relative Value Trader
# ---------------------------------------------------------------------------
class PairsTrader(BasePersona):
    """Pairs trading / relative value strategy.

    Philosophy:
    - Trade relative performance between correlated assets
    - When the spread deviates, mean-revert by going long the laggard
      and overweighting vs the leader
    - Classic pairs: XOM/CVX, KO/PEP, JPM/BAC, GOOGL/META

    Signals:
    - For each pair, compute relative strength (RSI of ratio)
    - Overweight the underperformer when ratio RSI < 30
    - Overweight the outperformer when ratio RSI > 70 (trend)
    """

    PAIRS = [
        ("XOM", "CVX"),
        ("KO", "PEP"),
        ("JPM", "BAC"),
        ("GOOGL", "META"),
        ("AAPL", "MSFT"),
        ("V", "MA"),
        ("HD", "LOW"),
    ]

    def __init__(self, universe: Optional[List[str]] = None):
        all_syms = list(set(s for pair in self.PAIRS for s in pair))
        config = PersonaConfig(
            name="Pairs Trader",
            description="Relative value: long laggard vs leader in correlated pairs",
            risk_tolerance=0.4,
            max_position_size=0.15,
            max_positions=8,
            rebalance_frequency="weekly",
            universe=universe or all_syms,
        )
        super().__init__(config)

    def generate_signals(self, date, prices, portfolio, data):
        weights = {}

        for sym_a, sym_b in self.PAIRS:
            if sym_a not in prices or sym_b not in prices:
                continue

            price_a = prices[sym_a]
            price_b = prices[sym_b]
            rsi_a = self._get_indicator(data, sym_a, "rsi_14", date)
            rsi_b = self._get_indicator(data, sym_b, "rsi_14", date)
            sma50_a = self._get_indicator(data, sym_a, "sma_50", date)
            sma50_b = self._get_indicator(data, sym_b, "sma_50", date)

            if any(v is None for v in [rsi_a, rsi_b, sma50_a, sma50_b]):
                continue

            # Relative momentum: which one is stronger?
            mom_a = price_a / sma50_a if sma50_a > 0 else 1
            mom_b = price_b / sma50_b if sma50_b > 0 else 1
            spread = mom_a - mom_b  # positive = A is stronger

            # Mean reversion in the pair
            if rsi_a < 35 and rsi_b > 55:
                # A oversold relative to B — overweight A
                weights[sym_a] = self.config.max_position_size
                weights[sym_b] = self.config.max_position_size * 0.5
            elif rsi_b < 35 and rsi_a > 55:
                # B oversold relative to A — overweight B
                weights[sym_b] = self.config.max_position_size
                weights[sym_a] = self.config.max_position_size * 0.5
            else:
                # Neutral — equal weight both
                weights[sym_a] = weights.get(sym_a, 0) + 0.06
                weights[sym_b] = weights.get(sym_b, 0) + 0.06

        # Cap total exposure
        total = sum(weights.values())
        if total > 0.95:
            scale = 0.95 / total
            weights = {k: v * scale for k, v in weights.items()}

        return weights


# ---------------------------------------------------------------------------
# 10. Ensemble Strategist
# ---------------------------------------------------------------------------
class EnsembleStrategist(BasePersona):
    """Ensemble strategy combining signals from multiple personas.

    Philosophy:
    - Diversification across strategy types reduces drawdowns
    - Weight strategies by their Sharpe ratio (or equal-weight)
    - Only take positions where multiple strategies agree
    - Uses Momentum, Growth, Buffett, and QuantMR for coverage

    Signals:
    - Run all sub-strategies
    - Take consensus positions (2+ strategies agree)
    - Weight by number of agreeing strategies
    """

    def __init__(self, universe: Optional[List[str]] = None):
        all_syms = list(set(
            sym for cls in [BuffettValue, MomentumTrader, GrowthInvestor, DividendInvestor]
            for sym in cls().config.universe
        ))
        config = PersonaConfig(
            name="Ensemble Strategist",
            description="Multi-strategy consensus: momentum + value + growth + dividend",
            risk_tolerance=0.5,
            max_position_size=0.15,
            max_positions=12,
            rebalance_frequency="weekly",
            universe=universe or all_syms,
        )
        super().__init__(config)
        # Sub-strategies with weights — use resolved universe so custom overrides propagate
        uni = self.config.universe
        self._sub_strategies = [
            (MomentumTrader(universe=uni), 0.35),   # Best Sharpe
            (GrowthInvestor(universe=uni), 0.25),
            (BuffettValue(universe=uni), 0.25),
            (DividendInvestor(universe=uni), 0.15),
        ]

    def generate_signals(self, date, prices, portfolio, data):
        # Collect signals from all sub-strategies
        all_signals = []
        for strategy, weight in self._sub_strategies:
            try:
                signals = strategy.generate_signals(date, prices, portfolio, data)
                all_signals.append((signals, weight))
            except Exception:
                pass

        if not all_signals:
            return {}

        # Aggregate: weighted average of signals
        combined = {}
        for signals, weight in all_signals:
            for sym, w in signals.items():
                if sym not in combined:
                    combined[sym] = {"total_weight": 0.0, "signal_count": 0, "exit_count": 0}
                if w > 0:
                    combined[sym]["total_weight"] += w * weight
                    combined[sym]["signal_count"] += 1
                else:
                    combined[sym]["exit_count"] += 1

        # Only take positions where 2+ strategies agree (consensus)
        weights = {}
        for sym, info in combined.items():
            if info["signal_count"] >= 2:
                # Scale weight by consensus strength
                consensus_factor = info["signal_count"] / len(all_signals)
                w = min(info["total_weight"] * consensus_factor,
                        self.config.max_position_size)
                weights[sym] = w
            elif info["exit_count"] >= 2:
                weights[sym] = 0.0  # Consensus exit

        # Normalize if over-allocated
        total = sum(v for v in weights.values() if v > 0)
        if total > 0.95:
            scale = 0.95 / total
            weights = {k: v * scale if v > 0 else v for k, v in weights.items()}

        return weights


# ---------------------------------------------------------------------------
# Persona registry
# ---------------------------------------------------------------------------
ALL_PERSONAS = {
    "buffett_value": BuffettValue,
    "momentum": MomentumTrader,
    "meme_stock": MemeStockTrader,
    "dividend": DividendInvestor,
    "quant": QuantStrategist,
    "fixed_income": FixedIncomeStrat,
    "growth": GrowthInvestor,
    "sector_rotation": SectorRotation,
    "pairs": PairsTrader,
    "ensemble": EnsembleStrategist,
}


def get_persona(name: str, **kwargs) -> BasePersona:
    """Get a persona by name."""
    cls = ALL_PERSONAS.get(name)
    if cls is None:
        raise ValueError(f"Unknown persona: {name}. Available: {list(ALL_PERSONAS.keys())}")
    return cls(**kwargs)


def list_personas() -> List[Dict[str, Any]]:
    """List all available personas."""
    result = []
    for key, cls in ALL_PERSONAS.items():
        instance = cls()
        result.append({
            "key": key,
            "name": instance.config.name,
            "description": instance.config.description,
            "risk_tolerance": instance.config.risk_tolerance,
            "rebalance_frequency": instance.config.rebalance_frequency,
            "universe_size": len(instance.config.universe),
        })
    return result


if __name__ == "__main__":
    print("=== Available Trading Personas ===\n")
    for p in list_personas():
        print(f"  {p['key']:20s} | {p['name']:25s} | Risk: {p['risk_tolerance']:.1f} | {p['description']}")

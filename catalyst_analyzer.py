"""CatalystAnalyzer — Python API for event-driven hypothesis generation and backtesting.

Industries with forward-looking catalyst patterns:
1. Gaming/Entertainment — game/movie/content releases (NTDOY, TTWO, EA, DIS)
2. Pharma/Biotech — FDA approval dates, clinical trial readouts (LLY, MRNA, VRTX)
3. Tech Hardware — product launches (AAPL events, NVDA chip launches)
4. Automotive — delivery numbers, new model launches (TSLA, RIVN)
5. Retail — seasonal (holiday, back-to-school, Prime Day) (AMZN, WMT, TGT)
6. Semiconductors — new chip architectures, design wins (NVDA, AMD, AVGO)

Usage:
    from catalyst_analyzer import CatalystAnalyzer

    analyzer = CatalystAnalyzer("NTDOY")
    news = analyzer.get_news()
    events = analyzer.predict_next_catalyst()
    historical = analyzer.analyze_historical_patterns()
    backtest = analyzer.backtest_event_strategy()
    prediction = analyzer.predict_next_catalyst()

    # Or all at once:
    report = analyzer.full_report()
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd

import sys
sys.path.insert(0, str(Path(__file__).parent))

from data_fetcher import fetch_ohlcv, get_api_key


# ---------------------------------------------------------------------------
# Industry catalyst profiles
# ---------------------------------------------------------------------------
INDUSTRY_CATALYSTS = {
    "gaming": {
        "description": "Game publishers: buy 3-6mo before major launch, sell on release",
        "tickers": ["NTDOY", "TTWO", "EA", "RBLX", "U", "DKNG"],
        "catalyst_types": ["game_launch", "console_launch", "earnings", "acquisition"],
        "typical_pattern": "buy_the_rumor_sell_the_news",
        "optimal_holding_days": 20,
        "optimal_strategy": "buy_spike",
    },
    "pharma_biotech": {
        "description": "FDA dates, clinical trials: binary outcomes with known dates",
        "tickers": ["LLY", "MRNA", "VRTX", "REGN", "BIIB", "ALNY", "CRSP", "NTLA"],
        "catalyst_types": ["fda_approval", "clinical_trial", "earnings", "patent"],
        "typical_pattern": "binary_event",
        "optimal_holding_days": 10,
        "optimal_strategy": "buy_dip",  # Buy dips before known catalysts
    },
    "tech_hardware": {
        "description": "Product launches: Apple events, chip launches, CES",
        "tickers": ["AAPL", "NVDA", "AMD", "AVGO", "ARM", "QCOM", "DELL", "HPE"],
        "catalyst_types": ["product_launch", "earnings", "chip_launch", "design_win"],
        "typical_pattern": "momentum_continuation",
        "optimal_holding_days": 10,
        "optimal_strategy": "buy_spike",
    },
    "automotive": {
        "description": "Delivery numbers (monthly/quarterly), new models",
        "tickers": ["TSLA", "RIVN", "LCID", "NIO", "LI", "XPEV", "GM", "F"],
        "catalyst_types": ["delivery_numbers", "new_model", "earnings", "guidance"],
        "typical_pattern": "buy_the_rumor_sell_the_news",
        "optimal_holding_days": 5,
        "optimal_strategy": "buy_dip",
    },
    "retail_seasonal": {
        "description": "Holiday, Prime Day, earnings — seasonal patterns",
        "tickers": ["AMZN", "WMT", "TGT", "COST", "HD", "LOW", "SHOP"],
        "catalyst_types": ["holiday_season", "prime_day", "earnings", "guidance"],
        "typical_pattern": "seasonal_momentum",
        "optimal_holding_days": 20,
        "optimal_strategy": "momentum",
    },
    "semiconductor": {
        "description": "New architectures, design wins, supply chain",
        "tickers": ["NVDA", "AMD", "AVGO", "MRVL", "TSM", "ASML", "LRCX", "AMAT"],
        "catalyst_types": ["chip_launch", "design_win", "earnings", "supply_update"],
        "typical_pattern": "momentum_continuation",
        "optimal_holding_days": 10,
        "optimal_strategy": "buy_spike",
    },
    "media_entertainment": {
        "description": "Box office, subscriber numbers, content releases",
        "tickers": ["DIS", "NFLX", "WBD", "CMCSA", "PARA"],
        "catalyst_types": ["box_office", "subscriber_numbers", "content_release", "earnings"],
        "typical_pattern": "earnings_driven",
        "optimal_holding_days": 20,
        "optimal_strategy": "momentum",
    },
}


# ---------------------------------------------------------------------------
# Data classes for structured results
# ---------------------------------------------------------------------------
@dataclass
class NewsItem:
    title: str
    date: str
    source: str
    catalyst_type: str
    url: str = ""
    sentiment: float | None = None

    def to_dict(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}


SELL_HORIZONS = [1, 2, 3, 5, 7, 10, 14, 20, 30]  # Days after event to measure


@dataclass
class EventPattern:
    date: str
    return_pct: float
    volume_ratio: float
    direction: str  # "up" or "down"
    # Returns at each sell horizon
    post_returns: dict[int, float] = field(default_factory=dict)  # {1: 0.02, 2: 0.03, ...}

    # Legacy compat
    @property
    def post_5d(self): return self.post_returns.get(5)
    @property
    def post_10d(self): return self.post_returns.get(10)
    @property
    def post_20d(self): return self.post_returns.get(20)

    def to_dict(self):
        d = {"date": self.date, "return_pct": self.return_pct,
             "volume_ratio": self.volume_ratio, "direction": self.direction}
        for h in SELL_HORIZONS:
            d[f"post_{h}d"] = self.post_returns.get(h, None)
        return d


@dataclass
class BacktestResult:
    strategy: str
    holding_days: int
    total_trades: int
    win_rate: float
    avg_return: float
    total_return: float
    best_trade: float
    worst_trade: float
    profit_factor: float

    def to_dict(self):
        d = self.__dict__.copy()
        for k, v in d.items():
            if isinstance(v, float) and not math.isfinite(v):
                d[k] = None
        return d


@dataclass
class CatalystPrediction:
    catalyst_type: str
    description: str
    expected_date: str | None
    historical_pattern: str
    recommended_action: str
    confidence: str  # "high", "medium", "low"
    expected_return: float
    expected_holding_days: int

    def to_dict(self):
        return self.__dict__.copy()


# ---------------------------------------------------------------------------
# Main API class
# ---------------------------------------------------------------------------
class CatalystAnalyzer:
    """Full catalyst analysis pipeline for any ticker.

    Methods:
        get_news() → List[NewsItem]
        get_upcoming_catalysts() → List[CatalystPrediction]
        analyze_historical_patterns() → Dict
        backtest_event_strategy() → Dict[str, BacktestResult]
        predict_next_catalyst() → List[CatalystPrediction]
        full_report() → Dict (everything combined)
    """

    def __init__(self, symbol: str, industry: str | None = None):
        self.symbol = symbol.upper()
        self.industry = industry.lower() if industry else self._detect_industry()
        self._price_data = None
        self._price_data_start = None
        self._news_cache = None

    def _detect_industry(self) -> str:
        """Auto-detect industry from ticker."""
        for ind, info in INDUSTRY_CATALYSTS.items():
            if self.symbol in info["tickers"]:
                return ind
        return "general"

    _DEFAULT_LOOKBACK_DAYS = 3 * 365

    def _get_price_data(self, start: str | None = None) -> pd.DataFrame:
        """Fetch and cache price data with indicators."""
        if start is None:
            start = (datetime.now() - timedelta(days=self._DEFAULT_LOOKBACK_DAYS)).strftime("%Y-%m-%d")
        if self._price_data is not None:
            if len(self._price_data) == 0 or (self._price_data_start is not None and self._price_data_start > start):
                self._price_data = None  # Cache doesn't cover requested range
        if self._price_data is None:
            df = fetch_ohlcv(self.symbol, start=start)
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)
            df["daily_return"] = df["Close"].pct_change().replace([float("inf"), float("-inf")], float("nan"))
            df["vol_avg_20"] = df["Volume"].rolling(20).mean().shift(1)
            vol_ratio = df["Volume"] / df["vol_avg_20"]
            df["vol_ratio"] = vol_ratio.replace([float("inf"), float("-inf")], float("nan"))
            self._price_data = df
            self._price_data_start = start
        return self._price_data

    # ----- 1. News -----

    _NEWS_FETCH_CAP = 50  # Always fetch generously; max_items is a return-time slice

    def get_news(self, max_items: int = 20) -> list[NewsItem]:
        """Pull recent news for the ticker."""
        if self._news_cache is not None:
            return self._news_cache[:max_items]

        items = []

        # yfinance (free)
        try:
            import yfinance as yf
            ticker = yf.Ticker(self.symbol)
            for n in (ticker.news or [])[:self._NEWS_FETCH_CAP]:
                try:
                    title = n.get("title", "")
                    ts = n.get("providerPublishTime", 0)
                    items.append(NewsItem(
                        title=title,
                        date=datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d") if ts > 946684800 else "",
                        source=n.get("publisher", "yfinance"),
                        catalyst_type=self._classify(title),
                        url=n.get("link", ""),
                    ))
                except Exception:
                    continue
        except Exception:
            pass

        # Finnhub (premium)
        key = get_api_key("FINNHUB_API_KEY")
        if key:
            import requests
            try:
                end = datetime.now().strftime("%Y-%m-%d")
                start = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
                resp = requests.get("https://finnhub.io/api/v1/company-news",
                                     params={"symbol": self.symbol, "from": start, "to": end, "token": key},
                                     timeout=15)
                if resp.status_code == 200:
                    for n in resp.json()[:self._NEWS_FETCH_CAP]:
                        try:
                            title = n.get("headline", "")
                            fh_ts = n.get("datetime", 0)
                            items.append(NewsItem(
                                title=title,
                                date=datetime.fromtimestamp(fh_ts, tz=timezone.utc).strftime("%Y-%m-%d") if fh_ts > 946684800 else "",
                                source=n.get("source", "finnhub"),
                                catalyst_type=self._classify(title),
                                url=n.get("url", ""),
                            ))
                        except Exception:
                            continue
            except Exception:
                pass

        # Deduplicate across sources by title
        seen = set()
        unique = []
        for item in items:
            dedup_key = item.title.lower().strip()
            if dedup_key not in seen:
                seen.add(dedup_key)
                unique.append(item)

        unique.sort(key=lambda x: x.date, reverse=True)
        self._news_cache = unique
        return unique[:max_items]

    # ----- 2. Historical event patterns -----

    def analyze_historical_patterns(
        self,
        volume_threshold: float = 2.0,
        return_threshold: float = 0.03,
    ) -> dict:
        """Find and analyze historical event days."""
        df = self._get_price_data()
        if len(df) < 50:
            return {"error": "Insufficient data"}

        events = []
        close_arr = df["Close"].values
        ret_arr = df["daily_return"].values
        vr_arr = df["vol_ratio"].values
        dates = df.index

        max_horizon = max(SELL_HORIZONS)
        last_event_i = -max_horizon  # Track last event to avoid overlapping windows
        for i in range(25, len(df) - max_horizon - 1):
            r_i = ret_arr[i]
            v_i = vr_arr[i]
            if r_i != r_i or v_i != v_i:  # NaN check
                continue
            if i - last_event_i < max_horizon:
                continue  # Skip events whose forward windows overlap prior event
            if v_i > volume_threshold and abs(r_i) > return_threshold:
                # Measure from next-day close (tradeable entry), consistent with backtest
                entry_price = close_arr[i + 1]
                if entry_price != entry_price or entry_price <= 0:
                    continue
                post = {}
                skip = False
                for h in SELL_HORIZONS:
                    future_price = close_arr[i + 1 + h]
                    if future_price != future_price:  # NaN
                        skip = True
                        break
                    post[h] = float(future_price / entry_price - 1)
                if skip:
                    continue
                events.append(EventPattern(
                    date=str(dates[i].date()),
                    return_pct=float(r_i),
                    volume_ratio=float(v_i),
                    direction="up" if r_i > 0 else "down",
                    post_returns=post,
                ))
                last_event_i = i

        up = [e for e in events if e.direction == "up"]
        down = [e for e in events if e.direction == "down"]

        result = {
            "total_events": len(events),
            "up_events": len(up),
            "down_events": len(down),
            "events": [e.to_dict() for e in events[-20:]],
        }

        # Sell-horizon analysis for up events
        if up:
            sell_analysis = {}
            for h in SELL_HORIZONS:
                rets = [e.post_returns[h] for e in up if h in e.post_returns]
                if not rets:
                    continue
                sell_analysis[f"{h}d"] = {
                    "avg_return": sum(rets) / len(rets),
                    "win_rate": sum(1 for r in rets if r > 0) / len(rets),
                    "best": float(max(rets)),
                    "worst": float(min(rets)),
                }
            result["after_up"] = sell_analysis
            result["optimal_sell_after_up"] = max(
                sell_analysis.items(), key=lambda x: x[1]["avg_return"]
            )[0]

        # Sell-horizon analysis for down events
        if down:
            sell_analysis = {}
            for h in SELL_HORIZONS:
                rets = [e.post_returns[h] for e in down if h in e.post_returns]
                if not rets:
                    continue
                sell_analysis[f"{h}d"] = {
                    "avg_return": sum(rets) / len(rets),
                    "bounce_rate": sum(1 for r in rets if r > 0) / len(rets),
                    "best": float(max(rets)),
                    "worst": float(min(rets)),
                }
            result["after_down"] = sell_analysis
            result["optimal_sell_after_down"] = max(
                sell_analysis.items(), key=lambda x: x[1]["avg_return"]
            )[0]

        return result

    # ----- 3. Backtest event strategies -----

    def backtest_event_strategy(self) -> dict[str, BacktestResult]:
        """Run all event-driven backtests and return structured results."""
        df = self._get_price_data()
        if len(df) < 50:
            return {}

        close_arr = df["Close"].values
        ret_arr = df["daily_return"].values
        vr_arr = df["vol_ratio"].values

        # Pre-compute entry signals (NaN comparisons produce False in numpy)
        signals = {
            "buy_spike": (ret_arr > 0.03) & (vr_arr > 2.0),
            "buy_dip": (ret_arr < -0.03) & (vr_arr > 2.0),
            "momentum": (ret_arr > 0.02) & (vr_arr > 1.5),
        }

        results = {}
        for strat, signal_arr in signals.items():
            if not signal_arr[25:].any():
                continue
            for hold in SELL_HORIZONS:
                key = f"{strat}_{hold}d"
                r = self._run_single_backtest(close_arr, signal_arr, strat, hold)
                if r.total_trades > 0:
                    results[key] = r
        return results

    def _run_single_backtest(self, close_arr, signal_arr, strategy: str, holding_days: int) -> BacktestResult:
        n = len(close_arr)

        trades = []
        position = None
        last_valid_price = None
        last_valid_i = -1

        for i in range(25, n):
            price = close_arr[i]
            if price == price:  # not NaN
                last_valid_price = price
                last_valid_i = i
            else:
                continue

            if position is not None:
                if i - position[1] >= holding_days:
                    trades.append(float(price / position[0] - 1))
                    position = None
                else:
                    continue  # Still holding — skip entry check

            if position is None and i + 1 < n and signal_arr[i]:
                entry_price = close_arr[i + 1]
                if entry_price == entry_price and entry_price > 0:
                    position = (entry_price, i + 1)

        # Close position at last valid price if holding period completed but
        # NaN close prices prevented exit (e.g., delisted stock)
        if position is not None:
            elapsed = (n - 1) - position[1]
            if elapsed >= holding_days and last_valid_price is not None and last_valid_i > position[1]:
                trades.append(float(last_valid_price / position[0] - 1))

        if not trades:
            return BacktestResult(strategy, holding_days, 0, 0, 0, 0, 0, 0, 0)

        winners = [t for t in trades if t > 0]
        losers = [t for t in trades if t < 0]

        return BacktestResult(
            strategy=strategy,
            holding_days=holding_days,
            total_trades=len(trades),
            win_rate=len(winners) / len(trades),
            avg_return=sum(trades) / len(trades),
            total_return=math.prod(1 + t for t in trades) - 1,
            best_trade=float(max(trades)),
            worst_trade=float(min(trades)),
            profit_factor=abs(sum(winners) / sum(losers)) if losers else 0.0 if not winners else float("inf"),
        )

    # ----- 4. Forward-looking predictions -----

    def predict_next_catalyst(self, patterns: dict | None = None, backtests: dict | None = None) -> list[CatalystPrediction]:
        """Generate forward-looking predictions based on historical patterns."""
        if patterns is None:
            patterns = self.analyze_historical_patterns()
        if backtests is None:
            backtests = self.backtest_event_strategy()

        predictions = []

        # Find best historical strategy
        best_bt = None
        best_key = None
        for key, bt in backtests.items():
            if bt.total_trades < 3 or bt.win_rate <= 0.5 or bt.profit_factor < 1.0:
                continue
            if best_bt is None or bt.avg_return > best_bt.avg_return:
                best_bt = bt
                best_key = key

        # Find best backtest matching industry-optimal strategy
        industry_bt = None
        industry_info = INDUSTRY_CATALYSTS.get(self.industry, {})
        opt_strat = industry_info.get("optimal_strategy")
        if opt_strat:
            for key, bt in backtests.items():
                if not key.startswith(opt_strat + "_"):
                    continue
                if bt.total_trades < 3 or bt.win_rate <= 0.5 or bt.profit_factor < 1.0:
                    continue
                if industry_bt is None or bt.avg_return > industry_bt.avg_return:
                    industry_bt = bt
        ind_best = industry_bt or best_bt

        # Use optimal horizons from pattern analysis instead of hardcoded ones
        opt_up_h = patterns.get('optimal_sell_after_up', '20d')
        opt_down_h = patterns.get('optimal_sell_after_down', '10d')
        opt_up_ret = patterns.get('after_up', {}).get(opt_up_h, {}).get('avg_return', 0)
        opt_down_ret = patterns.get('after_down', {}).get(opt_down_h, {}).get('avg_return', 0)

        # Industry-specific predictions
        if self.industry == "gaming":
            predictions.append(CatalystPrediction(
                catalyst_type="game_launch",
                description=f"Next major game/DLC release for {self.symbol}",
                expected_date=None,
                historical_pattern=f"After UP events: avg +{opt_up_ret:.1%} in {opt_up_h}"
                                   if "after_up" in patterns else "No clear pattern",
                recommended_action="BUY 3-6 months before announced release, SELL within days of launch",
                confidence="medium" if ind_best else "low",
                expected_return=ind_best.avg_return if ind_best else 0,
                expected_holding_days=ind_best.holding_days if ind_best else 20,
            ))

        elif self.industry == "pharma_biotech":
            predictions.append(CatalystPrediction(
                catalyst_type="fda_catalyst",
                description=f"Next FDA date / clinical readout for {self.symbol}",
                expected_date=None,
                historical_pattern=f"After DOWN events: avg +{opt_down_ret:.1%} in {opt_down_h} (bounce)"
                                   if "after_down" in patterns else "Binary outcomes",
                recommended_action="BUY dips before known FDA dates, small position size (binary risk)",
                confidence="low",
                expected_return=ind_best.avg_return if ind_best else 0,
                expected_holding_days=ind_best.holding_days if ind_best else 10,
            ))

        elif self.industry == "tech_hardware":
            predictions.append(CatalystPrediction(
                catalyst_type="product_launch",
                description=f"Next product announcement / launch event for {self.symbol}",
                expected_date=None,
                historical_pattern=f"After UP spikes: avg +{opt_up_ret:.1%} in {opt_up_h}"
                                   if "after_up" in patterns else "Momentum continuation",
                recommended_action="BUY on positive spike + volume, ride momentum 10-20 days",
                confidence="medium" if ind_best and ind_best.win_rate > 0.6 else "low",
                expected_return=ind_best.avg_return if ind_best else 0,
                expected_holding_days=ind_best.holding_days if ind_best else 10,
            ))

        elif self.industry == "automotive":
            predictions.append(CatalystPrediction(
                catalyst_type="delivery_numbers",
                description=f"Next quarterly delivery report for {self.symbol}",
                expected_date=None,
                historical_pattern=f"After DOWN events: bounce +{opt_down_ret:.1%} in {opt_down_h}"
                                   if "after_down" in patterns else "Buy dip on delivery miss",
                recommended_action="BUY dips around delivery number releases",
                confidence="medium" if ind_best else "low",
                expected_return=ind_best.avg_return if ind_best else 0,
                expected_holding_days=ind_best.holding_days if ind_best else 5,
            ))

        elif self.industry == "retail_seasonal":
            predictions.append(CatalystPrediction(
                catalyst_type="holiday_season",
                description=f"Next seasonal catalyst (holiday, Prime Day) for {self.symbol}",
                expected_date=None,
                historical_pattern=f"After UP events: avg +{opt_up_ret:.1%} in {opt_up_h}"
                                   if "after_up" in patterns else "Seasonal momentum",
                recommended_action="BUY before seasonal peaks (holiday, back-to-school), ride momentum 20 days",
                confidence="medium" if ind_best and ind_best.win_rate > 0.6 else "low",
                expected_return=ind_best.avg_return if ind_best else 0,
                expected_holding_days=ind_best.holding_days if ind_best else 20,
            ))

        elif self.industry == "semiconductor":
            predictions.append(CatalystPrediction(
                catalyst_type="chip_launch",
                description=f"Next chip launch / design win for {self.symbol}",
                expected_date=None,
                historical_pattern=f"After UP spikes: avg +{opt_up_ret:.1%} in {opt_up_h}"
                                   if "after_up" in patterns else "Momentum continuation",
                recommended_action="BUY on positive spike + volume from chip launch / design win news",
                confidence="medium" if ind_best and ind_best.win_rate > 0.6 else "low",
                expected_return=ind_best.avg_return if ind_best else 0,
                expected_holding_days=ind_best.holding_days if ind_best else 10,
            ))

        elif self.industry == "media_entertainment":
            predictions.append(CatalystPrediction(
                catalyst_type="subscriber_numbers",
                description=f"Next subscriber / box office report for {self.symbol}",
                expected_date=None,
                historical_pattern=f"After UP events: avg +{opt_up_ret:.1%} in {opt_up_h}"
                                   if "after_up" in patterns else "Earnings-driven",
                recommended_action="BUY before subscriber number releases or major content launches",
                confidence="medium" if ind_best and ind_best.win_rate > 0.6 else "low",
                expected_return=ind_best.avg_return if ind_best else 0,
                expected_holding_days=ind_best.holding_days if ind_best else 20,
            ))

        # Generic prediction from best backtest
        if best_bt and best_bt.win_rate > 0.5:
            strat_desc = {"buy_spike": "BUY after >3% up-day on 2x volume",
                          "buy_dip": "BUY after >3% down-day on 2x volume",
                          "momentum": "BUY after >2% up on 1.5x volume"}
            predictions.append(CatalystPrediction(
                catalyst_type="statistical_edge",
                description=f"Best historical strategy: {best_key}",
                expected_date="Next signal occurrence",
                historical_pattern=f"{best_bt.total_trades} trades, {best_bt.win_rate:.0%} win rate, "
                                   f"{best_bt.total_return:+.1%} total return",
                recommended_action=strat_desc.get(best_bt.strategy, best_bt.strategy),
                confidence="high" if best_bt.win_rate > 0.7 else "medium",
                expected_return=best_bt.avg_return,
                expected_holding_days=best_bt.holding_days,
            ))

        return predictions

    # ----- 5. Full report -----

    def full_report(self) -> dict:
        """Generate complete catalyst analysis report."""
        try:
            news = self.get_news()
        except Exception:
            news = []

        try:
            patterns = self.analyze_historical_patterns()
        except Exception as e:
            patterns = {"error": str(e)}

        try:
            backtests = self.backtest_event_strategy()
        except Exception:
            backtests = {}

        try:
            predictions = self.predict_next_catalyst(patterns=patterns, backtests=backtests)
        except Exception:
            predictions = []

        return self._sanitize_for_json({
            "symbol": self.symbol,
            "industry": self.industry,
            "industry_info": INDUSTRY_CATALYSTS.get(self.industry, {}),
            "news": [n.to_dict() for n in news[:10]],
            "historical_patterns": patterns,
            "backtests": {k: v.to_dict() for k, v in backtests.items()},
            "predictions": [p.to_dict() for p in predictions],
            "generated_at": datetime.now().isoformat(),
        })

    def print_report(self):
        """Print human-readable report."""
        report = self.full_report()

        print(f"\n{'='*60}")
        print(f"  CATALYST ANALYSIS: {self.symbol}")
        print(f"  Industry: {self.industry}")
        print(f"{'='*60}")

        # News
        news = report["news"]
        if news:
            print(f"\n  Recent News ({len(news)} items):")
            for n in news[:5]:
                print(f"    [{n['catalyst_type']}] {n['date']} — {n['title'][:65]}")

        # Patterns with sell-horizon grid
        p = report["historical_patterns"]
        if "error" in p:
            print(f"\n  Historical Events: {p['error']}")
        elif "total_events" in p:
            print(f"\n  Historical Events: {p['total_events']} ({p['up_events']} up, {p['down_events']} down)")

            if "after_up" in p:
                au = p["after_up"]
                print(f"\n  SELL HORIZON AFTER UP EVENTS (optimal: {p.get('optimal_sell_after_up', '?')}):")
                print(f"  {'Horizon':>8s} | {'Avg Ret':>8s} | {'Win Rate':>8s} | {'Best':>8s} | {'Worst':>8s}")
                print(f"  {'-'*48}")
                for h_key in sorted(au.keys(), key=lambda x: int(x.replace('d', ''))):
                    v = au[h_key]
                    print(f"  {h_key:>8s} | {v['avg_return']:>+7.1%} | {v['win_rate']:>7.0%} | {v['best']:>+7.1%} | {v['worst']:>+7.1%}")

            if "after_down" in p:
                ad = p["after_down"]
                print(f"\n  SELL HORIZON AFTER DOWN EVENTS (optimal: {p.get('optimal_sell_after_down', '?')}):")
                print(f"  {'Horizon':>8s} | {'Avg Ret':>8s} | {'Bounce':>8s} | {'Best':>8s} | {'Worst':>8s}")
                print(f"  {'-'*48}")
                for h_key in sorted(ad.keys(), key=lambda x: int(x.replace('d', ''))):
                    v = ad[h_key]
                    print(f"  {h_key:>8s} | {v['avg_return']:>+7.1%} | {v['bounce_rate']:>7.0%} | {v['best']:>+7.1%} | {v['worst']:>+7.1%}")

        # Backtests
        bts = report["backtests"]
        if bts:
            print(f"\n  Backtests ({len(bts)} strategies):")
            print(f"  {'Strategy':20s} | {'Trades':>6s} | {'Win%':>5s} | {'Avg Ret':>8s} | {'Total Ret':>10s}")
            print(f"  {'-'*60}")
            for key, bt in sorted(bts.items(), key=lambda x: float("inf") if x[1]["total_return"] is None else -x[1]["total_return"]):
                wr = bt['win_rate'] if bt['win_rate'] is not None else 0
                ar = bt['avg_return'] if bt['avg_return'] is not None else 0
                tr = bt['total_return']
                tr_s = f"{tr:+9.1%}" if tr is not None else "      N/A"
                print(f"  {key:20s} | {bt['total_trades']:6d} | {wr:4.0%} | "
                      f"{ar:+7.1%} | {tr_s}")

        # Predictions
        preds = report["predictions"]
        if preds:
            print(f"\n  Forward-Looking Predictions:")
            for pred in preds:
                print(f"    [{pred['confidence'].upper()}] {pred['catalyst_type']}: {pred['recommended_action']}")
                if pred["expected_return"] != 0:
                    print(f"         Expected: {pred['expected_return']:+.1%} over {pred['expected_holding_days']}d")

    # ----- Helpers -----

    _CLASSIFY_RULES = (
        (("fda", "approval", "trial", "phase"), "regulatory"),
        (("earnings", "revenue", "profit", "beat", "miss", "eps"), "earnings"),
        (("acquire", "merger", "buyout", "deal"), "ma"),
        (("launch", "release", "unveil", "debut", "premiere", "nintendo switch", "gta"), "product_launch"),
        (("patent", "intellectual property"), "patent"),
        (("delivery", "production", "sales figure"), "delivery_numbers"),
        (("subscriber", "streaming", "user growth", "monthly active"), "subscriber_numbers"),
        (("dividend", "buyback", "split"), "capital_return"),
        (("upgrade", "downgrade", "target", "analyst", "rating"), "analyst"),
        (("guidance", "outlook", "forecast"), "guidance"),
    )

    def _classify(self, title: str) -> str:
        t = title.lower()
        for keywords, category in self._CLASSIFY_RULES:
            if any(w in t for w in keywords):
                return category
        return "general"

    @staticmethod
    def _sanitize_for_json(obj):
        if isinstance(obj, float) and not math.isfinite(obj):
            return None
        if isinstance(obj, dict):
            return {k: CatalystAnalyzer._sanitize_for_json(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [CatalystAnalyzer._sanitize_for_json(v) for v in obj]
        return obj

    def save_report(self, directory: str | None = None) -> Path:
        """Save full report as JSON."""
        report = self.full_report()
        out_dir = Path(directory or str(Path(__file__).parent / "knowledge" / "catalyst_scans"))
        out_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M")
        path = out_dir / f"{self.symbol}_{ts}.json"
        path.write_text(json.dumps(report, indent=2, default=str))
        return path


# ---------------------------------------------------------------------------
# Batch scanner for multiple tickers
# ---------------------------------------------------------------------------
def scan_industry(industry: str) -> dict[str, dict]:
    """Scan all tickers in an industry."""
    info = INDUSTRY_CATALYSTS.get(industry.lower())
    if not info:
        raise ValueError(f"Unknown industry: {industry}. Available: {list(INDUSTRY_CATALYSTS.keys())}")

    results = {}
    for sym in info["tickers"]:
        try:
            analyzer = CatalystAnalyzer(sym, industry)
            results[sym] = analyzer.full_report()
        except Exception as e:
            results[sym] = {"error": str(e)}
    return results


def scan_all_industries() -> dict[str, dict]:
    """Scan top ticker from each industry."""
    results = {}
    for industry, info in INDUSTRY_CATALYSTS.items():
        sym = info["tickers"][0]
        try:
            analyzer = CatalystAnalyzer(sym, industry)
            backtests = analyzer.backtest_event_strategy()
            viable = [b for b in backtests.values()
                      if b.total_trades >= 3 and b.win_rate > 0.5 and b.profit_factor >= 1.0]
            best = max(viable, key=lambda b: b.total_return) if viable else None
            _san = CatalystAnalyzer._sanitize_for_json
            results[f"{industry}/{sym}"] = {
                "best_strategy": best.strategy if best else None,
                "holding_days": best.holding_days if best else None,
                "win_rate": _san(best.win_rate) if best else None,
                "total_return": _san(best.total_return) if best else None,
            }
        except Exception as e:
            results[f"{industry}/{sym}"] = {"error": str(e)}
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    symbol = sys.argv[1] if len(sys.argv) > 1 else "NTDOY"
    analyzer = CatalystAnalyzer(symbol)
    analyzer.print_report()
    path = analyzer.save_report()
    print(f"\n  Saved: {path}")

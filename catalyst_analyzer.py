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
    events = analyzer.get_upcoming_catalysts()
    historical = analyzer.analyze_historical_patterns()
    backtest = analyzer.backtest_event_strategy()
    prediction = analyzer.predict_next_catalyst()

    # Or all at once:
    report = analyzer.full_report()
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field as dataclass_field
from datetime import datetime, timedelta
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
    post_returns: dict[int, float] = dataclass_field(default_factory=dict)  # {1: 0.02, 2: 0.03, ...}

    # Legacy compat
    @property
    def post_5d(self): return self.post_returns.get(5, 0)
    @property
    def post_10d(self): return self.post_returns.get(10, 0)
    @property
    def post_20d(self): return self.post_returns.get(20, 0)

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
        return self.__dict__


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
        return self.__dict__


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
        self.industry = industry or self._detect_industry()
        self._price_data = None
        self._news_cache = None

    def _detect_industry(self) -> str:
        """Auto-detect industry from ticker."""
        for ind, info in INDUSTRY_CATALYSTS.items():
            if self.symbol in info["tickers"]:
                return ind
        return "general"

    def _get_price_data(self, start: str = "2022-01-01") -> pd.DataFrame:
        """Fetch and cache price data with indicators."""
        if self._price_data is None:
            df = fetch_ohlcv(self.symbol, start=start)
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)
            df["daily_return"] = df["Close"].pct_change()
            df["vol_avg_20"] = df["Volume"].rolling(20).mean()
            df["vol_ratio"] = df["Volume"] / df["vol_avg_20"]
            df["sma_50"] = df["Close"].rolling(50).mean()
            df["sma_200"] = df["Close"].rolling(200).mean()
            self._price_data = df
        return self._price_data

    # ----- 1. News -----

    def get_news(self, max_items: int = 20) -> list[NewsItem]:
        """Pull recent news for the ticker."""
        if self._news_cache is not None:
            return self._news_cache

        items = []

        # yfinance (free)
        try:
            import yfinance as yf
            ticker = yf.Ticker(self.symbol)
            for n in (ticker.news or [])[:max_items]:
                title = n.get("title", "")
                ts = n.get("providerPublishTime", 0)
                items.append(NewsItem(
                    title=title,
                    date=datetime.fromtimestamp(ts).strftime("%Y-%m-%d") if ts > 946684800 else "",
                    source=n.get("publisher", "yfinance"),
                    catalyst_type=self._classify(title),
                    url=n.get("link", ""),
                ))
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
                    for n in resp.json()[:max_items]:
                        title = n.get("headline", "")
                        fh_ts = n.get("datetime", 0)
                        items.append(NewsItem(
                            title=title,
                            date=datetime.fromtimestamp(fh_ts).strftime("%Y-%m-%d") if fh_ts > 946684800 else "",
                            source=n.get("source", "finnhub"),
                            catalyst_type=self._classify(title),
                            url=n.get("url", ""),
                        ))
            except Exception:
                pass

        self._news_cache = items
        return items

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
        close = df["Close"]
        ret = df["daily_return"]
        vr = df["vol_ratio"]

        max_horizon = max(SELL_HORIZONS)
        for i in range(25, len(df) - max_horizon):
            if pd.isna(vr.iloc[i]) or pd.isna(ret.iloc[i]):
                continue
            if vr.iloc[i] > volume_threshold and abs(ret.iloc[i]) > return_threshold:
                post = {}
                for h in SELL_HORIZONS:
                    post[h] = float(close.iloc[i + h] / close.iloc[i] - 1)
                events.append(EventPattern(
                    date=str(df.index[i].date()),
                    return_pct=float(ret.iloc[i]),
                    volume_ratio=float(vr.iloc[i]),
                    direction="up" if ret.iloc[i] > 0 else "down",
                    post_returns=post,
                ))

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
                rets = [e.post_returns.get(h, 0) for e in up]
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
                rets = [e.post_returns.get(h, 0) for e in down]
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

        results = {}
        for strat in ["buy_spike", "buy_dip", "momentum"]:
            for hold in SELL_HORIZONS:
                key = f"{strat}_{hold}d"
                r = self._run_single_backtest(df, strat, hold)
                if r.total_trades > 0:
                    results[key] = r
        return results

    def _run_single_backtest(self, df: pd.DataFrame, strategy: str, holding_days: int) -> BacktestResult:
        close = df["Close"]
        ret = df["daily_return"]
        vr = df["vol_ratio"]

        trades = []
        position = None

        for i in range(25, len(df)):
            price = close.iloc[i]
            r = ret.iloc[i] if not pd.isna(ret.iloc[i]) else 0
            v = vr.iloc[i] if not pd.isna(vr.iloc[i]) else 1

            if position is not None:
                if i - position[1] >= holding_days:
                    trades.append(price / position[0] - 1)
                    position = None

            if position is None:
                if strategy == "buy_spike" and r > 0.03 and v > 2.0:
                    position = (price, i)
                elif strategy == "buy_dip" and r < -0.03 and v > 2.0:
                    position = (price, i)
                elif strategy == "momentum" and r > 0.02 and v > 1.5:
                    position = (price, i)

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
            profit_factor=abs(sum(winners) / sum(losers)) if losers else 0.0 if not winners else 999.0,
        )

    # ----- 4. Forward-looking predictions -----

    def predict_next_catalyst(self, patterns: dict | None = None, backtests: dict | None = None) -> list[CatalystPrediction]:
        """Generate forward-looking predictions based on historical patterns."""
        if patterns is None:
            patterns = self.analyze_historical_patterns()
        if backtests is None:
            backtests = self.backtest_event_strategy()
        industry_info = INDUSTRY_CATALYSTS.get(self.industry, {})

        predictions = []

        # Find best historical strategy
        best_bt = None
        best_key = None
        for key, bt in backtests.items():
            if bt.win_rate <= 0.5:
                continue
            if best_bt is None or bt.total_return > best_bt.total_return:
                best_bt = bt
                best_key = key

        # Industry-specific predictions
        if self.industry == "gaming":
            predictions.append(CatalystPrediction(
                catalyst_type="game_launch",
                description=f"Next major game/DLC release for {self.symbol}",
                expected_date=None,
                historical_pattern=f"After UP events: avg +{patterns.get('after_up', {}).get('20d', {}).get('avg_return', 0):.1%} in 20d"
                                   if "after_up" in patterns else "No clear pattern",
                recommended_action="BUY 3-6 months before announced release, SELL within days of launch",
                confidence="medium",
                expected_return=best_bt.avg_return if best_bt else 0,
                expected_holding_days=best_bt.holding_days if best_bt else 20,
            ))

        elif self.industry == "pharma_biotech":
            predictions.append(CatalystPrediction(
                catalyst_type="fda_catalyst",
                description=f"Next FDA date / clinical readout for {self.symbol}",
                expected_date=None,
                historical_pattern=f"After DOWN events: avg +{patterns.get('after_down', {}).get('10d', {}).get('avg_return', 0):.1%} in 10d (bounce)"
                                   if "after_down" in patterns else "Binary outcomes",
                recommended_action="BUY dips before known FDA dates, small position size (binary risk)",
                confidence="low",
                expected_return=best_bt.avg_return if best_bt else 0,
                expected_holding_days=10,
            ))

        elif self.industry == "tech_hardware":
            predictions.append(CatalystPrediction(
                catalyst_type="product_launch",
                description=f"Next product announcement / launch event for {self.symbol}",
                expected_date=None,
                historical_pattern=f"After UP spikes: avg +{patterns.get('after_up', {}).get('10d', {}).get('avg_return', 0):.1%} in 10d"
                                   if "after_up" in patterns else "Momentum continuation",
                recommended_action="BUY on positive spike + volume, ride momentum 10-20 days",
                confidence="medium" if best_bt and best_bt.win_rate > 0.6 else "low",
                expected_return=best_bt.avg_return if best_bt else 0,
                expected_holding_days=best_bt.holding_days if best_bt else 10,
            ))

        elif self.industry == "automotive":
            predictions.append(CatalystPrediction(
                catalyst_type="delivery_numbers",
                description=f"Next quarterly delivery report for {self.symbol}",
                expected_date=None,
                historical_pattern=f"After DOWN events: bounce +{patterns.get('after_down', {}).get('5d', {}).get('avg_return', 0):.1%} in 5d"
                                   if "after_down" in patterns else "Buy dip on delivery miss",
                recommended_action="BUY dips around delivery number releases",
                confidence="medium",
                expected_return=best_bt.avg_return if best_bt else 0,
                expected_holding_days=5,
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
        news = self.get_news()
        patterns = self.analyze_historical_patterns()
        backtests = self.backtest_event_strategy()
        predictions = self.predict_next_catalyst(patterns=patterns, backtests=backtests)

        return {
            "symbol": self.symbol,
            "industry": self.industry,
            "industry_info": INDUSTRY_CATALYSTS.get(self.industry, {}),
            "news": [n.to_dict() for n in news[:10]],
            "historical_patterns": patterns,
            "backtests": {k: v.to_dict() for k, v in backtests.items()},
            "predictions": [p.to_dict() for p in predictions],
            "generated_at": datetime.now().isoformat(),
        }

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
        if "total_events" in p:
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
            for key, bt in sorted(bts.items(), key=lambda x: -x[1]["total_return"]):
                print(f"  {key:20s} | {bt['total_trades']:6d} | {bt['win_rate']:4.0%} | "
                      f"{bt['avg_return']:+7.1%} | {bt['total_return']:+9.1%}")

        # Predictions
        preds = report["predictions"]
        if preds:
            print(f"\n  Forward-Looking Predictions:")
            for pred in preds:
                print(f"    [{pred['confidence'].upper()}] {pred['catalyst_type']}: {pred['recommended_action']}")
                if pred["expected_return"] != 0:
                    print(f"         Expected: {pred['expected_return']:+.1%} over {pred['expected_holding_days']}d")

    # ----- Helpers -----

    def _classify(self, title: str) -> str:
        t = title.lower()
        if any(w in t for w in ["launch", "release", "unveil", "debut", "premiere", "switch", "gta"]):
            return "product_launch"
        if any(w in t for w in ["earnings", "revenue", "profit", "beat", "miss", "eps"]):
            return "earnings"
        if any(w in t for w in ["acquire", "merger", "buyout", "deal"]):
            return "ma"
        if any(w in t for w in ["fda", "approval", "trial", "phase"]):
            return "regulatory"
        if any(w in t for w in ["upgrade", "downgrade", "target", "analyst", "rating"]):
            return "analyst"
        if any(w in t for w in ["dividend", "buyback", "split"]):
            return "capital_return"
        if any(w in t for w in ["delivery", "production", "sales figure"]):
            return "delivery_numbers"
        return "general"

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
    info = INDUSTRY_CATALYSTS.get(industry)
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
            best = max(backtests.values(), key=lambda b: b.total_return) if backtests else None
            results[f"{industry}/{sym}"] = {
                "best_strategy": best.strategy if best else None,
                "holding_days": best.holding_days if best else None,
                "win_rate": best.win_rate if best else None,
                "total_return": best.total_return if best else None,
            }
        except Exception as e:
            results[f"{industry}/{sym}"] = {"error": str(e)}
    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import sys
    symbol = sys.argv[1] if len(sys.argv) > 1 else "NTDOY"
    analyzer = CatalystAnalyzer(symbol)
    analyzer.print_report()
    path = analyzer.save_report()
    print(f"\n  Saved: {path}")

"""agents-assemble: Trading agents with backtesting and persona-based strategies.

Install: pip install -e .

Quick start:
    from agents_assemble import Backtester, get_persona
    bt = Backtester(strategy=get_persona('momentum'), symbols=['AAPL', 'NVDA'])
    results = bt.run()
"""

from agents_assemble.engine.backtester import Backtester, Portfolio, Trade, Side, format_report
from agents_assemble.engine.judge import diagnose_strategy, rank_strategies, generate_judge_report
from agents_assemble.engine.recommender import generate_trade_recommendations, save_strategy_recommendation
from agents_assemble.data.fetcher import (
    fetch_ohlcv, fetch_multiple_ohlcv, fetch_fundamentals,
    fetch_fred_series, fetch_yield_curve, get_universe, UNIVERSE,
    scan_52_week_lows, scan_volatile_stocks,
)
from agents_assemble.strategies import get_persona, get_famous_investor, get_theme_strategy, get_recession_strategy

__version__ = "0.1.0"
__all__ = [
    "Backtester", "Portfolio", "Trade", "Side", "format_report",
    "fetch_ohlcv", "fetch_multiple_ohlcv", "fetch_fundamentals",
    "get_persona", "get_famous_investor", "get_theme_strategy", "get_recession_strategy",
    "diagnose_strategy", "rank_strategies",
    "get_universe", "UNIVERSE",
]

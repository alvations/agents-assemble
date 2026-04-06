"""Backtesting engine, judge, and trade recommendation."""
from agents_assemble.engine.backtester import Backtester, Portfolio, Trade, Side, format_report, compute_metrics
from agents_assemble.engine.judge import diagnose_strategy, rank_strategies, generate_judge_report
from agents_assemble.engine.recommender import generate_trade_recommendations, save_strategy_recommendation

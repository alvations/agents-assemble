"""Backtesting engine for agents-assemble.

Event-driven backtester with portfolio simulation, position management,
performance metrics, and transaction cost modeling.

Supports:
- Long/short positions
- Multiple assets simultaneously
- Commission and slippage modeling
- Benchmark comparison
- Comprehensive metrics (Sharpe, Sortino, max drawdown, Calmar, etc.)
- Signal-based and weight-based strategies
"""

from __future__ import annotations

import json
import math
import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable

import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# Extended backtest horizons (Feature 5)
# ---------------------------------------------------------------------------
EXTENDED_HORIZONS = {
    "2025": ("2025-01-01", "2025-12-31"),
    "2026_ytd": ("2026-01-01", datetime.now().strftime("%Y-%m-%d")),
}


# ---------------------------------------------------------------------------
# Historical black swan events for calibration (Feature 2)
# ---------------------------------------------------------------------------
HISTORICAL_CRASHES = {
    "covid_2020": {"magnitude": -0.34, "duration_days": 23, "recovery_days": 148,
                   "label": "COVID-19 Crash (Mar 2020)"},
    "gfc_2008": {"magnitude": -0.57, "duration_days": 355, "recovery_days": 1400,
                 "label": "Global Financial Crisis (2008-09)"},
    "flash_crash_2010": {"magnitude": -0.09, "duration_days": 1, "recovery_days": 4,
                         "label": "Flash Crash (May 2010)"},
    "dot_com_2000": {"magnitude": -0.49, "duration_days": 929, "recovery_days": 2500,
                     "label": "Dot-Com Bust (2000-02)"},
    "black_monday_1987": {"magnitude": -0.22, "duration_days": 1, "recovery_days": 400,
                          "label": "Black Monday (Oct 1987)"},
    "volmageddon_2018": {"magnitude": -0.10, "duration_days": 9, "recovery_days": 120,
                         "label": "Volmageddon (Feb 2018)"},
}

# Asset categories for black swan resilience scoring (Feature 3)
_DEFENSIVE_ASSETS = {
    "TLT", "IEF", "SHY", "BND", "AGG", "GOVT", "TIPS", "VTIP",  # Bonds
    "GLD", "IAU", "SLV", "SGOL",  # Gold/precious metals
    "BIL", "SHV", "MINT",  # Cash equivalents / T-bills
    "VPU", "XLU",  # Utilities
    "VNQ", "SCHD",  # REIT / dividend
}
_CONCENTRATED_GROWTH = {
    "QQQ", "ARKK", "TQQQ", "SOXL", "TECL", "SPXL",  # Leveraged / tech-heavy
    "TSLA", "NVDA", "AMD", "COIN", "MSTR",  # Volatile growth
}


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
class Side(Enum):
    BUY = "BUY"
    SELL = "SELL"


@dataclass
class Trade:
    date: pd.Timestamp
    symbol: str
    side: Side
    quantity: float
    price: float
    commission: float = 0.0
    slippage: float = 0.0

    @property
    def cost(self) -> float:
        """Total cost including fees."""
        base = self.quantity * self.price
        if self.side == Side.BUY:
            return base + self.commission + self.slippage
        return base - self.commission - self.slippage


@dataclass
class Position:
    symbol: str
    quantity: float = 0.0
    avg_cost: float = 0.0
    realized_pnl: float = 0.0

    def update(self, side: Side, qty: float, price: float) -> float:
        """Update position with a new trade. Returns realized P&L."""
        realized = 0.0
        if side == Side.BUY:
            if self.quantity >= 0:
                # Adding to or opening a long position
                total_cost = self.avg_cost * self.quantity + price * qty
                self.quantity += qty
                if self.quantity > 0:
                    self.avg_cost = total_cost / self.quantity
            else:
                # Covering a short position
                cover_qty = min(qty, abs(self.quantity))
                realized = (self.avg_cost - price) * cover_qty
                self.quantity += cover_qty
                remaining = qty - cover_qty
                if remaining > 0:
                    # Flipped from short to long
                    self.quantity = remaining
                    self.avg_cost = price
                elif self.quantity == 0:
                    self.avg_cost = 0.0
        else:  # SELL
            if self.quantity > 0:
                # Reducing or closing a long position
                close_qty = min(qty, self.quantity)
                realized = (price - self.avg_cost) * close_qty
                self.quantity -= close_qty
                remaining = qty - close_qty
                if remaining > 0:
                    # Flipped from long to short
                    self.quantity = -remaining
                    self.avg_cost = price
                elif self.quantity == 0:
                    self.avg_cost = 0.0
            else:
                # Adding to a short position
                total_cost = self.avg_cost * abs(self.quantity) + price * qty
                self.quantity -= qty
                if self.quantity < 0:
                    self.avg_cost = total_cost / abs(self.quantity)
        self.realized_pnl += realized
        return realized


@dataclass
class Portfolio:
    """Tracks cash, positions, and portfolio value over time."""
    initial_cash: float = 100_000.0
    cash: float | None = None
    positions: dict[str, Position] = field(default_factory=dict)
    trades: list[Trade] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)

    # Transaction cost model
    commission_per_trade: float = 0.0  # Robinhood = $0
    slippage_pct: float = 0.001  # 10 bps default slippage

    def __post_init__(self):
        if self.cash is None:
            self.cash = self.initial_cash

    def execute_trade(self, date: pd.Timestamp, symbol: str, side: Side,
                      quantity: float, price: float) -> Trade:
        """Execute a trade and update portfolio."""
        if not (quantity > 0):
            raise ValueError(f"Quantity must be positive, got {quantity}")
        if not (price > 0):
            raise ValueError(f"Price must be positive, got {price}")

        slippage = price * self.slippage_pct * quantity
        commission = self.commission_per_trade

        trade = Trade(date=date, symbol=symbol, side=side, quantity=quantity,
                      price=price, commission=commission, slippage=slippage)

        if symbol not in self.positions:
            self.positions[symbol] = Position(symbol=symbol)

        self.positions[symbol].update(side, quantity, price)

        if side == Side.BUY:
            self.cash -= trade.cost
        else:
            self.cash += trade.cost

        self.trades.append(trade)
        return trade

    def get_position(self, symbol: str) -> Position | None:
        pos = self.positions.get(symbol)
        if pos is not None and pos.quantity != 0:
            return pos
        return None

    def total_value(self, prices: dict[str, float]) -> float:
        """Calculate total portfolio value given current prices."""
        value = self.cash
        for sym, pos in self.positions.items():
            if pos.quantity != 0 and sym in prices:
                value += pos.quantity * prices[sym]
        return value

    def snapshot(self, date: pd.Timestamp, prices: dict[str, float]) -> dict[str, Any]:
        """Take a snapshot of portfolio state."""
        total = self.cash
        holdings = {}
        for sym, pos in self.positions.items():
            if pos.quantity != 0 and sym in prices:
                mv = pos.quantity * prices[sym]
                total += mv
                holdings[sym] = {
                    "quantity": pos.quantity,
                    "avg_cost": pos.avg_cost,
                    "market_value": mv,
                    "unrealized_pnl": (prices[sym] - pos.avg_cost) * pos.quantity,
                }
        if total > 0:
            for h in holdings.values():
                h["weight"] = h["market_value"] / total
        else:
            for h in holdings.values():
                h["weight"] = 0
        snap = {
            "date": date,
            "cash": self.cash,
            "total_value": total,
            "holdings": holdings,
            "num_positions": len(holdings),
        }
        self.history.append(snap)
        return snap


# ---------------------------------------------------------------------------
# Performance metrics
# ---------------------------------------------------------------------------
def compute_metrics(
    returns: pd.Series,
    benchmark_returns: pd.Series | None = None,
    risk_free_rate: float = 0.04,
    periods_per_year: int = 252,
) -> dict[str, float]:
    """Compute comprehensive performance metrics.

    Args:
        returns: Daily portfolio returns
        benchmark_returns: Daily benchmark returns (e.g., SPY)
        risk_free_rate: Annual risk-free rate (default 4% ~= current T-bill)
        periods_per_year: Trading days per year

    Returns:
        Dict of performance metrics
    """
    if returns.empty or len(returns) < 2:
        return {"error": "Insufficient data"}

    # Drop NaN and inf to prevent silent metric corruption.
    # pct_change() produces inf when equity touches zero then recovers;
    # inf propagates through mean/std/prod and silently corrupts all metrics.
    returns = returns.replace([float('inf'), float('-inf')], float('nan')).dropna()
    if len(returns) < 2:
        return {"error": "Insufficient data after removing NaN/inf"}

    # Basic return stats — compute cumulative product once and reuse for
    # total_return (here) and drawdown analysis (below)
    cum_returns = (1 + returns).cumprod()
    total_return = cum_returns.iloc[-1] - 1
    n_years = (returns.index[-1] - returns.index[0]).days / 365.25
    growth = 1 + total_return
    if growth > 0:
        try:
            cagr = growth ** (1 / max(n_years, 0.01)) - 1
        except OverflowError:
            cagr = float("inf")
    else:
        cagr = -1.0  # Total loss

    # Volatility
    daily_vol = returns.std()
    sqrt_periods = math.sqrt(periods_per_year)
    annual_vol = daily_vol * sqrt_periods

    # Sharpe ratio
    daily_rf = (1 + risk_free_rate) ** (1 / periods_per_year) - 1
    excess = returns - daily_rf
    excess_std = excess.std()
    if excess_std > 0:
        sharpe = excess.mean() / excess_std * sqrt_periods
    elif excess.mean() > 0:
        sharpe = float("inf")
    elif excess.mean() < 0:
        sharpe = float("-inf")
    else:
        sharpe = 0.0

    # Sortino ratio (downside deviation only)
    # Use arithmetic annualized excess return (same as Sharpe numerator)
    # so the two ratios are directly comparable.
    downside_diff = (returns - daily_rf).clip(upper=0)
    downside_dev = math.sqrt((downside_diff**2).mean()) * sqrt_periods
    annualized_excess = excess.mean() * periods_per_year
    if downside_dev > 0:
        sortino = annualized_excess / downside_dev
    elif annualized_excess > 0:
        sortino = float("inf")
    elif annualized_excess < 0:
        sortino = float("-inf")
    else:
        sortino = 0.0

    # Drawdown analysis (cum_returns already computed above)
    # clip(lower=1.0) treats the initial investment as a peak so that
    # early declines (e.g., equity drops from 1.0 to 0.8 on day 1) are
    # captured as drawdowns from the investor's starting capital.
    rolling_max = cum_returns.cummax().clip(lower=1.0)
    drawdowns = cum_returns / rolling_max - 1
    # Fix NaN from 0/0 when portfolio is wiped out (return of -1.0 makes
    # both cum_returns and rolling_max zero). NaN drawdown is -1.0 (total loss).
    drawdowns = drawdowns.fillna(-1.0)
    max_drawdown = drawdowns.min()
    max_dd_end = drawdowns.idxmin() if max_drawdown < 0 else None

    # Calmar ratio
    calmar = cagr / abs(max_drawdown) if max_drawdown < 0 else (float("inf") if cagr > 0 else 0)

    # Win rate
    winning_days = (returns > 0).sum()
    total_days = len(returns)
    win_rate = winning_days / total_days if total_days > 0 else 0

    # Profit factor
    gross_profit = returns[returns > 0].sum()
    gross_loss = abs(returns[returns < 0].sum())
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else (float("inf") if gross_profit > 0 else 0.0)

    # Skewness and kurtosis (NaN when variance is zero, e.g. constant returns)
    skew = returns.skew() if len(returns) >= 3 else 0.0
    if not math.isfinite(skew):
        skew = 0.0
    kurt = returns.kurtosis() if len(returns) >= 4 else 0.0
    if not math.isfinite(kurt):
        kurt = 0.0

    metrics = {
        "total_return": total_return,
        "cagr": cagr,
        "annual_volatility": annual_vol,
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "calmar_ratio": calmar,
        "max_drawdown": max_drawdown,
        "max_drawdown_date": max_dd_end.strftime("%Y-%m-%d") if max_dd_end is not None else None,
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "num_trading_days": total_days,
        "skewness": skew,
        "kurtosis": kurt,
        "best_day": returns.max(),
        "worst_day": returns.min(),
        "avg_daily_return": returns.mean(),
    }

    # Black swan resilience score (Feature 3) — 0-100 scale.
    # Higher = better expected performance during crashes.
    # Computed from: max drawdown depth, tail risk, and distribution shape.
    # Strategies with low drawdown, positive skew, and low kurtosis score higher.
    _dd_score = max(0, min(50, 50 * (1 + max_drawdown)))  # 0 if -100% DD, 50 if 0% DD
    _tail_score = max(0, min(25, 25 * (1 - abs(returns.quantile(0.01)))))  # 1st pctile
    _skew_score = max(0, min(25, 12.5 + 12.5 * min(1, max(-1, skew))))  # Positive skew helps
    metrics["black_swan_resilience"] = round(_dd_score + _tail_score + _skew_score, 1)

    # Benchmark comparison
    if benchmark_returns is not None and not benchmark_returns.empty:
        aligned = pd.DataFrame({"port": returns, "bench": benchmark_returns})
        aligned = aligned.replace([float('inf'), float('-inf')], float('nan')).dropna()
        if len(aligned) > 10:
            aligned_n_years = (aligned.index[-1] - aligned.index[0]).days / 365.25
            bench_total = (1 + aligned["bench"]).prod() - 1
            bench_growth = 1 + bench_total
            try:
                bench_cagr = bench_growth ** (1 / max(aligned_n_years, 0.01)) - 1 if bench_growth > 0 else -1.0
            except OverflowError:
                bench_cagr = float("inf")
            port_aligned_total = (1 + aligned["port"]).prod() - 1
            port_growth = 1 + port_aligned_total
            try:
                port_aligned_cagr = port_growth ** (1 / max(aligned_n_years, 0.01)) - 1 if port_growth > 0 else -1.0
            except OverflowError:
                port_aligned_cagr = float("inf")
            metrics["benchmark_total_return"] = bench_total
            metrics["benchmark_cagr"] = bench_cagr
            # Guard against inf - inf = nan when both CAGRs overflow
            alpha = port_aligned_cagr - bench_cagr
            if math.isnan(alpha):
                alpha = 0.0
            metrics["alpha"] = alpha

            # Beta
            cov = aligned[["port", "bench"]].cov()
            beta = cov.iloc[0, 1] / cov.iloc[1, 1] if cov.iloc[1, 1] > 0 else 0
            metrics["beta"] = beta

            # Information ratio (use guarded alpha to prevent nan propagation)
            tracking = aligned["port"] - aligned["bench"]
            tracking_error = tracking.std() * sqrt_periods
            info_ratio = alpha / tracking_error if tracking_error > 0 else 0
            metrics["information_ratio"] = info_ratio
            metrics["tracking_error"] = tracking_error

    return metrics


def compute_trade_metrics(trades: list[Trade]) -> dict[str, Any]:
    """Compute trade-level metrics."""
    if not trades:
        return {
            "num_trades": 0,
            "num_buys": 0,
            "num_sells": 0,
            "total_commission": 0.0,
            "total_slippage": 0.0,
            "total_transaction_costs": 0.0,
            "avg_trade_size": 0.0,
        }

    total_commission = sum(t.commission for t in trades)
    total_slippage = sum(t.slippage for t in trades)
    buys = [t for t in trades if t.side == Side.BUY]
    sells = [t for t in trades if t.side == Side.SELL]

    return {
        "num_trades": len(trades),
        "num_buys": len(buys),
        "num_sells": len(sells),
        "total_commission": total_commission,
        "total_slippage": total_slippage,
        "total_transaction_costs": total_commission + total_slippage,
        "avg_trade_size": sum(t.quantity * t.price for t in trades) / len(trades),
    }


# ---------------------------------------------------------------------------
# Backtester engine
# ---------------------------------------------------------------------------
class Backtester:
    """Event-driven backtester.

    Usage:
        def my_strategy(date, prices, portfolio, data):
            # Return dict of {symbol: target_weight} or {symbol: signal}
            if prices['AAPL'] < data['AAPL']['sma_50'].loc[date]:
                return {'AAPL': 0.5}  # 50% weight in AAPL
            return {'AAPL': 0.0}  # Exit

        bt = Backtester(
            strategy=my_strategy,
            symbols=['AAPL'],
            start='2022-01-01',
            end='2024-01-01'
        )
        results = bt.run()
        print(results['metrics'])
    """

    def __init__(
        self,
        strategy: Callable,
        symbols: list[str],
        start: str = "2020-01-01",
        end: str | None = None,
        initial_cash: float = 100_000.0,
        commission: float = 0.0,
        slippage_pct: float = 0.001,
        benchmark: str = "SPY",
        rebalance_frequency: str = "daily",  # daily, weekly, monthly
        data: dict[str, pd.DataFrame] | None = None,
    ):
        if not callable(strategy):
            raise TypeError(f"strategy must be callable, got {type(strategy).__name__}")
        self.strategy = strategy
        if not symbols:
            raise ValueError("symbols must be a non-empty list")
        self.symbols = symbols
        self.start = start
        self.end = end
        if end is not None and pd.Timestamp(start) > pd.Timestamp(end):
            raise ValueError(f"start ({start}) must be before end ({end})")
        if not (initial_cash > 0):
            raise ValueError(f"initial_cash must be positive, got {initial_cash}")
        if not (slippage_pct >= 0):
            raise ValueError(f"slippage_pct must be non-negative, got {slippage_pct}")
        if not (commission >= 0):
            raise ValueError(f"commission must be non-negative, got {commission}")
        self.initial_cash = initial_cash
        self.commission = commission
        self.slippage_pct = slippage_pct
        self.benchmark = benchmark
        if rebalance_frequency not in ("daily", "weekly", "monthly"):
            raise ValueError(
                f"rebalance_frequency must be 'daily', 'weekly', or 'monthly', "
                f"got {rebalance_frequency!r}"
            )
        self.rebalance_frequency = rebalance_frequency
        self._external_data = data

    def _load_data(self) -> tuple[dict[str, pd.DataFrame], pd.DataFrame | None]:
        """Load price data for all symbols + benchmark.

        Pre-loads 1 year before self.start so that indicators like SMA200
        are warm even on short-horizon backtests (1 week, 1 month, etc.).
        Performance is only measured from self.start to self.end.
        """
        from data_fetcher import fetch_ohlcv, fetch_multiple_ohlcv

        if self._external_data:
            all_data = dict(self._external_data)  # Shallow copy — don't mutate caller's dict
            for sym, df in all_data.items():
                if "Close" not in df.columns:
                    raise ValueError(f"External data for {sym!r} missing required 'Close' column")
        else:
            # Pre-load 1 year before start for indicator warmup
            warmup_start = (pd.Timestamp(self.start) - pd.DateOffset(days=365)).strftime("%Y-%m-%d")
            all_data = fetch_multiple_ohlcv(
                self.symbols, start=warmup_start, end=self.end
            )

        # Use Adj Close for return calculations if available (accounts for
        # dividends and splits).  Keep original Close for display purposes.
        for sym, df in all_data.items():
            if "Adj Close" in df.columns:
                adj = df["Adj Close"]
                if adj.notna().any():
                    # Preserve raw close for display, use adjusted for returns
                    df["Close_Raw"] = df["Close"]
                    df["Close"] = adj

        bench_data = None
        if self.benchmark:
            if self.benchmark in all_data:
                bench_data = all_data[self.benchmark]
            else:
                try:
                    bench_data = fetch_ohlcv(self.benchmark, start=self.start, end=self.end)
                    if bench_data is not None and "Adj Close" in bench_data.columns:
                        adj = bench_data["Adj Close"]
                        if adj.notna().any():
                            bench_data["Close_Raw"] = bench_data["Close"]
                            bench_data["Close"] = adj
                except Exception:
                    pass

        return all_data, bench_data

    def _should_rebalance(self, date: pd.Timestamp, dates: list[pd.Timestamp], idx: int) -> bool:
        """Check if we should rebalance on this date."""
        if self.rebalance_frequency == "daily":
            return True
        if self.rebalance_frequency == "weekly":
            if idx == 0:
                return True
            return date.isocalendar()[:2] != dates[idx - 1].isocalendar()[:2]
        if self.rebalance_frequency == "monthly":
            if idx == 0:
                return True
            return date.month != dates[idx - 1].month
        return True

    def run(self) -> dict[str, Any]:
        """Run the backtest.

        Returns dict with:
            - metrics: performance metrics
            - trade_metrics: trade statistics
            - portfolio_history: daily portfolio snapshots
            - trades: list of all trades
            - daily_returns: pd.Series of daily returns
            - equity_curve: pd.Series of portfolio value over time
        """
        all_data, bench_data = self._load_data()

        if not all_data:
            raise ValueError("No data loaded for any symbol")

        # Normalize all indexes to tz-naive for consistent comparison.
        # Copy DataFrames before modifying to avoid mutating caller's external data.
        for sym in list(all_data.keys()):
            if all_data[sym].index.tz is not None:
                df = all_data[sym].copy()
                df.index = df.index.tz_localize(None)
                all_data[sym] = df
        if bench_data is not None and bench_data.index.tz is not None:
            bench_data = bench_data.copy()
            bench_data.index = bench_data.index.tz_localize(None)

        portfolio = Portfolio(
            initial_cash=self.initial_cash,
            commission_per_trade=self.commission,
            slippage_pct=self.slippage_pct,
        )

        # Build close prices matrix — union index with forward-fill for partial data
        close_prices = pd.DataFrame({sym: df["Close"] for sym, df in all_data.items()})
        close_prices = close_prices.sort_index()
        # Deduplicate index — external data with duplicate dates causes
        # the simulation to process the same date twice (double-trading)
        close_prices = close_prices[~close_prices.index.duplicated(keep='last')]
        close_prices = close_prices.ffill()

        # Filter to requested date range (critical for external data which
        # bypasses fetch_multiple_ohlcv's own start/end filtering)
        if self.start:
            close_prices = close_prices.loc[close_prices.index >= pd.Timestamp(self.start)]
        if self.end:
            close_prices = close_prices.loc[close_prices.index <= pd.Timestamp(self.end)]

        common_dates = list(close_prices.index)

        if not common_dates:
            raise ValueError("No trading dates found across symbols")

        # Pre-compute technical indicators per symbol
        enriched_data = {}
        for sym, df in all_data.items():
            enriched = df.copy()
            close = enriched["Close"]
            sma_20 = close.rolling(20).mean()
            enriched["sma_20"] = sma_20
            enriched["sma_50"] = close.rolling(50).mean()
            enriched["sma_200"] = close.rolling(200).mean()
            enriched["ema_12"] = close.ewm(span=12).mean()
            enriched["ema_26"] = close.ewm(span=26).mean()
            enriched["macd"] = enriched["ema_12"] - enriched["ema_26"]
            enriched["macd_signal"] = enriched["macd"].ewm(span=9).mean()
            enriched["rsi_14"] = _compute_rsi(close, 14)
            enriched["bb_upper"], enriched["bb_lower"] = _compute_bollinger(close, 20, 2, sma=sma_20)
            if "High" in enriched.columns and "Low" in enriched.columns:
                enriched["atr_14"] = _compute_atr(enriched, 14)
            enriched["daily_return"] = close.pct_change()
            enriched["vol_20"] = enriched["daily_return"].rolling(20).std()
            if "Volume" in enriched.columns:
                enriched["volume_sma_20"] = enriched["Volume"].rolling(20).mean()

            # --- NEW INDICATORS ---

            # VWAP (Volume Weighted Average Price) - rolling 20-day
            if "Volume" in enriched.columns:
                typical_price = (enriched["High"] + enriched["Low"] + enriched["Close"]) / 3
                enriched["vwap_20"] = (typical_price * enriched["Volume"]).rolling(20).sum() / enriched["Volume"].rolling(20).sum()

            # OBV (On Balance Volume)
            if "Volume" in enriched.columns:
                obv = [0]
                closes = enriched["Close"].values
                volumes = enriched["Volume"].values
                for j in range(1, len(closes)):
                    if closes[j] > closes[j-1]:
                        obv.append(obv[-1] + volumes[j])
                    elif closes[j] < closes[j-1]:
                        obv.append(obv[-1] - volumes[j])
                    else:
                        obv.append(obv[-1])
                enriched["obv"] = obv
                enriched["obv_sma_20"] = pd.Series(obv, index=enriched.index).rolling(20).mean()

            # Stochastic Oscillator (%K, %D)
            if "High" in enriched.columns and "Low" in enriched.columns:
                low_14 = enriched["Low"].rolling(14).min()
                high_14 = enriched["High"].rolling(14).max()
                enriched["stoch_k"] = ((enriched["Close"] - low_14) / (high_14 - low_14)) * 100
                enriched["stoch_d"] = enriched["stoch_k"].rolling(3).mean()

                # Williams %R (14-period)
                enriched["williams_r"] = ((high_14 - enriched["Close"]) / (high_14 - low_14)) * -100

                # Ichimoku Cloud (simplified - Tenkan, Kijun, Senkou A/B)
                high_9 = enriched["High"].rolling(9).max()
                low_9 = enriched["Low"].rolling(9).min()
                high_26 = enriched["High"].rolling(26).max()
                low_26 = enriched["Low"].rolling(26).min()
                high_52 = enriched["High"].rolling(52).max()
                low_52 = enriched["Low"].rolling(52).min()
                enriched["ichimoku_tenkan"] = (high_9 + low_9) / 2      # Conversion line
                enriched["ichimoku_kijun"] = (high_26 + low_26) / 2      # Base line
                enriched["ichimoku_senkou_a"] = (enriched["ichimoku_tenkan"] + enriched["ichimoku_kijun"]) / 2
                enriched["ichimoku_senkou_b"] = (high_52 + low_52) / 2

            # Rate of Change (12-period)
            enriched["roc_12"] = enriched["Close"].pct_change(12) * 100

            # Commodity Channel Index (20-period)
            if "High" in enriched.columns and "Low" in enriched.columns:
                tp = (enriched["High"] + enriched["Low"] + enriched["Close"]) / 3
                tp_sma = tp.rolling(20).mean()
                tp_mad = tp.rolling(20).apply(lambda x: abs(x - x.mean()).mean(), raw=True)
                enriched["cci_20"] = (tp - tp_sma) / (0.015 * tp_mad)

            enriched_data[sym] = enriched

        # Pre-compute prices dict — avoids per-iteration pandas Series creation
        _raw_prices = close_prices.to_dict('index')
        prices_lookup = {
            dt: {sym: v for sym, v in row.items() if pd.notna(v)}
            for dt, row in _raw_prices.items()
        }

        # Gather external signals once (Feature 4) — these are static stubs
        # for now but will pull live data when API keys are configured.
        external_signals = gather_external_signals(self.symbols)

        # Run simulation
        equity_values = []
        equity_dates = []
        strategy_errors = 0

        for idx, date in enumerate(common_dates):
            prices = prices_lookup.get(date, {})

            if not self._should_rebalance(date, common_dates, idx) or not prices:
                snap = portfolio.snapshot(date, prices)
                equity_values.append(snap["total_value"])
                equity_dates.append(date)
                continue

            # Call strategy — try passing external_signals if the strategy
            # accepts a 5th positional arg; fall back to 4-arg call.
            try:
                try:
                    target_weights = self.strategy(
                        date, prices, portfolio, enriched_data, external_signals
                    )
                except TypeError:
                    # Strategy doesn't accept external_signals — use old signature
                    target_weights = self.strategy(date, prices, portfolio, enriched_data)
            except Exception:
                target_weights = {}
                strategy_errors += 1

            if not isinstance(target_weights, dict):
                target_weights = {}
                strategy_errors += 1

            if target_weights:
                self._rebalance(portfolio, target_weights, prices, date)

            snap = portfolio.snapshot(date, prices)
            equity_values.append(snap["total_value"])
            equity_dates.append(date)

        if not equity_values:
            raise ValueError("No data points generated during backtest")

        # Compute results
        equity_curve = pd.Series(equity_values, index=equity_dates)
        # Post-wipeout 0→0 returns are 0% (not NaN from 0/0 division).
        # Without this, dropna removes all post-wipeout days, computing
        # metrics from only pre-wipeout returns which is misleading.
        daily_returns = equity_curve.pct_change()
        zero_to_zero = (equity_curve == 0) & (equity_curve.shift(1) == 0)
        daily_returns = daily_returns.where(~zero_to_zero, 0.0).dropna()

        bench_returns = None
        if bench_data is not None and not bench_data.empty:
            bench_close = bench_data["Close"].dropna()
            if bench_close.index.has_duplicates:
                bench_close = bench_close[~bench_close.index.duplicated(keep='last')]
            bench_returns = bench_close.pct_change().dropna()

        metrics = compute_metrics(daily_returns, bench_returns)
        trade_metrics = compute_trade_metrics(portfolio.trades)

        return {
            "metrics": metrics,
            "trade_metrics": trade_metrics,
            "portfolio_history": portfolio.history,
            "trades": portfolio.trades,
            "daily_returns": daily_returns,
            "equity_curve": equity_curve,
            "initial_value": self.initial_cash,
            "final_value": equity_values[-1] if equity_values else self.initial_cash,
            "final_positions": {
                sym: {"qty": pos.quantity, "avg_cost": pos.avg_cost, "realized_pnl": pos.realized_pnl}
                for sym, pos in portfolio.positions.items() if pos.quantity != 0
            },
            "strategy_errors": strategy_errors,
        }

    def _rebalance(self, portfolio: Portfolio, target_weights: dict[str, float],
                   prices: dict[str, float], date: pd.Timestamp) -> None:
        """Rebalance portfolio to target weights."""
        # Filter out non-finite weights (NaN/inf from strategy bugs).
        # NaN weights silently fail all comparisons, leaving stale positions;
        # inf weights cause OverflowError in int(round(inf / price)).
        # Preserve original keys so filtered symbols are treated as "hold
        # current position" rather than orphans to be closed.
        _requested_syms = set(target_weights)
        target_weights = {k: v for k, v in target_weights.items()
                          if isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)}
        total_value = portfolio.total_value(prices)
        if total_value <= 0:
            return

        # Phase 1: Collect and execute all sells (reductions, closes, short initiations)
        sells: list[tuple[str, float]] = []

        for sym, target_w in target_weights.items():
            if sym not in prices:
                continue
            price = prices[sym]
            if not (price > 0):
                continue
            target_value = total_value * target_w
            current_pos = portfolio.get_position(sym)
            current_value = (current_pos.quantity * price) if current_pos else 0.0
            diff_value = target_value - current_value
            if diff_value < 0 and abs(diff_value) >= price * 0.5:
                qty = int(round(abs(diff_value) / price))
                if qty > 0:
                    sells.append((sym, qty))

        # Close long positions not in target weights (but not those the
        # strategy requested with an invalid weight — those are held as-is)
        for sym in list(portfolio.positions.keys()):
            if sym not in _requested_syms:
                pos = portfolio.get_position(sym)
                if pos is not None and pos.quantity > 0 and sym in prices and prices[sym] > 0:
                    sells.append((sym, pos.quantity))

        for sym, qty in sells:
            portfolio.execute_trade(date, sym, Side.SELL, qty, prices[sym])

        # Phase 2: Recompute total value after sells, then collect buys
        total_value = portfolio.total_value(prices)
        if total_value <= 0:
            return
        buys: list[tuple[str, float, float]] = []

        for sym, target_w in target_weights.items():
            if sym not in prices:
                continue
            price = prices[sym]
            if not (price > 0):
                continue
            target_value = total_value * target_w
            current_pos = portfolio.get_position(sym)
            current_value = (current_pos.quantity * price) if current_pos else 0.0
            diff_value = target_value - current_value
            if diff_value >= price * 0.5:
                qty = int(round(diff_value / price))
                if qty > 0:
                    # Covering shorts gets highest priority (same as orphaned short closes)
                    priority = float("inf") if (current_pos and current_pos.quantity < 0) else target_w
                    buys.append((sym, qty, priority))

        # Close short positions not in target weights (highest priority)
        for sym in list(portfolio.positions.keys()):
            if sym not in _requested_syms:
                pos = portfolio.get_position(sym)
                if pos is not None and pos.quantity < 0 and sym in prices and prices[sym] > 0:
                    buys.append((sym, abs(pos.quantity), float("inf")))

        # Execute buys with highest-weight positions first
        buys.sort(key=lambda x: -x[2])
        for sym, qty, _ in buys:
            price = prices[sym]
            cost_per_share = price * (1 + portfolio.slippage_pct)
            total_cost = qty * cost_per_share + portfolio.commission_per_trade
            if portfolio.cash >= total_cost:
                portfolio.execute_trade(date, sym, Side.BUY, qty, price)
            else:
                # Partial fill — buy as many shares as cash allows
                affordable = int((portfolio.cash - portfolio.commission_per_trade) / cost_per_share) if cost_per_share > 0 else 0
                if affordable > 0:
                    portfolio.execute_trade(date, sym, Side.BUY, affordable, price)

    def run_with_analysis(self) -> dict[str, Any]:
        """Run backtest and attach forward predictions + black swan analysis.

        Convenience method that calls run(), then enriches results with:
        - forward_predictions: list of ForwardPrediction
        - black_swan_results: list of BlackSwanResult
        - black_swan_resilience: 0-100 score

        Returns:
            Same dict as run(), plus analysis fields.
        """
        results = self.run()

        equity_curve = results.get("equity_curve", pd.Series(dtype=float))
        daily_returns = results.get("daily_returns", pd.Series(dtype=float))

        # Forward predictions (Feature 1)
        results["forward_predictions"] = predict_forward(equity_curve, daily_returns)

        # Black swan simulation (Feature 2)
        swan_results = simulate_black_swan(equity_curve, daily_returns)
        results["black_swan_results"] = swan_results

        # Black swan resilience with portfolio composition (Feature 3)
        holdings = {}
        last_snap = results.get("portfolio_history", [])
        if last_snap:
            holdings = last_snap[-1].get("holdings", {})
        results["black_swan_resilience"] = compute_black_swan_resilience(
            swan_results, holdings
        )

        return results


# ---------------------------------------------------------------------------
# Technical indicator helpers
# ---------------------------------------------------------------------------
def _compute_rsi(prices: pd.Series, period: int = 14) -> pd.Series:
    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0.0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, float("nan"))
    rsi = 100 - (100 / (1 + rs))
    # When loss==0 but gain>0 (all up days in window), RSI should be 100 not NaN
    rsi.loc[(loss == 0) & (gain > 0)] = 100.0
    # When both gain and loss are 0 (flat prices), RSI is neutral at 50
    rsi.loc[(loss == 0) & (gain == 0)] = 50.0
    return rsi


def _compute_bollinger(prices: pd.Series, period: int = 20,
                       num_std: float = 2, *,
                       sma: pd.Series | None = None) -> tuple[pd.Series, pd.Series]:
    if sma is None:
        sma = prices.rolling(period).mean()
    std = prices.rolling(period).std()
    return sma + num_std * std, sma - num_std * std


def _compute_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    high = df["High"]
    low = df["Low"]
    close = df["Close"].shift(1)
    tr = pd.concat([high - low, (high - close).abs(), (low - close).abs()], axis=1).max(axis=1)
    return tr.rolling(period).mean()


# ---------------------------------------------------------------------------
# Forward Prediction Engine (Feature 1) — EXPERIMENTAL
# ---------------------------------------------------------------------------
@dataclass
class ForwardPrediction:
    """EXPERIMENTAL: Forward return predictions with confidence intervals.

    Uses exponential smoothing + mean reversion toward historical CAGR.
    NOT investment advice. Predictions are calibrated extrapolations only.
    """
    horizon_label: str  # e.g. "1M", "3M", "6M", "12M"
    horizon_days: int
    base_return: float  # Base case predicted return
    optimistic_return: float  # Upper confidence bound (~75th pctile)
    pessimistic_return: float  # Lower confidence bound (~25th pctile)
    annualized_base: float  # Base return annualized
    confidence: float  # 0-1 confidence level (decays with horizon)
    method: str = "exponential_smoothing_mean_reversion"


def predict_forward(
    equity_curve: pd.Series,
    daily_returns: pd.Series,
    lookback_years: float = 3.0,
    horizons: dict[str, int] | None = None,
) -> list[ForwardPrediction]:
    """EXPERIMENTAL: Predict forward returns using trend extrapolation.

    Uses the last `lookback_years` of backtest data to project returns for
    multiple forward horizons. Combines exponential smoothing of recent
    momentum with mean reversion toward the historical CAGR.

    Args:
        equity_curve: Portfolio value time series from backtest.
        daily_returns: Daily return series from backtest.
        lookback_years: Years of history to use for calibration (default 3).
        horizons: Dict of {label: trading_days}. Defaults to standard set.

    Returns:
        List of ForwardPrediction for each horizon.
    """
    if horizons is None:
        horizons = {"1M": 21, "3M": 63, "6M": 126, "12M": 252}

    if len(daily_returns) < 60:
        # Not enough data to produce meaningful predictions
        return [
            ForwardPrediction(
                horizon_label=label, horizon_days=days,
                base_return=0.0, optimistic_return=0.0, pessimistic_return=0.0,
                annualized_base=0.0, confidence=0.0,
                method="insufficient_data",
            )
            for label, days in horizons.items()
        ]

    # Trim to lookback window
    lookback_days = int(lookback_years * 252)
    rets = daily_returns.iloc[-lookback_days:].copy()
    rets = rets.replace([float('inf'), float('-inf')], float('nan')).dropna()

    if len(rets) < 60:
        return [
            ForwardPrediction(
                horizon_label=label, horizon_days=days,
                base_return=0.0, optimistic_return=0.0, pessimistic_return=0.0,
                annualized_base=0.0, confidence=0.0,
                method="insufficient_data",
            )
            for label, days in horizons.items()
        ]

    # Historical CAGR (annualized)
    cum = (1 + rets).cumprod()
    n_years = len(rets) / 252.0
    historical_cagr = (cum.iloc[-1] ** (1 / max(n_years, 0.01))) - 1

    # Exponential smoothing of recent daily returns (alpha=0.02 for ~50-day half-life)
    alpha = 0.02
    smoothed_daily = rets.ewm(alpha=alpha).mean().iloc[-1]

    # Realized volatility (annualized)
    daily_vol = rets.std()
    annual_vol = daily_vol * math.sqrt(252)

    # Recent momentum (last 63 trading days annualized)
    recent = rets.iloc[-min(63, len(rets)):]
    recent_momentum = (1 + recent).prod() ** (252 / len(recent)) - 1

    predictions = []
    for label, days in horizons.items():
        # Blend: short horizons favor momentum, long horizons favor mean reversion
        # Weight shifts from 80% momentum at 1M to 20% momentum at 12M
        momentum_weight = max(0.2, 1.0 - (days / 252) * 0.8)
        reversion_weight = 1.0 - momentum_weight

        # Daily expected return from each component
        momentum_daily = smoothed_daily * 0.5 + (recent_momentum / 252) * 0.5
        reversion_daily = historical_cagr / 252

        blended_daily = momentum_weight * momentum_daily + reversion_weight * reversion_daily

        # Compound for the horizon
        base_return = (1 + blended_daily) ** days - 1

        # Confidence intervals using historical volatility
        # Scale vol by sqrt(days) for the horizon
        horizon_vol = daily_vol * math.sqrt(days)

        # Optimistic: ~75th percentile; Pessimistic: ~25th percentile
        # Using 0.675 z-score for 75th/25th percentile
        optimistic_return = base_return + 0.675 * horizon_vol
        pessimistic_return = base_return - 0.675 * horizon_vol

        # Annualize the base return
        if days > 0:
            annualized_base = (1 + base_return) ** (252 / days) - 1
        else:
            annualized_base = 0.0

        # Confidence decays with horizon: ~0.7 at 1M, ~0.3 at 12M
        confidence = max(0.1, 0.8 - (days / 252) * 0.5)

        predictions.append(ForwardPrediction(
            horizon_label=label,
            horizon_days=days,
            base_return=base_return,
            optimistic_return=optimistic_return,
            pessimistic_return=pessimistic_return,
            annualized_base=annualized_base,
            confidence=confidence,
            method="exponential_smoothing_mean_reversion",
        ))

    return predictions


def format_predictions(predictions: list[ForwardPrediction]) -> str:
    """Format forward predictions as a readable table."""
    lines = [
        "",
        "=" * 60,
        "  EXPERIMENTAL: Forward Return Predictions",
        "  (NOT investment advice — calibrated extrapolation only)",
        "=" * 60,
        "",
        f"  {'Horizon':<10s} {'Pessimistic':>12s} {'Base':>12s} {'Optimistic':>12s} {'Confidence':>12s}",
        f"  {'-' * 10} {'-' * 12} {'-' * 12} {'-' * 12} {'-' * 12}",
    ]
    for p in predictions:
        lines.append(
            f"  {p.horizon_label:<10s} "
            f"{p.pessimistic_return:>11.2%} "
            f"{p.base_return:>11.2%} "
            f"{p.optimistic_return:>11.2%} "
            f"{p.confidence:>11.0%}"
        )
    lines.append("")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Black Swan Simulation (Feature 2)
# ---------------------------------------------------------------------------
@dataclass
class BlackSwanResult:
    """Results from injecting a black swan event into an equity curve."""
    scenario_name: str
    crash_magnitude: float  # e.g. -0.34
    crash_duration_days: int
    original_final_value: float
    stressed_final_value: float
    stressed_max_drawdown: float
    recovery_days: int | None  # Days to recover to pre-crash level (None if never)
    tail_risk_var_95: float  # 95th percentile daily VaR under stress
    tail_risk_var_99: float  # 99th percentile daily VaR under stress


def simulate_black_swan(
    equity_curve: pd.Series,
    daily_returns: pd.Series,
    scenarios: dict[str, dict] | None = None,
    injection_point: float = 0.7,
) -> list[BlackSwanResult]:
    """Simulate black swan crash events on a backtest equity curve.

    Injects synthetic crash events at a specified point in the equity curve
    and measures the strategy's resilience. Uses deterministic scenarios
    calibrated from historical crashes (NOT Monte Carlo).

    Args:
        equity_curve: Portfolio value time series from backtest.
        daily_returns: Daily return series from backtest.
        scenarios: Dict of crash scenarios. Defaults to HISTORICAL_CRASHES.
            Each entry: {"magnitude": float, "duration_days": int,
                         "recovery_days": int, "label": str}
        injection_point: Where in the curve to inject (0-1, default 0.7 = 70%).

    Returns:
        List of BlackSwanResult, one per scenario.
    """
    if scenarios is None:
        scenarios = HISTORICAL_CRASHES

    if len(equity_curve) < 20:
        return []

    results = []
    inject_idx = int(len(equity_curve) * max(0.1, min(0.9, injection_point)))

    for name, params in scenarios.items():
        magnitude = params["magnitude"]  # e.g. -0.34
        crash_days = max(1, params["duration_days"])
        label = params.get("label", name)

        # Build the stressed equity curve
        stressed = equity_curve.copy().values.astype(float)
        dates = equity_curve.index

        # Pre-crash value
        pre_crash_value = stressed[inject_idx]

        # Apply crash: distribute the total drop over crash_days
        # Using an exponential decay pattern (most damage early)
        actual_crash_days = min(crash_days, len(stressed) - inject_idx - 1)
        if actual_crash_days < 1:
            actual_crash_days = 1

        for d in range(actual_crash_days):
            # Exponential decay: most of the drop happens early
            if actual_crash_days == 1:
                day_frac = 1.0
            else:
                day_frac = 1.0 - math.exp(-3.0 * (d + 1) / actual_crash_days)
            drop_so_far = magnitude * day_frac
            idx = inject_idx + d + 1
            if idx < len(stressed):
                stressed[idx] = pre_crash_value * (1 + drop_so_far)

        # Post-crash: scale all remaining values by the crash factor,
        # then blend back toward original curve (slow recovery)
        crash_end_idx = inject_idx + actual_crash_days + 1
        if crash_end_idx < len(stressed):
            crash_bottom = stressed[min(crash_end_idx - 1, len(stressed) - 1)]
            original_at_crash_end = equity_curve.values[min(crash_end_idx, len(equity_curve) - 1)]
            if original_at_crash_end > 0:
                scale_factor = crash_bottom / original_at_crash_end
            else:
                scale_factor = 1.0

            for i in range(crash_end_idx, len(stressed)):
                # Gradually recover: blend between scaled (crashed) and original
                days_since_crash = i - crash_end_idx
                # Recovery factor: 0 at crash end, approaches 1 asymptotically
                # Half-life proportional to historical recovery time
                hist_recovery = params.get("recovery_days", 252)
                half_life = max(20, hist_recovery * 0.3)
                recovery_frac = 1.0 - math.exp(-0.693 * days_since_crash / half_life)
                stressed[i] = (
                    scale_factor * equity_curve.values[i] * (1 - recovery_frac)
                    + equity_curve.values[i] * recovery_frac
                )

        stressed_series = pd.Series(stressed, index=dates)

        # Compute stressed metrics
        stressed_returns = stressed_series.pct_change().dropna()
        stressed_returns = stressed_returns.replace([float('inf'), float('-inf')], float('nan')).dropna()

        # Max drawdown of stressed curve
        cum = stressed_series / stressed_series.cummax().clip(lower=stressed_series.iloc[0])
        stressed_max_dd = (cum - 1).min()

        # Recovery time: days after crash bottom to return to pre-crash level
        recovery_days_result = None
        crash_bottom_idx = inject_idx + actual_crash_days
        if crash_bottom_idx < len(stressed):
            for i in range(crash_bottom_idx, len(stressed)):
                if stressed[i] >= pre_crash_value:
                    recovery_days_result = i - crash_bottom_idx
                    break

        # Tail risk VaR
        if len(stressed_returns) > 10:
            var_95 = float(np.percentile(stressed_returns, 5))
            var_99 = float(np.percentile(stressed_returns, 1))
        else:
            var_95 = 0.0
            var_99 = 0.0

        results.append(BlackSwanResult(
            scenario_name=label,
            crash_magnitude=magnitude,
            crash_duration_days=crash_days,
            original_final_value=float(equity_curve.iloc[-1]),
            stressed_final_value=float(stressed[-1]),
            stressed_max_drawdown=float(stressed_max_dd),
            recovery_days=recovery_days_result,
            tail_risk_var_95=var_95,
            tail_risk_var_99=var_99,
        ))

    return results


def compute_black_swan_resilience(
    black_swan_results: list[BlackSwanResult],
    holdings: dict[str, Any] | None = None,
) -> float:
    """Compute a 0-100 black swan resilience score.

    Combines:
    - Performance under simulated crashes (50 points)
    - Asset composition bonus/penalty (30 points)
    - Recovery speed (20 points)

    Args:
        black_swan_results: Results from simulate_black_swan().
        holdings: Current portfolio holdings dict {symbol: {...}} for
                  asset-class scoring. Optional.

    Returns:
        Score from 0 (extremely fragile) to 100 (highly resilient).
    """
    if not black_swan_results:
        return 50.0  # Neutral if no data

    # --- Crash survival score (0-50) ---
    # How much value is retained after each crash scenario?
    survival_scores = []
    for r in black_swan_results:
        if r.original_final_value > 0:
            retention = r.stressed_final_value / r.original_final_value
            # Scale: 1.0 retention = 50, 0.5 retention = 25, 0 = 0
            survival_scores.append(max(0, min(50, retention * 50)))
        else:
            survival_scores.append(0)
    crash_score = sum(survival_scores) / len(survival_scores) if survival_scores else 25

    # --- Asset composition score (0-30) ---
    composition_score = 15.0  # Neutral default
    if holdings:
        symbols = set(holdings.keys())
        defensive_count = len(symbols & _DEFENSIVE_ASSETS)
        growth_count = len(symbols & _CONCENTRATED_GROWTH)
        total = len(symbols) if symbols else 1

        # Defensive fraction boosts score, concentrated growth penalizes
        defensive_frac = defensive_count / total
        growth_frac = growth_count / total
        composition_score = 15 + 15 * defensive_frac - 15 * growth_frac
        composition_score = max(0, min(30, composition_score))

    # --- Recovery speed score (0-20) ---
    recovery_scores = []
    for r in black_swan_results:
        if r.recovery_days is not None:
            # Fast recovery (<60 days) = 20, slow (>500 days) = 0
            score = max(0, min(20, 20 * (1 - r.recovery_days / 500)))
            recovery_scores.append(score)
        else:
            recovery_scores.append(0)  # Never recovered
    recovery_score = sum(recovery_scores) / len(recovery_scores) if recovery_scores else 10

    return round(max(0, min(100, crash_score + composition_score + recovery_score)), 1)


def format_black_swan_report(results: list[BlackSwanResult], resilience_score: float | None = None) -> str:
    """Format black swan simulation results as a readable report."""
    lines = [
        "",
        "=" * 72,
        "  Black Swan Stress Test Results",
        "=" * 72,
        "",
    ]
    if resilience_score is not None:
        lines.append(f"  Overall Resilience Score: {resilience_score:.1f} / 100")
        lines.append("")

    for r in results:
        value_change = (r.stressed_final_value / r.original_final_value - 1) if r.original_final_value > 0 else -1
        recovery_str = f"{r.recovery_days} days" if r.recovery_days is not None else "Never"
        lines.extend([
            f"  {r.scenario_name}",
            f"    Crash: {r.crash_magnitude:+.1%} over {r.crash_duration_days} day(s)",
            f"    Final Value Impact: {value_change:+.2%}  (${r.stressed_final_value:,.0f} vs ${r.original_final_value:,.0f})",
            f"    Stressed Max DD: {r.stressed_max_drawdown:.2%}",
            f"    Recovery Time: {recovery_str}",
            f"    VaR (95/99): {r.tail_risk_var_95:.2%} / {r.tail_risk_var_99:.2%}",
            "",
        ])

    lines.append("=" * 72)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Sentiment Integration Stubs (Feature 4)
# ---------------------------------------------------------------------------
def _get_polymarket_signal(tickers: list[str] | None = None) -> dict[str, Any]:
    """Stub: Fetch market-implied probabilities from Polymarket.

    Returns dict with market-implied event probabilities that can inform
    trading decisions (e.g., election outcomes, rate decisions, geopolitical).

    Requires POLYMARKET_API_KEY env var. Returns empty dict if unavailable.
    """
    api_key = os.environ.get("POLYMARKET_API_KEY", "")
    if not api_key:
        return {}
    # TODO: Implement actual API call when key is available
    # Expected return format:
    # {
    #     "events": {
    #         "rate_cut_2025": {"probability": 0.65, "volume": 1200000},
    #         "recession_2025": {"probability": 0.20, "volume": 800000},
    #     },
    #     "timestamp": "2025-04-08T12:00:00Z",
    #     "source": "polymarket",
    # }
    return {}


def _get_reddit_sentiment(tickers: list[str] | None = None) -> dict[str, Any]:
    """Stub: Fetch ticker sentiment scores from Reddit (r/wallstreetbets, etc.).

    Returns dict with sentiment scores per ticker (-1 to +1 scale).

    Requires REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET env vars.
    Returns empty dict if unavailable.
    """
    client_id = os.environ.get("REDDIT_CLIENT_ID", "")
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET", "")
    if not client_id or not client_secret:
        return {}
    # TODO: Implement actual API call when credentials are available
    # Expected return format:
    # {
    #     "ticker_sentiment": {
    #         "AAPL": {"score": 0.35, "mentions": 142, "bullish_pct": 0.67},
    #         "TSLA": {"score": -0.12, "mentions": 89, "bullish_pct": 0.44},
    #     },
    #     "subreddits": ["wallstreetbets", "stocks", "investing"],
    #     "timestamp": "2025-04-08T12:00:00Z",
    #     "source": "reddit",
    # }
    return {}


def _get_kalshi_events(tickers: list[str] | None = None) -> dict[str, Any]:
    """Stub: Fetch event contract prices from Kalshi prediction market.

    Returns dict with event contract prices for macro/market events.

    Requires KALSHI_API_KEY env var. Returns empty dict if unavailable.
    """
    api_key = os.environ.get("KALSHI_API_KEY", "")
    if not api_key:
        return {}
    # TODO: Implement actual API call when key is available
    # Expected return format:
    # {
    #     "events": {
    #         "fed_rate_hold": {"price": 0.72, "volume": 50000},
    #         "sp500_above_5000": {"price": 0.85, "volume": 30000},
    #     },
    #     "timestamp": "2025-04-08T12:00:00Z",
    #     "source": "kalshi",
    # }
    return {}


def gather_external_signals(tickers: list[str] | None = None) -> dict[str, Any]:
    """Gather all available external signals into a single dict.

    Calls each signal source and merges results. Sources that return
    empty dicts (no API key) are silently skipped.

    Returns:
        Dict with keys "polymarket", "reddit", "kalshi" (only present if
        the source returned data).
    """
    signals = {}

    poly = _get_polymarket_signal(tickers)
    if poly:
        signals["polymarket"] = poly

    reddit = _get_reddit_sentiment(tickers)
    if reddit:
        signals["reddit"] = reddit

    kalshi = _get_kalshi_events(tickers)
    if kalshi:
        signals["kalshi"] = kalshi

    return signals


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------
def _fmt_ratio(value: float) -> str:
    """Format a ratio that may be infinite (calmar, profit_factor)."""
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        return "       N/A"
    return f"{value:>10.2f}"


def _fmt_pct(value: float) -> str:
    """Format a percentage that may be infinite (alpha on extreme short backtests)."""
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        return "       N/A"
    return f"{value:>10.2%}"


def format_report(results: dict[str, Any], title: str = "Backtest Report") -> str:
    """Format backtest results as a readable report."""
    m = results["metrics"]
    tm = results["trade_metrics"]

    if "error" in m:
        return f"{'=' * 60}\n  {title}\n{'=' * 60}\n\n  Error: {m['error']}\n\n{'=' * 60}"

    lines = [
        f"{'=' * 60}",
        f"  {title}",
        f"{'=' * 60}",
        "",
        "--- Performance ---",
        f"  Total Return:       {_fmt_pct(m.get('total_return', 0))}",
        f"  CAGR:               {_fmt_pct(m.get('cagr', 0))}",
        f"  Annual Volatility:  {_fmt_pct(m.get('annual_volatility', 0))}",
        f"  Sharpe Ratio:       {_fmt_ratio(m.get('sharpe_ratio', 0))}",
        f"  Sortino Ratio:      {_fmt_ratio(m.get('sortino_ratio', 0))}",
        f"  Calmar Ratio:       {_fmt_ratio(m.get('calmar_ratio', 0))}",
        f"  Max Drawdown:       {_fmt_pct(m.get('max_drawdown', 0))}",
        f"  Max DD Date:        {m.get('max_drawdown_date') or '       N/A':>10s}",
        f"  Trading Days:       {int(m.get('num_trading_days', 0)):>10d}",
        f"  Win Rate:           {_fmt_pct(m.get('win_rate', 0))}",
        f"  Profit Factor:      {_fmt_ratio(m.get('profit_factor', 0))}",
        "",
        "--- Trades ---",
        f"  Total Trades:       {tm.get('num_trades', 0):>10d}",
        f"  Buys:               {tm.get('num_buys', 0):>10d}",
        f"  Sells:              {tm.get('num_sells', 0):>10d}",
        f"  Total Costs:        ${tm.get('total_transaction_costs', 0):>9.2f}",
        "",
        "--- Portfolio ---",
        f"  Initial Value:      ${results.get('initial_value', 100_000):>10,.2f}",
        f"  Final Value:        ${results.get('final_value', 0):>10,.2f}",
    ]

    strategy_errors = results.get("strategy_errors", 0)
    if strategy_errors:
        lines.extend([
            "",
            "--- Warnings ---",
            f"  Strategy Errors:    {strategy_errors:>10d}",
        ])

    if "black_swan_resilience" in m:
        lines.extend([
            "",
            "--- Risk ---",
            f"  Swan Resilience:    {m['black_swan_resilience']:>10.1f} / 100",
        ])

    if "benchmark_total_return" in m:
        lines.extend([
            "",
            "--- vs Benchmark ---",
            f"  Benchmark Return:   {_fmt_pct(m.get('benchmark_total_return', 0))}",
            f"  Alpha:              {_fmt_pct(m.get('alpha', 0))}",
            f"  Beta:               {_fmt_ratio(m.get('beta', 0))}",
            f"  Info Ratio:         {_fmt_ratio(m.get('information_ratio', 0))}",
        ])

    lines.append(f"\n{'=' * 60}")
    return "\n".join(lines)


def _sanitize_for_json(obj):
    """Replace float inf/nan with None and Timestamps with strings for JSON compliance."""
    if isinstance(obj, pd.Timestamp):
        return obj.strftime("%Y-%m-%d")
    if isinstance(obj, float) and (math.isinf(obj) or math.isnan(obj)):
        return None
    if isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_for_json(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_sanitize_for_json(v) for v in obj)
    return obj


def save_results(results: dict[str, Any], path: str) -> None:
    """Save backtest results to JSON."""
    serializable = {}
    for k, v in results.items():
        if isinstance(v, pd.Series):
            serializable[k] = {str(idx): float(val) for idx, val in v.items()}
        elif isinstance(v, list) and v and isinstance(v[0], Trade):
            serializable[k] = [
                {"date": str(t.date), "symbol": t.symbol, "side": t.side.value,
                 "quantity": t.quantity, "price": t.price,
                 "commission": t.commission, "slippage": t.slippage}
                for t in v
            ]
        elif isinstance(v, list):
            serializable[k] = _sanitize_for_json(v)
        elif isinstance(v, dict):
            serializable[k] = {str(kk): vv for kk, vv in v.items()
                                if not isinstance(vv, (pd.Series, pd.DataFrame))}
        else:
            try:
                json.dumps(v)
                serializable[k] = v
            except (TypeError, ValueError):
                serializable[k] = str(v)

    serializable = _sanitize_for_json(serializable)
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(serializable, indent=2, default=str))


if __name__ == "__main__":
    # Simple buy-and-hold strategy test
    def buy_and_hold(date, prices, portfolio, data):
        if not portfolio.get_position("AAPL"):
            return {"AAPL": 0.95}
        return {}

    bt = Backtester(
        strategy=buy_and_hold,
        symbols=["AAPL"],
        start="2023-01-01",
        end="2024-12-31",
    )
    results = bt.run()
    print(format_report(results, "Buy & Hold AAPL"))

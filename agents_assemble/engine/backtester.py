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
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable

import pandas as pd


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

    @property
    def market_value(self) -> float:
        return 0.0  # Updated externally with current price

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
    cash: float = 100_000.0
    positions: dict[str, Position] = field(default_factory=dict)
    trades: list[Trade] = field(default_factory=list)
    history: list[dict[str, Any]] = field(default_factory=list)

    # Transaction cost model
    commission_per_trade: float = 0.0  # Robinhood = $0
    slippage_pct: float = 0.001  # 10 bps default slippage

    def execute_trade(self, date: pd.Timestamp, symbol: str, side: Side,
                      quantity: float, price: float) -> Trade:
        """Execute a trade and update portfolio."""
        if quantity <= 0:
            raise ValueError(f"Quantity must be positive, got {quantity}")
        if price <= 0:
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
        if pos and pos.quantity != 0:
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
        total = self.total_value(prices)
        holdings = {}
        for sym, pos in self.positions.items():
            if pos.quantity != 0 and sym in prices:
                mv = pos.quantity * prices[sym]
                holdings[sym] = {
                    "quantity": pos.quantity,
                    "avg_cost": pos.avg_cost,
                    "market_value": mv,
                    "weight": mv / total if total > 0 else 0,
                    "unrealized_pnl": (prices[sym] - pos.avg_cost) * pos.quantity,
                }
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

    # Drop interior NaN to prevent silent metric corruption
    returns = returns.dropna()
    if len(returns) < 2:
        return {"error": "Insufficient data after removing NaN"}

    # Basic return stats
    total_return = (1 + returns).prod() - 1
    n_years = len(returns) / periods_per_year
    growth = 1 + total_return
    if growth > 0:
        cagr = growth ** (1 / max(n_years, 0.01)) - 1
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
    sharpe = excess.mean() / excess_std * sqrt_periods if excess_std > 0 else 0

    # Sortino ratio (downside deviation only)
    downside_diff = (returns - daily_rf).clip(upper=0)
    downside_dev = math.sqrt((downside_diff**2).mean()) * sqrt_periods
    sortino = (cagr - risk_free_rate) / downside_dev if downside_dev > 0 else 0

    # Drawdown analysis
    cum_returns = (1 + returns).cumprod()
    rolling_max = cum_returns.cummax()
    drawdowns = cum_returns / rolling_max - 1
    max_drawdown = drawdowns.min()
    max_dd_end = drawdowns.idxmin()

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
        "max_drawdown_date": str(max_dd_end),
        "win_rate": win_rate,
        "profit_factor": profit_factor,
        "num_trading_days": total_days,
        "skewness": skew,
        "kurtosis": kurt,
        "best_day": returns.max(),
        "worst_day": returns.min(),
        "avg_daily_return": returns.mean(),
    }

    # Benchmark comparison
    if benchmark_returns is not None and not benchmark_returns.empty:
        aligned = pd.DataFrame({"port": returns, "bench": benchmark_returns}).dropna()
        if len(aligned) > 10:
            aligned_n_years = len(aligned) / periods_per_year
            bench_total = (1 + aligned["bench"]).prod() - 1
            bench_growth = 1 + bench_total
            bench_cagr = bench_growth ** (1 / max(aligned_n_years, 0.01)) - 1 if bench_growth > 0 else -1.0
            port_aligned_total = (1 + aligned["port"]).prod() - 1
            port_growth = 1 + port_aligned_total
            port_aligned_cagr = port_growth ** (1 / max(aligned_n_years, 0.01)) - 1 if port_growth > 0 else -1.0
            metrics["benchmark_total_return"] = bench_total
            metrics["benchmark_cagr"] = bench_cagr
            metrics["alpha"] = port_aligned_cagr - bench_cagr

            # Beta
            cov = aligned[["port", "bench"]].cov()
            beta = cov.iloc[0, 1] / cov.iloc[1, 1] if cov.iloc[1, 1] > 0 else 0
            metrics["beta"] = beta

            # Information ratio
            tracking = aligned["port"] - aligned["bench"]
            tracking_error = tracking.std() * sqrt_periods
            info_ratio = (port_aligned_cagr - bench_cagr) / tracking_error if tracking_error > 0 else 0
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
        self.strategy = strategy
        self.symbols = symbols
        self.start = start
        self.end = end
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
        from agents_assemble.data.fetcher import fetch_ohlcv, fetch_multiple_ohlcv

        if self._external_data:
            all_data = self._external_data
        else:
            # Pre-load 1 year before start for indicator warmup
            from datetime import datetime, timedelta
            try:
                warmup_start = (datetime.strptime(self.start, "%Y-%m-%d") - timedelta(days=365)).strftime("%Y-%m-%d")
            except (ValueError, TypeError):
                warmup_start = self.start
            all_data = fetch_multiple_ohlcv(
                self.symbols, start=warmup_start, end=self.end
            )

        bench_data = None
        if self.benchmark:
            if self.benchmark in all_data:
                bench_data = all_data[self.benchmark]
            elif self.benchmark not in self.symbols:
                try:
                    bench_data = fetch_ohlcv(self.benchmark, start=self.start, end=self.end)
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

        # Normalize all indexes to tz-naive for consistent comparison
        for sym in list(all_data.keys()):
            if all_data[sym].index.tz is not None:
                all_data[sym].index = all_data[sym].index.tz_localize(None)
        if bench_data is not None and bench_data.index.tz is not None:
            bench_data.index = bench_data.index.tz_localize(None)

        portfolio = Portfolio(
            initial_cash=self.initial_cash,
            cash=self.initial_cash,
            commission_per_trade=self.commission,
            slippage_pct=self.slippage_pct,
        )

        # Build close prices matrix — union index with forward-fill for partial data
        close_prices = pd.DataFrame({sym: df["Close"] for sym, df in all_data.items()})
        close_prices = close_prices.sort_index().ffill()

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
            enriched["sma_20"] = close.rolling(20).mean()
            enriched["sma_50"] = close.rolling(50).mean()
            enriched["sma_200"] = close.rolling(200).mean()
            enriched["ema_12"] = close.ewm(span=12).mean()
            enriched["ema_26"] = close.ewm(span=26).mean()
            enriched["macd"] = enriched["ema_12"] - enriched["ema_26"]
            enriched["macd_signal"] = enriched["macd"].ewm(span=9).mean()
            enriched["rsi_14"] = _compute_rsi(close, 14)
            enriched["bb_upper"], enriched["bb_lower"] = _compute_bollinger(close, 20, 2)
            enriched["atr_14"] = _compute_atr(enriched, 14)
            enriched["daily_return"] = close.pct_change()
            enriched["vol_20"] = enriched["daily_return"].rolling(20).std()
            enriched["volume_sma_20"] = enriched["Volume"].rolling(20).mean()
            enriched_data[sym] = enriched

        # Pre-compute prices dict — avoids per-iteration pandas Series creation
        _raw_prices = close_prices.to_dict('index')
        prices_lookup = {
            dt: {sym: v for sym, v in row.items() if pd.notna(v)}
            for dt, row in _raw_prices.items()
        }

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

            # Call strategy
            try:
                target_weights = self.strategy(date, prices, portfolio, enriched_data)
            except Exception:
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
        daily_returns = equity_curve.pct_change().dropna()

        bench_returns = None
        if bench_data is not None and not bench_data.empty:
            bench_close = bench_data["Close"]
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
        total_value = portfolio.total_value(prices)

        # Phase 1: Collect and execute all sells (reductions, closes, short initiations)
        sells: list[tuple[str, int]] = []

        for sym, target_w in target_weights.items():
            if sym not in prices:
                continue
            price = prices[sym]
            if price <= 0:
                continue
            target_value = total_value * target_w
            current_pos = portfolio.get_position(sym)
            current_value = (current_pos.quantity * price) if current_pos else 0.0
            diff_value = target_value - current_value
            if diff_value < 0 and abs(diff_value) >= price * 0.5:
                qty = int(round(abs(diff_value) / price))
                if qty > 0:
                    sells.append((sym, qty))

        # Close long positions not in target weights
        for sym in list(portfolio.positions.keys()):
            if sym not in target_weights:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity > 0 and sym in prices and prices[sym] > 0:
                    sells.append((sym, int(round(pos.quantity))))

        for sym, qty in sells:
            portfolio.execute_trade(date, sym, Side.SELL, qty, prices[sym])

        # Phase 2: Recompute total value after sells, then collect buys
        total_value = portfolio.total_value(prices)
        buys: list[tuple[str, int, float]] = []

        for sym, target_w in target_weights.items():
            if sym not in prices:
                continue
            price = prices[sym]
            if price <= 0:
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
            if sym not in target_weights:
                pos = portfolio.get_position(sym)
                if pos and pos.quantity < 0 and sym in prices and prices[sym] > 0:
                    buys.append((sym, int(round(abs(pos.quantity))), float("inf")))

        # Execute buys with highest-weight positions first
        buys.sort(key=lambda x: x[2], reverse=True)
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
                       num_std: float = 2) -> tuple[pd.Series, pd.Series]:
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
# Report generation
# ---------------------------------------------------------------------------
def _fmt_ratio(value: float) -> str:
    """Format a ratio that may be infinite (calmar, profit_factor)."""
    if not math.isfinite(value):
        return "       N/A"
    return f"{value:>10.2f}"


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
        f"  Total Return:       {m.get('total_return', 0):>10.2%}",
        f"  CAGR:               {m.get('cagr', 0):>10.2%}",
        f"  Annual Volatility:  {m.get('annual_volatility', 0):>10.2%}",
        f"  Sharpe Ratio:       {m.get('sharpe_ratio', 0):>10.2f}",
        f"  Sortino Ratio:      {_fmt_ratio(m.get('sortino_ratio', 0))}",
        f"  Calmar Ratio:       {_fmt_ratio(m.get('calmar_ratio', 0))}",
        f"  Max Drawdown:       {m.get('max_drawdown', 0):>10.2%}",
        f"  Win Rate:           {m.get('win_rate', 0):>10.2%}",
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

    if "benchmark_total_return" in m:
        lines.extend([
            "",
            "--- vs Benchmark ---",
            f"  Benchmark Return:   {m.get('benchmark_total_return', 0):>10.2%}",
            f"  Alpha:              {m.get('alpha', 0):>10.2%}",
            f"  Beta:               {m.get('beta', 0):>10.2f}",
            f"  Info Ratio:         {m.get('information_ratio', 0):>10.2f}",
        ])

    lines.append(f"\n{'=' * 60}")
    return "\n".join(lines)


def _sanitize_for_json(obj):
    """Replace float inf/nan with None for JSON compliance."""
    if isinstance(obj, float) and (math.isinf(obj) or math.isnan(obj)):
        return None
    if isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_for_json(v) for v in obj]
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
            serializable[k] = json.loads(json.dumps(v, default=str))
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
    from agents_assemble.data.fetcher import fetch_ohlcv

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

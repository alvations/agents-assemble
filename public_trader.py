"""Public.com trading client for agents-assemble.

Uses the official public_api_sdk Python SDK to translate strategy signals
into actual trade orders on Public.com.

Requires: PUBLIC_API_SECRET env var (get from public.com/settings/security/api)
SDK: pip install public-api-sdk (or use local copy at ../publicdotcom-py)

Usage:
    from public_trader import PublicTrader

    trader = PublicTrader()  # Uses PUBLIC_API_SECRET env var
    trader.execute_strategy("momentum_crash_hedge", dry_run=True)

API Reference: https://public.com/api/docs
"""

from __future__ import annotations

import os
import sys
import uuid
from decimal import Decimal
from pathlib import Path
from typing import Any, Dict, List, Optional

# Add SDK to path if local copy exists
SDK_PATH = Path(__file__).parent.parent / "publicdotcom-py" / "src"
if SDK_PATH.exists():
    sys.path.insert(0, str(SDK_PATH))

try:
    from public_api_sdk import PublicApiClient, PublicApiClientConfiguration
    from public_api_sdk.auth_config import AuthConfig
    from public_api_sdk.models.order import (
        OrderRequest, OrderInstrument, OrderSide, OrderType,
        OrderExpirationRequest, TimeInForce,
    )
    from public_api_sdk.models.instrument_type import InstrumentType
    HAS_SDK = True
except ImportError:
    HAS_SDK = False


class PublicTrader:
    """Client for executing strategy trades on Public.com using official SDK.

    Workflow:
    1. Authenticate with secret key via SDK
    2. Get account info and current portfolio
    3. Run strategy to get target weights
    4. Calculate diff between current and target positions
    5. Place orders to rebalance (or log in dry_run mode)
    """

    def __init__(self, secret: Optional[str] = None, account_id: Optional[str] = None,
                 dry_run: bool = True):
        self.secret = secret or os.environ.get("PUBLIC_API_SECRET")
        self.dry_run = dry_run
        self._client = None
        self._account_id = account_id

        if not HAS_SDK:
            print("WARNING: public_api_sdk not found. Install: pip install public-api-sdk")
            print("Or ensure ../publicdotcom-py/src is accessible.")

        if not self.secret:
            print("WARNING: No PUBLIC_API_SECRET set. Set env var or pass secret=.")
            print("Get your key at: https://public.com/settings/security/api")

    def _get_client(self) -> "PublicApiClient":
        """Get or create authenticated API client."""
        if self._client is None:
            if not HAS_SDK:
                raise ImportError("public_api_sdk required. pip install public-api-sdk")
            if not self.secret:
                raise ValueError("No API secret. Set PUBLIC_API_SECRET env var.")

            auth_config = AuthConfig(api_key=self.secret)
            config = PublicApiClientConfiguration(
                default_account_number=self._account_id
            )
            self._client = PublicApiClient(auth_config=auth_config, config=config)

            # Auto-discover account ID if not set
            if not self._account_id:
                accounts = self._client.get_accounts()
                if accounts.accounts:
                    self._account_id = accounts.accounts[0].account_id
                    self._client.config.default_account_number = self._account_id
                    print(f"  Using account: {self._account_id}")

        return self._client

    def get_portfolio(self) -> Dict[str, Dict]:
        """Get current positions as {symbol: {quantity, value}}."""
        client = self._get_client()
        portfolio = client.get_portfolio()
        positions = {}
        for holding in portfolio.holdings or []:
            sym = holding.instrument.symbol if holding.instrument else ""
            if sym:
                positions[sym] = {
                    "quantity": float(holding.quantity or 0),
                    "value": float(holding.current_value or 0),
                }
        return positions

    def get_quotes(self, symbols: List[str]) -> Dict[str, float]:
        """Get current prices for symbols."""
        client = self._get_client()
        instruments = [
            OrderInstrument(symbol=sym, type=InstrumentType.EQUITY)
            for sym in symbols
        ]
        quotes = client.get_quotes(instruments)
        return {q.instrument.symbol: float(q.last or q.ask or 0) for q in quotes if q.instrument}

    def place_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str = "MARKET",
        limit_price: Optional[float] = None,
        stop_price: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Place a single equity order.

        Args:
            symbol: Ticker (e.g., "AAPL")
            side: "BUY" or "SELL"
            quantity: Number of shares
            order_type: "MARKET", "LIMIT", "STOP", or "STOP_LIMIT"
            limit_price: Price for LIMIT/STOP_LIMIT orders
            stop_price: Price for STOP/STOP_LIMIT orders
        """
        if self.dry_run:
            price_str = f" @ ${limit_price}" if limit_price else ""
            print(f"  [DRY RUN] {side} {quantity} {symbol} {order_type}{price_str}")
            return {"orderId": str(uuid.uuid4()), "status": "DRY_RUN"}

        client = self._get_client()
        order_req = OrderRequest(
            order_id=str(uuid.uuid4()),
            instrument=OrderInstrument(symbol=symbol, type=InstrumentType.EQUITY),
            order_side=OrderSide(side),
            order_type=OrderType(order_type),
            expiration=OrderExpirationRequest(time_in_force=TimeInForce.DAY),
            quantity=Decimal(str(quantity)),
            limit_price=Decimal(str(limit_price)) if limit_price else None,
            stop_price=Decimal(str(stop_price)) if stop_price else None,
        )
        new_order = client.place_order(order_req)
        return {"orderId": new_order.order_id}

    def execute_strategy(
        self,
        strategy_name: str,
        portfolio_value: Optional[float] = None,
        max_position_pct: float = 0.20,
    ) -> Dict[str, Any]:
        """Execute a strategy by rebalancing to target weights.

        Args:
            strategy_name: Any strategy key (e.g., "momentum_crash_hedge")
            portfolio_value: Total portfolio value (auto-detected if API connected)
            max_position_pct: Maximum per-position allocation
        """
        sys.path.insert(0, str(Path(__file__).parent))

        # Resolve strategy
        persona = self._resolve_strategy(strategy_name)
        print(f"\n{'='*60}")
        print(f"  Strategy: {persona.config.name}")
        print(f"  Dry run:  {self.dry_run}")
        print(f"{'='*60}")

        # Get current state
        if not self.dry_run and self.secret and HAS_SDK:
            current_positions = self.get_portfolio()
            total_value = portfolio_value or sum(p["value"] for p in current_positions.values())
        else:
            current_positions = {}
            total_value = portfolio_value or 100_000

        # Generate signals from latest market data
        from data_fetcher import fetch_multiple_ohlcv
        from backtester import _compute_rsi, _compute_bollinger, _compute_atr
        import pandas as pd
        import numpy as np

        symbols = persona.config.universe
        print(f"  Fetching data for {len(symbols)} symbols...")

        try:
            all_data = fetch_multiple_ohlcv(symbols, start="2024-01-01")
        except Exception as e:
            return {"error": f"Data fetch failed: {e}"}

        # Enrich with indicators
        enriched = {}
        prices_today = {}
        for sym, df in all_data.items():
            if df.empty:
                continue
            if df.index.tz is not None:
                df.index = df.index.tz_localize(None)
            close = df["Close"]
            df["sma_20"] = close.rolling(20).mean()
            df["sma_50"] = close.rolling(50).mean()
            df["sma_200"] = close.rolling(200).mean()
            df["ema_12"] = close.ewm(span=12).mean()
            df["ema_26"] = close.ewm(span=26).mean()
            df["macd"] = df["ema_12"] - df["ema_26"]
            df["macd_signal"] = df["macd"].ewm(span=9).mean()
            df["rsi_14"] = _compute_rsi(close, 14)
            df["bb_upper"], df["bb_lower"] = _compute_bollinger(close, 20, 2)
            df["atr_14"] = _compute_atr(df, 14)
            df["daily_return"] = close.pct_change()
            df["vol_20"] = df["daily_return"].rolling(20).std()
            df["volume_sma_20"] = df["Volume"].rolling(20).mean()
            enriched[sym] = df
            prices_today[sym] = float(close.iloc[-1])

        if not prices_today:
            return {"error": "No price data"}

        today = pd.Timestamp.now().normalize()

        # Generate target weights
        from backtester import Portfolio
        portfolio = Portfolio(initial_cash=total_value, cash=total_value)
        target_weights = persona.generate_signals(today, prices_today, portfolio, enriched)

        # Calculate and execute rebalance orders
        print(f"\n  Target allocation ({sum(1 for w in target_weights.values() if w > 0)} positions):")
        orders_placed = []
        orders_skipped = []

        for sym, weight in sorted(target_weights.items(), key=lambda x: -x[1]):
            if weight <= 0:
                continue
            price = prices_today.get(sym, 0)
            if price <= 0:
                continue

            target_value = total_value * min(weight, max_position_pct)
            target_qty = int(target_value / price)
            current_qty = int(current_positions.get(sym, {}).get("quantity", 0))
            diff = target_qty - current_qty

            if diff == 0:
                orders_skipped.append(sym)
                continue

            side = "BUY" if diff > 0 else "SELL"
            qty = abs(diff)

            print(f"    {sym:8s} | w={weight:.1%} | {side} {qty:4d} @ ~${price:.2f} = ${qty*price:,.0f}")

            try:
                result = self.place_order(sym, side, qty)
                orders_placed.append({"symbol": sym, "side": side, "quantity": qty,
                                       "price": price, "result": result})
            except Exception as e:
                print(f"    ERROR: {sym}: {e}")

        # Close positions not in target
        for sym, pos in current_positions.items():
            if sym not in target_weights or target_weights.get(sym, 0) == 0:
                qty = int(pos.get("quantity", 0))
                if qty > 0:
                    price = prices_today.get(sym, 0)
                    print(f"    {sym:8s} | CLOSE | SELL {qty:4d} @ ~${price:.2f}")
                    try:
                        result = self.place_order(sym, "SELL", qty)
                        orders_placed.append({"symbol": sym, "side": "SELL", "quantity": qty,
                                               "price": price, "result": result})
                    except Exception as e:
                        print(f"    ERROR closing {sym}: {e}")

        print(f"\n  Orders: {len(orders_placed)} placed, {len(orders_skipped)} unchanged")
        return {"placed": orders_placed, "skipped": orders_skipped}

    def _resolve_strategy(self, name: str):
        """Find strategy across all categories."""
        from personas import ALL_PERSONAS, get_persona
        from famous_investors import FAMOUS_INVESTORS, get_famous_investor
        from theme_strategies import THEME_STRATEGIES, get_theme_strategy
        from recession_strategies import RECESSION_STRATEGIES, get_recession_strategy
        from unconventional_strategies import UNCONVENTIONAL_STRATEGIES, get_unconventional_strategy
        from research_strategies import RESEARCH_STRATEGIES, get_research_strategy
        from math_strategies import MATH_STRATEGIES, get_math_strategy
        from hedge_fund_strategies import HEDGE_FUND_STRATEGIES, get_hedge_fund_strategy
        from news_event_strategies import NEWS_EVENT_STRATEGIES, get_news_event_strategy

        for registry, getter in [
            (ALL_PERSONAS, get_persona), (FAMOUS_INVESTORS, get_famous_investor),
            (THEME_STRATEGIES, get_theme_strategy), (RECESSION_STRATEGIES, get_recession_strategy),
            (UNCONVENTIONAL_STRATEGIES, get_unconventional_strategy),
            (RESEARCH_STRATEGIES, get_research_strategy), (MATH_STRATEGIES, get_math_strategy),
            (HEDGE_FUND_STRATEGIES, get_hedge_fund_strategy),
            (NEWS_EVENT_STRATEGIES, get_news_event_strategy),
        ]:
            if name in registry:
                return getter(name)
        raise ValueError(f"Strategy '{name}' not found")

    def generate_trade_plan(self, strategy_name: str, portfolio_value: float = 100_000) -> str:
        """Generate a human-readable trade plan without executing."""
        old = self.dry_run
        self.dry_run = True
        self.execute_strategy(strategy_name, portfolio_value=portfolio_value)
        self.dry_run = old
        return "Trade plan generated (see output above)"


if __name__ == "__main__":
    strategy = sys.argv[1] if len(sys.argv) > 1 else "momentum_crash_hedge"
    print(f"Trade plan for: {strategy} (dry run)\n")
    trader = PublicTrader(dry_run=True)
    trader.generate_trade_plan(strategy)

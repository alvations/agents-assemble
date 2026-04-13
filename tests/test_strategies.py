"""Tests for all strategy files.

Validates:
- Every strategy class can be instantiated
- generate_signals() returns a dict of {str: float}
- All tickers in universes are strings
- No while True loops in strategy source
- Total strategy count >= 224
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from backtester import Portfolio

# Import helpers from conftest via the tests package
_TESTS_DIR = Path(__file__).parent
sys.path.insert(0, str(_TESTS_DIR))
from conftest import ALL_STRATEGY_MODULES, _load_all_registries, make_mock_data


# ---------------------------------------------------------------------------
# Gather all registries once at module level for parametrization
# ---------------------------------------------------------------------------
_REGISTRIES = _load_all_registries()
_ALL_STRATEGY_KEYS = []
for cat, registry, getter in _REGISTRIES:
    for key in registry:
        _ALL_STRATEGY_KEYS.append((cat, key, getter))


# ---------------------------------------------------------------------------
# 1. Strategy count
# ---------------------------------------------------------------------------
def test_total_strategy_count():
    """There should be at least 224 strategies across all registries."""
    total = sum(len(reg) for _, reg, _ in _REGISTRIES)
    assert total >= 224, f"Expected >= 224 strategies, got {total}"


# ---------------------------------------------------------------------------
# 2. Instantiation
# ---------------------------------------------------------------------------
class TestInstantiation:
    @pytest.mark.parametrize("cat,key,getter", _ALL_STRATEGY_KEYS,
                             ids=[f"{c}/{k}" for c, k, _ in _ALL_STRATEGY_KEYS])
    def test_strategy_instantiates(self, cat, key, getter):
        persona = getter(key)
        assert hasattr(persona, "config"), f"{cat}/{key} has no config"
        assert persona.config.name, f"{cat}/{key} has empty name"
        assert persona.config.universe, f"{cat}/{key} has empty universe"
        assert persona.config.max_positions > 0
        assert 0 < persona.config.max_position_size <= 1

    @pytest.mark.parametrize("cat,key,getter", _ALL_STRATEGY_KEYS,
                             ids=[f"{c}/{k}" for c, k, _ in _ALL_STRATEGY_KEYS])
    def test_universe_contains_strings(self, cat, key, getter):
        persona = getter(key)
        for ticker in persona.config.universe:
            assert isinstance(ticker, str), (
                f"{cat}/{key} has non-string ticker: {ticker!r} ({type(ticker).__name__})"
            )
            assert len(ticker) > 0, f"{cat}/{key} has empty ticker string"


# ---------------------------------------------------------------------------
# 3. Signal generation (test a representative sample to avoid 10+ minutes)
# ---------------------------------------------------------------------------
_SAMPLE_KEYS = []
for cat, registry, getter in _REGISTRIES:
    keys = list(registry.keys())
    # Pick first and last from each category
    _SAMPLE_KEYS.append((cat, keys[0], getter))
    if len(keys) > 1:
        _SAMPLE_KEYS.append((cat, keys[-1], getter))


class TestSignalGeneration:
    @pytest.mark.parametrize("cat,key,getter", _SAMPLE_KEYS,
                             ids=[f"{c}/{k}" for c, k, _ in _SAMPLE_KEYS])
    def test_generate_signals_returns_dict(self, cat, key, getter):
        persona = getter(key)
        symbols = persona.config.universe[:10]
        data, prices, date = make_mock_data(symbols)
        portfolio = Portfolio(initial_cash=100_000, cash=100_000)
        weights = persona.generate_signals(date, prices, portfolio, data)
        assert isinstance(weights, dict), (
            f"{cat}/{key} returned {type(weights).__name__}, expected dict"
        )

    @pytest.mark.parametrize("cat,key,getter", _SAMPLE_KEYS,
                             ids=[f"{c}/{k}" for c, k, _ in _SAMPLE_KEYS])
    def test_signal_values_are_numeric(self, cat, key, getter):
        persona = getter(key)
        symbols = persona.config.universe[:10]
        data, prices, date = make_mock_data(symbols)
        portfolio = Portfolio(initial_cash=100_000, cash=100_000)
        weights = persona.generate_signals(date, prices, portfolio, data)
        for sym, w in weights.items():
            assert isinstance(sym, str), f"{cat}/{key}: key {sym!r} is not str"
            assert isinstance(w, (int, float)), (
                f"{cat}/{key}: weight for {sym} is {type(w).__name__}"
            )


# ---------------------------------------------------------------------------
# 4. No while True loops
# ---------------------------------------------------------------------------
_STRATEGY_FILES = [
    "personas.py", "famous_investors.py", "theme_strategies.py",
    "recession_strategies.py", "unconventional_strategies.py",
    "research_strategies.py", "math_strategies.py", "hedge_fund_strategies.py",
    "news_event_strategies.py", "political_strategies.py",
    "portfolio_strategies.py", "crisis_commodity_strategies.py",
    "williams_seasonal_strategies.py", "gap_strategies.py",
    "strategy_orchestrator.py",
]


@pytest.mark.parametrize("filename", _STRATEGY_FILES)
def test_no_while_true_loops(filename):
    """Strategy files must not contain unbounded while True loops."""
    filepath = Path(__file__).parent.parent / filename
    if not filepath.exists():
        pytest.skip(f"{filename} not found")
    content = filepath.read_text()
    assert "while True" not in content, (
        f"{filename} contains 'while True' -- use 'for _ in range(N)' instead"
    )


# ---------------------------------------------------------------------------
# 5. AST syntax validity
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("filename", _STRATEGY_FILES)
def test_ast_valid(filename):
    """Every strategy file must be valid Python (parseable by ast)."""
    import ast
    filepath = Path(__file__).parent.parent / filename
    if not filepath.exists():
        pytest.skip(f"{filename} not found")
    content = filepath.read_text()
    try:
        ast.parse(content, filename=filename)
    except SyntaxError as e:
        pytest.fail(f"{filename} has syntax error: {e}")

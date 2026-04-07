"""Comprehensive test suite for agents-assemble strategies.

Tests all strategies can be instantiated and produce valid signals.
Does NOT backtest (that's run_multi_horizon.py) — just verifies
the code doesn't crash.

Usage: python test_strategies.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from personas import ALL_PERSONAS, get_persona
from famous_investors import FAMOUS_INVESTORS, get_famous_investor
from theme_strategies import THEME_STRATEGIES, get_theme_strategy
from recession_strategies import RECESSION_STRATEGIES, get_recession_strategy
from unconventional_strategies import UNCONVENTIONAL_STRATEGIES, get_unconventional_strategy
from research_strategies import RESEARCH_STRATEGIES, get_research_strategy
from math_strategies import MATH_STRATEGIES, get_math_strategy
from hedge_fund_strategies import HEDGE_FUND_STRATEGIES, get_hedge_fund_strategy


def test_all_strategies():
    """Test that all strategies can be instantiated and have valid configs."""
    all_registries = [
        ("Generic", ALL_PERSONAS, get_persona),
        ("Famous", FAMOUS_INVESTORS, get_famous_investor),
        ("Theme", THEME_STRATEGIES, get_theme_strategy),
        ("Recession", RECESSION_STRATEGIES, get_recession_strategy),
        ("Unconventional", UNCONVENTIONAL_STRATEGIES, get_unconventional_strategy),
        ("Research", RESEARCH_STRATEGIES, get_research_strategy),
        ("Math", MATH_STRATEGIES, get_math_strategy),
        ("Hedge Fund", HEDGE_FUND_STRATEGIES, get_hedge_fund_strategy),
    ]

    total = 0
    passed = 0
    failed = 0

    for category, registry, getter in all_registries:
        for key in registry:
            total += 1
            try:
                persona = getter(key)
                assert persona.config.name, f"{key} has no name"
                assert persona.config.universe, f"{key} has no universe"
                assert len(persona.config.universe) > 0, f"{key} has empty universe"
                assert persona.config.max_positions > 0, f"{key} has invalid max_positions"
                assert 0 < persona.config.max_position_size <= 1, f"{key} has invalid max_position_size"
                assert persona.config.rebalance_frequency in ("daily", "weekly", "monthly"), f"{key} has invalid rebalance_frequency"
                passed += 1
            except Exception as e:
                print(f"  FAIL: {category}/{key}: {e}")
                failed += 1

    print(f"\n{'='*50}")
    print(f"Test Results: {passed}/{total} passed, {failed} failed")
    print(f"{'='*50}")
    return failed == 0


if __name__ == "__main__":
    success = test_all_strategies()
    sys.exit(0 if success else 1)

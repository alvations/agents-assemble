"""Sync flat source files to agents_assemble/ package.

After self-evolving the flat files (backtester.py, personas.py, etc.),
run this script to copy them into the package with corrected imports.

Usage: python sync_package.py
"""

from pathlib import Path

ROOT = Path(__file__).parent

# Map ALL flat files to package locations (single source of truth)
FILE_MAP = {
    "data_fetcher.py": "agents_assemble/data/fetcher.py",
    "backtester.py": "agents_assemble/engine/backtester.py",
    "judge.py": "agents_assemble/engine/judge.py",
    "trade_recommender.py": "agents_assemble/engine/recommender.py",
    "personas.py": "agents_assemble/strategies/generic.py",
    "famous_investors.py": "agents_assemble/strategies/famous.py",
    "theme_strategies.py": "agents_assemble/strategies/themes.py",
    "recession_strategies.py": "agents_assemble/strategies/recession.py",
    "unconventional_strategies.py": "agents_assemble/strategies/unconventional.py",
    "research_strategies.py": "agents_assemble/strategies/research.py",
    "math_strategies.py": "agents_assemble/strategies/math.py",
    "hedge_fund_strategies.py": "agents_assemble/strategies/hedge_fund.py",
    "news_event_strategies.py": "agents_assemble/strategies/news_event.py",
    "political_strategies.py": "agents_assemble/strategies/political.py",
    "portfolio_strategies.py": "agents_assemble/strategies/portfolio.py",
    "crisis_commodity_strategies.py": "agents_assemble/strategies/crisis_commodity.py",
    "williams_seasonal_strategies.py": "agents_assemble/strategies/williams_seasonal.py",
}

# Import rewrites: flat import -> package import
IMPORT_REWRITES = {
    "from personas import": "from agents_assemble.strategies.generic import",
    "from data_fetcher import": "from agents_assemble.data.fetcher import",
    "from backtester import": "from agents_assemble.engine.backtester import",
    "from judge import": "from agents_assemble.engine.judge import",
    "from trade_recommender import": "from agents_assemble.engine.recommender import",
    "from famous_investors import": "from agents_assemble.strategies.famous import",
    "from theme_strategies import": "from agents_assemble.strategies.themes import",
    "from recession_strategies import": "from agents_assemble.strategies.recession import",
    "from unconventional_strategies import": "from agents_assemble.strategies.unconventional import",
    "from research_strategies import": "from agents_assemble.strategies.research import",
    "from math_strategies import": "from agents_assemble.strategies.math import",
    "from hedge_fund_strategies import": "from agents_assemble.strategies.hedge_fund import",
}

# Path rewrites: fix STRATEGY_DIR to point to root strategy/ not package-relative
PATH_REWRITES = {
    'Path(__file__).parent / "strategy"': 'Path(__file__).resolve().parent.parent.parent / "strategy"',
}


def sync():
    synced = 0
    for flat, pkg in FILE_MAP.items():
        src = ROOT / flat
        dst = ROOT / pkg
        if not src.exists():
            print(f"  SKIP: {flat} (not found)")
            continue

        content = src.read_text()

        # Rewrite imports for package context
        for old, new in IMPORT_REWRITES.items():
            content = content.replace(old, new)

        # Rewrite paths for package context
        for old, new in PATH_REWRITES.items():
            content = content.replace(old, new)

        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(content)
        synced += 1
        print(f"  SYNC: {flat} -> {pkg}")

    print(f"\nSynced {synced}/{len(FILE_MAP)} files")


if __name__ == "__main__":
    sync()

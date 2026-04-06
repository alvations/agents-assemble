"""Sync flat source files to agents_assemble/ package.

After self-evolving the flat files (backtester.py, personas.py, etc.),
run this script to copy them into the package with corrected imports.

Usage: python sync_package.py
"""

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent

# Map flat files to package locations
FILE_MAP = {
    "data_fetcher.py": "agents_assemble/data/fetcher.py",
    "backtester.py": "agents_assemble/engine/backtester.py",
    "judge.py": "agents_assemble/engine/judge.py",
    "trade_recommender.py": "agents_assemble/engine/recommender.py",
    "personas.py": "agents_assemble/strategies/generic.py",
    "famous_investors.py": "agents_assemble/strategies/famous.py",
    "theme_strategies.py": "agents_assemble/strategies/themes.py",
    "recession_strategies.py": "agents_assemble/strategies/recession.py",
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
    "import personas": "import agents_assemble.strategies.generic as personas",
    "import data_fetcher": "import agents_assemble.data.fetcher as data_fetcher",
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

        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(content)
        synced += 1
        print(f"  SYNC: {flat} -> {pkg}")

    print(f"\nSynced {synced}/{len(FILE_MAP)} files")


if __name__ == "__main__":
    sync()

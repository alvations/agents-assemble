#!/usr/bin/env python3
"""Refresh HODL Composite numbers in every strategy .md file.

Reads the latest multi-window JSON, computes horizon-weighted HODL composite
per strategy (matches the formula in rebuild_leaderboards._horizon_weighted),
then patches the ``| **HODL Composite** | X.XX |`` line in every strategy
``.md`` file under:

  - agents-assemble/strategy/winning/
  - agents-assemble/strategy/losing/
  - bespoke/data/strategy/winning/  (kept in sync as a data mirror)
  - bespoke/data/strategy/losing/

Bespoke is not modified as code — only the data mirror is refreshed, and the
refresh is driven entirely from agents-assemble. Bespoke itself has no
awareness of this sync.

Strategy name parsed from filename: ``<name>_YYYYMMDD_HHMMSS.md``.
"""
from __future__ import annotations

import glob
import json
import os
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_WIN = REPO_ROOT / "strategy" / "winning"
AGENTS_LOS = REPO_ROOT / "strategy" / "losing"
BESPOKE_DATA_WIN = REPO_ROOT.parent / "bespoke" / "data" / "strategy" / "winning"
BESPOKE_DATA_LOS = REPO_ROOT.parent / "bespoke" / "data" / "strategy" / "losing"

FILENAME_RE = re.compile(r"^(?P<name>.+?)_\d{8}_\d{6}\.md$")
HODL_LINE_RE = re.compile(r"^\|\s*\*\*HODL Composite\*\*\s*\|\s*(-?\d+\.\d+)\s*\|\s*$", re.MULTILINE)


def horizon_weighted_hodl(w: Dict[str, Dict[str, float]]) -> float:
    if not w:
        return 0.0
    by_h = defaultdict(list)
    for k, v in w.items():
        by_h[k.split("_")[0]].append(v)

    horizon_rets, horizon_dds = [], []
    for lst in by_h.values():
        horizon_rets.append(statistics.mean(x.get("ret", 0) for x in lst))
        horizon_dds.append(statistics.mean(abs(x.get("dd", 0)) for x in lst))

    sharpes = [v.get("sh", 0) for v in w.values()]
    consistency = sum(1 for s in sharpes if s > 0) / len(sharpes)
    avg_ret = statistics.mean(horizon_rets)
    avg_dd = statistics.mean(horizon_dds)
    return avg_ret * consistency * (1 - avg_dd)


def strategy_name_from(path: Path) -> str | None:
    m = FILENAME_RE.match(path.name)
    return m.group("name") if m else None


def load_mw_composites() -> Dict[str, float]:
    candidates = sorted((REPO_ROOT / "results").glob("_multi_window_full_*.json"))
    if not candidates:
        raise FileNotFoundError("No _multi_window_full_*.json under results/")
    mw = json.loads(candidates[-1].read_text())
    print(f"Source: {candidates[-1].name} ({len(mw)} strategies)")
    return {name: horizon_weighted_hodl(entry.get("w", {})) for name, entry in mw.items()}


def update_file(path: Path, new_value: float) -> Tuple[str, float | None]:
    """Returns (status, old_value_if_changed)."""
    text = path.read_text()
    m = HODL_LINE_RE.search(text)
    if not m:
        return "no-hodl-line", None
    old_value = float(m.group(1))
    new_str = f"{new_value:.2f}"
    if f"{old_value:.2f}" == new_str:
        return "unchanged", None
    replacement = f"| **HODL Composite** | {new_str} |"
    new_text = HODL_LINE_RE.sub(replacement, text, count=1)
    path.write_text(new_text)
    return "updated", old_value


def process_dir(label: str, directory: Path, composites: Dict[str, float]):
    if not directory.exists():
        print(f"  [skip] {label}: {directory} does not exist")
        return 0, 0, 0, 0
    updated = unchanged = missing_strategy = no_hodl = 0
    largest_moves: List[Tuple[str, float, float]] = []
    for path in sorted(directory.glob("*.md")):
        name = strategy_name_from(path)
        if not name:
            continue
        if name not in composites:
            missing_strategy += 1
            continue
        status, old_val = update_file(path, composites[name])
        if status == "updated":
            updated += 1
            largest_moves.append((name, old_val, composites[name]))
        elif status == "unchanged":
            unchanged += 1
        elif status == "no-hodl-line":
            no_hodl += 1

    print(f"\n{label}  ({directory.relative_to(REPO_ROOT.parent)})")
    print(f"  updated:           {updated}")
    print(f"  unchanged:         {unchanged}")
    print(f"  no HODL line:      {no_hodl}")
    print(f"  strategy not in MW:{missing_strategy}")

    if largest_moves:
        largest_moves.sort(key=lambda t: abs(t[2] - t[1]), reverse=True)
        print("  biggest moves (old -> new):")
        for n, o, x in largest_moves[:5]:
            print(f"    {n:40s} {o:+.2f} -> {x:+.2f}  (Δ{x-o:+.2f})")
    return updated, unchanged, no_hodl, missing_strategy


def main():
    composites = load_mw_composites()

    totals = [0, 0, 0, 0]
    for label, directory in [
        ("agents-assemble winning", AGENTS_WIN),
        ("agents-assemble losing",  AGENTS_LOS),
        ("bespoke data winning",    BESPOKE_DATA_WIN),
        ("bespoke data losing",     BESPOKE_DATA_LOS),
    ]:
        res = process_dir(label, directory, composites)
        for i, v in enumerate(res):
            totals[i] += v

    print("\n" + "=" * 60)
    print("TOTAL:")
    print(f"  updated:             {totals[0]}")
    print(f"  unchanged:           {totals[1]}")
    print(f"  no HODL line:        {totals[2]}")
    print(f"  strategy not in MW:  {totals[3]}")


if __name__ == "__main__":
    main()

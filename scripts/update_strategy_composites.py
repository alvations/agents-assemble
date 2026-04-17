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


def horizon_stats(w: Dict[str, Dict[str, float]]) -> Dict[str, float]:
    """Compute everything the passive-investor block needs from window data."""
    if not w:
        return {}
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
    composite = avg_ret * consistency * (1 - avg_dd)

    def horizon_mean(key, field):
        lst = by_h.get(key, [])
        return statistics.mean(x.get(field, 0) for x in lst) if lst else None

    ten_y = by_h.get("10Y", [{}])[0] if by_h.get("10Y") else {}

    return {
        "avg_5Y_ret": horizon_mean("5Y", "ret"),
        "avg_5Y_sh":  horizon_mean("5Y", "sh"),
        "avg_5Y_dd":  statistics.mean(abs(x.get("dd", 0)) for x in by_h.get("5Y", [])) if by_h.get("5Y") else None,
        "ten_y_ret":  ten_y.get("ret") if ten_y else None,
        "ten_y_sh":   ten_y.get("sh") if ten_y else None,
        "ten_y_dd":   abs(ten_y.get("dd", 0)) if ten_y else None,
        "hodl":       composite,
        "windows":    len(w),
        "consistency": consistency,
    }


def horizon_weighted_hodl(w: Dict[str, Dict[str, float]]) -> float:
    return horizon_stats(w).get("hodl", 0.0) if w else 0.0


def _fmt_pct(v, decimals=1):
    if v is None: return "n/a"
    return f"{v*100:.{decimals}f}%"


def _usage_note(composite: float) -> str:
    if composite >= 1.5:
        return ("**Strong long-horizon compounder.** Suitable as a core or satellite holding (5-15% of portfolio). "
                "Rebalance quarterly or annually.")
    if composite >= 0.5:
        return ("**Moderate long-term performer.** Consider as a diversifier (2-5% of portfolio). "
                "Rebalance quarterly; trim if concentration exceeds target.")
    if composite >= 0.1:
        return ("**Marginal long-term returns.** Treat as tactical, not core. Small allocation (<2%) if any.")
    return ("**Weak long-term profile.** Not recommended for passive buy-and-hold. "
            "May still work as a tactical or hedged position — see main body.")


def build_passive_section(stats: Dict[str, float]) -> str:
    lines = [
        "",
        "<details>",
        "<summary>For passive investors (buy and hold)</summary>",
        "",
        "### Long-Horizon Performance",
        "",
        "| Metric | Value |",
        "|--------|-------|",
        f"| **Avg 5Y Return** | {_fmt_pct(stats['avg_5Y_ret'])} |",
        f"| **Avg 5Y Sharpe** | {stats['avg_5Y_sh']:.2f} |" if stats['avg_5Y_sh'] is not None else "| **Avg 5Y Sharpe** | n/a |",
        f"| **Avg 5Y Max DD** | -{_fmt_pct(stats['avg_5Y_dd'])} |" if stats['avg_5Y_dd'] is not None else "| **Avg 5Y Max DD** | n/a |",
        f"| **10Y Return (2015-2024)** | {_fmt_pct(stats['ten_y_ret'])} |",
        f"| **10Y Sharpe** | {stats['ten_y_sh']:.2f} |" if stats['ten_y_sh'] is not None else "| **10Y Sharpe** | n/a |",
        f"| **10Y Max DD** | -{_fmt_pct(stats['ten_y_dd'])} |" if stats['ten_y_dd'] is not None else "| **10Y Max DD** | n/a |",
        f"| **HODL Composite** | {stats['hodl']:.2f} |",
        f"| **Windows Tested** | {stats['windows']} |",
        f"| **Consistency** | {stats['consistency']*100:.0f}% |",
        "",
        "### How to Use This Strategy Passively",
        "",
        _usage_note(stats['hodl']),
        "",
        "</details>",
        "",
    ]
    return "\n".join(lines)


def strategy_name_from(path: Path) -> str | None:
    m = FILENAME_RE.match(path.name)
    return m.group("name") if m else None


def load_mw_stats() -> Dict[str, Dict[str, float]]:
    candidates = sorted((REPO_ROOT / "results").glob("_multi_window_full_*.json"))
    if not candidates:
        raise FileNotFoundError("No _multi_window_full_*.json under results/")
    mw = json.loads(candidates[-1].read_text())
    print(f"Source: {candidates[-1].name} ({len(mw)} strategies)")
    return {name: horizon_stats(entry.get("w", {})) for name, entry in mw.items()}


def update_file(path: Path, stats: Dict[str, float]) -> Tuple[str, float | None]:
    """Returns (status, old_value_if_changed). Appends passive section if missing."""
    text = path.read_text()
    new_value = stats["hodl"]
    m = HODL_LINE_RE.search(text)
    if m:
        old_value = float(m.group(1))
        new_str = f"{new_value:.2f}"
        if f"{old_value:.2f}" == new_str:
            return "unchanged", None
        replacement = f"| **HODL Composite** | {new_str} |"
        path.write_text(HODL_LINE_RE.sub(replacement, text, count=1))
        return "updated", old_value
    # No HODL line — append a full passive-investor section
    passive_block = build_passive_section(stats)
    new_text = text.rstrip() + "\n" + passive_block
    path.write_text(new_text)
    return "appended", None


def process_dir(label: str, directory: Path, stats_by_name: Dict[str, Dict[str, float]]):
    if not directory.exists():
        print(f"  [skip] {label}: {directory} does not exist")
        return 0, 0, 0, 0
    updated = unchanged = appended = missing_strategy = 0
    largest_moves: List[Tuple[str, float, float]] = []
    missing_names: List[str] = []
    for path in sorted(directory.glob("*.md")):
        name = strategy_name_from(path)
        if not name:
            continue
        if name not in stats_by_name:
            missing_strategy += 1
            missing_names.append(path.name)
            continue
        status, old_val = update_file(path, stats_by_name[name])
        if status == "updated":
            updated += 1
            largest_moves.append((name, old_val, stats_by_name[name]["hodl"]))
        elif status == "unchanged":
            unchanged += 1
        elif status == "appended":
            appended += 1

    print(f"\n{label}  ({directory.relative_to(REPO_ROOT.parent)})")
    print(f"  updated (HODL line): {updated}")
    print(f"  appended section:    {appended}")
    print(f"  unchanged:           {unchanged}")
    print(f"  strategy not in MW:  {missing_strategy}")
    if missing_names:
        print(f"    files: {missing_names}")

    if largest_moves:
        largest_moves.sort(key=lambda t: abs(t[2] - t[1]), reverse=True)
        print("  biggest HODL moves (old -> new):")
        for n, o, x in largest_moves[:5]:
            print(f"    {n:40s} {o:+.2f} -> {x:+.2f}  (Δ{x-o:+.2f})")
    return updated, appended, unchanged, missing_strategy


def main():
    stats_by_name = load_mw_stats()

    totals = [0, 0, 0, 0]
    for label, directory in [
        ("agents-assemble winning", AGENTS_WIN),
        ("agents-assemble losing",  AGENTS_LOS),
        ("bespoke data winning",    BESPOKE_DATA_WIN),
        ("bespoke data losing",     BESPOKE_DATA_LOS),
    ]:
        res = process_dir(label, directory, stats_by_name)
        for i, v in enumerate(res):
            totals[i] += v

    print("\n" + "=" * 60)
    print("TOTAL:")
    print(f"  updated (HODL line): {totals[0]}")
    print(f"  appended section:    {totals[1]}")
    print(f"  unchanged:           {totals[2]}")
    print(f"  strategy not in MW:  {totals[3]}")


if __name__ == "__main__":
    main()

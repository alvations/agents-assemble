#!/usr/bin/env python3
"""Rebuild LEADERBOARD.md and HODL_LEADERBOARD.md from multi-window JSON."""

import json
import glob
import os
import re
import statistics
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root (parent of scripts/)
_mw_candidates = sorted(glob.glob(os.path.join(BASE, "results/_multi_window_full_*.json")))
MW_PATH = _mw_candidates[-1] if _mw_candidates else os.path.join(BASE, "results/_multi_window_full_20260413_183206.json")
LEADERBOARD_PATH = os.path.join(BASE, "LEADERBOARD.md")
HODL_PATH = os.path.join(BASE, "HODL_LEADERBOARD.md")
GITHUB_BASE = "https://github.com/alvations/agents-assemble/blob/main/strategy"

# 6 windows for LEADERBOARD
SIX_WINDOWS = ["1Y_2022", "1Y_2023", "1Y_2024", "1Y_2025", "3Y_2022_2024", "3Y_2023_2025"]

# All 28 windows for HODL
ALL_28_WINDOWS = [
    "1Y_2015", "1Y_2016", "1Y_2017", "1Y_2018", "1Y_2019",
    "1Y_2020", "1Y_2021", "1Y_2022", "1Y_2023", "1Y_2024", "1Y_2025",
    "3Y_2015_2017", "3Y_2016_2018", "3Y_2017_2019", "3Y_2018_2020",
    "3Y_2019_2021", "3Y_2020_2022", "3Y_2021_2023", "3Y_2022_2024", "3Y_2023_2025",
    "5Y_2015_2019", "5Y_2016_2020", "5Y_2017_2021", "5Y_2018_2022",
    "5Y_2019_2023", "5Y_2020_2024", "5Y_2021_2025",
    "10Y_2015_2024",
]


def load_mw():
    with open(MW_PATH) as f:
        return json.load(f)


def find_strategy_files():
    """Map strategy name -> (folder, filename) for latest .md file."""
    strat_files = {}
    for folder in ["winning", "losing"]:
        pattern = os.path.join(BASE, f"strategy/{folder}/*.md")
        for f in glob.glob(pattern):
            base = os.path.basename(f)
            m = re.match(r"^(.+?)_(\d{8}_\d{6})\.md$", base)
            if m:
                name, ts = m.group(1), m.group(2)
                if name not in strat_files or ts > strat_files[name][1]:
                    strat_files[name] = (folder, ts, base)
    return strat_files


def find_result_jsons():
    """Map strategy name -> latest result JSON path."""
    result_files = {}
    for f in glob.glob(os.path.join(BASE, "results/*.json")):
        base = os.path.basename(f)
        if base.startswith("_"):
            continue
        m = re.match(r"^(.+?)_(\d{8}_\d{6})\.json$", base)
        if m:
            name, ts = m.group(1), m.group(2)
            if name not in result_files or ts > result_files[name][1]:
                result_files[name] = (f, ts)
    return result_files


def find_strategy_jsons():
    """Map strategy name -> latest strategy JSON from strategy/winning or strategy/losing."""
    strat_jsons = {}
    for folder in ["winning", "losing"]:
        for f in glob.glob(os.path.join(BASE, f"strategy/{folder}/*.json")):
            base = os.path.basename(f)
            m = re.match(r"^(.+?)_(\d{8}_\d{6})\.json$", base)
            if m:
                name, ts = m.group(1), m.group(2)
                if name not in strat_jsons or ts > strat_jsons[name][1]:
                    strat_jsons[name] = (f, ts)
    return strat_jsons


def get_positions_count(name, result_jsons):
    """Get positions count from latest result JSON."""
    if name in result_jsons:
        try:
            with open(result_jsons[name][0]) as f:
                d = json.load(f)
            if "final_positions" in d:
                return len(d["final_positions"])
        except Exception:
            pass
    return None


def get_risk_and_assessment(name, strat_jsons):
    """Get risk parameters, assessment, and timing from strategy JSON."""
    if name in strat_jsons:
        try:
            with open(strat_jsons[name][0]) as f:
                d = json.load(f)
            risk = d.get("risk_parameters", {})
            assessment = d.get("overall_assessment", "")
            timing = ""
            eg = d.get("execution_guidance", {})
            if isinstance(eg, dict):
                timing = eg.get("timing", "")
            return risk, assessment, timing
        except Exception:
            pass
    return {}, "", ""


def strategy_link(name, strat_files):
    """Build GitHub link for strategy."""
    if name in strat_files:
        folder, ts, filename = strat_files[name]
        return f"{GITHUB_BASE}/{folder}/{filename}"
    return f"{GITHUB_BASE}/winning/{name}.md"


def compute_6win_data(entry):
    """Compute 6-window composite, consistency, avg_ret for LEADERBOARD."""
    w = entry["w"]
    available = [win for win in SIX_WINDOWS if win in w]
    if not available:
        return {"avg_ret": 0, "consistency": 0, "composite": 0, "avg_dd": 0}

    rets = [w[win]["ret"] for win in available]
    sharpes = [w[win]["sh"] for win in available]
    dds = [abs(w[win]["dd"]) for win in available]

    avg_ret = statistics.mean(rets)
    consistency = sum(1 for s in sharpes if s > 0) / len(sharpes)
    avg_dd = statistics.mean(dds)
    composite = avg_ret * consistency * (1 - avg_dd)

    return {
        "avg_ret": avg_ret,
        "consistency": consistency,
        "avg_dd": avg_dd,
        "composite": composite,
    }


def fmt_pct(val, mult=100):
    """Format a float as percentage string."""
    return f"{val * mult:.1f}%"


def fmt_composite(val):
    """Format composite score matching existing leaderboard style.

    Examples: 1.4, 1.25, 0.79, 0.22, 0.0, -0.0, -0.01, -0.04
    """
    rounded = round(val, 2)
    if rounded == 0:
        if val < -0.0001:
            return "-0.0"
        return "0.0"
    # Round to 2 decimal places, strip unnecessary trailing zeros
    s = f"{rounded:.2f}"
    # Strip trailing zeros: 1.40 -> 1.4, but keep at least one decimal: 1.00 -> 1.0
    if "." in s:
        s = s.rstrip("0")
        if s.endswith("."):
            s += "0"
    return s


def assessment_text(assessment):
    """Generate assessment quote line."""
    if not assessment:
        return ""
    return f"> {assessment}"


def risk_text(risk):
    """Generate risk line."""
    sl = risk.get("stop_loss", "N/A")
    tp = risk.get("take_profit_target", "N/A")
    ma = risk.get("max_portfolio_allocation", "N/A")
    return f"Risk: Stop loss {sl} | Take profit {tp} | Max allocation {ma}"


def build_leaderboard(mw, strat_files, result_jsons, strat_jsons):
    """Build LEADERBOARD.md content."""
    # Compute 6-window data for all strategies
    all_strategies = []
    component_map = {}  # parent -> [components sorted by composite]
    for name, entry in mw.items():
        data = compute_6win_data(entry)
        w = entry["w"]
        ret_3y = w.get("3Y_2023_2025", {}).get("ret", 0)
        sh_3y = w.get("3Y_2023_2025", {}).get("sh", 0)
        dd_3y = w.get("3Y_2023_2025", {}).get("dd", 0)
        positions = get_positions_count(name, result_jsons)
        stype = entry.get("type", "standalone")
        s = {
            "name": name,
            "entry": entry,
            "composite": data["composite"],
            "avg_ret": data["avg_ret"],
            "consistency": data["consistency"],
            "avg_dd": data["avg_dd"],
            "ret_3y": ret_3y,
            "sh_3y": sh_3y,
            "dd_3y": dd_3y,
            "positions": positions,
            "type": stype,
        }
        all_strategies.append(s)
        if stype == "component":
            parent = entry.get("parent", "")
            component_map.setdefault(parent, []).append(s)

    # Sort components by composite descending (highest first)
    for parent, comps in component_map.items():
        comps.sort(key=lambda x: x["composite"], reverse=True)

    # Ranked strategies = standalone + combined (skip components)
    strategies = [s for s in all_strategies if s["type"] != "component"]
    strategies.sort(key=lambda x: x["composite"], reverse=True)

    n_ranked = len(strategies)
    n_components = sum(len(v) for v in component_map.values())
    n_total = len(all_strategies)

    lines = []
    lines.append("# LEADERBOARD")
    lines.append("")
    lines.append(f"**{n_total} strategies** ({n_ranked} ranked + {n_components} components collapsed under combined strategies).")
    lines.append("")
    lines.append("## Ranking Formula")
    lines.append("")
    lines.append("```")
    lines.append("Composite = Avg Return x Consistency x (1 - Avg |Max Drawdown|)")
    lines.append("```")
    lines.append("")
    lines.append("**Windows:** 1Y (2022-2025) + 3Y (2022-2024, 2023-2025) = 6")
    lines.append("")
    lines.append("## How to Read This")
    lines.append("")
    lines.append("| Metric | What It Means | Good | Bad |")
    lines.append("|--------|--------------|------|-----|")
    lines.append('| **Return** | Total cumulative return | >50% | <0% |')
    lines.append('| **Sharpe** | Risk-adjusted return | >1.0 | <0 |')
    lines.append('| **Max DD** | Worst peak-to-trough drop | >-15% | <-30% |')
    lines.append('| **Composite** | Return x consistency x safety | >0.3 | <0 |')
    lines.append('| **Consistency** | % of 6 windows with positive Sharpe | 100% | <50% |')
    lines.append("")
    lines.append("---")
    lines.append("")

    # Top 10 detailed cards
    lines.append("## Top 10 Strategies")
    lines.append("")

    for i, s in enumerate(strategies[:10]):
        name = s["name"]
        link = strategy_link(name, strat_files)
        risk, assessment, timing = get_risk_and_assessment(name, strat_jsons)
        pos = s["positions"] if s["positions"] is not None else "?"
        cons_pct = f"{s['consistency'] * 100:.0f}%"
        avg_ret_pct = f"{s['avg_ret'] * 100:.1f}%"
        comp_str = f"{s['composite']:.2f}"

        lines.append(f"### #{i+1} [{name}]({link})")
        lines.append("")
        lines.append("| 3Y Return | 3Y Sharpe | 3Y Max DD | Positions | Consistency | Avg Return | Composite |")
        lines.append("|-----------|-----------|-----------|-----------|------------|------------|-----------|")
        lines.append(
            f"| **{s['ret_3y']*100:.1f}%** | **{s['sh_3y']:.2f}** | "
            f"{s['dd_3y']*100:.1f}% | {pos} | {cons_pct} | {avg_ret_pct} | **{comp_str}** |"
        )
        lines.append("")

        if assessment:
            lines.append(f"> {assessment}")
            lines.append("")

        if risk:
            lines.append(risk_text(risk))
            lines.append("")

        if timing:
            lines.append(f"Timing: {timing}")
            lines.append("")

        # Rolling window breakdown
        lines.append("<details>")
        lines.append("<summary>Rolling window breakdown</summary>")
        lines.append("")
        lines.append("| Window | Return | Sharpe | Max DD |")
        lines.append("|--------|--------|--------|--------|")
        w = s["entry"]["w"]
        for win in SIX_WINDOWS:
            if win in w:
                lines.append(
                    f"| {win} | {w[win]['ret']*100:.1f}% | {w[win]['sh']:.2f} | {w[win]['dd']*100:.1f}% |"
                )
        lines.append("</details>")
        lines.append("")

    lines.append("---")
    lines.append("")

    # Full rankings table
    lines.append(f"## Full Rankings ({n_ranked} Ranked + {n_components} Components)")
    lines.append("")
    lines.append("| # | Strategy | 3Y Ret | 3Y Sharpe | 3Y DD | Pos | Consistency | Avg Ret | Composite |")
    lines.append("|---|----------|--------|-----------|-------|-----|------------|---------|-----------|")

    for i, s in enumerate(strategies):
        name = s["name"]
        link = strategy_link(name, strat_files)
        pos = s["positions"] if s["positions"] is not None else "?"
        cons_pct = f"{s['consistency'] * 100:.0f}%"
        avg_ret_pct = f"{s['avg_ret'] * 100:.1f}%"
        raw_comp = fmt_composite(s["composite"])
        # Bold composite for top 10
        comp_str = f"**{raw_comp}**" if i < 10 else raw_comp
        combined_tag = " **[combined]**" if s["type"] == "combined" else ""

        lines.append(
            f"| {i+1} | [**{name}**]({link}){combined_tag} | "
            f"{s['ret_3y']*100:.1f}% | {s['sh_3y']:.2f} | {s['dd_3y']*100:.1f}% | "
            f"{pos} | {cons_pct} | {avg_ret_pct} | {comp_str} |"
        )

        # Show components nested under combined strategies
        if s["type"] == "combined" and name in component_map:
            parent_composite = s["composite"]
            for cs in component_map[name]:
                clink = strategy_link(cs["name"], strat_files)
                cpos = cs["positions"] if cs["positions"] is not None else "?"
                ccons = f"{cs['consistency'] * 100:.0f}%"
                cavg = f"{cs['avg_ret'] * 100:.1f}%"
                raw_ccomp = fmt_composite(cs["composite"])
                # Bold if component beats parent
                ccomp = f"**{raw_ccomp}**" if cs["composite"] > parent_composite else raw_ccomp
                lines.append(
                    f"| ↳ | [{cs['name']}]({clink}) | "
                    f"{cs['ret_3y']*100:.1f}% | {cs['sh_3y']:.2f} | {cs['dd_3y']*100:.1f}% | "
                    f"{cpos} | {ccons} | {cavg} | {ccomp} |"
                )

    lines.append("")
    lines.append(f"*Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Disclaimer")
    lines.append("")
    lines.append("This content is for **educational and research purposes only**. It is **not financial advice**.")
    lines.append("")
    lines.append("- Past performance does not guarantee future results.")
    lines.append("- Backtests use historical data and may not reflect real-world conditions (liquidity, slippage, market impact).")
    lines.append("- All strategies tested with simulated capital. No real money was used or is at risk.")
    lines.append("- Consult a qualified financial advisor before making investment decisions.")
    lines.append("- The authors and contributors accept no responsibility for financial losses from using this information.")
    lines.append("- Securities mentioned are not buy/sell recommendations. Do your own due diligence.")
    lines.append("- Trading involves substantial risk of loss. Only invest what you can afford to lose.")
    lines.append("")
    lines.append("By using this information, you acknowledge that you understand and accept these risks.")

    return "\n".join(lines) + "\n"


def compute_hodl_data(entry):
    """Compute HODL composite from all 28 windows."""
    w = entry["w"]
    available = [win for win in ALL_28_WINDOWS if win in w]
    if not available:
        return {"hodl_composite": 0, "consistency": 0, "avg_ret": 0, "avg_dd": 0}

    rets = [w[win]["ret"] for win in available]
    sharpes = [w[win]["sh"] for win in available]
    dds = [abs(w[win]["dd"]) for win in available]

    avg_ret = statistics.mean(rets)
    consistency = sum(1 for s in sharpes if s > 0) / len(sharpes)
    avg_dd = statistics.mean(dds)
    hodl_composite = avg_ret * consistency * (1 - avg_dd)

    return {
        "hodl_composite": hodl_composite,
        "consistency": consistency,
        "avg_ret": avg_ret,
        "avg_dd": avg_dd,
    }


def compute_avg_from_windows(entry, prefix):
    """Compute average ret and sharpe for windows starting with prefix (e.g. '5Y_', '10Y_')."""
    w = entry["w"]
    matching = [k for k in w if k.startswith(prefix)]
    if not matching:
        return 0, 0
    avg_ret = statistics.mean([w[k]["ret"] for k in matching])
    avg_sh = statistics.mean([w[k]["sh"] for k in matching])
    return avg_ret, avg_sh


def build_hodl_leaderboard(mw, strat_files):
    """Build HODL_LEADERBOARD.md content."""
    strategies = []
    for name, entry in mw.items():
        data = compute_hodl_data(entry)
        # Get pre-computed averages from MW JSON, fall back to computing from windows
        avg_5y_ret = entry.get("avg_5Y_ret")
        avg_10y_ret = entry.get("avg_10Y_ret")
        avg_10y_sh = entry.get("avg_10Y_sh")
        if avg_5y_ret is None:
            avg_5y_ret, _ = compute_avg_from_windows(entry, "5Y_")
        if avg_10y_ret is None:
            avg_10y_ret, avg_10y_sh_calc = compute_avg_from_windows(entry, "10Y_")
            if avg_10y_sh is None:
                avg_10y_sh = avg_10y_sh_calc
        if avg_10y_sh is None:
            _, avg_10y_sh = compute_avg_from_windows(entry, "10Y_")

        hodl_c = data["hodl_composite"]
        cons = data["consistency"]
        suitable = hodl_c > 0.1 and cons > 0.50

        strategies.append({
            "name": name,
            "entry": entry,
            "hodl_composite": hodl_c,
            "consistency": cons,
            "avg_5y_ret": avg_5y_ret,
            "avg_10y_ret": avg_10y_ret,
            "avg_10y_sh": avg_10y_sh,
            "suitable": suitable,
        })

    strategies.sort(key=lambda x: x["hodl_composite"], reverse=True)
    n_suitable = sum(1 for s in strategies if s["suitable"])

    lines = []
    lines.append("# HODL LEADERBOARD")
    lines.append("")
    lines.append(f"**For passive, long-term investors.** {len(strategies)} strategies, {n_suitable} suitable.")
    lines.append("")
    lines.append("## HODL Composite (28 windows, 2015-2025)")
    lines.append("")
    lines.append("```")
    lines.append("Composite = Avg Return x Consistency x (1 - Avg |Max Drawdown|)")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Top 10 detailed cards
    lines.append("## Top 10")
    lines.append("")

    for i, s in enumerate(strategies[:10]):
        name = s["name"]
        link = strategy_link(name, strat_files)
        cons_pct = f"{s['consistency'] * 100:.0f}%"
        hodl_str = f"{s['hodl_composite']:.2f}"
        suitable_str = "**Yes**" if s["suitable"] else "No"

        lines.append(f"### #{i+1} [{name}]({link})")
        lines.append("")
        lines.append("| 5Y Avg | 10Y Ret | 10Y Sharpe | Consistency | HODL Composite | Suitable |")
        lines.append("|--------|---------|------------|------------|----------------|----------|")
        lines.append(
            f"| {s['avg_5y_ret']*100:.1f}% | {s['avg_10y_ret']*100:.1f}% | "
            f"{s['avg_10y_sh']:.2f} | {cons_pct} | **{hodl_str}** | {suitable_str} |"
        )
        lines.append("")

    lines.append("---")
    lines.append("")

    # Full rankings table
    lines.append(f"## Full Rankings ({len(strategies)} Strategies)")
    lines.append("")
    lines.append("| # | Strategy | 5Y Avg | 10Y Ret | 10Y Sharpe | Consistency | HODL Composite | Suitable |")
    lines.append("|---|----------|--------|---------|------------|------------|----------------|----------|")

    for i, s in enumerate(strategies):
        name = s["name"]
        link = strategy_link(name, strat_files)
        cons_pct = f"{s['consistency'] * 100:.0f}%"
        hodl_str = fmt_composite(s["hodl_composite"])
        suitable_str = "Yes" if s["suitable"] else "No"

        lines.append(
            f"| {i+1} | [**{name}**]({link}) | "
            f"{s['avg_5y_ret']*100:.1f}% | {s['avg_10y_ret']*100:.1f}% | "
            f"{s['avg_10y_sh']:.2f} | {cons_pct} | {hodl_str} | {suitable_str} |"
        )

    lines.append("")
    lines.append(f"*Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## Disclaimer")
    lines.append("")
    lines.append("This content is for **educational and research purposes only**. It is **not financial advice**.")
    lines.append("")
    lines.append("- Past performance does not guarantee future results.")
    lines.append("- Backtests use historical data and may not reflect real-world conditions (liquidity, slippage, market impact).")
    lines.append("- All strategies tested with simulated capital. No real money was used or is at risk.")
    lines.append("- Consult a qualified financial advisor before making investment decisions.")
    lines.append("- The authors and contributors accept no responsibility for financial losses from using this information.")
    lines.append("- Securities mentioned are not buy/sell recommendations. Do your own due diligence.")
    lines.append("- Trading involves substantial risk of loss. Only invest what you can afford to lose.")
    lines.append("")
    lines.append("By using this information, you acknowledge that you understand and accept these risks.")

    return "\n".join(lines) + "\n"


def build_all_leaderboard(mw, strat_files, result_jsons, strat_jsons):
    """Build ALL_LEADERBOARD.md — flat list of ALL strategies including components."""
    strategies = []
    for name, entry in mw.items():
        data = compute_6win_data(entry)
        w = entry["w"]
        ret_3y = w.get("3Y_2023_2025", {}).get("ret", 0)
        sh_3y = w.get("3Y_2023_2025", {}).get("sh", 0)
        dd_3y = w.get("3Y_2023_2025", {}).get("dd", 0)
        positions = get_positions_count(name, result_jsons)
        strategies.append({
            "name": name, "entry": entry, "composite": data["composite"],
            "avg_ret": data["avg_ret"], "consistency": data["consistency"],
            "avg_dd": data["avg_dd"], "ret_3y": ret_3y, "sh_3y": sh_3y,
            "dd_3y": dd_3y, "positions": positions,
            "type": entry.get("type", "standalone"),
        })
    strategies.sort(key=lambda x: x["composite"], reverse=True)

    lines = [
        "# ALL STRATEGIES LEADERBOARD",
        "",
        f"**{len(strategies)} strategies** — flat ranking of ALL strategies (no collapsing).",
        "",
        "This is the complete, unfiltered list. See [LEADERBOARD.md](LEADERBOARD.md) for the collapsed view",
        "where component strategies are nested under their combined parent.",
        "",
        "Ranked by **Composite Score** (6 rolling windows, 2022-2025).",
        "",
        "---",
        "",
        "| # | Strategy | Type | 3Y Ret | 3Y Sharpe | 3Y DD | Pos | Consistency | Avg Ret | Composite |",
        "|---|----------|------|--------|-----------|-------|-----|------------|---------|-----------|",
    ]

    for i, s in enumerate(strategies):
        name = s["name"]
        link = strategy_link(name, strat_files)
        pos = s["positions"] if s["positions"] is not None else "?"
        cons_pct = f"{s['consistency'] * 100:.0f}%"
        avg_ret_pct = f"{s['avg_ret'] * 100:.1f}%"
        comp_str = fmt_composite(s["composite"])
        stype = s["type"]

        lines.append(
            f"| {i+1} | [**{name}**]({link}) | {stype} | "
            f"{s['ret_3y']*100:.1f}% | {s['sh_3y']:.2f} | {s['dd_3y']*100:.1f}% | "
            f"{pos} | {cons_pct} | {avg_ret_pct} | {comp_str} |"
        )

    lines.append("")
    lines.append(f"*Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
    return "\n".join(lines) + "\n"


ALL_LB_PATH = os.path.join(BASE, "ALL_LEADERBOARD.md")


def main():
    print("Loading multi-window results...")
    mw = load_mw()
    print(f"  {len(mw)} strategies loaded")

    n_standalone = sum(1 for d in mw.values() if d.get("type", "standalone") == "standalone")
    n_combined = sum(1 for d in mw.values() if d.get("type") == "combined")
    n_component = sum(1 for d in mw.values() if d.get("type") == "component")
    print(f"  {n_standalone} standalone + {n_combined} combined + {n_component} components")

    print("Finding strategy files...")
    strat_files = find_strategy_files()
    print(f"  {len(strat_files)} strategy .md files found")

    print("Finding result JSONs...")
    result_jsons = find_result_jsons()
    print(f"  {len(result_jsons)} result JSONs found")

    print("Finding strategy JSONs...")
    strat_jsons = find_strategy_jsons()
    print(f"  {len(strat_jsons)} strategy JSONs found")

    # Build LEADERBOARD.md (collapsed — components nested under combined)
    print("\nBuilding LEADERBOARD.md (collapsed)...")
    lb_content = build_leaderboard(mw, strat_files, result_jsons, strat_jsons)
    with open(LEADERBOARD_PATH, "w") as f:
        f.write(lb_content)
    print(f"  Written {lb_content.count(chr(10))} lines")

    # Build ALL_LEADERBOARD.md (flat — every strategy ranked independently)
    print("\nBuilding ALL_LEADERBOARD.md (flat)...")
    all_content = build_all_leaderboard(mw, strat_files, result_jsons, strat_jsons)
    with open(ALL_LB_PATH, "w") as f:
        f.write(all_content)
    print(f"  Written {all_content.count(chr(10))} lines")

    # Build HODL_LEADERBOARD.md
    print("\nBuilding HODL_LEADERBOARD.md...")
    hodl_content = build_hodl_leaderboard(mw, strat_files)
    with open(HODL_PATH, "w") as f:
        f.write(hodl_content)
    print(f"  Written {hodl_content.count(chr(10))} lines")

    # Verify
    print("\nVerification:")
    lb_ranked = sum(1 for line in lb_content.split("\n") if re.match(r"^\| \d+ \|", line))
    lb_components = lb_content.count("| ↳ |")
    all_rows = sum(1 for line in all_content.split("\n") if re.match(r"^\| \d+ \|", line))
    hodl_rows = sum(1 for line in hodl_content.split("\n") if re.match(r"^\| \d+ \|", line))

    print(f"  LEADERBOARD.md: {lb_ranked} ranked + {lb_components} components nested")
    print(f"  ALL_LEADERBOARD.md: {all_rows} strategies (flat)")
    print(f"  HODL_LEADERBOARD.md: {hodl_rows} strategies")
    print(f"\n  Total strategies in MW: {len(mw)}")


if __name__ == "__main__":
    main()

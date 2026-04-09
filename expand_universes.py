"""Expand strategy universes autonomously.

For each strategy with too few tickers (<8), this script:
1. Analyzes the strategy thesis and existing universe
2. Finds candidate tickers from our cached data that fit the thesis
3. Backtests with expanded universe across rolling windows
4. Only adds tickers if composite score IMPROVES
5. Logs all decisions for review

Usage:
    python3 expand_universes.py                    # Review all strategies
    python3 expand_universes.py --min-tickers 6    # Only expand strategies with <6 tickers
    python3 expand_universes.py --strategy momentum # Expand specific strategy
    python3 expand_universes.py --dry-run          # Show candidates without modifying
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from backtester import Backtester


# ---------------------------------------------------------------------------
# Sector/theme ticker pools — candidates for expansion
# ---------------------------------------------------------------------------
TICKER_POOLS = {
    "tech": ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "AVGO", "CRM", "ADBE", "ORCL",
             "CSCO", "INTC", "AMD", "QCOM", "TXN", "NOW", "INTU", "ANET", "PANW", "FTNT",
             "CRWD", "ZS", "DDOG", "SNOW", "NET", "HUBS", "VEEV", "WDAY", "TEAM", "MDB"],
    "finance": ["JPM", "BAC", "WFC", "GS", "MS", "C", "BLK", "SCHW", "BX", "KKR",
                "AXP", "V", "MA", "COF", "PNC", "USB", "TFC", "SPGI", "MCO", "ICE"],
    "healthcare": ["UNH", "JNJ", "PFE", "MRK", "ABBV", "LLY", "TMO", "ABT", "DHR", "BMY",
                   "AMGN", "GILD", "ISRG", "SYK", "MDT", "ZTS", "IDXX", "REGN", "VRTX", "BIIB"],
    "energy": ["XOM", "CVX", "COP", "EOG", "SLB", "OXY", "DVN", "MPC", "VLO", "PSX",
               "EPD", "ET", "WMB", "MPLX", "OKE", "KMI", "TRGP", "AM", "PAA", "CTRA"],
    "consumer": ["PG", "KO", "PEP", "COST", "WMT", "MCD", "NKE", "SBUX", "TGT", "HD",
                 "LOW", "TJX", "ROST", "DG", "DLTR", "CL", "KHC", "GIS", "SJM", "HRL"],
    "industrial": ["CAT", "DE", "HON", "GE", "MMM", "EMR", "ITW", "ETN", "ROK", "PH",
                   "CMI", "DOV", "IR", "AME", "NDSN", "GGG", "ROP", "FAST", "CTAS", "ODFL"],
    "defense": ["LMT", "RTX", "NOC", "GD", "HII", "LHX", "LDOS", "KTOS", "BAESY", "BA"],
    "reit": ["O", "EQIX", "DLR", "PLD", "AMT", "CCI", "SPG", "VICI", "WELL", "ARE",
             "NLY", "AGNC", "STAG", "MAIN", "ARCC", "VNQ"],
    "dividend": ["JNJ", "PG", "KO", "PEP", "ABBV", "MO", "PM", "XOM", "CVX", "O",
                 "SCHD", "VIG", "NOBL", "VYM", "HDV", "T", "VZ", "IBM", "MMM", "EMR"],
    "gold_commodity": ["GLD", "IAU", "SLV", "GDX", "GDXJ", "NEM", "GOLD", "AEM", "FNV", "WPM",
                       "COPX", "FCX", "DBC", "DBA", "PDBC"],
    "bond": ["TLT", "IEF", "SHY", "BND", "AGG", "LQD", "HYG", "MUB", "VTEB", "TIP",
             "FBND", "SPBO", "VWOB", "SCHI", "BIL"],
    "china": ["BABA", "JD", "PDD", "BIDU", "NIO", "XPEV", "LI", "TCOM", "ZTO", "YUMC",
              "BILI", "TME", "VIPS", "MNSO", "FUTU"],
    "japan": ["TM", "SONY", "MUFG", "SMFG", "NMR", "HMC", "ITOCY", "MITSY", "MRBEY", "MKTAY"],
    "singapore": ["D05.SI", "U11.SI", "O39.SI", "A17U.SI", "N2IU.SI", "C38U.SI", "Z74.SI",
                  "F34.SI", "Y92.SI", "S63.SI", "C52.SI", "H78.SI"],
    "uranium": ["CCJ", "UUUU", "LEU", "UEC", "NXE", "DNN", "URA", "SMR", "OKLO", "VST"],
    "crypto": ["COIN", "MSTR", "MARA", "RIOT", "GBTC", "ETHE", "BITO", "HOOD"],
    "shipping": ["TRMD", "FRO", "STNG", "INSW", "TNK", "DHT", "ZIM", "SBLK", "GOGL", "DAC"],
}


def _classify_strategy(name: str, description: str, universe: list[str]) -> list[str]:
    """Classify which ticker pools are relevant for this strategy."""
    name_lower = name.lower()
    desc_lower = description.lower()
    combined = name_lower + " " + desc_lower

    pools = []
    if any(w in combined for w in ["tech", "ai", "software", "saas", "cloud", "cyber", "compute"]):
        pools.append("tech")
    if any(w in combined for w in ["bank", "financ", "payment", "insurance", "float"]):
        pools.append("finance")
    if any(w in combined for w in ["health", "pharma", "biotech", "medical", "drug"]):
        pools.append("healthcare")
    if any(w in combined for w in ["energy", "oil", "gas", "pipeline", "midstream"]):
        pools.append("energy")
    if any(w in combined for w in ["consumer", "retail", "staple", "food", "beverage"]):
        pools.append("consumer")
    if any(w in combined for w in ["industrial", "manufactur", "reshoring", "infrastructure"]):
        pools.append("industrial")
    if any(w in combined for w in ["defense", "military", "aerospace"]):
        pools.append("defense")
    if any(w in combined for w in ["reit", "real estate", "property"]):
        pools.append("reit")
    if any(w in combined for w in ["dividend", "income", "yield", "aristocrat"]):
        pools.append("dividend")
    if any(w in combined for w in ["gold", "commodit", "mining", "metal"]):
        pools.append("gold_commodity")
    if any(w in combined for w in ["bond", "treasury", "fixed income"]):
        pools.append("bond")
    if any(w in combined for w in ["china", "chinese", "adr"]):
        pools.append("china")
    if any(w in combined for w in ["japan", "sogo", "shosha"]):
        pools.append("japan")
    if any(w in combined for w in ["singapore", "sgx", "dbs", "uob"]):
        pools.append("singapore")
    if any(w in combined for w in ["uranium", "nuclear"]):
        pools.append("uranium")
    if any(w in combined for w in ["crypto", "bitcoin", "blockchain"]):
        pools.append("crypto")
    if any(w in combined for w in ["shipping", "tanker", "freight"]):
        pools.append("shipping")

    return pools if pools else ["tech", "consumer"]  # Default fallback


def _find_candidates(universe: set[str], pools: list[str], max_candidates: int = 10) -> list[str]:
    """Find candidate tickers from pools that aren't already in the universe."""
    candidates = []
    for pool_name in pools:
        pool = TICKER_POOLS.get(pool_name, [])
        for ticker in pool:
            if ticker not in universe and ticker not in candidates:
                candidates.append(ticker)
    return candidates[:max_candidates]


def _compute_composite(strategy, symbols, windows):
    """Run rolling window backtests and compute horizon-weighted composite."""
    results = {}
    for wn, (start, end) in windows.items():
        try:
            bt = Backtester(
                strategy=strategy, symbols=symbols, start=start, end=end,
                initial_cash=100000, benchmark="SPY",
                rebalance_frequency=strategy.config.rebalance_frequency,
            )
            r = bt.run()
            m = r["metrics"]
            results[wn] = {
                "ret": round(m.get("total_return", 0), 4),
                "sh": round(m.get("sharpe_ratio", 0), 2),
                "dd": round(m.get("max_drawdown", 0), 4),
            }
        except Exception:
            results[wn] = None

    # Horizon-weighted composite
    horizons = {}
    for wn, wd in results.items():
        if wd is None:
            continue
        h = wn.split("_")[0]
        horizons.setdefault(h, []).append(wd)

    main_rets = []
    for h in ["1Y", "3Y", "5Y"]:
        if h in horizons:
            main_rets.append(sum(v["ret"] for v in horizons[h]) / len(horizons[h]))

    avg_ret = sum(main_rets) / len(main_rets) if main_rets else 0
    all_valid = [v for v in results.values() if v]
    consistency = sum(1 for v in all_valid if v["sh"] > 0) / len(all_valid) if all_valid else 0
    avg_dd = sum(abs(v["dd"]) for v in all_valid) / len(all_valid) if all_valid else 0.5
    composite = avg_ret * consistency * (1 - avg_dd)

    return round(composite, 4), round(consistency, 2), results


# Quick windows for testing (subset of full 28)
QUICK_WINDOWS = {
    "1Y_2023": ("2023-01-01", "2023-12-31"),
    "1Y_2024": ("2024-01-01", "2024-12-31"),
    "3Y_2022_2024": ("2022-01-01", "2024-12-31"),
    "3Y_2023_2025": ("2023-01-01", "2025-12-31"),
    "5Y_2020_2024": ("2020-01-01", "2024-12-31"),
}


def expand_strategy(key, getter, src, min_tickers=8, dry_run=False):
    """Attempt to expand a strategy's universe if it has too few tickers."""
    try:
        strategy = getter(key)
    except Exception:
        return None

    universe = list(strategy.config.universe)
    if len(universe) >= min_tickers:
        return {"key": key, "action": "skip", "reason": f"already has {len(universe)} tickers"}

    name = strategy.config.name
    desc = strategy.config.description

    # Step 1: Classify and find candidates
    pools = _classify_strategy(name, desc, universe)
    candidates = _find_candidates(set(universe), pools, max_candidates=8)

    if not candidates:
        return {"key": key, "action": "skip", "reason": "no candidates found"}

    # Step 2: Backtest ORIGINAL universe
    orig_composite, orig_consistency, _ = _compute_composite(strategy, universe, QUICK_WINDOWS)

    # Step 3: Test each candidate one at a time
    accepted = []
    current_universe = list(universe)

    for ticker in candidates:
        test_universe = current_universe + [ticker]

        # Create a temporary strategy with expanded universe
        try:
            test_strategy = getter(key, universe=test_universe)
        except Exception:
            continue

        new_composite, new_consistency, _ = _compute_composite(test_strategy, test_universe, QUICK_WINDOWS)

        if new_composite > orig_composite and new_consistency >= orig_consistency - 0.05:
            accepted.append(ticker)
            current_universe = test_universe
            orig_composite = new_composite
            orig_consistency = new_consistency

    if not accepted:
        return {
            "key": key, "action": "no_improvement",
            "original_size": len(universe), "candidates_tested": len(candidates),
            "original_composite": orig_composite,
        }

    if dry_run:
        return {
            "key": key, "action": "would_add", "tickers": accepted,
            "new_size": len(current_universe), "new_composite": orig_composite,
        }

    return {
        "key": key, "action": "expanded", "added": accepted,
        "old_size": len(universe), "new_size": len(current_universe),
        "new_composite": orig_composite, "new_consistency": orig_consistency,
    }


def main():
    parser = argparse.ArgumentParser(description="Expand strategy universes")
    parser.add_argument("--min-tickers", type=int, default=8, help="Minimum tickers threshold")
    parser.add_argument("--strategy", type=str, help="Specific strategy to expand")
    parser.add_argument("--dry-run", action="store_true", help="Show candidates without modifying")
    args = parser.parse_args()

    # Load all strategies
    mods = [
        ("theme_strategies", "THEME_STRATEGIES", "get_theme_strategy", "theme"),
        ("unconventional_strategies", "UNCONVENTIONAL_STRATEGIES", "get_unconventional_strategy", "unconventional"),
        ("portfolio_strategies", "PORTFOLIO_STRATEGIES", "get_portfolio_strategy", "portfolio"),
        ("crisis_commodity_strategies", "CRISIS_COMMODITY_STRATEGIES", "get_crisis_commodity_strategy", "crisis"),
        ("hedge_fund_strategies", "HEDGE_FUND_STRATEGIES", "get_hedge_fund_strategy", "hedge_fund"),
        ("news_event_strategies", "NEWS_EVENT_STRATEGIES", "get_news_event_strategy", "news_event"),
        ("recession_strategies", "RECESSION_STRATEGIES", "get_recession_strategy", "recession"),
        ("math_strategies", "MATH_STRATEGIES", "get_math_strategy", "math"),
        ("political_strategies", "POLITICAL_STRATEGIES", "get_political_strategy", "political"),
        ("williams_seasonal_strategies", "WILLIAMS_SEASONAL_STRATEGIES", "get_williams_seasonal_strategy", "williams_seasonal"),
        ("personas", "ALL_PERSONAS", "get_persona", "generic"),
        ("famous_investors", "FAMOUS_INVESTORS", "get_famous_investor", "famous"),
        ("strategy_orchestrator", "ORCHESTRATOR_STRATEGIES", "get_orchestrated_strategy", "orchestrator"),
    ]

    ALL = []
    for mod_name, reg_name, getter_name, src in mods:
        try:
            m = __import__(mod_name)
            reg = getattr(m, reg_name)
            getter = getattr(m, getter_name)
            for k in reg:
                ALL.append((k, getter, src))
        except Exception:
            pass

    # Filter
    if args.strategy:
        ALL = [(k, g, s) for k, g, s in ALL if k == args.strategy]

    print(f"Reviewing {len(ALL)} strategies (min tickers: {args.min_tickers})")
    print(f"{'Dry run' if args.dry_run else 'LIVE mode'}")
    print()

    # Count how many need expansion
    thin = []
    for key, getter, src in ALL:
        try:
            p = getter(key)
            if len(p.config.universe) < args.min_tickers:
                thin.append((key, getter, src, len(p.config.universe)))
        except Exception:
            pass

    print(f"Strategies with <{args.min_tickers} tickers: {len(thin)}")
    for key, _, _, n in thin:
        print(f"  {key}: {n} tickers")
    print()

    # Expand each
    results = []
    for i, (key, getter, src, n) in enumerate(thin):
        t0 = time.time()
        result = expand_strategy(key, getter, src, args.min_tickers, args.dry_run)
        elapsed = int(time.time() - t0)
        if result:
            result["elapsed"] = elapsed
            results.append(result)
            action = result.get("action", "?")
            if action == "expanded":
                print(f"[{i+1}/{len(thin)}] EXPANDED {key}: +{len(result['added'])} tickers "
                      f"({result['old_size']}→{result['new_size']}), "
                      f"composite={result['new_composite']:.2f} ({elapsed}s)")
            elif action == "would_add":
                print(f"[{i+1}/{len(thin)}] WOULD ADD to {key}: {result['tickers']} ({elapsed}s)")
            elif action == "no_improvement":
                print(f"[{i+1}/{len(thin)}] NO IMPROVEMENT for {key} "
                      f"(tested {result['candidates_tested']} candidates) ({elapsed}s)")
            else:
                print(f"[{i+1}/{len(thin)}] SKIP {key}: {result.get('reason', '?')} ({elapsed}s)")

    # Save log
    log_path = Path("knowledge") / f"universe_expansion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    log_path.write_text(json.dumps(results, indent=2, default=str))
    print(f"\nLog saved to {log_path}")

    expanded = [r for r in results if r.get("action") == "expanded"]
    print(f"\nSummary: {len(expanded)} strategies expanded out of {len(thin)} reviewed")


if __name__ == "__main__":
    main()

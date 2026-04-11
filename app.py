"""agents-assemble Web Dashboard — browser-based trading platform.

Launch: python app.py
Open: http://localhost:8888

Features:
- Strategy leaderboard with sorting/filtering
- Equity charts with indicators (Bloomberg-style)
- Catalyst scanner for any ticker
- Backtest any strategy across horizons
- News feed
- Trade execution (Public.com integration)
- Portfolio view
"""

from __future__ import annotations

import json
import math
import re
import base64
import sys
import time
from datetime import date, timedelta
from pathlib import Path

from flask import Flask, request, jsonify

sys.path.insert(0, str(Path(__file__).parent))

app = Flask(__name__)

_DATE_SUFFIX_RE = re.compile(r'_\d{4}(-\d{2}(-\d{2})?)?$')
_SYMBOL_RE = re.compile(r'^[A-Z0-9.\-^=]{1,15}$')
_STRATEGY_RE = re.compile(r'^[a-z0-9_]{1,60}$')
_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')

def _mtime(p):
    try:
        return p.stat().st_mtime
    except OSError:
        return 0

def _valid_date(s):
    """Validate YYYY-MM-DD string is a real calendar date."""
    if not _DATE_RE.match(s):
        return False
    try:
        date.fromisoformat(s)
        return True
    except ValueError:
        return False

def _sanitize_for_json(obj):
    if isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize_for_json(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    if hasattr(obj, 'item'):
        try:
            val = obj.item()
        except (ValueError, TypeError):
            # Multi-element numpy array — convert to list and recurse
            if hasattr(obj, 'tolist'):
                return _sanitize_for_json(obj.tolist())
            return None
        if isinstance(val, float) and not math.isfinite(val):
            return None
        return val
    return obj

def _safe_metric(val, ndigits=4):
    if isinstance(val, bool):
        return 0
    if hasattr(val, 'item'):
        try:
            val = val.item()
        except (ValueError, TypeError):
            return 0
    if not isinstance(val, (int, float)) or not math.isfinite(val):
        return 0
    return round(val, ndigits)

# ---------------------------------------------------------------------------
# HTML Template (single-page app with Bloomberg dark theme)
# ---------------------------------------------------------------------------
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<title>agents-assemble</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root {
    --bg: #0a0f1e;
    --card: #111827;
    --card-hover: #151d2e;
    --gold: #d4af37;
    --gold-dim: rgba(212,175,55,0.15);
    --gold-shimmer: rgba(255,215,0,0.05);
    --warm-white: #f5f0e8;
    --cream: #e8e0d4;
    --warm-gray: #8b7e6a;
    --warm-gray-light: #a49880;
    --emerald: #34d399;
    --rose: #f87171;
    --border: rgba(212,175,55,0.08);
    --border-hover: rgba(212,175,55,0.25);
    --shadow: 0 2px 16px rgba(0,0,0,0.3);
    --shadow-lg: 0 8px 32px rgba(0,0,0,0.4);
    --radius: 12px;
    --radius-sm: 8px;
    --radius-pill: 50px;
    --font: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    --mono: 'SF Mono', 'Fira Code', 'Cascadia Code', monospace;
    --transition: 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html { scroll-behavior: smooth; }
body { background: var(--bg); color: var(--cream); font-family: var(--font); font-size: 14px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
::selection { background: var(--gold-dim); color: var(--warm-white); }
a { color: var(--gold); text-decoration: none; transition: color var(--transition); }
a:hover { color: var(--warm-white); }

/* ---- Top Navigation ---- */
.topbar {
    position: sticky; top: 0; z-index: 100;
    background: rgba(10,15,30,0.85); backdrop-filter: blur(20px) saturate(1.2);
    border-bottom: 1px solid var(--border);
    padding: 0 32px; height: 56px;
    display: flex; align-items: center; justify-content: space-between;
}
.topbar .logo {
    font-weight: 300; font-size: 17px; letter-spacing: 0.5px; color: var(--cream);
    display: flex; align-items: center; gap: 8px;
}
.topbar .logo .diamond {
    display: inline-block; width: 8px; height: 8px; background: var(--gold);
    transform: rotate(45deg); border-radius: 1px;
}
.topbar .nav { display: flex; gap: 4px; }
.topbar .nav a {
    color: var(--warm-gray); font-size: 13px; font-weight: 400;
    padding: 6px 14px; border-radius: var(--radius-sm);
    transition: all var(--transition); letter-spacing: 0.2px;
    position: relative;
}
.topbar .nav a::after {
    content: ''; position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
    width: 0; height: 2px; background: var(--gold);
    transition: width var(--transition); border-radius: 1px;
}
.topbar .nav a.active, .topbar .nav a:hover { color: var(--warm-white); }
.topbar .nav a.active::after { width: 20px; }
.topbar .status-pill {
    font-size: 11px; color: var(--warm-gray); font-family: var(--mono);
    display: flex; align-items: center; gap: 6px;
}
.topbar .status-pill .dot {
    width: 6px; height: 6px; border-radius: 50%; background: var(--emerald);
    animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }

/* ---- Container ---- */
.container { max-width: 1200px; margin: 0 auto; padding: 24px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 20px; }
.full { grid-column: 1 / -1; }

/* ---- Panels / Cards ---- */
.panel {
    background: var(--card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 24px;
    box-shadow: var(--shadow); transition: border-color var(--transition);
}
.panel:hover { border-color: var(--border-hover); }
.panel h2 {
    font-weight: 300; font-size: 12px; letter-spacing: 1.5px; text-transform: uppercase;
    color: var(--warm-gray); margin-bottom: 16px;
    padding-bottom: 12px; border-bottom: 1px solid var(--border);
}
.panel h3 {
    font-weight: 500; font-size: 13px; color: var(--gold);
    margin: 16px 0 8px; letter-spacing: 0.3px;
}

/* ---- Tables ---- */
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th {
    text-align: left; padding: 10px 12px;
    font-size: 11px; font-weight: 500; letter-spacing: 0.8px; text-transform: uppercase;
    color: var(--warm-gray); border-bottom: 1px solid var(--border);
    background: transparent;
}
td { padding: 10px 12px; border-bottom: 1px solid rgba(255,255,255,0.03); font-family: var(--mono); font-size: 12px; }
tr { transition: background var(--transition); }
tr:hover { background: rgba(212,175,55,0.03); }
.positive { color: var(--emerald); }
.negative { color: var(--rose); }

/* ---- Inputs & Buttons ---- */
input, select {
    background: rgba(255,255,255,0.04); color: var(--cream);
    border: 1px solid var(--border); padding: 10px 16px;
    border-radius: var(--radius-sm); font-family: var(--font); font-size: 13px;
    transition: all var(--transition); outline: none;
}
input:focus, select:focus { border-color: var(--gold); box-shadow: 0 0 0 3px rgba(212,175,55,0.1); }
input::placeholder { color: var(--warm-gray); }
button {
    background: var(--gold); color: var(--bg); cursor: pointer;
    font-family: var(--font); font-size: 13px; font-weight: 600;
    border: none; padding: 10px 20px; border-radius: var(--radius-sm);
    transition: all var(--transition); letter-spacing: 0.3px;
}
button:hover { background: #e0c050; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(212,175,55,0.25); }
button:active { transform: translateY(0); }
button.secondary {
    background: transparent; color: var(--gold); border: 1px solid var(--gold);
}
button.secondary:hover { background: var(--gold-dim); }
button.danger { background: var(--rose); color: white; }
button.danger:hover { background: #ef4444; box-shadow: 0 4px 12px rgba(248,113,113,0.25); }
button.ghost {
    background: transparent; color: var(--warm-gray); border: 1px solid var(--border);
}
button.ghost:hover { color: var(--cream); border-color: var(--warm-gray); background: transparent; }
.input-group { display: flex; gap: 10px; margin-bottom: 16px; align-items: center; }
.input-group input, .input-group select { flex: 1; }

/* ---- Chart ---- */
.chart-img { width: 100%; border-radius: var(--radius-sm); }

/* ---- Tags ---- */
.tag {
    display: inline-block; padding: 3px 10px; border-radius: var(--radius-pill);
    font-size: 11px; font-weight: 500; letter-spacing: 0.3px; margin-right: 4px;
    font-family: var(--font);
}
.tag-green { background: rgba(52,211,153,0.1); color: var(--emerald); border: 1px solid rgba(52,211,153,0.2); }
.tag-red { background: rgba(248,113,113,0.1); color: var(--rose); border: 1px solid rgba(248,113,113,0.2); }
.tag-blue { background: rgba(96,165,250,0.1); color: #60a5fa; border: 1px solid rgba(96,165,250,0.2); }
.tag-yellow { background: rgba(212,175,55,0.1); color: var(--gold); border: 1px solid rgba(212,175,55,0.2); }

/* ---- Loading ---- */
.loading { color: var(--warm-gray); font-style: italic; font-size: 13px; }

/* ---- Status Bar ---- */
#status {
    position: fixed; bottom: 16px; right: 16px;
    background: var(--card); border: 1px solid var(--border);
    padding: 8px 16px; border-radius: var(--radius-pill);
    font-size: 11px; color: var(--warm-gray); font-family: var(--mono);
    box-shadow: var(--shadow);
}

/* ---- Quick Actions ---- */
.quick-actions { display: flex; gap: 10px; margin: 8px 0; flex-wrap: wrap; }
.quick-btn {
    padding: 10px 22px; font-size: 13px; border-radius: var(--radius-pill);
    cursor: pointer; transition: all var(--transition); font-weight: 500;
    letter-spacing: 0.2px; border: none;
}
.quick-btn:hover { transform: translateY(-2px); }
.quick-btn-primary { background: var(--gold); color: var(--bg); }
.quick-btn-primary:hover { box-shadow: 0 6px 20px rgba(212,175,55,0.3); }
.quick-btn-secondary { background: transparent; color: var(--gold); border: 1px solid rgba(212,175,55,0.3); }
.quick-btn-secondary:hover { background: var(--gold-dim); box-shadow: 0 4px 16px rgba(212,175,55,0.15); }
.quick-btn-warn { background: transparent; color: var(--rose); border: 1px solid rgba(248,113,113,0.3); }
.quick-btn-warn:hover { background: rgba(248,113,113,0.08); box-shadow: 0 4px 16px rgba(248,113,113,0.15); }

/* ---- Hero Market Card ---- */
.hero-market {
    background: linear-gradient(135deg, var(--card) 0%, rgba(212,175,55,0.04) 100%);
    border: 1px solid var(--border); border-radius: var(--radius);
    padding: 28px 32px; margin-bottom: 20px;
}
.hero-market .hero-title {
    font-weight: 300; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase;
    color: var(--warm-gray); margin-bottom: 16px;
    display: flex; align-items: center; justify-content: space-between;
}
.market-bar { display: flex; gap: 16px; flex-wrap: wrap; }
.market-pill {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 8px 16px; border-radius: var(--radius-sm);
    font-size: 13px; background: rgba(255,255,255,0.03);
    border: 1px solid var(--border); transition: border-color var(--transition);
}
.market-pill:hover { border-color: var(--border-hover); }
.market-pill .arrow-up { color: var(--emerald); }
.market-pill .arrow-down { color: var(--rose); }
.market-pill .label { color: var(--warm-gray); font-size: 12px; }
.market-pill b { font-weight: 500; color: var(--cream); }

/* ---- Top Picks as horizontal scroll cards ---- */
.top-picks-scroll { display: flex; gap: 14px; overflow-x: auto; padding: 4px 0 12px; scrollbar-width: thin; scrollbar-color: var(--border) transparent; }
.top-picks-scroll::-webkit-scrollbar { height: 4px; }
.top-picks-scroll::-webkit-scrollbar-track { background: transparent; }
.top-picks-scroll::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
.top-pick-card {
    flex: 0 0 260px; background: var(--card); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 20px; cursor: pointer;
    transition: all var(--transition); position: relative; overflow: hidden;
}
.top-pick-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
    opacity: 0; transition: opacity var(--transition);
}
.top-pick-card:hover { border-color: var(--border-hover); transform: translateY(-2px); box-shadow: var(--shadow-lg); }
.top-pick-card:hover::before { opacity: 1; }
.top-pick-rank {
    font-size: 11px; font-weight: 500; letter-spacing: 1px; color: var(--gold);
    margin-bottom: 10px; text-transform: uppercase;
}
.top-pick-info .name { font-weight: 500; font-size: 14px; color: var(--warm-white); margin-bottom: 4px; }
.top-pick-info .meta { color: var(--warm-gray); font-size: 12px; }
.top-pick-stats { margin-top: 14px; display: flex; justify-content: space-between; align-items: flex-end; }
.top-pick-stats .ret { font-size: 22px; font-weight: 300; font-family: var(--mono); }
.top-pick-stats .sharpe { color: var(--warm-gray); font-size: 12px; font-family: var(--mono); }

/* ---- Detail Panel (slide from right) ---- */
.modal-overlay {
    display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.6); backdrop-filter: blur(4px);
    z-index: 1000; overflow-y: auto;
}
.modal-overlay.active { display: flex; justify-content: flex-end; }
.modal-content {
    background: var(--bg); border-left: 1px solid var(--border);
    width: 680px; max-width: 90vw; min-height: 100vh;
    padding: 32px; position: relative;
    animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    overflow-y: auto;
}
@keyframes slideIn { from { transform: translateX(100%); opacity: 0; } to { transform: translateX(0); opacity: 1; } }
.modal-close {
    position: sticky; top: 0; float: right;
    color: var(--warm-gray); cursor: pointer; font-size: 14px;
    background: var(--card); border: 1px solid var(--border);
    width: 36px; height: 36px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    transition: all var(--transition); z-index: 2;
}
.modal-close:hover { color: var(--rose); border-color: var(--rose); background: rgba(248,113,113,0.08); }
.modal-divider { height: 1px; background: linear-gradient(90deg, var(--gold), transparent); margin: 20px 0; opacity: 0.3; }

/* ---- Stock Group Buttons ---- */
.stock-group-btns { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }
.stock-group-btn {
    padding: 6px 16px; font-size: 12px; border-radius: var(--radius-pill);
    cursor: pointer; background: transparent; color: var(--warm-gray);
    border: 1px solid var(--border); transition: all var(--transition);
    font-family: var(--font); font-weight: 400;
}
.stock-group-btn:hover { color: var(--gold); border-color: var(--gold); background: var(--gold-dim); }

/* ---- Portfolio builder ---- */
.strat-checkbox { margin-right: 8px; accent-color: var(--gold); width: 16px; height: 16px; }
.alloc-input { width: 64px; text-align: center; padding: 6px 8px; font-family: var(--mono); font-size: 12px; }
.overlap-badge {
    display: inline-block; padding: 2px 8px; border-radius: var(--radius-pill);
    font-size: 10px; background: rgba(212,175,55,0.1); color: var(--gold);
    border: 1px solid rgba(212,175,55,0.2);
}

/* ---- View toggle ---- */
.view-toggle {
    display: inline-flex; border: 1px solid var(--border);
    border-radius: var(--radius-sm); overflow: hidden; margin-bottom: 14px;
}
.view-toggle button {
    border: none; border-radius: 0; padding: 8px 20px; font-size: 12px;
    font-weight: 500; letter-spacing: 0.3px;
}
.view-toggle button.active { background: var(--gold); color: var(--bg); }
.view-toggle button:not(.active) { background: transparent; color: var(--warm-gray); }
.view-toggle button:not(.active):hover { color: var(--cream); background: rgba(255,255,255,0.03); }

/* ---- Sparkline ---- */
.sparkline { font-size: 12px; letter-spacing: 2px; }

/* ---- Search bar (Google-style) ---- */
.search-hero {
    max-width: 640px; margin: 0 auto 24px; text-align: center;
}
.search-hero input {
    width: 100%; padding: 16px 24px; font-size: 16px;
    border-radius: var(--radius-pill); background: var(--card);
    border: 1px solid var(--border); color: var(--cream);
    text-align: center; font-family: var(--font);
    transition: all var(--transition);
}
.search-hero input:focus {
    border-color: var(--gold); box-shadow: 0 0 0 4px rgba(212,175,55,0.1), var(--shadow-lg);
}
.search-hero-sub {
    display: flex; gap: 10px; justify-content: center; align-items: center; margin-top: 14px;
}

/* ---- Progress bar ---- */
.progress-track { background: rgba(255,255,255,0.05); border-radius: 4px; height: 4px; overflow: hidden; }
.progress-fill { background: linear-gradient(90deg, var(--gold), #e0c050); height: 100%; transition: width 0.5s; border-radius: 4px; }

/* ---- Responsive ---- */
@media (max-width: 1024px) {
    .container { padding: 16px; }
    .grid { grid-template-columns: 1fr; }
    .grid-3 { grid-template-columns: 1fr; }
    .modal-content { width: 100%; max-width: 100vw; }
}
@media (max-width: 768px) {
    .topbar { padding: 0 16px; flex-wrap: wrap; height: auto; padding: 12px 16px; gap: 8px; }
    .topbar .nav { flex-wrap: wrap; gap: 2px; }
    .topbar .nav a { font-size: 12px; padding: 4px 10px; }
    .topbar .status-pill { display: none; }
    .hero-market { padding: 20px; }
    .top-pick-card { flex: 0 0 220px; }
    .search-hero input { font-size: 14px; padding: 12px 20px; }
}

/* ---- Fade-in animation ---- */
@keyframes fadeUp { from { opacity: 0; transform: translateY(12px); } to { opacity: 1; transform: translateY(0); } }
[id^="section-"] { animation: fadeUp 0.3s ease-out; }
</style>
</head>
<body>

<!-- Top Navigation -->
<div class="topbar">
    <div class="logo">
        <span class="diamond"></span>
        agents-assemble
    </div>
    <div class="nav">
        <a href="#" class="active" onclick="showSection('dashboard', this)">Dashboard</a>
        <a href="#" onclick="showSection('strategies', this)">Strategies</a>
        <a href="#" onclick="showSection('stockpick', this)">StockPick</a>
        <a href="#" onclick="showSection('portfolio', this)">Portfolio</a>
        <a href="#" onclick="showSection('catalyst', this)">Catalyst</a>
        <a href="#" onclick="showSection('charts', this)">Charts</a>
        <a href="#" onclick="showSection('trade', this)">Trade</a>
    </div>
    <div class="status-pill">
        <span class="dot"></span>
        <span id="market-status-time"></span>
    </div>
</div>

<div class="container">

<!-- ===================== DASHBOARD ===================== -->
<div id="section-dashboard">

<!-- Hero Market Card -->
<div class="hero-market">
    <div class="hero-title">
        <span>Today's Market</span>
    </div>
    <div id="market-pills" class="market-bar">
        <span class="market-pill"><span class="label">Loading market data...</span></span>
    </div>
</div>

<!-- Quick Actions -->
<div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:24px;">
    <button class="quick-btn quick-btn-primary" onclick="showSection('stockpick', document.querySelector('[onclick*=stockpick]'))">StockPick Analysis</button>
    <button class="quick-btn quick-btn-secondary" onclick="document.getElementById('leaderboard-table').scrollIntoView({behavior:'smooth'})">Leaderboard</button>
    <button class="quick-btn quick-btn-secondary" onclick="showSection('trade', document.querySelector('[onclick*=trade]'))">Trade Plan</button>
    <button class="quick-btn quick-btn-warn" onclick="showSection('catalyst', document.querySelector('[onclick*=catalyst]'))">Catalyst Scanner</button>
    <button class="quick-btn quick-btn-secondary" onclick="loadTopPicks()">Refresh</button>
</div>

<!-- Top Picks (horizontal scroll) -->
<div class="panel full" style="margin-bottom:20px;">
    <h2>Top Picks</h2>
    <div class="view-toggle" style="margin-bottom:12px;">
        <button class="active" onclick="setTopPicksView('active', this)">Active</button>
        <button onclick="setTopPicksView('passive', this)">Passive</button>
    </div>
    <div id="top-picks-list" class="loading">Loading top picks...</div>
</div>

<div class="grid">
    <!-- Market Overview -->
    <div class="panel">
        <h2>Market Overview</h2>
        <div id="market-overview" class="loading">Loading...</div>
    </div>
    <!-- Quick Scan -->
    <div class="panel">
        <h2>Quick Scan</h2>
        <div class="input-group">
            <input type="text" id="scan-ticker" placeholder="Enter ticker (e.g. NVDA)" value="NVDA" style="flex:1;">
            <button onclick="scanTicker()">Scan</button>
        </div>
        <div id="scan-results"></div>
    </div>
</div>

<!-- Leaderboard -->
<div class="panel full" style="margin-top:20px;">
    <h2>Strategy Leaderboard</h2>
    <div class="input-group">
        <select id="horizon-select" onchange="loadLeaderboard()">
            <option value="3y" selected>3Y (2022-2024)</option>
            <option value="1y">1Y (2024)</option>
            <option value="5y">5Y (2020-2024)</option>
        </select>
        <span id="leaderboard-status" style="color:var(--warm-gray);font-size:12px;"></span>
    </div>
    <div id="leaderboard-table" class="loading">Loading strategies...</div>
</div>
</div>

<!-- Strategy Detail Panel -->
<div id="strategy-modal" class="modal-overlay" onclick="if(event.target===this)closeStrategyModal()">
    <div class="modal-content">
        <button class="modal-close" onclick="closeStrategyModal()">&#10005;</button>
        <div id="strategy-modal-body">Loading...</div>
    </div>
</div>

<!-- ===================== STRATEGIES ===================== -->
<div id="section-strategies" style="display:none">
<div class="panel">
    <h2>All Strategies</h2>
    <div class="input-group">
        <select id="cat-filter" onchange="loadStrategies()">
            <option value="">All Categories</option>
            <option value="generic">Generic</option>
            <option value="famous">Famous Investors</option>
            <option value="theme">Themes</option>
            <option value="research">Research</option>
            <option value="political">Political</option>
            <option value="portfolio">Portfolio</option>
            <option value="unconventional">Unconventional</option>
            <option value="math">Math</option>
            <option value="recession">Recession</option>
            <option value="news_event">News/Event</option>
            <option value="hedge_fund">Hedge Fund</option>
            <option value="crisis">Crisis/Commodity</option>
        </select>
        <button class="secondary" onclick="loadStrategies()">Refresh</button>
    </div>
    <div id="all-strategies" class="loading">Loading...</div>
</div>
</div>

<!-- ===================== CATALYST SCANNER ===================== -->
<div id="section-catalyst" style="display:none">
<div class="panel">
    <h2>Catalyst Analyzer</h2>
    <div class="input-group">
        <input type="text" id="catalyst-ticker" placeholder="Enter ticker (e.g. NTDOY)" value="NTDOY" style="flex:1;">
        <button onclick="runCatalyst()">Analyze</button>
    </div>
    <div id="catalyst-results" class="loading">Enter a ticker and click Analyze</div>
</div>
</div>

<!-- ===================== CHARTS ===================== -->
<div id="section-charts" style="display:none">
<div class="panel">
    <h2>Equity Chart</h2>
    <div class="input-group">
        <input type="text" id="chart-ticker" placeholder="Ticker" value="NVDA">
        <input type="text" id="chart-start" placeholder="Start date" value="2024-01-01">
        <button onclick="loadChart()">Generate</button>
    </div>
    <div id="chart-container"></div>
</div>
</div>

<!-- ===================== STOCKPICK ===================== -->
<div id="section-stockpick" style="display:none">
<div class="panel" style="border-color: rgba(212,175,55,0.15);">
    <h2>StockPick &mdash; AI Strategy Matcher</h2>
    <p style="color:var(--warm-gray-light); margin-bottom:20px; font-size:14px; max-width:640px;">
        Enter your stock picks below. We match them to our best backtested strategies,
        suggest additional tickers, and show volatility-adjusted position sizing.
    </p>

    <!-- Stock Group Presets -->
    <div class="stock-group-btns">
        <button class="stock-group-btn" onclick="setStockGroup('NVDA, AAPL, MSFT, GOOGL, AMZN, META, TSLA')">Mag 7</button>
        <button class="stock-group-btn" onclick="setStockGroup('JNJ, PG, KO, PEP, MMM, EMR, CL')">Dividend Kings</button>
        <button class="stock-group-btn" onclick="setStockGroup('DBS, OCBC, UOB')">SG Banks</button>
        <button class="stock-group-btn" onclick="setStockGroup('CCJ, UEC, NXE, LEU, DNN, UUUU')">Uranium</button>
        <button class="stock-group-btn" onclick="setStockGroup('SMCI, AVGO, ARM, TSM, AMD, MRVL')">AI Chips</button>
        <button class="stock-group-btn" onclick="setStockGroup('LLY, NVO, VKTX, AMGN')">GLP-1 / Obesity</button>
        <button class="stock-group-btn" onclick="setStockGroup('LMT, RTX, NOC, GD, BA')">Defense</button>
        <button class="stock-group-btn" onclick="setStockGroup('BRK-B, JPM, V, MA, GS')">Financials</button>
    </div>

    <div class="search-hero" style="max-width:100%; text-align:left;">
        <div class="input-group" style="margin-bottom:0;">
            <input type="text" id="pick-symbols" placeholder="Tickers separated by commas (e.g. NVDA, AAPL, TSLA)" style="flex:3; font-size:15px; padding:14px 20px; border-radius:var(--radius-pill);">
            <input type="number" id="pick-amount" value="100000" min="1000" step="1000" style="width:140px; font-size:14px; padding:14px 16px;" placeholder="Portfolio $">
            <select id="pick-horizon" style="width:80px; font-size:14px; padding:14px 12px;">
                <option value="3y" selected>3Y</option>
                <option value="1y">1Y</option>
                <option value="5y">5Y</option>
            </select>
            <button onclick="analyzeStockPick()" style="font-size:14px; padding:14px 28px; border-radius:var(--radius-pill);">Analyze</button>
        </div>
    </div>
    <div id="pick-loading-bar" style="display:none; margin:16px 0;">
        <div class="progress-track">
            <div id="pick-progress" class="progress-fill" style="width:0%;"></div>
        </div>
        <p id="pick-loading-text" style="color:var(--warm-gray); font-size:12px; margin-top:6px;">Matching strategies...</p>
    </div>
    <div id="pick-results"></div>
</div>
</div>

<!-- ===================== PORTFOLIO BUILDER ===================== -->
<div id="section-portfolio" style="display:none">
<div class="panel">
    <h2>Portfolio Builder</h2>
    <p style="color:var(--warm-gray); margin-bottom:16px; font-size:13px;">Select multiple strategies, set allocation percentages, and see the combined position list with overlap detection.</p>
    <div class="input-group">
        <input type="number" id="portfolio-total" value="100000" min="1000" step="1000" style="width:160px" placeholder="Total Portfolio $">
        <button onclick="buildPortfolio()">Build Portfolio</button>
        <button class="ghost" onclick="clearPortfolio()">Clear</button>
    </div>
    <div class="grid">
        <div class="panel" style="max-height:500px; overflow-y:auto;">
            <h3>Select Strategies</h3>
            <div id="portfolio-strategy-list" class="loading">Loading strategies...</div>
        </div>
        <div>
            <div class="panel" style="margin-bottom:20px;">
                <h3>Allocation Summary</h3>
                <div id="portfolio-alloc-summary">Select strategies to begin.</div>
            </div>
            <div class="panel">
                <h3>Overlap Detection</h3>
                <div id="portfolio-overlap">No strategies selected.</div>
            </div>
        </div>
    </div>
    <div class="panel full" style="margin-top:20px;">
        <h3>Combined Position List</h3>
        <div id="portfolio-positions">Select strategies and click "Build Portfolio" to see combined positions.</div>
    </div>
</div>
</div>

<!-- ===================== TRADE ===================== -->
<div id="section-trade" style="display:none">
<div class="panel">
    <h2>Trade Execution</h2>
    <p style="color:var(--rose); margin-bottom:16px; font-size:12px; padding:12px 16px; background:rgba(248,113,113,0.06); border-radius:var(--radius-sm); border:1px solid rgba(248,113,113,0.12);">
        DISCLAIMER: This is not financial advice. Past performance does not predict future results. Trade at your own risk.
    </p>
    <div class="input-group">
        <select id="trade-strategy" style="flex:2">
            <optgroup label="Top Performers (Sharpe > 1.0)">
                <option value="concentrate_winners">Concentrate Winners (1.11 Sharpe, +818% 10Y)</option>
                <option value="momentum">Momentum (1.08 Sharpe, +570% 10Y)</option>
                <option value="momentum_crash_hedge">Momentum Crash-Hedged (1.05 Sharpe, +743% 10Y)</option>
                <option value="ai_revolution">AI Revolution (0.94 Sharpe, +783% 10Y)</option>
            </optgroup>
            <optgroup label="Portfolio Strategies (hedged)">
                <option value="barbell_portfolio">Barbell Portfolio (2.05 Sharpe 1Y)</option>
                <option value="staples_hedged_growth">Staples-Hedged Growth</option>
                <option value="core_satellite">Core-Satellite (60/40 active)</option>
            </optgroup>
            <optgroup label="Political / Billionaire">
                <option value="nancy_pelosi">Nancy Pelosi (1.39 Sharpe 3Y)</option>
                <option value="bill_ackman">Bill Ackman (1.22 Sharpe 3Y)</option>
                <option value="stanley_druckenmiller">Druckenmiller (1.38 Sharpe 1Y)</option>
            </optgroup>
            <optgroup label="Themes">
                <option value="glp1_obesity">GLP-1 Obesity (0.92 Sharpe 3Y)</option>
                <option value="defense_aerospace">Defense &amp; Aerospace</option>
                <option value="small_cap_value_rotation">Small Cap Value</option>
            </optgroup>
            <optgroup label="Defensive">
                <option value="defensive_rotation">Defensive Rotation (recession hedge)</option>
                <option value="income_shield">Income Shield (high dividend)</option>
            </optgroup>
        </select>
        <input type="number" id="trade-amount" value="100000" min="1000" step="1000" style="width:140px" placeholder="$">
        <button onclick="generateTradePlan()">Generate Plan</button>
        <button class="danger" onclick="executeTrades()">Execute (Live)</button>
    </div>
    <div id="trade-results"></div>
</div>
</div>

</div><!-- /container -->

<div id="status">agents-assemble &middot; 91 strategies &middot; 580 tickers &middot; <span id="status-time"></span></div>

<script>
function esc(s) {
    const d = document.createElement('div');
    d.appendChild(document.createTextNode(s));
    return d.innerHTML;
}
function jesc(s) {
    return String(s).replace(/\\\\/g, '\\\\\\\\').replace(/'/g, "\\\\'");
}
function fetchJSON(url, opts) {
    return fetch(url, opts).then(r => r.json().then(d => {
        if (!r.ok) throw new Error(d.error || 'Server error ' + r.status);
        return d;
    }, () => { throw new Error('Server error ' + r.status); }));
}
function showSection(name, el) {
    document.querySelectorAll('[id^="section-"]').forEach(s => s.style.display = 'none');
    const sec = document.getElementById('section-' + name);
    if (sec) { sec.style.display = 'block'; sec.style.animation = 'none'; sec.offsetHeight; sec.style.animation = ''; }
    document.querySelectorAll('.nav a').forEach(a => a.classList.remove('active'));
    if (el) el.classList.add('active');
    if (name === 'portfolio' && !portfolioStrategiesLoaded) loadPortfolioStrategies();
    if (name === 'strategies' && !strategiesLoaded) loadStrategies();
}

// Update status time
function updateClock() {
    const now = new Date();
    const el = document.getElementById('status-time');
    if (el) el.textContent = now.toLocaleTimeString();
    const el2 = document.getElementById('market-status-time');
    if (el2) el2.textContent = now.toLocaleDateString('en-US', {weekday:'short', month:'short', day:'numeric'}) + ' ' + now.toLocaleTimeString();
}
setInterval(updateClock, 1000);
updateClock();

// ==================== LEADERBOARD ====================
let leaderboardData = [];
let sortCol = 'return'; let sortAsc = false;

function renderLeaderboard() {
    const sorted = [...leaderboardData].sort((a, b) => {
        const va = a[sortCol] || 0, vb = b[sortCol] || 0;
        return sortAsc ? va - vb : vb - va;
    });
    const caretUp = '<svg width="8" height="5" viewBox="0 0 8 5" style="vertical-align:middle;margin-left:4px;"><path d="M4 0L8 5H0z" fill="currentColor"/></svg>';
    const caretDn = '<svg width="8" height="5" viewBox="0 0 8 5" style="vertical-align:middle;margin-left:4px;"><path d="M4 5L0 0h8z" fill="currentColor"/></svg>';
    const arrow = sortAsc ? caretUp : caretDn;
    const horizon = document.getElementById('horizon-select').value.toUpperCase();
    const cols = [
        {key:'return', label:horizon + ' Return'}, {key:'sharpe', label:'Sharpe'}, {key:'max_dd', label:'Max DD'}
    ];
    let html = '<table><tr><th style="width:40px">#</th><th>Strategy</th><th>Category</th>';
    cols.forEach(c => {
        const active = sortCol === c.key ? ' style="color:var(--gold);cursor:pointer"' : ' style="cursor:pointer"';
        html += '<th' + active + ' onclick="sortLeaderboard(\'' + c.key + '\')">' + c.label + (sortCol === c.key ? ' ' + arrow : '') + '</th>';
    });
    html += '<th style="width:80px"></th></tr>';
    sorted.forEach((s, i) => {
        const ret = s.return || 0, sharpe = s.sharpe || 0, max_dd = s.max_dd || 0;
        const retClass = ret > 0 ? 'positive' : 'negative';
        html += '<tr><td style="color:var(--warm-gray)">' + (i+1) + '</td>'
            + '<td style="font-family:var(--font);font-weight:500;font-size:13px;"><a href="#" onclick="openStrategyDetail(\'' + esc(jesc(s.name)) + '\');return false;">' + esc(s.name) + '</a></td>'
            + '<td><span class="tag tag-blue">' + esc(s.source) + '</span></td>'
            + '<td class="' + retClass + '">' + (ret*100).toFixed(1) + '%</td>'
            + '<td>' + sharpe.toFixed(2) + '</td>'
            + '<td class="negative">' + (max_dd*100).toFixed(1) + '%</td>'
            + '<td><button class="ghost" onclick="openStrategyDetail(\'' + esc(jesc(s.name)) + '\')" style="padding:4px 12px;font-size:11px;">View</button></td></tr>';
    });
    html += '</table>';
    document.getElementById('leaderboard-table').innerHTML = html;
}
function sortLeaderboard(col) {
    if (sortCol === col) sortAsc = !sortAsc; else { sortCol = col; sortAsc = false; }
    renderLeaderboard();
}

function loadLeaderboard() {
    const horizon = document.getElementById('horizon-select').value;
    document.getElementById('leaderboard-status').textContent = 'Loading ' + horizon + '...';
    document.getElementById('leaderboard-table').innerHTML = '<p class="loading">Loading strategies for ' + horizon + '...</p>';
    fetchJSON('/api/leaderboard?horizon=' + horizon).then(data => {
        leaderboardData = data;
        document.getElementById('leaderboard-status').textContent = data.length + ' strategies loaded';
        renderLeaderboard();
    }).catch(e => {
        document.getElementById('leaderboard-status').textContent = '';
        document.getElementById('leaderboard-table').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}
loadLeaderboard();

// ==================== MARKET OVERVIEW + PILLS ====================
let marketData = {};
function loadMarket() {
    fetchJSON('/api/market').then(data => {
        marketData = data;
        let html = '<table><tr><th>Index</th><th>Price</th><th>20D Change</th><th>Trend</th></tr>';
        Object.entries(data).forEach(([sym, info]) => {
            const cls = info.change >= 0 ? 'positive' : 'negative';
            const trendArrow = info.change >= 0 ? '<span class="positive">Bullish</span>' : '<span class="negative">Bearish</span>';
            html += '<tr><td style="font-family:var(--font);font-weight:500;">' + sym + '</td><td>$' + info.price.toFixed(2) + '</td>'
                + '<td class="' + cls + '">' + (info.change >= 0 ? '+' : '') + (info.change*100).toFixed(1) + '%</td>'
                + '<td>' + trendArrow + '</td></tr>';
        });
        html += '</table>';
        document.getElementById('market-overview').innerHTML = html;

        let pills = '';
        const nameMap = {SPY: 'S&P 500', QQQ: 'Nasdaq', IWM: 'Russell', TLT: 'Bonds', GLD: 'Gold'};
        Object.entries(data).forEach(([sym, info]) => {
            const arrow = info.change >= 0 ? '<span class="arrow-up">&#9650;</span>' : '<span class="arrow-down">&#9660;</span>';
            const cls = info.change >= 0 ? 'positive' : 'negative';
            pills += '<span class="market-pill">' + arrow + ' <b>' + (nameMap[sym] || sym) + '</b> '
                + '<span class="' + cls + '" style="font-family:var(--mono)">' + (info.change >= 0 ? '+' : '') + (info.change*100).toFixed(1) + '%</span></span>';
        });

        const spy = data.SPY, iwm = data.IWM;
        if (spy && spy.change < -0.02 && iwm && iwm.change < -0.02) {
            pills += '<span class="market-pill" style="border-color:rgba(248,113,113,0.3);"><span class="arrow-down">!!</span> <b style="color:var(--rose);">RISK OFF</b></span>';
        } else if (spy && spy.change > 0.02) {
            pills += '<span class="market-pill" style="border-color:rgba(52,211,153,0.3);"><span class="arrow-up">&#9650;</span> <b style="color:var(--emerald);">RISK ON</b></span>';
        }
        document.getElementById('market-pills').innerHTML = pills;
    }).catch(e => {
        document.getElementById('market-overview').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}
loadMarket();

// ==================== TOP PICKS ====================
let topPicksView = 'active';
let topPicksData = [];

function setTopPicksView(view, btn) {
    topPicksView = view;
    btn.parentElement.querySelectorAll('button').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderTopPicks();
}

function loadTopPicks() {
    document.getElementById('top-picks-list').innerHTML = '<p class="loading">Loading top picks...</p>';
    fetchJSON('/api/top-picks').then(data => {
        topPicksData = data;
        renderTopPicks();
    }).catch(e => {
        document.getElementById('top-picks-list').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

function renderTopPicks() {
    if (!topPicksData || !topPicksData.length) {
        document.getElementById('top-picks-list').innerHTML = '<p class="loading">No data yet.</p>';
        return;
    }
    const picks = topPicksView === 'passive'
        ? topPicksData.filter(p => (p.rebalance === 'monthly' || p.rebalance === 'quarterly') && (p.sharpe||0) > 0.5).slice(0, 5)
        : topPicksData.slice(0, 5);

    let html = '<div class="top-picks-scroll">';
    picks.forEach((p, i) => {
        const ret = p.total_return || 0;
        const retClass = ret > 0 ? 'positive' : 'negative';
        const posCount = (p.positions || []).length;
        const topSyms = (p.positions || []).slice(0, 3).map(pos => pos.symbol).join(', ');
        html += '<div class="top-pick-card" onclick="openStrategyDetail(\'' + esc(jesc(p.name)) + '\')">'
            + '<div class="top-pick-rank">No. ' + (i+1) + '</div>'
            + '<div class="top-pick-info">'
            + '<div class="name">' + esc(p.name) + '</div>'
            + '<div class="meta"><span class="tag tag-blue" style="margin-right:4px;">' + esc(p.source || '') + '</span>' + posCount + ' positions</div>';
        if (topSyms) html += '<div class="meta" style="margin-top:2px;">' + esc(topSyms) + '</div>';
        if (topPicksView === 'passive' && p.execution_guidance) {
            html += '<div class="meta" style="color:var(--gold);margin-top:2px;">' + esc(p.execution_guidance.timing || '') + '</div>';
        }
        html += '</div>'
            + '<div class="top-pick-stats">'
            + '<div class="ret ' + retClass + '">' + (ret > 0 ? '+' : '') + ret.toFixed(1) + '%</div>'
            + '<div class="sharpe">Sharpe ' + (p.sharpe || 0).toFixed(2) + '</div>';
        if (topPicksView === 'passive' && p.risk_parameters) {
            html += '<div class="sharpe" style="color:var(--rose);">Max DD ' + esc(p.risk_parameters.max_drawdown_tolerance || '?') + '</div>';
        }
        html += '</div></div>';
    });
    html += '</div>';

    if (topPicksView === 'passive') {
        html += '<p style="color:var(--warm-gray); font-size:11px; margin-top:8px;">Passive view: monthly/quarterly rebalance strategies with Sharpe > 0.5.</p>';
    }

    document.getElementById('top-picks-list').innerHTML = html;
}
loadTopPicks();

// ==================== STRATEGY DETAIL PANEL ====================
function openStrategyDetail(strategyName) {
    const modal = document.getElementById('strategy-modal');
    const body = document.getElementById('strategy-modal-body');
    body.innerHTML = '<p class="loading">Loading details for ' + esc(strategyName) + '...</p>';
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';

    fetchJSON('/api/strategy-detail/' + encodeURIComponent(strategyName)).then(data => {
        let html = '<h2 style="font-weight:300; font-size:24px; color:var(--warm-white); margin-bottom:4px; margin-right:48px;">' + esc(data.name || strategyName) + '</h2>';
        html += '<p style="color:var(--warm-gray); font-size:13px; margin-bottom:20px;">' + esc(data.source || '') + '</p>';
        html += '<div class="modal-divider"></div>';

        if (data.metrics) {
            html += '<div class="grid-3" style="margin-bottom:20px;">';
            const m = data.metrics;
            const ret = parseFloat(m.total_return) || 0;
            html += '<div class="panel"><h3>Performance</h3>'
                + '<p style="font-family:var(--font)"><b>Return:</b> <span class="' + (ret > 0 ? 'positive' : 'negative') + '" style="font-family:var(--mono)">' + esc(m.total_return || '?') + '</span></p>'
                + '<p style="font-family:var(--font)"><b>Sharpe:</b> <span style="font-family:var(--mono)">' + esc(m.sharpe_ratio || '?') + '</span></p>'
                + '<p style="font-family:var(--font)"><b>Win Rate:</b> <span style="font-family:var(--mono)">' + esc(m.win_rate || '?') + '</span></p>'
                + '<p style="font-family:var(--font)"><b>Alpha:</b> <span style="font-family:var(--mono)">' + esc(m.alpha || '?') + '</span></p></div>';
            html += '<div class="panel"><h3>Risk</h3>'
                + '<p style="font-family:var(--font)"><b>Max DD:</b> <span class="negative" style="font-family:var(--mono)">' + esc(m.max_drawdown || '?') + '</span></p>';
            if (data.risk_parameters) {
                const rp = data.risk_parameters;
                html += '<p style="font-family:var(--font)"><b>Stop Loss:</b> <span style="font-family:var(--mono)">' + esc(rp.stop_loss || '?') + '</span></p>'
                    + '<p style="font-family:var(--font)"><b>Take Profit:</b> <span style="font-family:var(--mono)">' + esc(rp.take_profit_target || '?') + '</span></p>'
                    + '<p style="font-family:var(--font)"><b>Rebalance:</b> ' + esc(rp.rebalance_frequency || '?') + '</p>';
            }
            html += '</div>';
            html += '<div class="panel"><h3>Execution</h3>';
            if (data.execution_guidance) {
                const eg = data.execution_guidance;
                html += '<p style="font-family:var(--font)"><b>Order Type:</b> ' + esc(eg.order_type || '?') + '</p>'
                    + '<p style="font-family:var(--font)"><b>Timing:</b> ' + esc(eg.timing || '?') + '</p>'
                    + '<p style="font-family:var(--font)"><b>Scaling:</b> ' + esc(eg.scaling || '?') + '</p>';
            } else {
                html += '<p style="color:var(--warm-gray);">No execution guidance available.</p>';
            }
            html += '</div></div>';
        }

        if (data.overall_assessment) {
            html += '<div class="panel" style="margin-bottom:20px; border-color:rgba(212,175,55,0.15);">'
                + '<h3>Assessment</h3><p style="font-family:var(--font);line-height:1.7;">' + esc(data.overall_assessment) + '</p></div>';
        }

        if (data.positions && data.positions.length > 0) {
            html += '<div class="panel" style="margin-bottom:20px;">';
            html += '<h3>Current Positions (' + data.positions.length + ')</h3>';
            html += '<div style="overflow-x:auto;"><table><tr><th>Symbol</th><th>Action</th><th>Volatility</th><th>Entry Rule</th><th>Stop Loss</th><th>Take Profit</th><th>Size</th></tr>';
            data.positions.forEach(p => {
                const actionClass = p.action === 'BUY' ? 'tag-green' : p.action === 'HOLD' ? 'tag-yellow' : 'tag-red';
                html += '<tr><td style="font-weight:500">' + esc(p.symbol || '') + '</td>'
                    + '<td><span class="tag ' + actionClass + '">' + esc(p.action || '') + '</span></td>'
                    + '<td>' + esc(p.annual_volatility || '') + '</td>'
                    + '<td style="font-size:11px;font-family:var(--font);">' + esc(p.entry_rule || '') + '</td>'
                    + '<td class="negative">' + esc(p.stop_loss || '') + '</td>'
                    + '<td class="positive">' + esc(p.take_profit || '') + '</td>'
                    + '<td style="font-weight:600">' + esc(p.position_size || '') + '</td></tr>';
            });
            html += '</table></div></div>';
        }

        if (data.rolling_returns && data.rolling_returns.length > 0) {
            html += '<div class="panel" style="margin-bottom:20px;">';
            html += '<h3>Rolling Monthly Returns</h3>';
            const bars = data.rolling_returns.map(r => {
                const v = parseFloat(r) || 0;
                if (v > 5) return '<span class="positive">&#9608;</span>';
                if (v > 2) return '<span class="positive">&#9607;</span>';
                if (v > 0) return '<span class="positive">&#9605;</span>';
                if (v > -2) return '<span class="negative">&#9604;</span>';
                if (v > -5) return '<span class="negative">&#9603;</span>';
                return '<span class="negative">&#9601;</span>';
            }).join('');
            html += '<div class="sparkline" style="font-size:14px; letter-spacing:2px;">' + bars + '</div>';
            html += '<p style="color:var(--warm-gray); font-size:11px; margin-top:6px;">Each bar = 1 month. Green = positive, Red = negative.</p>';
            html += '</div>';
        }

        html += '<div class="modal-divider"></div>';
        html += '<div style="display:flex; gap:10px; margin-top:16px;">';
        html += '<button onclick="closeStrategyModal(); showSection(\'trade\', document.querySelector(\'[onclick*=trade]\'));">Generate Trade Plan</button>';
        html += '<button class="ghost" onclick="closeStrategyModal();">Close</button>';
        html += '</div>';

        body.innerHTML = html;
    }).catch(e => {
        body.innerHTML = '<p class="negative">Error loading strategy: ' + esc(String(e)) + '</p><button class="ghost" onclick="closeStrategyModal()" style="margin-top:12px;">Close</button>';
    });
}

function closeStrategyModal() {
    document.getElementById('strategy-modal').classList.remove('active');
    document.body.style.overflow = '';
}

// ==================== QUICK SCAN ====================
function scanTicker() {
    const sym = document.getElementById('scan-ticker').value.trim().toUpperCase();
    if (!sym) { document.getElementById('scan-results').innerHTML = '<p class="negative">Enter a ticker symbol.</p>'; return; }
    document.getElementById('scan-results').innerHTML = '<p class="loading">Scanning ' + esc(sym) + '...</p>';
    fetchJSON('/api/scan/' + encodeURIComponent(sym)).then(data => {
        let html = '<h3 style="color:var(--warm-white); font-size:15px; margin-bottom:8px;">' + sym + '</h3>';
        if (data.industry) html += '<p style="color:var(--warm-gray);font-size:12px;margin-bottom:8px;">' + esc(data.industry) + '</p>';
        if (data.best) {
            html += '<p><span class="tag tag-green">' + esc(data.best.strategy || '') + '</span> '
                + '<span style="font-family:var(--mono)">Win: ' + (data.best.win_rate*100).toFixed(0) + '%</span> '
                + '<span class="positive" style="font-family:var(--mono)">' + (data.best.total_return*100).toFixed(1) + '%</span></p>';
        }
        if (data.patterns) {
            html += '<p style="color:var(--warm-gray);font-size:12px;margin-top:4px;">Events: <span style="font-family:var(--mono)">' + data.patterns.total_events + '</span> (' + data.patterns.up_events + ' up / ' + data.patterns.down_events + ' down)</p>';
        }
        document.getElementById('scan-results').innerHTML = html;
    }).catch(e => {
        document.getElementById('scan-results').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

function runCatalyst() {
    const sym = document.getElementById('catalyst-ticker').value.trim().toUpperCase();
    if (!sym) { document.getElementById('catalyst-results').innerHTML = '<p class="negative">Enter a ticker symbol.</p>'; return; }
    document.getElementById('catalyst-results').innerHTML = '<p class="loading">Analyzing ' + esc(sym) + '... (this takes ~30s)</p>';
    fetchJSON('/api/catalyst/' + encodeURIComponent(sym)).then(data => {
        let html = '<h3 style="color:var(--warm-white); font-size:16px; margin-bottom:12px;">' + sym;
        if (data.industry) html += ' <span style="color:var(--warm-gray);font-weight:300;font-size:13px;">&mdash; ' + esc(data.industry) + '</span>';
        html += '</h3>';
        if (data.historical_patterns && data.historical_patterns.total_events) {
            const p = data.historical_patterns;
            html += '<div class="panel" style="margin-bottom:16px;"><h3>Historical Patterns</h3>';
            html += '<p style="font-family:var(--font)">Events: <span style="font-family:var(--mono)">' + p.total_events + '</span> (<span class="positive">' + p.up_events + ' up</span> / <span class="negative">' + p.down_events + ' down</span>)</p>';
            if (p.optimal_sell_after_up) html += '<p style="font-family:var(--font)">Optimal sell (UP): <span class="tag tag-green">' + p.optimal_sell_after_up + '</span></p>';
            if (p.optimal_sell_after_down) html += '<p style="font-family:var(--font)">Optimal sell (DOWN): <span class="tag tag-yellow">' + p.optimal_sell_after_down + '</span></p>';
            html += '</div>';
        }
        if (data.backtests) {
            html += '<div class="panel" style="margin-bottom:16px;"><h3>Backtests</h3>';
            html += '<table><tr><th>Strategy</th><th>Trades</th><th>Win%</th><th>Return</th><th>PF</th></tr>';
            const sorted = Object.entries(data.backtests).sort((a,b) => b[1].total_return - a[1].total_return);
            sorted.slice(0, 10).forEach(([key, bt]) => {
                const cls = bt.total_return > 0 ? 'positive' : 'negative';
                html += '<tr><td style="font-family:var(--font)">' + key + '</td><td>' + bt.total_trades + '</td>'
                    + '<td>' + (bt.win_rate*100).toFixed(0) + '%</td>'
                    + '<td class="' + cls + '">' + (bt.total_return*100).toFixed(1) + '%</td>'
                    + '<td>' + bt.profit_factor.toFixed(1) + '</td></tr>';
            });
            html += '</table></div>';
        }
        if (data.predictions && data.predictions.length > 0) {
            html += '<div class="panel" style="margin-bottom:16px;"><h3>Forward Predictions</h3>';
            data.predictions.forEach(p => {
                html += '<p style="margin:6px 0;"><span class="tag tag-' + (p.confidence === 'high' ? 'green' : p.confidence === 'medium' ? 'yellow' : 'red') + '">'
                    + esc(p.confidence.toUpperCase()) + '</span> <span style="font-family:var(--font)">' + esc(p.recommended_action) + '</span></p>';
            });
            html += '</div>';
        }
        if (data.news && data.news.length > 0) {
            html += '<div class="panel"><h3>Latest News</h3>';
            data.news.slice(0, 8).forEach(n => {
                if (n.title && n.title.length > 5) {
                    html += '<p style="font-size:12px;margin:6px 0;line-height:1.5;font-family:var(--font)"><span class="tag tag-yellow">' + esc(n.catalyst_type || 'news') + '</span> '
                        + '<span style="color:var(--warm-gray);font-family:var(--mono);font-size:11px;">' + esc(n.date || '') + '</span> '
                        + (n.url && /^https?:\/\//i.test(n.url) ? '<a href="' + encodeURI(n.url) + '" target="_blank">' + esc(n.title.substring(0, 80)) + '</a>' : esc(n.title.substring(0, 80)))
                        + '</p>';
                }
            });
            html += '</div>';
        }
        document.getElementById('catalyst-results').innerHTML = html;
    }).catch(e => {
        document.getElementById('catalyst-results').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

function loadChart() {
    const sym = document.getElementById('chart-ticker').value.toUpperCase();
    const start = document.getElementById('chart-start').value;
    document.getElementById('chart-container').innerHTML = '<p class="loading">Generating chart for ' + sym + '...</p>';
    fetchJSON('/api/chart/' + encodeURIComponent(sym) + '?start=' + encodeURIComponent(start)).then(data => {
        if (data.image) {
            document.getElementById('chart-container').innerHTML = '<img class="chart-img" src="data:image/png;base64,' + data.image + '">';
        }
    }).catch(e => {
        document.getElementById('chart-container').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

function generateTradePlan() {
    const strat = document.getElementById('trade-strategy').value;
    const amt = document.getElementById('trade-amount').value;
    document.getElementById('trade-results').innerHTML = '<p class="loading">Generating trade plan for ' + esc(strat) + '...</p>';
    fetchJSON('/api/trade-plan/' + encodeURIComponent(strat) + '?amount=' + encodeURIComponent(amt)).then(data => {
        let html = '<h3 style="font-weight:300; font-size:18px; color:var(--warm-white); margin-bottom:8px;">' + esc(data.strategy || '') + ' <span class="tag tag-yellow">DRY RUN</span></h3>';
        const planAmt = data.amount || 100000;
        html += '<p style="color:var(--warm-gray);font-size:12px;margin-bottom:16px;">Portfolio: <span style="font-family:var(--mono)">$' + planAmt.toLocaleString() + '</span> &middot; Slippage: 10bps &middot; Positions: ' + (data.orders||[]).length + '</p>';
        if (data.orders && data.orders.length > 0) {
            html += '<div class="panel"><div style="overflow-x:auto;"><table><tr><th>Action</th><th>Symbol</th><th>Qty</th><th>Entry</th><th>Limit</th><th>Stop Loss</th><th>Take Profit</th><th>Alloc</th></tr>';
            let totalAlloc = 0;
            data.orders.forEach(o => {
                const limit = (o.price * 0.995).toFixed(2);
                const stopLoss = (o.price * 0.85).toFixed(2);
                const takeProfit = (o.price * 1.10).toFixed(2);
                const alloc = ((o.quantity * o.price / planAmt) * 100).toFixed(1);
                totalAlloc += parseFloat(alloc);
                html += '<tr>'
                    + '<td><span class="tag tag-' + (o.side === 'BUY' ? 'green' : 'red') + '">' + o.side + '</span></td>'
                    + '<td style="font-weight:600">' + o.symbol + '</td>'
                    + '<td>' + o.quantity + '</td>'
                    + '<td>$' + o.price.toFixed(2) + '</td>'
                    + '<td class="positive">$' + limit + '</td>'
                    + '<td class="negative">$' + stopLoss + '</td>'
                    + '<td class="positive">$' + takeProfit + '</td>'
                    + '<td>' + alloc + '%</td></tr>';
            });
            html += '<tr style="border-top:1px solid var(--border)"><td colspan="7" style="font-family:var(--font);font-weight:500;">Total Allocation</td><td style="font-weight:600">' + totalAlloc.toFixed(1) + '%</td></tr>';
            html += '</table></div>';
            html += '<div style="margin-top:16px; display:flex; gap:12px; flex-wrap:wrap;">';
            html += '<span class="tag tag-yellow">Trailing Stop: 12% after 5% gain</span>';
            html += '<span class="tag tag-blue">LIMIT orders at 0.5% below, 3 tranches</span>';
            html += '</div></div>';
        } else {
            html += '<p class="negative">No positions generated -- strategy may not have signals today.</p>';
        }
        document.getElementById('trade-results').innerHTML = html;
    }).catch(e => {
        document.getElementById('trade-results').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

function executeTrades() {
    if (!confirm('LIVE TRADING: This will place REAL orders with REAL money on Public.com.\\n\\nDo you have PUBLIC_API_SECRET set?\\n\\nClick OK to proceed or Cancel to abort.')) return;
    const strat = document.getElementById('trade-strategy').value;
    const amt = document.getElementById('trade-amount').value;
    document.getElementById('trade-results').innerHTML = '<p class="loading" style="color:var(--rose)">Executing live trades for ' + esc(strat) + '...</p>';
    fetchJSON('/api/execute-trade/' + encodeURIComponent(strat), {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({amount: parseFloat(amt)})}).then(data => {
        let html = '<h3 style="color:var(--rose); font-weight:300; font-size:18px;">Execution Result: ' + esc(strat) + '</h3>';
        if (data.error) {
            html += '<p class="negative">' + esc(data.error) + '</p>';
        } else if (data.placed && data.placed.length > 0) {
            html += '<p class="positive" style="margin:8px 0;">' + data.placed.length + ' orders placed</p>';
            html += '<div class="panel"><table><tr><th>Symbol</th><th>Side</th><th>Qty</th><th>Status</th></tr>';
            data.placed.forEach(o => {
                html += '<tr><td style="font-weight:600">' + esc(o.symbol) + '</td><td>' + esc(o.side) + '</td><td>' + o.quantity + '</td><td class="positive">SENT</td></tr>';
            });
            html += '</table></div>';
        } else {
            html += '<p class="negative">No orders were placed -- strategy may not have signals today.</p>';
        }
        document.getElementById('trade-results').innerHTML = html;
    }).catch(e => {
        document.getElementById('trade-results').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

// ==================== STOCKPICK ====================
let pickData = null;
let pickRecs = [];
let pickIdx = 0;
let pickCycleCount = 0;

function shuffleArray(arr) {
    const a = [...arr];
    for (let i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}

function renderPickRecommendation(rec, idx, total) {
    let html = '';
    const ms = rec.matched_strategy;

    html += '<div style="display:flex;align-items:center;gap:10px;margin:16px 0">';
    html += '<button class="ghost" onclick="prevPick()" style="padding:6px 14px">Prev</button>';
    html += '<span style="color:var(--warm-gray);font-size:13px;">Strategy ' + (idx+1) + ' of ' + total + '</span>';
    html += '<button class="ghost" onclick="nextPick()" style="padding:6px 14px">Next</button>';
    html += '<button class="secondary" onclick="rerollPicks()" style="padding:6px 14px">Shuffle</button>';
    html += '</div>';

    if (ms) {
        html += '<div class="panel" style="margin:12px 0; border-color:rgba(212,175,55,0.15)">';
        html += '<h3 style="font-size:16px;color:var(--warm-white);font-weight:300;">Matched Strategy: ' + esc(ms.name) + ' <span class="tag tag-blue">' + esc(ms.source) + '</span></h3>';
        html += '<p style="color:var(--warm-gray-light);margin-top:6px;">' + esc(rec.strategy_explanation || '') + '</p>';
        html += '</div>';
    } else {
        html += '<div class="panel" style="margin:12px 0; border-color:rgba(248,113,113,0.15)">';
        html += '<h3 style="font-size:16px;color:var(--warm-white);font-weight:300;">No Direct Strategy Match</h3>';
        html += '<p style="color:var(--warm-gray-light);margin-top:6px;">' + esc(rec.strategy_explanation || '') + '</p>';
        html += '</div>';
    }

    if (rec.backtest && rec.backtest.metrics) {
        const m = rec.backtest.metrics;
        const ret = m.total_return || 0;
        const sharpe = m.sharpe_ratio || 0;
        const maxdd = m.max_drawdown || 0;
        const alpha = m.alpha || 0;
        const winr = m.win_rate || 0;
        html += '<div class="grid-3" style="margin:12px 0">';
        html += '<div class="panel"><h3>Backtest (' + esc(rec.backtest.horizon) + ')</h3>';
        html += '<p style="font-family:var(--font)"><b>Return:</b> <span class="' + (ret > 0 ? 'positive' : 'negative') + '" style="font-family:var(--mono)">' + (ret*100).toFixed(1) + '%</span></p>';
        html += '<p style="font-family:var(--font)"><b>Sharpe:</b> <span style="font-family:var(--mono)">' + sharpe.toFixed(2) + '</span></p>';
        html += '<p style="font-family:var(--font)"><b>Max DD:</b> <span class="negative" style="font-family:var(--mono)">' + (maxdd*100).toFixed(1) + '%</span></p>';
        html += '</div>';
        html += '<div class="panel"><h3>Alpha & Edge</h3>';
        html += '<p style="font-family:var(--font)"><b>Alpha:</b> <span class="' + (alpha > 0 ? 'positive' : 'negative') + '" style="font-family:var(--mono)">' + (alpha*100).toFixed(1) + '%</span></p>';
        html += '<p style="font-family:var(--font)"><b>Win Rate:</b> <span style="font-family:var(--mono)">' + (winr*100).toFixed(0) + '%</span></p>';
        html += '<p style="font-family:var(--font)"><b>Beta:</b> <span style="font-family:var(--mono)">' + (m.beta || 0).toFixed(2) + '</span></p>';
        html += '</div>';
        html += '<div class="panel"><h3>Hypothesis</h3>';
        html += '<p style="font-size:12px;line-height:1.6;font-family:var(--font)">' + esc(rec.hypothesis || '') + '</p>';
        html += '</div>';
        html += '</div>';
    }

    if (rec.positions && rec.positions.length > 0) {
        html += '<div class="panel" style="margin:12px 0">';
        html += '<h3>Position Recommendations</h3>';
        html += '<p style="color:var(--warm-gray);font-size:12px;margin-bottom:8px;">Each position sized by volatility. Your picks highlighted.</p>';
        html += '<div style="overflow-x:auto;"><table><tr><th></th><th>Symbol</th><th>Action</th><th>Vol</th><th>Entry Rule</th><th>Stop Loss</th><th>Take Profit</th><th>Size</th><th>$ Amount</th><th>Links</th></tr>';
        rec.positions.forEach(p => {
            const rowStyle = p.is_user_pick ? ' style="background:rgba(52,211,153,0.04)"' : '';
            const pickTag = p.is_user_pick ? '<span class="tag tag-green">YOUR PICK</span>' : '<span class="tag tag-yellow">SUGGESTED</span>';
            const actionClass = p.action === 'BUY' ? 'tag-green' : p.action === 'HOLD' ? 'tag-yellow' : p.action === 'WATCH' ? 'tag-blue' : 'tag-red';
            const tvOk = p.tradingview_url && /^https?:\/\//i.test(p.tradingview_url);
            const yfOk = p.yahoo_url && /^https?:\/\//i.test(p.yahoo_url);
            const links = (tvOk ? '<a href="' + encodeURI(p.tradingview_url) + '" target="_blank">TV</a>' : '')
                + (yfOk ? ' <a href="' + encodeURI(p.yahoo_url) + '" target="_blank">YF</a>' : '');
            html += '<tr' + rowStyle + '>'
                + '<td>' + pickTag + '</td>'
                + '<td style="font-weight:600">' + esc(p.symbol) + '</td>'
                + '<td><span class="tag ' + actionClass + '">' + esc(p.action) + '</span></td>'
                + '<td>' + esc(p.annual_volatility) + '</td>'
                + '<td style="font-size:11px;font-family:var(--font)">' + esc(p.entry_rule) + '</td>'
                + '<td class="negative">' + esc(p.stop_loss) + '</td>'
                + '<td class="positive">' + esc(p.take_profit) + '</td>'
                + '<td style="font-weight:600">' + esc(p.position_size) + '</td>'
                + '<td>' + esc(p.position_dollars) + '</td>'
                + '<td>' + links + '</td></tr>';
            if (p.note) {
                html += '<tr' + rowStyle + '><td colspan="10" style="font-size:11px;color:var(--gold);padding-left:30px;font-family:var(--font)">' + esc(p.note) + '</td></tr>';
            }
        });
        html += '</table></div></div>';
    }

    if (rec.notes && rec.notes.length > 0) {
        html += '<div class="panel" style="margin:12px 0; border-color:rgba(212,175,55,0.15)">';
        html += '<h3>Notes & Warnings</h3>';
        rec.notes.forEach(n => {
            html += '<p style="color:var(--gold); font-size:12px; margin:4px 0; font-family:var(--font)">' + esc(n) + '</p>';
        });
        html += '</div>';
    }

    if (rec.claude_analysis) {
        html += '<div class="panel" style="margin:12px 0; border-color:rgba(96,165,250,0.15)">';
        html += '<h3 style="color:#60a5fa">Claude AI Analysis</h3>';
        html += '<div style="white-space:pre-wrap; font-size:13px; line-height:1.7; font-family:var(--font); color:var(--warm-gray-light)">' + esc(rec.claude_analysis) + '</div>';
        html += '</div>';
    }

    return html;
}

function showPickResult() {
    if (!pickData || !pickRecs.length) return;
    let html = '';
    if (pickData.invalid_picks && pickData.invalid_picks.length > 0) {
        html += '<p class="negative" style="font-size:12px;margin-bottom:8px;">Could not find data for: ' + esc(pickData.invalid_picks.join(', ')) + '</p>';
    }
    html += '<p style="color:var(--warm-gray);font-size:12px;">' + pickData.total_strategies_matched + ' strategies matched your picks. Showing top ' + pickRecs.length + '.</p>';
    html += renderPickRecommendation(pickRecs[pickIdx], pickIdx, pickRecs.length);
    html += '<p style="color:var(--warm-gray);font-size:11px;margin-top:16px;">Not financial advice. Past performance does not predict future results.</p>';
    document.getElementById('pick-results').innerHTML = html;
}

function nextPick() {
    pickIdx++;
    if (pickIdx >= pickRecs.length) { pickIdx = 0; pickCycleCount++; }
    showPickResult();
}

function prevPick() {
    pickIdx--;
    if (pickIdx < 0) pickIdx = pickRecs.length - 1;
    showPickResult();
}

function rerollPicks() {
    pickRecs = shuffleArray(pickRecs);
    pickIdx = 0;
    showPickResult();
}

function setStockGroup(tickers) {
    document.getElementById('pick-symbols').value = tickers;
}

function analyzeStockPick() {
    const syms = document.getElementById('pick-symbols').value.toUpperCase().trim();
    const amt = document.getElementById('pick-amount').value;
    const horizon = document.getElementById('pick-horizon').value;
    if (!syms) { document.getElementById('pick-results').innerHTML = '<p class="negative">Enter at least one ticker.</p>'; return; }

    const loadBar = document.getElementById('pick-loading-bar');
    const progress = document.getElementById('pick-progress');
    const loadText = document.getElementById('pick-loading-text');
    loadBar.style.display = 'block';
    progress.style.width = '0%';
    document.getElementById('pick-results').innerHTML = '';

    let pct = 0;
    const steps = ['Fetching market data...', 'Matching strategies...', 'Running backtests...', 'Analyzing with Claude AI...', 'Building recommendations...'];
    let stepIdx = 0;
    const progressTimer = setInterval(() => {
        pct = Math.min(pct + Math.random() * 8 + 2, 90);
        progress.style.width = pct + '%';
        if (pct > stepIdx * 18 + 10 && stepIdx < steps.length) {
            loadText.textContent = steps[stepIdx];
            stepIdx++;
        }
    }, 800);

    fetchJSON('/api/stock-pick?symbols=' + encodeURIComponent(syms) + '&amount=' + amt + '&horizon=' + horizon + '&top_n=5')
    .then(data => {
        clearInterval(progressTimer);
        progress.style.width = '100%';
        loadText.textContent = 'Complete';
        setTimeout(() => { loadBar.style.display = 'none'; }, 500);

        if (data.error) { document.getElementById('pick-results').innerHTML = '<p class="negative">' + esc(data.error) + '</p>'; return; }
        pickData = data;
        pickRecs = shuffleArray(data.recommendations || []);
        pickIdx = 0;
        pickCycleCount = 0;
        showPickResult();
    }).catch(e => {
        clearInterval(progressTimer);
        loadBar.style.display = 'none';
        document.getElementById('pick-results').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

// ==================== STRATEGIES LIST ====================
let strategiesLoaded = false;
function loadStrategies() {
    document.getElementById('all-strategies').innerHTML = '<p class="loading">Loading...</p>';
    fetchJSON('/api/strategies').then(data => {
        let html = '<table><tr><th>Strategy</th><th>Category</th><th>Universe</th><th>Rebalance</th><th>Risk</th></tr>';
        const filter = document.getElementById('cat-filter').value;
        data.forEach(s => {
            if (filter && s.source !== filter) return;
            html += '<tr><td style="font-family:var(--font);font-weight:500;"><a href="#" onclick="openStrategyDetail(\'' + esc(jesc(s.name)) + '\');return false;">' + esc(s.name) + '</a></td>'
                + '<td><span class="tag tag-blue">' + esc(s.source) + '</span></td>'
                + '<td>' + s.universe_size + '</td>'
                + '<td style="font-family:var(--font)">' + esc(s.rebalance || '?') + '</td>'
                + '<td>' + esc(s.risk || '?') + '</td></tr>';
        });
        html += '</table>';
        document.getElementById('all-strategies').innerHTML = html;
        strategiesLoaded = true;
    }).catch(e => {
        document.getElementById('all-strategies').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}
document.querySelector('[onclick*="strategies"]').addEventListener('click', function() { if (!strategiesLoaded) setTimeout(loadStrategies, 100); });

// ==================== PORTFOLIO BUILDER ====================
let portfolioStrategiesLoaded = false;
let portfolioStrategies = [];
let selectedStrategies = {};

function loadPortfolioStrategies() {
    const el = document.getElementById('portfolio-strategy-list');
    el.innerHTML = '<p class="loading">Loading strategies...</p>';
    fetchJSON('/api/top-picks').then(data => {
        portfolioStrategies = data;
        portfolioStrategiesLoaded = true;
        let html = '';
        data.forEach(s => {
            const ret = s.total_return || 0;
            const retClass = ret > 0 ? 'positive' : 'negative';
            const checked = selectedStrategies[s.name] ? 'checked' : '';
            html += '<div style="padding:8px 0; border-bottom:1px solid var(--border); display:flex; align-items:center; gap:10px;">'
                + '<input type="checkbox" class="strat-checkbox" id="pf-' + esc(s.name) + '" ' + checked + ' onchange="togglePortfolioStrategy(\'' + esc(jesc(s.name)) + '\', this.checked)">'
                + '<label for="pf-' + esc(s.name) + '" style="flex:1; cursor:pointer; font-family:var(--font);">'
                + '<span style="font-weight:500;">' + esc(s.name) + '</span> <span class="tag tag-blue">' + esc(s.source || '') + '</span>'
                + ' <span class="' + retClass + '" style="font-family:var(--mono);font-size:12px;">' + (ret > 0 ? '+' : '') + ret.toFixed(1) + '%</span>'
                + ' <span style="color:var(--warm-gray);font-size:12px;font-family:var(--mono);">Sharpe ' + (s.sharpe || 0).toFixed(2) + '</span>'
                + '</label>'
                + '<input type="number" class="alloc-input" id="alloc-' + esc(s.name) + '" value="' + (selectedStrategies[s.name] ? selectedStrategies[s.name].alloc : 10) + '" min="1" max="100" onchange="updatePortfolioAlloc(\'' + esc(jesc(s.name)) + '\', this.value)">'
                + '<span style="color:var(--warm-gray); font-size:12px;">%</span>'
                + '</div>';
        });
        el.innerHTML = html || '<p class="loading">No strategies found.</p>';
    }).catch(e => {
        el.innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

function togglePortfolioStrategy(name, checked) {
    if (checked) {
        const strat = portfolioStrategies.find(s => s.name === name);
        const allocEl = document.getElementById('alloc-' + name);
        selectedStrategies[name] = { alloc: parseInt(allocEl ? allocEl.value : 10) || 10, data: strat };
    } else {
        delete selectedStrategies[name];
    }
    updatePortfolioSummary();
}

function updatePortfolioAlloc(name, value) {
    if (selectedStrategies[name]) {
        selectedStrategies[name].alloc = parseInt(value) || 10;
    }
    updatePortfolioSummary();
}

function updatePortfolioSummary() {
    const summaryEl = document.getElementById('portfolio-alloc-summary');
    const overlapEl = document.getElementById('portfolio-overlap');
    const names = Object.keys(selectedStrategies);
    if (names.length === 0) {
        summaryEl.innerHTML = '<p style="color:var(--warm-gray)">Select strategies to begin.</p>';
        overlapEl.innerHTML = '<p style="color:var(--warm-gray)">No strategies selected.</p>';
        return;
    }
    const totalAlloc = names.reduce((sum, n) => sum + selectedStrategies[n].alloc, 0);
    let html = '<table><tr><th>Strategy</th><th>Alloc %</th><th>Normalized</th></tr>';
    names.forEach(n => {
        const raw = selectedStrategies[n].alloc;
        const norm = totalAlloc > 0 ? (raw / totalAlloc * 100).toFixed(1) : '0';
        html += '<tr><td style="font-family:var(--font)">' + esc(n) + '</td><td>' + raw + '%</td><td>' + norm + '%</td></tr>';
    });
    html += '<tr style="border-top:1px solid var(--border);"><td style="font-family:var(--font);font-weight:500;">Total</td><td style="font-weight:600">' + totalAlloc + '%</td><td style="font-weight:600">100%</td></tr>';
    html += '</table>';
    if (totalAlloc !== 100) {
        html += '<p style="color:var(--gold); font-size:12px; margin-top:8px;">Allocations will be normalized to 100% when building.</p>';
    }
    summaryEl.innerHTML = html;

    const symbolMap = {};
    names.forEach(n => {
        const positions = (selectedStrategies[n].data && selectedStrategies[n].data.positions) || [];
        positions.forEach(p => {
            if (!symbolMap[p.symbol]) symbolMap[p.symbol] = [];
            symbolMap[p.symbol].push(n);
        });
    });
    const overlaps = Object.entries(symbolMap).filter(([sym, strats]) => strats.length > 1);
    if (overlaps.length > 0) {
        let ohtml = '<table><tr><th>Symbol</th><th>Strategies</th></tr>';
        overlaps.forEach(([sym, strats]) => {
            ohtml += '<tr><td style="font-weight:600">' + esc(sym) + '</td><td>';
            strats.forEach(s => { ohtml += '<span class="overlap-badge">' + esc(s) + '</span> '; });
            ohtml += '</td></tr>';
        });
        ohtml += '</table>';
        ohtml += '<p style="color:var(--gold); font-size:12px; margin-top:8px;">' + overlaps.length + ' symbols appear in multiple strategies.</p>';
        overlapEl.innerHTML = ohtml;
    } else {
        overlapEl.innerHTML = '<p class="positive">No overlap detected. Good diversification.</p>';
    }
}

function buildPortfolio() {
    const names = Object.keys(selectedStrategies);
    if (names.length === 0) {
        document.getElementById('portfolio-positions').innerHTML = '<p class="negative">Select at least one strategy.</p>';
        return;
    }
    const totalAmount = parseFloat(document.getElementById('portfolio-total').value) || 100000;
    const totalAlloc = names.reduce((sum, n) => sum + selectedStrategies[n].alloc, 0);
    if (totalAlloc <= 0) {
        document.getElementById('portfolio-positions').innerHTML = '<p class="negative">All allocations are zero. Set allocation percentages above 0.</p>';
        return;
    }

    const combined = {};
    names.forEach(n => {
        const normFactor = (selectedStrategies[n].alloc / totalAlloc);
        const positions = (selectedStrategies[n].data && selectedStrategies[n].data.positions) || [];
        positions.forEach(p => {
            const sizePct = parseFloat(p.position_size) || 3;
            const dollarAlloc = totalAmount * normFactor * (sizePct / 100);
            if (!combined[p.symbol]) {
                combined[p.symbol] = {
                    symbol: p.symbol,
                    action: p.action || 'BUY',
                    totalDollars: 0,
                    strategies: [],
                    volatility: p.annual_volatility || '?',
                    stop_loss: p.stop_loss || '?',
                    take_profit: p.take_profit || '?',
                };
            }
            combined[p.symbol].totalDollars += dollarAlloc;
            combined[p.symbol].strategies.push(n);
        });
    });

    const positions = Object.values(combined).sort((a, b) => b.totalDollars - a.totalDollars);

    let html = '<p style="color:var(--warm-gray); font-size:12px; margin-bottom:12px;">Total portfolio: <span style="font-family:var(--mono)">$' + totalAmount.toLocaleString() + '</span> across ' + names.length + ' strategies, ' + positions.length + ' unique positions.</p>';
    html += '<div style="overflow-x:auto;"><table><tr><th>Symbol</th><th>Action</th><th>$ Amount</th><th>% of Portfolio</th><th>Volatility</th><th>Stop Loss</th><th>Take Profit</th><th>From Strategies</th></tr>';
    positions.forEach(p => {
        const pct = (p.totalDollars / totalAmount * 100).toFixed(1);
        const isOverlap = p.strategies.length > 1;
        const rowStyle = isOverlap ? ' style="background:rgba(212,175,55,0.03);"' : '';
        html += '<tr' + rowStyle + '><td style="font-weight:600">' + esc(p.symbol) + '</td>'
            + '<td><span class="tag tag-green">' + esc(p.action) + '</span></td>'
            + '<td>$' + Math.round(p.totalDollars).toLocaleString() + '</td>'
            + '<td>' + pct + '%</td>'
            + '<td>' + esc(p.volatility) + '</td>'
            + '<td class="negative">' + esc(p.stop_loss) + '</td>'
            + '<td class="positive">' + esc(p.take_profit) + '</td>'
            + '<td>';
        p.strategies.forEach(s => { html += '<span class="tag tag-blue" style="font-size:10px;">' + esc(s) + '</span> '; });
        html += '</td></tr>';
    });
    html += '</table></div>';
    document.getElementById('portfolio-positions').innerHTML = html;
}

function clearPortfolio() {
    selectedStrategies = {};
    document.querySelectorAll('.strat-checkbox').forEach(cb => { cb.checked = false; });
    updatePortfolioSummary();
    document.getElementById('portfolio-positions').innerHTML = '<p style="color:var(--warm-gray)">Select strategies and click "Build Portfolio" to see combined positions.</p>';
}

// ==================== KEYBOARD SHORTCUTS ====================
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeStrategyModal();
    }
});
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return HTML

_leaderboard_cache = {}  # {horizon: (timestamp, results)}
_CACHE_TTL_FILE = 300   # 5 min for file-based (3y)
_CACHE_TTL_COMPUTED = 1800  # 30 min for backtested horizons

@app.route("/api/leaderboard")
def api_leaderboard():
    """Return leaderboard. Uses cache, falls back to results/ files for 3y."""
    horizon = request.args.get("horizon", "3y")

    if horizon in _leaderboard_cache:
        cached_at, cached_data = _leaderboard_cache[horizon]
        ttl = _CACHE_TTL_FILE if horizon == "3y" else _CACHE_TTL_COMPUTED
        if time.monotonic() - cached_at < ttl:
            return jsonify(cached_data)

    # For 3y, read from existing results/ files (instant)
    if horizon == "3y":
        results_dir = Path(__file__).parent / "results"
        if not results_dir.is_dir():
            _leaderboard_cache[horizon] = (time.monotonic(), [])
            return jsonify([])
        results = []
        for f in sorted(results_dir.glob("*.json"), key=_mtime):
            try:
                data = json.loads(f.read_text())
                metrics = data.get("metrics", data)
                name = _DATE_SUFFIX_RE.sub('', f.stem)
                if not name:
                    continue
                ret = metrics.get("total_return", 0)
                if isinstance(ret, (int, float)) and not isinstance(ret, bool):
                    source = data.get("source", data.get("category", "backtest"))
                    results.append({
                        "name": name, "source": source,
                        "return": _safe_metric(ret),
                        "sharpe": _safe_metric(metrics.get("sharpe_ratio", 0), 2),
                        "max_dd": _safe_metric(metrics.get("max_drawdown", 0)),
                    })
            except Exception:
                pass
        seen = {}
        for r in results:
            seen[r["name"]] = r
        results = sorted(seen.values(), key=lambda x: x["return"], reverse=True)[:30]
        results = _sanitize_for_json(results)
        _leaderboard_cache[horizon] = (time.monotonic(), results)
        return jsonify(results)

    # For other horizons, run backtests (slower but cached after first load)
    from run_multi_horizon import run_single, _get_all_strategies, ALL_HORIZONS
    h_map = ALL_HORIZONS
    if horizon not in h_map:
        return jsonify({"error": f"Invalid horizon: {horizon}"}), 400
    start, end = h_map[horizon]
    results = []
    for s in _get_all_strategies():
        try:
            r = run_single(s, horizon, start, end, verbose=False)
            if r["status"] == "success":
                m = r["metrics"]
                results.append({
                    "name": s["key"], "source": s["source"],
                    "return": _safe_metric(m.get("total_return", 0)),
                    "sharpe": _safe_metric(m.get("sharpe_ratio", 0), 2),
                    "max_dd": _safe_metric(m.get("max_drawdown", 0)),
                })
        except Exception:
            continue
    seen = {}
    for r in results:
        seen[r["name"]] = r
    results = sorted(seen.values(), key=lambda x: x["return"], reverse=True)
    results = _sanitize_for_json(results[:30])
    _leaderboard_cache[horizon] = (time.monotonic(), results)
    return jsonify(results)

_strategies_cache = {}  # {"data": [...], "ts": monotonic_time}
_CACHE_TTL_STRATEGIES = 600  # 10 min — strategy metadata doesn't change at runtime

@app.route("/api/strategies")
def api_strategies():
    """List all strategies with metadata — no backtesting, instant response."""
    if _strategies_cache and time.monotonic() - _strategies_cache.get("ts", 0) < _CACHE_TTL_STRATEGIES:
        return jsonify(_strategies_cache["data"])
    from run_multi_horizon import _get_all_strategies
    results = []
    for s in _get_all_strategies():
        try:
            persona = s["getter"](s["key"])
            results.append({
                "name": s["key"],
                "source": s["source"],
                "display_name": persona.config.name,
                "description": persona.config.description,
                "universe_size": len(persona.config.universe),
                "rebalance": persona.config.rebalance_frequency,
                "risk": f"{persona.config.risk_tolerance:.0%}",
            })
        except Exception:
            results.append({"name": s["key"], "source": s["source"],
                            "universe_size": 0, "rebalance": "?", "risk": "?"})
    _strategies_cache["data"] = results
    _strategies_cache["ts"] = time.monotonic()
    return jsonify(results)

_market_cache = {}  # {"data": {...}, "ts": monotonic_time}
_CACHE_TTL_MARKET = 60  # 60s — market data doesn't change between page loads

@app.route("/api/market")
def api_market():
    if _market_cache and time.monotonic() - _market_cache.get("ts", 0) < _CACHE_TTL_MARKET:
        return jsonify(_market_cache["data"])
    from data_fetcher import fetch_multiple_ohlcv
    indices = {"SPY": "S&P 500", "QQQ": "Nasdaq", "IWM": "Russell 2000",
               "TLT": "Bonds 20Y", "GLD": "Gold"}
    start = str(date.today() - timedelta(days=60))
    try:
        all_dfs = fetch_multiple_ohlcv(list(indices.keys()), start=start)
    except Exception:
        all_dfs = {}
    data = {}
    for sym in indices:
        try:
            df = all_dfs.get(sym)
            if df is None or len(df) <= 1:
                continue
            last = float(df["Close"].iloc[-1])
            ref = float(df["Close"].iloc[-20]) if len(df) > 20 else float(df["Close"].iloc[0])
            change = (last / ref - 1) if ref > 0 else 0
            if last > 0 and math.isfinite(last) and math.isfinite(change):
                data[sym] = {"price": last, "change": change}
        except Exception:
            pass
    if data:
        _market_cache["data"] = data
        _market_cache["ts"] = time.monotonic()
        return jsonify(data)
    elif _market_cache.get("data"):
        return jsonify(_market_cache["data"])
    return jsonify(data)

@app.route("/api/scan/<symbol>")
def api_scan(symbol):
    sym = symbol.strip().upper()
    if not _SYMBOL_RE.match(sym):
        return jsonify({"error": "Invalid symbol"}), 400
    from catalyst_analyzer import CatalystAnalyzer
    try:
        a = CatalystAnalyzer(sym)
        patterns = a.analyze_historical_patterns()
    except Exception as e:
        return jsonify({"error": f"Failed to analyze {sym}: {e}"}), 500
    # Quick mode: 3 strategies at 10d (fast)
    best_entry = None
    try:
        df = a._get_price_data()
        bts = {}
        if len(df) >= 50:
            close_arr = df["Close"].values
            ret_arr = df["daily_return"].values
            vr_arr = df["vol_ratio"].values
            for strat in ['buy_spike', 'buy_dip', 'momentum']:
                try:
                    r = a._run_single_backtest(close_arr, ret_arr, vr_arr, strat, 10)
                    if r.total_trades > 0:
                        bts[f'{strat}_10d'] = r
                except Exception:
                    pass
        valid_bts = {k: v for k, v in bts.items()
                     if isinstance(v.total_return, (int, float)) and not isinstance(v.total_return, bool) and math.isfinite(v.total_return)}
        if valid_bts:
            best_key = max(valid_bts, key=lambda k: valid_bts[k].total_return)
            best_dict = valid_bts[best_key].to_dict()
            best_dict.setdefault("strategy", best_key)
            best_entry = best_dict
    except Exception:
        pass
    return jsonify(_sanitize_for_json({
        "symbol": sym,
        "industry": a.industry,
        "patterns": {k: v for k, v in patterns.items() if k != "events"} if patterns else None,
        "best": best_entry,
    }))

@app.route("/api/catalyst/<symbol>")
def api_catalyst(symbol):
    sym = symbol.strip().upper()
    if not _SYMBOL_RE.match(sym):
        return jsonify({"error": "Invalid symbol"}), 400
    from catalyst_analyzer import CatalystAnalyzer
    try:
        a = CatalystAnalyzer(sym)
        report = a.full_report()
    except Exception as e:
        return jsonify({"error": f"Catalyst analysis failed for {sym}: {e}"}), 500
    return jsonify(_sanitize_for_json(report))

@app.route("/api/chart/<symbol>")
def api_chart(symbol):
    sym = symbol.strip().upper()
    if not _SYMBOL_RE.match(sym):
        return jsonify({"error": "Invalid symbol"}), 400
    from terminal import Terminal
    start = request.args.get("start", "2024-01-01")
    if not _valid_date(start):
        return jsonify({"error": "Invalid start date (expected valid YYYY-MM-DD)"}), 400
    t = Terminal()
    try:
        path = t.equity_chart(sym, start=start)
    except Exception as e:
        return jsonify({"error": f"Chart generation failed for {sym}: {e}"}), 500
    if not path or not Path(path).is_file():
        return jsonify({"error": f"Chart generation failed for {sym}"}), 500
    chart_path = Path(path)
    try:
        img_b64 = base64.b64encode(chart_path.read_bytes()).decode()
    except Exception:
        return jsonify({"error": f"Failed to read chart for {sym}"}), 500
    finally:
        chart_path.unlink(missing_ok=True)
    return jsonify({"image": img_b64})

@app.route("/api/trade-plan/<strategy>")
def api_trade_plan(strategy):
    if not _STRATEGY_RE.match(strategy):
        return jsonify({"error": "Invalid strategy name"}), 400
    from public_trader import PublicTrader
    trader = PublicTrader(dry_run=True)
    try:
        persona = trader._resolve_strategy(strategy)
    except Exception:
        return jsonify({"error": f"Unknown strategy: {strategy}"}), 400
    if persona is None:
        return jsonify({"error": f"Unknown strategy: {strategy}"}), 400
    from data_fetcher import fetch_multiple_ohlcv
    from backtester import _compute_rsi, _compute_bollinger, _compute_atr

    try:
        amount = float(request.args.get("amount", 100000))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount parameter"}), 400
    if amount <= 0 or not math.isfinite(amount):
        return jsonify({"error": "Amount must be a positive number"}), 400
    symbols = persona.config.universe[:15]
    try:
        all_data = fetch_multiple_ohlcv(symbols, start=str(date.today() - timedelta(days=400)))
    except Exception as e:
        return jsonify({"error": f"Failed to fetch market data: {e}"}), 500

    enriched = {}
    prices = {}
    for sym, raw_df in all_data.items():
        if raw_df.empty: continue
        df = raw_df.copy()
        if df.index.tz is not None: df.index = df.index.tz_convert(None)
        close = df["Close"]
        df["sma_50"] = close.rolling(50).mean()
        df["sma_200"] = close.rolling(200).mean()
        df["ema_12"] = close.ewm(span=12).mean()
        df["ema_26"] = close.ewm(span=26).mean()
        df["macd"] = df["ema_12"] - df["ema_26"]
        df["macd_signal"] = df["macd"].ewm(span=9).mean()
        df["rsi_14"] = _compute_rsi(close, 14)
        df["bb_upper"], df["bb_lower"] = _compute_bollinger(close, 20, 2)
        df["daily_return"] = close.pct_change()
        df["vol_20"] = df["daily_return"].rolling(20).std()
        df["volume_sma_20"] = df["Volume"].rolling(20).mean()
        df["sma_20"] = close.rolling(20).mean()
        df["atr_14"] = _compute_atr(df, 14)
        last_close = float(close.iloc[-1])
        if not math.isfinite(last_close) or last_close <= 0:
            continue
        enriched[sym] = df
        prices[sym] = last_close

    if not enriched:
        return jsonify({"error": "No market data available for strategy symbols"}), 500
    from backtester import Portfolio
    portfolio = Portfolio(initial_cash=amount)
    last_dates = [df.index[-1] for df in enriched.values()]
    signal_date = max(last_dates)
    try:
        weights = persona.generate_signals(signal_date, prices, portfolio, enriched)
    except Exception as e:
        return jsonify({"error": f"Strategy signal generation failed: {e}"}), 500
    if not isinstance(weights, dict):
        return jsonify({"strategy": strategy, "orders": [], "amount": amount})

    orders = []
    remaining = amount
    numeric_weights = {s: w for s, w in weights.items()
                       if isinstance(w, (int, float)) and not isinstance(w, bool) and math.isfinite(w)}
    max_pos = persona.config.max_position_size
    capped = {s: w for s, w in numeric_weights.items()
              if w > 0 and s in prices and prices[s] > 0}
    total_w = sum(capped.values())
    if total_w > 1.0:
        capped = {s: w / total_w for s, w in capped.items()}
    capped = {s: min(w, max_pos) for s, w in capped.items()}
    for sym, w in sorted(capped.items(), key=lambda x: -x[1]):
        if remaining <= 0:
            break
        alloc = min(amount * w, remaining)
        qty = int(alloc / prices[sym])
        if qty > 0:
            remaining -= qty * prices[sym]
            orders.append({"side": "BUY", "symbol": sym, "quantity": qty, "price": prices[sym]})

    return jsonify(_sanitize_for_json({"strategy": strategy, "orders": orders, "amount": amount}))


@app.route("/api/stock-pick")
def api_stock_pick():
    """StockPick: Analyze user stock picks, match to strategy, generate recs."""
    raw = request.args.get("symbols", "")
    symbols = [s.strip().upper() for s in raw.split(",") if s.strip()]
    if not symbols:
        return jsonify({"error": "No symbols provided. Enter tickers separated by commas."}), 400
    # Validate each symbol
    for s in symbols:
        if not _SYMBOL_RE.match(s):
            return jsonify({"error": f"Invalid ticker: {s}"}), 400
    if len(symbols) > 20:
        return jsonify({"error": "Maximum 20 tickers at once"}), 400

    try:
        amount = float(request.args.get("amount", 100000))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount parameter"}), 400
    if amount <= 0 or not math.isfinite(amount):
        return jsonify({"error": "Amount must be a positive number"}), 400

    horizon = request.args.get("horizon", "3y")
    if horizon not in ("1y", "3y", "5y"):
        horizon = "3y"

    # Check if Claude is available (don't fail if not)
    include_claude = request.args.get("claude", "1") != "0"

    try:
        top_n = int(request.args.get("top_n", 5))
    except (ValueError, TypeError):
        top_n = 5
    top_n = max(1, min(top_n, 10))

    from stock_picker import analyze_stock_picks
    try:
        result = analyze_stock_picks(
            symbols,
            portfolio_amount=amount,
            horizon=horizon,
            include_claude=include_claude,
            top_n=top_n,
        )
    except Exception as e:
        return jsonify({"error": f"Analysis failed: {str(e)[:200]}"}), 500

    return jsonify(_sanitize_for_json(result))


# ---------------------------------------------------------------------------
# Top Picks & Strategy Detail (Iterations 1-2, 5)
# ---------------------------------------------------------------------------
_top_picks_cache = {}

@app.route("/api/top-picks")
def api_top_picks():
    """Return top strategies with their current positions from winning/ directory."""
    if _top_picks_cache and time.monotonic() - _top_picks_cache.get("ts", 0) < 300:
        return jsonify(_top_picks_cache["data"])

    winning_dir = Path(__file__).parent / "strategy" / "winning"
    if not winning_dir.is_dir():
        return jsonify([])

    # Read all winning strategy JSONs, deduplicate by name (keep newest)
    strategies = {}
    for f in sorted(winning_dir.glob("*.json"), key=_mtime, reverse=True):
        try:
            data = json.loads(f.read_text())
            name = data.get("strategy_name", "")
            if not name or name in strategies:
                continue
            ms = data.get("metrics_summary", {})
            sharpe = ms.get("sharpe_ratio", "0")
            try:
                sharpe_f = float(str(sharpe).replace("%", ""))
            except (ValueError, TypeError):
                sharpe_f = 0
            if not math.isfinite(sharpe_f):
                sharpe_f = 0
            total_return = ms.get("total_return", "0")
            try:
                ret_f = float(str(total_return).replace("%", ""))
            except (ValueError, TypeError):
                ret_f = 0
            if not math.isfinite(ret_f):
                ret_f = 0

            positions = data.get("position_recommendations", [])
            risk_params = data.get("risk_parameters", {})
            exec_guidance = data.get("execution_guidance", {})
            rebalance = risk_params.get("rebalance_frequency", "?")

            strategies[name] = {
                "name": name,
                "source": data.get("source", data.get("category", "unknown")),
                "sharpe": sharpe_f,
                "total_return": ret_f,
                "overall_assessment": data.get("overall_assessment", ""),
                "rebalance": rebalance,
                "risk_parameters": risk_params,
                "execution_guidance": exec_guidance,
                "positions": [
                    {
                        "symbol": p.get("symbol", ""),
                        "action": p.get("action", ""),
                        "position_size": p.get("position_size", ""),
                        "annual_volatility": p.get("annual_volatility", ""),
                        "stop_loss": p.get("stop_loss", ""),
                        "take_profit": p.get("take_profit", ""),
                    }
                    for p in positions[:10]
                ],
            }
        except Exception:
            pass

    # Sort by Sharpe descending
    result = sorted(strategies.values(), key=lambda x: x["sharpe"], reverse=True)
    result = _sanitize_for_json(result[:30])
    _top_picks_cache["data"] = result
    _top_picks_cache["ts"] = time.monotonic()
    return jsonify(result)


@app.route("/api/strategy-detail/<name>")
def api_strategy_detail(name):
    """Return full detail for a strategy by name (from winning/ or losing/)."""
    if not _STRATEGY_RE.match(name):
        return jsonify({"error": "Invalid strategy name"}), 400

    # Search winning/ then losing/
    base = Path(__file__).parent / "strategy"
    found = None
    for subdir in ["winning", "losing"]:
        d = base / subdir
        if not d.is_dir():
            continue
        candidates = sorted(
            [f for f in d.glob(f"{name}*.json")
             if _DATE_SUFFIX_RE.sub('', f.stem) == name],
            key=_mtime, reverse=True)
        if candidates:
            found = candidates[0]
            break

    if not found:
        return jsonify({"error": f"Strategy '{name}' not found"}), 404

    try:
        data = json.loads(found.read_text())
    except Exception as e:
        return jsonify({"error": f"Failed to read strategy: {e}"}), 500

    ms = data.get("metrics_summary", {})
    positions = data.get("position_recommendations", [])
    risk_params = data.get("risk_parameters", {})
    exec_guidance = data.get("execution_guidance", {})

    # Generate rolling return approximation from results/ files if available
    rolling_returns = []
    results_dir = Path(__file__).parent / "results"
    if results_dir.is_dir():
        result_files = sorted(
            [f for f in results_dir.glob(f"{name}*.json")
             if _DATE_SUFFIX_RE.sub('', f.stem) == name],
            key=_mtime, reverse=True)
        if result_files:
            try:
                rdata = json.loads(result_files[0].read_text())
                eq = rdata.get("equity_curve")
                mr = rdata.get("monthly_returns") if eq is None else None
                if isinstance(mr, list) and len(mr) > 0:
                    # monthly_returns are already percentage values — use directly
                    rolling_returns = [round(float(v), 1) for v in mr
                                       if isinstance(v, (int, float)) and not isinstance(v, bool)]
                elif isinstance(eq, list) and len(eq) > 1:
                    # Convert equity curve to approximate monthly returns
                    step = max(1, len(eq) // 12)
                    for i in range(step, len(eq), step):
                        prev = eq[i - step] if isinstance(eq[i - step], (int, float)) and not isinstance(eq[i - step], bool) else 0
                        curr = eq[i] if isinstance(eq[i], (int, float)) and not isinstance(eq[i], bool) else 0
                        if prev > 0:
                            rolling_returns.append(round((curr / prev - 1) * 100, 1))
            except Exception:
                pass

    result = {
        "name": data.get("strategy_name", name),
        "source": data.get("source", data.get("category", "")),
        "is_winning": data.get("is_winning", False),
        "overall_assessment": data.get("overall_assessment", ""),
        "metrics": ms,
        "risk_parameters": risk_params,
        "execution_guidance": exec_guidance,
        "positions": [
            {
                "symbol": p.get("symbol", ""),
                "action": p.get("action", ""),
                "annual_volatility": p.get("annual_volatility", ""),
                "entry_rule": p.get("entry_rule", ""),
                "stop_loss": p.get("stop_loss", ""),
                "take_profit": p.get("take_profit", ""),
                "position_size": p.get("position_size", ""),
                "trailing_stop": p.get("trailing_stop", ""),
            }
            for p in positions
        ],
        "rolling_returns": rolling_returns,
    }
    return jsonify(_sanitize_for_json(result))


@app.route("/api/execute-trade/<strategy>", methods=["POST"])
def api_execute_trade(strategy):
    """LIVE trade execution via Public.com API. Requires PUBLIC_API_SECRET."""
    if not _STRATEGY_RE.match(strategy):
        return jsonify({"error": "Invalid strategy name"}), 400
    import os
    if not os.environ.get("PUBLIC_API_SECRET"):
        return jsonify({"error": "PUBLIC_API_SECRET not set. Go to public.com/settings/security/api to get your key, then: export PUBLIC_API_SECRET=your_key"}), 403

    body = request.get_json(silent=True)
    if not isinstance(body, dict):
        return jsonify({"error": "Request body must be JSON"}), 400
    try:
        amount = float(body.get("amount", 100000))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid amount parameter"}), 400
    if amount <= 0 or not math.isfinite(amount):
        return jsonify({"error": "Amount must be a positive number"}), 400
    from public_trader import PublicTrader
    trader = PublicTrader(dry_run=False)
    try:
        results = trader.execute_strategy(strategy, portfolio_value=amount)
        return jsonify(_sanitize_for_json(results))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("\\n  ⚡ agents-assemble Trading Terminal")
    print("  Open: http://localhost:8888\\n")
    app.run(host="0.0.0.0", port=8888, debug=False)

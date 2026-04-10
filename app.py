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
<html>
<head>
<title>agents-assemble | Trading Terminal</title>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: #0a0a1a; color: #e0e0e0; font-family: 'Courier New', monospace; font-size: 13px; }
a { color: #00ff88; text-decoration: none; }
a:hover { text-decoration: underline; }

/* Top bar */
.topbar { background: #111128; padding: 8px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222; }
.topbar .logo { color: #00ff88; font-size: 16px; font-weight: bold; }
.topbar .nav a { margin-left: 20px; color: #888; font-size: 12px; }
.topbar .nav a.active, .topbar .nav a:hover { color: #00ff88; }

/* Main layout */
.container { max-width: 1400px; margin: 0 auto; padding: 15px; }
.grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }
.grid-3 { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 15px; }
.full { grid-column: 1 / -1; }

/* Panels */
.panel { background: #111128; border: 1px solid #222; border-radius: 6px; padding: 15px; }
.panel h2 { color: #00ff88; font-size: 14px; margin-bottom: 10px; border-bottom: 1px solid #222; padding-bottom: 5px; }
.panel h3 { color: #ffaa00; font-size: 12px; margin: 10px 0 5px; }

/* Tables */
table { width: 100%; border-collapse: collapse; font-size: 12px; }
th { background: #1a1a2e; color: #00ff88; text-align: left; padding: 6px 8px; border-bottom: 1px solid #333; }
td { padding: 5px 8px; border-bottom: 1px solid #1a1a2e; }
tr:hover { background: #1a1a2e; }
.positive { color: #00ff88; }
.negative { color: #ff4444; }

/* Inputs */
input, select, button { background: #1a1a2e; color: #e0e0e0; border: 1px solid #333; padding: 6px 10px; border-radius: 4px; font-family: inherit; font-size: 12px; }
button { background: #00ff88; color: #0a0a1a; cursor: pointer; font-weight: bold; }
button:hover { background: #00cc66; }
button.danger { background: #ff4444; }
.input-group { display: flex; gap: 8px; margin-bottom: 10px; }
.input-group input { flex: 1; }

/* Chart */
.chart-img { width: 100%; border-radius: 4px; }

/* Tags */
.tag { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 10px; margin-right: 4px; }
.tag-green { background: #00ff8822; color: #00ff88; border: 1px solid #00ff8844; }
.tag-red { background: #ff444422; color: #ff4444; border: 1px solid #ff444444; }
.tag-blue { background: #4488ff22; color: #4488ff; border: 1px solid #4488ff44; }
.tag-yellow { background: #ffaa0022; color: #ffaa00; border: 1px solid #ffaa0044; }

/* Loading */
.loading { color: #888; font-style: italic; }
#status { position: fixed; bottom: 10px; right: 10px; background: #111128; border: 1px solid #333; padding: 5px 10px; border-radius: 4px; font-size: 11px; }

/* Quick Actions */
.quick-actions { display: flex; gap: 10px; margin: 10px 0; flex-wrap: wrap; }
.quick-btn { padding: 10px 18px; font-size: 13px; border-radius: 6px; cursor: pointer; transition: all 0.2s; border: 1px solid #333; }
.quick-btn:hover { transform: translateY(-1px); box-shadow: 0 2px 8px rgba(0,255,136,0.2); }
.quick-btn-primary { background: #00ff88; color: #0a0a1a; }
.quick-btn-secondary { background: #1a1a2e; color: #00ff88; border-color: #00ff88; }
.quick-btn-warn { background: #1a1a2e; color: #ffaa00; border-color: #ffaa00; }

/* Market status bar */
.market-bar { display: flex; gap: 12px; flex-wrap: wrap; margin-bottom: 12px; }
.market-pill { display: inline-flex; align-items: center; gap: 6px; padding: 5px 12px; border-radius: 20px; font-size: 12px; border: 1px solid #333; background: #111128; }
.market-pill .arrow-up { color: #00ff88; }
.market-pill .arrow-down { color: #ff4444; }
.market-pill .neutral { color: #888; }
.market-pill .label { color: #888; font-size: 10px; }

/* Top picks card */
.top-pick-card { background: #0d0d22; border: 1px solid #222; border-radius: 6px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; cursor: pointer; transition: border-color 0.2s; }
.top-pick-card:hover { border-color: #00ff88; }
.top-pick-rank { font-size: 18px; font-weight: bold; color: #00ff88; width: 30px; }
.top-pick-info { flex: 1; margin-left: 10px; }
.top-pick-info .name { font-weight: bold; font-size: 13px; }
.top-pick-info .meta { color: #888; font-size: 11px; margin-top: 2px; }
.top-pick-stats { text-align: right; }
.top-pick-stats .ret { font-size: 14px; font-weight: bold; }
.top-pick-stats .sharpe { color: #888; font-size: 11px; }

/* Strategy detail modal */
.modal-overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.7); z-index: 1000; overflow-y: auto; }
.modal-overlay.active { display: block; }
.modal-content { background: #0a0a1a; border: 1px solid #00ff88; border-radius: 8px; max-width: 900px; margin: 40px auto; padding: 20px; position: relative; }
.modal-close { position: absolute; top: 10px; right: 15px; color: #ff4444; cursor: pointer; font-size: 18px; background: none; border: none; }
.modal-close:hover { color: #ff6666; background: none; }

/* Stock group buttons */
.stock-group-btns { display: flex; gap: 6px; flex-wrap: wrap; margin-bottom: 10px; }
.stock-group-btn { padding: 4px 12px; font-size: 11px; border-radius: 20px; cursor: pointer; background: #1a1a2e; color: #4488ff; border: 1px solid #4488ff44; }
.stock-group-btn:hover { background: #4488ff22; color: #4488ff; }

/* Portfolio builder */
.strat-checkbox { margin-right: 6px; accent-color: #00ff88; }
.alloc-input { width: 60px; text-align: center; padding: 3px 6px; }
.overlap-badge { display: inline-block; padding: 1px 6px; border-radius: 3px; font-size: 10px; background: #ffaa0022; color: #ffaa00; border: 1px solid #ffaa0044; }

/* View toggle */
.view-toggle { display: inline-flex; border: 1px solid #333; border-radius: 4px; overflow: hidden; margin-bottom: 10px; }
.view-toggle button { border: none; border-radius: 0; padding: 6px 16px; font-size: 12px; }
.view-toggle button.active { background: #00ff88; color: #0a0a1a; }
.view-toggle button:not(.active) { background: #1a1a2e; color: #888; }
.view-toggle button:not(.active):hover { color: #00ff88; }

/* Sparkline (text-based) */
.sparkline { font-size: 10px; letter-spacing: 1px; color: #00ff88; }

/* Responsive */
@media (max-width: 768px) {
    .grid { grid-template-columns: 1fr; }
    .grid-3 { grid-template-columns: 1fr; }
    .topbar { flex-direction: column; gap: 8px; }
    .topbar .nav { display: flex; flex-wrap: wrap; gap: 4px; }
    .topbar .nav a { margin-left: 0; }
}
</style>
</head>
<body>

<div class="topbar">
    <div class="logo">⚡ agents-assemble</div>
    <div class="nav">
        <a href="#" class="active" onclick="showSection('dashboard', this)">Dashboard</a>
        <a href="#" onclick="showSection('strategies', this)">Strategies</a>
        <a href="#" onclick="showSection('stockpick', this)">StockPick</a>
        <a href="#" onclick="showSection('portfolio', this)">Portfolio</a>
        <a href="#" onclick="showSection('catalyst', this)">Catalyst</a>
        <a href="#" onclick="showSection('charts', this)">Charts</a>
        <a href="#" onclick="showSection('trade', this)">Trade</a>
    </div>
</div>

<div class="container">

<!-- DASHBOARD -->
<div id="section-dashboard">

<!-- Market Status Bar -->
<div class="panel full" style="margin-bottom:15px; padding:10px 15px;">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
        <div style="display:flex; align-items:center; gap:8px;">
            <span style="color:#00ff88; font-weight:bold; font-size:13px;">MARKET STATUS</span>
            <span id="market-status-time" style="color:#555; font-size:11px;"></span>
        </div>
        <div id="market-pills" class="market-bar">
            <span class="market-pill"><span class="label">Loading market data...</span></span>
        </div>
    </div>
</div>

<!-- Quick Actions -->
<div class="panel full" style="margin-bottom:15px;">
    <h2>Quick Actions</h2>
    <div class="quick-actions">
        <button class="quick-btn quick-btn-primary" onclick="showSection('stockpick', document.querySelector('[onclick*=stockpick]'))">Run StockPick (AI Matcher)</button>
        <button class="quick-btn quick-btn-secondary" onclick="document.getElementById('leaderboard-table').scrollIntoView({behavior:'smooth'})">View Leaderboard</button>
        <button class="quick-btn quick-btn-secondary" onclick="showSection('trade', document.querySelector('[onclick*=trade]'))">Generate Trade Plan</button>
        <button class="quick-btn quick-btn-warn" onclick="showSection('catalyst', document.querySelector('[onclick*=catalyst]'))">Catalyst Scanner</button>
        <button class="quick-btn quick-btn-secondary" onclick="loadTopPicks()">Refresh Top Picks</button>
    </div>
</div>

<div class="grid">
    <!-- Today's Top Picks -->
    <div class="panel">
        <h2>TODAY'S TOP PICKS</h2>
        <p style="color:#888; font-size:11px; margin-bottom:10px;">Top 5 strategies with highest Sharpe ratios and their current positions.</p>
        <div class="view-toggle" style="margin-bottom:8px;">
            <button class="active" onclick="setTopPicksView('active', this)">Active</button>
            <button onclick="setTopPicksView('passive', this)">Passive</button>
        </div>
        <div id="top-picks-list" class="loading">Loading top picks...</div>
    </div>

    <!-- Market Overview + Quick Scan -->
    <div>
        <div class="panel" style="margin-bottom:15px;">
            <h2>MARKET OVERVIEW</h2>
            <div id="market-overview" class="loading">Loading...</div>
        </div>
        <div class="panel">
            <h2>QUICK SCAN</h2>
            <div class="input-group">
                <input type="text" id="scan-ticker" placeholder="Ticker (e.g. NVDA)" value="NVDA">
                <button onclick="scanTicker()">Scan</button>
            </div>
            <div id="scan-results"></div>
        </div>
    </div>
</div>

<!-- Leaderboard -->
<div class="panel full" style="margin-top:15px;">
    <h2>STRATEGY LEADERBOARD | Return + Sharpe + Max DD</h2>
    <div class="input-group">
        <select id="horizon-select" onchange="loadLeaderboard()">
            <option value="3y" selected>3Y (2022-2024)</option>
            <option value="1y">1Y (2024)</option>
            <option value="5y">5Y (2020-2024)</option>
        </select>
        <span id="leaderboard-status" style="color:#888;font-size:11px;padding-top:6px"></span>
    </div>
    <div id="leaderboard-table" class="loading">Loading strategies...</div>
</div>
</div>

<!-- Strategy Detail Modal -->
<div id="strategy-modal" class="modal-overlay" onclick="if(event.target===this)closeStrategyModal()">
    <div class="modal-content">
        <button class="modal-close" onclick="closeStrategyModal()">X</button>
        <div id="strategy-modal-body">Loading...</div>
    </div>
</div>

<!-- STRATEGIES -->
<div id="section-strategies" style="display:none">
<div class="panel">
    <h2>🎯 All 91 Strategies</h2>
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
        <button onclick="loadStrategies()">Refresh</button>
    </div>
    <div id="all-strategies" class="loading">Loading...</div>
</div>
</div>

<!-- CATALYST SCANNER -->
<div id="section-catalyst" style="display:none">
<div class="panel">
    <h2>🔬 Catalyst Analyzer</h2>
    <div class="input-group">
        <input type="text" id="catalyst-ticker" placeholder="Ticker (e.g. NTDOY)" value="NTDOY">
        <button onclick="runCatalyst()">Analyze</button>
    </div>
    <div id="catalyst-results" class="loading">Enter a ticker and click Analyze</div>
</div>
</div>

<!-- CHARTS -->
<div id="section-charts" style="display:none">
<div class="panel">
    <h2>📉 Equity Chart</h2>
    <div class="input-group">
        <input type="text" id="chart-ticker" placeholder="Ticker" value="NVDA">
        <input type="text" id="chart-start" placeholder="Start" value="2024-01-01">
        <button onclick="loadChart()">Generate</button>
    </div>
    <div id="chart-container"></div>
</div>
</div>

<!-- STOCK PICK (Iteration 3: prominent, grouped, better UX) -->
<div id="section-stockpick" style="display:none">
<div class="panel" style="border-color:#00ff88;">
    <h2>STOCKPICK -- AI STRATEGY MATCHER</h2>
    <p style="color:#ccc; margin-bottom:12px; font-size:13px;">Enter your stock picks. We match them to our best backtested strategies, suggest additional tickers, and show volatility-adjusted position sizing. Claude AI reviews the result.</p>

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

    <div class="input-group" style="margin-top:8px;">
        <input type="text" id="pick-symbols" placeholder="Tickers separated by commas (e.g. NVDA, AAPL, TSLA)" style="flex:3; font-size:14px; padding:10px 12px;">
        <input type="number" id="pick-amount" value="100000" min="1000" step="1000" style="width:130px; font-size:14px; padding:10px 12px;" placeholder="Portfolio $">
        <select id="pick-horizon" style="width:80px; font-size:14px; padding:10px 12px;">
            <option value="3y" selected>3Y</option>
            <option value="1y">1Y</option>
            <option value="5y">5Y</option>
        </select>
        <button onclick="analyzeStockPick()" style="font-size:14px; padding:10px 20px;">Analyze</button>
    </div>
    <div id="pick-loading-bar" style="display:none; margin:10px 0;">
        <div style="background:#1a1a2e; border-radius:4px; height:6px; overflow:hidden;">
            <div id="pick-progress" style="background:#00ff88; height:100%; width:0%; transition:width 0.5s;"></div>
        </div>
        <p id="pick-loading-text" style="color:#888; font-size:11px; margin-top:4px;">Matching strategies...</p>
    </div>
    <div id="pick-results"></div>
</div>
</div>

<!-- PORTFOLIO BUILDER (Iteration 4) -->
<div id="section-portfolio" style="display:none">
<div class="panel">
    <h2>PORTFOLIO BUILDER -- Combine Strategies</h2>
    <p style="color:#888; margin-bottom:10px; font-size:12px;">Select multiple strategies, set allocation percentages, and see the combined position list with overlap detection.</p>
    <div class="input-group">
        <input type="number" id="portfolio-total" value="100000" min="1000" step="1000" style="width:150px" placeholder="Total Portfolio $">
        <button onclick="buildPortfolio()">Build Portfolio</button>
        <button onclick="clearPortfolio()" style="background:#1a1a2e; color:#ff4444; border-color:#ff4444;">Clear</button>
    </div>
    <div class="grid">
        <div class="panel" style="max-height:500px; overflow-y:auto;">
            <h3>Select Strategies (check to include)</h3>
            <div id="portfolio-strategy-list" class="loading">Loading strategies...</div>
        </div>
        <div>
            <div class="panel" style="margin-bottom:15px;">
                <h3>Allocation Summary</h3>
                <div id="portfolio-alloc-summary">Select strategies to begin.</div>
            </div>
            <div class="panel">
                <h3>Overlap Detection</h3>
                <div id="portfolio-overlap">No strategies selected.</div>
            </div>
        </div>
    </div>
    <div class="panel full" style="margin-top:15px;">
        <h3>Combined Position List</h3>
        <div id="portfolio-positions">Select strategies and click "Build Portfolio" to see combined positions.</div>
    </div>
</div>
</div>

<!-- TRADE -->
<div id="section-trade" style="display:none">
<div class="panel">
    <h2>💰 Trade Execution (Public.com)</h2>
    <p style="color:#ff4444; margin-bottom:10px;">⚠️ DISCLAIMER: This is not financial advice. Past performance does not predict future results. Trade at your own risk.</p>
    <div class="input-group">
        <select id="trade-strategy" style="flex:2">
            <optgroup label="⭐ Top Performers (Sharpe > 1.0)">
                <option value="concentrate_winners">Concentrate Winners (1.11 Sharpe, +818% 10Y)</option>
                <option value="momentum">Momentum (1.08 Sharpe, +570% 10Y)</option>
                <option value="momentum_crash_hedge">Momentum Crash-Hedged (1.05 Sharpe, +743% 10Y)</option>
                <option value="ai_revolution">AI Revolution (0.94 Sharpe, +783% 10Y)</option>
            </optgroup>
            <optgroup label="📊 Portfolio Strategies (hedged)">
                <option value="barbell_portfolio">Barbell Portfolio (2.05 Sharpe 1Y)</option>
                <option value="staples_hedged_growth">Staples-Hedged Growth</option>
                <option value="core_satellite">Core-Satellite (60/40 active)</option>
            </optgroup>
            <optgroup label="🏛️ Political / Billionaire">
                <option value="nancy_pelosi">Nancy Pelosi (1.39 Sharpe 3Y)</option>
                <option value="bill_ackman">Bill Ackman (1.22 Sharpe 3Y)</option>
                <option value="stanley_druckenmiller">Druckenmiller (1.38 Sharpe 1Y)</option>
            </optgroup>
            <optgroup label="🔬 Themes">
                <option value="glp1_obesity">GLP-1 Obesity (0.92 Sharpe 3Y)</option>
                <option value="defense_aerospace">Defense & Aerospace</option>
                <option value="small_cap_value_rotation">Small Cap Value</option>
            </optgroup>
            <optgroup label="🛡️ Defensive">
                <option value="defensive_rotation">Defensive Rotation (recession hedge)</option>
                <option value="income_shield">Income Shield (high dividend)</option>
            </optgroup>
        </select>
        <input type="number" id="trade-amount" value="100000" min="1000" step="1000" style="width:120px" placeholder="$">
        <button onclick="generateTradePlan()" style="flex:0">📋 Generate Plan</button>
        <button onclick="executeTrades()" class="danger" style="flex:0">⚡ EXECUTE (Live)</button>
    </div>
    <div id="trade-results"></div>
</div>
</div>

</div>

<div id="status">agents-assemble | 91 strategies | 580 tickers | <span id="status-time"></span></div>

<script>
function esc(s) {
    const d = document.createElement('div');
    d.appendChild(document.createTextNode(s));
    return d.innerHTML;
}
function fetchJSON(url, opts) {
    return fetch(url, opts).then(r => r.json().then(d => {
        if (!r.ok) throw new Error(d.error || 'Server error ' + r.status);
        return d;
    }, () => { throw new Error('Server error ' + r.status); }));
}
function showSection(name, el) {
    document.querySelectorAll('[id^="section-"]').forEach(s => s.style.display = 'none');
    document.getElementById('section-' + name).style.display = 'block';
    document.querySelectorAll('.nav a').forEach(a => a.classList.remove('active'));
    if (el) el.classList.add('active');
    // Auto-load portfolio strategy list when switching to portfolio tab
    if (name === 'portfolio' && !portfolioStrategiesLoaded) loadPortfolioStrategies();
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
    const arrow = sortAsc ? '&#9650;' : '&#9660;';
    const horizon = document.getElementById('horizon-select').value.toUpperCase();
    const cols = [
        {key:'return', label:horizon + ' Return'}, {key:'sharpe', label:'Sharpe'}, {key:'max_dd', label:'Max DD'}
    ];
    let html = '<table><tr><th>#</th><th>Strategy</th><th>Category</th>';
    cols.forEach(c => {
        const active = sortCol === c.key ? ' style="color:#00ff88;cursor:pointer"' : ' style="cursor:pointer"';
        html += '<th' + active + ' onclick="sortLeaderboard(\'' + c.key + '\')">' + c.label + (sortCol === c.key ? ' ' + arrow : '') + '</th>';
    });
    html += '<th>Actions</th></tr>';
    sorted.forEach((s, i) => {
        const ret = s.return || 0, sharpe = s.sharpe || 0, max_dd = s.max_dd || 0;
        const retClass = ret > 0 ? 'positive' : 'negative';
        html += '<tr><td>' + (i+1) + '</td>'
            + '<td><b><a href="#" onclick="openStrategyDetail(\'' + esc(s.name) + '\');return false;">' + esc(s.name) + '</a></b></td>'
            + '<td><span class="tag tag-blue">' + esc(s.source) + '</span></td>'
            + '<td class="' + retClass + '">' + (ret*100).toFixed(1) + '%</td>'
            + '<td>' + sharpe.toFixed(2) + '</td>'
            + '<td class="negative">' + (max_dd*100).toFixed(1) + '%</td>'
            + '<td><button onclick="openStrategyDetail(\'' + esc(s.name) + '\')" style="padding:2px 8px;font-size:10px;">Detail</button></td></tr>';
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
        // Render market overview table
        let html = '<table><tr><th>Index</th><th>Price</th><th>20D Change</th><th>Trend</th></tr>';
        Object.entries(data).forEach(([sym, info]) => {
            const cls = info.change >= 0 ? 'positive' : 'negative';
            const trendArrow = info.change >= 0 ? '&#9650; Bullish' : '&#9660; Bearish';
            html += '<tr><td><b>' + sym + '</b></td><td>$' + info.price.toFixed(2) + '</td>'
                + '<td class="' + cls + '">' + (info.change >= 0 ? '+' : '') + (info.change*100).toFixed(1) + '%</td>'
                + '<td class="' + cls + '">' + trendArrow + '</td></tr>';
        });
        html += '</table>';
        document.getElementById('market-overview').innerHTML = html;

        // Render market pills in status bar
        let pills = '';
        const nameMap = {SPY: 'S&P 500', QQQ: 'Nasdaq', IWM: 'Russell', TLT: 'Bonds', GLD: 'Gold'};
        Object.entries(data).forEach(([sym, info]) => {
            const arrow = info.change >= 0 ? '<span class="arrow-up">&#9650;</span>' : '<span class="arrow-down">&#9660;</span>';
            const cls = info.change >= 0 ? 'positive' : 'negative';
            pills += '<span class="market-pill">' + arrow + ' <b>' + (nameMap[sym] || sym) + '</b> '
                + '<span class="' + cls + '">' + (info.change >= 0 ? '+' : '') + (info.change*100).toFixed(1) + '%</span></span>';
        });

        // VIX check: if SPY is down and IWM is down, show risk warning
        const spy = data.SPY, iwm = data.IWM;
        if (spy && spy.change < -0.02 && iwm && iwm.change < -0.02) {
            pills += '<span class="market-pill" style="border-color:#ff4444;"><span class="arrow-down">!!</span> <b style="color:#ff4444;">RISK OFF</b></span>';
        } else if (spy && spy.change > 0.02) {
            pills += '<span class="market-pill" style="border-color:#00ff88;"><span class="arrow-up">&#9650;</span> <b style="color:#00ff88;">RISK ON</b></span>';
        }
        document.getElementById('market-pills').innerHTML = pills;
    }).catch(e => {
        document.getElementById('market-overview').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}
loadMarket();

// ==================== TOP PICKS ====================
let topPicksView = 'active'; // 'active' or 'passive'
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
        document.getElementById('top-picks-list').innerHTML = '<p class="loading">No data yet. Click "Refresh Top Picks".</p>';
        return;
    }
    const picks = topPicksView === 'passive'
        ? topPicksData.filter(p => p.rebalance === 'monthly' || p.rebalance === 'quarterly' || (p.sharpe||0) > 0.5).slice(0, 5)
        : topPicksData.slice(0, 5);

    let html = '';
    picks.forEach((p, i) => {
        const ret = p.total_return || 0;
        const retClass = ret > 0 ? 'positive' : 'negative';
        const posCount = (p.positions || []).length;
        const topSyms = (p.positions || []).slice(0, 3).map(pos => pos.symbol).join(', ');
        html += '<div class="top-pick-card" onclick="openStrategyDetail(\'' + esc(p.name) + '\')">'
            + '<div class="top-pick-rank">#' + (i+1) + '</div>'
            + '<div class="top-pick-info">'
            + '<div class="name">' + esc(p.name) + ' <span class="tag tag-blue">' + esc(p.source || '') + '</span></div>'
            + '<div class="meta">' + posCount + ' positions' + (topSyms ? ' | Top: ' + esc(topSyms) : '') + '</div>';

        if (topPicksView === 'passive' && p.execution_guidance) {
            html += '<div class="meta" style="color:#ffaa00;">' + esc(p.execution_guidance.timing || '') + '</div>';
        }
        html += '</div>'
            + '<div class="top-pick-stats">'
            + '<div class="ret ' + retClass + '">' + (ret > 0 ? '+' : '') + ret.toFixed(1) + '%</div>'
            + '<div class="sharpe">Sharpe: ' + (p.sharpe || 0).toFixed(2) + '</div>';
        if (topPicksView === 'passive' && p.risk_parameters) {
            html += '<div class="sharpe" style="color:#ff4444;">Max DD: ' + esc(p.risk_parameters.max_drawdown_tolerance || '?') + '</div>';
        }
        html += '</div></div>';
    });

    if (topPicksView === 'passive') {
        html += '<p style="color:#888; font-size:10px; margin-top:8px;">Passive view: monthly/quarterly rebalance strategies with Sharpe > 0.5. Buy and hold with trailing stops.</p>';
    }

    document.getElementById('top-picks-list').innerHTML = html;
}
loadTopPicks();

// ==================== STRATEGY DETAIL MODAL (Iteration 2) ====================
function openStrategyDetail(strategyName) {
    const modal = document.getElementById('strategy-modal');
    const body = document.getElementById('strategy-modal-body');
    body.innerHTML = '<p class="loading">Loading details for ' + esc(strategyName) + '...</p>';
    modal.classList.add('active');

    fetchJSON('/api/strategy-detail/' + encodeURIComponent(strategyName)).then(data => {
        let html = '<h2 style="color:#00ff88; margin-bottom:15px;">' + esc(data.name || strategyName) + '</h2>';

        // Performance metrics
        if (data.metrics) {
            html += '<div class="grid-3" style="margin-bottom:15px;">';
            const m = data.metrics;
            const ret = parseFloat(m.total_return) || 0;
            html += '<div class="panel"><h3>Performance</h3>'
                + '<p><b>Return:</b> <span class="' + (ret > 0 ? 'positive' : 'negative') + '">' + esc(m.total_return || '?') + '</span></p>'
                + '<p><b>Sharpe:</b> ' + esc(m.sharpe_ratio || '?') + '</p>'
                + '<p><b>Win Rate:</b> ' + esc(m.win_rate || '?') + '</p>'
                + '<p><b>Alpha:</b> ' + esc(m.alpha || '?') + '</p></div>';
            html += '<div class="panel"><h3>Risk</h3>'
                + '<p><b>Max DD:</b> <span class="negative">' + esc(m.max_drawdown || '?') + '</span></p>';
            if (data.risk_parameters) {
                const rp = data.risk_parameters;
                html += '<p><b>Stop Loss:</b> ' + esc(rp.stop_loss || '?') + '</p>'
                    + '<p><b>Take Profit:</b> ' + esc(rp.take_profit_target || '?') + '</p>'
                    + '<p><b>Rebalance:</b> ' + esc(rp.rebalance_frequency || '?') + '</p>';
            }
            html += '</div>';
            html += '<div class="panel"><h3>Execution</h3>';
            if (data.execution_guidance) {
                const eg = data.execution_guidance;
                html += '<p><b>Order Type:</b> ' + esc(eg.order_type || '?') + '</p>'
                    + '<p><b>Timing:</b> ' + esc(eg.timing || '?') + '</p>'
                    + '<p><b>Scaling:</b> ' + esc(eg.scaling || '?') + '</p>';
            } else {
                html += '<p style="color:#888;">No execution guidance available.</p>';
            }
            html += '</div></div>';
        }

        // Overall assessment
        if (data.overall_assessment) {
            html += '<div class="panel" style="margin-bottom:15px; border-color:#ffaa00;">'
                + '<h3>Assessment</h3><p>' + esc(data.overall_assessment) + '</p></div>';
        }

        // Positions table
        if (data.positions && data.positions.length > 0) {
            html += '<div class="panel" style="margin-bottom:15px;">';
            html += '<h3>Current Positions (' + data.positions.length + ')</h3>';
            html += '<table><tr><th>Symbol</th><th>Action</th><th>Volatility</th><th>Entry Rule</th><th>Stop Loss</th><th>Take Profit</th><th>Size</th></tr>';
            data.positions.forEach(p => {
                const actionClass = p.action === 'BUY' ? 'tag-green' : p.action === 'HOLD' ? 'tag-yellow' : 'tag-red';
                html += '<tr><td><b>' + esc(p.symbol || '') + '</b></td>'
                    + '<td><span class="tag ' + actionClass + '">' + esc(p.action || '') + '</span></td>'
                    + '<td>' + esc(p.annual_volatility || '') + '</td>'
                    + '<td style="font-size:11px;">' + esc(p.entry_rule || '') + '</td>'
                    + '<td class="negative">' + esc(p.stop_loss || '') + '</td>'
                    + '<td class="positive">' + esc(p.take_profit || '') + '</td>'
                    + '<td><b>' + esc(p.position_size || '') + '</b></td></tr>';
            });
            html += '</table></div>';
        }

        // Rolling performance sparkline (text-based)
        if (data.rolling_returns && data.rolling_returns.length > 0) {
            html += '<div class="panel" style="margin-bottom:15px;">';
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
            html += '<p style="color:#555; font-size:10px; margin-top:4px;">Each bar = 1 month. Green = positive, Red = negative.</p>';
            html += '</div>';
        }

        // Action buttons
        html += '<div style="display:flex; gap:8px; margin-top:10px;">';
        html += '<button onclick="closeStrategyModal(); showSection(\'trade\', document.querySelector(\'[onclick*=trade]\'));">Generate Trade Plan</button>';
        html += '<button onclick="closeStrategyModal();" style="background:#1a1a2e; color:#888;">Close</button>';
        html += '</div>';

        body.innerHTML = html;
    }).catch(e => {
        body.innerHTML = '<p class="negative">Error loading strategy: ' + esc(String(e)) + '</p><button onclick="closeStrategyModal()">Close</button>';
    });
}

function closeStrategyModal() {
    document.getElementById('strategy-modal').classList.remove('active');
}

// ==================== QUICK SCAN ====================
function scanTicker() {
    const sym = document.getElementById('scan-ticker').value.toUpperCase();
    document.getElementById('scan-results').innerHTML = '<p class="loading">Scanning ' + sym + '...</p>';
    fetchJSON('/api/scan/' + encodeURIComponent(sym)).then(data => {
        let html = '<h3>' + sym + ' — ' + esc(data.industry || '') + '</h3>';
        if (data.best) {
            html += '<p><span class="tag tag-green">' + esc(data.best.strategy || '') + '</span> '
                + 'Win: ' + (data.best.win_rate*100).toFixed(0) + '% | '
                + 'Return: <span class="positive">' + (data.best.total_return*100).toFixed(1) + '%</span></p>';
        }
        if (data.patterns) {
            html += '<p>Events: ' + data.patterns.total_events + ' (' + data.patterns.up_events + '↑ ' + data.patterns.down_events + '↓)</p>';
        }
        document.getElementById('scan-results').innerHTML = html;
    }).catch(e => {
        document.getElementById('scan-results').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

function runCatalyst() {
    const sym = document.getElementById('catalyst-ticker').value.toUpperCase();
    document.getElementById('catalyst-results').innerHTML = '<p class="loading">Analyzing ' + sym + '... (this takes ~30s)</p>';
    fetchJSON('/api/catalyst/' + encodeURIComponent(sym)).then(data => {
        let html = '<h3>' + sym + ' — ' + esc(data.industry || 'general') + '</h3>';
        // Patterns
        if (data.historical_patterns && data.historical_patterns.total_events) {
            const p = data.historical_patterns;
            html += '<p>Events: ' + p.total_events + ' (' + p.up_events + '↑ ' + p.down_events + '↓)</p>';
            if (p.optimal_sell_after_up) html += '<p>Optimal sell (UP): <span class="tag tag-green">' + p.optimal_sell_after_up + '</span></p>';
            if (p.optimal_sell_after_down) html += '<p>Optimal sell (DOWN): <span class="tag tag-yellow">' + p.optimal_sell_after_down + '</span></p>';
        }
        // Backtests
        if (data.backtests) {
            html += '<h3>Backtests</h3><table><tr><th>Strategy</th><th>Trades</th><th>Win%</th><th>Return</th><th>PF</th></tr>';
            const sorted = Object.entries(data.backtests).sort((a,b) => b[1].total_return - a[1].total_return);
            sorted.slice(0, 10).forEach(([key, bt]) => {
                const cls = bt.total_return > 0 ? 'positive' : 'negative';
                html += '<tr><td>' + key + '</td><td>' + bt.total_trades + '</td>'
                    + '<td>' + (bt.win_rate*100).toFixed(0) + '%</td>'
                    + '<td class="' + cls + '">' + (bt.total_return*100).toFixed(1) + '%</td>'
                    + '<td>' + bt.profit_factor.toFixed(1) + '</td></tr>';
            });
            html += '</table>';
        }
        // Predictions
        if (data.predictions && data.predictions.length > 0) {
            html += '<h3>Forward Predictions</h3>';
            data.predictions.forEach(p => {
                html += '<p><span class="tag tag-' + (p.confidence === 'high' ? 'green' : p.confidence === 'medium' ? 'yellow' : 'red') + '">'
                    + esc(p.confidence.toUpperCase()) + '</span> ' + esc(p.recommended_action) + '</p>';
            });
        }
        // News
        if (data.news && data.news.length > 0) {
            html += '<h3>Latest News</h3>';
            data.news.slice(0, 8).forEach(n => {
                if (n.title && n.title.length > 5) {
                    html += '<p style="font-size:11px;margin:3px 0"><span class="tag tag-yellow">' + esc(n.catalyst_type || 'news') + '</span> '
                        + '<span style="color:#888">' + esc(n.date || '') + '</span> '
                        + (n.url && /^https?:\/\//i.test(n.url) ? '<a href="' + encodeURI(n.url) + '" target="_blank">' + esc(n.title.substring(0, 80)) + '</a>' : esc(n.title.substring(0, 80)))
                        + '</p>';
                }
            });
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
    document.getElementById('trade-results').innerHTML = '<p class="loading">Generating trade plan for ' + strat + '...</p>';
    fetchJSON('/api/trade-plan/' + strat + '?amount=' + amt).then(data => {
        let html = '<h3>Trade Plan: ' + esc(data.strategy || '') + ' (DRY RUN)</h3>';
        const planAmt = data.amount || 100000;
        html += '<p style="color:#888;font-size:11px">Portfolio: $' + planAmt.toLocaleString() + ' | Slippage: 10bps | Positions: ' + (data.orders||[]).length + '</p>';
        if (data.orders && data.orders.length > 0) {
            html += '<table><tr><th>Action</th><th>Symbol</th><th>Qty</th><th>Entry Price</th><th>Limit (0.5% below)</th><th>Stop Loss (15%)</th><th>Take Profit (10%)</th><th>Alloc</th></tr>';
            let totalAlloc = 0;
            data.orders.forEach(o => {
                const limit = (o.price * 0.995).toFixed(2);
                const stopLoss = (o.price * 0.85).toFixed(2);
                const takeProfit = (o.price * 1.10).toFixed(2);
                const alloc = ((o.quantity * o.price / planAmt) * 100).toFixed(1);
                totalAlloc += parseFloat(alloc);
                html += '<tr>'
                    + '<td><span class="tag tag-' + (o.side === 'BUY' ? 'green' : 'red') + '">' + o.side + '</span></td>'
                    + '<td><b>' + o.symbol + '</b></td>'
                    + '<td>' + o.quantity + '</td>'
                    + '<td>$' + o.price.toFixed(2) + '</td>'
                    + '<td class="positive">$' + limit + '</td>'
                    + '<td class="negative">$' + stopLoss + '</td>'
                    + '<td class="positive">$' + takeProfit + '</td>'
                    + '<td>' + alloc + '%</td></tr>';
            });
            html += '<tr style="border-top:2px solid #333"><td colspan="7"><b>Total Allocation</b></td><td><b>' + totalAlloc.toFixed(1) + '%</b></td></tr>';
            html += '</table>';
            html += '<p style="margin-top:10px"><span class="tag tag-yellow">Trailing Stop</span> 12% trailing stop after 5% gain on each position</p>';
            html += '<p><span class="tag tag-blue">Order Type</span> LIMIT orders at 0.5% below current price. Scale in over 3 tranches.</p>';
        } else {
            html += '<p class="negative">No positions generated — strategy may not have signals today.</p>';
        }
        document.getElementById('trade-results').innerHTML = html;
    }).catch(e => {
        document.getElementById('trade-results').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

function executeTrades() {
    if (!confirm('⚠️ LIVE TRADING: This will place REAL orders with REAL money on Public.com.\\n\\nDo you have PUBLIC_API_SECRET set?\\n\\nClick OK to proceed or Cancel to abort.')) return;
    const strat = document.getElementById('trade-strategy').value;
    const amt = document.getElementById('trade-amount').value;
    document.getElementById('trade-results').innerHTML = '<p class="loading" style="color:#ff4444">⚡ EXECUTING live trades for ' + strat + '...</p>';
    fetchJSON('/api/execute-trade/' + strat, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({amount: parseFloat(amt)})}).then(data => {
        let html = '<h3 style="color:#ff4444">⚡ EXECUTION RESULT: ' + esc(strat) + '</h3>';
        if (data.error) {
            html += '<p class="negative">' + esc(data.error) + '</p>';
        } else if (data.placed && data.placed.length > 0) {
            html += '<p class="positive">' + data.placed.length + ' orders placed!</p>';
            html += '<table><tr><th>Symbol</th><th>Side</th><th>Qty</th><th>Status</th></tr>';
            data.placed.forEach(o => {
                html += '<tr><td>' + esc(o.symbol) + '</td><td>' + esc(o.side) + '</td><td>' + o.quantity + '</td><td class="positive">SENT</td></tr>';
            });
            html += '</table>';
        } else {
            html += '<p class="negative">No orders were placed — strategy may not have signals today.</p>';
        }
        document.getElementById('trade-results').innerHTML = html;
    }).catch(e => {
        document.getElementById('trade-results').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

// StockPick analyzer — carousel of N strategies with shuffle re-roll
let pickData = null;       // Full API response
let pickRecs = [];         // Shuffled recommendations array
let pickIdx = 0;           // Current index in carousel
let pickCycleCount = 0;    // How many full cycles done

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

    // Navigation bar
    html += '<div style="display:flex;align-items:center;gap:10px;margin:10px 0">';
    html += '<button onclick="prevPick()" style="padding:4px 12px">&lt; Prev</button>';
    html += '<span style="color:#888">Strategy ' + (idx+1) + ' of ' + total + '</span>';
    html += '<button onclick="nextPick()" style="padding:4px 12px">Next &gt;</button>';
    html += '<button onclick="rerollPicks()" style="padding:4px 12px;background:#ffaa00;color:#0a0a1a">🎲 Re-roll</button>';
    html += '</div>';

    // Strategy match header
    if (ms) {
        html += '<div class="panel" style="margin:10px 0; border-color:#00ff88">';
        html += '<h2>🎯 Matched Strategy: ' + esc(ms.name) + ' <span class="tag tag-blue">' + esc(ms.source) + '</span></h2>';
        html += '<p>' + esc(rec.strategy_explanation || '') + '</p>';
        html += '</div>';
    } else {
        html += '<div class="panel" style="margin:10px 0; border-color:#ffaa00">';
        html += '<h2>⚠️ No Direct Strategy Match</h2>';
        html += '<p>' + esc(rec.strategy_explanation || '') + '</p>';
        html += '</div>';
    }

    // Backtest results
    if (rec.backtest && rec.backtest.metrics) {
        const m = rec.backtest.metrics;
        const ret = m.total_return || 0;
        const sharpe = m.sharpe_ratio || 0;
        const maxdd = m.max_drawdown || 0;
        const alpha = m.alpha || 0;
        const winr = m.win_rate || 0;
        html += '<div class="grid-3" style="margin:10px 0">';
        html += '<div class="panel"><h3>Backtest (' + esc(rec.backtest.horizon) + ')</h3>';
        html += '<p><b>Return:</b> <span class="' + (ret > 0 ? 'positive' : 'negative') + '">' + (ret*100).toFixed(1) + '%</span></p>';
        html += '<p><b>Sharpe:</b> ' + sharpe.toFixed(2) + '</p>';
        html += '<p><b>Max DD:</b> <span class="negative">' + (maxdd*100).toFixed(1) + '%</span></p>';
        html += '</div>';
        html += '<div class="panel"><h3>Alpha & Edge</h3>';
        html += '<p><b>Alpha:</b> <span class="' + (alpha > 0 ? 'positive' : 'negative') + '">' + (alpha*100).toFixed(1) + '%</span></p>';
        html += '<p><b>Win Rate:</b> ' + (winr*100).toFixed(0) + '%</p>';
        html += '<p><b>Beta:</b> ' + (m.beta || 0).toFixed(2) + '</p>';
        html += '</div>';
        html += '<div class="panel"><h3>Hypothesis</h3>';
        html += '<p style="font-size:11px">' + esc(rec.hypothesis || '') + '</p>';
        html += '</div>';
        html += '</div>';
    }

    // Position table
    if (rec.positions && rec.positions.length > 0) {
        html += '<div class="panel" style="margin:10px 0">';
        html += '<h2>Position Recommendations — Vol-Adjusted Risk</h2>';
        html += '<p style="color:#888;font-size:11px">Each position sized by volatility. Your picks highlighted in green.</p>';
        html += '<table><tr><th></th><th>Symbol</th><th>Action</th><th>Vol</th><th>Entry Rule</th><th>Stop Loss</th><th>Take Profit</th><th>Size</th><th>$ Amount</th><th>Live Price</th></tr>';
        rec.positions.forEach(p => {
            const rowStyle = p.is_user_pick ? ' style="background:#00ff8811"' : '';
            const pickTag = p.is_user_pick ? '<span class="tag tag-green">YOUR PICK</span>' : '<span class="tag tag-yellow">SUGGESTED</span>';
            const actionClass = p.action === 'BUY' ? 'tag-green' : p.action === 'HOLD' ? 'tag-yellow' : p.action === 'WATCH' ? 'tag-blue' : 'tag-red';
            const tvOk = p.tradingview_url && /^https?:\/\//i.test(p.tradingview_url);
            const yfOk = p.yahoo_url && /^https?:\/\//i.test(p.yahoo_url);
            const links = (tvOk ? '<a href="' + encodeURI(p.tradingview_url) + '" target="_blank">TV</a>' : '')
                + (yfOk ? ' <a href="' + encodeURI(p.yahoo_url) + '" target="_blank">YF</a>' : '');
            html += '<tr' + rowStyle + '>'
                + '<td>' + pickTag + '</td>'
                + '<td><b>' + esc(p.symbol) + '</b></td>'
                + '<td><span class="tag ' + actionClass + '">' + esc(p.action) + '</span></td>'
                + '<td>' + esc(p.annual_volatility) + '</td>'
                + '<td style="font-size:11px">' + esc(p.entry_rule) + '</td>'
                + '<td class="negative">' + esc(p.stop_loss) + '</td>'
                + '<td class="positive">' + esc(p.take_profit) + '</td>'
                + '<td><b>' + esc(p.position_size) + '</b></td>'
                + '<td>' + esc(p.position_dollars) + '</td>'
                + '<td>' + links + '</td></tr>';
            if (p.note) {
                html += '<tr' + rowStyle + '><td colspan="10" style="font-size:11px;color:#ffaa00;padding-left:30px">⚠️ ' + esc(p.note) + '</td></tr>';
            }
        });
        html += '</table></div>';
    }

    // Notes
    if (rec.notes && rec.notes.length > 0) {
        html += '<div class="panel" style="margin:10px 0; border-color:#ffaa00">';
        html += '<h2>Notes & Warnings</h2>';
        rec.notes.forEach(n => {
            html += '<p style="color:#ffaa00; font-size:12px">⚠️ ' + esc(n) + '</p>';
        });
        html += '</div>';
    }

    // Claude AI analysis
    if (rec.claude_analysis) {
        html += '<div class="panel" style="margin:10px 0; border-color:#4488ff">';
        html += '<h2>🤖 Claude AI Analysis</h2>';
        html += '<div style="white-space:pre-wrap; font-size:12px; line-height:1.5">' + esc(rec.claude_analysis) + '</div>';
        html += '</div>';
    }

    return html;
}

function showPickResult() {
    if (!pickData || !pickRecs.length) return;
    let html = '';
    // Invalid picks warning
    if (pickData.invalid_picks && pickData.invalid_picks.length > 0) {
        html += '<p class="negative" style="font-size:11px">Could not find data for: ' + esc(pickData.invalid_picks.join(', ')) + '</p>';
    }
    html += '<p style="color:#888;font-size:11px">' + pickData.total_strategies_matched + ' strategies matched your picks. Showing top ' + pickRecs.length + '.</p>';
    html += renderPickRecommendation(pickRecs[pickIdx], pickIdx, pickRecs.length);
    html += '<p style="color:#555;font-size:10px;margin-top:10px">Not financial advice. Past performance does not predict future results. Trade at your own risk.</p>';
    document.getElementById('pick-results').innerHTML = html;
}

function nextPick() {
    pickIdx++;
    if (pickIdx >= pickRecs.length) {
        // Completed a full cycle — reshuffle
        pickIdx = 0;
        pickCycleCount++;
        pickRecs = shuffleArray(pickRecs);
    }
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

// Stock group preset handler
function setStockGroup(tickers) {
    document.getElementById('pick-symbols').value = tickers;
}

function analyzeStockPick() {
    const syms = document.getElementById('pick-symbols').value.toUpperCase().trim();
    const amt = document.getElementById('pick-amount').value;
    const horizon = document.getElementById('pick-horizon').value;
    if (!syms) { document.getElementById('pick-results').innerHTML = '<p class="negative">Enter at least one ticker.</p>'; return; }

    // Show loading bar
    const loadBar = document.getElementById('pick-loading-bar');
    const progress = document.getElementById('pick-progress');
    const loadText = document.getElementById('pick-loading-text');
    loadBar.style.display = 'block';
    progress.style.width = '0%';
    document.getElementById('pick-results').innerHTML = '';

    // Simulate progress
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
        loadText.textContent = 'Done!';
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

// Load all strategies list
function loadStrategies() {
    document.getElementById('all-strategies').innerHTML = '<p class="loading">Loading...</p>';
    fetchJSON('/api/strategies').then(data => {
        let html = '<table><tr><th>Strategy</th><th>Category</th><th>Universe Size</th><th>Rebalance</th><th>Risk</th></tr>';
        const filter = document.getElementById('cat-filter').value;
        data.forEach(s => {
            if (filter && s.source !== filter) return;
            html += '<tr><td><b><a href="#" onclick="openStrategyDetail(\'' + esc(s.name) + '\');return false;">' + esc(s.name) + '</a></b></td>'
                + '<td><span class="tag tag-blue">' + esc(s.source) + '</span></td>'
                + '<td>' + s.universe_size + '</td>'
                + '<td>' + esc(s.rebalance || '?') + '</td>'
                + '<td>' + esc(s.risk || '?') + '</td></tr>';
        });
        html += '</table>';
        document.getElementById('all-strategies').innerHTML = html;
    }).catch(e => {
        document.getElementById('all-strategies').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}
// Auto-load strategies when switching to that tab
document.querySelector('[onclick*="strategies"]').addEventListener('click', function() { setTimeout(loadStrategies, 100); });

// ==================== PORTFOLIO BUILDER (Iteration 4) ====================
let portfolioStrategiesLoaded = false;
let portfolioStrategies = []; // cached strategy list for portfolio
let selectedStrategies = {};  // {name: {alloc: 10, data: {...}}}

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
            html += '<div style="padding:6px 0; border-bottom:1px solid #1a1a2e; display:flex; align-items:center; gap:8px;">'
                + '<input type="checkbox" class="strat-checkbox" id="pf-' + esc(s.name) + '" ' + checked + ' onchange="togglePortfolioStrategy(\'' + esc(s.name) + '\', this.checked)">'
                + '<label for="pf-' + esc(s.name) + '" style="flex:1; cursor:pointer;">'
                + '<b>' + esc(s.name) + '</b> <span class="tag tag-blue">' + esc(s.source || '') + '</span>'
                + ' <span class="' + retClass + '">' + (ret > 0 ? '+' : '') + ret.toFixed(1) + '%</span>'
                + ' Sharpe: ' + (s.sharpe || 0).toFixed(2)
                + '</label>'
                + '<input type="number" class="alloc-input" id="alloc-' + esc(s.name) + '" value="' + (selectedStrategies[s.name] ? selectedStrategies[s.name].alloc : 10) + '" min="1" max="100" onchange="updatePortfolioAlloc(\'' + esc(s.name) + '\', this.value)">'
                + '<span style="color:#888; font-size:11px;">%</span>'
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
        selectedStrategies[name] = { alloc: parseInt(allocEl ? allocEl.value : 10), data: strat };
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
        summaryEl.innerHTML = 'Select strategies to begin.';
        overlapEl.innerHTML = 'No strategies selected.';
        return;
    }
    const totalAlloc = names.reduce((sum, n) => sum + selectedStrategies[n].alloc, 0);
    let html = '<table><tr><th>Strategy</th><th>Alloc %</th><th>Normalized</th></tr>';
    names.forEach(n => {
        const raw = selectedStrategies[n].alloc;
        const norm = totalAlloc > 0 ? (raw / totalAlloc * 100).toFixed(1) : '0';
        html += '<tr><td>' + esc(n) + '</td><td>' + raw + '%</td><td>' + norm + '%</td></tr>';
    });
    html += '<tr style="border-top:2px solid #333;"><td><b>Total</b></td><td><b>' + totalAlloc + '%</b></td><td><b>100%</b></td></tr>';
    html += '</table>';
    if (totalAlloc !== 100) {
        html += '<p style="color:#ffaa00; font-size:11px;">Allocations will be normalized to 100% when building.</p>';
    }
    summaryEl.innerHTML = html;

    // Overlap detection
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
            ohtml += '<tr><td><b>' + esc(sym) + '</b></td><td>';
            strats.forEach(s => { ohtml += '<span class="overlap-badge">' + esc(s) + '</span> '; });
            ohtml += '</td></tr>';
        });
        ohtml += '</table>';
        ohtml += '<p style="color:#ffaa00; font-size:11px;">' + overlaps.length + ' symbols appear in multiple strategies. Combined allocations will be summed.</p>';
        overlapEl.innerHTML = ohtml;
    } else {
        overlapEl.innerHTML = '<p style="color:#00ff88;">No overlap detected. Good diversification!</p>';
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

    // Merge all positions, combining overlaps
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

    let html = '<p style="color:#888; font-size:11px; margin-bottom:8px;">Total portfolio: $' + totalAmount.toLocaleString() + ' across ' + names.length + ' strategies, ' + positions.length + ' unique positions.</p>';
    html += '<table><tr><th>Symbol</th><th>Action</th><th>$ Amount</th><th>% of Portfolio</th><th>Volatility</th><th>Stop Loss</th><th>Take Profit</th><th>From Strategies</th></tr>';
    positions.forEach(p => {
        const pct = (p.totalDollars / totalAmount * 100).toFixed(1);
        const isOverlap = p.strategies.length > 1;
        const rowStyle = isOverlap ? ' style="background:#ffaa0011;"' : '';
        html += '<tr' + rowStyle + '><td><b>' + esc(p.symbol) + '</b></td>'
            + '<td><span class="tag tag-green">' + esc(p.action) + '</span></td>'
            + '<td>$' + Math.round(p.totalDollars).toLocaleString() + '</td>'
            + '<td>' + pct + '%</td>'
            + '<td>' + esc(p.volatility) + '</td>'
            + '<td class="negative">' + esc(p.stop_loss) + '</td>'
            + '<td class="positive">' + esc(p.take_profit) + '</td>'
            + '<td>';
        p.strategies.forEach(s => { html += '<span class="tag tag-blue" style="font-size:9px;">' + esc(s) + '</span> '; });
        html += '</td></tr>';
    });
    html += '</table>';
    document.getElementById('portfolio-positions').innerHTML = html;
}

function clearPortfolio() {
    selectedStrategies = {};
    document.querySelectorAll('.strat-checkbox').forEach(cb => { cb.checked = false; });
    updatePortfolioSummary();
    document.getElementById('portfolio-positions').innerHTML = 'Select strategies and click "Build Portfolio" to see combined positions.';
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
        except Exception:
            continue
        if r["status"] == "success":
            m = r["metrics"]
            results.append({
                "name": s["key"], "source": s["source"],
                "return": _safe_metric(m.get("total_return", 0)),
                "sharpe": _safe_metric(m.get("sharpe_ratio", 0), 2),
                "max_dd": _safe_metric(m.get("max_drawdown", 0)),
            })
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
    from data_fetcher import fetch_ohlcv
    indices = {"SPY": "S&P 500", "QQQ": "Nasdaq", "IWM": "Russell 2000",
               "TLT": "Bonds 20Y", "GLD": "Gold"}
    data = {}
    for sym in indices:
        try:
            df = fetch_ohlcv(sym, start=str(date.today() - timedelta(days=60)), cache=True)
            if len(df) > 1:
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
    sym = symbol.upper()
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
                     if isinstance(v.total_return, (int, float)) and math.isfinite(v.total_return)}
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
    sym = symbol.upper()
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
    sym = symbol.upper()
    if not _SYMBOL_RE.match(sym):
        return jsonify({"error": "Invalid symbol"}), 400
    from terminal import Terminal
    start = request.args.get("start", "2024-01-01")
    if not _valid_date(start):
        return jsonify({"error": "Invalid start date (expected valid YYYY-MM-DD)"}), 400
    t = Terminal()
    path = t.equity_chart(sym, start=start)
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
    capped = {s: min(w, max_pos) for s, w in numeric_weights.items()
              if w > 0 and s in prices and prices[s] > 0}
    total_w = sum(capped.values())
    if total_w > 1.0:
        capped = {s: w / total_w for s, w in capped.items()}
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
            total_return = ms.get("total_return", "0")
            try:
                ret_f = float(str(total_return).replace("%", ""))
            except (ValueError, TypeError):
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
        candidates = sorted(d.glob(f"{name}*.json"), key=_mtime, reverse=True)
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
        result_files = sorted(results_dir.glob(f"{name}*.json"), key=_mtime, reverse=True)
        if result_files:
            try:
                rdata = json.loads(result_files[0].read_text())
                # Extract monthly returns if available in the backtest data
                eq = rdata.get("equity_curve", rdata.get("monthly_returns", []))
                if isinstance(eq, list) and len(eq) > 1:
                    # Convert equity curve to monthly returns
                    step = max(1, len(eq) // 12)
                    for i in range(step, len(eq), step):
                        prev = eq[i - step] if isinstance(eq[i - step], (int, float)) else 0
                        curr = eq[i] if isinstance(eq[i], (int, float)) else 0
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

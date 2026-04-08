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
    if isinstance(obj, list):
        return [_sanitize_for_json(v) for v in obj]
    if isinstance(obj, float) and not math.isfinite(obj):
        return None
    return obj

def _safe_metric(val, ndigits=4):
    if not isinstance(val, (int, float)) or isinstance(val, bool) or not math.isfinite(val):
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
</style>
</head>
<body>

<div class="topbar">
    <div class="logo">⚡ agents-assemble</div>
    <div class="nav">
        <a href="#" class="active" onclick="showSection('dashboard', this)">Dashboard</a>
        <a href="#" onclick="showSection('strategies', this)">Strategies</a>
        <a href="#" onclick="showSection('catalyst', this)">Catalyst Scanner</a>
        <a href="#" onclick="showSection('charts', this)">Charts</a>
        <a href="#" onclick="showSection('stockpick', this)">StockPick</a>
        <a href="#" onclick="showSection('trade', this)">Trade</a>
    </div>
</div>

<div class="container">

<!-- DASHBOARD -->
<div id="section-dashboard">
<div class="grid">
    <div class="panel full">
        <h2>📊 Strategy Leaderboard | Return + Sharpe + Max DD</h2>
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
    <div class="panel">
        <h2>📰 Quick Scan</h2>
        <div class="input-group">
            <input type="text" id="scan-ticker" placeholder="Ticker (e.g. NVDA)" value="NVDA">
            <button onclick="scanTicker()">Scan</button>
        </div>
        <div id="scan-results"></div>
    </div>
    <div class="panel">
        <h2>📈 Market Overview</h2>
        <div id="market-overview" class="loading">Loading...</div>
    </div>
</div>
</div>

<!-- STRATEGIES -->
<div id="section-strategies" style="display:none">
<div class="panel">
    <h2>🎯 All 91 Strategies</h2>
    <div class="input-group">
        <select id="cat-filter" onchange="filterStrategies()">
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

<!-- STOCK PICK -->
<div id="section-stockpick" style="display:none">
<div class="panel">
    <h2>🎯 StockPick — AI Strategy Matcher</h2>
    <p style="color:#888; margin-bottom:10px;">Enter your stock picks. We'll match them to our best backtested strategy, suggest additional tickers, and show vol-adjusted position sizing. Claude AI reviews the result.</p>
    <div class="input-group">
        <input type="text" id="pick-symbols" placeholder="Tickers separated by commas (e.g. NVDA, AAPL, TSLA)" style="flex:3">
        <input type="number" id="pick-amount" value="100000" min="1000" step="1000" style="width:120px" placeholder="Portfolio $">
        <select id="pick-horizon" style="width:80px">
            <option value="3y" selected>3Y</option>
            <option value="1y">1Y</option>
            <option value="5y">5Y</option>
        </select>
        <button onclick="analyzeStockPick()">🔍 Analyze</button>
    </div>
    <div id="pick-results"></div>
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

<div id="status">⚡ agents-assemble | 91 strategies | 580 tickers</div>

<script>
function esc(s) {
    const d = document.createElement('div');
    d.appendChild(document.createTextNode(s));
    return d.innerHTML;
}
function showSection(name, el) {
    document.querySelectorAll('[id^="section-"]').forEach(s => s.style.display = 'none');
    document.getElementById('section-' + name).style.display = 'block';
    document.querySelectorAll('.nav a').forEach(a => a.classList.remove('active'));
    el.classList.add('active');
}

// Sortable table helper
let leaderboardData = [];
let sortCol = 'return'; let sortAsc = false;

function renderLeaderboard() {
    const sorted = [...leaderboardData].sort((a, b) => {
        const va = a[sortCol] || 0, vb = b[sortCol] || 0;
        return sortAsc ? va - vb : vb - va;
    });
    const arrow = sortAsc ? '▲' : '▼';
    const horizon = document.getElementById('horizon-select').value.toUpperCase();
    const cols = [
        {key:'return', label:horizon + ' Return'}, {key:'sharpe', label:'Sharpe'}, {key:'max_dd', label:'Max DD'}
    ];
    let html = '<table><tr><th>#</th><th>Strategy</th><th>Category</th>';
    cols.forEach(c => {
        const active = sortCol === c.key ? ' style="color:#00ff88;cursor:pointer"' : ' style="cursor:pointer"';
        html += '<th' + active + ' onclick="sortLeaderboard(\'' + c.key + '\')">' + c.label + (sortCol === c.key ? ' ' + arrow : '') + '</th>';
    });
    html += '</tr>';
    sorted.forEach((s, i) => {
        const ret = s.return || 0, sharpe = s.sharpe || 0, max_dd = s.max_dd || 0;
        const retClass = ret > 0 ? 'positive' : 'negative';
        html += '<tr><td>' + (i+1) + '</td><td><b>' + esc(s.name) + '</b></td>'
            + '<td><span class="tag tag-blue">' + esc(s.source) + '</span></td>'
            + '<td class="' + retClass + '">' + (ret*100).toFixed(1) + '%</td>'
            + '<td>' + sharpe.toFixed(2) + '</td>'
            + '<td class="negative">' + (max_dd*100).toFixed(1) + '%</td></tr>';
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
    fetch('/api/leaderboard?horizon=' + horizon).then(r => r.json()).then(data => {
        leaderboardData = data;
        document.getElementById('leaderboard-status').textContent = data.length + ' strategies loaded';
        renderLeaderboard();
    }).catch(e => {
        document.getElementById('leaderboard-status').textContent = '';
        document.getElementById('leaderboard-table').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}
// Load on start
loadLeaderboard();

// Market overview
fetch('/api/market').then(r => r.json()).then(data => {
    let html = '<table><tr><th>Index</th><th>Price</th><th>Change</th></tr>';
    Object.entries(data).forEach(([sym, info]) => {
        const cls = info.change >= 0 ? 'positive' : 'negative';
        html += '<tr><td>' + sym + '</td><td>$' + info.price.toFixed(2) + '</td>'
            + '<td class="' + cls + '">' + (info.change >= 0 ? '+' : '') + (info.change*100).toFixed(1) + '%</td></tr>';
    });
    html += '</table>';
    document.getElementById('market-overview').innerHTML = html;
}).catch(e => {
    document.getElementById('market-overview').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
});

function scanTicker() {
    const sym = document.getElementById('scan-ticker').value.toUpperCase();
    document.getElementById('scan-results').innerHTML = '<p class="loading">Scanning ' + sym + '...</p>';
    fetch('/api/scan/' + encodeURIComponent(sym)).then(r => r.json()).then(data => {
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
    fetch('/api/catalyst/' + encodeURIComponent(sym)).then(r => r.json()).then(data => {
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
    fetch('/api/chart/' + encodeURIComponent(sym) + '?start=' + encodeURIComponent(start)).then(r => r.json()).then(data => {
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
    fetch('/api/trade-plan/' + strat + '?amount=' + amt).then(r => r.json()).then(data => {
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
    fetch('/api/execute-trade/' + strat, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({amount: parseFloat(amt)})}).then(r => r.json()).then(data => {
        let html = '<h3 style="color:#ff4444">⚡ EXECUTION RESULT: ' + strat + '</h3>';
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
            const links = (p.tradingview_url ? '<a href="' + encodeURI(p.tradingview_url) + '" target="_blank">TV</a>' : '')
                + (p.yahoo_url ? ' <a href="' + encodeURI(p.yahoo_url) + '" target="_blank">YF</a>' : '');
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

function analyzeStockPick() {
    const syms = document.getElementById('pick-symbols').value.toUpperCase().trim();
    const amt = document.getElementById('pick-amount').value;
    const horizon = document.getElementById('pick-horizon').value;
    if (!syms) { document.getElementById('pick-results').innerHTML = '<p class="negative">Enter at least one ticker.</p>'; return; }
    document.getElementById('pick-results').innerHTML = '<p class="loading">Analyzing your picks... matching strategies, running backtests, asking Claude — ~30s</p>';
    fetch('/api/stock-pick?symbols=' + encodeURIComponent(syms) + '&amount=' + amt + '&horizon=' + horizon + '&top_n=5')
    .then(r => r.json()).then(data => {
        if (data.error) { document.getElementById('pick-results').innerHTML = '<p class="negative">' + esc(data.error) + '</p>'; return; }
        pickData = data;
        pickRecs = shuffleArray(data.recommendations || []);
        pickIdx = 0;
        pickCycleCount = 0;
        showPickResult();
    }).catch(e => {
        document.getElementById('pick-results').innerHTML = '<p class="negative">Error: ' + esc(String(e)) + '</p>';
    });
}

// Load all strategies list
function loadStrategies() {
    document.getElementById('all-strategies').innerHTML = '<p class="loading">Loading...</p>';
    fetch('/api/strategies').then(r => r.json()).then(data => {
        let html = '<table><tr><th>Strategy</th><th>Category</th><th>Universe Size</th><th>Rebalance</th><th>Risk</th></tr>';
        const filter = document.getElementById('cat-filter').value;
        data.forEach(s => {
            if (filter && s.source !== filter) return;
            html += '<tr><td><b>' + esc(s.name) + '</b></td>'
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
function filterStrategies() { loadStrategies(); }

// Auto-load strategies when switching to that tab
document.querySelector('[onclick*="strategies"]').addEventListener('click', () => setTimeout(loadStrategies, 100));
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

@app.route("/api/strategies")
def api_strategies():
    """List all strategies with metadata — no backtesting, instant response."""
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
                if math.isfinite(last) and math.isfinite(change):
                    data[sym] = {"price": last, "change": change}
        except Exception:
            pass
    if data:
        merged = _market_cache.get("data", {}).copy()
        merged.update(data)
        _market_cache["data"] = merged
        _market_cache["ts"] = time.monotonic()
        return jsonify(merged)
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
        if bts:
            best_key = max(bts, key=lambda k: bts[k].total_return)
            best_dict = bts[best_key].to_dict()
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

    return jsonify({"strategy": strategy, "orders": orders, "amount": amount})


@app.route("/api/stock-pick")
def api_stock_pick():
    """StockPick: Analyze user stock picks, match to strategy, generate recs."""
    raw = request.args.get("symbols", "")
    symbols = [s.strip().upper() for s in raw.split(",") if s.strip()]
    if not symbols:
        return jsonify({"error": "No symbols provided. Enter tickers separated by commas."}), 400
    # Validate each symbol
    for s in symbols:
        if not re.match(r'^[A-Z0-9.\-^=]{1,15}$', s):
            return jsonify({"error": f"Invalid ticker: {s}"}), 400
    if len(symbols) > 20:
        return jsonify({"error": "Maximum 20 tickers at once"}), 400

    try:
        amount = float(request.args.get("amount", 100000))
    except (ValueError, TypeError):
        amount = 100000
    if amount <= 0 or not math.isfinite(amount):
        amount = 100000

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


@app.route("/api/execute-trade/<strategy>", methods=["POST"])
def api_execute_trade(strategy):
    """LIVE trade execution via Public.com API. Requires PUBLIC_API_SECRET."""
    if not _STRATEGY_RE.match(strategy):
        return jsonify({"error": "Invalid strategy name"}), 400
    import os
    if not os.environ.get("PUBLIC_API_SECRET"):
        return jsonify({"error": "PUBLIC_API_SECRET not set. Go to public.com/settings/security/api to get your key, then: export PUBLIC_API_SECRET=your_key"}), 403

    body = request.get_json(silent=True) or {}
    try:
        amount = float(body.get("amount", request.args.get("amount", 100000)))
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

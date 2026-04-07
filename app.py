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

import io
import json
import base64
import sys
from datetime import datetime
from pathlib import Path

from flask import Flask, render_template_string, request, jsonify

sys.path.insert(0, str(Path(__file__).parent))

app = Flask(__name__)

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
        <a href="#" class="active" onclick="showSection('dashboard')">Dashboard</a>
        <a href="#" onclick="showSection('strategies')">Strategies</a>
        <a href="#" onclick="showSection('catalyst')">Catalyst Scanner</a>
        <a href="#" onclick="showSection('charts')">Charts</a>
        <a href="#" onclick="showSection('trade')">Trade</a>
    </div>
</div>

<div class="container">

<!-- DASHBOARD -->
<div id="section-dashboard">
<div class="grid">
    <div class="panel full">
        <h2>📊 Strategy Leaderboard — 3Y (2022-2024) | Return + Sharpe + Max DD</h2>
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

<!-- TRADE -->
<div id="section-trade" style="display:none">
<div class="panel">
    <h2>💰 Trade Execution (Public.com)</h2>
    <p style="color:#ff4444; margin-bottom:10px;">⚠️ DISCLAIMER: This is not financial advice. Past performance does not predict future results. Trade at your own risk.</p>
    <div class="input-group">
        <select id="trade-strategy">
            <option value="momentum_crash_hedge">Momentum Crash-Hedged</option>
            <option value="concentrate_winners">Concentrate Winners</option>
            <option value="ai_revolution">AI Revolution</option>
            <option value="barbell_portfolio">Barbell Portfolio</option>
            <option value="nancy_pelosi">Nancy Pelosi</option>
        </select>
        <button onclick="generateTradePlan()">Generate Trade Plan (Dry Run)</button>
    </div>
    <div id="trade-results"></div>
</div>
</div>

</div>

<div id="status">⚡ agents-assemble | 91 strategies | 580 tickers</div>

<script>
function showSection(name) {
    document.querySelectorAll('[id^="section-"]').forEach(el => el.style.display = 'none');
    document.getElementById('section-' + name).style.display = 'block';
    document.querySelectorAll('.nav a').forEach(a => a.classList.remove('active'));
    event.target.classList.add('active');
}

// Load leaderboard on start
fetch('/api/leaderboard').then(r => r.json()).then(data => {
    let html = '<table><tr><th>#</th><th>Strategy</th><th>Category</th><th>3Y Return</th><th>3Y Sharpe</th><th>3Y Max DD</th></tr>';
    data.forEach((s, i) => {
        const retClass = s.return > 0 ? 'positive' : 'negative';
        html += '<tr><td>' + (i+1) + '</td><td><b>' + s.name + '</b></td>'
            + '<td><span class="tag tag-blue">' + s.source + '</span></td>'
            + '<td class="' + retClass + '">' + (s.return*100).toFixed(1) + '%</td>'
            + '<td>' + s.sharpe.toFixed(2) + '</td>'
            + '<td class="negative">' + (s.max_dd*100).toFixed(1) + '%</td></tr>';
    });
    html += '</table>';
    document.getElementById('leaderboard-table').innerHTML = html;
});

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
});

function scanTicker() {
    const sym = document.getElementById('scan-ticker').value.toUpperCase();
    document.getElementById('scan-results').innerHTML = '<p class="loading">Scanning ' + sym + '...</p>';
    fetch('/api/scan/' + sym).then(r => r.json()).then(data => {
        let html = '<h3>' + sym + ' — ' + data.industry + '</h3>';
        if (data.best) {
            html += '<p><span class="tag tag-green">' + data.best.strategy + '</span> '
                + 'Win: ' + (data.best.win_rate*100).toFixed(0) + '% | '
                + 'Return: <span class="positive">' + (data.best.total_return*100).toFixed(1) + '%</span></p>';
        }
        if (data.patterns) {
            html += '<p>Events: ' + data.patterns.total_events + ' (' + data.patterns.up_events + '↑ ' + data.patterns.down_events + '↓)</p>';
        }
        document.getElementById('scan-results').innerHTML = html;
    }).catch(e => {
        document.getElementById('scan-results').innerHTML = '<p class="negative">Error: ' + e + '</p>';
    });
}

function runCatalyst() {
    const sym = document.getElementById('catalyst-ticker').value.toUpperCase();
    document.getElementById('catalyst-results').innerHTML = '<p class="loading">Analyzing ' + sym + '... (this takes ~30s)</p>';
    fetch('/api/catalyst/' + sym).then(r => r.json()).then(data => {
        let html = '<h3>' + sym + ' — ' + (data.industry || 'general') + '</h3>';
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
                    + p.confidence.toUpperCase() + '</span> ' + p.recommended_action + '</p>';
            });
        }
        document.getElementById('catalyst-results').innerHTML = html;
    });
}

function loadChart() {
    const sym = document.getElementById('chart-ticker').value.toUpperCase();
    const start = document.getElementById('chart-start').value;
    document.getElementById('chart-container').innerHTML = '<p class="loading">Generating chart for ' + sym + '...</p>';
    fetch('/api/chart/' + sym + '?start=' + start).then(r => r.json()).then(data => {
        if (data.image) {
            document.getElementById('chart-container').innerHTML = '<img class="chart-img" src="data:image/png;base64,' + data.image + '">';
        }
    });
}

function generateTradePlan() {
    const strat = document.getElementById('trade-strategy').value;
    document.getElementById('trade-results').innerHTML = '<p class="loading">Generating trade plan for ' + strat + '...</p>';
    fetch('/api/trade-plan/' + strat).then(r => r.json()).then(data => {
        let html = '<h3>Trade Plan: ' + strat + ' (DRY RUN)</h3>';
        if (data.orders) {
            html += '<table><tr><th>Action</th><th>Symbol</th><th>Qty</th><th>~Price</th><th>~Value</th></tr>';
            data.orders.forEach(o => {
                html += '<tr><td><span class="tag tag-' + (o.side === 'BUY' ? 'green' : 'red') + '">' + o.side + '</span></td>'
                    + '<td>' + o.symbol + '</td><td>' + o.quantity + '</td>'
                    + '<td>$' + o.price.toFixed(2) + '</td>'
                    + '<td>$' + (o.quantity * o.price).toFixed(0) + '</td></tr>';
            });
            html += '</table>';
        }
        document.getElementById('trade-results').innerHTML = html;
    });
}

function loadStrategies() { /* reload */ location.reload(); }
function filterStrategies() { /* TODO: client-side filter */ }
</script>
</body>
</html>
"""

# ---------------------------------------------------------------------------
# API Endpoints
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/leaderboard")
def api_leaderboard():
    from run_multi_horizon import run_single, _get_all_strategies
    results = []
    for s in _get_all_strategies():
        r = run_single(s, "3y", "2022-01-01", "2024-12-31", verbose=False)
        if r["status"] == "success":
            m = r["metrics"]
            results.append({
                "name": s["key"], "source": s["source"],
                "return": m.get("total_return", 0),
                "sharpe": m.get("sharpe_ratio", 0),
                "max_dd": m.get("max_drawdown", 0),
            })
    results.sort(key=lambda x: x["return"], reverse=True)
    return jsonify(results[:30])

@app.route("/api/market")
def api_market():
    from data_fetcher import fetch_ohlcv
    indices = {"SPY": "S&P 500", "QQQ": "Nasdaq", "IWM": "Russell 2000",
               "TLT": "Bonds 20Y", "GLD": "Gold"}
    data = {}
    for sym in indices:
        try:
            df = fetch_ohlcv(sym, start="2024-12-01", cache=True)
            if len(df) > 1:
                data[sym] = {
                    "price": float(df["Close"].iloc[-1]),
                    "change": float(df["Close"].iloc[-1] / df["Close"].iloc[-20] - 1) if len(df) > 20 else 0,
                }
        except Exception:
            pass
    return jsonify(data)

@app.route("/api/scan/<symbol>")
def api_scan(symbol):
    from catalyst_analyzer import CatalystAnalyzer
    a = CatalystAnalyzer(symbol.upper())
    patterns = a.analyze_historical_patterns()
    bts = a.backtest_event_strategy()
    best = max(bts.values(), key=lambda b: b.total_return) if bts else None
    return jsonify({
        "symbol": symbol.upper(),
        "industry": a.industry,
        "patterns": {k: v for k, v in patterns.items() if k != "events"},
        "best": best.to_dict() if best else None,
    })

@app.route("/api/catalyst/<symbol>")
def api_catalyst(symbol):
    from catalyst_analyzer import CatalystAnalyzer
    a = CatalystAnalyzer(symbol.upper())
    report = a.full_report()
    return jsonify(report)

@app.route("/api/chart/<symbol>")
def api_chart(symbol):
    from terminal import Terminal
    start = request.args.get("start", "2024-01-01")
    t = Terminal()
    path = t.equity_chart(symbol.upper(), start=start)
    with open(path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode()
    return jsonify({"image": img_b64})

@app.route("/api/trade-plan/<strategy>")
def api_trade_plan(strategy):
    from public_trader import PublicTrader
    trader = PublicTrader(dry_run=True)
    # Get strategy signals
    persona = trader._resolve_strategy(strategy)
    from data_fetcher import fetch_multiple_ohlcv
    from backtester import _compute_rsi, _compute_bollinger, _compute_atr
    import pandas as pd
    import numpy as np

    symbols = persona.config.universe[:15]
    all_data = fetch_multiple_ohlcv(symbols, start="2024-01-01")

    enriched = {}
    prices = {}
    for sym, df in all_data.items():
        if df.empty: continue
        if df.index.tz is not None: df.index = df.index.tz_localize(None)
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
        enriched[sym] = df
        prices[sym] = float(close.iloc[-1])

    from backtester import Portfolio
    portfolio = Portfolio(initial_cash=100000, cash=100000)
    today = pd.Timestamp.now().normalize()
    weights = persona.generate_signals(today, prices, portfolio, enriched)

    orders = []
    for sym, w in sorted(weights.items(), key=lambda x: -x[1]):
        if w > 0 and sym in prices:
            qty = int(100000 * min(w, 0.20) / prices[sym])
            if qty > 0:
                orders.append({"side": "BUY", "symbol": sym, "quantity": qty, "price": prices[sym]})

    return jsonify({"strategy": strategy, "orders": orders})


if __name__ == "__main__":
    print("\\n  ⚡ agents-assemble Trading Terminal")
    print("  Open: http://localhost:8888\\n")
    app.run(host="0.0.0.0", port=8888, debug=False)

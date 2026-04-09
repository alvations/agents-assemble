"""News integration functions to insert into data_fetcher.py after line 876."""

NEWS_CODE = r'''

# ---------------------------------------------------------------------------
# FREE DATA: RSS News (Yahoo Finance + Google News -- no API key needed)
# ---------------------------------------------------------------------------
def _parse_rss_xml(xml_text: str) -> list[dict[str, str]]:
    """Parse RSS XML into list of dicts with title/link/pubDate/description/source."""
    import xml.etree.ElementTree as ET

    items: list[dict[str, str]] = []
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return items

    for item in root.iter("item"):
        entry: dict[str, str] = {}
        title_el = item.find("title")
        if title_el is not None and title_el.text:
            entry["title"] = title_el.text.strip()
        link_el = item.find("link")
        if link_el is not None and link_el.text:
            entry["link"] = link_el.text.strip()
        pub_el = item.find("pubDate")
        if pub_el is not None and pub_el.text:
            entry["pubDate"] = pub_el.text.strip()
        desc_el = item.find("description")
        if desc_el is not None and desc_el.text:
            entry["description"] = desc_el.text.strip()
        source_el = item.find("source")
        if source_el is not None and source_el.text:
            entry["source"] = source_el.text.strip()
        if entry.get("title"):
            items.append(entry)
    return items


def fetch_yahoo_rss_news(symbol: str, max_items: int = 20) -> list[dict[str, Any]]:
    """Fetch news headlines from Yahoo Finance RSS feed (free, no API key).

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        max_items: Maximum number of items to return

    Returns:
        List of dicts with: title, link, published, description, source
    """
    url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={symbol}&region=US&lang=en-US"
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "agents-assemble/1.0"})
        if resp.status_code != 200:
            return []
        raw_items = _parse_rss_xml(resp.text)
        results = []
        for item in raw_items[:max_items]:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "published": item.get("pubDate", ""),
                "description": item.get("description", ""),
                "source": "yahoo_finance",
            })
        return results
    except Exception:
        return []


def fetch_google_news_rss(
    symbol: str, max_items: int = 20, topic: str = "stock"
) -> list[dict[str, Any]]:
    """Fetch news headlines from Google News RSS feed (free, no API key).

    Searches Google News for "<symbol> <topic>" and returns RSS results.

    Args:
        symbol: Ticker symbol or company name (e.g. 'AAPL', 'Apple')
        max_items: Maximum number of items to return
        topic: Additional search term (default: 'stock')

    Returns:
        List of dicts with: title, link, published, description, source
    """
    from urllib.parse import quote

    query = quote(f"{symbol} {topic}")
    url = f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "agents-assemble/1.0"})
        if resp.status_code != 200:
            return []
        raw_items = _parse_rss_xml(resp.text)
        results = []
        for item in raw_items[:max_items]:
            results.append({
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "published": item.get("pubDate", ""),
                "description": item.get("description", ""),
                "source": item.get("source", "google_news"),
            })
        return results
    except Exception:
        return []


def fetch_news_rss(
    symbol: str, max_items: int = 30, sources: list[str] | None = None
) -> list[dict[str, Any]]:
    """Unified RSS news fetcher -- pulls from Yahoo Finance + Google News.

    Free, no API key needed. Deduplicates by title.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        max_items: Maximum total items to return
        sources: List of sources to use. Options: 'yahoo', 'google'.
                 Default: both.

    Returns:
        List of dicts with: title, link, published, description, source
    """
    if sources is None:
        sources = ["yahoo", "google"]

    all_items: list[dict[str, Any]] = []

    if "yahoo" in sources:
        all_items.extend(fetch_yahoo_rss_news(symbol, max_items=max_items))

    if "google" in sources:
        all_items.extend(fetch_google_news_rss(symbol, max_items=max_items))

    # Deduplicate by normalized title
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in all_items:
        key = item["title"].lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(item)

    return unique[:max_items]


# ---------------------------------------------------------------------------
# FREE DATA: SEC EDGAR 8-K filings (material events -- no API key)
# ---------------------------------------------------------------------------
def _get_cik_for_symbol(symbol: str) -> str | None:
    """Look up SEC CIK number for a ticker symbol via EDGAR company tickers JSON."""
    cache_file = CACHE_DIR / "sec_company_tickers.json"
    import json

    # Cache the tickers file (~2MB, changes rarely)
    tickers_data = None
    if cache_file.exists():
        age_hours = (time.time() - cache_file.stat().st_mtime) / 3600
        if age_hours < 24:
            try:
                tickers_data = json.loads(cache_file.read_text())
            except Exception:
                pass

    if tickers_data is None:
        try:
            resp = requests.get(
                "https://www.sec.gov/files/company_tickers.json",
                headers=SEC_HEADERS,
                timeout=15,
            )
            if resp.status_code == 200:
                tickers_data = resp.json()
                cache_file.write_text(json.dumps(tickers_data))
        except Exception:
            return None

    if tickers_data is None:
        return None

    sym_upper = symbol.upper()
    for entry in tickers_data.values():
        if entry.get("ticker", "").upper() == sym_upper:
            cik = str(entry.get("cik_str", ""))
            return cik.zfill(10)  # Pad to 10 digits
    return None


def fetch_sec_8k_filings(
    symbol: str, limit: int = 20, days_back: int = 90
) -> list[dict[str, Any]]:
    """Fetch recent 8-K filings (material events) from SEC EDGAR.

    8-K filings report major events: earnings, acquisitions, executive changes,
    debt issuance, bankruptcy, etc. These are the most time-sensitive SEC filings
    and often move stock prices.

    Free, no API key needed. Requires User-Agent header with email.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        limit: Maximum number of filings to return
        days_back: How far back to search (default: 90 days)

    Returns:
        List of dicts with: form_type, filed_date, accession_number,
        primary_document, description, url
    """
    cik = _get_cik_for_symbol(symbol)
    if not cik:
        return []

    # Use EDGAR submissions API (free, no key)
    url = f"https://data.sec.gov/submissions/CIK{cik}.json"
    try:
        resp = requests.get(url, headers=SEC_HEADERS, timeout=15)
        if resp.status_code != 200:
            return []
        data = resp.json()
    except Exception:
        return []

    recent = data.get("filings", {}).get("recent", {})
    if not recent:
        return []

    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    primary_docs = recent.get("primaryDocument", [])
    descriptions = recent.get("primaryDocDescription", [])

    cutoff = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    results = []

    for i in range(min(len(forms), len(dates), len(accessions))):
        form = forms[i] if i < len(forms) else ""
        if not form.startswith("8-K"):
            continue
        filed = dates[i] if i < len(dates) else ""
        if filed < cutoff:
            continue

        acc = accessions[i] if i < len(accessions) else ""
        acc_no_dash = acc.replace("-", "")
        doc = primary_docs[i] if i < len(primary_docs) else ""
        desc = descriptions[i] if i < len(descriptions) else ""

        filing_url = ""
        if doc:
            filing_url = (
                f"https://www.sec.gov/Archives/edgar/data/"
                f"{cik.lstrip('0')}/{acc_no_dash}/{doc}"
            )

        results.append({
            "form_type": form,
            "filed_date": filed,
            "accession_number": acc,
            "primary_document": doc,
            "description": desc,
            "url": filing_url,
            "source": "sec_edgar",
        })

        if len(results) >= limit:
            break

    return results


# ---------------------------------------------------------------------------
# FREE DATA: Reddit sentiment (read-only JSON, no API key)
# ---------------------------------------------------------------------------
_REDDIT_HEADERS = {"User-Agent": "agents-assemble/1.0 (financial research)"}

_FINANCE_SUBREDDITS = [
    "wallstreetbets",
    "stocks",
    "investing",
    "options",
    "SecurityAnalysis",
]


def fetch_reddit_posts(
    symbol: str,
    subreddits: list[str] | None = None,
    max_per_sub: int = 10,
    sort: str = "new",
) -> list[dict[str, Any]]:
    """Fetch Reddit posts mentioning a ticker from financial subreddits.

    Uses Reddit's public JSON endpoint (no API key needed).
    Appends .json to subreddit search URL.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        subreddits: List of subreddit names. Default: WSB, stocks, investing, etc.
        max_per_sub: Max posts per subreddit
        sort: Sort order: 'new', 'hot', 'top', 'relevance'

    Returns:
        List of dicts with: title, body, score, num_comments, created_utc,
        subreddit, url, source
    """
    if subreddits is None:
        subreddits = _FINANCE_SUBREDDITS

    all_posts: list[dict[str, Any]] = []

    for sub in subreddits:
        url = f"https://www.reddit.com/r/{sub}/search.json"
        params = {
            "q": f"${symbol} OR {symbol}",
            "restrict_sr": "on",
            "sort": sort,
            "t": "week",
            "limit": max_per_sub,
        }
        try:
            resp = requests.get(
                url, params=params, headers=_REDDIT_HEADERS, timeout=15
            )
            if resp.status_code != 200:
                continue
            data = resp.json()
            children = data.get("data", {}).get("children", [])
            for child in children:
                post = child.get("data", {})
                all_posts.append({
                    "title": post.get("title", ""),
                    "body": (post.get("selftext", "") or "")[:500],
                    "score": post.get("score", 0),
                    "num_comments": post.get("num_comments", 0),
                    "created_utc": post.get("created_utc", 0),
                    "subreddit": post.get("subreddit", sub),
                    "url": f"https://reddit.com{post.get('permalink', '')}",
                    "source": "reddit",
                })
        except Exception:
            continue

    all_posts.sort(key=lambda x: x.get("score", 0), reverse=True)
    return all_posts


def fetch_reddit_sentiment(symbol: str) -> dict[str, Any]:
    """Estimate Reddit sentiment for a ticker from financial subreddits.

    Uses keyword-based sentiment scoring on post titles/bodies.
    No API key needed -- uses Reddit's public JSON endpoints.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')

    Returns:
        Dict with: symbol, total_mentions, avg_score, avg_comments,
        sentiment_score (-1 to 1), sentiment_label, top_posts, subreddit_breakdown
    """
    posts = fetch_reddit_posts(symbol, max_per_sub=25)

    if not posts:
        return {
            "symbol": symbol,
            "total_mentions": 0,
            "sentiment_score": 0.0,
            "sentiment_label": "neutral",
            "avg_score": 0,
            "avg_comments": 0,
            "top_posts": [],
            "subreddit_breakdown": {},
        }

    bullish_words = {
        "buy", "calls", "long", "moon", "rocket", "bullish", "undervalued",
        "breakout", "squeeze", "yolo", "diamond", "hands", "tendies",
        "gamma", "rip", "surge", "rally", "beat", "upgrade", "upside",
        "strong", "growth", "outperform", "accumulate", "conviction",
    }
    bearish_words = {
        "sell", "puts", "short", "bear", "crash", "dump", "overvalued",
        "bubble", "rug", "pull", "tank", "drop", "miss", "downgrade",
        "weak", "decline", "underperform", "avoid", "risk", "bag",
        "holder", "loss", "dead", "falling", "knife", "recession",
    }

    scores = []
    sub_counts: dict[str, int] = {}

    for post in posts:
        text = f"{post['title']} {post['body']}".lower()
        bull_count = sum(1 for w in bullish_words if w in text)
        bear_count = sum(1 for w in bearish_words if w in text)
        total_kw = bull_count + bear_count
        if total_kw > 0:
            sentiment = (bull_count - bear_count) / total_kw
        else:
            sentiment = 0.0
        weight = 1 + math.log1p(max(post.get("score", 0), 0))
        scores.append(sentiment * weight)

        sub = post.get("subreddit", "unknown")
        sub_counts[sub] = sub_counts.get(sub, 0) + 1

    avg_sentiment = sum(scores) / len(scores) if scores else 0.0
    avg_sentiment = max(-1.0, min(1.0, avg_sentiment))

    if avg_sentiment > 0.15:
        label = "bullish"
    elif avg_sentiment < -0.15:
        label = "bearish"
    else:
        label = "neutral"

    avg_score = sum(p.get("score", 0) for p in posts) / len(posts) if posts else 0
    avg_comments = (
        sum(p.get("num_comments", 0) for p in posts) / len(posts) if posts else 0
    )

    return {
        "symbol": symbol,
        "total_mentions": len(posts),
        "sentiment_score": round(avg_sentiment, 3),
        "sentiment_label": label,
        "avg_score": round(avg_score, 1),
        "avg_comments": round(avg_comments, 1),
        "top_posts": [
            {"title": p["title"], "score": p["score"], "subreddit": p["subreddit"]}
            for p in posts[:5]
        ],
        "subreddit_breakdown": sub_counts,
    }


# ---------------------------------------------------------------------------
# FREE DATA: StockTwits social sentiment (no API key needed)
# ---------------------------------------------------------------------------
def fetch_stocktwits_sentiment(
    symbol: str, max_messages: int = 30
) -> dict[str, Any]:
    """Fetch StockTwits sentiment for a ticker (free, no API key).

    StockTwits is a social network for traders. Users tag messages as
    Bullish/Bearish, providing crowd-sourced sentiment data.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        max_messages: Max messages to analyze (API returns up to 30)

    Returns:
        Dict with: symbol, total_messages, bullish_count, bearish_count,
        sentiment_ratio, sentiment_label, sample_messages
    """
    url = f"https://api.stocktwits.com/api/2/streams/symbol/{symbol}.json"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code != 200:
            return {
                "symbol": symbol, "total_messages": 0,
                "sentiment_label": "unavailable",
            }
        data = resp.json()
    except Exception:
        return {
            "symbol": symbol, "total_messages": 0,
            "sentiment_label": "unavailable",
        }

    messages = data.get("messages", [])[:max_messages]
    if not messages:
        return {"symbol": symbol, "total_messages": 0, "sentiment_label": "neutral"}

    bullish = 0
    bearish = 0
    samples = []

    for msg in messages:
        sentiment = msg.get("entities", {}).get("sentiment", {})
        if isinstance(sentiment, dict):
            basic = sentiment.get("basic", "")
        else:
            basic = ""

        if basic == "Bullish":
            bullish += 1
        elif basic == "Bearish":
            bearish += 1

        if len(samples) < 5:
            samples.append({
                "body": (msg.get("body", "") or "")[:200],
                "sentiment": basic or "neutral",
                "created_at": msg.get("created_at", ""),
            })

    total_tagged = bullish + bearish
    ratio = bullish / total_tagged if total_tagged > 0 else 0.5

    if ratio > 0.6:
        label = "bullish"
    elif ratio < 0.4:
        label = "bearish"
    else:
        label = "neutral"

    return {
        "symbol": symbol,
        "total_messages": len(messages),
        "bullish_count": bullish,
        "bearish_count": bearish,
        "sentiment_ratio": round(ratio, 3),
        "sentiment_label": label,
        "sample_messages": samples,
    }


# ---------------------------------------------------------------------------
# AGGREGATORS: Unified news + sentiment across all free sources
# ---------------------------------------------------------------------------
def fetch_all_news(
    symbol: str,
    sources: list[str] | None = None,
    max_items: int = 50,
) -> list[dict[str, Any]]:
    """Fetch news from ALL available free sources, deduplicated.

    Args:
        symbol: Ticker symbol (e.g. 'AAPL')
        sources: List of sources. Options: 'yahoo_rss', 'google_rss',
                 'yfinance', 'finnhub', 'reddit', 'sec_8k'.
                 Default: all free sources (yfinance + RSS + SEC).
        max_items: Maximum total items

    Returns:
        List of dicts with: title, link, published, description, source
    """
    if sources is None:
        sources = ["yahoo_rss", "google_rss", "yfinance", "sec_8k"]
        if get_api_key("FINNHUB_API_KEY"):
            sources.append("finnhub")

    all_items: list[dict[str, Any]] = []

    if "yahoo_rss" in sources:
        all_items.extend(fetch_yahoo_rss_news(symbol, max_items=20))

    if "google_rss" in sources:
        all_items.extend(fetch_google_news_rss(symbol, max_items=20))

    if "yfinance" in sources:
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            for n in (ticker.news or [])[:20]:
                ts = n.get("providerPublishTime", 0)
                pub = ""
                if ts and ts > 946684800:
                    try:
                        pub = datetime.utcfromtimestamp(ts).strftime(
                            "%a, %d %b %Y %H:%M:%S +0000"
                        )
                    except Exception:
                        pass
                all_items.append({
                    "title": n.get("title", ""),
                    "link": n.get("link", ""),
                    "published": pub,
                    "description": "",
                    "source": "yfinance",
                })
        except Exception:
            pass

    if "finnhub" in sources:
        try:
            news = fetch_finnhub_news(symbol)
            for n in news[:20]:
                ts = n.get("datetime", 0)
                pub = ""
                if ts and ts > 946684800:
                    try:
                        pub = datetime.utcfromtimestamp(ts).strftime(
                            "%a, %d %b %Y %H:%M:%S +0000"
                        )
                    except Exception:
                        pass
                all_items.append({
                    "title": n.get("headline", ""),
                    "link": n.get("url", ""),
                    "published": pub,
                    "description": n.get("summary", ""),
                    "source": "finnhub",
                })
        except Exception:
            pass

    if "reddit" in sources:
        posts = fetch_reddit_posts(symbol, max_per_sub=5)
        for p in posts[:15]:
            ts = p.get("created_utc", 0)
            pub = ""
            if ts:
                try:
                    pub = datetime.utcfromtimestamp(ts).strftime(
                        "%a, %d %b %Y %H:%M:%S +0000"
                    )
                except Exception:
                    pass
            all_items.append({
                "title": p.get("title", ""),
                "link": p.get("url", ""),
                "published": pub,
                "description": p.get("body", "")[:200],
                "source": f"reddit/{p.get('subreddit', '')}",
            })

    if "sec_8k" in sources:
        filings = fetch_sec_8k_filings(symbol, limit=10)
        for f in filings:
            all_items.append({
                "title": f"8-K Filing: {f.get('description', 'Material Event')}",
                "link": f.get("url", ""),
                "published": f.get("filed_date", ""),
                "description": f"SEC 8-K filed {f.get('filed_date', '')}",
                "source": "sec_edgar",
            })

    # Deduplicate by normalized title
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for item in all_items:
        key = item.get("title", "").lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(item)

    return unique[:max_items]


def fetch_aggregate_sentiment(symbol: str) -> dict[str, Any]:
    """Aggregate sentiment across all available free sources.

    Combines: Reddit sentiment, StockTwits sentiment, Finnhub social sentiment
    (if API key set), and basic news headline sentiment.

    Args:
        symbol: Ticker symbol

    Returns:
        Dict with: symbol, overall_sentiment (-1 to 1), overall_label,
        sources (per-source sentiment breakdown), news_count
    """
    sources_data: dict[str, dict[str, Any]] = {}
    weighted_scores: list[tuple[float, float]] = []  # (score, weight)

    # Reddit sentiment (weight: 1.0)
    try:
        reddit = fetch_reddit_sentiment(symbol)
        if reddit.get("total_mentions", 0) > 0:
            sources_data["reddit"] = {
                "sentiment_score": reddit["sentiment_score"],
                "sentiment_label": reddit["sentiment_label"],
                "mentions": reddit["total_mentions"],
            }
            weighted_scores.append((reddit["sentiment_score"], 1.0))
    except Exception:
        pass

    # StockTwits sentiment (weight: 1.5 -- tagged sentiment is more reliable)
    try:
        st = fetch_stocktwits_sentiment(symbol)
        if (st.get("total_messages", 0) > 0
                and st.get("sentiment_label") != "unavailable"):
            st_score = (st.get("sentiment_ratio", 0.5) - 0.5) * 2
            sources_data["stocktwits"] = {
                "sentiment_score": round(st_score, 3),
                "sentiment_label": st["sentiment_label"],
                "messages": st["total_messages"],
                "bullish": st.get("bullish_count", 0),
                "bearish": st.get("bearish_count", 0),
            }
            weighted_scores.append((st_score, 1.5))
    except Exception:
        pass

    # Finnhub social sentiment (weight: 1.0)
    fh_key = get_api_key("FINNHUB_API_KEY")
    if fh_key:
        try:
            fh = fetch_finnhub_sentiment(symbol)
            if fh:
                reddit_data = fh.get("reddit", [])
                if reddit_data:
                    latest = (
                        reddit_data[-1] if isinstance(reddit_data, list) else {}
                    )
                    pos = latest.get("positiveMention", 0)
                    neg = latest.get("negativeMention", 0)
                    total_m = pos + neg
                    if total_m > 0:
                        fh_score = (pos - neg) / total_m
                        sources_data["finnhub"] = {
                            "sentiment_score": round(fh_score, 3),
                            "positive_mentions": pos,
                            "negative_mentions": neg,
                        }
                        weighted_scores.append((fh_score, 1.0))
        except Exception:
            pass

    # News headline sentiment (weight: 0.5 -- basic keyword approach)
    try:
        news = fetch_news_rss(symbol, max_items=20)
        if news:
            positive = {
                "beat", "surge", "rally", "upgrade", "buy", "growth",
                "profit", "record", "strong", "outperform", "raise",
                "bullish", "gain", "up", "positive", "exceed", "above",
            }
            negative = {
                "miss", "crash", "decline", "downgrade", "sell", "loss",
                "weak", "cut", "bearish", "drop", "below", "warning",
                "risk", "concern", "fear", "negative", "layoff", "recall",
            }
            bull = 0
            bear = 0
            for n in news:
                title = n.get("title", "").lower()
                bull += sum(1 for w in positive if w in title)
                bear += sum(1 for w in negative if w in title)
            total_kw = bull + bear
            if total_kw > 0:
                news_score = (bull - bear) / total_kw
                sources_data["news_headlines"] = {
                    "sentiment_score": round(news_score, 3),
                    "articles_analyzed": len(news),
                    "positive_signals": bull,
                    "negative_signals": bear,
                }
                weighted_scores.append((news_score, 0.5))
    except Exception:
        pass

    # Calculate weighted average
    if weighted_scores:
        total_weight = sum(w for _, w in weighted_scores)
        overall = sum(s * w for s, w in weighted_scores) / total_weight
        overall = max(-1.0, min(1.0, overall))
    else:
        overall = 0.0

    if overall > 0.15:
        label = "bullish"
    elif overall < -0.15:
        label = "bearish"
    else:
        label = "neutral"

    return {
        "symbol": symbol,
        "overall_sentiment": round(overall, 3),
        "overall_label": label,
        "sources": sources_data,
        "news_count": sum(
            v.get("mentions", 0) + v.get("messages", 0)
            + v.get("articles_analyzed", 0)
            for v in sources_data.values()
        ),
    }


# ---------------------------------------------------------------------------
# FREE DATA: Market events calendar (FRED releases)
# ---------------------------------------------------------------------------
def fetch_market_events(days_ahead: int = 14) -> list[dict[str, Any]]:
    """Fetch upcoming economic data releases from FRED.

    Requires FRED_API_KEY env var (free registration at fred.stlouisfed.org).
    Falls back to a static calendar of major recurring events if no key.

    Args:
        days_ahead: Number of days to look ahead

    Returns:
        List of dicts with: name, date, description, source
    """
    fred_key = get_api_key("FRED_API_KEY")

    if fred_key:
        today = datetime.now().strftime("%Y-%m-%d")
        end = (datetime.now() + timedelta(days=days_ahead)).strftime("%Y-%m-%d")
        url = "https://api.stlouisfed.org/fred/releases/dates"
        params = {
            "api_key": fred_key,
            "file_type": "json",
            "realtime_start": today,
            "realtime_end": end,
            "include_release_dates_with_no_data": "false",
        }
        try:
            resp = requests.get(url, params=params, timeout=15)
            if resp.status_code == 200:
                data = resp.json()
                events = []
                for release in data.get("release_dates", []):
                    events.append({
                        "name": (
                            f"FRED Release #{release.get('release_id', '?')}"
                        ),
                        "date": release.get("date", ""),
                        "description": release.get(
                            "release_name", "Economic data release"
                        ),
                        "source": "fred",
                    })
                return events
        except Exception:
            pass

    # Fallback: static calendar of major recurring US economic events
    now = datetime.now()
    events = []
    major_events = [
        ("FOMC Rate Decision", "Federal Reserve interest rate decision",
         [1, 3, 5, 6, 7, 9, 11, 12]),
        ("CPI Report", "Consumer Price Index -- inflation measure",
         list(range(1, 13))),
        ("Jobs Report (NFP)", "Non-Farm Payrolls -- first Friday of month",
         list(range(1, 13))),
        ("GDP Report", "Gross Domestic Product -- quarterly",
         [1, 4, 7, 10]),
        ("PCE Price Index",
         "Personal Consumption Expenditures -- Fed preferred inflation gauge",
         list(range(1, 13))),
        ("ISM Manufacturing",
         "ISM Manufacturing PMI -- first business day of month",
         list(range(1, 13))),
        ("Retail Sales", "Monthly retail sales data",
         list(range(1, 13))),
        ("Housing Starts", "New residential construction",
         list(range(1, 13))),
    ]
    for name, desc, months in major_events:
        for m in months:
            event_date = (
                now.replace(month=m, day=15) if m != now.month
                else now + timedelta(days=7)
            )
            try:
                delta = (event_date - now).days
                if 0 <= delta <= days_ahead:
                    events.append({
                        "name": name,
                        "date": event_date.strftime("%Y-%m-%d"),
                        "description": desc,
                        "source": "static_calendar",
                    })
            except (ValueError, OverflowError):
                pass

    return sorted(events, key=lambda x: x.get("date", ""))

'''

if __name__ == "__main__":
    # Insert after line 876 in data_fetcher.py
    with open("data_fetcher.py", "r") as f:
        lines = f.readlines()

    # Find the insertion point: after "    return []" that ends fetch_sec_filings
    # and before "# FREE DATA: Earnings calendar"
    insert_after = None
    for i, line in enumerate(lines):
        if (line.strip() == "# FREE DATA: Earnings calendar and analyst estimates (yfinance)"
                and i > 0
                and lines[i-1].strip().startswith("# ----")):
            insert_after = i - 1  # Before the "# ----" line
            break

    if insert_after is None:
        print("ERROR: Could not find insertion point")
        exit(1)

    print(f"Inserting after line {insert_after + 1}")

    new_lines = lines[:insert_after] + [NEWS_CODE + "\n"] + lines[insert_after:]

    with open("data_fetcher.py", "w") as f:
        f.writelines(new_lines)

    # Verify AST
    import ast
    with open("data_fetcher.py") as f:
        code = f.read()
    ast.parse(code)
    print(f"SUCCESS: AST valid, {code.count(chr(10))} lines")

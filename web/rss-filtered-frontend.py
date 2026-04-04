import requests
import feedparser
import json
import html
from pathlib import Path
from datetime import datetime, timedelta
from tqdm import tqdm

# ── FEED CONFIG ──
# Feeds organized by category for the dashboard layout.
# Add/remove feeds and categories as you like.
feed_categories = {
    "sports": {
        "title": "Sports",
        "description": "Sports news and analysis",
        "color": "#03edf9",
        "feeds": {
            "Aaron Blackshear": "https://strictlyforbuckets.com/blog/index.xml",
            "Kansas City Royals – MLB Trade Rumors": "https://www.mlbtraderumors.com/kansas-city-royals/feed/atom",
            "Mike Tanier": "https://miketanier.substack.com/feed",
            "Neil's Substack": "https://neilpaine.substack.com/feed",
            "Royals Data Dugout": "https://royalsdatadugout.substack.com/feed",
            "Royals Review -  All Posts": "https://www.royalsreview.com/rss/index.xml",
            "Royals – FanGraphs Baseball": "https://www.fangraphs.com/blogs/category/teams/royals/feed/",
            "SportsLogos.Net News": "https://news.sportslogos.net/feed/",
            "How Gambling Works": "https://howgamblingworks.substack.com/feed",
        },
    },
    "news": {
        "title": "News & Politics",
        "description": "Breaking news, politics, and current affairs",
        "color": "#ff7edb",
        "feeds": {
            "amanda_marcotte": "https://politepol.com/fd/qbzvP6fNF3Qn.xml",
            "The American Pamphleteer": "https://ladylibertie.substack.com/feed",
            "The Downballot": "https://www.the-downballot.com/feed",
            "Kansas Reflector": "https://kansasreflector.com/feed/",
            "The Nation- Electoral Reform": "https://www.thenation.com/feed/?post_type=article&subject=electoral-reform",
            "Oligarch Watch": "https://oligarchwatch.substack.com/feed",
            "Olivia Julianna": "https://oliviajulianna.substack.com/feed",
            "Polymarket": "https://news.polymarket.com/feed",
            "Press Watchers": "https://presswatchers.org/feed/",
            "Sabatos Crystal Ball": "https://centerforpolitics.org/crystalball/feed/",
            "Status Kuo": "https://statuskuo.substack.com/feed",
            "Teen Vogue": "https://politepol.com/fd/Vjc601sG0jpO.xml",
            "Unraveled": "https://unraveledpress.com/rss.xml",
        },
    },
    "law": {
        "title": "Law",
        "description": "Legal news and analysis",
        "color": "#fede5d",
        "feeds": {
            "/dev/lawyer": "https://writing.kemitchell.com/feed.xml",
            "Above the Law": "https://abovethelaw.com/feed/",
            "The Nation- Supreme Court": "https://www.thenation.com/feed/?post_type=article&subject=supreme-court",
            "Techdirt": "https://www.techdirt.com/feed/",
        },
    },
    "tech": {
        "title": "Tech & Dev",
        "description": "Technology, development, and tools",
        "color": "#72f1b8",
        "feeds": {
            "Brett Terpstra": "http://brett.trpstra.net/brettterpstra",
            "Ed Zitrons Wheres Your Ed At": "https://www.wheresyoured.at/feed",
            "Emacs- George Supreeth": "https://georgesupreeth.com/web/feed.xml",
            "LinuxLinks": "https://www.linuxlinks.com/feed/",
            "Ludic": "https://ludic.mataroa.blog/rss/",
            "The New Stack": "https://thenewstack.io/blog/feed/",
            "Newsletters- Tech": "https://kill-the-newsletter.com/feeds/527km9xxoq0vonzops4m.xml",
            "Shellsharks Feeds": "https://shellsharks.com/feeds/feed.xml",
            "Terminal Trove": "https://terminaltrove.com/blog.xml",
        },
    },
    "culture": {
        "title": "Culture & Newsletters",
        "description": "Writing, culture, food, and newsletters",
        "color": "#c084fc",
        "feeds": {
            "Amanda's Mild Takes": "https://amandasmildtakes.substack.com/feed",
            "The Baffler": "https://thebaffler.com/homepage/feed",
            "Bicycle For Your Mind": "https://bicycleforyourmind.com/feed.rss",
            "bitches gotta eat!": "https://bitchesgottaeat.substack.com/feed",
            "Dan Hon": "https://newsletter.danhon.com/rss.xml",
            "Dan Sinkers Blog": "https://dansinker.com/feed.xml",
            "Danny Funt+": "https://dannyfunt.substack.com/feed",
            "Gin and Tacos": "http://www.ginandtacos.com/feed/",
            "How Things Work": "https://www.hamiltonnolan.com/feed",
            "I Love Typography": "https://ilovetypography.com/feed/",
            "KCUR- Local Food ": "https://www.kcur.org/tags/local-food.rss",
            "The Linkfest": "https://buttondown.com/clivethompson/rss",
            "Newsletters- Current Events": "https://kill-the-newsletter.com/feeds/jnggh1214ov2zpew9383.xml",
            "Newsletters- Misc": "https://kill-the-newsletter.com/feeds/5mr68b7cb43ac2h04ai5.xml",
            "Raygun": "https://www.raygunsite.com/blogs/news.atom",
            "Recomendo": "https://www.recomendo.com/feed",
            "Roads & Kingdoms": "https://roadsandkingdoms.com/feed/",
            "STAT": "https://www.statnews.com/feed/",
            "The Sunday Long Read": "https://us9.campaign-archive.com/feed?id=67e6e8a504&u=6e1ae4ac632498a38c1d57c54",
            "Tommy Craggs": "https://tommycraggs.com/feed/",
            "Why Is This Interesting?": "https://whyisthisinteresting.substack.com/feed",
        },
    },
    "trivia": {
        "title": "Trivia & Fun",
        "description": "Humor, interesting finds, and fun stuff",
        "color": "#f87171",
        "feeds": {
            "Daily Findings": "https://politepol.com/fd/yWM63dUvklo4.xml",
            "DepthHub": "https://www.reddit.com/r/DepthHub/.rss",
            "Humorism": "https://www.humorism.xyz/rss/",
            "Thunder Dungeon": "https://thunderdungeon.com/feed/",
        },
    },
}

# Keywords per feed: only articles matching these keywords will be shown.
# Feeds not listed here show all articles (no filtering).
feed_keywords = {
    "Above the Law": ["firm", "school"],
    "Best and Worst": ["Kansas", "Royals"],
    "Brett Terpstra": ["Web Excursions"],
    "ContraBandCamp": ["Mailbag"],
    "ebaumsworld": ["spicy", "sex"],
    "Emily in Your Phone": ["Roundup"],
    "Mike Tanier": ["Chiefs"],
    "Neil's Substack": ["The Week That Was"],
    "nrn": ["Menu Tracker"],
    "RotoGraphs Fantasy Baseball": ["Mining The News", "Royals", "Kansas"],
    "Royals Review -  All Posts": ["trade", "draft", "prospects"],
    "Pleated Jeans": ["comic"],
    "Ruin My Week": ["work", "boss", "job", "sex"],
    "STAT": ["adhd", "Vyvanse"],
    "Status Kuo": ["giggles"],
    "Techdirt": ["court", "law", "maga"],
    "The New Stack": ["python"],
    "The Takeout": ["best"],
    "Thunder Dungeon": ["meme dump", "sex"],
    "Why Is This Interesting?": ["Monday Media Diet"],
}


def format_date(entry):
    """Extract and format the publish date from a feed entry."""
    for attr in ("published_parsed", "updated_parsed"):
        parsed = getattr(entry, attr, None)
        if parsed:
            try:
                dt = datetime(*parsed[:6])
                now = datetime.now()
                diff = now - dt
                hours = diff.total_seconds() / 3600
                if hours < 1:
                    return "Just now"
                if hours < 24:
                    return f"{int(hours)}h ago"
                if hours < 168:
                    return f"{int(hours // 24)}d ago"
                return dt.strftime("%b %d")
            except Exception:
                pass
    # Fallback to raw string
    for attr in ("published", "updated"):
        raw = getattr(entry, attr, None)
        if raw:
            return raw[:16]
    return "Recently"


def fetch_feed(site_name, url):
    """Fetch and parse a single RSS feed. Returns list of article dicts."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=True)
        response.raise_for_status()
        feed = feedparser.parse(response.content)

        if feed.bozo:
            print(f"  ⚠ Parse warning for {site_name}: {feed.bozo_exception}")

        entries = feed.entries
        if not entries:
            print(f"  ✗ No entries: {site_name}")
            return []

        # Filter to last 7 days
        one_week_ago = datetime.now() - timedelta(weeks=1)
        recent = []
        for entry in entries[:15]:
            for attr in ("published_parsed", "updated_parsed"):
                parsed = getattr(entry, attr, None)
                if parsed:
                    try:
                        if datetime(*parsed[:6]) > one_week_ago:
                            recent.append(entry)
                    except Exception:
                        recent.append(entry)
                    break
            else:
                # No date info — include it anyway
                recent.append(entry)

        if not recent:
            print(f"  ✗ No recent entries: {site_name}")
            return []

        # Build article list
        articles = []
        import re
        for entry in recent[:10]:
            title = getattr(entry, "title", "Untitled") or "Untitled"
            title = re.sub(r"<[^>]*>", "", title).strip()
            link = getattr(entry, "link", "#") or "#"
            pub_date = format_date(entry)
            articles.append({"title": title, "link": link, "pubDate": pub_date})

        # Apply keyword filter
        keywords = feed_keywords.get(site_name, [])
        if keywords:
            import re as re2
            pattern = re2.compile("|".join(keywords), re2.IGNORECASE)
            filtered = [a for a in articles if pattern.search(a["title"])]
            if not filtered:
                print(f"  ✗ No keyword matches: {site_name}")
                return []
            articles = filtered

        print(f"  ✓ {site_name}: {len(articles)} articles")
        return articles

    except requests.exceptions.HTTPError as e:
        print(f"  ✗ HTTP Error for {site_name}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"  ✗ Request Error for {site_name}: {e}")
    except Exception as e:
        print(f"  ✗ Unexpected error for {site_name}: {e}")
    return []


def generate_dashboard_html(feed_data, categories_config):
    """Generate the full dashboard HTML with embedded feed data."""
    timestamp = datetime.now().strftime("%I:%M %p, %b %d %Y")

    # Build the JSON data structure for the frontend
    categories_json = {}
    for cat_key, cat_config in categories_config.items():
        sources = []
        for feed_name in sorted(cat_config["feeds"].keys(), key=lambda x: x.lower().lstrip("the ")):
            articles = feed_data.get(feed_name, [])
            sources.append({
                "name": feed_name,
                "articles": articles,
                "status": "active" if articles else "empty",
            })
        categories_json[cat_key] = {
            "title": cat_config["title"],
            "description": cat_config["description"],
            "color": cat_config["color"],
            "sources": sources,
        }

    data_json = json.dumps(categories_json, ensure_ascii=False)

    # Build tab buttons from categories
    tab_buttons = ''.join(
        f'<button class="tab-btn" onclick="setTab(\'{k}\')">{v["title"]}</button>'
        for k, v in categories_config.items()
    )

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NewsHub</title>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,300;0,400;0,700;1,400&family=Train+One&display=swap" rel="stylesheet">
    <style>
        :root {{
          --pink: #ff7edb;
          --purple: #241b2f;
          --blue: #03edf9;
          --yellow: #fede5d;
          --offwhite: #ffffff;
          --neongreen: #72f1b8;
          --green: #72f1b8;
          --card-bg: rgba(255, 255, 255, 0.02);
          --card-border: rgba(3, 237, 249, 0.3);
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
          background: var(--purple);
          font-family: "Fira Sans", sans-serif;
          font-size: 16px;
          line-height: 1.4;
          color: var(--offwhite);
        }}

        /* ── TOP BAR ── */
        .top-bar {{
          position: sticky; top: 0; z-index: 100;
          background: rgba(36, 27, 47, 0.95);
          backdrop-filter: blur(12px);
          border-bottom: 2px solid var(--blue);
          padding: 0 24px;
          display: flex; align-items: center; justify-content: space-between;
          height: 60px;
        }}
        .top-bar-left {{ display: flex; align-items: center; gap: 20px; }}
        .logo {{
          font-family: "Train One", system-ui;
          font-size: 28px; color: var(--pink); letter-spacing: 2px;
        }}
        .tab-bar {{ display: flex; gap: 4px; flex-wrap: wrap; }}
        .tab-btn {{
          background: transparent; border: 1px solid transparent;
          color: var(--yellow); font-family: "Fira Sans", sans-serif;
          font-size: 13px; font-weight: 700; text-transform: uppercase;
          letter-spacing: 1px; padding: 6px 14px; border-radius: 6px;
          cursor: pointer; transition: all 0.2s;
        }}
        .tab-btn:hover {{ background: rgba(3, 237, 249, 0.1); }}
        .tab-btn.active {{
          background: rgba(3, 237, 249, 0.15);
          border-color: var(--blue); color: var(--blue);
        }}
        .top-bar-right {{ display: flex; align-items: center; gap: 12px; }}
        .search-box {{
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid var(--card-border); border-radius: 8px;
          padding: 8px 14px; color: var(--offwhite);
          font-family: "Fira Sans", sans-serif; font-size: 14px;
          width: 220px; outline: none; transition: border-color 0.2s;
        }}
        .search-box::placeholder {{ color: rgba(255, 255, 255, 0.3); }}
        .search-box:focus {{ border-color: var(--blue); }}

        /* ── STATS BAR ── */
        .stats-bar {{
          padding: 10px 24px; display: flex; align-items: center;
          justify-content: space-between;
          border-bottom: 1px solid rgba(3, 237, 249, 0.15);
          font-size: 13px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
        }}
        .stats-left {{ display: flex; gap: 24px; color: rgba(255, 255, 255, 0.4); }}
        .stats-left strong {{ font-size: 16px; }}
        .stats-right {{ display: flex; align-items: center; gap: 8px; }}
        .filter-btn {{
          background: rgba(255, 255, 255, 0.04);
          border: 1px solid var(--card-border); border-radius: 6px;
          color: var(--yellow); font-family: "Fira Sans", sans-serif;
          font-size: 12px; font-weight: 700; text-transform: uppercase;
          padding: 5px 12px; cursor: pointer; transition: all 0.2s; letter-spacing: 0.5px;
        }}
        .filter-btn:hover {{ border-color: var(--blue); }}
        .view-toggle {{
          display: flex; border: 1px solid var(--card-border);
          border-radius: 6px; overflow: hidden; margin-left: 4px;
        }}
        .view-toggle button {{
          background: transparent; border: none;
          color: rgba(255, 255, 255, 0.3); font-size: 15px;
          padding: 5px 10px; cursor: pointer; transition: all 0.15s;
        }}
        .view-toggle button.active {{ background: rgba(3, 237, 249, 0.15); color: var(--blue); }}

        /* ── DASHBOARD GRID ── */
        .dashboard {{ padding: 20px; max-width: 1500px; margin: 0 auto; }}
        .dashboard.grid-view {{ column-count: 3; column-gap: 18px; }}
        .dashboard.list-view {{ column-count: 1; }}

        /* ── FEED WIDGET ── */
        .feed-widget {{
          break-inside: avoid; margin-bottom: 18px;
          background: var(--card-bg); border: 1px solid var(--card-border);
          border-radius: 10px; overflow: hidden; transition: border-color 0.2s;
        }}
        .feed-widget:hover {{ border-color: var(--neongreen); }}
        .widget-header {{
          display: flex; align-items: center; justify-content: space-between;
          padding: 14px 18px; border-bottom: 1px solid rgba(3, 237, 249, 0.2);
          cursor: pointer; user-select: none; transition: background 0.15s;
        }}
        .widget-header:hover {{ background: rgba(3, 237, 249, 0.05); }}
        .widget-header-left {{ display: flex; align-items: center; gap: 10px; }}
        .widget-color-bar {{ width: 4px; height: 22px; border-radius: 2px; }}
        .widget-title {{
          font-size: 14px; font-weight: 700; color: var(--pink);
          text-transform: uppercase; letter-spacing: 1px;
        }}
        .widget-badge {{
          font-size: 10px; font-weight: 700; padding: 2px 8px;
          border-radius: 10px; text-transform: uppercase;
          background: var(--neongreen); color: var(--purple);
        }}
        .widget-badge.empty {{ background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.3); }}
        .collapse-icon {{
          color: rgba(255, 255, 255, 0.3); font-size: 12px;
          transition: transform 0.2s; display: inline-block;
        }}
        .collapse-icon.collapsed {{ transform: rotate(-90deg); }}
        .widget-body {{ max-height: 500px; overflow-y: auto; }}
        .widget-body.collapsed {{ display: none; }}

        /* ── ARTICLES ── */
        .article-item {{
          padding: 12px 18px; border-bottom: 1px solid rgba(255, 255, 255, 0.03);
          transition: all 0.15s; border-left: 3px solid transparent;
        }}
        .article-item:hover {{
          background: rgba(3, 237, 249, 0.08); border-left-color: var(--blue);
        }}
        .article-item:last-child {{ border-bottom: none; }}
        .article-link {{
          color: var(--offwhite); text-decoration: none;
          font-size: 14px; font-weight: 400; line-height: 1.45; display: block;
        }}
        .article-link:hover {{ color: var(--neongreen); }}
        .article-meta {{
          font-size: 11px; color: var(--yellow); margin-top: 6px;
          display: flex; justify-content: space-between; align-items: center;
          text-transform: uppercase; font-weight: 700;
        }}
        .article-source-tag {{
          background: var(--purple); color: var(--blue);
          border: 1px solid var(--blue); padding: 1px 6px;
          border-radius: 4px; font-size: 9px; font-weight: 700; text-transform: uppercase;
        }}
        .widget-empty {{
          text-align: center; padding: 20px;
          color: rgba(255, 255, 255, 0.25); font-size: 13px;
        }}

        /* ── CATEGORY DIVIDER ── */
        .category-divider {{
          column-span: all;
          background: rgba(255, 255, 255, 0.03);
          border: 2px solid var(--blue); border-radius: 10px;
          padding: 18px 24px; margin: 10px 0 20px;
          display: flex; justify-content: space-between; align-items: center;
        }}
        .category-divider h2 {{
          font-size: 24px; color: var(--pink); margin: 0;
          text-transform: uppercase; font-weight: 700;
          font-family: "Fira Sans", sans-serif; line-height: 1.2;
        }}
        .cat-desc {{
          color: var(--yellow); font-size: 13px;
          text-transform: uppercase; font-weight: 400; margin-top: 2px;
        }}
        .cat-stats {{
          text-align: right; color: var(--neongreen);
          font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;
        }}

        /* ── FOOTER ── */
        .last-updated {{
          text-align: center; color: var(--neongreen); font-size: 13px;
          margin: 30px 24px; padding: 16px;
          background: rgba(255, 255, 255, 0.02);
          border: 1px solid var(--blue); border-radius: 6px;
          text-transform: uppercase; font-weight: 700; letter-spacing: 1px;
        }}

        /* ── SCROLLBAR ── */
        * {{ scrollbar-width: thin; scrollbar-color: rgba(3, 237, 249, 0.3) transparent; }}
        *::-webkit-scrollbar {{ width: 5px; }}
        *::-webkit-scrollbar-track {{ background: transparent; }}
        *::-webkit-scrollbar-thumb {{ background: rgba(3, 237, 249, 0.3); border-radius: 4px; }}

        /* ── RESPONSIVE ── */
        @media (max-width: 1100px) {{ .dashboard.grid-view {{ column-count: 2; }} }}
        @media (max-width: 700px) {{
          .dashboard.grid-view {{ column-count: 1; }}
          .top-bar {{ flex-direction: column; height: auto; padding: 12px; gap: 10px; }}
          .top-bar-left {{ flex-wrap: wrap; justify-content: center; }}
          .top-bar-right {{ flex-wrap: wrap; justify-content: center; }}
          .search-box {{ width: 100%; }}
          .stats-bar {{ flex-direction: column; gap: 10px; align-items: flex-start; }}
          .category-divider {{ flex-direction: column; gap: 10px; }}
          .category-divider .cat-stats {{ text-align: left; }}
        }}
    </style>
</head>
<body>

    <div class="top-bar">
        <div class="top-bar-left">
            <div class="logo">NewsHub</div>
            <div class="tab-bar">
                <button class="tab-btn active" onclick="setTab('all')">All Feeds</button>
                {tab_buttons}
            </div>
        </div>
        <div class="top-bar-right">
            <input class="search-box" id="searchBox" type="text" placeholder="Search articles..." oninput="onSearch()">
        </div>
    </div>

    <div class="stats-bar">
        <div class="stats-left">
            <span><strong id="totalArticles" style="color:var(--blue)">0</strong> articles</span>
            <span><strong id="totalSources" style="color:var(--neongreen)">0</strong> sources</span>
        </div>
        <div class="stats-right">
            <button class="filter-btn" onclick="toggleCollapseAll()">Collapse All</button>
            <button class="filter-btn" onclick="expandAll()">Expand All</button>
            <div class="view-toggle">
                <button class="active" id="gridBtn" onclick="setView('grid')">▦</button>
                <button id="listBtn" onclick="setView('list')">☰</button>
            </div>
        </div>
    </div>

    <div class="dashboard grid-view" id="dashboard"></div>

    <div class="last-updated">Generated: {timestamp}</div>

<script>
    // Feed data baked in by Python — no CORS, no proxies, no API limits
    const categories = {data_json};

    let activeTab = 'all';
    let searchQuery = '';
    let collapsedWidgets = {{}};

    function setTab(tab) {{
        activeTab = tab;
        document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
        event.target.classList.add('active');
        renderDashboard();
    }}
    function setView(mode) {{
        const dash = document.getElementById('dashboard');
        dash.className = mode === 'grid' ? 'dashboard grid-view' : 'dashboard list-view';
        document.getElementById('gridBtn').classList.toggle('active', mode === 'grid');
        document.getElementById('listBtn').classList.toggle('active', mode === 'list');
    }}
    function onSearch() {{
        searchQuery = document.getElementById('searchBox').value.toLowerCase();
        renderDashboard();
    }}
    function toggleCollapseAll() {{
        Object.values(categories).forEach(cat => {{
            cat.sources.forEach(s => {{ collapsedWidgets[s.name] = true; }});
        }});
        renderDashboard();
    }}
    function expandAll() {{
        collapsedWidgets = {{}};
        renderDashboard();
    }}
    function toggleWidget(name) {{
        collapsedWidgets[name] = !collapsedWidgets[name];
        renderDashboard();
    }}

    function escapeHTML(s) {{
        const div = document.createElement('div');
        div.textContent = s;
        return div.innerHTML;
    }}

    function renderDashboard() {{
        const container = document.getElementById('dashboard');
        let html = '';
        const catsToShow = activeTab === 'all' ? Object.keys(categories) : [activeTab];
        let totalArticles = 0;
        let totalSources = 0;

        catsToShow.forEach(catKey => {{
            const cat = categories[catKey];
            if (!cat) return;
            const catArticles = cat.sources.reduce((s, src) => s + src.articles.length, 0);
            totalArticles += catArticles;
            totalSources += cat.sources.length;

            html += `<div class="category-divider">
                <div>
                    <h2>${{cat.title}}</h2>
                    <div class="cat-desc">${{cat.description}}</div>
                </div>
                <div class="cat-stats">
                    <div>${{cat.sources.length}} sources</div>
                    <div>${{catArticles}} articles</div>
                </div>
            </div>`;

            cat.sources.forEach(source => {{
                const isCollapsed = collapsedWidgets[source.name];
                let articles = source.articles;
                if (searchQuery) {{
                    articles = articles.filter(a => a.title.toLowerCase().includes(searchQuery));
                }}

                const count = articles.length;
                const badgeClass = count > 0 ? '' : 'empty';
                const badgeText = count > 0 ? count : 'empty';

                let bodyHTML = '';
                if (count === 0) {{
                    bodyHTML = `<div class="widget-empty">No recent articles</div>`;
                }} else {{
                    bodyHTML = articles.map(a => `
                        <div class="article-item">
                            <a href="${{escapeHTML(a.link)}}" class="article-link" target="_blank" rel="noopener noreferrer">${{escapeHTML(a.title)}}</a>
                            <div class="article-meta">
                                <span>${{a.pubDate}}</span>
                                <span class="article-source-tag">${{escapeHTML(source.name)}}</span>
                            </div>
                        </div>
                    `).join('');
                }}

                const safeName = source.name.replace(/'/g, "\\\\'");
                html += `
                <div class="feed-widget">
                    <div class="widget-header" onclick="toggleWidget('${{safeName}}')">
                        <div class="widget-header-left">
                            <div class="widget-color-bar" style="background:${{cat.color}}"></div>
                            <span class="widget-title">${{escapeHTML(source.name)}}</span>
                            <span class="widget-badge ${{badgeClass}}">${{badgeText}}</span>
                        </div>
                        <span class="collapse-icon ${{isCollapsed ? 'collapsed' : ''}}">▾</span>
                    </div>
                    <div class="widget-body ${{isCollapsed ? 'collapsed' : ''}}">
                        ${{bodyHTML}}
                    </div>
                </div>`;
            }});
        }});

        container.innerHTML = html;
        document.getElementById('totalArticles').textContent = totalArticles;
        document.getElementById('totalSources').textContent = totalSources;
    }}

    renderDashboard();
</script>
</body>
</html>'''


def main():
    output_dir = Path.home() / "Downloads"
    output_file = output_dir / "newshub.html"

    print(f"\\n{'='*60}")
    print(f"  NewsHub Dashboard Generator")
    print(f"  {datetime.now().strftime('%I:%M %p, %b %d %Y')}")
    print(f"{'='*60}\\n")

    # Collect all feeds from all categories
    all_feeds = {}
    for cat_key, cat_config in feed_categories.items():
        all_feeds.update(cat_config["feeds"])

    # Sort feeds alphabetically (ignoring "The ")
    sorted_names = sorted(all_feeds.keys(), key=lambda x: x.lower().lstrip("the "))

    # Fetch all feeds
    feed_data = {}
    for name in tqdm(sorted_names, desc="Fetching feeds"):
        url = all_feeds[name]
        articles = fetch_feed(name, url)
        feed_data[name] = articles

    # Generate HTML
    html_content = generate_dashboard_html(feed_data, feed_categories)

    output_file.write_text(html_content, encoding="utf-8")

    # Summary
    total_feeds = len(all_feeds)
    active_feeds = sum(1 for v in feed_data.values() if v)
    total_articles = sum(len(v) for v in feed_data.values())

    print(f"\\n{'='*60}")
    print(f"  ✓ Dashboard saved to: {output_file}")
    print(f"  ✓ {active_feeds}/{total_feeds} feeds loaded, {total_articles} articles")
    print(f"{'='*60}\\n")


if __name__ == "__main__":
    main()

import requests
import feedparser
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from tqdm import tqdm

rss_feeds = {
    "The American Pamphleteer": "https://ladylibertie.substack.com/feed",
    "The Baffler": "https://thebaffler.com/homepage/feed",
    "Danny Funt+": "https://dannyfunt.substack.com/feed",
    "DepthHub": "https://www.reddit.com/r/DepthHub/.rss",
    "Gin and Tacos": "http://www.ginandtacos.com/feed/",
    "How Things Work": "https://www.hamiltonnolan.com/feed",
    "I Love Typography": "https://ilovetypography.com/feed/",
    "KCUR- Local Food ": "https://www.kcur.org/tags/local-food.rss",
    "Mike Tanier": "https://miketanier.substack.com/feed",
    "The Nation- Electoral Reform": "https://www.thenation.com/feed/?post_type=article&subject=electoral-reform",
    "The Nation- Supreme Court": "https://www.thenation.com/feed/?post_type=article&subject=supreme-court",
    "Neil’s Substack": "https://neilpaine.substack.com/feed",
    "Royals – FanGraphs Baseball": "https://www.fangraphs.com/blogs/category/teams/royals/feed/",
    "Royals Data Dugout": "https://royalsdatadugout.substack.com/feed",
    "Sabatos Crystal Ball": "https://centerforpolitics.org/crystalball/feed/",
    "Amand Marcotte": "https://politepol.com/fd/qbzvP6fNF3Qn.xml",
    "Shellsharks Feeds": "https://shellsharks.com/feeds/feed.xml",
    "Status Kuo": "https://statuskuo.substack.com/feed",
    "The Sunday Long Read": "https://us9.campaign-archive.com/feed?id=67e6e8a504&u=6e1ae4ac632498a38c1d57c54",
    "Why Is This Interesting?": "https://whyisthisinteresting.substack.com/feed",
    "Ludic": "https://ludic.mataroa.blog/rss/",
    "Techdirt": "https://www.techdirt.com/feed/",
    "Above the Law": "https://abovethelaw.com/feed/",
    "The Linkfest": "https://buttondown.com/clivethompson/rss",
    "Olivia Julianna": "https://oliviajulianna.substack.com/feed",
    "Press Watchers": "https://presswatchers.org/feed/",
    "Humorism": "https://www.humorism.xyz/rss/",
    "Unraveled": "https://unraveledpress.com/rss.xml",
}


# Keywords per feed (empty list means no filtering for that feed)
feed_keywords = {
    "Above the Law": ["firm", "school"],
    "Mike Tanier": ["Chiefs"],
    "Neil’s Substack": ["The Week That Was"],
    "Status Kuo": ["giggles"],
    "Techdirt": ["court", "law", "maga"],
    "Why Is This Interesting?": ["Monday Media Diet"]
    # Default: feeds not listed here won't be filtered
}

def fetch_feed(site_name, url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=True)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        if feed.bozo:
            print(f"Error parsing feed for {site_name}: {feed.bozo_exception}")
            return pd.DataFrame()

        entries = feed.entries
        if not entries:
            print(f"No entries found for {site_name}")
            return pd.DataFrame()

        one_week_ago = datetime.now() - timedelta(weeks=1)
        recent_entries = [
            entry
            for entry in entries
            if "published_parsed" in entry
            and entry.published_parsed
            and datetime(*entry.published_parsed[:6]) > one_week_ago
        ]

        if not recent_entries:
            print(f"No recent entries found for {site_name}.")
            return pd.DataFrame()

        df = pd.DataFrame(recent_entries)
        df["site_name"] = site_name

        if "link" not in df.columns:
            df["link"] = None
        if "title" not in df.columns:
            df["title"] = "Untitled"
        if "published" not in df.columns:
            df["published"] = "Unknown Date"

        # Apply keyword filter if defined for this feed
        keywords = feed_keywords.get(site_name, [])
        if keywords:
            mask = df["title"].str.contains("|".join(keywords), case=False, na=False)
            df = df[mask]
            if df.empty:
                print(f"No keyword matches for {site_name}.")
                return pd.DataFrame()

        return df[["title", "link", "site_name", "published"]].head(10)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error for {site_name}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error for {site_name}: {e}")
    return pd.DataFrame()


def rss_df_to_html(df, output_file):
    with open(output_file, "w") as file:
        file.write("<html>\n")
        file.write("<head>\n")
        file.write("    <title>Muneer Feeds</title>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        file.write("<h1>RSS Feeds</h1>\n")
        file.write(f"<p>Last updated: {datetime.now()}</p>\n")

        for site_name, group in df.groupby("site_name"):
            file.write(f"<h2>{site_name}</h2>\n<ul>\n")
            for _, row in group.iterrows():
                file.write(
                    f'<li><a href="{row.link}">{row.title}</a> - {row.published}</li>\n'
                )
            file.write("</ul>\n")

        file.write("</body>\n</html>\n")


def sort_key(title):
    title = title.lower()
    if title.startswith("the "):
        title = title[4:]
    return title


sorted_rss_feeds = dict(sorted(rss_feeds.items(), key=lambda item: sort_key(item[0])))

output_dir = Path("/Users/muneer78/Downloads")
output_file = output_dir / "reading.html"

feed_data = []

for feed_name, feed_url in tqdm(sorted_rss_feeds.items(), desc="Processing RSS Feeds"):
    df = fetch_feed(feed_name, feed_url)
    if not df.empty:
        feed_data.append(df)

if feed_data:
    final_df = pd.concat(feed_data, ignore_index=True)
    rss_df_to_html(final_df, output_file)
    print(f"HTML saved to: {output_file}")
else:
    print("No feed data to save.")

import requests
from bs4 import BeautifulSoup
import feedparser


def find_rss_feed(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        # Look for RSS feed links
        rss_links = soup.find_all("link", type="application/rss+xml")
        feeds = []
        for link in rss_links:
            feed_url = link.get("href")
            if not feed_url.startswith("http"):
                feed_url = requests.compat.urljoin(url, feed_url)
            feeds.append(feed_url)
        return feeds
    except Exception as e:
        print(f"Error fetching RSS feeds for {url}: {e}")
        return []


def get_feed_title(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        return feed.feed.title if "title" in feed.feed else "No title found"
    except Exception as e:
        print(f"Error parsing feed {feed_url}: {e}")
        return "Error fetching title"


# Example usage
urls = [
    ("ℤ→ℤ", "https://ztoz.blog/"),
    ("Cafe Hysteria", "https://madisonhuizinga.substack.com/"),
    ("Constantly Hating", "https://constantlyhating.substack.com"),
    ("Culture Study- Anne Helen Petersen", "https://annehelen.substack.com/"),
    ("The Verge Installer Newsletter", "https://www.theverge.com/installer-newsletter"),
    ("Never Hungover", "https://www.neverhungover.club/"),
    ("Screenshot Reliquary", "https://screenshotreliquary.substack.com/"),
    ("Shatter Zone", "https://shatterzone.substack.com/"),
    ("The Future, Now and Then", "https://davekarpf.substack.com/"),
    ("The Small Bow", "https://www.thesmallbow.com/"),
    ("Things I Think Are Awesome", "https://arnicas.substack.com/"),
    ("Why Is This Interesting?", "https://whyisthisinteresting.substack.com/"),
    ("The 19th", "https://19thnews.org/"),
]

for title, url in urls:
    feeds = find_rss_feed(url)
    for feed in feeds:
        print(f"'{title}': '{feed}',")

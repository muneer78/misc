import feedparser
from datetime import datetime

FEED_URL = "https://exampleblog.com/rss"
feed = feedparser.parse(FEED_URL)
with open("reading_list.txt", "a", encoding="utf-8") as f:
    f.write(f"\n\n=== {datetime.now()} ===\n")
    for entry in feed.entries[:5]:
        f.write(f"{entry.title}\n{entry.link}\n\n")
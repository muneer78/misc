import requests
import feedparser
import pandas as pd
from pathlib import Path
from datetime import datetime

rss_feeds = {
    "Fitzdog Radio": "https://gregfitz.libsyn.com/rss",
}

# def fetch_feed(site_name, url):
#     try:
#         response = requests.get(url, timeout=10, verify=True)
#         response.raise_for_status()  # Raise HTTP errors
#         feed = feedparser.parse(response.content)
#         if feed.bozo:  # Check for parsing errors
#             print(f"Error parsing feed for {site_name}: {feed.bozo_exception}")
#             return pd.DataFrame()

#         entries = feed.entries
#         if not entries:
#             print(f"No entries found for {site_name}.")
#             return pd.DataFrame()

#         # Convert entries to a DataFrame
#         df = pd.DataFrame(entries)
#         df['site_name'] = site_name

#         # Ensure required fields exist, fill missing with placeholders
#         if 'link' not in df.columns:
#             df['link'] = None  # Use None or an empty string as a placeholder
#         if 'title' not in df.columns:
#             df['title'] = "Untitled"  # Placeholder for missing titles

#         return df[['title', 'link', 'site_name']]  # Keep only relevant columns
#     except requests.exceptions.SSLError as e:
#         print(f"SSL Error for {site_name}: {e}")
#     except requests.exceptions.RequestException as e:
#         print(f"Error for {site_name}: {e}")
#     return pd.DataFrame()


def fetch_feed(site_name, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10, verify=True)
        response.raise_for_status()  # Raise HTTP errors
        feed = feedparser.parse(response.content)
        if feed.bozo:  # Check for parsing errors
            print(f"Error parsing feed for {site_name}: {feed.bozo_exception}")
            return pd.DataFrame()

        entries = feed.entries
        if not entries:
            print(f"No entries found for {site_name}.")
            return pd.DataFrame()

        # Convert entries to a DataFrame
        df = pd.DataFrame(entries)
        df["site_name"] = site_name

        # Ensure required fields exist, fill missing with placeholders
        if "link" not in df.columns:
            df["link"] = None
        if "title" not in df.columns:
            df["title"] = "Untitled"

        # Return only the last 10 items
        return df[["title", "link", "site_name"]].head(10)
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
                file.write(f'<li><a href="{row.link}">{row.title}</a></li>\n')
            file.write("</ul>\n")

        file.write("</body>\n</html>\n")


# Process feeds
output_dir = Path("/Users/muneer78/Downloads")
output_file = output_dir / "rss_feeds.html"

dfs = [fetch_feed(site_name, url) for site_name, url in rss_feeds.items()]
df = pd.concat(dfs, ignore_index=True)
rss_df_to_html(df, output_file)
print(f"HTML saved to: {output_file}")

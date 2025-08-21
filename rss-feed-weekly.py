import requests
import feedparser
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from tqdm import tqdm

rss_feeds = {
    '/dev/lawyer': 'https://writing.kemitchell.com/feed.xml',
    'Aaron Blackshear': 'https://strictlyforbuckets.com/blog/index.xml',
    'Alexwlchan': 'https://alexwlchan.net/atom.xml',
    'Ali Barthwell Author Archive': 'https://politepol.com/fd/Z7RsuNu72Zc4.xml',
    'The American Pamphleteer': 'https://ladylibertie.substack.com/feed',
    'Anya Prosvetova': 'https://www.anyalitica.dev/feed.xml',
    'Awful Announcing': 'https://awfulannouncing.com/feed',
    'The Baffler': 'https://thebaffler.com/homepage/feed',
    'Bicycle For Your Mind': 'https://bicycleforyourmind.com/feed.rss',
    'Billman': 'https://biilmann.blog/rss.xml',
    'Billmill.org': 'https://notes.billmill.org/atom.xml',
    'bitches gotta eat!': 'https://bitchesgottaeat.substack.com/feed',
    'Brett Terpstra': 'http://brett.trpstra.net/brettterpstra',
    'Brian Moylan Author Archive': 'https://politepol.com/fd/VoicyDwzX43M.xml',
    'Dan Hon': 'https://newsletter.danhon.com/rss.xml',
    'Dan Sinkers Blog': 'https://dansinker.com/feed.xml',
    'Danny Funt+': 'https://dannyfunt.substack.com/feed',
    'DepthHub': 'https://www.reddit.com/r/DepthHub/.rss',
    'Ed Zitrons Wheres Your Ed At': 'https://www.wheresyoured.at/feed',
    'Ellane W': 'https://ellanew.com/feed.rss',
    'Farm to Fountains': 'https://farmtofountains.com/feed/',
    'furbo': 'https://furbo.org/feed/',
    'Gin and Tacos': 'http://www.ginandtacos.com/feed/',
    'How Gambling Works': 'https://howgamblingworks.substack.com/feed',
    'How Things Work': 'https://www.hamiltonnolan.com/feed',
    'I Love Typography': 'https://ilovetypography.com/feed/',
    'Julia Evans': 'https://jvns.ca/atom.xml',
    'Kansas City Royals – MLB Trade Rumors': 'https://www.mlbtraderumors.com/kansas-city-royals/feed/atom',
    'Kansas Reflector': 'https://kansasreflector.com/feed/',
    'KCUR- Local Food ': 'https://www.kcur.org/tags/local-food.rss',
    'Mathspp': 'https://mathspp.com/blog.atom',
    'Mike Tanier': 'https://miketanier.substack.com/feed',
    'The Nation- Electoral Reform': 'https://www.thenation.com/feed/?post_type=article&subject=electoral-reform',
    'The Nation- Supreme Court': 'https://www.thenation.com/feed/?post_type=article&subject=supreme-court',
    'Neil’s Substack': 'https://neilpaine.substack.com/feed',
    'The New Stack': 'https://thenewstack.io/blog/feed/',
    'NPR: Food': 'https://feeds.npr.org/1053/rss.xml',
    'PyBites': 'https://pybit.es/feed/',
    'PyCoders Weekly': 'https://pycoders.com/feed/T8SjZAIK',
    'PyMOTW on Doug Hellmann': 'https://feeds.feedburner.com/PyMOTW',
    'Python Insider': 'https://blog.python.org/feeds/posts/default',
    'Recomendo': 'https://www.recomendo.com/feed',
    'Roads & Kingdoms': 'https://roadsandkingdoms.com/feed/',
    'Robin Sloan': 'https://www.robinsloan.com/feed.xml',
    'Royals Farm Report': 'https://royalsfarmreport.com/feed/',
    'Royals Review -  All Posts': 'https://www.royalsreview.com/rss/index.xml',
    'Royals – FanGraphs Baseball': 'https://www.fangraphs.com/blogs/category/teams/royals/feed/',
    'Royals Data Dugout': 'https://royalsdatadugout.substack.com/feed',
    'Sabatos Crystal Ball': 'https://centerforpolitics.org/crystalball/feed/',
    'Salon.com > amanda_marcotte': 'https://www.salon.com/writer/amanda_marcotte/feed',
    'Shellsharks Feeds': 'https://shellsharks.com/feeds/feed.xml',
    'SportsLogos.Net News': 'https://news.sportslogos.net/feed/',
    'The Sunday Long Read': 'https://us9.campaign-archive.com/feed?id=67e6e8a504&u=6e1ae4ac632498a38c1d57c54',
    'TerminaL Trove': 'https://terminaltrove.com/blog.xml',
    'Tommy Craggs': 'https://tommycraggs.com/feed/',
    'Why Is This Interesting?': 'https://whyisthisinteresting.substack.com/feed',
    'Ludic': 'https://ludic.mataroa.blog/rss/',
}

def fetch_feed(site_name, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
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
            print(f"No entries found for {site_name}")
            return pd.DataFrame()

        # Filter entries from the last 2 weeks
        one_week_ago = datetime.now() - timedelta(weeks=1)
        recent_entries = [entry for entry in entries if 'published_parsed' in entry and entry.published_parsed and datetime(*entry.published_parsed[:6]) > one_week_ago]

        if not recent_entries:
            print(f"No recent entries found for {site_name}.")
            return pd.DataFrame()

        # Convert entries to a DataFrame
        df = pd.DataFrame(recent_entries)
        df['site_name'] = site_name

        # Ensure required fields exist, fill missing with placeholders
        if 'link' not in df.columns:
            df['link'] = None
        if 'title' not in df.columns:
            df['title'] = "Untitled"
        if 'published' not in df.columns:
            df['published'] = "Unknown Date"

        # Return only the last 10 items
        return df[['title', 'link', 'site_name', 'published']].head(10)
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error for {site_name}: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error for {site_name}: {e}")
    return pd.DataFrame()

def rss_df_to_html(df, output_file):
    with open(output_file, 'w') as file:
        file.write('<html>\n')
        file.write('<head>\n')
        file.write('    <title>Muneer Feeds</title>\n')
        file.write('</head>\n')
        file.write('<body>\n')
        file.write('<h1>RSS Feeds</h1>\n')
        file.write(f'<p>Last updated: {datetime.now()}</p>\n')

        for site_name, group in df.groupby('site_name'):
            file.write(f'<h2>{site_name}</h2>\n<ul>\n')
            for _, row in group.iterrows():
                file.write(f'<li><a href="{row.link}">{row.title}</a> - {row.published}</li>\n')
            file.write('</ul>\n')

        file.write('</body>\n</html>\n')

# Function to remove "The " from the start of a title for sorting purposes
def sort_key(title):
    title = title.lower()
    if title.startswith("the "):
        title = title[4:]
    return title

# Sort the rss_feeds dictionary by keys without paying attention to capitalization
sorted_rss_feeds = dict(sorted(rss_feeds.items(), key=lambda item: sort_key(item[0])))

# Process feeds
output_dir = Path("/Users/muneer78/Downloads")
output_file = output_dir / "rss_feeds.html"

# Initialize an empty list to store the feed data
feed_data = []

# Iterate over the sorted feeds with a progress bar
for feed_name, feed_url in tqdm(sorted_rss_feeds.items(), desc="Processing RSS Feeds"):
    df = fetch_feed(feed_name, feed_url)
    if not df.empty:
        feed_data.append(df)

# Concatenate all DataFrames
if feed_data:
    final_df = pd.concat(feed_data, ignore_index=True)
    rss_df_to_html(final_df, output_file)
    print(f"HTML saved to: {output_file}")
else:
    print("No feed data to save.")
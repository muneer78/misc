import requests
import feedparser
import pandas as pd
from pathlib import Path
from datetime import datetime

rss_feeds = {
    '404 Media': 'https://www.404media.co/rss/',
    'Andscape': 'https://andscape.com/feed',
    'Article – The Nation': 'https://www.thenation.com/feed/?post_type=article&subject=supreme-court',
    'Article – The Nation': 'https://www.thenation.com/feed/?post_type=article&subject=electoral-reform',
    'Articles and Investigations - ProPublica': 'https://www.propublica.org/feeds/54Ghome',
    'Arts & Letters Daily': 'http://ftr.fivefilters.org/makefulltextfeed.php?url=www.aldaily.com/feed/&max=3&links=preserve',
    'Atlas Obscura - Latest Articles and Places': 'https://www.atlasobscura.com/feeds/latest',
    'Attack of the 50 Foot Blockchain': 'https://davidgerard.co.uk/blockchain/feed/',
    'Awful Announcing': 'https://awfulannouncing.com/feed',
    'Balls and Strikes': 'https://ballsandstrikes.org/feed/',
    'Baseball America': 'https://feeds.redcircle.com/54051e90-c6e1-43ac-9a01-4c8fc92bc79d',
    'Baseball Prospectus': 'https://www.baseballprospectus.com/feed/',
    'baseballmusings.com': 'http://feeds2.feedburner.com/Baseballmusingscom',
    'Baty.net': 'https://baty.net/feed',
    'Bicycle For Your Mind': 'http://bicycleforyourmind.com/feed.rss',
    'Boing Boing': 'http://feeds.boingboing.net/boingboing/iBag',
    'Book Marks Features | Book Marks': 'https://bookmarks.reviews/category/features/feed/',
    'Brand Eating': 'https://www.brandeating.com/feeds/posts/default',
    'Teen Vogue': 'https://politepol.com/fd/Vjc601sG0jpO.xml',
    'Brian Moylan Author Archive': 'https://politepol.com/fd/VoicyDwzX43M.xml',
    'Budget Bytes': 'https://budgetbytes.com/feed/',
    'Bustle': 'https://www.bustle.com/rss',
    'CaptainAwkward.com': 'https://captainawkward.com/feed/',
    'Daring Fireball': 'https://daringfireball.net/feeds/main',
    'DepthHub: A jumping-off point for deeply-involved subreddits': 'https://www.reddit.com/r/DepthHub/.rss',
    'Election Law Blog': 'https://electionlawblog.org/?feed=rss2',
    'FanGraphs Baseball': 'https://blogs.fangraphs.com/feed/',
    'FanGraphs Fantasy Baseball': 'http://feeds.feedburner.com/RotoGraphs',
    'Farm To Fountain': 'https://farmtofountains.com/feed/',
    'Fast Food News – Fast Food Menu Prices': 'https://www.fastfoodmenuprices.com/news/feed/',
    'Food & Drink – The Pitch': 'https://www.thepitchkc.com/category/food-drink/feed/',
    'Food : NPR': 'https://feeds.npr.org/1053/rss.xml',
    'Gadgets | Latest gadget news, updates & reviews on TechCrunch': 'https://techcrunch.com/gadgets/feed/',
    'Gizmodo': 'https://gizmodo.com/rss',
    'Groceries | Eat This, Not That!': 'https://rss.app/feeds/JKtAQLtZCtIyjikJ.xml',
    'Hacker News: Show HN': 'https://hnrss.org/show',
    'Harpers Magazine': 'http://harpers.org/feed/',
    'Hatewatch | Southern Poverty Law Center': 'https://www.splcenter.org/hatewatch/rss.xml',
    'HolyPython.com': 'https://holypython.com/feed/',
    'Kansas City Royals – MLB Trade Rumors': 'https://www.mlbtraderumors.com/kansas-city-royals/feed/atom',
    'kottke.org': 'http://feeds.kottke.org/main',
    'Lamebook - Funny Facebook Statuses, Fails, LOLs and More - The Original': 'http://feeds.feedburner.com/Lamebook',
    'Laughing Squid': 'http://laughingsquid.com/feed/',
    'Legal Profession Blog': 'http://feeds.feedburner.com/LegalProfessionBlog',
    'LifeHacker': 'https://lifehacker.com/feed/rss',
    'local ': 'https://www.kcur.org/tags/local-food.rss',
    'Longreads': 'https://longreads.com/feed/',
    'Lowering the Bar': 'http://feeds.feedblitz.com/loweringthebar&x=1',
    'Marginal REVOLUTION': 'http://marginalrevolution.com/feed',
    'Matt Bruenig Dot Com': 'https://mattbruenig.com/feed/',
    'Mental Floss': 'https://www.mentalfloss.com/rss.xml',
    'Misc Newsletters': 'https://kill-the-newsletter.com/feeds/5mr68b7cb43ac2h04ai5.xml',
    'Neatorama': 'http://www.neatorama.com/feed',
    'News Archives | The Pitch': 'https://www.thepitchkc.com/category/news-52777/feed/',
    'Open Culture': 'https://www.openculture.com/feed',
    'Pitch Weekly': 'https://www.thepitchkc.com/feed/',
    'Pitcher List': 'http://www.pitcherlist.com/feed/',
    'Pluralistic: Daily links from Cory Doctorow': 'https://pluralistic.net/feed/',
    'Popular Information': 'https://popular.info/feed',
    'Poynter': 'https://www.poynter.org/feed/',
    'ProPublica': 'http://feeds.propublica.org/propublica/main',
    'Public Notice': 'https://www.publicnotice.co/feed',
    'PyMOTW on Doug Hellmann': 'https://feeds.feedburner.com/PyMOTW',
    'Python Weekly Newsletter Archive Feed': 'http://us2.campaign-archive1.com/feed?u=e2e180baf855ac797ef407fc7&id=9e26887fc5',
    'Right Wing Watch': 'https://www.rightwingwatch.org/feed/',
    'RotoGraphs Fantasy Baseball': 'https://fantasy.fangraphs.com/feed/',
    'Royals Farm Report': 'https://royalsfarmreport.com/feed/',
    'Royals Review -  All Posts': 'https://www.royalsreview.com/rss/index.xml',
    'Royals – FanGraphs Baseball': 'https://www.fangraphs.com/blogs/category/teams/royals/feed/',
    'Salon.com > amanda_marcotte': 'https://www.salon.com/writer/amanda_marcotte/feed',
    'SportsLogos.Net News': 'https://news.sportslogos.net/feed/',
    'Steven A. Guccione': 'https://stevesaltfacebook.blog/feed/',
    'Tedium: The Dull Side of the Internet.': 'https://feed.tedium.co/',
    'The Bulwark': 'https://thebulwark.com/feed/',
    'The Electric Typewriter': 'http://tetw.org/rss',
    'The Impulsive Buy': 'https://www.theimpulsivebuy.com/wordpress/feed/',
    'The Intercept': 'https://theintercept.com/feed/?_=1382',
    'The Root': 'https://www.theroot.com/rss',
    'The Verge -  All Posts': 'http://www.theverge.com/rss/index.xml',
    'TPM – Talking Points Memo': 'https://talkingpointsmemo.com/feed',
    'Whats Good at Trader Joes': 'http://www.whatsgoodattraderjoes.com/feeds/posts/default',
    'Whatever': 'https://whatever.scalzi.com/feed/',
    'Wonkette': 'http://wonkette.com/feed',
    'Work Stories, Humor, Memes, News | Pleated Jeans': 'https://pleated-jeans.com/category/work/feed/',
    'xkcd.com': 'http://xkcd.com/rss.xml',
    'You searched for antiwork - Ruin My Week': 'https://ruinmyweek.com/search/antiwork/feed/rss2/',
    'Current Affairs': 'https://www.currentaffairs.org/news/rss.xml'
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
            print(f"No entries found for {site_name}.")
            return pd.DataFrame()

        # Convert entries to a DataFrame
        df = pd.DataFrame(entries)
        df['site_name'] = site_name

        # Ensure required fields exist, fill missing with placeholders
        if 'link' not in df.columns:
            df['link'] = None
        if 'title' not in df.columns:
            df['title'] = "Untitled"

        # Return only the last 10 items
        return df[['title', 'link', 'site_name']].head(10)
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
                file.write(f'<li><a href="{row.link}">{row.title}</a></li>\n')
            file.write('</ul>\n')

        file.write('</body>\n</html>\n')

# Process feeds
output_dir = Path("/Users/muneer78/Downloads")
output_file = output_dir / "rss_feeds.html"

dfs = [fetch_feed(site_name, url) for site_name, url in rss_feeds.items()]
df = pd.concat(dfs, ignore_index=True)
rss_df_to_html(df, output_file)
print(f"HTML saved to: {output_file}")
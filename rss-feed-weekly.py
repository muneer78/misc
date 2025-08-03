import requests
import feedparser
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from tqdm import tqdm

rss_feeds = {
    '/dev/lawyer': 'https://writing.kemitchell.com/feed.xml',
    'Alexwlchan': 'https://alexwlchan.net/atom.xml',
    'Ali Barthwell Author Archive': 'https://politepol.com/fd/Z7RsuNu72Zc4.xml',
    'The American Pamphleteer': 'https://ladylibertie.substack.com/feed',
    'Ana Rodrigues': 'https://ohhelloana.blog/feed.xml',
    'Anarcat': 'https://anarc.at/blog/index.rss',
    'Anya Prosvetova': 'https://www.anyalitica.dev/feed.xml',
    'Awful Announcing': 'https://awfulannouncing.com/feed',
    'Baeldung on Linux': 'https://feeds.feedblitz.com/baeldung/linux',
    'The Baffler': 'https://thebaffler.com/homepage/feed',
    'Balls and Strikes': 'https://ballsandstrikes.org/feed/',
    'Baty.net': 'https://baty.net/index.xml',
    'The Beautiful Mess': 'https://cutlefish.substack.com/feed',
    'Bicycle For Your Mind': 'https://bicycleforyourmind.com/feed.rss',
    'Billmill.org': 'https://notes.billmill.org/atom.xml',
    'bitches gotta eat!': 'https://bitchesgottaeat.substack.com/feed',
    'Brett Terpstra': 'http://brett.trpstra.net/brettterpstra',
    'Brian Moylan Author Archive': 'https://politepol.com/fd/VoicyDwzX43M.xml',
    'CaptainAwkward.com': 'https://captainawkward.com/feed/',
    'ContraBandCamp': 'https://www.contrabandcamp.com/feed',
    'The Contrarian': 'https://contrarian.substack.com/feed',
    'Dan Sinkers Blog': 'https://dansinker.com/feed.xml',
    'Daniel Lemire': 'https://lemire.me/blog/feed/',
    'Danny Funt+': 'https://dannyfunt.substack.com/feed',
    'Data Engineer Things': 'https://blog.det.life/feed',
    'Data Engineering Central': 'https://dataengineeringcentral.substack.com/feed',
    'daverupert.com': 'https://daverupert.com/atom.xml',
    'DepthHub': 'https://www.reddit.com/r/DepthHub/.rss',
    'Ed Zitrons Wheres Your Ed At': 'https://www.wheresyoured.at/feed',
    'Ellane W': 'https://ellanew.com/feed.rss',
    'Farm to Fountains': 'https://farmtofountains.com/feed/',
    'furbo': 'https://furbo.org/feed/',
    'Gin and Tacos': 'http://www.ginandtacos.com/feed/',
    'Git Gist': 'http://gitgist.com/index.xml',
    'GM Games – Sports General Manager Video Games': 'https://gmgames.org/feed/',
    'Hackaday': 'https://hackaday.com/feed/',
    'How Gambling Works': 'https://howgamblingworks.substack.com/feed',
    'How Things Work': 'https://www.hamiltonnolan.com/feed',
    'I Love Typography': 'https://ilovetypography.com/feed/',
    'i.webthings.hub': 'https://iwebthings.joejenett.com/feed.atom',
    'Indexed': 'http://thisisindexed.com/feed/',
    'The Ink': 'https://the.ink/feed',
    'Into The Fountains': 'https://intothefountains.substack.com/feed',
    'James Coffee Blog': 'https://jamesg.blog/feeds/posts.xml',
    'Julia Evans': 'https://jvns.ca/atom.xml',
    'Just Security': 'https://www.justsecurity.org/feed/',
    'Kalzumeus': 'https://www.kalzumeus.com/feed/articles/',
    'Kansas City Royals – MLB Trade Rumors': 'https://www.mlbtraderumors.com/kansas-city-royals/feed/atom',
    'Kansas Reflector': 'https://kansasreflector.com/feed/',
    'Katherine Yang': 'https://kayserifserif.place/feed.xml',
    'KCUR- Local Food ': 'https://www.kcur.org/tags/local-food.rss',
    'Ken Shirriff': 'https://www.righto.com/feeds/posts/default',
    'Kendra Little': 'https://kendralittle.com/blog/rss.xml',
    'Kicks Condor': 'https://www.kickscondor.com/feed.xml',
    'kk.org': 'https://kk.org/feed',
    'Laura Olin': 'https://buttondown.com/lauraolin/rss',
    'Law Dork': 'https://www.lawdork.com/feed',
    'Lucian Truscott Newsletter': 'https://luciantruscott.substack.com/feed',
    'Luke Muehlhauser': 'http://lukemuehlhauser.com/feed/',
    'Mathspp': 'https://mathspp.com/blog.atom',
    'maya.land': 'https://maya.land/feed.xml',
    'Mike Tanier': 'https://miketanier.substack.com/feed',
    'The Nation- Electoral Reform': 'https://www.thenation.com/feed/?post_type=article&subject=electoral-reform',
    'The Nation- Supreme Court': 'https://www.thenation.com/feed/?post_type=article&subject=supreme-court',
    'Neal Stephenson': 'https://nealstephenson.substack.com/feed',
    'Ned Batchelder': 'http://nedbatchelder.com/blog/rss.xml',
    'Neil’s Substack': 'https://neilpaine.substack.com/feed',
    'The New Stack': 'https://thenewstack.io/blog/feed/',
    'Notes on the Crises- Nathan Tankus': 'https://www.crisesnotes.com/rss/',
    'notnite': 'https://notnite.com/blog/rss.xml',
    'NPR: Food': 'https://feeds.npr.org/1053/rss.xml',
    'Null Bitmap': 'https://buttondown.com/jaffray/rss',
    'null program- Chris Wellons': 'https://nullprogram.com/feed/',
    'Own Your Web': 'https://buttondown.email/ownyourweb/rss',
    'Perl Hacks': 'https://perlhacks.com/feed/',
    'The Perry Bible Fellowship': 'https://pbfcomics.com/feed/',
    'Pudding.cool': 'https://pudding.cool/feed.xml',
    'PyBites': 'https://pybit.es/feed/',
    'PyCoders Weekly': 'https://pycoders.com/feed/T8SjZAIK',
    'PyMOTW on Doug Hellmann': 'https://feeds.feedburner.com/PyMOTW',
    'Python In Office': 'https://pythoninoffice.com/feed/',
    'Python Insider': 'https://blog.python.org/feeds/posts/default',
    'Qubyte Codes': 'https://qubyte.codes/social.atom.xml',
    'Recomendo': 'https://www.recomendo.com/feed',
    'Roads & Kingdoms': 'https://roadsandkingdoms.com/feed/',
    'Robin Sloan': 'https://www.robinsloan.com/feed.xml',
    'The Root': 'https://www.theroot.com/rss',
    'RotoGraphs Fantasy Baseball': 'https://fantasy.fangraphs.com/feed/',
    'Royals Farm Report': 'https://royalsfarmreport.com/feed/',
    'Royals Review -  All Posts': 'https://www.royalsreview.com/rss/index.xml',
    'Royals – FanGraphs Baseball': 'https://www.fangraphs.com/blogs/category/teams/royals/feed/',
    'Salon.com > amanda_marcotte': 'https://www.salon.com/writer/amanda_marcotte/feed',
    'Sandwich Tribunal': 'https://www.sandwichtribunal.com/feed/',
    'Shellsharks Feeds': 'https://shellsharks.com/feeds/feed.xml',
    'SportsLogos.Net News': 'https://news.sportslogos.net/feed/',
    'The Sunday Long Read': 'https://us9.campaign-archive.com/feed?id=67e6e8a504&u=6e1ae4ac632498a38c1d57c54',
    'The Sword And the Sandwich': 'https://buttondown.com/theswordandthesandwich/rss',
    'Tales of Whoa': 'http://brownforsheriff.tumblr.com/rss',
    'Talking Points Memo': 'https://talkingpointsmemo.com/feed',
    'The Tao of Mac': 'https://taoofmac.com/atom.xml',
    'Tastefully Offensive': 'https://www.tastefullyoffensive.com/feed/',
    'Tech Support': 'https://techsupport.substack.com/feed',
    'Terence Eden’s Blog': 'https://shkspr.mobi/blog/feed/atom/',
    'TerminaL Trove': 'https://terminaltrove.com/blog.xml',
    'Terry Moran': 'https://terrymoran.substack.com/feed',
    'Thinking about...- Timothy Snyder': 'https://snyder.substack.com/feed',
    'Tommy Craggs': 'https://tommycraggs.com/feed/',
    'Trades Ten Years Later': 'https://tradestenyearslater.substack.com/feed',
    'Trout Nation': 'http://jennytrout.com/?feed=rss2',
    'Troy Vassalotti :: Blog': 'https://www.troyv.dev/feed.xml',
    'UnHerd': 'https://unherd.com/feed/',
    'Unnamed Website': 'https://unnamed.website/index.xml',
    'Uses This': 'https://usesthis.com/feed.atom',
    'Whats Good at Trader Joes': 'http://www.whatsgoodattraderjoes.com/feeds/posts/default',
    'The Whimsical Web': 'https://whimsical.club/feed.xml',
    'Why Is This Interesting?': 'https://whyisthisinteresting.substack.com/feed',
    'Window Seat- Stuart Loh': 'https://stuloh.substack.com/feed',
    'Wonder Tools': 'https://wondertools.substack.com/feed',
    'Worrydream': 'https://worrydream.com/feed.xml',
    'Wrong Hands': 'https://wronghands1.com/feed/',
    'x-log': 'https://blog.x-way.org/atom.xml',
    'xandra.cc': 'https://library.xandra.cc/feed/?type=rss',
    'Xe Iaso': 'https://xeiaso.net/blog.rss',
    'Zeldman': 'https://zeldman.com/feed/',
    'Zserge': 'https://zserge.com/rss.xml',
    'ℤ→ℤ': 'https://ztoz.blog/index.xml',
    'stfn.pl': 'https://stfn.pl/rss.xml',
    'starbreaker': 'https://starbreaker.org/index.html/./follow/everything.xml',
    'uncountable.uk': 'https://thoughts.uncountable.uk/feed',
    'Essential Thinker': 'https://essentialthinker.com/feed/',
    'ivndbt': 'https://ivndbt.com/rss.xml',
    'boretti': 'https://borretti.me/feed',
    'everything changes' : 'https://everythingchanges.us/feed.xml',
    'Tall Snarky Canadian': 'https://snarky.ca/rss/',
    'Hugh Rundle': 'https://www.hughrundle.net/atom.xml',
    'Harsh Shandya': 'https://msfjarvis.dev/index.xml',
    'koaning': 'https://koaning.io/feed.xml',
    'cottongeeks': 'https://www.cottongeeks.com/rss.xml',
    'The Checkout': 'https://grocerynerd.substack.com/feed',
    'Hugo van Kemenade': 'https://hugovk.dev/blog/index.xml',
    'Lukes Wild Website': 'https://www.lkhrs.com/blog/index.xml',
    'Pointers Gone Wild': 'https://pointersgonewild.com/rss.xml',
    'Legal LOLz Unfiltered': 'https://lolzunfiltered.substack.com/feed',
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
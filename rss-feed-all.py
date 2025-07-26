import requests
import feedparser
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from tqdm import tqdm

rss_feeds = {
    '/dev/lawyer': 'https://writing.kemitchell.com/feed.xml',
    'Alexwlchan': 'https://alexwlchan.net/atom.xml',
    'The American Pamphleteer': 'https://ladylibertie.substack.com/feed',
    'amiantos': 'https://amiantos.net/feed/',
    'Ana Rodrigues': 'https://ohhelloana.blog/feed.xml',
    'Anarcat': 'https://anarc.at/blog/index.rss',
    'Andrew Gallant': 'https://blog.burntsushi.net/index.xml',
    'Andy Bell': 'https://bell.bz/feed.xml',
    'Anil Dash': 'https://www.anildash.com/feed.xml',
    'Antipope': 'http://www.antipope.org/charlie/blog-static/atom.xml',
    'antirez': 'https://antirez.com/rss',
    'Anya Prosvetova': 'https://www.anyalitica.dev/feed.xml',
    'App Defaults': 'https://defaults.rknight.me/feed.xml',
    'AppAddict': 'https://appaddict.app/feed.atom',
    'Armin Ronacher': 'https://lucumr.pocoo.org/feed.atom',
    'Austin Henley': 'https://austinhenley.com/blog/feed.rss',
    'Awful Announcing': 'https://awfulannouncing.com/feed',
    'Baeldung on Linux': 'https://feeds.feedblitz.com/baeldung/linux',
    'Bart de Goede': 'https://bart.degoe.de/index.xml',
    'Baty.net': 'https://baty.net/index.xml',
    'Bicycle For Your Mind': 'https://bicycleforyourmind.com/feed.rss',
    'Billmill.org': 'https://notes.billmill.org/atom.xml',
    'Birchtree': 'https://birchtree.me/rss/',
    'bitches gotta eat!': 'https://bitchesgottaeat.substack.com/feed',
    'BitDoze': 'https://www.bitdoze.com/rss.xml',
    'bitecode': 'https://www.bitecode.dev/feed',
    'Bitfield consulting': 'https://bitfieldconsulting.com/posts?format=rss',
    'The Bored Horse': 'https://bored.horse/feed.xml',
    'Brett Terpstra': 'http://brett.trpstra.net/brettterpstra',
    'Bruce Sterling': 'https://bruces.medium.com/feed',
    'Bryan Maniotakis': 'https://bryanmanio.com/feed/',
    'bt': 'https://btxx.org/index.rss',
    'but shes a girl...': 'https://www.rousette.org.uk/index.xml',
    'Cal Paterson': 'https://calpaterson.com/calpaterson.rss',
    'Chabik': 'https://chabik.com/rss/',
    'Chefie Data Newsletter': 'https://nouman10.substack.com/feed',
    'Chop Wood, Carry Water': 'https://chopwoodcarrywaterdailyactions.substack.com/feed',
    'Chris Coyier': 'https://chriscoyier.net/feed/',
    'Christian Tietze': 'https://christiantietze.de/feed.atom',
    'claromes': 'https://claromes.com/feeds/rss.xml',
    'Confessions of a Data Guy': 'https://www.confessionsofadataguy.com/feed/',
    'ContraBandCamp': 'https://www.contrabandcamp.com/feed',
    'The Contrarian': 'https://contrarian.substack.com/feed',
    'Cool As Heck': 'https://cool-as-heck.blog/feed/',
    'The Copetti site': 'https://www.copetti.org/index.xml',
    'Curtis McHale': 'https://curtismchale.ca/feed/',
    'Dan Sinkers Blog': 'https://dansinker.com/feed.xml',
    'Danny Funt+': 'https://dannyfunt.substack.com/feed',
    'Darek Kay': 'https://darekkay.com/atom.xml',
    'daverupert.com': 'https://daverupert.com/atom.xml',
    'David Pape': 'https://www.zyzzyxdonta.net/index.xml',
    'Democracy Docket': 'https://www.democracydocket.com/feed/',
    'DepthHub': 'https://www.reddit.com/r/DepthHub/.rss',
    'Developer With a Cat': 'https://developerwithacat.com/rss.xml',
    'Django Andy': 'https://djangoandy.com/feed/',
    'Dmitry Frank': 'https://dmitryfrank.com/lib/plugins/feed/feed.php?plugin=blog&fn=getBlog&ns=blog&title=Blog',
    'Drew deVault': 'https://drewdevault.com/blog/index.xml',
    'Dynomight': 'https://dynomight.net/feed.xml',
    'Ed Zitrons Wheres Your Ed At': 'https://www.wheresyoured.at/feed',
    'Ellane W': 'https://ellanew.com/feed.rss',
    'Email is good.': 'https://email-is-good.com/feed/',
    'Eric Ma': 'https://ericmjl.github.io/blog/',
    'Ethan Persoff': 'https://www.ep.tc/rss.xml',
    'Evan Miller': 'https://www.evanmiller.org/news.xml',
    'Farm to Fountains': 'https://farmtofountains.com/feed/',
    'Flow State': 'https://www.flowstate.fm/feed',
    'Fogknife': 'https://fogknife.com/atom.xml',
    'Fractal Kitty': 'https://www.fractalkitty.com/rss/',
    'Friends of Type': 'https://feeds.feedburner.com/FriendsOfType',
    'Gin and Tacos': 'http://www.ginandtacos.com/feed/',
    'Git Gist': 'http://gitgist.com/index.xml',
    'Gwern.net Newsletter': 'https://gwern.substack.com/feed/',
    'Hackaday': 'https://hackaday.com/feed/',
    'Hanselman': 'https://www.hanselman.com/blog/feed/rss',
    'Here Fot It- R. Eric Thomas': 'https://letter.rericthomas.com/rss/',
    'hjr265.me': 'https://hjr265.me/blog/index.xml',
    'How Gambling Works': 'https://howgamblingworks.substack.com/feed',
    'i.webthings.hub': 'https://iwebthings.joejenett.com/feed.atom',
    'inessential': 'https://inessential.com/feed.json',
    'Ineza Bonté': 'https://www.ineza.codes/rss.xml',
    'Infinite Wishes': 'https://emmas.site/blog/atom.xml',
    'Interconnected': 'https://interconnected.org/home/feed',
    'Into The Fountains': 'https://intothefountains.substack.com/feed',
    'Jack H. Peterson': 'https://jackhpeterson.com/atom.xml',
    'James Coffee Blog': 'https://jamesg.blog/feeds/posts.xml',
    'Julia Evans': 'https://jvns.ca/atom.xml',
    'jwz': 'https://cdn.jwz.org/blog/feed/',
    'Kalzumeus': 'https://www.kalzumeus.com/feed/articles/',
    'Kansas City Royals – MLB Trade Rumors': 'https://www.mlbtraderumors.com/kansas-city-royals/feed/atom',
    'Katherine Yang': 'https://kayserifserif.place/feed.xml',
    'KCUR- Local Food ': 'https://www.kcur.org/tags/local-food.rss',
    'Kendra Little': 'https://kendralittle.com/blog/rss.xml',
    'kenpoms thoughts': 'https://kenpom.substack.com/feed/',
    'Kicks Condor': 'https://www.kickscondor.com/feed.xml',
    'kk.org': 'https://kk.org/feed',
    'Laura Hilliger': 'https://www.laurahilliger.com/feed/',
    'Laura Olin': 'https://buttondown.com/lauraolin/rss',
    'Lazybear': 'https://lazybea.rs/index.xml',
    'Live Laugh Blog': 'https://livelaugh.blog/rss.xml',
    'LJPUK': 'https://ljpuk.net/feed/',
    'LostFocus': 'https://lostfocus.de/feed/',
    'Lucian Truscott Newsletter': 'https://luciantruscott.substack.com/feed',
    'Luke Muehlhauser': 'http://lukemuehlhauser.com/feed/',
    'Unbreaking': 'https://unbreaking.org/blog/feed.xml',
    'Maggie Appleton': 'https://maggieappleton.com/rss.xml',
    'marsja.se': 'https://www.marsja.se/feed',
    'Martin Fowler': 'https://martinfowler.com/feed.atom',
    'Math & Programming': 'https://www.jeremykun.com/index.xml',
    'Mathspp': 'https://mathspp.com/blog.atom',
    'Matthew Lyon': 'https://lyonhe.art/index.xml',
    'mattrighetti': 'https://mattrighetti.com/feed.xml',
    'maya.land': 'https://maya.land/feed.xml',
    'Meditations In An Emergency': 'https://www.meditationsinanemergency.com/rss/',
    'Men Yell At Me': 'https://lyz.substack.com/feed?sectionId=54096',
    'Mike Tanier': 'https://miketanier.substack.com/feed',
    'The Nation- Electoral Reform': 'https://www.thenation.com/feed/?post_type=article&subject=electoral-reform',
    'The Nation- Supreme Court': 'https://www.thenation.com/feed/?post_type=article&subject=supreme-court',
    'Neal Stephenson': 'https://nealstephenson.substack.com/feed',
    'Ned Batchelder': 'http://nedbatchelder.com/blog/rss.xml',
    'Neil’s Substack': 'https://neilpaine.substack.com/feed',
    'The New Stack': 'https://thenewstack.io/blog/feed/',
    'ni.har': 'https://nih.ar/rss.xml',
    'Nicola Iarocci': 'https://nicolaiarocci.com/index.xml',
    'Null Bitmap': 'https://buttondown.com/jaffray/rss',
    'null program- Chris Wellons': 'https://nullprogram.com/feed/',
    'Omar Rizwan': 'https://omar.website/posts/index.xml',
    'Own Your Web': 'https://buttondown.email/ownyourweb/rss',
    'Patrick Van der Spiegels Posts': 'https://patrick.vanderspie.gl/posts/index.xml',
    'Paul Gross': 'https://www.pgrs.net/feed.xml',
    'Paul Kinlan': 'https://paul.kinlan.me/index.xml',
    'Perl Hacks': 'https://perlhacks.com/feed/',
    'The Perry Bible Fellowship': 'https://pbfcomics.com/feed/',
    'plover': 'https://blog.plover.com/index.rss',
    'Process Things - Code': 'https://exch.gr/code/feed.xml',
    'Process Things - Essays': 'https://exch.gr/essays/feed.xml',
    'PyBites': 'https://pybit.es/feed/',
    'PyCoders Weekly': 'https://pycoders.com/feed/T8SjZAIK',
    'PyMOTW on Doug Hellmann': 'https://feeds.feedburner.com/PyMOTW',
    'Python In Office': 'https://pythoninoffice.com/feed/',
    'Python Insider': 'https://blog.python.org/feeds/posts/default',
    'Qubyte Codes': 'https://qubyte.codes/social.atom.xml',
    'Raymond Camden': 'https://www.raymondcamden.com/feed.xml',
    'read-only': 'https://read-only.net/feed.xml',
    'Recomendo': 'https://www.recomendo.com/feed',
    'Reilly Spitzfaden': 'https://reillyspitzfaden.com/blog/feed.xml',
    'Robin Rendle': 'https://buttondown.com/robinrendle/rss',
    'Rosemary Orchard |': 'https://rosemaryorchard.com/feed.xml',
    'Royals Farm Report': 'https://royalsfarmreport.com/feed/',
    'Royals Review -  All Posts': 'https://www.royalsreview.com/rss/index.xml',
    'Royals – FanGraphs Baseball': 'https://www.fangraphs.com/blogs/category/teams/royals/feed/',
    'Rubenerd': 'http://showfeed.rubenerd.com/',
    'Schemescape': 'https://log.schemescape.com/feed.xml',
    'Scott Aaronson': 'https://scottaaronson.blog/?feed=rss2',
    'Sergis writing': 'https://sergiswriting.com/atom.xml',
    'Shellsharks Feeds': 'https://shellsharks.com/feeds/feed.xml',
    'Simone': 'https://simone.org/rss/',
    'SportsLogos.Net News': 'https://news.sportslogos.net/feed/',
    'SQL Shack – articles about database auditing, server performance, data recovery, and more': 'https://www.sqlshack.com/feed/',
    'Steven A. Guccione': 'https://stevesaltfacebook.blog/feed/',
    'The Sunday Long Read': 'https://us9.campaign-archive.com/feed?id=67e6e8a504&u=6e1ae4ac632498a38c1d57c54',
    'TerminaL Trove': 'https://terminaltrove.com/blog.xml',
    'Tommy Craggs': 'https://tommycraggs.com/feed/',
    'Troy Vassalotti :: Blog': 'https://www.troyv.dev/feed.xml',
    'UnHerd': 'https://unherd.com/feed/',
    'Unnamed Website': 'https://unnamed.website/index.xml',
    'The Useless Web': 'https://theuselessweb.com/sites/index.xml',
    'Uses This': 'https://usesthis.com/feed.atom',
    'The Verge Installer Newsletter': 'https://www.theverge.com/rss/installer-newsletter/index.xml',
    'Vicki Boykis': 'https://vickiboykis.com/index.xml',
    'Werd I/O': 'https://granary.io/url?url=https://werd.io/content/all/&input=html&output=atom&hub=https://bridgy-fed.superfeedr.com/',
    'The Whimsical Web': 'https://whimsical.club/feed.xml',
    'Why Is This Interesting?': 'https://whyisthisinteresting.substack.com/feed',
    'wilw.dev': 'https://wilw.dev/rss.xml',
    'Wonder Tools': 'https://wondertools.substack.com/feed',
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
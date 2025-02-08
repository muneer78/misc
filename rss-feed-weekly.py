import requests
import feedparser
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from tqdm import tqdm

rss_feeds = {
    'Andscape': 'https://andscape.com/feed',
    'Supreme Court – The Nation': 'https://www.thenation.com/feed/?post_type=article&subject=supreme-court',
    'Electoral Reform – The Nation': 'https://www.thenation.com/feed/?post_type=article&subject=electoral-reform',
    'ProPublica': 'https://www.propublica.org/feeds/54Ghome',
    # 'Arts & Letters Daily': 'http://ftr.fivefilters.org/makefulltextfeed.php?url=www.aldaily.com/feed/&max=3&links=preserve',
    'Atlas Obscura': 'https://www.atlasobscura.com/feeds/latest',
    'Attack of the 50 Foot Blockchain': 'https://davidgerard.co.uk/blockchain/feed/',
    'Awesome Python Weekly': 'https://python.libhunt.com/newsletter/feed',
    'Awful Announcing': 'https://awfulannouncing.com/feed',
    'Balls and Strikes': 'https://ballsandstrikes.org/feed/',
    'Baseball America': 'https://feeds.redcircle.com/54051e90-c6e1-43ac-9a01-4c8fc92bc79d',
    'Baseball Prospectus': 'https://www.baseballprospectus.com/feed/',
    'Baseballmusings.com': 'http://feeds2.feedburner.com/Baseballmusingscom',
    'Boing Boing': 'http://feeds.boingboing.net/boingboing/iBag',
    'Book Marks': 'https://bookmarks.reviews/category/features/feed/',
    'Brand Eating': 'https://www.brandeating.com/feeds/posts/default',
    'Teen Vogue': 'https://politepol.com/fd/Vjc601sG0jpO.xml',
    'Brian Moylan Author Archive': 'https://politepol.com/fd/VoicyDwzX43M.xml',
    'Budget Bytes': 'https://budgetbytes.com/feed/',
    'Bustle': 'https://www.bustle.com/rss',
    'CaptainAwkward.com': 'https://captainawkward.com/feed/',
    'Daring Fireball': 'https://daringfireball.net/feeds/main',
    'DepthHub': 'https://www.reddit.com/r/DepthHub/.rss',
    'Election Law Blog': 'https://electionlawblog.org/?feed=rss2',
    'FanGraphs Baseball': 'https://blogs.fangraphs.com/feed/',
    'FanGraphs Fantasy Baseball': 'http://feeds.feedburner.com/RotoGraphs',
    'Farm To Fountain': 'https://farmtofountains.com/feed/',
    'Fast Food News': 'https://www.fastfoodmenuprices.com/news/feed/',
    'Food & Drink – The Pitch': 'https://www.thepitchkc.com/category/food-drink/feed/',
    'Food : NPR': 'https://feeds.npr.org/1053/rss.xml',
    'Foodbeast Products': 'https://www.foodbeast.com/./products/feed/',
    'TechCrunch Gadgets': 'https://techcrunch.com/gadgets/feed/',
    'Gizmodo': 'https://gizmodo.com/rss',
    'Groceries | Eat This, Not That!': 'https://rss.app/feeds/JKtAQLtZCtIyjikJ.xml',
    'Hacker News: Show HN': 'https://hnrss.org/show',
    'Harpers Magazine': 'http://harpers.org/feed/',
    # 'Hatewatch | Southern Poverty Law Center': 'https://www.splcenter.org/hatewatch/rss.xml',
    'HolyPython.com': 'https://holypython.com/feed/',
    'Kansas City Royals – MLB Trade Rumors': 'https://www.mlbtraderumors.com/kansas-city-royals/feed/atom',
    'kottke.org': 'http://feeds.kottke.org/main',
    'Lamebook - Funny Facebook Statuses, Fails, LOLs and More - The Original': 'http://feeds.feedburner.com/Lamebook',
    'Laughing Squid': 'http://laughingsquid.com/feed/',
    'Legal Profession Blog': 'http://feeds.feedburner.com/LegalProfessionBlog',
    'LifeHacker': 'https://lifehacker.com/feed/rss',
    'KCUR- Local Food ': 'https://www.kcur.org/tags/local-food.rss',
    'Longreads': 'https://longreads.com/feed/',
    'Lowering the Bar': 'http://feeds.feedblitz.com/loweringthebar&x=1',
    'Marginal REVOLUTION': 'http://marginalrevolution.com/feed',
    'Matt Bruenig Dot Com': 'https://mattbruenig.com/feed/',
    'Mental Floss': 'https://www.mentalfloss.com/rss.xml',
    'Misc Newsletters': 'https://kill-the-newsletter.com/feeds/5mr68b7cb43ac2h04ai5.xml',
    'Neatorama': 'http://www.neatorama.com/feed',
    'The Pitch': 'https://www.thepitchkc.com/category/news-52777/feed/',
    'Open Culture': 'https://www.openculture.com/feed',
    'Paul Krugman': 'https://paulkrugman.substack.com/feed',
    'Pitch Weekly': 'https://www.thepitchkc.com/feed/',
    'Pitcher List': 'http://www.pitcherlist.com/feed/',
    'Pluralistic: Daily links from Cory Doctorow': 'https://pluralistic.net/feed/',
    'Popular Information': 'https://popular.info/feed',
    'Poynter': 'https://www.poynter.org/feed/',
    'ProPublica': 'http://feeds.propublica.org/propublica/main',
    'Public Notice': 'https://www.publicnotice.co/feed',
    'PyMOTW on Doug Hellmann': 'https://feeds.feedburner.com/PyMOTW',
    'Python Weekly': 'http://us2.campaign-archive1.com/feed?u=e2e180baf855ac797ef407fc7&id=9e26887fc5',
    # 'Right Wing Watch': 'https://www.rightwingwatch.org/feed/',
    'RotoGraphs Fantasy Baseball': 'https://fantasy.fangraphs.com/feed/',
    'Royals Farm Report': 'https://royalsfarmreport.com/feed/',
    'Royals Review -  All Posts': 'https://www.royalsreview.com/rss/index.xml',
    'Royals – FanGraphs Baseball': 'https://www.fangraphs.com/blogs/category/teams/royals/feed/',
    'Salon.com > amanda_marcotte': 'https://www.salon.com/writer/amanda_marcotte/feed',
    'SportsLogos.Net News': 'https://news.sportslogos.net/feed/',
    'Tedium: The Dull Side of the Internet.': 'https://feed.tedium.co/',
    'The Bulwark': 'https://thebulwark.com/feed/',
    'The Electric Typewriter': 'http://tetw.org/rss',
    'The Impulsive Buy': 'https://www.theimpulsivebuy.com/wordpress/feed/',
    'The Intercept': 'https://theintercept.com/feed/?_=1382',
    'The Root': 'https://www.theroot.com/rss',
    'The Tao of Mac': 'https://taoofmac.com/atom.xml',
    'Whats Good at Trader Joes': 'http://www.whatsgoodattraderjoes.com/feeds/posts/default',
    'Whatever': 'https://whatever.scalzi.com/feed/',
    'Wonkette': 'http://wonkette.com/feed',
    'Work Stories, Humor, Memes, News | Pleated Jeans': 'https://pleated-jeans.com/category/work/feed/',
    'xkcd.com': 'http://xkcd.com/rss.xml',
    'Antiwork - Ruin My Week': 'https://ruinmyweek.com/search/antiwork/feed/rss2/',
    'Current Affairs': 'https://www.currentaffairs.org/news/rss.xml',
    'bitecode': 'https://www.bitecode.dev/feed',
    'Blogofthe.Day': 'https://blogofthe.day/feed.xml',
    'Danny Funt+': 'https://dannyfunt.substack.com/feed',
    # 'Invent with Python': 'https:/inventwithpython.com/blog/feeds/all.atom.xml',
    'Mouse vs. Python': 'https://www.blog.pythonlibrary.org/feed/',
    'Ned Batchelder': 'http://nedbatchelder.com/blog/rss.xml',
    'Planet Python': 'https://planetpython.org/rss20.xml',
    'Pudding.cool': 'https://pudding.cool/feed.xml',
    'Python Insider': 'https://blog.python.org/feeds/posts/default',
    'Perl Hacks': 'https://perlhacks.com/feed/',
    'PyBites': 'https://pybit.es/feed/',
    'PyCoders Weekly': 'https://pycoders.com/feed/T8SjZAIK',
    'Python Morsels': 'https://www.pythonmorsels.com/topics/feed/',
    'The Python Papers': 'https://www.pythonpapers.com/feed',
    'The Python Rabbithole': 'https://zlliu.substack.com/feed',
    'Trades Ten Years Later': 'https://tradestenyearslater.substack.com/feed',
    'someecards': 'https://www.someecards.com/rss/homepage.xml',
    'Not Always Legal': 'https://notalwaysright.com/legal/feed/',
    'Not Always Right- Inspirational': 'https://notalwaysright.com/tag/inspirational/feed/',
    'Sandwich Tribunal': 'https://www.sandwichtribunal.com/feed/',
    'WebCurios': 'https://webcurios.co.uk/feed/', 
    'Recomendo': 'https://www.recomendo.com/feed',
    'McFilter': 'http://www.mcqn.net/mcfilter/index.xml',
    'Robin Sloan': 'https://www.robinsloan.com/feed.xml',
    'One Point Zero': 'https://onepointzero.com/feed/basic',
    'Patrick Van der Spiegels Posts': 'https://patrick.vanderspie.gl/posts/index.xml',
    'daverupert.com': 'https://daverupert.com/atom.xml',
    'Bicycle For Your Mind': 'https://bicycleforyourmind.com/feed.rss',
    'Django Andy': 'https://djangoandy.com/feed/',
    'Rubenerd': 'http://showfeed.rubenerd.com/',
    'Ali Reza Hayati': 'https://alirezahayati.com/feed/',
    'Bart de Goede': 'https://bart.degoe.de/index.xml',
    'Lazybear': 'https://lazybea.rs/index.xml',
    'read-only': 'https://read-only.net/feed.xml',
    'Blog on hjr265.me': 'https://hjr265.me/blog/index.xml',
    'Tomorrows Baseball Today': 'https://tbtmlb.substack.com/feed',
    'LOL (lots of links)': 'https://lotsoflinks.substack.com/feed',
    'Scriveners Error': 'https://scrivenerserror.blogspot.com/feeds/posts/default?alt=rss',
    'i.webthings.hub': 'https://iwebthings.joejenett.com/feed.atom',
    'App Defaults': 'https://defaults.rknight.me/feed.xml',
    'TYWKIWDBI      ("Tai-Wiki-Widbee")': 'https://tywkiwdbi.blogspot.com/feeds/posts/default',
    'mathspp.com feed': 'https://mathspp.com/blog.atom',
    'Kimberly Hirsh': 'https://kimberlyhirsh.com/feed.xml',
    'One Foot Tsunami': 'https://onefoottsunami.com/feed/atom/',
    'Robin Rendle': 'https://robinrendle.com/feed.xml','ArtButMakeItSports': 'https://www.artbutmakeitsports.com/feed',
    'Flow State': 'https://www.flowstate.fm/feed',
    'local food': 'https://www.kcur.org/tags/local-food.rss',
    'Fix The News': 'https://fixthenews.com/rss/',
    'LinkMachineGo': 'https://www.timemachinego.com/linkmachinego/feed/',
    'FoxTrot Comics by Bill Amend': 'https://foxtrot.com/feed/',
    'Qubyte Codes': 'https://qubyte.codes/social.atom.xml',
    'Food & Drink Archives | The Pitch': 'https://www.thepitchkc.com/category/food-drink/feed/',
    'Ellane W': 'https://ellanew.com/feed.rss',
    'Rosemary Orchard |': 'https://rosemaryorchard.com/feed.xml',
    'Vaporwave Van Gogh': 'https://vaporwave-van-gogh.tumblr.com/rss',
    'Own Your Web': 'https://buttondown.email/ownyourweb/rss',
    'maya.land': 'https://maya.land/feed.xml',
    'The Bored Horse': 'https://bored.horse/feed.xml',
    'Julia Evans': 'https://jvns.ca/atom.xml',
    'Ana Rodrigues': 'https://ohhelloana.blog/feed.xml',
    'Topic: Bet ftw': 'https://news.google.com/rss/search?q=Bet%20ftw',
    'Agile &amp; Coding': 'https://davidvujic.blogspot.com/feeds/posts/default?alt=rss',
    'Amadeus Maximilian’s Blog': 'https://amxmln.com/rss.xml',
    'Infinite Wishes 🏳️‍⚧️🚀': 'https://emmas.site/blog/atom.xml',
    'Process Things - Essays': 'https://exch.gr/essays/feed.xml',
    'Process Things - Code': 'https://exch.gr/code/feed.xml',
    'ongoing by Tim Bray': 'http://www.tbray.org/ongoing/ongoing.atom',
    'what are the haps': 'https://ryannorth.tumblr.com/rss',
    'mattrighetti': 'https://mattrighetti.com/feed.xml',
    'Amelia Wattenberger': 'https://wattenberger.com/rss.xml',
    'Dan Sinkers Blog': 'https://dansinker.com/feed.xml',
    'Jack H. Peterson': 'https://jackhpeterson.com/atom.xml',
    'Jan-Lukas Else': 'https://jlelse.blog/.rss',
    'Terence Eden’s Blog': 'https://shkspr.mobi/blog/feed/atom/',
    'The Sunday Long Read subscribers Archive Feed': 'https://us9.campaign-archive.com/feed?u=6e1ae4ac632498a38c1d57c54&id=67e6e8a504',
    'Live Laugh Blog': 'https://livelaugh.blog/rss.xml',
    'Harpers Magazine': 'https://harpers.org/feed/',
    'Kev Quirk': 'https://kevquirk.com/feed',
    'Chris DeLuca': 'https://www.chrisdeluca.me/feed.xml',
    'Michael Burkhardts Whirled Wide Web': 'https://mihobu.lol/rss.xml',
    'kevin spencer': 'https://kevinspencer.org/posts/feed/',
    'IndieNews English': 'https://granary.io/url?input=html&output=atom&url=https%3A%2F%2Fnews.indieweb.org%2Fen',
    'Pixel Envy': 'https://feedpress.me/pxlnv',
    'snarfed.org': 'https://snarfed.org/feed',
    'Michael Sippey': 'https://sippey.com/rss.xml',
    'Interconnected': 'https://interconnected.org/home/feed',
    'Neil’s Substack': 'https://neilpaine.substack.com/feed',
    'Read Rodge': 'https://rodgersherman.substack.com/feed',
    'splitbrain.org - blog': 'https://www.splitbrain.org/feed/blog',
    'Nabeel Valley': 'https://nabeelvalley.co.za/feed/rss.xml',
    'AppAddict': 'https://appaddict.app/feed.atom',
    'Computers, internet, tech: Recently added blogs and sub-categories at ooh.directory': 'https://ooh.directory/feeds/cats/b7q2w7/rss/technology.xml',
    'Into The Fountains': 'https://intothefountains.substack.com/feed',
    'Miss Cellania': 'https://misscellania.blogspot.com/feeds/posts/default?alt=rss',
    'Veronica Writes': 'https://berglyd.net/feed.xml',
    'Email is good.': 'https://email-is-good.com/feed/',
    'LostFocus': 'https://lostfocus.de/feed/',
    'Sergis writing': 'https://sergiswriting.com/atom.xml',
    'Chris Coyier': 'https://chriscoyier.net/feed/',
    'Some Bits: Nelsons Linkblog': 'https://www.somebits.com/linkblog/index.atom',
    'Ineza Bonté': 'https://www.ineza.codes/rss.xml',
    'krrd.ing': 'https://krrd.ing/rss.xml',
    'Maggie Appleton': 'https://maggieappleton.com/rss.xml',
    'User Mag': 'https://www.usermag.co/feed',
    'The Candybox Blog': 'http://www.nathalielawhead.com/candybox/feed',
    'The Sword And the Sandwich': 'https://buttondown.com/theswordandthesandwich/rss',
    'Tantek Çelik': 'https://tantek.com/updates.atom',
    'Hackaday': 'https://hackaday.com/feed/',
    'Links I Would Gchat You If We Were Friends': 'https://linksiwouldgchatyou.substack.com/feed',
    'A Collection of Unmitigated Pedantry': 'https://acoup.blog/feed/',
    'Notes by JCProbably': 'https://notes.jeddacp.com/feed/',
    'Nicola Iarocci': 'https://nicolaiarocci.com/index.xml',
    'Chris Glass': 'https://chrisglass.com/feed/',
    'Joes Weather Blog': 'https://fox4kc.com/weather/weather-blog/feed/',
    'Baty.net': 'https://baty.net/index.xml',
    'but shes a girl...': 'https://www.rousette.org.uk/index.xml',
    'Law Dork': 'https://www.lawdork.com/feed',
    'Bookmarks – Chris Glass': 'https://chrisglass.com/links/feed/',
    'Birchtree': 'https://birchtree.me/rss/',
    'Longreads': 'https://longreads.com/feed/',
    'Molly Whites activity feed': 'https://www.mollywhite.net/feed/feed.xml',
    'arun.is': 'https://arun.is/rss.xml',
    'Werd I/O': 'https://granary.io/url?url=https://werd.io/content/all/&input=html&output=atom&hub=https://bridgy-fed.superfeedr.com/',
    'Trout Nation': 'http://jennytrout.com/?feed=rss2',
    'Andy Bell': 'https://bell.bz/feed.xml',
    'bitches gotta eat!': 'https://bitchesgottaeat.substack.com/feed',
    'Ed Zitrons Wheres Your Ed At': 'https://www.wheresyoured.at/feed',
    'Troy Vassalotti :: Blog': 'https://www.troyv.dev/feed.xml',
    'Katherine Yang': 'https://kayserifserif.place/feed.xml',
    'WARREN ELLIS LTD': 'https://warrenellis.ltd/feed/',
    'Linkblog': 'https://www.splitbrain.org/feed/links',
    'This Week in the IndieWeb': 'https://indieweb.org/this-week/feed.xml',
    'x-log': 'https://blog.x-way.org/atom.xml',
    'Konfetti Explorations Feeds': 'https://marisabel.nl/feeds/combined.php',
    'Sandwich Tribunal': 'https://www.sandwichtribunal.com/feed/',
    'ReedyBears Blog': 'https://reedybear.bearblog.dev/feed/',
    'Steven A. Guccione': 'https://stevesaltfacebook.blog/feed/',
    'Chris Shaw': 'https://thoughts.uncountable.uk/feed',
    'Chriss Wiki :: blog': 'https://utcc.utoronto.ca/~cks/space/blog/?atom',
    'Linux Journal - The Original Magazine of the Linux Community': 'http://www.linuxjournal.com/node/feed',
    'bt RSS Feed': 'https://btxx.org/index.rss',
    'The Electric Typewriter': 'https://electrictype.substack.com/feed',
    'Robin Rendle': 'https://buttondown.com/robinrendle/rss',
    'LinuxInsider': 'http://www.linuxinsider.com/perl/syndication/rssfull.pl',
    '/dev/lawyer': 'https://writing.kemitchell.com/feed.xml',
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
            print(f"No entries found for {site_name}.")
            return pd.DataFrame()

        # Filter entries from the last 2 weeks
        one_week_ago = datetime.now() - timedelta(weeks=1)
        recent_entries = [entry for entry in entries if 'published_parsed' in entry and datetime(*entry.published_parsed[:6]) > one_week_ago]

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

# Sort the rss_feeds dictionary by keys without paying attention to capitalization
sorted_rss_feeds = dict(sorted(rss_feeds.items(), key=lambda item: item[0].lower()))

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
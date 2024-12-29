import requests
import feedparser
import pandas as pd
from pathlib import Path
from datetime import datetime

rss_feeds = {
    '404 Media': 'https://www.404media.co/rss/',
    'ADHD and Marriage': 'https://www.adhdmarriage.com/rss.xml',
    'ADHD Roller Coaster — Gina Pera': 'https://adhdrollercoaster.org/feed/',
    'All Sports Books': 'https://allsportsbookreviews.substack.com/feed',
    'angrypolymath.com': 'http://angrypolymath.com/?feed=rss2',
    'Art Wear | A T-shirt and Screen Printing Blog': 'http://art-wear.org/blog/?feed=rss2',
    'Article – The Nation': 'https://www.thenation.com/feed/?post_type=article&subject=supreme-court',
    'Article – The Nation': 'https://www.thenation.com/feed/?post_type=article&subject=electoral-reform',
    'Arts & Letters Daily': 'http://ftr.fivefilters.org/makefulltextfeed.php?url=www.aldaily.com/feed/&max=3&links=preserve',
    'Attack of the 50 Foot Blockchain': 'https://davidgerard.co.uk/blockchain/feed/',
    'Awful Announcing': 'https://awfulannouncing.com/feed',
    'Balkinization': 'https://balkin.blogspot.com/feeds/posts/default',
    'Barking Up The Wrong Tree': 'https://www.bakadesuyo.com/feed/',
    'Book Marks Features | Book Marks': 'https://bookmarks.reviews/category/features/feed/',
    'Bygonely': 'https://www.bygonely.com/feed/',
    'CaptainAwkward.com': 'https://captainawkward.com/feed/',
    'Cerealously': 'http://www.cerealously.net/feed/',
    'Chefie Data Newsletter': 'https://nouman10.substack.com/feed',
    'Columbia Journalism Review': 'http://www.cjr.org/feed',
    'Commonplace - The Commoncog Blog': 'https://commoncog.com/blog/rss/',
    'Confessions of a Data Guy': 'https://www.confessionsofadataguy.com/feed/',
    'Crooked Timber': 'https://crookedtimber.org/feed/',
    'CROW’s Substack': 'https://crownewsletter.substack.com/feed',
    'Current Affairs': 'https://www.currentaffairs.org/news/rss.xml'
    'Damn Interesting': 'http://www.damninteresting.com/?feed=rss2',
    'Discourse Blog': 'https://discourseblog.substack.com/feed/',
    'Discourse.net': 'https://www.discourse.net/feed/',
    'Dissent Magazine': 'https://www.dissentmagazine.org/feed',
    'Duck of Minerva': 'https://duckofminerva.com/feed',
    'DudeFoods.com – Food Recipes & Videos': 'http://dudefoods.com/feed/',
    'emptywheel': 'https://www.emptywheel.net/feed/',
    'Eschaton': 'https://www.eschatonblog.com/feeds/posts/default',
    'Excess of Democracy': 'https://excessofdemocracy.com/blog?format=rss',
    'Five Books': 'https://fivebooks.com/feed/',
    'Freedom to Tinker': 'https://freedom-to-tinker.com/feed/',
    'Futility Closet': 'http://feeds.feedburner.com/FutilityCloset',
    'Garbage Day': 'https://rss.beehiiv.com/feeds/owMwaGYU36.xml',
    'Gin and Tacos': 'http://www.ginandtacos.com/feed/',
    'GM Games – Sports General Manager Video Games': 'https://gmgames.org/feed/',
    'GQ': 'https://www.gq.com/feed/rss',
    'Groceries | Eat This, Not That!': 'https://rss.app/feeds/JKtAQLtZCtIyjikJ.xml',
    'Gwern.net Newsletter': 'https://gwern.substack.com/feed/',
    'Hatewatch | Southern Poverty Law Center': 'https://www.splcenter.org/hatewatch/rss.xml',
    'Hyperfocus and ADHD Articles | ADDitude': 'https://www.additudemag.com/tag/hyperfocus/feed/',
    'Idle Words': 'https://idlewords.com/index.xml',
    'Indexed': 'http://thisisindexed.com/feed/',
    'Jacobin': 'http://jacobinmag.com/feed/',
    'Junk Banter': 'http://junkbanter.com/feed/',
    'kenpoms thoughts': 'https://kenpom.substack.com/feed',
    'Kicks Condor': 'https://www.kickscondor.com/feed.xml',
    'Lamebook - Funny Facebook Statuses, Fails, LOLs and More - The Original': 'http://feeds.feedburner.com/Lamebook',
    'Laughing Squid': 'http://laughingsquid.com/feed/',
    'librarian.net': 'http://librarian.net/feed/',
    'Literary  Hub': 'https://lithub.com/feed/',
    'Lowering the Bar': 'http://feeds.feedblitz.com/loweringthebar&x=1',
    'Luke Muehlhauser': 'http://lukemuehlhauser.com/feed/',
    'Matt Bruenig Dot Com': 'https://mattbruenig.com/feed/',
    'MetaFilter': 'https://rss.metafilter.com/metafilter.rss',
    'Mischiefs of Faction': 'https://www.mischiefsoffaction.com/blog-feed.xml',
    'Miss Cellania': 'https://misscellania.blogspot.com/feeds/posts/default',
    'naked capitalism': 'https://www.nakedcapitalism.com/feed',
    'Narratively': 'https://narratively.com/feed/',
    'Neatorama': 'http://www.neatorama.com/feed',
    'Ness Labs': 'https://nesslabs.com/feed',
    'New York Magazine -- Intelligencer': 'http://feeds.feedburner.com/nymag/intelligencer',
    'New Yorker': 'http://www.newyorker.com/feed/everything',
    'Obsidian Wings': 'https://obsidianwings.blogs.com/obsidian_wings/atom.xml',
    'Ordinary Times': 'https://ordinary-times.com/feed/',
    'Outliner Software': 'https://www.outlinersoftware.com/utils/rss',
    'Outside the Law School Scam': 'http://outsidethelawschoolscam.blogspot.com/feeds/posts/default',
    'Pew Research Center » Fact Tank': 'http://www.pewresearch.org/fact-tank/feed/',
    'Pinpoint Uncertainty': 'http://pinpointuncertainty.blogspot.com/feeds/posts/default',
    'Pitcher List': 'http://www.pitcherlist.com/feed/',
    'Popular Information': 'https://popular.info/feed',
    'Power 3.0 | Authoritarian Resurgence, Democratic Resilience': 'https://www.power3point0.org/feed/podcast/',
    'Poynter': 'https://www.poynter.org/feed/',
    'ProPublica': 'http://feeds.propublica.org/propublica/main',
    'Public Notice': 'https://www.publicnotice.co/feed',
    'Quomodocumque': 'https://quomodocumque.wordpress.com/feed/',
    'Rare Historical Photos': 'https://feeds2.feedburner.com/rarehistoricalphotos',
    'Roads & Kingdoms': 'https://roadsandkingdoms.com/feed/',
    'Skeptical Inquirer': 'https://skepticalinquirer.org/feed/',
    'SQL Shack – articles about database auditing, server performance, data recovery, and more': 'https://www.sqlshack.com/feed/',
    'Standard Ebooks - New Releases': 'https://standardebooks.org/rss/new-releases',
    'STAT': 'https://www.statnews.com/feed/',
    'Steven A. Guccione': 'https://stevesaltfacebook.blog/feed/',
    'Stories by Anmol Tomar on Medium': 'https://anmol3015.medium.com/feed',
    'Stories by Zoumana Keita on Medium': 'https://zoumanakeita.medium.com/feed',
    'Sumana': 'https://brainwane.dreamwidth.org/data/rss',
    'Tales of Whoa': 'http://brownforsheriff.tumblr.com/rss',
    'Texas Monthly': 'https://www.texasmonthly.com//feed',
    'The Audacity of Despair': 'https://davidsimon.com/feed/',
    'The Baffler': 'https://thebaffler.com/feed',
    'The Belly of the Beast': 'https://thelawyerbubble.com/feed/',
    'The Corner | National Review': 'https://www.nationalreview.com/corner/feed/',
    'The Cut': 'http://feeds.feedburner.com/nymag/fashion',
    'the daily howler': 'https://dailyhowler.blogspot.com/feeds/posts/default',
    'The Dispatch': 'https://thedispatch.com/feed/',
    'The Dry Down': 'https://thedrydown.substack.com/feed/',
    'The Generalist Academy': 'https://generalist.academy/feed/',
    'The Junk Food Aisle': 'https://www.thejunkfoodaisle.com/feed/',
    'The Kitchn | Inspiring cooks, nourishing homes': 'http://feeds.feedburner.com/apartmenttherapy/thekitchn',
    'The Law School Tuition Bubble': 'http://lawschooltuitionbubble.wordpress.com/feed/',
    'The Little Professor': 'http://littleprofessor.typepad.com/the_little_professor/atom.xml',
    'The Markup': 'https://themarkup.org/feeds/rss.xml',
    'The Moral High Ground': 'https://evanhurst.substack.com/feed',
    'The New Inquiry': 'http://thenewinquiry.com/feed/',
    'The New Republic': 'https://newrepublic.com/rss.xml',
    'The Perry Bible Fellowship': 'https://pbfcomics.com/feed/',
    'The Quietus': 'https://thequietus.com/feed',
    'The Smart Set': 'https://www.thesmartset.com/feed/',
    'Thomas Frank | The Guardian': 'https://www.theguardian.com/profile/thomas-frank/rss',
    'Tom Pepinsky': 'https://tompepinsky.com/feed/',
    'TPM – Talking Points Memo': 'https://talkingpointsmemo.com/feed',
    'Tyler Cowens Ethnic Dining Guide': 'https://tylercowensethnicdiningguide.com/index.php/feed/',
    'TYWKIWDBI      ("Tai-Wiki-Widbee")': 'https://tywkiwdbi.blogspot.com/feeds/posts/default',
    'Vintage Everyday': 'https://www.vintag.es/feeds/posts/default',
    'Voting Rights Lab': 'https://votingrightslab.org/feed/',
    'Vulture': 'http://feeds.feedburner.com/nymag/vulture',
    'Waging Nonviolence': 'https://wagingnonviolence.org/feed/',
    'Waxy.org': 'https://waxy.org/feed/',
    'Web3 is Going Just Great': 'https://web3isgoinggreat.com/feed.xml',
    'What To Read If': 'https://whattoreadif.substack.com/feed',
    'Whats Good at Trader Joes': 'http://www.whatsgoodattraderjoes.com/feeds/posts/default',
    'Wondermark': 'http://feeds.feedburner.com/wondermark',
    'Your Local Epidemiologist': 'https://yourlocalepidemiologist.substack.com/feed',
    'Zompist’s E-Z rant page': 'https://zompist.wordpress.com/feed/',
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
output_file = output_dir / "rss-feeds-infrequent.html"

dfs = [fetch_feed(site_name, url) for site_name, url in rss_feeds.items()]
df = pd.concat(dfs, ignore_index=True)
rss_df_to_html(df, output_file)
print(f"HTML saved to: {output_file}")
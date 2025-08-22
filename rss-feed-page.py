import requests
import feedparser
import pandas as pd
from pathlib import Path
from datetime import datetime

rss_feeds = {
    "404 Media": "https://www.404media.co/rss/",
    "ADHD and Marriage": "https://www.adhdmarriage.com/rss.xml",
    "ADHD Roller Coaster — Gina Pera": "https://adhdrollercoaster.org/feed/",
    "All Sports Books": "https://allsportsbookreviews.substack.com/feed",
    "Andscape": "https://andscape.com/feed",
    "angrypolymath.com": "http://angrypolymath.com/?feed=rss2",
    "Art Wear | A T-shirt and Screen Printing Blog": "http://art-wear.org/blog/?feed=rss2",
    "Article – The Nation": "https://www.thenation.com/feed/?post_type=article&subject=supreme-court",
    "Article – The Nation": "https://www.thenation.com/feed/?post_type=article&subject=electoral-reform",
    "Articles and Investigations - ProPublica": "https://www.propublica.org/feeds/54Ghome",
    "Arts & Letters Daily": "http://ftr.fivefilters.org/makefulltextfeed.php?url=www.aldaily.com/feed/&max=3&links=preserve",
    "Atlas Obscura - Latest Articles and Places": "https://www.atlasobscura.com/feeds/latest",
    "Attack of the 50 Foot Blockchain": "https://davidgerard.co.uk/blockchain/feed/",
    "Awful Announcing": "https://awfulannouncing.com/feed",
    "Balkinization": "https://balkin.blogspot.com/feeds/posts/default",
    "Balls and Strikes": "https://ballsandstrikes.org/feed/",
    "Barking Up The Wrong Tree": "https://www.bakadesuyo.com/feed/",
    "Baseball America": "https://feeds.redcircle.com/54051e90-c6e1-43ac-9a01-4c8fc92bc79d",
    "Baseball Prospectus": "https://www.baseballprospectus.com/feed/",
    "baseballmusings.com": "http://feeds2.feedburner.com/Baseballmusingscom",
    "Baty.net": "https://baty.net/feed",
    "Bicycle For Your Mind": "http://bicycleforyourmind.com/feed.rss",
    "Boing Boing": "http://feeds.boingboing.net/boingboing/iBag",
    "Book Marks Features | Book Marks": "https://bookmarks.reviews/category/features/feed/",
    "Brand Eating": "https://www.brandeating.com/feeds/posts/default",
    "Teen Vogue": "https://politepol.com/fd/Vjc601sG0jpO.xml",
    "Brian Moylan Author Archive": "https://politepol.com/fd/VoicyDwzX43M.xml",
    "Budget Bytes": "https://budgetbytes.com/feed/",
    "Bustle": "https://www.bustle.com/rss",
    "Bygonely": "https://www.bygonely.com/feed/",
    "CaptainAwkward.com": "https://captainawkward.com/feed/",
    "Cerealously": "http://www.cerealously.net/feed/",
    "Chefie Data Newsletter": "https://nouman10.substack.com/feed",
    "Columbia Journalism Review": "http://www.cjr.org/feed",
    "Commonplace - The Commoncog Blog": "https://commoncog.com/blog/rss/",
    "Confessions of a Data Guy": "https://www.confessionsofadataguy.com/feed/",
    "Conspiracy Theories": "https://feeds.megaphone.fm/END5064265457",
    "Crooked Timber": "https://crookedtimber.org/feed/",
    "CROW’s Substack": "https://crownewsletter.substack.com/feed",
    "Damn Interesting": "http://www.damninteresting.com/?feed=rss2",
    "Daring Fireball": "https://daringfireball.net/feeds/main",
    "Dear Prudence | Advice on relationships, sex, work, family, and life": "https://feeds.megaphone.fm/SM3958815784",
    "DepthHub: A jumping-off point for deeply-involved subreddits": "https://www.reddit.com/r/DepthHub/.rss",
    "Discourse Blog": "https://discourseblog.substack.com/feed/",
    "Discourse.net": "https://www.discourse.net/feed/",
    "Dissent Magazine": "https://www.dissentmagazine.org/feed",
    "Duck of Minerva": "https://duckofminerva.com/feed",
    "DudeFoods.com – Food Recipes & Videos": "http://dudefoods.com/feed/",
    "Election Law Blog": "https://electionlawblog.org/?feed=rss2",
    "emptywheel": "https://www.emptywheel.net/feed/",
    "Eschaton": "https://www.eschatonblog.com/feeds/posts/default",
    "Excess of Democracy": "https://excessofdemocracy.com/blog?format=rss",
    "FanGraphs Baseball": "https://blogs.fangraphs.com/feed/",
    "FanGraphs Fantasy Baseball": "http://feeds.feedburner.com/RotoGraphs",
    "Farm To Fountain": "https://farmtofountains.com/feed/",
    "Fast Food News – Fast Food Menu Prices": "https://www.fastfoodmenuprices.com/news/feed/",
    "Fitzdog Radio": "https://gregfitz.libsyn.com/rss",
    "Five Books": "https://fivebooks.com/feed/",
    "Food & Drink – The Pitch": "https://www.thepitchkc.com/category/food-drink/feed/",
    "Food : NPR": "https://feeds.npr.org/1053/rss.xml",
    "Freedom to Tinker": "https://freedom-to-tinker.com/feed/",
    "Futility Closet": "http://feeds.feedburner.com/FutilityCloset",
    "Gadgets | Latest gadget news, updates & reviews on TechCrunch": "https://techcrunch.com/gadgets/feed/",
    "Garbage Day": "https://rss.beehiiv.com/feeds/owMwaGYU36.xml",
    "Gin and Tacos": "http://www.ginandtacos.com/feed/",
    "Gizmodo": "https://gizmodo.com/rss",
    "GM Games – Sports General Manager Video Games": "https://gmgames.org/feed/",
    "GQ": "https://www.gq.com/feed/rss",
    "Groceries | Eat This, Not That!": "https://rss.app/feeds/JKtAQLtZCtIyjikJ.xml",
    "Gwern.net Newsletter": "https://gwern.substack.com/feed/",
    "Hacker News: Show HN": "https://hnrss.org/show",
    "Harpers Magazine": "http://harpers.org/feed/",
    "Hatewatch | Southern Poverty Law Center": "https://www.splcenter.org/hatewatch/rss.xml",
    "HolyPython.com": "https://holypython.com/feed/",
    "Hyperfocus and ADHD Articles | ADDitude": "https://www.additudemag.com/tag/hyperfocus/feed/",
    "Idle Words": "https://idlewords.com/index.xml",
    "Indexed": "http://thisisindexed.com/feed/",
    "Jacobin": "http://jacobinmag.com/feed/",
    "Junk Banter": "http://junkbanter.com/feed/",
    "Kansas City Royals – MLB Trade Rumors": "https://www.mlbtraderumors.com/kansas-city-royals/feed/atom",
    "kenpoms thoughts": "https://kenpom.substack.com/feed",
    "Kicks Condor": "https://www.kickscondor.com/feed.xml",
    "kottke.org": "http://feeds.kottke.org/main",
    "Lamebook - Funny Facebook Statuses, Fails, LOLs and More - The Original": "http://feeds.feedburner.com/Lamebook",
    "Laughing Squid": "http://laughingsquid.com/feed/",
    "Legal Profession Blog": "http://feeds.feedburner.com/LegalProfessionBlog",
    "librarian.net": "http://librarian.net/feed/",
    "LifeHacker": "https://lifehacker.com/feed/rss",
    "Literary  Hub": "https://lithub.com/feed/",
    "local ": "https://www.kcur.org/tags/local-food.rss",
    "Longreads": "https://longreads.com/feed/",
    "Lowering the Bar": "http://feeds.feedblitz.com/loweringthebar&x=1",
    "Luke Muehlhauser": "http://lukemuehlhauser.com/feed/",
    "Marginal REVOLUTION": "http://marginalrevolution.com/feed",
    "Matt Bruenig Dot Com": "https://mattbruenig.com/feed/",
    "Mental Floss": "https://www.mentalfloss.com/rss.xml",
    "MetaFilter": "https://rss.metafilter.com/metafilter.rss",
    "Misc Newsletters": "https://kill-the-newsletter.com/feeds/5mr68b7cb43ac2h04ai5.xml",
    "Mischiefs of Faction": "https://www.mischiefsoffaction.com/blog-feed.xml",
    "Miss Cellania": "https://misscellania.blogspot.com/feeds/posts/default",
    "My MeFi": "http://www.metafilter.com/mymefi/DE5A3ACAA6A85381/rss",
    "naked capitalism": "https://www.nakedcapitalism.com/feed",
    "Narratively": "https://narratively.com/feed/",
    "Neatorama": "http://www.neatorama.com/feed",
    "Ness Labs": "https://nesslabs.com/feed",
    "New York Magazine -- Intelligencer": "http://feeds.feedburner.com/nymag/intelligencer",
    "New Yorker": "http://www.newyorker.com/feed/everything",
    "News Archives | The Pitch": "https://www.thepitchkc.com/category/news-52777/feed/",
    "NYT > Paul Krugman": "https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/column/paul-krugman/rss.xml",
    "Obsidian Wings": "https://obsidianwings.blogs.com/obsidian_wings/atom.xml",
    "Open Culture": "https://www.openculture.com/feed",
    "Ordinary Times": "https://ordinary-times.com/feed/",
    "Outliner Software": "https://www.outlinersoftware.com/utils/rss",
    "Outside the Law School Scam": "http://outsidethelawschoolscam.blogspot.com/feeds/posts/default",
    "Pew Research Center » Fact Tank": "http://www.pewresearch.org/fact-tank/feed/",
    "Pinpoint Uncertainty": "http://pinpointuncertainty.blogspot.com/feeds/posts/default",
    "Pitch Weekly": "https://www.thepitchkc.com/feed/",
    "Pitcher List": "http://www.pitcherlist.com/feed/",
    "Pluralistic: Daily links from Cory Doctorow": "https://pluralistic.net/feed/",
    "Popular Information": "https://popular.info/feed",
    "Power 3.0 | Authoritarian Resurgence, Democratic Resilience": "https://www.power3point0.org/feed/podcast/",
    "Poynter": "https://www.poynter.org/feed/",
    "ProPublica": "http://feeds.propublica.org/propublica/main",
    "Public Notice": "https://www.publicnotice.co/feed",
    "PyMOTW on Doug Hellmann": "https://feeds.feedburner.com/PyMOTW",
    "Python Weekly Newsletter Archive Feed": "http://us2.campaign-archive1.com/feed?u=e2e180baf855ac797ef407fc7&id=9e26887fc5",
    "Quomodocumque": "https://quomodocumque.wordpress.com/feed/",
    "Rare Historical Photos": "https://feeds2.feedburner.com/rarehistoricalphotos",
    "Right Wing Watch": "https://www.rightwingwatch.org/feed/",
    "Roads & Kingdoms": "https://roadsandkingdoms.com/feed/",
    "RotoGraphs Fantasy Baseball": "https://fantasy.fangraphs.com/feed/",
    "Royals Farm Report": "https://royalsfarmreport.com/feed/",
    "Royals Review -  All Posts": "https://www.royalsreview.com/rss/index.xml",
    "Royals – FanGraphs Baseball": "https://www.fangraphs.com/blogs/category/teams/royals/feed/",
    "Salon.com > amanda_marcotte": "https://www.salon.com/writer/amanda_marcotte/feed",
    "Serious Eats": "http://feeds.feedburner.com/seriouseatsfeaturesvideos",
    "Skeptical Inquirer": "https://skepticalinquirer.org/feed/",
    "SportsLogos.Net News": "https://news.sportslogos.net/feed/",
    "SQL Shack – articles about database auditing, server performance, data recovery, and more": "https://www.sqlshack.com/feed/",
    "Standard Ebooks - New Releases": "https://standardebooks.org/rss/new-releases",
    "STAT": "https://www.statnews.com/feed/",
    "Steven A. Guccione": "https://stevesaltfacebook.blog/feed/",
    "Stories by Anmol Tomar on Medium": "https://anmol3015.medium.com/feed",
    "Stories by Zoumana Keita on Medium": "https://zoumanakeita.medium.com/feed",
    "Sumana": "https://brainwane.dreamwidth.org/data/rss",
    "Tales of Whoa": "http://brownforsheriff.tumblr.com/rss",
    "Tedium: The Dull Side of the Internet.": "https://feed.tedium.co/",
    "Texas Monthly": "https://www.texasmonthly.com//feed",
    "The Audacity of Despair": "https://davidsimon.com/feed/",
    "The Baffler": "https://thebaffler.com/feed",
    "The Belly of the Beast": "https://thelawyerbubble.com/feed/",
    "The Bulwark": "https://thebulwark.com/feed/",
    "The Corner | National Review": "https://www.nationalreview.com/corner/feed/",
    "The Cut": "http://feeds.feedburner.com/nymag/fashion",
    "the daily howler": "https://dailyhowler.blogspot.com/feeds/posts/default",
    "The Dispatch": "https://thedispatch.com/feed/",
    "The Dry Down": "https://thedrydown.substack.com/feed/",
    "The Electric Typewriter": "http://tetw.org/rss",
    "The Generalist Academy": "https://generalist.academy/feed/",
    "The Impulsive Buy": "https://www.theimpulsivebuy.com/wordpress/feed/",
    "The Intercept": "https://theintercept.com/feed/?_=1382",
    "The Junk Food Aisle": "https://www.thejunkfoodaisle.com/feed/",
    "The Kitchn | Inspiring cooks, nourishing homes": "http://feeds.feedburner.com/apartmenttherapy/thekitchn",
    "The Law School Tuition Bubble": "http://lawschooltuitionbubble.wordpress.com/feed/",
    "The Little Professor": "http://littleprofessor.typepad.com/the_little_professor/atom.xml",
    "The Markup": "https://themarkup.org/feeds/rss.xml",
    "The Moral High Ground": "https://evanhurst.substack.com/feed",
    "The New Inquiry": "http://thenewinquiry.com/feed/",
    "The New Republic": "https://newrepublic.com/rss.xml",
    "The Perry Bible Fellowship": "https://pbfcomics.com/feed/",
    "The Quietus": "https://thequietus.com/feed",
    "The Root": "https://www.theroot.com/rss",
    "The Smart Set": "https://www.thesmartset.com/feed/",
    "The Verge -  All Posts": "http://www.theverge.com/rss/index.xml",
    "Thomas Frank | The Guardian": "https://www.theguardian.com/profile/thomas-frank/rss",
    "Tom Pepinsky": "https://tompepinsky.com/feed/",
    "TPM – Talking Points Memo": "https://talkingpointsmemo.com/feed",
    "Tyler Cowens Ethnic Dining Guide": "https://tylercowensethnicdiningguide.com/index.php/feed/",
    'TYWKIWDBI      ("Tai-Wiki-Widbee")': "https://tywkiwdbi.blogspot.com/feeds/posts/default",
    "Vintage Everyday": "https://www.vintag.es/feeds/posts/default",
    "Voting Rights Lab": "https://votingrightslab.org/feed/",
    "Vulture": "http://feeds.feedburner.com/nymag/vulture",
    "Waxy.org": "https://waxy.org/feed/",
    "Web3 is Going Just Great": "https://web3isgoinggreat.com/feed.xml",
    "What To Read If": "https://whattoreadif.substack.com/feed",
    "Whats Good at Trader Joes": "http://www.whatsgoodattraderjoes.com/feeds/posts/default",
    "Whatever": "https://whatever.scalzi.com/feed/",
    "Wondermark": "http://feeds.feedburner.com/wondermark",
    "Wonkette": "http://wonkette.com/feed",
    "Work Stories, Humor, Memes, News | Pleated Jeans": "https://pleated-jeans.com/category/work/feed/",
    "xkcd.com": "http://xkcd.com/rss.xml",
    "You searched for antiwork - Ruin My Week": "https://ruinmyweek.com/search/antiwork/feed/rss2/",
    "Your Local Epidemiologist": "https://yourlocalepidemiologist.substack.com/feed",
    "Zompist’s E-Z rant page": "https://zompist.wordpress.com/feed/",
    "Current Affairs": "https://www.currentaffairs.org/news/rss.xml",
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

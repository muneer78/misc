import requests
import feedparser
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from tqdm import tqdm

rss_feeds = {
    '/dev/lawyer': 'https://writing.kemitchell.com/feed.xml',
    'A Collection of Unmitigated Pedantry': 'https://acoup.blog/feed/',
    'ADDitude: Hyperfocus and ADHD Articles': 'https://www.additudemag.com/tag/hyperfocus/feed/',
    'After School': 'https://afterschool.substack.com/feed',
    'Agile &amp; Coding': 'https://davidvujic.blogspot.com/feeds/posts/default?alt=rss',
    'Alexwlchan': 'https://alexwlchan.net/atom.xml',
    'Ali Barthwell Author Archive': 'https://politepol.com/fd/Z7RsuNu72Zc4.xml',
    'Ali Reza Hayati': 'https://alirezahayati.com/feed/',
    'Amadeus Maximilian’s Blog': 'https://amxmln.com/rss.xml',
    'Amelia Wattenberger': 'https://wattenberger.com/rss.xml',
    'The American Pamphleteer': 'https://ladylibertie.substack.com/feed',
    'Ana Rodrigues': 'https://ohhelloana.blog/feed.xml',
    'Andy Bell': 'https://bell.bz/feed.xml',
    'Antiwork - Ruin My Week': 'https://ruinmyweek.com/search/antiwork/feed/rss2/',
    'App Defaults': 'https://defaults.rknight.me/feed.xml',
    'The Aftermath': 'https://aftermath.site/feed',
    'The Appeal': 'https://theappeal.org/theappeal',
    'AppAddict': 'https://appaddict.app/feed.atom',
    'ArtButMakeItSports': 'https://www.artbutmakeitsports.com/feed',
    'arun.is': 'https://arun.is/rss.xml',
    'Attack of the 50 Foot Blockchain': 'https://davidgerard.co.uk/blockchain/feed/',
    'The Audacity of Despair': 'https://davidsimon.com/feed/',
    'Awesome Python Weekly': 'https://python.libhunt.com/newsletter/feed',
    'Awful Announcing': 'https://awfulannouncing.com/feed',
    'The Baffler': 'https://thebaffler.com/feed',
    'Balkinization': 'https://balkin.blogspot.com/feeds/posts/default',
    'Balls and Strikes': 'https://ballsandstrikes.org/feed/',
    'Bart de Goede': 'https://bart.degoe.de/index.xml',
    'Baseballmusings.com': 'http://feeds2.feedburner.com/Baseballmusingscom',
    'Baty.net': 'https://baty.net/index.xml',
    'The Beacon': 'https://thebeaconnews.org/feed/',
    'The Belly of the Beast': 'https://thelawyerbubble.com/feed/',
    'Bicycle For Your Mind': 'https://bicycleforyourmind.com/feed.rss',
    'Birchtree': 'https://birchtree.me/rss/',
    'bitches gotta eat!': 'https://bitchesgottaeat.substack.com/feed',
    'bitecode': 'https://www.bitecode.dev/feed',
    'Blackbird Spyplane': 'https://www.blackbirdspyplane.com/feed',
    'Blogofthe.Day': 'https://blogofthe.day/feed.xml',
    'Bookmarks – Chris Glass': 'https://chrisglass.com/links/feed/',
    'Brand Eating': 'https://www.brandeating.com/feeds/posts/default',
    'Brian Moylan Author Archive': 'https://politepol.com/fd/VoicyDwzX43M.xml',
    'bt RSS Feed': 'https://btxx.org/index.rss',
    'but shes a girl...': 'https://www.rousette.org.uk/index.xml',
    'Buzz Machine': 'https://buzzmachine.com/feed/',
    'CaptainAwkward.com': 'https://captainawkward.com/feed/',
    'The Cassandra Collective': 'https://cassandracollective.ghost.io/rss/',
    'Cerealously': 'http://www.cerealously.net/feed/',
    'Chefie Data Newsletter': 'https://nouman10.substack.com/feed',
    'Chop Wood, Carry Water': 'https://chopwoodcarrywaterdailyactions.substack.com/feed',
    'Civil Discourse with Joyce Vance': 'https://joycevance.substack.com/feed',
    'Chris Coyier': 'https://chriscoyier.net/feed/',
    'Chris Glass': 'https://chrisglass.com/feed/',
    'Chris Shaw': 'https://thoughts.uncountable.uk/feed',
    'Chriss Wiki :: blog': 'https://utcc.utoronto.ca/~cks/space/blog/?atom',
    'Club Sportico': 'https://club.sportico.com/feed',
    'Computers, internet, tech: Recently added blogs and sub-categories at ooh.directory': 'https://ooh.directory/feeds/cats/b7q2w7/rss/technology.xml',
    'ContraBandCamp': 'https://www.contrabandcamp.com/feed',
    'Cool As Heck': 'https://cool-as-heck.blog/feed/',
    'Cory Dransfeldt': 'https://www.coryd.dev/feeds/links.xml',
    'Counting Stuff': 'https://www.counting-stuff.com/rss/',
    'CREW': 'https://www.citizensforethics.org/feed',
    'CROW’s Substack': 'https://crownewsletter.substack.com/feed',
    'Current Affairs': 'https://www.currentaffairs.org/news/rss.xml',
    'Current Events': 'https://kill-the-newsletter.com/feeds/jnggh1214ov2zpew9383.xml',
    'Damn Interesting': 'http://www.damninteresting.com/?feed=rss2',
    'Dan Sinkers Blog': 'https://dansinker.com/feed.xml',
    'Danny Funt+': 'https://dannyfunt.substack.com/feed',
    'Daring Fireball': 'https://daringfireball.net/feeds/main',
    'daverupert.com': 'https://daverupert.com/atom.xml',
    'default.blog': 'https://www.counting-stuff.com/rss/',
    'Democracy Docket': 'https://www.democracydocket.com/feed/',
    'Democracy Forward': 'https://democracyforward.org/feed',
    'DepthHub': 'https://www.reddit.com/r/DepthHub/.rss',
    'Discourse Blog': 'https://www.discourseblog.com/feed',
    'Django Andy': 'https://djangoandy.com/feed/',
    'Doc Searls': 'https://doc.searls.com/feed/',
    'Documented': 'https://documentedny.com/feed',
    'The Dry Down': 'https://thedrydown.substack.com/feed/',
    'Eater -  Kansas City': 'https://www.eater.com/rss/kansas-city/index.xml',
    'Ed Zitrons Wheres Your Ed At': 'https://www.wheresyoured.at/feed',
    'Election Law Blog': 'https://electionlawblog.org/?feed=rss2',
    'Electoral Reform – The Nation': 'https://www.thenation.com/feed/?post_type=article&subject=electoral-reform',
    'Ellane W': 'https://ellanew.com/feed.rss',
    'Email is good.': 'https://email-is-good.com/feed/',
    'Emily in Your Phone': 'https://emilyinyourphone.substack.com/feed',
    'Esquire - News and Politics': 'https://www.esquire.com/rss/news-politics.xml/',
    'FanGraphs Baseball': 'https://blogs.fangraphs.com/feed/',
    'Farm to Fountains': 'https://farmtofountains.com/feed/',
    'Fast Food News': 'https://www.fastfoodmenuprices.com/news/feed/',
    'FedScoop': 'https://fedscoop.com/feed/',
    'Five Books': 'https://fivebooks.com/feed/',
    'Fix The News': 'https://fixthenews.com/rss/',
    'Flatland KC': 'https://flatlandkc.org/feed/',
    'Flow State': 'https://www.flowstate.fm/feed',
    'The Flytrap': 'https://rss.beehiiv.com/feeds/OmyX5EL51W.xml',
    'Foodbeast Products': 'https://www.foodbeast.com/./products/feed/',
    'FoxTrot Comics by Bill Amend': 'https://foxtrot.com/feed/',
    'Freddie deBoer': 'https://freddiedeboer.substack.com/feed',
    'Futility Closet': 'http://feeds.feedburner.com/FutilityCloset',
    'Garbage Day': 'https://rss.beehiiv.com/feeds/owMwaGYU36.xml',
    'The Generalist Academy': 'https://generalist.academy/feed/',
    'Gin and Tacos': 'http://www.ginandtacos.com/feed/',
    'GM Games – Sports General Manager Video Games': 'https://gmgames.org/feed/',
    'Groceries | Eat This, Not That!': 'https://rss.app/feeds/JKtAQLtZCtIyjikJ.xml',
    'Gwern.net Newsletter': 'https://gwern.substack.com/feed/',
    'Hackaday': 'https://hackaday.com/feed/',
    'Hacker News: Show HN': 'https://hnrss.org/show',
    'The Handbasket': 'https://rss.beehiiv.com/feeds/40ZQ7CSldT.xml',
    'Harpers Magazine': 'https://harpers.org/feed/',
    'Hatewatch | Southern Poverty Law Center': 'https://www.splcenter.org/resources/hate-watch/feed/',
    'Heather Bryant — @HBCompass': 'https://www.hbcompass.io/rss/',
    'Hell Gate': 'https://hellgatenyc.com/all-posts/rss/',
    'Hopium Chronicles By Simon Rosenberg': 'https://www.hopiumchronicles.com/feed',
    'hjr265.me': 'https://hjr265.me/blog/index.xml',
    'How Things Work': 'https://www.hamiltonnolan.com/feed',
    'i.webthings.hub': 'https://iwebthings.joejenett.com/feed.atom',
    'Indexed': 'http://thisisindexed.com/feed/',
    'Ineza Bonté': 'https://www.ineza.codes/rss.xml',
    'Infinite Wishes 🏳️‍⚧️🚀': 'https://emmas.site/blog/atom.xml',
    'Interconnected': 'https://interconnected.org/home/feed',
    'International Consortium of Investigative Journalists': 'https://www.icij.org/feed',
    'Into The Fountains': 'https://intothefountains.substack.com/feed',
    'Jack H. Peterson': 'https://jackhpeterson.com/atom.xml',
    'Joes Weather Blog': 'https://fox4kc.com/weather/weather-blog/feed/',
    'Julia Evans': 'https://jvns.ca/atom.xml',
    'Junk Banter': 'http://junkbanter.com/feed/',
    'The Junk Food Aisle': 'https://www.thejunkfoodaisle.com/feed/',
    'jwz': 'https://cdn.jwz.org/blog/feed/',
    'Kansas City Royals – MLB Trade Rumors': 'https://www.mlbtraderumors.com/kansas-city-royals/feed/atom',
    'Kansas Reflector': 'https://kansasreflector.com/feed/',
    'Katherine Yang': 'https://kayserifserif.place/feed.xml',
    'KCUR- Local Food ': 'https://www.kcur.org/tags/local-food.rss',
    'kenpoms thoughts': 'https://kenpom.substack.com/feed/',
    'Kev Quirk': 'https://kevquirk.com/feed',
    'Kicks Condor': 'https://www.kickscondor.com/feed.xml',
    'kottke.org': 'http://feeds.kottke.org/main',
    'krrd.ing': 'https://krrd.ing/rss.xml',
    'Lambda Legal': 'https://lambdalegal.org/feed/',
    'Lamebook - Funny Facebook Statuses, Fails, LOLs and More - The Original': 'http://feeds.feedburner.com/Lamebook',
    'Laughing Squid': 'http://laughingsquid.com/feed/',
    'Law Dork': 'https://www.lawdork.com/feed',
    'Laura Olin': 'https://buttondown.com/lauraolin/rss',
    'Lazybear': 'https://lazybea.rs/index.xml',
    'Legal Profession Blog': 'http://feeds.feedburner.com/LegalProfessionBlog',
    'Letters from an American': 'https://heathercoxrichardson.substack.com/feed',
    'Linkblog': 'https://www.splitbrain.org/feed/links',
    'LinkMachineGo': 'https://www.timemachinego.com/linkmachinego/feed/',
    'Links I Would Gchat You If We Were Friends': 'https://linksiwouldgchatyou.substack.com/feed',
    'Live Laugh Blog': 'https://livelaugh.blog/rss.xml',
    'LOL (lots of links)': 'https://lotsoflinks.substack.com/feed',
    'Longreads': 'https://longreads.com/feed/',
    'LostFocus': 'https://lostfocus.de/feed/',
    'Lowering the Bar': 'http://feeds.feedblitz.com/loweringthebar&x=1',
    'Lucian Truscott Newsletter': 'https://luciantruscott.substack.com/feed',
    'Luke Muehlhauser': 'http://lukemuehlhauser.com/feed/',
    'Maggie Appleton': 'https://maggieappleton.com/rss.xml',
    'MANU': 'https://manuelmoreale.com/feed/rss',
    'Marginal REVOLUTION': 'http://marginalrevolution.com/feed',
    'mathspp.com feed': 'https://mathspp.com/blog.atom',
    'Matt Bruenig Dot Com': 'https://mattbruenig.com/feed/',
    'mattrighetti': 'https://mattrighetti.com/feed.xml',
    'maya.land': 'https://maya.land/feed.xml',
    'McFilter': 'http://www.mcqn.net/mcfilter/index.xml',
    'Media Matters for America': 'https://politepol.com/fd/TZerYpPaBA2M',
    'Meditations In An Emergency': 'https://www.meditationsinanemergency.com/rss/',
    'Mental Floss': 'https://www.mentalfloss.com/rss.xml',
    'Michael Burkhardts Whirled Wide Web': 'https://mihobu.lol/rss.xml',
    'Michael Sippey': 'https://sippey.com/rss.xml',
    'Michael Tsai': 'https://mjtsai.com/blog/feed/',
    'Mining The News': 'https://siftrss.com/f/13aRaX8yGr5',
    'Misc Newsletters': 'https://kill-the-newsletter.com/feeds/5mr68b7cb43ac2h04ai5.xml',
    'Miss Cellania': 'https://misscellania.blogspot.com/feeds/posts/default?alt=rss',
    'Molly Whites activity feed': 'https://www.mollywhite.net/feed/feed.xml',
    'The Moral High Ground': 'https://evanhurst.substack.com/feed',
    'Mouse vs. Python': 'https://www.blog.pythonlibrary.org/feed/',
    'Nabeel Valley': 'https://nabeelvalley.co.za/feed/rss.xml',
    'Narratively': 'https://narratively.com/feed/',
    'Neatorama': 'http://www.neatorama.com/feed',
    'Ned Batchelder': 'http://nedbatchelder.com/blog/rss.xml',
    'Neil’s Substack': 'https://neilpaine.substack.com/feed',
    'Neurodivergent Insights': 'https://neurodivergentinsights.com/blog?format=rss',
    'Nicola Iarocci': 'https://nicolaiarocci.com/index.xml',
    'Nieman Lab': 'https://www.niemanlab.org/feed/',
    'Not Always Legal': 'https://notalwaysright.com/legal/feed/',
    'Not Always Right- Inspirational': 'https://notalwaysright.com/tag/inspirational/feed/',
    'Notes by JCProbably': 'https://notes.jeddacp.com/feed/',        
    'NPR: Food': 'https://feeds.npr.org/1053/rss.xml',
    'One First': 'https://www.stevevladeck.com/feed',
    'One Foot Tsunami': 'https://onefoottsunami.com/feed/atom/',
    'One Point Zero': 'https://onepointzero.com/feed/basic',
    'ongoing by Tim Bray': 'http://www.tbray.org/ongoing/ongoing.atom',
    'Open Culture': 'https://www.openculture.com/feed',
    'Ordinary Times': 'https://ordinary-times.com/feed/',
    'Own Your Web': 'https://buttondown.email/ownyourweb/rss',
    'Patrick Van der Spiegels Posts': 'https://patrick.vanderspie.gl/posts/index.xml',
    'Paul Gross': 'https://www.pgrs.net/feed.xml',
    'Paul Krugman': 'https://paulkrugman.substack.com/feed',
    'Perl Hacks': 'https://perlhacks.com/feed/',
    'Pitch Weekly': 'https://www.thepitchkc.com/feed/',
    'Pitch Weekly: Food & Drink': 'https://www.thepitchkc.com/category/food-drink/feed/',
    'Pixel Envy': 'https://feedpress.me/pxlnv',
    'Planet Python': 'https://planetpython.org/rss20.xml',
    'plover': 'https://blog.plover.com/index.rss',
    'Pluralistic: Daily links from Cory Doctorow': 'https://pluralistic.net/feed/',
    'Popular Information': 'https://popular.info/feed',
    'Power 3.0 | Authoritarian Resurgence, Democratic Resilience': 'https://www.power3point0.org/feed/podcast/',
    'Poynter': 'https://www.poynter.org/feed/',
    'Prism Politics and Democracy': 'https://prismreports.org/category/politics-democracy/feed/',
    'Process Things - Code': 'https://exch.gr/code/feed.xml',
    'Process Things - Essays': 'https://exch.gr/essays/feed.xml',
    'ProHoopsHistory Newsletter': 'https://prohoopshistory.substack.com/feed',
    'ProPublica': 'http://feeds.propublica.org/propublica/main',
    'Prospect361': 'https://prospect361.com/feed',
    'Public Citizen': 'https://www.citizen.org/feed/',
    'Public Notice': 'https://www.publicnotice.co/feed',
    'Puck': 'https://puck.news/feed',
    'Pudding.cool': 'https://pudding.cool/feed.xml',
    'PyBites': 'https://pybit.es/feed/',
    'PyCoders Weekly': 'https://pycoders.com/feed/T8SjZAIK',
    'PyMOTW on Doug Hellmann': 'https://feeds.feedburner.com/PyMOTW',
    'Python In Office': 'https://pythoninoffice.com/feed/',
    'Python Insider': 'https://blog.python.org/feeds/posts/default',
    'Python Morsels': 'https://www.pythonmorsels.com/topics/feed/',
    'Python Weekly': 'http://us2.campaign-archive1.com/feed?u=e2e180baf855ac797ef407fc7&id=9e26887fc5',
    'Qubyte Codes': 'https://qubyte.codes/social.atom.xml',
    'Quotaliciousness': 'https://quotulatiousness.ca/blog/feed/',
    'Read Rodge': 'https://rodgersherman.substack.com/feed',
    'read-only': 'https://read-only.net/feed.xml',
    'Recomendo': 'https://www.recomendo.com/feed',
    'ReedyBears Blog': 'https://reedybear.bearblog.dev/feed/',
    'Rest of World - Digital utopia': 'https://restofworld.org/feed/collection/digital-utopia',
    'Rest of World - The future of work': 'https://restofworld.org/feed/collection/future-of-work',
    'Right Wing Watch': 'https://www.rightwingwatch.org/feed/',
    'Roads & Kingdoms': 'https://roadsandkingdoms.com/feed/',
    'Robin Rendle': 'https://buttondown.com/robinrendle/rss',
    'Robin Sloan': 'https://www.robinsloan.com/feed.xml',
    'Rosemary Orchard |': 'https://rosemaryorchard.com/feed.xml',
    'RotoGraphs Fantasy Baseball': 'https://fantasy.fangraphs.com/feed/',
    'Royals Farm Report': 'https://royalsfarmreport.com/feed/',
    'Royals Review -  All Posts': 'https://www.royalsreview.com/rss/index.xml',
    'Royals – FanGraphs Baseball': 'https://www.fangraphs.com/blogs/category/teams/royals/feed/',
    'Rubenerd': 'http://showfeed.rubenerd.com/',
    'Salon.com > amanda_marcotte': 'https://www.salon.com/writer/amanda_marcotte/feed',
    'Sandwich Tribunal': 'https://www.sandwichtribunal.com/feed/',
    'Scriveners Error': 'https://scrivenerserror.blogspot.com/feeds/posts/default?alt=rss',
    'Sergis writing': 'https://sergiswriting.com/atom.xml',
    'Shellsharks Feeds': 'https://shellsharks.com/feeds/feed.xml',
    'Shellsharks Links': 'https://shellsharks.com/feeds/link-feed.xml',
    'Sludge': 'https://readsludge.com/feed/',
    'small good things': 'https://eilloh.net/posts_feed',
    'The Smart Set': 'https://www.thesmartset.com/feed/',
    'snarfed.org': 'https://snarfed.org/feed',
    'Some Bits: Nelsons Linkblog': 'https://www.somebits.com/linkblog/index.atom',
    'someecards': 'https://www.someecards.com/rss/homepage.xml',
    'splitbrain.org - blog': 'https://www.splitbrain.org/feed/blog',
    'SportsLogos.Net News': 'https://news.sportslogos.net/feed/',
    'SQL Shack – articles about database auditing, server performance, data recovery, and more': 'https://www.sqlshack.com/feed/',
    'Standard Ebooks - New Releases': 'https://standardebooks.org/rss/new-releases',
    'STAT': 'https://www.statnews.com/feed/',
    'The Status Kuo': 'https://statuskuo.substack.com/feed',
    'Steven A. Guccione': 'https://stevesaltfacebook.blog/feed/',
    'The Sunday Long Read': 'https://us9.campaign-archive.com/feed?id=67e6e8a504&u=6e1ae4ac632498a38c1d57c54',
    'Supreme Court – The Nation': 'https://www.thenation.com/feed/?post_type=article&subject=supreme-court',
    'Tales of Whoa': 'http://brownforsheriff.tumblr.com/rss',
    'Talking Points Memo': 'https://talkingpointsmemo.com/feed',
    'Tastefully Offensive': 'https://www.tastefullyoffensive.com/feed/',
    'Tech': 'https://kill-the-newsletter.com/feeds/527km9xxoq0vonzops4m.xml',
    'Tedium: The Dull Side of the Internet.': 'https://feed.tedium.co/',
    'Teen Vogue': 'https://politepol.com/fd/Vjc601sG0jpO.xml',
    'Terence Eden’s Blog': 'https://shkspr.mobi/blog/feed/atom/',
    'Texas Monthly': 'https://www.texasmonthly.com//feed',
    'Texts From Last Night': 'http://feeds.feedburner.com/tfln',
    'The Beautiful Mess': 'https://cutlefish.substack.com/feed',
    'The Bored Horse': 'https://bored.horse/feed.xml',
    'The Bulwark': 'https://thebulwark.com/feed/',
    'The Candybox Blog': 'http://www.nathalielawhead.com/candybox/feed',
    'The Dispatch': 'https://thedispatch.com/feed/',
    'The Electric Typewriter': 'https://electrictype.substack.com/feed',
    'The Generalist Academy': 'https://generalist.academy/feed/',
    'The Impulsive Buy': 'https://www.theimpulsivebuy.com/wordpress/feed/',
    'The Intercept': 'https://theintercept.com/feed/?_=1382',
    'The Junk Food Aisle': 'https://www.thejunkfoodaisle.com/feed/',
    'The Markup': 'https://themarkup.org/feeds/rss.xml',
    'The Perry Bible Fellowship': 'https://pbfcomics.com/feed/',
    'The Pitch': 'https://www.thepitchkc.com/category/news-52777/feed/',
    'The Python Papers': 'https://www.pythonpapers.com/feed',
    'The Python Rabbithole': 'https://zlliu.substack.com/feed',
    'The Racket News': 'https://www.theracketnews.com/feed',
    'The Root': 'https://www.theroot.com/rss',
    'The Sword And the Sandwich': 'https://buttondown.com/theswordandthesandwich/rss',
    'The Tao of Mac': 'https://taoofmac.com/atom.xml',
    'Thinking about...': 'https://snyder.substack.com/feed',
    'Tomorrows Baseball Today': 'https://tbtmlb.substack.com/feed',
    'Trades Ten Years Later': 'https://tradestenyearslater.substack.com/feed',
    'Trout Nation': 'http://jennytrout.com/?feed=rss2',
    'Troy Vassalotti :: Blog': 'https://www.troyv.dev/feed.xml',
    'Twitter @Rany Jazayerli': 'https://rsshub.app/twitter/user/jazayerli/exclude_rts_replies=1&forceWebApi=1',
    'TYWKIWDBI ("Tai-Wiki-Widbee")': 'https://tywkiwdbi.blogspot.com/feeds/posts/default',
    'UnHerd': 'https://unherd.com/feed/',
    'URL Media' : 'https://url-media.com/feed/',
    'User Mag': 'https://www.usermag.co/feed',
    'Vaporwave Van Gogh': 'https://vaporwave-van-gogh.tumblr.com/rss',
    'Veronica Writes': 'https://berglyd.net/feed.xml',
    'VZQK50': 'https://www.vzqk50.com/blog/scraps//../../index.xml',
    'WebCurios': 'https://webcurios.co.uk/feed/',
    'Welcome To Hell World': 'https://www.welcometohellworld.com/rss/',
    'Werd I/O': 'https://granary.io/url?url=https://werd.io/content/all/&input=html&output=atom&hub=https://bridgy-fed.superfeedr.com/',
    'what are the haps': 'https://ryannorth.tumblr.com/rss',
    'Whatever': 'https://whatever.scalzi.com/feed/',
    'Whats Good at Trader Joes': 'http://www.whatsgoodattraderjoes.com/feeds/posts/default',
    'Why Evolution Is True': 'https://whyevolutionistrue.com/feed/',
    'Wired':"https://www.wired.com/feed/rss",
    'Wonkette': 'http://wonkette.com/feed',
    'Work Stories, Humor, Memes, News | Pleated Jeans': 'https://pleated-jeans.com/category/work/feed/',
    'Wrong Hands': 'https://wronghands1.com/feed/',
    'x-log': 'https://blog.x-way.org/atom.xml',
    'xkcd.com': 'http://xkcd.com/rss.xml',
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
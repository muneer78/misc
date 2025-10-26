from xml.etree.ElementTree import Element, SubElement, ElementTree
from pathlib import Path

# Input dictionary
rss_feeds = {
    "Common Dreams": "https://www.commondreams.org/feeds/feed.rss",
    "": "https://marginalrevolution.com/feed",
    "Daring Fireball": "https://daringfireball.net/feeds/main",
    "Crooked Timber": "https://crookedtimber.org/feed/",
    "Eater": "https://www.eater.com/rss/front-page/index.xml",
    "Election Law Blog": "https://electionlawblog.org/?feed=rss2",
    "fark": "https://www.fark.com/fark.rss",
    "Garbage Day": "https://rss.beehiiv.com/feeds/owMwaGYU36.xml",
    "Gizmodo": "https://gizmodo.com/rss",
    "Hatewatch": "https://www.splcenter.org/hatewatch/rss.xml",
    "Laughing Squid": "http://laughingsquid.com/feed/",
    "Mental Floss": "https://www.mentalfloss.com/rss.xml",
    "Neatorama": "http://www.neatorama.com/feed",
    "New Yorker": "http://www.newyorker.com/feed/everything",
    "Pitch Weekly": "https://www.thepitchkc.com/category/news-52777/feed/",
    "Exposed by CMD": "https://www.exposedbycmd.org/feed/",
    "The Markup": "https://themarkup.org/feeds/rss.xml",
    "The New Republic": "https://newrepublic.com/rss.xml",
    "The Root": "https://www.theroot.com/rss",
    "Whatever": "https://whatever.scalzi.com/feed/",
    "Wonkette": "http://wonkette.com/feed",
}

# Output file path
output_opml = Path("/Users/muneer78/Downloads/rss_feeds.opml")

# Create the root OPML structure
opml = Element("opml", version="2.0")
head = SubElement(opml, "head")
title = SubElement(head, "title")
title.text = "RSS Feeds"

body = SubElement(opml, "body")

# Add each RSS feed to the OPML file
for name, url in rss_feeds.items():
    outline = SubElement(body, "outline", type="rss", text=name, title=name, xmlUrl=url)

# Write the OPML file
tree = ElementTree(opml)
tree.write(output_opml, encoding="utf-8", xml_declaration=True)

print(f"OPML file saved to: {output_opml}")

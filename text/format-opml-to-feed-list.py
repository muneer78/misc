import xml.etree.ElementTree as ET

# Load and parse the OPML file
tree = ET.parse("/Users/muneer78/Downloads/feeds.opml")
root = tree.getroot()

# Open a new file to write the formatted feeds
with open("/Users/muneer78/Downloads/formatted_feeds.txt", "w") as f:
    for outline in root.findall(".//outline"):
        title = outline.get("title")
        xmlUrl = outline.get("xmlUrl")
        if title and xmlUrl:
            f.write(f"'{title}': '{xmlUrl}',\n")

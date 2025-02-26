import xml.etree.ElementTree as ET

# Define the input and output file paths
input_file = "/Users/muneer78/Downloads/NewsBlur-stedman15-2025-02-26.opml"
output_file = "/Users/muneer78/Downloads/rss_feeds_newsblur.txt"

# Read the OPML file and fix the encoding issue
with open(input_file, 'r', encoding='utf-8') as file:
    content = file.read().replace('encoding="utf8"', 'encoding="UTF-8"')

# Parse the fixed content
root = ET.fromstring(content)

# Collect the RSS feeds in a list
rss_feeds = []
for outline in root.findall(".//outline[@type='rss']"):
    name = outline.get('title')
    url = outline.get('xmlUrl')
    rss_feeds.append((name, url))

# Sort the RSS feeds alphabetically by name
rss_feeds.sort()

# Open the output file for writing
with open(output_file, 'w') as file:
    file.write("rss_feeds = {\n")
    for name, url in rss_feeds:
        file.write(f"    '{name}': '{url}',\n")
    file.write("}\n")

print(f"RSS feeds have been extracted and written to {output_file}")
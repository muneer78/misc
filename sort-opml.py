import xml.etree.ElementTree as ET

# Load and parse the OPML file
tree = ET.parse("fraidy_sorted.opml")
root = tree.getroot()

# Find all outline elements
outlines = root.findall(".//outline")

# Sort outlines by 'category' and then by 'text', both case-insensitive
outlines_sorted = sorted(outlines, key=lambda x: (x.get("text", "").lower()))

# Remove existing outline elements
for parent in root.findall(
    ".//outline/.."
):  # Getting the parent of each outline element
    for child in parent.findall("outline"):
        parent.remove(child)

# Re-add the sorted outline elements
for outline in outlines_sorted:
    parent.append(outline)

# Write the sorted OPML back to file
tree.write("fraidy.opml")

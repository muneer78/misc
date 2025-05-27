from xml.etree import ElementTree as ET
from pathlib import Path

# File paths
input_opml = Path("/Users/muneer78/Downloads/fraidycat.opml")  # Input OPML file
output_opml = Path("/Users/muneer78/Downloads/fraidycat_modified.opml")  # Output OPML file

# Parse the OPML file
tree = ET.parse(input_opml)
root = tree.getroot()

# Process each <outline> element
for outline in root.findall(".//outline"):
    # Ensure the element has the required attributes
    if "text" in outline.attrib:
        outline.set("title", outline.attrib["text"])
    if "xmlUrl" in outline.attrib and "text" in outline.attrib:
        # Remove all other attributes except "type", "xmlUrl", "text", and "title"
        allowed_attributes = {"type", "xmlUrl", "text", "title"}
        for attr in list(outline.attrib.keys()):
            if attr not in allowed_attributes:
                del outline.attrib[attr]
    
    # Add "type=rss" if not already present
    if "type" not in outline.attrib:
        outline.set("type", "rss")

# Write the modified OPML to a new file
tree.write(output_opml, encoding="utf-8", xml_declaration=True)

print(f"Modified OPML file saved to: {output_opml}")
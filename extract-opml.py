import csv
import xml.etree.ElementTree as ET
import html


# Function to extract and clean text from the outline elements
def extract_and_clean_text(element):
    text_value = element.get("text")
    if text_value:
        # Replace HTML entities with respective characters
        clean_text = html.unescape(text_value)
        return clean_text
    return None


# Parse the OPML file
input_file = "PocketCasts.opml"  # Replace with your actual file path
tree = ET.parse(input_file)
root = tree.getroot()

# Initialize a list to store the cleaned text values
output_data = []

# Iterate over all outline elements in the OPML file
for outline in root.iter("outline"):
    clean_text = extract_and_clean_text(outline)
    if clean_text:
        output_data.append([clean_text])

# Write the output to a CSV file
output_file = "podcasts.csv"  # Replace with your desired output file path
with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Extracted Text"])  # Header
    writer.writerows(output_data)

print("Extraction and replacement completed. Output saved to 'output.csv'")

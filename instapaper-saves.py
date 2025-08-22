import re
import pandas as pd

# Specify the path to your HTML file
html_file_path = "instapaper-export.html"

# Read the HTML content from the file
with open(html_file_path, "r", encoding="utf-8") as file:
    html_content = file.read()

# Define regular expression patterns
url_pattern = r'<a href="([^"]+)">([^<]+)<\/a>'

# Find matches for URLs and titles
url_matches = re.findall(url_pattern, html_content)

# Create a list of dictionaries with the extracted data
data = [
    {
        "URL": match[0],
        "Title": match[1],
        "Website Title": match[0].split("//")[1].split("/")[0],
    }
    for match in url_matches
]

# Create a Pandas DataFrame
df = pd.DataFrame(data)

# Remove "www" and ".com" if they exist in the "Website Title" column
df["Website Title"] = (
    df["Website Title"].str.replace("www.", "").str.replace(".com", "")
)

# Send the DataFrame to csv
df.to_csv("instapaper_urls.csv")

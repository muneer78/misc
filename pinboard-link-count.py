from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd
from collections import Counter
from pathlib import Path
from tqdm import tqdm  # Import tqdm for the progress bar

# File path
input_html = Path("/Users/muneer78/data/pinboard-export.2021.03.28-14.40.html")  # Replace with your HTML file path

# Read the HTML file
with open(input_html, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Extract all links
links = [a["href"] for a in soup.find_all("a", href=True)]

# Extract domains from links with a progress bar
domains = []
for link in tqdm(links, desc="Extracting domains"):
    domains.append(urlparse(link).netloc)

# Count occurrences of each domain
domain_counts = Counter(domains)

# Create a DataFrame
df = pd.DataFrame(domain_counts.items(), columns=["domain", "count"])

# Sort the DataFrame by count in descending order
df = df.sort_values(by="count", ascending=False).reset_index(drop=True)

# Output the DataFrame
print(df)

# Save the DataFrame to a CSV file (optional)
output_csv = Path("/Users/muneer78/Downloads/domains_count.csv")  # Replace with your desired output path
df.to_csv(output_csv, index=False)
print(f"Domain counts saved to: {output_csv}")
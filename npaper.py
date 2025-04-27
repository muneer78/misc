from bs4 import BeautifulSoup
from urllib.request import urlopen  # Use urllib for fetching URLs
from pathlib import Path

# Input and output file paths
input_file = Path("/Users/muneer78/Downloads/sarah-haider.txt")  # Input file containing URLs
output_file = Path("/Users/muneer78/Downloads/haider-book.txt")  # Output file for extracted content

# Check if the input file exists
if not input_file.exists():
    print(f"Input file '{input_file}' does not exist.")
    exit(1)

# Read URLs from the input file
with input_file.open("r", encoding="utf-8") as file:
    urls = [line.strip() for line in file if line.strip()]  # Remove empty lines

# Open the output file for writing
with output_file.open("w", encoding="utf-8") as file:
    for url in urls:
        try:
            # Fetch the HTML content of the URL
            response = urlopen(url)
            html_content = response.read()

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, "html.parser")

            # Extract all paragraphs
            paragraphs = soup.find_all("p")
            if paragraphs:
                file.write(f"URL: {url}\n")
                for p in paragraphs:
                    file.write(p.get_text(strip=True) + "\n")
                file.write("\n---\n")  # Separator between articles
                print(f"Successfully processed: {url}")
            else:
                print(f"No paragraphs found in: {url}")
        except Exception as e:
            print(f"Error processing {url}: {e}")
print(f"Content extracted and saved to '{output_file}'.")
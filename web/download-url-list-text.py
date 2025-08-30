from bs4 import BeautifulSoup
import requests
from pathlib import Path

# Input and output file paths
input_file = Path(
    "/Users/muneer78/Downloads/sarah-haider.txt"
)  # Input file containing URLs
output_file = Path(
    "/Users/muneer78/Downloads/haider.txt"
)  # Output file for extracted content

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
            # Fetch the HTML content of the URL using requests
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract the title of the page
            title = soup.title.string.strip() if soup.title else "No Title"

            # Extract the main body text (all paragraphs)
            paragraphs = soup.find_all("p")
            body_text = "\n".join(
                p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
            )

            # Write the title and body text to the output file
            file.write(f"Title: {title}\n")
            file.write(body_text)
            file.write("\n---\n")  # Separator between sections
            print(f"Successfully processed: {url}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")
        except Exception as e:
            print(f"Error processing {url}: {e}")

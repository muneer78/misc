import requests
from bs4 import BeautifulSoup
import csv
import time

base_url = "https://grantland.com/features/"
all_urls = set()  # To store unique URLs and avoid duplicates

# Open CSV file to write
with open("grantland_features_urls.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["URL"])  # Header row

    current_url = base_url
    while current_url:
        response = requests.get(current_url)

        # Check if the request was successful
        if response.status_code != 200:
            print(
                f"Failed to retrieve {current_url} with status code: {response.status_code}"
            )
            break

        # Parse the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract and save feature article links
        for link in soup.find_all("a", href=True):
            url = link["href"]
            if (
                url.startswith(base_url) and url not in all_urls
            ):  # Only add unique links within 'features'
                all_urls.add(url)
                writer.writerow([url])

        # Find the "next" page link
        next_link = soup.find(
            "a", text="Next"
        )  # Adjust selector based on site design if needed
        if next_link:
            current_url = next_link["href"]
            time.sleep(1)  # Pause to avoid overwhelming the server
        else:
            current_url = None  # End the loop if no more pages

print("Scraping completed. All URLs are saved in grantland_features_urls.csv")

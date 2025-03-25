import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Folder to save images
download_folder = os.path.expanduser("~/Downloads/chuck_lorre_images")
if not os.path.exists(download_folder):
    os.makedirs(download_folder)

# Base URL
base_url = "https://www.chucklorre.com/?e="

# Loop through pages e=1 to e=1517
for page_num in range(1, 1518):
    print(f"Scraping page {page_num}...")

    # Construct URL for each page
    page_url = base_url + str(page_num)

    # Send request to the page
    response = requests.get(page_url)
    if response.status_code != 200:
        print(f"Failed to retrieve page {page_num}")
        continue

    # Parse the page content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all image tags
    img_tags = soup.find_all('img')

    # Download each image
    for img in img_tags:
        img_url = img.get('src')
        if not img_url:
            continue  # Skip if no image source

        # Make sure we have a complete URL for the image
        img_url = urljoin(page_url, img_url)

        # Extract image filename from the URL
        img_name = os.path.basename(img_url)

        # Create the full path to save the image
        img_path = os.path.join(download_folder, img_name)

        # Download and save the image
        try:
            img_data = requests.get(img_url).content
            with open(img_path, 'wb') as f:
                f.write(img_data)
            print(f"Downloaded: {img_name}")
        except Exception as e:
            print(f"Failed to download {img_name}: {e}")

print("Finished scraping all pages.")

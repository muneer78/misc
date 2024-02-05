import requests
from bs4 import BeautifulSoup
import pandas as pd

def extract_urls_from_page(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = [a['href'] for a in soup.find_all('a', href=True)]
        return urls
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def main():
    # Replace 'your_url_here' with the actual URL you want to extract URLs from
    base_url = 'https://web.archive.org/web/*/http://clubtrillion.blogspot.com*'

    urls = extract_urls_from_page(base_url)

    if not urls:
        print("No URLs found.")
        return

    # Create a DataFrame with the extracted URLs
    df = pd.DataFrame({'URLs': urls})

    # Save DataFrame to a CSV file
    df.to_csv('clubtrillion.csv', index=False)

    print("URLs extracted successfully.")

if __name__ == "__main__":
    main()

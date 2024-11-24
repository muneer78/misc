import requests
from bs4 import BeautifulSoup
import pdfkit

# Configure pdfkit
pdfkit_config = pdfkit.configuration(wkhtmltopdf='/Users/muneer78/project/.venv/lib/python3.11/site-packages/pdfkit')  # Update path for your system

# Medium Reading List URL
READING_LIST_URL = "https://medium.com/me/reading-list"

# Headers (add your own authentication headers if necessary)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Fetch Reading List HTML
response = requests.get(READING_LIST_URL, headers=HEADERS, cookies={"your_cookie_name": "your_cookie_value"})
if response.status_code != 200:
    print(f"Failed to fetch the Reading List. Status Code: {response.status_code}")
    exit()

# Parse the Reading List
soup = BeautifulSoup(response.text, 'html.parser')

# Find article links
articles = soup.find_all('a', {'data-action': 'open-post'})
article_links = [article['href'] for article in articles]

# Export each article as a PDF
for i, link in enumerate(article_links):
    if not link.startswith("https"):
        link = "https://medium.com" + link  # Ensure absolute URL
    
    print(f"Processing article: {link}")
    article_response = requests.get(link, headers=HEADERS)
    if article_response.status_code == 200:
        # Save article as PDF
        try:
            pdfkit.from_string(article_response.text, f"Medium_Article_{i+1}.pdf", configuration=pdfkit_config)
            print(f"Saved: Medium_Article_{i+1}.pdf")
        except Exception as e:
            print(f"Failed to save article as PDF: {e}")
    else:
        print(f"Failed to fetch article: {link} (Status: {article_response.status_code})")

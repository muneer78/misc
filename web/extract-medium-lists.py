from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

OUTPUT_FILE = "medium-reading-list.org"

def clean_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

def extract_story_links(page):
    soup = BeautifulSoup(page.content(), "html.parser")

    results = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]

        # Medium story URLs
        if "/p/" in href or href.count("/") >= 4:
            if href.startswith("/"):
                href = "https://medium.com" + href

            clean = clean_url(href)

            title = a.get_text(strip=True)

            # Skip empty/non-story links
            if (
                title
                and "?" not in clean
                and clean not in seen
                and "/lists/" not in clean
                and "/me/" not in clean
            ):
                seen.add(clean)
                results.append((title, clean))

    return results

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    # Persistent profile keeps you logged in
    context = p.chromium.launch_persistent_context(
    user_data_dir="playwright-medium-profile",
    headless=False
)

page = context.new_page()

# Open Medium login
page.goto("https://medium.com/m/signin")

print("\nLog into Medium in the browser window.")
input("Press ENTER after login is complete...")

    # Go to your Lists page
page.goto("https://medium.com/me/lists")

time.sleep(5)

# Scroll to load all lists
for _ in range(20):
    page.mouse.wheel(0, 5000)
    time.sleep(1)

soup = BeautifulSoup(page.content(), "html.parser")

list_links = []

for a in soup.find_all("a", href=True):
    href = a["href"]

    if "/lists/" in href:
        if href.startswith("/"):
            href = "https://medium.com" + href

        if href not in list_links:
            list_links.append(href)

all_articles = []
seen_articles = set()

print(f"\nFound {len(list_links)} lists")

for link in list_links:
    print(f"Processing: {link}")

    page.goto(link)
    time.sleep(3)

    # Scroll to load all stories
    for _ in range(25):
        page.mouse.wheel(0, 5000)
        time.sleep(0.5)

    stories = extract_story_links(page)

    for title, url in stories:
        if url not in seen_articles:
            seen_articles.add(url)
            all_articles.append((title, url))

# Write org file
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for title, url in all_articles:
        f.write(f"** TODO [[{url}][{title}]]\n")

print(f"\nSaved {len(all_articles)} links to {OUTPUT_FILE}")

browser.close()

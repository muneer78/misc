import requests
from bs4 import BeautifulSoup

def save_article(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    text = soup.get_text()
    filename = url.replace("https://", "").replace("/", "_")[:50] + ".md"
    with open(f"articles/{filename}", "w", encoding="utf-8") as f:
        f.write(text)
save_article("https://example.com/article")
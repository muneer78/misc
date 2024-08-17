import os
from datetime import datetime
import requests
from bs4 import BeautifulSoup

ROOT = "https://nitter.net"
RETRIES = 10
HEADERS = {
    "Accept": "*/*",
    "X-User-IP": "1.1.1.1",
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.4 Safari/605.1.15",
}

# Define the URL here
URL = "https://x.com/nameshiv/status/1301521850552315904"

class Thread:
    def __init__(self, author, date, pages):
        self.text = f'> by {author}  date: {date}\n'
        self.pages = pages
        self.counter = 1
        self.extract_thread()

    def get_content(self, tag, quote=''):
        if not quote:
            self.text += "\n---\n"
        for elt in tag:
            if elt.name == "a":
                self.get_link(elt)
            else:
                self.text += elt.replace("\n", "\n" + quote)
        self.text += "\n{}\n".format(quote)

    def get_link(self, tag):
        # Avoid putting members' names in links or useless local links
        if tag.next[0] == "@" or tag["href"][0] == '/':
            self.text += f'**{tag.text}**'
        else:
            self.text = f'{self.text}[{tag.text}]({tag["href"]})\n'

    def get_media(self, path, kind, line, a, b=None):
        url = ROOT + path
        res = get_request(url)
        ext = path.split(a)[-1][0:b]
        name = f'{kind}_{self.counter}.{ext}'
        if res:
            with open(name, "wb") as f:
                f.write(res.content)
            self.text += f'{line.format(name)}\n'
        else:
            self.text += f'Missing : {url}\n'
        self.counter += 1

    def check_if_quoted(self, tag):
        parents = tag.find_parents("div", {'class': ['quote-media-container', 'quote-text']})
        if parents:
            self.text += ">"

    def extract_thread(self):
        name = "main-thread"
        for _, page in enumerate(self.pages):
            if _ > 0:
                name = "after-tweet thread-line"
            tweets = page.find("div", class_=name)
            tags = tweets.select(
                "div.tweet-content.media-body, a.still-image, video,\
                div.card-content, div.quote-text, div.card-image, div.attachment.video-container")
            for tag in tags:
                # Text tags
                if tag['class'][0] == "tweet-content":
                    self.get_content(tag)
                if tag['class'][0] == "card-content":
                    self.text += f"**{tag.get_text().strip()}**\n"
                if tag['class'][0] == "quote-text":
                    date = tag.parent.find("span").text
                    date = datetime.strptime(date, "%d %b %Y").strftime("%d-%m-%Y")
                    writer = tag.parent.find("a", class_="username").text
                    url = ROOT + tag.parent.find("a", class_="quote-link")["href"]
                    self.text += f"\n>[**{writer}**  {date}]({url})  \n"
                    self.get_content(tag, ">")
                # Images & videos
                if tag['class'][0] == "still-image":
                    self.check_if_quoted(tag)
                    self.get_media(tag["href"], "image", "![image]({})", ".", None)
                if tag['class'][0] == "attachment":
                    self.check_if_quoted(tag)
                    self.get_media(tag.img["src"], "image", "![image]({})", ".", 3)
                if tag['class'][0] == "card-image":
                    parent = tag.find_parent("a", class_="card-container")
                    self.get_media(tag.img["src"], "image", f"[![image]({{}})]({parent['href']})", "format%3D", 3)
                if tag.name == "video":
                    self.get_media(tag.source["src"], "video", "![video]({})", ".", 3)

        self.text += "\n\n"

# Getting request
def get_request(url):
    for _ in range(RETRIES):
        try:
            res = requests.get(url, headers=HEADERS)
            if res.status_code == 200:
                return res
        except requests.exceptions.ConnectionError:
            print("We can't connect to the server")
    return None

def get_webpages(url):
    # Get all tweets in case of a very long thread
    res = get_request(url)
    if not res:
        print(f"Failed to fetch data from {url}")
        return []

    soup = BeautifulSoup(res.content, "lxml")
    fin = soup.find("div", class_="timeline-item thread-last")

    if not fin:
        more_replies = soup.find_all("a", class_="more-replies-text")
        if more_replies:
            next_page = more_replies[-1]['href']
            return [soup] + get_webpages(ROOT + next_page)
        else:
            print("No more replies found.")
            return [soup]

    return [soup]

def get_thread():
    # Use the URL defined at the top of the script
    url = URL
    pages = get_webpages(url)

    # Check if pages are found
    if not pages:
        print("No pages found.")
        return

    # Check if the expected element is found
    main_content = pages[0].find("div", class_="tweet-content media-body")
    if not main_content:
        print("Main content not found.")
        return

    name = main_content.text[0:20]

    # Check if the directory already exists
    if os.path.isdir(name):
        print("You already have this tweet")
        return

    # Create a new directory and write to file
    os.mkdir(name)
    os.chdir(name)

    author = pages[0].find("a", class_="username")
    if not author:
        print("Author not found.")
        return
    author = author.get_text()

    date = pages[0].find("p", class_="tweet-published")
    if not date:
        print("Date not found.")
        return
    date = date.text
    date = datetime.strptime(date, "%b %d, %Y · %I:%M %p %Z").strftime("%d-%m-%Y")

    thread = Thread(author, date, pages)
    with open("text.md", "w", encoding="utf-8") as file:
        file.write(thread.text)

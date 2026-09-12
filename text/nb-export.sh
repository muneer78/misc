#!/usr/bin/env python3

from pathlib import Path
from html import escape
from urllib.parse import urlparse
import re

NB_DIR = Path.home() / ".nb" / "home"
OUTPUT = Path.home() / "Desktop" / "bookmarks.html"


def title_from_url(url):
    """Create a reasonable bookmark title from the URL."""
    parsed = urlparse(url)
    path = parsed.path.rstrip("/")

    if path:
        name = path.split("/")[-1]
        name = re.sub(r"[-_]+", " ", name)
        name = re.sub(r"\.(html?|php)$", "", name)
        if name:
            return name.title()

    return parsed.netloc


bookmarks = []

for file in sorted(NB_DIR.glob("*.md")):
    try:
        url = file.read_text(encoding="utf-8").strip()
    except OSError:
        continue

    if not url.startswith(("http://", "https://")):
        continue

    title = title_from_url(url)
    bookmarks.append((title, url))


with OUTPUT.open("w", encoding="utf-8") as f:
    f.write("""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     Do Not Edit! -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
""")

    for title, url in bookmarks:
        f.write(
            f'    <DT><A HREF="{escape(url, quote=True)}">'
            f'{escape(title)}</A>\n'
        )

    f.write("</DL><p>\n")


print(f"Exported {len(bookmarks)} bookmarks")
print(f"Created: {OUTPUT}")

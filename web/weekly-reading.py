#!/usr/bin/env python3
"""
weekly_reading.py

Weekly reading-list processor.

What it does, in order:
  1. Reads the queue of org-mode links in READING_LIST (default: reading-list.org).
  2. Takes the next BATCH_SIZE entries (default 10), in file order (oldest first).
  3. Fetches each URL and strips it down to the readable article body with
     readability-lxml (same tool used in the feed-to-articles project).
  4. Writes all BATCH_SIZE articles into a single dated HTML digest file,
     saved into OUTPUT_DIR (web-tools/articles/).
  5. Adds a link to that digest at the top of ARTICLE_INDEX
     (web-tools/article-dir.html), inserted into the existing #article-list,
     labeled "M-D-YY Reading List" (e.g. "8-15-26 Reading List") with a
     "YYYY-MM-DD" date span --
     matching the site's current markup exactly.
  6. Removes those entries from READING_LIST and appends the original org
     lines to SENT_LIST (default: sent-urls.org), so the queue only ever
     shrinks and nothing is processed twice.

Usage:
    python weekly_reading.py

Run it on a weekly cron/GitHub Actions schedule, same idea as fetch.yml in
feed-to-articles.
"""

import argparse
import datetime as dt
import html
import re
from pathlib import Path

import requests
from trafilatura import extract, extract_metadata

# --- Hardcoded paths: edit these for your setup ---
READING_LIST = Path("/Users/muneer78/Documents/GitHub/emacs-files/reading-list.org")
SENT_LIST = Path("/Users/muneer78/Documents/GitHub/emacs-files/sent-urls.org")
# web-tools repo: digest HTML files go in articles/, article-dir.html (the
# index page) lives one level up, alongside articles/.
REPO_DIR = Path("/Users/muneer78/Documents/GitHub/web-tools")
OUTPUT_DIR = REPO_DIR / "articles"
ARTICLE_INDEX = REPO_DIR / "article-dir.html"
# ---------------------------------------------------

DEFAULT_BATCH_SIZE = 10
USER_AGENT = "weekly-reading-bot/1.0 (+personal use)"
REQUEST_TIMEOUT = 20

# Matches "** TODO [[url][title]]" (optionally with extra spaces after TODO,
# and tolerating a link split across lines like:
#   ** TODO [[https://example.com/foo
#   ][Title]]
ORG_LINK_RE = re.compile(
    r"^\*\*\s+TODO\s+\[\[(?P<url>.*?)\]\[(?P<title>.*?)\]\]\s*$",
    re.MULTILINE | re.DOTALL,
)


class ReadingEntry:
    def __init__(self, raw_text: str, url: str, title: str):
        self.raw_text = raw_text  # exact original text, for removal / re-append
        self.url = url.strip().replace("\n", "").strip()
        self.title = html.unescape(title.strip().replace("\n", " "))

    def __repr__(self):
        return f"ReadingEntry({self.title!r}, {self.url!r})"


def parse_reading_list(path: Path) -> list[ReadingEntry]:
    """Parse org-mode TODO links, oldest (top of file) first."""
    text = path.read_text(encoding="utf-8")
    entries = []
    for m in ORG_LINK_RE.finditer(text):
        entries.append(ReadingEntry(m.group(0), m.group("url"), m.group("title")))
    return entries


def remove_entries(path: Path, entries_to_remove: list[ReadingEntry]) -> None:
    """Rewrite the reading list with the given entries stripped out."""
    text = path.read_text(encoding="utf-8")
    for entry in entries_to_remove:
        # Remove the exact matched span once. Using str.replace with count=1
        # is safe here because ORG_LINK_RE captured the literal original text.
        text = text.replace(entry.raw_text, "", 1)
    # Collapse the blank lines left behind so the file doesn't accumulate gaps
    text = re.sub(r"\n{3,}", "\n\n", text)
    path.write_text(text, encoding="utf-8")


def append_sent(path: Path, entries: list[ReadingEntry]) -> None:
    """Append processed entries to the sent-urls.org archive, creating it if needed."""
    header = "" if path.exists() else "* Sent\n"
    with path.open("a", encoding="utf-8") as f:
        if header:
            f.write(header)
        for entry in entries:
            f.write(entry.raw_text.strip() + "\n")


def fetch_readable(entry: ReadingEntry) -> dict:
    """Fetch a URL and extract the article body with Trafilatura."""
    try:
        response = requests.get(
            entry.url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()

        content_html = extract(
            response.text,
            url=entry.url,
            output_format="html",
            include_comments=False,
            include_links=True,
            include_images=True,
            include_formatting=True,
        )

        if not content_html:
            raise ValueError("Trafilatura could not extract article content")

        metadata = extract_metadata(response.text, default_url=entry.url)

        return {
            "ok": True,
            "title": metadata.title if metadata and metadata.title else entry.title,
            "content_html": content_html,
            "error": None,
        }

    except Exception as e:
        return {
            "ok": False,
            "title": entry.title,
            "content_html": None,
            "error": str(e),
        }


def build_digest_html(results: list[tuple[ReadingEntry, dict]], week_label: str) -> str:
    articles_html = []
    for entry, result in results:
        if result["ok"]:
            body = f"""
    <article>
      <h2><a href="{html.escape(entry.url)}">{html.escape(result['title'])}</a></h2>
      <p class="source">{html.escape(entry.url)}</p>
      <div class="body">{result['content_html']}</div>
    </article>"""
        else:
            body = f"""
    <article class="failed">
      <h2><a href="{html.escape(entry.url)}">{html.escape(entry.title)}</a></h2>
      <p class="source">{html.escape(entry.url)}</p>
      <p class="error">Could not extract this article automatically ({html.escape(result['error'])}).
        <a href="{html.escape(entry.url)}">Read it on the original site</a> instead.</p>
    </article>"""
        articles_html.append(body)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Weekly Reading &mdash; {html.escape(week_label)}</title>
<style>
  body {{ max-width: 700px; margin: 2rem auto; padding: 0 1rem;
          font-family: Georgia, 'Times New Roman', serif; line-height: 1.6; color: #222; }}
  h1 {{ font-family: -apple-system, Helvetica, Arial, sans-serif; }}
  article {{ margin-bottom: 3rem; padding-bottom: 2rem; border-bottom: 1px solid #ddd; }}
  article h2 {{ margin-bottom: 0.2rem; font-size: 1.4rem; }}
  article h2 a {{ color: #111; text-decoration: none; }}
  .source {{ font-size: 0.8rem; color: #888; margin-top: 0; word-break: break-all; }}
  .body img {{ max-width: 100%; height: auto; }}
  .failed {{ color: #a33; }}
  .error {{ font-size: 0.9rem; }}
</style>
</head>
<body>
<h1>Weekly Reading &mdash; {html.escape(week_label)}</h1>
{''.join(articles_html)}
</body>
</html>
"""


# Fallback template, used only if article-dir.html doesn't exist yet.
# Mirrors the real file's structure: a <ul id="article-list"> that new
# <li><a>...</a><span class="date">...</span></li> entries get inserted into.
INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Article Directory</title>
</head>
<body>
  <div class="container">
    <div class="wrapper-masthead">
      <header class="masthead">
        <div class="site-name">Article Directory</div>
      </header>
    </div>

    <ul id="article-list">
    </ul>
  </div>
</body>
</html>
"""

ARTICLE_LIST_OPEN_TAG = '<ul id="article-list">'


def update_article_index(
    index_path: Path, digest_filename: str, label: str, date_str: str
) -> None:
    """Insert a new <li> at the top of #article-list in article-dir.html.

    Matches the site's existing markup exactly:
        <li><a href="articles/FILE">LABEL</a><span class="date">DATE</span></li>
    New entries go right after <ul id="article-list">, so the newest link is
    always first -- same position as the one hand-written example entry.
    """
    text = (
        index_path.read_text(encoding="utf-8")
        if index_path.exists()
        else INDEX_TEMPLATE
    )

    new_entry = (
        f'      <li><a href="articles/{html.escape(digest_filename)}">'
        f'{html.escape(label)}</a><span class="date">{html.escape(date_str)}</span></li>'
    )

    if ARTICLE_LIST_OPEN_TAG in text:
        text = text.replace(
            ARTICLE_LIST_OPEN_TAG, f"{ARTICLE_LIST_OPEN_TAG}\n{new_entry}", 1
        )
    elif "</ul>" in text:
        # #article-list tag missing but *some* <ul> is there -- insert before its close
        text = text.replace("</ul>", f"{new_entry}\n    </ul>", 1)
    else:
        # No <ul> at all -- rebuild a minimal one before </body>
        text = text.replace(
            "</body>",
            f'    <ul id="article-list">\n{new_entry}\n    </ul>\n  </body>',
            1,
        )

    index_path.write_text(text, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-size", default=DEFAULT_BATCH_SIZE, type=int)
    args = parser.parse_args()

    entries = parse_reading_list(READING_LIST)
    if not entries:
        print("No entries found in reading list; nothing to do.")
        return

    batch = entries[: args.batch_size]
    print(f"Processing {len(batch)} of {len(entries)} queued articles...")

    results = []
    for entry in batch:
        print(f"  fetching: {entry.title} ({entry.url})")
        results.append((entry, fetch_readable(entry)))

    today = dt.date.today()
    week_label = today.isoformat()
    digest_html = build_digest_html(results, week_label)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"weekly-reading-{week_label}.html"
    out_path.write_text(digest_html, encoding="utf-8")
    print(f"Wrote digest to {out_path}")

    index_label = f"{today.month}-{today.day}-{today.strftime('%y')} Reading List"
    update_article_index(ARTICLE_INDEX, out_path.name, index_label, today.isoformat())
    print(f"Updated {ARTICLE_INDEX} with entry: {index_label}")

    remove_entries(READING_LIST, batch)
    append_sent(SENT_LIST, batch)
    print(f"Removed {len(batch)} entries from {READING_LIST}, archived to {SENT_LIST}")
    print(f"Done -- files written under {REPO_DIR}, no git action taken.")


if __name__ == "__main__":
    main()

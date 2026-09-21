#!/usr/bin/env python3
"""
Weekly reading-list processor.

Reads Org-mode TODO links, extracts article content with Trafilatura, writes a
dated HTML digest, updates the article index, and archives processed links.
"""

import argparse
import datetime as dt
import html
import re
from pathlib import Path

import requests
from trafilatura import extract, extract_metadata


READING_LIST = Path("/Users/muneer78/Documents/GitHub/emacs-files/reading-list.org")
SENT_LIST = Path("/Users/muneer78/Documents/GitHub/emacs-files/sent-urls.org")

REPO_DIR = Path("/Users/muneer78/Documents/GitHub/web-tools")
OUTPUT_DIR = REPO_DIR / "articles"
ARTICLE_INDEX = REPO_DIR / "article-dir.html"

DEFAULT_BATCH_SIZE = 10
USER_AGENT = "weekly-reading-bot/1.0 (+personal use)"
REQUEST_TIMEOUT = 20

ORG_LINK_RE = re.compile(
    r"^\*\*\s+TODO\s+\[\[(?P<url>.*?)\]\[(?P<title>.*?)\]\]\s*$",
    re.MULTILINE | re.DOTALL,
)


class ReadingEntry:
    def __init__(self, raw_text: str, url: str, title: str):
        self.raw_text = raw_text
        self.url = url.strip().replace("\n", "").strip()
        self.title = html.unescape(title.strip().replace("\n", " "))

    def __repr__(self):
        return f"ReadingEntry({self.title!r}, {self.url!r})"


def parse_reading_list(path: Path) -> list[ReadingEntry]:
    """Parse Org-mode TODO links, oldest first."""
    text = path.read_text(encoding="utf-8")
    return [
        ReadingEntry(m.group(0), m.group("url"), m.group("title"))
        for m in ORG_LINK_RE.finditer(text)
    ]


def remove_entries(path: Path, entries_to_remove: list[ReadingEntry]) -> None:
    """Remove processed entries from the reading list."""
    text = path.read_text(encoding="utf-8")
    for entry in entries_to_remove:
        text = text.replace(entry.raw_text, "", 1)

    text = re.sub(r"\n{3,}", "\n\n", text)
    path.write_text(text, encoding="utf-8")


def append_sent(path: Path, entries: list[ReadingEntry]) -> None:
    """Append processed entries to the sent archive."""
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


def build_digest_html(
    results: list[tuple[ReadingEntry, dict]], week_label: str
) -> str:
    """Build the weekly digest using the Synthwave web-app theme."""
    articles_html = []

    for number, (entry, result) in enumerate(results, start=1):
        title = html.escape(result["title"] if result["ok"] else entry.title)
        url = html.escape(entry.url, quote=True)

        if result["ok"]:
            article = f"""
        <article class="article-card" id="article-{number}">
          <div class="article-number">{number:02d}</div>
          <h2><a href="{url}">{title}</a></h2>
          <p class="source">
            <span class="source-label">SOURCE</span>
            <a href="{url}">{url}</a>
          </p>
          <div class="article-body">
            {result["content_html"]}
          </div>
          <div class="article-footer">
            <a class="original-link" href="{url}">READ ORIGINAL →</a>
          </div>
        </article>"""
        else:
            error = html.escape(result["error"])
            article = f"""
        <article class="article-card failed" id="article-{number}">
          <div class="article-number">{number:02d}</div>
          <h2><a href="{url}">{title}</a></h2>
          <p class="source">
            <span class="source-label">SOURCE</span>
            <a href="{url}">{url}</a>
          </p>
          <p class="error">
            Could not extract this article automatically: {error}
          </p>
          <div class="article-footer">
            <a class="original-link" href="{url}">READ ORIGINAL →</a>
          </div>
        </article>"""

        articles_html.append(article)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Weekly Reading — {html.escape(week_label)}</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fira+Sans:ital,wght@0,300;0,400;0,700;1,400&family=Train+One&display=swap" rel="stylesheet">

  <style>
    :root {{
      --pink: #ff7edb;
      --purple: #241b2f;
      --blue: #03edf9;
      --yellow: #fede5d;
      --offwhite: #ffffff;
      --neongreen: #72f1b8;
      --green: #72f1b8;
      --panel: #2d2239;
      --muted: #c8bfd2;
    }}

    * {{
      box-sizing: border-box;
    }}

    html {{
      font-size: 100%;
      scroll-behavior: smooth;
    }}

    body {{
      margin: 0;
      background: var(--purple);
      font-family: "Fira Sans", sans-serif;
      font-size: 18px;
      line-height: 1.65;
      color: var(--offwhite);
    }}

    a {{
      color: var(--blue);
      text-decoration-thickness: 2px;
      text-underline-offset: 3px;
    }}

    a:hover {{
      color: var(--pink);
    }}

    .container {{
      width: min(100% - 32px, 900px);
      margin: 0 auto;
      padding: 48px 0 80px;
    }}

    .masthead {{
      margin-bottom: 48px;
      padding: 32px;
      border: 2px solid var(--blue);
      background: var(--panel);
      box-shadow: 8px 8px 0 var(--pink);
    }}

    .eyebrow {{
      margin: 0 0 8px;
      color: var(--neongreen);
      font-size: 0.85rem;
      font-weight: 700;
      letter-spacing: 0.16em;
      text-transform: uppercase;
    }}

    h1, h2, h3, h4, h5, h6 {{
      line-height: 1.2;
    }}

    h1 {{
      margin: 0;
      color: var(--yellow);
      font-family: "Train One", sans-serif;
      font-size: clamp(2.1rem, 8vw, 4.5rem);
      font-weight: 400;
      letter-spacing: 0.02em;
      overflow-wrap: anywhere;
    }}

    .digest-date {{
      margin: 16px 0 0;
      color: var(--muted);
    }}

    .article-card {{
      position: relative;
      margin-bottom: 48px;
      padding: 32px;
      border: 2px solid var(--pink);
      background: var(--panel);
      box-shadow: 8px 8px 0 var(--blue);
    }}

    .article-number {{
      display: inline-block;
      margin-bottom: 14px;
      color: var(--purple);
      background: var(--yellow);
      padding: 4px 9px;
      font-size: 0.8rem;
      font-weight: 700;
      letter-spacing: 0.1em;
    }}

    .article-card h2 {{
      margin: 0 0 12px;
      font-size: clamp(1.5rem, 4vw, 2.2rem);
    }}

    .article-card h2 a {{
      color: var(--offwhite);
      text-decoration: none;
    }}

    .article-card h2 a:hover {{
      color: var(--pink);
    }}

    .source {{
      margin: 0 0 28px;
      color: var(--muted);
      font-size: 0.8rem;
      overflow-wrap: anywhere;
    }}

    .source-label {{
      display: inline-block;
      margin-right: 8px;
      color: var(--neongreen);
      font-weight: 700;
      letter-spacing: 0.08em;
    }}

    .source a {{
      color: var(--muted);
    }}

    .article-body {{
      overflow-wrap: anywhere;
    }}

    .article-body h1,
    .article-body h2,
    .article-body h3,
    .article-body h4 {{
      margin-top: 1.6em;
      color: var(--yellow);
      font-family: "Fira Sans", sans-serif;
    }}

    .article-body p {{
      margin: 0 0 1.2em;
    }}

    .article-body img,
    .article-body figure {{
      max-width: 100%;
      height: auto;
    }}

    .article-body img {{
      display: block;
      margin: 24px auto;
      border: 2px solid var(--blue);
    }}

    .article-body blockquote {{
      margin: 24px 0;
      padding: 8px 0 8px 20px;
      border-left: 4px solid var(--pink);
      color: var(--muted);
    }}

    .article-body pre {{
      overflow-x: auto;
      padding: 16px;
      border: 1px solid var(--neongreen);
      background: #17101f;
    }}

    .article-body code {{
      color: var(--neongreen);
      background: #17101f;
      padding: 0.1em 0.3em;
      font-size: 0.9em;
    }}

    .article-body pre code {{
      padding: 0;
    }}

    .article-body hr {{
      border: 0;
      border-top: 2px solid var(--blue);
      margin: 36px 0;
    }}

    .article-body table {{
      display: block;
      width: 100%;
      overflow-x: auto;
      border-collapse: collapse;
      margin: 24px 0;
    }}

    .article-body th,
    .article-body td {{
      padding: 10px 12px;
      border: 1px solid var(--blue);
      text-align: left;
    }}

    .article-body th {{
      color: var(--yellow);
    }}

    .article-footer {{
      margin-top: 32px;
      padding-top: 18px;
      border-top: 1px solid rgba(3, 237, 249, 0.45);
    }}

    .original-link {{
      color: var(--neongreen);
      font-weight: 700;
      letter-spacing: 0.04em;
      text-decoration: none;
    }}

    .failed {{
      border-color: var(--yellow);
      box-shadow: 8px 8px 0 var(--pink);
    }}

    .error {{
      color: var(--yellow);
    }}

    .page-footer {{
      padding-top: 8px;
      color: var(--muted);
      font-size: 0.85rem;
      text-align: center;
    }}

    @media (max-width: 600px) {{
      body {{
        font-size: 16px;
      }}

      .container {{
        width: min(100% - 24px, 900px);
        padding-top: 28px;
      }}

      .masthead,
      .article-card {{
        padding: 22px;
        box-shadow: 5px 5px 0 var(--blue);
      }}

      .masthead {{
        box-shadow: 5px 5px 0 var(--pink);
      }}
    }}
  </style>
</head>

<body>
  <main class="container">
    <header class="masthead">
      <p class="eyebrow">Reading List / {len(results)} Articles</p>
      <h1>Weekly Reading</h1>
      <p class="digest-date">{html.escape(week_label)}</p>
    </header>

    {''.join(articles_html)}

    <footer class="page-footer">
      Weekly Reading · {html.escape(week_label)}
    </footer>
  </main>
</body>
</html>
"""


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
    """Insert a new digest link at the top of #article-list."""
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
            ARTICLE_LIST_OPEN_TAG,
            f"{ARTICLE_LIST_OPEN_TAG}\n{new_entry}",
            1,
        )
    elif "</ul>" in text:
        text = text.replace("</ul>", f"{new_entry}\n    </ul>", 1)
    else:
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
    update_article_index(
        ARTICLE_INDEX,
        out_path.name,
        index_label,
        today.isoformat(),
    )
    print(f"Updated {ARTICLE_INDEX} with entry: {index_label}")

    remove_entries(READING_LIST, batch)
    append_sent(SENT_LIST, batch)

    print(
        f"Removed {len(batch)} entries from {READING_LIST}, "
        f"archived to {SENT_LIST}"
    )
    print(f"Done -- files written under {REPO_DIR}, no git action taken.")


if __name__ == "__main__":
    main()

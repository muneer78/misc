#!/usr/bin/env python3
"""
weekly_reading.py

Weekly reading-list processor.

What it does, in order:
  1. Reads the queue of org-mode links in READING_LIST (default: reading-list.org).
  2. Takes the next BATCH_SIZE entries (default 10), in file order (oldest first).
  3. Fetches each URL and strips it down to the readable article body with
     readability-lxml (same tool used in the feed-to-articles project).
  4. Writes all BATCH_SIZE articles into a single dated HTML digest file.
  5. Removes those entries from READING_LIST and appends the original org
     lines to SENT_LIST (default: sent-urls.org), so the queue only ever
     shrinks and nothing is processed twice.
  6. "Sends" the digest by copying it into SHARED_DIR and, if SHARED_DIR is a
     git repo, committing and pushing it -- the same git-repo-as-storage
     approach used for articles-today.md in the feed-to-articles project.

Usage:
    python weekly_reading.py --reading-list reading-list.org --shared-dir /path/to/shared/repo

Run it on a weekly cron/GitHub Actions schedule, same idea as fetch.yml in
feed-to-articles.
"""

import argparse
import datetime as dt
import html
import re
import subprocess
import sys
from pathlib import Path

import requests
from readability import Document

# --- Hardcoded paths: edit these for your setup ---
READING_LIST = Path("/Users/muneer78/Documents/GitHub/emacs-files/reading-list.org")
SENT_LIST = Path("/Users/muneer78/Documents/GitHub/emacs-files/sent-urls.org")
OUTPUT_DIR = Path("/Users/muneer78/Google Drive/My Drive/Shared/digests/")
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
    """Fetch a URL and extract the readable article body via readability-lxml."""
    try:
        resp = requests.get(
            entry.url,
            headers={"User-Agent": USER_AGENT},
            timeout=REQUEST_TIMEOUT,
        )
        resp.raise_for_status()
        doc = Document(resp.text)
        return {
            "ok": True,
            "title": doc.short_title() or entry.title,
            "content_html": doc.summary(html_partial=True),
            "error": None,
        }
    except Exception as e:  # network errors, parse errors, non-200s, etc.
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


def send_to_shared(local_file: Path, shared_dir: Path) -> None:
    """Copy the digest into shared_dir; commit & push if it's a git repo."""
    shared_dir.mkdir(parents=True, exist_ok=True)
    dest = shared_dir / local_file.name
    dest.write_bytes(local_file.read_bytes())

    if (shared_dir / ".git").exists():
        subprocess.run(["git", "add", dest.name], cwd=shared_dir, check=True)
        commit = subprocess.run(
            ["git", "commit", "-m", f"Weekly reading digest: {local_file.stem}"],
            cwd=shared_dir,
        )
        if commit.returncode == 0:
            subprocess.run(["git", "push"], cwd=shared_dir, check=True)
        # a nonzero commit code usually just means "nothing to commit"; ignore
    else:
        print(f"[info] {shared_dir} is not a git repo; file copied only, no push done.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--batch-size", default=DEFAULT_BATCH_SIZE, type=int)
    parser.add_argument(
        "--shared-dir",
        default=None,
        type=Path,
        help="Folder (optionally a git repo) to copy/push the digest to",
    )
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

    week_label = dt.date.today().isoformat()
    digest_html = build_digest_html(results, week_label)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"weekly-reading-{week_label}.html"
    out_path.write_text(digest_html, encoding="utf-8")
    print(f"Wrote digest to {out_path}")

    remove_entries(READING_LIST, batch)
    append_sent(SENT_LIST, batch)
    print(f"Removed {len(batch)} entries from {READING_LIST}, archived to {SENT_LIST}")

    if args.shared_dir:
        send_to_shared(out_path, args.shared_dir)
        print(f"Sent digest to shared folder: {args.shared_dir}")
    else:
        print("No --shared-dir given; skipped the send step.")


if __name__ == "__main__":
    main()

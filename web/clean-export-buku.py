#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Filter a copy of a Buku database and export it as HTML.

The source database is opened read-only and is never modified. Link checking
is optional; when enabled, HTTP 404 and 410 responses are removed from the
copy and other HTTP failures are tagged with Buku's ``http:{}`` pattern. An
existing output page keeps its layout and styling while its bookmark list is
replaced.
"""

import argparse
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path


DEFAULT_DB = Path.home() / ".local/share/buku/bookmarks.db"
DEFAULT_OUTPUT = Path("/Users/muneer78/Documents/GitHub/web-tools/bookmarks.html")
DEFAULT_DEAD_STATUSES = "404,410"
DEFAULT_EXCLUDED_TAGS = "porn,sex"

BOOKMARK_LIST_RE = re.compile(
    r'(?P<open><ul\b[^>]*\bid=["\']bookmark-list["\'][^>]*>)'
    r"(?P<items>.*?)"
    r"(?P<close></ul\s*>)",
    re.IGNORECASE | re.DOTALL,
)
EXPORTED_LIST_RE = re.compile(r"<ul>(?P<items>.*?)</ul\s*>", re.IGNORECASE | re.DOTALL)


def copy_database(source: Path, destination: Path) -> None:
    if not source.is_file():
        raise SystemExit(f"error: Buku DB not found at {source}")
    if source.resolve() == destination.resolve():
        raise SystemExit("error: the filtered DB must not overwrite the source DB")

    destination.parent.mkdir(parents=True, exist_ok=True)
    source_uri = f"{source.resolve().as_uri()}?mode=ro"
    with sqlite3.connect(source_uri, uri=True) as source_db:
        with sqlite3.connect(destination) as destination_db:
            source_db.backup(destination_db)


def exclude_tagged_bookmarks(db_path: Path, excluded_tags: set[str]) -> int:
    if not excluded_tags:
        return 0

    with sqlite3.connect(db_path) as connection:
        rows = connection.execute("SELECT id, tags FROM bookmarks").fetchall()
        excluded_ids = [
            bookmark_id
            for bookmark_id, raw_tags in rows
            if excluded_tags.intersection(
                tag.strip().casefold()
                for tag in (raw_tags or "").split(",")
                if tag.strip()
            )
        ]
        connection.executemany(
            "DELETE FROM bookmarks WHERE id = ?",
            ((bookmark_id,) for bookmark_id in excluded_ids),
        )
    return len(excluded_ids)


def clean_links(
    db_path: Path,
    buku: str,
    dead_statuses: str,
    threads: int,
    update_redirects: bool,
) -> None:
    command = [
        buku,
        "--nostdin",
        "--db",
        str(db_path),
        "--update",
        "--tag-error",
        "http:{}",
    ]
    if update_redirects:
        command.append("--url-redirect")
    if dead_statuses:
        command.extend(["--del-error", dead_statuses])
    command.extend(["--threads", str(threads), "--tacit"])
    subprocess.run(command, check=True)


def export_html(db_path: Path, output: Path, css_href: str) -> None:
    exporter = Path(__file__).with_name("export-buku.py")
    if not exporter.is_file():
        raise SystemExit(f"error: exporter not found at {exporter}")

    output.parent.mkdir(parents=True, exist_ok=True)
    existing_html = output.read_text(encoding="utf-8") if output.is_file() else None

    with tempfile.TemporaryDirectory(prefix="buku-export-") as temp_dir:
        exported_path = Path(temp_dir) / "bookmarks.html"
        subprocess.run(
            [
                sys.executable,
                str(exporter),
                "--db",
                str(db_path),
                "--format",
                "html",
                "--css",
                css_href,
                "--output",
                str(exported_path),
            ],
            check=True,
        )
        exported_html = exported_path.read_text(encoding="utf-8")

    if existing_html is None:
        output.write_text(exported_html, encoding="utf-8")
        return

    existing_list = BOOKMARK_LIST_RE.search(existing_html)
    exported_list = EXPORTED_LIST_RE.search(exported_html)
    if not existing_list or not exported_list:
        raise SystemExit(
            "error: unable to preserve styling; existing HTML must contain "
            "<ul id=\"bookmark-list\">"
        )

    items = exported_list.group("items").strip()
    updated_html = (
        existing_html[: existing_list.start("items")]
        + f"\n{items}\n"
        + existing_html[existing_list.end("items") :]
    )
    output.write_text(updated_html, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB,
        help=f"source Buku DB (default: {DEFAULT_DB})",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"HTML output path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--exclude",
        default=DEFAULT_EXCLUDED_TAGS,
        help=(
            "comma-separated tags to omit before checking links "
            f"(default: {DEFAULT_EXCLUDED_TAGS})"
        ),
    )
    parser.add_argument(
        "--delete-errors",
        default=DEFAULT_DEAD_STATUSES,
        help=(
            "HTTP statuses Buku should delete (default: 404,410); "
            "pass an empty value to retain and tag all failures"
        ),
    )
    parser.add_argument(
        "--threads",
        type=int,
        choices=range(1, 11),
        default=4,
        metavar="N",
        help="concurrent Buku requests, 1-10 (default: 4)",
    )
    parser.add_argument(
        "--buku",
        default="buku",
        help="Buku executable (default: buku)",
    )
    parser.add_argument(
        "--css",
        default="static/mun.css",
        help="stylesheet href used when creating a new HTML file",
    )
    parser.add_argument(
        "--filtered-db",
        type=Path,
        help="retain the cleaned, filtered database at this path",
    )
    parser.add_argument(
        "--check-links",
        action="store_true",
        help="refresh links, tag HTTP errors, and delete dead links",
    )
    parser.add_argument(
        "--update-redirects",
        action="store_true",
        help="rewrite permanent redirects (can fail when the target already exists)",
    )
    return parser.parse_args()


def run(args: argparse.Namespace, db_path: Path) -> None:
    source = args.db.expanduser()
    output = args.output.expanduser()
    if output.resolve() in {source.resolve(), db_path.resolve()}:
        raise SystemExit("error: HTML output must not overwrite a database")

    copy_database(source, db_path)
    excluded_tags = {
        tag.strip().casefold() for tag in args.exclude.split(",") if tag.strip()
    }
    excluded_count = exclude_tagged_bookmarks(db_path, excluded_tags)
    print(f"Filtered {excluded_count} bookmark(s) by tag.", file=sys.stderr)

    if args.check_links:
        buku = shutil.which(args.buku)
        if not buku:
            raise SystemExit(f"error: Buku executable not found: {args.buku}")
        clean_links(
            db_path,
            buku,
            args.delete_errors.strip(),
            args.threads,
            args.update_redirects,
        )

    export_html(db_path, output, args.css)


def main() -> None:
    args = parse_args()
    if args.filtered_db:
        filtered_db = args.filtered_db.expanduser()
        run(args, filtered_db)
        print(f"Filtered DB: {filtered_db}", file=sys.stderr)
    else:
        with tempfile.TemporaryDirectory(prefix="buku-clean-") as temp_dir:
            run(args, Path(temp_dir) / "bookmarks.db")


if __name__ == "__main__":
    main()

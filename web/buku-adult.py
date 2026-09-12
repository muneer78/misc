#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Export Buku bookmarks tagged ``porn`` or ``sex`` as an HTML page."""

import argparse
import subprocess
import sys
from pathlib import Path


DEFAULT_DB = Path.home() / ".local/share/buku/bookmarks.db"
DEFAULT_OUTPUT = Path("/Volumes/doak/files/personal/bookmarks/adult.html")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB,
        help=f"Buku DB (default: {DEFAULT_DB})",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"HTML output path (default: {DEFAULT_OUTPUT})",
    )
    parser.add_argument(
        "--css",
        default="static/mun.css",
        help="stylesheet href embedded in the HTML",
    )
    args = parser.parse_args()

    exporter = Path(__file__).with_name("export-buku.py")
    subprocess.run(
        [
            sys.executable,
            str(exporter),
            "--db",
            str(args.db.expanduser()),
            "--include",
            "porn,sex",
            "--format",
            "html",
            "--css",
            args.css,
            "--output",
            str(args.output.expanduser()),
        ],
        check=True,
    )


if __name__ == "__main__":
    main()

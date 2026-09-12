#!/usr/bin/env python3

import html
import json
import subprocess
from pathlib import Path

OUTPUT = Path("github-starred.html")


def get_starred_repos():
    """Retrieve all repositories starred by the authenticated GitHub user."""

    result = subprocess.run(
        [
            "gh", "api",
            "--paginate",
            "--slurp",
            "/user/starred",
            "-H", "Accept: application/vnd.github+json",
        ],
        capture_output=True,
        text=True,
        check=True,
    )

    pages = json.loads(result.stdout)
    return [repo for page in pages for repo in page]


def make_tags(repo):
    """Create Buku tags from GitHub metadata."""

    tags = {"github"}

    # Primary programming language
    if repo.get("language"):
        tags.add(repo["language"].lower())

    # GitHub repository topics
    for topic in repo.get("topics", []):
        tags.add(topic.lower())

    return ",".join(sorted(tags))


def main():
    repos = get_starred_repos()

    lines = [
        "<!DOCTYPE NETSCAPE-Bookmark-file-1>",
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">',
        "<TITLE>GitHub Starred Repositories</TITLE>",
        "<H1>GitHub Starred Repositories</H1>",
        "<DL><p>",
    ]

    for repo in repos:
        name = html.escape(repo["full_name"])
        url = html.escape(repo["html_url"], quote=True)
        tags = html.escape(make_tags(repo), quote=True)

        lines.append(
            f'    <DT><A HREF="{url}" TAGS="{tags}">{name}</A>'
        )

        # Preserve GitHub description as the bookmark description
        if repo.get("description"):
            description = html.escape(repo["description"])
            lines.append(f"    <DD>{description}")

    lines.append("</DL><p>")

    OUTPUT.write_text("\n".join(lines), encoding="utf-8")

    print(f"Exported {len(repos)} starred repositories.")
    print(f"Output: {OUTPUT}")


if __name__ == "__main__":
    main()
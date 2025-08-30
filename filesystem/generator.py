from pathlib import Path
import math
import markdown
import frontmatter
from jinja2 import Environment, FileSystemLoader
from collections import defaultdict
import shutil
import xml.etree.ElementTree as ET
from datetime import datetime

# Config
POSTS_PER_PAGE = 10

content_dir = Path("content")
output_dir = Path("site")
template_dir = Path("templates")
static_dir = Path("static")

env = Environment(loader=FileSystemLoader(template_dir))
template = env.get_template("base.html")


def save_html(path, html):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


def make_rss_feed(title, link, description, posts):
    rss = ET.Element("rss", version="2.0")
    channel = ET.SubElement(rss, "channel")
    ET.SubElement(channel, "title").text = title
    ET.SubElement(channel, "link").text = link
    ET.SubElement(channel, "description").text = description

    for post in posts:
        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = post["title"]
        ET.SubElement(
            item, "link"
        ).text = f"{link}/{post['section']}/{post['slug']}.html"
        ET.SubElement(
            item, "guid"
        ).text = f"{link}/{post['section']}/{post['slug']}.html"
        ET.SubElement(item, "pubDate").text = datetime.strptime(
            post["date"], "%Y-%m-%d"
        ).strftime("%a, %d %b %Y 00:00:00 +0000")
        ET.SubElement(item, "description").text = post["excerpt"]

    return ET.tostring(rss, encoding="utf-8", xml_declaration=True).decode("utf-8")


def render_breadcrumb(section=None, post_title=None):
    """Return HTML for breadcrumb navigation, styled."""
    parts = ['<a href="/">Home</a>']
    if section:
        section_url = f"/{section}"
        section_name = section.title()
        parts.append(f'<a href="{section_url}">{section_name}</a>')
    if post_title:
        parts.append(post_title)
    return '<nav class="breadcrumb">' + " &gt; ".join(parts) + "</nav>"


all_posts = []
tags = defaultdict(list)
sections = defaultdict(list)

# Load all posts from content (including subfolders)
for md_file in content_dir.rglob("*.md"):
    post = frontmatter.load(md_file)
    rel_dir = md_file.parent.relative_to(content_dir)
    slug = md_file.stem
    html_body = markdown.markdown(post.content)
    excerpt = "\n".join(post.content.split("\n\n")[:3])

    post_data = {
        "title": post["title"],
        "date": post["date"],
        "tags": post.get("tags", []),
        "slug": slug,
        "body": html_body,
        "excerpt": excerpt,
        "section": str(rel_dir),
    }
    all_posts.append(post_data)
    sections[str(rel_dir)].append(post_data)
    for tag in post_data["tags"]:
        tags[tag].append(post_data)

    # Write individual post page with breadcrumb
    breadcrumb_html = render_breadcrumb(
        section=str(rel_dir), post_title=post_data["title"]
    )
    content_html = breadcrumb_html + post_data["body"]
    page_html = template.render(title=post_data["title"], content=content_html)
    save_html(output_dir / rel_dir / f"{slug}.html", page_html)

# Homepage (last 5 posts)
latest = sorted(all_posts, key=lambda x: x["date"], reverse=True)[:5]
index_html = "<h2>Recent Posts</h2>"
for post in latest:
    index_html += (
        f"<h3><a href='/{post['section']}/{post['slug']}.html'>{post['title']}</a></h3>"
    )
    index_html += f"<p>{markdown.markdown(post['excerpt'])}</p><hr>"
save_html(output_dir / "index.html", template.render(title="Home", content=index_html))

# Archive page
archive_html = "<h2>Archive</h2><ul>"
for post in sorted(all_posts, key=lambda x: x["date"], reverse=True):
    archive_html += f"<li><a href='/{post['section']}/{post['slug']}.html'>{post['title']}</a> - {post['date']}</li>"
archive_html += "</ul>"
save_html(
    output_dir / "archive.html", template.render(title="Archive", content=archive_html)
)

# Section pages with pagination & breadcrumb
for section, posts in sections.items():
    posts = sorted(posts, key=lambda x: x["date"], reverse=True)
    total_pages = math.ceil(len(posts) / POSTS_PER_PAGE)

    for page_num in range(1, total_pages + 1):
        start = (page_num - 1) * POSTS_PER_PAGE
        end = start + POSTS_PER_PAGE
        page_posts = posts[start:end]

        # Build post list html
        section_html = render_breadcrumb(section=section)
        section_html += f"<h2>{section.title()}</h2><ul>"
        for post in page_posts:
            section_html += (
                f"<li><a href='/{section}/{post['slug']}.html'>{post['title']}</a></li>"
            )
        section_html += "</ul>"

        # Pagination navigation
        nav_html = '<nav class="pagination">'
        if page_num > 1:
            prev_page = "index.html" if page_num == 2 else f"page{page_num - 1}.html"
            nav_html += f'<a href="{prev_page}">&lt; Previous</a>'
        if page_num < total_pages:
            next_page = f"page{page_num + 1}.html"
            nav_html += f'<a href="{next_page}">Next &gt;</a>'
        nav_html += "</nav>"

        section_html += nav_html

        # Save page: page 1 = index.html, others pageN.html
        filename = "index.html" if page_num == 1 else f"page{page_num}.html"
        save_html(
            output_dir / section / filename,
            template.render(title=section.title(), content=section_html),
        )

# Tag pages
for tag, tagged_posts in tags.items():
    tag_html = f"<h2>Posts tagged with '{tag}'</h2><ul>"
    for post in tagged_posts:
        tag_html += f"<li><a href='/{post['section']}/{post['slug']}.html'>{post['title']}</a></li>"
    tag_html += "</ul>"
    save_html(
        output_dir / "tags" / f"{tag}.html",
        template.render(title=f"Tag: {tag}", content=tag_html),
    )

# RSS: main blog
blog_rss = make_rss_feed(
    "My Blog",
    "https://example.com",
    "Recent posts",
    sorted(all_posts, key=lambda x: x["date"], reverse=True)[:10],
)
save_html(output_dir / "rss.xml", blog_rss)

# RSS: per tag
for tag, tagged_posts in tags.items():
    tag_rss = make_rss_feed(
        f"My Blog - Tag: {tag}",
        "https://example.com/tags",
        f"Posts tagged {tag}",
        tagged_posts[:10],
    )
    save_html(output_dir / "tags" / f"{tag}.xml", tag_rss)

# Copy static files
output_static = output_dir / "static"
if output_static.exists():
    shutil.rmtree(output_static)
shutil.copytree(static_dir, output_static)

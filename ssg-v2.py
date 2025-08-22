#!/usr/bin/env python3
"""
Enhanced Static Site Generator with Tag Pages (Jekyll-tagging plugin functionality)
"""

import shutil
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional
import re
from collections import defaultdict

# Try different frontmatter libraries
try:
    import frontmatter

    PARSER_TYPE = "frontmatter"
except ImportError:
    try:
        import python_frontmatter as frontmatter

        PARSER_TYPE = "python_frontmatter"
    except ImportError:
        print("No frontmatter library found. Installing python-frontmatter...")
        import subprocess

        subprocess.run(["pip", "install", "python-frontmatter"])
        import python_frontmatter as frontmatter

        PARSER_TYPE = "python_frontmatter"

# Try to import Jinja2
try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    JINJA2_AVAILABLE = True
except ImportError:
    print("Jinja2 not found. Installing Jinja2...")
    import subprocess

    subprocess.run(["pip", "install", "Jinja2"])
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    JINJA2_AVAILABLE = True

# Try to import mistune
try:
    import mistune

    MISTUNE_AVAILABLE = True
    print(f"✅ Using Mistune version: {mistune.__version__}")
except ImportError:
    print("Mistune library not found. Installing mistune...")
    import subprocess

    subprocess.run(["pip", "install", "mistune"])
    try:
        import mistune

        MISTUNE_AVAILABLE = True
        print(f"✅ Using Mistune version: {mistune.__version__}")
    except ImportError:
        MISTUNE_AVAILABLE = False
        print("❌ Failed to install mistune library. Basic conversion will be used.")

# Try to import send2trash for safer directory removal
try:
    import send2trash

    SEND2TRASH_AVAILABLE = True
    print("✅ send2trash available - will move old site to trash")
except ImportError:
    SEND2TRASH_AVAILABLE = False
    print("⚠️  send2trash not available - will create timestamped backup instead")


class SSGGenerator:
    def __init__(
        self,
        content_dir: str = "content",
        output_dir: str = "site",
        template_dir: str = "templates",
    ):
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.template_dir = Path(template_dir)
        self.posts = []
        self.collections = {}
        self.tags = defaultdict(list)  # Tag name -> list of posts
        self.tag_counts = defaultdict(int)  # Tag name -> count

        self.site_config = {
            "name": "Encyclopedia Muneerica",
            "description": "A YungMun Joint",
            "baseurl": "",
            "url": "",
            "github": "muneer78",
            "twitter": "reenum",
            "navigation": [
                {"name": "Archive", "url": "/archive.html"},
                {"name": "Tags", "url": "/tags/"},
            ],
            "tag_config": {
                "permalink": "/tags/:tag/",  # URL structure for tag pages
                "layout": "tag_page",  # Template for tag pages
                "min_posts": 1,  # Minimum posts required to generate tag page
                "sort_by": "date",  # Sort tag posts by date
                "sort_order": "desc",  # Sort order (asc/desc)
            },
        }

        # Initialize Mistune markdown parser
        if MISTUNE_AVAILABLE:
            self.markdown_parser = mistune.create_markdown(
                escape=False, plugins=["strikethrough", "footnotes", "table"]
            )
        else:
            self.markdown_parser = None

        if JINJA2_AVAILABLE:
            self.jinja_env = Environment(
                loader=FileSystemLoader(self.template_dir),
                autoescape=select_autoescape(["html", "xml"]),
            )
            # Add custom filters for tag functionality
            self.jinja_env.filters["tag_url"] = self.tag_url_filter
            self.jinja_env.filters["tag_count"] = self.tag_count_filter
            self.jinja_env.filters["popular_tags"] = self.popular_tags_filter
            self.jinja_env.filters["related_posts"] = self.related_posts_filter
        else:
            self.jinja_env = None
            print(
                "❌ Jinja2 is not available. Templating will be basic string replacement."
            )

    def tag_url_filter(self, tag_name: str) -> str:
        """Generate URL for a tag page"""
        tag_slug = self.slugify_tag(tag_name)
        return f"/tags/{tag_slug}/"

    def tag_count_filter(self, tag_name: str) -> int:
        """Get the count of posts for a tag"""
        return self.tag_counts.get(tag_name, 0)

    def popular_tags_filter(self, limit: int = 10) -> List[Dict]:
        """Get most popular tags with their counts"""
        sorted_tags = sorted(self.tag_counts.items(), key=lambda x: x[1], reverse=True)
        return [
            {"name": tag, "count": count, "url": self.tag_url_filter(tag)}
            for tag, count in sorted_tags[:limit]
        ]

    def related_posts_filter(self, post: Dict, limit: int = 5) -> List[Dict]:
        """Find related posts based on shared tags"""
        if "tags" not in post or not post["tags"]:
            return []

        related_scores = defaultdict(int)
        for tag in post["tags"]:
            for related_post in self.tags[tag]:
                if related_post["url"] != post["url"]:
                    related_scores[related_post["url"]] += 1

        # Sort by score and return top posts
        related_posts = []
        for url, score in sorted(
            related_scores.items(), key=lambda x: x[1], reverse=True
        )[:limit]:
            related_post = next((p for p in self.posts if p["url"] == url), None)
            if related_post:
                related_posts.append(related_post)

        return related_posts

    def slugify_tag(self, tag_name: str) -> str:
        """Convert tag name to URL-friendly slug"""
        slug = tag_name.lower()
        slug = re.sub(r"[^a-z0-9\-_]", "-", slug)
        slug = re.sub(r"-+", "-", slug)
        slug = slug.strip("-")
        return slug

    def parse_frontmatter(self, file_path: Path) -> Optional[Dict]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            if PARSER_TYPE == "frontmatter":
                if hasattr(frontmatter, "loads"):
                    post = frontmatter.loads(content)
                elif hasattr(frontmatter, "load"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        post = frontmatter.load(f)
                else:
                    return self.manual_frontmatter_parse(content, file_path)
            else:
                post = frontmatter.loads(content)

            metadata = dict(post.metadata) if hasattr(post, "metadata") else {}
            body = post.content if hasattr(post, "content") else str(post)

            return {"metadata": metadata, "content": body, "file_path": file_path}

        except Exception as e:
            print(f"❌ Error parsing {file_path}: {e}")
            return self.manual_frontmatter_parse_from_file(file_path)

    def manual_frontmatter_parse_from_file(self, file_path: Path) -> Optional[Dict]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return self.manual_frontmatter_parse(content, file_path)
        except Exception as e:
            print(f"❌ Manual parsing failed for {file_path}: {e}")
            return None

    def manual_frontmatter_parse(self, content: str, file_path: Path) -> Optional[Dict]:
        if not content.startswith("---"):
            return {
                "metadata": {"title": file_path.stem.replace("-", " ").title()},
                "content": content,
                "file_path": file_path,
            }

        try:
            parts = content.split("---", 2)
            if len(parts) < 3:
                return None

            frontmatter_str = parts[1].strip()
            body = parts[2].strip()

            metadata = {}
            for line in frontmatter_str.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")

                    if value.startswith("[") and value.endswith("]"):
                        value = value[1:-1]
                        value = [
                            tag.strip().strip("\"'")
                            for tag in value.split(",")
                            if tag.strip()
                        ]
                    elif "," in value and key.lower() in ["tags"]:
                        value = [
                            tag.strip().strip("\"'")
                            for tag in value.split(",")
                            if tag.strip()
                        ]

                    metadata[key] = value

            return {"metadata": metadata, "content": body, "file_path": file_path}
        except Exception as e:
            print(f"❌ Manual parsing error for {file_path}: {e}")
            return None

    def extract_date_from_filename(self, filename: str) -> Optional[datetime]:
        match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
        if match:
            try:
                return datetime.strptime(match.group(1), "%Y-%m-%d")
            except ValueError:
                pass
        return None

    def load_template(self, template_name: str):
        if self.jinja_env:
            try:
                return self.jinja_env.get_template(template_name)
            except Exception as e:
                print(f"⚠️  Jinja2 failed to load template {template_name}: {e}")

        print(
            f"⚠️  Template {template_name} not found or Jinja2 failed, using basic template"
        )
        if template_name == "post.html":
            return """<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/mun.css" />
</head>
<body>
    <div class="wrapper-masthead">
      <div class="container">
        <header class="masthead clearfix">
          <div class="site-info">
            <h1 class="site-name"><a href="/">Encyclopedia Muneerica</a></h1>
            <p class="site-description">A YungMun Joint</p>
          </div>
          <nav>
            <a href="/">Posts</a>
            <a href="/archive.html">Archive</a>
            <a href="/tags/">Tags</a>
            <a href="/rss.xml">RSS</a>
          </nav>
        </header>
      </div>
    </div>
    <div id="main" role="main" class="container">
        <article class="post">
            <h1>{{ title }}</h1>
            <div class="post-meta">
                <small>{{ date }}
                {% if tags %} [Tags: 
                    {% for tag in tags %}
                      <a href="{{ tag | tag_url }}">{{ tag }}</a>{% if not loop.last %}, {% endif %}
                    {% endfor %}
                ]{% endif %}
                </small>
            </div>
            <div class="post-content">{{ content }}</div>

            {% if tags %}
            <div class="post-tags">
                <h4>Tags:</h4>
                {% for tag in tags %}
                <a href="{{ tag | tag_url }}" class="tag-link">{{ tag }}</a>
                {% endfor %}
            </div>
            {% endif %}

            <!-- Post Navigation -->
            <nav class="post-navigation">
                <div class="nav-links">
                    {% if prev_post %}
                    <div class="nav-previous">
                        <a href="/{{ prev_post.url }}" rel="prev">
                            <span class="nav-subtitle">← Previous Post</span>
                            <span class="nav-title">{{ prev_post.title }}</span>
                        </a>
                    </div>
                    {% endif %}

                    {% if next_post %}
                    <div class="nav-next">
                        <a href="/{{ next_post.url }}" rel="next">
                            <span class="nav-subtitle">Next Post →</span>
                            <span class="nav-title">{{ next_post.title }}</span>
                        </a>
                    </div>
                    {% endif %}
                </div>
            </nav>

            {% if related_posts %}
            <div class="related-posts">
                <h4>Related Posts:</h4>
                <ul>
                {% for related in related_posts %}
                    <li><a href="/{{ related.url }}">{{ related.title }}</a></li>
                {% endfor %}
                </ul>
            </div>
            {% endif %}
        </article>
    </div>
    <div class="wrapper-footer">
      <div class="container">
        <footer class="footer">
          <p>If you want to copy anything here, tell me. Chances are, I'll be flattered.</p>
        </footer>
      </div>
    </div>
</body>
</html>"""
        elif template_name == "tag_page.html":
            return """<!DOCTYPE html>
<html>
  <head>
    <title>Tag: {{ tag_name }} - Encyclopedia Muneerica</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/mun.css" />
  </head>
  <body>
    <div class="wrapper-masthead">
      <div class="container">
        <header class="masthead clearfix">
          <div class="site-info">
            <h1 class="site-name"><a href="/">Encyclopedia Muneerica</a></h1>
            <p class="site-description">A YungMun Joint</p>
          </div>
          <nav>
            <a href="/">Posts</a>
            <a href="/archive.html">Archive</a>
            <a href="/tags/">Tags</a>
            <a href="/rss.xml">RSS</a>
          </nav>
        </header>
      </div>
    </div>
    <div id="main" role="main" class="container">
      <h1>Posts tagged "{{ tag_name }}"</h1>
      <p>{{ tag_posts|length }} post(s) found.</p>

      {% for post in tag_posts %}
      <article class="post-preview">
        <h3><a href="/{{ post.url }}">{{ post.title }}</a></h3>
        <div class="post-meta">
          <small>{{ post.date.strftime('%B %d, %Y') if post.date else '' }}
          {% if post.tags %} [Tags: 
            {% for tag in post.tags %}
              <a href="{{ tag | tag_url }}">{{ tag }}</a>{% if not loop.last %}, {% endif %}
            {% endfor %}
          ]{% endif %}
          </small>
        </div>
        <div class="post-excerpt">{{ post.excerpt }}</div>
        <p><a href="/{{ post.url }}" class="read-more">Read More →</a></p>
      </article>
      {% if not loop.last %}<hr>{% endif %}
      {% endfor %}

      <p><a href="/tags/">← Back to All Tags</a></p>
    </div>
    <div class="wrapper-footer">
      <div class="container">
        <footer class="footer">
          <p>If you want to copy anything here, tell me. Chances are, I'll be flattered.</p>
        </footer>
      </div>
    </div>
  </body>
</html>"""
        elif template_name == "tag_index.html":
            return """<!DOCTYPE html>
<html>
  <head>
    <title>All Tags - Encyclopedia Muneerica</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/mun.css" />
  </head>
  <body>
    <div class="wrapper-masthead">
      <div class="container">
        <header class="masthead clearfix">
          <div class="site-info">
            <h1 class="site-name"><a href="/">Encyclopedia Muneerica</a></h1>
            <p class="site-description">A YungMun Joint</p>
          </div>
          <nav>
            <a href="/">Posts</a>
            <a href="/archive.html">Archive</a>
            <a href="/tags/">Tags</a>
            <a href="/rss.xml">RSS</a>
          </nav>
        </header>
      </div>
    </div>
    <div id="main" role="main" class="container">
      <h1>All Tags</h1>

      <div class="tag-cloud">
        {% for tag_info in all_tags %}
        <a href="{{ tag_info.url }}" class="tag tag-size-{{ tag_info.size_class }}">
          {{ tag_info.name }} ({{ tag_info.count }})
        </a>
        {% endfor %}
      </div>

      <h2>Popular Tags</h2>
      <ul class="popular-tags">
        {% for tag_info in popular_tags %}
        <li>
          <a href="{{ tag_info.url }}">{{ tag_info.name }}</a> 
          <span class="tag-count">({{ tag_info.count }} posts)</span>
        </li>
        {% endfor %}
      </ul>

      <p><a href="/">← Back to Home</a></p>
    </div>
    <div class="wrapper-footer">
      <div class="container">
        <footer class="footer">
          <p>If you want to copy anything here, tell me. Chances are, I'll be flattered.</p>
        </footer>
      </div>
    </div>
  </body>
</html>"""
        else:
            return """<!DOCTYPE html>
<html>
  <head>
    <title>{{ page_title or title }}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/mun.css" />
    <link rel="alternate" type="application/rss+xml" title="Encyclopedia Muneerica" href="/rss.xml" />
  </head>
  <body>
    <div class="wrapper-masthead">
      <div class="container">
        <header class="masthead clearfix">
          <div class="site-info">
            <h1 class="site-name"><a href="/">Encyclopedia Muneerica</a></h1>
            <p class="site-description">A YungMun Joint</p>
          </div>
          <nav>
            <a href="/">Posts</a>
            <a href="/archive.html">Archive</a>
            <a href="/tags/">Tags</a>
            <a href="/cities/">Cities</a>
            <a href="/newsletter/">Newsletter</a>
            <a href="/strange_researches/">Strange Researches</a>
            <a href="/rss.xml">RSS</a>
          </nav>
        </header>
      </div>
    </div>
    <div id="main" role="main" class="container">
      {{ content }}
      {% if journal_posts %}
      <h2>Recent Entries</h2>
      {% for post in journal_posts %}
      <article class="post-preview">
        <h3><a href="/{{ post.url }}">{{ post.title }}</a></h3>
        <div class="post-meta">
          <small>{{ post.date.strftime('%B %d, %Y') if post.date else '' }}
          {% if post.tags %} [Tags: 
            {% for tag in post.tags %}
              <a href="{{ tag | tag_url }}">{{ tag }}</a>{% if not loop.last %}, {% endif %}
            {% endfor %}
          ]{% endif %}
          </small>
        </div>
        <div class="post-excerpt">{{ post.excerpt }}</div>
        <p><a href="/{{ post.url }}" class="read-more">Read More →</a></p>
      </article>
      {% if not loop.last %}<hr>{% endif %}
      {% endfor %}
      {% else %}
      <h2>No Journal Entries Found</h2>
      <p>No posts found.</p>
      {% endif %}

      <!-- Popular Tags Sidebar -->
      <div class="sidebar">
        <h3>Popular Tags</h3>
        <div class="tag-cloud">
          {% for tag_info in [] | popular_tags(10) %}
          <a href="{{ tag_info.url }}" class="tag">{{ tag_info.name }} ({{ tag_info.count }})</a>
          {% endfor %}
        </div>
      </div>
    </div>
    <div class="wrapper-footer">
      <div class="container">
        <footer class="footer">
          <p>If you want to copy anything here, tell me. Chances are, I'll be flattered.</p>
        </footer>
      </div>
    </div>
  </body>
</html>"""

    def render_template(self, template, **kwargs) -> str:
        if self.jinja_env and hasattr(template, "render"):
            return template.render(**kwargs)
        else:
            result = template if isinstance(template, str) else ""

            # Handle navigation links for non-Jinja2 fallback
            prev_post = kwargs.get("prev_post")
            next_post = kwargs.get("next_post")

            if prev_post:
                prev_nav = f"""<div class="nav-previous">
                    <a href="/{prev_post["url"]}" rel="prev">
                        <span class="nav-subtitle">← Previous Post</span>
                        <span class="nav-title">{prev_post["title"]}</span>
                    </a>
                </div>"""
            else:
                prev_nav = ""

            if next_post:
                next_nav = f"""<div class="nav-next">
                    <a href="/{next_post["url"]}" rel="next">
                        <span class="nav-subtitle">Next Post →</span>
                        <span class="nav-title">{next_post["title"]}</span>
                    </a>
                </div>"""
            else:
                next_nav = ""

            # Replace navigation placeholders
            result = result.replace("{{ prev_nav }}", prev_nav)
            result = result.replace("{{ next_nav }}", next_nav)

            # Handle other template variables
            for key, value in kwargs.items():
                if key in ["prev_post", "next_post"]:
                    continue  # Already handled above

                placeholder = f"{{{{ {key} }}}}"
                if isinstance(value, list):
                    result = result.replace(
                        placeholder, ", ".join(str(v) for v in value)
                    )
                else:
                    result = result.replace(
                        placeholder, str(value) if value is not None else ""
                    )

            # Clean up remaining Jinja2 syntax
            result = re.sub(r"{%.*?%}", "", result, flags=re.DOTALL)
            result = re.sub(r"{{.*?}}", "", result)
            return result

    def convert_markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown to HTML using Mistune"""
        if MISTUNE_AVAILABLE and self.markdown_parser:
            try:
                return self.markdown_parser(markdown_text)
            except Exception as e:
                print(
                    f"⚠️  Mistune conversion failed: {e}, falling back to basic conversion"
                )
                return self.basic_markdown_conversion(markdown_text)
        else:
            print("⚠️  Mistune not available, using basic conversion for content.")
            return self.basic_markdown_conversion(markdown_text)

    def basic_markdown_conversion(self, markdown_text: str) -> str:
        """Basic markdown conversion fallback"""
        html = markdown_text

        # Headers
        html = re.sub(r"^# (.*$)", r"<h1>\1</h1>", html, flags=re.MULTILINE)
        html = re.sub(r"^## (.*$)", r"<h2>\1</h2>", html, flags=re.MULTILINE)
        html = re.sub(r"^### (.*$)", r"<h3>\1</h3>", html, flags=re.MULTILINE)
        html = re.sub(r"^#### (.*$)", r"<h4>\1</h4>", html, flags=re.MULTILINE)
        html = re.sub(r"^##### (.*$)", r"<h5>\1</h5>", html, flags=re.MULTILINE)
        html = re.sub(r"^###### (.*$)", r"<h6>\1</h6>", html, flags=re.MULTILINE)

        # Blockquotes
        html = re.sub(
            r"^> (.*$)", r"<blockquote>\1</blockquote>", html, flags=re.MULTILINE
        )

        # Bold and italic
        html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
        html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html)

        # Code blocks (basic)
        html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

        # Links
        html = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', html)

        # Images
        html = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', html)

        # Lists (basic)
        html = re.sub(r"^\- (.*$)", r"<li>\1</li>", html, flags=re.MULTILINE)
        html = re.sub(r"^\* (.*$)", r"<li>\1</li>", html, flags=re.MULTILINE)
        html = re.sub(r"^\+ (.*$)", r"<li>\1</li>", html, flags=re.MULTILINE)

        # Wrap consecutive <li> elements in <ul>
        html = re.sub(
            r"(<li>.*?</li>)(?:\n<li>.*?</li>)*",
            r"<ul>\g<0></ul>",
            html,
            flags=re.DOTALL,
        )

        # Paragraphs
        html = html.replace("\n\n", "</p><p>")
        html = "<p>" + html + "</p>"
        html = re.sub(r"<p></p>", "", html)
        html = re.sub(r"<p>(<h[1-6]>.*?</h[1-6]>)</p>", r"\1", html)
        html = re.sub(r"<p>(<blockquote>.*?</blockquote>)</p>", r"\1", html)
        html = re.sub(r"<p>(<ul>.*?</ul>)</p>", r"\1", html, flags=re.DOTALL)

        return html

    def generate_excerpt(self, markdown_text: str, length: int = 200) -> str:
        """Generate an excerpt from markdown text"""
        # Remove code blocks
        text = re.sub(r"```.*?```", "", markdown_text, flags=re.DOTALL)
        # Remove blockquotes
        text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
        text = text.replace(": >", "")
        # Remove list items
        text = re.sub(r"^\s*[-*+]\s+.*$", "", text, flags=re.MULTILINE)
        # Remove headers
        text = re.sub(r"^#+\s+", "", text, flags=re.MULTILINE)
        # Remove markdown formatting
        text = re.sub(r"[_*`]", "", text)
        # Remove images
        text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
        # Remove links but keep text
        text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
        # Clean up whitespace
        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) > length:
            return text[:length].rsplit(" ", 1)[0] + "..."
        return text

    def collect_posts(self):
        if not self.content_dir.exists():
            print(f"❌ Content directory {self.content_dir} not found!")
            return

        markdown_files = list(self.content_dir.rglob("*.md"))
        print(f"📄 Found {len(markdown_files)} markdown files")

        # Initialize collections dictionary
        self.collections = {}
        self.tags = defaultdict(list)
        self.tag_counts = defaultdict(int)

        for file_path in markdown_files:
            print(f"Processing: {file_path.name}")
            parsed = self.parse_frontmatter(file_path)

            if parsed:
                metadata = parsed["metadata"]
                content = parsed["content"]

                file_date = self.extract_date_from_filename(file_path.name)
                post_date = metadata.get("date", file_date)

                if isinstance(post_date, str):
                    try:
                        post_date = datetime.strptime(post_date, "%Y-%m-%d")
                    except ValueError:
                        post_date = file_date or datetime.now()
                elif isinstance(post_date, date) and not isinstance(
                    post_date, datetime
                ):
                    # Convert date to datetime
                    post_date = datetime.combine(post_date, datetime.min.time())

                tags = metadata.get("tags", [])
                if isinstance(tags, str):
                    tags = tags.strip("[]")
                    tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
                elif not isinstance(tags, list):
                    tags = []

                # Normalize tags (remove duplicates, trim whitespace)
                tags = list(set(tag.strip() for tag in tags if tag.strip()))

                # Determine collection based on subfolder
                relative_path = file_path.relative_to(self.content_dir)
                collection_name = (
                    relative_path.parts[0] if len(relative_path.parts) > 1 else "posts"
                )

                post = {
                    "title": metadata.get(
                        "title", file_path.stem.replace("-", " ").title()
                    ),
                    "date": post_date,
                    "content": content,
                    "metadata": metadata,
                    "file_path": file_path,
                    "url": self.generate_post_url(file_path, collection_name),
                    "tags": tags,
                    "excerpt": self.generate_excerpt(content),
                    "collection": collection_name,
                }

                # Add to main posts list
                self.posts.append(post)

                # Add to collection
                if collection_name not in self.collections:
                    self.collections[collection_name] = []
                self.collections[collection_name].append(post)

                # Process tags
                for tag in tags:
                    self.tags[tag].append(post)
                    self.tag_counts[tag] += 1

                print(
                    f"✅ Successfully parsed: {post['title']} (collection: {collection_name}, tags: {tags})"
                )
            else:
                print(f"❌ Failed to parse: {file_path.name}")

        # Print collection and tag summary
        print("\n📚 Collections found:")
        for collection_name, posts in self.collections.items():
            print(f"  - {collection_name}: {len(posts)} posts")

        print(f"\n🏷️  Tags found: {len(self.tags)} unique tags")
        for tag, count in sorted(
            self.tag_counts.items(), key=lambda x: x[1], reverse=True
        )[:10]:
            print(f"  - {tag}: {count} posts")
        print()

    def generate_post_url(self, file_path: Path, collection_name: str = "posts") -> str:
        name = file_path.stem
        name = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)

        if collection_name == "posts":
            return f"posts/{name}.html"
        else:
            return f"{collection_name}/{name}.html"

    def list_tags(self, tags):
        # Return tags as list of strings
        return [str(tag) for tag in tags]

    def generate_tag_pages(self):
        """Generate individual tag pages"""
        tags_dir = self.output_dir / "tags"
        tags_dir.mkdir(parents=True, exist_ok=True)

        tag_template = self.load_template("tag_page.html")
        min_posts = self.site_config["tag_config"].get("min_posts", 1)

        generated_count = 0
        for tag_name, tag_posts in self.tags.items():
            if len(tag_posts) < min_posts:
                continue

            # Sort posts by date (newest first)
            sorted_posts = sorted(
                tag_posts, key=lambda x: x["date"] or datetime.min, reverse=True
            )

            # Create tag page
            tag_slug = self.slugify_tag(tag_name)
            tag_dir = tags_dir / tag_slug
            tag_dir.mkdir(parents=True, exist_ok=True)

            rendered = self.render_template(
                tag_template,
                tag_name=tag_name,
                tag_posts=sorted_posts,
                tag_count=len(sorted_posts),
                page_title=f"Tag: {tag_name}",
                site_config=self.site_config,
            )

            tag_page_path = tag_dir / "index.html"
            with open(tag_page_path, "w", encoding="utf-8") as f:
                f.write(rendered)

            generated_count += 1
            print(
                f"✅ Generated tag page: /tags/{tag_slug}/ ({len(sorted_posts)} posts)"
            )

        print(f"📊 Generated {generated_count} tag pages")

    def generate_tag_index(self):
        """Generate main tags index page"""
        tags_dir = self.output_dir / "tags"
        tags_dir.mkdir(parents=True, exist_ok=True)

        tag_index_template = self.load_template("tag_index.html")

        # Calculate tag size classes for tag cloud
        max_count = max(self.tag_counts.values()) if self.tag_counts else 1
        min_count = min(self.tag_counts.values()) if self.tag_counts else 1

        all_tags = []
        for tag_name, count in sorted(self.tag_counts.items()):
            # Calculate size class (1-5) based on post count
            if max_count == min_count:
                size_class = 3
            else:
                size_class = int(1 + 4 * (count - min_count) / (max_count - min_count))

            all_tags.append(
                {
                    "name": tag_name,
                    "count": count,
                    "url": self.tag_url_filter(tag_name),
                    "size_class": size_class,
                }
            )

        # Sort alphabetically for the main list
        all_tags.sort(key=lambda x: x["name"].lower())

        # Get popular tags (top 10)
        popular_tags = sorted(
            [
                {"name": tag, "count": count, "url": self.tag_url_filter(tag)}
                for tag, count in self.tag_counts.items()
            ],
            key=lambda x: x["count"],
            reverse=True,
        )[:10]

        rendered = self.render_template(
            tag_index_template,
            all_tags=all_tags,
            popular_tags=popular_tags,
            total_tags=len(self.tag_counts),
            page_title="All Tags",
            site_config=self.site_config,
        )

        tag_index_path = tags_dir / "index.html"
        with open(tag_index_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        print(f"✅ Generated tag index: /tags/ ({len(self.tag_counts)} tags)")

    def generate_collection_pages(self):
        """Generate collection index pages"""
        for collection_name, posts in self.collections.items():
            if collection_name == "posts":
                continue  # Skip main posts collection

            collection_dir = self.output_dir / collection_name
            collection_dir.mkdir(parents=True, exist_ok=True)

            # Sort posts by date (newest first)
            sorted_posts = sorted(
                posts, key=lambda x: x["date"] or datetime(1900, 1, 1), reverse=True
            )

            # Use default template for collection pages
            template = self.load_template("default.html")

            rendered = self.render_template(
                template,
                title=f"{collection_name.title()} Collection",
                page_title=f"{collection_name.title()} - Encyclopedia Muneerica",
                journal_posts=sorted_posts,
                content=f"<h1>{collection_name.title()}</h1><p>All posts in the {collection_name} collection.</p>",
                site_config=self.site_config,
            )

            collection_index_path = collection_dir / "index.html"
            with open(collection_index_path, "w", encoding="utf-8") as f:
                f.write(rendered)

            print(
                f"✅ Generated collection page: /{collection_name}/ ({len(posts)} posts)"
            )

    def generate_posts(self):
        """Generate individual post pages"""
        # Sort all posts chronologically for navigation
        sorted_posts = sorted(
            self.posts, key=lambda x: x["date"] or datetime(1900, 1, 1)
        )

        for i, post in enumerate(sorted_posts):
            post_url = post["url"]
            post_path = self.output_dir / post_url
            post_path.parent.mkdir(parents=True, exist_ok=True)

            # Convert markdown to HTML
            html_content = self.convert_markdown_to_html(post["content"])

            # Load post template
            template = self.load_template("post.html")

            # Get related posts
            related_posts = self.related_posts_filter(post, limit=5)

            # Get previous and next posts
            prev_post = sorted_posts[i - 1] if i > 0 else None
            next_post = sorted_posts[i + 1] if i < len(sorted_posts) - 1 else None

            rendered = self.render_template(
                template,
                title=post["title"],
                content=html_content,
                date=post["date"].strftime("%B %d, %Y") if post["date"] else "",
                tags=post["tags"],
                related_posts=related_posts,
                prev_post=prev_post,
                next_post=next_post,
                site_config=self.site_config,
                post=post,
            )

            with open(post_path, "w", encoding="utf-8") as f:
                f.write(rendered)

            print(f"✅ Generated post: {post['title']} -> {post_url}")

    def generate_index(self):
        """Generate the main index page"""
        # Sort posts by date (newest first)
        sorted_posts = sorted(
            [p for p in self.posts if p["collection"] == "posts"],
            key=lambda x: x["date"] or datetime(1900, 1, 1),
            reverse=True,
        )

        # Take only the most recent posts for the homepage
        recent_posts = sorted_posts[:10]

        template = self.load_template("index.html")
        if not template:
            template = self.load_template("default.html")

        rendered = self.render_template(
            template,
            title="Encyclopedia Muneerica",
            page_title="Encyclopedia Muneerica - A YungMun Joint",
            journal_posts=recent_posts,
            content="<h1>Welcome to Encyclopedia Muneerica</h1><p>A YungMun Joint - exploring ideas, places, and everything in between.</p>",
            site_config=self.site_config,
        )

        index_path = self.output_dir / "index.html"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        print(f"✅ Generated index page with {len(recent_posts)} recent posts")

    def generate_archive(self):
        """Generate archive page with all posts"""
        # Group posts by year
        posts_by_year = defaultdict(list)
        for post in self.posts:
            year = post["date"].year if post["date"] else "Unknown"
            posts_by_year[year].append(post)

        # Sort posts within each year
        for year in posts_by_year:
            posts_by_year[year].sort(
                key=lambda x: x["date"] or datetime(1900, 1, 1), reverse=True
            )

        # Sort years (newest first)
        sorted_years = sorted(posts_by_year.keys(), reverse=True)

        template = self.load_template("archive.html")
        if not template:
            template = self.load_template("default.html")

        archive_content = "<h1>Archive</h1>\n"
        for year in sorted_years:
            archive_content += f"<h2>{year}</h2>\n<ul>\n"
            for post in posts_by_year[year]:
                date_str = post["date"].strftime("%B %d") if post["date"] else ""
                archive_content += f'<li><a href="/{post["url"]}">{post["title"]}</a> <small>({date_str})</small></li>\n'
            archive_content += "</ul>\n"

        rendered = self.render_template(
            template,
            title="Archive",
            page_title="Archive - Encyclopedia Muneerica",
            content=archive_content,
            site_config=self.site_config,
        )

        archive_path = self.output_dir / "archive.html"
        with open(archive_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        print(f"✅ Generated archive page with {len(self.posts)} posts")

    def generate_rss(self):
        """Generate RSS feed"""
        # Sort posts by date (newest first)
        sorted_posts = sorted(
            self.posts, key=lambda x: x["date"] or datetime(1900, 1, 1), reverse=True
        )[:20]  # Only include latest 20 posts

        rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
    <title>{self.site_config["name"]}</title>
    <description>{self.site_config["description"]}</description>
    <link>{self.site_config["url"]}</link>
    <lastBuildDate>{datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")}</lastBuildDate>
    <generator>Enhanced SSG v3.0</generator>
"""

        for post in sorted_posts:
            # Convert markdown to HTML for RSS
            html_content = self.convert_markdown_to_html(post["content"])
            pub_date = (
                post["date"].strftime("%a, %d %b %Y %H:%M:%S GMT")
                if post["date"]
                else ""
            )

            rss_content += f"""
    <item>
        <title>{post["title"]}</title>
        <description><![CDATA[{html_content}]]></description>
        <link>{self.site_config["url"]}/{post["url"]}</link>
        <guid>{self.site_config["url"]}/{post["url"]}</guid>
        <pubDate>{pub_date}</pubDate>
"""
            if post["tags"]:
                for tag in post["tags"]:
                    rss_content += f"        <category>{tag}</category>\n"

            rss_content += "    </item>\n"

        rss_content += """</channel>
</rss>"""

        rss_path = self.output_dir / "rss.xml"
        with open(rss_path, "w", encoding="utf-8") as f:
            f.write(rss_content)

        print(f"✅ Generated RSS feed with {len(sorted_posts)} posts")

    def copy_static_files(self):
        """Copy static files to output directory"""
        static_dir = Path("static")
        if static_dir.exists():
            output_static_dir = self.output_dir / "static"
            if output_static_dir.exists():
                shutil.rmtree(output_static_dir)
            shutil.copytree(static_dir, output_static_dir)
            print(f"✅ Copied static files to {output_static_dir}")

    def generate_site(self):
        """Generate the complete site"""
        print("🚀 Starting site generation...")

        # Move existing output directory to trash
        if self.output_dir.exists():
            try:
                # Try using send2trash if available
                try:
                    import send2trash

                    send2trash.send2trash(str(self.output_dir))
                    print(f"🗑️  Moved existing {self.output_dir} to trash")
                except ImportError:
                    # Fallback to creating a backup with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    backup_name = f"{self.output_dir.name}_backup_{timestamp}"
                    backup_path = self.output_dir.parent / backup_name
                    shutil.move(str(self.output_dir), str(backup_path))
                    print(f"📦 Moved existing {self.output_dir} to {backup_path}")
            except Exception as e:
                print(f"⚠️  Could not move to trash, removing directory: {e}")
                shutil.rmtree(self.output_dir)

        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Collect all posts
        self.collect_posts()

        if not self.posts:
            print("❌ No posts found! Check your content directory.")
            return

        # Generate all pages
        self.generate_posts()
        self.generate_index()
        self.generate_archive()
        self.generate_collection_pages()
        self.generate_tag_pages()
        self.generate_tag_index()
        self.generate_rss()
        self.copy_static_files()

        print("\n🎉 Site generation complete!")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📄 Generated {len(self.posts)} posts")
        print(f"🏷️  Generated {len(self.tag_counts)} tag pages")
        print(f"📚 Generated {len(self.collections)} collections")


def main():
    """Main function to run the site generator"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Enhanced Static Site Generator with Tag Support"
    )
    parser.add_argument(
        "--content", default="content", help="Content directory (default: content)"
    )
    parser.add_argument(
        "--output", default="site", help="Output directory (default: site)"
    )
    parser.add_argument(
        "--templates",
        default="templates",
        help="Templates directory (default: templates)",
    )
    parser.add_argument(
        "--serve", action="store_true", help="Serve the site locally after generation"
    )
    parser.add_argument(
        "--port", type=int, default=8000, help="Port for local server (default: 8000)"
    )

    args = parser.parse_args()

    # Create and run the generator
    generator = SSGGenerator(
        content_dir=args.content, output_dir=args.output, template_dir=args.templates
    )

    try:
        generator.generate_site()

        if args.serve:
            import http.server
            import socketserver
            import os

            # Change to output directory
            os.chdir(args.output)

            # Start server
            Handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", args.port), Handler) as httpd:
                print(f"🌐 Serving at http://localhost:{args.port}")
                print("Press Ctrl+C to stop the server")
                try:
                    httpd.serve_forever()
                except KeyboardInterrupt:
                    print("\n👋 Server stopped")

    except Exception as e:
        print(f"❌ Error during site generation: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()

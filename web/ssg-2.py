#!/usr/bin/env python3
"""
Enhanced Static Site Generator with Jekyll-like configuration
Matches Encyclopedia Muneerica Jekyll setup
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import re
import math

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
    from jinja2 import Environment, FileSystemLoader, Template

    JINJA2_AVAILABLE = True
except ImportError:
    print("Jinja2 not found. Installing...")
    import subprocess

    subprocess.run(["pip", "install", "Jinja2"])
    from jinja2 import Environment, FileSystemLoader, Template

    JINJA2_AVAILABLE = True


class SSGGenerator:
    def __init__(
        self,
        content_dir: str = "content",
        output_dir: str = "site",
        template_dir: str = "templates",
        assets_dir: str = "assets",
    ):
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.template_dir = Path(template_dir)
        self.assets_dir = Path(assets_dir)
        self.posts = []

        # Site configuration matching Jekyll _config.yml
        self.site_config = {
            "name": "Encyclopedia Muneerica",
            "description": "A YungMun Joint",
            "avatar": "https://raw.githubusercontent.com/muneer78/muneer78.github.io/master/images/synthwavehokusai.jpg",
            "baseurl": "",
            "url": "",
            "github": "muneer78",
            "twitter": "reenum",
            "pagination": {
                "enabled": True,
                "per_page": 10,
                "sort_field": "date",
                "sort_reverse": True,
            },
            "navigation": [
                {"name": "Posts", "url": "/"},
                {"name": "Archive", "url": "/archive"},
                {"name": "Cities", "url": "/cities"},
                {"name": "Newsletter", "url": "/newsletter"},
                {"name": "Strange Researches", "url": "/strange_researches"},
            ],
        }

        # Set up Jinja2 environment
        if JINJA2_AVAILABLE and self.template_dir.exists():
            self.jinja_env = Environment(
                loader=FileSystemLoader(str(self.template_dir))
            )
        else:
            self.jinja_env = None

    def parse_frontmatter(self, file_path: Path) -> Optional[Dict]:
        """Parse frontmatter from markdown file with better error handling"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Check if file is empty
            if not content.strip():
                print(f"⚠️  Empty file: {file_path}")
                return None

            # Try different parsing methods
            if PARSER_TYPE == "frontmatter":
                if hasattr(frontmatter, "loads"):
                    post = frontmatter.loads(content)
                elif hasattr(frontmatter, "load"):
                    with open(file_path, "r", encoding="utf-8") as f:
                        post = frontmatter.load(f)
                else:
                    # Manual parsing as fallback
                    return self.manual_frontmatter_parse(content, file_path)
            else:
                post = frontmatter.loads(content)

            # Extract metadata and content
            metadata = dict(post.metadata) if hasattr(post, "metadata") else {}
            body = post.content if hasattr(post, "content") else str(post)

            return {"metadata": metadata, "content": body, "file_path": file_path}

        except UnicodeDecodeError as e:
            print(f"❌ Unicode error in {file_path}: {e}")
            return None
        except Exception as e:
            print(f"❌ Error parsing {file_path}: {e}")
            # Try manual parsing as fallback
            return self.manual_frontmatter_parse_from_file(file_path)

    def manual_frontmatter_parse_from_file(self, file_path: Path) -> Optional[Dict]:
        """Manual frontmatter parsing as fallback"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return self.manual_frontmatter_parse(content, file_path)
        except Exception as e:
            print(f"❌ Manual parsing failed for {file_path}: {e}")
            return None

    def manual_frontmatter_parse(self, content: str, file_path: Path) -> Optional[Dict]:
        """Manual frontmatter parsing"""
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

            # Simple YAML-like parsing
            metadata = {}
            for line in frontmatter_str.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip().strip("\"'")

                    # Handle lists (for tags)
                    if value.startswith("[") and value.endswith("]"):
                        # Parse list: [tag1, tag2, tag3]
                        value = value[1:-1]  # Remove brackets
                        value = [
                            tag.strip().strip("\"'")
                            for tag in value.split(",")
                            if tag.strip()
                        ]
                    elif "," in value and key.lower() in ["tags", "categories"]:
                        # Handle comma-separated values
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
        """Extract date from filename pattern YYYY-MM-DD-title.md"""
        match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
        if match:
            try:
                return datetime.strptime(match.group(1), "%Y-%m-%d")
            except ValueError:
                pass
        return None

    def create_excerpt(self, content: str, lines: int = 6) -> str:
        """Create excerpt from content (first N lines)"""
        # Convert markdown to text for excerpt
        text_content = content

        # Remove markdown headers
        text_content = re.sub(r"^#+\s*", "", text_content, flags=re.MULTILINE)

        # Remove markdown formatting
        text_content = re.sub(r"\*\*(.*?)\*\*", r"\1", text_content)  # Bold
        text_content = re.sub(r"\*(.*?)\*", r"\1", text_content)  # Italic
        text_content = re.sub(r"`(.*?)`", r"\1", text_content)  # Code
        text_content = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", text_content)  # Links

        # Split into lines and take first N lines
        lines_list = [line.strip() for line in text_content.split("\n") if line.strip()]
        excerpt_lines = lines_list[:lines]

        return "\n".join(excerpt_lines)

    def load_template(self, template_name: str) -> str:
        """Load template file"""
        template_path = self.template_dir / template_name
        if template_path.exists():
            with open(template_path, "r", encoding="utf-8") as f:
                return f.read()
        else:
            print(f"⚠️  Template {template_name} not found, using Jekyll-like template")
            if template_name == "default.html":
                return """<!DOCTYPE html>
<html>
  <head>
    <title>{% if page_title %}{{ page_title }} – {% endif %}{{ site.name }} – {{ site.description }}</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" href="/style.css" />
    <link rel="alternate" type="application/rss+xml" title="{{ site.name }} - {{ site.description }}" href="/feed.xml" />
  </head>
  <body>
    <div class="wrapper-masthead">
      <div class="container">
        <header class="masthead clearfix">
          <a href="/" class="site-avatar"><img src="{{ site.avatar }}" /></a>
          <div class="site-info">
            <h1 class="site-name"><a href="/">{{ site.name }}</a></h1>
            <p class="site-description">{{ site.description }}</p>
          </div>
          <nav>
            {% for nav_item in site.navigation %}
            <a href="{{ nav_item.url }}">{{ nav_item.name }}</a>
            {% endfor %}
          </nav>
        </header>
      </div>
    </div>

    <div id="main" role="main" class="container">
      {{ content }}
    </div>

    <div class="wrapper-footer">
      <div class="container">
        <footer class="footer">
          <div class="svg-icons">
            {% if site.github %}<a href="https://github.com/{{ site.github }}">GitHub</a>{% endif %}
            {% if site.twitter %}<a href="https://twitter.com/{{ site.twitter }}">Twitter</a>{% endif %}
            <a href="/feed.xml">RSS</a>
          </div>
        </footer>
      </div>
    </div>
  </body>
</html>"""
            elif template_name == "post.html":
                return """{% extends "default.html" %}
{% block content %}
<article class="post">
  <h1>{{ title }}</h1>
  <div class="entry">
    {{ content }}
  </div>
  <div class="date">
    Written on {{ date }}
  </div>
</article>
{% endblock %}"""
            elif template_name == "archive.html":
                return """{% extends "default.html" %}
{% block content %}
<h1>Archive</h1>
<div class="posts">
  {% for post in posts %}
    {% if not (post.categories contains "strange-researches" or post.categories contains "cities") %}
      <article class="post">
        <a href="{{ post.url }}">{{ post.title }}</a>
        <div class="entry">
          {{ post.excerpt }}
          <a href="{{ post.url }}" class="read-more">Read More</a>
        </div>
      </article>
    {% endif %}
  {% endfor %}
</div>
{% if pagination %}
<div class="pagination">
  {% if pagination.previous_page %}
    <a href="{{ pagination.previous_page_path }}" class="previous">Previous</a>
  {% endif %}
  {% if pagination.next_page %}
    <a href="{{ pagination.next_page_path }}" class="next">Next</a>
  {% endif %}
</div>
{% endif %}
{% endblock %}"""
            else:  # category.html
                return """{% extends "default.html" %}
{% block content %}
<h1>{{ category_title }}</h1>
<div class="posts">
  {{ content }}
</div>
{% endblock %}"""

    def render_template(self, template: str, **kwargs) -> str:
        """Render template with Jinja2 or fallback to simple replacement"""
        # Add site config to template context
        template_context = {"site": self.site_config, **kwargs}

        if self.jinja_env:
            try:
                # Use Jinja2 for proper template rendering
                jinja_template = Template(template)
                return jinja_template.render(**template_context)
            except Exception as e:
                print(
                    f"⚠️  Jinja2 rendering failed: {e}, falling back to simple replacement"
                )

        # Fallback to simple string replacement
        result = template
        for key, value in template_context.items():
            if key == "site":
                # Handle site.property syntax
                for prop, val in value.items():
                    placeholder = f"{{{{ site.{prop} }}}}"
                    result = result.replace(placeholder, str(val))
            else:
                placeholder = f"{{{{ {key} }}}}"
                result = result.replace(placeholder, str(value))

        # Remove unprocessed Jinja2 syntax
        result = re.sub(r"{%.*?%}", "", result)  # Remove {% %} blocks
        result = re.sub(r"{{.*?}}", "", result)  # Remove unprocessed {{ }} variables

        return result

    def convert_markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown to HTML (basic conversion) and rewrite image paths."""
        try:
            import markdown

            html = markdown.markdown(
                markdown_text, extensions=["codehilite", "fenced_code"]
            )
        except ImportError:
            print("⚠️  Markdown library not found, using basic conversion")
            # Enhanced basic markdown conversion
            html = markdown_text

            # Headers
            html = re.sub(r"^# (.*$)", r"<h1>\1</h1>", html, flags=re.MULTILINE)
            html = re.sub(r"^## (.*$)", r"<h2>\1</h2>", html, flags=re.MULTILINE)
            html = re.sub(r"^### (.*$)", r"<h3>\1</h3>", html, flags=re.MULTILINE)
            html = re.sub(r"^#### (.*$)", r"<h4>\1</h4>", html, flags=re.MULTILINE)

            # Links
            html = re.sub(r"\[([^\]]+)\]\(([^\)]+)\)", r'<a href="\2">\1</a>', html)

            # Bold and italic
            html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
            html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html)

            # Code blocks
            html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)

            # Line breaks and paragraphs
            html = re.sub(r"\n\n+", "\n\n", html)  # Normalize multiple newlines
            paragraphs = html.split("\n\n")
            html_paragraphs = []

            for p in paragraphs:
                p = p.strip()
                if p:
                    # Don't wrap headers in <p> tags
                    if not re.match(r"^<h[1-6]>", p):
                        html_paragraphs.append(f"<p>{p}</p>")
                    else:
                        html_paragraphs.append(p)

            html = "\n".join(html_paragraphs)

        # Rewrite image paths
        def rewrite_image_src(match):
            alt_text = match.group(1)
            original_path = match.group(2)
            image_filename = Path(original_path).name
            new_path = f"/{self.assets_dir.name}/{image_filename}"
            return f'<img src="{new_path}" alt="{alt_text}">'

        html = re.sub(r"!\[(.*?)\]\((.*?)\)", rewrite_image_src, html)
        return html

    def collect_posts(self):
        """Collect all markdown files and parse them"""
        if not self.content_dir.exists():
            print(f"❌ Content directory {self.content_dir} not found!")
            return

        markdown_files = list(self.content_dir.rglob("*.md"))
        print(f"📄 Found {len(markdown_files)} markdown files")

        for file_path in markdown_files:
            print(f"Processing: {file_path}")
            parsed = self.parse_frontmatter(file_path)

            if parsed:
                metadata = parsed["metadata"]
                content = parsed["content"]

                # Extract date from filename if not in frontmatter
                file_date = self.extract_date_from_filename(file_path.name)
                post_date = metadata.get("date", file_date)

                if isinstance(post_date, str):
                    try:
                        post_date = datetime.strptime(post_date, "%Y-%m-%d")
                    except ValueError:
                        post_date = file_date

                # Determine category - check metadata first, then folder structure
                category = metadata.get("category", "").lower()
                if not category:
                    relative_path = file_path.relative_to(self.content_dir)
                    if len(relative_path.parts) > 1:
                        category = relative_path.parts[0]
                    else:
                        category = "posts"

                # Handle special Jekyll categories
                if category in ["strange-researches", "cities"]:
                    category = category.replace("-", "_")

                # Extract tags from metadata
                tags = metadata.get("tags", [])
                if isinstance(tags, str):
                    tags = [tag.strip() for tag in tags.split(",")]

                # Create excerpt
                excerpt = self.create_excerpt(content, 6)

                # Generate URL based on Jekyll permalink style
                post_url = self.generate_post_url(file_path, category, post_date)

                # Create post object
                post = {
                    "title": metadata.get(
                        "title", file_path.stem.replace("-", " ").title()
                    ),
                    "date": post_date or datetime.now(),
                    "content": content,
                    "excerpt": excerpt,
                    "metadata": metadata,
                    "file_path": file_path,
                    "url": post_url,
                    "category": category,
                    "categories": [category] if category else [],
                    "tags": tags,
                }

                self.posts.append(post)
                print(
                    f"✅ Successfully parsed: {post['title']} (category: {category}, tags: {tags})"
                )
            else:
                print(f"❌ Failed to parse: {file_path.name}")

    def generate_post_url(self, file_path: Path, category: str, date: datetime) -> str:
        """Generate URL for post based on Jekyll permalink style"""
        # Remove date prefix if present
        name = file_path.stem
        name = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)

        # Convert to URL-friendly format
        name = name.lower().replace(" ", "-")
        name = re.sub(r"[^a-z0-9\-]", "", name)  # Remove special chars
        name = re.sub(r"-+", "-", name)  # Remove multiple dashes
        name = name.strip("-")  # Remove leading/trailing dashes

        # Use Jekyll-style permalink: /:title/
        return f"{name}/"

    def copy_assets_files(self):
        """Copy assets files if they exist"""
        if self.assets_dir.exists():
            assets_output = self.output_dir / self.assets_dir.name
            if assets_output.exists():
                shutil.rmtree(assets_output)
            shutil.copytree(self.assets_dir, assets_output)
            print(f"✅ Copied assets from {self.assets_dir} to {assets_output}")

    def generate_posts(self):
        """Generate individual post HTML files"""
        post_template = self.load_template("post.html")

        for post in self.posts:
            html_content = self.convert_markdown_to_html(post["content"])

            rendered = self.render_template(
                post_template,
                page_title=post["title"],
                title=post["title"],
                date=post["date"].strftime("%B %e, %Y") if post["date"] else "",
                content=html_content,
                category=post["category"],
                tags=post["tags"],
                categories=post["categories"],
            )

            # Create directory structure based on URL
            if post["url"].endswith("/"):
                output_path = self.output_dir / post["url"].strip("/") / "index.html"
            else:
                output_path = self.output_dir / post["url"]

            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered)

            print(f"✅ Generated post: {post['url']}")

    def generate_archive_page(self):
        """Generate archive page with pagination, excluding certain categories"""
        # Sort posts by date (newest first)
        sorted_posts = sorted(
            self.posts, key=lambda x: x["date"] or datetime.min, reverse=True
        )

        # Filter out strange-researches and cities posts (matching Jekyll logic)
        archive_posts = []
        for post in sorted_posts:
            if not (
                "strange-researches" in post["categories"]
                or "cities" in post["categories"]
                or "strange_researches" in post["categories"]
            ):
                archive_posts.append(post)

        # Implement pagination
        per_page = self.site_config["pagination"]["per_page"]
        total_posts = len(archive_posts)
        total_pages = math.ceil(total_posts / per_page) if total_posts > 0 else 1

        # Generate paginated archive pages
        for page_num in range(1, total_pages + 1):
            start_idx = (page_num - 1) * per_page
            end_idx = start_idx + per_page
            page_posts = archive_posts[start_idx:end_idx]

            # Create pagination context
            pagination = {
                "page": page_num,
                "per_page": per_page,
                "posts": len(page_posts),
                "total_posts": total_posts,
                "total_pages": total_pages,
                "previous_page": page_num - 1 if page_num > 1 else None,
                "next_page": page_num + 1 if page_num < total_pages else None,
                "previous_page_path": f"/archive/page{page_num - 1}/"
                if page_num > 2
                else "/archive/"
                if page_num > 1
                else None,
                "next_page_path": f"/archive/page{page_num + 1}/"
                if page_num < total_pages
                else None,
            }

            archive_template = self.load_template("archive.html")
            rendered = self.render_template(
                archive_template,
                page_title="Archive",
                posts=page_posts,
                pagination=pagination,
            )

            # Create archive directory structure
            if page_num == 1:
                archive_path = self.output_dir / "archive" / "index.html"
            else:
                archive_path = (
                    self.output_dir / "archive" / f"page{page_num}" / "index.html"
                )

            archive_path.parent.mkdir(parents=True, exist_ok=True)

            with open(archive_path, "w", encoding="utf-8") as f:
                f.write(rendered)

            print(f"✅ Generated archive page: {page_num}/{total_pages}")

    def generate_category_pages(self):
        """Generate category pages (cities, strange_researches, etc.)"""
        # Sort posts by date (newest first)
        sorted_posts = sorted(
            self.posts, key=lambda x: x["date"] or datetime.min, reverse=True
        )

        # Group posts by category
        categories = {}
        for post in sorted_posts:
            cat = post["category"]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(post)

        category_template = self.load_template("category.html")

        # Generate special category pages
        for category, cat_posts in categories.items():
            if category in ["cities", "strange_researches"]:
                # Build category page content
                content_parts = []
                content_parts.append('<div class="posts">')

                for post in cat_posts:
                    date_str = (
                        post["date"].strftime("%B %e, %Y") if post["date"] else ""
                    )
                    content_parts.append('<article class="post">')
                    content_parts.append(
                        f'<a href="/{post["url"]}">{post["title"]}</a>'
                    )
                    content_parts.append('<div class="entry">')
                    content_parts.append(f"{post['excerpt']}")
                    content_parts.append(
                        f'<a href="/{post["url"]}" class="read-more">Read More</a>'
                    )
                    content_parts.append("</div>")
                    content_parts.append("</article>")

                content_parts.append("</div>")
                content = "\n".join(content_parts)

                # Render category page
                rendered = self.render_template(
                    category_template,
                    page_title=category.replace("_", " ").title(),
                    category_title=category.replace("_", " ").title(),
                    category=category,
                    content=content,
                )

                # Create category directory
                category_dir = self.output_dir / category
                category_dir.mkdir(parents=True, exist_ok=True)

                category_index = category_dir / "index.html"
                with open(category_index, "w", encoding="utf-8") as f:
                    f.write(rendered)

                print(f"✅ Generated category page: /{category}/")

    def generate_index(self):
        """Generate main index page"""
        # Sort posts by date (newest first)
        sorted_posts = sorted(
            self.posts, key=lambda x: x["date"] or datetime.min, reverse=True
        )

        # Get recent posts (all categories for main page)
        recent_posts = sorted_posts[:10]

        # Build index content
        content_parts = []
        content_parts.append('<div class="posts">')

        for post in recent_posts:
            content_parts.append('<article class="post">')
            content_parts.append(
                f'<h1><a href="/{post["url"]}">{post["title"]}</a></h1>'
            )
            content_parts.append('<div class="entry">')
            if post["content"] != post["excerpt"]:
                content_parts.append(f"{post['excerpt']}")
                content_parts.append(
                    f'<a href="/{post["url"]}" class="read-more">Read More</a>'
                )
            else:
                content_parts.append(f"{post['content']}")
            content_parts.append("</div>")
            content_parts.append("</article>")

        content_parts.append("</div>")
        content = "\n".join(content_parts)

        def render_template(self, template: str, **kwargs) -> str:
            """Render template with Jinja2 or fallback to simple replacement"""
            # Add site config to template context
            template_context = {"site": self.site_config, **kwargs}

            if self.jinja_env:
                try:
                    # Use Jinja2 for proper template rendering
                    jinja_template = Template(template)
                    return jinja_template.render(**template_context)
                except Exception as e:
                    print(
                        f"⚠️  Jinja2 rendering failed: {e}, falling back to simple replacement"
                    )

            # Enhanced fallback to simple string replacement
            result = template

            # Handle site object properties
            if "site" in template_context:
                site_data = template_context["site"]
                for prop, val in site_data.items():
                    if isinstance(val, list) and prop == "navigation":
                        # Handle navigation menu
                        nav_html = ""
                        for nav_item in val:
                            nav_html += (
                                f'<a href="{nav_item["url"]}">{nav_item["name"]}</a>'
                            )
                        result = result.replace(
                            "{% for nav_item in site.navigation %}", ""
                        )
                        result = result.replace(
                            '<a href="{{ nav_item.url }}">{{ nav_item.name }}</a>',
                            nav_html,
                        )
                        result = result.replace("{% endfor %}", "")
                    else:
                        placeholder = f"{{{{ site.{prop} }}}}"
                        result = result.replace(placeholder, str(val))

            # Handle other variables
            for key, value in template_context.items():
                if key != "site":
                    placeholder = f"{{{{ {key} }}}}"
                    if isinstance(value, list):
                        # Handle lists (like posts)
                        continue  # Skip list rendering in simple mode
                    else:
                        result = result.replace(
                            placeholder, str(value) if value is not None else ""
                        )

            # Handle conditional blocks
            result = re.sub(
                r"{%\s*if\s+[^%]+\s*%}(.*?){%\s*endif\s*%}",
                r"\1",
                result,
                flags=re.DOTALL,
            )

            # Remove remaining Jinja2 syntax
            result = re.sub(r"{%.*?%}", "", result, flags=re.DOTALL)
            result = re.sub(r"{{.*?}}", "", result)

            return result

        # Write index file
        index_path = self.output_dir / "index.html"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        print(f"✅ Generated: index.html")

    def generate_newsletter_page(self):
        """Generate newsletter page (placeholder)"""
        newsletter_template = self.load_template("default.html")
        content = "<h1>Newsletter</h1><p>Newsletter content coming soon...</p>"

        rendered = self.render_template(
            newsletter_template, page_title="Newsletter", content=content
        )

        newsletter_dir = self.output_dir / "newsletter"
        newsletter_dir.mkdir(parents=True, exist_ok=True)

        with open(newsletter_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(rendered)

        print("✅ Generated newsletter page")

    def generate_rss_feed(self):
        """Generate RSS feed"""
        # Sort posts by date (newest first)
        sorted_posts = sorted(
            self.posts, key=lambda x: x["date"] or datetime.min, reverse=True
        )
        recent_posts = sorted_posts[:20]  # Last 20 posts

        # Get current time in RFC 2822 format
        now = datetime.now()
        build_date = now.strftime("%a, %d %b %Y %H:%M:%S +0000")

        rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
    <rss version="2.0">
    <channel>
        <title>{self.site_config["name"]}</title>
        <description>{self.site_config["description"]}</description>
        <link>{self.site_config["url"]}</link>
        <lastBuildDate>{build_date}</lastBuildDate>
    """

        for post in recent_posts:
            # Escape HTML in content
            description = (
                post["excerpt"]
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )
            title = (
                post["title"]
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

            pub_date = ""
            if post["date"]:
                pub_date = post["date"].strftime("%a, %d %b %Y %H:%M:%S +0000")

            rss_content += f"""    <item>
            <title>{title}</title>
            <link>{self.site_config["url"]}/{post["url"]}</link>
            <description><![CDATA[{post["excerpt"]}]]></description>
            <pubDate>{pub_date}</pubDate>
            <guid>{self.site_config["url"]}/{post["url"]}</guid>
        </item>
    """

        rss_content += """</channel>
    </rss>"""

        with open(self.output_dir / "feed.xml", "w", encoding="utf-8") as f:
            f.write(rss_content)

        print("✅ Generated RSS feed")

    def copy_static_files(self):
        """Copy static files if they exist"""
        static_dir = Path("static")
        if static_dir.exists():
            static_output = self.output_dir / "static"
            if static_output.exists():
                shutil.rmtree(static_output)
            shutil.copytree(static_dir, static_output)
            print("✅ Copied static files")

    def generate(self):
        """Generate the complete site"""
        print("🏗️  Starting site generation...")

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Collect and parse posts
        self.collect_posts()

        if not self.posts:
            print("❌ No posts found! Check your content files.")
            return

        # Generate individual posts
        self.generate_posts()

        # Generate archive page with pagination
        self.generate_archive_page()

        # Generate category pages
        self.generate_category_pages()

        # Generate index page
        self.generate_index()

        # Generate newsletter page
        self.generate_newsletter_page()

        # Generate RSS feed
        self.generate_rss_feed()

        # Copy static files
        self.copy_static_files()

        # Copy assets files
        self.copy_assets_files()

        print(f"🎉 Site generated successfully!")
        print(f"📊 Generated {len(self.posts)} posts")

        # Show summary
        categories = {}
        for post in self.posts:
            cat = post["category"]
            categories[cat] = categories.get(cat, 0) + 1

        if categories:
            print("📂 Posts by category:")
            for category, count in sorted(categories.items()):
                print(f"   • {category}: {count} post{'s' if count != 1 else ''}")

        print(f"🌐 Site available at: {self.output_dir}")
        print("✨ Generation complete!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Enhanced Static Site Generator")
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
        "--assets", default="assets", help="Assets directory (default: assets)"
    )
    parser.add_argument(
        "--clean", action="store_true", help="Clean output directory before generation"
    )

    args = parser.parse_args()

    # Clean output directory if requested
    if args.clean and Path(args.output).exists():
        shutil.rmtree(args.output)
        print(f"🧹 Cleaned output directory: {args.output}")

    # Generate site
    generator = SSGGenerator(
        content_dir=args.content,
        output_dir=args.output,
        template_dir=args.templates,
        assets_dir=args.assets,
    )

    generator.generate()

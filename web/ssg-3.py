#!/usr/bin/env python3
"""
Enhanced Static Site Generator Navigation
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import re

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

# Try to import markdown
try:
    import markdown

    MARKDOWN_AVAILABLE = True
except ImportError:
    print("Markdown library not found. Installing markdown...")
    import subprocess

    subprocess.run(["pip", "install", "markdown"])
    try:
        import markdown

        MARKDOWN_AVAILABLE = True
    except ImportError:
        MARKDOWN_AVAILABLE = False
        print("❌ Failed to install markdown library. Basic conversion will be used.")


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

        # Site configuration (from ssg-2.py)
        self.site_config = {
            "name": "Encyclopedia Muneerica",
            "description": "A YungMun Joint",
            "baseurl": "",
            "url": "",
            "github": "muneer78",
            "twitter": "reenum",
            "navigation": [
                {"name": "Archive", "url": "/archive.html"},
            ],
        }

        # Initialize Jinja2 environment
        if JINJA2_AVAILABLE:
            self.jinja_env = Environment(
                loader=FileSystemLoader(self.template_dir),
                autoescape=select_autoescape(["html", "xml"]),
            )
        else:
            self.jinja_env = None
            print(
                "❌ Jinja2 is not available. Templating will be basic string replacement."
            )

    def parse_frontmatter(self, file_path: Path) -> Optional[Dict]:
        """Parse frontmatter from markdown file with better error handling"""
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
        """Manual frontmatter parsing as fallback"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return self.manual_frontmatter_parse(content, file_path)
        except Exception as e:
            print(f"❌ Manual parsing failed for {file_path}: {e}")
            return None

    def manual_frontmatter_parse(self, content: str, file_path: Path) -> Optional[Dict]:
        """Manual frontmatter parsing with enhanced tag handling"""
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

                    # Handle lists (for tags)
                    if value.startswith("[") and value.endswith("]"):
                        # Parse list: [tag1, tag2, tag3]
                        value = value[1:-1]  # Remove brackets
                        value = [
                            tag.strip().strip("\"'")
                            for tag in value.split(",")
                            if tag.strip()
                        ]
                    elif "," in value and key.lower() in ["tags"]:
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

    def load_template(self, template_name: str):
        """Load template file using Jinja2 or basic fallback"""
        if self.jinja_env:
            try:
                return self.jinja_env.get_template(template_name)
            except Exception as e:
                print(f"⚠️  Jinja2 failed to load template {template_name}: {e}")

        # Fallback to basic string template if Jinja2 is not available or fails
        print(
            f"⚠️  Template {template_name} not found or Jinja2 failed, using basic template"
        )
        if template_name == "post.html":
            return """<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>{{ title }}</h1>
    <div class="meta">{{ date }}</div>
    <div class="content">{{ content }}</div>
    <div class="tags">{{ tags }}</div>
    <p><a href="/">← Back to Home</a></p>
</body>
</html>"""
        else:  # default.html or index.html
            return """<!DOCTYPE html>
<html>
  <head>
    <title>{{ page_title or title }}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/mun.css" />
    <link rel="alternate" type="application/rss+xml" title="Encylopedia Muneerica" href="/rss.xml" />
  </head>

  <body>
    <div class="wrapper-masthead">
      <div class="container">
        <header class="masthead clearfix">
          <div class="site-info">
            <h1 class="site-name"><a href="/">Encylopedia Muneerica</a></h1>
            <p class="site-description">A YungMun Joint</p>
          </div>

          <nav>
            <a href="/">Posts</a>
            <a href="/archive.html">Archive</a>
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
          {% if post.tags %} [Tags: {{ post.tags|join(', ') }}]{% endif %}
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
        """Render template using Jinja2 or basic string replacement"""
        if self.jinja_env and hasattr(template, "render"):
            return template.render(**kwargs)
        else:
            # Fallback to basic string replacement
            result = template if isinstance(template, str) else ""
            for key, value in kwargs.items():
                placeholder = f"{{{{ {key} }}}}"
                if isinstance(value, list):
                    # Handle lists by joining with commas
                    result = result.replace(
                        placeholder, ", ".join(str(v) for v in value)
                    )
                else:
                    result = result.replace(
                        placeholder, str(value) if value is not None else ""
                    )

            # Clean up any remaining Jinja2 syntax for fallback
            result = re.sub(r"{%.*?%}", "", result, flags=re.DOTALL)
            result = re.sub(r"{{.*?}}", "", result)

            return result

    def convert_markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown to HTML"""
        if MARKDOWN_AVAILABLE:
            return markdown.markdown(markdown_text)  # This is the preferred way
        else:
            print(
                "⚠️  Markdown library not available, using basic conversion for content."
            )
            html = markdown_text
            # Add or refine your basic blockquote handling here if absolutely necessary
            # For your specific problem, ensure your Markdown input clearly separates blockquotes
            # or adjust your CSS. A simple regex like this might not be enough for complex cases.
            html = re.sub(
                r"^\s*>\s?(.*)$",
                r"<blockquote>\1</blockquote>",
                html,
                flags=re.MULTILINE,
            )
            html = re.sub(r"^# (.*$)", r"<h1>\1</h1>", html, flags=re.MULTILINE)
            html = re.sub(r"^## (.*$)", r"<h2>\1</h2>", html, flags=re.MULTILINE)
            html = re.sub(r"^### (.*$)", r"<h3>\1</h3>", html, flags=re.MULTILINE)
            html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
            html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html)
            html = html.replace("\n\n", "</p><p>")
            html = "<p>" + html + "</p>"
            html = re.sub(r"<p></p>", "", html)
            return html

    def generate_excerpt(self, markdown_text: str, length: int = 200) -> str:
        """Generate a text excerpt from markdown content."""
        # Remove markdown formatting for excerpt
        text = re.sub(r"```.*?```", "", markdown_text, flags=re.DOTALL)

        # Remove standard markdown blockquote markers (e.g., '> ') from the beginning of lines
        text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)

        # Explicitly remove the literal sequence ': >' wherever it appears in the text
        text = text.replace(": >", "")

        text = re.sub(r"^\s*[-*+]\s+.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^#+\s+", "", text, flags=re.MULTILINE)
        text = re.sub(r"[_*`]", "", text)
        text = re.sub(r"!\[.*?\]\(.*?\)", "", text)  # Removes image links

        # Extract link text instead of removing the whole link
        text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)

        text = text.replace("\n", " ")
        text = re.sub(r"\s+", " ", text).strip()

        if len(text) > length:
            return text[:length].rsplit(" ", 1)[0] + "..."
        return text

    def collect_posts(self):
        """Collect all markdown files and parse them"""
        if not self.content_dir.exists():
            print(f"❌ Content directory {self.content_dir} not found!")
            return

        markdown_files = list(self.content_dir.rglob("*.md"))
        print(f"📄 Found {len(markdown_files)} markdown files")

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

                # Enhanced tag parsing
                tags = metadata.get("tags", [])
                if isinstance(tags, str):
                    # Remove brackets if present
                    tags = tags.strip("[]")
                    tags = [tag.strip() for tag in tags.split(",") if tag.strip()]
                elif not isinstance(tags, list):
                    tags = []

                post = {
                    "title": metadata.get(
                        "title", file_path.stem.replace("-", " ").title()
                    ),
                    "date": post_date,
                    "content": content,
                    "metadata": metadata,
                    "file_path": file_path,
                    "url": self.generate_post_url(file_path),
                    "tags": tags,
                    "excerpt": self.generate_excerpt(content),
                }

                self.posts.append(post)
                print(f"✅ Successfully parsed: {post['title']})")
            else:
                print(f"❌ Failed to parse: {file_path.name}")

    def get_all_tags(self):
        tags_set = set()
        for post in self.posts:
            for tag in post.get("tags", []):
                tags_set.add(tag)
        return sorted(tags_set)

    def generate_post_url(self, file_path: Path) -> str:
        """Generate URL for post"""
        name = file_path.stem
        name = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)
        return f"posts/{name}.html"

    def build_tag_links(self, tags):
        return [f'<a href="/tag/{tag}/">{tag}</a>' for tag in tags]

    def generate_posts(self):
        """Generate individual post HTML files"""
        post_template = self.load_template("post.html")
        posts_dir = self.output_dir / "posts"
        posts_dir.mkdir(parents=True, exist_ok=True)

        all_tags = self.get_all_tags()
        for post in self.posts:
            post["tag_links"] = [
                f'<a href="/tag/{t}/">{t}</a>'
                for t in post.get("tags", [])
                if t in all_tags
            ]
            html_content = self.convert_markdown_to_html(
                post["content"]
            )  # <-- Add this line
            tag_links = post["tag_links"]
            rendered = self.render_template(
                post_template,
                title=post["title"],
                date=post["date"].strftime("%B %d, %Y") if post["date"] else "",
                content=html_content,
                tags=", ".join(tag_links),
            )

            output_path = self.output_dir / post["url"]
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered)

            print(f"✅ Generated: {post['url']}")

    def generate_tag_pages(self):
        all_tags = self.get_all_tags()
        archive_template = self.load_template("archive.html")
        for tag in all_tags:
            tag_posts = [post for post in self.posts if tag in post.get("tags", [])]
            tag_posts_sorted = sorted(
                tag_posts, key=lambda x: x["date"] or datetime.min, reverse=True
            )
            for post in tag_posts_sorted:
                post["tag_links"] = [
                    f'<a href="/tag/{t}/">{t}</a>'
                    for t in post.get("tags", [])
                    if t in all_tags
                ]
            rendered = self.render_template(
                archive_template,
                page_title=f"Tag: {tag} - Encyclopedia Muneerica",
                title=f"Tag: {tag}",
                journal_posts=tag_posts_sorted,
            )
            tag_dir = self.output_dir / "tag" / tag
            tag_dir.mkdir(parents=True, exist_ok=True)
            with open(tag_dir / "index.html", "w", encoding="utf-8") as f:
                f.write(rendered)
            print(f"✅ Generated tag page: /tag/{tag}/index.html")

    def generate_index(self):
        """Generate index page with recent entries"""
        # Sort posts by date (newest first)
        sorted_posts = sorted(
            self.posts, key=lambda x: x["date"] or datetime.min, reverse=True
        )
        for post in sorted_posts:
            post["tags"] = self.build_tag_links(post.get("tags", []))

        # Take only the last 15 posts
        recent_posts = sorted_posts[:15]

        # Load the index template
        index_template = self.load_template("index.html")

        # Render with Jinja2, passing journal_posts for the loop
        rendered = self.render_template(
            index_template,
            page_title="Encyclopedia Muneerica",
            title="Encyclopedia Muneerica",
            journal_posts=recent_posts,
            content="",
        )

        # Write index file
        index_path = self.output_dir / "index.html"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        print(f"✅ Generated: index.html with {len(recent_posts)} recent entries")

    def generate_tags_index(self):
        """Generate /tags/ index page with links to all tag pages."""
        # Collect all unique tags
        tags = set()
        for post in self.posts:
            for tag in post.get("tags", []):
                tags.add(tag)
        tags = sorted(tags, key=str.lower)

        # Prepare tag objects for template
        tags_list = [{"name": tag, "url": f"/tag/{tag}/"} for tag in tags]

        # Use archive.html as base template
        archive_template = self.load_template("archive.html")
        rendered = self.render_template(
            archive_template,
            page_title="Tags - Encyclopedia Muneerica",
            title="All Tags",
            journal_posts=[],  # No posts, just links
            tags_list=tags_list,
        )

        tags_dir = self.output_dir / "tags"
        tags_dir.mkdir(parents=True, exist_ok=True)
        with open(tags_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(rendered)
        print("✅ Generated tags index page: /tags/")

    def generate_archive(self):
        """Generate archive page with all posts."""
        # Sort all posts by date (newest first)
        all_posts = sorted(
            self.posts, key=lambda x: x["date"] or datetime.min, reverse=True
        )
        for post in all_posts:
            post["tags"] = self.build_tag_links(post.get("tags", []))

        # Load the default template
        archive_template = self.load_template("archive.html")

        rendered = self.render_template(
            archive_template,
            page_title="Archive - Encyclopedia Muneerica",
            title="Archive - Encyclopedia Muneerica",
            journal_posts=all_posts,
        )

        archive_path = self.output_dir / "archive.html"
        with open(archive_path, "w", encoding="utf-8") as f:
            f.write(rendered)

        print(f"✅ Generated: archive.html with all {len(all_posts)} posts")

    def copy_static_files(self):
        """Copy static files if they exist"""
        static_dir = Path("static")
        if static_dir.exists():
            static_output = self.output_dir / "static"
            if static_output.exists():
                shutil.rmtree(static_output)
            shutil.copytree(static_dir, static_output)
            print("✅ Copied static files")
        else:
            print("⚠️  No 'static' directory found to copy.")

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

        # Generate index page
        self.generate_index()

        # Generate archive page
        self.generate_archive()

        # Generate tag pages and index
        self.generate_tag_pages()
        self.generate_tags_index()

        # Copy static files
        self.copy_static_files()

        print(f"🎉 Site generated successfully!")
        print(f"📊 Generated {len(self.posts)} posts")
        print(f"📁 Output directory: {self.output_dir}")


def main():
    generator = SSGGenerator()
    generator.generate()


if __name__ == "__main__":
    main()

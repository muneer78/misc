#!/usr/bin/env python3
"""
Enhanced Static Site Generator Navigation (No Tag Pages)
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

        self.site_config = {
            "name": "Muneer After Dark",
            "description": "A YungMun Joint",
            "baseurl": "",
            "url": "",
            "github": "muneer78",
            "twitter": "reenum",
            "navigation": [
                {"name": "Archive", "url": "/archive.html"},
            ],
        }

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

    def parse_blockquotes(self, markdown_text: str) -> str:
        lines = markdown_text.split("\n")
        html_lines = []
        in_blockquote = False

        for line in lines:
            stripped = line.lstrip()
            if stripped.startswith(">"):
                if not in_blockquote:
                    html_lines.append("<blockquote>")
                    in_blockquote = True
                if stripped.strip() == ">":
                    # Insert a blank line within the blockquote using paragraph break
                    html_lines.append("<p></p>")
                else:
                    html_lines.append(stripped[1:].lstrip())
            else:
                if in_blockquote:
                    html_lines.append("</blockquote>")
                    in_blockquote = False
                html_lines.append(line)

        if in_blockquote:
            html_lines.append("</blockquote>")

        return "\n".join(html_lines)

    def ensure_paragraph_spacing(self, text: str) -> str:
        # Insert a blank line between two non-empty lines not already separated by a blank line
        lines = text.split("\n")
        new_lines = []
        for i, line in enumerate(lines):
            new_lines.append(line)
            if line.strip() and i + 1 < len(lines) and lines[i + 1].strip():
                new_lines.append("")  # Insert blank line
        return "\n".join(new_lines)

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
</head>
<body>
    <h1>{{ title }}</h1>
    <div class="meta">{{ date }}</div>
    <div class="content">{{ content }}</div>
    <div class="tags">{{ tags }}</div>
    <p><a href="/">← Back to Home</a></p>
</body>
</html>"""
        else:
            return """<!DOCTYPE html>
<html>
  <head>
    <title>{{ page_title or title }}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" type="text/css" href="/static/mun-personal.css" />
    <link rel="alternate" type="application/rss+xml" title="Muneer After Dark href="/rss.xml" />
  </head>
  <body>
    <div class="wrapper-masthead">
      <div class="container">
        <header class="masthead clearfix">
          <div class="site-info">
            <h1 class="site-name"><a href="/">Muneer After Dark</a></h1>
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
        if self.jinja_env and hasattr(template, "render"):
            return template.render(**kwargs)
        else:
            result = template if isinstance(template, str) else ""
            for key, value in kwargs.items():
                placeholder = f"{{{{ {key} }}}}"
                if isinstance(value, list):
                    result = result.replace(
                        placeholder, ", ".join(str(v) for v in value)
                    )
                else:
                    result = result.replace(
                        placeholder, str(value) if value is not None else ""
                    )
            result = re.sub(r"{%.*?%}", "", result, flags=re.DOTALL)
            result = re.sub(r"{{.*?}}", "", result)
            return result

    def convert_markdown_to_html(self, markdown_text: str) -> str:
        # Parse blockquotes first
        markdown_text = self.parse_blockquotes(markdown_text)
        # Ensure paragraphs are separated
        markdown_text = self.ensure_paragraph_spacing(markdown_text)
        if MARKDOWN_AVAILABLE:
            return markdown.markdown(markdown_text)
        else:
            print(
                "⚠️  Markdown library not available, using basic conversion for content."
            )
            html = markdown_text
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
        text = re.sub(r"```.*?```", "", markdown_text, flags=re.DOTALL)
        text = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE)
        text = text.replace(": >", "")
        text = re.sub(r"^\s*[-*+]\s+.*$", "", text, flags=re.MULTILINE)
        text = re.sub(r"^#+\s+", "", text, flags=re.MULTILINE)
        text = re.sub(r"[_*`]", "", text)
        text = re.sub(r"!\[.*?\]\(.*?\)", "", text)
        text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
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

                tags = metadata.get("tags", [])
                if isinstance(tags, str):
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

    def generate_post_url(self, file_path: Path) -> str:
        name = file_path.stem
        name = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name)
        return f"posts/{name}.html"

    def list_tags(self, tags):
        # Return tags as plain text, not links or spans
        return [str(tag) for tag in tags]

    def generate_posts(self):
        post_template = self.load_template("post.html")
        posts_dir = self.output_dir / "posts"
        posts_dir.mkdir(parents=True, exist_ok=True)

        for post in self.posts:
            html_content = self.convert_markdown_to_html(post["content"])
            # Pass tags as a list directly
            rendered = self.render_template(
                post_template,
                title=post["title"],
                date=post["date"].strftime("%B %d, %Y") if post["date"] else "",
                content=html_content,
                tags=post.get("tags", []),
            )

            output_path = self.output_dir / post["url"]
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(rendered)

            print(f"✅ Generated: {post['url']}")

    def generate_index(self):
        sorted_posts = sorted(
            self.posts, key=lambda x: x["date"] or datetime.min, reverse=True
        )
        for post in sorted_posts:
            post["tags"] = self.list_tags(post.get("tags", []))
        recent_posts = sorted_posts[:15]
        index_template = self.load_template("index.html")
        rendered = self.render_template(
            index_template,
            page_title="Muneer After Dark",
            title="Muneer After Dark",
            journal_posts=recent_posts,
            content="",
        )
        index_path = self.output_dir / "index.html"
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"✅ Generated: index.html with {len(recent_posts)} recent entries")

    def generate_archive(self):
        all_posts = sorted(
            self.posts, key=lambda x: x["date"] or datetime.min, reverse=True
        )
        for post in all_posts:
            post["tags"] = self.list_tags(post.get("tags", []))
        archive_template = self.load_template("archive.html")
        rendered = self.render_template(
            archive_template,
            page_title="Archive - Muneer After Dark",
            title="Archive - Muneer After Dark",
            journal_posts=all_posts,
        )
        archive_path = self.output_dir / "archive.html"
        with open(archive_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"✅ Generated: archive.html with all {len(all_posts)} posts")

    def generate_rss_feed(self):
        # Prepare posts for RSS (limit to recent 20)
        sorted_posts = sorted(
            self.posts, key=lambda x: x["date"] or datetime.min, reverse=True
        )
        rss_posts = []
        for post in sorted_posts[:20]:
            rss_posts.append(
                {
                    "title": post["title"],
                    "link": f"/{post['url']}",
                    "description": self.generate_excerpt(post["content"], length=300),
                    "pubDate": post["date"].strftime("%a, %d %b %Y %H:%M:%S GMT")
                    if post["date"]
                    else "",
                }
            )
        # Render RSS XML
        rss_template = self.load_template("rss.xml")
        rendered = self.render_template(
            rss_template,
            posts=rss_posts,
            site_title=self.site_config.get("name", "My Blog"),
            site_link=self.site_config.get("baseurl", "/"),
            site_description=self.site_config.get("description", ""),
        )
        # Write to site/rss.xml
        rss_path = self.output_dir / "rss.xml"
        with open(rss_path, "w", encoding="utf-8") as f:
            f.write(rendered)
        print("✅ Generated: rss.xml")

    def copy_static_files(self):
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
        print("🏗️  Starting site generation...")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.collect_posts()
        if not self.posts:
            print("❌ No posts found! Check your content files.")
            return
        self.generate_posts()
        self.generate_index()
        self.generate_archive()
        self.generate_rss_feed()
        self.copy_static_files()
        print(f"🎉 Site generated successfully!")
        print(f"📊 Generated {len(self.posts)} posts")
        print(f"📁 Output directory: {self.output_dir}")


def main():
    generator = SSGGenerator()
    generator.generate()


if __name__ == "__main__":
    main()

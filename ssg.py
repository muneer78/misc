#!/usr/bin/env python3
"""
Enhanced Static Site Generator Navigation (No Tag Pages) - Using Mistune
"""

import os
import shutil
from pathlib import Path
from datetime import datetime, date
from typing import Dict, List, Optional, Union
import re

# Try different frontmatter libraries
try:
    import frontmatter
    PARSER_TYPE = 'frontmatter'
except ImportError:
    try:
        import python_frontmatter as frontmatter
        PARSER_TYPE = 'python_frontmatter'
    except ImportError:
        print("No frontmatter library found. Installing python-frontmatter...")
        import subprocess
        subprocess.run(['pip', 'install', 'python-frontmatter'])
        import python_frontmatter as frontmatter
        PARSER_TYPE = 'python_frontmatter'

# Try to import Jinja2
try:
    from jinja2 import Environment, FileSystemLoader, select_autoescape
    JINJA2_AVAILABLE = True
except ImportError:
    print("Jinja2 not found. Installing Jinja2...")
    import subprocess
    subprocess.run(['pip', 'install', 'Jinja2'])
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
    subprocess.run(['pip', 'install', 'mistune'])
    try:
        import mistune
        MISTUNE_AVAILABLE = True
        print(f"✅ Using Mistune version: {mistune.__version__}")
    except ImportError:
        MISTUNE_AVAILABLE = False
        print("❌ Failed to install mistune library. Basic conversion will be used.")

class SSGGenerator:
    def __init__(self, content_dir: str = "content", output_dir: str = "site", template_dir: str = "templates"):
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.template_dir = Path(template_dir)
        self.posts = []
        self.collections = {}
        self.excluded_from_archive = ['personal', 'spicy']

        self.site_config = {
            'name': 'Encyclopedia Muneerica',
            'description': 'A YungMun Joint',
            'baseurl': '',
            'url': '',
            'github': 'muneer78',
            'twitter': 'reenum',
            'navigation': [
                {'name': 'Archive', 'url': '/archive.html'},
            ]
        }

        # Initialize Mistune markdown parser
        if MISTUNE_AVAILABLE:
            self.markdown_parser = mistune.create_markdown(
                escape=False,
                plugins=['strikethrough', 'footnotes', 'table']
            )
        else:
            self.markdown_parser = None

        if JINJA2_AVAILABLE:
            self.jinja_env = Environment(
                loader=FileSystemLoader(self.template_dir),
                autoescape=select_autoescape(['html', 'xml'])
            )
        else:
            self.jinja_env = None
            print("❌ Jinja2 is not available. Templating will be basic string replacement.")

    def normalize_date(self, date_obj: Union[datetime, date, None]) -> datetime:
        """Convert date objects to datetime objects for consistent comparison"""
        if date_obj is None:
            return datetime.min
        elif isinstance(date_obj, date) and not isinstance(date_obj, datetime):
            # Convert date to datetime
            return datetime.combine(date_obj, datetime.min.time())
        elif isinstance(date_obj, datetime):
            return date_obj
        else:
            return datetime.min

    def parse_frontmatter(self, file_path: Path) -> Optional[Dict]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            if PARSER_TYPE == 'frontmatter':
                if hasattr(frontmatter, 'loads'):
                    post = frontmatter.loads(content)
                elif hasattr(frontmatter, 'load'):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        post = frontmatter.load(f)
                else:
                    return self.manual_frontmatter_parse(content, file_path)
            else:
                post = frontmatter.loads(content)

            metadata = dict(post.metadata) if hasattr(post, 'metadata') else {}
            body = post.content if hasattr(post, 'content') else str(post)

            return {
                'metadata': metadata,
                'content': body,
                'file_path': file_path
            }

        except Exception as e:
            print(f"❌ Error parsing {file_path}: {e}")
            return self.manual_frontmatter_parse_from_file(file_path)

    def manual_frontmatter_parse_from_file(self, file_path: Path) -> Optional[Dict]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.manual_frontmatter_parse(content, file_path)
        except Exception as e:
            print(f"❌ Manual parsing failed for {file_path}: {e}")
            return None

    def manual_frontmatter_parse(self, content: str, file_path: Path) -> Optional[Dict]:
        if not content.startswith('---'):
            return {
                'metadata': {'title': file_path.stem.replace('-', ' ').title()},
                'content': content,
                'file_path': file_path
            }

        try:
            parts = content.split('---', 2)
            if len(parts) < 3:
                return None

            frontmatter_str = parts[1].strip()
            body = parts[2].strip()

            metadata = {}
            for line in frontmatter_str.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip().strip('"\'')

                    if value.startswith('[') and value.endswith(']'):
                        value = value[1:-1]
                        value = [tag.strip().strip('"\'') for tag in value.split(',') if tag.strip()]
                    elif ',' in value and key.lower() in ['tags']:
                        value = [tag.strip().strip('"\'') for tag in value.split(',') if tag.strip()]

                    metadata[key] = value

            return {
                'metadata': metadata,
                'content': body,
                'file_path': file_path
            }
        except Exception as e:
            print(f"❌ Manual parsing error for {file_path}: {e}")
            return None

    def extract_date_from_filename(self, filename: str) -> Optional[datetime]:
        match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
        if match:
            try:
                return datetime.strptime(match.group(1), '%Y-%m-%d')
            except ValueError:
                pass
        return None

    def load_template(self, template_name: str):
        if self.jinja_env:
            try:
                return self.jinja_env.get_template(template_name)
            except Exception as e:
                print(f"⚠️  Jinja2 failed to load template {template_name}: {e}")

        print(f"⚠️  Template {template_name} not found or Jinja2 failed, using basic template")
        if template_name == 'post.html':
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
        if self.jinja_env and hasattr(template, 'render'):
            return template.render(**kwargs)
        else:
            result = template if isinstance(template, str) else ""
            for key, value in kwargs.items():
                placeholder = f"{{{{ {key} }}}}"
                if isinstance(value, list):
                    result = result.replace(placeholder, ', '.join(str(v) for v in value))
                else:
                    result = result.replace(placeholder, str(value) if value is not None else '')
            result = re.sub(r'{%.*?%}', '', result, flags=re.DOTALL)
            result = re.sub(r'{{.*?}}', '', result)
            return result

    def convert_markdown_to_html(self, markdown_text: str) -> str:
        """Convert markdown to HTML using Mistune"""
        if MISTUNE_AVAILABLE and self.markdown_parser:
            try:
                return self.markdown_parser(markdown_text)
            except Exception as e:
                print(f"⚠️  Mistune conversion failed: {e}, falling back to basic conversion")
                return self.basic_markdown_conversion(markdown_text)
        else:
            print("⚠️  Mistune not available, using basic conversion for content.")
            return self.basic_markdown_conversion(markdown_text)

    def basic_markdown_conversion(self, markdown_text: str) -> str:
        """Basic markdown conversion fallback"""
        html = markdown_text
        
        # Headers
        html = re.sub(r'^# (.*$)', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*$)', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*$)', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.*$)', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        html = re.sub(r'^##### (.*$)', r'<h5>\1</h5>', html, flags=re.MULTILINE)
        html = re.sub(r'^###### (.*$)', r'<h6>\1</h6>', html, flags=re.MULTILINE)
        
        # Blockquotes
        html = re.sub(r'^> (.*$)', r'<blockquote>\1</blockquote>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        
        # Code blocks (basic)
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # Links
        html = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', html)
        
        # Images
        html = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', r'<img src="\2" alt="\1">', html)
        
        # Lists (basic)
        html = re.sub(r'^\- (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'^\* (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
        html = re.sub(r'^\+ (.*$)', r'<li>\1</li>', html, flags=re.MULTILINE)
        
        # Wrap consecutive <li> elements in <ul>
        html = re.sub(r'(<li>.*?</li>)(?:\n<li>.*?</li>)*', r'<ul>\g<0></ul>', html, flags=re.DOTALL)
        
        # Paragraphs
        html = html.replace('\n\n', '</p><p>')
        html = '<p>' + html + '</p>'
        html = re.sub(r'<p></p>', '', html)
        html = re.sub(r'<p>(<h[1-6]>.*?</h[1-6]>)</p>', r'\1', html)
        html = re.sub(r'<p>(<blockquote>.*?</blockquote>)</p>', r'\1', html)
        html = re.sub(r'<p>(<ul>.*?</ul>)</p>', r'\1', html, flags=re.DOTALL)
        
        return html

    def generate_excerpt(self, markdown_text: str, length: int = 200) -> str:
        """Generate an excerpt from markdown text"""
        # Remove code blocks
        text = re.sub(r'```.*?```', '', markdown_text, flags=re.DOTALL)
        # Remove blockquotes
        text = re.sub(r'^\s*>\s?', '', text, flags=re.MULTILINE)
        text = text.replace(': >', '')
        # Remove list items
        text = re.sub(r'^\s*[-*+]\s+.*$', '', text, flags=re.MULTILINE)
        # Remove headers
        text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
        # Remove markdown formatting
        text = re.sub(r'[_*`]', '', text)
        # Remove images
        text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
        # Remove links but keep text
        text = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text)
        # Clean up whitespace
        text = text.replace('\n', ' ')
        text = re.sub(r'\s+', ' ', text).strip()
        
        if len(text) > length:
            return text[:length].rsplit(' ', 1)[0] + '...'
        return text

    def collect_posts(self):
        if not self.content_dir.exists():
            print(f"❌ Content directory {self.content_dir} not found!")
            return

        markdown_files = list(self.content_dir.rglob("*.md"))
        print(f"📄 Found {len(markdown_files)} markdown files")

        # Initialize collections dictionary
        self.collections = {}

        for file_path in markdown_files:
            print(f"Processing: {file_path.name}")
            parsed = self.parse_frontmatter(file_path)

            if parsed:
                metadata = parsed['metadata']
                content = parsed['content']

                file_date = self.extract_date_from_filename(file_path.name)
                post_date = metadata.get('date', file_date)

                if isinstance(post_date, str):
                    try:
                        post_date = datetime.strptime(post_date, '%Y-%m-%d')
                    except ValueError:
                        post_date = file_date or datetime.now()

                tags = metadata.get('tags', [])
                if isinstance(tags, str):
                    tags = tags.strip('[]')
                    tags = [tag.strip() for tag in tags.split(',') if tag.strip()]
                elif not isinstance(tags, list):
                    tags = []

                # Determine collection based on subfolder
                relative_path = file_path.relative_to(self.content_dir)
                collection_name = relative_path.parts[0] if len(relative_path.parts) > 1 else 'posts'
                
                post = {
                    'title': metadata.get('title', file_path.stem.replace('-', ' ').title()),
                    'date': post_date,
                    'content': content,
                    'metadata': metadata,
                    'file_path': file_path,
                    'url': self.generate_post_url(file_path, collection_name),
                    'tags': tags,
                    'excerpt': self.generate_excerpt(content),
                    'collection': collection_name
                }

                # Add to main posts list
                self.posts.append(post)
                
                # Add to collection
                if collection_name not in self.collections:
                    self.collections[collection_name] = []
                self.collections[collection_name].append(post)
                
                print(f"✅ Successfully parsed: {post['title']} (collection: {collection_name})")
            else:
                print(f"❌ Failed to parse: {file_path.name}")

        # Print collection summary
        print(f"\n📚 Collections found:")
        for collection_name, posts in self.collections.items():
            print(f"  - {collection_name}: {len(posts)} posts")
        print()

    def generate_post_url(self, file_path: Path, collection_name: str = 'posts') -> str:
        """Generate URL for post, keeping the date in the filename"""
        name = file_path.stem  # Keep the full filename including date
        
        if collection_name == 'posts':
            return f"posts/{name}.html"
        else:
            return f"{collection_name}/{name}.html"

    def list_tags(self, tags):
        # Return tags as plain text, not links or spans
        return [str(tag) for tag in tags]

    def generate_posts(self):
        post_template = self.load_template('post.html')
        
        # Create directories for each collection
        for collection_name in self.collections.keys():
            collection_dir = self.output_dir / collection_name
            collection_dir.mkdir(parents=True, exist_ok=True)

        for post in self.posts:
            html_content = self.convert_markdown_to_html(post['content'])
            # Pass tags as a list directly
            rendered = self.render_template(
                post_template,
                title=post['title'],
                date=post['date'].strftime('%B %d, %Y') if post['date'] else '',
                content=html_content,
                tags=post.get('tags', []),
                collection=post.get('collection', 'posts')
            )

            output_path = self.output_dir / post['url']
            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(rendered)

            print(f"✅ Generated: {post['url']}")

    def generate_collection_indexes(self):
        """Generate index pages for each collection"""
        index_template = self.load_template('index.html')
        
        for collection_name, collection_posts in self.collections.items():
            if collection_name == 'posts':
                continue  # Skip main posts collection, handled by main index
                
            # Sort posts by date using normalize_date
            sorted_posts = sorted(collection_posts, key=lambda x: self.normalize_date(x['date']), reverse=True)
            for post in sorted_posts:
                post['tags'] = self.list_tags(post.get('tags', []))
            
            # Generate collection title
            collection_title = collection_name.replace('_', ' ').replace('-', ' ').title()
            
            rendered = self.render_template(
                index_template,
                page_title=f"{collection_title} - Encyclopedia Muneerica",
                title=f"{collection_title} - Encyclopedia Muneerica",
                journal_posts=sorted_posts,
                content="",
                collection=collection_name
            )
            
            # Create collection index page
            collection_index_path = self.output_dir / collection_name / 'index.html'
            collection_index_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(collection_index_path, 'w', encoding='utf-8') as f:
                f.write(rendered)
            
            print(f"✅ Generated: {collection_name}/index.html with {len(sorted_posts)} posts")

    def generate_index(self):
        # Generate main index with only posts from 'posts' collection
        posts_collection = self.collections.get('posts', [])
        sorted_posts = sorted(posts_collection, key=lambda x: self.normalize_date(x['date']), reverse=True)
        for post in sorted_posts:
            post['tags'] = self.list_tags(post.get('tags', []))
        recent_posts = sorted_posts[:15]
        
        index_template = self.load_template('index.html')
        rendered = self.render_template(
            index_template,
            page_title="Encyclopedia Muneerica",
            title="Encyclopedia Muneerica",
            journal_posts=recent_posts,
            content="",
            collection="posts"
        )
        index_path = self.output_dir / 'index.html'
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
        print(f"✅ Generated: index.html with {len(recent_posts)} recent entries")

    def generate_archive(self):
        # Filter out posts from excluded collections
        filtered_posts = [
            post for post in self.posts 
            if post.get('collection', 'posts') not in self.excluded_from_archive
        ]
        
        # Sort the filtered posts using normalize_date
        all_posts = sorted(filtered_posts, key=lambda x: self.normalize_date(x['date']), reverse=True)
        
        for post in all_posts:
            post['tags'] = self.list_tags(post.get('tags', []))
        
        # Filter collections for template context (excluding personal and spicy)
        filtered_collections = {
            name: posts for name, posts in self.collections.items() 
            if name not in self.excluded_from_archive
        }
        
        archive_template = self.load_template('archive.html')
        rendered = self.render_template(
            archive_template,
            page_title="Archive - Encyclopedia Muneerica",
            title="Archive - Encyclopedia Muneerica",
            journal_posts=all_posts,
            collections=filtered_collections
        )
        archive_path = self.output_dir / 'archive.html'
        with open(archive_path, 'w', encoding='utf-8') as f:
            f.write(rendered)
        print(f"✅ Generated: archive.html with {len(all_posts)} posts across {len(filtered_collections)} collections (excluding personal/spicy)")

    def generate_rss_feed(self):
        # Prepare posts for RSS (limit to recent 20) using normalize_date
        sorted_posts = sorted(self.posts, key=lambda x: self.normalize_date(x['date']), reverse=True)
        rss_posts = []
        for post in sorted_posts[:20]:
            rss_posts.append({
                "title": post["title"],
                "link": f"/{post['url']}",
                "description": self.generate_excerpt(post["content"], length=300),
                "pubDate": post["date"].strftime("%a, %d %b %Y %H:%M:%S GMT") if post["date"] else "",
            })
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
        static_dir = Path('static')
        if static_dir.exists():
            static_output = self.output_dir / 'static'
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
        self.generate_collection_indexes()
        self.generate_archive()
        self.generate_rss_feed()
        self.copy_static_files()
        print(f"🎉 Site generated successfully!")
        print(f"📊 Generated {len(self.posts)} posts across {len(self.collections)} collections")
        print(f"📁 Output directory: {self.output_dir}")

def main():
    generator = SSGGenerator()
    generator.generate()

if __name__ == "__main__":
    main()

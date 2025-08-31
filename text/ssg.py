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
        self.included_in_archive = ['posts']

        self.site_config = {
            'name': 'Encyclopedia Muneerica',
            'description': 'A YungMun Joint',
            'baseurl': '',
            'url': '',
            'github': 'muneer78',
            'twitter': 'reenum',
            'navigation': [
                {'name': 'Archive', 'url': '/archive.html'},
                {'name': 'Tags', 'url': '/tags/'},
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

    def slugify_tag(self, tag: str) -> str:
        """Convert tag name to URL-safe slug"""
        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r'[^\w\s-]', '', tag.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')

    def collect_tags(self):
        """Collect and organize posts by tags"""
        self.tag_collections = {}
        self.all_tags = set()

        for post in self.posts:
            post_tags = post.get('tags', [])
            for tag in post_tags:
                if tag:  # Skip empty tags
                    self.all_tags.add(tag)
                    tag_slug = self.slugify_tag(tag)

                    if tag not in self.tag_collections:
                        self.tag_collections[tag] = {
                            'slug': tag_slug,
                            'posts': []
                        }
                    self.tag_collections[tag]['posts'].append(post)

        print(f"🏷️  Found {len(self.all_tags)} unique tags")

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
            # Improved basic template rendering
            result = template if isinstance(template, str) else ""

            # Handle simple variable substitution
            for key, value in kwargs.items():
                placeholder = f"{{{{ {key} }}}}"
                if isinstance(value, list):
                    if key == 'tags':
                        # For tags, join without escaping HTML since they contain links
                        result = result.replace(placeholder, ' '.join(str(v) for v in value))
                    else:
                        result = result.replace(placeholder, ', '.join(str(v) for v in value))
                else:
                    result = result.replace(placeholder, str(value) if value is not None else '')

            # Handle basic if statements for post_count pluralization
            result = re.sub(r'{%\s*if\s+post_count\s*!=\s*1\s*%}s{%\s*endif\s*%}',
                            's' if kwargs.get('post_count', 1) != 1 else '', result)

            # Handle basic if statements for total_tags pluralization
            result = re.sub(r'{%\s*if\s+total_tags\s*!=\s*1\s*%}s{%\s*endif\s*%}',
                            's' if kwargs.get('total_tags', 1) != 1 else '', result)

            # Handle basic for loops for tag_list
            if 'tag_list' in kwargs and kwargs['tag_list']:
                tag_items = ""
                for tag in kwargs['tag_list']:
                    tag_item = '''<a href="/tags/{slug}/" class="tag-link">
              {name} <span class="tag-count">({count})</span>
            </a>'''.format(
                        slug=tag['slug'],
                        name=tag['name'],
                        count=tag['count']
                    )
                    tag_items += tag_item + "\n        "
                result = re.sub(r'{%\s*for\s+tag\s+in\s+tag_list\s*%}.*?{%\s*endfor\s*%}',
                                tag_items.rstrip(), result, flags=re.DOTALL)

            # Handle basic for loops for tag_posts
            if 'tag_posts' in kwargs and kwargs['tag_posts']:
                post_items = ""
                for i, post in enumerate(kwargs['tag_posts']):
                    post_date = post['date'].strftime('%B %d, %Y') if post['date'] else ''
                    tags_str = ', '.join([f'<span class="tag">{tag}</span>' for tag in post.get('tags', [])])

                    post_item = f'''<article class="post-preview">
            <h3><a href="/{post['url']}">{post['title']}</a></h3>
            <div class="post-meta">
              {post_date}
              {f'<span class="tags">{tags_str}</span>' if tags_str else ''}
            </div>
            <div class="post-excerpt">{post['excerpt']}</div>
            <p><a href="/{post['url']}" class="read-more">Read More →</a></p>
          </article>'''
                    if i < len(kwargs['tag_posts']) - 1:
                        post_item += "\n      <hr>"
                    post_items += post_item + "\n      "
                result = re.sub(r'{%\s*for\s+post\s+in\s+tag_posts\s*%}.*?{%\s*endfor\s*%}',
                                post_items.rstrip(), result, flags=re.DOTALL)

            # Handle conditional blocks
            if 'tag_posts' in kwargs:
                if kwargs['tag_posts']:
                    result = re.sub(r'{%\s*if\s+tag_posts\s*%}(.*?){%\s*else\s*%}.*?{%\s*endif\s*%}',
                                    r'\1', result, flags=re.DOTALL)
                else:
                    result = re.sub(r'{%\s*if\s+tag_posts\s*%}.*?{%\s*else\s*%}(.*?){%\s*endif\s*%}',
                                    r'\1', result, flags=re.DOTALL)

            if 'tag_list' in kwargs:
                if kwargs['tag_list']:
                    result = re.sub(r'{%\s*if\s+tag_list\s*%}(.*?){%\s*else\s*%}.*?{%\s*endif\s*%}',
                                    r'\1', result, flags=re.DOTALL)
                else:
                    result = re.sub(r'{%\s*if\s+tag_list\s*%}.*?{%\s*else\s*%}(.*?){%\s*endif\s*%}',
                                    r'\1', result, flags=re.DOTALL)

            # Clean up remaining template syntax
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
        # Return tags as clickable HTML links instead of plain text
        tag_links = []
        for tag in tags:
            tag_slug = self.slugify_tag(str(tag))
            tag_links.append(f'<a href="/tags/{tag_slug}/" class="tag-link">{tag}</a>')
        return tag_links

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
        # Include posts in included collections
        filtered_posts = [
            post for post in self.posts 
            if post.get('collection', 'posts') in self.included_in_archive
        ]
        
        # Sort the filtered posts using normalize_date
        all_posts = sorted(filtered_posts, key=lambda x: self.normalize_date(x['date']), reverse=True)
        
        for post in all_posts:
            post['tags'] = self.list_tags(post.get('tags', []))
        
        # Filter collections for template context
        filtered_collections = {
            name: posts for name, posts in self.collections.items() 
            if name in self.included_in_archive
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
        print(f"✅ Generated: archive.html with {len(all_posts)} posts across {len(filtered_collections)} collections")

    def generate_tag_pages(self):
        """Generate individual pages for each tag"""
        # Create tags directory first
        tags_dir = self.output_dir / 'tags'
        tags_dir.mkdir(parents=True, exist_ok=True)

        # Try to load the tag template
        try:
            if self.jinja_env:
                tag_template = self.jinja_env.get_template('tag.html')
            else:
                # Use a fallback template if Jinja2 fails
                tag_template = self.get_fallback_tag_template()
        except Exception as e:
            print(f"⚠️  Could not load tag.html template: {e}")
            tag_template = self.get_fallback_tag_template()

        for tag_name, tag_data in self.tag_collections.items():
            tag_slug = tag_data['slug']
            tag_posts = sorted(tag_data['posts'], key=lambda x: self.normalize_date(x['date']), reverse=True)

            # Process tags for each post
            for post in tag_posts:
                post['tags'] = self.list_tags(post.get('tags', []))

            rendered = self.render_template(
                tag_template,
                tag_name=tag_name,
                tag_slug=tag_slug,
                tag_posts=tag_posts,
                post_count=len(tag_posts)
            )

            # Create tag directory and index file
            tag_dir = tags_dir / tag_slug
            tag_dir.mkdir(parents=True, exist_ok=True)
            tag_file = tag_dir / 'index.html'

            with open(tag_file, 'w', encoding='utf-8') as f:
                f.write(rendered)

            print(f"✅ Generated: tags/{tag_slug}/index.html ({len(tag_posts)} posts)")

    def get_fallback_tag_template(self):
        """Return a fallback tag template if the file doesn't exist"""
        return '''<!DOCTYPE html>
    <html>
      <head>
        <title>{{ tag_name }} - Encyclopedia Muneerica</title>
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
                <a href="/archive.html">Archive</a>
                <a href="/cities/index.html">Cities</a>
                <a href="/strange_researches/index.html">Strange Researches</a>
                <a href="/newsletter/index.html">Newsletter</a>
                <a href="/tags/index.html">Tags</a>
                <a href="/rss.xml">RSS</a>
              </nav>
            </header>
          </div>
        </div>
        <div id="main" role="main" class="container">
          <h1>Posts tagged with "{{ tag_name }}"</h1>
          <p>{{ post_count }} post{% if post_count != 1 %}s{% endif %} found</p>
          {% if tag_posts %}
          {% for post in tag_posts %}
          <article class="post-preview">
            <h3><a href="/{{ post.url }}">{{ post.title }}</a></h3>
            <div class="post-meta">{{ post.date.strftime('%B %d, %Y') if post.date else '' }}</div>
            <div class="post-excerpt">{{ post.excerpt }}</div>
            <p><a href="/{{ post.url }}" class="read-more">Read More →</a></p>
          </article>
          {% if not loop.last %}<hr>{% endif %}
          {% endfor %}
          {% else %}
          <p>No posts found for this tag.</p>
          {% endif %}
          <p><a href="/tags/">← Back to All Tags</a></p>
        </div>
        <div class="wrapper-footer">
          <div class="container">
            <footer class="footer">
              <p>If you want to copy anything here, tell me.</p>
            </footer>
          </div>
        </div>
      </body>
    </html>'''

    def get_fallback_tags_index_template(self):
        """Return a fallback tags index template"""
        return '''<!DOCTYPE html>
    <html>
      <head>
        <title>Tags - Encyclopedia Muneerica</title>
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
                <a href="/archive.html">Archive</a>
                <a href="/tags/index.html">Tags</a>
                <a href="/cities/index.html">Cities</a>
                <a href="/strange_researches/index.html">Strange Researches</a>
                <a href="/newsletter/index.html">Newsletter</a>
                <a href="/rss.xml">RSS</a>
              </nav>
            </header>
          </div>
        </div>
        <div id="main" role="main" class="container">
          <h1>All Tags</h1>
          <p>{{ total_tags }} tag{% if total_tags != 1 %}s{% endif %} found</p>
          {% if tag_list %}
          <div class="tag-cloud">
            {% for tag in tag_list %}
            <a href="/tags/{{ tag.slug }}/" class="tag-link">{{ tag.name }} ({{ tag.count }})</a>
            {% endfor %}
          </div>
          {% else %}
          <p>No tags found.</p>
          {% endif %}
        </div>
        <div class="wrapper-footer">
          <div class="container">
            <footer class="footer">
              <p>If you want to copy anything here, tell me.</p>
            </footer>
          </div>
        </div>
        <style>
        .tag-cloud { margin: 2em 0; }
        .tag-link { 
          display: inline-block; margin: 0.5em 1em 0.5em 0; padding: 0.5em 1em;
          background: #f5f5f5; border-radius: 4px; text-decoration: none; color: #333;
          border: 1px solid #ddd; transition: background-color 0.2s;
        }
        .tag-link:hover { background: #e0e0e0; }
        </style>
      </body>
    </html>'''

    def generate_tags_index(self):
        """Generate index page showing all tags"""
        # Create tags directory first
        tags_dir = self.output_dir / 'tags'
        tags_dir.mkdir(parents=True, exist_ok=True)

        try:
            if self.jinja_env:
                tags_index_template = self.jinja_env.get_template('tags-index.html')
            else:
                tags_index_template = self.get_fallback_tags_index_template()
        except Exception as e:
            print(f"⚠️  Could not load tags-index.html template: {e}")
            tags_index_template = self.get_fallback_tags_index_template()

        # Sort tags by post count (descending) then alphabetically
        tag_list = []
        for tag_name, tag_data in self.tag_collections.items():
            tag_list.append({
                'name': tag_name,
                'slug': tag_data['slug'],
                'count': len(tag_data['posts'])
            })

        tag_list.sort(key=lambda x: (-x['count'], x['name'].lower()))

        rendered = self.render_template(
            tags_index_template,
            tag_list=tag_list,
            total_tags=len(tag_list)
        )

        tags_index_file = tags_dir / 'index.html'
        with open(tags_index_file, 'w', encoding='utf-8') as f:
            f.write(rendered)

        print(f"✅ Generated: tags/index.html ({len(tag_list)} tags)")

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
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    backup_name = f"{self.output_dir.name}_backup_{timestamp}"
                    backup_path = self.output_dir.parent / backup_name
                    shutil.move(str(self.output_dir), str(backup_path))
                    print(f"📦 Moved existing {self.output_dir} to {backup_path}")
            except Exception as e:
                print(f"⚠️  Could not move to trash, removing directory: {e}")
                shutil.rmtree(self.output_dir)

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.collect_posts()
        if not self.posts:
            print("❌ No posts found! Check your content files.")
            return

        self.collect_tags()  # New: Collect tags after posts
        self.generate_posts()
        self.generate_index()
        self.generate_collection_indexes()
        self.generate_archive()
        self.generate_tag_pages()  # New: Generate tag pages
        self.generate_tags_index()  # New: Generate tags index
        self.generate_rss_feed()
        self.copy_static_files()
        print(f"🎉 Site generated successfully!")
        print(f"📊 Generated {len(self.posts)} posts across {len(self.collections)} collections")
        print(f"🏷️  Generated {len(self.tag_collections)} tag pages")
        print(f"📁 Output directory: {self.output_dir}")

def main():
    generator = SSGGenerator()
    generator.generate()

if __name__ == "__main__":
    main()

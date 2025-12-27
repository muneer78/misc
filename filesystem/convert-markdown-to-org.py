#!/usr/bin/env python3
"""
Convert a directory of markdown files into a single Emacs Org-mode file.
Preserves folder structure as nested headings, uses file titles as headings,
and converts frontmatter to Org tags and properties.
"""

import os
import re
import sys
from pathlib import Path
import yaml


def parse_frontmatter(content):
    """Extract YAML frontmatter and remaining content from markdown."""
    frontmatter = {}
    body = content
    
    # Check for YAML frontmatter (--- at start)
    if content.startswith('---\n'):
        parts = content.split('---\n', 2)
        if len(parts) >= 3:
            try:
                frontmatter = yaml.safe_load(parts[1]) or {}
                body = parts[2].strip()
            except yaml.YAMLError:
                pass
    
    return frontmatter, body


def frontmatter_to_org_tags(frontmatter):
    """Convert frontmatter dict to Org-mode tags string."""
    tags = []
    
    # Common frontmatter fields that work well as tags
    tag_fields = ['tags', 'categories', 'keywords']
    
    for field in tag_fields:
        if field in frontmatter:
            value = frontmatter[field]
            if isinstance(value, list):
                tags.extend(value)
            elif isinstance(value, str):
                tags.extend([t.strip() for t in value.split(',')])
    
    # Clean up tags (remove spaces, special chars)
    clean_tags = []
    for tag in tags:
        tag = re.sub(r'[^\w\-]', '_', str(tag))
        if tag:
            clean_tags.append(tag)
    
    return ':'.join(clean_tags) if clean_tags else ''


def frontmatter_to_properties(frontmatter):
    """Convert frontmatter to Org-mode properties and metadata."""
    if not frontmatter:
        return ''
    
    lines = []
    
    # Extract tags for #+TAGS: line (for org-ssg.el compatibility)
    tag_fields = ['tags', 'categories', 'keywords']
    tags = []
    for field in tag_fields:
        if field in frontmatter:
            value = frontmatter[field]
            if isinstance(value, list):
                tags.extend(value)
            elif isinstance(value, str):
                tags.extend([t.strip() for t in value.split(',')])
    
    # Add #+TAGS: line if we have tags
    if tags:
        # Clean up tags
        clean_tags = [re.sub(r'[^\w\-]', '_', str(tag)) for tag in tags if tag]
        lines.append(f'#+TAGS: {" ".join(clean_tags)}')
    
    # Add other frontmatter as #+KEY: VALUE
    skip_fields = {'tags', 'categories', 'keywords', 'title', 'date'}
    for key, value in frontmatter.items():
        if key.lower() not in skip_fields:
            if isinstance(value, (list, dict)):
                value = str(value)
            lines.append(f'#+{key.upper()}: {value}')
    
    # Add properties drawer for other metadata
    props = [':PROPERTIES:']
    for key, value in frontmatter.items():
        if key.lower() not in skip_fields and key.lower() not in tag_fields:
            if isinstance(value, (list, dict)):
                value = str(value)
            props.append(f':{key.upper()}: {value}')
    
    if len(props) > 1:  # Only add if there are properties
        props.append(':END:')
        lines.extend(props)
    
    return '\n'.join(lines) if lines else ''


def convert_markdown_to_org(content, base_level):
    """Convert markdown syntax to Org-mode syntax."""
    lines = content.split('\n')
    result = []
    in_code_block = False
    in_quote_block = False
    quote_lines = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Handle code blocks
        if line.startswith('```'):
            if not in_code_block:
                # Start of code block
                in_code_block = True
                lang = line[3:].strip()
                result.append(f"#+BEGIN_SRC {lang if lang else ''}")
            else:
                # End of code block
                in_code_block = False
                result.append("#+END_SRC")
            i += 1
            continue
        
        if in_code_block:
            result.append(line)
            i += 1
            continue
        
        # Handle block quotes
        if line.startswith('>'):
            if not in_quote_block:
                in_quote_block = True
                quote_lines = []
            # Remove the '>' and any following space
            quote_lines.append(line[1:].lstrip())
            i += 1
            continue
        elif in_quote_block:
            # Check if this is truly the end of the quote block
            # Empty line followed by another quote = separate blocks
            # Empty line followed by non-quote = end of block
            if line.strip() == '':
                # Look ahead to see if there's another quote coming
                if i + 1 < len(lines) and lines[i + 1].startswith('>'):
                    # End current quote block, empty line will separate them
                    result.append("#+BEGIN_QUOTE")
                    result.extend(quote_lines)
                    result.append("#+END_QUOTE")
                    result.append('')  # Add the empty line separator
                    in_quote_block = False
                    quote_lines = []
                    i += 1
                    continue
                else:
                    # Empty line might be inside the quote (for paragraphs)
                    quote_lines.append('')
                    i += 1
                    continue
            else:
                # Non-empty, non-quote line = end of quote block
                result.append("#+BEGIN_QUOTE")
                result.extend(quote_lines)
                result.append("#+END_QUOTE")
                in_quote_block = False
                quote_lines = []
                # Don't increment i, process this line normally
        
        # Convert headers (adjust level based on folder depth)
        if line.startswith('#'):
            level = len(re.match(r'^#+', line).group())
            new_level = '*' * (level + base_level)
            line = re.sub(r'^#+', new_level, line)
        
        # Convert bold: **text** or __text__ to *text*
        line = re.sub(r'\*\*(.+?)\*\*', r'*\1*', line)
        line = re.sub(r'__(.+?)__', r'*\1*', line)
        
        # Convert italic: *text* or _text_ to /text/
        # Be careful not to convert bold
        line = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'/\1/', line)
        line = re.sub(r'_(.+?)_', r'/\1/', line)
        
        # Convert inline code: `code` to =code=
        line = re.sub(r'`([^`]+)`', r'=\1=', line)
        
        # Convert images: ![alt](path) to [[file:path]]
        # Images need to be converted before regular links
        line = re.sub(r'!\[([^\]]*)\]\(([^\)]+)\)', r'[[file:\2]]', line)
        
        # Convert links: [text](url) to [[url][text]]
        line = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'[[\2][\1]]', line)
        
        result.append(line)
        i += 1
    
    # Handle any unclosed quote block at end of content
    if in_quote_block:
        result.append("#+BEGIN_QUOTE")
        result.extend(quote_lines)
        result.append("#+END_QUOTE")
    
    return '\n'.join(result)


def get_folder_structure(directory):
    """Build a nested structure of folders and markdown files."""
    directory = Path(directory)
    structure = {'name': directory.name, 'path': directory, 'folders': {}, 'files': []}
    
    def scan_dir(path, struct):
        try:
            for item in sorted(path.iterdir()):
                if item.is_file() and item.suffix in ['.md', '.markdown']:
                    struct['files'].append(item)
                elif item.is_dir() and not item.name.startswith('.'):
                    folder_name = item.name
                    struct['folders'][folder_name] = {
                        'name': folder_name,
                        'path': item,
                        'folders': {},
                        'files': []
                    }
                    scan_dir(item, struct['folders'][folder_name])
        except PermissionError:
            pass
    
    scan_dir(directory, structure)
    return structure


def write_structure(out, structure, level=1):
    """Recursively write the folder structure to org file."""
    
    # Write files in current folder
    for md_file in structure['files']:
        print(f"Processing {md_file.relative_to(structure['path'].parent)}...")
        
        # Read file
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        frontmatter, body = parse_frontmatter(content)
        
        # Get filename without extension as heading
        title = md_file.stem
        
        # Write heading at current level
        heading_stars = '*' * level
        tags = frontmatter_to_org_tags(frontmatter)
        if tags:
            out.write(f"{heading_stars} {title} :{tags}:\n")
        else:
            out.write(f"{heading_stars} {title}\n")
        
        # Write properties
        properties = frontmatter_to_properties(frontmatter)
        if properties:
            out.write(properties + '\n')
        
        # Convert and write content
        org_content = convert_markdown_to_org(body, level)
        out.write('\n' + org_content + '\n\n')
    
    # Write subfolders
    for folder_name, folder_struct in structure['folders'].items():
        # Create heading for folder
        heading_stars = '*' * level
        out.write(f"{heading_stars} {folder_name}\n\n")
        
        # Recursively process folder contents
        write_structure(out, folder_struct, level + 1)


def process_directory(directory, output_file):
    """Process all markdown files in directory tree and combine into org file."""
    directory = Path(directory)
    
    if not directory.is_dir():
        print(f"Error: {directory} is not a directory")
        sys.exit(1)
    
    # Build folder structure
    structure = get_folder_structure(directory)
    
    # Count total files
    def count_files(struct):
        count = len(struct['files'])
        for subfolder in struct['folders'].values():
            count += count_files(subfolder)
        return count
    
    total_files = count_files(structure)
    
    if total_files == 0:
        print(f"No markdown files found in {directory}")
        sys.exit(1)
    
    print(f"Found {total_files} markdown file(s)")
    
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(f"#+TITLE: {directory.name}\n")
        out.write(f"#+DATE: {os.popen('date +%Y-%m-%d').read().strip()}\n\n")
        
        # Write the entire structure
        write_structure(out, structure)
    
    print(f"\nSuccessfully created {output_file}")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python md_to_org.py <directory> [output_file]")
        print("Example: python md_to_org.py ./notes combined.org")
        print("\nThis will preserve the folder structure as nested Org headings.")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else 'combined.org'
    
    process_directory(input_dir, output)
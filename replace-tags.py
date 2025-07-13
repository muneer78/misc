#!/usr/bin/env python3
"""
Script to recursively replace 'uplifting' with 'positive' on lines starting with 'tags:'
"""

import os
import re
import argparse
from pathlib import Path


def process_file(file_path, dry_run=False):
    """Process a single file to replace 'uplifting' with 'positive' on tags: lines"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        modified = False
        new_lines = []

        for line in lines:
            # Check if line starts with 'tags:' and contains 'uplifting'
            if line.strip().startswith('tags:') and 'uplifting' in line:
                new_line = line.replace('uplifting', 'positive')
                new_lines.append(new_line)
                modified = True
                if dry_run:
                    print(f"  {file_path}: {line.strip()} -> {new_line.strip()}")
            else:
                new_lines.append(line)

        if modified and not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Modified: {file_path}")

        return modified

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False


def replace_tags_recursively(directory, file_extensions=None, dry_run=False):
    """
    Recursively process files in directory

    Args:
        directory: Path to directory to process
        file_extensions: List of file extensions to process (e.g., ['.txt', '.md', '.yml'])
                        If None, processes all files
        dry_run: If True, show what would be changed without making changes
    """
    directory = Path(directory)

    if not directory.exists():
        print(f"Directory {directory} does not exist!")
        return

    if not directory.is_dir():
        print(f"{directory} is not a directory!")
        return

    total_files = 0
    modified_files = 0

    print(f"{'DRY RUN: ' if dry_run else ''}Processing directory: {directory}")
    print(f"File extensions: {file_extensions if file_extensions else 'all files'}")
    print("-" * 50)

    # Walk through all files recursively
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = Path(root) / file

            # Skip if file extension filter is specified and doesn't match
            if file_extensions and file_path.suffix.lower() not in file_extensions:
                continue

            # Skip binary files (basic check)
            if file_path.suffix.lower() in ['.exe', '.bin', '.jpg', '.png', '.gif', '.pdf', '.zip']:
                continue

            total_files += 1

            if process_file(file_path, dry_run):
                modified_files += 1

    print("-" * 50)
    print(f"Total files processed: {total_files}")
    print(f"Files {'that would be ' if dry_run else ''}modified: {modified_files}")


def main():
    parser = argparse.ArgumentParser(description='Replace "uplifting" with "positive" on lines starting with "tags:"')
    parser.add_argument('directory', help='Directory to process')
    parser.add_argument('--extensions', '-e', nargs='+',
                        help='File extensions to process (e.g., .txt .md .yml)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Show what would be changed without making changes')

    args = parser.parse_args()

    # Convert extensions to lowercase with dots
    extensions = None
    if args.extensions:
        extensions = [ext.lower() if ext.startswith('.') else f'.{ext.lower()}'
                      for ext in args.extensions]

    replace_tags_recursively(args.directory, extensions, args.dry_run)


if __name__ == "__main__":
    # Example usage when run directly
    import sys

    if len(sys.argv) == 1:
        print("Usage examples:")
        print("  python script.py /path/to/directory")
        print("  python script.py /path/to/directory --dry-run")
        print("  python script.py /path/to/directory --extensions .txt .md .yml")
        print("  python script.py . --dry-run  # Process current directory")
        print()
        print("Running with current directory as example...")
        replace_tags_recursively('.', dry_run=True)
    else:
        main()
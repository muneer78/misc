#!/usr/bin/env python3
"""
Script to update tags in content files based on a mapping file.
Reads the tag mapping from misc.txt and updates the corresponding files.
"""

import os
import re
import shutil
from pathlib import Path
from datetime import datetime


def parse_tag_mapping(mapping_file):
    """Parse the tag mapping file and return a dictionary of file -> tags."""
    file_tags = {}

    with open(mapping_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or not line.startswith('./content/'):
                continue

            # Split on ':tags:' to separate file path from tags
            parts = line.split(':tags:', 1)
            if len(parts) != 2:
                continue

            file_path = parts[0].strip()
            tags = parts[1].strip()

            # Remove the './' prefix from file path
            file_path = file_path[2:] if file_path.startswith('./') else file_path

            file_tags[file_path] = tags

    return file_tags


def create_backup(file_path):
    """Create a backup of the file before modifying it."""
    try:
        backup_path = f"{file_path}.backup"
        shutil.copy2(file_path, backup_path)
        return True
    except Exception as e:
        print(f"Error creating backup for {file_path}: {e}")
        return False


def update_file_tags(file_path, new_tags):
    """Update the tags line in a file."""
    if not os.path.exists(file_path):
        print(f"Warning: File not found: {file_path}")
        return False

    # Create backup before modifying
    if not create_backup(file_path):
        print(f"Skipping {file_path} due to backup failure")
        return False

    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Find and update the tags line
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith('tags:'):
                lines[i] = f"tags: {new_tags}\n"
                updated = True
                break

        if updated:
            with open(file_path, 'w') as f:
                f.writelines(lines)
            print(f"Updated: {file_path} (backup created)")
            return True
        else:
            print(f"Warning: No tags line found in: {file_path}")
            # Remove backup since no changes were made
            backup_path = f"{file_path}.backup"
            if os.path.exists(backup_path):
                os.remove(backup_path)
            return False

    except Exception as e:
        print(f"Error updating {file_path}: {e}")
        return False


def main():
    # Path to the tag mapping file
    mapping_file = 'misc.txt'

    if not os.path.exists(mapping_file):
        print(f"Error: Mapping file '{mapping_file}' not found!")
        return

    # Parse the tag mapping
    print("Parsing tag mapping...")
    file_tags = parse_tag_mapping(mapping_file)
    print(f"Found {len(file_tags)} files to update")

    # Update each file
    updated_count = 0
    for file_path, tags in file_tags.items():
        if update_file_tags(file_path, tags):
            updated_count += 1

    print(f"\nCompleted! Updated {updated_count} out of {len(file_tags)} files.")
    print(f"Backup files created with .backup extension")
    print("To remove all backups, run: find . -name '*.backup' -delete")


if __name__ == "__main__":
    main()
#!/bin/bash

# Directory to scan
TARGET_DIR="${1:-.}"

# File extension for backups
BACKUP_SUFFIX=".bak"

# Find all Markdown files recursively
find "$TARGET_DIR" -type f -name "*.md" | while read -r file; do
  echo "Linting and fixing: $file"

  # Backup original
  cp "$file" "$file$BACKUP_SUFFIX"

  # Run markdownlint-cli2 with autofix
  markdownlint-cli2 "$file" --fix
done

echo "✅ Linting complete. Backups saved with '$BACKUP_SUFFIX' suffix."

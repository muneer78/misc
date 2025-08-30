#!/bin/bash

# Directory to scan
TARGET_DIR="${1:-.}"

# Find all .md.bak files recursively
find "$TARGET_DIR" -type f -name "*.md.bak" | while read -r bak_file; do
  # Derive original file name (strip .bak)
  original_file="${bak_file%.bak}"

  echo "Restoring $bak_file -> $original_file"

  # Remove the updated file
  rm -f "$original_file"

  # Move the backup back to original name
  mv "$bak_file" "$original_file"
done

echo "✅ Restoration complete. Updated files removed."

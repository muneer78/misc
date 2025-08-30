#!/bin/bash

# Path to your directory
directory="/Users/muneer78/Desktop/test"

# Loop through all .md files in the directory
for file in "$directory"/*.md; do
  # Create a backup
  cp "$file" "$file.bak"  
  
  # Remove quotes around the title (corrected for your example)
  sed -E 's/^title\s*"([^"]*)"/title: \1/' "$file" > temp && mv temp "$file"
done

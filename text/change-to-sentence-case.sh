#!/bin/bash

# Path to your directory
directory="/Users/muneer78/Desktop/test"

# Loop through all .md files in the directory
for file in "$directory"/*.md; do
  cp "$file" "$file.bak"  # Create a backup
  
  # Remove "UL" after title and convert to sentence case
  sed -E 's/^title: ULUL(.*)/title: \1/' "$file" | \
  sed -E 's/(title: )(.)/\1\U\2/' | \
  sed -E 's/(title: .)(.*)/\1\L\2/' > temp && mv temp "$file"
done

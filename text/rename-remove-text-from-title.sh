#!/bin/bash

# Path to your directory
directory="/Users/muneer78/Desktop/test"

# Loop through all .md files in the directory
for file in "$directory"/*.md; do
  cp "$file" "$file.bak"  # Create a backup
  
  # Process the file with awk
  awk -F': ' '
  /^title:/ {
      gsub(/^UL/, "", $2);              # Remove "UL" from the title
      $2 = toupper(substr($2, 1, 1)) substr($2, 2);  # Capitalize first letter
      $2 = substr($2, 1, 1) tolower(substr($2, 2));  # Retain first letter and lowercase the rest
  }
  { print }
  ' "$file" > temp && mv temp "$file"
done

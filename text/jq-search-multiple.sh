#!/bin/bash

# Directory to search
directory="."  # Replace with the path to your JSON files directory
# Search string
search_string="3870948"

# Flag to track if any JSON files are found or matches found
found_json=false
found_match=false

# Find all JSON files in the directory and its subdirectories
find "$directory" -type f -name "*.json" | while read -r file; do
    found_json=true
    
    # Use jq to search for the term in each JSON file
    matches=$(jq --arg search "$search_string" \
        'paths(scalars) as $p | select(getpath($p) | contains($search)) | $p' "$file" 2>/dev/null)
    
    if [ -n "$matches" ]; then
        found_match=true
        echo "Found '$search_string' in file: $file"
    fi
done

# Check flags and print appropriate messages if no JSON files or matches are found
if ! $found_json; then
    echo "No JSON files in directory"
elif ! $found_match; then
    echo "Search term not found"
fi

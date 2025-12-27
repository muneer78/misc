#!/bin/bash

# Directory path containing the files
directory_path="$1"

# Iterate over each file in the directory
for filepath in "$directory_path"/*; do
    # Skip directories
    if [ -d "$filepath" ]; then
        continue
    fi

    # Extract the filename from the path
    filename=$(basename "$filepath")

    # Convert filename to lowercase, replace whitespace with dashes, and remove commas and apostrophes
    new_filename=$(echo "$filename" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr '_' '-' | tr -d ',\()' | sed "s/playboy's/playboys/g")

    # Rename the file
    new_filepath="$directory_path/$new_filename"

    if mv "$filepath" "$new_filepath"; then
        echo "Renamed: $filename to $new_filename"
    else
        echo "Error renaming file: $filepath"
    fi
done

echo "File renaming complete."

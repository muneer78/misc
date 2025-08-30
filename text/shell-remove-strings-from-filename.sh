#!/bin/bash

# Get the current directory where the script is run
directory_path="$1"

# Iterate over each file in the directory
for filepath in "$directory_path"/*; do
    # Skip directories
    if [ -d "$filepath" ]; then
        continue
    fi

    # Extract the filename from the path
    filename=$(basename "$filepath")

    # Remove the string 'playboy_usa_' and change underscores to dashes
    new_filename=$(echo "$filename" | sed 's/playboy_usa_//g' | tr '_' '-')

    # Rename the file
    new_filepath="$directory_path/$new_filename"

    if mv "$filepath" "$new_filepath"; then
        echo "Renamed: $filename to $new_filename"
    else
        echo "Error renaming file: $filepath"
    fi
done

echo "File renaming complete."
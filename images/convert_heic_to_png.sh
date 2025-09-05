#!/bin/bash

# Check if a folder path is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <folder_path>"
    exit 1
fi

folder_path="$1"

# Check if the provided path is a valid directory
if [ ! -d "$folder_path" ]; then
    echo "Error: Directory not found at $folder_path"
    exit 1
fi

# Loop through all .heic files in the specified folder
for file in "$folder_path"/*.heic; do
    # Check if the file exists (prevents error if no .heic files are found)
    if [ -f "$file" ]; then
        # Use basename to get just the filename without the path
        filename=$(basename "$file")
        # Use dirname to get the directory path
        directory=$(dirname "$file")

        # Convert the file and save the output in the same directory
        sips -s format png "$file" --out "$directory/${filename%.heic}.png"
        echo "Converted $file to $directory/${filename%.heic}.png"
    fi
done
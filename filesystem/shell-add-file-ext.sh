#!/bin/bash

# Define the pattern to match filenames starting with 'business'
pattern="^business"

# Set directory
directory="/mnt/c/Users/mahmad/OneDrive - Ryan RTS/Downloads/checks" # Change to your desired path

# Check if directory exists
if [[ ! -d "$directory" ]]; then
    echo "Directory does not exist: $directory"
    exit 1
fi

# Find files matching the pattern and not ending in '.csv'
find "$directory" -type f ! -name "*.csv" -name "$pattern*" | while read -r file; do
    # Get the base filename
    filename=$(basename "$file")
    
    # Append '.csv' to the filename
    new_filename="${filename}.csv"
    
    # Rename the file
    mv "$file" "$directory/$new_filename"
    echo "Renamed: $filename to $new_filename"
done

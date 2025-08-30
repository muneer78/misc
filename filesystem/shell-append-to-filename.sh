#!/bin/bash

# Function to prepend a prefix to filenames in a given directory
prepend_to_filenames() {
    local directory=$1
    local prefix=$2
    
    # Loop through all files in the directory
    for filename in "$directory"/*; do
        # Check if it's a file (not a directory)
        if [ -f "$filename" ]; then
            # Get the base filename (without the path)
            base_filename=$(basename "$filename")
            
            # Create the new filename by adding the prefix
            new_filename="$directory/$prefix$base_filename"
            
            # Rename the file
            mv "$filename" "$new_filename"
            echo "Renamed: $base_filename -> $prefix$base_filename"
        fi
    done
}

# Example usage
directory_path="path/to/your/directory"  # Replace with your directory path
prefix_string="polars-"  # Replace with your desired prefix
prepend_to_filenames "$directory_path" "$prefix_string"

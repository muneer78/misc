#!/bin/bash

# Base directory
base_dir="/Users/muneer78/code"
unmatched_dir="$base_dir/unmatched"

# Create the unmatched directory if it doesn't exist
mkdir -p "$unmatched_dir"

# Find all files in the base directory (excluding subdirectories)
find "$base_dir" -maxdepth 1 -type f > base_files.txt

# Find all files in the specified subdirectories
find "$base_dir/fantasy-sports" "$base_dir/betlog" "$base_dir/misc" "$base_dir/utils" -type f > sub_files.txt

# Total counts for progress
total_base_files=$(wc -l < base_files.txt)
base_count=0

echo "Processing base directory files..."
# Process files in the base directory
while IFS= read -r base_file; do
    base_count=$((base_count + 1))
    base_filename=$(basename "$base_file")
    matched=false
    while IFS= read -r sub_file; do
        sub_filename=$(basename "$sub_file")
        if [ "$base_filename" == "$sub_filename" ]; then
            matched=true
            break
        fi
    done < sub_files.txt
    if [ "$matched" = false ]; then
        echo "[$base_count/$total_base_files] Moving unmatched file: $base_file"
        mv "$base_file" "$unmatched_dir/"
    else
        echo "[$base_count/$total_base_files] Matched: $base_file"
    fi
done < base_files.txt

# Cleanup
rm base_files.txt sub_files.txt

echo "Unmatched files moved to $unmatched_dir."

#!/bin/bash

# Path to your directory
directory="/Users/muneer78/Desktop/test"

# Loop through all .bak files in the directory
for bak_file in "$directory"/*.bak; do
  # Get the original file name by removing the .bak extension
  original_file="${bak_file%.bak}"
  
  # Restore the original file from the backup
  mv "$bak_file" "$original_file"
done

#!/bin/bash

# Change to the directory containing your images
cd /Users/muneer78/Downloads/convert-images

# Create a list of all image files (adjust the pattern as needed)
files=(*.jpg *.png *.jpeg *.JPG *.heic)

# Get the total number of files
count=${#files[@]}

# Loop through the files for pairwise comparison
for ((i = 0; i < count; i++)); do
  for ((j = i + 1; j < count; j++)); do
    file1="${files[i]}"
    file2="${files[j]}"

    # Use 'cmp -s' to run the comparison silently
    if cmp -s "$file1" "$file2"; then
      echo "✅ The following images are identical: $file1 and $file2"
    fi
  done
done
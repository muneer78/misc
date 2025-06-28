#!/bin/zsh

img_dir="/Users/muneer78/Downloads/convert-images"  # <-- Set this to your images directory

cd "$img_dir" || { echo "Directory not found: $img_dir"; exit 1; }

# Find all images with the specified extensions (case-insensitive)
find . -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.avif" -o -iname "*.heic" -o -iname "*.webp" \) | while read -r img; do
    filename="${img%.*}"
    magick convert "$img" "$filename.png"
    echo "Converted $img to $filename.png"
    rm "$img"
    echo "Removed original file: $img"
    echo "Conversion complete for $filename"
    echo "-----------------------------------"
done
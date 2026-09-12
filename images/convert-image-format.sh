#!/bin/zsh
img_dir="/Users/muneer78/Downloads/convert-images"  # <-- Set this to your images directory
cd "$img_dir" || { echo "Directory not found: $img_dir"; exit 1; }

# Find all images with the specified extensions (case-insensitive)
find . -maxdepth 1 -type f \( -iname "*.jpg" -o -iname "*.jpeg" -o -iname "*.avif" -o -iname "*.heic" -o -iname "*.webp" \) | while read -r img; do
    filename="${img%.*}"
    output="${filename}.png"

    if sips -s format png "$img" --out "$output" >/dev/null 2>&1; then
        echo "Converted $img to $output"
        rm "$img"
        echo "Removed original file: $img"
    else
        echo "FAILED to convert $img — original left in place"
    fi
    echo "-----------------------------------"
done

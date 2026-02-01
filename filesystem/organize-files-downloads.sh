#!/bin/bash

# Set the target directory (convert to absolute path for safety)
TARGET_DIR="/Users/muneer78/Downloads"

# Ensure relative destination folders exist
mkdir -p "$TARGET_DIR/docs"
mkdir -p "$TARGET_DIR/pics"
mkdir -p "$TARGET_DIR/convert-images"
mkdir -p "$TARGET_DIR/videos"
mkdir -p "$TARGET_DIR/data"

# Function to move files by extension
move_files() {
    local subdir=$1
    shift
    local ext_list=("$@")

    for ext in "${ext_list[@]}"; do
        echo "Moving *.$ext to $subdir..."
        mv "$TARGET_DIR"/*."$ext" "$TARGET_DIR/$subdir" 2>/dev/null || echo "No files with extension .$ext found."
    done
}

# Organize files
move_files "docs" txt pdf md epub csv
move_files "docs" epub azw3 mobi
move_files "pics" jpg jpeg gif png
move_files "convert-images" webp avif heic
move_files "videos" mp4 mov avi
move_files "data" xml json html xlsx opml zip

echo "All done organizing files in '$TARGET_DIR'!"
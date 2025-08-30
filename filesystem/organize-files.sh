#!/bin/bash

# Check if a directory was passed as an argument
if [ $# -lt 1 ]; then
    echo "Usage: $0 <directory-to-organize>"
    exit 1
fi

# Set the target directory (convert to absolute path for safety)
TARGET_DIR=$(realpath "$1")

# Verify the target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: Directory '$TARGET_DIR' does not exist."
    exit 1
fi

# Ensure relative destination folders exist
mkdir -p "$TARGET_DIR/docs"
mkdir -p "$TARGET_DIR/images"
mkdir -p "$TARGET_DIR/convert-images"
mkdir -p "$TARGET_DIR/videos"

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
move_files "docs" txt pdf md docx
move_files "images" jpg jpeg gif png
move_files "convert-images" webp
move_files "videos" mp4 mov

echo "All done organizing files in '$TARGET_DIR'!"

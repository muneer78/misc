#!/bin/zsh

# Define the trash directory
TRASH_DIR="$HOME/.Trash"

# Check if a directory is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Get the directory from the command line argument
DIR="$1"

# Check if the provided path is a directory
if [ ! -d "$DIR" ]; then
    echo "Error: Provided path is not a directory."
    exit 1
fi

# Find and move all .webp files to the trash
echo "Moving .webp files from $DIR to trash:"
find "$DIR" -type f -name "*.webp" -exec mv {} "$TRASH_DIR" \;

echo "Operation completed."
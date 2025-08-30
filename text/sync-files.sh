#!/bin/zsh

# Define source directories
SOURCE_DIR1="/Users/muneer78/Documents/Projects/betlog/"
SOURCE_DIR2="/Users/muneer78/Documents/Projects/misc/"
SOURCE_DIR3="/Users/muneer78/Documents/Projects/misc/"
SOURCE_DIR4="/Users/muneer78/Documents/Projects/misc/"

# Define destination directory
DEST_DIR="/Users/muneer78/code/"

# Sync files from both source directories into the destination
rsync -avu --no-relative --progress --exclude=".*" "$SOURCE_DIR1" "$SOURCE_DIR2" "$SOURCE_DIR3" "$SOURCE_DIR4" "$DEST_DIR"

echo "Sync completed!"

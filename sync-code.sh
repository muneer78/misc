#!/bin/zsh

# Define source directories
SOURCE_DIR1="/Users/muneer78/Documents/Projects/betlog/"
SOURCE_DIR2="/Users/muneer78/Documents/Projects/fantasy-sports//"
SOURCE_DIR3="/Users/muneer78/Documents/Projects/misc/"
SOURCE_DIR4="/Users/muneer78/Documents/Projects/utils/"
SOURCE_DIR5="/Users/muneer78/scripts/"

# Define destination directory
DEST_DIR="/Users/muneer78/code/"

# Sync each source directory into a same-named directory in the destination
rsync -avu --progress --exclude="*venv/" --exclude=".*" "$SOURCE_DIR1" "$DEST_DIR/betlog/"
rsync -avu --progress --exclude="*venv/" --exclude=".*" "$SOURCE_DIR2" "$DEST_DIR/fantasy-sports/"
rsync -avu --progress --exclude="*venv/" --exclude=".*" "$SOURCE_DIR3" "$DEST_DIR/misc/"
rsync -avu --progress --exclude="*venv/" --exclude=".*" "$SOURCE_DIR4" "$DEST_DIR/utils/"
rsync -avu --progress --exclude="*venv/" --exclude=".*" "$SOURCE_DIR5" "$DEST_DIR/misc/"

echo "Sync completed!"

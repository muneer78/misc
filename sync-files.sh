# #!/bin/zsh

# # Define source directories
# SOURCE_DIR1="/Users/muneer78/Documents/Projects/betlog/"
# SOURCE_DIR2="/Users/muneer78/Documents/Projects/misc/"
# SOURCE_DIR3="/Users/muneer78/Documents/Projects/misc/"
# SOURCE_DIR4="/Users/muneer78/Documents/Projects/misc/"

# # Define destination directory
# DEST_DIR="/Users/muneer78/code/"

# # Sync files from both source directories into the destination
# rsync -avu --no-relative --progress --exclude=".*" "$SOURCE_DIR1" "$SOURCE_DIR2" "$SOURCE_DIR3" "$SOURCE_DIR4" "$DEST_DIR"

# echo "Sync completed!"

# # To sync music folders, rsync -avu --no-relative --progress "/Users/muneer78/Library/CloudStorage/GoogleDrive-reenum@gmail.com/My Drive/Music" "/Users/muneer78/Cloud-Drive/Music"

#!/bin/zsh

#!/bin/zsh

# Define source directories
SOURCE_DIR1="/Users/muneer78/Documents/Projects/betlog/"
SOURCE_DIR2="/Users/muneer78/Documents/Projects/fantasy-sports//"
SOURCE_DIR3="/Users/muneer78/Documents/Projects/misc/"
SOURCE_DIR4="/Users/muneer78/Documents/Projects/utils/"

# Define destination directory
DEST_DIR="/Users/muneer78/code/"

# Sync each source directory into a same-named directory in the destination
rsync -avu --progress --exclude="*venv/" --exclude=".*" "$SOURCE_DIR1" "$DEST_DIR/betlog/"
rsync -avu --progress --exclude="*venv/" --exclude=".*" "$SOURCE_DIR2" "$DEST_DIR/fantasy-sports/"
rsync -avu --progress --exclude="*venv/" --exclude=".*" "$SOURCE_DIR3" "$DEST_DIR/misc/"
rsync -avu --progress --exclude="*venv/" --exclude=".*" "$SOURCE_DIR4" "$DEST_DIR/utils/"

echo "Sync completed!"

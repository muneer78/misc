#!/bin/zsh

# Define source directories for each category
declare -A SOURCE_DIRECTORIES=(
    [docs]="/Users/muneer78/Downloads/docs"
    [ebooks]="/Users/muneer78/Downloads/docs"
    [images]="/Users/muneer78/Downloads/images"
    [videos]="/Users/muneer78/Downloads/videos"
)

# Define target directories and file extensions
declare -A FILE_CATEGORIES=(
    [docs]="/Users/muneer78/reading/docs:txt pdf md docx"
    [ebooks]="/Users/muneer78/reading/ebooks:epub"
    [images]="/Users/muneer78/images:jpg jpeg gif png"
    [videos]="/Users/muneer78/Library/CloudStorage/GoogleDrive-reenum@gmail.com/My Drive/PB/videos:mp4 mov"
)

# Function to move files by extension
move_files() {
    local source_dir=$1
    local target_dir=$2
    shift 2
    local ext_list=("$@")

    # Ensure the target directory exists
    mkdir -p "$target_dir"

    # Move files matching the extensions
    for ext in "${ext_list[@]}"; do
        echo "Moving *.$ext from $source_dir to $target_dir..."
        mv "$source_dir"/*."$ext" "$target_dir" 2>/dev/null || echo "No files with extension .$ext found in $source_dir."
    done
}

# Organize files based on source and target directories
for category in ${(k)FILE_CATEGORIES}; do
    target_and_extensions=(${(s/:/)FILE_CATEGORIES[$category]}) # Split target and extensions
    target_dir=$target_and_extensions[1]
    extensions=(${(@s/ /)target_and_extensions[2]}) # Get all extensions
    source_dir=$SOURCE_DIRECTORIES[$category] # Get source directory

    # Ensure the source directory exists
    if [ -d "$source_dir" ]; then
        move_files "$source_dir" "$target_dir" "${extensions[@]}"
    else
        echo "Source directory $source_dir does not exist for category $category. Skipping."
    fi
done

echo "All done organizing files!"
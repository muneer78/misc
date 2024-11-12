#!/bin/zsh

if [ -z "$1" ]; then
    echo "Please specify a directory."
    exit 1
fi

target_dir="$1"

if [ ! -d "$target_dir" ]; then
    echo "Directory '$target_dir' does not exist."
    exit 1
fi

found_files=0  # Flag to track if any files are found

for file in "$target_dir"/*.rtf; do
    if [[ -e "$file" ]]; then
        found_files=1
        echo "Processing $file..."

        filename="${file%.*}"
        pandoc "$file" -f rtf -t markdown -o "${filename}.md" && \
        echo "Converted $file to ${filename}.md" || \
        echo "Failed to convert $file"
    fi
done

if [[ $found_files -eq 0 ]]; then
    echo "No .rtf files found in $target_dir."
fi

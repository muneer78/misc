#!/bin/bash

# Define the directory to organize
DIRECTORY="$1"

# # Check if the directory exists
# if [ ! -d "$DIRECTORY" ]; then
#   echo "Directory does not exist."
#   exit 1
# fi

# Create folders for different file types
mkdir -p "$DIRECTORY/documents"
mkdir -p "$DIRECTORY/ebooks"

# # Move files into their respective folders
# for file in "$DIRECTORY"/*; do
#   case "${file##*.}" in
#     jpg|jpeg|png|gif)
#       mv "$file" "$DIRECTORY/images/"
#       ;;
#     pdf|doc|docx|txt|md)
#       mv "$file" "$DIRECTORY/documents/"
#       ;;
#     mp4|mkv|avi|gif)
#       mv "$file" "$DIRECTORY/videos/"
#       ;;
#     *)
#       echo "File type not recognized: $file"
#       ;;
#   esac
# done

# Move files into their respective folders
for file in "$DIRECTORY"/*; do
  case "${file##*.}" in
    pdf|doc|docx|txt|md|html)
      mv "$file" "$DIRECTORY/documents/"
      ;;
    epub|mobi|azw3)
      mv "$file" "$DIRECTORY/ebooks/"
      ;;
    *)
      echo "File type not recognized: $file"
      ;;
  esac
done

echo "Files organized successfully!"
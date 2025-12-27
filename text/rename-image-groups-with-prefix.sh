#!/bin/bash
# Set the directory here
DIR="/Users/muneer78/Downloads/convert-images/"
# Check if exiftool is installed
if ! command -v exiftool &> /dev/null
then
    echo "exiftool could not be found. Please install it first."
    exit 1
fi
# Define the prefix here
PREFIX="toasty-"

# Use a temporary file to store the list of files and their EXIF dates
TEMP_LIST=$(mktemp)
echo "Gathering files and EXIF data..."
# The key change is adding -FileExtension to the exiftool command
# We will use -filename to get the base filename and -FileExtension to get the extension
exiftool -T -n -d "%Y%m%d_%H%M%S" -DateTimeOriginal -FileModifyDate -FileName -FileExtension -r -ext JPG -ext jpg -ext jpeg -ext png -ext heic "$DIR" > "$TEMP_LIST"
# Check if the temporary file is empty
if [ ! -s "$TEMP_LIST" ]; then
    echo "No images with EXIF data found in $DIR. Exiting."
    rm "$TEMP_LIST"
    exit 1
fi
echo "Sorting files and preparing to rename..."
counter=1
sort -k1,1 "$TEMP_LIST" | while IFS=$'\t' read -r creation_date modify_date filename extension; do
    # Use the modify date as a fallback
    final_date=$creation_date
    if [ -z "$final_date" ]; then
        final_date=$modify_date
    fi
    
    # Check if a valid date was found
    if [ ! -z "$final_date" ]; then
        # Clean up the extension - remove any unwanted characters and ensure it's valid
        # If extension is empty or invalid, extract it from the original filename
        if [ -z "$extension" ] || [ "$extension" = "-" ]; then
            extension="${filename##*.}"
            echo "Warning: Using fallback extension '$extension' for file '$filename'"
        fi
        
        # Ensure extension doesn't start with a dot (exiftool returns without dot)
        extension="${extension#.}"
        
        # Validate that we have a proper extension
        if [ -z "$extension" ] || [ "$extension" = "$filename" ]; then
            echo "Warning: Could not determine extension for '$filename', skipping."
            continue
        fi
        
        # Create the new filename with the prefix and the original extension
        new_name="${PREFIX}${counter}.${extension}"
        old_filepath="${DIR}/${filename}"
        new_filepath="${DIR}/${new_name}"
        
        # Check if source file exists
        if [ ! -f "$old_filepath" ]; then
            echo "Warning: Source file '$old_filepath' does not exist, skipping."
            continue
        fi
        
        # Rename the file, only if the new name doesn't exist
        if mv -n "$old_filepath" "$new_filepath" 2>/dev/null; then
            echo "Renamed '$filename' to '$new_name'"
            # Increment the counter only on successful rename
            ((counter++))
        else
            echo "Warning: Could not rename '$filename' to '$new_name' (file may already exist)"
        fi
    else
        echo "No EXIF or modify date found for '$filename', skipping."
    fi
done
# Clean up the temporary file
rm "$TEMP_LIST"
echo "All eligible files have been processed."

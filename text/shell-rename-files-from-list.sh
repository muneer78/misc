#!/bin/bash

# Directory path containing the files
directory_path="/Users/muneer78/Desktop/saved"

# Path to the CSV file (the file should be in the same directory)
csv_file="updated_file.csv"

# Iterate over each file in the directory
for filename in "$directory_path"/*; do
    # Skip directories and the updated_file.csv file itself
    if [ -d "$filename" ] || [[ "$filename" == *"updated_file.csv" ]]; then
        continue
    fi

    # Read through each line of the CSV file
    while IFS=',' read -r title postdate; do
        # Skip the header of the CSV
        if [ "$title" == "title" ]; then
            continue
        fi

        # Check if the filename contains the title from the CSV
        if [[ "$filename" == *"$title"* ]]; then
            # Extract the date from the filename (using the regex for YYYY-MM-DD)
            if [[ "$filename" =~ ([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
                date="${BASH_REMATCH[1]}"
                # Replace the date portion of the filename with the postdate from the CSV
                new_filename="${filename/$date/$postdate}"
                
                # Rename the file
                old_file="$directory_path/$filename"
                new_file="$directory_path/$new_filename"
                mv "$old_file" "$new_file"
                echo "Renamed: $filename to $new_filename"
            fi
        fi
    done < "$csv_file"
done

echo "File renaming complete."

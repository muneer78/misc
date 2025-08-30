#!/bin/bash

# Directory path containing the files
directory_path="/Users/muneer78/Desktop/saved"

# Output file to store extracted filenames and dates
output_file="filenames_with_dates.txt"

# Clear the output file if it exists
> "$output_file"

# Iterate over each file in the directory
for filename in "$directory_path"/*; do
    # Skip directories and the updated_file.csv file itself
    if [ -d "$filename" ] || [[ "$filename" == *"updated_file.csv" ]]; then
        continue
    fi

    # Extract the date from the filename using a regex (YYYY-MM-DD format)
    if [[ "$filename" =~ ([0-9]{4}-[0-9]{2}-[0-9]{2}) ]]; then
        date="${BASH_REMATCH[1]}"
        # Output the filename and extracted date to the output file
        echo "$filename,$date" >> "$output_file"
    fi
done

echo "Date extraction complete. Results saved in '$output_file'."

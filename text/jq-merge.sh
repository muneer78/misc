#!/bin/bash

# Directory containing JSON files
directory="/path/to/your/json/files"
# Output file for merged JSON
output_file="/path/to/your/merged_output.json"
# Output file for non-JSON content
non_json_file="/path/to/your/non_json_content.txt"

# Ensure the directory exists
if [ ! -d "$directory" ]; then
    echo "Directory does not exist: $directory"
    exit 1
fi

# Initialize an array to hold valid JSON data
merged_data="[]"
# Initialize the non-JSON output file
> "$non_json_file"

# Iterate through all JSON files in the directory
for file in "$directory"/*.json; do
    # Check if the file exists and is not empty
    [ -e "$file" ] || continue

    # Delete the first line from the file
    tail -n +2 "$file" > "${file}.tmp" && mv "${file}.tmp" "$file"

    # Check if the modified file is valid JSON
    if jq empty "$file" 2>/dev/null; then
        # Merge JSON content
        merged_data=$(jq -s 'add' <(echo "$merged_data") "$file")
    else
        # If invalid JSON, store its content in the non-JSON file
        echo "Non-JSON content found in file: $file" >> "$non_json_file"
        cat "$file" >> "$non_json_file"
        echo -e "\n\n" >> "$non_json_file"
    fi
done

# Write the merged JSON data to the output file
echo "$merged_data" | jq '.' > "$output_file"

echo "JSON files merged into $output_file"
echo "Non-JSON content written to $non_json_file"

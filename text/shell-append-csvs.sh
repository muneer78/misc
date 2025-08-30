#!/bin/bash

# Define the identifier for the output file
identifier="DS5088"

# Directory containing CSV files
directory_path="path/to/your/csv_files_directory"

# Temporary file to hold concatenated data
temp_file="temp_combined.csv"
> "$temp_file"  # Empty the file if it exists

# Get a list of all CSV files in the directory
csv_files=("$directory_path"/*.csv)

# Add header from the first file and append the rest
if [ -f "${csv_files[0]}" ]; then
    head -n 1 "${csv_files[0]}" > "$temp_file"
fi

for file in "${csv_files[@]}"; do
    tail -n +2 "$file" >> "$temp_file"  # Append data, skipping header in each file
done

# Remove duplicates and sort by "_id" column in descending order
# Assuming _id is in the first column; adjust if necessary.
sort -u -t, -k1,1 -r "$temp_file" > "${identifier}_all_records.csv"

# Count records and report
initial_count=$(wc -l < "$temp_file")
final_count=$(wc -l < "${identifier}_all_records.csv")
dropped_count=$((initial_count - final_count))

echo "Initial number of records: $initial_count"
echo "Number of unique records: $final_count"
echo "Number of dropped records: $dropped_count"

# Cleanup temporary file
rm "$temp_file"

echo "CSV files in $directory_path have been successfully appended."

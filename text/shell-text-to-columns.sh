#!/bin/bash

# Sample data (you can replace this with an actual file if needed)
input_data=(
    "John, Doe, 30"
    "Jane, Smith, 25"
    "Alice, Johnson, 40"
)

# Output CSV file name
output_filename="output.csv"

# Initialize the CSV file with headers
echo "col_1,col_2,col_3" > "$output_filename"

# Process each line in the input data
for line in "${input_data[@]}"; do
    # Split the line by ", " (comma and space) and store values into variables
    IFS=', ' read -r col1 col2 col3 <<< "$line"
    
    # Append the result to the output file
    echo "$col1,$col2,$col3" >> "$output_filename"
done

echo "Data has been written to $output_filename"

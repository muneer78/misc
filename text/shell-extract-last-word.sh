#!/bin/bash

# Input CSV file
input_file="data.csv"

# Output file to store results
output_file="output.csv"

# Print the header for the output
echo "Text,Last_Word" > "$output_file"

# Process each line in the CSV file (skip the header)
tail -n +2 "$input_file" | while IFS=, read -r text; do
    # Extract the last word from the text column using awk
    last_word=$(echo "$text" | awk '{print $NF}')
    
    # Output the text and the last word to the output file
    echo "$text,$last_word" >> "$output_file"
done

# Display the result
cat "$output_file"

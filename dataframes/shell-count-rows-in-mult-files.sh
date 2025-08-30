#!/bin/bash

# Function to print results (column counts, etc.)
print_results() {
    output_file=$1
    title=$2

    # Count the total number of rows in the file
    total_rows=$(wc -l < "$output_file")
    echo "Total rows: $total_rows"
    
    echo "$title:"

    # Get header (first line of the CSV)
    header=$(head -n 1 "$output_file")
    IFS=',' read -ra columns <<< "$header"

    # For each column, count occurrences of each unique value (excluding header)
    for column in "${columns[@]}"; do
        # Count unique occurrences of values in the column (assuming CSV format)
        count=$(awk -F',' -v col="$column" '
        BEGIN {OFS=","}
        NR > 1 {count[$col]++} 
        END {for (val in count) print val, count[val]}
        ' "$output_file")

        echo "$column:"
        echo "$count"
    done
    echo ""
}

# Example usage
output_file="combined_file.csv"
title="Column Counts"

# Step 1: Print column counts
print_results "$output_file" "$title"

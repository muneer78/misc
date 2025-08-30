#!/bin/bash

# Input and output files
input_file="SalesforceProposedNationalOriginValues.csv"
output_file="NationalOriginValues.csv"

# Check if the input file exists
if [[ ! -f "$input_file" ]]; then
    echo "File not found: $input_file"
    exit 1
fi

# Extract the header
header=$(head -n 1 "$input_file")

# Process the file (ignoring the header) with the following steps:
# 1. Trim spaces from `Country_of_Origin` column (assuming it's the second column).
# 2. Sort by `LanguageInSalesforce` column (assuming it's the first column) in a case-insensitive manner.
tail -n +2 "$input_file" | \
    awk -F, '{
        # Trim leading/trailing spaces in Country_of_Origin (2nd column)
        gsub(/^[ \t]+|[ \t]+$/, "", $2)
        print $0
    }' | \
    sort -t, -k1,1 -f | \
    awk -v header="$header" 'BEGIN {print header} {print}' > "$output_file"

echo "Done. Output saved to $output_file"

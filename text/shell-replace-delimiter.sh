#!/bin/bash

# Input and output files
input_file="TransactionSummaryLLCGrp_Daily_184835_05-09-2024.csv"
output_file="TransactionSummaryLLCGrp_Daily_184835_05-09-2024v2.csv"

# Check if the input file exists
if [[ ! -f "$input_file" ]]; then
    echo "File not found: $input_file"
    exit 1
fi

# Read, replace '|' with ',', and write to the output file
awk '{gsub(/\|/, ","); print}' "$input_file" > "$output_file"

echo "File processed and saved as: $output_file"

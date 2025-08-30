#!/bin/bash

# Input text file
input_file="concentrations.txt"
output_file="output_file.csv"

# Temporary file to store intermediate results
temp_file="temp_output.txt"

# Function to process text based on the given pattern
process_text() {
    local text="$1"
    if [[ "$text" =~ (.+\ LLC) ]]; then
        echo "${BASH_REMATCH[1]}" | tr '[:lower:]' '[:upper:]'
    else
        echo "$text" | tr '[:lower:]' '[:upper:]'
    fi
}

# Function to convert AR values from 'k' or 'K' to integer
convert_ar_to_integer() {
    local value="$1"
    if [[ "$value" =~ [kK]$ ]]; then
        value="${value//[kK]/000}"
    fi
    echo "$value" | grep -o '[0-9]*' | head -n 1
}

# Process the input file
{
    # Read the header and write it to the output file
    read -r header
    echo "$header" > "$output_file"

    # Iterate over each line of the file, skipping the header
    while IFS=',' read -r client_name debtor ar include date_added ff_date; do
        # Skip the line if 'Include' column is not 1
        if [ "$include" -ne 1 ]; then
            continue
        fi
        
        # Process 'Client Name' and 'Debtor'
        client_name=$(process_text "$client_name")
        debtor=$(process_text "$debtor")

        # Process 'AR' column
        ar=$(convert_ar_to_integer "$ar")

        # Convert 'Date Added' and 'FF Date' to 'YYYY-MM-DD' format (assuming input in a recognizable format)
        date_added=$(date -d "$date_added" +'%Y-%m-%d' 2>/dev/null || echo "$date_added")
        ff_date=$(date -d "$ff_date" +'%Y-%m-%d' 2>/dev/null || echo "$ff_date")

        # Output the processed line to the temporary file
        echo "$client_name,$debtor,$ar,$date_added,$ff_date" >> "$temp_file"
    done < "$input_file"

    # Sort by 'Client Name' and 'Debtor' columns (assuming they are the 1st and 2nd columns)
    sort -t',' -k1,1 -k2,2 "$temp_file" >> "$output_file"

    # Clean up temporary file
    rm "$temp_file"
} 

echo "Processing complete. Results saved in '$output_file'."

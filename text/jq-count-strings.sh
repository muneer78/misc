#!/bin/bash

# Input text
text='{"error":"DUPLICATES_DETECTED","fields":'

# Use jq to extract the text after "{" and before ","
output=$(echo "$text" | jq -R 'capture("\\{(?<match>[^,]+),") | .match' 2>/dev/null)

# Print the result
echo "$output"

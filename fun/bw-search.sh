#!/bin/bash

# Prompt for the search term
read -p "Enter the search term: " search_term

# Run the Bitwarden CLI command with the search term
bw --response --pretty list items --search "$search_term" | jq -r '
  .data.data[] |
  select(.object == "item") |
  "Name: \(.name)\nRevision Date: \(.revisionDate[0:10])\nID: \(.id)\nUsername: \(.login.username // "N/A")\nPassword: \(.login.password // "N/A")\n"
'
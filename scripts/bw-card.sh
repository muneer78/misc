#!/bin/bash

# Run the Bitwarden CLI command with the search term
bw get item c2f868a2-b09d-45d1-83ec-af81001c21f8 --pretty | jq -r '
  select(.object == "item") |
  "Number: \(.card.number // "N/A")\nExpiry Month: \(.card.expMonth // "N/A")\nExpiry Year: \(.card.expYear // "N/A")\nCVV: \(.card.code // "N/A")"'

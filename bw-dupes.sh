#!/bin/bash

# Search the entire vault for entries grouped by domain and similar names
bw --response --pretty list items | jq -r '
  .data.data[] |
  select(.object == "item" and .login.uris != null) |
  .login.uris[] |
  select(.uri != null) |
  {
    domain: (.uri | capture("(?<=://)([^/]+)") | .["1"]),
    name: .name,
    revisionDate: (.revisionDate | .[:10]),
    id: .id,
    username: (.login.username // "N/A"),
    password: (.login.password // "N/A")
  }' | jq -s '
  group_by(.domain)[] |
  select(.domain != null) |
  .[0].domain as $domain |
  { ($domain): . }' | jq -r '.'

# Compare names for 90% similarity
python3 - <<EOF
import sys
import json
from difflib import SequenceMatcher

# Load grouped JSON output
data = json.load(sys.stdin)

# Function to calculate similarity
def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

# Find and print similar names
for domain, entries in data.items():
    print(f"\nDomain: {domain}")
    names = [entry['name'] for entry in entries if 'name' in entry]
    for i, name1 in enumerate(names):
        for name2 in names[i + 1:]:
            if similar(name1, name2) >= 0.9:
                print(f"Similar names: {name1} and {name2}")
EOF
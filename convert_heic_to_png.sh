#!/bin/bash

for file in *.heic; do
    if [[ -f "$file" ]]; then
        sips -s format png "$file" --out "${file%.heic}.png"
        echo "Converted $file to ${file%.heic}.png"
    fi
done

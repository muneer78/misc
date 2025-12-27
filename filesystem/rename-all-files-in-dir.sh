#!/bin/bash

directory='/Users/muneer78/Downloads/'

for filepath in "$directory"/*; do
  if [[ -f "$filepath" ]]; then
    filename=$(basename "$filepath")
    extension="${filename##*.}"
    name="${filename%.*}"

    # Replace spaces and underscores with dashes
    newname=$(echo "$name" | sed -E 's/[ _]+/-/g')
    # Remove special characters * ' " `
    newname=$(echo "$newname" | tr -d "*'\"\`")
    # Convert to lowercase
    newname=$(echo "$newname" | tr '[:upper:]' '[:lower:]')
    # Remove first occurrence of double dash
    newname=$(echo "$newname" | sed 's/--/-/')

    lowerext=$(echo "$extension" | tr '[:upper:]' '[:lower:]')
    newfilename="${newname}.${lowerext}"

    if [[ "$filename" != "$newfilename" ]]; then
      mv "$filepath" "$directory/$newfilename"
      echo "Renamed: $filename -> $newfilename"
    fi
  fi
done
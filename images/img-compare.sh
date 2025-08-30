#!/bin/bash

FOLDER1="/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Pictures"
FOLDER2="/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Downloads/From Windows"
DESTINATION="/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Downloads/NonDuplicates"
THRESHOLD=5  # Lower = more strict match
DUPLICATES_LOG="/Users/mahmad/Library/CloudStorage/OneDrive-RyanRTS/Downloads/duplicates.txt"

mkdir -p "$DESTINATION"
> "$DUPLICATES_LOG"

for img2 in "$FOLDER2"/*; do
  is_duplicate=false

  for img1 in "$FOLDER1"/*; do
    # Compare images using RMSE metric
    result=$(magick compare -metric RMSE "$img1" "$img2" null: 2>&1)
    error=$(echo "$result" | awk '{print $1}' | tr -d '()')

    if (( $(echo "$error < $THRESHOLD" | bc -l) )); then
      is_duplicate=true
      {
        echo "Duplicate found"
        echo "  $img1"
        echo "  $img2"
        echo "  RMSE: $error"
        echo "---------------------------"
      } >> "$DUPLICATES_LOG"
      break
    fi
  done

  if [ "$is_duplicate" = false ]; then
    cp "$img2" "$DESTINATION/"
  fi
done

echo "Non-duplicates copied to $DESTINATION"
echo "Duplicate list saved to $DUPLICATES_LOG"

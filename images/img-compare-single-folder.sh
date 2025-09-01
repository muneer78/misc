#!/bin/bash

FOLDER="/Users/muneer78/files/personal/pictures"
DESTINATION="/Users/muneer78/Downloads/NonDuplicates"
THRESHOLD=5  # Lower = more strict match
DUPLICATES_LOG="/Users/muneer78/Downloads/duplicates.txt"

mkdir -p "$DESTINATION"
> "$DUPLICATES_LOG"

# Create array of image files
images=("$FOLDER"/*)
duplicate_files=()

echo "Scanning for duplicates in $FOLDER..."

# Compare each image with every other image
for ((i=0; i<${#images[@]}; i++)); do
  img1="${images[i]}"

  # Skip if this file is already marked as duplicate
  if [[ " ${duplicate_files[@]} " =~ " ${img1} " ]]; then
    continue
  fi

  for ((j=i+1; j<${#images[@]}; j++)); do
    img2="${images[j]}"

    # Skip if this file is already marked as duplicate
    if [[ " ${duplicate_files[@]} " =~ " ${img2} " ]]; then
      continue
    fi

    # Compare images using RMSE metric
    result=$(magick compare -metric RMSE "$img1" "$img2" null: 2>&1)
    error=$(echo "$result" | awk '{print $1}' | tr -d '()')

    # Check if error is a valid number
    if [[ "$error" =~ ^[0-9]*\.?[0-9]+$ ]] && (( $(echo "$error < $THRESHOLD" | bc -l) )); then
      duplicate_files+=("$img2")  # Mark the second image as duplicate
      {
        echo "Duplicate found"
        echo "  Original: $(basename "$img1")"
        echo "  Duplicate: $(basename "$img2")"
        echo "  RMSE: $error"
        echo "---------------------------"
      } >> "$DUPLICATES_LOG"
      echo "Found duplicate: $(basename "$img2") matches $(basename "$img1")"
    elif [[ ! "$error" =~ ^[0-9]*\.?[0-9]+$ ]]; then
      echo "Warning: Could not compare $(basename "$img1") and $(basename "$img2") - Error: $result"
    fi
  done
done

# Copy non-duplicate files to destination
copied_count=0
for img in "${images[@]}"; do
  if [[ ! " ${duplicate_files[@]} " =~ " ${img} " ]]; then
    cp "$img" "$DESTINATION/"
    ((copied_count++))
  fi
done

echo ""
echo "Results:"
echo "  Total images scanned: ${#images[@]}"
echo "  Duplicates found: ${#duplicate_files[@]}"
echo "  Unique images copied: $copied_count"
echo "  Non-duplicates copied to: $DESTINATION"
echo "  Duplicate list saved to: $DUPLICATES_LOG"
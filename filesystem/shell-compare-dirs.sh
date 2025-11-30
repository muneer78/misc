#!/bin/bash --

# Usage: ./compare-dirs.sh DIR1 DIR2

DIR1="$1"
DIR2="$2"
REPORT="diff_report.txt"

# Generate sorted file lists with relative paths
find "$DIR1" -type f | sed "s|^$DIR1/||" | sort > dir1_files.txt
find "$DIR2" -type f | sed "s|^$DIR2/||" | sort > dir2_files.txt

# Prepare report header
echo "Path,Location,LastModified,Size" > "$REPORT"

# Function to get file info
get_file_info() {
    local base="$1"
    local relpath="$2"
    stat --format="%n,%Y,%s" "$base/$relpath" 2>/dev/null | \
    sed "s|$base/||;s|^|$base,|"
}

# Process files only in DIR1 or DIR2
comm -3 dir1_files.txt dir2_files.txt | while read -r relpath; do
    if [[ -f "$DIR1/$relpath" ]]; then
        get_file_info "$DIR1" "$relpath" | awk -F, '{print $2 ",only_in_DIR1," $3 "," $4}' >> "$REPORT"
    elif [[ -f "$DIR2/$relpath" ]]; then
        get_file_info "$DIR2" "$relpath" | awk -F, '{print $2 ",only_in_DIR2," $3 "," $4}' >> "$REPORT"
    fi
done

# Process files present in both directories but with different content
comm -12 dir1_files.txt dir2_files.txt | xargs -I{} -P4 bash -c '
    relpath="{}"
    if ! cmp -s "$0/$relpath" "$1/$relpath"; then
        get_file_info "$0" "$relpath" | awk -F, "{print \$2 \",diff_in_DIR1,\" \$3 \",\" \$4}" >> "$2"
        get_file_info "$1" "$relpath" | awk -F, "{print \$2 \",diff_in_DIR2,\" \$3 \",\" \$4}" >> "$2"
    fi
' "$DIR1" "$DIR2" "$REPORT"

echo "Report generated: $REPORT"
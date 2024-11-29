for file in *-[0-9]*.mp4; do
    [[ -f $file ]] || continue  # Skip if no matching files
    newfile="${file%-*}-video-${file##*-}"
    mv -- "$file" "$newfile"
done
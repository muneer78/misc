#!/bin/zsh

function find_max_in_files() {
    local folder_path="$1"
    local pattern="^[[:alpha:]]+-\d+\.[^\.]+$"

    for file in $folder_path/**/*; do
        if [[ $file =~ $pattern ]]; then
            local prefix="${file%%-*}"
            local max_value=$(< "$file" awk '{if ($1 > max) max = $1} END {print max}')
            print -n "$prefix: "
            print "$max_value"
        fi
    done

    print -l ${max_values[@]}
}

# Prompt the user for the folder path
print "Enter the folder path:"
read folder_path

# Call the function with the provided folder path
find_max_in_files "$folder_path"
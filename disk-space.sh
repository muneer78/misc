#!/bin/bash
set -euo pipefail

# Only use macOS versions of df, awk, etc
PATH=/bin:/usr/bin

# This works for a single internal disk that contains root FS 
# - tested on 11.4 Big Sur
df / | sed '1d' |
    awk '
        /^\/dev\/disk1s1s1/ {
            size_byte = $2 * 512            # df uses 512 byte blocks
            avail_byte = $4 * 512
            total_size_gb = size_byte / 1000000000
            total_avail_gb = avail_byte / 1000000000

            printf "Size: %.1f GB     Free: %.1f GB\n", total_size_gb, total_avail_gb
        }
    '
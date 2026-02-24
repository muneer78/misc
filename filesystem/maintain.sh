#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/Users/muneer78/Documents/GitHub/misc/filesystem"

cd "$BASE_DIR"

./rename-all-files-in-dir.sh
./organize-files-downloads.sh
./organize-files-final-dest.sh
./sync-files.sh
#!/usr/bin/env bash
set -euo pipefail

BASE_DIR="/Users/muneer78/Documents/GitHub/misc/filesystem"

cd "$BASE_DIR"

./rename-all-files-in-dir.sh
./organize-files-final-dest.sh
./sync-emacs-from-github.sh
./sync-rss.sh
./sync-files.sh
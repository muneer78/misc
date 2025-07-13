#!/bin/zsh

rsync -avu /Users/muneer78/files/reg-scripts/rss-feed-weekly.py /Users/muneer78/Documents/Projects/misc/

rsync -avcru /Users/muneer78/files/reg-scripts/ /Users/muneer78/Documents/Projects/misc/

echo "Sync completed!"

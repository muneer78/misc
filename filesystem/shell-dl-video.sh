#!/bin/bash

# Ask for the URL
read -p "Enter the URL: " url

# Set the download directory
download_dir="/Users/muneer78/Downloads/videos"

# Run yt-dlp with the specified options
yt-dlp --recode-video "mp4" -P "$download_dir" "$url"
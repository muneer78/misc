#!/bin/zsh

for img in *.webp; do
    filename=${img%.*}
    magick  convert "$filename.webp" "$filename.png"
done
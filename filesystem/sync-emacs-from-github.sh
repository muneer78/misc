#!/bin/bash

# sync init.el from dotfiles-jf
rsync -aivru  /Users/muneer78/Documents/GitHub/misc/emacs/init.el /Users/muneer78/.emacs.d/init.el

echo "Processing complete."

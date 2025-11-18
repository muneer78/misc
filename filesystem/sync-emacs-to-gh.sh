#!/bin/bash

# sync init.el from dotfiles-jf
rsync -aivru /Users/muneer78/.emacs.d/init.el /Users/muneer78/Documents/GitHub/dotfiles-jf/init.el

echo "Processing complete."

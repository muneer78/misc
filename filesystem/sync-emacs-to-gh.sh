#!/bin/bash

rsync -aivru /Users/muneer78/.emacs.d/init.el /Users/muneer78/Documents/GitHub/misc/emacs/init.el

rsync -aivru /Users/muneer78/.emacs.d/elfeed.org /Users/muneer78/Documents/GitHub/emacs-files/

echo "Processing complete."

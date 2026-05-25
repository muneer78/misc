#!/bin/bash

rsync -aivru /Users/muneer78/.emacs.d/init.el /Users/muneer78/Documents/GitHub/misc/emacs/init.el

rsync -aivru /Users/muneer78/.emacs.d/elfeed.org /Users/muneer78/Documents/GitHub/emacs-files/

rsync -aivru /Users/muneer78/.emacs.d/snippets/ /Users/muneer78/Documents/GitHub/emacs-files/snippets/


echo "Processing complete."

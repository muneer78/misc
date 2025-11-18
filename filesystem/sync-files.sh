#!/bin/zsh

rsync -avu /Users/muneer78/Documents/GitHub/mun-ssg/*.py /Users/muneer78/Documents/Github/misc/text/

rsync -avu /Users/muneer78/files/data '/Users/muneer78/Library/CloudStorage/GoogleDrive-reenum@gmail.com/My Drive/files/data'
rsync -avu /Users/muneer78/files/personal/pictures '/Users/muneer78/Library/CloudStorage/GoogleDrive-reenum@gmail.com/My Drive/files/personal/pictures'
rsync -avu /Users/muneer78/files/data '/Users/muneer78/Library/CloudStorage/GoogleDrive-reenum@gmail.com/My Drive/files/'

rsync -avu /Users/muneer78/.emacs.d/init.el /Users/muneer78/Documents/GitHub/dotfiles-jf/init.el

echo "Sync completed!"

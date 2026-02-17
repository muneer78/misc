#!/bin/bash

# sync init.el from dotfiles-jf
rsync -aivru /Users/muneer78/.emacs.d/init.el /Users/muneer78/Documents/GitHub/misc/emacs/init.el

rsync -aivru /Users/muneer78/files/emacs/todos.org_archive /Users/muneer78/files/emacs/todos.org /Users/muneer78/files/emacs/posts.org /Users/muneer78/files/emacs/personal.org /Users/muneer78/files/emacs/org-ssg.el /Users/muneer78/files/emacs/newsticker-rss-feeds.el /Users/muneer78/files/emacs/life.org /Users/muneer78/files/emacs/contacts.org /Users/muneer78/Documents/GitHub/emacs-files/

echo "Processing complete."

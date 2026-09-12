#!/bin/zsh

rsync -avu /Users/muneer78/Documents/GitHub/mun-ssg/*.py /Users/muneer78/Documents/Github/misc/text/
rsync -avu /Users/muneer78/Documents/GitHub/misc/filesystem/maintain.sh '/Volumes/doak/files/scripts/'

## sync init.el to dotfiles-jf
rsync -aivru --safe-links /Users/muneer78/.emacs.d/init.el /Users/muneer78/Documents/GitHub/dotfiles/

## sync micro settings file
rsync -aivru --safe-links /Users/muneer78/.config/micro/settings.json /Users/muneer78/Documents/GitHub/dotfiles/micro/

## sync micro bindings file
rsync -aivru --safe-links /Users/muneer78/.config/micro/bindings.json /Users/muneer78/Public/GitHub/dotfiles/micro/

## sync starship file
rsync -aivru --safe-links /Users/muneer78/.config/starship.toml /Users/muneer78/Public/GitHub/dotfiles/

## sync completion.zsh

rsync -aivru --safe-links /Users/muneer78/.config/completion.zsh /Users/muneer78/Documents/GitHub/dotfiles/

## sync tmux conf
rsync -aivru --safe-links /Users/muneer78/.tmux.conf /Users/muneer78/Documents/GitHub/dotfiles/

## sync zshrc
## rsync -aivru --safe-links /Users/muneer78/.zshrc /Users/muneer78/Documents/GitHub/dotfiles/

echo "Processing complete."
echo "Sync completed!"

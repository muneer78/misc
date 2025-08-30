#!/usr/bin/env bash

set -e

# This file contains settings for mac which makes me happy.
# It is not a full list.
#
# The best resource of finding new settings for other users is:
# https://www.defaults-write.com
#
# Some parts are taken from:
# - https://github.com/rootbeersoup/dotfiles
# - https://github.com/skwp/dotfiles
#
# All values are sorted inside their blocks: newest are on the top.
#

echo 'Configuring your mac. Hang tight.'
osascript -e 'tell application "System Preferences" to quit'

# === General ===

# Dark mode
defaults write .GlobalPreferences AppleInterfaceStyle -string "Dark"
defaults write .GlobalPreferences AppleInterfaceStyleSwitchesAutomatically -bool false

# Hide remaining battery time; show percentage
defaults write com.apple.menuextra.battery ShowPercent -string "YES"
defaults write com.apple.menuextra.battery ShowTime -string "NO"

# Disable window animations and Get Info animations in Finder
defaults write com.apple.finder DisableAllAnimations -bool true

# Disable bouncing dock
defaults write com.apple.dock no-bouncing -bool false

# Disable startup noise:
sudo nvram SystemAudioVolume=%01

# Scrollbars visible when scrolling:
defaults write NSGlobalDomain AppleShowScrollBars -string "WhenScrolling"

# Always use expanded save dialog:
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode -bool true
defaults write NSGlobalDomain NSNavPanelExpandedStateForSaveMode2 -bool true

# This line deactivates rubber scrolling:
# http://osxdaily.com/2012/05/10/disable-elastic-rubber-band-scrolling-in-mac-os-x/
defaults write -g NSScrollViewRubberbanding -int 0

# Maximize windows on double clicking them:
defaults write -g AppleActionOnDoubleClick 'Maximize'

# Disable opening and closing window animations
defaults write NSGlobalDomain NSAutomaticWindowAnimationsEnabled -bool false

# Disable crash reporter
defaults write com.apple.CrashReporter DialogType none

# Enable full keyboard access for all controls (e.g. enable Tab in modal dialogs)
defaults write NSGlobalDomain AppleKeyboardUIMode -int 3

# Enable snap-to-grid for desktop icons
/usr/libexec/PlistBuddy -c "Set :DesktopViewSettings:IconViewSettings:arrangeBy grid" ~/Library/Preferences/com.apple.finder.plist

# Focus follows mouse
defaults write com.apple.Terminal "FocusFollowsMouse" -bool "true"

# Sound: always show in menu bar
defaults -currentHost write com.apple.controlcenter Sound -int 18

# === Dock ===

# Size:
defaults write com.apple.dock tilesize -int 56

# Show indicator lights for open apps in Dock:
defaults write com.apple.dock show-process-indicators -bool true

# Dock size and location:
defaults write com.apple.Dock size-immutable -bool yes

# Show Dock instantly:
defaults write com.apple.dock autohide-delay -float 0

# Don’t animate opening applications from the Dock
defaults write com.apple.dock launchanim -bool false

# === Mail ===

# Disable send and reply animations in Mail.app
defaults write com.apple.Mail DisableReplyAnimations -bool true
defaults write com.apple.Mail DisableSendAnimations -bool true

# Copy email addresses as `foo@example.com` instead of `Foo Bar <foo@example.com>` in Mail.app
defaults write com.apple.mail AddressesIncludeNameOnPasteboard -bool false

# Force all Mail messages to display as plain text
defaults write com.apple.mail PreferPlainText -bool TRUE

# === Finder ===

# Keep folders on top when sorting by name:
defaults write com.apple.finder _FXSortFoldersFirst -bool true

# Show Finder path bar:
defaults write com.apple.finder ShowPathbar -bool true

# Do not show status bar in Finder:
defaults write com.apple.finder ShowStatusBar -bool false

# Show hidden files in Finder:
defaults write com.apple.finder AppleShowAllFiles -bool true

# Show file extensions in Finder:
defaults write NSGlobalDomain AppleShowAllExtensions -bool true

# Allow quitting Finder via ⌘ + Q; doing so will also hide desktop icons
defaults write com.apple.finder QuitMenuItem -bool true

# Allow text selection in Quick Look
defaults write com.apple.finder QLEnableTextSelection -bool true

# Display full POSIX path as Finder window title
defaults write com.apple.finder _FXShowPosixPathInTitle -bool true

# Disable the warning when changing a file extension
defaults write com.apple.finder FXEnableExtensionChangeWarning -bool false

# Show Library folder
chflags nohidden ~/Library

# When performing a search, search the current folder by default
defaults write com.apple.finder FXDefaultSearchScope -string "SCcf"

# Avoid creating .DS_Store files on network or USB volumes
defaults write com.apple.desktopservices DSDontWriteNetworkStores -bool true
defaults write com.apple.desktopservices DSDontWriteUSBStores -bool true

# Expand the following File Info panes:
# “General”, “Open with”, and “Sharing & Permissions”
defaults write com.apple.finder FXInfoPanesExpanded -dict \
	General -bool true \
	OpenWith -bool true \
	Privileges -bool true


# === Safari ===

# Privacy: don’t send search queries to Apple
defaults write com.apple.Safari UniversalSearchEnabled -bool false
defaults write com.apple.Safari SuppressSearchSuggestions -bool true

# Improve Safari security
defaults write com.apple.Safari \
  com.apple.Safari.ContentPageGroupIdentifier.WebKit2JavaEnabled \
  -bool false
defaults write com.apple.Safari \
  com.apple.Safari.ContentPageGroupIdentifier.WebKit2JavaEnabledForLocalFiles \
  -bool false


# === Text editing ===

# Disable smart quotes:
defaults write NSGlobalDomain NSAutomaticQuoteSubstitutionEnabled -bool false

# Disable autocorrect:
defaults write NSGlobalDomain NSAutomaticSpellingCorrectionEnabled -bool false

# Disable auto-capitalization:
defaults write NSGlobalDomain NSAutomaticCapitalizationEnabled -bool false

# Disable smart dashes:
defaults write NSGlobalDomain NSAutomaticDashSubstitutionEnabled -bool false

# Disable automatic period substitution:
defaults write NSGlobalDomain NSAutomaticPeriodSubstitutionEnabled -bool false


# === Activity monitor ===

# Show the main window when launching Activity Monitor
defaults write com.apple.ActivityMonitor OpenMainWindow -bool true

# Visualize CPU usage in the Activity Monitor Dock icon
defaults write com.apple.ActivityMonitor IconType -int 5

# Show all processes in Activity Monitor
defaults write com.apple.ActivityMonitor ShowCategory -int 0


# === App Store ===

# Disable in-app rating requests from apps downloaded from the App Store.
defaults write com.apple.appstore InAppReviewEnabled -int 0

# === Screenshots ===
# Disable shadow in screenshots
defaults write com.apple.screencapture disable-shadow -bool true

Set the screenshot location to ~/Pictures
defaults write com.apple.screencapture "location" -string "~/Pictures"

# Default screenshot format set to png
defaults write com.apple.screencapture type -string "png"

# === Apple Intelligence ===
defaults write com.apple.CloudSubscriptionFeatures.optIn "545129924" -bool "false"

# === TextEdit ===
defaults write com.apple.TextEdit "RichText" -bool "false"


# Kill affected applications
APPS=(Finder
Dock
Mail
Safari
SystemUIServer
Terminal
TextEdit)

for APP in "${APPS[@]}"; do
    killall "$APP" &>/dev/null
done

echo 'Done!'

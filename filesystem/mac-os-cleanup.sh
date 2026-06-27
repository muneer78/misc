#!/bin/bash

# Check if script is run as sudo
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run as root. Re-running with sudo..."
    exec sudo "$0" "$@"
fi

# macOS Cleanup Script with Logging and Error Tracking
LOG_FILE="$HOME/.scripts/logs/cleanup_log_$(date '+%Y%m%d_%H%M%S').log"
echo "Starting enhanced purgeable space cleanup on macOS..." | tee -a "$LOG_FILE"

# Define cache paths to clean
CACHE_PATHS=(
    "/Library/Caches/*"
    "$HOME/Library/Caches/*"
    "/System/Library/Caches/*"
    "/private/var/folders/*"
)

# Define application-specific caches
APP_CACHE_PATHS=(
    "$HOME/Library/Caches/com.apple.Safari/*"
    "$HOME/Library/Caches/Google/Chrome/*"
    "$HOME/Library/Application Support/Google/Chrome/Default/Cache/*"
    "$HOME/Library/Application Support/Microsoft/Edge/Default/Cache/*"
    "$HOME/Library/Caches/Dropbox/*"
    "$HOME/Library/Caches/Spotify/*"
    "$HOME/Library/Caches/Adobe/*"
)

# Define developer-related caches
DEV_CACHE_PATHS=(
    "$HOME/Library/Developer/CoreSimulator/Caches/*"
    "$HOME/Library/Developer/CoreSimulator/Devices/*"
    "$HOME/.gradle/caches/*"
    "$HOME/Library/Caches/com.apple.dt.Xcode/*"
    "$HOME/Library/Developer/Xcode/DerivedData/*"
)

# Define temporary files
TEMP_PATHS=(
    "/private/tmp/*"
    "/private/var/tmp/*"
)

# Define other cleanup targets
OTHER_PATHS=(
    "$HOME/Library/Containers/com.apple.mail/Data/Library/Mail Downloads/*"
    "$HOME/Library/Saved Application State/*"
    "$HOME/Library/Application Support/CrashReporter/*"
    "$HOME/Library/Application Support/MobileSync/Backup/*"
)

# Function to log actions with severity levels
log_action() {
    local level=$1
    local message=$2
    echo "$(date '+%Y-%m-%d %H:%M:%S') [$level] - $message" | tee -a "$LOG_FILE"
}

# Function to clean paths
clean_paths() {
    local paths=("$@")
    for path in "${paths[@]}"; do
        log_action "INFO" "Attempting to delete $path"
        if rm -rf $path 2>>"$LOG_FILE"; then
            log_action "INFO" "Deleted $path successfully"
        else
            log_action "ERROR" "Failed to delete $path"
        fi
    done
}

# Clear system and user caches
log_action "INFO" "Clearing system and user caches..."
clean_paths "${CACHE_PATHS[@]}"

# Clear application-specific caches
log_action "INFO" "Clearing application-specific caches..."
clean_paths "${APP_CACHE_PATHS[@]}"

# Clear developer-related caches
log_action "INFO" "Clearing developer-related caches..."
clean_paths "${DEV_CACHE_PATHS[@]}"

# Clear temporary files
log_action "INFO" "Clearing temporary files..."
clean_paths "${TEMP_PATHS[@]}"

# Clear other paths
log_action "INFO" "Clearing additional cleanup paths..."
clean_paths "${OTHER_PATHS[@]}"

# Remove old Time Machine local snapshots
if tmutil listlocalsnapshots / > /dev/null 2>&1; then
    log_action "INFO" "Removing old Time Machine local snapshots..."
    tmutil listlocalsnapshots / | grep -o 'com.apple.TimeMachine.*' | while read -r snapshot; do
        log_action "INFO" "Deleting snapshot: $snapshot"
        if tmutil deletelocalsnapshots "$snapshot" >>"$LOG_FILE" 2>&1; then
            log_action "INFO" "Deleted snapshot $snapshot successfully"
        else
            log_action "ERROR" "Failed to delete snapshot $snapshot"
        fi
    done
else
    log_action "WARNING" "Time Machine is not enabled or there are no local snapshots."
fi

# Flush disk cache
log_action "INFO" "Flushing disk cache..."
if sync && purge >>"$LOG_FILE" 2>&1; then
    log_action "INFO" "Flushed disk cache successfully"
else
    log_action "ERROR" "Failed to flush disk cache"
fi

# Clear system swap files
log_action "INFO" "Clearing swap files..."
if rm -rf /private/var/vm/swapfile* 2>>"$LOG_FILE"; then
    log_action "INFO" "Cleared swap files successfully"
else
    log_action "ERROR" "Failed to clear swap files"
fi

# Remove files older than 30 days in Downloads
log_action "INFO" "Removing files older than 30 days from the Downloads Directory..."
if find ~/Downloads -type f -mtime +30 -exec rm -rf {} \; 2>>"$LOG_FILE"; then
    log_action "INFO" "Removed files older than 30 days successfully"
else
    log_action "ERROR" "Failed to remove files older than 30 days"
fi


# Remove files older than 30 days in Documents
log_action "INFO" "Removing files older than 30 days from the Documents Directory..."
if find ~/Documents -type f -mtime +30 -exec rm -rf {} \; 2>>"$LOG_FILE"; then
    log_action "INFO" "Removed files older than 30 days successfully"
else
    log_action "ERROR" "Failed to remove files older than 30 days"
fi

# Remove files older than 30 days in the root of Documents
log_action "INFO" "Removing files older than 30 days from the root of the Documents Directory..."
if find ~/Documents -maxdepth 1 -type f -mtime +30 -exec rm -f {} \; 2>>"$LOG_FILE"; then
    log_action "INFO" "Removed files older than 30 days successfully"
else
    log_action "ERROR" "Failed to remove files older than 30 days"
fi

# Flush DNS cache
log_action "INFO" "Flushing DNS cache..."
if dscacheutil -flushcache && killall -HUP mDNSResponder >>"$LOG_FILE" 2>&1; then
    log_action "INFO" "Flushed DNS cache successfully"
else
    log_action "ERROR" "Failed to flush DNS cache"
fi

# Empty the Trash
log_action "INFO" "Emptying the Trash..."
if rm -rf "$HOME/.Trash/*" 2>>"$LOG_FILE"; then
    log_action "INFO" "Emptied the Trash successfully"
else
    log_action "ERROR" "Failed to empty the Trash"
fi

log_action "INFO" "Rebuilding Spotlight index..."
if mdutil -E / >>"$LOG_FILE" 2>&1; then
    log_action "INFO" "Rebuilt Spotlight index successfully"
else
    log_action "ERROR" "Failed to rebuild Spotlight index"
fi

log_action "INFO" "Resetting system logs..."
if rm -rf /var/log/* 2>>"$LOG_FILE"; then
    log_action "INFO" "Reset system logs successfully"
else
    log_action "ERROR" "Failed to reset system logs"
fi

log_action "INFO" "Verifying and repairing disk..."
if diskutil verifyVolume / >>"$LOG_FILE" 2>&1; then
    log_action "INFO" "Disk verified successfully"
else
    log_action "ERROR" "Disk verification failed"
fi

if diskutil repairVolume / >>"$LOG_FILE" 2>&1; then
    log_action "INFO" "Disk repaired successfully (if needed)"
else
    log_action "ERROR" "Disk repair failed"
fi

# Searching for unused applications
log_action "INFO" "Searching for unused applications..."
find /Applications -type d -atime +180 -exec echo "Unused: {}" \; >>"$LOG_FILE" 2>&1 || log_action "ERROR" "Failed to search for unused applications"

# Checking battery health
log_action "INFO" "Checking battery health..."
ioreg -l | grep -i "CycleCount\|DesignCapacity\|FullChargeCapacity" >>"$LOG_FILE" 2>&1 || log_action "ERROR" "Failed to retrieve battery health information"


# Generating system report
log_action "INFO" "Generating system report..."
{
    echo "System Report"
    echo "Disk Usage:"
    df -h
    echo "Memory Usage:"
    vm_stat
} >> "$HOME/system_report.txt" || log_action "ERROR" "Failed to generate system report"

# Checking for macOS updates
log_action "INFO" "Checking for macOS updates..."
if softwareupdate -l >>"$LOG_FILE" 2>&1; then
    log_action "INFO" "Checked for macOS updates successfully"
else
    log_action "ERROR" "Failed to check for macOS updates"
fi

# Display available disk space
log_action "INFO" "Cleanup complete!"
log_action "INFO" "Available disk space after cleanup:"
df -h / | tee -a "$LOG_FILE"
#!/bin/bash

# Define source and destination paths
SOURCE_DIR="Z:/multiversity_of_science/projectfiles"
DEST_DIR="$HOME/slyce"
LOG_FILE="$DEST_DIR/sync_log.txt"
DATE=$(date '+%Y-%m-%d %H:%M:%S')

# Ensure repo is cloned if not present
if [ ! -d "$DEST_DIR/.git" ]; then
    echo "[$DATE] Cloning repo..." >> "$LOG_FILE"
    git clone https://github.com/slycetress/slyce.git "$DEST_DIR"
fi

# Sync files (additive only, no deletion)
echo "[$DATE] Syncing files from $SOURCE_DIR to $DEST_DIR" >> "$LOG_FILE"
cp -ru "$SOURCE_DIR"/* "$DEST_DIR" 2>> "$LOG_FILE"

# Stage, commit, and push only if there are changes
cd "$DEST_DIR"
if [ -n "$(git status --porcelain)" ]; then
    git add .
    git commit -m "Additive sync: $DATE"
    git push origin main
    echo "[$DATE] Changes pushed to GitHub." >> "$LOG_FILE"
else
    echo "[$DATE] No changes to commit." >> "$LOG_FILE"
fi
#!/bin/bash

# URL of the vimrc file
VIMRC_URL="PLACEHOLDER"

# Path to user's .vimrc
USER_VIMRC="$HOME/.vimrc"

# Backup file name
BACKUP_VIMRC="$HOME/.vimrc.backup.$(date +%Y%m%d%H%M%S)"

# Temporary file for new vimrc
TMP_VIMRC="/tmp/new_vimrc"

# Function to display error messages
error_exit() {
    echo "Error: $1" >&2
    exit 1
}

# Function to download file
download_file() {
    if command -v curl &> /dev/null; then
        if curl -fsSL "$1" -o "$2"; then
            return 0
        else
            return 1
        fi
    elif command -v wget &> /dev/null; then
        if wget -q "$1" -O "$2"; then
            return 0
        else
            return 1
        fi
    else
        echo "Neither curl nor wget is available. Please install one of them."
        return 1
    fi
}

# Download the new vimrc
echo "Downloading new .vimrc..."
if ! download_file "$VIMRC_URL" "$TMP_VIMRC"; then
    error_exit "Failed to download the new .vimrc file."
fi

# Check if current .vimrc exists
if [ -f "$USER_VIMRC" ]; then
    # Compare the files
    if cmp -s "$USER_VIMRC" "$TMP_VIMRC"; then
        echo "The current .vimrc is identical to the new one. No changes needed."
        rm "$TMP_VIMRC"
        exit 0
    else
        echo "Existing .vimrc found and it's different from the new one. Creating backup..."
        if ! cp "$USER_VIMRC" "$BACKUP_VIMRC"; then
            error_exit "Failed to create backup of existing .vimrc."
        fi
        echo "Backup created at $BACKUP_VIMRC"
    fi
else
    echo "No existing .vimrc found. Will create a new one."
fi

# Move the new vimrc to the user's home directory
echo "Installing new .vimrc..."
if ! mv "$TMP_VIMRC" "$USER_VIMRC"; then
    error_exit "Failed to install the new .vimrc file."
fi

echo "New .vimrc successfully installed!"
if [ -f "$BACKUP_VIMRC" ]; then
    echo "If you need to revert, you can use the backup at $BACKUP_VIMRC"
fi

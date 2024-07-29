#!/bin/bash

# Define the default root directory where your repos are located
DEFAULT_ROOT_DIR="/home/cobra/Repos"

# Use the provided argument as the root directory, or the default if none is provided
ROOT_DIR=${1:-$DEFAULT_ROOT_DIR}

echo "Starting update process for repositories in $ROOT_DIR"

# Function to pull changes in a git repository
pull_repo() {
    local repo_dir=$1
    echo "Pulling updates in $repo_dir"
    cd "$repo_dir" || return
    git pull
    echo "Completed update in $repo_dir"
    cd - || return
}

# Export the function so it can be used by find -exec
export -f pull_repo

# Find all .git directories and pull changes in their parent directories
find "$ROOT_DIR" -name ".git" -type d -exec bash -c 'pull_repo "$(dirname "{}")"' \;

echo "All repositories updated."

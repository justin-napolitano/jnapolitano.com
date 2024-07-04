#!/bin/bash

# sync_submodules.sh
# Script to initialize and update all submodules to the latest commits from their remote repositories

# Usage:
# 1. Ensure this script is executable:
#    chmod +x sync_submodules.sh
# 2. Run the script:
#    ./sync_submodules.sh

# Overview:
# This script is designed to initialize and update all submodules in a GitHub repository 
# to the latest commits from their respective remote repositories. It ensures that all 
# submodules, including nested submodules, are synchronized with their remote counterparts.

# Prerequisites:
# - Ensure that you have Git installed on your system.
# - Ensure that you have cloned the repository containing the submodules.

# Check if the script is run from the root of the repository
if [ ! -f .gitmodules ]; then
  echo "Error: .gitmodules file not found. Please run this script from the root of your repository."
  exit 1
fi

# Initialize submodules (if not already initialized)
git submodule init

# Update all submodules to the latest commits from their remote repositories
git submodule update --init --recursive --remote

# Check if the submodule update was successful
if [ $? -eq 0 ]; then
  echo "Submodules have been successfully updated."
else
  echo "Error: Failed to update submodules."
  exit 1
fi

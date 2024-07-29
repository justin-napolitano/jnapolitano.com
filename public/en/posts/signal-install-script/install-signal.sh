#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# 1. Install the official public software signing key
echo "Installing the Signal public software signing key..."
wget -O- https://updates.signal.org/desktop/apt/keys.asc | gpg --dearmor > signal-desktop-keyring.gpg
cat signal-desktop-keyring.gpg | sudo tee /usr/share/keyrings/signal-desktop-keyring.gpg > /dev/null

# 2. Add the Signal repository to the list of repositories
echo "Adding the Signal repository to the list of repositories..."
echo 'deb [arch=amd64 signed-by=/usr/share/keyrings/signal-desktop-keyring.gpg] https://updates.signal.org/desktop/apt xenial main' |\
  sudo tee /etc/apt/sources.list.d/signal-xenial.list

# 3. Update the package database and install Signal
echo "Updating the package database..."
sudo apt update

echo "Installing Signal Desktop..."
sudo apt install -y signal-desktop

echo "Signal Desktop installation completed successfully!"

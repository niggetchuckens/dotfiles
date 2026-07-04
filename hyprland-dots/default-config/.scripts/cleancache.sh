#!/bin/bash

echo "--- Starting Arch Linux Cleanup ---"

# 1. Remove orphaned packages (dependencies no longer needed)
if [[ -n $(pacman -Qtdq) ]]; then
    echo "Removing orphaned packages..."
    sudo pacman -Rns $(pacman -Qtdq)
else
    echo "No orphans to remove."
fi

# 2. Clean the Pacman/Yay cache (keeps only the last 3 versions to save space)
# This prevents your /var/cache/pacman/pkg from bloating
echo "Cleaning package cache (keeping last 3)..."
sudo paccache -r
yay -Sc --noconfirm

# 3. Clear user-level cache (Waybar, Thumbnails, etc.)
echo "Clearing ~/.cache folder..."
rm -rf ~/.cache/*

# 4. Clean up journal logs older than 2 days
echo "Vacuuming systemd journal..."
sudo journalctl --vacuum-time=2d

# 5. Clean your headless monitor ghost files (based on our earlier fix)
echo "Cleaning headless monitor temp files..."
rm -f /tmp/sunshine_monitor

echo "--- Cleanup Complete! ---"
#!/bin/bash
# Smart Keyring Starter
# Prevents GNOME Keyring from hijacking the Secret Service if KDE Wallet is present.

if command -v kwalletd6 >/dev/null 2>&1 || command -v kwalletd5 >/dev/null 2>&1; then
    echo "KDE Wallet detected. Skipping gnome-keyring-daemon to prevent Chromium Safe Storage corruption."
else
    gnome-keyring-daemon --start --components=secrets
fi

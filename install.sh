#!/bin/bash
set -e

BLUE='\033[0;34m'
GREEN='\033[0;32m'
NC='\033[0m'

echo -e "${BLUE}[INFO] Bootstrapping the installer...${NC}"

if ! command -v python3 &> /dev/null; then
    echo -e "${BLUE}[INFO] Python not found. Identifying package manager...${NC}"
    if command -v pacman &> /dev/null; then
        sudo pacman -S --needed --noconfirm python
    elif command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y python3
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3
    else
        echo "Error: Supported package manager not found. Please install Python manually."
        exit 1
    fi
fi

python3 installer.py
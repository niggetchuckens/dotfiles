#!/bin/bash
# debian_setup.sh - Helper for YukiOS on Debian Minimal

BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}[INFO] Fixing repositories and installing base build tools...${NC}"

# 1. Update sources.list for Trixie (ensuring contrib and non-free)
sudo tee /etc/apt/sources.list <<EOF
deb http://deb.debian.org/debian/ trixie main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security trixie-security main contrib non-free non-free-firmware
EOF

sudo apt update
sudo apt install -y software-properties-common apt-transport-https build-essential git curl python3-pip

# 2. Install Build Dependencies for Hyprland
echo -e "${BLUE}[INFO] Installing Hyprland dependencies...${NC}"
sudo apt install -y meson ninja-build cmake pkg-config libwayland-dev libgbm-dev \
libxkbcommon-dev libpixman-1-dev libudev-dev libinput-dev libdisplay-info-dev \
libliftoff-dev libseat-dev libxcb-composite0-dev libxcb-xkb-dev libxcb-util-dev \
libxcb-errors-dev libavutil-dev libavcodec-dev libavformat-dev libswscale-dev

# 3. Build Hyprland from source
echo -e "${BLUE}[INFO] Building Hyprland...${NC}"
BUILD_DIR="$HOME/hyprland_build"
[ -d "$BUILD_DIR" ] && rm -rf "$BUILD_DIR"
git clone --recursive https://github.com/hyprwm/Hyprland "$BUILD_DIR"
cd "$BUILD_DIR" && make all && sudo make install

echo -e "${BLUE}[INFO] Debian base setup complete.${NC}"
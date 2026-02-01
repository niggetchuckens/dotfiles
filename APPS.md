# Applications Required for Hyprland Setup

This document lists all the applications and dependencies needed for this Hyprland configuration to work properly in case the installer can't install it automaticlly.

## Core Components

### Window Manager & Display
- **hyprland** - Dynamic tiling Wayland compositor
- **hyprpolkitagent** - PolicyKit authentication agent for Hyprland
- **xdg-desktop-portal-hyprland** - XDG Desktop Portal backend for Hyprland

### Wayland Utilities
- **wayland** - Wayland display server protocol
- **wl-clipboard** - Command-line copy/paste utilities for Wayland (provides `wl-copy`, `wl-paste`)
- **xwayland** - X11 compatibility layer for Wayland

## User Interface

### Status Bar & Panels
- **waybar** - Highly customizable Wayland bar for Sway and Hyprland

### Application Launchers
- **rofi** - Window switcher and application launcher (with Wayland support)
- **wofi** - Native Wayland launcher (used for clipboard history)

### Session Management
- **wlogout** - Wayland-based logout menu

### Notifications
- **dunst** or **mako** - Notification daemon (recommended for Wayland)

## Terminal & Shell

- **kitty** - GPU-based terminal emulator with native Wayland support
- **oh-my-posh** - Prompt theme engine (for shell customization)

## File Management

- **nautilus** - GNOME file manager

## System Utilities

### Screenshots & Screen Recording
- **grim** - Screenshot utility for Wayland compositors
- **slurp** - Select a region in Wayland compositors

### Clipboard Management
- **cliphist** - Clipboard history manager for Wayland

### Wallpaper
- **swaybg** - Wallpaper utility for Wayland compositors

### Brightness Control
- **brightnessctl** - Read and control device brightness

### Audio
- **pipewire** - Multimedia framework (audio/video routing)
- **wireplumber** - Session manager for PipeWire
- **pipewire-pulse** - PulseAudio replacement for PipeWire
- **wpctl** - WirePlumber control utility (used in volume keybinds)
- **pavucontrol** - PulseAudio Volume Control (GUI audio mixer)

### Media Control
- **playerctl** - Media player controller (for media keys)

### Network
- **networkmanager** - Network connection manager
- **nm-connection-editor** - NetworkManager GUI

### Power Management
- **power-profiles-daemon** - Power profile management service

### Authentication & Security
- **gnome-keyring** - GNOME keyring daemon (secrets management)
- **polkit** - Authorization framework

## Applications

### Web Browsers
- **brave** - Privacy-focused web browser

### Communication
- **discord** - Voice, video, and text communication platform

### System Information
- **fastfetch** - System information tool

### Remote Desktop
- **sunshine** - Self-hosted game stream host (started at boot)

## Development Tools

### Text Editors
- **nvim** (Neovim) - Hyperextensible Vim-based text editor

## Fonts

- **CommitMono Nerd Font** - Monospace font with icon glyphs (used by Waybar)
- **Papirus Icon Theme** - Icon theme (used by Rofi)

## Optional but Recommended

### Package Management
- **yay** - AUR helper (referenced in Waybar updates script)
- **checkupdates** - Check for available package updates (pacman-contrib)

### Cursor Theme
- **Bibata Modern Classic** - Cursor theme

## System Services

The following systemd services should be enabled:
- `systemctl --user enable hyprpolkitagent.service`
- `systemctl --user enable pipewire.service`
- `systemctl --user enable wireplumber.service`

## Environment Variables

The following environment variables are set in the configuration:
- `HYPRCURSOR_THEME=Bibata Modern Classic Right`
- `HYPRCURSOR_SIZE=24`
- `LIBVA_DRIVER_NAME=nvidia` (for NVIDIA GPUs)
- `__GLX_VENDOR_LIBRARY_NAME=nvidia` (for NVIDIA GPUs)
- `ELECTRON_OZONE_PLATAFORM_HINT=auto`
- `WLR_DRM_NO_ATOMIC=1`

## Installation Commands

### Arch Linux (using pacman)
```bash
# Core Hyprland and Wayland
sudo pacman -S hyprland xdg-desktop-portal-hyprland wayland wl-clipboard xorg-xwayland

# UI Components
sudo pacman -S waybar rofi wofi wlogout

# Terminal and utilities
sudo pacman -S kitty nautilus

# Screenshots and clipboard
sudo pacman -S grim slurp cliphist swaybg

# System utilities
sudo pacman -S brightnessctl pipewire wireplumber pipewire-pulse pavucontrol playerctl

# Network and power
sudo pacman -S networkmanager network-manager-applet power-profiles-daemon

# Security
sudo pacman -S polkit gnome-keyring

# Applications
sudo pacman -S brave-bin discord fastfetch neovim

# Fonts and themes
sudo pacman -S ttf-commit-mono-nerd papirus-icon-theme bibata-cursor-theme

# Optional
sudo pacman -S pacman-contrib
yay -S yay sunshine oh-my-posh
```

## Notes

- This configuration is optimized for NVIDIA GPUs (see environment variables)
- Default terminal: kitty
- Default browser keybind: Brave
- Primary modifier key: ALT
- Clipboard history is stored via cliphist
- Screenshots are taken using grim + slurp + wl-copy
- Waybar includes system monitoring (CPU, memory, battery, etc.)

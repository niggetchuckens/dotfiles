#!/bin/bash
export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t $XDG_RUNTIME_DIR/hypr | head -n 1)

# 1. Remove any existing HEADLESS monitors
hyprctl monitors | grep "Monitor HEADLESS" | awk '{print $2}' | xargs -I {} hyprctl output remove {}
# 2. Create a new HEADLESS monitor
# Adjust resolution as needed for your iPad
# Here, we use 2048x1536 at 60Hz
hyprctl output create headless
sleep 0.5
DYNAMIC_NAME=$(hyprctl monitors | grep "Monitor HEADLESS" | awk '{print $2}')
hyprctl keyword monitor "$DYNAMIC_NAME,2160x1620@60,auto,1"
hyprctl dispatch moveworkspacetomonitor 10 "$DYNAMIC_NAME"
hyprctl dispatch workspace 10

# 3. Launch Yuzu with Proton
# Adjust the path to your Yuzu installation as needed
# Replace the path below with the actual path to your Yuzu executable

$HOME/.local/share/applications/Yuzu.desktop


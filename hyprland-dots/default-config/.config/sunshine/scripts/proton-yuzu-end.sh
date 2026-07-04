#!/bin/bash
export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t $XDG_RUNTIME_DIR/hypr | head -n 1)

# 1. Remove any existing HEADLESS monitors
hyprctl monitors | grep "Monitor HEADLESS" | awk '{print $2}' | xargs -I {} hyprctl output remove {}

# 2. Restore the main monitor workspace 
hyprctl keyword monitor eDP-1,1920x1080@144,0x0,1
for ws in {1..10}; do
    hyprctl dispatch moveworkspacetomonitor "$ws" eDP-1
done

# 3. Close Yuzu if it's still running
pkill -9 yuzu

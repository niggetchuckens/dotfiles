#!/bin/bash
# Get Hyprland signature
export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t $XDG_RUNTIME_DIR/hypr | head -n 1)

# 1. Identify all active HEADLESS monitors and remove them
hyprctl monitors | grep "Monitor HEADLESS" | awk '{print $2}' | xargs -I {} hyprctl output remove {}

# 2. Revert your primary laptop screen to native if it was changed
# (Optional: only if you also resized eDP-1)
hyprctl keyword monitor eDP-1,1920x1080@144,0x0,1

# 3. Move your workspaces back to your main monitor (eDP-1)
# This prevents windows from getting "stuck" in a deleted monitor
for ws in {1..10}; do
    hyprctl dispatch moveworkspacetomonitor "$ws" eDP-1
done
#!/bin/bash
export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t $XDG_RUNTIME_DIR/hypr | head -n 1)

hyprctl monitors | grep "Monitor HEADLESS" | awk '{print $2}' | xargs -I {} hyprctl output remove {}
hyprctl output create headless
sleep 0.5
DYNAMIC_NAME=$(hyprctl monitors | grep "Monitor HEADLESS" | awk '{print $2}')
hyprctl keyword monitor "$DYNAMIC_NAME,2160x1620@60,auto,1"
hyprctl dispatch moveworkspacetomonitor 9 "$DYNAMIC_NAME"
code /home/hime/code
hyprctl dispatch "[workspace 9] code"
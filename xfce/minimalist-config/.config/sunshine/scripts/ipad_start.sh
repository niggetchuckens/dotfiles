#!/bin/bash
export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t $XDG_RUNTIME_DIR/hypr | head -n 1)

hyprctl keyword monitor eDP-1,2160x1620@60,auto,1.5
#!/bin/bash
export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t $XDG_RUNTIME_DIR/hypr | head -n 1)

hyprctl keyword monitor eDP-1,1920x1080@144,auto,1
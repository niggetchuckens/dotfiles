#!/bin/bash
export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t $XDG_RUNTIME_DIR/hypr | head -n 1)
MONITOR=$(hyprctl monitors | grep "Monitor" | awk '{print $2}' | head -n 1)

echo "Restoring $MONITOR to preferred resolution" >> /tmp/sunshine_res.log
hyprctl keyword monitor "$MONITOR,preferred,auto,1"

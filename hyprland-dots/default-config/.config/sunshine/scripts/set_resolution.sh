#!/bin/bash
# Get the first active monitor
export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t $XDG_RUNTIME_DIR/hypr | head -n 1)
MONITOR=$(hyprctl monitors | grep "Monitor" | awk '{print $2}' | head -n 1)

# Sunshine provides these environment variables
WIDTH=${SUNSHINE_CLIENT_WIDTH}
HEIGHT=${SUNSHINE_CLIENT_HEIGHT}
FPS=${SUNSHINE_CLIENT_FPS}

# Fallback to default if variables are not set (e.g. manual run)
if [ -z "$WIDTH" ] || [ -z "$HEIGHT" ]; then
    WIDTH=1920
    HEIGHT=1080
fi

if [ -z "$FPS" ]; then
    FPS=60
fi

echo "Setting $MONITOR to ${WIDTH}x${HEIGHT}@${FPS}" >> /tmp/sunshine_res.log
hyprctl keyword monitor "$MONITOR,${WIDTH}x${HEIGHT}@${FPS},0x0,1"

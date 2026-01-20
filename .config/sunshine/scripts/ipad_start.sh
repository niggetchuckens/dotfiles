#!/bin/bash
export HYPRLAND_INSTANCE_SIGNATURE=$(ls -t $XDG_RUNTIME_DIR/hypr | head -n 1)

# 1. Clean up any ghosts that didn't get removed properly
hyprctl monitors | grep "Monitor HEADLESS" | awk '{print $2}' | xargs -I {} hyprctl output remove {}

# 2. Create the new output
hyprctl output create headless

# 3. Wait for the system to register the new ID
sleep 0.5

# 4. Grab the name of the monitor we just created
DYNAMIC_NAME=$(hyprctl monitors | grep "Monitor HEADLESS" | awk '{print $2}')

# 5. Apply the iPad 7th Gen Resolution (2160x1620)
# We set scale to 1.0 for the full workspace
hyprctl keyword monitor "$DYNAMIC_NAME,2160x1620@60,auto,1"

# 6. Crucial: Tell the iPad to look at this specific monitor
# We do this by moving a dedicated workspace to it
hyprctl dispatch moveworkspacetomonitor 9 "$DYNAMIC_NAME"
hyprctl dispatch workspace 9
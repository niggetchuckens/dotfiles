#!/usr/bin/env bash

# 1. Smarter Dynamic Detection
# This version looks for the 'internal' flag first, then falls back to common patterns
INTERNAL=$(hyprctl monitors -j | jq -r '.[] | select(.internal == true).name')
[ -z "$INTERNAL" ] && INTERNAL=$(hyprctl monitors -j | jq -r '.[] | select(.name | contains("eDP")).name')

# Get any monitor that is NOT the internal one
EXTERNAL=$(hyprctl monitors -j | jq -r ".[] | select(.name != \"$INTERNAL\").name")

# 2. Native Resolution Grabber (Safe first-entry)
get_native_res() {
    local mon_name=$1
    # Grab the first mode listed in availableModes
    hyprctl monitors -j | jq -r ".[] | select(.name == \"$mon_name\") | .availableModes[0]"
}

INT_RES=$(get_native_res "$INTERNAL")
EXT_RES=$(get_native_res "$EXTERNAL")

# Fallback logic for NVIDIA quirks
: "${INTERNAL:=eDP-1}"
: "${EXTERNAL:=HDMI-A-1}"
[ -z "$INT_RES" ] || [ "$INT_RES" == "null" ] && INT_RES="preferred"
[ -z "$EXT_RES" ] || [ "$EXT_RES" == "null" ] && EXT_RES="preferred"

options="󰍹 Laptop Only\n󰍹 External Only\n󰒶 Mirror\n󰆊 Extend (Right)"
chosen=$(echo -e "$options" | rofi -dmenu -i -p "Display Setup")

case "$chosen" in
    *"Laptop Only"*)
        hyprctl keyword monitor "$INTERNAL,$INT_RES,auto,1"
        hyprctl keyword monitor "$EXTERNAL,disable"
        ;;
    *"External Only"*)
        # Ensure external is enabled before disabling internal
        hyprctl keyword monitor "$EXTERNAL,$EXT_RES,auto,1"
        hyprctl keyword monitor "$INTERNAL,disable"
        ;;
    *"Mirror"*)
        hyprctl keyword monitor "$INTERNAL,$INT_RES,auto,1"
        hyprctl keyword monitor "$EXTERNAL,$EXT_RES,auto,1,mirror,$INTERNAL"
        ;;
    *"Extend"*)
        hyprctl keyword monitor "$INTERNAL,$INT_RES,0x0,1"
        hyprctl keyword monitor "$EXTERNAL,$EXT_RES,auto,1"
        ;;
    *) exit 0 ;;
esac

# 3. NVIDIA-specific Waybar Refresh
# The 580xx driver might take a millisecond longer to swap buffers
pkill -9 waybar
sleep 1.5
rm -rf /tmp/waybar_ipc_addr
waybar & disown

notify-send "YukiOS - display" "Monitor Layout Applied"
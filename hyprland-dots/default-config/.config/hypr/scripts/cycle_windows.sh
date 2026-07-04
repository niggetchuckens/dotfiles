#!/bin/bash

# Cycle through windows. If the active window is fullscreen, 
# it toggles fullscreen off, cycles focus, and then toggles 
# fullscreen back on for the next window.
#
# Usage: ./cycle_windows.sh [prev]

DIRECTION=$1
IS_FULLSCREEN=$(hyprctl activewindow -j | jq -r '.fullscreen')

if [ "$IS_FULLSCREEN" -ne 0 ]; then
    hyprctl dispatch fullscreen 0
    hyprctl dispatch cyclenext $DIRECTION
    hyprctl dispatch fullscreen 0
else
    hyprctl dispatch cyclenext $DIRECTION
fi

#!/bin/bash
sleep 1
killall -e xdg-desktop-portal-hyprland
killall -e xdg-desktop-portal-gtk
killall -e xdg-desktop-portal
if [ -x "/usr/libexec/xdg-desktop-portal-hyprland" ]; then
    PORTAL_DIR="/usr/libexec"
else
    PORTAL_DIR="/usr/lib"
fi

${PORTAL_DIR}/xdg-desktop-portal-hyprland &
sleep 2
${PORTAL_DIR}/xdg-desktop-portal &

#!/bin/bash

updates_arch=$(checkupdates 2>/dev/null | wc -l)
updates_aur=$(yay -Qum 2>/dev/null | wc -l)

total=$((updates_arch + updates_aur))

if [ "$total" -gt 0 ]; then
    echo "{\"text\": \"$total\", \"tooltip\": \"Arch: $updates_arch\nAUR: $updates_aur\"}"
fi
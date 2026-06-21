#!/bin/bash

# 1. Ask for Search Query or URL
INPUT=$(rofi -dmenu -p "Search or Paste URL" -theme-str 'window {width: 60%;}')

# Exit if empty
[[ -z "$INPUT" ]] && exit 1

# 2. Check if input is a URL or a Search
if [[ "$INPUT" =~ ^https?:// ]]; then
    SELECTED_URL=$INPUT
else
    # Perform search using yt-dlp and format for Rofi
    # This gets titles and IDs, then lets you pick one
    SEARCH_RESULTS=$(yt-dlp "ytsearch20:$INPUT" --get-title --get-id --flat-playlist)
    
    # Format results so they look nice in Rofi
    # We use awk to join the title and the ID with a separator
    CHOICE=$(echo "$SEARCH_RESULTS" | awk 'NR%2{title=$0;next} {print title " | " $0}' | rofi -dmenu -i -p "Results" -theme-str 'window {width: 80%;}')
    
    [[ -z "$CHOICE" ]] && exit 1
    
    # Extract the ID from the end of the choice
    VIDEO_ID=$(echo "$CHOICE" | awk -F ' | ' '{print $NF}')
    SELECTED_URL="https://www.youtube.com/watch?v=$VIDEO_ID"
fi

# 3. Play with mpv
notify-send "Opening..." "$SELECTED_URL"
mpv --ytdl-format="bestvideo[height<=1080]+bestaudio/best" "$SELECTED_URL" &

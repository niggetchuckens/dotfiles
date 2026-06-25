#!/usr/bin/env python3
import os
import sys
import tty
import termios
import subprocess

# Colors (ANSI Escape Sequences)
RESET = "\033[0m"
BOLD = "\033[1m"
BLUE = "\033[34m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
MAGENTA = "\033[35m"
RED = "\033[31m"
BG_SELECT = "\033[44m\033[37m" # Blue bg, white fg for selected list item

def get_os_id():
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if line.startswith("ID="):
                    return line.strip().split('=')[1].strip('"')
    except Exception:
        pass
    return "unknown"

OS_ID = get_os_id()

# ASCII Previews for layouts
ASCII_HYPR_FANCY = """
  ┌────────────────────────────────────────────────────────┐
  │ [1] [2] [3] [4]                 12:00 PM  [󰁹 100%]    │  <- Waybar
  │                                                        │
  │     ┌─────────────────────┐                            │
  │     │   Kitty            │                            │
  │     │                     │      ┌───────────────┐     │
  │     │ $ btop              │      │ 󰈀 Firefox     │     │
  │     │                     │      │               │     │
  │     └─────────────────────┘      │ (Mocha Theme) │     │
  │                                  │               │     │
  │                                  └───────────────┘     │
  └────────────────────────────────────────────────────────┘
  * Smooth animations, shadows, rounded corners & Kawase blur.
"""

ASCII_HYPR_MIN = """
  ┌────────────────────────────────────────────────────────┐
  │ [1] [2] [3] [4]                 12:00 PM  [󰁹 100%]    │  <- Waybar
  │                                                        │
  │ ┌───────────────────────────┐┌───────────────────────┐ │
  │ │   Kitty                  ││ 󰈀 Firefox             │ │
  │ │                           ││                       │ │
  │ │ $ neovim                  ││ (Optimized Snapping) │ │
  │ │                           ││                       │ │
  │ └───────────────────────────┘└───────────────────────┘ │
  │                                                        │
  └────────────────────────────────────────────────────────┘
  * Lightweight rendering, no animations, zero-lag compositor.
"""

ASCII_I3_FANCY = """
  ┌────────────────────────────────────────────────────────┐
  │ 1:kitty  2:firefox  3:discord         12:00 - [100%]   │  <- i3bar
  │                                                        │
  │   ┌───────────────────────────┐ ┌───────────────────┐  │
  │   │   Kitty                  │ │ 󰈀 Firefox         │  │
  │   │                           │ │                   │  │
  │   │ $ fastfetch               │ │ (Mocha Theme)     │  │  <- Picom Gaps
  │   │                           │ │                   │  │
  │   └───────────────────────────┘ └───────────────────┘  │
  │                                                        │
  └────────────────────────────────────────────────────────┘
  * Custom Gaps, Picom compositor (shadows, active window focus).
"""

ASCII_I3_MIN = """
  ┌────────────────────────────────────────────────────────┐
  │ 1:kitty  2:firefox  3:discord         12:00 - [100%]   │  <- i3bar
  │                                                        │
  │ ┌─────────────────────────────┐┌─────────────────────┐ │
  │ │   Kitty                     ││ 󰈀 Firefox           │ │
  │ │                             ││                     │ │
  │ │ $ memory: 1.1GB/16GB        ││ (Tight tiling)      │ │
  │ │                             ││                     │ │
  │ └─────────────────────────────┘└─────────────────────┘ │
  │                                                        │
  └────────────────────────────────────────────────────────┘
  * Compositor-free, no gaps, maximum battery & CPU savings.
"""

ASCII_XFCE_FANCY = """
  ┌────────────────────────────────────────────────────────┐
  │   [Kitty] [Firefox]               Tray: 12:00 PM 󰁹   │  <- Panel (90% Opac)
  │                                                        │
  │ ┌───────────────────────────────────────────────┐      │
  │ │ 󰍛  XFCE System Info                           │      │
  │ ├───────────────────────────────────────────────┤      │
  │ │ GTK Theme: Adwaita-dark                       │      │  <- Centered Titles
  │ │ Icons: Papirus-Dark                           │      │
  │ │ Compositor: XFWM Shadow & Inactive Opacity    │      │
  │ └───────────────────────────────────────────────┘      │
  │                                                        │
  └────────────────────────────────────────────────────────┘
  * Clean Top Panel, modern dark theme, compositor shadows, Alt+M powermenu.
"""

ASCII_XFCE_MIN = """
  ┌────────────────────────────────────────────────────────┐
  │   [Kitty] [Firefox]               Tray: 12:00 PM 󰁹   │  <- Panel (Solid)
  │                                                        │
  │ ┌───────────────────────────────────────────────┐      │
  │ │ 󰍛  XFCE System Info (Minimal)                 │      │
  │ ├───────────────────────────────────────────────┤      │
  │ │ GTK Theme: Default System                     │      │
  │ │ Window Drags: Wireframes (CPU optimized)      │      │  <- Zero Eye Candy
  │ │ Compositor: DISABLED                          │      │
  │ └───────────────────────────────────────────────┘      │
  │                                                        │
  └────────────────────────────────────────────────────────┘
  * Clean layouts, zero transparency, solid panel, keyboard workflow.
"""

# Options Data Structure
OPTIONS = [
    {
        "name": "Hyprland (Fancy Build)",
        "type": "Wayland WM",
        "compositor": "Hyprland (Built-in)",
        "features": "Kawase blur, rounded corners, drop shadows, custom animations",
        "script": "hyprland-dots/default-config/install.py",
        "ascii": ASCII_HYPR_FANCY
    },
    {
        "name": "Hyprland (Minimalist Build)",
        "type": "Wayland WM",
        "compositor": "Hyprland (Optimized)",
        "features": "Animations off, zero blur, maximum fps, battery-saver profiles",
        "script": "hyprland-dots/minimalist-config/install.py",
        "ascii": ASCII_HYPR_MIN
    },
    {
        "name": "i3 Window Manager (Fancy Build)",
        "type": "X11 WM",
        "compositor": "Picom (Shadows & Fading)",
        "features": "Custom gaps, blurred terminal, drop shadows, workspace tiling",
        "script": "i3-dots/fancy-config/install.py",
        "ascii": ASCII_I3_FANCY
    },
    {
        "name": "i3 Window Manager (Minimalist Build)",
        "type": "X11 WM",
        "compositor": "None (Compositor Off)",
        "features": "No gaps, sharp edges, instant window focus, zero memory overhead",
        "script": "i3-dots/minimalist-config/install.py",
        "ascii": ASCII_I3_MIN
    },
    {
        "name": "XFCE4 Desktop (Fancy Build)",
        "type": "X11 DE",
        "compositor": "XFWM (Built-in, Shadows On)",
        "features": "90% transparent panel, centered titles, inactive window dimming",
        "script": "xfce/fancy-config/install.py",
        "ascii": ASCII_XFCE_FANCY
    },
    {
        "name": "XFCE4 Desktop (Minimalist Build)",
        "type": "X11 DE",
        "compositor": "None (Compositor Off)",
        "features": "Solid panel, box wireframe window movements, maximum desktop speed",
        "script": "xfce/minimalist-config/install.py",
        "ascii": ASCII_XFCE_MIN
    }
]

def get_key():
    """Reads a single keypress from standard input without requiring enter."""
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch2 = sys.stdin.read(2)
            if ch2 == '[A':
                return 'up'
            elif ch2 == '[B':
                return 'down'
        elif ch in ('\r', '\n'):
            return 'enter'
        elif ch.lower() == 'q':
            return 'quit'
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return None

def clear_screen():
    os.system("clear")

def print_menu(selected_idx):
    clear_screen()
    
    # Splash Banner
    print(f"{BOLD}{BLUE}╔══════════════════════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{BLUE}║                   YukiOS Configuration Hub & Installer                   ║{RESET}")
    os_text = f"[Detected OS: {OS_ID.capitalize()}]"
    padding = (74 - len(os_text)) // 2
    os_line = "║" + " " * padding + os_text + " " * (74 - len(os_text) - padding) + "║"
    print(f"{BOLD}{BLUE}{os_line}{RESET}")
    print(f"{BOLD}{BLUE}╚══════════════════════════════════════════════════════════════════════════╝{RESET}\n")
    print(f"{YELLOW}Use Arrow Keys (↑/↓) to highlight profiles. Press Enter to Install. 'q' to Quit.{RESET}\n")
    
    col_width = 38
    print(f"{BOLD}{CYAN}Available Profiles:{RESET}".ljust(col_width) + f"{BOLD}{CYAN}Live Layout Preview & Specs:{RESET}")
    print(f"─" * 32 + " " * 6 + "─" * 58)

    # Render Options & Preview side-by-side
    current_opt = OPTIONS[selected_idx]
    ascii_lines = current_opt["ascii"].strip("\n").split("\n")
    
    for idx, opt in enumerate(OPTIONS):
        # Format left menu item
        name_str = opt["name"]
        if idx == selected_idx:
            # Highlighted item
            prefix = " > "
            item_line = f"{BOLD}{BG_SELECT}{prefix}{name_str.ljust(col_width-5)}{RESET}"
        else:
            prefix = "   "
            item_line = f"{prefix}{name_str.ljust(col_width-3)}"
            
        # Draw left item, padding spaces if needed, then draw right column line
        if idx < len(ascii_lines):
            print(f"{item_line}    {ascii_lines[idx]}")
        else:
            print(f"{item_line}")
            
    # Draw any remaining ascii layout preview lines
    for idx in range(len(OPTIONS), len(ascii_lines)):
        print(" " * col_width + f"    {ascii_lines[idx]}")
        
    # Render specifications section at the bottom
    print("\n" + "─" * 96)
    print(f"{BOLD}{GREEN}Specifications for: {current_opt['name']}{RESET}")
    print(f"  • {BOLD}Profile Type:{RESET}  {current_opt['type']}")
    print(f"  • {BOLD}Compositor:  {RESET}  {current_opt['compositor']}")
    print(f"  • {BOLD}Highlights:  {RESET}  {current_opt['features']}")
    print(f"  • {BOLD}Setup Script:{RESET}  {current_opt['script']}")
    print("─" * 96)

def main():
    # Hide cursor
    print("\033[?25l", end="")
    selected_idx = 0
    
    try:
        while True:
            print_menu(selected_idx)
            key = get_key()
            
            if key == 'up':
                selected_idx = (selected_idx - 1) % len(OPTIONS)
            elif key == 'down':
                selected_idx = (selected_idx + 1) % len(OPTIONS)
            elif key == 'enter':
                # Re-enable cursor and clear screen
                print("\033[?25h", end="")
                clear_screen()
                
                selected_opt = OPTIONS[selected_idx]
                script_path = selected_opt["script"]
                script_dir = os.path.dirname(script_path)
                script_name = os.path.basename(script_path)
                
                print(f"{BOLD}{GREEN}[INFO] Starting system setup for {selected_opt['name']}...{RESET}\n")
                
                # Execute target install.py
                try:
                    subprocess.run([sys.executable, script_name], cwd=script_dir, check=True)
                except subprocess.CalledProcessError as e:
                    print(f"\n{RED}[ERROR] Installation script failed: {e}{RESET}")
                    input(f"\n{YELLOW}Press Enter to exit...{RESET}")
                    sys.exit(1)
                except KeyboardInterrupt:
                    print(f"\n{YELLOW}[WARN] Installation cancelled by user.{RESET}")
                    input(f"\n{YELLOW}Press Enter to exit...{RESET}")
                    sys.exit(0)
                break
            elif key == 'quit':
                break
    finally:
        # Re-enable cursor
        print("\033[?25h", end="")
        clear_screen()
        print("Goodbye!")

if __name__ == "__main__":
    main()

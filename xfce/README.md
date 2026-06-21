# 🐭 XFCE4 Dotfiles (Fancy & Minimalist)

This repository contains fully optimized XFCE4 desktop environment configuration profiles matching the Catppuccin Mocha aesthetic of the original Hyprland/i3 dotfiles. 

Unlike a tiling window manager, this configuration preserves the full Desktop Environment experience, but it is heavily optimized for a fast, keyboard-driven workflow with all distracting window animations and fancy workspace effects disabled in the minimalist build, and sleek modern aesthetics in the fancy build.

## 📁 Repository Structure

```
xfce/
├── fancy-config/             # High visual fidelity setup (shadows, blur, transparent terminal)
│   ├── .config/
│   │   ├── xfce4/            # XFCE core settings (panel with transparent Mocha base, xsettings, custom shortcuts)
│   │   │   ├── xfconf/xfce-perchannel-xml/
│   │   │   │     ├── xfce4-panel.xml
│   │   │   │     ├── xfwm4.xml (compositing enabled, shadows, title centered)
│   │   │   │     └── xsettings.xml
│   │   │   └── terminal/     # Catppuccin Mocha theme for XFCE Terminal fallback
│   │   └── picom/            # Picom configurations
│   └── install.py            # Installer script for the fancy profile
│
├── minimalist-config/        # Low-overhead performance profile (compositor off, wireframe resizing, zero bloat)
│   ├── .config/
│   │   └── xfce4/            # XFCE core settings (tiling-ready window snapping, compositor disabled)
│   │       ├── xfconf/xfce-perchannel-xml/
│   │       │     ├── xfce4-panel.xml
│   │       │     ├── xfwm4.xml (compositing disabled, wireframe dragging, fast window snapping)
│   │       │     └── xsettings.xml
│   │       └── terminal/     # High contrast dark theme for XFCE Terminal fallback
│   └── install.py            # Installer script for the minimalist profile
│
└── README.md                 # This file
```

---

## 🚀 Installation & Setup

Choose your preferred configuration profile and run the corresponding installation script. The script handles stopping background daemons (`xfconfd`) during installation to prevent them from overwriting the files, then copies the settings and installs standard utilities.

### Option A: Minimalist Setup (Recommended for low-end CPUs or maximum speed)
To install the lightweight profile with no compositing overhead and instant window manipulation:
```bash
cd dotfiles/xfce/minimalist-config
python3 install.py
```

### Option B: Fancy Setup (With shadows, transparent terminal, and title borders)
To install the visually rich profile:
```bash
cd dotfiles/xfce/fancy-config
python3 install.py
```

---

## ⌨️ Optimized Workflow Keybindings

We have updated the default XFCE4 keybindings to exactly match the keyboard-driven workflow of the Hyprland and i3 setups:

| Keybinding | Action |
|------------|--------|
| `ALT + Return` | Open Kitty Terminal |
| `ALT + W` | Run Application Launcher (Rofi) |
| `ALT + Shift + W` | Run Command Launcher (Rofi) |
| `ALT + Q` | Close current window |
| `ALT + F` | Toggle fullscreen |
| `ALT + V` | Stick/Float window |
| `ALT + [1-9]` | Switch to Workspace 1-9 |
| `ALT + Shift + [1-9]` | Move window to Workspace 1-9 |
| `SUPER + Left/Right/Up/Down` | Snap/Tile window to Left/Right/Top/Bottom |
| `SUPER + Shift + S` | Capture selection screenshot to clipboard (needs `maim`) |
| `Ctrl + Alt + Delete` | Lock Screen (`xflock4`) |

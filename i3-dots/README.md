# 🪟 i3 Dotfiles (Fancy & Minimalist)

This repository contains fully optimized and ported i3 window manager configuration profiles matching the Catppuccin Mocha aesthetic of the original Hyprland dotfiles.

## 📁 Repository Structure

```
i3-dots/
├── fancy-config/             # High visual fidelity setup (shadows, blur, fading, gaps)
│   ├── .config/
│   │   ├── i3/config        # Configured to use picom compositor, gaps, & shadows
│   │   ├── i3status/config  # Standard status bar metrics
│   │   └── picom/picom.conf # Picom compositor with dual-kawase blur & rounded corners
│   └── install.py           # Installer script for the fancy profile
│
└── minimalist-config/        # Low-overhead performance profile (no compositor, tight gaps)
    ├── .config/
    │   ├── i3/config        # Compositor-free config optimized for Celeron/Pentium CPUs
    │   └── i3status/config  # Standard status bar metrics
    └── install.py           # Installer script for the minimalist profile
```

---

## 🚀 Installation & Setup

Choose your preferred configuration profile and run the corresponding installation script.

### Option A: Minimalist Setup (Recommended for low-end CPUs)
To install the lightweight profile with no compositing overhead:
```bash
cd dotfiles/i3-dots/minimalist-config
python3 install.py
```

### Option B: Fancy Setup (With shadows, blur, and rounded corners)
To install the visually rich profile with window effects:
```bash
cd dotfiles/i3-dots/fancy-config
python3 install.py
```

---

## ⌨️ Common Keybindings

| Keybinding | Action |
|------------|--------|
| `ALT + Return` | Open Kitty Terminal |
| `ALT + W` | Run Application Launcher (Rofi) |
| `ALT + Shift + W` | Run Command Launcher (Rofi) |
| `ALT + Q` | Close current window |
| `ALT + F` | Toggle fullscreen |
| `ALT + V` | Toggle floating state |
| `ALT + Shift + C` | Reload i3 Configuration |
| `ALT + Shift + R` | Restart i3 Window Manager |
| `ALT + [1-9,0]` | Switch workspace |
| `ALT + Shift + [1-9,0]` | Move window to workspace |
| `SUPER + Shift + S` | Capture selection screenshot to clipboard (needs `maim`) |

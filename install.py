import subprocess
import os
import shutil
import sys
import argparse
from datetime import datetime

BLUE, GREEN, YELLOW, RED, NC = '\033[0;34m', '\033[0;32m', '\033[1;33m', '\033[0;31m', '\033[0m'

def print_info(msg):
    print(f"{BLUE}[INFO]{NC} {msg}")

def run(cmd):
    subprocess.run(cmd, shell=True, check=True)

def print_success(msg):
    print(f"{GREEN}[SUCCESS]{NC} {msg}")

def print_error(msg):
    print(f"{RED}[ERROR]{NC} {msg}")
    
def copy_folder(src_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, src_name)
    destination = os.path.join(os.path.expanduser("~"), src_name)

    if os.path.exists(source):
        print_info(f"Copying {src_name} to {destination}...")
        run(f"cp -r {source}/* {destination}/")
    else:
        print(f"{YELLOW}[WARN]{NC} Source {src_name} not found.")

def get_distro():
    info = {}
    try:
        with open("/etc/os-release") as f:
            for line in f:
                if "=" in line:
                    k, v = line.rstrip().split("=", 1)
                    info[k] = v.strip('"')
    except FileNotFoundError:
        return "unknown", []
    return info.get("ID", ""), info.get("ID_LIKE", "").split()

def main(confirm: str = None):
    # Splash screen updated to YukiOS
    print(f"\n{BLUE}╔════════════════════════════════════════════╗{NC}")
    print(f"{BLUE}║           YukiOS dotfiles installer        ║{NC}")
    print(f"{BLUE}╚════════════════════════════════════════════╝{NC}\n")

    if confirm is None:
        confirm = input(f"{YELLOW}[?]{NC} Do you want to proceed with the installation? [y/N]: ")
    if confirm.lower() != 'y':
        print_info("Installation cancelled.")
        return
    
    distro, id_like = get_distro()

    # --- 1. Package Installation ---
    if distro in ['arch', 'manjaro', 'endeavouros'] or 'arch' in id_like:
        print_info("Arch-based system detected. Using yay...")
        # amd-ucode removed as per instructions. pulseaudio removed to avoid conflict.
        pkgs = ("hyprland sddm waybar kitty rofi-wayland pavucontrol "
                "pipewire pipewire-pulse pipewire-jack wireplumber dunst "
                "polkit-kde-agent qt5-wayland qt6-wayland xdg-desktop-portal-hyprland "
                "grim slurp wl-clipboard swaylock swayidle brightnessctl "
                "bluez bluez-utils blueman thunar fastfetch htop btop neovim git "
                "noto-fonts noto-fonts-emoji ttf-font-awesome ttf-jetbrains-mono-nerd "
                "nvidia nvidia-utils libva-nvidia-driver docker")
        run("yay -Syu --noconfirm")
        run(f"yay -S --needed --noconfirm {pkgs}")

    elif distro in ['debian', 'ubuntu', 'pop', 'trixie'] or 'debian' in id_like:
        print_info("Debian-based system detected. Using apt...")
        # Fixed font names for Trixie and replaced neofetch with fastfetch.
        pkgs = ("hyprland sddm waybar kitty rofi-wayland pavucontrol "
                "pipewire pipewire-audio-client-libraries pipewire-pulse wireplumber "
                "dunst polkit-kde-agent fonts-noto-core fonts-noto-color-emoji "
                "fonts-font-awesome fonts-jetbrains-mono xdg-desktop-portal-hyprland "
                "grim slurp wl-clipboard swaylock swayidle brightnessctl "
                "bluez blueman thunar fastfetch htop btop neovim git docker.io "
                "nvidia-driver libva-wayland2")
        run("sudo apt update && sudo apt install -y " + pkgs)

    elif distro in ['fedora'] or 'fedora' in id_like:
        print_info("Fedora system detected. Using dnf...")
        pkgs = ("hyprland sddm waybar kitty rofi-wayland pavucontrol "
                "pipewire pipewire-pulseaudio wireplumber dunst polkit-kde "
                "qt5-qtwayland qt6-qtwayland xdg-desktop-portal-hyprland grim slurp "
                "wl-clipboard swaylock swayidle brightnessctl bluez blueman "
                "thunar fastfetch htop btop neovim git google-noto-fonts "
                "google-noto-emoji-fonts fontawesome-fonts jetbrains-mono-fonts docker")
        run(f"sudo dnf install -y {pkgs}")

    # --- 2. Hardware / NVIDIA Environment Variables ---
    print_info("Configuring NVIDIA/Wayland environment variables...")
    env_fixes = [
        '\n# YukiOS Hardware Fixes\n',
        'export LIBVA_DRIVER_NAME=nvidia\n',
        'export XDG_SESSION_TYPE=wayland\n',
        'export GBM_BACKEND=nvidia-drm\n',
        'export __GLX_VENDOR_LIBRARY_NAME=nvidia\n',
        'export WLR_NO_HARDWARE_CURSORS=1\n',
        'alias neofetch="fastfetch"\n'
    ]
    bashrc_path = os.path.expanduser("~/.bashrc")
    with open(bashrc_path, "a") as f:
        f.writelines(env_fixes)

    # --- 3. Deploy Dotfiles ---
    print(f"{BLUE}[INFO]{NC} Deploying dotfiles...")
    os.makedirs(os.path.expanduser("~/.config"), exist_ok=True) 
    os.makedirs(os.path.expanduser("~/.local"), exist_ok=True)  
    os.makedirs(os.path.expanduser("~/.scripts"), exist_ok=True) 

    copy_folder(".config") 
    copy_folder(".local")  
    copy_folder(".scripts") 

    # --- 4. Enable Services ---
    for service in ["sddm", "bluetooth", "docker"]:
        try:
            run(f"sudo systemctl enable {service}")
        except:
            pass

    print_success("YukiOS setup complete! Please reboot your system.")

if __name__ == "__main__":
    if os.geteuid() == 0:
        print_error("Do not run this script as root. It uses sudo/yay internally.")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation")
    args = parser.parse_args()
    main(confirm='y' if args.yes else None)
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

def build_hyprland_debian():
    """Builds Hyprland from source for Debian users."""
    print_info("Building Hyprland from source for Debian...")
    # Essential build dependencies for Debian
    build_deps = ("meson wget build-essential ninja-build cmake gettext gettext-base "
                  "fontconfig libfontconfig-dev libffi-dev libxml2-dev libdrm-dev "
                  "libxkbcommon-dev libpixman-1-dev libudev-dev libgbm-dev "
                  "libinput-dev libwayland-dev wayland-protocols libdisplay-info-dev "
                  "libhwdata-dev libavutil-dev libavcodec-dev libavformat-dev "
                  "libswscale-dev libliftoff-dev libseat-dev libxcb-composite0-dev "
                  "libxcb-dri3-dev libxcb-present-dev libxcb-render0-dev "
                  "libxcb-res0-dev libxcb-shm0-dev libxcb-terminate0-dev "
                  "libxcb-xfixes0-dev libxcb-xkb-dev libxcb-xinput-dev libxcb-util-dev")
    run(f"sudo apt install -y {build_deps}")

    # Build and install Hyprland
    build_dir = os.path.expanduser("~/hyprland_build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
    
    run(f"git clone --recursive https://github.com/hyprwm/Hyprland {build_dir}")
    run(f"cd {build_dir} && make all && sudo make install")
    print_success("Hyprland built and installed successfully.")

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
    # YukiOS Splash Screen
    print(f"\n{BLUE}╔════════════════════════════════════════════╗{NC}")
    print(f"{BLUE}║           YukiOS dotfiles installer        ║{NC}")
    print(f"{BLUE}╚════════════════════════════════════════════╝{NC}\n")

    if confirm is None:
        confirm = input(f"{YELLOW}[?]{NC} Do you want to proceed? [y/N]: ")
    if confirm.lower() != 'y':
        print_info("Installation cancelled.")
        return
    
    distro, id_like = get_distro()

    # --- 1. Package Installation ---
    if distro in ['arch', 'manjaro', 'endeavouros'] or 'arch' in id_like:
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
        print_info("Debian system detected. Enabling non-free repos and building Hyprland...")
        run("sudo apt-get install -y software-properties-common")
        run("sudo apt-add-repository non-free-firmware contrib non-free -y")
        run("sudo apt update")
        
        pkgs = ("sddm waybar kitty pavucontrol pipewire pipewire-pulse wireplumber "
                "dunst fonts-noto-core fonts-noto-color-emoji fonts-font-awesome "
                "fonts-jetbrains-mono grim slurp wl-clipboard swaylock swayidle "
                "brightnessctl bluez blueman thunar fastfetch htop btop neovim git "
                "docker.io nvidia-driver libva-wayland2")
        run("sudo apt install -y " + pkgs)
        
        # Build Hyprland since it's missing from Trixie repos
        build_hyprland_debian()

    # --- 2. Copy Dotfiles ---
    print_info("Deploying dotfiles...")
    os.makedirs(os.path.expanduser("~/.config"), exist_ok=True)
    os.makedirs(os.path.expanduser("~/.local"), exist_ok=True)
    os.makedirs(os.path.expanduser("~/.scripts"), exist_ok=True) 

    copy_folder(".config")
    copy_folder(".local")
    copy_folder(".scripts")

    # --- 3. Hardware Fixes & Alias ---
    bashrc_path = os.path.expanduser("~/.bashrc")
    with open(bashrc_path, "a") as f:
        f.write('\n# YukiOS Hardware Fixes\n')
        f.write('export LIBVA_DRIVER_NAME=nvidia\n')
        f.write('export XDG_SESSION_TYPE=wayland\n')
        f.write('export GBM_BACKEND=nvidia-drm\n')
        f.write('export __GLX_VENDOR_LIBRARY_NAME=nvidia\n')
        f.write('export WLR_NO_HARDWARE_CURSORS=1\n')
        f.write('alias neofetch="fastfetch"\n')

    # --- 4. Enable Services ---
    for service in ["sddm", "bluetooth", "docker"]:
        try:
            run(f"sudo systemctl enable {service}")
        except:
            pass

    print_success("YukiOS setup complete! Please reboot.")

if __name__ == "__main__":
    if os.geteuid() == 0:
        print_error("Do not run as root. The script uses sudo internally.")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--yes", action="store_true")
    args = parser.parse_args()
    main(confirm='y' if args.yes else None)
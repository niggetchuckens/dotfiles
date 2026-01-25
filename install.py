import subprocess
import os
import shutil
import sys
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
        print(f"{BLUE}[INFO]{NC} Copying {src_name} to {destination}...")
        run(f"cp -r {source}/* {destination}/")
    else:
        print(f"{YELLOW}[WARN]{NC} Source {src_name} not found in script directory.")
    
def get_distro():
    info = {}
    with open("/etc/os-release") as f:
        for line in f:
            if "=" in line:
                k, v = line.rstrip().split("=", 1)
                info[k] = v.strip('"')
    return info.get("ID", ""), info.get("ID_LIKE", "").split()

def run_command(cmd, shell=True):
    try:
        subprocess.run(cmd, shell=shell, check=True)
    except subprocess.CalledProcessError as e:
        print_error(f"Command failed: {cmd}")
        sys.exit(1)

def main():
    print(f"\n{YELLOW}╔════════════════════════════════════════════╗{NC}")
    print(f"{YELLOW}║   Hyprland Python Installer                ║{NC}")
    print(f"{YELLOW}╚════════════════════════════════════════════╝{NC}\n")

    # Confirmation
    confirm = input(f"{YELLOW}[?]{NC} This will install Hyprland and related packages. Continue? (y/N): ")
    if confirm.lower() != 'y':
        print_info("Installation cancelled")
        return
    
    distro, id_like = get_distro()
    # 1. Install Full Package Lists
    if distro in ['arch', 'manjaro', 'endeavouros'] or 'arch' in id_like:
        pkgs = ("hyprland sddm waybar kitty rofi-wayland pavucontrol "
                "pipewire pipewire-pulse wireplumber dunst polkit-kde-agent "
                "qt5-wayland qt6-wayland xdg-desktop-portal-hyprland grim slurp "
                "wl-clipboard swaylock swayidle brightnessctl network-manager-applet "
                "bluez bluez-utils blueman thunar neofetch htop btop neovim git curl "
                "wget unzip zip tar gzip noto-fonts noto-fonts-emoji "
                "ttf-font-awesome ttf-jetbrains-mono-nerd docker oh-my-posh rclone github-copilot-cli nodejs npm")
        run_command("yay -Syu --noconfirm")
        run_command(f"yay -S --needed --noconfirm {pkgs}")
        run_command("curl -fsSL https://gh.io/copilot-install | bash")
        run_command("export PATH=\"$PATH:/home/hime/.local/bin\"")
    
    elif distro in ['ubuntu', 'debian', 'pop'] or 'debian' in id_like:
        pkgs = ("sddm pulseaudio pavucontrol pipewire pipewire-pulse wireplumber "
                "dunst rofi kitty grim slurp wl-clipboard swaylock swayidle "
                "brightnessctl network-manager-gnome bluez blueman thunar fastfetch "
                "htop neovim git curl wget unzip zip tar gzip fonts-noto-core "
                "fonts-noto-color-emoji fonts-font-awesome docker.io")
        run("sudo apt update && sudo apt install -y " + pkgs)
        
    elif distro == 'fedora':
        pkgs = ("hyprland sddm waybar kitty rofi-wayland pulseaudio pavucontrol "
                "pipewire pipewire-pulseaudio wireplumber dunst polkit-kde "
                "qt5-qtwayland qt6-qtwayland xdg-desktop-portal-hyprland grim slurp "
                "wl-clipboard swaylock swayidle brightnessctl network-manager-applet "
                "bluez bluez-tools blueman thunar neofetch htop btop neovim git curl "
                "wget unzip zip tar gzip google-noto-fonts google-noto-emoji-fonts "
                "fontawesome-fonts jetbrains-mono-fonts docker")
        run_command(f"sudo dnf install -y {pkgs}")

    # 2. Copy Dotfiles
    print(f"{BLUE}[INFO]{NC} Deploying dotfiles...")
    os.makedirs(os.path.expanduser("~/.config"), exist_ok=True)
    os.makedirs(os.path.expanduser("~/.local"), exist_ok=True)
    
    copy_folder(".config")
    copy_folder(".local")
    copy_folder(".scripts")
    copy_folder("oh-my-posh")

    # 3. Enable Services
    for service in ["sddm", "bluetooth", "NetworkManager", "docker"]:
        try:
            run_command(f"sudo systemctl enable {service}.service")
        except:
            pass

    print(f"{GREEN}[SUCCESS]{NC} Setup complete! Please reboot.")

if __name__ == "__main__": 

    if os.geteuid() == 0:
        print_error("Please do not run this script as root (use sudo within the script instead)")
        sys.exit(1)

    main()
import shutil
import subprocess
import os
import argparse
import sys
import getpass
import install_fonts

BLUE, GREEN, YELLOW, RED, NC = '\033[0;34m', '\033[0;32m', '\033[1;33m', '\033[0m', '\033[0m'

def print_info(msg):
    print(f"{BLUE}[INFO]{NC} {msg}")

def print_success(msg):
    print(f"{GREEN}[SUCCESS]{NC} {msg}")

def print_error(msg):
    print(f"{RED}[ERROR]{NC} {msg}")
    
def copy_folder(src_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, src_name)
    user_home = os.path.expanduser("~")
    destination = os.path.join(user_home, src_name)

    if os.path.exists(source):
        print(f"{BLUE}[INFO]{NC} Copying {src_name} to {destination}...")
        os.makedirs(destination, exist_ok=True)
        run_command(f"cp -r {source}/* {destination}/")
    else:
        print(f"{YELLOW}[WARN]{NC} Source {src_name} not found in script directory.")
    
def copy_file(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, file_name)
    user_home = os.path.expanduser("~")
    destination = os.path.join(user_home, file_name)

    if os.path.exists(source):
        print(f"{BLUE}[INFO]{NC} Copying {file_name} to {user_home}...")
        run_command(f"cp {source} {destination}")
    else:
        print(f"{YELLOW}[WARN]{NC} {file_name} not found in script directory.")
        
def run_command(cmd, shell=True):
    try:
        subprocess.run(cmd, shell=shell, check=True)
    except subprocess.CalledProcessError:
        print_error(f"Command failed: {cmd}")
        sys.exit(1)

def main(confirm = None):
    current_user = getpass.getuser()
    user_home = os.path.expanduser("~")

    print(f"\n{BLUE}╔════════════════════════════════════════════╗{NC}")
    print(f"{BLUE}║           YukiOS dotfiles installer        ║{NC}")
    print(f"{BLUE}╚════════════════════════════════════════════╝{NC}\n")

    if confirm is None:
        confirm = input(f"{YELLOW}[?]{NC} Proceed with installation for user '{current_user}'? [y/N]: ")
    if confirm.lower() != 'y': return

    # --- 1. Install Packages ---       
    pkgs = (
                "hyprland wget sddm xdg-desktop-portal-hyprland wayland wl-clipboard xorg-xwayland "
                "waybar rofi wofi hyprpolkitagent wlogout dunst kitty nautilus grim slurp cliphist "
                "swaybg brightnessctl pipewire wireplumber pipewire-pulse pavucontrol sunshine portproton "
                "playerctl network-manager-applet power-profiles-daemon visual=studio-code-bin "
                "polkit gnome-keyring discord fastfetch neovim pacman-contrib spotify vesktop "
                "ttf-commit-mono-nerd papirus-icon-theme bibata-cursor-theme oh-my-posh gemini-cli "
                "tor python-requests python-pysocks psmisc iptables "
            )
    
    yay = shutil.which("yay")
    if not yay:
        print_info("Installing yay AUR helper...")
        run_command("sudo pacman -S --needed --noconfirm base-devel git")
        run_command(f"git clone https://aur.archlinux.org/yay.git /tmp/yay && cd /tmp/yay && makepkg -si --noconfirm")
        print_success("yay installed successfully.")    
    
    commands = (   
                f"yay -Syu --needed --noconfirm {pkgs}",
                f"export PATH=\"$PATH:{user_home}/.local/bin\""
            )
    for command in commands:
        run_command(command)
        
    sunshine = input(f"{YELLOW}[?]{NC} Install Sunshine (Game Streaming Server)? [y/N]: ")
    if sunshine.lower() == 'y':
        print_info("Installing Sunshine...")
        sunshine_commands = (
            f"wget {sunshine_url} -O {user_home}/sunshine.pkg.tar.zst",
            f"sudo pacman -U {user_home}/sunshine.pkg.tar.zst --noconfirm",
            f"rm {user_home}/sunshine.pkg.tar.zst",
            "systemctl --user enable sunshine") # Enable sunshine service for github build bc the yay installation need lots of ram (my 16gb can't match that :c )
        for command in sunshine_commands:
            run_command(command)
   

    # --- 2. Deploy Dotfiles ---
    
    for folder in [".config", ".local", ".scripts"]:
        os.makedirs(os.path.join(user_home, folder), exist_ok=True)
        copy_folder(folder)
        copy_file(".bashrc")

    install_fonts.main()

    # --- 3. Enable Services ---

    system_services = ["sddm", "NetworkManager", "power-profiles-daemon", "tailscaled", "avahi-daemon"]
    for svc in system_services:
        try:
            run_command(f"sudo systemctl enable {svc}.service")
        except: pass

    try:
        run_command("systemctl --user enable sunshine-boot.service")
    except: pass

    # --- 5. System Configuration ---
    print_info("Configuring system time and timezone...")
    try:
        run_command("sudo timedatectl set-timezone America/Santiago")
        run_command("sudo timedatectl set-ntp true")
        run_command("sudo hwclock --systohc")
        print_success("Timezone and NTP configured.")
    except:
        print_error("Failed to configure timezone/NTP.")

    print(f"{GREEN}[SUCCESS]{NC} YukiOS setup complete for {current_user}! Please reboot.")

if __name__ == "__main__": 
    if os.geteuid() == 0:
        print_error("Please do not run this script as root (use sudo within the script instead)")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--yes", action="store_true")
    args = parser.parse_args()
    main(confirm='y' if args.yes else None)

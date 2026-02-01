import subprocess
import os
import argparse
import sys
import getpass

BLUE, GREEN, YELLOW, RED, NC = '\033[0;34m', '\033[0;32m', '\033[1;33m', '\033[0m', '\033[0m'

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
    user_home = os.path.expanduser("~")
    destination = os.path.join(user_home, src_name)

    if os.path.exists(source):
        print(f"{BLUE}[INFO]{NC} Copying {src_name} to {destination}...")
        os.makedirs(destination, exist_ok=True)
        run(f"cp -r {source}/* {destination}/")
    else:
        print(f"{YELLOW}[WARN]{NC} Source {src_name} not found in script directory.")
    
def copy_file(file_name):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, file_name)
    user_home = os.path.expanduser("~")
    destination = os.path.join(user_home, file_name)

    if os.path.exists(source):
        print(f"{BLUE}[INFO]{NC} Copying {file_name} to {user_home}...")
        run(f"cp {source} {destination}")
    else:
        print(f"{YELLOW}[WARN]{NC} {file_name} not found in script directory.")
        
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

def run_command(cmd, shell=True):
    try:
        subprocess.run(cmd, shell=shell, check=True)
    except subprocess.CalledProcessError:
        print_error(f"Command failed: {cmd}")
        sys.exit(1)

def main(confirm = None):
    current_user = getpass.getuser()
    user_home = os.path.expanduser("~")

    # YukiOS Splash Screen with yukivim
    print(f"\n{BLUE}╔════════════════════════════════════════════╗{NC}")
    print(f"{BLUE}║           YukiOS dotfiles installer        ║{NC}")
    print(f"{BLUE}╚════════════════════════════════════════════╝{NC}\n")

    if confirm is None:
        confirm = input(f"{YELLOW}[?]{NC} Proceed with installation for user '{current_user}'? [y/N]: ")
    if confirm.lower() != 'y': return
    
    distro, id_like = get_distro()
  
    # --- 1. Distro Specific Setup ---
    # Package lists updated to match APPS.md requirements
    if distro in ['arch', 'manjaro', 'endeavouros'] or 'arch' in id_like:
        sunshine_url = 'https://github.com/LizardByte/Sunshine/releases/download/v2026.131.3509/sunshine-2026.131.3509-1-x86_64.pkg.tar.zst'
        
        pkgs = ("hyprland wget sddm xdg-desktop-portal-hyprland wayland wl-clipboard xorg-xwayland "
                "waybar rofi wofi hyprpolkitagent wlogout dunst kitty nautilus grim slurp cliphist "
                "swaybg brightnessctl pipewire wireplumber pipewire-pulse pavucontrol "
                "playerctl networkmanager network-manager-applet power-profiles-daemon "
                "polkit gnome-keyring discord fastfetch neovim pacman-contrib "
                "ttf-commit-mono-nerd papirus-icon-theme bibata-cursor-theme oh-my-posh")
        
        
        run_command("yay -Syu --noconfirm")
        run_command(f"yay -S --needed --noconfirm {pkgs}")
        run_command(f"export PATH=\"$PATH:{user_home}/.local/bin\"")
        
        sunshine = input(f"{YELLOW}[?]{NC} Install Sunshine (Game Streaming Server)? [y/N]: ")
        if sunshine.lower() == 'y':
            print_info("Installing Sunshine...")
            run_command(f"wget {sunshine_url} -O {user_home}/sunshine.pkg.tar.zst")
            run_command(f"sudo pacman -U {user_home}/sunshine.pkg.tar.zst --noconfirm")
            run_command(f"rm {user_home}/sunshine.pkg.tar.zst")
            run_command("systemctl --user enable sunshine") # Enable sunshine service for github build bc the yay installation need lots of ram (my 16gb can't match that :c )

        
    
    elif distro in ['ubuntu', 'kali', 'linuxmint'] or 'ubuntu' in id_like:
        # Ubuntu mapping for APPS.md items
        pkgs = ("hyprland xdg-desktop-portal-hyprland wayland-protocols wl-clipboard xwayland "
                "waybar sddm rofi wofi wlogout dunst kitty nautilus grim slurp "
                "brightnessctl pipewire wireplumber pipewire-audio-client-libraries "
                "pavucontrol playerctl network-manager network-manager-gnome "
                "power-profiles-daemon polkitd gnome-keyring "
                "fastfetch neovim fonts-noto papirus-icon-theme cmake g++" 
                "gettext libpolkit-agent-1-dev libpolkit-gobject-1-dev" 
                "libhyprutils-dev libwayland-dev libglib2.0-dev qt6-base-dev"
                "qt6-declarative-dev curl libpolkit-qt6-1-dev meson cpuid")
        
        run_command("sudo apt update")
        run_command(f"sudo apt install -y {pkgs}")
        
        # Hyprpolkitagent manual install
        print_info("Installing hyprpolkitagent...")
        run_command("git clone https://github.com/hyprwm/hyprpolkitagent.git")
        run_command("cd hyprpolkitagent")
        run_command("cmake --no-cache -S . -B build")
        run_command("cmake --build build")
        run_command("sudo cmake --install build")
        
        # Oh-my-posh manual install
        print_info("Installing oh-my-posh...")
        run_command(f"curl -s https://oh-my-posh.dev/install.sh | bash -s -- -d {user_home}/.local/bin")
        
        with open(bashrc_path, "a") as f:
            f.write('export HYPRCURSOR_THEME="Bibata Modern Classic Right"\n')
            f.write('export HYPRCURSOR_SIZE=24\n')
            f.write('export ELECTRON_OZONE_PLATAFORM_HINT=auto\n')
            f.write('export WLR_DRM_NO_ATOMIC=1\n')
            f.write('export WLR_NO_HARDWARE_CURSORS=1\n') 

    elif distro == 'fedora':
        # Fedora mapping for APPS.md items
        pkgs = ("hyprland xdg-desktop-portal-hyprland wayland-utils wl-clipboard xorg-x11-server-Xwayland "
                "waybar rofi wofi wlogout dunst kitty nautilus grim slurp cliphist "
                "swaybg brightnessctl pipewire wireplumber pipewire-pulseaudio pavucontrol "
                "playerctl NetworkManager NetworkManager-adwaita-helper power-profiles-daemon "
                "polkit gnome-keyring discord fastfetch neovim papirus-icon-theme")
        run_command(f"sudo dnf install -y {pkgs}")

    # --- 2. Deploy Dotfiles ---
    for folder in [".config", ".local", ".scripts"]:
        os.makedirs(os.path.join(user_home, folder), exist_ok=True)
        copy_folder(folder)
        copy_file(".bashrc")

    # --- 3. Environment Variables & Alias ---
    # Values taken from APPS.md "Environment Variables" section
    bashrc_path = os.path.join(user_home, ".bashrc")
    with open(bashrc_path, "a") as f:
        f.write('export HYPRCURSOR_THEME="Bibata Modern Classic Right"\n')
        f.write('export HYPRCURSOR_SIZE=24\n')
        f.write('export ELECTRON_OZONE_PLATAFORM_HINT=auto\n')
        f.write('export WLR_DRM_NO_ATOMIC=1\n')

    # --- 4. Enable Services ---
    # User-level services from APPS.md
    user_services = ["hyprpolkitagent", "pipewire", "wireplumber"]
    for svc in user_services:
        try:
            run_command(f"systemctl --user enable {svc}.service")
        except: pass

    # System-level services
    system_services = ["sddm", "NetworkManager", "power-profiles-daemon"]
    for svc in system_services:
        try:
            run_command(f"sudo systemctl enable {svc}.service")
        except: pass

    print(f"{GREEN}[SUCCESS]{NC} YukiOS setup complete for {current_user}! Please reboot.")

if __name__ == "__main__": 
    if os.geteuid() == 0:
        print_error("Please do not run this script as root (use sudo within the script instead)")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--yes", action="store_true")
    args = parser.parse_args()
    main(confirm='y' if args.yes else None)
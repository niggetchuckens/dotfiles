import subprocess
import os
import argparse
import sys
import shutil
import getpass
import install_fonts

BLUE, GREEN, YELLOW, RED, NC = '\033[0;34m', '\033[0;32m', '\033[1;33m', '\033[0m', '\033[0m'

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

    # YukiOS Splash Screen with yukivim
    print(f"\n{BLUE}╔════════════════════════════════════════════╗{NC}")
    print(f"{BLUE}║      YukiOS minimalist i3-dots installer   ║{NC}")
    print(f"{BLUE}╚════════════════════════════════════════════╝{NC}\n")

    if confirm is None:
        confirm = input(f"{YELLOW}[?]{NC} Proceed with installation for user '{current_user}'? [y/N]: ")
    if confirm.lower() != 'y': return
    
    sunshine_url = 'https://github.com/LizardByte/Sunshine/releases/download/v2026.131.3509/sunshine-2026.131.3509-1-x86_64.pkg.tar.zst'
        
    pkgs = (
                "hyprland wget sddm xdg-desktop-portal-hyprland wayland wl-clipboard xorg-xwayland "
                "waybar rofi wofi hyprpolkitagent wlogout dunst kitty nautilus grim slurp cliphist "
                "swaybg brightnessctl pipewire wireplumber pipewire-pulse pavucontrol "
                "playerctl network-manager-applet power-profiles-daemon "
                "polkit gnome-keyring fastfetch neovim pacman-contrib "
                "ttf-commit-mono-nerd papirus-icon-theme bibata-cursor-theme oh-my-posh "
                "i3-wm i3status feh maim xclip"
            )
        
        
    commands = (   
                f"yay -Syu --needed --noconfirm {pkgs}",
                f"export PATH=\"$PATH:{user_home}/.local/bin\""
            )
        
    for command in commands:
        run_command(command)
        
    # --- Communication Apps ---
    discord_choice = input(f"{YELLOW}[?]{NC} Install a Discord Client? (d=Discord, v=Vesktop [Best for Wayland/Screenshare], n=None) [v/d/N]: ")
    if discord_choice.lower() == 'd':
        print_info("Installing standard Discord...")
        if OS_ID == "fedora":
            run_command("sudo flatpak install -y flathub com.discordapp.Discord")
        else:
            run_command("yay -S --needed --noconfirm discord")
    elif discord_choice.lower() == 'v':
        print_info("Installing Vesktop (Optimized Discord)...")
        if OS_ID == "fedora":
            run_command("sudo flatpak install -y flathub dev.vencord.Vesktop")
        else:
            run_command("yay -S --needed --noconfirm vesktop-bin")

    sunshine = input(f"{YELLOW}[?]{NC} Install Sunshine (Game Streaming Server)? [y/N]: ")
    if sunshine.lower() == 'y':
        print_info("Installing Sunshine...")
        if OS_ID == "fedora":
            sunshine_url = 'https://github.com/LizardByte/Sunshine/releases/download/v2026.131.3509/sunshine-fedora-40-amd64.rpm'
            sunshine_commands = (
                f"wget {sunshine_url} -O {user_home}/sunshine.rpm",
                f"sudo dnf install -y {user_home}/sunshine.rpm",
                f"rm {user_home}/sunshine.rpm",
                "systemctl --user enable sunshine")
        else:
            sunshine_url = 'https://github.com/LizardByte/Sunshine/releases/download/v2026.131.3509/sunshine-2026.131.3509-1-x86_64.pkg.tar.zst'
            sunshine_commands = (
                f"wget {sunshine_url} -O {user_home}/sunshine.pkg.tar.zst",
                f"sudo pacman -U {user_home}/sunshine.pkg.tar.zst --noconfirm",
                f"rm {user_home}/sunshine.pkg.tar.zst",
                "systemctl --user enable sunshine")
        for command in sunshine_commands:
            run_command(command)
   


    mod_choice = input(f"{YELLOW}[?]{NC} Choose main modifier key (a=ALT, s=SUPER) [a/S]: ").strip().lower()
    main_mod = "ALT" if mod_choice == 'a' else "SUPER"

    kb_choice = input(f"{YELLOW}[?]{NC} Choose keyboard layout (1=US English, 2=Spanish, 3=Latin American) [1/2/3]: ").strip()
    if kb_choice == '2': kb_layout = 'es'
    elif kb_choice == '3': kb_layout = 'latam'
    else: kb_layout = 'us'
    # --- 2. Deploy Dotfiles ---
    for folder in [".config", ".local", ".scripts"]:
        os.makedirs(os.path.join(user_home, folder), exist_ok=True)
        copy_folder(folder)
        copy_file(".bashrc")

    # Patch main modifier key

    # Patch keyboard layout
    i3_config = os.path.join(user_home, ".config", "i3", "config")
    if os.path.exists(i3_config):
        with open(i3_config, 'a') as f: 
            f.write(f"\n# Set keyboard layout\nexec_always --no-startup-id setxkbmap {kb_layout}\n")
    i3_config = os.path.join(user_home, ".config", "i3", "config")
    if os.path.exists(i3_config):
        with open(i3_config, 'r') as f: content = f.read()
        target_mod = "Mod1" if main_mod == "ALT" else "Mod4"
        content = content.replace("set $mod Mod1", f"set $mod {target_mod}").replace("set $mod Mod4", f"set $mod {target_mod}")
        with open(i3_config, 'w') as f: f.write(content)

    # --- 3. Environment Variables, Alias & Fonts ---
    # Values taken from APPS.md "Environment Variables" section
    
    install_fonts.main()

    # --- 4. Enable Services ---
    # User-level services from APPS.md
    user_services = ["hyprpolkitagent", "pipewire", "wireplumber"]
    for svc in user_services:
        try:
            run_command(f"systemctl --user enable {svc}.service")
        except: pass

    # System-level services
    system_services = ["sddm", "NetworkManager", "power-profiles-daemon", "tlp-pd"]
    for svc in system_services:
        try:
            run_command(f"sudo systemctl enable {svc}.service")
        except: pass

    # Mask notification daemons to avoid DBus auto-start conflicts
    try:
        run_command("systemctl --user mask dunst mako")
        run_command("mkdir -p ~/.local/share/dbus-1/services")
        run_command("ln -sf /dev/null ~/.local/share/dbus-1/services/org.knopwob.dunst.service")
        run_command("ln -sf /dev/null ~/.local/share/dbus-1/services/fr.emersion.mako.service")
    except: pass

    print_info("Adapting i3 config for runtime services (Polkit)...")
    i3_config_path = os.path.join(user_home, ".config", "i3", "config")
    if os.path.exists(i3_config_path):
        with open(i3_config_path, 'r') as f:
            file_content = f.read()
        
        if OS_ID == "fedora":
            if "lxpolkit" not in file_content:
                file_content += "\n# Polkit Agent (Fedora)\nexec --no-startup-id lxpolkit\n"
        else:
            if "hyprpolkitagent" not in file_content:
                file_content += "\n# Polkit Agent (Arch)\nexec --no-startup-id systemctl --user start hyprpolkitagent\n"
            
        with open(i3_config_path, 'w') as f:
            f.write(file_content)

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

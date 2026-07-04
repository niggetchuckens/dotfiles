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

    # YukiOS Splash Screen with yukivim
    print(f"\n{BLUE}╔════════════════════════════════════════════╗{NC}")
    print(f"{BLUE}║      YukiOS minimalist xfce-dots installer ║{NC}")
    print(f"{BLUE}╚════════════════════════════════════════════╝{NC}\n")

    if confirm is None:
        confirm = input(f"{YELLOW}[?]{NC} Proceed with installation for user '{current_user}'? [y/N]: ")
    if confirm.lower() != 'y': return
    
    sunshine_url = 'https://github.com/LizardByte/Sunshine/releases/download/v2026.131.3509/sunshine-2026.131.3509-1-x86_64.pkg.tar.zst'
        
    pkgs = (
                "xfce4 xfce4-goodies wget sddm wayland wl-clipboard xorg-xwayland "
                "rofi wofi kitty nautilus grim slurp cliphist "
                "brightnessctl pipewire wireplumber pipewire-pulse pavucontrol "
                "playerctl network-manager-applet power-profiles-daemon "
                "polkit gnome-keyring discord fastfetch neovim pacman-contrib "
                "ttf-commit-mono-nerd papirus-icon-theme bibata-cursor-theme oh-my-posh "
                "maim xclip"
            )
        
        
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
    # Stop Xfconfd to prevent XFCE session from overwriting XML files on log out
    print_info("Stopping xfconfd before deploying new configs...")
    try:
        subprocess.run("killall -q -9 xfconfd xfsettingsd xfwm4 xfce4-panel", shell=True)
    except Exception:
        pass

    for folder in [".config", ".local", ".scripts"]:
        os.makedirs(os.path.join(user_home, folder), exist_ok=True)
        copy_folder(folder)
        copy_file(".bashrc")

    # --- 3. Environment Variables, Alias & Fonts ---
    # Values taken from APPS.md "Environment Variables" section
    
    install_fonts.main()

    # --- 4. Enable Services ---
    # User-level services from APPS.md
    user_services = ["pipewire", "wireplumber"]
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

    # Mask notification daemons to avoid DBus auto-start conflicts
    try:
        run_command("systemctl --user mask dunst mako")
        run_command("mkdir -p ~/.local/share/dbus-1/services")
        run_command("ln -sf /dev/null ~/.local/share/dbus-1/services/org.knopwob.dunst.service")
        run_command("ln -sf /dev/null ~/.local/share/dbus-1/services/fr.emersion.mako.service")
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

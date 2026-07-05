import shutil
import subprocess
import os
import argparse
import sys
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
        run_command(f"cp -r {source}/* {destination}/", exit_on_fail=False)
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
        
def run_command(cmd, shell=True, exit_on_fail=True):
    try:
        subprocess.run(cmd, shell=shell, check=True)
    except subprocess.CalledProcessError:
        print_error(f"Command failed: {cmd}")
        if exit_on_fail:
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
    
    if OS_ID == "fedora":
        pkgs = (
            "hyprland wget sddm xdg-desktop-portal-hyprland wayland-devel wl-clipboard xorg-x11-server-Xwayland "
            "waybar rofi-wayland wofi lxpolkit wlogout dunst kitty nautilus grim slurp cliphist "
            "swaybg brightnessctl pipewire wireplumber pipewire-pulseaudio pavucontrol "
            "playerctl network-manager-applet "
            "polkit gnome-keyring seahorse fastfetch neovim papirus-icon-theme oh-my-posh flatpak"
        )
        flatpaks = "com.spotify.Client"
        commands = (
            "sudo dnf copr enable -y ashbuk/Hyprland-Fedora",
            f"sudo dnf install -y {pkgs}",
            "sudo flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo",
            f"sudo flatpak install -y flathub {flatpaks}",
            f"export PATH=\"$PATH:{user_home}/.local/bin\""
        )
    else:
        pkgs = (
            "hyprland wget sddm xdg-desktop-portal-hyprland wayland wl-clipboard xorg-xwayland "
            "waybar rofi wofi hyprpolkitagent wlogout dunst kitty nautilus grim slurp cliphist "
            "swaybg brightnessctl pipewire wireplumber pipewire-pulse pavucontrol "
            "playerctl network-manager-applet power-profiles-daemon "
            "polkit gnome-keyring seahorse fastfetch neovim pacman-contrib "
            "ttf-commit-mono-nerd papirus-icon-theme bibata-cursor-theme oh-my-posh"
        )
        commands = (   
            f"yay -Syu --needed --noconfirm {pkgs}",
            f"export PATH=\"$PATH:{user_home}/.local/bin\""
        )
        

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

    # --- Communication Apps ---
    discord_choice = input(f"{YELLOW}[?]{NC} Install a Discord Client? (d=Discord, v=Vesktop [Best for Wayland], n=None) [v/d/N]: ")
    if discord_choice.lower() == 'd':
        print_info("Installing standard Discord...")
        if OS_ID == "fedora":
            run_command("sudo flatpak install -y flathub com.discordapp.Discord")
        else:
            run_command("yay -S --needed --noconfirm discord")
    elif discord_choice.lower() == 'v':
        print_info("Installing Vesktop (Wayland-optimized Discord)...")
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
                "systemctl --user enable sunshine") # Enable sunshine service for github build bc the yay installation need lots of ram (my 16gb can't match that :c )
        for command in sunshine_commands:
            run_command(command)
   


    mod_choice = input(f"{YELLOW}[?]{NC} Choose main modifier key (a=ALT, s=SUPER) [a/S]: ").strip().lower()
    main_mod = "ALT" if mod_choice == 'a' else "SUPER"
    # --- 2. Deploy Dotfiles ---
    
    for folder in [".config", ".local", ".scripts"]:
        os.makedirs(os.path.join(user_home, folder), exist_ok=True)
        copy_folder(folder)
        copy_file(".bashrc")

    # Patch main modifier key
    keybind_conf = os.path.join(user_home, ".config", "hypr", "configs", "keybind.conf")
    if os.path.exists(keybind_conf):
        with open(keybind_conf, 'r') as f: content = f.read()
        content = content.replace("$mod = SUPER", f"$mod = {main_mod}").replace("$mod = ALT", f"$mod = {main_mod}")
        with open(keybind_conf, 'w') as f: f.write(content)
        
    if OS_ID == "fedora":
        print_info("Adapting autostart.conf for Fedora (Polkit & GTK Themes)...")
        autostart_path = os.path.join(user_home, ".config", "hypr", "configs", "autostart.conf")
        if os.path.exists(autostart_path):
            with open(autostart_path, 'r') as f:
                content = f.read()
            content = content.replace("systemctl --user start hyprpolkitagent", "lxpolkit")
            if "gsettings set org.gnome.desktop.interface" not in content:
                content += "\n# Configurar temas e iconos GTK (Especialmente util para Fedora)\n"
                content += "exec-once = gsettings set org.gnome.desktop.interface icon-theme 'Papirus-Dark'\n"
                content += "exec-once = gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita-dark'\n"
            with open(autostart_path, 'w') as f:
                f.write(content)

    install_fonts.main()

    # --- 3. Enable Services ---

    system_services = ["sddm", "NetworkManager", "power-profiles-daemon", "tailscaled", "avahi-daemon"]
    for svc in system_services:
        try:
            run_command(f"sudo systemctl enable {svc}.service", exit_on_fail=False)
        except: pass

    try:
        run_command("systemctl --user enable sunshine-boot.service")
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

    print_info("Setting bash as the default shell...")
    try:
        run_command(f"sudo usermod --shell /bin/bash {current_user}", exit_on_fail=False)
        print_success("Default shell set to bash.")
    except:
        print_error("Failed to set default shell to bash.")

    print(f"{GREEN}[SUCCESS]{NC} YukiOS setup complete for {current_user}! Please reboot.")

if __name__ == "__main__": 
    if os.geteuid() == 0:
        print_error("Please do not run this script as root (use sudo within the script instead)")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("-y", "--yes", action="store_true")
    args = parser.parse_args()
    main(confirm='y' if args.yes else None)

#!/usr/bin/env python3
"""
Font Installation Script
Reads FONTS.md and installs fonts using system package manager
"""

import subprocess
import sys
import re
from pathlib import Path

# Font name to package name mappings
FONT_PACKAGE_MAP = {
    'JetBrains Mono': 'ttf-jetbrains-mono ttf-jetbrains-mono-nerd',
    'JetBrainsMono Nerd Font': 'ttf-jetbrains-mono-nerd',
    'Hack': 'ttf-hack ttf-hack-nerd',
    'Iosevka': 'ttc-iosevka ttf-iosevka-nerd',
    'Noto Sans': 'noto-fonts',
    'Noto Serif': 'noto-fonts',
    'Noto Sans CJK': 'noto-fonts-cjk',
    'Noto Serif CJK': 'noto-fonts-cjk',
    'Noto Sans Mono': 'noto-fonts',
    'Noto Color Emoji': 'noto-fonts-emoji',
    'Roboto': 'ttf-roboto',
    'Source Han Sans': 'adobe-source-han-sans-jp-fonts',
    'Source Han Serif': 'adobe-source-han-serif-jp-fonts',
    'MesloLG': 'ttf-meslo-nerd',
    'Adwaita': 'cantarell-fonts',
    'feather': 'ttf-font-awesome',
}

FONT_PACKAGE_MAP_DNF = {
    'JetBrains Mono': 'jetbrains-mono-fonts',
    'JetBrainsMono Nerd Font': 'jetbrains-mono-fonts',
    'Hack': 'google-noto-sans-mono-fonts', 
    'Iosevka': 'iosevka-fonts',
    'Noto Sans': 'google-noto-sans-fonts',
    'Noto Serif': 'google-noto-serif-fonts',
    'Noto Sans CJK': 'google-noto-sans-cjk-fonts',
    'Noto Serif CJK': 'google-noto-serif-cjk-fonts',
    'Noto Sans Mono': 'google-noto-sans-mono-fonts',
    'Noto Color Emoji': 'google-noto-emoji-color-fonts',
    'Roboto': 'google-roboto-fonts',
    'Source Han Sans': 'adobe-source-han-sans-jp-fonts',
    'Source Han Serif': 'adobe-source-han-serif-jp-fonts',
    'Adwaita': 'abattis-cantarell-fonts',
    'feather': 'fontawesome-fonts',
}

def detect_package_manager():
    """Detect which package manager is available"""
    managers = {
        'pacman': ['/usr/bin/pacman', '/bin/pacman'],
        'apt': ['/usr/bin/apt', '/bin/apt'],
        'dnf': ['/usr/bin/dnf', '/bin/dnf'],
    }
    
    for manager, paths in managers.items():
        for path in paths:
            if Path(path).exists():
                return manager
    return None

def read_fonts_list(fonts_md_path):
    """Read and parse FONTS.md file"""
    fonts = set()
    with open(fonts_md_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line.startswith('- '):
                # Extract first font name (before comma if multiple variants)
                font_name = line[2:].split(',')[0].strip()
                fonts.add(font_name)
    return sorted(fonts)

def get_packages_to_install(fonts, pkg_manager):
    """Map font names to package names"""
    packages = set()
    map_to_use = FONT_PACKAGE_MAP_DNF if pkg_manager == 'dnf' else FONT_PACKAGE_MAP
    
    for font in fonts:
        # Check if font matches any key in the map
        for font_key, package_names in map_to_use.items():
            if font.startswith(font_key):
                packages.update(package_names.split())
                break
    
    return sorted(packages)

def install_packages_pacman(packages):
    """Install packages using pacman"""
    if not packages:
        print("No packages to install")
        return
    
    print(f"Installing {len(packages)} font packages with yay...")
    print(f"Packages: {', '.join(packages)}\n")
    
    cmd = ['yay', '-S', '--needed', '--noconfirm'] + packages
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Fonts installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Installation failed: {e}", file=sys.stderr)
        sys.exit(1)

def install_packages_apt(packages):
    """Install packages using apt (Ubuntu/Debian)"""
    if not packages:
        print("No packages to install")
        return
    
    print(f"Installing {len(packages)} font packages with apt...")
    print(f"Packages: {', '.join(packages)}\n")
    
    cmd = ['sudo', 'apt', 'install', '-y'] + packages
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Fonts installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Installation failed: {e}", file=sys.stderr)
        sys.exit(1)

def install_packages_dnf(packages):
    """Install packages using dnf"""
    if not packages:
        print("No packages to install")
        return
    
    print(f"Installing {len(packages)} font packages with dnf...")
    print(f"Packages: {', '.join(packages)}\n")
    
    cmd = ['sudo', 'dnf', 'install', '-y', '--skip-unavailable'] + packages
    try:
        subprocess.run(cmd, check=True)
        print("\n✓ Fonts from DNF installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Installation failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("\nInstalling Nerd Fonts manually for Fedora...")
    fonts_dir = Path.home() / ".local" / "share" / "fonts" / "NerdFonts"
    fonts_dir.mkdir(parents=True, exist_ok=True)
    
    zip_path = fonts_dir / "JetBrainsMono.zip"
    url = "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/JetBrainsMono.zip"
    
    try:
        subprocess.run(["wget", "-q", "--show-progress", url, "-O", str(zip_path)], check=True)
        subprocess.run(["unzip", "-q", "-o", str(zip_path), "-d", str(fonts_dir)], check=True)
        zip_path.unlink(missing_ok=True)
        print("✓ JetBrainsMono Nerd Font installed successfully!")
    except Exception as e:
        print(f"✗ Failed to install Nerd Fonts manually: {e}", file=sys.stderr)

def main():
    # Find FONTS.md
    script_dir = Path(__file__).parent
    fonts_md = script_dir / 'FONTS.md'
    
    if not fonts_md.exists():
        print(f"Error: FONTS.md not found at {fonts_md}", file=sys.stderr)
        sys.exit(1)
    
    print("Reading font list from FONTS.md...")
    fonts = read_fonts_list(fonts_md)
    print(f"Found {len(fonts)} unique fonts\n")
    
    # Detect package manager
    pkg_manager = detect_package_manager()
    if not pkg_manager:
        print("Error: No supported package manager found (pacman, apt, dnf)", file=sys.stderr)
        sys.exit(1)
    
    print(f"Detected package manager: {pkg_manager}\n")
    
    # Map fonts to packages
    packages = get_packages_to_install(fonts, pkg_manager)
    
    if not packages:
        print("Warning: No font packages could be mapped from FONTS.md")
        print("You may need to update the FONT_PACKAGE_MAP in the script")
        sys.exit(0)
    
    print(f"Mapped to {len(packages)} packages")
    
    # Prompt user
    response = input(f"\nInstall {len(packages)} font packages? [Y/n]: ").strip().lower()
    if response and response not in ['y', 'yes']:
        print("Installation cancelled")
        sys.exit(0)
    
    # Install based on package manager
    if pkg_manager == 'pacman':
        install_packages_pacman(packages)
    elif pkg_manager == 'apt':
        install_packages_apt(packages)
    elif pkg_manager == 'dnf':
        install_packages_dnf(packages)
    else:
        print(f"Package manager {pkg_manager} not yet supported in this script")
        sys.exit(1)
    
    print("\nRun 'fc-cache -fv' to rebuild font cache if needed")

if __name__ == '__main__':
    main()

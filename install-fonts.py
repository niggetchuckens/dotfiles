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
    'Iosevka': 'ttc-iosevka ttc-iosevka-nerd',
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
    'Grape Nuts': 'ttf-grape-nuts',
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

def get_packages_to_install(fonts):
    """Map font names to package names"""
    packages = set()
    
    for font in fonts:
        # Check if font matches any key in the map
        for font_key, package_names in FONT_PACKAGE_MAP.items():
            if font.startswith(font_key):
                packages.update(package_names.split())
                break
    
    return sorted(packages)

def install_packages_pacman(packages):
    """Install packages using pacman"""
    if not packages:
        print("No packages to install")
        return
    
    print(f"Installing {len(packages)} font packages with pacman...")
    print(f"Packages: {', '.join(packages)}\n")
    
    cmd = ['sudo', 'pacman', '-S', '--needed', '--noconfirm'] + packages
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
    packages = get_packages_to_install(fonts)
    
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
    else:
        print(f"Package manager {pkg_manager} not yet supported in this script")
        sys.exit(1)
    
    print("\nRun 'fc-cache -fv' to rebuild font cache if needed")

if __name__ == '__main__':
    main()

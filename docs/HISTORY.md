# System Modification History

## 📅 2026-06-12

### 🎮 Sunshine Service Configuration
- Created `~/.config/systemd/user/sunshine-boot.service`.
- Enabled user lingering for `hime`.
- Configured Sunshine for KMS capture to allow SDDM login streaming.
- **Apps Added**:
    - "Visual Studio Code" (`code`).
    - "Steam Big Picture" (`steam steam://open/bigpicture`).
- **Pairing**: Migrated pairing state from Docker configuration.

### 🌐 Tailscale
- Installed and configured Tailscale for secure networking.
- Verified status and connectivity.

### 🐧 Kernel & Repositories
- **CachyOS LTS Kernel**: Installed `linux-cachyos-lts` and `linux-cachyos-lts-headers` for improved stability and performance on Ryzen 4800H.
- **BlackArch Repo**: Added BlackArch repository for security tools and packages.
- **CachyOS Repo**: Added CachyOS repositories for optimized packages (v3/v4).

### 🛠️ Pacman Customization
- Enabled `Color` and `ILoveCandy` (Pacman progress bar) in `/etc/pacman.conf`.

### 🌍 Time & Timezone
- Set system timezone to `America/Santiago`.
- Enabled NTP synchronization via `systemd-timesyncd`.
- Synced system clock to hardware clock (RTC).

### 📂 Dotfiles Management
- Refactored `install.py` to fix errors and add automated system configuration.
- Synced latest `.bashrc`, `.config/hypr`, `.config/waybar`, and `.config/sunshine` changes.

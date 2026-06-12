# Gemini Session History - 2026-06-12

## Tasks Performed
1. **Sunshine Service Configuration**:
    - Created `~/.config/systemd/user/sunshine-boot.service`.
    - Enabled user lingering for `hime`.
    - Configured Sunshine for KMS capture to allow SDDM login streaming.
2. **Sunshine App Configuration**:
    - Added "Visual Studio Code" (`code`) to `apps.json`.
    - Added "Steam Big Picture" (`steam steam://open/bigpicture`) to `apps.json`.
    - Migrated pairing state from Docker configuration.
3. **Dotfiles Update**:
    - Refactored `~/dotfiles/install.py` to fix errors and add features.
    - Added Tailscale installation and setup.
    - Added AUR installation logic for `yay`.
    - Integrated `sunshine-boot.service` creation into the installer.

## System State Changes
- New user service: `sunshine-boot.service` (Enabled & Started).
- `~/.config/sunshine/apps.json` updated.
- `~/.config/sunshine/sunshine_state.json` migrated.
- `~/.gemini/GEMINI.md` and project memory updated.

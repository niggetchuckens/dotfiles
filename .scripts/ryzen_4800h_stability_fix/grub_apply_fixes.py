#!/usr/bin/env python3
"""
Ryzen 7 4800H GRUB Bootloader Optimization Script
Applies preventive fixes for Ryzen 7 4800H stability issues on Linux
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_cmd(cmd, use_sudo=False):
    """Execute shell command and return output"""
    if use_sudo:
        cmd = f"echo '**********' | sudo -S {cmd}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        print("⚠️  Command timed out")
        return "", 1


def backup_grub():
    """Create backup of GRUB configuration"""
    timestamp = datetime.now().strftime("%s")
    run_cmd(f"cp /etc/default/grub /etc/default/grub.backup.{timestamp}", use_sudo=True)
    print(f"✓ Backup created: /etc/default/grub.backup.{timestamp}")


def apply_ryzen_fixes():
    """Apply optimized Ryzen 7 4800H parameters to GRUB"""
    
    print("\n=== Ryzen 7 4800H GRUB Optimization ===\n")
    
    # Backup
    backup_grub()
    
    # Get current GRUB config
    current, _ = run_cmd("grep 'GRUB_CMDLINE_LINUX_DEFAULT=' /etc/default/grub | head -1")
    print(f"\nCurrent config:\n{current}\n")
    
    # New optimized parameters for Ryzen 7 4800H
    new_line = 'GRUB_CMDLINE_LINUX_DEFAULT="loglevel=3 nvme_core.default_ps_max_latency_us=0 quiet processor.max_cstate=1 rcu_nocbs=0-15 idle=nomwait pcie_aspm=off amd_iommu=on iommu=pt amd_pstate=disabled mitigations=off usb_storage.quirks=0x0951:0x1666:u modprobe.blacklist=ucsi_ccg modprobe.blacklist=btusb"'
    
    # Apply fix via sed (escape for shell)
    escaped_line = new_line.replace('"', '\\"').replace('$', '\\$')
    sed_cmd = f'sed -i "s|GRUB_CMDLINE_LINUX_DEFAULT=.*|{escaped_line}|" /etc/default/grub'
    
    _, ret = run_cmd(sed_cmd, use_sudo=True)
    if ret == 0:
        print("✓ GRUB parameters updated")
    else:
        print("✗ Failed to update GRUB parameters")
        return False
    
    # Regenerate GRUB config
    _, ret = run_cmd("grub-mkconfig -o /boot/grub/grub.cfg", use_sudo=True)
    if ret == 0:
        print("✓ GRUB configuration regenerated")
    else:
        print("✗ Failed to regenerate GRUB configuration")
        return False
    
    # Verify
    print("\n=== Verification ===\n")
    
    result, _ = run_cmd("grep 'processor.max_cstate\\|idle=\\|amd_pstate\\|mitigations' /boot/grub/grub.cfg | head -3")
    print("Active parameters in GRUB:")
    for line in result.split('\n')[:3]:
        if line:
            print(f"  {line.strip()}")
    
    # CPU info
    result, _ = run_cmd("lscpu | grep -i 'model name\\|cores\\|threads'")
    print("\nCPU Information:")
    for line in result.split('\n'):
        if line:
            print(f"  {line}")
    
    # Scaling driver
    result, _ = run_cmd("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver 2>/dev/null")
    print(f"\nCPU Frequency Driver: {result if result else 'N/A'}")
    
    return True


def main():
    if sys.platform != "linux":
        print("✗ This script only works on Linux")
        sys.exit(1)
    
    if apply_ryzen_fixes():
        print("\n✓ All fixes applied successfully!")
        print("\n⚠️  IMPORTANT: Reboot your system to activate these changes")
        print("   Command: sudo reboot")
    else:
        print("\n✗ Failed to apply fixes")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Ryzen 7 4800H Kernel Memory Management Tuning
Optimizes memory settings to prevent crashes and OOM events
"""

import subprocess
import sys
from pathlib import Path


def run_cmd(cmd, use_sudo=False):
    """Execute shell command and return output"""
    if use_sudo:
        cmd = f"echo '**********' | sudo -S {cmd}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", 1


def create_sysctl_config():
    """Create optimized sysctl configuration for Ryzen 7 4800H"""
    
    config = """# Ryzen 7 4800H Memory and VM Tuning
# Optimizes kernel memory management, swap behavior, and CPU scheduling

# ===== Memory Management =====
# Allow more memory before starting swap
vm.swappiness=10

# Keep more pages in cache (improves performance)
vm.page-cluster=3

# Increase max memory map count for modern applications
vm.max_map_count=262144

# ===== OOM Killer Settings =====
# Be less aggressive with OOM killing
vm.oom_dump_tasks=1
vm.panic_on_oom=0
vm.oom_kill_allocating_task=0

# ===== CPU Scheduling =====
# Reduce jitter and improve real-time behavior
kernel.sched_migration_cost_ns=5000000
kernel.sched_autogroup_enabled=1

# ===== Network Performance =====
net.core.rmem_max=134217728
net.core.wmem_max=134217728
net.ipv4.tcp_rmem=4096 87380 67108864
net.ipv4.tcp_wmem=4096 65536 67108864

# ===== File System =====
# Increase file descriptor limits
fs.file-max=2097152
fs.inotify.max_user_watches=524288

# ===== Power Management =====
# Improve power efficiency
kernel.sched_powersave_bias=0
"""
    
    return config


def apply_sysctl():
    """Apply sysctl configuration"""
    
    print("\n=== Applying Kernel Memory Tuning ===\n")
    
    config = create_sysctl_config()
    config_file = "/etc/sysctl.d/99-ryzen-4800h-tuning.conf"
    
    # Write config with sudo
    with open("/tmp/ryzen_sysctl.conf", "w") as f:
        f.write(config)
    
    _, ret = run_cmd(f"cp /tmp/ryzen_sysctl.conf {config_file}", use_sudo=True)
    if ret == 0:
        print(f"✓ Sysctl config written to {config_file}")
    else:
        print(f"✗ Failed to write sysctl config")
        return False
    
    # Apply settings
    _, ret = run_cmd("sysctl -p /etc/sysctl.d/99-ryzen-4800h-tuning.conf", use_sudo=True)
    if ret == 0:
        print("✓ Kernel parameters applied successfully")
    else:
        print("✗ Failed to apply kernel parameters")
        return False
    
    # Verify
    print("\nVerifying applied settings:")
    result, _ = run_cmd("sysctl vm.swappiness vm.page-cluster vm.max_map_count kernel.sched_migration_cost_ns", use_sudo=True)
    for line in result.split('\n'):
        if line:
            print(f"  {line}")
    
    return True


def main():
    if sys.platform != "linux":
        print("✗ This script only works on Linux")
        sys.exit(1)
    
    try:
        if apply_sysctl():
            print("\n✓ Memory tuning applied successfully!")
        else:
            print("\n✗ Failed to apply memory tuning")
            sys.exit(1)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

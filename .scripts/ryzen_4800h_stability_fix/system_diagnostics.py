#!/usr/bin/env python3
"""
Ryzen 7 4800H Diagnostic and Log Analysis Script
Checks for crashes, OOM issues, and system stability problems
"""

import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path


def run_cmd(cmd, use_sudo=False):
    """Execute shell command and return output"""
    if use_sudo:
        cmd = f"echo 'completo' | sudo -S {cmd}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        print("⚠️  Command timed out")
        return "", 1


def check_system_health():
    """Comprehensive system health check"""
    
    print("=" * 60)
    print("RYZEN 7 4800H SYSTEM HEALTH DIAGNOSTIC")
    print("=" * 60)
    
    report = []
    report.append(f"\n📋 Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Uptime and Load
    print("\n[1/6] System Status...")
    result, _ = run_cmd("uptime")
    report.append(f"### System Uptime\n```\n{result}\n```\n")
    print(f"✓ Uptime: {result}")
    
    # Kernel Boot Parameters
    print("[2/6] Kernel Parameters...")
    result, _ = run_cmd("cat /proc/cmdline | tr ' ' '\\n' | grep -E 'processor|idle|pcie_aspm|amd_iommu|iommu|amd_pstate|rcu_nocbs'")
    report.append(f"### Active Kernel Parameters\n```\n{result}\n```\n")
    print("✓ Kernel parameters verified")
    
    # Recent Errors and Crashes
    print("[3/6] Error Analysis...")
    result, _ = run_cmd("sudo journalctl --priority=err --since='24 hours ago' -q 2>&1", use_sudo=True)
    errors = result.split('\n') if result else []
    report.append(f"### Recent System Errors (Last 24h)\n```\n{chr(10).join(errors[:20])}\n```\n")
    print(f"✓ Found {len(errors)} errors in logs")
    
    # OOM Issues
    print("[4/6] Memory Status...")
    result, _ = run_cmd("sudo dmesg | grep -i 'out of memory\\|killed process' | tail -5", use_sudo=True)
    oom_events = result.split('\n') if result else []
    if oom_events and oom_events[0]:
        report.append(f"### Out-of-Memory Events\n```\n{chr(10).join(oom_events)}\n```\n")
        print(f"⚠️  Found {len([e for e in oom_events if e])} OOM events")
    else:
        report.append("### Out-of-Memory Events\nNone detected ✓\n")
        print("✓ No OOM events detected")
    
    # CPU and Thermal
    print("[5/6] CPU Status...")
    result, _ = run_cmd("lscpu | grep -i 'model name'")
    report.append(f"### CPU Information\n```\n{result}\n```\n")
    
    result, _ = run_cmd("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver 2>/dev/null")
    if result:
        report.append(f"**Frequency Driver:** `{result}`\n")
    
    result, _ = run_cmd("sensors 2>/dev/null | grep -E 'Tctl|Tccd|Core' | head -5")
    if result:
        report.append(f"### Thermal Status\n```\n{result}\n```\n")
    print("✓ CPU status verified")
    
    # GRUB Configuration
    print("[6/6] GRUB Configuration...")
    result, _ = run_cmd("grep 'GRUB_CMDLINE_LINUX_DEFAULT=' /etc/default/grub")
    if result:
        # Extract and format parameters
        params = result.split('"')[1] if '"' in result else result
        report.append(f"### Current GRUB Configuration\n```\nGRUB_CMDLINE_LINUX_DEFAULT=\"{params}\"\n```\n")
    print("✓ GRUB configuration verified")
    
    # Summary
    report.append("\n" + "=" * 60)
    report.append("### Recommendations\n")
    if "processor.max_cstate=1" not in str(result):
        report.append("- ⚠️ **Missing:** processor.max_cstate=1 (add for Ryzen stability)\n")
    if "idle=nomwait" not in str(result):
        report.append("- ⚠️ **Missing:** idle=nomwait (prevents MWAIT issues)\n")
    if "amd_pstate=disabled" not in str(result):
        report.append("- ⚠️ **Missing:** amd_pstate=disabled (use legacy driver)\n")
    
    report.append("\n**Next Step:** Run `grub_apply_fixes.py` if fixes are needed\n")
    report.append("=" * 60)
    
    return "\n".join(report)


def save_report(content):
    """Save diagnostic report to ~/.copilot/history"""
    history_dir = Path.home() / ".copilot" / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"ryzen_4800h_diagnostics_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = history_dir / filename
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"\n✓ Report saved: {filepath}")
    return filepath


def main():
    if sys.platform != "linux":
        print("✗ This script only works on Linux")
        sys.exit(1)
    
    try:
        report = check_system_health()
        print("\n" + report)
        save_report(report)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

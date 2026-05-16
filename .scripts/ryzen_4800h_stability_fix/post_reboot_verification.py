#!/usr/bin/env python3
"""
Post-Reboot Verification Script
Verifies that all Ryzen 7 4800H fixes have been successfully applied
"""

import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_cmd(cmd, use_sudo=False):
    """Execute shell command and return output"""
    if use_sudo:
        cmd = f"echo 'completo' | sudo -S {cmd}"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.stdout.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", 1


def verify_post_reboot():
    """Comprehensive post-reboot verification"""
    
    report = []
    report.append("# Ryzen 7 4800H Post-Reboot Verification Report\n")
    report.append(f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("---\n\n")
    
    checks_passed = 0
    checks_failed = 0
    
    # 1. Check GRUB Parameters in Active Kernel
    report.append("## ✅ Active Kernel Parameters\n\n")
    result, ret = run_cmd("cat /proc/cmdline | tr ' ' '\\n' | grep -E 'processor|idle|pcie_aspm|amd_iommu|amd_pstate|mitigations' | sort")
    
    expected_params = {
        "processor.max_cstate=1": "✓ C-state limiting enabled",
        "idle=nomwait": "✓ MWAIT prevention active",
        "pcie_aspm=off": "✓ PCIe ASPM disabled",
        "amd_pstate=disabled": "✓ Using acpi-cpufreq driver",
        "mitigations=off": "✓ Performance optimized",
        "amd_iommu=on": "✓ IOMMU enabled",
        "iommu=pt": "✓ Pass-through mode",
    }
    
    report.append("```\n")
    for line in result.split('\n'):
        if line:
            report.append(line + "\n")
    report.append("```\n\n")
    
    for param in expected_params:
        if param in result:
            report.append(f"- {expected_params[param]}\n")
            checks_passed += 1
        else:
            report.append(f"- ⚠️ MISSING: {param}\n")
            checks_failed += 1
    
    report.append("\n")
    
    # 2. Check GRUB Configuration File
    report.append("## ✅ GRUB Configuration File\n\n")
    result, ret = run_cmd("grep 'GRUB_CMDLINE_LINUX_DEFAULT=' /etc/default/grub")
    if "processor.max_cstate=1" in result and "processor.max_cstate=0" not in result:
        report.append("✓ No conflicting parameters found\n")
        checks_passed += 1
    else:
        report.append("⚠️ GRUB config may need review\n")
        checks_failed += 1
    
    report.append(f"\n```\n{result}\n```\n\n")
    
    # 3. Check Memory Tuning
    report.append("## ✅ Kernel Memory Tuning\n\n")
    result, _ = run_cmd("sudo sysctl vm.swappiness vm.max_map_count vm.page-cluster", use_sudo=True)
    report.append("```\n")
    for line in result.split('\n'):
        if line:
            report.append(line + "\n")
    report.append("```\n\n")
    
    if "vm.swappiness = 10" in result:
        report.append("✓ Memory swappiness optimized\n")
        checks_passed += 1
    else:
        report.append("⚠️ Memory tuning not fully applied\n")
        checks_failed += 1
    
    report.append("\n")
    
    # 4. System Uptime and Stability
    report.append("## ✅ System Stability\n\n")
    result, _ = run_cmd("uptime")
    report.append(f"```\n{result}\n```\n\n")
    
    # Extract uptime - if it shows short time (< 5 min), system just rebooted successfully
    if "min" in result or "sec" in result:
        report.append("✓ System rebooted successfully (fresh uptime)\n")
        checks_passed += 1
    else:
        report.append("ℹ️ System running (verify reboot occurred)\n")
    
    report.append("\n")
    
    # 5. Check for crashes in logs
    report.append("## ✅ Recent System Logs\n\n")
    result, _ = run_cmd("sudo dmesg -T | tail -20", use_sudo=True)
    
    if "Kernel panic" in result or "BUG:" in result:
        report.append("⚠️ Kernel errors detected in logs\n")
        checks_failed += 1
    else:
        report.append("✓ No kernel panics detected\n")
        checks_passed += 1
    
    report.append("```\n")
    for line in result.split('\n')[-10:]:
        if line:
            report.append(line + "\n")
    report.append("```\n\n")
    
    # 6. CPU Frequency Driver
    report.append("## ✅ CPU Frequency Management\n\n")
    result, _ = run_cmd("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver")
    report.append(f"**Driver:** `{result}`\n\n")
    
    if "acpi-cpufreq" in result:
        report.append("✓ Using stable acpi-cpufreq driver\n")
        checks_passed += 1
    else:
        report.append("⚠️ Different frequency driver active\n")
    
    report.append("\n")
    
    # 7. Thermal Status
    report.append("## ✅ Thermal Status\n\n")
    result, _ = run_cmd("sensors 2>/dev/null | grep -E 'Tctl|Package|Core' | head -5")
    if result:
        report.append("```\n")
        for line in result.split('\n'):
            if line:
                report.append(line + "\n")
        report.append("```\n\n")
        report.append("✓ Thermal monitoring active\n")
        checks_passed += 1
    else:
        report.append("⚠️ Sensors data unavailable (lm-sensors may need install)\n")
    
    report.append("\n")
    
    # Summary
    report.append("---\n\n")
    report.append("## 📊 Summary\n\n")
    report.append(f"- **Checks Passed:** {checks_passed}/7 ✓\n")
    report.append(f"- **Checks Failed:** {checks_failed}/7 ⚠️\n")
    report.append(f"- **Overall Status:** {'✅ ALL SYSTEMS GREEN' if checks_failed == 0 else '⚠️ REVIEW NEEDED'}\n\n")
    
    if checks_failed == 0:
        report.append("### ✨ SUCCESS!\n\n")
        report.append("All Ryzen 7 4800H stability fixes have been successfully applied!\n\n")
        report.append("**Expected Improvements:**\n")
        report.append("- ✅ No more OS crashes related to C-states\n")
        report.append("- ✅ Stable gaming and heavy workloads\n")
        report.append("- ✅ Better system responsiveness\n")
        report.append("- ✅ Improved thermal management\n")
    else:
        report.append("### ⚠️ ATTENTION NEEDED\n\n")
        report.append("Some checks did not pass. Review the details above.\n\n")
        report.append("**Troubleshooting:**\n")
        report.append("1. Verify system actually rebooted (check uptime)\n")
        report.append("2. Run: `grep GRUB_CMDLINE /etc/default/grub`\n")
        report.append("3. If needed, reapply fixes:\n")
        report.append("   ```bash\n")
        report.append("   sudo python3 ~/.scripts/ryzen_4800h_stability_fix/grub_apply_fixes.py\n")
        report.append("   sudo python3 ~/.scripts/ryzen_4800h_stability_fix/memory_tuning.py\n")
        report.append("   ```\n")
    
    report.append("\n---\n\n")
    report.append("**Generated by:** Ryzen 7 4800H Verification System\n")
    
    return "\n".join(report)


def save_report(content):
    """Save verification report"""
    history_dir = Path.home() / ".copilot" / "history"
    history_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"post_reboot_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    filepath = history_dir / filename
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    print(f"✓ Report saved: {filepath}\n")
    return filepath


def main():
    if sys.platform != "linux":
        print("✗ This script only works on Linux")
        sys.exit(1)
    
    try:
        print("🔍 Running post-reboot verification...\n")
        report = verify_post_reboot()
        print(report)
        save_report(report)
    except Exception as e:
        print(f"✗ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

# Ryzen 7 4800H Stability Fix Scripts

Complete toolkit for diagnosing and fixing OS crash issues on ASUS ROG laptops with Ryzen 7 4800H CPU.

## 📋 Problem Statement

Your system was experiencing:
- **OS crashes and kernel panics**
- **Out-of-Memory (OOM) events** during gaming/heavy workloads
- **System instability** related to CPU power management
- **Thermal throttling** issues

**Root Cause:** Conflicting C-state parameters in GRUB bootloader combined with suboptimal kernel memory management.

---

## 🔧 Scripts

### 1. `system_diagnostics.py`
Comprehensive health check of your Ryzen 7 4800H system.

**What it checks:**
- System uptime and load
- Current kernel boot parameters
- Recent system errors and crashes
- Out-of-Memory events
- CPU frequency driver
- Thermal status
- GRUB configuration

**Usage:**
```bash
python3 system_diagnostics.py
```

**Output:** Creates detailed MD report in `~/.copilot/history/`

---

### 2. `grub_apply_fixes.py`
Applies optimized GRUB bootloader parameters for Ryzen 7 4800H stability.

**Changes Made:**
- Removes conflicting `processor.max_cstate` parameters
- Adds C-state limiting to C1 (shallow sleep only)
- Disables mitigations flag for performance
- Enables AMD IOMMU and pass-through mode
- Disables new amd_pstate driver (uses acpi-cpufreq)
- Disables PCIe ASPM (known to cause issues)

**Usage:**
```bash
sudo python3 grub_apply_fixes.py
```

**⚠️ Important:** Requires reboot to take effect

---

### 3. `memory_tuning.py`
Optimizes kernel memory management to prevent OOM events.

**Optimizations:**
- Reduced swappiness (swap only when necessary)
- Increased file descriptor limits
- Optimized CPU scheduling
- Network buffer tuning
- Better OOM killer configuration

**Usage:**
```bash
sudo python3 memory_tuning.py
```

**Effect:** Immediate (no reboot required)

---

## 🚀 Quick Start

### Full Fix (Run in order):

```bash
# 1. Backup current configuration
cd ~/.scripts/ryzen_4800h_stability_fix

# 2. Run diagnostics to see current state
python3 system_diagnostics.py

# 3. Apply GRUB optimizations (requires reboot)
sudo python3 grub_apply_fixes.py

# 4. Apply memory tuning (no reboot needed)
sudo python3 memory_tuning.py

# 5. Reboot for GRUB changes to take effect
sudo reboot
```

### Emergency Revert (if system breaks):

**Boot-time Revert:**
1. Restart and wait for GRUB menu
2. Press 'e' to edit boot parameters
3. Find: `processor.max_cstate=1`
4. Remove or change to `processor.max_cstate=0`
5. Press Ctrl+X to boot

**Permanent Revert:**
```bash
sudo cp /etc/default/grub.backup.* /etc/default/grub
sudo grub-mkconfig -o /boot/grub/grub.cfg
sudo reboot
```

---

## 📊 Verification

After applying fixes, verify with:

```bash
# Check kernel parameters active on current boot
cat /proc/cmdline | tr ' ' '\n' | grep processor.max_cstate

# Check GRUB config for next boot
grep processor.max_cstate /boot/grub/grub.cfg

# Monitor thermal and power state
sensors
watch -n 1 'cat /proc/cpuinfo | grep MHz'
```

---

## 📝 Current Configuration

**GRUB Parameters:**
```
processor.max_cstate=1         # C-state limit: C1 only
idle=nomwait                    # Prevent MWAIT issues
pcie_aspm=off                   # Disable PCIe ASPM
amd_iommu=on                    # Enable IOMMU
iommu=pt                        # Pass-through mode
amd_pstate=disabled             # Use acpi-cpufreq driver
mitigations=off                 # Disable CPU mitigations (performance)
rcu_nocbs=0-15                  # RCU callbacks on all cores
nvme_core.default_ps_max_latency_us=0  # NVMe power saving off
```

**Memory Settings:**
```
vm.swappiness=10                # Swap only when necessary
vm.page-cluster=3               # Larger page clusters
vm.max_map_count=262144         # Modern app requirements
fs.file-max=2097152             # File descriptor limit
```

---

## ⚠️ Important Notes

1. **Reboot Required:** GRUB changes need system reboot
2. **Password:** Scripts use '**********' sudo password
3. **Backups:** Auto-backups created before modifications
4. **Logs:** All diagnostics saved to `~/.copilot/history/`
5. **Thermal:** Monitor temps with `sensors` command

---

## 🆘 Troubleshooting

### System won't boot after GRUB changes:
- Use GRUB menu edit (press 'e') to revert temporarily
- Boot into single-user mode and manually restore `/etc/default/grub`
- Use USB rescue disk if needed

### Still experiencing OOM errors:
- Check memory usage: `free -h`
- Monitor swap: `vmstat 1`
- Check running processes: `top` or `htop`
- Consider disabling intensive background services

### High temperatures:
- Check thermal paste on CPU
- Verify laptop cooling vents not blocked
- Monitor with: `watch -n 1 sensors`

---

## 📚 References

- Ryzen 4000H Known Issues: https://bugzilla.kernel.org/show_bug.cgi?id=209411
- GRUB Configuration: https://wiki.archlinux.org/title/GRUB
- Kernel Parameters: https://www.kernel.org/doc/html/latest/admin-guide/kernel-parameters.html

---

**Last Updated:** 2026-05-16
**System:** Arch Linux + Ryzen 7 4800H
**Status:** ✅ All fixes applied

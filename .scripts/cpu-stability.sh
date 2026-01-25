#!/bin/bash

# CPU Stability Fixer for Arch Linux
# Targets: Ryzen Idle Freezes & Intel 13/14th Gen Volts

echo "Checking CPU Vendor..."
VENDOR=$(grep -m 1 'vendor_id' /proc/cpuinfo | awk '{print $3}')

# 1. Determine the fix based on CPU
if [[ "$VENDOR" == "AuthenticAMD" ]]; then
    echo "Detected AMD CPU. Applying Ryzen C-State & IOMMU stability fixes..."
    PARAMS="processor.max_cstate=1 iommu=soft"
elif [[ "$VENDOR" == "GenuineIntel" ]]; then
    echo "Detected Intel CPU. Applying voltage and microcode stability fixes..."
    PARAMS="intel_pstate=passive idle=nomwait"
else
    echo "Unknown CPU vendor. Applying general stability parameters..."
    PARAMS="idle=nomwait"
fi

# 2. Update GRUB Configuration
echo "Updating /etc/default/grub..."
sudo sed -i "s/GRUB_CMDLINE_LINUX_DEFAULT=\"/GRUB_CMDLINE_LINUX_DEFAULT=\"$PARAMS /" /etc/default/grub

# 3. Regenerate GRUB config
echo "Regenerating GRUB config..."
sudo grub-mkconfig -o /boot/grub/grub.cfg

# 4. Ensure Microcode is installed (since you use yay)
echo "Ensuring CPU microcode is up to date..."
if [[ "$VENDOR" == "AuthenticAMD" ]]; then
    yay -S --needed amd-ucode
else
    yay -S --needed intel-ucode
fi

echo "Done! Please reboot for changes to take effect."

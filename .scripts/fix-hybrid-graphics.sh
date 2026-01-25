#!/bin/bash

# Updated Fix for Ryzen 4800H + RTX 2060 Hybrid Freezes
PARAMS="processor.max_cstate=1 amdgpu.runpm=0 nvidia.NVreg_EnableGpuFirmware=0 idle=nomwait"

echo "Applying Hybrid Graphics stability patches..."

# 1. Update GRUB
sudo sed -i "s/GRUB_CMDLINE_LINUX_DEFAULT=\"/GRUB_CMDLINE_LINUX_DEFAULT=\"$PARAMS /" /etc/default/grub

# 2. Add the NVIDIA "Preserve Video Memory" fix
# This prevents freezes when the GPU tries to sleep/wake
if [ ! -f /etc/modprobe.d/nvidia.conf ]; then
    echo "options nvidia NVreg_PreserveVideoMemoryAllocations=1" | sudo tee /etc/modprobe.d/nvidia.conf
fi

# 3. Regenerate Config
sudo grub-mkconfig -o /boot/grub/grub.cfg

echo "Patches applied. Please reboot."

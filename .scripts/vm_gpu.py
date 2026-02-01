import os
import sys
import subprocess

# PCI Addresses for your Nvidia Group 9
GPU_DEVICES = [
    "0000:01:00.0", # VGA compatible controller
    "0000:01:00.1", # Audio device
    "0000:01:00.2", # USB controller
    "0000:01:00.3"  # Serial bus controller
]

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {cmd}: {e.stderr.decode()}")

def bind_to_vfio():
    print("--- Isolating GPU for VM ---")
    
    for dev in GPU_DEVICES:
        # 1. Get Vendor and Device IDs (e.g., 10de 1f15)
        with open(f"/sys/bus/pci/devices/{dev}/vendor", 'r') as f:
            vendor = f.read().strip()
        with open(f"/sys/bus/pci/devices/{dev}/device", 'r') as f:
            device = f.read().strip()
        
        # 2. Unbind from current driver if one exists
        driver_path = f"/sys/bus/pci/devices/{dev}/driver"
        if os.path.exists(driver_path):
            print(f"Unbinding {dev} from {os.path.basename(os.readlink(driver_path))}")
            with open(f"{driver_path}/unbind", 'w') as f:
                f.write(dev)

        # 3. Bind to vfio-pci
        print(f"Binding {dev} to vfio-pci ({vendor} {device})")
        with open("/sys/bus/pci/drivers/vfio-pci/new_id", 'w') as f:
            f.write(f"{vendor} {device}")

    print("Done! GPU is now held by VFIO.")

def bind_to_host():
    print("--- Returning GPU to Arch Linux ---")
    
    for dev in GPU_DEVICES:
        driver_path = f"/sys/bus/pci/devices/{dev}/driver"
        if os.path.exists(driver_path):
            print(f"Unbinding {dev} from vfio-pci")
            with open(f"{driver_path}/unbind", 'w') as f:
                f.write(dev)
    
    # Trigger a rescan so the host's nvidia/snd drivers reclaim the hardware
    print("Rescanning PCI bus...")
    with open("/sys/bus/pci/rescan", 'w') as f:
        f.write("1")
    
    print("Done! GPU returned to host.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("This script must be run as root (sudo).")
        sys.exit(1)

    if len(sys.argv) != 2:
        print("Usage: sudo python gpu_switch.py [vm|host]")
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == "vm":
        bind_to_vfio()
    elif mode == "host":
        bind_to_host()
    else:
        print("Invalid mode. Use 'vm' or 'host'.")

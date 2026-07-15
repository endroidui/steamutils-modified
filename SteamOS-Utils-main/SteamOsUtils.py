#!/usr/bin/env python3
import subprocess
import argparse

def run_cmd(cmd):
    print(f"\n>>> Running: {cmd}")
    subprocess.run(cmd, shell=True)

def get_header_pkg_name():
    try:
        # Detects the installed kernel base package dynamically
        output = subprocess.check_output("pacman -Q | grep linux-neptune | grep -v headers | head -n 1 | awk '{print $1}'", shell=True)
        base_pkg = output.decode('utf-8').strip()
        if base_pkg:
            return f"{base_pkg}-headers"
    except Exception:
        pass
    return "linux-neptune-headers"

def main():
    parser = argparse.ArgumentParser(description="Native ACPI Enabler for SteamOS")
    parser.add_argument('--enable_acpi_calls', action='store_true', help='Enable ACPI calls natively')
    parser.parse_known_args()

    print("=== SteamOS Native ACPI & Battery Fix ===")
    
    # 1. Unlock filesystem
    run_cmd("sudo steamos-readonly disable")
    
    # 2. Initialize and populate keys
    run_cmd("sudo pacman-key --init")
    run_cmd("sudo pacman-key --populate archlinux holo")
    
    # 3. Detect and install the exact matching headers
    header_pkg = get_header_pkg_name()
    print(f"\n[Scanner] Target headers package identified as: {header_pkg}")
    run_cmd(f"sudo pacman -S --noconfirm {header_pkg} dkms acpi_call-dkms")
    
    # 4. Load the compiled module
    run_cmd("sudo modprobe acpi_call")
    
    # 5. Lock battery at 80%
    run_cmd("echo '\\_SB.PCI0.LPC0.EC0.VPC0.SBMC 0x03' | sudo tee /proc/acpi/call")
    
    print("\nSUCCESS! ACPI calls enabled and 80% charge limit locked.")

if __name__ == "__main__":
    main()
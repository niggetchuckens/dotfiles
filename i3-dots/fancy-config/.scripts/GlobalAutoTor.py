import os
import sys
import time

if os.geteuid() != 0:
    print("Please run this script with sudo (e.g. echo completo | sudo -S python3 GlobalAutoTor.py [start|stop])")
    sys.exit(1)

def setup_torrc():
    # Append TransPort and DNSPort if not there
    with open('/etc/tor/torrc', 'r') as f:
        content = f.read()
    
    if "TransPort 9040" not in content:
        print("[+] Configuring /etc/tor/torrc for Transparent Proxy...")
        with open('/etc/tor/torrc', 'a') as f:
            f.write("\n## Transparent Proxy Config\n")
            f.write("VirtualAddrNetworkIPv4 10.192.0.0/10\n")
            f.write("AutomapHostsOnResolve 1\n")
            f.write("TransPort 9040 IsolateClientAddr IsolateClientProtocol IsolateDestAddr IsolateDestPort\n")
            f.write("DNSPort 5353\n")
    print("[+] Cleaning up dangling user Tor instances...")
    os.system("killall tor 2>/dev/null")
    print("[+] Restarting system Tor service...")
    os.system("systemctl restart tor")
    time.sleep(3)

def start_iptables():
    print("[+] Setting up iptables to route ALL PC traffic through Tor...")
    os.system("iptables -F")
    os.system("iptables -t nat -F")
    
    # 1. Allow the Tor process to output traffic to the internet
    os.system("iptables -t nat -A OUTPUT -m owner --uid-owner tor -j RETURN")
    
    # 2. Ignore loopback traffic (don't route localhost through Tor)
    os.system("iptables -t nat -A OUTPUT -o lo -j RETURN")
    
    # 3. Redirect all DNS requests to Tor's DNS port
    os.system("iptables -t nat -A OUTPUT -p udp --dport 53 -j REDIRECT --to-ports 5353")
    
    # 4. Redirect all outgoing TCP traffic to Tor's TransPort
    os.system("iptables -t nat -A OUTPUT -p tcp --syn -j REDIRECT --to-ports 9040")

def stop_iptables():
    print("[+] Stopping Transparent Proxy. Restoring direct internet...")
    os.system("iptables -F")
    os.system("iptables -t nat -F")

if len(sys.argv) < 2:
    print("Usage: echo completo | sudo -S python3 GlobalAutoTor.py [start|stop]")
    sys.exit(1)

action = sys.argv[1].lower()

if action == "stop":
    stop_iptables()
    print("[!] Network is now direct.")
elif action == "start":
    setup_torrc()
    start_iptables()
    print("[!] SUCCESS: ALL your PC network traffic is now transparently routed through Tor!")
    print("[!] You do NOT need to configure proxies in your browser anymore.")
    print("[+] Rotating IP every 30 seconds. Press Ctrl+C to stop and restore network.")
    try:
        while True:
            time.sleep(30)
            print("\n[+] 30 seconds passed. Rotating Tor IP...")
            os.system("systemctl reload tor")
    except KeyboardInterrupt:
        print("\n[!] Caught Ctrl+C.")
        stop_iptables()
        print("[!] Exited. Network restored to normal.")
else:
    print("Invalid action. Use 'start' or 'stop'.")

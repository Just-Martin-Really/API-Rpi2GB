# WLAN-AP-Router – Automated Setup

Automates the complete configuration of a **Raspberry Pi 5** as a WLAN Access Point, Router, and Firewall.

## Project structure

```
wlan-ap-router/
│
├── main.py                     # Entry point – only file you run
│
├── config/                     # Settings and paths (Python constants)
│   ├── settings.py             # Network params: SSID, IPs, passwords
│   |── paths.py                # All file-system paths in one place
|   └── __init__.py
│
├── configs/                    # Plain-text config files deployed to the system
│   ├── dnsmasq.conf            # DHCP + DNS        → /etc/dnsmasq.conf
│   ├── nftables.conf           # Firewall rules    → /etc/nftables.conf
│   └── sysctl_append.conf      # Kernel params     → appended to /etc/sysctl.conf
│   
├── core/                       # Low-level, reusable primitives
│   ├── utils.py                # Shell runner, file I/O, console helpers
│   ├── installer.py            # Step 1: apt install
│   |── cleanup.py              # Step 2: remove conflicts
|   └── __init__.py
└── services/                   # One file per service / setup concern
    ├── access_point.py         # Step 3: nmcli WPA2 AP
    ├── dnsmasq.py              # Step 4: deploy + start dnsmasq
    ├── forwarding.py           # Step 5: IPv4 kernel forwarding
    ├── firewall.py             # Step 6: deploy + validate nftables
    ├── enable.py               # Step 7: systemctl enable + systemd overrides
    |── verify.py               # Step 8: PASS/FAIL health check
    └── __init__.py
```

**Rule:** to change network or firewall configuration, edit `configs/*.conf` or `config/settings.py` — never `main.py` or any service file.

---

## Usage

```bash
# Copy project to the Raspberry Pi
scp -r wlan-ap-router/ projekt_user@192.168.178.69:~/

# Run the setup
cd wlan-ap-router/
sudo python3 main.py
```

---

## What to edit and where

| What you want to change | File to edit |
|-------------------------|-------------|
| SSID, password, AP IP   | `config/settings.py` |
| DHCP range, DNS domain  | `configs/dnsmasq.conf` |
| Firewall rules          | `configs/nftables.conf` |
| Kernel parameters       | `configs/sysctl_append.conf` |
| Which packages to install | `core/installer.py` |
| Which services autostart  | `services/enable.py` |



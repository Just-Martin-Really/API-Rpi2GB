#  Remove services and profiles that would block the AP setup.
#  Stops systemd-resolved (occupies port 53, conflicts with dnsmasq)
#  Removes existing Wi-Fi client profiles on wlan0

from .utils import run, print_ok, print_info
from config.settings import WLAN_IFACE


def cleanup_conflicts() -> None:

    # Remove potential blockers:
    
    # Disable systemd-resolved if present
    run("systemctl stop systemd-resolved", check=False)
    run("systemctl disable systemd-resolved", check=False)
    print_info("systemd-resolved stopped/disabled (if it was running)")

    # Remove any old Wi-Fi client profiles on wlan0
    run(f"nmcli device disconnect {WLAN_IFACE}", check=False)
    output = run(f"nmcli -t -f NAME,DEVICE con show", check=False).stdout
    for line in output.splitlines():
        if WLAN_IFACE in line:
            conn_name = line.split(':')[0]
            run(f"nmcli connection delete '{conn_name}'", check=False)
            print_info(f"Deleted old connection: {conn_name}")
    print_ok("Conflicts cleared")
#!/usr/bin/env python3


#  To change network/AP settings:  edit config/settings.py
#  To change DHCP/DNS/firewall:    edit configs/*.conf


import os
import sys

from core     import install_packages, cleanup_conflicts
from services import (
    configure_access_point,
    configure_dnsmasq,
    enable_ip_forwarding,
    configure_firewall,
    enable_services,
    verify_configuration,
)


def main() -> None:
    if os.geteuid() != 0:
        print("ERROR: Run as root:  sudo python3 main.py")
        sys.exit(1)

    print("\n" + "=" * 60)
    print("  WLAN-AP-Router  –  Automated Setup")
    print("=" * 60)

    install_packages()
    cleanup_conflicts()
    configure_access_point()
    configure_dnsmasq()
    enable_ip_forwarding()
    configure_firewall()
    enable_services()
    verify_configuration()


if __name__ == "__main__":
    main()

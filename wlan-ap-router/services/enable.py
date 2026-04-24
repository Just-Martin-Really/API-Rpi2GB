# shared helper: Enable systemd services and manage drop-in overrides.
#  set_service_dependency() is used by dnsmasq.py and firewall.py too.

import os
from core.utils import run, print_ok
from config.paths import SYSTEMD_OVERRIDE_DIR

AUTOSTART_SERVICES = ["dnsmasq", "nftables", "NetworkManager"]


def enable_services() -> None:
    """Enable and restart all required services for autostart on boot."""
    for svc in AUTOSTART_SERVICES:
        run(f"systemctl enable {svc}")
        run(f"systemctl restart {svc}")
        print_ok(f"{svc} – enabled and running")


def set_service_dependency(service: str) -> None:
    """Create a systemd drop-in so the service starts after network-online.target."""
    override_dir  = SYSTEMD_OVERRIDE_DIR.format(service=service)
    override_file = os.path.join(override_dir, "override.conf")
    os.makedirs(override_dir, exist_ok=True)
    with open(override_file, "w") as f:
        f.write("[Unit]\nAfter=network-online.target\nWants=network-online.target\n")
    run("systemctl daemon-reload")
    print_ok(f"Systemd override set for {service}")

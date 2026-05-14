# Set and persist the WLAN regulatory domain.
#   Without an explicit phy country, the Broadcom firmware stays in
#   "country 99 (world)" and silently suppresses AP beacons on some channels
#   even when `iw reg get` shows the global country. A systemd oneshot
#   re-applies the country before NetworkManager starts on every boot.

from core.utils import run, print_ok
from config.settings import WIFI_COUNTRY

SYSTEMD_UNIT_PATH = "/etc/systemd/system/wlan-regdomain.service"


def configure_regdomain() -> None:
    """Apply the regulatory domain now and on every boot."""

    run(f"iw reg set {WIFI_COUNTRY}")

    unit = (
        "[Unit]\n"
        "Description=Apply WLAN regulatory domain\n"
        "After=network-pre.target\n"
        "Before=NetworkManager.service\n"
        "\n"
        "[Service]\n"
        "Type=oneshot\n"
        f"ExecStart=/usr/sbin/iw reg set {WIFI_COUNTRY}\n"
        "\n"
        "[Install]\n"
        "WantedBy=multi-user.target\n"
    )
    with open(SYSTEMD_UNIT_PATH, "w") as f:
        f.write(unit)

    run("systemctl daemon-reload")
    run("systemctl enable wlan-regdomain.service")
    print_ok(f"Regulatory domain set to {WIFI_COUNTRY} (persistent)")

# Disable WiFi power-save on wlan0.
#   The Broadcom (brcmfmac) driver suppresses or staggers AP beacons while
#   power-save is on, which makes the SSID invisible to clients even though
#   NetworkManager reports the connection as activated.

from core.utils import run, print_ok
from config.settings import WLAN_IFACE

NM_CONF_PATH = "/etc/NetworkManager/conf.d/wifi-powersave.conf"


def disable_wifi_powersave() -> None:
    """Persistently disable NetworkManager WiFi power-save and apply it now."""

    with open(NM_CONF_PATH, "w") as f:
        f.write("[connection]\nwifi.powersave = 2\n")  # 2 = disabled

    run("nmcli general reload conf", check=False)
    run(f"iw dev {WLAN_IFACE} set power_save off", check=False)
    print_ok("WiFi power-save disabled (persistent via NetworkManager)")

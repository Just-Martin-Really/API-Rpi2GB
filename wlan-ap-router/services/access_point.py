# Create and activate the WPA2 WLAN Access Point via NetworkManager
#  NetworkManager manages the mac80211 driver and hostapd internally,
#  so no separate hostapd.conf is required.

from core.utils import run, print_ok, print_info
from config.settings import WLAN_IFACE, AP_CONN_NAME, SSID, WIFI_PASSWORD, AP_IP


def configure_access_point() -> None:
    """Create (or update) the WPA2 AP profile and bring it up."""

    _ensure_profile_exists()
    _apply_settings()
    _activate()

    print_ok(f"Access Point '{SSID}' active on {WLAN_IFACE} ({AP_IP}/24)")


def _ensure_profile_exists() -> None:
    if run(f"nmcli connection show {AP_CONN_NAME}", check=False).returncode != 0:
        run(
            f"nmcli connection add type wifi ifname {WLAN_IFACE} "
            f"con-name {AP_CONN_NAME} mode ap ssid {SSID}"
        )
        print_ok(f"Profile '{AP_CONN_NAME}' created")
    else:
        print_info(f"Profile '{AP_CONN_NAME}' already exists – updating settings")


def _apply_settings() -> None:
    run(f'nmcli connection modify {AP_CONN_NAME} '
        f'wifi-sec.key-mgmt wpa-psk wifi-sec.psk "{WIFI_PASSWORD}"')
    run(f"nmcli connection modify {AP_CONN_NAME} "
        f"ipv4.method manual ipv4.addresses {AP_IP}/24")


def _activate() -> None:
    run(f"nmcli connection down {AP_CONN_NAME}", check=False)
    run(f"nmcli connection up   {AP_CONN_NAME}")

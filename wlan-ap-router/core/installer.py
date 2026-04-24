from .utils import run, print_ok

PACKAGES = ["hostapd", "dnsmasq"]


def install_packages() -> None:
    """Install hostapd and dnsmasq via apt-get."""
    run("apt-get update -qq")
    run(f"apt-get install -y {' '.join(PACKAGES)}")
    print_ok(f"Installed: {', '.join(PACKAGES)}")

#  Deploy dnsmasq config and start DHCP + DNS service
#  Config source: configs/dnsmasq.conf
#  Deploy target: /etc/dnsmasq.conf

from core.utils  import run, deploy_file, print_ok
from config.paths import DNSMASQ_SRC
from config.settings import DNSMASQ_DEST
from .enable import set_service_dependency


def configure_dnsmasq() -> None:
    """Deploy configs/dnsmasq.conf → /etc/dnsmasq.conf and start the service."""
    deploy_file(DNSMASQ_SRC, DNSMASQ_DEST)
    set_service_dependency("dnsmasq")
    run("systemctl enable dnsmasq")
    run("systemctl restart dnsmasq")
    print_ok("dnsmasq is running (DHCP + DNS)")

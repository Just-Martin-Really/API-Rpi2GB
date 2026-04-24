#  Deploy nftables config, validate syntax, and start the firewall
#  Config source: configs/nftables.conf
#  Deploy target: /etc/nftables.conf

import sys
from core.utils   import run, deploy_file, print_ok, print_warn
from config.paths    import NFTABLES_SRC
from config.settings import NFTABLES_DEST
from .enable import set_service_dependency


def configure_firewall() -> None:
    """Deploy configs/nftables.conf → /etc/nftables.conf and start the firewall."""

    deploy_file(NFTABLES_SRC, NFTABLES_DEST)
    _validate_syntax()
    set_service_dependency("nftables")
    run("systemctl enable nftables")
    run("systemctl restart nftables")
    print_ok("Firewall is active")


def _validate_syntax() -> None:
    if run(f"nft -c -f {NFTABLES_DEST}", check=False).returncode != 0:
        print_warn("nftables syntax error – aborting. Fix configs/nftables.conf and re-run.")
        sys.exit(1)
    print_ok("nftables syntax check passed")

#  Enable IPv4 packet forwarding in the kernel (persistent).
#  Config source: configs/sysctl_append.conf
#  Deploy target: /etc/sysctl.conf  (lines appended, not replaced)


from core.utils   import run, line_in_file, append_to_file, print_ok, print_info
from config.paths    import SYSCTL_APPEND_SRC
from config.settings import SYSCTL_CONF


def enable_ip_forwarding() -> None:
    """Append kernel parameters from configs/sysctl_append.conf to /etc/sysctl.conf."""

    added = _append_missing_lines()
    if not added:
        print_info("sysctl settings already present – skipping")

    run("sysctl -p")
    print_ok("IP forwarding is active")


def _append_missing_lines() -> bool:
    """Return True if at least one line was appended."""
    with open(SYSCTL_APPEND_SRC, encoding="utf-8") as f:
        lines = [l for l in f if l.strip() and not l.strip().startswith("#")]

    added = False
    for line in lines:
        if not line_in_file(SYSCTL_CONF, line):
            append_to_file(SYSCTL_CONF, line if line.endswith("\n") else line + "\n")
            print_ok(f"Appended: {line.strip()}")
            added = True
    return added

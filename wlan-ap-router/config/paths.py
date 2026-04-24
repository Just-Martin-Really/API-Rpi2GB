#  File-system paths for config sources and system destinations.
#  Keeps all path logic in one place.


import os

# Root of this project
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Config source files (edit these, not the Python code) 
CONFIGS_DIR       = os.path.join(PROJECT_ROOT, "configs")
DNSMASQ_SRC       = os.path.join(CONFIGS_DIR, "dnsmasq.conf")
NFTABLES_SRC      = os.path.join(CONFIGS_DIR, "nftables.conf")
SYSCTL_APPEND_SRC = os.path.join(CONFIGS_DIR, "sysctl_append.conf")

# Systemd override directory template 
SYSTEMD_OVERRIDE_DIR = "/etc/systemd/system/{service}.service.d"

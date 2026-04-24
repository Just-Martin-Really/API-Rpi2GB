#  Central configuration – change these values to match your environment.
#  All other modules import from here; nothing else is hard-coded.


#  Network interfaces 
WLAN_IFACE    = "wlan0"
ETH_IFACE     = "eth0"

# Access Point
AP_CONN_NAME  = "ap-wlan0"
SSID          = "Production"
WIFI_PASSWORD = "Production-01"   # Change before use, that is a very bad password
AP_IP         = "192.168.50.1"

# DHCP 
DHCP_START    = "192.168.50.20"
DHCP_END      = "192.168.50.150"
DHCP_MASK     = "255.255.255.0"
DHCP_LEASE    = "24h"

# DNS 
DNS_DOMAIN    = "lab.local"
UPSTREAM_DNS  = "8.8.8.8"

# System config file destinations (don't edit these) 
DNSMASQ_DEST  = "/etc/dnsmasq.conf"
NFTABLES_DEST = "/etc/nftables.conf"
SYSCTL_CONF   = "/etc/sysctl.conf"

#  Verify that every component is correctly configured and running

#  Checks:
#    1. IP forwarding active (= 1)
#    2. dnsmasq service running
#    3. nftables service running
#    4. nftables ruleset contains policy drop + masquerade
#    5. Default route present via eth0
#    6. wlan0 has the expected AP IP address


from core.utils import run
from config.settings import WLAN_IFACE, ETH_IFACE, AP_IP

def verify_configuration() -> None:
    """Quick check: IP forwarding, services, firewall rules, routing, wlan0 IP."""

    results = []

    out = run("sysctl net.ipv4.ip_forward").stdout.strip()
    results.append(("IP forwarding = 1", "1" in out, out))

    out = run("systemctl is-active dnsmasq", check=False).stdout.strip()
    results.append(("dnsmasq active", out == "active", out))

    out = run("systemctl is-active nftables", check=False).stdout.strip()
    results.append(("nftables active", out == "active", out))

    out = run("nft list ruleset", check=False).stdout
    ok = "policy drop" in out and "masquerade" in out
    results.append(("nftables: drop + masquerade", ok, "found" if ok else "missing"))

    out = run("ip route", check=False).stdout
    ok = f"dev {ETH_IFACE}" in out and "default" in out
    results.append(("Default route via eth0", ok, "present" if ok else "missing"))

    out = run(f"ip addr show {WLAN_IFACE}", check=False).stdout
    ok = AP_IP in out
    results.append((f"{WLAN_IFACE} has {AP_IP}", ok, out[:60]))

    print("\n" + "-" * 60)
    all_pass = True
    for label, passed, detail in results:
        status = "PASS" if passed else "FAIL"
        print(f"  {status}  {label}")
        if not passed:
            print(f"       -> {detail}")
            all_pass = False
    print("-" * 60)
    if all_pass:
        print("All checks passed – WLAN-AP-Router is ready!")
    else:
        print("Some checks failed. Please review the output above.")
    print("-" * 60)



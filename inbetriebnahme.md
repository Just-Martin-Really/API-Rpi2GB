# Meine Änderungen — WLAN-AP-Router (2GB Pi)

## Was ich gemacht habe und warum

Ich habe zwei Commits an der dnsmasq-Konfiguration gemacht, beide im Rahmen der Fehlersuche, warum der Pico `backend-server.lab.local` nicht auflösen konnte.

### Commit 1: expand-hosts

Ohne `expand-hosts` macht dnsmasq aus einem DHCP-Hostnamen keine FQDN. Das heißt: der 16GB Pi meldet sich per DHCP mit dem Hostnamen `backend-server`, aber dnsmasq würde `backend-server.lab.local` trotzdem nicht auflösen. `expand-hosts` zusammen mit `domain=lab.local` schließt diese Lücke.

### Commit 2: statischer address=-Eintrag

```
address=/backend-server.lab.local/192.168.50.92
```

Dieser Eintrag macht die DNS-Auflösung unabhängig vom DHCP-Lease. Auch wenn der 16GB Pi seinen Hostnamen nicht korrekt per DHCP announced, antwortet dnsmasq trotzdem mit der richtigen IP. Das ist robuster als expand-hosts allein.

### Warum hat das den Pico trotzdem nicht gerettet

Beide Fixes sind korrekt und sinnvoll für andere Clients im Netz — aber für den Pico sind sie irrelevant.

**Ursache:** `.local` ist per RFC 6762 für Multicast DNS (mDNS) reserviert. MicroPython verwendet lwIP als Netzwerkstack, und lwIP schickt alle Anfragen, deren Name auf `.local` endet, als mDNS-Multicast an `224.0.0.251:5353` — egal was als DNS-Server per DHCP konfiguriert ist. dnsmasq auf `192.168.50.1` bekommt diese Pakete nie zu sehen.

Die Lösung lag deshalb nicht in der dnsmasq-Konfiguration, sondern im Pico-Code: der Broker wird dort jetzt direkt per IP angesprochen (→ API-pico).

Für zukünftige Projekte: `.local` als interne Domain vermeiden, sobald Clients mit lwIP oder anderen mDNS-aware Stacks im Einsatz sind. `.internal` oder `.lan` wären unproblematisch.

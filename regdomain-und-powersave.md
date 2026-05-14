# Regulatory Domain und Power-Save: warum der Installer das setzt

## Symptom

Nach erfolgreicher Provisionierung meldete `nmcli dev status` `wlan0 → ap-wlan0 → connected` und `iw dev wlan0 info` zeigte `type AP` mit Kanal und Sendeleistung. Trotzdem war die SSID `Production` von keinem Client sichtbar.

## Ursachen (zwei, gleichzeitig)

### 1. Regulatory Domain auf der phy nicht gesetzt

`iw reg get` zeigte:

```
global
country DE: DFS-ETSI
...
phy#0
country 99: DFS-UNSET
```

Der globale Country-Code war auf DE, aber die WLAN-phy selbst stand auf `country 99` (world). Der Broadcom-Treiber (brcmfmac) wartet in diesem Zustand auf eine Regulatory-Bestätigung und sendet keine Beacons mit gültigen Limits aus. Ein Indikator war die unrealistische Sendeleistung `txpower 31 dBm` (DE-Limit für 2.4 GHz: 20 dBm), der Treiber hatte die Limits nicht angewandt.

### 2. Power-Save aktiv im AP-Modus

`iw dev wlan0 get power_save` meldete `on`. Der brcmfmac-Treiber unterdrückt im Power-Save-Modus Beacons auch im AP-Betrieb. NetworkManager meldet die Verbindung trotzdem als `activated`, obwohl die Funk-Sichtbarkeit fehlt. Dieses Verhalten ist projektübergreifend bekannt (siehe auch `docs/backend/handover.md` auf dem 16GB Pi).

## Fix

Zwei neue Installer-Schritte vor `configure_access_point`:

| Schritt | Modul | Wirkung |
|---|---|---|
| `configure_regdomain` | `services/regdomain.py` | Setzt `iw reg set DE` sofort und installiert eine systemd-Unit `wlan-regdomain.service`, die vor `NetworkManager.service` läuft und den Country-Code auf jedem Boot neu setzt. |
| `disable_wifi_powersave` | `services/powersave.py` | Schreibt `/etc/NetworkManager/conf.d/wifi-powersave.conf` mit `wifi.powersave = 2` und schaltet PS zur Laufzeit aus. |

Zusätzlich pinnt `services/access_point.py` jetzt Band und Kanal (`bg`, Kanal 6) auf dem NM-Profil. Ohne expliziten Kanal verzögert der Treiber das Beaconing manchmal um Sekunden bis Minuten.

## Konfiguration

Alles über `wlan-ap-router/config/settings.py`:

```python
WIFI_COUNTRY  = "DE"
AP_BAND       = "bg"
AP_CHANNEL    = 6
```

## Verifikation nach Boot

```bash
iw reg get | grep -A1 'phy#0'           # erwartet: country DE: DFS-ETSI
iw dev wlan0 get power_save              # erwartet: Power save: off
iw dev wlan0 info                        # erwartet: type AP, channel 6, txpower <= 20 dBm
nmcli -p con show ap-wlan0 | grep -E '802-11-wireless\.(band|channel)'
```

## Hinweis: `hostapd.service` masked ist korrekt

`systemctl status hostapd` zeigt `Loaded: masked, Active: inactive (dead)`. Das ist Absicht. Dieses Projekt nutzt den AP-Modus von NetworkManager direkt, der intern den nl80211-Pfad benutzt und kein eigenes hostapd-Binary fährt. Die maskierte Unit verhindert, dass eine versehentlich nachinstallierte hostapd-Instanz mit NetworkManager um `wlan0` konkurriert.

# Stückliste: ein fujinet-nfc-Leser

> **Stand der Preise: 2026-11-08.** Richtpreise in Euro inkl. MwSt., **ohne Versand**. Preise und Lieferbarkeit ändern sich, prüfe sie vor dem Kauf. Die Links sind einfache Produktlinks, **keine Affiliate-Links**. Die genannten Händler sind Beispiele, keine Empfehlung; jedes gleichwertige Teil aus jedem Shop tut es auch.

Diese Datei wird von `rechnungen/stueckliste.py` erzeugt, nicht von Hand ändern. Alle Mengen gelten für **einen** Leser. Mit \* ist das günstigste geprüfte Angebot markiert.

Zur Anleitung: [Anleitung (Deutsch)](anleitung-de.md), Kapitel 1.

## Wemos D1 mini (ESP8266)

Braucht 4 MB Flash (die Firmware ist für das Board `d1_mini` gebaut). Ein Board mit 1 MB, etwa der "D1 Mini V3.0", ist zu klein. Manche Boards haben eine Micro-USB-Buchse, neuere USB-C: Das Kabel in der nächsten Zeile passend dazu kaufen.

| Händler | Produkt (laut Seite) | Preis |
|---|---|---:|
| [Makershop](https://www.makershop.de/plattformen/d1-mini/esp8266-mini-board/) | D1 mini ESP8266 WLAN Board mit 4 MB Flash (Micro-USB, 4 MB Flash) | 3,80 € * |
| [funduino](https://funduino.com/en/products/wemos-d1-mini-nodemcu-lua-wifi-esp8266-entwicklungsboard) | WeMos D1 Mini ESP8266 - Entwicklungsboard mit WLAN, 3,3 V (Micro-USB, 4 MB Flash) | 5,95 € |
| [Roboter-Bausatz](https://www.roboter-bausatz.de/p/d1-mini-v4.0-esp8266-iot-board-arduino-kompatibel) | D1 Mini V4.0 ESP8266 IoT Board Arduino kompatibel (USB-C, 4 MB Flash) | 5,14 € |

## PN532-NFC-Modul mit I2C

Ein "PN532 NFC RFID Modul V3" mit zwei DIP-Schaltern (auf I2C stellen, siehe Anleitung). Die beigelegte Karte und der Transponder sind nicht als NTAG ausgewiesen: nicht damit rechnen.

| Händler | Produkt (laut Seite) | Preis |
|---|---|---:|
| [BerryBase](https://www.berrybase.de/pn532-nfc-und-rfid-modul-uart-i2c-spi-inkl.-karte-dongle) | PN532 NFC- und RFID-Modul, UART / I2C / SPI, inkl. Karte & Dongle (Seite: Protokoll über 2 DIP-Schalter) | 7,20 € |
| [funduino](https://funduino.com/products/pn532-nfc-rfid-v3-modul-fur-arduino-und-co) | PN532 NFC RFID Modul V3 - I2C, SPI, UART, 3,3-5,5 V (Seite: I2C, SPI oder UART über 2 DIP-Schalter) | 5,67 € * |

## Passiver Summer

Muss **passiv** sein: Der Leser spielt Melodien per PWM an Pin D7. Ein aktiver Summer piept nur. Das Modul KY-006 hat drei Pins: Signal (S) an D7, Minus an G, der mittlere bleibt frei.

| Händler | Produkt (laut Seite) | Preis |
|---|---|---:|
| [BerryBase](https://www.berrybase.de/ky-006-passives-buzzer-modul) | KY-006, Passives Buzzer Modul | 1,10 € * |
| [funduino](https://funduino.com/en/products/ky-006-passiver-buzzer-alarm-modul-fur-arduino) | KY-006 Buzzer Modul - passiv, 3-5 V, PWM-gesteuert | 1,30 € |

## Eine WS2812-LED

Eine einzelne adressierbare RGB-LED auf einer kleinen Platine, Daten-Eingang an Pin D8. Sie hat Lötpads, hier wird gelötet.

| Händler | Produkt (laut Seite) | Preis |
|---|---|---:|
| [Roboter-Bausatz](https://www.roboter-bausatz.de/p/1bit-rgb-led-ring-ws2812-5v-aehnl.-neopixel) | 1Bit RGB LED Ring WS2812 5V ähnl. Neopixel (1 Stück, Seite: ein WS2812b-RGB-Modul) | 0,75 € |

## NFC-Karten oder -Tags (NTAG213/215/216)

Typ NTAG213, NTAG215 oder NTAG216 (die Firmware schreibt NDEF-Text auf NTAG-Chips). Packungen mit 10 Stickern oder einzelne Sticker; zum Anfang genügt einer, später einer je Spiel.

| Händler | Produkt (laut Seite) | Preis |
|---|---|---:|
| [BerryBase](https://www.berrybase.de/rfid-nfc-tags-ntag215-25mm-selbstklebend-weiss-10-stueck) | RFID / NFC Tags, Ntag215, 25mm, selbstklebend, weiß, 10 Stück (10 Stück) | 4,40 € |
| [Roboter-Bausatz](https://www.roboter-bausatz.de/p/10-stueck-nfc-tags-sticker-13.56mhz-ntag215-rund-25mm-iso14443a-ntag-215) | 10 Stück NFC Tags Sticker 13.56MHz Ntag215 rund 25mm ISO14443A NTAG 215 (10 Stück) | 2,39 € |
| [funduino](https://funduinoshop.com/en/electronic-modules/wireless-iot/rfid-nfc/rfid-tag-sticker-25mm-nfc-tag213) | NFC Sticker TAG213 - ISO14443 A, Ø 25 mm, 180 Byte (1 Sticker, Chip-Typ laut Seite TAG213) | 1,39 € * |

## Dupont-Jumperkabel (Buchse-Buchse, etwa 20 cm)

Gebraucht werden acht kurze Kabel. Beide Angebote sind Bänder mit 40 Adern zum Auseinanderziehen; das BerryBase-Set enthält zusätzlich Stecker-Stecker- und Stecker-Buchse-Kabel.

| Händler | Produkt (laut Seite) | Preis |
|---|---|---:|
| [BerryBase](https://www.berrybase.de/40pin-jumper-dupont-kabel-set-je-1x-f-f-m-m-f-m-20cm) | 40pin Jumper / Dupont Kabel Set, je 1x F-F / M-M / F-M, 20cm (3 Bänder zu 40) | 4,90 € * |
| [Roboter-Bausatz](https://www.roboter-bausatz.de/p/10x-40-pin-dupont-kabel-buchse-buchse-20-cm) | 10x 40 Pin Kabel Buchse-Buchse 20 cm (10 Bänder zu 40) | 9,19 € |

## USB-Kabel mit Datenleitungen (zum Flashen des D1 mini und zur Stromversorgung)

Das Kabel muss Daten übertragen, nicht nur Strom; manche billigen Ladekabel können das nicht. Den Stecker passend zum D1 mini nehmen, Micro-USB oder USB-C. Die Summe rechnet das Kabel, das zum eingerechneten Board passt.

| Händler | Produkt (laut Seite) | Preis |
|---|---|---:|
| [BerryBase](https://www.berrybase.de/blackcotton-usb-a-usb-c-kabel-usb-2.0-schwarz-1-0m) | BlackCotton USB-A - USB-C Kabel, USB 2.0, schwarz, 1,0m (USB-A auf USB-C) | 1,60 € |
| [BerryBase](https://www.berrybase.de/blackcotton-micro-usb-2.0-kabel-schwarz-1-0m) | BlackCotton Micro USB 2.0 Kabel, schwarz, 1,0m (USB-A auf Micro-USB) | 1,90 € * |

## USB-Netzteil, 5 V, mindestens 1 A (besser 2 A)

Beim Beschreiben von Karten fließt mehr Strom als beim Lesen. Ein altes Handy-Ladegerät mit USB-A-Buchse genügt, vielleicht hast Du eins.

| Händler | Produkt (laut Seite) | Preis |
|---|---|---:|
| [Roboter-Bausatz](https://www.roboter-bausatz.de/p/usb-netzteil-ladegeraet-5v-2a-schwarz) | USB Ladegerät Netzteil 5V 2A (Schwarz) | 3,35 € * |
| [BerryBase](https://www.berrybase.de/dual-usb-netzteil-ladeadapter-2-4a-2x-usb-flache-bauform-weiss) | Dual USB Netzteil / Ladeadapter, 2,4A, 2x USB, flache Bauform, weiß | 12,90 € |

## Tasmota-Steckdose (optional)

Nur für den vollautomatischen Betrieb. Alle drei werden mit installiertem Tasmota verkauft (Delock: "mit der installierten Tasmota Firmware"; Nous und voelkner: Tasmota im Produktnamen), Du musst also nichts flashen. Die Höchstlast liegt weit über dem, was ein Atari-Netzteil zieht (wenige Watt): Nous A1T "empfohlene Leistung 2300 W / 10 A", Delock max. 16 A / 2500 W, voelkner 3450 W / 16 A. Die Delock-Seite nennt Stecker und Steckdose nach CEE 7/4 und 7/3 (EU); die Nous-Seiten nennen den Steckertyp nicht, schau auf die Produktfotos.

| Händler | Produkt (laut Seite) | Preis |
|---|---|---:|
| [BerryBase](https://www.berrybase.de/nous-a1t-smarte-steckdose-tasmota-firmware-wlan) | Nous A1T Smarte Steckdose, Tasmota Firmware, WLAN | 16,90 € * |
| [voelkner](https://www.voelkner.de/products/12146122/Nous-A1T-Smarte-Steckdose-Tasmota-Firmware-WLAN.html) | Nous A1T smarter Stecker Tasmota 1er 3450W/16A/Messung/Tasmota | 18,42 € |
| [BerryBase](https://www.berrybase.de/delock-wlan-steckdose-mit-integriertem-webinterface-energieueberwachung-tasmota-firmware) | Delock WLAN Steckdose mit integriertem Webinterface & Energieüberwachung, Tasmota Firmware | 23,50 € |

## Gehäuse (optional)

Der Leser nutzt dieselbe Verdrahtung wie das Projekt [tagreader](https://github.com/adonno/tagreader). Dessen druckbares Gehäuse liegt im Ordner [STLs](https://github.com/adonno/tagreader/tree/master/STLs); es passt für D1 mini und PN532. Ohne 3D-Drucker tut es auch eine kleine Kunststoff-Projektbox aus beliebiger Quelle: Die PN532-Antenne darf nur nicht von Metall abgeschirmt werden, die Karte wird durch wenige Millimeter Kunststoff gelesen. Das Gehäuse steht nicht in der Summe.

## Summe

Je Teil das günstigste geprüfte Angebot (jeweils eine Verkaufseinheit, wie angeboten), ohne Versand. Ein Sammelkauf in einem Shop spart oft Versand, das ist hier nicht eingerechnet.

| Teil | Händler | Preis |
|---|---|---:|
| Wemos D1 mini (ESP8266) | [Makershop](https://www.makershop.de/plattformen/d1-mini/esp8266-mini-board/) | 3,80 € |
| PN532-NFC-Modul mit I2C | [funduino](https://funduino.com/products/pn532-nfc-rfid-v3-modul-fur-arduino-und-co) | 5,67 € |
| Passiver Summer | [BerryBase](https://www.berrybase.de/ky-006-passives-buzzer-modul) | 1,10 € |
| Eine WS2812-LED | [Roboter-Bausatz](https://www.roboter-bausatz.de/p/1bit-rgb-led-ring-ws2812-5v-aehnl.-neopixel) | 0,75 € |
| NFC-Karten oder -Tags (NTAG213/215/216) | [funduino](https://funduinoshop.com/en/electronic-modules/wireless-iot/rfid-nfc/rfid-tag-sticker-25mm-nfc-tag213) | 1,39 € |
| Dupont-Jumperkabel (Buchse-Buchse, etwa 20 cm) | [BerryBase](https://www.berrybase.de/40pin-jumper-dupont-kabel-set-je-1x-f-f-m-m-f-m-20cm) | 4,90 € |
| USB-Kabel mit Datenleitungen (zum Flashen des D1 mini und zur Stromversorgung) | [BerryBase](https://www.berrybase.de/blackcotton-micro-usb-2.0-kabel-schwarz-1-0m) | 1,90 € |
| USB-Netzteil, 5 V, mindestens 1 A (besser 2 A) | [Roboter-Bausatz](https://www.roboter-bausatz.de/p/usb-netzteil-ladegeraet-5v-2a-schwarz) | 3,35 € |
| Tasmota-Steckdose (optional) | [BerryBase](https://www.berrybase.de/nous-a1t-smarte-steckdose-tasmota-firmware-wlan) | 16,90 € |

- **Ohne Steckdose: 22,86 €**
- **Mit Steckdose: 39,76 €**

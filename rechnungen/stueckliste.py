"""Stückliste für einen fujinet-nfc-Leser: Daten, Summen und die beiden Markdown-Dateien.

Aufruf (aus dem Projektstamm):

    python3 rechnungen/stueckliste.py            # erzeugt docs/parts-en.md und docs/stueckliste-de.md
    python3 rechnungen/stueckliste.py --pruefen  # ruft jede URL ab und meldet Status und Preis-Fund

Alle Preise stehen in Cent (ganze Zahlen), Quelle ist jeweils die verlinkte Händlerseite,
abgerufen am ABRUFDATUM. Die Summen entstehen nur hier im Code, nie von Hand.
Angebote, die am Abrufdatum nicht lieferbar waren oder deren Seite sich nicht abrufen ließ,
stehen nicht in der Liste.
"""

# ruff: noqa: E501  (lange Produkt-URLs und Texte sind Daten, Umbrüche würden sie verfälschen)
from __future__ import annotations

import sys
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

ABRUFDATUM = "2026-11-08"
TAGREADER_STL = "https://github.com/adonno/tagreader/tree/master/STLs"
TAGREADER_REPO = "https://github.com/adonno/tagreader"
WURZEL = Path(__file__).resolve().parent.parent
USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) Firefox/130.0"


@dataclass(frozen=True)
class Angebot:
    """Ein geprüftes Angebot: Händler, Seite, dort gesehener Produktname, Preis in Cent."""

    shop: str
    url: str
    produkt: str  # Produktname, wie er auf der Seite steht
    cent: int  # Preis der Verkaufseinheit inkl. MwSt., ohne Versand
    einheit_en: str = ""  # z. B. "pack of 10"
    einheit_de: str = ""
    hinweis_en: str = ""
    hinweis_de: str = ""
    stecker: str = ""  # "micro" oder "usbc": D1 mini und Kabel müssen zusammenpassen
    pruefung: str = "curl"  # "curl" oder "browser" (Seite für curl gesperrt, im Browser gelesen)


@dataclass(frozen=True)
class Teil:
    key: str
    name_en: str
    name_de: str
    anmerkung_en: str
    anmerkung_de: str
    angebote: tuple[Angebot, ...]
    optional: bool = False


# Jede Zeile unten: Produktname und Preis am 2026-11-08 von der jeweiligen Seite gelesen.
TEILE: tuple[Teil, ...] = (
    Teil(
        key="d1mini",
        name_en="Wemos D1 mini (ESP8266)",
        name_de="Wemos D1 mini (ESP8266)",
        anmerkung_en=(
            "Needs 4 MB flash (the firmware is built for the `d1_mini` board). A 1 MB board such as "
            'the "D1 Mini V3.0" is too small. Some boards have a Micro-USB socket, newer ones USB-C: '
            "buy the cable in the next row to match."
        ),
        anmerkung_de=(
            "Braucht 4 MB Flash (die Firmware ist für das Board `d1_mini` gebaut). Ein Board mit 1 MB, "
            'etwa der "D1 Mini V3.0", ist zu klein. Manche Boards haben eine Micro-USB-Buchse, neuere '
            "USB-C: Das Kabel in der nächsten Zeile passend dazu kaufen."
        ),
        angebote=(
            Angebot(
                "Makershop",
                "https://www.makershop.de/plattformen/d1-mini/esp8266-mini-board/",
                "D1 mini ESP8266 WLAN Board mit 4 MB Flash",
                380,
                hinweis_en="Micro-USB, 4 MB flash",
                hinweis_de="Micro-USB, 4 MB Flash",
                stecker="micro",
            ),
            Angebot(
                "funduino",
                "https://funduino.com/en/products/wemos-d1-mini-nodemcu-lua-wifi-esp8266-entwicklungsboard",
                "WeMos D1 Mini ESP8266 - Entwicklungsboard mit WLAN, 3,3 V",
                595,
                hinweis_en="Micro-USB, 4 MB flash",
                hinweis_de="Micro-USB, 4 MB Flash",
                stecker="micro",
                pruefung="browser",
            ),
            Angebot(
                "Roboter-Bausatz",
                "https://www.roboter-bausatz.de/p/d1-mini-v4.0-esp8266-iot-board-arduino-kompatibel",
                "D1 Mini V4.0 ESP8266 IoT Board Arduino kompatibel",
                514,
                hinweis_en="USB-C, 4 MB flash",
                hinweis_de="USB-C, 4 MB Flash",
                stecker="usbc",
            ),
        ),
    ),
    Teil(
        key="pn532",
        name_en="PN532 NFC module with I2C",
        name_de="PN532-NFC-Modul mit I2C",
        anmerkung_en=(
            'A "PN532 NFC RFID module V3" with two DIP switches (set them to I2C, see the guide). '
            "The sample card and tag that come with it are not stated to be NTAG: do not count on them."
        ),
        anmerkung_de=(
            'Ein "PN532 NFC RFID Modul V3" mit zwei DIP-Schaltern (auf I2C stellen, siehe '
            "Anleitung). Die beigelegte Karte und der Transponder sind nicht als NTAG ausgewiesen: nicht damit rechnen."
        ),
        angebote=(
            Angebot(
                "BerryBase",
                "https://www.berrybase.de/pn532-nfc-und-rfid-modul-uart-i2c-spi-inkl.-karte-dongle",
                "PN532 NFC- und RFID-Modul, UART / I2C / SPI, inkl. Karte & Dongle",
                720,
                hinweis_en="page: protocol set by 2 DIP switches",
                hinweis_de="Seite: Protokoll über 2 DIP-Schalter",
            ),
            Angebot(
                "funduino",
                "https://funduino.com/products/pn532-nfc-rfid-v3-modul-fur-arduino-und-co",
                "PN532 NFC RFID Modul V3 - I2C, SPI, UART, 3,3-5,5 V",
                567,
                hinweis_en="page: I2C, SPI or UART set by 2 DIP switches",
                hinweis_de="Seite: I2C, SPI oder UART über 2 DIP-Schalter",
                pruefung="browser",
            ),
        ),
    ),
    Teil(
        key="buzzer",
        name_en="Passive buzzer",
        name_de="Passiver Summer",
        anmerkung_en=(
            "Must be **passive**: the reader plays melodies by PWM on pin D7. An active buzzer only beeps. "
            "The KY-006 module has three pins: signal (S) to D7, minus to G, the middle pin stays free."
        ),
        anmerkung_de=(
            "Muss **passiv** sein: Der Leser spielt Melodien per PWM an Pin D7. Ein aktiver Summer piept "
            "nur. Das Modul KY-006 hat drei Pins: Signal (S) an D7, Minus an G, der mittlere bleibt frei."
        ),
        angebote=(
            Angebot(
                "BerryBase",
                "https://www.berrybase.de/ky-006-passives-buzzer-modul",
                "KY-006, Passives Buzzer Modul",
                110,
            ),
            Angebot(
                "funduino",
                "https://funduino.com/en/products/ky-006-passiver-buzzer-alarm-modul-fur-arduino",
                "KY-006 Buzzer Modul - passiv, 3-5 V, PWM-gesteuert",
                130,
                pruefung="browser",
            ),
        ),
    ),
    Teil(
        key="led",
        name_en="One WS2812 LED",
        name_de="Eine WS2812-LED",
        anmerkung_en=(
            "A single addressable RGB LED on a small board, data in to pin D8. It has solder pads, "
            "so this is a soldering job."
        ),
        anmerkung_de=(
            "Eine einzelne adressierbare RGB-LED auf einer kleinen Platine, Daten-Eingang an Pin D8. "
            "Sie hat Lötpads, hier wird gelötet."
        ),
        angebote=(
            Angebot(
                "Roboter-Bausatz",
                "https://www.roboter-bausatz.de/p/1bit-rgb-led-ring-ws2812-5v-aehnl.-neopixel",
                "1Bit RGB LED Ring WS2812 5V ähnl. Neopixel",
                75,
                einheit_en="1 piece",
                einheit_de="1 Stück",
                hinweis_en="page: one WS2812b RGB module",
                hinweis_de="Seite: ein WS2812b-RGB-Modul",
            ),
        ),
    ),
    Teil(
        key="tags",
        name_en="NFC cards or tags (NTAG213/215/216)",
        name_de="NFC-Karten oder -Tags (NTAG213/215/216)",
        anmerkung_en=(
            "Type NTAG213, NTAG215 or NTAG216 (the firmware writes NDEF text to NTAG chips). "
            "Packs of 10 stickers or single stickers; one is enough to start, one per game later."
        ),
        anmerkung_de=(
            "Typ NTAG213, NTAG215 oder NTAG216 (die Firmware schreibt NDEF-Text auf NTAG-Chips). "
            "Packungen mit 10 Stickern oder einzelne Sticker; zum Anfang genügt einer, später einer je Spiel."
        ),
        angebote=(
            Angebot(
                "BerryBase",
                "https://www.berrybase.de/rfid-nfc-tags-ntag215-25mm-selbstklebend-weiss-10-stueck",
                "RFID / NFC Tags, Ntag215, 25mm, selbstklebend, weiß, 10 Stück",
                440,
                einheit_en="pack of 10",
                einheit_de="10 Stück",
            ),
            Angebot(
                "Roboter-Bausatz",
                "https://www.roboter-bausatz.de/p/10-stueck-nfc-tags-sticker-13.56mhz-ntag215-rund-25mm-iso14443a-ntag-215",
                "10 Stück NFC Tags Sticker 13.56MHz Ntag215 rund 25mm ISO14443A NTAG 215",
                239,
                einheit_en="pack of 10",
                einheit_de="10 Stück",
            ),
            Angebot(
                "funduino",
                "https://funduinoshop.com/en/electronic-modules/wireless-iot/rfid-nfc/rfid-tag-sticker-25mm-nfc-tag213",
                "NFC Sticker TAG213 - ISO14443 A, Ø 25 mm, 180 Byte",
                139,
                einheit_en="1 sticker, chip type given as TAG213",
                einheit_de="1 Sticker, Chip-Typ laut Seite TAG213",
                pruefung="browser",
            ),
        ),
    ),
    Teil(
        key="wires",
        name_en="Dupont jumper wires (female-female, about 20 cm)",
        name_de="Dupont-Jumperkabel (Buchse-Buchse, etwa 20 cm)",
        anmerkung_en=(
            "Eight short wires are needed. Both offers are ribbons of 40 wires that you tear apart; "
            "the BerryBase set also has male-male and male-female wires."
        ),
        anmerkung_de=(
            "Gebraucht werden acht kurze Kabel. Beide Angebote sind Bänder mit 40 Adern zum "
            "Auseinanderziehen; das BerryBase-Set enthält zusätzlich Stecker-Stecker- und "
            "Stecker-Buchse-Kabel."
        ),
        angebote=(
            Angebot(
                "BerryBase",
                "https://www.berrybase.de/40pin-jumper-dupont-kabel-set-je-1x-f-f-m-m-f-m-20cm",
                "40pin Jumper / Dupont Kabel Set, je 1x F-F / M-M / F-M, 20cm",
                490,
                einheit_en="3 ribbons of 40",
                einheit_de="3 Bänder zu 40",
            ),
            Angebot(
                "Roboter-Bausatz",
                "https://www.roboter-bausatz.de/p/10x-40-pin-dupont-kabel-buchse-buchse-20-cm",
                "10x 40 Pin Kabel Buchse-Buchse 20 cm",
                919,
                einheit_en="10 ribbons of 40",
                einheit_de="10 Bänder zu 40",
            ),
        ),
    ),
    Teil(
        key="cable",
        name_en="USB cable, data-capable (to flash the D1 mini and power it)",
        name_de="USB-Kabel mit Datenleitungen (zum Flashen des D1 mini und zur Stromversorgung)",
        anmerkung_en=(
            "The cable must carry data, not just power; some cheap charging cables do not. "
            "Take the connector that fits your D1 mini, Micro-USB or USB-C. The sum uses the cable that matches the board it counts."
        ),
        anmerkung_de=(
            "Das Kabel muss Daten übertragen, nicht nur Strom; manche billigen Ladekabel können das nicht. "
            "Den Stecker passend zum D1 mini nehmen, Micro-USB oder USB-C. Die Summe rechnet das Kabel, das zum eingerechneten Board passt."
        ),
        angebote=(
            Angebot(
                "BerryBase",
                "https://www.berrybase.de/blackcotton-usb-a-usb-c-kabel-usb-2.0-schwarz-1-0m",
                "BlackCotton USB-A - USB-C Kabel, USB 2.0, schwarz, 1,0m",
                160,
                hinweis_en="USB-A to USB-C",
                hinweis_de="USB-A auf USB-C",
                stecker="usbc",
            ),
            Angebot(
                "BerryBase",
                "https://www.berrybase.de/blackcotton-micro-usb-2.0-kabel-schwarz-1-0m",
                "BlackCotton Micro USB 2.0 Kabel, schwarz, 1,0m",
                190,
                hinweis_en="USB-A to Micro-USB",
                hinweis_de="USB-A auf Micro-USB",
                stecker="micro",
            ),
        ),
    ),
    Teil(
        key="psu",
        name_en="USB power supply, 5 V, at least 1 A (2 A is better)",
        name_de="USB-Netzteil, 5 V, mindestens 1 A (besser 2 A)",
        anmerkung_en=(
            "Writing cards draws more current than reading. A spare phone charger with a USB-A "
            "socket does the job, so you may already own one."
        ),
        anmerkung_de=(
            "Beim Beschreiben von Karten fließt mehr Strom als beim Lesen. Ein altes Handy-Ladegerät mit "
            "USB-A-Buchse genügt, vielleicht hast Du eins."
        ),
        angebote=(
            Angebot(
                "Roboter-Bausatz",
                "https://www.roboter-bausatz.de/p/usb-netzteil-ladegeraet-5v-2a-schwarz",
                "USB Ladegerät Netzteil 5V 2A (Schwarz)",
                335,
            ),
            Angebot(
                "BerryBase",
                "https://www.berrybase.de/dual-usb-netzteil-ladeadapter-2-4a-2x-usb-flache-bauform-weiss",
                "Dual USB Netzteil / Ladeadapter, 2,4A, 2x USB, flache Bauform, weiß",
                1290,
            ),
        ),
    ),
    Teil(
        key="plug",
        name_en="Tasmota smart plug (optional)",
        name_de="Tasmota-Steckdose (optional)",
        anmerkung_en=(
            "Only for the fully automatic mode. All three are sold with Tasmota already installed "
            '(Delock: "with the installed Tasmota firmware"; Nous and voelkner: Tasmota in the '
            "product name), so you do not need to flash anything. Max. load is far above an Atari power supply "
            '(a few watts): Nous A1T "recommended 2300 W / 10 A", Delock max. 16 A / 2500 W, voelkner 3450 W / 16 A. '
            "The Delock page states an EU plug and socket (CEE 7/4 and 7/3); the Nous pages do not state the "
            "plug type, look at the product photos."
        ),
        anmerkung_de=(
            "Nur für den vollautomatischen Betrieb. Alle drei werden mit installiertem Tasmota verkauft "
            '(Delock: "mit der installierten Tasmota Firmware"; Nous und voelkner: Tasmota im '
            "Produktnamen), Du musst also nichts flashen. Die Höchstlast liegt weit über dem, was ein "
            'Atari-Netzteil zieht (wenige Watt): Nous A1T "empfohlene Leistung 2300 W / 10 A", Delock max. '
            "16 A / 2500 W, voelkner 3450 W / 16 A. Die Delock-Seite nennt Stecker und Steckdose nach "
            "CEE 7/4 und 7/3 (EU); die Nous-Seiten nennen den Steckertyp nicht, schau auf die Produktfotos."
        ),
        angebote=(
            Angebot(
                "BerryBase",
                "https://www.berrybase.de/nous-a1t-smarte-steckdose-tasmota-firmware-wlan",
                "Nous A1T Smarte Steckdose, Tasmota Firmware, WLAN",
                1690,
            ),
            Angebot(
                "voelkner",
                "https://www.voelkner.de/products/12146122/Nous-A1T-Smarte-Steckdose-Tasmota-Firmware-WLAN.html",
                "Nous A1T smarter Stecker Tasmota 1er 3450W/16A/Messung/Tasmota",
                1842,
            ),
            Angebot(
                "BerryBase",
                "https://www.berrybase.de/delock-wlan-steckdose-mit-integriertem-webinterface-energieueberwachung-tasmota-firmware",
                "Delock WLAN Steckdose mit integriertem Webinterface & Energieüberwachung, Tasmota Firmware",
                2350,
            ),
        ),
        optional=True,
    ),
)


@dataclass
class Summen:
    ohne_steckdose: int = 0
    mit_steckdose: int = 0
    wahl: dict[str, Angebot] = field(default_factory=dict)


def guenstigstes(teil: Teil) -> Angebot:
    return min(teil.angebote, key=lambda a: a.cent)


def rechne() -> Summen:
    """Je Teil das günstigste geprüfte Angebot; Steckdose nur in der zweiten Summe."""
    s = Summen()
    for teil in TEILE:
        if teil.key == "cable":
            # Das Kabel richtet sich nach dem Stecker des gewählten D1 mini.
            stecker = s.wahl["d1mini"].stecker
            wahl = min((a for a in teil.angebote if a.stecker == stecker), key=lambda a: a.cent)
        else:
            wahl = guenstigstes(teil)
        s.wahl[teil.key] = wahl
        s.mit_steckdose += wahl.cent
        if not teil.optional:
            s.ohne_steckdose += wahl.cent
    return s


def euro(cent: int, de: bool) -> str:
    text = f"{cent // 100}{',' if de else '.'}{cent % 100:02d}"
    return f"{text} €" if de else f"EUR {text}"


def tabelle(teil: Teil, de: bool) -> list[str]:
    kopf = (
        "| Händler | Produkt (laut Seite) | Preis |"
        if de
        else "| Shop | Product (as on the page) | Price |"
    )
    zeilen = [kopf, "|---|---|---:|"]
    bester = rechne().wahl[teil.key]
    for a in teil.angebote:
        einheit = a.einheit_de if de else a.einheit_en
        hinweis = a.hinweis_de if de else a.hinweis_en
        extra = ", ".join(x for x in (einheit, hinweis) if x)
        produkt = a.produkt + (f" ({extra})" if extra else "")
        preis = euro(a.cent, de) + (" *" if a is bester and len(teil.angebote) > 1 else "")
        zeilen.append(f"| [{a.shop}]({a.url}) | {produkt} | {preis} |")
    return zeilen


def erzeuge(de: bool) -> str:
    s = rechne()
    z: list[str] = []
    if de:
        z += [
            "# Stückliste: ein fujinet-nfc-Leser",
            "",
            f"> **Stand der Preise: {ABRUFDATUM}.** Richtpreise in Euro inkl. MwSt., **ohne Versand**. "
            "Preise und Lieferbarkeit ändern sich, prüfe sie vor dem Kauf. Die Links sind einfache "
            "Produktlinks, **keine Affiliate-Links**. Die genannten Händler sind Beispiele, keine "
            "Empfehlung; jedes gleichwertige Teil aus jedem Shop tut es auch.",
            "",
            "Diese Datei wird von `rechnungen/stueckliste.py` erzeugt, nicht von Hand ändern. "
            "Alle Mengen gelten für **einen** Leser. Mit \\* ist das günstigste geprüfte Angebot markiert.",
            "",
            "Zur Anleitung: [Anleitung (Deutsch)](anleitung-de.md), Kapitel 1.",
            "",
        ]
    else:
        z += [
            "# Parts list: one fujinet-nfc reader",
            "",
            f"> **Prices as of {ABRUFDATUM}.** Indicative prices in euro incl. VAT, **excluding shipping**. "
            "Prices and availability change, check them before you buy. The links are plain product links, "
            "**no affiliate links**. The shops named are examples, not an endorsement; an equivalent part "
            "from any shop works too.",
            "",
            "This file is generated by `rechnungen/stueckliste.py`, do not edit it by hand. "
            "All quantities are for **one** reader. \\* marks the cheapest verified offer.",
            "",
            "See also the [guide](guide-en.md), chapter 1.",
            "",
        ]
    for teil in TEILE:
        name = teil.name_de if de else teil.name_en
        z.append(f"## {name}")
        z.append("")
        z.append(teil.anmerkung_de if de else teil.anmerkung_en)
        z.append("")
        z += tabelle(teil, de)
        z.append("")
    z += gehaeuse(de)
    z += summen_abschnitt(s, de)
    return "\n".join(z).rstrip() + "\n"


def gehaeuse(de: bool) -> list[str]:
    if de:
        return [
            "## Gehäuse (optional)",
            "",
            f"Der Leser nutzt dieselbe Verdrahtung wie das Projekt [tagreader]({TAGREADER_REPO}). Dessen "
            f"druckbares Gehäuse liegt im Ordner [STLs]({TAGREADER_STL}); es passt für D1 mini und PN532. "
            "Ohne 3D-Drucker tut es auch eine kleine Kunststoff-Projektbox aus beliebiger Quelle: "
            "Die PN532-Antenne darf nur nicht von Metall abgeschirmt werden, die Karte wird durch "
            "wenige Millimeter Kunststoff gelesen. Das Gehäuse steht nicht in der Summe.",
            "",
        ]
    return [
        "## Case (optional)",
        "",
        f"The reader uses the same wiring as the [tagreader]({TAGREADER_REPO}) project. Its printable "
        f"case is in the [STLs]({TAGREADER_STL}) folder; it fits the D1 mini and the PN532. Without a 3D "
        "printer, a small plastic project box from any source works as well: just do not shield the "
        "PN532 antenna with metal, the card is read through a few millimetres of plastic. "
        "The case is not part of the sum.",
        "",
    ]


def summen_abschnitt(s: Summen, de: bool) -> list[str]:
    z = ["## Summe" if de else "## Total", ""]
    z.append(
        "Je Teil das günstigste geprüfte Angebot (jeweils eine Verkaufseinheit, wie angeboten), "
        "ohne Versand. Ein Sammelkauf in einem Shop spart oft Versand, das ist hier nicht eingerechnet."
        if de
        else "Per part the cheapest verified offer (one sales unit each, as offered), excluding shipping. "
        "Buying everything in one shop often saves shipping; that is not counted here."
    )
    z.append("")
    z.append("| Teil | Händler | Preis |" if de else "| Part | Shop | Price |")
    z.append("|---|---|---:|")
    for teil in TEILE:
        a = s.wahl[teil.key]
        name = teil.name_de if de else teil.name_en
        z.append(f"| {name} | [{a.shop}]({a.url}) | {euro(a.cent, de)} |")
    z.append("")
    z.append(
        f"- **Ohne Steckdose: {euro(s.ohne_steckdose, de)}**"
        if de
        else f"- **Without smart plug: {euro(s.ohne_steckdose, de)}**"
    )
    z.append(
        f"- **Mit Steckdose: {euro(s.mit_steckdose, de)}**"
        if de
        else f"- **With smart plug: {euro(s.mit_steckdose, de)}**"
    )
    z.append("")
    return z


def preis_formen(cent: int) -> list[str]:
    """Schreibweisen eines Preises, wie sie in Händlerseiten vorkommen (3,80 / 3.80 / 3.8)."""
    euro_teil, rest = divmod(cent, 100)
    formen = [f"{euro_teil},{rest:02d}", f"{euro_teil}.{rest:02d}"]
    if rest % 10 == 0:
        formen.append(f"{euro_teil}.{rest // 10}")
    return formen


def pruefen() -> int:
    """Ruft jede URL ab und meldet HTTP-Status und ob der Preis im Seitentext vorkommt.

    Seiten mit pruefung="browser" sind für curl teils gesperrt (HTTP 429); sie gelten als
    "im Browser geprüft", solange curl nicht das Gegenteil zeigt (Seite da, Preis fehlt).
    Die tagreader-Links waren beim Abruf nicht erreichbar und sind per README und Wayback belegt.
    """
    fehler = 0
    urls = [(a.url, a.cent, a.pruefung) for t in TEILE for a in t.angebote] + [
        (TAGREADER_STL, 0, "wayback"),
        (TAGREADER_REPO, 0, "wayback"),
    ]
    for url, cent, art in urls:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=40) as r:
                status = r.status
                text = r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            status, text = e.code, ""
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            status, text = 0, str(e)
        gefunden = bool(cent) and any(f in text for f in preis_formen(cent))
        if status == 200 and (gefunden or not cent):
            urteil = "Preis gefunden" if cent else "-"
        elif art == "browser" and status in (0, 403, 429):
            urteil = "im Browser geprüft"
        elif art == "wayback" and status == 0:
            urteil = "per Wayback/README geprüft"
        else:
            urteil = "PREIS NICHT GEFUNDEN" if status == 200 else "FEHLER"
            fehler += 1
        print(f"{status}  {urteil:28s}  {url}")
    print(f"{fehler} Auffälligkeiten von {len(urls)} Links")
    return 1 if fehler else 0


def main() -> int:
    if "--pruefen" in sys.argv[1:]:
        return pruefen()
    (WURZEL / "docs" / "parts-en.md").write_text(erzeuge(False), encoding="utf-8")
    (WURZEL / "docs" / "stueckliste-de.md").write_text(erzeuge(True), encoding="utf-8")
    s = rechne()
    print(f"ohne Steckdose: {euro(s.ohne_steckdose, True)}")
    print(f"mit Steckdose:  {euro(s.mit_steckdose, True)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

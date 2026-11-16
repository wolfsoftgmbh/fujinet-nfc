"""Prüft die Firmware-Konfiguration auf Veröffentlichungstauglichkeit (kein ESPHome-Lauf nötig)."""

import re
from pathlib import Path

FIRMWARE = Path(__file__).resolve().parent.parent / "firmware"
DATEIEN = [
    FIRMWARE / "fujinet-nfc.yaml",
    FIRMWARE / "fujinet-nfc-de.yaml",
    FIRMWARE / "secrets.example.yaml",
]


def test_keine_wlan_daten_in_yaml() -> None:
    for datei in DATEIEN:
        text = datei.read_text(encoding="utf-8")
        assert "wifi_ssid" not in text, datei.name
        assert "wifi_password" not in text, datei.name


def test_improv_serial_aktiv() -> None:
    text = (FIRMWARE / "fujinet-nfc.yaml").read_text(encoding="utf-8")
    assert re.search(r"^improv_serial:", text, re.MULTILINE)


def test_version_0_3_0() -> None:
    text = (FIRMWARE / "fujinet-nfc.yaml").read_text(encoding="utf-8")
    assert re.search(r'^\s+version:\s*"0\.3\.0"\s*$', text, re.MULTILINE)

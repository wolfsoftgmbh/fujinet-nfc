# Firmware: fujinet-nfc

ESPHome configuration for a Wemos D1 mini (ESP8266) with a PN532 (I2C), a passive buzzer (D7) and a
WS2812 LED (D8). Standalone: no `api:`, no Home Assistant. User guide:
[English](../docs/guide-en.md), [Deutsch](../docs/anleitung-de.md).

## Files

| File | Content |
|---|---|
| `fujinet-nfc.yaml` | ESPHome configuration (entities, scripts, PN532, web interface). All user-facing texts are `substitutions` at the top, in English. |
| `fujinet-nfc-de.yaml` | German build: overrides the text substitutions and includes `fujinet-nfc.yaml` as a package. |
| `fujinet_leser/karte.h` | Card logic as a plain C++17 header: parse card text (`tnfs://server/path` or path), build URLs, evaluate answers, host list lookup, smart plug URL |
| `fujinet_leser/test_karte.cpp` | Host tests for it |
| `components/pn532/` | Local copy of ESPHome's `pn532` component with three fixes for writing NTAG cards (see its README) |
| `secrets.example.yaml` | Template for `secrets.yaml` (git-ignored) |

Identifiers and comments inside the code are German; the interface is English or German.

## Build

Requirement: `uv` (ESPHome runs via `uvx`).

ESPHome is pinned to **2026.10.1** in the Makefile (`uvx --from esphome==2026.10.1`): the NDEF
handling relies on `NdefRecordText::get_payload()` returning the text without the status byte, and
the local `pn532` copy is taken from this version. A version change needs `make check` again, a
fresh copy of the component with the fixes re-applied, and a test with a real card.

```bash
cp firmware/secrets.example.yaml firmware/secrets.yaml   # empty ota_password = none; no WiFi in the file
make firmware                                            # both languages, about 2 minutes
```

Result in `firmware/build/`:

- `fujinet-nfc-en.factory.bin`, `fujinet-nfc-de.factory.bin` — first flash, e.g. with
  [ESPHome Web](https://web.esphome.io) or the flash page in `site/` (see below)
- `fujinet-nfc-en.ota.bin`, `fujinet-nfc-de.ota.bin` — updates via the reader's web interface

Release images are built with `make release`. It refuses to build unless `firmware/secrets.yaml`
equals `secrets.example.yaml` and has no `wifi_*` entries. The images contain no WiFi data at all: the reader
opens its setup network "FujiNet-NFC", or the WiFi is set over USB (Improv serial, e.g. ESPHome Web).
WiFi saved this way survives updates. These images have no OTA password.

Flash page: `make seite` copies the factory images into `site/firmware/` (git-ignored in the
development repository; the public repository carries them, and the Pages workflow publishes `site/`
as <https://wolfsoftgmbh.github.io/fujinet-nfc/>). To try it locally:
`cd site && python3 -m http.server 8000 --bind 127.0.0.1`. The installer only works over `https://` or
`localhost`.

Adding a language: copy `fujinet-nfc-de.yaml`, translate the substitutions, add the build to the
Makefile.

## Password for the web interface (self-built only)

The release images have no web password. When building yourself: enable the commented-out `auth:`
block under `web_server:` in `fujinet-nfc.yaml` and add `web_username` and `web_password` to
`secrets.yaml` (template keys in `secrets.example.yaml`). `ota_password` sets an OTA password.

## Checks

```bash
make check   # ruff, mypy, external resources, test-karte (g++), esphome config for both languages
make test    # pytest against the mock FujiNet
```

## Resources (ESPHome 2026.10.1, `make firmware`)

| Build | RAM | Flash |
|---|---|---|
| English | 50.5 % (41336 of 81920 bytes) | 49.8 % (520649 of 1044464 bytes) |
| German | 50.7 % (41500 of 81920 bytes) | 49.9 % (520813 of 1044464 bytes) |

Measured on the device (diagnostic build, 2026-11-02): about 36 KB free heap while running.

## NDEF notes

ESPHome parses text records itself: `NdefRecordText::get_payload()` returns only the text, without
status byte and language code. That is why the YAML does not call `text_aus_ndef_payload()` from
`karte.h`. Cards with UTF-16 text yield garbage and are rejected as "no image path".

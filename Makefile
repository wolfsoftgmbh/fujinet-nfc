.RECIPEPREFIX = >
.PHONY: help check lint types extern test test-karte esphome-config firmware release seite

# ESPHome ist fest gepinnt (NDEF-Payload-Verhalten, Config-Schema).
ESPHOME = uvx --from esphome==2026.10.1 esphome

# Verzeichnisse mit dem Python-Code (für mypy)
QUELLE = rechnungen werkzeuge

help:
> @echo "make check   Lint, Typen, externe Ressourcen — hostlokal, unter 10 s"
> @echo "make firmware Firmware bauen nach firmware/build/ (ESPHome-Compile, dauert)"
> @echo "make release Release-Images bauen; nur mit unveränderter secrets.yaml (Vorlage)"
> @echo "make seite   Factory-Images in die Flash-Seite site/ kopieren (nach make firmware)"
> @echo "make test    pytest (Mock-FujiNet u. a.)"

check: lint types extern test-karte esphome-config

lint:
> uvx ruff check .
> uvx ruff format --check .

types:
> uvx mypy $(QUELLE)

extern:
> ./scripts/keine-externen-ressourcen.sh
> ./scripts/keine-externen-ressourcen.sh site

test:
> uvx pytest -q

test-karte:
> g++ -std=c++17 -Wall -Wextra -Werror -o firmware/fujinet_leser/test_karte firmware/fujinet_leser/test_karte.cpp
> ./firmware/fujinet_leser/test_karte

esphome-config:
> test -f firmware/secrets.yaml || cp firmware/secrets.example.yaml firmware/secrets.yaml
> cd firmware && $(ESPHOME) config fujinet-nfc.yaml > /dev/null
> cd firmware && $(ESPHOME) config fujinet-nfc-de.yaml > /dev/null

firmware: esphome-config
> mkdir -p firmware/build
> cd firmware && $(ESPHOME) compile fujinet-nfc.yaml
> cp firmware/.esphome/build/fujinet-nfc/.pioenvs/fujinet-nfc/firmware.bin firmware/build/fujinet-nfc-en.ota.bin
> cp firmware/.esphome/build/fujinet-nfc/.pioenvs/fujinet-nfc/firmware.factory.bin firmware/build/fujinet-nfc-en.factory.bin
> cd firmware && $(ESPHOME) compile fujinet-nfc-de.yaml
> cp firmware/.esphome/build/fujinet-nfc/.pioenvs/fujinet-nfc/firmware.bin firmware/build/fujinet-nfc-de.ota.bin
> cp firmware/.esphome/build/fujinet-nfc/.pioenvs/fujinet-nfc/firmware.factory.bin firmware/build/fujinet-nfc-de.factory.bin

# Flash-Seite: Factory-Images neben die Seite legen (das Verzeichnis wird nur im Arbeitsstand mit den Images gefüllt).
seite:
> @for l in en de; do test -f firmware/build/fujinet-nfc-$$l.factory.bin || { echo "firmware/build/fujinet-nfc-$$l.factory.bin fehlt. Erst: make firmware (oder make release)"; exit 1; }; done
> mkdir -p site/firmware
> cp firmware/build/fujinet-nfc-en.factory.bin firmware/build/fujinet-nfc-de.factory.bin site/firmware/
> @echo "Seite fertig: site/ (z. B. cd site && python3 -m http.server 8000 --bind 127.0.0.1)"

# Release-Images gehen auf die Release-Seite: Sie dürfen nur die Platzhalter aus der Vorlage
# enthalten, nie echte WLAN-Daten aus einem Selbstbau.
release:
> ! grep -qE '^[[:space:]]*wifi_' firmware/secrets.yaml || { echo "firmware/secrets.yaml enthält WLAN-Einträge (wifi_*). Für Release-Images: cp firmware/secrets.example.yaml firmware/secrets.yaml"; exit 1; }
> cmp -s firmware/secrets.yaml firmware/secrets.example.yaml || { echo "firmware/secrets.yaml weicht von der Vorlage ab (echte WLAN-Daten?). Für Release-Images: cp firmware/secrets.example.yaml firmware/secrets.yaml"; exit 1; }
> $(MAKE) firmware


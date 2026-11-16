# pn532 — local copy from ESPHome 2026.10.1

Copy of `esphome/components/pn532` (ESPHome 2026.10.1, Copyright (c) 2019 ESPHome; C++ part GPL-3.0,
Python part MIT, see [LICENSE](LICENSE)) with three changes for fujinet-nfc, each marked with a
`fujinet-nfc:` comment:

1. `pn532.cpp`, `format_tag_`: NTAG/Ultralight (Tag Type 2) is **no longer** erased before writing. The
   NDEF message ends with the terminator TLV `0xFE`; readers ignore whatever follows it.
2. `pn532_mifare_ultralight.cpp`, `write_mifare_ultralight_page_`: up to five attempts per page. Before
   each retry the card is selected again (`waehle_karte_neu_` in `pn532.cpp`), because an NTAG rejects
   everything after an error until it is selected again.
3. `pn532.cpp`: `on_finished_write` only fires on success. Upstream also reports a failed write as
   finished, and the reader then played the success tune.

Reason (device test 2026-11-02, NTAG215 with 496 bytes): erasing writes 124 pages in one go and failed
every time on a single failed transfer, first at page 24, then at page 56. Without erasing, a path takes
about 8 pages, and a single dropout is retried.

When moving to a new ESPHome version, copy the component again and re-apply the three changes.

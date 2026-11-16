# Changelog

## v0.3.0

**Changing from v0.2.0 needs your WiFi entered once more:** the new version stores it differently, so
the update does not keep the old entry. Set it over USB (flash page) or over the hotspot "FujiNet-NFC".
From now on it survives updates.

- WiFi data is no longer part of the firmware image. The reader gets its WiFi over USB (Improv serial,
  for example from the flash page) or over its own network "FujiNet-NFC". WiFi saved this way survives
  updates. Release images no longer contain any WiFi data.
- The off time of the smart plug is adjustable, 1 to 30 seconds, default 2 seconds. The reader sends
  `Power Off`, waits itself and sends `Power On` (up to three tries) instead of a Tasmota `Backlog …
  Delay`: other requests reaching the plug no longer cut the off time short. New message if the plug
  does not switch back on.
- If the FujiNet does not answer a mount (for example while the Atari is loading from it), the reader
  tries once more after 2 seconds and only then reports the new message "FujiNet did not answer the
  mount". While the plug is off the reader accepts no further card.
- New flash page (ESP Web Tools, English and German) to install the reader from the browser. In its WiFi
  dialog a "Show password" tick box makes the typed password visible.
- Status light: between cards the LED breathes green (FujiNet and, if set, the plug are reachable) or
  red (one of them is missing). New "Status" display and "Status light" switch.
- Guides in English and German extended; parts list with shops, wiring diagram.
- Repository prepared for publication on GitHub (license GPL-3.0, README, contributing notes).

## v0.2.0

- English is the default language, German is a second firmware image.
- The reader writes cards itself: enter the path in the web interface, press "Write next card".
- Cards can name the server: `tnfs://server/path`. The server is looked up in the FujiNet's host list,
  or put into a free slot, never overwriting one.
- Stage 2: smart plug (Tasmota) restarts the Atari after each mount.
- Writing cards is robust: success is only reported on success, an invalid text ends the write
  mode, the card is selected again before a retry.
- `make release` refuses to build release images that contain real WiFi data.
- Detailed guides in English and German.

## v0.1.0

- First version: standalone ESPHome reader (D1 mini + PN532, no Home Assistant) that reads an image path
  from an NFC card and mounts it on a FujiNet over WiFi (`/mount`).
- Settings (FujiNet address, host slot, drive, sound) in the reader's web interface; WiFi setup over a
  hotspot with a setup page; sound and LED signal.

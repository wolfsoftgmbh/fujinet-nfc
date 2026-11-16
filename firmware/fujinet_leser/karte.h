// Reine Entscheidungslogik des FujiNet-Lesers. Nur Standardbibliothek, keine
// Exceptions, damit der Header auf dem ESP8266 (ESPHome) wie auf dem Host baut.
#pragma once

#include <cctype>
#include <cstdint>
#include <optional>
#include <string>

namespace fujinet_leser {

// Rohnutzlast eines NDEF-Text-Records: Statusbyte (Bits 0-5 = Laenge des
// Sprachcodes, Bit 7 = UTF-16), Sprachcode, Text.
inline std::optional<std::string> text_aus_ndef_payload(const std::string& payload) {
  if (payload.empty()) return std::nullopt;
  const unsigned char status = static_cast<unsigned char>(payload[0]);
  if (status & 0x80) return std::nullopt;
  const std::size_t sprach_laenge = status & 0x3F;
  if (1 + sprach_laenge > payload.size()) return std::nullopt;
  return payload.substr(1 + sprach_laenge);
}

inline std::string klein(std::string s) {
  for (char& c : s) c = static_cast<char>(std::tolower(static_cast<unsigned char>(c)));
  return s;
}

inline std::string ohne_rand(const std::string& text) {
  std::size_t anfang = 0;
  std::size_t ende = text.size();
  while (anfang < ende && std::isspace(static_cast<unsigned char>(text[anfang]))) ++anfang;
  while (ende > anfang && std::isspace(static_cast<unsigned char>(text[ende - 1]))) --ende;
  return text.substr(anfang, ende - anfang);
}

inline bool ist_image_pfad(const std::string& text) {
  static const char* const endungen[] = {".atr", ".atx", ".xex", ".cas"};
  if (text.size() < 4) return false;
  const std::string ende = klein(text.substr(text.size() - 4));
  for (const char* e : endungen) {
    if (ende == e) return true;
  }
  return false;
}

inline std::optional<std::string> normalisiere_pfad(const std::string& text) {
  std::string pfad = ohne_rand(text);
  if (pfad.empty()) return std::nullopt;
  if (pfad.find('&') != std::string::npos || pfad.find('=') != std::string::npos) return std::nullopt;
  if (!ist_image_pfad(pfad)) return std::nullopt;
  if (pfad[0] != '/') pfad.insert(pfad.begin(), '/');
  return pfad;
}

inline std::string url_kodieren(const std::string& s) {
  static const char hex[] = "0123456789ABCDEF";
  std::string aus;
  for (char ch : s) {
    const unsigned char c = static_cast<unsigned char>(ch);
    const bool frei = (c >= 'A' && c <= 'Z') || (c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') ||
                      c == '-' || c == '_' || c == '.' || c == '~' || c == '/';
    if (frei) {
      aus += ch;
    } else {
      aus += '%';
      aus += hex[c >> 4];
      aus += hex[c & 0x0F];
    }
  }
  return aus;
}

// Was auf der Karte steht: ein Pfad, optional mit Server davor (tnfs://server/pfad).
// host leer = Host-Slot aus den Einstellungen des Lesers.
// FujiNet speichert Servernamen in einem Feld von 32 Byte (MAX_HOSTNAME_LEN, v1.6.1),
// also hoechstens 31 Zeichen. Laengere Namen kaeme gekuerzt an und wuerde nie wiedergefunden.
constexpr std::size_t max_server_laenge = 31;

struct KartenZiel {
  std::string host;
  std::string pfad;
};

inline std::optional<KartenZiel> lies_karte(const std::string& roh) {
  const std::string text = ohne_rand(roh);
  static const std::string praefix = "tnfs://";
  if (klein(text.substr(0, praefix.size())) != praefix) {
    if (text.find("://") != std::string::npos) return std::nullopt;  // anderes Protokoll
    auto pfad = normalisiere_pfad(text);
    if (!pfad) return std::nullopt;
    return KartenZiel{"", *pfad};
  }
  const std::string rest = text.substr(praefix.size());
  const std::size_t schnitt = rest.find('/');
  if (schnitt == std::string::npos || schnitt == 0 || schnitt > max_server_laenge) return std::nullopt;
  const std::string host = rest.substr(0, schnitt);
  for (char ch : host) {
    const unsigned char c = static_cast<unsigned char>(ch);
    if (!(std::isalnum(c) || c == '.' || c == '-')) return std::nullopt;
  }
  auto pfad = normalisiere_pfad(rest.substr(schnitt));
  if (!pfad) return std::nullopt;
  return KartenZiel{host, *pfad};
}

inline std::string karten_text(const KartenZiel& ziel) {
  return ziel.host.empty() ? ziel.pfad : "tnfs://" + ziel.host + ziel.pfad;
}

// Zeilen 0..7 der Antwort von GET /hosts; fehlende Zeilen sind leer.
inline std::string host_zeile(const std::string& liste, int slot) {
  std::size_t anfang = 0;
  for (int i = 0; i < slot; ++i) {
    const std::size_t nl = liste.find('\n', anfang);
    if (nl == std::string::npos) return "";
    anfang = nl + 1;
  }
  std::size_t ende = liste.find('\n', anfang);
  if (ende == std::string::npos) ende = liste.size();
  return ohne_rand(liste.substr(anfang, ende - anfang));
}

inline int finde_host_slot(const std::string& liste, const std::string& host) {
  if (host.empty()) return -1;
  const std::string gesucht = klein(host);
  for (int slot = 0; slot < 8; ++slot) {
    if (klein(host_zeile(liste, slot)) == gesucht) return slot;
  }
  return -1;
}

// Nur eine vollstaendige Liste (8 Zeilen, wie sie FujiNet v1.6.1 liefert) wird nach freien
// Slots durchsucht. Eine kurze oder leere Antwort kommt nicht vom FujiNet; aus ihr einen
// "freien" Slot abzuleiten koennte einen belegten ueberschreiben.
inline int freier_host_slot(const std::string& liste) {
  std::size_t zeilenumbrueche = 0;
  for (char ch : liste) {
    if (ch == '\n') ++zeilenumbrueche;
  }
  if (zeilenumbrueche < 7) return -1;
  for (int slot = 0; slot < 8; ++slot) {
    if (host_zeile(liste, slot).empty()) return slot;
  }
  return -1;
}

inline std::optional<std::string> basis_url(const std::string& adresse) {
  std::string basis = ohne_rand(adresse);
  while (!basis.empty() && basis.back() == '/') basis.pop_back();
  if (basis.empty()) return std::nullopt;
  return klein(basis.substr(0, 7)) == "http://" ? basis : "http://" + basis;
}

inline std::optional<std::string> baue_mount_url(const std::string& adresse, int host_slot, int laufwerk,
                                                 const std::string& pfad) {
  if (host_slot < 0 || host_slot > 7 || laufwerk < 1 || laufwerk > 8) return std::nullopt;
  auto basis = basis_url(adresse);
  if (!basis) return std::nullopt;
  return *basis + "/mount?hostslot=" + std::to_string(host_slot) + "&deviceslot=" + std::to_string(laufwerk - 1) +
         "&mode=1&filename=" + url_kodieren(pfad);
}

inline std::optional<std::string> baue_hosts_url(const std::string& adresse) {
  auto basis = basis_url(adresse);
  if (!basis) return std::nullopt;
  return *basis + "/hosts";
}

// POST an diese URL traegt den Server in den Host-Slot ein (FujiNet v1.6.1, post_handler_hosts).
inline std::optional<std::string> baue_host_setzen_url(const std::string& adresse, int host_slot,
                                                       const std::string& host) {
  if (host_slot < 0 || host_slot > 7) return std::nullopt;
  auto basis = baue_hosts_url(adresse);
  if (!basis) return std::nullopt;
  return *basis + "?hostslot=" + std::to_string(host_slot) + "&hostname=" + url_kodieren(host);
}

// Stufe 2: Tasmota-Steckdose vor dem Atari-Netzteil. Der Leser schaltet aus, wartet selbst
// und schaltet ein. Ein "Backlog Power Off;Delay N;Power On" taugt nicht: Jeder Befehl, der
// waehrend des Delay bei der Steckdose eintrifft (Status eines zweiten Lesers, Home
// Assistant), beendet die Wartezeit sofort: CommandHandler setzt backlog_timer neu
// (tasmota/tasmota_support/support_command.ino, SetOption34). Gemessen am 2026-11-13,
// Tasmota 14.1: 1,9 s statt 10 s. Leere Adresse = keine Steckdose.
inline std::optional<std::string> baue_steckdose_aus_url(const std::string& adresse) {
  auto basis = basis_url(ohne_rand(adresse));
  if (!basis) return std::nullopt;
  return *basis + "/cm?cmnd=Power%20Off";
}

inline std::optional<std::string> baue_steckdose_an_url(const std::string& adresse) {
  auto basis = basis_url(ohne_rand(adresse));
  if (!basis) return std::nullopt;
  return *basis + "/cm?cmnd=Power%20On";
}

// Ausschaltzeit in Sekunden auf 1..30 begrenzen.
inline int klemme_aus_sekunden(int s) { return s < 1 ? 1 : (s > 30 ? 30 : s); }

// Statusabfrage der Steckdose fuer das Ruhelicht: Tasmota "Status" schaltet nichts.
inline std::optional<std::string> baue_steckdosen_status_url(const std::string& adresse) {
  auto basis = basis_url(ohne_rand(adresse));
  if (!basis) return std::nullopt;
  return *basis + "/cm?cmnd=Status";
}

enum class MountErgebnis { erfolg, fehler_fujinet, verweigert, nicht_erreichbar, unbekannt };

inline MountErgebnis werte_antwort_aus(int status, const std::string& body) {
  if (status <= 0) return MountErgebnis::nicht_erreichbar;
  if (status == 303 || status == 401) return MountErgebnis::verweigert;
  if (status == 200) {
    if (body.find("Operation successful") != std::string::npos) return MountErgebnis::erfolg;
    if (body.find("<title>Error") != std::string::npos) return MountErgebnis::fehler_fujinet;
  }
  return MountErgebnis::unbekannt;
}

class Entpreller {
 public:
  explicit Entpreller(uint32_t sperre_ms) : sperre_ms_(sperre_ms) {}

  // true, wenn die UID neu ist oder die Sperrzeit abgelaufen ist; nur dann
  // wird UID und Zeit gemerkt.
  bool neu(const std::string& uid, uint32_t jetzt_ms) {
    if (hat_letzte_ && uid == letzte_uid_ && static_cast<uint32_t>(jetzt_ms - letzte_ms_) < sperre_ms_) {
      return false;
    }
    hat_letzte_ = true;
    letzte_uid_ = uid;
    letzte_ms_ = jetzt_ms;
    return true;
  }

 private:
  uint32_t sperre_ms_;
  bool hat_letzte_ = false;
  std::string letzte_uid_;
  uint32_t letzte_ms_ = 0;
};

}  // namespace fujinet_leser

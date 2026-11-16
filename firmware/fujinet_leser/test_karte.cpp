// Host-Tests fuer karte.h (g++ -std=c++17), kein Framework.
#include <cstdio>
#include <string>

#include "karte.h"

using namespace fujinet_leser;

static int geprueft = 0;
static int gescheitert = 0;

#define PRUEFE(a)                                                        \
  do {                                                                   \
    ++geprueft;                                                          \
    if (!(a)) {                                                          \
      ++gescheitert;                                                     \
      std::printf("FEHLER %s:%d: %s\n", __FILE__, __LINE__, #a);         \
    }                                                                    \
  } while (0)

int main() {
  // NDEF
  PRUEFE(text_aus_ndef_payload(std::string("\x02" "en" "/spiele/mule.atr", 19)) == "/spiele/mule.atr");
  PRUEFE(!text_aus_ndef_payload(""));
  PRUEFE(!text_aus_ndef_payload(std::string("\x85" "en-US", 6)));  // UTF-16-Bit
  PRUEFE(!text_aus_ndef_payload(std::string("\x05" "en", 3)));     // Sprachcode laenger als Nutzlast
  // Pfadregel
  PRUEFE(ist_image_pfad("/a/B.ATR") && ist_image_pfad("x.xex") && ist_image_pfad("x.atx") && ist_image_pfad("x.cas"));
  PRUEFE(!ist_image_pfad("/media/fat/games/ATARI800/x.mgl"));  // kein_pfad_mgl
  PRUEFE(!ist_image_pfad("**launch.random:snes"));            // kein_pfad_zapscript
  PRUEFE(!ist_image_pfad("") && !ist_image_pfad(".atrx"));
  PRUEFE(normalisiere_pfad("  spiele/mule.atr \n") == "/spiele/mule.atr");
  PRUEFE(!normalisiere_pfad("/a&b.atr") && !normalisiere_pfad("/a=b.atr") && !normalisiere_pfad("/x.car"));
  // Kodierung
  PRUEFE(url_kodieren("/Spiele/Boulder Dash (1984).atr") == "/Spiele/Boulder%20Dash%20%281984%29.atr");  // kodiert_sonderzeichen
  PRUEFE(url_kodieren("/ä.atr") == "/%C3%A4.atr");
  PRUEFE(url_kodieren("A-z_0.9~/") == "A-z_0.9~/");
  // URL
  PRUEFE(baue_mount_url("192.168.0.50", 0, 1, "/s/m.atr") == "http://192.168.0.50/mount?hostslot=0&deviceslot=0&mode=1&filename=/s/m.atr");
  PRUEFE(baue_mount_url("http://fujinet.local:8095", 2, 3, "/a b.xex") == "http://fujinet.local:8095/mount?hostslot=2&deviceslot=2&mode=1&filename=/a%20b.xex");
  PRUEFE(baue_mount_url("192.168.0.50/", 0, 1, "/x.atr") == "http://192.168.0.50/mount?hostslot=0&deviceslot=0&mode=1&filename=/x.atr");
  PRUEFE(baue_mount_url("HTTP://Fuji.local:8095/", 0, 1, "/x.atr") == "HTTP://Fuji.local:8095/mount?hostslot=0&deviceslot=0&mode=1&filename=/x.atr");
  PRUEFE(baue_mount_url("http://192.168.0.50//", 0, 1, "/x.atr") == "http://192.168.0.50/mount?hostslot=0&deviceslot=0&mode=1&filename=/x.atr");
  // Leerzeichen um die Adresse (aus der Weboberfläche kopiert) werden entfernt.
  PRUEFE(baue_mount_url(" 192.168.0.50 ", 0, 1, "/x.atr") == "http://192.168.0.50/mount?hostslot=0&deviceslot=0&mode=1&filename=/x.atr");
  PRUEFE(baue_hosts_url(" 192.168.0.50") == "http://192.168.0.50/hosts");
  PRUEFE(!baue_hosts_url("   ").has_value());
  PRUEFE(!baue_mount_url("/", 0, 1, "/x.atr"));
  PRUEFE(!baue_mount_url("", 0, 1, "/x.atr"));  // url_ohne_adresse
  PRUEFE(!baue_mount_url("h", 8, 1, "/x.atr") && !baue_mount_url("h", 0, 0, "/x.atr") && !baue_mount_url("h", 0, 9, "/x.atr"));
  // Antwort
  PRUEFE(werte_antwort_aus(200, "<p>Operation successful.</p>") == MountErgebnis::erfolg);
  PRUEFE(werte_antwort_aus(200, "<title>Error</title>") == MountErgebnis::fehler_fujinet);
  PRUEFE(werte_antwort_aus(303, "") == MountErgebnis::verweigert);    // ergebnis_303
  PRUEFE(werte_antwort_aus(401, "{}") == MountErgebnis::verweigert);  // ergebnis_401
  PRUEFE(werte_antwort_aus(0, "") == MountErgebnis::nicht_erreichbar);  // ergebnis_status_0
  PRUEFE(werte_antwort_aus(-1, "") == MountErgebnis::nicht_erreichbar);
  PRUEFE(werte_antwort_aus(500, "") == MountErgebnis::unbekannt);
  PRUEFE(werte_antwort_aus(200, "<html>irgendwas</html>") == MountErgebnis::unbekannt);
  // Entpreller
  Entpreller e(3000);
  PRUEFE(e.neu("04-A1", 1000) && !e.neu("04-A1", 3999) && e.neu("04-A1", 4000) && e.neu("04-B2", 4001));
  Entpreller u(3000);
  PRUEFE(u.neu("x", 0xFFFFFF00u) && !u.neu("x", 0x00000100u) && u.neu("x", 0x00000C00u));  // Ueberlauf

  // Kartentext mit Server (tnfs://)
  {
    auto z = lies_karte("tnfs://fujinet.pl/games/Bandits.atr");
    PRUEFE(z && z->host == "fujinet.pl" && z->pfad == "/games/Bandits.atr");
    auto g = lies_karte("  TNFS://Apps.Irata.Online/Atari_8-bit/Games/Homesoft/S/Star Raiders.xex \n");
    PRUEFE(g && g->host == "Apps.Irata.Online" && g->pfad == "/Atari_8-bit/Games/Homesoft/S/Star Raiders.xex");
    auto p = lies_karte("spiele/mule.atr");  // alter Kartentext: kein Server
    PRUEFE(p && p->host.empty() && p->pfad == "/spiele/mule.atr");
    PRUEFE(!lies_karte("tnfs://fujinet.pl"));                 // ohne Pfad
    PRUEFE(!lies_karte("tnfs:///games/x.atr"));               // ohne Server
    PRUEFE(!lies_karte("tnfs://fuji net.pl/games/x.atr"));    // Leerzeichen im Server
    PRUEFE(!lies_karte("tnfs://fujinet.pl/games/x.car"));     // keine Cartridge
    PRUEFE(!lies_karte("tnfs://h&x/games/x.atr"));            // & im Server
    PRUEFE(!lies_karte("http://fujinet.pl/games/x.atr"));     // anderes Protokoll
    PRUEFE(!lies_karte("**launch.random:snes"));
    PRUEFE(lies_karte("tnfs://" + std::string(31, 'a') + "/x.atr"));   // 31 Zeichen: geht
    PRUEFE(!lies_karte("tnfs://" + std::string(32, 'a') + "/x.atr"));  // 32: FujiNet kuerzt
    PRUEFE(karten_text(*z) == "tnfs://fujinet.pl/games/Bandits.atr");
    PRUEFE(karten_text(*p) == "/spiele/mule.atr");
  }
  // Host-Liste des FujiNet (GET /hosts: acht Zeilen)
  {
    const std::string liste = "SD\ntnfs.fujinet.online\napps.irata.online\nfujinet.atari8bit.net\nfujinet.pl\n\n\n\n";
    PRUEFE(finde_host_slot(liste, "fujinet.pl") == 4);
    PRUEFE(finde_host_slot(liste, "APPS.irata.online") == 2);  // Gross/klein egal
    PRUEFE(finde_host_slot(liste, "fujinet.online") == -1);    // nur exakte Namen
    PRUEFE(finde_host_slot(liste, "") == -1);
    PRUEFE(freier_host_slot(liste) == 5);
    const std::string voll = "SD\na\nb\nc\nd\ne\nf\ng\n";
    PRUEFE(freier_host_slot(voll) == -1);
    PRUEFE(freier_host_slot("SD\na") == -1);                    // unvollstaendige Liste: nichts frei
    PRUEFE(freier_host_slot("") == -1);
    PRUEFE(freier_host_slot("SD\na\n\n\n\n\n\nb") == 2);         // 8 Zeilen ohne Umbruch am Ende
    PRUEFE(finde_host_slot("SD\r\nfujinet.pl\r\n", "fujinet.pl") == 1);  // CRLF
    PRUEFE(freier_host_slot("SD\n  \nx\nx\nx\nx\nx\nx\n") == 1); // nur Leerzeichen = frei
  }
  // URLs fuer die Host-Liste
  PRUEFE(baue_hosts_url("192.168.0.183") == "http://192.168.0.183/hosts");
  PRUEFE(baue_hosts_url("http://fuji.local:8095/") == "http://fuji.local:8095/hosts");
  PRUEFE(!baue_hosts_url(""));
  PRUEFE(baue_host_setzen_url("192.168.0.183", 5, "fujinet.pl") == "http://192.168.0.183/hosts?hostslot=5&hostname=fujinet.pl");
  PRUEFE(!baue_host_setzen_url("192.168.0.183", 8, "x") && !baue_host_setzen_url("192.168.0.183", -1, "x"));
  // Stufe 2: Tasmota-Steckdose, Aus und An als getrennte Anfragen
  PRUEFE(baue_steckdose_aus_url("192.168.0.201") == "http://192.168.0.201/cm?cmnd=Power%20Off");
  PRUEFE(baue_steckdose_an_url("192.168.0.201") == "http://192.168.0.201/cm?cmnd=Power%20On");
  PRUEFE(baue_steckdose_aus_url("http://192.168.0.201/") == "http://192.168.0.201/cm?cmnd=Power%20Off");
  PRUEFE(baue_steckdose_an_url("  http://192.168.0.201  ") == "http://192.168.0.201/cm?cmnd=Power%20On");
  PRUEFE(baue_steckdose_aus_url(" 192.168.0.201 ") == baue_steckdose_aus_url("192.168.0.201"));
  PRUEFE(!baue_steckdose_aus_url("") && !baue_steckdose_an_url("") && !baue_steckdose_aus_url("   "));
  PRUEFE(klemme_aus_sekunden(0) == 1 && klemme_aus_sekunden(1) == 1 && klemme_aus_sekunden(2) == 2);
  PRUEFE(klemme_aus_sekunden(30) == 30 && klemme_aus_sekunden(99) == 30 && klemme_aus_sekunden(-5) == 1);
  PRUEFE(baue_steckdosen_status_url(" 192.168.0.201 ") == "http://192.168.0.201/cm?cmnd=Status");
  PRUEFE(!baue_steckdosen_status_url("  "));

  std::printf("%d Pruefungen, %d fehlgeschlagen\n", geprueft, gescheitert);
  if (gescheitert == 0) std::printf("test-karte: %d Pruefungen bestanden\n", geprueft);
  return gescheitert == 0 ? 0 : 1;
}

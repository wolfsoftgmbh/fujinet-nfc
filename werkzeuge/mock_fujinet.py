"""Mock der FujiNet-Firmware fuer Lesertests: antwortet auf GET /mount wie das Original."""

import argparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote, urlsplit

# Woertlich aus data/webui/template/www/redirect_to_index.html der FujiNet-Firmware.
SEITE_OK = """<html>
    <head>
        <title>Successful</title>
        <meta http-equiv="refresh" content="0; URL=/" />
    </head>
    <body>
        <p>Operation successful.</p>
    </body>
</html>"""

# error_page.html der Firmware; der Platzhalter <%FN_ERRMSG%> ist durch Text ersetzt.
SEITE_FEHLER = """<html>
    <head>
        <title>Error</title>
    </head>
    <body>
        <h1>Error</h1>
        <h2>Error: file not found</h2>
    </body>
</html>"""


def query_parsen(roh: str) -> dict[str, str]:
    """Wie FujiNet (httpService.cpp): erst die ganze Query dekodieren, dann an '&' zerlegen."""
    ergebnis: dict[str, str] = {}
    for teil in unquote(roh).split("&"):
        if not teil:
            continue
        schluessel, _, wert = teil.partition("=")
        ergebnis[schluessel] = wert
    return ergebnis


def antwort(
    query: dict[str, str], modus: str, vorhanden: set[str]
) -> tuple[int, dict[str, str], str]:
    """Liefert (Status, Header, Body) fuer GET /mount."""
    if modus == "passwort":
        return 303, {"Location": "/login?redirect=/mount"}, ""
    if modus == "ok" and query.get("filename", "") in vorhanden:
        return 200, {"Content-Type": "text/html"}, SEITE_OK
    return 200, {"Content-Type": "text/html"}, SEITE_FEHLER


def handler_bauen(modus: str, vorhanden: set[str]) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            teile = urlsplit(self.path)
            if teile.path != "/mount":
                self.send_error(404)
                return
            query = query_parsen(teile.query)
            print(f"GET /mount {query}", flush=True)
            status, header, body = antwort(query, modus, vorhanden)
            daten = body.encode()
            self.send_response(status)
            for name, wert in header.items():
                self.send_header(name, wert)
            self.send_header("Content-Length", str(len(daten)))
            self.end_headers()
            self.wfile.write(daten)

        def log_message(self, format: str, *args: object) -> None:
            pass

    return Handler


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--port", type=int, default=8096)
    parser.add_argument("--modus", choices=["ok", "fehler", "passwort"], default="ok")
    parser.add_argument("--vorhanden", nargs="*", default=[])
    args = parser.parse_args()
    server = HTTPServer(("0.0.0.0", args.port), handler_bauen(args.modus, set(args.vorhanden)))
    server.serve_forever()


if __name__ == "__main__":
    main()

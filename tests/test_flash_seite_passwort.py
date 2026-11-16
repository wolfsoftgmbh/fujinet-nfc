"""Haken "Passwort anzeigen" im WLAN-Dialog der Flash-Seite (site/index.html), im Headless-Chromium.

Ohne Playwright oder Chromium wird der Test übersprungen.
"""

import functools
import http.server
import threading
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import pytest

sync_api = pytest.importorskip("playwright.sync_api")

SITE = Path(__file__).resolve().parent.parent / "site"

STELLVERTRETER = """
() => {
  const dialog = document.createElement("ewt-install-dialog");
  const wurzel = dialog.attachShadow({ mode: "open" });
  wurzel.innerHTML = '<div id="box"><ew-filled-text-field name="password" '
    + 'type="password"></ew-filled-text-field></div>';
  document.body.appendChild(dialog);
  window.__dialog = dialog;
}
"""
ZAEHLE = "() => window.__dialog.shadowRoot.querySelectorAll('input[type=checkbox]').length"
FELD_TYP = (
    "() => window.__dialog.shadowRoot.querySelector('ew-filled-text-field').getAttribute('type')"
)


class _StillerHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
        pass


@pytest.fixture
def seite_url() -> Iterator[str]:
    handler = functools.partial(_StillerHandler, directory=str(SITE))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_address[1]}/index.html"
    server.shutdown()
    server.server_close()


@pytest.fixture
def seite(seite_url: str) -> Iterator[Any]:
    with sync_api.sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception as fehler:  # kein Chromium installiert
            pytest.skip(f"kein Chromium: {fehler}")
        page = browser.new_page()
        page.fremde: list[str] = []  # type: ignore[attr-defined]
        page.on(
            "request",
            lambda r: (
                page.fremde.append(r.url)  # type: ignore[attr-defined]
                if not r.url.startswith(("http://127.0.0.1", "data:", "blob:"))
                else None
            ),
        )
        page.goto(seite_url)
        yield page
        browser.close()


def test_haken_erscheint_einmal_und_schaltet(seite: Any) -> None:
    seite.evaluate(STELLVERTRETER)
    seite.wait_for_function(f"({ZAEHLE})() === 1")
    assert seite.evaluate(FELD_TYP) == "password"
    haken = seite.locator("ewt-install-dialog input[type=checkbox]")
    haken.check()
    assert seite.evaluate(FELD_TYP) == "text"
    assert (
        seite.evaluate(
            "() => window.__dialog.shadowRoot.querySelector('ew-filled-text-field')"
            ".getAttribute('type')"
        )
        == "text"
    )
    haken.uncheck()
    assert seite.evaluate(FELD_TYP) == "password"
    assert seite.evaluate(ZAEHLE) == 1


def test_neu_erzeugtes_feld_bekommt_haken_wieder(seite: Any) -> None:
    seite.evaluate(STELLVERTRETER)
    seite.wait_for_function(f"({ZAEHLE})() === 1")
    seite.locator("ewt-install-dialog input[type=checkbox]").check()
    seite.evaluate(
        "() => { const w = window.__dialog.shadowRoot; w.getElementById('box').innerHTML ="
        ' \'<ew-filled-text-field name="password" type="password"></ew-filled-text-field>\'; }'
    )
    seite.wait_for_function(f"({ZAEHLE})() === 1")
    assert seite.evaluate(FELD_TYP) == "password"
    assert seite.locator("ewt-install-dialog input[type=checkbox]").is_checked() is False


def test_text_folgt_der_sprache(seite: Any) -> None:
    seite.click("button[data-wahl=de]")
    seite.evaluate(STELLVERTRETER)
    seite.wait_for_function(f"({ZAEHLE})() === 1")
    assert "Passwort anzeigen" in seite.evaluate("() => window.__dialog.shadowRoot.textContent")


def test_echtes_feld_gibt_type_weiter(seite: Any) -> None:
    ergebnis = seite.evaluate(
        """async () => {
          await import("./vendor/esp-web-tools/web/install-dialog-im156JnI.js");
          if (!customElements.get("ew-filled-text-field")) return "nicht definiert";
          const f = document.createElement("ew-filled-text-field");
          f.setAttribute("name", "password");
          f.type = "password";
          document.body.appendChild(f);
          await f.updateComplete;
          f.type = "text";
          await f.updateComplete;
          const innen = f.shadowRoot.querySelector("input");
          return innen ? innen.type : "kein input";
        }"""
    )
    if ergebnis == "nicht definiert":
        pytest.skip("ew-filled-text-field ohne Dialog nicht definiert")
    assert ergebnis == "text"


def test_keine_fremden_anfragen(seite: Any) -> None:
    seite.evaluate(STELLVERTRETER)
    seite.wait_for_function(f"({ZAEHLE})() === 1")
    assert seite.fremde == []

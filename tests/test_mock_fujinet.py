import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "werkzeuge"))

import mock_fujinet as mf  # noqa: E402

Q = {"hostslot": "1", "deviceslot": "1", "mode": "1", "filename": "/spiele/mule.atr"}
VORHANDEN = {"/spiele/mule.atr"}


def test_ok_vorhanden() -> None:
    status, _, body = mf.antwort(Q, "ok", VORHANDEN)
    assert status == 200
    assert "Operation successful." in body


def test_ok_fehlt() -> None:
    status, _, body = mf.antwort(Q, "ok", set())
    assert status == 200
    assert "<title>Error</title>" in body


def test_fehler() -> None:
    status, _, body = mf.antwort(Q, "fehler", VORHANDEN)
    assert status == 200
    assert "<title>Error</title>" in body


def test_passwort_303() -> None:
    status, header, _ = mf.antwort(Q, "passwort", VORHANDEN)
    assert status == 303
    assert header["Location"].startswith("/login?")


def test_query_wie_fujinet_dekodiert() -> None:
    q = mf.query_parsen("hostslot=1&filename=/a%26b.atr")
    assert q["filename"] == "/a"
    assert q["hostslot"] == "1"

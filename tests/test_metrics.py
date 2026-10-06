import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from metrics import accuracy, konfusionsmatrix, konsistenz, unterschaetzungsquote
from run_eval import parse_antwort


def test_accuracy():
    assert accuracy([("high", "high"), ("high", "minimal")]) == 0.5


def test_unterschaetzung_zaehlt_nur_zu_niedrige_einstufung():
    paare = [("high", "minimal"), ("minimal", "high"), ("limited", "limited")]
    assert abs(unterschaetzungsquote(paare) - 1 / 3) < 1e-9


def test_ungueltige_antwort_zaehlt_als_unterschaetzung():
    assert unterschaetzungsquote([("high", None)]) == 1.0


def test_konfusionsmatrix_ungueltig():
    m = konfusionsmatrix([("high", None)])
    assert m["high"]["ungueltig"] == 1


def test_konsistenz():
    assert konsistenz({"a": ["high", "high"], "b": ["high", "limited"]}) == 0.5


def test_parse_antwort():
    assert parse_antwort('Text {"klasse": "High", "begruendung": "x"}') == "high"
    assert parse_antwort("kein json") is None
    assert parse_antwort('{"klasse": "unbekannt"}') is None

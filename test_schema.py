import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from run_eval import lade_faelle

PFLICHT = {"id", "beschreibung", "erwartete_klasse", "rechtsgrundlage", "begruendung", "schwierigkeit"}
KLASSEN = {"prohibited", "high", "limited", "minimal"}
STUFEN = {"leicht", "mittel", "schwer"}


def test_faelle_haben_gueltiges_schema():
    faelle = lade_faelle()
    assert faelle, "Keine Faelle geladen"
    for f in faelle:
        assert set(f) == PFLICHT, f["id"]
        assert re.fullmatch(r"case_\d{3}", f["id"])
        assert f["erwartete_klasse"] in KLASSEN
        assert f["schwierigkeit"] in STUFEN


def test_ids_sind_eindeutig():
    ids = [f["id"] for f in lade_faelle()]
    assert len(ids) == len(set(ids))

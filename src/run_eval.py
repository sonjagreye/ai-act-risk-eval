"""Fuehrt die Faelle gegen ein Modell aus und schreibt Ergebnisse als JSONL.

Beispiele:
  python src/run_eval.py --provider mock
  ANTHROPIC_API_KEY=... ANTHROPIC_WORKSPACE_ID=... python src/run_eval.py --provider anthropic --model <modellname> --runs 3
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
from metrics import (KLASSEN, accuracy, konfusionsmatrix, konsistenz,
                     nach_schwierigkeit, unterschaetzungsquote)

ROOT = Path(__file__).resolve().parent.parent


def lade_faelle(pfad=ROOT / "data" / "cases.yaml"):
    with open(pfad, encoding="utf-8") as f:
        return yaml.safe_load(f)


def baue_prompt(vorlage, beschreibung):
    return vorlage.replace("{beschreibung}", beschreibung)


def parse_antwort(text):
    """Extrahiert die Klasse aus einer JSON-Antwort. Gibt None bei Fehlern."""
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return None
    try:
        klasse = json.loads(match.group(0)).get("klasse", "").strip().lower()
    except (json.JSONDecodeError, AttributeError):
        return None
    return klasse if klasse in KLASSEN else None


def modell_mock(prompt, **_):
    """Deterministischer Platzhalter fuer Tests und Trockenlaeufe."""
    return '{"klasse": "high", "begruendung": "Mock-Antwort"}'


def modell_anthropic(prompt, model, **_):
    import anthropic  # optionale Abhaengigkeit

    workspace_id = os.getenv("ANTHROPIC_WORKSPACE_ID")
    kwargs = {}
    if workspace_id:
        kwargs["default_headers"] = {"anthropic-workspace-id": workspace_id}

    client = anthropic.Anthropic(**kwargs)
    antwort = client.messages.create(
        model=model, max_tokens=400,
        messages=[{"role": "user", "content": prompt}],
    )

    # Neuere Claude-Modelle koennen vor dem eigentlichen Text zusaetzliche
    # Content-Bloecke (z. B. ThinkingBlock) liefern. Fuer die Auswertung werden
    # nur Text-Bloecke zusammengefuehrt.
    text_bloecke = [
        block.text
        for block in antwort.content
        if getattr(block, "type", None) == "text" and getattr(block, "text", None)
    ]
    if not text_bloecke:
        raise ValueError("Anthropic-Antwort enthielt keinen Text-Block.")
    return "\n".join(text_bloecke)


PROVIDER = {"mock": modell_mock, "anthropic": modell_anthropic}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--provider", choices=PROVIDER, default="mock")
    ap.add_argument("--model", default="")
    ap.add_argument("--prompt", default=str(ROOT / "prompts" / "zero_shot.txt"))
    ap.add_argument("--runs", type=int, default=1)
    ap.add_argument("--out", default=str(ROOT / "results" / "raw"))
    args = ap.parse_args()

    faelle = lade_faelle()
    vorlage = Path(args.prompt).read_text(encoding="utf-8")
    aufruf = PROVIDER[args.provider]

    zeilen, laeufe = [], {}
    for fall in faelle:
        for lauf in range(args.runs):
            roh = aufruf(baue_prompt(vorlage, fall["beschreibung"]), model=args.model)
            klasse = parse_antwort(roh)
            laeufe.setdefault(fall["id"], []).append(klasse)
            zeilen.append({
                "fall": fall["id"], "lauf": lauf, "erwartet": fall["erwartete_klasse"],
                "vorhergesagt": klasse, "schwierigkeit": fall["schwierigkeit"], "roh": roh,
            })

    erste_zeilen = [z for z in zeilen if z["lauf"] == 0]
    erste = [(z["erwartet"], z["vorhergesagt"]) for z in erste_zeilen]
    bericht = {
        "provider": args.provider, "modell": args.model, "laeufe": args.runs,
        "zeitpunkt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "accuracy": round(accuracy(erste), 3),
        "unterschaetzung": round(unterschaetzungsquote(erste), 3),
        "konsistenz": round(konsistenz(laeufe), 3) if args.runs > 1 else None,
        "nach_schwierigkeit": nach_schwierigkeit(erste_zeilen),
        "konfusionsmatrix": konfusionsmatrix(erste),
    }

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    stempel = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"{args.provider}_{args.model or 'default'}_{stempel}".replace("/", "-")
    (out / f"{name}.jsonl").write_text(
        "\n".join(json.dumps(z, ensure_ascii=False) for z in zeilen), encoding="utf-8")
    (out / f"{name}_summary.json").write_text(
        json.dumps(bericht, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(bericht, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

# ai-act-risk-eval

**Author:** Sonja Greye

Evaluation, wie zuverlaessig Sprachmodelle KI-Anwendungsfaelle nach der Verordnung (EU) 2024/1689 (EU AI Act) einer Risikoklasse zuordnen.

> Dieses Repository ist ein Forschungs- und Lernprojekt und keine Rechtsberatung.

## Fragestellung

1. Wie oft stimmt die Einstufung eines Modells mit der Einstufung aus dem Gesetzestext ueberein?
2. Wie haeufig wird das Risiko **zu niedrig** eingestuft? Dieser Fehler ist in der Praxis schwerwiegender als eine Ueberschaetzung.
3. Wie konsistent sind die Antworten bei wiederholten Laeufen?
4. Wo liegen die Schwaechen: bei Ausnahmen (z. B. Betrugserkennung), bei Transparenzpflichten oder bei verbotenen Praktiken?

## Methode

- **Faelle:** `data/cases.yaml`, eigenformulierte fiktive Anwendungsfaelle mit erwarteter Klasse, Rechtsgrundlage und Begruendung. Schema: `data/schema.json`.
- **Klassen:** `prohibited` (Art. 5), `high` (Art. 6 i.V.m. Anhang III), `limited` (Art. 50), `minimal`.
- **Prompt:** `prompts/zero_shot.txt`. Weitere Varianten (mit Gesetzesauszug, mit Begruendungspflicht) lassen sich als zusaetzliche Dateien ergaenzen.
- **Metriken:** Genauigkeit, Konfusionsmatrix, Unterschaetzungsquote, Konsistenz ueber mehrere Laeufe, Genauigkeit nach Schwierigkeit (`src/metrics.py`).
- Ungueltige Modellantworten (kein parsebares JSON) zaehlen als Unterschaetzung.

## Nutzung

```bash
pip install -r requirements.txt
pytest -q

# Trockenlauf ohne API
python src/run_eval.py --provider mock

# Echter Lauf (zusaetzlich: pip install anthropic)
export ANTHROPIC_API_KEY=...
python src/run_eval.py --provider anthropic --model <modellname> --runs 3
```

Rohantworten und Zusammenfassung landen in `results/raw/` (nicht versioniert). Auswertungen, die veroeffentlicht werden sollen, kommen als Bericht nach `results/`.

## Ergebnisse

_Noch ausstehend. Hier Tabelle und Diagramm je Modell und Prompt-Variante eintragen, mit Datum, Modellversion und Anzahl der Laeufe._

## Grenzen

- Kleine Stichprobe, daher keine statistisch belastbaren Aussagen.
- Die Einstufung einzelner Faelle hat Auslegungsspielraum. Die erwartete Klasse ist eine begruendete Lesart, keine verbindliche Auskunft.
- Die Faelle sind knapp gehalten. Reale Systeme haben mehr Kontext, der die Einstufung aendern kann.
- Der Rechtsstand (inklusive moeglicher Aenderungen und Fristen) muss vor Veroeffentlichung geprueft werden.

## Roadmap

- [ ] Auf 40 bis 60 Faelle erweitern, mit Gegenlesen durch eine fachkundige Person
- [ ] Prompt-Varianten ergaenzen und vergleichen
- [ ] Auswertungsskript mit Diagramm
- [ ] Weitere Provider anbinden

## Lizenz

MIT, siehe `LICENSE`.

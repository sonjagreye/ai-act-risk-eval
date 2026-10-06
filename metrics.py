"""Metriken fuer die Risikoklassifizierung. Keine externen Abhaengigkeiten."""
from collections import Counter, defaultdict

KLASSEN = ["minimal", "limited", "high", "prohibited"]
RANG = {k: i for i, k in enumerate(KLASSEN)}


def accuracy(paare):
    """paare: Liste von (erwartet, vorhergesagt)."""
    if not paare:
        return 0.0
    return sum(1 for e, v in paare if e == v) / len(paare)


def konfusionsmatrix(paare):
    matrix = {e: {v: 0 for v in KLASSEN + ["ungueltig"]} for e in KLASSEN}
    for e, v in paare:
        matrix[e][v if v in KLASSEN else "ungueltig"] += 1
    return matrix


def unterschaetzungsquote(paare):
    """Anteil der Faelle, in denen das Risiko zu niedrig eingestuft wurde.
    Ungueltige Antworten zaehlen als Unterschaetzung."""
    if not paare:
        return 0.0
    kritisch = 0
    for e, v in paare:
        if v not in RANG or RANG[v] < RANG[e]:
            kritisch += 1
    return kritisch / len(paare)


def konsistenz(laeufe):
    """laeufe: dict fall_id -> Liste vorhergesagter Klassen ueber mehrere Laeufe.
    Rueckgabe: Anteil der Faelle, bei denen alle Laeufe uebereinstimmen."""
    if not laeufe:
        return 0.0
    gleich = sum(1 for antworten in laeufe.values() if len(set(antworten)) == 1)
    return gleich / len(laeufe)


def nach_schwierigkeit(eintraege):
    """eintraege: Liste von dicts mit schwierigkeit, erwartet, vorhergesagt."""
    gruppen = defaultdict(list)
    for e in eintraege:
        gruppen[e["schwierigkeit"]].append((e["erwartet"], e["vorhergesagt"]))
    return {g: accuracy(p) for g, p in gruppen.items()}


def verteilung(werte):
    return dict(Counter(werte))

"""Ajoute des relevés de logements (JSON sur stdin) à suivi/logements.csv et signale les variations.

Entrée : liste d'objets {source (booking|airbnb), base, nuits, nom, slug (Booking) ou id de l'annonce (Airbnb), chambres, m2, note, note_sur (10 ou 5), avis, total_eur, remarque}.
"""
import csv, datetime, json, os, sys

sys.stdout.reconfigure(encoding="utf-8")
CSV = r"C:\Users\benoi\Documents\Voyages\2027-08_Reunion-31juil-13aout\suivi\logements.csv"
COLS = ["date", "source", "base", "nuits", "nom", "slug", "chambres", "m2", "note", "note_sur", "avis", "total_eur", "remarque"]
today = datetime.date.today().isoformat()
old = list(csv.DictReader(open(CSV, encoding="utf-8")))
last = {}
for r in old:
    last[(r["source"], r["base"], r["slug"])] = r
new = json.load(sys.stdin)
with open(CSV, "a", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    for r in new:
        w.writerow([today, r["source"], r["base"], r["nuits"], r["nom"], r["slug"], r.get("chambres", ""), r.get("m2", ""), r.get("note", ""), r.get("note_sur", ""), r.get("avis", ""), r["total_eur"], r.get("remarque", "")])
        p = last.get((r["source"], r["base"], r["slug"]))
        if p is None:
            print("NOUVEAU", r["base"], r["nom"], r["total_eur"], "€")
        elif float(p["total_eur"]) != float(r["total_eur"]):
            print("VARIATION", r["base"], r["nom"], p["total_eur"], "→", r["total_eur"], "€ (précédent %s)" % p["date"])
print("Relevé logements enregistré :", len(new), "lignes")

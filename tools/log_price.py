"""Ajoute un relevé de prix au CSV de suivi et dit si c'est le moment d'acheter.

Usage : python log_price.py --fare Smart --out 4274.88 --ret 2546.72 [--note "..."]
        python log_price.py --report
"""
import argparse, csv, datetime, os, sys
sys.stdout.reconfigure(encoding="utf-8")

CSV = r"C:\Users\benoi\Documents\Voyages\2027-08_Reunion-31juil-13aout\suivi\prix.csv"
COLS = ["date", "fare", "aller_6pax", "retour_6pax", "total_6pax", "light_adulte_calendrier", "note"]


def rows():
    if not os.path.exists(CSV):
        return []
    with open(CSV, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def verdict(fare):
    hist = [r for r in rows() if r["fare"] == fare and r["total_6pax"]]
    if not hist:
        return "Premier relevé."
    last = float(hist[-1]["total_6pax"])
    best = min(hist, key=lambda r: float(r["total_6pax"]))
    b = float(best["total_6pax"])
    if last <= b:
        return f"NOUVEAU PLUS BAS : {last:.2f} € (équivalent ou sous l'ancien record du {best['date']})."
    return f"Dernier {last:.2f} € ; plus bas jamais vu {b:.2f} € le {best['date']} (écart +{last - b:.2f} €)."


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--fare", default="Smart")
    p.add_argument("--out", type=float)
    p.add_argument("--ret", type=float)
    p.add_argument("--light-adulte", type=float, default=None)
    p.add_argument("--note", default="")
    p.add_argument("--report", action="store_true")
    a = p.parse_args()
    if a.report:
        for fare in sorted({r["fare"] for r in rows()}):
            print(fare, "->", verdict(fare))
        return
    if a.out is None or a.ret is None:
        sys.exit("--out et --ret requis")
    new = not os.path.exists(CSV)
    os.makedirs(os.path.dirname(CSV), exist_ok=True)
    with open(CSV, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(COLS)
        w.writerow([datetime.date.today().isoformat(), a.fare, a.out, a.ret, round(a.out + a.ret, 2),
                    a.light_adulte if a.light_adulte is not None else "", a.note])
    print(verdict(a.fare))


if __name__ == "__main__":
    main()

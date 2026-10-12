"""Variante « juillet » : aller ven. 2 juillet 2027, retour ven. 16 juillet. Produit juillet/index.html à partir des mêmes scripts."""
import os, re

HERE = os.path.dirname(os.path.abspath(__file__))


def rep(s, old, new, count=1):
    assert old in s, "introuvable : " + old[:70]
    return s.replace(old, new, count)


# ---- données de base (build_reunion2) adaptées
d2 = open(os.path.join(HERE, "build_reunion2.py"), encoding="utf-8").read()
d2 = rep(d2, '("Light+", 4041.88, 2319.72,', '("Light+", 2159.48, 2325.12,')
d2 = rep(d2, '("Smart", 4274.88, 2546.72,', '("Smart", 2392.48, 2552.12,')
d2 = rep(d2, '("Flex", 4699.88, 3572.72,', '("Flex", 4116.48, 3578.12,')
d2 = re.sub(r"STRIP = \[.*?\]\n", 'STRIP = [("mar 29/06", 2045.48), ("mer 30/06", 2159.48), ("jeu 1/07", 2272.48), ("ven 2/07", 2159.48), ("sam 3/07", 3458.48), ("dim 4/07", 3458.48), ("lun 5/07", 3458.48)]\n', d2, count=1, flags=re.S)
d2 = rep(d2, 'lab == "sam 31/07"', 'lab == "ven 2/07"')
d2 = rep(d2, '"\\suivi\\prix.csv"', '"\\suivi\\prix_juillet.csv"') if '"\\suivi\\prix.csv"' in d2 else d2.replace(r'\suivi\prix.csv', r'\suivi\prix_juillet.csv')
d2 = rep(d2, "Monospace 7 places, 12 jours, siège auto", "Monospace 7 places, 13 jours, siège auto")
d2 = rep(d2, '("Monospace 7 places, 13 jours, siège auto", 1100,', '("Monospace 7 places, 13 jours, siège auto", 1200,')
d2 = rep(d2, '("Repas et courses · 13 jours", 1450, "≈ 110 €/jour, estimation")', '("Repas et courses · 14 jours", 1550, "≈ 110 €/jour, estimation")')
d2 = d2.replace("la nuit en août", "la nuit en juillet").replace("offres août 2027 pas encore ouvertes", "offres de juillet 2027 pas encore ouvertes")
VAR2 = "build_reunion2_juillet.py"
open(os.path.join(HERE, VAR2), "w", encoding="utf-8").write(d2)

# ---- script principal adapté
s = open(os.path.join(HERE, "build_reunion3.py"), encoding="utf-8").read()
s = rep(s, '"build_reunion2.py"', '"%s"' % VAR2)
s = rep(s, r'\suivi\logements.csv', r'\suivi\logements_juillet.csv')
s = rep(s, 'open(OUT + r"\\index.html", "w", encoding="utf-8").write(page)', 'os.makedirs(OUT + r"\\juillet", exist_ok=True)\nopen(OUT + r"\\juillet\\index.html", "w", encoding="utf-8").write(page)')
s = rep(s, "<title>La Réunion, été 2027</title>", "<title>La Réunion, juillet 2027</title>")
s = rep(s, '<p class="dates">sam. 31 juillet → ven. 13 août 2027<br>', '<p class="dates">ven. 2 juillet → ven. 16 juillet 2027<br>')
s = rep(s, "Vols relevés le 11 octobre 2026", "Vols relevés le 12 octobre 2026")
s = rep(s, "puis six jours de lagon et de découvertes", "puis sept jours de lagon et de découvertes")
s = rep(s, '<div class="rseg t" style="flex:4"><b>C</b><span>Saint-Gilles · 4 nuits</span></div>', '<div class="rseg t" style="flex:5"><b>C</b><span>Saint-Gilles · 5 nuits</span></div>')
s = rep(s, "Jours 6 et 8 : à pied", "Jours 6, 8 et 11 : à pied")
s = rep(s, '<article class="fl"><p class="fn">BF 700 · samedi 31 juillet</p><p class="big">19:55 <i>→</i> 09:00</p><p>Orly 4 → Saint-Denis, A350-1000, direct, 11 h 05. Arrivée dimanche 1er août.</p></article>',
        '<article class="fl"><p class="fn">BF 702 · vendredi 2 juillet</p><p class="big">16:30 <i>→</i> 05:35</p><p>Orly 4 → Saint-Denis, direct. Arrivée samedi 3 juillet à 05:35, avant l\'ouverture des logements.</p></article>')
s = rep(s, "BF 703 · vendredi 13 août", "BF 703 · vendredi 16 juillet")
s = rep(s, "Prix du 11/10/2026", "Prix du 12/10/2026")
s = rep(s, "décider de la date de départ (31/07, 28/07 ou 1/08) et du tarif.", "le départ du vendredi 2 juillet suppose l'accord de l'autre parent (les enfants sont à vous à partir du samedi 3) et de sortir les enfants avant la fin des cours.")
s = rep(s, "la veille du 2 août", "la veille du 4 juillet")
s = rep(s, "offres d'août 2027 pas encore en ligne", "offres de juillet 2027 pas encore en ligne")
# encadré des vols
i = s.index('<p class="callout"><strong>À noter.</strong>')
j = s.index("</p>", i) + 4
s = s[:i] + ('<p class="callout"><strong>À noter.</strong> Le vendredi 2 juillet est le jour le moins cher du mois (2 159 € pour six en Light+, aller seul). Le samedi 3 juillet coûte 3 458 €, le 31 juillet 4 042 €. '
             'Le vol part à 16 h 30 et arrive à 05 h 35 : il faut partir de Lille vers 11 h. Les enfants seraient à vous dès le vendredi, alors que le calendrier les donne à partir du samedi 3.</p>') + s[j:]
# nuits et dates du budget
s = rep(s, "3 nuits 1 → 4 août", "3 nuits 3 → 6 juillet")
s = rep(s, "3 nuits 4 → 7 août", "3 nuits 6 → 9 juillet")
s = rep(s, "Saint-Gilles · 4 nuits (La Kaz de Léa & Dérick)", "Saint-Gilles · 5 nuits (La Kaz de Léa & Dérick)")
s = rep(s, "4 nuits 7 → 11 août", "5 nuits 9 → 14 juillet")
s = rep(s, "2 nuits 11 → 13 août", "2 nuits 14 → 16 juillet")
s = rep(s, '"D": "1539190691897979977"' if '"D": "1539190691897979977"' in s else '"D": "la-kaz-coco-villa-avec-piscine-proche-aeroport"', '"D": "1539190691897979977"')
s = rep(s, 'tag = "Notre choix" if (r["slug"] == PICK[Lb["id"]] and not ab)', 'tag = "Notre choix" if (r["slug"] == PICK[Lb["id"]])')
s = rep(s, 'if r["slug"] == PICK[Lb["id"]] and r["source"] == "booking"][0]', 'if r["slug"] == PICK[Lb["id"]]][0]')

# ---- hook : calendrier de juillet, jour supplémentaire, renumérotation
hook = r'''
exec(open(os.path.join(HERE, "days_overrides.py"), encoding="utf-8").read())
LODG[0]["nights"] = "3 → 6 juillet · 3 nuits"
LODG[1]["nights"] = "6 → 9 juillet · 3 nuits"
LODG[2]["nights"] = "9 → 14 juillet · 5 nuits"
LODG[3]["nights"] = "14 → 16 juillet · 2 nuits"
D[0]["steps"] = [("05:35", "Atterrissage à Roland Garros (BF 702, départ d'Orly vendredi 16:30). Bagages, retrait du monospace 7 places avec le siège auto réservé à l'avance.")] + [(t, x) for t, x in D[0]["steps"][1:]]
D[0]["note"] = "Arrivée de bonne heure : les logements ouvrent l'après-midi, demander à poser les bagages dès le matin. Sieste obligatoire au gîte avant la Cité du Volcan. Il fait frais en altitude dès la fin d'après-midi."
D[9]["note"] = D[9]["note"] + " Début de saison des baleines en juillet : observations moins fréquentes qu'en août."
D[11]["note"] = D[11]["note"].replace("Le jeudi 12 août tombe un jour d'ouverture", "Le jeudi 15 juillet tombe un jour d'ouverture")
D[10]["note"] = D[10]["note"] + " Le 14 juillet est férié : vérifier l'ouverture du guide de tunnels."
extra = dict(n=11, p="t", date="", t="Journée libre au lagon", base="C", km="à pied", img=None, steps=[
    ("09:00", "Lagon de l'Ermitage et de La Saline : masque et tuba pour les ados, baignade dans les zones surveillées."),
    ("12:00", "Déjeuner en bord de mer à La Saline-les-Bains."),
    ("14:30", "Aquarium de La Réunion ou Jardin d'Éden à Saint-Gilles-les-Hauts (réouverture de l'aquarium à vérifier)."),
    ("17:30", "Coucher de soleil sur la plage de Boucan Canot, dîner sur place.")],
    note="Journée de réserve : à échanger avec une sortie annulée par la météo (baleines, Maïdo) ou à garder pour se reposer avant le long tour du Sud du lendemain.")
D.insert(10, extra)
WD = ["sam", "dim", "lun", "mar", "mer", "jeu", "ven"]
for i, d in enumerate(D):
    d["n"] = i + 1
    d["date"] = "%s %d/07" % (WD[i % 7], 3 + i)
RT = {(k if k <= 10 else k + 1): v for k, v in RT.items()}
WALK[11] = ["stgilles", "ermitage"]
'''
s = rep(s, 'exec(open(os.path.join(HERE, "days_overrides.py"), encoding="utf-8").read())', hook)
open(os.path.join(HERE, "build_reunion3_juillet.py"), "w", encoding="utf-8").write(s)
exec(compile(s, "build_reunion3_juillet", "exec"))

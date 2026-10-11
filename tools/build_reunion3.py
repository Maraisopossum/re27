"""Page La Réunion 2027, design system « roadbook » : vraie carte OSM + itinéraires OSRM réels."""
import os, io, base64, json, html, csv, math
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, "build_reunion2.py"), encoding="utf-8").read()
exec(compile(src.split("# ---------------------------------------------------------------- HTML")[0], "build_reunion2_data", "exec"))

CARTE = OUT + r"\carte"
RT = {int(k): v for k, v in json.load(open(CARTE + r"\routes.json")).items()}
PL = json.load(open(CARTE + r"\places.json", encoding="utf-8"))
BASE = json.load(open(CARTE + r"\base.json"))
Z = BASE["z"]

NAME = {"RUN": "Aéroport Roland-Garros", "niagara": "Cascade Niagara", "palmistes": "Plaine des Palmistes", "murat": "Bourg-Murat",
        "bellecombe": "Pas de Bellecombe", "belouve": "Bélouve, départ du Trou de Fer", "cilaos": "Cilaos", "etangsale": "Étang-Salé-les-Bains",
        "kelonia": "Kélonia", "stgilles": "Saint-Gilles-les-Bains", "maido": "Belvédère du Maïdo", "stleu": "Saint-Leu", "salines": "Salines-les-Bains",
        "stpierre": "Saint-Pierre", "grandeanse": "Grande Anse", "capmechant": "Cap Méchant", "stphilippe": "Saint-Philippe", "anse_casc": "Anse des Cascades",
        "ndlaves": "Notre-Dame des Laves", "stemarie": "Sainte-Marie, hôtel", "stdenis_jardin": "Jardin de l'État, Saint-Denis", "taibit": "Col du Taïbit",
        "ilet_cordes": "Îlet à Cordes", "ermitage": "Plage de l'Ermitage"}
WALK = {5: ["cilaos", "taibit"], 6: ["cilaos", "ilet_cordes"], 8: ["stgilles", "ermitage"]}
BASES = {"A": "murat", "B": "cilaos", "C": "stgilles", "D": "stemarie"}

# --- textes recalés sur les distances OSRM réelles
def hm(m):
    return "%d h %02d" % (m // 60, m % 60) if m >= 60 else "%d min" % m

for d in D:
    if d["n"] in RT:
        r = RT[d["n"]]
        d["km"] = "%d km · %s" % (round(r["km"]), hm(r["min"]))
    elif d["n"] in WALK:
        d["km"] = "à pied"
FIX = {
    1: [("Cascade Niagara à Sainte-Suzanne, à 10 min de l'aéroport, accès libre : 20 min pour se dégourdir les jambes.", "Cascade Niagara à Sainte-Suzanne, à 15 km de l'aéroport, accès libre : 20 min pour se dégourdir les jambes."),
        ("Installation à Bourg-Murat, courses au supermarché", "Installation à Bourg-Murat (79 km depuis l'aéroport, 2 h de route au total), courses au supermarché")],
    2: [("Départ de Bourg-Murat par la route du Volcan, à travers la Plaine des Sables (paysage lunaire).", "Départ de Bourg-Murat par la route du Volcan, 25 km à travers la Plaine des Sables (paysage lunaire), environ 50 min.")],
    3: [("Départ pour la Plaine des Palmistes puis la route forestière de Bébour et Bélouve.", "Départ pour la Plaine des Palmistes puis la route forestière de Bébour et Bélouve : 30 km, environ 55 min.")],
    4: [("Départ de Bourg-Murat. RN3 vers Saint-Pierre, puis RN5 vers Saint-Louis (1 h 15).", "Départ de Bourg-Murat par Entre-Deux jusqu'à Saint-Louis, puis la RN5 de Cilaos. 56 km au total."),
        ("La route de Cilaos : 35 km, plus de 400 virages, 1 h 15. Pause à un belvédère au milieu. Médicament contre le mal des transports pour les petits, si besoin.", "La route de Cilaos : 35 km et plus de 400 virages. Le calculateur annonce 1 h 15 au total, prévoir 2 h avec une pause à un belvédère. Médicament contre le mal des transports pour les petits, si besoin."),
        ("Arrivée à Cilaos, déjeuner au village", "Arrivée à Cilaos vers 11:30, déjeuner au village")],
    7: [("Départ de Cilaos et descente vers Saint-Louis (1 h 15).", "Départ de Cilaos et descente vers Saint-Louis (1 h 15 de route de montagne)."),
        ("Plage d'Étang-Salé-les-Bains : sable noir volcanique, baignade et pause d'une heure.", "Plage d'Étang-Salé-les-Bains (47 km depuis Cilaos) : sable noir volcanique, baignade et pause d'une heure.")],
    9: [("Départ de Saint-Gilles par la route du Maïdo, via Le Guillaume.", "Départ de Saint-Gilles par la route du Maïdo, 35 km, 1 h environ.")],
    10: [("Saint-Leu (25 min) :", "Saint-Leu (16 km) :")],
    11: [("Départ de Saint-Gilles par la RN1 vers Saint-Pierre (1 h). Front de mer et marché de Saint-Pierre.", "Départ de Saint-Gilles par la RN1 vers Saint-Pierre (52 km). Front de mer de Saint-Pierre."),
         ("Grande Anse : grande plage de galets et sable, côté sauvage du Sud.", "Grande Anse (11 km plus loin) : grande plage, côté sauvage du Sud."),
         ("Cap Méchant et Puits des Anglais à Saint-Philippe : falaises basaltiques et coulées de lave.", "Cap Méchant (22 km) à Saint-Philippe : falaises basaltiques et coulées de lave."),
         ("Anse des Cascades à Sainte-Rose : bassins", "Anse des Cascades à Sainte-Rose (25 km depuis Saint-Philippe) : bassins"),
         ("RN2 par Saint-Benoît jusqu'à Sainte-Marie (≈ 1 h 15).", "RN2 par Saint-Benoît jusqu'à Sainte-Marie (50 km)."),
         ("La plus longue journée de conduite.", "La plus longue journée de conduite : 169 km, 3 h 05 de route sans les arrêts.")],
}
for d in D:
    for a, b in FIX.get(d["n"], []):
        d["steps"] = [(t, s.replace(a, b)) for t, s in d["steps"]]
        d["note"] = d["note"].replace(a, b)
D[10]["km"] = "169 km · 3 h 05"
D[1].update(t="Tout en haut du Piton de la Fournaise : cratère Dolomieu", img="fournaise", steps=[
    ("06:00", "Petit-déjeuner, sacs prêts la veille : 2 à 3 litres d'eau par personne, pique-nique, polaires, coupe-vent, bonnets, gants, lunettes, crème solaire."),
    ("06:30", "Départ de Bourg-Murat par la route du Volcan : 25 km à travers la Plaine des Sables, environ 50 min. Arriver tôt, avant les nuages."),
    ("07:30", "Parking du Pas de Bellecombe, 2 311 m. Il fait 0 à 5 °C et il y a du vent. La petite s'installe dans le porte-bébé rigide."),
    ("07:45", "Escalier de Bellecombe (plus de 400 marches) et descente dans l'Enclos Fouqué."),
    ("08:15", "Formica Leo à 1,3 km, premier cratère : pause, c'est ici que l'on décide de poursuivre."),
    ("08:30", "Traversée de la coulée de lave sur le sentier du cratère Dolomieu : 6,1 km à l'aller, environ 310 m de montée et 190 m de descente, 2 h 15 à 2 h 45 avec la petite."),
    ("11:00", "Bord du cratère Dolomieu, vers 2 500 m : pique-nique au bord, 30 à 45 min, vue sur le cratère et son effondrement."),
    ("11:45", "Demi-tour par le même sentier : même distance, même temps."),
    ("14:30", "Retour au parking après la remontée des 400 marches. Total environ 12 km, 5 h 30 à 6 h 30 de marche."),
    ("15:30", "Retour à Bourg-Murat, douche chaude, dîner tôt devant la cheminée.")],
    note="Accès à confirmer la veille auprès de l'ONF et de l'observatoire OVPF : depuis mai 2026 seuls Formica Leo, le sentier Rivals vers le cratère Caubet et le sentier d'accès au site d'observation du Dolomieu étaient ouverts, et l'enclos ferme en cas d'éruption ou d'éboulement. Le point le plus haut atteint peut donc être le site d'observation plutôt que le bord. Plan B si fermé : Formica Leo (2 h) et la Cité du Volcan. Toute la famille ensemble, sans groupes séparés : avec la petite en porte-bébé, relais toutes les 30 min, demi-tour sans discussion dès que le brouillard ou le vent monte. Le lendemain, le Trou de Fer (9 km) arrive sur des jambes fatiguées : décaler d'une journée si besoin.")
exec(open(os.path.join(HERE, "days_overrides.py"), encoding="utf-8").read())
D[4].update(t="Cascade du Bras Rouge en famille, thermes de Cilaos", steps=[
    ("08:30", "Départ à pied de Cilaos vers la cascade du Bras Rouge : environ 3,8 km par le sentier, 2 h 20 aller-retour, 300 m de descente à l'aller et la même remontée au retour."),
    ("11:00", "Pique-nique devant la cascade, on se mouille les pieds."),
    ("12:30", "Remontée vers Cilaos, la petite en porte-bébé, relais entre les adultes."),
    ("14:30", "Thermes de Cilaos (établissement Irénée Accot) pour récupérer."),
    ("17:00", "Village de Cilaos : broderies, lentilles et vin de Cilaos pour les courses du soir.")],
    note="Toute la famille marche ensemble, sans groupes séparés. Le col du Taïbit (830 m de dénivelé, environ 5 h) est écarté pour rester à six. La boucle des cascades fait 12 km : à garder pour un autre voyage.")
TOTAL_KM = round(sum(v["km"] for v in RT.values()))


# --- logements : prix réels Booking (suivi/logements.csv)
LROWS = list(csv.DictReader(open(OUT + r"\suivi\logements.csv", encoding="utf-8")))
LDATE = max(r["date"] for r in LROWS)
PICK = {"A": "la-kaz-a-lena-la-plaine-des-cafres", "B": "au-coeur-des-hauts-cilaos", "C": "la-kaz-de-lea-derick", "D": "la-kaz-coco-villa-avec-piscine-proche-aeroport"}
for Lb in LODG:
    rr = sorted([r for r in LROWS if r["base"] == Lb["id"] and r["date"] == LDATE], key=lambda r: float(r["total_eur"]))
    opts = []
    for r in rr:
        tot, n = float(r["total_eur"]), int(r["nuits"])
        ab = r["source"] == "airbnb"
        facts = []
        if r["chambres"]: facts.append(r["chambres"] + " chambres")
        if r["m2"]: facts.append(r["m2"] + " m²")
        if r["note"]:
            facts.append(("%s/5, %s avis" % (r["note"].replace(".", ","), r["avis"])) if ab else ("note %s/10" % r["note"].replace(".", ",")))
        if r["remarque"]: facts.append(r["remarque"])
        url = ("https://www.airbnb.fr/rooms/%s" % r["slug"]) if ab else ("https://www.booking.com/hotel/re/%s.fr.html" % r["slug"])
        tag = "Notre choix" if (r["slug"] == PICK[Lb["id"]] and not ab) else ("Airbnb" if ab else "Booking")
        opts.append((r["nom"], ", ".join(facts) + ".", url, "%s · %d €/nuit" % (money(tot), round(tot / n)), tag))
    Lb["opts"] = opts
    Lb["pick"] = [float(r["total_eur"]) for r in rr if r["slug"] == PICK[Lb["id"]] and r["source"] == "booking"][0]
BUD[4] = ("Plaine des Cafres · 3 nuits (La Kaz à Léna)", int(LODG[0]["pick"]), "relevé Booking %s, 3 nuits 1 → 4 août" % LDATE)
BUD[5] = ("Cilaos · 3 nuits (Au Coeur des hauts)", int(LODG[1]["pick"]), "relevé Booking %s, 3 nuits 4 → 7 août" % LDATE)
BUD[6] = ("Saint-Gilles · 4 nuits (La Kaz de Léa & Dérick)", int(LODG[2]["pick"]), "relevé Booking %s, 4 nuits 7 → 11 août" % LDATE)
BUD[7] = ("Sainte-Marie · 2 nuits (La Kaz Coco)", int(LODG[3]["pick"]), "relevé Booking %s, 2 nuits 11 → 13 août" % LDATE)

# --- carte
def px(lon, lat):
    x = (lon + 180) / 360 * 2 ** Z
    r = math.radians(lat)
    y = (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2 ** Z
    return ((x - BASE["x0"]) * 256, (y - BASE["y0"]) * 256)


def simplify(pts, tol):
    if len(pts) < 3:
        return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1e-9
    m, idx = 0, 0
    for i in range(1, len(pts) - 1):
        d = abs(dy * pts[i][0] - dx * pts[i][1] + x2 * y1 - y2 * x1) / L
        if d > m:
            m, idx = d, i
    if m > tol:
        return simplify(pts[:idx + 1], tol)[:-1] + simplify(pts[idx:], tol)
    return [pts[0], pts[-1]]


ROUTE_PX = {n: simplify([px(*c) for c in r["coords"]], 1.4) for n, r in RT.items()}
PT = {k: px(v["lon"], v["lat"]) for k, v in PL.items() if v and "lat" in v}

im = Image.open(CARTE + r"\base_z12.png").convert("RGB")
buf = io.BytesIO()
im.save(buf, "WEBP", quality=58, method=6)
BASE_URI = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
print("base map", len(BASE_URI) // 1024, "KB")


def pl(pts):
    return " ".join("%.1f,%.1f" % p for p in pts)


def day_map(n):
    keys = RT[n]["places"] if n in RT else WALK[n]
    pts = []
    if n in RT:
        pts += ROUTE_PX[n]
    pts += [PT[k] for k in keys]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    pad = max(w, h) * 0.14 + 40
    x0, y0, w, h = min(xs) - pad, min(ys) - pad, w + 2 * pad, h + 2 * pad
    ar = 3 / 2  # cadre 3:2
    if w / h < ar:
        nw = h * ar; x0 -= (nw - w) / 2; w = nw
    else:
        nh = w / ar; y0 -= (nh - h) / 2; h = nh
    fs = w / 34
    part = "r" if n <= 6 else "t"
    out = '<svg class="dmap" viewBox="%.0f %.0f %.0f %.0f" role="img" aria-label="Carte du jour %d">' % (x0, y0, w, h, n)
    out += '<use href="#osm"/>'
    if n in RT:
        out += '<polyline points="%s" class="halo" vector-effect="non-scaling-stroke"/><polyline points="%s" class="route %s" vector-effect="non-scaling-stroke"/>' % (pl(ROUTE_PX[n]), pl(ROUTE_PX[n]), part)
    else:
        a, b = PT[keys[0]], PT[keys[1]]
        out += '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" class="walk" vector-effect="non-scaling-stroke"/>' % (a[0], a[1], b[0], b[1])
    seen = set()
    boxes = []
    order = [keys[0], keys[-1]] + [k for k in keys[1:-1]]
    for k in order:
        if k in seen:
            continue
        seen.add(k)
        x, y = PT[k]
        end = k in (keys[0], keys[-1])
        out += '<circle cx="%.1f" cy="%.1f" r="%.1f" class="pin %s"/>' % (x, y, fs * (0.42 if end else 0.3), part if end else "mid")
        lab = NAME[k].split(",")[0]
        right = x < x0 + w * 0.62
        tw = len(lab) * fs * 0.52
        tx = x + fs * 0.75 if right else x - fs * 0.75
        bx0, bx1 = (tx, tx + tw) if right else (tx - tw, tx)
        by0, by1 = y - fs * 0.6, y + fs * 0.6
        if any(not (bx1 < a0 or bx0 > a1 or by1 < b0 or by0 > b1) for a0, a1, b0, b1 in boxes):
            continue
        boxes.append((bx0, bx1, by0, by1))
        out += '<text x="%.1f" y="%.1f" text-anchor="%s" class="plab" style="font-size:%.1fpx">%s</text>' % (tx, y + fs * 0.35, "start" if right else "end", fs, E(lab))
    return out + '<text x="%.0f" y="%.0f" text-anchor="end" class="attr" style="font-size:%.1fpx">© contributeurs OpenStreetMap</text></svg>' % (x0 + w - fs * 0.4, y0 + h - fs * 0.4, fs * 0.62)


def overview_map():
    xs = [p[0] for pts in ROUTE_PX.values() for p in pts]
    ys = [p[1] for pts in ROUTE_PX.values() for p in pts]
    x0, x1, y0, y1 = 120, 2200, 150, 1960
    w, h = x1 - x0, y1 - y0
    out = '<svg class="omap" id="omap" viewBox="%d %d %d %d" role="img" aria-label="Carte de La Réunion avec les trajets en voiture">' % (x0, y0, w, h)
    out += '<use href="#osm"/>'
    for n in sorted(RT):
        part = "r" if n <= 6 else "t"
        out += '<g class="rg" data-d="%d"><polyline points="%s" class="halo" vector-effect="non-scaling-stroke"/><polyline points="%s" class="route %s" vector-effect="non-scaling-stroke"/></g>' % (n, pl(ROUTE_PX[n]), pl(ROUTE_PX[n]), part)
    for L, k in BASES.items():
        x, y = PT[k]
        part = "r" if L in "AB" else "t"
        dx = {"A": 60, "B": -60, "C": -60, "D": 60}[L]
        out += '<g class="base"><circle cx="%.0f" cy="%.0f" r="34" class="bp %s"/><text x="%.0f" y="%.0f" text-anchor="middle" class="bl2">%s</text></g>' % (x, y, part, x, y + 13, L)
    out += '<text x="%d" y="%d" text-anchor="end" class="attr" style="font-size:26px">© contributeurs OpenStreetMap · tracés routiers OSRM</text></svg>' % (x1 - 20, y1 - 20)
    return out


def tulips(n):
    if n not in RT:
        return ""
    r = RT[n]
    rows = '<tr class="st"><td class="g">%s</td><td>%s</td><td class="k">0,0</td><td class="k">0,0</td></tr>' % (GL["start"], E(NAME[r["places"][0]]))
    cum = 0.0
    for i, leg in enumerate(r["legs"]):
        cum += leg["km"]
        last = i == len(r["legs"]) - 1
        rows += '<tr class="%s"><td class="g">%s</td><td>%s<small>%s</small></td><td class="k">%s</td><td class="k">%s</td></tr>' % (
            "en" if last else "mid", GL["end"] if last else GL["via"], E(NAME[leg["to"]]), hm(leg["min"]), ("%.1f" % leg["km"]).replace(".", ","), ("%.1f" % cum).replace(".", ","))
    return '<div class="tw"><table class="tul"><thead><tr><th></th><th>Étape en voiture</th><th>km</th><th>cumul</th></tr></thead><tbody>%s</tbody></table><p class="cap">Distances et durées calculées par OSRM sur OpenStreetMap, hors arrêts. Sur les routes de montagne, compter plus.</p></div>' % rows


GL = {"start": '<svg viewBox="0 0 20 20" aria-hidden="true"><circle cx="10" cy="10" r="6" fill="none" stroke="currentColor" stroke-width="2.4"/><circle cx="10" cy="10" r="2" fill="currentColor"/></svg>',
      "via": '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M10 3 17 10 10 17 3 10Z" fill="none" stroke="currentColor" stroke-width="2.4"/></svg>',
      "end": '<svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 17V3m0 1h10l-3 3.5L15 11H5" fill="currentColor" stroke="currentColor" stroke-width="2"/></svg>'}

exec(open(os.path.join(HERE, "hikes_section.py"), encoding="utf-8").read())
css = open(os.path.join(HERE, "reunion3.css"), encoding="utf-8").read()
js = open(os.path.join(HERE, "reunion3.js"), encoding="utf-8").read()

days_html = ""
for d in D:
    st = "".join('<li><span class="tm">%s</span><span>%s</span></li>' % (E(t), E(s)) for t, s in d["steps"])
    im_h = ""
    if d["img"]:
        im_h = '<figure class="ph"><img src="%s" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>' % (uri(d["img"], 700), E(ALT[d["img"]]), E(ALT[d["img"]]))
    mp = day_map(d["n"]) if (d["n"] in RT or d["n"] in WALK) else ""
    days_html += (
        '<details class="day %s" data-p="%s" id="j%d"><summary><span class="dn">%d</span><span class="dt">%s</span><span class="dr"><span class="dd">%s</span><span class="dk">%s</span></span></summary>'
        '<div class="db"><div class="dleft">%s%s<ol class="steps">%s</ol></div><div class="dside">%s%s<p class="note">%s</p></div></div></details>'
    ) % (d["p"], d["p"], d["n"], d["n"], E(d["t"]), E(d["date"]), E(d["km"]), tulips(d["n"]), "", st, mp, im_h, E(d["note"]))

chips = "".join('<button class="dc %s" data-d="%d" aria-label="Jour %d">%d</button>' % ("r" if n <= 6 else "t", n, n, n) for n in sorted(RT))

lod_html = ""
for L in LODG:
    rows = ""
    for name, desc, url, price, tag in L["opts"]:
        link = '<a href="%s" target="_blank" rel="noopener">Fiche</a>' % E(url) if url else ""
        rows += ('<li class="opt"><div class="on"><h4>%s</h4><p>%s</p></div><div class="op"><strong>%s</strong><em>%s</em>%s</div></li>') % (E(name), E(desc), E(price), E(tag), link)
    lod_html += ('<section class="base %s"><header><span class="bl">%s</span><div><h3>%s</h3><p class="meta">%s · %s</p></div></header><p class="why">%s</p><ul class="opts">%s</ul></section>') % (
        L["cls"], L["id"], E(L["name"]), E(L["nights"]), E(L["alt"]), E(L["why"]), rows)

fare_rows = "".join('<tr><th scope="row">%s</th><td>%s</td><td>%s</td><td><strong>%s</strong></td><td class="l">%s</td></tr>' % (f, money(o), money(r), money(o + r), E(desc)) for f, o, r, desc in FARES)
hist_rows = "".join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><strong>%s</strong></td></tr>' % (r["date"], r["fare"], money(float(r["aller_6pax"])), money(float(r["retour_6pax"])), money(float(r["total_6pax"]))) for r in hist)
fare_opts = "".join('<option value="%s">%s</option>' % (o + r, f) for f, o, r, _ in FARES)
bud_rows = ""
for lab, v, srcb in BUD:
    if v == "FARE":
        bud_rows += '<tr><th scope="row">%s</th><td class="num" id="farev">%s</td><td class="l">%s</td></tr>' % (E(lab), money(FARES[1][1] + FARES[1][2]), E(srcb))
    else:
        bud_rows += '<tr><th scope="row">%s</th><td class="num">%s</td><td class="l">%s</td></tr>' % (E(lab), money(v), E(srcb))
base_total = sum(v for _, v, _ in BUD if v != "FARE")
credits = "".join('<li>%s : %s, %s, <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></li>' % (E(ALT[k]), E(fix(cred[k]["artist"])), E(cred[k]["license"]), E(cred[k]["page"])) for k in ALT if k in cred)

page = f"""<meta charset="utf-8"><meta name="robots" content="noindex,nofollow"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>La Réunion, été 2027</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@500;600;700&family=Barlow:wght@400;500;600&display=swap">
<style>{css}</style>
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs><image id="osm" href="{BASE_URI}" x="0" y="0" width="{BASE['w']}" height="{BASE['h']}"/></defs></svg>
<header class="mast">
  <div class="mast-in">
    <div class="mast-t">
      <h1>La Réunion</h1>
      <p class="dates">sam. 31 juillet → ven. 13 août 2027<br>Lille, Orly, Saint-Denis · 6 voyageurs</p>
      <p class="lead">Six nuits de randonnée dans les hauts, puis six jours de lagon et de découvertes. Environ {TOTAL_KM} km en voiture, tous tracés sur la carte OpenStreetMap ci-contre. Vols relevés le 11 octobre 2026, suivi quotidien des prix, quatre bases à choisir.</p>
    </div>
    <div class="mast-m">{overview_map()}<div class="dchips" role="group" aria-label="Surligner un jour sur la carte">{chips}</div><p class="cap">Touchez un numéro pour surligner le trajet du jour, orange = randonnées, turquoise = tourisme. Jours 5, 6 et 8 : à pied, sans trajet voiture.</p></div>
  </div>
  <div class="ruler" aria-label="Les 12 nuits">
    <div class="rseg r" style="flex:3"><b>A</b><span>Plaine des Cafres · 3 nuits</span></div>
    <div class="rseg r" style="flex:3"><b>B</b><span>Cilaos · 3 nuits</span></div>
    <div class="rseg t" style="flex:4"><b>C</b><span>Saint-Gilles · 4 nuits</span></div>
    <div class="rseg t" style="flex:2"><b>D</b><span>Aéroport · 2 nuits</span></div>
  </div>
</header>
<main class="wrap">
<nav class="nav" aria-label="Sections"><a href="#vols">Vols</a><a href="#suivi">Prix</a><a href="#logements">Logements</a><a href="#randos">Randonnées</a><a href="#jours">Jour par jour</a><a href="#budget">Budget</a><a href="#todo">À faire</a></nav>

<section id="vols">
  <h2>Les vols</h2>
  <div class="flights">
    <article class="fl"><p class="fn">BF 700 · samedi 31 juillet</p><p class="big">19:55 <i>→</i> 09:00</p><p>Orly 4 → Saint-Denis, A350-1000, direct, 11 h 05. Arrivée dimanche 1er août.</p></article>
    <article class="fl"><p class="fn">BF 703 · vendredi 13 août</p><p class="big">08:00 <i>→</i> 17:20</p><p>Saint-Denis → Orly 4, direct, 11 h 20. Arrivée le jour même.</p></article>
  </div>
  <p class="lead sm">Six passagers : 5 « adultes » (tout enfant de 12 ans et plus est facturé adulte) et la petite, tarif enfant de 2 à 11 ans. Prix du 11/10/2026, taxes incluses, pour tous les passagers.</p>
  <div class="tw"><table class="tbl"><thead><tr><th>Tarif</th><th>Aller</th><th>Retour</th><th>Total</th><th class="l">Inclus</th></tr></thead><tbody>{fare_rows}</tbody></table></div>
  <p class="callout"><strong>À noter.</strong> Smart convient : un bagage de 23 kg par personne couvre six valises. Le 31 juillet est le jour le plus cher de la semaine : partir le 28 ou le 29 coûte environ 580 € de moins pour six (Light+, aller seul), le 1er août environ 400 € de moins.</p>
  <h3>Aller seul, six personnes, tarif Light+, selon le jour de départ</h3>
  {chart_svg()}
  <p class="cap">Total pour les six passagers de l'aller seul. Source : moteur de réservation French bee, 11/10/2026.</p>
</section>

<section id="suivi">
  <h2>Suivi quotidien des prix</h2>
  <p class="lead sm">La compétence <code>suivi-prix-reunion</code> relève le calendrier French bee et le total pour six, l'écrit dans un historique et dit si le prix du jour est le plus bas connu. Une tâche planifiée la lance chaque matin à 8h.</p>
  <div class="tw"><table class="tbl"><thead><tr><th>Relevé</th><th>Tarif</th><th>Aller</th><th>Retour</th><th>Total pour 6</th></tr></thead><tbody>{hist_rows}</tbody></table></div>
  <p class="callout">Consultation seulement : aucune donnée personnelle saisie, rien réservé. <a href="https://www.frenchbee.com/fr/la-reunion/vol-paris-la-reunion/calendrier-des-tarifs" target="_blank" rel="noopener">Calendrier des tarifs French bee</a>. Historique : <code>Documents\\Voyages\\2027-08_Reunion-31juil-13aout\\suivi\\prix.csv</code>.</p>
</section>

<section id="logements">
  <h2>Où dormir</h2>
  <p class="lead sm">Quatre bases, du plus frais au plus chaud. Prix <b>relevés sur Booking.com et Airbnb le {LDATE}</b> pour les nuits exactes de chaque base, 5 adultes + 1 enfant de 2 ans, taxes et frais compris, au total du séjour. Rien n'est réservé : les disponibilités et les prix changent, le suivi les relèvera de nouveau.</p>
  {lod_html}
</section>

<section id="randos">
  <h2>Randonnées</h2>
  <p class="lead sm">Six marcheurs ensemble, la petite en porte-bébé. Les tracés viennent d'OpenStreetMap : relations de sentiers balisés quand elles existent (cratère Dolomieu, Trou de Fer, Grand Bassin, Roche Merveilleuse), sinon un tracé calculé sur les sentiers OSM (cascade du Bras Rouge). Les altitudes sont des mesures satellite SRTM, précision de l'ordre de la dizaine de mètres. À comparer au balisage et à la fiche Randopitons avant de partir.</p>
  {hike_html}
  <p class="callout">Pas de tracé fiable dans OpenStreetMap pour La Chapelle et l'Îlet à Cordes (jour 6) : le calcul donnait 11,8 km au lieu de 5 environ. À relever sur Randopitons avant de partir. Le col du Taïbit n'est pas relié au sentier de Cilaos dans OSM et n'est plus au programme.</p>
</section>

<section id="jours">
  <h2>Jour par jour</h2>
  <div class="filters" role="group" aria-label="Filtrer les jours"><button class="chip on" data-f="all">Tous les jours</button><button class="chip" data-f="r">Randonnées</button><button class="chip" data-f="t">Tourisme</button><button class="chip" id="openall">Tout déplier</button></div>
  {days_html}
</section>

<section id="budget">
  <h2>Budget</h2>
  <p class="lead sm">Les vols viennent de relevés réels. Le reste est une estimation raisonnable à remplacer par les devis.</p>
  <label class="sel" for="farepick">Tarif de vol <select id="farepick">{fare_opts}</select></label>
  <div class="tw"><table class="tbl bt"><thead><tr><th>Poste</th><th>Montant</th><th class="l">Base</th></tr></thead><tbody>{bud_rows}</tbody><tfoot><tr><th scope="row">Total</th><td class="num" id="total">0</td><td class="l">hors souvenirs et extras</td></tr></tfoot></table></div>
</section>

<section id="todo">
  <h2>À faire et à vérifier</h2>
  <ul class="todo">
    <li><b>Vols :</b> décider de la date de départ (31/07, 28/07 ou 1/08) et du tarif.</li>
    <li><b>Voiture :</b> offres d'août 2027 pas encore en ligne. Monospace 7 places, siège auto pour la petite, retour de nuit possible.</li>
    <li><b>Volcan :</b> consulter l'arrêté préfectoral et les infos ONF la veille du 2 août.</li>
    <li><b>Matériel :</b> porte-bébé de randonnée, polaires et bonnets pour 2 000 m, chaussures de marche, masque et tuba.</li>
    <li><b>Mer :</b> baignade uniquement dans les zones autorisées du lagon.</li>
    <li><b>Réservations :</b> logements A à D, bateau baleines, tunnels de lave (dès 7 ans, la petite ne peut pas y aller), retrait de la voiture.</li>
  </ul>
  <details id="cred"><summary>Crédits : carte et photos</summary><ul class="cred"><li>Fond de carte © contributeurs <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> (licence ODbL), tuiles standard assemblées au niveau de zoom 12.</li><li>Itinéraires routiers calculés avec OSRM sur les données OpenStreetMap, lieux localisés avec Nominatim. Durées indicatives, la route de montagne est plus lente.</li>{credits}</ul></details>
</section>
</main>
<script>const BASE={base_total};{js}</script>
"""
open(OUT + r"\index.html", "w", encoding="utf-8").write(page)
print(len(page) // 1024, "KB;", TOTAL_KM, "km")

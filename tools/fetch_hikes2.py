"""Randonnées : vrais tracés OSM (relations Waymarked Trails) + routeur piéton OSM, altitudes SRTM, tuiles z14, GPX."""
import json, math, os, time, urllib.request
from PIL import Image

OUT = r"C:\Users\benoi\Documents\Voyages\2027-08_Reunion-31juil-13aout"
CARTE = OUT + r"\carte"
TILES = CARTE + r"\tiles"
os.makedirs(TILES, exist_ok=True)
os.makedirs(OUT + r"\gpx", exist_ok=True)
UA = {"User-Agent": "FamilyTripPlanner/1.0 (benoitdegove@gmail.com)"}


def get(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60).read()


def ll(x, y):
    return (x / 20037508.34 * 180, math.degrees(2 * math.atan(math.exp(y / 20037508.34 * math.pi)) - math.pi / 2))


def hav(p, q):
    R = 6371000
    la1, la2 = math.radians(p[1]), math.radians(q[1])
    dl = math.radians(q[0] - p[0]); dp = la2 - la1
    h = math.sin(dp / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def length(pl):
    return sum(hav(pl[i - 1], pl[i]) for i in range(1, len(pl)))


def relation(rid):
    d = json.loads(get("https://hiking.waymarkedtrails.org/api/v1/details/relation/%d" % rid))
    mains = []
    for m in d["route"]["main"]:
        if "ways" not in m:
            continue
        pl = []
        for w in m["ways"]:
            c = [ll(*p) for p in w["geometry"]["coordinates"]]
            if not pl:
                pl = c
            else:
                if hav(pl[-1], c[0]) <= hav(pl[-1], c[-1]):
                    pl += c[1:]
                else:
                    pl += c[::-1][1:]
        mains.append(pl)
    return d, mains


def foot(a, b):
    u = "https://routing.openstreetmap.de/routed-foot/route/v1/foot/%.5f,%.5f;%.5f,%.5f?overview=full&geometries=geojson" % (a[1], a[0], b[1], b[0])
    return json.loads(get(u))["routes"][0]["geometry"]["coordinates"]


def elev(pts):
    out = []
    for i in range(0, len(pts), 90):
        ch = pts[i:i + 90]
        u = "https://api.opentopodata.org/v1/srtm30m?locations=" + "|".join("%.5f,%.5f" % (p[1], p[0]) for p in ch)
        for t in range(4):
            try:
                r = json.loads(get(u)); break
            except Exception:
                time.sleep(3)
        out += [x["results"][0]["elevation"] if False else x["elevation"] for x in r["results"]]
        time.sleep(1.2)
    return out


def stats(main):
    cum = [0.0]
    for i in range(1, len(main)): cum.append(cum[-1] + hav(main[i - 1], main[i]))
    n = max(8, int(cum[-1] / 40))
    samp, j = [], 0
    for k in range(n + 1):
        t = cum[-1] * k / n
        while j < len(cum) - 2 and cum[j + 1] < t: j += 1
        f = (t - cum[j]) / ((cum[j + 1] - cum[j]) or 1)
        samp.append((main[j][0] + (main[j + 1][0] - main[j][0]) * f, main[j][1] + (main[j + 1][1] - main[j][1]) * f, t))
    el = elev(samp)
    sm = [sum(el[max(0, i - 2):i + 3]) / len(el[max(0, i - 2):i + 3]) for i in range(len(el))]
    up = sum(max(0, sm[i] - sm[i - 1]) for i in range(1, len(sm)))
    dn = sum(max(0, sm[i - 1] - sm[i]) for i in range(1, len(sm)))
    return dict(len_m=round(cum[-1]), up=round(up), down=round(dn), emin=round(min(sm)), emax=round(max(sm)), prof=[[round(s[2]), round(e)] for s, e in zip(samp, sm)])


def nearest(pl, p):
    return min(range(len(pl)), key=lambda i: hav(pl[i], p))


H = []
# 1. Formica Leo : sentier du cratère Dolomieu (relation OSM), coupé à Formica Leo
d, mains = relation(18113433)
tr = max(mains, key=length)
if hav(tr[0], (55.6845, -21.2251)) > hav(tr[-1], (55.6845, -21.2251)): tr = tr[::-1]
FL = (55.69217, -21.22393)
k = nearest(tr, FL)
H.append(dict(id="dolomieu", day=2, name="Sommet du Piton de la Fournaise : cratère Dolomieu", kind="osm", segs=[dict(role="main", pts=tr)],
              main=tr, pins=[("Parking du Pas de Bellecombe", tr[0]), ("Formica Leo", tr[k]), ("Bord du cratère Dolomieu", tr[-1])],
              official="Sentier officiel du cratère Dolomieu : %s km à l'aller (ONF), voie normale de l'ascension" % str(d.get("official_length", 6200) / 1000).replace(".", ","),
              src="Randopitons et ONF : environ 5 h 30 à 6 h 30 aller-retour pour un marcheur adulte, plus avec un enfant porté",
              level="Exigeant : 12 km aller-retour à plus de 2 200 m, vent et froid, sol de lave",
              links=[("Fiche Randopitons", d.get("url")), ("Relation OSM", "https://www.openstreetmap.org/relation/18113433")]))
# 2. Trou de Fer : sentier du Trou de Fer (relation OSM)
d, mains = relation(6656170)
main = max(mains, key=length)
if hav(main[0], (55.5363, -21.0608)) > hav(main[-1], (55.5363, -21.0608)): main = main[::-1]
H.append(dict(id="troudefer", day=3, name="Sentier du Trou de Fer, depuis Bélouve", kind="osm", segs=[dict(role="main", pts=main)] + [dict(role="more", pts=m) for m in mains if m is not main],
              main=main, pins=[("Gîte de Bélouve", main[0]), ("Fin du tronçon cartographié", main[-1])],
              official="%s km de sentier cartographiés dans OSM (plusieurs tronçons)" % str(round(d["route"]["length"] / 1000, 1)).replace(".", ","),
              src="Decathlon Outdoor : environ 9 km aller-retour, 3 h 15, 230 m de dénivelé", level="Moyen, brouillard après 10 h",
              links=[("Relation OSM", "https://www.openstreetmap.org/relation/6656170")]))
# 3. Roche Merveilleuse : approche depuis Cilaos (routeur piéton) + sentier de découverte (relation OSM)
d, mains = relation(18130434)
loop = max(mains, key=length)
ap = foot((-21.1360, 55.4725), (loop[0][1], loop[0][0]))
ap = [tuple(p) for p in ap]
H.append(dict(id="roche", day=4, name="Roche Merveilleuse, depuis Cilaos", kind="mix", segs=[dict(role="main", pts=ap), dict(role="loop", pts=loop)], main=ap + loop,
              pins=[("Cilaos, centre", ap[0]), ("Belvédère de la Roche Merveilleuse", loop[0])],
              official="Boucle du sentier de découverte : %s km (ONF)" % str(round(d.get("official_length", 2000) / 1000, 1)).replace(".", ","),
              src="Visorando et Decathlon : 2 h à 2 h 20 aller-retour, environ 200 m de dénivelé", level="Facile, retour en partie sur la route",
              links=[("Fiche Randopitons", d.get("url")), ("Relation OSM", "https://www.openstreetmap.org/relation/18130434")]))
# 4. Cascade du Bras Rouge (routeur piéton)
br = [tuple(p) for p in foot((-21.1360, 55.4725), (-21.12885, 55.45527))]
H.append(dict(id="brasrouge", day=5, name="Cascade du Bras Rouge, depuis Cilaos", kind="foot", segs=[dict(role="main", pts=br)], main=br,
              pins=[("Cilaos, centre", br[0]), ("Cascade de Bras Rouge", br[-1])],
              official="Tracé calculé sur les sentiers OSM, à comparer au balisage",
              src="Decathlon Outdoor : 2 h 20 aller-retour", level="Facile à moyen", links=[]))

# 5. Grand Bassin depuis le belvédère de Bois Court (routeur piéton)
gb = [tuple(p) for p in json.load(open(CARTE + r"\gb_path.json"))]  # plus court chemin sur le réseau de sentiers OSM (Overpass), voir grand_bassin_path.py
H.append(dict(id="grandbassin", day=4, name="Grand Bassin depuis Bois Court", kind="osmpath", segs=[dict(role="main", pts=gb)], main=gb,
              pins=[("Belvédère de Bois Court", gb[0]), ("Hameau de Grand Bassin", gb[-1])],
              official="Sentier Grand Bassin (OSM), plus court chemin sur le réseau de sentiers, à comparer au balisage",
              src="Visorando et récits : 4 h 30 à 6 h aller-retour jusqu'au hameau, environ 700 m de dénivelé réel ; avec la cascade du Voile de la Mariée de Grand Bassin, environ 5 h 20", level="Difficile : descente raide à l'aller, remontée continue au retour",
              links=[("Fiche Visorando", "https://www.visorando.com/randonnee-grand-bassin-et-le-voile-de-la-mariee/")]))

allres = []
Z = 14
def tx(lon): return (lon + 180) / 360 * 2 ** Z
def ty(lat):
    r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2 ** Z

for h in H:
    st = stats(h["main"])
    h["stats"] = st
    allp = [p for s in h["segs"] for p in s["pts"]]
    xs = [p[0] for p in allp]; ys = [p[1] for p in allp]
    lon0, lon1 = min(xs) - 0.005, max(xs) + 0.005
    lat0, lat1 = max(ys) + 0.004, min(ys) - 0.004
    x0, x1, y0, y1 = int(tx(lon0)), int(tx(lon1)), int(ty(lat0)), int(ty(lat1))
    W, Hh = (x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256
    im = Image.new("RGB", (W, Hh), (230, 230, 230))
    for x in range(x0, x1 + 1):
        for y in range(y0, y1 + 1):
            fn = TILES + r"\%d_%d_%d.png" % (Z, x, y)
            if not os.path.exists(fn):
                open(fn, "wb").write(get("https://tile.openstreetmap.org/%d/%d/%d.png" % (Z, x, y))); time.sleep(0.4)
            im.paste(Image.open(fn).convert("RGB"), ((x - x0) * 256, (y - y0) * 256))
    im.save(TILES + r"\hike_%s.png" % h["id"])
    h["tile"] = dict(z=Z, x0=x0, y0=y0, w=W, h=Hh)
    for s in h["segs"]: s["pts"] = [[round(p[0], 5), round(p[1], 5)] for p in s["pts"]]
    h["main"] = [[round(p[0], 5), round(p[1], 5)] for p in h["main"]]
    h["pins"] = [(n, [round(p[0], 5), round(p[1], 5)]) for n, p in h["pins"]]
    gpx = ['<?xml version="1.0" encoding="UTF-8"?><gpx version="1.1" creator="reunion-2027" xmlns="http://www.topografix.com/GPX/1/1"><metadata><name>%s</name><desc>Tracé OpenStreetMap (© contributeurs OSM, ODbL). A comparer au balisage sur place.</desc></metadata><trk><name>%s</name><trkseg>' % (h["name"], h["name"])]
    gpx += ['<trkpt lat="%.5f" lon="%.5f"/>' % (p[1], p[0]) for p in h["main"]]
    gpx.append("</trkseg></trk></gpx>")
    open(OUT + r"\gpx\%s.gpx" % h["id"], "w", encoding="utf-8").write("".join(gpx))
    print(h["id"], st["len_m"], "m", "D+", st["up"], "D-", st["down"], st["emin"], "-", st["emax"], "tile", W, Hh)
json.dump(H, open(CARTE + r"\hikes.json", "w", encoding="utf-8"), ensure_ascii=False)
print("ok")

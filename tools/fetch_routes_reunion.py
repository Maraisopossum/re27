import json, math, time, urllib.request, io, os
from PIL import Image
UA = {"User-Agent": "FamilyTripPlanner/1.0 (benoitdegove@gmail.com)"}
C = r"C:\Users\benoi\Documents\Voyages\2027-08_Reunion-31juil-13aout\carte"
P = json.load(open(C + r"\places.json", encoding="utf-8"))
DAYS = {
 1: ["RUN", "niagara", "palmistes", "murat"],
 2: ["murat", "bellecombe", "murat"],
 3: ["murat", "belouve", "murat"],
 4: ["murat", "cilaos"],
 7: ["cilaos", "etangsale", "kelonia", "stgilles"],
 9: ["stgilles", "maido", "stgilles"],
 10: ["stgilles", "stleu", "salines", "stgilles"],
 11: ["stgilles", "stpierre", "grandeanse", "capmechant", "stphilippe", "anse_casc", "ndlaves", "stemarie"],
 12: ["stemarie", "stdenis_jardin", "stemarie"],
 13: ["stemarie", "RUN"],
}
res = {}
for d, ks in DAYS.items():
    co = ";".join("%.5f,%.5f" % (P[k]["lon"], P[k]["lat"]) for k in ks)
    u = "https://router.project-osrm.org/route/v1/driving/" + co + "?overview=full&geometries=geojson&steps=false"
    r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60))
    rt = r["routes"][0]
    legs = [{"from": ks[i], "to": ks[i + 1], "km": round(l["distance"] / 1000, 1), "min": round(l["duration"] / 60)} for i, l in enumerate(rt["legs"])]
    res[d] = {"places": ks, "km": round(rt["distance"] / 1000, 1), "min": round(rt["duration"] / 60), "legs": legs,
              "coords": [[round(x, 5), round(y, 5)] for x, y in rt["geometry"]["coordinates"]]}
    print(d, res[d]["km"], "km", res[d]["min"], "min", [(l["to"], l["km"]) for l in legs], len(res[d]["coords"]), "pts")
    time.sleep(1)
json.dump(res, open(C + r"\routes.json", "w"), ensure_ascii=False)

# tiles z12
Z = 12
def tx(lon): return (lon + 180) / 360 * 2 ** Z
def ty(lat):
    r = math.radians(lat); return (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2 ** Z
lon0, lon1, lat0, lat1 = 55.17, 55.87, -20.83, -21.43
x0, x1 = int(tx(lon0)), int(tx(lon1)); y0, y1 = int(ty(lat0)), int(ty(lat1))
print("tiles", x0, x1, y0, y1, (x1 - x0 + 1) * (y1 - y0 + 1))
W, H = (x1 - x0 + 1) * 256, (y1 - y0 + 1) * 256
img = Image.new("RGB", (W, H), (230, 230, 230))
for x in range(x0, x1 + 1):
    for y in range(y0, y1 + 1):
        fn = os.path.join(C, "tile_%d_%d_%d.png" % (Z, x, y))
        if not os.path.exists(fn):
            req = urllib.request.Request("https://tile.openstreetmap.org/%d/%d/%d.png" % (Z, x, y), headers=UA)
            open(fn, "wb").write(urllib.request.urlopen(req, timeout=30).read()); time.sleep(0.3)
        img.paste(Image.open(fn).convert("RGB"), ((x - x0) * 256, (y - y0) * 256))
img.save(C + r"\base_z12.png")
json.dump({"z": Z, "x0": x0, "y0": y0, "w": W, "h": H}, open(C + r"\base.json", "w"))
print("base", W, H)

"""Reconstruit carte/base_z12.png (fond OSM de l'île) depuis tile.openstreetmap.org, avec cache dans carte/tiles."""
import json, os, time, urllib.request
from PIL import Image

C = r"C:\Users\benoi\Documents\Voyages\2027-08_Reunion-31juil-13aout\carte"
b = json.load(open(C + r"\base.json"))
Z, x0, y0 = b["z"], b["x0"], b["y0"]
nx, ny = b["w"] // 256, b["h"] // 256
os.makedirs(C + r"\tiles", exist_ok=True)
img = Image.new("RGB", (b["w"], b["h"]), (230, 230, 230))
for x in range(x0, x0 + nx):
    for y in range(y0, y0 + ny):
        fn = C + r"\tiles\%d_%d_%d.png" % (Z, x, y)
        if not os.path.exists(fn):
            req = urllib.request.Request("https://tile.openstreetmap.org/%d/%d/%d.png" % (Z, x, y), headers={"User-Agent": "FamilyTripPlanner/1.0 (benoitdegove@gmail.com)"})
            open(fn, "wb").write(urllib.request.urlopen(req, timeout=30).read())
            time.sleep(0.3)
        img.paste(Image.open(fn).convert("RGB"), ((x - x0) * 256, (y - y0) * 256))
img.save(C + r"\base_z12.png")
print("ok", b["w"], b["h"])

# Section « Randonnées » : exécutée par build_reunion3.py (exec) après le chargement des données.
HK = json.load(open(CARTE + r"\hikes.json", encoding="utf-8"))


def hpx(t, lon, lat):
    x = (lon + 180) / 360 * 2 ** t["z"]
    r = math.radians(lat)
    y = (1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2 ** t["z"]
    return ((x - t["x0"]) * 256, (y - t["y0"]) * 256)


def hike_card(h):
    t = h["tile"]
    im2 = Image.open(CARTE + r"\tiles\hike_%s.png" % h["id"]).convert("RGB")
    b = io.BytesIO()
    im2.save(b, "WEBP", quality=70, method=6)
    uri2 = "data:image/webp;base64," + base64.b64encode(b.getvalue()).decode()
    w, hh = t["w"], t["h"]
    fs = max(w, hh) / 34
    svg = '<svg class="hmap" viewBox="0 0 %d %d" role="img" aria-label="Tracé OpenStreetMap : %s"><image href="%s" width="%d" height="%d"/>' % (w, hh, E(h["name"]), uri2, w, hh)
    for sg in h["segs"]:
        pts = " ".join("%.1f,%.1f" % hpx(t, *p) for p in sg["pts"])
        if sg["role"] == "more":
            svg += '<polyline points="%s" class="hmore" vector-effect="non-scaling-stroke"/>' % pts
        else:
            svg += '<polyline points="%s" class="halo" vector-effect="non-scaling-stroke"/><polyline points="%s" class="hline" vector-effect="non-scaling-stroke"/>' % (pts, pts)
    for i, (nm, p) in enumerate(h["pins"]):
        x, y = hpx(t, *p)
        svg += '<circle cx="%.1f" cy="%.1f" r="%.1f" class="hpin %s"/>' % (x, y, fs * 0.45, "a" if i == 0 else "b")
        right = x < w * 0.6
        svg += '<text x="%.1f" y="%.1f" text-anchor="%s" class="plab" style="font-size:%.1fpx">%s</text>' % (x + (fs * 0.8 if right else -fs * 0.8), y + fs * 0.3, "start" if right else "end", fs, E(nm))
    svg += '<text x="%d" y="%d" text-anchor="end" class="attr" style="font-size:%.1fpx">© contributeurs OpenStreetMap</text></svg>' % (w - 8, hh - 8, fs * 0.6)
    pr = h["stats"]["prof"]
    pw, ph, pl_, pb = 360, 110, 38, 18
    dmax = max(p[0] for p in pr) or 1
    emin, emax = min(p[1] for p in pr), max(p[1] for p in pr)
    rng = max(emax - emin, 20)
    pts = " ".join("%.1f,%.1f" % (pl_ + p[0] / dmax * (pw - pl_ - 6), 8 + (ph - 8 - pb) * (1 - (p[1] - emin) / rng)) for p in pr)
    prof = ('<svg class="hprof" viewBox="0 0 %d %d" role="img" aria-label="Profil d\'altitude"><line x1="%d" x2="%d" y1="8" y2="8" class="grid"/><line x1="%d" x2="%d" y1="%d" y2="%d" class="grid"/>'
            '<text x="%d" y="12" text-anchor="end" class="axis">%d m</text><text x="%d" y="%d" text-anchor="end" class="axis">%d m</text>'
            '<polyline points="%s" class="pline"/><text x="%d" y="%d" text-anchor="start" class="axis">0</text><text x="%d" y="%d" text-anchor="end" class="axis">%s km</text></svg>') % (
        pw, ph, pl_, pw - 6, pl_, pw - 6, ph - pb, ph - pb, pl_ - 4, emax, pl_ - 4, ph - pb + 4, emin, pts, pl_, ph - 4, pw - 6, ph - 4, ("%.1f" % (dmax / 1000)).replace(".", ","))
    st = h["stats"]
    L = st["len_m"]
    ar_km = ("%.1f" % (2 * L / 1000)).replace(".", ",")
    nais = round((2 * L / 1000 / 5) * 60 + (st["up"] + st["down"]) / 100 * 10)
    allp = [p for s2 in h["segs"] for p in s2["pts"]]
    c = ((min(p[1] for p in allp) + max(p[1] for p in allp)) / 2, (min(p[0] for p in allp) + max(p[0] for p in allp)) / 2)
    links = "".join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (E(u), E(n)) for n, u in h["links"] if u)
    links += '<a href="https://www.openstreetmap.org/#map=15/%.4f/%.4f" target="_blank" rel="noopener">Ouvrir sur OpenStreetMap</a>' % c
    links += '<a href="https://maraisopossum.github.io/re27/gpx/%s.gpx" target="_blank" rel="noopener">Trace GPX</a>' % h["id"]
    return ('<article class="hike" id="h-%s"><div class="hm">%s</div><div class="hb"><h3>%s</h3><p class="meta">Jour %d · %s</p>'
            '<table class="hs"><tr><th>Aller</th><td>%s km</td><th>Aller-retour</th><td>%s km</td></tr>'
            '<tr><th>Dénivelé à l\'aller</th><td>+%d / −%d m</td><th>Dénivelé au retour</th><td>+%d / −%d m</td></tr>'
            '<tr><th>Altitude</th><td>%d à %d m</td><th>Marche seule, estimée</th><td>≈ %s</td></tr></table>'
            '%s<p class="hn"><b>Durée annoncée par les sources :</b> %s. Niveau : %s.</p><p class="hl">%s</p></div></article>') % (
        h["id"], svg, E(h["name"]), h["day"], E(h["official"]), ("%.1f" % (L / 1000)).replace(".", ","), ar_km, st["up"], st["down"], st["down"], st["up"],
        st["emin"], st["emax"], hm(nais), prof, E(h["src"]), E(h["level"]), links)


hike_html = "".join(hike_card(h) for h in HK)

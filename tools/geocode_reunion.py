import json, time, urllib.parse, urllib.request
UA = {"User-Agent": "FamilyTripPlanner/1.0 (benoitdegove@gmail.com)"}
Q = {
 "RUN": "Aéroport de La Réunion Roland-Garros",
 "niagara": "Cascade Niagara, Sainte-Suzanne, La Réunion",
 "palmistes": "La Plaine-des-Palmistes, La Réunion",
 "murat": "Bourg-Murat, Le Tampon, La Réunion",
 "citevolcan": "Cité du Volcan, Le Tampon",
 "bellecombe": "Pas de Bellecombe, La Réunion",
 "belouve": "Gîte de Bélouve, La Réunion",
 "trou_fer": "Belvédère du Trou de Fer, La Réunion",
 "cilaos": "Cilaos, La Réunion",
 "roche_merv": "Roche Merveilleuse, Cilaos",
 "etangsale": "Étang-Salé-les-Bains, La Réunion",
 "kelonia": "Kélonia, Saint-Leu, La Réunion",
 "stgilles": "Saint-Gilles-les-Bains, La Réunion",
 "ermitage": "L'Ermitage-les-Bains, La Réunion",
 "maido": "Maïdo, Saint-Paul, La Réunion",
 "stpierre": "Saint-Pierre, La Réunion",
 "grandeanse": "Grande Anse, Petite-Île, La Réunion",
 "capmechant": "Cap Méchant, Saint-Philippe, La Réunion",
 "anse_casc": "Anse des Cascades, Sainte-Rose, La Réunion",
 "ndlaves": "Notre-Dame-des-Laves, Sainte-Rose, La Réunion",
 "stdenis_jardin": "Jardin de l'État, Saint-Denis, La Réunion",
 "stemarie": "Sainte-Marie, La Réunion",
 "salines": "Salines-les-Bains, Saint-Paul, La Réunion",
 "stleu": "Saint-Leu, La Réunion",
 "stphilippe": "Saint-Philippe, La Réunion",
 "taibit": "Col du Taïbit, La Réunion",
 "ilet_cordes": "Îlet à Cordes, Cilaos, La Réunion",
}
out = {}
for k, q in Q.items():
    u = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode({"q": q, "format": "json", "limit": 1})
    try:
        r = json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=30))
        out[k] = {"q": q, "lat": float(r[0]["lat"]), "lon": float(r[0]["lon"]), "name": r[0]["display_name"][:80]} if r else None
    except Exception as e:
        out[k] = {"q": q, "err": str(e)}
    print(k, out[k] and (out[k].get("lat"), out[k].get("lon"), out[k].get("name", out[k].get("err"))))
    time.sleep(1.2)
json.dump(out, open(r"C:\Users\benoi\Documents\Voyages\2027-08_Reunion-31juil-13aout\carte\places.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

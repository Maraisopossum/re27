import os, io, base64, json, html, csv
from PIL import Image

V = r"C:\Users\benoi\Documents\Voyages"
OUT = V + r"\2027-08_Reunion-31juil-13aout"
IMGDIR = V + r"\2027-08_Cinq-dernieres\img"
cred = json.load(open(IMGDIR + r"\credits.json", encoding="utf-8"))
E = html.escape
_c = {}


def uri(k, w=900):
    if k not in _c:
        im = Image.open(os.path.join(IMGDIR, k + ".jpg")).convert("RGB")
        im.thumbnail((w, w))
        b = io.BytesIO()
        im.save(b, "JPEG", quality=70, optimize=True, progressive=True)
        _c[k] = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
    return _c[k]


def fix(s):
    return s.replace("\ufffd", "é")


ALT = {"fournaise": "Piton de la Fournaise", "cilaos": "Cirque de Cilaos", "maido": "Maïdo et Mafate", "ermitage": "Lagon de l'Ermitage",
       "lagon": "Lagon des Salines", "humpback": "Baleine à bosse", "kelonia": "Kélonia, Saint-Leu", "langevin": "Cascade de La Réunion",
       "grandanse": "Grande Anse"}

# ---------------------------------------------------------------- vols
FARES = [
    ("Light+", 4041.88, 2319.72, "Pas de bagage en soute (un cabas de 12 kg en cabine par personne), repas chaud"),
    ("Smart", 4274.88, 2546.72, "1 bagage de 23 kg par personne, repas chaud, changement avec frais"),
    ("Flex", 4699.88, 3572.72, "Smart + modification et remboursement sans frais (différence tarifaire en plus)"),
]
STRIP = [("mer 28/07", 3458.48), ("jeu 29/07", 3458.48), ("ven 30/07", 3639.48), ("sam 31/07", 4041.88), ("dim 1/08", 3639.48), ("lun 2/08", 3639.48), ("mar 3/08", 3639.48)]

hist = list(csv.DictReader(open(OUT + r"\suivi\prix.csv", encoding="utf-8")))

# ---------------------------------------------------------------- logements
LODG = [
    {"id": "A", "cls": "r", "name": "Plaine des Cafres, Bourg-Murat", "nights": "1 → 4 août · 3 nuits", "alt": "800 à 1 000 m",
     "why": "Base du volcan : 40 min de route jusqu'au Pas de Bellecombe, 1 h 15 de la forêt de Bélouve. Il fait 5 à 8 °C la nuit en août, le chauffage ou la cheminée comptent plus que la piscine.",
     "opts": [
         ("Gîte de la Fournaise, Le Tampon", "3 chambres, 75 m², chauffage, jusqu'à 14 personnes. Tarif affiché 25 € par personne et par nuit, soit environ 150 € la nuit pour 6.", "https://en.reunion.fr/offers/gite-de-la-fournaise-le-tampon-en-940601", "≈ 150 €/nuit", "Rapport qualité-prix"),
         ("Alicalapa-Tenon, Bourg-Murat", "Chambres d'hôtes 3 étoiles, 5 chambres, table d'hôte, demi-tarif repas enfant de moins de 10 ans. À 2 chambres + 1 pour les ados, il faut prendre presque toute la maison.", "https://resa.sudreuniontourisme.fr/en/accommodation/310830/alicalapa-tenon/details", "≈ 90 €/chambre", "Dîners inclus possibles"),
         ("Côté Volcan, Bourg-Murat", "Maison d'hôtes de 5 chambres au bord de la route du volcan, sentiers à proximité, vélos électriques.", "https://www.gites.fr/gites_la-plaine-des-cafres_38942_en.html", "à demander", "Plus près du volcan"),
     ]},
    {"id": "B", "cls": "r", "name": "Cilaos", "nights": "4 → 7 août · 3 nuits", "alt": "1 200 m",
     "why": "Cirque le plus facile à vivre pour randonner avec les enfants : village, thermes, départs de sentiers à pied. La route d'accès compte plus de 400 virages.",
     "opts": [
         ("Les Terrasses de Cilaos", "Maison de 180 m², 9 personnes, 3 chambres, 1 salle de bains, note 9,2/10 sur gites.fr. La plus spacieuse de la liste.", "https://www.gites.fr/gites_cilaos_38933.html", "≈ 150 à 250 €/nuit", "Le plus de place"),
         ("Gîte Timadam", "Maison de 80 m², 6 personnes, 3 chambres, 1 salle de bains, 9,3/10. Un seul bain pour six : il faut s'organiser.", "https://www.gites.fr/gites_cilaos_38933.html", "≈ 100 à 150 €/nuit", "Le mieux noté en capacité exacte"),
         ("Casamelias « Le Chalet »", "Chalet de 55 m², 6 personnes, 3 chambres, 9,5/10. Petit mais la meilleure note.", "https://www.gites.fr/gites_cilaos_38933.html", "≈ 100 à 150 €/nuit", "Charme"),
         ("La Kaz des Hauts", "94 m², 8 personnes, 3 chambres, 1 salle de bains, 9/10.", "https://www.gites.fr/gites_cilaos_38933.html", "≈ 110 à 170 €/nuit", "Marge de place"),
     ]},
    {"id": "C", "cls": "t", "name": "Saint-Gilles-les-Bains, côte ouest", "nights": "7 → 11 août · 4 nuits", "alt": "niveau de la mer",
     "why": "Côté sec et ensoleillé de l'île en hiver austral : lagon, bateaux, restaurants à pied. Piscine sécurisée et climatisation pour la petite.",
     "opts": [
         ("Ti Kaz Brisants", "Villa de 180 m², 6 personnes, 3 chambres, 3 salles de bains, à 400 m de la plage, note 9,7/10 sur gites.fr. Piscine à confirmer avec le propriétaire.", "https://www.gites.fr/gites_saint-gilles-les-bains_38978_en.html", "à demander", "Meilleur confort sanitaire"),
         ("Villa « Florence »", "200 m², 8 personnes, 3 chambres, longue piscine et vue mer, à 400 m de la plage.", "https://www.gites.fr/gites_saint-gilles-les-bains_38978_en.html", "à demander", "Piscine et vue"),
         ("Villa n°9874, Mediavacances", "Piscine privée, 3 chambres climatisées, salon de 40 m², 2 salles d'eau, lagon à 2 min à pied. Capacité annoncée 4 à 6 : confirmer pour 6.", "https://www.mediavacances.com/locations-vacances/9874", "1 600 à 2 000 €/semaine", "Lagon à pied"),
         ("Villa Tamarin, Saint-Gilles", "Relevé réel du 29/09 pour une autre semaine d'août : 1 209 € les 6 nuits (≈ 200 €/nuit). À revérifier pour vos dates.", "", "≈ 200 €/nuit", "Prix déjà vu"),
         ("Relais de l'Hermitage (hôtel)", "Deux piscines dont une chauffée en hiver, accès direct à la plage de l'Hermitage, chambres familiales jusqu'à 4 personnes, certaines communicantes. Il faut deux chambres.", "https://www.havas-voyages.fr/p-sejour/ile-de-la-reunion-0-relais-de-lhermitage--573429.html", "à demander", "Sans cuisine ni courses"),
     ]},
    {"id": "D", "cls": "t", "name": "Sainte-Marie, près de l'aéroport", "nights": "11 → 13 août · 2 nuits", "alt": "niveau de la mer",
     "why": "Le vol décolle à 08:00 : enregistrement vers 05:00, donc il faut dormir à 15 minutes de Roland Garros.",
     "opts": [
         ("La Maison des Oeillets", "Chambre familiale de 30 m² avec entrée privée, jeux d'enfants, quelques pas de l'aéroport. Salle de bains partagée, capacité 6 à confirmer.", "https://www.bedandbreakfast.eu/en/a/escA9eImsKRU/la-maison-des-oeillets-aeroport-roland-garros", "à demander", "Le plus proche"),
         ("Villa Galabé et Tafia", "Chambres climatisées avec sanitaires privés, jardin tropical, piscine d'eau salée chauffée, à 15 min de l'aéroport.", "https://en.reunion.fr/offers/villa-galabe-et-tafia-sainte-marie-en-4603617/", "à demander", "Piscine"),
         ("Hôtel Tulip Inn Sainte-Clotilde", "Hôtel avec navette aéroport. Prendre deux chambres.", "https://www.expedia.com/Roland-Garros-Airport-Hotels.0-aRUN-0.Travel-Guide-Filter-Hotels", "≈ 2 × 100 €/nuit", "Navette"),
     ]},
]

# ---------------------------------------------------------------- jours
D = [
    dict(n=1, p="r", date="dim 1/08", t="Arrivée et route vers la Plaine des Cafres", base="A", km="70 km · 1 h 30", img=None,
         steps=[("09:00", "Atterrissage à Roland Garros (BF 700). Bagages, retrait du monospace 7 places avec le siège auto réservé à l'avance."),
                ("10:30", "Cascade Niagara à Sainte-Suzanne, à 10 min de l'aéroport, accès libre : 20 min pour se dégourdir les jambes."),
                ("11:15", "RN2 jusqu'à Saint-Benoît, puis la RN3 par la Plaine des Palmistes et le col de Bellevue. Déjeuner à la Plaine des Palmistes."),
                ("14:30", "Installation à Bourg-Murat, courses au supermarché de la Plaine des Cafres ou du Tampon."),
                ("16:00", "Cité du Volcan à Bourg-Murat (1 h 30) : le musée explique la randonnée du lendemain."),
                ("20:00", "Coucher tôt après la nuit dans l'avion.")],
         note="Journée courte exprès. Il fait frais en altitude dès la fin d'après-midi : polaires sorties du bagage cabine."),
    dict(n=2, p="r", date="lun 2/08", t="Piton de la Fournaise et Formica Leo", base="A", km="2 × 25 km · 45 min", img="fournaise",
         steps=[("07:30", "Départ de Bourg-Murat par la route du Volcan, à travers la Plaine des Sables (paysage lunaire)."),
                ("08:30", "Parking du Pas de Bellecombe, 2 311 m. Température 3 à 8 °C : bonnets, coupe-vent, eau, pique-nique."),
                ("09:00", "Escalier vers l'Enclos Fouqué puis boucle du cratère Formica Leo : 4,4 km, environ 170 m de dénivelé, 1 h 40 à 2 h."),
                ("11:30", "Remontée des marches vers le belvédère : plus de 400 marches, la partie dure pour les enfants. Pauses prévues."),
                ("12:30", "Pique-nique au bord de la Plaine des Sables."),
                ("15:00", "Belvédère du Nez de Bœuf : vue sur Bras de la Plaine et Grand Bassin. Retour au gîte.")],
         note="Accès à vérifier la veille : depuis mai 2026 seuls Formica Leo, le sentier Rivals vers le cratère Caubet et le sentier du site d'observation du Dolomieu sont ouverts. Un éboulement de l'escalier a déjà fermé l'enclos. Plan B : Cité du Volcan, cratère Commerson, Plaine des Sables. Avec la petite : porte-bébé rigide, elle marche une partie de la boucle."),
    dict(n=3, p="r", date="mar 3/08", t="Forêt de Bélouve et Trou de Fer", base="A", km="2 × 55 km · 1 h 15", img=None,
         steps=[("07:00", "Départ pour la Plaine des Palmistes puis la route forestière de Bébour et Bélouve."),
                ("08:30", "Marche vers le belvédère du Trou de Fer : environ 9 km aller-retour, 3 h 15, 230 m de dénivelé, par la forêt de tamarins des hauts."),
                ("10:30", "Belvédère : le canyon de la rivière Bras de Caverne, le plus beau avant que les nuages montent (vers 10-11 h)."),
                ("12:30", "Pique-nique dans la forêt de Bébour, tables et sanitaires sur place."),
                ("14:30", "Retour à Bourg-Murat, après-midi de repos. Dîner devant la cheminée.")],
         note="Partir tôt est le seul réglage qui compte : le Trou de Fer est souvent dans le brouillard après midi. Attention : la boucle de la Tamarinaie est signalée impraticable depuis juin 2026, vérifier l'état des sentiers à l'ONF ou à la maison forestière. Avec la petite : porte-bébé, gourde et tour de relais entre adultes."),
    dict(n=4, p="r", date="mer 4/08", t="La route de Cilaos et la Roche Merveilleuse", base="B", km="100 km · 2 h 30", img="cilaos",
         steps=[("09:00", "Départ de Bourg-Murat. RN3 vers Saint-Pierre, puis RN5 vers Saint-Louis (1 h 15)."),
                ("10:30", "La route de Cilaos : 35 km, plus de 400 virages, 1 h 15. Pause à un belvédère au milieu. Médicament contre le mal des transports pour les petits, si besoin."),
                ("12:30", "Arrivée à Cilaos, déjeuner au village, installation, courses (lentilles de Cilaos, vin)."),
                ("15:30", "Roche Merveilleuse : 2 h aller-retour, environ 200 m de dénivelé, balcon sur le cirque. Le dernier tiers du retour se fait sur la route : demi-tour au belvédère avec la petite."),
                ("18:00", "Dîner de gîte.")],
         note="Cilaos est à 1 200 m : comptez 8 à 12 °C la nuit."),
    dict(n=5, p="r", date="jeu 5/08", t="Col du Taïbit ou Bras Rouge, selon les jambes", base="B", km="à pied", img=None,
         steps=[("07:30", "Les deux marches se séparent. Groupe 1 (ados + 1 adulte) : Col du Taïbit, 2 090 m, sentier exigeant d'environ 5 h aller-retour pour 830 m de dénivelé, montée en 2 h 15. Vue sur Marla et le cirque de Mafate."),
                ("08:30", "Groupe 2 (1 adulte + la petite) : cascade du Bras Rouge, 2 h 20 aller-retour."),
                ("13:00", "Retrouvailles pour déjeuner à Cilaos."),
                ("15:30", "Thermes de Cilaos (établissement Irénée Accot) pour récupérer."),
                ("19:00", "Dîner.")],
         note="Si toute la famille veut aller ensemble : la cascade du Bras Rouge convient à tous, et la boucle des cascades (12 km) est une version longue pour les grands. Taïbit : partir très tôt, départ du sentier en bordure du village."),
    dict(n=6, p="r", date="ven 6/08", t="Îlet à Cordes et La Chapelle", base="B", km="à pied", img=None,
         steps=[("08:30", "Sentier de La Chapelle vers l'îlet à Cordes : 4 h aller-retour, niveau moyen, environ 400 m de dénivelé à l'aller et 500 m au retour."),
                ("11:30", "Îlet à Cordes : hameau de lentilles, déjeuner de pays. Si les jambes fatiguent, rentrer en navette ou en taxi plutôt qu'à pied."),
                ("15:30", "Retour à Cilaos, fin de la partie randonnée."),
                ("19:00", "Dernier dîner de gîte, valises à refaire.")],
         note="Dernière journée de marche : choisir sur place entre l'aller-retour complet et un aller simple. L'office de tourisme de Cilaos renseigne sur la navette."),
    dict(n=7, p="t", date="sam 7/08", t="Cilaos, Étang-Salé, Kélonia, Saint-Gilles", base="C", km="120 km · 3 h", img="kelonia",
         steps=[("08:30", "Départ de Cilaos et descente vers Saint-Louis (1 h 15)."),
                ("10:00", "Plage d'Étang-Salé-les-Bains : sable noir volcanique, baignade et pause d'une heure."),
                ("12:30", "Pique-nique, puis la route de Saint-Leu."),
                ("14:00", "Kélonia, observatoire des tortues marines à Saint-Leu : bassins et animaux, 1 h 30. Visite adaptée à la petite."),
                ("16:30", "Arrivée à Saint-Gilles, installation à la villa."),
                ("17:30", "Baignade dans le lagon de l'Ermitage au coucher du soleil.")],
         note="Début de la partie tourisme. En mer, baignade uniquement dans les zones autorisées et surveillées du lagon, des restrictions de baignade s'appliquent sur le reste de la côte ouest."),
    dict(n=8, p="t", date="dim 8/08", t="Lagon de l'Ermitage, masque et tuba", base="C", km="à pied", img="ermitage",
         steps=[("09:00", "Plage de l'Ermitage : eau à 24 °C, lagon peu profond protégé par la barrière de corail."),
                ("10:00", "Masque et tuba pour les 12, 14 et 16 ans, poissons et coraux à moins de 50 m de la plage. Bateau à fond de verre pour la petite."),
                ("12:30", "Déjeuner en bord de mer à Saint-Gilles."),
                ("15:30", "Plage de Boucan Canot, jeux de plage."),
                ("17:30", "Coucher de soleil sur la plage de l'Ermitage.")],
         note="Journée sans voiture : c'est la vraie pause du séjour."),
    dict(n=9, p="t", date="lun 9/08", t="Lever du jour au Maïdo", base="C", km="2 × 35 km · 1 h", img="maido",
         steps=[("05:15", "Départ de Saint-Gilles par la route du Maïdo, via Le Guillaume."),
                ("06:30", "Belvédère du Maïdo, 2 190 m : lever du soleil sur le cirque de Mafate, 5 à 8 °C."),
                ("07:30", "Petite marche sur le sentier du Grand Bord, vue sur Mafate."),
                ("09:30", "Petit-déjeuner, retour à Saint-Gilles."),
                ("12:00", "Déjeuner, repos à la piscine."),
                ("15:30", "Aquarium de La Réunion dans le port de Saint-Gilles, ou Jardin d'Éden à Saint-Gilles-les-Hauts.")],
         note="La route du Maïdo est fermée par mauvais temps, le matin est le moment le plus dégagé. L'aquarium était annoncé en travaux jusqu'en décembre 2026 : vérifier la réouverture."),
    dict(n=10, p="t", date="mar 10/08", t="Baleines et dauphins, parapente à Saint-Leu", base="C", km="2 × 25 km", img="humpback",
         steps=[("08:00", "Port de Saint-Gilles : sortie en mer de 2 h pour voir baleines à bosse et dauphins. Saison de juillet à début octobre, observation jamais garantie."),
                ("11:00", "Retour au port, déjeuner."),
                ("14:00", "Saint-Leu (25 min) : parapente biplace pour les 14 et 16 ans, les autres sur la plage."),
                ("16:30", "Lagon des Salines-les-Bains, baignade et jeux."),
                ("18:00", "Retour à la villa.")],
         note="Bateau « Grand Bleu » ou « Dauphin Safari » : 39 € l'adulte (13 ans et plus), 20 € l'enfant de 1 à 12 ans, soit ≈ 196 € pour six. « Safari marin » d'Aliocha : 42 € dès 12 ans, 32 € en dessous, dès 3 ans, soit ≈ 242 €. Tarifs de plateformes de réservation, à confirmer. Parapente : âge minimum selon l'opérateur, à demander."),
    dict(n=11, p="t", date="mer 11/08", t="Tour du Sud sauvage jusqu'à l'aéroport", base="D", km="≈ 200 km · 5 h de route", img="grandanse",
         steps=[("07:30", "Départ de Saint-Gilles par la RN1 vers Saint-Pierre (1 h). Front de mer et marché de Saint-Pierre."),
                ("10:00", "Grande Anse : grande plage de galets et sable, côté sauvage du Sud."),
                ("11:30", "Cap Méchant et Puits des Anglais à Saint-Philippe : falaises basaltiques et coulées de lave."),
                ("12:30", "Déjeuner à Saint-Philippe."),
                ("14:00", "Anse des Cascades à Sainte-Rose : bassins d'eau douce et pique-nique sous les filaos."),
                ("15:00", "Notre-Dame des Laves à Sainte-Rose : église épargnée par la coulée de 1977."),
                ("16:30", "RN2 par Saint-Benoît jusqu'à Sainte-Marie (≈ 1 h 15)."),
                ("18:00", "Installation à l'hôtel près de l'aéroport.")],
         note="La plus longue journée de conduite. Variante courte : Saint-Pierre, Grande Anse, déjeuner à Saint-Philippe, puis retour par la RN2 vers l'aéroport sans l'Anse des Cascades. Les adolescents peuvent tenir le carnet de bord."),
    dict(n=12, p="t", date="jeu 12/08", t="Saint-Denis et dernière baignade", base="D", km="≈ 30 km", img="langevin",
         steps=[("09:30", "Saint-Denis : Jardin de l'État et Muséum d'histoire naturelle, puis promenade du Barachois en bord de mer."),
                ("12:30", "Déjeuner créole en ville."),
                ("14:30", "Achats : vanille, thé, rhum arrangé pour la famille. Pause à la piscine de l'hôtel."),
                ("18:00", "Valises bouclées, dîner léger."),
                ("19:30", "Coucher : le réveil sonne à 03:45.")],
         note="Rendre la voiture à l'aéroport vers 04:30. Plusieurs loueurs rendent les clés dans une boîte hors horaires : le demander à la réservation. Enregistrement de French bee environ 3 h avant le départ."),
    dict(n=13, p="t", date="ven 13/08", t="Retour, BF 703 à 08:00", base="D", km="15 min", img=None,
         steps=[("05:00", "Enregistrement et dépôt des bagages à Roland Garros."),
                ("08:00", "Décollage de BF 703."),
                ("17:20", "Arrivée à Orly 4, puis le TGV de retour vers Lille.")],
         note="Le vol de jour permet de dormir dans l'avion et d'arriver en fin d'après-midi, reposés pour la rentrée."),
]

# ---------------------------------------------------------------- budget
BUD = [
    ("Vols French bee A/R · 6 personnes", "FARE", "relevé 11/10/2026"),
    ("TGV Lille ↔ Paris, A/R (6 voyageurs)", 600, "estimation"),
    ("Monospace 7 places, 12 jours, siège auto", 1100, "estimation, offres août 2027 pas encore ouvertes"),
    ("Carburant et péages", 150, "estimation"),
    ("Plaine des Cafres · 3 nuits", 540, "≈ 180 €/nuit, estimation"),
    ("Cilaos · 3 nuits", 450, "≈ 150 €/nuit, estimation"),
    ("Saint-Gilles · 4 nuits", 920, "≈ 230 €/nuit, estimation"),
    ("Sainte-Marie · 2 nuits", 400, "≈ 200 €/nuit, 2 chambres, estimation"),
    ("Repas et courses · 13 jours", 1450, "≈ 110 €/jour, estimation"),
    ("Excursions et entrées", 600, "baleines, parapente ×2, Kélonia, Cité du Volcan, thermes, estimation"),
    ("Imprévus, assurance annulation", 300, "estimation"),
]

SVG_PTS = {"RUN": (-20.887, 55.51), "SD": (-20.879, 55.45), "A": (-21.21, 55.57), "B": (-21.13, 55.47), "C": (-21.06, 55.225),
           "PB": (-21.245, 55.71), "MA": (-21.07, 55.39), "TF": (-21.09, 55.58), "KE": (-21.17, 55.285), "AC": (-21.19, 55.82),
           "SP": (-21.34, 55.48), "SPH": (-21.36, 55.77)}
COAST = [(-20.88, 55.45), (-20.89, 55.53), (-20.91, 55.61), (-20.96, 55.65), (-21.03, 55.71), (-21.13, 55.80), (-21.19, 55.83), (-21.36, 55.77),
         (-21.39, 55.62), (-21.34, 55.48), (-21.29, 55.41), (-21.27, 55.34), (-21.17, 55.29), (-21.06, 55.22), (-20.99, 55.27), (-20.93, 55.29),
         (-20.92, 55.33), (-20.88, 55.40)]


def pj(p):
    return (50 + (p[1] - 55.20) * 950, 40 + (-20.85 - p[0]) * 1010)


def island_svg():
    d = "M" + " L".join("%.0f,%.0f" % pj(p) for p in COAST) + " Z"
    pts = ""
    for k, lab, dx, dy, cls in [("A", "A · Plaine des Cafres", 14, 4, "r"), ("B", "B · Cilaos", -12, -8, "r"), ("C", "C · Saint-Gilles", 14, 4, "t"),
                                ("RUN", "D · Aéroport", 14, 4, "t"), ("PB", "Pas de Bellecombe", 10, 18, "m"), ("MA", "Maïdo", -12, -8, "m"),
                                ("TF", "Trou de Fer", 10, -6, "m"), ("KE", "Kélonia", 10, 16, "m"), ("AC", "Anse des Cascades", -138, 4, "m")]:
        x, y = pj(SVG_PTS[k])
        anch = "end" if dx < 0 else "start"
        r = 7 if cls in "rt" else 4
        pts += '<circle cx="%.0f" cy="%.0f" r="%d" class="pt-%s"/><text x="%.0f" y="%.0f" text-anchor="%s" class="lab%s">%s</text>' % (x, y, r, cls, x + (dx if dx > 0 else dx + 0), y + dy, anch, " bold" if cls in "rt" else "", E(lab))
    route = [("C", "SP"), ("SP", "SPH"), ("SPH", "AC"), ("AC", "RUN")]
    rt = " ".join("%.0f,%.0f" % pj(SVG_PTS[k]) for k in ["C", "SP", "SPH", "AC", "RUN"])
    return ('<svg viewBox="0 0 720 620" role="img" aria-label="Schéma de La Réunion avec les quatre bases et le tour du sud" class="isle">'
            '<path d="%s" class="land"/>'
            '<polyline points="%s" class="route"/>%s</svg>') % (d, rt, pts)


def chart_svg():
    W, H, L, B, T = 680, 250, 60, 40, 20
    mx, mn = 4300, 3000
    n = len(STRIP)
    bw = (W - L - 20) / n * 0.62
    out = '<svg viewBox="0 0 %d %d" role="img" aria-label="Total pour six, aller seul, par jour de départ" class="chart">' % (W, H)
    for v in (3000, 3400, 3800, 4200):
        y = T + (H - T - B) * (1 - (v - mn) / (mx - mn))
        out += '<line x1="%d" x2="%d" y1="%.0f" y2="%.0f" class="grid"/><text x="%d" y="%.0f" class="axis" text-anchor="end">%s €</text>' % (L, W - 10, y, y, L - 8, y + 4, f"{v:,}".replace(",", " "))
    step = (W - L - 20) / n
    for i, (lab, v) in enumerate(STRIP):
        x = L + i * step + (step - bw) / 2
        y = T + (H - T - B) * (1 - (v - mn) / (mx - mn))
        h = H - B - y
        cls = "bar hl" if lab == "sam 31/07" else ("bar low" if v == min(s[1] for s in STRIP) else "bar")
        out += '<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" class="%s"/>' % (x, y, bw, h, cls)
        out += '<text x="%.0f" y="%.0f" class="val" text-anchor="middle">%s</text>' % (x + bw / 2, y - 6, f"{v:,.0f}".replace(",", " "))
        out += '<text x="%.0f" y="%d" class="axis" text-anchor="middle">%s</text>' % (x + bw / 2, H - 18, lab)
    return out + "</svg>"


def money(v):
    return f"{v:,.0f}".replace(",", " ") + " €"


# ---------------------------------------------------------------- HTML
css = open(r"C:\Users\benoi\Documents\Voyages\_outils\reunion2.css", encoding="utf-8").read()
js = open(r"C:\Users\benoi\Documents\Voyages\_outils\reunion2.js", encoding="utf-8").read()

days_html = ""
for d in D:
    st = "".join('<li><span class="tm">%s</span><span>%s</span></li>' % (E(t), E(s)) for t, s in d["steps"])
    im = ""
    if d["img"]:
        im = '<figure class="ph"><img src="%s" alt="%s" loading="lazy"><figcaption>%s</figcaption></figure>' % (uri(d["img"]), E(ALT[d["img"]]), E(ALT[d["img"]]))
    days_html += (
        '<details class="day %s" data-p="%s" id="j%d"><summary><span class="dn">%s</span><span class="dt">%s</span><span class="dk">%s</span></summary>'
        '<div class="db"><ol class="steps">%s</ol><div class="dside">%s<p class="note">%s</p></div></div></details>'
    ) % (d["p"], d["p"], d["n"], E(d["date"]), E(d["t"]), E(d["km"]), st, im, E(d["note"]))

lod_html = ""
for L in LODG:
    cards = ""
    for name, desc, url, price, tag in L["opts"]:
        link = '<a href="%s" target="_blank" rel="noopener">Voir la fiche</a>' % E(url) if url else ""
        cards += ('<article class="opt"><div class="oh"><h4>%s</h4><span class="tag">%s</span></div><p>%s</p>'
                  '<div class="of"><strong class="pr">%s</strong>%s</div></article>') % (E(name), E(tag), E(desc), E(price), link)
    lod_html += ('<section class="base %s"><header><span class="bl">%s</span><div><h3>%s</h3><p class="meta">%s · %s</p></div></header>'
                 '<p class="why">%s</p><div class="opts">%s</div></section>') % (L["cls"], L["id"], E(L["name"]), E(L["nights"]), E(L["alt"]), E(L["why"]), cards)

fare_rows = ""
for f, o, r, desc in FARES:
    fare_rows += '<tr><th scope="row">%s</th><td>%s</td><td>%s</td><td><strong>%s</strong></td><td class="l">%s</td></tr>' % (f, money(o), money(r), money(o + r), E(desc))

hist_rows = ""
for r in hist:
    hist_rows += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td><strong>%s</strong></td></tr>' % (
        r["date"], r["fare"], money(float(r["aller_6pax"])), money(float(r["retour_6pax"])), money(float(r["total_6pax"])))

fare_opts = "".join('<option value="%s">%s</option>' % (o + r, f) for f, o, r, _ in FARES)
bud_rows = ""
for lab, v, src in BUD:
    if v == "FARE":
        bud_rows += '<tr><th scope="row">%s</th><td class="num" id="farev">%s</td><td class="l">%s</td></tr>' % (E(lab), money(FARES[1][1] + FARES[1][2]), E(src))
    else:
        bud_rows += '<tr><th scope="row">%s</th><td class="num" data-v="%d">%s</td><td class="l">%s</td></tr>' % (E(lab), v, money(v), E(src))
base_total = sum(v for _, v, _ in BUD if v != "FARE")

credits = "".join('<li>%s : %s, %s, <a href="%s" target="_blank" rel="noopener">Wikimedia Commons</a></li>' % (E(ALT[k]), E(fix(cred[k]["artist"])), E(cred[k]["license"]), E(cred[k]["page"])) for k in ALT if k in cred)

page = f"""<title>La Réunion, été 2027</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700&family=Public+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>{css}</style>
<main class="wrap">
<header class="top">
  <p class="eyebrow">6 voyageurs · Lille → Orly → Saint-Denis</p>
  <h1>La Réunion<br>31 juillet → 13 août 2027</h1>
  <p class="lead">Deux semaines en deux temps : six nuits de randonnée dans les hauts, puis six jours de lagon et de découvertes. Vols French bee relevés le 11 octobre 2026, un suivi quotidien des prix, quatre bases à choisir et un programme jour par jour.</p>
  <div class="strip" aria-label="Frise des 12 nuits">
    <div class="seg r a" style="flex:3"><b>A</b><span>Plaine des Cafres · 3 n</span></div>
    <div class="seg r b" style="flex:3"><b>B</b><span>Cilaos · 3 n</span></div>
    <div class="seg t c" style="flex:4"><b>C</b><span>Saint-Gilles · 4 n</span></div>
    <div class="seg t d" style="flex:2"><b>D</b><span>Aéroport · 2 n</span></div>
  </div>
  <div class="legend"><span class="k r"></span>Partie 1, randonnées (1 → 6 août) <span class="k t"></span>Partie 2, tourisme (7 → 12 août)</div>
</header>

<nav class="nav" aria-label="Sections"><a href="#vols">Vols</a><a href="#suivi">Suivi des prix</a><a href="#logements">Logements</a><a href="#jours">Itinéraires</a><a href="#budget">Budget</a><a href="#todo">À faire</a></nav>

<section id="vols">
  <h2>Les vols</h2>
  <div class="flights">
    <article class="fl"><p class="eyebrow">Aller · samedi 31 juillet</p><p class="big">19:55 <i>→</i> 09:00</p><p>Paris Orly 4 → Saint-Denis, <b>BF 700</b>, A350-1000, direct, 11 h 05. Arrivée dimanche 1er août à 09:00.</p></article>
    <article class="fl"><p class="eyebrow">Retour · vendredi 13 août</p><p class="big">08:00 <i>→</i> 17:20</p><p>Saint-Denis → Paris Orly 4, <b>BF 703</b>, direct, 11 h 20. Arrivée le jour même à 17:20.</p></article>
  </div>
  <p class="lead sm">Les six passagers : 5 « adultes » (tout enfant de 12 ans et plus est facturé adulte) et la petite, tarif enfant de 2 à 11 ans. Prix du 11/10/2026, taxes incluses, pour tous les passagers.</p>
  <div class="tw"><table class="tbl"><thead><tr><th>Tarif</th><th>Aller</th><th>Retour</th><th>Total</th><th class="l">Ce qui est inclus</th></tr></thead><tbody>{fare_rows}</tbody></table></div>
  <div class="callout"><strong>Conseil.</strong> Smart convient : un bagage de 23 kg par personne couvre six valises. Le 31 juillet est le jour le plus cher de la semaine : partir le 28 ou le 29 coûte environ 580 € de moins pour six (tarif Light+, aller seul), et partir le 1er août environ 400 € de moins. Ce sont des dates à comparer si le calendrier des vacances le permet.</div>
  <h3>Aller seul, six personnes, tarif Light+ selon le jour de départ</h3>
  {chart_svg()}
  <p class="cap">Chaque barre est le total pour les six passagers de l'aller seul. Source : moteur de réservation French bee, 11/10/2026.</p>
</section>

<section id="suivi">
  <h2>Suivi quotidien des prix</h2>
  <p class="lead sm">La compétence <code>suivi-prix-reunion</code> relève le calendrier French bee puis le total pour six, l'écrit dans un fichier d'historique et dit si le prix du jour est le plus bas connu. À lancer par « vérifie les prix du vol Réunion ».</p>
  <div class="tw"><table class="tbl"><thead><tr><th>Relevé</th><th>Tarif</th><th>Aller</th><th>Retour</th><th>Total pour 6</th></tr></thead><tbody>{hist_rows}</tbody></table></div>
  <div class="callout"><strong>Ce qui est automatisé.</strong> Le relevé consulte le site de French bee dans le navigateur de l'application Claude. Il ne remplit aucune donnée personnelle et ne réserve jamais. La page du jour : <a href="https://www.frenchbee.com/fr/la-reunion/vol-paris-la-reunion/calendrier-des-tarifs" target="_blank" rel="noopener">calendrier des tarifs French bee</a>. Historique : <code>Documents\\Voyages\\2027-08_Reunion-31juil-13aout\\suivi\\prix.csv</code>.</div>
</section>

<section id="logements">
  <h2>Où dormir</h2>
  <p class="lead sm">Quatre bases, du plus frais au plus chaud : un gîte chauffé près du volcan, une maison à Cilaos, une villa avec piscine à Saint-Gilles, une nuit courte près de l'aéroport. Les descriptions viennent des fiches publiques (gites.fr, Réunion Tourisme, plateformes de location). <b>Aucune disponibilité ni aucun prix pour août 2027 n'a pu être confirmé</b> : les tarifs ci-dessous sont des fourchettes à vérifier auprès de chaque propriétaire.</p>
  {island_svg()}
  <p class="cap">Schéma approximatif de l'île : points A à D = les quatre bases, trait = tour du Sud du 11 août.</p>
  {lod_html}
</section>

<section id="jours">
  <h2>Programme jour par jour</h2>
  <div class="filters" role="group" aria-label="Filtrer les jours"><button class="chip on" data-f="all">Tous les jours</button><button class="chip" data-f="r">Randonnées</button><button class="chip" data-f="t">Tourisme</button><button class="chip" id="openall">Tout déplier</button></div>
  {days_html}
</section>

<section id="budget">
  <h2>Budget</h2>
  <p class="lead sm">Les vols viennent de relevés réels. Le reste est une estimation raisonnable à remplacer par les devis au fil des réservations.</p>
  <label class="sel" for="farepick">Tarif de vol <select id="farepick">{fare_opts}</select></label>
  <div class="tw"><table class="tbl bt"><thead><tr><th>Poste</th><th>Montant</th><th class="l">Base</th></tr></thead><tbody>{bud_rows}</tbody><tfoot><tr><th scope="row">Total</th><td class="num" id="total">0</td><td class="l">hors souvenirs et extras</td></tr></tfoot></table></div>
</section>

<section id="todo">
  <h2>À faire et à vérifier</h2>
  <ul class="todo">
    <li><b>Vols :</b> décider de la date de départ (31/07 ou 28/07 ou 1/08) et du tarif ; la billetterie French bee confirme les prix au moment de l'achat.</li>
    <li><b>Voiture :</b> les offres pour août 2027 ne sont pas encore en ligne. Prendre un monospace 7 places avec siège auto pour la petite, retour de nuit possible.</li>
    <li><b>Volcan :</b> consulter l'arrêté préfectoral et les infos ONF la veille du 2 août.</li>
    <li><b>Matériel :</b> porte-bébé de randonnée, polaires et bonnets pour 2 000 m, chaussures de marche, masque et tuba, crème solaire.</li>
    <li><b>Mer :</b> baignade uniquement dans les zones autorisées du lagon.</li>
    <li><b>Réservations :</b> logements (A à D), bateau baleines, parapente, retrait de la voiture à l'aéroport.</li>
  </ul>
  <p class="cap">Photos : <a href="#cred">crédits</a>.</p>
  <details id="cred"><summary>Crédits photo</summary><ul class="cred">{credits}</ul></details>
</section>
</main>
<script>const BASE={base_total};{js}</script>
"""
open(OUT + r"\index.html", "w", encoding="utf-8").write(page)
print(len(page) // 1024, "KB")

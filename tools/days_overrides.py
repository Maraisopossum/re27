# Ajustements du programme (exécuté par build_reunion3.py après les corrections de base).
NAME["boiscourt"] = "Belvédère de Bois-Court"
NAME["tunnels"] = "Sainte-Rose, tunnels de lave"
TUN = ("Tunnels de lave guidés (tunnelsdelave.re, formulaire, 06 92 16 20 90) : « 20 000 lieues sous les laves », 2 à 3 h sous terre, dès 7 ans, "
       "55 € l'adulte (12 ans et plus) et 40 € l'enfant de moins de 12 ans, casque et lampe fournis, pantalon long et chaussures fermées. Tarifs et lieu de rendez-vous à confirmer à la réservation.")

# Jour 2 : objectif randonnée complète
D[1]["note"] = ("Objectif : la randonnée complète jusqu'au bord du cratère Dolomieu, aller-retour par le même sentier. " + D[1]["note"].replace("Plan B si fermé", "Si l'accès est restreint, plan B"))

# Jour 4 : Grand Bassin et Voile de la Mariée, puis route de Cilaos
D[3].update(t="Grand Bassin et Voile de la Mariée, puis Cilaos", km="59 km · à pied 9 km", img=None, steps=[
    ("07:00", "Départ de Bourg-Murat pour le belvédère de Bois-Court, 5,5 km, 11 min. Sacs de la veille : 2 litres d'eau par personne, pique-nique, sandales pour la cascade."),
    ("07:30", "Descente vers le hameau de Grand Bassin par le sentier Grand Bassin : 4,4 km et environ 760 m de descente, 2 h à 2 h 30 avec la petite en porte-bébé. Le hameau n'a pas de route."),
    ("10:00", "Hameau de Grand Bassin, puis le bassin et la cascade du Voile de la Mariée en contrebas (environ 30 min de plus selon les récits). Pique-nique et pause au bord de l'eau."),
    ("11:30", "Remontée par le même sentier : environ 840 m de montée continue, 2 h 30 à 3 h. C'est la partie dure : relais du porte-bébé toutes les 30 min."),
    ("14:30", "Retour au belvédère de Bois-Court. Total environ 9 km à pied, 5 à 6 h 30 avec les pauses."),
    ("15:00", "Route de Cilaos par Entre-Deux et Saint-Louis : 54 km, le calculateur annonce 1 h 15, prévoir 2 h dans les virages."),
    ("17:30", "Arrivée à Cilaos, installation, courses et dîner tôt.")],
    note=("Journée la plus exigeante après le volcan : le même effort que le Dolomieu en montée, 840 m en fin de randonnée. Partir tôt pour éviter la chaleur et les averses, et demi-tour au hameau sans la cascade si la petite ou quelqu'un fatigue. "
          "Attention : un autre Voile de la Mariée existe à Salazie, sur la route D48 (balade de 2,4 km aller-retour, sentier glissant, fermeture signalée après un cyclone) : voir le jour 12. Source des durées : Visorando et récits de randonneurs."))

# Jour 5 : Bras Rouge le matin, Roche Merveilleuse l'après-midi
D[4].update(t="Cascade du Bras Rouge et Roche Merveilleuse", steps=[
    ("08:30", "Départ à pied de Cilaos vers la cascade du Bras Rouge : environ 3,8 km par le sentier, 2 h 20 aller-retour, 330 m de descente à l'aller et la même remontée au retour."),
    ("11:00", "Pique-nique devant la cascade, on se mouille les pieds."),
    ("12:30", "Remontée vers Cilaos, la petite en porte-bébé, déjeuner au village."),
    ("14:30", "Roche Merveilleuse : approche depuis le village et boucle du sentier de découverte, environ 2 h aller-retour, 270 m de montée. Belvédère sur le cirque."),
    ("17:00", "Thermes de Cilaos (établissement Irénée Accot) ou courses du soir, lentilles et vin de Cilaos.")],
    note="Toute la famille marche ensemble, sans groupes séparés. Le col du Taïbit est écarté. Journée de 4 h 20 de marche en deux fois : lendemain de Grand Bassin, on peut sauter la Roche Merveilleuse et aller aux thermes.")

# Jour 10 : sans parapente
D[9].update(steps=[
    ("08:00", "Port de Saint-Gilles : sortie en mer de 2 h pour voir baleines à bosse et dauphins. Saison de juillet à début octobre, observation jamais garantie."),
    ("11:00", "Retour au port, déjeuner."),
    ("14:00", "Saint-Leu (16 km) : promenade en bord de mer et glace en ville, plage pour les ados."),
    ("16:30", "Lagon des Salines-les-Bains, baignade et jeux."),
    ("18:00", "Retour à la villa.")],
    t="Baleines et dauphins, lagon des Salines",
    note="Bateau « Grand Bleu » ou « Dauphin Safari » : 39 € l'adulte (13 ans et plus), 20 € l'enfant de 1 à 12 ans, soit ≈ 196 € pour six. « Safari marin » d'Aliocha : 42 € dès 12 ans, 32 € en dessous, dès 3 ans, soit ≈ 242 €. Tarifs de plateformes de réservation, à confirmer. Pas de parapente au programme.")

# Jour 11 : Sud sauvage et tunnels de lave
D[10].update(t="Sud sauvage et tunnels de lave jusqu'à l'aéroport", km="170 km · 3 h 05", steps=[
    ("07:30", "Départ de Saint-Gilles par la RN1 vers Saint-Pierre (52 km). Pas d'arrêt long : la route est la plus lente du séjour."),
    ("09:30", "Cap Méchant à Saint-Philippe (29 km après Saint-Pierre) : falaises basaltiques et coulées de lave."),
    ("11:00", "Saint-Philippe (7 km plus loin) : déjeuner, jardin et marché selon le jour."),
    ("13:00", "Sainte-Rose (27 km depuis Saint-Philippe), rendez-vous des tunnels de lave vers 14:00 (heure et lieu à confirmer à la réservation)."),
    ("14:00", "Tunnels de lave guidés pour cinq : un parent et les trois ados, 2 à 3 h sous terre, dès 7 ans, la petite n'est pas admise."),
    ("14:00", "Pendant ce temps, l'autre parent et la petite : Anse des Cascades (2 km), bassins d'eau douce et pique-nique, puis l'église Notre-Dame des Laves épargnée par la coulée de 1977."),
    ("17:00", "Retrouvailles, RN2 par Saint-Benoît jusqu'à Sainte-Marie (54 km, 1 h)."),
    ("18:30", "Installation à l'hôtel près de l'aéroport.")],
    note=(TUN + " C'est la seule activité du séjour qui sépare la famille, à cause de l'âge minimum : il faut choisir quel parent reste avec la petite. Journée de 170 km, 3 h 05 de route sans les arrêts."))

# Jour 12 : Saint-Denis
D[11].update(t="Saint-Denis : jardin, musées, mosquée et front de mer", km="26 km · 31 min", img="langevin", steps=[
    ("09:00", "Jardin de l'État (13 km depuis Sainte-Marie) : jardin botanique du XVIIIe siècle, allées de palmiers, bassins, aire de jeux pour la petite. Ouvert de 7 h à 18 h."),
    ("10:30", "Muséum d'histoire naturelle, dans le jardin, ancien bâtiment du Conseil colonial : mardi à dimanche, 9 h 30 à 17 h 30, environ 2 € l'adulte."),
    ("11:45", "Rue de Paris : cases créoles, cathédrale, mosquée Noor-e-Islam à voir de l'extérieur avec son minaret blanc, temple tamoul."),
    ("12:30", "Déjeuner créole en centre-ville : cari, rougail, samoussas."),
    ("14:00", "Musée Léon Dierx, dans l'ancien palais épiscopal de la rue de Paris : art moderne, Gauguin, Renoir, Picasso. Mardi à dimanche, 9 h 30 à 17 h, environ 2 €, gratuit le premier dimanche du mois."),
    ("15:30", "Le Barachois : esplanade en bord de mer, canons tournés vers le large, glace et jeux pour les enfants."),
    ("17:30", "Retour à l'hôtel de Sainte-Marie, dîner léger, valises bouclées.")],
    note=("Musées fermés le lundi, jour d'horaires de sources à vérifier avant d'y aller. Le jeudi 12 août tombe un jour d'ouverture. Option si la famille préfère la nature : le Voile de la Mariée de Salazie, sur la D48 à 1 h de Sainte-Marie, balade de 2,4 km aller-retour, sentier glissant, fermeture signalée après un cyclone, à confirmer. "
          "Coucher à 19 h 30 : le réveil sonne à 03 h 45, rendre la voiture à l'aéroport vers 04 h 30, enregistrement environ 3 h avant le départ."))

# Budget : parapente remplacé par les tunnels de lave
BUD[9] = ("Excursions et entrées", 700, "baleines ≈ 196 €, tunnels de lave 4 × 55 €, Kélonia, Cité du Volcan, thermes, estimation")

# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Stack

Un seul fichier HTML/CSS/JS statique (index.html), publié en Artifact claude.ai. Générateur Python (`Documents\Voyages\_outils\build_reunion2.py`) qui intègre photos et carte en data URI. Scripts externes uniquement depuis cdnjs ; aucune image ni requête réseau autre que `data:` ne passe dans l'Artifact.

## Users

Les deux parents d'une famille de six qui préparent puis vivent un voyage à La Réunion (31 juillet → 13 août 2027). Ils décident à deux sur ordinateur, puis consultent le programme du jour sur téléphone, en voiture ou en randonnée, au soleil. Les trois ados (12, 14, 16 ans) lisent aussi la page.

## Product Purpose

Une page de voyage unique qui porte la décision (vols relevés, tarifs, quatre bases de logement, budget) et le déroulé jour par jour avec itinéraires routiers réels. Réussite : réserver vols et logements sans rouvrir dix onglets, puis suivre la journée sans réfléchir.

## Positioning

Une page de famille, pas un site de voyagiste : prix relevés et datés, suivi quotidien des prix, itinéraires tracés sur la vraie carte OpenStreetMap.

## Operating Context

Deux semaines en deux temps : partie 1 randonnées (1 → 6 août, Plaine des Cafres puis Cilaos), partie 2 tourisme (7 → 12 août, Saint-Gilles puis près de l'aéroport). Vol aller sam. 31/07 19:55, retour ven. 13/08 08:00. Voiture : monospace 7 places. Altitudes de 0 à 2 300 m : 3 à 28 °C.

## Capabilities and Constraints

- Contenu existant à conserver : vols, tableau des tarifs, graphique des jours de départ, suivi des prix (prix.csv), logements A à D, 13 jours, budget interactif, à faire, crédits photo.
- Les prix de logements d'août 2027 ne sont pas confirmés : ne jamais les présenter comme des relevés.
- Portée du design system : cette page La Réunion seulement.
- Contraintes Artifact : thèmes clair et sombre, 400 px de large sans défilement horizontal, pas d'impression, liens externes en nouvel onglet.

## Brand Commitments

Aucun nom ni logo. Français, ton direct, sans formules creuses.

## Evidence on Hand

Photos Wikimedia Commons déjà utilisées (crédits dans la page). Relevés French bee du 11/10/2026 dans `suivi\prix.csv`. Pas de photos prises par la famille.

## Product Principles

1. Les chiffres sont datés et sourcés ; une estimation est toujours marquée comme telle.
2. Le programme du jour se lit en dix secondes sur téléphone.
3. La carte montre les trajets réellement roulés, pas un schéma.
4. Une page, deux temps : randonnée et tourisme se distinguent d'un coup d'œil.

## Accessibility & Inclusion

Lisible en plein soleil, contraste AA minimum, cibles tactiles confortables, mouvement réduit respecté.

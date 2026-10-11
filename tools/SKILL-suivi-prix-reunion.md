---
name: suivi-prix-reunion
description: Relève chaque jour le prix des vols French bee Paris-Orly ↔ La Réunion pour le voyage de la famille (aller sam. 31 juillet 2027 au soir, retour ven. 13 août 2027), enregistre l'historique et dit si c'est le moment le moins cher pour acheter. À utiliser pour "vérifie les prix du vol Réunion", "suivi prix Réunion", "est-ce le bon moment pour réserver", ou quand une tâche planifiée quotidienne l'invoque.
---

# Suivi des prix du vol Réunion (French bee)

Voyage : 6 personnes (5 « adultes » dont les 3 ados et l'enfant de 12 ans, + 1 enfant de 2 à 11 ans), Orly ↔ Saint-Denis (RUN), aller **samedi 31 juillet 2027** (BF 700, 19:55 → 09:00 le lendemain), retour **vendredi 13 août 2027** (BF 703, 08:00 → 17:20). Historique : `C:\Users\benoi\Documents\Voyages\2027-08_Reunion-31juil-13aout\suivi\prix.csv`.

Règle absolue : consultation seulement. Ne jamais remplir de données personnelles, ne jamais payer, ne jamais créer de compte. Refuser les cookies non essentiels.

## Étape 1 : calendrier (rapide, par adulte, tarif Light)

Navigateur intégré (outils `mcp__Claude_Browser__*`) :

1. `navigate` vers `https://www.frenchbee.com/fr/la-reunion/vol-paris-la-reunion/calendrier-des-tarifs`, cliquer « Tout refuser » sur le bandeau cookies.
2. `javascript_tool` : attendre 3 s, puis `document.querySelector('#edit-instant-search-calendar-travel-type-r')` → `.click()` + `dispatchEvent(new Event('change',{bubbles:true}))` (le calendrier démarre en « aller simple » tant qu'on ne fait pas ça).
3. Cliquer le bouton d'histogramme du mois `jui` (`.calendar__histogram-button`, filtrer par `textContent`), puis la case **31** dans `.calendar__dates-departure td` (clic sur le `<a>`). Lire le prix aller affiché.
4. Le calendrier retour `.calendar__dates-return` s'active et affiche août 2027 : lire les prix du 12, 13 et 14. Cliquer le **13** puis lire « Prix total (TTC/adulte) » dans `.calendar__form-block`.
5. Noter aussi le prix de l'aller pour le 30/07, 1/08 et le prix mensuel du bouton `aout`, pour repérer des dates voisines moins chères.

## Étape 2 : total pour 6 (Light+, Smart, Flex)

1. Sur la même page, régler les compteurs du formulaire du calendrier : adultes 5, enfants 2-11 ans 1 (champs `input[type=number]` visibles, + `instant_search_calendar_passenger_ADT=5` et `..._CHD=1`), puis cliquer `input[value=Continuer]`. On arrive sur `mytrip.frenchbee.com/booking/availability/0` (compter 15 s de chargement).
2. `get_page_text` : la bande de jours donne le total « pour tous les passagers » par jour d'aller. Cliquer l'onglet `ECO` (bouton dont le texte commence par ECO) pour lire les 3 tarifs de l'aller : Light+ / Smart / Flex.
3. Sélectionner le tarif Smart avec un vrai clic (`find` « 4 274 » ou le prix lu, puis `computer left_click` sur la ref ; un clic JS ne suffit pas). Une fenêtre « Garder Bee Smart » apparaît : cliquer dessus. On passe aux vols retour (`availability/1`) : même méthode, onglet ECO, lire les 3 tarifs du retour.
4. S'arrêter là. Ne pas aller aux informations passagers.

Totaux = aller + retour pour chaque famille de tarif.

## Étape 3 : enregistrer et conclure

```
python C:\Users\benoi\.claude\skills\suivi-prix-reunion\log_price.py --fare Smart --out <aller> --ret <retour> --light-adulte <prix calendrier>
```
(répéter pour Light+ et Flex). Le script affiche « NOUVEAU PLUS BAS » ou l'écart avec le meilleur prix connu. `--report` résume l'historique.

Réponse à l'utilisateur, en français, courte : prix du jour pour les 3 tarifs, écart avec la veille et avec le plus bas connu, dates voisines moins chères (ex. aller 28/07 ou 1/08), recommandation (acheter / attendre). Relevé initial du 11/10/2026 : Smart 6 821,60 €, Light+ 6 361,60 €, Flex 8 272,60 €.

Si un sélecteur a changé, repartir de `read_page` / `find` : le principe reste calendrier d'abord, moteur de réservation ensuite.

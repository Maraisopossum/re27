---
name: Roadbook Réunion
description: Design system de la page de voyage La Réunion 2027 : un carnet de route de rallye-raid, jaune signalisation, encre noire, règles épaisses, kilométrage réel et carte OpenStreetMap.
colors:
  paper: "#f1f4f5"
  panel: "#ffffff"
  ink: "#0f1417"
  muted: "#46545b"
  hair: "#c9d2d6"
  yellow: "#ffd23f"
  lava: "#c43d08"
  lagon: "#00707c"
  good: "#1f7a3f"
typography:
  display:
    fontFamily: "Barlow Condensed"
    fontSize: 6rem
    fontWeight: 700
    lineHeight: 1.02
  headline:
    fontFamily: "Barlow Condensed"
    fontSize: 2.5rem
    fontWeight: 700
    lineHeight: 1.02
  title:
    fontFamily: "Barlow Condensed"
    fontSize: 1.4rem
    fontWeight: 700
    lineHeight: 1.1
  body:
    fontFamily: "Barlow"
    fontSize: 1.0625rem
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Barlow Condensed"
    fontSize: 0.9rem
    fontWeight: 600
rounded:
  none: 0px
spacing:
  xs: 0.4rem
  sm: 0.8rem
  md: 1rem
  lg: 2rem
  xl: 3.8rem
components:
  day-strip:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.ink}"
    typography: "{typography.title}"
    rounded: "{rounded.none}"
  day-number-hike:
    backgroundColor: "{colors.lava}"
    textColor: "{colors.panel}"
    typography: "{typography.headline}"
    width: 3.6rem
  day-number-tourism:
    backgroundColor: "{colors.lagon}"
    textColor: "{colors.panel}"
    typography: "{typography.headline}"
    width: 3.6rem
  tulip-table-head:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    typography: "{typography.label}"
  callout:
    backgroundColor: "{colors.yellow}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    padding: 0.7rem 1rem
  day-chip:
    backgroundColor: "{colors.panel}"
    textColor: "{colors.ink}"
    typography: "{typography.label}"
    size: 2.5rem
---

# Design System: Roadbook Réunion

## Overview

**Creative North Star: « Le carnet de route »**

La page se lit comme un roadbook de rallye-raid tenu dans une voiture : une couverture jaune signalisation avec la vraie carte de l'île, puis des bandes numérotées par jour où chaque étape porte son kilométrage cumulé. Tout est à angle droit, encadré d'encre noire, sans ombre ni arrondi. La carte OpenStreetMap et les tracés routiers sont le contenu principal, la typographie condensée sert de signalisation.

Le système sépare deux temps d'un voyage par la couleur et jamais par la forme : lava orange pour la randonnée, turquoise lagon pour le tourisme.

**Key Characteristics:**
- Couverture jaune pleine largeur, carte à droite, titre en capitales condensées à gauche.
- Règles noires de 6 px pour ouvrir chaque section, 2 px pour encadrer les objets.
- Chiffres (jours, km, prix, horaires) toujours en condensé gras, tabulaires.
- Mode clair « jour » et mode sombre « nuit », jaune de couverture identique dans les deux.

## Colors

Un jaune de signalisation, une encre noire, un papier blanc froid, et deux couleurs d'état de voyage.

### Primary
- **Jaune de route** (`#ffd23f`): couverture, encadrés d'avertissement, surlignage de départ et d'arrivée dans les tableaux.
### Secondary
- **Lava** (`#c43d08`): partie randonnée, jours 1 à 6, bases A et B, tracés correspondants.
- **Lagon** (`#00707c`): partie tourisme, jours 7 à 13, bases C et D, tracés correspondants.
### Neutral
- **Papier froid** (`#f1f4f5`): fond de page.
- **Panneau** (`#ffffff`): bandes de jour et tableaux.
- **Encre** (`#0f1417`): texte, règles, en-têtes de tableaux.
- **Gris routier** (`#46545b`): texte secondaire.
- **Trait fin** (`#c9d2d6`): filets entre lignes.
- **Vert validé** (`#1f7a3f`): barres de prix les plus basses.

Mode nuit : papier `#0c1215`, panneau `#141c20`, encre `#eef2f3`, lava `#ff8a50`, lagon `#4fd1dd`, gris `#a3b3b9`. Le jaune de couverture et les cartes restent inchangés.

**The Two-Paints Rule.** Lava et lagon n'apparaissent que pour dire randonnée ou tourisme. Aucun autre usage décoratif.

**The No-Cream Rule.** Le papier est blanc froid. Jamais de crème, de sépia ni de parchemin.

## Typography

**Display Font:** Barlow Condensed, repli Arial Narrow.
**Body Font:** Barlow, repli Helvetica Neue, Arial.

- **Display** (700, jusqu'à 6rem, capitales): titre de couverture.
- **Headline** (700, 2.5rem, capitales): titres de section, posés sous une règle noire de 6 px.
- **Title** (700, 1.4rem): titres de jour et de logement.
- **Body** (400, 1.0625rem, interligne 1.55): texte courant, mesure de 44 rem au plus.
- **Label** (600, 0.9rem, capitales, interlettrage 0.07em): dates, en-têtes de tableaux, filtres.

**The Odometer Rule.** Tout nombre qui se compare (km, prix, heures) utilise le condensé gras avec chiffres tabulaires.

## Layout

Colonne de 72 rem au plus, gouttière de 1 rem minimum. La couverture est une grille à deux colonnes (texte 5fr, carte 6fr) qui passe en une colonne sous 860 px. La règle des nuits (A à D) clôt la couverture. Les bandes de jour s'ouvrent en deux colonnes (étapes et tableau à gauche, carte et photo à droite).

## Elevation & Depth

Aucune ombre. La profondeur vient de l'encadrement : filet de 2 px autour des objets, règle de 6 px au-dessus des sections, inversion encre sur papier pour les en-têtes de tableau. Le focus clavier est un contour jaune doublé d'un anneau d'encre.

## Shapes

Angles droits partout, rayon nul. Les puces de jour sont des carrés avec une base de 6 px colorée en lava ou lagon. Les marqueurs de carte sont des ronds blancs cerclés, seule exception, issue de la cartographie.

## Components

### Bande de jour
Bloc encadré de 2 px : à gauche une plaque numérotée (3.6rem) colorée lava ou lagon, au centre le titre, à droite la date et la distance du jour. S'ouvre sur le tableau de tulipes, les horaires, la carte du jour, une photo et une note.

### Tableau de tulipes
En-tête encre sur papier, une ligne par étape avec un glyphe dessiné (départ : cible, étape : losange, arrivée : drapeau), distance de l'étape et cumul en condensé gras. Départ et arrivée surlignés en jaune atténué.

### Carte
Fond OpenStreetMap standard (zoom 12) intégré à la page, tracés OSRM en 4.5 px sur un halo blanc de 8 px, couleur du temps (lava ou lagon), marqueurs de bases en pastilles lettrées A à D. Attribution OpenStreetMap toujours visible.

### Puce de jour
Carré de 2.5 rem, base colorée, surligne le trajet du jour sur la carte de couverture.

### Encadré
Fond jaune, encre noire, filet de 2 px. Pour les conseils et mises en garde.

## Do's and Don'ts

### Do:
- **Do** montrer les kilomètres et durées réels calculés sur OpenStreetMap, avec leur source.
- **Do** marquer toute estimation comme estimation et toute donnée datée avec sa date.
- **Do** garder la carte lisible au soleil : fond clair, tracés épais, halo blanc.

### Don't:
- **Don't** utiliser d'arrondis, d'ombres portées, de dégradés ou de verre.
- **Don't** ajouter une étiquette au-dessus d'un titre ; le titre porte son poids.
- **Don't** colorer en lava ou lagon pour autre chose que randonnée et tourisme.
- **Don't** présenter une fourchette de logement comme un tarif relevé.

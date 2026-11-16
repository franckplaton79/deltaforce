# État du manuel — 15 novembre 2026

## Ce qui est livré
- **30 pages HTML**, français intégral, aucun PDF.
- **1 008 fiches** d'objets, chacune avec icône JPG, nom français, nom d'origine, catégorie, grade, description, poids ou grille, valeur et valeur par case.
- Couverture de traduction : **1 008/1 008 noms**, **1 008/1 008 descriptions**.
- **89 007 mots**, 37 Mo, 31 JPG d'ambiance, 1 008 JPG d'objets, **21 mémos audio MP3**, **46 blocs de sources datées**.
- Audit automatique sur les 30 pages : **0 problème** (balises équilibrées, liens internes, fichiers référencés). `node --check js/site.js` passe.

## Pages ajoutées aux deux dernières étapes
- `butin.html` — valeur par case calculée depuis la base, onze tableaux, seuil de décision communautaire.
- `munitions.html` — sept niveaux de pénétration, table des cinq issues, répartition réelle des 71 munitions par niveau, cinq munitions d'Aurora.

## Enrichissements de la dernière passe
- `balistique.html` : tableau des 17 calibres avec les niveaux réellement atteints par famille.
- `reglages.html` : détail des réglages PC option par option, avec la raison de chaque valeur et un avertissement sur leur origine communautaire.
- `audio.html` : deux mémos de plus (munitions, valeur par case du butin).

## Dernière passe (15 nov., suite)
- `sorties.html` : section « sortir en solo » (quatre réflexes, sorties sans sac, piège du dernier quart d’heure).
- `progression.html` : tableau des quatre compteurs + jetons d’arme + plafond hebdomadaire.
- `index.html` : trois idées reçues et sommaire par sujet.
- 2 JPG, 2 mémos audio, 2 blocs de sources (42 au total).

## Passe du 15 nov. (soir)
- `db.html` : tableau des sept pages avec les champs manquants, méthode de recoupement en trois étapes, section outils communautaires et projets open source.
- `operateurs.html` : tableau comparatif trio / solo par opérateur.
- 2 JPG, 2 mémos audio, 2 blocs de sources (44 au total), petite feuille de style `ol.steps`.

## Passe du 15 nov. (nuit)
- `saison.html` : « quatre ajouts d’Aurora qu’on remarque une semaine trop tard » (plans de chargement niv. 35, pas de tir 2.0, remise à zéro des missions, accessoires Haavk limités).
- `data/items_fr.json` : **625 descriptions réécrites** (433 accessoires, 93 équipements, 30 consommables, 69 collectibles) pour sortir des gabarits ; variantes, conseil d’usage, valeurs formatées ; 86 corrections de détail.
- 2 mémos audio (plans de chargement, missions remises à zéro), 1 bloc de sources (45 au total).

## Passe finale du 15 nov.
- `plan.html` : « comment lire ce manuel » (trois moments d’usage, trois niveaux de confiance) + figure table de planification.
- `conseils.html` : tableau de croisement des trois guides vidéo, avec les points d’accord et les divergences datées + figure écoute terrain.
- `tools/make_db.py` : libellés de catégories lisibles dans les filtres (« canons » au lieu de « canon ») et tableau « les menues options du menu » sur la page Armes.
- 2 JPG, 2 mémos audio (19 au total).

## Dernière passe (15 nov., actualité)
- `saison.html` : tableau des neuf activités Brakkesh (10–26 nov.) et des trois monnaies à ne pas confondre, dates du 17 et du 19 novembre, conditions de Supercritical (18 déc., niv. 30, 600 000 Tekniq).
- `db.html` : section « ce que la base ne contient pas encore » — AN-94, cinq munitions d’Aurora, accessoires Haavk, figurine Phantom Blade Zero : décrits dans les pages, pas dans les fiches, faute de valeurs publiées.
- 2 JPG, 2 mémos audio (21 au total), 1 bloc de sources (46 au total).

## Navigation refondue (16 nov.)
- **Méga-menu** « Toutes les pages » dans l’en-tête de chaque page : panneau en 6 colonnes (Démarrer, Terrain, Combattre, Ressources, Base, Repères), chaque entrée avec titre + description, page courante surlignée.
- Trois raccourcis permanents (Mémo, Base de données, Saison), rangée défilante des 29 pages sous le bouton, fermeture au clic extérieur / Échap / clic sur un lien (`js/site.js`).
- `build/make.py` : `NAV_GROUPS` remplace `NAV_MAIN` plat, `nav_html()` génère le méga-menu ; ancien bouton ☰ mobile supprimé.
- CSS : bloc `.mmenu*` avec points de rupture 1100/980/700 px.
- `plan.html` : section expliquant la différence entre menu (chercher une page) et plan (chercher une information).

## Renommage (16 nov.)
- Marque du site : « Delta Force Ultimate Guide » (en-tête, balise `title` de chaque page, pied de page, commentaire de `js/site.js`).
- Bouton de navigation : « MENU » en capitales, compteur de pages retiré du bouton.

## Illustrations (16 nov.)
- **10 nouveaux bandeaux JPG** : 7 pages de base de données (armes, munitions, équipement, collectibles, cartes d’accès, consommables, accessoires) + objets, sources, conseils.
- `tools/make_db.py` : paramètre `hero=` et figure `.page-hero` insérée entre l’en-tête et le corps, légende = phrase d’introduction.
- CSS : `.page-hero` (bannière 190–320 px avec dégradé et légende), agrandissement et survol des icônes d’objets.
- Ce qui reste impossible à générer : les 1 008 icônes d’objets proviennent du jeu (JPG, 25 Mo) et sont déjà en place.

## Illustrations d'entrées (chantier en cours)
- **Arsenal terminé** : 12 armes sur 12 illustrées (`assets/entries/arsenal-*.jpg`), injectées dans les cartes via `tools/entries.py` + `tools/entries.json`.
- **Munitions terminé** : 7 paliers en grille + figures « règle », « plaques », « cinq munitions d’Aurora ».
- **Opérateurs terminé** : 6 fiches illustrées + 1 figure des quatre classes.
- **Détonation, Warfare, Zenith, Débuter** : figures de section ajoutées (bombe, économie de manche, armes ; blindés, rôles, anti-blindé, équipage, reconnaissance ; Riptide ; premier kit).
- Dernière série : index (port de nuit), plan (carte murale), spacecity ×2, cartes ×2, sorties, réglages, économie, saison (aurore).
- Saison : 9 figures d’entrée ajoutées (bataille de Zenith Port, stand de tir, passe, accessoires Haavk, missions 3×3, pêche, calendrier, outils, dernière semaine Brakkesh) + butin (tri au sol).
- Reste : quelques entrées secondaires de Saison et des pages de conseil.
- **Toutes les 31 pages ont désormais au moins une illustration.** Aucune page sans image.

## Reste à faire
1. Relecture de cohérence des chiffres entre pages (les compteurs d’audio et de pages sont centralisés dans `src/index.html` et `src/audio.html`).
2. Illustrations dédiées manquantes sur les pages de conseil (réutilisation de visuels existants pour l'instant).
3. ~~Passes de relecture stylistique sur les pages DB~~ — fait sur les descriptions ; reste la relecture des intitulés de filtres.
4. Vérification périodique des échéances de saison (17, 19, 26 novembre, 3, 10, 12, 18 décembre).

## Estimation
- Consolidation éditoriale du reste : environ 6 à 9 tours de travail, soit 2 à 3 heures de travail humain équivalent.
- Mise à jour de saison : une passe courte à chaque nouvelle date.
- L'enrichissement continu (nouvelles fiches, nouveaux builds) n'a pas de fin naturelle : il suit les patchs du jeu.

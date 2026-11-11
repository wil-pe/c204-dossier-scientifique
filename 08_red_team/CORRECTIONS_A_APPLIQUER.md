# Programme C204 — Red Team n° 2 — Corrections à appliquer

Version 1 — 10 novembre 2026. Complément de `RAPPORT_RED_TEAM_2.md` (les numéros de paragraphe y renvoient).
La Red Team n'a modifié **aucun** fichier des autres équipes : chaque équipe applique elle-même ses corrections.

**Gravité.** *Bloquante* : le dossier final ne doit pas sortir sans la correction (chiffre faux repris dans une
conclusion, affirmation contredite par une pièce du dossier, étiquette trompeuse sur une donnée centrale).
*Importante* : erreur réelle ou conclusion plus forte que la preuve, sans effet sur le verdict d'ensemble.
*Mineure* : formulation, référence, cohérence d'écriture.

**Bilan : 58 corrections numérotées — 4 bloquantes, 30 importantes, 24 mineures** (plus un lot de corrections mineures
pour H, six errata du rapport n° 1 de la Red Team et cinq corrections pour l'Équipe I). Aucune ne renverse un verdict du programme.

Les numéros de ligne sont ceux des fichiers dans leur état du 10 novembre 2026 à 23 h.

---

## 0. Dossier de base — `00_DOSSIER_DE_BASE.md` (direction)

| N° | Lieu | Correction proposée | Gravité |
|---|---|---|---|
| 1 | §6 bis, errata | Ajouter **E11** : « DOC-009 existe en deux états. L'état C204-DOC-014 (première trace : août 2003, site tiers) porte quatre distances : 6 m, 5 m, 8 m, 11 m. La phrase du §3 “aucune dimension numérique sur le document” (l. 117) ne vaut que pour DOC-009. L'attribution de ces valeurs à l'auteur de 2000-2001 n'est pas établie. » | **bloquante** |
| 2 | §6 bis, errata | Ajouter **E12** : « L'hypothèse H1 (L ≈ 1,20 m, §7, l. 229) est remplacée par L = 0,85 m, plage 0,65–1,25 m (Équipe A, confiance faible). Volume ≈ 0,06 m³ ; masse volumique pour 227 kg ≈ 3 700 kg/m³. » | **bloquante** |
| 3 | §6 bis, errata | Ajouter **E13** (transcriptions, Équipe A, contrôlées par la Red Team) : DOC-008 ligne 7 « Singularity status sensor » (« status » : confiance faible ; « stator » non exclu) au lieu de « sensor booster » (l. 98) ; DOC-006 « REVISED JULY 30, 2034 » (confiance moyenne) au lieu de « JULY 10 » (l. 83) ; mention « This area is not to scale » au-dessus du sphéroïde central de DOC-009. | importante |
| 4 | §6 bis, E3 | Remplacer « 4,8 ps pour 227 kg » par « 4,6–4,8 ps » et ajouter la source de l'écart : décompte des degrés de liberté du Modèle standard (4 scalaires et 24 vecteurs, ou 1 scalaire et 27 vecteurs), ±4 %. | mineure |
| 5 | §6 bis, errata | Ajouter **E14** : charge d'un micro-trou noir — valeur typique ≈ 6 e (valeur quadratique moyenne, Page 1977, résumé vérifié) ; borne supérieure d'ordre de grandeur ≈ 137 e. | importante |
| 6 | §6 bis, errata | Ajouter **E15** : entraînement des référentiels à 1 m d'une paire en orbite — jusqu'à 5×10⁻¹⁴ rad/s (terme orbital), et non ≤ 3×10⁻²² rad/s (spin d'un trou isolé). | importante |

## 1. Équipe A — `01_archive/` et `02_reconstruction/`

| N° | Fichier, lieu | Correction proposée | Gravité |
|---|---|---|---|
| 7 | `02_reconstruction/dimensions.json`, cotes `champ_6` à `champ_9` (l. 98–101) ; `DOSSIER_TECHNIQUE.md` l. 177 | Garder « DOC » pour la *lecture*, mais ajouter un champ ou une note : « provenance : état DOC-014, première trace août 2003 sur un site tiers ; attribution à l'auteur non établie ; même trame matricielle que `PT3.jpg` (barre des cotes 8 + 9 : 246 et 247 px), donc réalisable par un tiers à partir du fichier public ». | **bloquante** |
| 8 | `DOSSIER_TECHNIQUE.md` l. 168 ; `dimensions.json` l. 71–73 | Remplacer « médiane de cinq estimations indépendantes » par « médiane de quatre méthodes non indépendantes (le ruban de danger y figure sous deux hypothèses exclusives, 2 et 3 pouces) ; quatre reposent sur un étalon supposé ». Remplacer « ± 0,20 m » par « intervalle central 0,74–1,05 m ; plage 0,65–1,25 m ; loi bimodale ». | importante |
| 9 | `dimensions.json`, cote `L` | Étiquette : `"DÉD"` → `"DÉD (mesures) sur étalons HYP"` ; harmoniser avec `06_modele_3D/parametres.json`, qui porte `"HYP"` pour la même cote. | importante |
| 10 | `dimensions.json`, méthode M3 | Signaler que le rapport télécommande/L est lu sur le dessin DOC-007, dont I-03 établit qu'il n'est pas un relevé de l'objet : méthode la plus faible, à ne pas pondérer comme les autres. | mineure |
| 11 | `01_archive/INVENTAIRE.md`, tableaux §2.1 et §2.2, colonne « 1re attestation » (DOC-006 l. 39, DOC-008, DOC-009, DOC-013, DOC-015 l. 53) | Remplacer « 4 novembre 2000 » par « sujet créé le 4 nov. 2000 ; fichiers datés du 4 mars 2001 (voir réserve) » : le tableau contredit la réserve écrite sous lui. | importante |
| 12 | `INVENTAIRE.md` l. 52 (DOC-014) | Ajouter : « trame identique à DOC-009 à l'échelle du pixel ; valeurs approximativement proportionnelles au dessin (12,3 ± 1,1 px/m sur la copie de 550 px) mais rapport cote 8 / cote 9 dessiné 0,63 pour 8/11 = 0,73 ». Voir `08_red_team/calculs2/journaux/mesure_doc014.txt`. | mineure |
| 13 | `01_archive/TRANSCRIPTIONS.md` l. 79 (DOC-008, ligne 7) | Ajouter la variante « stator » (même nombre de lettres, mêmes hampes que « status »). | mineure |
| 14 | `TRANSCRIPTIONS.md` l. 125 (DOC-014, ligne 8) | Confiance « É » → « É à M » pour le chiffre 8 (moins net que les trois autres valeurs). | mineure |
| 15 | `DOSSIER_TECHNIQUE.md` §6 et `INCOHERENCES.md` I-09 | Harmoniser avec l'Équipe E la hauteur fermée (0,285 m ici, 0,242 m chez E : épaisseur de couvercle 0,25 P contre 0,125 P) et le diamètre des logements (77 contre 81 mm), ou donner la fourchette. | importante |
| 16 | `INCOHERENCES.md` I-10 | Compléter avec les envergures 11-12-13 à l'échelle des cotes : ≈ 26, 32 et 36 m [DÉD], contre 3,0–3,7 m dans le texte. | mineure |

## 2. Équipe B — `03_physique_theorique/`

| N° | Fichier, lieu | Correction proposée | Gravité |
|---|---|---|---|
| 17 | `RAPPORT_B.md` l. 26 (§0.2) ; tableau §3.5 (e), colonne « Ω Lense-Thirring max » (l. 344 et suiv.) | Remplacer « entraînement des référentiels ≤ 3 × 10⁻²² rad/s (spin maximal) » par « 3 × 10⁻²² rad/s pour le spin d'un trou isolé ; jusqu'à 5 × 10⁻¹⁵ rad/s (2 × 10¹² kg) ou 4 × 10⁻¹⁴ rad/s (2 × 4,4 × 10¹² kg) pour le moment cinétique orbital d'une paire à 0,3 m (Équipe D, S05) ». Renommer la colonne « Ω (spin seul) ». | importante |
| 18 | `RAPPORT_B.md` l. 448–450 (§4.3) et l. 919–921 (§11) | Remplacer « le récit est intérieurement cohérent » et « confirmé et renforcé » par : « cohérent pour UNE singularité et un occupant à ≥ 3,6 m ; pour deux singularités de 3,9–5,1 × 10¹² kg, 53–69 g à 1 m, 13–17 g à 2 m, et 2 g seulement à 5,2–5,9 m. La cohérence n'est donc acquise qu'à un ordre de grandeur près (errata E1). » | importante |
| 19 | `ANNEXE_B1_demonstrations.md`, D4 | Ajouter en tête : « Hypothèse : a² + Q² ≤ (GM/c²)² (existence d'un horizon). Dans le cas sur-extrémal il n'y a pas d'horizon, la zone g_φφ < 0 est accessible et la violation de causalité est totale (Carter 1968) ; la conclusion pratique repose alors sur D3 (b). » Même précision au §2.3 du rapport. | importante |
| 20 | `ANNEXE_B1_demonstrations.md`, D1, « Contraposée » (l. 42) ; `RAPPORT_B.md` l. 596 | Ajouter : « La dilatation seule ne crée pas de courbe fermée. Dans un espace-temps à trou de ver traversable, c'est en revanche une différence de dilatation entre les bouches qui engendre l'horizon chronologique (Morris, Thorne & Yurtsever 1988 ; Frolov & Novikov 1990) : l'ingrédient est alors le trou de ver, donc l'énergie négative. » Remplacer « impossible par théorème » par « impossible par théorème dans tout espace-temps stablement causal ». | importante |
| 21 | `ANNEXE_B1_demonstrations.md`, D2, « Portée et limite » (l. 76) | Énoncer les quatre hypothèses : géométrie stationnaire ; véhicule immobile dans ce champ ; \|a\| ≤ 2 g sur tout le chemin jusqu'à la zone de référence ; potentiel négligeable au-delà de L. Ajouter : « cas non stationnaire non couvert ; il relève de l'argument d'échelle D3 (a) ». | importante |
| 22 | `RAPPORT_B.md` l. 55 (§0.11) ; annexe D10 (l. 269) | « littéralement sinusoïdal en ln r » → « égal à r fois une sinusoïde de ln r (L/r, M/r, F/r sont des sinusoïdes exactes de ln r) ». | mineure |
| 23 | `RAPPORT_B.md` §3.3 | Ajouter : « pour aR > ½, des courbes fermées passent par tout événement extérieur (Tipler 1974) : les zones de signe de g_φφ ne sont pas des zones causalement distinctes, ce qui limite l'analogie avec DOC-009 ». | mineure |
| 24 | `RAPPORT_B.md` l. 500 (§4.6) ; `REFERENCES.md` | Retirer Chambers, Hiscock & Taylor 1997 de l'appui à « perd son moment cinétique plus vite que sa masse » (l'article conclut à a/M → 0,555 pour des champs scalaires) ; ne garder que Page 1976 II, ou citer l'article comme exception. | importante |
| 25 | `RAPPORT_B.md` l. 419 (§4.2) | « anisotropie modérée pour Kerr (Leahy & Unruh 1979), jamais un cône » → « asymétrie d'émission calculée pour les neutrinos (Leahy & Unruh 1979) ; aucune collimation n'est prédite » en marquant la seconde partie [DÉD]. | mineure |
| 26 | `RAPPORT_B.md` §4.5 et l. 883 | Présenter « ≤ 137 e » comme borne supérieure d'ordre de grandeur et donner la valeur typique : ≈ 6 e (Page 1977). | mineure |
| 27 | `RAPPORT_B.md` §3.5 (d), §4.4 | Remplacer la séparation de 0,3 m [HYP non signalé] par l'entraxe documentaire 0,10 m (Équipe A), ou donner les deux : t_c = 2×10²³ ans, ω = 377 rad/s pour 2 × 10¹² kg. | mineure |
| 28 | `RAPPORT_B.md` §1 | « ≈ 4 minutes » pour `executer_tout.py` (en-tête du script) : 144 s mesurées. | mineure |

## 3. Équipe C — `04_ingenierie/`

| N° | Fichier, lieu | Correction proposée | Gravité |
|---|---|---|---|
| 29 | `calculs/c06_alimentation_bilan.py` l. 133 (`2 * M_2G`) ; `bilan_energetique.csv` l. 18 ; `RAPPORT_C.md` l. 53, 252, 259, 299 ; fiche F5 l. 52 et 63 | « Fabriquer deux singularités donnant 2 g à 1 m : 5,3×10²⁸ J » → **2,64×10²⁸ J** (2,94×10¹¹ kg au total, soit 2 × 1,47×10¹¹ kg) ; équivalents : 2,4×10⁸ ans d'électricité mondiale, 69 s de Soleil. Fourchette du résumé : « 2,6×10²⁸ à 8×10²⁹ J ». | importante |
| 30 | `RAPPORT_C.md` l. 19–20 (§0.1), l. 285–288 (§7) ; `tableau_faisabilite.csv` | « tient dans 227 kg (budget de masse : 216 kg) » : ajouter un **budget en volume**. À L = 0,85 m le volume utile est ≈ 35 L (Équipes E et I) ; les deux réservoirs de 15 L [HYP] l'occupent presque entièrement. Reformuler : « constructible, et logeable à condition de réduire réservoirs, batterie et bobines (voir palier R1 de l'Équipe I : 36 kg dans 35 L) ; 216 kg ne tiennent pas dans ce volume ». | **bloquante** |
| 31 | `calculs/c00_constantes.py` l. 43 ; tout le rapport | Passer `COFFRE_L, COFFRE_P, COFFRE_H` de 1,20 × 0,36 × 0,30 à 0,85 × 0,26 × 0,285 (ou paramétrer) et relancer `c05`, `c07`, `c09`, `c12`. Chiffres attendus : surface 1,07 m² ; 38–49 °C ⇔ 0,15–0,29 kW ; 4 étalons à jet de césium = 189 % du volume ; blindage logeable ≈ 8 cm (reste ≈ 130 Gy/s) ; température de rayonnement seul ×1,14. | importante |
| 32 | `RAPPORT_C.md` l. 71–72 ; fiches F1, F4 | Entraxe 15 cm et rayon de carter 5 cm [HYP] → 9,8 cm et 3,85 cm (Équipe A, DOC-007) : attraction mutuelle ≈ 3 100 fois le poids ; période orbitale ≈ 8 ms ; flux pariétal 9,5 GW/m². | mineure |
| 33 | `RAPPORT_C.md` l. 167, l. 282 ; fiche F6 l. 44 et 124 | « détecter une masse d'une tonne à 2–3 m (4–7 µGal, 40–50 E) » → « un bloc de 2,4 t à 2 m (4,0 µGal, 40 E) ou un mur de 10 t à 3 m (7,4 µGal, 49 E) ; une tonne à 2–3 m ne donne que 1,7–0,7 µGal, sous l'écart-type du CG-6 ». | importante |
| 34 | fiche F6 l. 50–52 ; `REFERENCES.md` n° 63 | Retirer Jekeli (2006) de l'appui à « suppose une carte préalable » (l'article traite la compensation *in situ* par gradiomètre, sans carte) ; citer une référence de navigation par corrélation de carte, ou reformuler : « la navigation par carte de gravité suppose une carte ; la compensation par gradiomètre embarqué (Jekeli 2006) ne donne pas non plus de position absolue ». | importante |
| 35 | `RAPPORT_C.md` l. 148–149 | Préciser que 62 cm de plomb correspond à une couche de déci-transmission en faisceau large (5,7 cm) et que le faisceau étroit donne ≈ 39 cm : « 40–60 cm ». | mineure |
| 36 | `RAPPORT_C.md` §11 | « c01 (≈ 5 min) » : durée à remesurer (quelques minutes). | mineure |

## 4. Équipe D — `05_simulations/`

| N° | Fichier, lieu | Correction proposée | Gravité |
|---|---|---|---|
| 37 | `S08_reconstitution_doc009/README.md` l. 4, l. 97–99 ; `RAPPORT_D.md` l. 77 (n° 22) et l. 86 (iv) ; chaîne `"conclusion"` du script | « sans aucune cote », « ni cote, ni échelle, ni grandeur », « aucune information physique vérifiable » → « DOC-009 ne porte aucune cote ; sa variante DOC-014 (attribution non établie) porte quatre distances en mètres, à peu près proportionnelles au dessin (dispersion 9 %) et incompatibles avec les distances du texte ». | importante |
| 38 | `S08…/README.md` l. 81–83 (conclusions 2 et 3) ; `RAPPORT_D.md` n° 22 | « Horizon de Kerr exclu », « ergosurface défavorisée » : ajouter « ces deux tests portent sur le sphéroïde central, que le document déclare lui-même hors d'échelle (“This area is not to scale”) ; la forme d'un horizon dépend en outre des coordonnées. Résultat descriptif, sans valeur de preuve ». | importante |
| 39 | `s08_reconstitution_doc009.py` l. 183–184, 590–593 ; `RAPPORT_D.md` l. 93–94 | Sortir du registre de validation les 2 tests qui énoncent la conclusion et les 15 contrôles de l'ajustement sur lui-même, ou les classer « résultats ». Écrire : « 164 tests de validation et 17 contrôles ou résultats (S08) ». Signaler que le test « aucune famille physique n'ajuste mieux » passe avec un rapport de 1,03. | importante |
| 40 | `RAPPORT_D.md` §4, tableau des tests révisés | Ajouter pour S08 « score de noirceur » : « méthode abandonnée alors qu'elle plaçait une famille physique devant l'ellipse ; code et figure non conservés : justification non reproductible ». | importante |
| 41 | `S07…/s07_energie_negative.py` l. 199–201 | Marquer le repère Pfenning & Ford « non vérifié (valeur de mémoire, absente du résumé) » et l'exclure du décompte, ou relire l'article. | mineure |
| 42 | `S01…/s01_hawking.py` l. 218–221 ; `RAPPORT_D.md` §6 | Dire que l'écart de +6,8 % sur M* est un biais du modèle (commun à l'Équipe B : 5,3×10¹¹ kg) et non une réussite à 10 %. | mineure |
| 43 | `RAPPORT_D.md` l. 74 (n° 19) ; `S06…/README.md` | « Charge réellement soutenable : ~137 e » → « borne supérieure ~137 e ; valeur typique ≈ 6 e (Page 1977) ». | mineure |
| 44 | `S05…/README.md` (hypothèses) ; `RAPPORT_D.md` n° 17 | Ajouter le cas d = 0,10 m (entraxe documentaire) à côté de 0,3 m [HYP]. | mineure |
| 45 | `RAPPORT_D.md` §2, ligne van Stockum-Tipler | « CTC ⇔ L < 0 ⇔ aR > 1/2 » → « à l'extérieur : zones L < 0 dès que aR > 1/2 ; dans la matière : ar > 1 ». | mineure |

## 5. Équipe E — `06_modele_3D/`

| N° | Fichier, lieu | Correction proposée | Gravité |
|---|---|---|---|
| 46 | `RAPPORT_E.md` (corps du rapport, §3.3 l. 98, §4, §8) | Mettre le texte à l'échelle des sorties régénérées (L = 0,85 m), ou supprimer les cotes absolues : la note de tête ne suffit pas. En particulier §1 (l. 32–34) : « 10 % du volume intérieur (10,3 L sur 102 L) » → « 14 % (4,7 L sur 35 L) », valeur de `NOMENCLATURE.md`. | importante |
| 47 | `RAPPORT_E.md` l. 21 (§1) ; `NOMENCLATURE.md` §1 | Présenter le bilan par couche : extérieur 94 [DOC] / 12 [DÉD] / 3 [HYP] ; **intérieur 0 [DOC]** / 34 [DÉD] / 30 [HYP]. Préciser que 45 des 94 [DOC] sont des raies, fonds de bandes et pastilles répétés et que 46 n'ont pour source que le dessin DOC-007. | importante |
| 48 | `generer_modele.py` (6 pièces « Cordon de la télécommande ») ; `nomenclature.csv` | Classement [DOC] → [DÉD], conformément au §5.6 du rapport (« tracé [DÉD] »). Bilan : 88 [DOC], 52 [DÉD], 33 [HYP]. | mineure |
| 49 | `generer_nomenclature.py` ; `nomenclature.csv` | Colonne `dimensions_H1` → `dimensions` (elle contient des cotes à L = 0,85 m). | mineure |
| 50 | `parametres.json`, `enveloppe/H_couvercle` | Harmoniser avec l'Équipe A (0,125 P ici, 0,25 P chez A) ou porter l'incertitude à la valeur de l'écart ; même remarque pour le diamètre des logements. | importante |

## 6. Équipe F — `07_experiences/`

| N° | Fichier, lieu | Correction proposée | Gravité |
|---|---|---|---|
| 51 | `RAPPORT_F.md` l. 33–35 (§0.6), l. 155 (§4.1) ; `fiches/EXP-12…md` l. 89 | « 10¹¹–10¹² kg » et « 10¹¹ kg » → « 3,9–5,1×10¹² kg par singularité (7,8×10¹² à 1,0×10¹³ kg pour les deux) ». Marge de la ligne « masse de l'appareil » d'EXP-12 : 2×10¹³. | importante |
| 52 | `RAPPORT_F.md` l. 31, l. 99 ; `EXP-11…md` l. 77 et tableau ; `EXP-12…md` l. 92 | Étiqueter « 9×10³ Gy/s à 3 m » comme « lecture littérale : 400 MW entièrement en rayons X de 100 keV » et ajouter la valeur du spectre de Hawking : « ≈ 3,5×10³ Gy/s à 1 m, ≈ 3,8×10² Gy/s à 3 m pour les γ primaires d'une singularité de 400 MW (Équipes C et G) ». | importante |
| 53 | `EXP-12…md` l. 112 (§7, « Réfutée ») ; `RAPPORT_F.md` §4.5 | Réécrire le critère : « pour une grandeur commutable : différence marche − arrêt ; pour une grandeur permanente selon le récit (masse, pesanteur propre, rayonnement des singularités, qui ne “s'éteignent” pas) : différence dispositif − leurre, ou mesure absolue rapportée au fond ». Ajouter au §1 d'EXP-12 et au §0.4 du rapport : « le banc ne réfute rien de l'objet de 2000-2001, qui n'est pas disponible ; il s'applique à un dispositif candidat ». | importante |
| 54 | `RAPPORT_F.md` l. 26 (§0.3), tableau §2.1 ; `EXP-12…md` (ligne « entraînement ») | « ≤ 3,3×10⁻²² rad/s » → « 3,3×10⁻²² rad/s (spin seul) ; jusqu'à 5×10⁻¹⁴ rad/s pour une paire en orbite » ; écart au gyrolaser géant : « 1 à 9 ordres de grandeur selon le terme ». | importante |
| 55 | `EXP-12…md` l. 100 et §6 | Lever l'ambiguïté « 100 cycles » (100 paires marche/arrêt) / « 64 cycles » ; donner les seuils pour le protocole réellement décrit (64 cycles : 1,36σ par cycle). Budgéter la dérive thermique des accéléromètres ; pour N1, porter 5 µrad et 20 nT à des valeurs réalistes (≥ 20 µrad ; ≥ 100 nT). | mineure |
| 56 | `RAPPORT_F.md` l. 97 | La ligne « 300–500 MW » donne « 3×10⁸ W à évacuer » puis des chiffres calculés pour 4×10⁸ W (5 150 K ; 154 kg/s) : harmoniser. Remplacer « 1,8 m² » par 1,07 m² (190–310 W). | mineure |

## 7. Équipe H — `09_recherche_contemporaine/`

| N° | Fichier, lieu | Correction proposée | Gravité |
|---|---|---|---|
| 57 | `RAPPORT_H.md` l. 22–26 (§0.3), l. 252–254 (§3.2), l. 301 (§3.5), ligne 11 du tableau §13 | Distinguer ce qui est démontré de ce qui est suggéré : « Dafermos & Luk démontrent la stabilité C⁰ de l'horizon de Cauchy de Kerr (la métrique se prolonge continûment) ; leur preuve suggère qu'il est génériquement une singularité nulle faible ; Zilberman et al. montrent la divergence générique des flux quantiques ». Verdict : « non établi, défavorisé » ; confiance « élevée » → « moyenne ». Reprendre la formulation de l'Équipe B (§2.4). | importante |
| 58 | `RAPPORT_H.md` l. 80 et l. 163 | « au-delà de 2 à 3 charges élémentaires… [Gibbons75] » → « valeur quadratique moyenne ≈ 6 e (Page 1977) ; borne ~137 e ; le critère e·Q/4πε₀r_s < m_e c² est un ordre de grandeur de notre part, absent de Gibbons (1975) ». | importante |

Corrections mineures de H, regroupées (même gravité : **mineure**) : l. 27 (§0.4) ajouter « sans singularité de
courbure » après « de taille finie » ; l. 273 remplacer [Tipler77] par Tipler 1976 (PRL 37, 879) ou citer les
deux ; l. 680 retirer [MW90] (hors de son domaine de température) ; l. 744 retirer [Kugel24] de « ni fabricable »
ou préciser « par concentration de lumière » ; l. 259 préciser « en espace anti-de Sitter » pour [HKS23] ; l. 493
« Seize ordres de grandeur » → « dix-huit » (0,4 mg) ou citer 90 mg ; l. 165 « ~10⁻¹² s » → « ≈ 5×10⁻¹² s » ;
`bibliographie_verifiee.csv` : [McGrew18] et [Bothwell22] portent le titre de la prépublication avec la référence
de la version publiée. Signaler enfin que le tableau d'ordres de grandeur du §0 bis n'est adossé à aucun script.

## 8. Équipe G — `08_red_team/RAPPORT_RED_TEAM_1.md` (auto-correction ; le fichier n'est pas modifié)

Errata à joindre au rapport n° 1 (tous de gravité **importante** pour la cohérence du dossier, sans effet sur les objections) :

- l. 68 (F1) : « un trou noir de 100 kg vit 8×10⁻¹¹ s » → **4×10⁻¹³ s** ; l. 293 (§5, D3) : « 4×10⁻¹² s » → **4×10⁻¹³ s**.
- l. 133 (F7) : « Mc² pour 2×10¹² kg : 1,8×10²⁹ J » repose sur la masse photons seuls ; avec 2 × 3,9–5,1×10¹² kg : **7–9×10²⁹ J** (30 à 40 min de luminosité solaire).
- l. 113 (F5) : « ≥ 36 cm de plomb (2 à 6 t) » est une borne en faisceau étroit ; fourchette 40–60 cm, 6–15 t.
- l. 79 (F2) : « ≲ 170 e » : préciser « borne ; valeur typique ≈ 6 e ».
- §4.3 et steelman : séparation de 0,15–0,30 m non documentaire ; entraxe d'après DOC-007 : 0,10 m.
- §2 S7 (e) : la mention « not to scale » de DOC-009 est confirmée (Équipe A) : confiance faible → moyenne à élevée.

## 9. Équipe I — `10_machine_optimisee/` (état de 23 h 21)

| N° | Fichier, lieu | Correction proposée | Gravité |
|---|---|---|---|
| I-1 | `RAPPORT_I.md` §7 (l. 623 et suiv.), §6, résumé (l. 28–32) | Renommer la figure de mérite « décalage relativiste subi par tout objet sur ce trajet » et écrire que R1 n'en est pas la cause (un lest de même masse a la même valeur). Ne pas reporter l'indice de proximité (76) dans le dossier final sans la réserve « notes subjectives ». | importante |
| I-2 | `RAPPORT_I.md` l. 361 (§3.11) ; `nomenclature_R1.csv` R1-04, R1-18 | « ≤ 30 V partout », « ≤ 24 V partout », « haute tension : nulle » → « aucune haute tension accessible ; le tube Geiger-Müller (R1-18) est polarisé en interne à quelques centaines de volts sous un courant de l'ordre du microampère ; les photomultiplicateurs au silicium à ≈ 30 V » — ou remplacer le tube par un dosimètre à semi-conducteur. | importante |
| I-3 | `RAPPORT_I.md` l. 284 et l. 375 ; `nomenclature_R1.csv` R1-B1 | L'essai T6 demande « 3 césiums emportés, 3 restés » ; la configuration B n'en chiffre que 3. Ajouter les étalons de référence (≈ 240 k€, 90 kg, hors véhicule) ou décrire le lien de temps qui les remplace, avec son bruit. | importante |
| I-4 | `RAPPORT_I.md` l. 28 | « orienté vers le futur seulement » → « jamais vers le passé : selon le trajet, l'unité vieillit un peu moins ou un peu plus que la référence ». | mineure |
| I-5 | `RAPPORT_I.md` l. 569 | « toute machine de taille finie l'exige (Hawking 1992) » → ajouter « sans singularité de courbure ». | mineure |

(Les cinq corrections de l'Équipe I ne sont pas comptées dans le bilan des 58.)

---

## Ordre de traitement conseillé

1. Les quatre bloquantes : n° 1 et 2 (errata du dossier de base), n° 7 (provenance des cotes de DOC-014), n° 30
   (budget en volume de C).
2. Les chiffres repris d'une équipe à l'autre : n° 17, 29, 51, 52, 54, puis l'auto-correction du rapport n° 1.
3. Les conclusions plus fortes que la preuve : n° 18, 37–40, 47, 53, 57.
4. Le reste.

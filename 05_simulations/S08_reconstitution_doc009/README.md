# S08 — Reconstitution quantitative de C204-DOC-009 (« Tipler sinusoid field ») et de sa variante cotée DOC-014

> **Analyse d'image et simulation illustratives — ce n'est pas une preuve expérimentale.** S08 est une
> **description géométrique** du dessin, non un test physique. Les sources sont des copies secondaires ; les
> mesures valent à 0,5–2,5 pixels près. Une ressemblance de forme ne prouverait rien sur la physique ; une
> absence de ressemblance ne prouve rien sur l'intention de l'auteur.

Version révisée après la validation contradictoire (phase 7, corrections n° 37 à 40 de la Red Team).

## Ce que portent les documents

- **DOC-009** (copie de référence 318×369 px ; meilleure copie `PT3.jpg`, 578×799 px) : **aucune cote**.
- **DOC-014** (`timetravel16_07.jpg`, 550×594 px) : même tracé, avec **quatre distances en mètres** dans la légende —
  6 m (repère 6), 5 m (7), 8 m (8), 11 m (9). Première trace en août 2003 sur un site tiers ; **attribution à l'auteur de
  2000-2001 non établie** (Équipe A, Red Team).
- Les deux états portent, au-dessus du sphéroïde central, la mention **« This area is not to scale »**.

La première version de ce README affirmait « sans aucune cote », « ni cote, ni échelle, ni grandeur » : c'était vrai de
DOC-009 seulement, et faux de DOC-014. Corrigé.

## Méthode

1. Trois copies traitées par le même code (`--copie reference | pt3 | doc014` ; sans argument, le script traite la référence,
   relance les deux autres et compare). `PT3.jpg` et DOC-014 sont **recalées** sur la copie de référence (échelles, rotation,
   translation ; corrélation 0,993 et 0,959) : toutes les mesures sont exprimées dans le même repère, la noirceur étant lue à la
   résolution native (≈ 1,6 fois plus fine). Fichiers de `01_archive/` ouverts en lecture seule.
2. **Axe en tirets** : ajustement linéaire robuste (inclinaison −0,69°).
3. **Ellipses** (6 anneaux, enveloppe du sphéroïde central, deux grands contours) : maximisation de la noirceur moyenne le long du
   contour, 24 départs aléatoires (graine 204), rappel vers la lecture à l'œil (±4 px ; ±2,5 px pour les traits pâles).
4. **Points de contour relevés indépendamment de toute famille** : sphéroïde central — trait le plus extérieur le long de rayons, hors
   pôles et axe (74 à 84 points selon la copie) ; grand contour E1 — les 12 sommets d'anneaux, plus les points du trait pâle sur
   ses arcs gauches (0, 11 et 13 points selon la copie).
5. **Familles ajustées aux points** (moindres carrés robustes) : ellipse (4 paramètres), super-ellipse (5, témoin), ergosurface et
   horizon de Kerr en coordonnées de Kerr-Schild (4), équipotentielle newtonienne de deux masses à écartement libre (4) ou telles
   que dessinées (1).
6. **Test des pôles** : familles ajustées sur les arcs équatoriaux ; on compare les pôles qu'elles prédisent aux pôles dessinés.
7. **« Entonnoir »** : profil R(x) des courbes reliant le sphéroïde aux grands anneaux (31 ancres lues à l'œil sur la copie de
   référence, affinées automatiquement sur chaque copie à ±2 px).
8. **Cotes de DOC-014** : extrémités des quatre traits de cote lues sur la copie recalée (±1,5 px), rapportées aux valeurs inscrites.

## Tests de validation, contrôles et résultats (correction n° 39)

Un **test de validation** confronte le code à une réponse connue indépendamment et peut échouer. La première version annonçait
« 28/28 tests » ; la Red Team a montré que 17 n'en étaient pas (15 contrôles de l'ajustement sur lui-même, 2 énoncés de
conclusion). Décompte actuel :

**9 tests de validation (9 passés)** : ellipse de synthèse retrouvée à 0,04 px ; inclinaison de l'axe contre la lecture à l'œil ;
deux singularités détectées (transcription de l'Équipe A) ; limites analytiques des familles (équipotentielle → cercle ; rapport
d'axes de l'ergosurface extrémale = √5) ; puissance du test des pôles sur données de synthèse, dans les deux sens (moyenne de
20 tirages : vraie ellipse → ellipse 0,4 px, ergosurface 7,8 px ; vraie ergosurface a/M = 0,93 → ergosurface 1,0 px, ellipse 6,6 px).

**21 éléments consignés hors décompte** (`resultats/S08_resultats.json`, clé `validation.hors_decompte`) :
- 18 *contrôles* : 7 contrastes de trait, 9 écarts à la lecture à l'œil (bornés par le terme de rappel : ne peuvent guère échouer),
  affinage des ancres (borné à ±2 px par construction), rejeu de la méthode abandonnée ;
- 3 *résultats* : alignement des anneaux ; « l'ellipse prédit les pôles mieux que toute famille physique » ; « aucune famille
  physique n'ajuste mieux que l'ellipse ». Ce dernier ne tient qu'avec un **rapport de 1,01 à 1,03** (équipotentielle à
  écartement libre contre ellipse) : cela signifie « aussi bien », non « moins bien ».

Le test des pôles a été **choisi après avoir vu les données** (le RMS sur les arcs ne discriminait pas) ; sa puissance est validée sur
données de synthèse, mais ce choix a posteriori limite sa valeur.

### Méthodes abandonnées

- **Score de noirceur (correction n° 40).** La première version comparait les familles par la noirceur moyenne maximale le long de
  la courbe. Elle plaçait une famille physique devant l'ellipse (1,13 fois sur le sphéroïde, 1,12 fois sur le grand contour), et
  nous l'avions abandonnée **sans conserver ni le code ni une figure** : justification non reproductible, comme l'a relevé la Red Team.
  Elle est désormais rejouée dans le script (section 10 bis, graine 2040, 60 départs) et tracée (`S08_fig4_methode_abandonnee*.png`).
  Résultat sur la copie de référence : l'équipotentielle obtient 1,13 fois le score de l'ellipse **en passant à 5,5 px (RMS) des
  points du contour** (ellipse : 1,5 px) ; l'ergosurface d'axe horizontal 1,08 fois, à 14 px. Ces courbes longent des méridiens
  internes, non l'enveloppe. Sur les copies nettes l'avantage disparaît (1,04 sur `PT3`, 1,00 sur DOC-014) ; sur le grand contour
  aucune famille physique ne dépasse l'ellipse (0,73 à 0,91) — le 1,12 initial venait d'un ajustement de l'ellipse attiré par le
  cadre du schéma. Le rejeu ne restitue donc qu'une partie des chiffres initiaux, faute d'archive.
- **RMS sur les seuls arcs équatoriaux** : non discriminant (ellipse et ergosurface s'ajustent également sur données de synthèse).
- **Grand contour unique** : voir ci-dessous.

## Erreur de lecture corrigée grâce aux meilleures copies

Sur `PT3.jpg` et DOC-014, le « grand contour pâle » se révèle fait de **deux ellipses de même hauteur** : **E1**, enveloppe des six
anneaux, et **E2**, décalée de 0,14 A vers la droite (rapport d'axes 1,45–1,47). Sur la copie de 318 px elles se confondaient ; la
première version les ajustait comme une seule courbe, et mélangeait des points de l'une et de l'autre. E1 est maintenant définie
par les 12 sommets d'anneaux. Conséquence : l'énoncé « ergosurface non exclue pour le grand contour (3,0 px contre 2,5 px) » de la
première version est **retiré** ; il reposait sur ce mélange.

## Résultats (repère de la copie de référence ; A = demi-grand axe de E1 = 146 px)

| Mesure | DOC-009, référence | DOC-009, `PT3.jpg` | DOC-014 |
|---|---|---|---|
| Rapport d'axes du sphéroïde central | 1,58 | 1,55 | 1,54 |
| Rapport d'axes du grand contour E1 | 1,54 | 1,59 | 1,60 |
| RMS de l'ellipse : sphéroïde / E1 [px] | 1,46 / 1,14 | 1,48 / 1,04 | 1,53 / 1,01 |
| Erreur aux pôles : ellipse / horizon / ergosurface / équipotentielle libre [px] | 0,8 / 3,4 / 5,3 / 8,0 | 0,9 / 3,3 / 5,5 / 7,3 | 0,5 / 2,9 / 5,9 / 7,6 |
| E1 : RMS ergosurface ÷ RMS ellipse | 1,83 | 2,32 | 2,50 |
| E1 : RMS équipotentielle libre ÷ RMS ellipse (points de contour) | **1,01** (12) | **1,79** (23) | **1,94** (25) |
| Anneaux sur E1 : RMS des 12 sommets / erreur max. de validation croisée [px] | 1,1 / 5,2 | 1,2 / 4,8 | 1,2 / 5,0 |
| Second contour E2 : contraste / décalage | 1,7 / 0,14 A | 1,9 / 0,14 A | 2,6 / 0,14 A |
| Rayons des anneaux negative / null / positive [A] | 0,47 / 0,34 / 0,20 | 0,48 / 0,34 / 0,20 | 0,47 / 0,34 / 0,20 |
| Décalage masses ↔ centre du système d'anneaux [A] | 0,222 | 0,224 | 0,222 |
| Séparation des deux singularités [A] | 0,069 | 0,064 | 0,067 |
| Entonnoir : RMS Flamm / Ellis / meilleure courbe symétrique libre / témoin asymétrique [px] | 20 / 54 / 2,5 / 1,0 | 20 / 53 / 2,5 / 1,0 | 20 / 53 / 2,6 / 1,1 |
| Méridiens détectés | 14 | 15 | 15 |

**Les conclusions changent-elles sur les meilleures copies ?** Douze énoncés descriptifs ont été évalués sur chaque copie
(`resultats/S08_comparaison_copies.json`, figure 5). **Onze reçoivent la même réponse sur les trois copies** ; dix sont vérifiés
partout, un ne l'est nulle part (validation croisée des anneaux). **Un seul dépend de la copie** : sur la référence, où le trait
pâle de E1 n'est pas détecté (12 points seulement), l'équipotentielle à écartement libre ajuste E1 aussi bien que l'ellipse (1,01) ;
sur les copies nettes elle est nettement moins bonne (1,8 à 1,9). Les meilleures copies **précisent** donc la description
(deux grands contours, anneaux, équipotentielle) sans la renverser.

### Constats (descriptifs)

1. Sphéroïde central et grand contour E1 sont des **ellipses** à 1–1,5 px près, de rapport d'axes voisin (1,54 à 1,60).
2. **Forme d'horizon** : le rapport d'axes dépasse √2, maximum d'un horizon de Kerr *tracé en coordonnées de Kerr-Schild*.
   **Forme d'ergosurface** : elle prédit des pôles déprimés, à 5–6 px des pôles dessinés (ellipse : < 1 px).
   **Ces deux constats portent sur le sphéroïde central, que le document déclare lui-même hors d'échelle (« This area is not to
   scale ») ; la forme d'un horizon dépend en outre des coordonnées (sphère en Boyer-Lindquist). Résultat descriptif, sans valeur
   de preuve** (correction n° 38).
3. **Équipotentielles** : celles des deux masses *telles que dessinées* seraient quasi sphériques (6 px d'écart sur le sphéroïde, 30 à 35 px
   sur E1) ; à écartement libre, elles ne se distinguent pas de l'ellipse au RMS sur le sphéroïde (1,03), mais manquent les pôles de
   7 à 8 px.
4. **Anneaux** : leurs 12 sommets s'alignent sur l'ellipse E1 à 1,1 px (RMS, 4 paramètres ajustés) — compatible avec des sections
   parallèles d'une même ellipse. **Réserve** : en validation croisée par paires, le rayon du plus petit anneau est prédit à 5 px
   près (extrapolation en bout d'ellipse) ; le critère de 3 px que nous nous étions fixé n'est **pas** satisfait. Leur taille
   *décroît* en s'éloignant du centre.
5. **Le système d'anneaux n'est pas centré sur les masses** (décalage 0,22 A, identique sur les trois copies).
6. **Entonnoir asymétrique** (rapport droite/gauche 1,86). Les profils physiques contraints échouent (Flamm 20 px, caténoïde d'Ellis
   53 px) ; les courbes symétriques libres laissent 2,5 px ; un témoin asymétrique sans signification physique, 1,0 px.
7. **Aucune sinusoïde** : celle qu'on ajuste dégénère en parabole (longueur d'onde ≥ 780 px pour un profil de 198 px).

### Les quatre distances de DOC-014 (correction n° 37)

| Cote | Valeur inscrite | Longueur dessinée (repère de référence) | Échelle |
|---|---|---|---|
| 6 — Vertical safe distance | 6 m | 41,5 px | 6,9 px/m |
| 7 — Mass offset | 5 m | 38,4 px | 7,7 px/m |
| 8 — Rear mass dist. | 8 m | 57,8 px | 7,2 px/m |
| 9 — Forward mass dist. | 11 m | 93,2 px | 8,5 px/m |

- Échelle moyenne **7,6 px de référence par mètre** (12,2 px/m sur la copie de 550 px), **dispersion 9 %** pour une incertitude de
  pointé de 2,6 % : valeurs **à peu près** proportionnelles au dessin, pas exactement (cote 8 / cote 9 dessiné 0,62, inscrit 0,73).
  Accord avec la mesure indépendante de la Red Team (12,3 ± 1,1 px/m).
- À cette échelle [DÉD] : demi-grand axe de E1 ≈ 19 m ; envergures des trois paires d'anneaux **26, 33 et 36 m**, soit des
  demi-envergures de 13 à 18 m — **3,6 à 6 fois** les « 10 à 12 pieds » (3,0–3,7 m) du texte.
- Le trait de la cote 7 (« mass offset ») part de la verticale des pôles (x ≈ 140 px) et s'arrête à un trait vertical en x ≈ 179 px,
  qui ne coïncide ni avec le centre du système d'anneaux (170 px) ni avec celui de E2 (190 px).

**Verdict** : DOC-009 est une figure géométriquement régulière (ellipses, anneaux alignés, sphéroïde « fil de fer ») qui ne
correspond à aucune famille de surfaces physiques testée mieux qu'à des ellipses génériques. **DOC-009 ne porte aucune cote ; sa
variante DOC-014 (attribution non établie) porte quatre distances en mètres, à peu près proportionnelles au dessin (dispersion
9 %) et incompatibles avec les distances du texte.** À conserver comme description du schéma, non comme test physique.

## Limites et degré de confiance

- Numérisation des anneaux et du sphéroïde : **élevé** (±0,5 à 1 px, stable sur trois copies). Grands contours pâles : **moyen**.
- Tests de forme : **faible comme arguments physiques** (zone déclarée hors d'échelle ; statistique des pôles choisie a posteriori ;
  seules des familles déclarées par nous ont été essayées ; le RMS ne départage pas les familles à 4 paramètres).
- Cotes de DOC-014 : lecture manuelle des extrémités (±1,5 px) ; valeurs transcrites par l'Équipe A ; attribution non établie.
- Ancres de l'entonnoir et estimations initiales saisies sur la copie de référence ; recalage par similitude, sans correction de
  déformation locale ; DOC-014 traité sur une seule de ses deux copies (`OP4.jpg`, 460 px, non traitée).
- Le rejeu de la méthode abandonnée ne reproduit pas à l'identique la première exécution (départs aléatoires non archivés).

## Fichiers

- `s08_reconstitution_doc009.py` (≈ 50 s pour les trois copies). Exécution : `.venv/bin/python 05_simulations/S08_reconstitution_doc009/s08_reconstitution_doc009.py`
- `figures/S08_fig1_numerisation*.png`, `S08_fig2_familles_physiques*.png`, `S08_fig3_entonnoir_anneaux*.png`,
  `S08_fig4_methode_abandonnee*.png` (suffixes : aucun = référence, `_pt3`, `_doc014`), `S08_fig5_comparaison_copies.png`
- `resultats/S08_resultats*.json`, `S08_ellipses_numerisees*.csv`, `S08_comparaison_copies.json`

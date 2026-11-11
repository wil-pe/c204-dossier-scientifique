# Rapport de l'Équipe E — ingénierie inverse et reconstruction 3D de l'unité « C204 »

Version 1.1 — 10 novembre 2026 — dossier `06_modele_3D/` — rédigée à l'échelle **L = 0,85 m ± 0,20 m**
(estimation de l'Équipe A), après la validation contradictoire (voir le journal des corrections en fin de rapport).

> **Statut de l'objet.** Ce rapport décrit la reconstruction 3D d'un objet **tel qu'il est décrit** par des
> documents non authentifiés (messages « John Titor », 2000-2001, compilation secondaire de 2023). Rien n'atteste
> que cet objet ait existé ni fonctionné. Les « fonctions » citées sont celles **revendiquées** par les légendes
> et le texte ; elles ne sont ni vérifiées ni physiquement établies. Le modèle est une aide à la lecture critique
> des documents, pas le plan d'une machine.

Étiquettes : **[DOC]** documenté · **[DÉD]** déduit · **[HYP]** hypothétique · **[INT]** interprétation de tiers.
Chaque affirmation chiffrée est suivie de son incertitude et d'un degré de confiance (élevé / moyen / faible).

---

## 1. Résumé

- **Variante A (coffre)** : 173 pièces primitives — 88 [DOC], 52 [DÉD], 33 [HYP]. Ce total cache une coupure
  nette, qu'il faut lire **par couche** :

  | Couche | [DOC] | [DÉD] | [HYP] |
  |---|---|---|---|
  | Extérieur (coque, couvercle, platine, télécommande) | **88** | 18 | 3 |
  | **Intérieur (tout ce qui est sous la platine)** | **0** | 34 | 30 |

  **Aucune pièce intérieure n'est documentée.** Et les 88 [DOC] ne valent pas « la moitié de l'objet » : 42 sont
  des motifs répétés (20 raies noires, 4 fonds de bande, 18 pastilles du pupitre) ; 48 n'ont pour source que le
  dessin DOC-007 (« [DOC] dessin »), que les photos contredisent sur la position des bandes ; 37 s'appuient sur le
  dessin **et** sur une photo ou sur DOC-004 ; 3 sur les photos seules. Pour les pièces relevées sur la seule vue
  de dessus, seule l'emprise en plan est documentée : épaisseurs et reliefs sont supposés.
- **Contenu modélisé** : coffre plat à couvercle articulé, platine supérieure de DOC-007 (bandes de danger, deux
  logements circulaires, pupitre à 6 organes, rangement), intérieur du couvercle (bandes, plaque 7, étiquettes
  des photos), télécommande et cordon, puis les 12 composants de DOC-008 et les horloges/calculateurs du texte.
- **Variante B (écorché DOC-005)** : 40 pièces — 1 [DOC] (enveloppe), 39 [DÉD] (volumes génériques). Modélisée
  séparément : prisme à extrémités biseautées, 4 patins, 2 cloisons, pupitre d'extrémité (9 pièces), 24 volumes
  internes.
- **Variante A′** : même coffre, autre disposition interne hypothétique (I2), pour montrer que l'emplacement de
  la plupart des composants internes est un choix et non une donnée.
- **Proportions mesurées** (aucune cote n'est documentée) : L/P = 3,27 ± 0,08 (DOC-007) ; H_corps/L = 0,246 ±
  0,015 et angle d'ouverture 108° ± 6° (DOC-004, caméra en perspective ajustée) ; logements à 0,382 L, entraxe
  0,356 P, diamètre 0,095 L (DOC-007).
- **Constat principal de modélisation** : dimensionnés à l'échelle de leur propre schéma, les 12 composants de
  DOC-008 n'occupent que **9 % du volume intérieur** du coffre (3,1 L sur 35 L) ; **10 %** (3,7 L) en ajoutant
  les volumes génériques [HYP] des horloges et des calculateurs. Ce taux ne dépend presque pas de l'échelle
  (10 à 11 % pour L de 0,65 à 1,25 m). Les documents ne décrivent donc pas ce qui remplirait 90 % du volume, ni
  ce qui pèserait l'essentiel des 227 kg revendiqués.
- **Écart « côte à côte / alignées en profondeur »** (DOC-008 contre DOC-007) : il disparaît si DOC-008 est lu
  comme une élévation vue depuis une extrémité du coffre [DÉD] ; il reste un écart d'entraxe (1,62 contre 1,16
  diamètre).
- **Variante B** : les proportions d'enveloppe ne sont pas incompatibles avec le coffre, et le pupitre de
  l'extrémité droite de DOC-005 ressemble à celui de DOC-007 ; en revanche la forme (extrémités biseautées,
  patins, pas de couvercle) et le contenu (mécanique dense) sont incompatibles avec DOC-004/007/008.

## 2. Livrables

| Fichier | Rôle |
|---|---|
| `parametres.json` | **Source unique** : toutes les cotes (valeur en m, incertitude, source, étiquette). Une cote proportionnelle porte `rapport` + `reference` et se recalcule. (`parametres_H1_L1.20m.json.bak` : état initial à 1,20 m, conservé par la direction.) |
| `generer_modele.py` → `modele_c204.json` | Liste de pièces : primitive + transformation + nom + repère + source + classement + appui documentaire + fonction revendiquée + décalage d'éclaté (variantes A, A2, B) ; bilans par classement et par couche. |
| `mesures/verifier_interferences.py` | Contrôle que les composants internes ne se chevauchent pas, ne traversent pas les parois et n'entrent pas dans le rangement. |
| `construire_modele.py` → `exports/` | GLB, OBJ (+MTL) et STL : coffre fermé, coffre ouvert avec composants internes, vue éclatée, variante A′ ouverte, variante B. Couleurs par classement. |
| `rendre_vues.py` → `rendus/` | 14 images PNG (rendu logiciel sans GPU, voir §3.5). |
| `generer_visionneuse.py` → `visionneuse.html` | Visionneuse interactive autonome (three.js r128 via cdnjs, données embarquées). |
| `generer_nomenclature.py` → `NOMENCLATURE.md`, `nomenclature.csv` | Repères de DOC-007, DOC-008, DOC-005, six systèmes du texte, éléments des photos ; une ligne par pièce (colonnes `dimensions`, `appui`). |
| `generer_schemas.py` → `architecture_fonctionnelle.svg`, `schema_electrique_hypothetique.svg` | Schéma-blocs des flux ; schéma unifilaire hypothétique. |
| `mesures/mesurer_proportions.py` → `mesures/mesures_proportions.json` + 3 images de contrôle | Relevé des proportions sur les documents (pointés et calculs traçables). |
| `reconstruire.sh` | Régénère tout (≈ 20 s) à partir de `parametres.json`. |
| `RAPPORT_E.md` | Ce rapport. |

Rendus : `01_exterieur_ferme`, `02_ouvert_aspect`, `03_ouvert_classement`, `04_interieur_composants`, `05_eclate`,
`06_ortho_dessus`, `07_ortho_face`, `08_ortho_cote`, `09_variante_B_ecorche`, `10_comparaison_DOC-007`,
`11_comparaison_DOC-004`, `12_comparaison_DOC-005`, `13_dispositions_internes_I1_I2`, `14_comparaison_DOC-008`.

**Changer l'échelle** : modifier `echelle.L` dans `parametres.json`, puis `./reconstruire.sh`. Le modèle a été
reconstruit et contrôlé (aucune interférence entre pièces) pour L = 0,65 ; 0,85 ; 1,00 ; 1,20 et 1,25 m. Pour
imposer une cote isolée (par exemple P ou H_corps), supprimer ses champs `rapport`/`reference` et saisir `valeur`.

## 3. Méthode

### 3.1 Lecture des sources

Les 12 originaux de `01_archive/originaux/` ont été examinés un par un (lecture seule), ainsi que les
agrandissements de `01_archive/ameliores/`. Des recadrages quadrillés (coordonnées en pixels de l'image
d'origine) ont servi aux pointés ; ils ne sont pas conservés, mais tous les pointés figurent dans
`mesures/mesurer_proportions.py` et sont reportés sur les images de contrôle `mesures/DOC-00x_*.png`.

### 3.2 Mesure des proportions

- **DOC-007** (seule vue orthographique) : relevé automatique des contours, des deux disques et des raies
  obliques par seuillage et profils ; pointé manuel des limites de zones. Incertitude de pointé ±1 px, soit
  ±0,3 % de L en abscisse et ±0,9 % de P en ordonnée.
- **DOC-004** (vue 3/4, illustration tramée) : ajustement par moindres carrés d'une caméra en perspective
  (focale, 3 rotations, 3 translations) sur 9 coins pointés à ±3 px, avec P/L, H/L et l'angle du couvercle comme
  inconnues. Contre-épreuves : P/L imposé à la valeur de DOC-007 ; balayage de la focale de 500 à 5 000 px ;
  résolution axonométrique indépendante (perspective faible).
  Équations : un point M du coffre normalisé (L = 1) se projette en u = c + f·(x_c/z_c, y_c/z_c) avec
  (x_c, y_c, z_c) = R·M + t, c = centre de l'image (hypothèse : image non recadrée) ; on minimise la somme des
  carrés des écarts aux 9 coins pointés. Axonométrie : si e_x, e_y, e_z sont les arêtes moyennes projetées
  (px), alors e_x·e_xᵀ/L² + e_y·e_yᵀ/P² + e_z·e_zᵀ/H² = s²·I₂, soit trois équations linéaires en 1/L², 1/P²,
  1/H². Limites : distorsion optique ignorée, point principal supposé centré, coins arrondis et trame grossière.
- **DOC-008** (schéma de principe) : tailles des 12 composants rapportées au diamètre de l'anneau noir des
  carters (65 px). Ce ne sont que des proportions **internes au schéma**, sans garantie d'échelle.
- **DOC-005** (écorché) : longueur, hauteur et fuyantes de l'enveloppe ; le dessin est proche d'une projection
  oblique, dont le rapport de réduction des fuyantes est inconnu.
- **Photos** (DOC-003, la mieux résolue) : position relative des bandes, de la plaque et des étiquettes à
  l'intérieur du couvercle.

### 3.3 Paramétrage

Une seule cote absolue : **L = 0,85 m ± 0,20 m**, estimation de l'Équipe A (`02_reconstruction/dimensions.json` :
médiane de cinq étalonnages — sangle, ruban de danger de 2 ou 3 pouces, télécommande, cordon spiralé ; confiance
faible). Elle remplace l'hypothèse H1 du dossier de base (1,20 m), qui reste dans la plage plausible (0,65–1,25 m
selon la Red Team) mais peu probable. Étiquette : [DÉD] chez l'Équipe A ; **[HYP] dans `parametres.json`**, parce
que quatre des cinq méthodes reposent sur un étalon supposé (Red Team 2, §6.3) — la divergence d'étiquette est
assumée et signalée.

Tout le reste est une proportion mesurée ([DOC]) ou transposée ([DÉD]) multipliée par L, P, H_corps ou D_ref.
Les volumes génériques [HYP] (horloges, calculateurs), la profondeur du rangement, l'épaisseur de la
télécommande et les loquets sont eux aussi proportionnels, pour que le modèle reste cohérent à toute échelle.
Seules restent absolues de petites cotes [HYP] : épaisseurs de tôle et de marquage (1 à 8 mm), reliefs, jeu sous
la platine (10 mm), rayon du cordon (8 mm, étalon E4 de l'Équipe A).

**Harmonisation avec l'Équipe A** : là où A donne une autre valeur, la valeur nominale de l'Équipe E est
conservée, l'incertitude est portée au moins à l'écart, et la valeur de A est citée (§4.2 et `parametres.json`).

### 3.4 Règle de classement des pièces

Le classement porte sur la pièce **telle que modélisée** (forme + position). Deux champs le complètent :
`existence` (le composant figure sur une image, dans le texte seul, ou est ajouté par nous) et `appui` (dessin
DOC-007 seul, dessin + photo ou illustration, photo seule, schéma DOC-008, texte seul).

| Classement | Critère | Exemples |
|---|---|---|
| [DOC] | forme et position lisibles sur un document ; pour une pièce vue seulement de dessus, l'emprise en plan seule est documentée | coffre, bandes, cadre des logements, pupitre, plaque 7, boîtier de télécommande |
| [DÉD] | composant documenté, forme ou position obtenue en croisant des documents | carters, bobines, enveloppes (DOC-008) placés sous les logements (DOC-007) ; cordon de la télécommande (tracé 3D) ; loquets ; étiquettes vues sur DOC-004 seulement |
| [HYP] | forme, taille ou position supposées | fond du coffre ; batterie, réservoirs, pompe, générateur d'électrons, capteurs (existence DOC-008, **emplacement** supposé) ; horloges et calculateurs (texte seul) |

Bilan d'existence de la variante A : 163 pièces « DOC image », 7 « DOC texte » (4 horloges, 3 calculateurs),
3 « HYP » (fond, poignée droite, fond du rangement).

### 3.5 Génération, rendu, contrôle

- Chaque pièce est **une** primitive (boîte, cylindre, sphère/ellipsoïde, tore, prisme extrudé éventuellement
  percé). Rotation R = Rz·Ry·Rx, doublée d'un quaternion pour lever toute ambiguïté entre Python et three.js.
- États : `ferme`, `ouvert` (108°), `eclate`, `a_plat` (180°, convention de DOC-007). Le couvercle tourne autour
  de l'arête arrière haute du corps.
- Contrôle d'interférences (`mesures/verifier_interferences.py`, boîtes englobantes) : aucune à L = 0,85 m.
- Rendus : rastérisation à tampon de profondeur écrite en numpy (occultation exacte), ombrage plat, arêtes par
  détection de contours (identifiant de pièce et normale), enveloppes translucides par « depth peeling »,
  suréchantillonnage ×2 ; matplotlib ne sert qu'à l'habillage. Chaque PNG a été ouvert et corrigé (cadrage,
  étiquettes, pièces parasites, chevauchements de la disposition I2).
- Contrôle de ressemblance : `10_comparaison_DOC-007.png` (vue de dessus, couvercle à plat) et
  `11_comparaison_DOC-004.png`, où le modèle est rendu **avec la caméra ajustée sur DOC-004** : les arêtes du
  coffre se superposent au document à 4 px près (RMS).

## 4. Proportions mesurées

### 4.1 DOC-007 — plan de la platine et du couvercle (confiance élevée pour le relevé du dessin)

Contour extérieur : 357,5 px × 111 px (corps) et × 107,5 px (couvercle). **L/P = 3,22 (corps), 3,33
(couvercle), retenu 3,27 ± 0,08** (Équipe A : 3,30 ± 0,05). Abscisses en fraction de L depuis le bord gauche ;
ordonnées en fraction de P depuis l'avant. Les cotes en millimètres valent pour L = 0,85 m et portent en plus
l'incertitude d'échelle (±24 %).

| Élément | Abscisse (fraction de L) | Ordonnée (fraction de P) | À L = 0,85 m |
|---|---|---|---|
| Rebord (contour → panneau) | 0,0175 ± 0,004 | idem | 15 mm |
| Zone tramée gauche, trait de division | 0,078 | — | 67 mm |
| Bande de danger n°1 | 0,134 → 0,232 | toute la profondeur | 114 → 197 mm |
| Cadre des deux logements | 0,301 → 0,462 | 0,239 → 0,919, barrette à 0,581 | 256 → 392 mm |
| **Logement « MAIN SINGULARITY » (1)** | **0,382** | **0,757** (côté charnière) | x = 325 mm, y = 197 mm |
| **Logement « STEERING SINGULARITY » (2)** | **0,382** | **0,401** (côté avant) | x = 325 mm, y = 104 mm |
| Rayon des logements | 0,0476 ± 0,003 | — | r = 40 mm (Ø 81 mm ; Équipe A : Ø 77 mm) |
| Entraxe des logements | — | 0,356 (= 1,16 diamètre) | 93 mm (Équipe A : 98 mm) |
| Bande de danger n°2 | 0,533 → 0,629 | toute la profondeur | 453 → 535 mm |
| Écran de secours (4), fente | 0,664 | 0,05 → 0,90 | 564 mm |
| Panneau 5 (coupure d'urgence) | 0,699 → 0,789 | fenêtre 0,83–0,92 ; organe rond à 0,242 | 594 → 671 mm |
| Panneau 8 / 6 | 0,789 → 0,880 | touches 0,33–0,95 ; boîtier 6 : 0,09–0,26 | 671 → 748 mm |
| Rangement 9 | 0,880 → 0,982 | toute la profondeur | 748 → 835 mm |
| Plaque 7 (couvercle) | 0,712 → 0,870 | 0,098 → 0,879 depuis la charnière | 134 × 203 mm |
| Charnières | 0,193–0,274 et 0,730–0,808 | — | 2 × ≈ 68 mm |
| Télécommande 3 | boîtier 0,0965 L × 0,1007 L | posée devant | 82 × 86 mm |

Bandes : 4 raies noires par bande, inclinées de 32,6° ± 1,5° sur l'axe long, pas 0,246 P, épaisseur 0,131 P.
Pupitre 8 : 18 pastilles (2 isolées, une colonne de 11, une colonne de 5), pas 0,045 P.

### 4.2 DOC-004 — hauteur et ouverture (confiance moyenne)

| Méthode | L/P | H_corps/L | H_corps/P | Angle du couvercle | Résidu |
|---|---|---|---|---|---|
| Caméra en perspective, tout libre (focale trouvée : 761 px) | 3,61 | 0,248 | 0,895 | 109,5° | 4,0 px |
| Idem, P/L imposé à 0,304 (DOC-007) | 3,29 | 0,241 | 0,792 | 100,6° | 4,7 px |
| Focale imposée de 500 à 5 000 px | 3,75 → 3,30 | 0,251 → 0,241 | 0,94 → 0,80 | 108° → 112° | 4,1 à 9,1 px |
| Axonométrie (perspective faible) | 3,68 | 0,251 | 0,923 | — | — |

**Retenu : H_corps/L = 0,246 ± 0,015 [DOC]** (robuste : 0,241–0,251 quelle que soit la méthode) ; **angle
d'ouverture 108° ± 6° [DOC]** ; profondeur du couvercle 0,125 P [DÉD, confiance faible : rebord visible sur
10–15 px].

**Comparaison avec l'Équipe A** (à L = 0,85 m) :

| Cote | Équipe E (ce modèle) | Équipe A (`dimensions.json`) | Traitement |
|---|---|---|---|
| Profondeur P | 0,260 m (L/3,27) | 0,26 m (L/3,30) | accord |
| Hauteur du corps | 0,209 m ± 0,013 (0,246 L) | 0,22 m ± 0,07 (0,85 P) | écart 0,011 m, couvert par l'incertitude |
| Épaisseur du couvercle | **0,032 m (0,125 P)** | **0,065 m (0,25 P ± 0,10)** | valeur de E conservée ; incertitude portée à l'écart : **± 0,125 P (± 0,032 m)** |
| Hauteur fermée | **0,242 m** | **0,285 m ± 0,08** | conséquence de la ligne précédente : 0,24 à 0,29 m selon l'équipe |
| Diamètre des logements | 81 mm (0,0952 L) | 77 mm (0,090 L) | écart de 4 mm, couvert par l'incertitude de pointé (± 5 mm sur le diamètre) |

Les deux estimations de l'épaisseur du couvercle viennent du même document (DOC-004) et sont toutes deux de
confiance faible ; rien ne permet de les départager. Volume extérieur fermé : 0,053 m³ ici (0,063 m³ chez A) ;
masse volumique moyenne pour 227 kg revendiqués : ≈ 4 250 kg/m³ ici, ≈ 3 600 kg/m³ chez A — dans les deux cas
plus dense que l'aluminium massif.

### 4.3 DOC-008 — tailles relatives (confiance moyenne sur le relevé, faible sur l'échelle)

Référence D = diamètre extérieur de l'anneau noir (enveloppe de refroidissement). Calage retenu :
**D = diamètre des logements de DOC-007 = 0,081 m ± 0,012 [DÉD]** (borne haute : l'entraxe, 0,093 m).

| Repère | Largeur × hauteur (en D) | À D = 0,081 m | Troisième dimension |
|---|---|---|---|
| 1 carter (disque intérieur) | Ø 0,68 | Ø 55 mm | sphère |
| 8 enveloppe de refroidissement | Ø 1,00 | Ø 81 mm | sphère |
| 2 bobines | 6 barres à ±0,28 / 0,52 / 0,77 R, calottes à 1,12 R | spires Ø 57 à 83 mm | tores [DÉD] |
| 3 générateur / régulateur de champ | 0,65 × 0,37 | 53 × 30 mm | 40 mm [HYP] |
| 4 collecteur d'injection | rampe à 0,69 D sous l'axe | — | tubes Ø 4,5 mm [HYP] |
| 5 régulateur d'électrons | 0,42 × 0,52 | 34 × 42 mm | 34 mm [HYP] |
| 6 générateur d'électrons | 0,97 × 1,75 | 78 × 142 mm | 78 mm [HYP] |
| 7 amplificateur de capteur | 0,19 × 0,19 | 15 mm | cube |
| 9 pompe | 0,79 × 0,31 | 64 × 25 mm | 32 mm [HYP] |
| 10 réservoirs (×2) | 0,66 × 1,99 | Ø 53 × 161 mm | cylindre à fonds bombés |
| 11 capteurs de gravité | ensemble 1,85 × 0,99 | 149 × 80 mm | 40 mm [HYP] |
| 12 batterie | 1,35 × 0,45 | 110 × 36 mm | 57 mm [HYP] |

Entraxe des carters sur le schéma : 1,62 D (contre 1,16 D sur DOC-007). Étendue totale du schéma : 5,2 D × 5,7 D
= 0,42 × 0,46 m, soit plus que la section intérieure du coffre (0,23 × 0,19 m) : **DOC-008 n'est pas un dessin à
l'échelle**. (L'Équipe A lit le repère 7 « Singularity status sensor » plutôt que « sensor booster », confiance
faible ; l'intitulé du modèle garde la lecture du dossier de base et devra suivre l'erratum E13 s'il est adopté.)

### 4.4 DOC-005 — enveloppe de la variante B (confiance faible)

H/L = 0,230 ± 0,03 [DOC] ; fuyantes de 0,243 L à ≈ 45° → **P/L entre 0,24 (cavalière) et 0,49 (cabinet)**,
moyenne géométrique 0,344 retenue [DÉD] ; extrémité droite en retrait de 0,092 L sur toute la hauteur, extrémité
gauche biseautée de 0,118 L sur la moitié basse. Aucune échelle : L pris égal à celui de la variante A par
convention [HYP] (soit 0,85 × 0,29 × 0,20 m).

### 4.5 Photos (DOC-003) — intérieur du couvercle (confiance moyenne à faible)

Bande 1 : 0,108–0,178 L ; bande 2 : 0,446–0,521 L ; étiquette centrale : 0,258–0,380 L ; plaque : 0,676–0,831 L ;
L / hauteur apparente du couvercle ≈ 3,67 ; 2 à 3 raies noires par bande.

## 5. Choix de modélisation

1. **Repère** : origine au coin avant-gauche-bas du corps ; X longueur, Y profondeur (charnière à l'arrière), Z
   hauteur. L'« avant » est le bas de DOC-007, côté opposé à la charnière. (L'Équipe A oriente Y de la charnière
   vers l'avant : même géométrie, sens opposé.)
2. **Coffre** : parois pleines de l'épaisseur du rebord visible en plan (0,0175 L, soit 15 mm) — simplification :
   l'épaisseur réelle de tôle est inconnue ; coins arrondis non modélisés.
3. **Platine** : pavage de dalles reprenant exactement les zones de DOC-007 ; le cadre des logements est un
   prisme percé de deux trous ; le rangement 9 est un bac ouvert (profondeur 0,41 H_corps, soit 85 mm [HYP]).
4. **Bandes de danger** : fond jaune (photos) et raies noires découpées au rectangle de la bande ; la position et
   le nombre de raies suivent DOC-007 (voir écarts E4, E5).
5. **Intérieur du couvercle** : plaque 7 (DOC-007) ; étiquette blanche à liseré rouge, étiquette orange,
   étiquette jaune et élément gris d'après les photos, transposés entre les bandes de DOC-007 [DÉD].
6. **Télécommande** : contour et détails du boîtier d'après DOC-007 [DOC], épaisseur [HYP] ; posée devant
   l'unité comme sur DOC-007. **Cordon [DÉD]** : six tronçons cylindriques lisses de 16 mm, tracé déduit (monte
   le long de la face avant et entre dans le rangement, d'où il sort sur DOC-004). Masqués à l'état fermé.
7. **Noyau** (carters, enveloppes, bobines, calottes, raccords supérieurs, amplificateurs, collecteur,
   régulateur d'électrons, régulateurs de champ) : géométrie de DOC-008 lue comme une **élévation vue en bout**
   (plan Y–Z), centrée sous les logements de DOC-007, entraxe ramené à celui de DOC-007. Le régulateur 5 est
   abaissé de 0,60 D à 0,66 D sous l'axe pour ne pas interpénétrer les bobines une fois l'entraxe réduit.
8. **Autres composants de DOC-008** (6, 9, 10, 11, 12) : tailles du schéma, **emplacement [HYP]** (disposition
   I1). **Horloges et calculateurs** : volumes génériques [HYP] proportionnels à L, existence « texte seul ».
9. **Ce qui n'est pas modélisé**, faute de document : évacuation des rayons X (aucun organe visible), câblage et
   tuyauterie (seulement schématisés en SVG), structure interne, texte des plaques, véhicule. Aucun organe
   fonctionnel n'a été ajouté pour « faire marcher » l'ensemble.
10. **Variante B** : enveloppe = prisme extrudé (translucide), 4 patins, 2 cloisons, pupitre (pont, fente 15,
    plaque 16, platine à fenêtre et bouton 17, interrupteur encadré 35), 24 volumes génériques rattachés aux
    repères 1 à 35. Le repère 8 (long tube oblique) n'est pas modélisé. Toutes les fonctions sont **inconnues**
    (pas de légende).

## 6. Hypothèses alternatives là où l'information manque

### 6.1 Disposition interne sous la platine (aucun document ne la montre)

Seule contrainte documentée : les deux carters sont sous les logements (x = 0,382 L).

| Hypothèse | Principe | Pour | Contre | Statut |
|---|---|---|---|---|
| **I1** | noyau central ; batterie sous la zone tramée gauche (divisée en deux sur DOC-007 : trappes ?) ; réservoirs et pompe à gauche du noyau ; générateur d'électrons à droite ; capteurs, horloges, calculateurs sous le pupitre | masses réparties ; électronique près des commandes ; composants lourds accessibles par la gauche | repose sur une lecture [INT] du trait de division | **retenue** (variante A) |
| **I2** | servitudes (batterie, réservoirs, pompe, horloges, calculateurs) regroupées à droite du noyau ; générateur d'électrons et capteurs dans la baie gauche | câblage court vers le pupitre | masse concentrée à droite ; baie gauche presque vide | modélisée (variante A′) |
| **I3** | symétrique : un réservoir et un régulateur de part et d'autre de chaque carter, batterie scindée en deux | cohérent avec la symétrie gauche/droite de DOC-008 | DOC-008 montre une seule batterie et une seule pompe | décrite, non modélisée |

Voir `rendus/13_dispositions_internes_I1_I2.png`. Aucune des trois n'est étayée : dans les trois cas, les
composants décrits flottent dans un coffre vide à 90 %.

### 6.2 Lecture de DOC-008

| Lecture | Conséquence | Jugement |
|---|---|---|
| (a) élévation vue depuis une extrémité du coffre | « côte à côte » = alignement en profondeur de DOC-007 ; amplificateur 7 en haut, collecteur 4 en bas | **retenue [DÉD]**, confiance moyenne à faible ; reste l'écart d'entraxe |
| (b) schéma de principe sans valeur géométrique | aucune contrainte de position | possible ; rend [HYP] tout le noyau sauf sa position en plan |
| (c) vue en plan | carters côte à côte selon la longueur : contredit DOC-007 et DOC-004 | écartée |

Sens avant/arrière de la lecture (a) : arbitraire. Le modèle place le carter de gauche du schéma sous la
singularité principale.

### 6.3 Autres indéterminations

- **Carter (1) et enveloppe (8)** : sur DOC-008, les flèches 1 et 8 aboutissent toutes deux au contour de la
  sphère. Modèle : sphère intérieure = carter, sphère extérieure translucide = enveloppe. L'inverse est possible.
- **Axe des bobines** : selon Y dans le modèle (barres de DOC-008 lues comme des spires coaxiales). Si DOC-008
  n'a pas de valeur géométrique, l'axe peut être quelconque.
- **Hauteur fermée** : 0,242 m (ce modèle) ou 0,285 m (Équipe A). Pour reproduire la valeur de A, porter
  `H_couvercle.rapport` à 0,25 et `H_corps` à 0,85 P.
- **Rapport L/P** : 3,27 (DOC-007, retenu) ou ≈ 3,6 (DOC-004 et photos), ce qui donnerait P ≈ 0,24 m.
- **Échelle** : 0,85 m retenu ; 1,20 m (H1) reste possible (probabilité de l'ordre de 5 % selon la Red Team).
- **Loquets** : 2 dans le modèle ; DOC-004 en suggère 2 ou 3, les photos montrent des ferrures rondes ailleurs.
- **Nature de DOC-005** : (a) dessin d'un autre objet réutilisé ; (b) sous-ensemble ; (c) autre modèle. La
  modélisation ne tranche pas ; elle apporte deux éléments, l'un pour (§7, C1), l'autre contre (E1).

## 7. Écarts entre documents constatés en modélisant

| N° | Documents | Écart constaté | Traitement dans le modèle | Gravité |
|---|---|---|---|---|
| E1 | DOC-005 / DOC-004, 007, 008 | Enveloppe à extrémités biseautées sur patins, sans couvercle ni bandes ; contenu mécanique dense (cylindres à ailettes, ligne d'arbre, réservoirs) sans rapport avec les 12 composants de DOC-008 ni avec les deux logements | Variante B séparée | majeure |
| E2 | DOC-007 / DOC-004 / photos | L/P = 3,22–3,33 (DOC-007) contre 3,3–3,75 (DOC-004, meilleur ajustement 3,61) et ≈ 3,67 (DOC-003) | DOC-007 retenu (seule vue orthographique) | moyenne |
| E3 | Équipe E / Équipe A (même document DOC-004) | Épaisseur du couvercle 0,125 P (E) contre 0,25 P (A) ; hauteur fermée 0,242 m contre 0,285 m à L = 0,85 m. (H1 annonçait 0,30 m pour L = 1,20 m, soit 0,21 m ramené à 0,85 m.) | valeur de E conservée, incertitude portée à l'écart | moyenne |
| E4 | DOC-007 / photos / DOC-004 | Bande 2 centrée à 0,58 L (DOC-007), ≈ 0,48 L (DOC-003), ≈ 0,5–0,57 L (DOC-004, lecture grossière) ; bandes larges de 0,097 L (DOC-007) contre ≈ 0,07 L (photos) ; plaque 7 à 0,71–0,87 L contre 0,68–0,83 L | DOC-007 retenu | moyenne |
| E5 | DOC-007 / photos | 4 raies noires par bande contre 2 ou 3 | DOC-007 retenu | mineure |
| E6 | DOC-007 / DOC-004 | Deux charnières courtes contre une tringle claire continue | 2 charnières ; tringle non modélisée | mineure |
| E7 | DOC-007 / photos, DOC-004 | L'intérieur du couvercle de DOC-007 ne porte que les bandes et la plaque 7 ; photos et DOC-004 montrent en plus 3 étiquettes et un élément gris | étiquettes ajoutées [DOC photos] | mineure |
| E8 | DOC-007 / DOC-004 | Platine : zones tramées et disques noirs (DOC-007) contre zones blanches, deux étiquettes à repères d'angle, une plaquette striée et des logements ouverts sur des formes bombées (DOC-004) | étiquettes et plaquette ajoutées [DÉD] ; sommet des carters visible dans les logements | moyenne |
| E9 | DOC-008 / DOC-007 | Carters côte à côte (DOC-008) contre logements alignés en profondeur ; entraxe 1,62 D contre 1,16 D | lecture en élévation ; entraxe de DOC-007 | moyenne (levée en partie) |
| E10 | DOC-008 / coffre | Schéma plus grand (0,42 × 0,46 m à l'échelle des carters) que la section intérieure (0,23 × 0,19 m) ; composants de DOC-008 = 9 % du volume intérieur (3,1 L sur 35 L) | tailles du schéma conservées, constat signalé | majeure pour le bilan de masse |
| E11 | DOC-007 / DOC-004, photos | Télécommande : boîtier rectangulaire à bloc de raccordement et câble en trait simple, à gauche (DOC-007) ; boîtier de type combiné, cordon spiralé, à droite (DOC-004, photos) | contour de DOC-007, cordon lisse [DÉD] | mineure |
| E12 | DOC-007 / DOC-004 | Le câble atteint la face avant à 0,958 L (DOC-007) ; le cordon sort du compartiment de droite par le dessus (DOC-004) | tracé conciliant les deux | mineure |
| E13 | texte / images | 4 horloges au césium, 3 calculateurs, évacuation des rayons X : aucune image, aucun organe visible ; repère 7 de DOC-008 sans liaison dessinée | volumes [HYP] ou omission | majeure pour la complétude |
| E14 | DOC-008 (interne) | Trait épais joignant les deux bornes de la batterie (littéralement un court-circuit) ; aucune alimentation pour la pompe 9 ni les capteurs 11 ; trait fin 11 → 9 de nature non légendée | relevé tel quel dans le schéma unifilaire | moyenne |
| E15 | DOC-004 / photos | Ferrures de la face avant : ≈ 0,11 L, (0,45 L ?), 0,74 L (DOC-004) contre ≈ 0,6 L et l'extrémité droite (DOC-002/003) | 2 loquets [DÉD] | mineure |

**Concordances notables** (à verser au dossier contradictoire) :

- **C1** — Le pupitre de l'extrémité droite de DOC-005 (fente sombre 15 ; platine à fenêtre rectangulaire et
  bouton rond bombé 17 ; interrupteur rectangulaire encadré 35 ; plaque 16) reprend, dans le même ordre et à peu
  près la même disposition avant/arrière, les organes 4, 5, 6 et 9 de DOC-007 [DÉD, confiance faible à moyenne].
  DOC-005 n'est donc pas totalement étranger au coffre.
- **C2** — H/L de DOC-005 (0,23) et du corps du coffre (0,246) sont voisins ; P/L de DOC-005 (0,24–0,49)
  encadre celui du coffre (0,306).
- **C3** — La lueur rouge de DOC-002 se trouve à l'aplomb de la fenêtre du panneau 5 de DOC-007.
- **C4** — DOC-004 confirme l'alignement en profondeur des deux logements et l'ordre des zones de DOC-007.

## 8. Données utiles aux autres équipes (à L = 0,85 m ; incertitude d'échelle ±24 % en plus)

| Grandeur | Valeur | Classement |
|---|---|---|
| Encombrement fermé | 0,850 × 0,260 × 0,242 m (hors charnières et loquets) ; hauteur 0,285 m selon l'Équipe A | [HYP] échelle, [DOC] proportions |
| Volume extérieur fermé / intérieur utile | 0,053 m³ / 0,035 m³ | [DÉD] |
| Centre du logement principal (repère du modèle) | x = 0,325 m ; y = 0,197 m | [DOC] proportions |
| Centre du logement de direction | x = 0,325 m ; y = 0,104 m | [DOC] proportions |
| Altitude supposée de l'axe des carters | z = 0,143 m | [HYP] (jeu de 10 mm sous la platine) |
| Distance entre les deux « singularités » | 0,093 m ± 0,003 (pointé) ; 0,098 m selon l'Équipe A | [DOC] proportions |
| Diamètre des logements / enveloppes | 0,081 m ± 0,005 ; 0,077 m selon l'Équipe A | [DOC] / [DÉD] |
| Diamètre moyen des spires | 0,057 à 0,083 m ; 6 spires par carter | [DÉD] |
| Volume des composants de DOC-008 | 3,1 L (9 % du volume intérieur) ; 3,7 L (10 %) avec horloges et calculateurs [HYP] | [DÉD] |
| Masse volumique moyenne pour 227 kg | ≈ 4 250 kg/m³ (≈ 3 600 kg/m³ avec la hauteur de l'Équipe A) | calcul sur données [HYP] |

Schémas : `architecture_fonctionnelle.svg` (flux revendiqués, avec distinction liaisons dessinées / texte /
hypothèses) et `schema_electrique_hypothetique.svg` (topologie relevée sur DOC-008 en noir, ajouts en tirets
roses). Aucune tension, aucun courant, aucune puissance n'est documenté ; le schéma ne dit rien de la faisabilité.

## 9. Tests effectués

- **Paramétrage** : reconstruction avec L = 0,65 ; 0,85 ; 1,00 ; 1,20 et 1,25 m (copies de `parametres.json`) :
  173 pièces régénérées à chaque fois, **aucune interférence** (`mesures/verifier_interferences.py`).
- **Exports** : relecture par trimesh des GLB (173 nœuds), OBJ et STL ; étendues conformes (fermé : 0,858 ×
  0,280 × 0,242 m avec charnières et loquets). Non testés dans un logiciel de CAO ou un trancheur.
- **Rendus** : les 14 PNG régénérés à 0,85 m ; `04_interieur_composants` et `05_eclate` rouverts et contrôlés
  (plus de chevauchement des volumes génériques ; cordon passé en orange [DÉD] ; mention d'échelle à 0,85 m).
- **Visionneuse** : syntaxe du script vérifiée (`node --check`), JSON embarqué relu (386 pièces, bilan 88 / 52 /
  33) ; page ouverte dans le navigateur de prévisualisation (three.js r128 chargé depuis cdnjs) et pilotée par
  script : quatre états (0°, 108°, 180°, éclaté ; 159 pièces visibles fermé, 173 ouvert), variantes A (173),
  A′ (173), B (40), en-tête « L = 0,85 m ± 0,20 m », clics simulés sur quatre pièces — fiches correctes, dont
  le cordon ([DÉD], existence « DOC image », appui « dessin + photo ») et une horloge (32 × 64 × 32 mm, « texte
  seul ») —, glisser (rotation) ; aucune erreur JavaScript. Les tests de la version 1.0 (modes de couleur,
  enveloppes translucides, filtres, thème sombre forcé, molette, recherche, mise en page à 1280 × 800,
  375 × 812 et 268 × 340 px) n'ont pas été rejoués après les corrections : le code correspondant n'a pas changé.
  **Non testés** : bascule automatique `prefers-color-scheme: dark` (le panneau de prévisualisation impose le
  thème clair aux fichiers locaux), gestes tactiles réels (pincement), Safari et Firefox, ouverture hors
  connexion (un message d'erreur est prévu si three.js ne se charge pas).

## 10. Limites

1. **Échelle** : une seule estimation de confiance faible (0,85 m ± 0,20 m, plage 0,65–1,25 m). Toute dimension
   absolue est à ±24 % au mieux.
2. **Sources** : copies de basse résolution (DOC-004 : 477 × 440 px tramé ; DOC-008 : 415 × 580 px, légende
   à peine lisible). Les pointés manuels sont reproductibles mais subjectifs à 1–3 px près. L'Équipe A a
   travaillé sur de meilleures copies de DOC-007 (460 × 600 px) : ses rapports concordent avec les nôtres à
   quelques pour cent près, sauf l'épaisseur du couvercle (§4.2).
3. **DOC-007 fait foi pour le plan** par choix de méthode (seule vue orthographique) ; or les photos et DOC-004
   s'en écartent sur plusieurs points (E2, E4, E5). Le modèle reproduit le dessin du manuel, pas nécessairement
   l'objet photographié : 48 des 88 pièces [DOC] n'ont que ce dessin pour appui.
4. **Intérieur** : rien n'est documenté sous la platine — 0 pièce [DOC] sur 64 ; tout le noyau est [DÉD] au
   mieux, le reste [HYP]. La lecture de DOC-008 en élévation est une proposition, pas un fait.
5. **Troisième dimension** : pour presque toutes les pièces de la platine et du couvercle, l'épaisseur et le
   relief sont supposés ; seule l'emprise en plan est lue sur les documents.
6. **Simplifications géométriques** : primitives seulement, coins vifs, parois pleines, cordon lisse, pas de
   visserie, pas de texte. Les volumes de la variante B sont des approximations grossières d'une vue unique
   (profondeurs supposées).
7. **Aucune validation physique** : le modèle ne dit rien de la plausibilité d'un quelconque fonctionnement. Les
   intitulés (« singularité », « générateur d'électrons », etc.) sont des citations des légendes.
8. **Fichiers non conservés** : les recadrages quadrillés ayant servi aux pointés ont été produits dans un
   répertoire temporaire ; seuls les pointés et les images de contrôle sont archivés.
9. **Rendu** : logiciel, ombrage plat, sans ombres portées ; les images sont illustratives.

## 11. Reproduire

```sh
cd 06_modele_3D
./reconstruire.sh              # modèle, contrôle d'interférences, exports, rendus, visionneuse, nomenclature, schémas (≈ 20 s)
./reconstruire.sh --mesures    # relance aussi la mesure des proportions sur les originaux
```

Dépendances : l'environnement `.venv` du projet (numpy, scipy, pillow, shapely, trimesh, matplotlib) ; aucun
paquet ajouté. Ouvrir `visionneuse.html` dans un navigateur connecté à Internet (three.js r128 via cdnjs).

---

## Journal des corrections post-validation

Corrections de la Red Team n° 2 (`08_red_team/CORRECTIONS_A_APPLIQUER.md`, §5 ; `RAPPORT_RED_TEAM_2.md`, §1 et
§6.4), appliquées le 10 novembre 2026. État de départ : la direction avait porté `echelle.L` de 1,20 m à 0,85 m,
rendu dynamiques les mentions d'échelle des scripts et ajouté une note en tête de ce rapport.

| N° | Correction demandée | Suite donnée |
|---|---|---|
| 46 | Mettre le corps du rapport à l'échelle des sorties (0,85 m) | **Appliquée.** Toutes les cotes absolues des §1, 3.3, 4, 5, 6.3, 7, 8, 9 et 10 sont recalculées à partir de `modele_c204.json` ; la note de tête de la direction est retirée. **Le chiffre proposé (« 14 %, 4,7 L sur 35 L ») n'est pas repris** : voir ci-dessous. |
| 47 | Présenter le bilan par couche | **Appliquée** (§1, §10 et `NOMENCLATURE.md` §1, champ `bilan_couches` du modèle) : extérieur 88 / 18 / 3, **intérieur 0 / 34 / 30**. Décomptes vérifiés sur les sorties : **42** motifs répétés (20 raies, 4 fonds, 18 pastilles) et non 45 ; **48** pièces [DOC] appuyées sur le seul dessin DOC-007 (46 dont la source est exactement « DOC-007 », plus les 2 charnières) et non 46. Distinction « [DOC] dessin » / « [DOC] photo » ajoutée (champ et colonne `appui`). |
| 48 | Cordon de la télécommande [DOC] → [DÉD] | **Appliquée** (6 pièces ; existence « DOC image » conservée). Nouveau bilan : **88 [DOC], 52 [DÉD], 33 [HYP]**. |
| 49 | Colonne `dimensions_H1` → `dimensions` | **Appliquée** (`generer_nomenclature.py`, `nomenclature.csv`). |
| 50 | Harmoniser avec l'Équipe A | **Appliquée** selon la consigne de la direction : valeurs nominales conservées, incertitude portée à l'écart, valeur de A citée. `H_couvercle` : 0,125 P **± 0,125 P** (A : 0,25 P) ; hauteur fermée 0,242 m (A : 0,285 m) ; logements Ø 81 mm ± 5 (A : 77 mm, écart déjà couvert) ; hauteur du corps et entraxe : valeur de A citée. Tableau comparatif au §4.2. |

**Écart assumé par rapport à la correction n° 46 — le taux d'occupation.** Le « 14 % » relevé par la Red Team
dans les sorties régénérées à 0,85 m était un artefact : les sept volumes génériques [HYP] (4 horloges,
3 calculateurs) gardaient une taille absolue fixée pour un coffre de 1,20 m. À 0,85 m, ils provoquaient
**18 interférences** (horloges traversant la paroi avant, horloges et calculateurs imbriqués, un calculateur
dans le bac de rangement), détectées par le nouveau contrôle `mesures/verifier_interferences.py`. Ces cotes ont
été rendues proportionnelles à L (mêmes valeurs qu'avant à 1,20 m) ; le modèle n'a plus d'interférence de 0,65 à
1,25 m, et le taux devient **9 % pour les composants de DOC-008 seuls (3,1 L sur 35 L), 10 % avec les volumes
génériques (3,7 L)**. Le constat de fond est inchangé (environ 90 % du volume n'est pas décrit), mais tout
document du programme qui cite « 14 % (4,7 L sur 35 L) » doit être aligné sur ces valeurs.

**Point non modifié, signalé** : l'étiquette de L reste [HYP] dans `parametres.json` alors que l'Équipe A écrit
[DÉD] ; la Red Team relève elle-même que quatre des cinq méthodes d'étalonnage reposent sur un étalon supposé.
L'arbitrage revient à la direction.

**Corrections ajoutées de notre propre chef** (découlant du changement d'échelle) : profondeur du rangement,
épaisseur de la télécommande, loquets, plaquette signalétique et décalages de la vue éclatée rendus
proportionnels ; contrôle d'interférences intégré à `reconstruire.sh` ; réserve sur la troisième dimension
ajoutée à la définition du classement [DOC] ; sources de `parametres.json` débarrassées des références à H1
devenues inexactes ; champ `appui` affiché dans les fiches de la visionneuse.

**Tests refaits après corrections** : `reconstruire.sh` complet ; contrôle d'interférences à cinq échelles ;
relecture visuelle de `04_interieur_composants.png` et `05_eclate.png` ; `node --check` sur le script de la
visionneuse ; visionneuse rouverte dans le navigateur (états, variantes, quatre fiches, rotation, aucune erreur).

## Simulateur 3D interactif (ajout postérieur à la validation)

`simulateur.html` est une page unique et autonome (données embarquées ; seule ressource externe : three.js r128
sur cdnjs), produite par `generer_simulateur.py` à partir de `simulateur_gabarit.html`, de `modele_c204.json` et,
en lecture seule, de `../10_machine_optimisee/modele_c204_R1.json`. `reconstruire.sh` la régénère ;
`visionneuse.html` n'est pas modifiée. Quatre onglets :

1. **Explorer** — l'objet tel que décrit : fermé ou ouvert, éclatement continu de 0 à 100 % avec étiquettes
   reliées aux sous-ensembles, couleurs par niveau de preuve, fiche de la pièce au clic.
2. **Si elle fonctionnait (selon le récit)** — frise en sept étapes ; « champ » de DOC-009 à l'échelle du texte
   ou de DOC-014 (attribution non établie) ; véhicule schématique [HYP]. Bandeau permanent : « Reconstitution
   d'un récit — aucune de ces images ne correspond à un phénomène observé ».
3. **Ce que dit la physique** — conséquences réelles des chiffres du récit, chaque nombre accompagné de sa
   formule ; coefficients relus dans les sorties des Équipes B et C.
4. **C204-R1 (constructible)** — instrument de l'Équipe I, signaux simulés et annoncés comme tels ; le décalage
   relativiste d'un trajet est « subi par tout objet sur ce trajet ; R1 le calcule, il ne le produit pas ».

**Valeurs de contrôle** (mêmes formules en Python à la génération et en JavaScript dans la page, écart relatif
inférieur à 0,2 %) : P·M² = 7,68×10³³ W·kg² ; 5,06×10¹² kg à 300 MW et 3,92×10¹² kg à 500 MW ; 53,3 à 68,9 g à
1 m pour deux singularités ; photons d'une singularité de 400 MW : 3,45×10³ Gy/s à 1 m et 384 Gy/s à 3 m ;
surface du coffre 1,07 m² ; Γ − 1 de 1,5×10⁻¹⁴ à 1,5×10⁻¹⁵ ; 6,05×10⁻¹³ s pour 113,5 kg ; 2,04×10¹⁹ J pour
227 kg ; 127 coïncidences de muons par heure ; trajets : −0,5013, −1,3279, −0,3927, +0,3926 et +6,2380 ns/h.

**Choix à connaître.** Le coefficient d'absorption retenu pour la dose est celui de l'eau à 15 MeV
(1,441×10⁻² cm²/g), qui reproduit le recalcul de la Red Team ; le script c05 de l'Équipe C prend la valeur à
20 MeV (3,31×10³ Gy/s à 1 m). Le véhicule, sa cabine double, la place de l'unité à l'arrière de la benne et le
repère de l'occupant sont des volumes schématiques [HYP]. Le rayon des anneaux du « champ » suit les
proportions relevées en pixels sur DOC-009 ; les bruits, la panne injectée (+1,7 ns/h) et le seuil du voteur
(0,01 ns/h) du mode 4 sont des valeurs de démonstration affichées dans la page.

**Essais** : `node --check` ; 143 contrôles automatisés (`node essais_simulateur.mjs`, tous réussis) dans Chrome
sans tête piloté par le protocole DevTools
(clics, glissements, molette, pincement et clavier réels) à 1280×800 et à 375×812, plus thème sombre, mouvement
réduit et CDN bloqué ; captures dans `rendus/simulateur_*.png`. Non essayé : Safari, Firefox, un vrai
téléphone, un lecteur d'écran, un ordinateur sans carte graphique récente.

# Fiche F5 — Alimentation par batteries et bilan énergétique global (réponse à Q3)

Repère : DOC-008 r.12 (« battery supply »).
Calculs : `calculs/c06_alimentation_bilan.py` → `bilan_energetique.csv` (livrable), `resultats/c06_alimentation.json`.

## 1. Ce que dit la source

**[DOC texte]** « The electricity comes from batteries » ; « the real energy is in creating the machine, not
operating it » ; « the energy stored in the singularity is used to create the distortion fields. That energy
is created in a particle accelerator » ; singularités « created, captured and cleaned » dans un grand
accélérateur circulaire ; « E = MC squared can be solved for mass too ».
**[DOC]** DOC-008 r.12 : un boîtier à six éléments et deux bornes — l'iconographie d'une batterie au plomb de 12 V.

Lecture charitable : la source ne prétend pas que la batterie fournit l'énergie du déplacement ; elle alimente
les auxiliaires, et l'énergie « réelle » est stockée dans les singularités lors de leur fabrication. C'est cette
lecture que nous chiffrons.

## 2. Ce qu'une batterie embarquable contient

| Pack | Masse | Volume [HYP] (part des 35 L utiles) | Énergie | Puissance soutenue [HYP] |
|---|---|---|---|---|
| Plomb 12 V 60 Ah (ce que montre le dessin) | 17 kg | 9 L (26 %) | 0,72 kWh = 2,6 MJ | 2,5 kW |
| **Pack LiFePO₄ logeable (Équipe I, palier R1)** | 9,5 kg | 4 L (11 %) | **1,34 kWh = 4,8 MJ** | 2,9 kW |
| Plomb-acide à 30 Wh/kg | 50 kg | 20 L (57 %) | 1,5 kWh = 5,4 MJ | 7,5 kW |
| **Pack Li-ion à 150 Wh/kg (référence des comparaisons)** | 50 kg | 30 L (86 %) | **7,5 kWh = 27 MJ** | 25 kW |
| Cellules Li-ion nues à 270 Wh/kg | 50 kg | 20 L (57 %) | 13,5 kWh = 49 MJ | 40 kW |
| Borne haute : toute l'unité en pack Li-ion à 180 Wh/kg | 227 kg | 136 L (389 %) | 41 kWh = 147 MJ | 113 kW |
| Borne chimique : 12 kWh/kg (hydrocarbure + air) [HYP] | 50 kg | 65 L (186 %) | 600 kWh = 2,2 GJ | — |

Le pack de 50 kg reste la référence des comparaisons d'énergie (borne généreuse), mais il occuperait à lui seul
86 % du volume utile du coffre de 0,85 m : dans ce coffre, la batterie réellement logeable avec le reste est de
l'ordre de 1,3 kWh. **[DÉD]**

Densités : National Academies 2020 (plomb ≈ 30 Wh/kg ; packs Li-ion 120–180 Wh/kg) ; Frith et al. 2023
(cellules ≥ 270 Wh/kg). **[VÉR]**

## 3. Besoins sous-système par sous-système (extrait de `bilan_energetique.csv`)

| Poste | Puissance | Énergie sur 6 h | Écart à 27 MJ | Verdict |
|---|---|---|---|---|
| 4 horloges CSAC | 0,48 W | 10 kJ | −3,4 décades | compatible |
| 4 étalons à jet de césium 5071A | 200 W | 4,3 MJ | −0,8 | compatible |
| 3 calculateurs + voteur [HYP] | 90 W | 1,9 MJ | −1,1 | compatible |
| Gravimètre CG-6 / gravimètre quantique AQG-B | 5,2 W / 500 W | 0,11 / 10,8 MJ | −2,4 / −0,4 | compatible |
| Canon à électrons 100 kV × 1 mA | 100 W | 2,2 MJ | −1,1 | compatible |
| **Total auxiliaires** | **0,23 à 0,92 kW** | **1,4 à 5,5 kWh** | −0,7 à −0,1 | **compatible** |
| Cryoréfrigérateur d'aimant supraconducteur [HYP] | 7 kW | 151 MJ | +0,7 | hors batterie sur 6 h |
| Aimant hybride de 45 T (MagLab : 30–33 MW) | 33 MW | 7×10¹¹ J | +4,4 | impossible |
| Pompe de refroidissement (353 MW thermiques) | 2,3 MW | 4,9×10¹⁰ J | +3,3 | impossible |
| Chaleur à évacuer (2 × 400 MW, γ + e±) | 353 MW | 7,6×10¹² J | +5,5 | — |
| Énergie rayonnée par 2 singularités de 400 MW | 800 MW | 1,7×10¹³ J (0,19 g de masse) | +5,8 | fournie par les singularités |
| Champ de 5,1×10¹¹ T dans 1 litre | — | 1,05×10²⁶ J | +18,6 | impossible |
| +1 % de masse sur 4,4×10¹² kg | — | 3,9×10²⁷ J | +20,2 | impossible |
| Rotation maximale de 4,4×10¹² kg | — | 7,6×10²⁸ J | +21,4 | impossible |
| Charge extrémale de 4,4×10¹² kg (½ M c²) | — | 2,0×10²⁹ J | +21,9 | impossible |
| **Création de 2 × 100 kg** | — | **1,8×10¹⁹ J** | +11,8 | impossible (et inutile : 4×10⁻¹³ s) |
| **Création de 2 × 1,47×10¹¹ kg (2 g à 1 m à elles deux)** | — | **2,64×10²⁸ J** | +21,0 | impossible |
| **Création de 2 × 4,4×10¹² kg (400 MW chacune)** | — | **7,9×10²⁹ J** | +22,5 | impossible |

## 4. Réponse à Q3 — énergie nécessaire

1. **Fonctionnement des auxiliaires** (ce qui est réellement constructible) : 1,4 à 5,5 kWh par trajet de 6 h
   en configuration complète ; 0,75 kWh (126 W) en configuration logeable — horloges miniatures, trois
   calculateurs, gravimètre relatif, pupitre —, que couvre un pack logeable de 1,34 kWh. Une batterie suffit.
   **[DÉD]**, confiance élevée.
2. **Fabrication des singularités** : E = 2 M c², rendement supposé de 100 %.
   - masses exigées par « 300–500 MW » : 7,9×10²⁹ J = 7×10⁹ années de production électrique mondiale
     (29 925 TWh en 2023) = 1,3×10⁹ années d'énergie primaire mondiale (620 EJ) = 34 minutes de la luminosité
     totale du Soleil ;
   - masses exigées par « 2 g à 1 m » (2,94×10¹¹ kg au total, soit 2 × 1,47×10¹¹ kg) : 2,64×10²⁸ J = 2,4×10⁸ années de
     production électrique mondiale = 69 s de Soleil — c'est aussi l'énergie de la question Q4 (fiche F9) ;
   - masses compatibles avec 227 kg (2 × 100 kg) : 1,8×10¹⁹ J = 17 % de la production électrique mondiale d'une année.
   **[DÉD]**, confiance élevée (simple équivalence masse-énergie).
3. **Aucun trajet intermédiaire n'existe** (« fabriquer petit, puis faire grossir ») **[DÉD]**, confiance moyenne :
   - un accélérateur ne peut au mieux former qu'un trou noir de l'ordre de l'énergie de collision. En gravitation
     à quatre dimensions le seuil est la masse de Planck, 1,22×10¹⁹ GeV, soit 9×10¹⁴ fois l'énergie du LHC
     (13,6 TeV). Les scénarios à dimensions supplémentaires (Dimopoulos & Landsberg 2001 ; Giddings & Thomas 2002)
     sont **spéculatifs** et exclus par CMS jusqu'à ~10 TeV ; ils donneraient des objets de 10⁻²³ kg vivant ~10⁻²⁶ s ;
   - un trou noir de masse m s'évapore avec P = α ħc⁶/(G²m²) et ne peut absorber qu'à travers σ = 27πG²m²/c⁴.
     Le bilan n'est positif que si m⁴ > α ħ c¹⁰/(27π G⁴ S), S étant le flux d'énergie incident. Même plongé dans
     de la matière à densité nucléaire arrivant à la vitesse de la lumière (S = 6×10⁴² W/m²), il faut
     **m > 7×10¹⁰ kg** ; avec le laser le plus intense jamais réalisé (10²³ W/cm² ; Yoon et al. 2021),
     m > 6×10¹⁴ kg. En dessous, le trou maigrit plus vite qu'on ne peut le nourrir ;
   - il faudrait donc créer d'emblée ~10¹¹ kg, c'est-à-dire concentrer ~10²⁸ J dans ~10⁻¹⁶ m en ~10⁻²⁵ s
     (puissance ~10⁵² W). Un trou de 100 kg, lui, exigerait 7,5×10³⁰ W d'apport permanent, soit 2×10⁴ fois la
     luminosité du Soleil, à travers une cible de 10⁻⁴⁹ m².
4. **Énergie du « déplacement » lui-même** : aucune grandeur physique ne définit l'énergie d'un trajet vers le
   passé. À titre de repère seulement, obtenir le rapport 10 ans par heure (facteur 87 660) par dilatation
   cinématique — donc vers le futur uniquement — coûterait (γ − 1) m c² = 2×10²⁵ J pour 2 500 kg.

## 5. Classement

| Élément | Statut | Constructible aujourd'hui ? |
|---|---|---|
| Batterie alimentant horloges, calculateurs, capteurs, canon à électrons | Démontré | **Oui** — pack LiFePO₄ logeable de 1,34 kWh avec BMS (9,5 kg, 4 L) pour la configuration réduite (0,75 kWh par trajet) ; un pack de 7,5 kWh (50 kg, ≈ 30 L) n'entre pas avec le reste dans 35 L |
| Batterie alimentant pompes et aimants de l'architecture | Contredit (2 à 4 décades) | Non |
| Batterie comme source primaire de l'effet | **Contredit** (conservation de l'énergie : 21 à 23 décades) | Impossible |
| Création de micro-trous noirs dans un accélérateur | **Spéculatif** (dimensions supplémentaires) ; **contredit** aux masses requises | Non |

## 6. Limites

Les puissances des auxiliaires marquées **[HYP]** sont des estimations d'ingénieur. Le critère de croissance
ignore la pression de radiation et la collimation du flux, qui le durcissent. Les comparaisons énergétiques
utilisent les chiffres 2023 de l'Energy Institute (lus via un résumé, site primaire inaccessible).

# Programme C204 — Rapport de l'Équipe D (mathématiques et simulation numérique)

Version 2 — 11 novembre 2026 (révisée après la validation contradictoire, phase 7 ; voir le journal en fin de rapport). Dossier : `05_simulations/`.

> **Avertissement.** Toutes les simulations de ce dossier sont **illustratives**. Elles traduisent des
> hypothèses en nombres ; elles ne constituent **en aucun cas une preuve expérimentale**. Aucune affirmation
> de « John Titor » n'est tenue pour vraie ; le voyage temporel n'a jamais été démontré. Ne pas confondre :
> dilatation du temps ≠ voyage dans le passé ; champ électromagnétique ≠ champ gravitationnel ;
> simulation ≠ expérience.

Étiquettes du dossier de base : **[DOC]** documenté, **[DÉD]** déduit, **[HYP]** hypothèse, **[INT]** interprétation de tiers,
**[VÉR]** fait vérifiable indépendamment.

---

## 1. Modèle global

Le corpus revendique [DOC texte] : deux « micro-singularités » chargées en rotation, dans une unité de 227 kg, produisant
300–500 MW, 1,5–2 g, et un déplacement de « 10 ans par heure » par un « sinusoïde de Tipler » imitant un champ de Kerr.
Nous n'avons pas simulé « la machine » — il n'existe aucun modèle physique à simuler — mais **chaque brique physique invoquée**,
prise séparément, en demandant à chaque fois : *que vaudrait cette grandeur, et à quelle échelle ?*

| Sim. | Question posée | Cadre théorique | Statut du cadre |
|---|---|---|---|
| S01 | Quelle masse donne 300–500 MW ? Vit-elle assez longtemps ? Tient-elle dans 227 kg ? | Rayonnement de Hawking semi-classique | Théoriquement possible (non observé) |
| S02 | Où sont horizons, ergosphère, région à CTC d'un trou noir de Kerr(-Newman), et à quelle échelle en mètres ? | Solutions exactes de la RG | Démontré (extérieur) / Spéculatif (r < r₋) |
| S03 | Que fait une particule qui tombe « à travers l'anneau » ? Quelle dilatation maximale ? | Géodésiques de Kerr | idem |
| S04 | Quand un cylindre de Tipler produit-il des CTC, et avec quelle masse ? | Solution de van Stockum | Spéculatif (cylindre infini) |
| S05 | Quels champs (g, marées, dilatation, entraînement, ondes) produisent deux masses à 1–3 m ? | Newton + RG linéarisée | Démontré |
| S06 | Peut-on retenir une singularité chargée par des champs électromagnétiques ? | Électrodynamique classique, pièges de Penning/Paul | Démontré (pour des ions) |
| S07 | Combien d'énergie négative pour un trou de ver ou une bulle de distorsion d'un mètre ? | RG + effet Casimir | Spéculatif / Démontré (Casimir) |
| S08 | À quoi ressemble géométriquement le schéma DOC-009 (et sa variante cotée DOC-014) ? | Analyse d'image + ajustements (description, non test physique) | — |
| S09 | Les conclusions dépendent-elles des hypothèses de lecture ? | Monte-Carlo, sensibilité | — |

Code : Python 3.12 (numpy, scipy, matplotlib, sympy, pillow) ; module commun `c204_commun.py` (constantes CODATA 2018, valeurs
revendiquées, mention obligatoire sur chaque figure, registre de tests) ; un script par simulation ; `run_all.sh` relance tout
(≈ 3 min 15 s) ; graines aléatoires fixées (204 ; 2040 pour le rejeu de la méthode abandonnée de S08).

## 2. Équations principales

- **Hawking** : r_s = 2GM/c² ; T = ħc³/(8πGMk_B) ; P_γ,corps noir = ħc⁶/(15360πG²M²) ; P_tot = α f(M)c²/M² (α = 5,34×10²⁵ g³/s) ;
  dM/dt = −α f(M)/M² ; τ = ∫M²dM/(αf).
- **Kerr-Newman** : Δ = r² − 2Mr + a² + Q² ; Σ = r² + a²cos²θ ; r± = M ± √(M² − a² − Q²) ; ω = −g_tφ/g_φφ ; CTC ⇔ g_φφ < 0.
- **Géodésiques** : Σ² ṙ² = R(r) = [(r² + a²)E − aL]² − Δ[μ²r² + (L − aE)² + Q] ; Σ² θ̇² = Θ(θ) ; temps de Mino dτ = Σ dλ.
- **van Stockum-Tipler** : ds² = H(dr² + dz²) + L dφ² + 2M dφ dt − F dt² ; CTC là où L < 0 — à l'extérieur : zones L < 0 dès que aR > 1/2 ; dans la matière : ar > 1 ; μ = a²R²c²/(2G).
- **Champ faible** : Φ = −ΣGM/r ; dt/dτ − 1 = −Φ/c² ; Ω_LT = (G/c²r³)[3(J·n)n − J] ; P_OG = (32/5)G⁴m₁²m₂²(m₁ + m₂)/(c⁵d⁵).
- **Pièges** : Q/M ≤ √(4πε₀G) ; E_lév = g/(Q/M) ; Penning stable ⇔ ω_c² > 2ω_z² ; Paul : équation de Mathieu, q_max = 0,908.
- **Énergie négative** : Morris-Thorne τ₀ = c⁴/(8πGb₀²), M = −b₀c²/(2G) ; Alcubierre E = −(c²v²/12G)∫r²f′²dr ; Casimir u = −π²ħc/(720d⁴).

Détails, variables, conditions initiales et aux limites : README de chaque dossier SNN.

## 3. Résultats et degré de confiance

| # | Résultat | Valeur | Confiance |
|---|---|---|---|
| 1 | Coefficients du dossier §6 (r_s, T, P corps noir, τ corps noir, Q_max/M) | confirmés à < 0,2 % | élevée |
| 2 | Masse d'une singularité donnant 300–500 MW (photons, corps noir) | 8,4×10¹¹ – 1,1×10¹² kg | élevée |
| 3 | Idem en comptant toutes les espèces émises | 3,9×10¹² – 5,0×10¹² kg | moyenne |
| 4 | Masse donnant 1,5–2 g entre 1 et 3 m | 2,2×10¹¹ – 2,6×10¹² kg | élevée |
| 5 | **Écart avec l'unité de 227 kg** | **9,9 ordres de grandeur** ; 0 tirage compatible sur 200 000 | élevée |
| 6 | Trou noir de 113 kg : durée de vie ; puissance | 5,9×10⁻¹³ s ; 5,7×10³⁰ W (≈ 2,4 Gt de TNT libérées) | moyenne (ordre de grandeur : élevée) |
| 7 | Trou noir de 10¹² kg : température ; puissance totale | k_BT = 10,6 MeV (γ, e±, ν, pas des rayons X) ; 7,8 GW | moyenne |
| 8 | Taille de toute la structure de Kerr (10¹² kg) ; région à CTC | ~10⁻¹⁵ m ; ≤ GM/c² = 7×10⁻¹⁶ m, en r < 0, derrière r₋ | élevée (calcul) / faible (réalité de r < r₋) |
| 9 | Masse pour une structure de Kerr d'un mètre | 1,35×10²⁷ kg (0,71 masse de Jupiter) | élevée |
| 10 | Passage par le disque de l'anneau : conditions | constante de Carter < 0 ; sur l'axe E² > 1 + M/a (E > 1,45 pour a = 0,9 M) ; sinon rebond ou singularité | élevée (calcul) |
| 11 | Dilatation maximale sur orbite stable ; condition pour 87 660 | 10,8 (a = 0,998 M) ; statique à 1,9×10⁻²⁵ m de l'horizon (10¹² kg) | élevée |
| 12 | Cylindre de Tipler : seuil des CTC | aR > 1/2 ; μ ≥ c²/(8G) = 1,7×10²⁶ kg/m, cylindre infini | élevée (calcul) |
| 13 | Idem avec 227 kg par mètre | il manque 7×10²³ en masse | élevée |
| 14 | Pesanteur à 1 m de 2 × 113 kg | 1,5×10⁻⁹ g (revendiqué : 1,5–2 g) | élevée |
| 15 | Uniformité de « 1,5–2 g » | impossible : coquille de 15,5 % du rayon ; 6 g de marée sur 1 m | élevée |
| 16 | Dilatation à 1 m de 2 × 10¹² kg (resp. 2 × 113 kg) | 1,5×10⁻¹⁵ (1,7×10⁻²⁵) contre 87 660 : 20 (30) ordres de grandeur ; mauvais signe pour un retour vers le passé | élevée |
| 17 | Entraînement des référentiels à 1 m ; ondes gravitationnelles ; coalescence | d = 0,30 m [HYP] : ≤ 5×10⁻¹⁴ rad/s ; ≤ 10⁻¹⁶ W ; ≥ 10²³ ans. d = 0,098 m (entraxe documentaire, DOC-007) : ≤ 2,5×10⁻¹⁴ rad/s ; ≤ 2×10⁻¹⁴ W ; ≥ 3×10²¹ ans (pour 2 × 10¹² kg : 377 rad/s, 2,3×10²³ ans) | élevée |
| 18 | Champ de lévitation et piège de Penning à la charge extrémale | 1,1×10¹¹ V/m ; 7×10¹¹ T (> magnétar) | élevée |
| 19 | Charge d'un micro-trou noir | borne supérieure ~137 e (ordre de grandeur) ; valeur typique ≈ 6 e (valeur quadratique moyenne, Page 1977) → champs requis > champ de Schwinger | moyenne |
| 20 | Poids transmis au véhicule (10¹² kg) | 9,8×10¹² N, 10⁹ fois la charge utile d'un pick-up | élevée |
| 21 | Énergie négative : trou de ver de 1 m ; bulle d'Alcubierre de 3 m | −6,7×10²⁶ kg ; −2,7×10²⁷ kg ; ~10⁴³ fois ce que l'effet Casimir fournirait | élevée (calcul) / moyenne (comparaison) |
| 22 | DOC-009 et sa variante DOC-014 (description géométrique, **sans valeur de test physique**) | contours elliptiques de rapport d'axes ≈ 1,6 ; anneaux alignés sur une ellipse (RMS 1,1 px ; validation croisée 5 px, critère de 3 px non satisfait) ; système décentré de 0,22 A par rapport aux masses ; entonnoir asymétrique ; aucune sinusoïde. Forme d'horizon (Kerr-Schild) et d'ergosurface non retrouvées sur le sphéroïde central — **zone que le document déclare lui-même hors d'échelle (« This area is not to scale ») ; la forme d'un horizon dépend en outre des coordonnées : résultat descriptif, sans valeur de preuve**. DOC-009 ne porte aucune cote ; DOC-014 (attribution non établie) porte quatre distances en mètres, à peu près proportionnelles au dessin (dispersion 9 %) et incompatibles avec les distances du texte (demi-envergures de 13 à 18 m contre 3,0–3,7 m). Mêmes constats sur les trois copies analysées (11 énoncés sur 12) | moyenne (description) / faible (comme argument physique) |
| 23 | Cohérence interne puissance ↔ pesanteur (sans la masse de l'unité) | 56 % des lectures « photons, corps noir », 1,5 % des lectures « toutes espèces » | moyenne (dépend des distributions [HYP]) |

**Lecture d'ensemble.** (i) La contrainte de masse de l'unité est incompatible avec toutes les autres revendications chiffrées, de 9 à
13 ordres de grandeur, quelle que soit la lecture. (ii) Les chiffres « 300–500 MW », « taille d'un électron ↔ masse d'une montagne » et
« 2 g à ~1 m » se recoupent autour de 10¹² kg **si** l'on ne compte que les photons d'un corps noir — lecture qui est celle des
vulgarisations des années 1970-1990 sur les trous noirs primordiaux ; cet accord se défait (facteur 1,5 à 20) dès que l'on compte toutes
les espèces émises. (iii) Même en accordant des masses de 10¹² kg, la dilatation temporelle, l'entraînement des référentiels et la taille
de la région à CTC restent 15 à 20 ordres de grandeur en deçà de ce que le récit exige, et aucun champ électromagnétique ne peut retenir
ni alléger de tels objets. (iv) DOC-009 ne porte aucune cote ; sa variante DOC-014 (attribution non établie) porte quatre distances en mètres, à peu près proportionnelles au dessin (dispersion 9 %) et incompatibles avec les distances du texte ; la géométrie du schéma ne correspond à aucune famille de surfaces physiques mieux qu'à des ellipses génériques (constat descriptif, sans valeur de preuve).

Ces résultats **n'établissent pas** l'intention ni l'identité de l'auteur, et ne « réfutent » pas une physique inconnue : ils montrent que
les grandeurs avancées sont incompatibles entre elles et avec la physique connue.

## 4. Tests de validation

**160 tests de validation, tous passés, et 23 contrôles, résultats ou repères consignés hors décompte** (`journal_run_all.txt`, `resultats_globaux.json`) :

| | S01 | S02 | S03 | S04 | S05 | S06 | S07 | S08 | S09 | Total |
|---|---|---|---|---|---|---|---|---|---|---|
| Tests de validation | 18 | 17 | 41 | 25 | 11 | 20 | 12 | 9 | 7 | **160** |
| Hors décompte | 1 | 0 | 0 | 0 | 0 | 0 | 1 | 21 | 0 | **23** |

Un **test de validation** confronte le code à une réponse connue indépendamment et peut échouer. Sont consignés **hors décompte** : 18 contrôles de l'ajustement sur
lui-même (S08), 3 énoncés de résultat (S08), 1 repère non vérifié (S07) et 1 biais de modèle documenté (S01).

**Rapprochement avec la Red Team.** La version 1 annonçait « 181 tests ». La Red Team a montré que 17 des 28 « tests » de S08 n'en étaient pas (2 énonçaient la conclusion,
15 contrôlaient l'ajustement sur lui-même) : avec cette seule correction (n° 39), le décompte est de **164 tests de validation et 17 contrôles ou résultats**. Nous avons en
outre sorti le repère Pfenning & Ford (n° 41 → 163), la comparaison de M* qui relève d'un biais de modèle (n° 42 → 162) et, par le même critère, deux autres éléments de S08
(le constat sur les anneaux, qui est un résultat, et l'affinage des ancres, borné par construction → 160). Deux contrôles nouveaux de la phase 7 (second contour E2, rejeu de la
méthode abandonnée) portent le hors-décompte à 23. Hors S08, les tests restants sont inchangés à ces deux retraits près.

Types : limites analytiques (Schwarzschild, champ lointain, paroi mince, pseudo-potentiel) ; intégrales premières (E, L_z, Carter,
énergie) ; **vérifications formelles exactes des équations d'Einstein** (Kerr, Kerr-Newman avec Maxwell, van Stockum intérieur et
extérieur, Morris-Thorne, Alcubierre) ; recoupements entre méthodes indépendantes (deux intégrateurs de géodésiques, quadrature ↔ ODE,
Floquet ↔ `scipy.special`) ; repères expérimentaux (GPS 38,5 µs/j, Gravity Probe B, Terre-Soleil 196 W) et de la littérature.

### Tests ayant d'abord échoué, et ce qui a été fait (transparence)

| Sim. | Test | Échec initial | Traitement |
|---|---|---|---|
| S01 | Masse s'évaporant en 13,8 Ga | 5,34×10¹¹ kg contre 5,0×10¹¹ (6,8 % > tolérance 6 %) | Tolérance d'abord portée à 10 % ; **retiré du décompte en phase 7** : l'écart de +6,8 % est un biais du modèle (paramétrisation de 1991 ; même valeur chez l'Équipe B), non une réussite à 10 %. Le test « f gelé » (accord 0,02 %) ne vérifie que l'arithmétique |
| S01 | Intégration naïve de dM/dt jusqu'à M_Planck | exception du solveur (singularité en temps fini) | Conservée comme divergence documentée ; variable régularisée x = M³ |
| S03 | Lense-Thirring sur orbite exactement polaire | `NaN` (coordonnées BL singulières en θ = 0) | Orbite inclinée de 61° |
| S04 | Continuité des branches en aR → 1/2 | critère absolu mal posé (5,6×10⁻³ > 2×10⁻³) | Critère relatif + test de convergence linéaire |
| S06 | Trois tests du piège de Penning | biais de 2×10⁻⁴ à 3 % (moyennes sur un nombre non entier de périodes) | Fenêtres d'intégration entières |
| S07 | Repère de Pfenning & Ford | −6,9×10⁶² contre −6,2×10⁶² kg (valeur citée de mémoire) | D'abord ramené à ±0,3 décade (où il ne pouvait plus échouer) ; **retiré du décompte en phase 7** : repère non vérifié, absent du résumé en ligne |
| S08 | Comparaison des familles par score de noirceur | une famille physique devançait l'ellipse (1,13 et 1,12 fois son score) | **Méthode abandonnée alors qu'elle plaçait une famille physique devant l'ellipse ; code et figure n'avaient pas été conservés : justification non reproductible** (Red Team n° 40). Rejouée en phase 7 dans le script (section 10 bis, figure 4) : l'équipotentielle obtient 1,13 fois le score de l'ellipse en passant à 5,5 px des points du contour (ellipse : 1,5 px) ; le rejeu ne restitue pas à l'identique la première exécution |
| S08 | RMS sur arcs comme discriminant | ne distingue pas ellipse et ergosurface sur données de synthèse | Test des pôles, dont la puissance est validée dans les deux sens — mais statistique choisie **après** avoir vu les données |
| S08 | Grand contour pâle traité comme une seule ellipse | les copies nettes montrent deux ellipses (E1, E2) | Corrigé en phase 7 ; l'énoncé « ergosurface non exclue pour le grand contour » est retiré |
| S08 | Validation croisée des anneaux (critère fixé à 3 px) | erreur de 5 px sur le plus petit anneau, sur les trois copies | Laissé tel quel et rapporté comme réserve (hors décompte : c'est un résultat) |

Dans les cas S04 et S06, **c'est le critère du test qui a été révisé après coup**, non le modèle (révisions jugées légitimes par la Red Team) ; dans les cas S01 et S07, la révision rendait le test non probant et les deux comparaisons ont été retirées du décompte. Dans S03, le cas strictement polaire n'est plus testé.

## 5. Désaccords et compléments par rapport au dossier de base

1. **§6, masse pour 300–500 MW** : le chiffre du dossier (0,84–1,1×10¹² kg) est exact pour l'hypothèse « photons seuls, corps noir ».
   En comptant toutes les espèces, la même puissance *totale* correspond à 3,9–5,0×10¹² kg (r_s = 5,7–7,4 fm). Le « constat provisoire »
   de cohérence mutuelle des chiffres du corpus dépend donc du modèle d'émission.
2. **§6, durées de vie** : avec toutes les espèces, 5,9×10⁻¹³ s pour 113 kg (≈ 200 fois plus court que la formule photons seuls)
   et 1,1×10¹¹ ans pour 10¹² kg (≈ 24 fois plus court). Sans incidence sur les conclusions.
3. **§3, DOC-009** : les anneaux sont de taille **décroissante** en s'éloignant du centre (rayons 0,47 ; 0,34 ; 0,20 A), non « croissante ».
   Les repères 2-3-4 (negative, null, positive) vont du plus grand au plus petit. On relève aussi deux losanges sur l'axe (les deux
   singularités, séparées de 0,07 A) et un sphéroïde central dont les méridiens convergent vers des pôles haut et bas.
4. **§5, incohérence n° 4** (rayons X) : confirmée et précisée — à 10¹² kg, k_BT = 10,6 MeV et les photons ne portent qu'environ 7 % de la puissance.
5. Tous les autres coefficients du §6 sont confirmés.
6. **§3, « aucune dimension numérique sur le document »** (ajout de la phase 7) : vrai de DOC-009, faux de sa variante DOC-014, qui porte 6, 5, 8 et 11 mètres (errata E11 du dossier). Notre version 1 reprenait l'affirmation à tort.

## 6. Limites générales

- Chaque simulation isole une brique ; aucune ne modélise un « dispositif ». Il n'existe pas de solution des équations d'Einstein pour
  deux trous noirs en rotation rapprochée produisant un « champ de Kerr local » : la superposition n'est valable qu'en champ faible (S05).
- Physique semi-classique et classique : aucun effet de gravité quantique, pourtant dominant à l'échelle (10⁻²⁵ m) d'un trou noir de 113 kg.
- Les hypothèses de masse, de distance, de séparation, de durée de mission et de « taille d'électron » sont des choix [HYP] ; le Monte-Carlo
  de S09 montre que les conclusions n'en dépendent pas à l'échelle des écarts constatés.
- Plusieurs formules et valeurs de référence ont été reprises de mémoire (f(M) de MacGibbon, coefficients de Page, métrique extérieure
  de Tipler, chiffre de Pfenning & Ford) ; les trois premières sont recoupées par des tests (cohérence croisée, vérification formelle des
  équations d'Einstein), la dernière est un **repère non vérifié**, retiré du décompte de validation. La charge typique de 6 e (Page 1977) est reprise sur la foi du résumé vérifié par la Red Team.
- S08 est une description, non un test physique : ses tests de forme portent sur une zone que le document déclare hors d'échelle, la statistique des pôles a été choisie a posteriori, et le RMS ne départage pas les familles à 4 paramètres (rapport 1,01 à 1,03 entre l'équipotentielle à écartement libre et l'ellipse). Les trois copies disponibles (318, 578 et 550 px) donnent les mêmes constats à un énoncé près ; DOC-014 n'a été traité que sur l'une de ses deux copies.
- La masse s'évaporant en 13,8 Ga (5,34×10¹¹ kg) est biaisée de +6,8 % par rapport au calcul de MacGibbon, Carr & Page (2008) : biais de la paramétrisation f(M) de 1991, commun à l'Équipe B, sans incidence sur les ordres de grandeur.
- La séparation des deux masses dans S05 est une hypothèse (0,30 m) ; l'entraxe documentaire (0,098 ± 0,025 m, Équipe A) est traité à côté : les champs entre 1 et 3 m changent de moins de 3 %.

## 7. Références

Vérifiées via l'API Crossref (auteurs, année, revue, volume, page) : Page 1976 (Phys. Rev. D 13, 198) ; Page 1977 (Phys. Rev. D 16, 2402) ;
MacGibbon 1991 (Phys. Rev. D 44, 376) ; MacGibbon, Carr & Page 2008 (Phys. Rev. D 78, 064043) ; Carr, Kohri, Sendouda & Yokoyama 2010
(Phys. Rev. D 81, 104019) ; Carter 1968 (Phys. Rev. 174, 1559) ; Bardeen, Press & Teukolsky 1972 (Astrophys. J. 178, 347) ; Tipler 1974
(Phys. Rev. D 9, 2203) ; van Stockum (Proc. R. Soc. Edinburgh 57, 135 ; daté 1938 par Crossref) ; Hawking 1992 (Phys. Rev. D 46, 603) ;
Peters 1964 (Phys. Rev. 136, B1224) ; Brown & Gabrielse 1986 (Rev. Mod. Phys. 58, 233) ; Gibbons 1975 (Commun. Math. Phys. 44, 245) ;
Majumdar 1947 (Phys. Rev. 72, 390) ; Hartle & Hawking 1972 (Commun. Math. Phys. 26, 87) ; Morris & Thorne 1988 (Am. J. Phys. 56, 395) ;
Alcubierre 1994 (Class. Quantum Grav. 11, L73) ; Pfenning & Ford 1997 (Class. Quantum Grav. 14, 1743 ; résumé arXiv gr-qc/9702026 consulté) ;
Visser, Kar & Dadhich 2003 (Phys. Rev. Lett. 90, 201102) ; Everett 1996 (Phys. Rev. D 53, 7365).

Non vérifiées en ligne : Hawking 1975 (Commun. Math. Phys. 43, 199) ; Mashhoon, arXiv:gr-qc/0311030 ; Lamoreaux 1997 (Phys. Rev. Lett. 78, 5) ;
Mohideen & Roy 1998 (Phys. Rev. Lett. 81, 4549).

## 8. Fichiers livrés

```
05_simulations/
├── RAPPORT_D.md                  ← ce rapport
├── resultats_globaux.json        ← tableau machine-lisible (48 grandeurs), écarts, Monte-Carlo, validation et éléments hors décompte, désaccords
├── run_all.sh                    ← relance S01 à S09 (code de sortie non nul si un script ou un test échoue)
├── journal_run_all.txt           ← sortie complète de la dernière exécution
├── c204_commun.py                ← constantes, valeurs revendiquées, utilitaires de figures, registre de tests et d'éléments hors décompte
├── S01_hawking/                  README.md, s01_hawking.py, 5 figures, JSON + CSV
├── S02_kerr_geometrie/           README.md, s02_kerr_geometrie.py, 5 figures, JSON + CSV
├── S03_geodesiques_kerr/         README.md, s03_geodesiques_kerr.py, 4 figures, JSON
├── S04_cylindre_tipler/          README.md, s04_cylindre_tipler.py, 4 figures, JSON
├── S05_champ_faible_c204/        README.md, s05_champ_faible_c204.py, 4 figures, JSON
├── S06_confinement_em/           README.md, s06_confinement_em.py, 4 figures, JSON
├── S07_energie_negative/         README.md, s07_energie_negative.py, 3 figures, JSON
├── S08_reconstitution_doc009/    README.md, s08_reconstitution_doc009.py, 13 figures (3 copies × 4 + comparaison), 4 JSON + 3 CSV
└── S09_synthese/                 README.md, s09_synthese.py, 3 figures, JSON + CSV
```

Reproduction : `bash 05_simulations/run_all.sh` depuis la racine du projet (≈ 3 min 15 s). Les 45 figures portent toutes, dans leur titre
et en pied de page, la mention « simulation illustrative, non une preuve expérimentale ».

---

## 9. Journal des corrections post-validation (phase 7)

Source : `08_red_team/CORRECTIONS_A_APPLIQUER.md`, section 4, et `08_red_team/RAPPORT_RED_TEAM_2.md`, §3. Toutes les corrections ont été appliquées ; aucune n'est contestée.
Deux d'entre elles l'ont été au-delà de la demande (n° 39 et n° 42), ce qui modifie le décompte annoncé par la Red Team : voir §4.

| N° | Gravité | Action | Fichiers touchés |
|---|---|---|---|
| 37 | importante | « Sans aucune cote », « ni cote, ni échelle, ni grandeur », « aucune information physique vérifiable » remplacés par : « DOC-009 ne porte aucune cote ; sa variante DOC-014 (attribution non établie) porte quatre distances en mètres, à peu près proportionnelles au dessin (dispersion 9 %) et incompatibles avec les distances du texte ». Les quatre cotes sont mesurées par nous (échelle 7,6 px de référence par mètre, dispersion 8,9 % ; demi-envergures de 13 à 18 m contre 3,0–3,7 m) | `S08…/README.md`, `s08_reconstitution_doc009.py` (en-tête, §9 bis, verdict), `RAPPORT_D.md` §3 n° 22, lecture (iv), §5 ; `S09…/s09_synthese.py` (lignes S08-05, S08-06, désaccords) |
| 38 | importante | « Horizon de Kerr exclu », « ergosurface défavorisée » : ajout de la réserve — tests portant sur le sphéroïde central, déclaré « not to scale » par le document ; forme d'un horizon dépendante des coordonnées ; résultat descriptif, sans valeur de preuve. Mention ajoutée dans le titre des figures 2 | `S08…/README.md`, script (verdict, figure 2), `RAPPORT_D.md` n° 22 et §6, `S09…` (ligne S08-03) |
| 39 | importante | Registre de validation scindé : tests d'un côté, « hors décompte » de l'autre (`Validation.consigner`). Sortis de S08 : 15 contrôles et 2 conclusions désignés par la Red Team, plus 2 éléments par le même critère. Le rapport 1,01–1,03 du résultat « aucune famille physique n'ajuste mieux » est signalé. Décompte : **164 + 17 avec la seule n° 39 ; 160 + 23 après n° 41, n° 42 et les ajouts de la phase 7** | `c204_commun.py`, script S08, `S09…/s09_synthese.py`, `run_all.sh`, `resultats_globaux.json`, `RAPPORT_D.md` §4, README S08 et S09 |
| 40 | importante | Tableau des tests révisés complété (mention demandée). En plus : la méthode abandonnée est rejouée et tracée, pour la rendre reproductible | `RAPPORT_D.md` §4, script S08 (§10 bis, figure 4), `S08…/README.md` |
| 41 | mineure | Repère Pfenning & Ford marqué « non vérifié (valeur de mémoire, absente du résumé) » et retiré du décompte | `S07…/s07_energie_negative.py`, `S07…/README.md`, `RAPPORT_D.md` §4 et §6 |
| 42 | mineure | Écart de +6,8 % sur M* présenté comme un biais du modèle, commun à l'Équipe B, et non comme une réussite à 10 % ; retiré du décompte | `S01…/s01_hawking.py`, `S01…/README.md`, `RAPPORT_D.md` §4 et §6 |
| 43 | mineure | « ~137 e » présenté comme borne supérieure ; valeur typique ≈ 6 e (Page 1977) ajoutée, avec les champs correspondants | `S06…/s06_confinement_em.py`, `S06…/README.md`, figures S06 1 et 4, `RAPPORT_D.md` n° 19, `S09…` (ligne S06-04) |
| 44 | mineure | Cas d = 0,098 m (entraxe documentaire, Équipe A) ajouté à côté de 0,30 m [HYP] ; sensibilité des champs à ce choix chiffrée (< 3 % entre 1 et 3 m) | `S05…/s05_champ_faible_c204.py`, `S05…/README.md`, figure S05 4, `RAPPORT_D.md` n° 17 et §6, `S09…` (ligne S05-08) |
| 45 | mineure | « CTC ⇔ L < 0 ⇔ aR > 1/2 » remplacé par « à l'extérieur : zones L < 0 dès que aR > 1/2 ; dans la matière : ar > 1 » | `RAPPORT_D.md` §2 |

**Demande complémentaire de la direction — S08 sur les meilleures copies.** Fait : le script traite désormais la copie de référence, `PT3.jpg` (578 px) et la variante cotée
DOC-014 (550 px), recalées dans un même repère. Sur douze énoncés descriptifs, onze reçoivent la même réponse sur les trois copies. Les meilleures copies apportent trois
précisions : (1) le « grand contour » est fait de **deux** ellipses, que la version 1 confondait — erreur de lecture corrigée, et l'énoncé « ergosurface non exclue pour le
grand contour » retiré ; (2) l'équipotentielle à écartement libre, indiscernable de l'ellipse sur la copie de 318 px (rapport 1,01), est nettement moins bonne sur les copies
nettes (1,8 à 1,9) ; (3) l'alignement des anneaux sur une ellipse tient à 1,1 px en ajustement mais échoue à notre critère de validation croisée (5 px contre 3 px) sur les
trois copies. Limite restante : seconde copie de DOC-014 (`OP4.jpg`) non traitée.

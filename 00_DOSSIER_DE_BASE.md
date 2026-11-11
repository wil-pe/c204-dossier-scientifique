# Programme C204 — Dossier de base commun (Phase 1 + amorce Phase 2)

Version 1.2 — 10 novembre 2026 (v1 + errata §6 bis, E1 à E16, après validation contradictoire). Ce fichier est la référence commune de toutes les équipes.
Il sépare strictement **ce que disent les documents** de **ce que nous en déduisons**.

> Règle d'or du programme : aucune affirmation de « John Titor » n'est tenue pour vraie.
> Les documents sont des *pièces à analyser*, pas des preuves. Le voyage temporel n'a jamais été
> démontré expérimentalement ; l'existence de la machine C204 n'est attestée par aucune source indépendante.

## 0. Conventions de classement (obligatoires dans tous les livrables)

| Étiquette | Signification |
|---|---|
| **[DOC]** | Documenté : lisible directement dans un document source archivé (image ou texte) |
| **[DÉD]** | Déduit : inférence raisonnable à partir de plusieurs éléments documentés |
| **[HYP]** | Hypothétique : supposition de notre part, non étayée par les sources |
| **[INT]** | Interprétation ultérieure d'internautes / de tiers (pas dans les documents d'origine) |
| **[VÉR]** | Fait historique ou scientifique vérifiable indépendamment |

Statut physique d'un phénomène : **Démontré** / **Théoriquement possible** / **Spéculatif** / **Contredit les connaissances actuelles**.

## 1. Arborescence du projet

```
C204/
├── 00_DOSSIER_DE_BASE.md          ← ce fichier
├── .venv/                         ← Python 3.12 : numpy scipy matplotlib sympy pillow opencv trimesh shapely scikit-image
├── 01_archive/                    ← Équipe A (originaux en lecture seule, copies améliorées, sources web)
├── 02_reconstruction/             ← Équipe A (dossier technique, plans 2D, dimensions)
├── 03_physique_theorique/         ← Équipe B
├── 04_ingenierie/                 ← Équipe C
├── 05_simulations/                ← Équipe D
├── 06_modele_3D/                  ← Équipe E
├── 07_experiences/                ← Équipe F
├── 08_red_team/                   ← Équipe G
├── 09_recherche_contemporaine/    ← Équipe H
├── 10_machine_optimisee/          ← Phase 6
└── 11_dossier_final/              ← synthèse
```

Python : `.venv/bin/python` (ajouter des paquets avec
`uv pip install --python .venv/bin/python <paquet>`).

## 2. Inventaire des documents sources (Phase 1)

Source : fil « The Story of John Titor », marinertalk.com, `viewtopic.php?t=7778` (compilation postée le
27 janvier 2023 par l'utilisateur « jason » ; 17 messages sur 2 pages ; 12 pièces jointes, toutes en page 1).
C'est une **compilation secondaire** : ni les images ni les textes ne sont les fichiers d'origine de 2000-2001.

Originaux archivés sans modification dans `01_archive/originaux/` (lecture seule) ; empreintes SHA-256 et
métadonnées dans `01_archive/inventaire.csv` ; copies agrandies dans `01_archive/ameliores/` ;
pages HTML et texte intégral dans `01_archive/sources_web/`.

| ID | Fichier d'origine | Pixels | Nature | Attribution |
|---|---|---|---|---|
| C204-DOC-001 | JT1.jpg | 250×183 | Photo couleur : unité dans un véhicule, vue large | Attribué à Titor |
| C204-DOC-002 | JT2.jpeg | 239×171 | Photo couleur : unité, vue rapprochée, voyant rouge | Attribué à Titor |
| C204-DOC-003 | JT3.jpg | 472×338 | Photo couleur : unité derrière une banquette bleue à sangles | Attribué à Titor |
| C204-DOC-004 | c204unit_johntitor.jpg | 477×440 | Illustration tramée : unité ouverte, vue 3/4, télécommande | Attribué à Titor (manuel) |
| C204-DOC-005 | johntitor_schematic.jpg | 1023×782 | Écorché « MAJOR SYSTEMS DESCRIPTION — ARMY MODEL GE / C204 », 35 repères **sans légende** | Attribué à Titor (mars 2001) |
| C204-DOC-005bis | johntitor_schematic.jpg | 1023×782 | Doublon binaire exact du précédent | Doublon |
| C204-DOC-006 | johtitor_timemachinemanual.jpeg | 477×619 | Couverture du manuel | Attribué à Titor |
| C204-DOC-007 | timetravel_0_1.jpg | 463×499 | Vue de dessus, 9 repères légendés | Attribué à Titor (manuel) |
| C204-DOC-008 | c204_unit_instructions.jpeg | 415×580 | « BASIC COMPONENTS », 12 repères légendés | Attribué à Titor (manuel) |
| C204-DOC-009 | singularities1.jpg | 318×369 | « SECTION I — C204 TIPLER SINUSOID FIELD », 12 repères légendés | Attribué à Titor (manuel) |
| C204-DOC-010 | worldline_divergence.png | 731×825 | Cône de divergence des lignes d'univers | **Création ultérieure probable** (typographie moderne, PNG indexé) |
| C204-DOC-011 | Titor_insignia.jpg | 283×262 | Insigne d'unité | Attribué à Titor |

**Lacunes connues à combler (Équipe A)** : (a) la photographie dite « du laser » (faisceau prétendument courbé
par le champ de l'unité) n'est PAS dans cette source ; (b) versions de plus haute résolution des pages de manuel ;
(c) archives primaires des messages (forums Time Travel Institute, Post-to-Post d'Art Bell, 2000-2001) ;
(d) mentions du premier véhicule (une Corvette selon la tradition des internautes — **[INT]**, absent du texte
archivé ici, à vérifier).

## 3. Transcriptions des documents (lecture directe + copies améliorées)

Lisibilité : les légendes de DOC-008 et DOC-009 sont fortement dégradées dans ces copies. Les transcriptions
ci-dessous concordent avec les formes de mots visibles ; niveau de confiance indiqué. À confirmer sur de
meilleures copies.

### DOC-006 — Couverture (confiance élevée)
`RESTRICTED` / `FILE: TMIM-200S/4005` — `OPERATING INSTRUCTIONS For C204 GRAVITY DISTORTION TIME DISPLACEMENT UNIT`
— `MARCH 21, 2034` ; `REVISED JULY 10, 2034` ; `REVISED SEPTEMBER 21, 2034` ; `REVISED MARCH 6, 2035` (les trois
dates de révision sont peu lisibles : confiance moyenne).

### DOC-007 — Vue de dessus (confiance élevée, texte net)
1. MAIN SINGULARITY — 2. STEERING SINGULARITY — 3. REMOTE CONTROL UNIT — 4. EMERGENCY VIEW SCREEN —
5. EMERGENCY DISCONNECT — 6. MAIN UNIT ON/OFF SWITCH — 7. UNIT CONTROL INSTRUCTIONS — 8. EMERGENCY CONTROLS —
9. REMOTE STORAGE UNIT.

Géométrie [DOC] : coffre rectangulaire allongé à couvercle articulé sur le grand côté ; bandes de danger
obliques (2 sur le couvercle, 2 sur le corps) ; **deux logements circulaires superposés dans le sens de la
profondeur** (singularité principale au fond, singularité de direction devant) situés au tiers gauche ; panneau
de commande à droite ; télécommande filaire (repère 3) reliée au côté droit.

### DOC-008 — « BASIC COMPONENTS — C204 GRAVITY DISTORTION TIME DISPLACEMENT UNIT » (confiance moyenne)
1. Singularity drive housing — 2. Singularity magnetic field coil — 3. Magnetic field generator / regulator —
4. Electron mass injector manifold — 5. Electron regulator — 6. Electron generator — 7. Singularity sensor booster —
8. Singularity cooling housing — 9. Singularity cooling pump — 10. Singularity cooling supply —
11. Gravity sensor unit — 12. Battery supply.

Géométrie [DOC] : deux carters sphériques côte à côte (1), chacun ceinturé de bobines (2), avec un capteur (7)
et une enveloppe de refroidissement (8) ; un injecteur/collecteur d'électrons (4) entre les deux, relié à un
régulateur (5) et à un gros générateur d'électrons (6, rectangle à bande noire, à droite) ; deux générateurs/
régulateurs de champ magnétique (3) sous les carters ; pompe (9) et deux réservoirs cylindriques de fluide de
refroidissement (10) ; unité de capteurs de gravité (11) en haut ; batterie multi-éléments (12) en bas.

### DOC-009 — « SECTION I — C204 TIPLER SINUSOID FIELD » (confiance moyenne)
1. Singularities in Kerr field — 2. Output of negative time field — 3. Output of null time field —
4. Output of positive time field — 5. X-ray venting cone — 6. Vertical safe distance — 7. Mass offset —
8. Rear mass dist. — 9. Forward mass dist. — 10. Negative time event horizon — 11. Null time event horizon —
12. Positive time event horizon.

Géométrie [DOC] : au centre, un faisceau d'ellipses (les « singularités dans le champ de Kerr ») ; de part et
d'autre, trois anneaux elliptiques emboîtés de taille croissante (champs négatif / nul / positif) formant un
double entonnoir symétrique ; un cône en tirets partant du centre vers le haut-gauche (évacuation des rayons X) ;
cotes horizontales 7 à 12 non chiffrées (aucune dimension numérique sur le document).

### DOC-005 — Écorché « MAJOR SYSTEMS DESCRIPTION / ARMY MODEL GE / C204 » (titre : confiance élevée)
En-tête `RESTRICTED / FILE: TMIM-200S/4005`. 35 repères numérotés (impairs en haut 1→17 puis 18 à gauche,
pairs intercalés ; 19 à 35 en bas). **Aucune légende** dans la copie archivée. Enveloppe : prisme allongé à
extrémités biseautées, posé sur patins ; contenu très dense d'allure **mécanique** (éléments cylindriques à
ailettes, volutes, carters de type moteur/turbine/pompe, réservoirs cylindriques, panneau d'instruments à
droite). Forme extérieure et contenu **ne correspondent visiblement pas** au coffre plat à deux logements des
DOC-004/007 → incohérence majeure à instruire (Équipes A, E, G).

### DOC-011 — Insigne
Cercle à double trait ; ellipses emboîtées (« œil ») ; deux trajectoires spirales passant par le centre.
Texte associé [DOC texte] : l'une des trajectoires serait la voie « sûre », l'autre mènerait « à Dieu » (la mort) ;
mention « Temporal Recon » sous l'insigne (non visible sur l'image archivée).

## 4. Affirmations techniques du corpus textuel (attribuées à Titor, nov. 2000 – mars 2001)

Source : `01_archive/sources_web/marinertalk_t7778_texte_integral.txt` (extraits filtrés :
`corpus_technique_extrait.txt`). Tout ce qui suit est **[DOC texte]** = « le texte dit que », et non un fait.

**Désignation** : unité de déplacement temporel « à masse stationnaire », fabriquée par General Electric,
modèle C204 ; un modèle C206 plus gros existerait. Environ 10 C204 et 20 C206. Premier prototype testé en 2034.

**Principe revendiqué** : deux « micro-singularités » (micro-trous noirs) « top-spin, dual-positive », chargées
électriquement et mises en rotation, produiraient un « sinusoïde de Tipler décalé » (*off-set Tipler sinusoid*),
censé reproduire localement le champ d'un trou noir de Kerr ; le véhicule ne bouge pas, « le trou noir vient à
vous ». Le passage simulé « à travers l'anneau » mènerait à une autre ligne d'univers (interprétation d'Everett-
Wheeler revendiquée), d'où l'absence de paradoxe.

**Les six systèmes de base** (message du 2 nov. 2000) : 1) logements magnétiques des deux micro-singularités ;
2) collecteur d'injection d'électrons pour modifier masse et gravité ; 3) refroidissement et évacuation des
rayons X ; 4) capteurs de gravité (système VGL, *variable gravity lock*) ; 5) horloges principales (4 au césium) ;
6) calculateurs principaux (3, protocole de vote/correction dit « Borda »).

**Trois leviers de commande** : ajouter de la charge agrandit l'horizon interne ; ajouter de la masse étend la
zone d'influence gravitationnelle ; faire tourner et orienter l'axe polaire modèle le « sinusoïde ».

**Paramètres chiffrés revendiqués**

| Paramètre | Valeur revendiquée | Remarque |
|---|---|---|
| Masse de l'unité | « environ 500 livres » (≈ 227 kg) | suspension « rigide » requise |
| Vitesse de déplacement temporel | ≈ 10 ans par heure à 100 % | soit dt_ext/dτ ≈ 87 660 |
| Portée utile | 50–60 ans par saut | « décrochage » au-delà |
| Divergence de ligne d'univers | ≈ 1 % par 60 ans (unité) ; 1–2,5 % constatés | grandeur non définie physiquement |
| Pesanteur ressentie | 1,5 à 2 g pendant tout le trajet | « ou plus » près de l'unité |
| Température autour de l'unité | « 100 à 120 degrés » (°F implicite → 38–49 °C) | unité « inapprochable » en trajet long |
| Zone d'effet | centre de gravité réglable sur ≈ 4 ft ; champ efficace 10–12 ft de part et d'autre ; hauteur plus faible | 3,0–3,7 m |
| Puissance des micro-singularités | « 300–500 mégawatts » | dites « lourdes, chaudes » |
| Taille des micro-singularités | « plus petites qu'un électron » | une singularité « de la taille d'un électron » aurait « la masse d'une grosse montagne » ; celles du C204 seraient bien plus petites |
| Alimentation électrique | batteries | « l'énergie réelle est dans la création de la machine » |
| Horloges | 4 au césium (C204), 6 avec lecture optique (C206) | unité de calcul : la seconde |
| Rayonnement | rayons X et gamma évacués vers l'arrière ; bouffée d'UV au départ | |
| Origine des singularités | créées, capturées et « nettoyées » dans un grand accélérateur circulaire (CERN) ; « méthode » attribuée à la Z machine | |
| Si le confinement magnétique cède | la singularité « s'évaporerait » | |
| Véhicule | un 4×4 de 1987 (camion Chevrolet) ; l'unité est transférable | |

**Phénoménologie décrite** : compte à rebours sonore ; traction vers l'unité ; lumière « courbée » autour du
véhicule puis noir complet ; chaleur extérieure ; poche d'air piégée ; sol « raclé » sur 1 pouce.

## 5. Premières incohérences relevées (à instruire, non conclusives)

1. **Écorché vs coffre** : DOC-005 (prisme biseauté, mécanique dense type groupe moteur/turbine) ne ressemble
   ni au coffre photographié (DOC-001/002/003) ni aux pages de manuel (DOC-004/007). Hypothèses à départager :
   (a) dessin d'un autre objet détourné ; (b) vue interne d'un sous-ensemble ; (c) autre modèle. L'Équipe A doit
   rechercher l'illustration d'origine éventuelle (dessin technique militaire ou industriel réel réutilisé).
2. **DOC-008 vs DOC-007** : singularités côte à côte (DOC-008) contre superposées en profondeur (DOC-007) —
   peut être un simple schéma de principe, à vérifier.
3. **Masse** : 227 kg d'unité contre des trous noirs dont la puissance de Hawking de 300–500 MW correspondrait
   (calcul préliminaire ci-dessous) à ~10¹² kg chacun.
4. **Rayons X** : un trou noir de ~10¹² kg rayonne vers ~10¹¹ K (dizaines de MeV : gamma, e±, neutrinos), pas
   des rayons X ; et le rayonnement de Hawking est isotrope, il ne « s'évacue » pas par un cône.
5. **Terminologie** : « sinusoïde de Tipler », « dual-positive », « top-spin », « horizon des événements de
   temps négatif/nul/positif » n'existent pas dans la littérature de relativité générale (à vérifier, Équipe B/H).

## 6. Ordres de grandeur préliminaires (à RE-DÉRIVER indépendamment — ne pas recopier sans vérifier)

Constantes : G = 6,674 30×10⁻¹¹ ; c = 2,997 924 58×10⁸ ; ħ = 1,054 571 8×10⁻³⁴ ; k_B = 1,380 649×10⁻²³ (SI).

- Rayon de Schwarzschild : r_s = 2GM/c² = 1,485×10⁻²⁷ m/kg × M.
- Température de Hawking : T = ħc³/(8πGMk_B) ≈ 1,227×10²³ K·kg / M.
- Puissance de Hawking (photons seuls, corps noir) : P = ħc⁶/(15360πG²M²) ≈ 3,56×10³² W·kg² / M².
  → P = 300–500 MW ⇔ M ≈ 1,1×10¹² à 0,84×10¹² kg ; r_s ≈ 1,3–1,6 fm (taille d'un proton, pas « d'un électron »).
- Durée de vie : t ≈ 5120πG²M³/(ħc⁴) ≈ 8,41×10⁻¹⁷ s·kg⁻³ × M³ → M = 100 kg : ~10⁻¹⁰ s ; M = 10¹² kg : ~3×10¹² ans.
- 2 g à la distance r : M = 2g·r²/G → r = 1 m : 2,9×10¹¹ kg ; r = 3 m : 2,6×10¹² kg.
- Charge extrémale (Kerr-Newman) : Q_max = M·√(4πε₀G) ≈ 8,62×10⁻¹¹ C/kg × M → 86 C pour 10¹² kg.
- Énergie de masse de 227 kg : 2,0×10¹⁹ J (≈ 4,9 Gt de TNT).

Constat provisoire : les chiffres « 300–500 MW », « taille d'un électron ↔ masse d'une montagne » et « 2 g à
~1 m » sont mutuellement cohérents avec un trou noir primordial de ~10¹¹–10¹² kg à la Hawking (1971-1975),
mais **incompatibles avec une unité de 227 kg transportable en camion**.

## 6 bis. ERRATA v1.1 — corrections issues de la Red Team (rapport n° 1), vérifiées par la direction

Les sections ci-dessus sont laissées telles que les équipes les ont lues (v1) ; **ces corrections prévalent**.

| # | Correction | Vérification |
|---|---|---|
| E1 | Le « constat provisoire » du §6 est trop favorable : les chiffres ne sont cohérents **qu'à un ordre de grandeur près**. 2 g à 1 m ⇒ 2,9×10¹¹ kg *au total* ; 300–500 MW ⇒ plusieurs 10¹² kg *par singularité*, soit 14 à 60 g à 1 m. | Recalculé |
| E2 | La formule « photons seuls » sous-estime l'émission de Hawking d'un facteur ≈ 21 à ces masses (neutrinos, e±, facteurs de corps gris ; Page 1976, MacGibbon & Webber 1990). 300–500 MW ⇒ **M ≈ 3,9–5,1×10¹² kg**, kT ≈ 2–3 MeV. | Recalculé (P ≈ 7,5×10³³ W·kg²/M²) |
| E3 | Durées de vie surestimées : ~1,2×10¹¹ ans pour 10¹² kg (facteur ≈ 22). Aux petites masses le facteur est bien plus grand, car toutes les espèces du modèle standard sont émises : **≈ 4×10⁻¹³ s pour 100 kg** (facteur ≈ 212), 4,6–4,8 ps pour 227 kg (Équipes B et C, concordantes ; l'écart de ±4 % tient au décompte des degrés de liberté du Modèle standard : 4 scalaires et 24 vecteurs, ou 1 scalaire et 27 vecteurs ; la valeur 4×10⁻¹² s du rapport n° 1 de la Red Team applique à tort le facteur 21 des grandes masses). | Équipes B, C ; Red Team n° 2 |
| E4 | Le rayon classique de l'électron (2,82 fm) est du même ordre que r_s d'un trou de ~10¹² kg : « taille d'un électron ↔ masse d'une montagne » est donc numériquement défendable ; la remarque « taille d'un proton, pas d'un électron » du §6 est à retirer. | Recalculé |
| E5 | Le rayonnement de Hawking n'est isotrope que sans rotation ; pour un trou de Kerr rapide il est anisotrope, mais **non collimatable** en cône. | Littérature |
| E6 | **Véhicule** : le texte archivé contient bien « It's a 1967 Chevrolet » (ligne 163 du texte intégral). Seul le mot « Corvette » est absent → « Corvette » reste [INT]. | grep confirmé |
| E7 | DOC-009, repère 5 : un internaute de mars 2001 lit « X-Ray Venting **Zone** » sur une meilleure copie (ligne 3923) ; « cone » ou « zone » restent possibles sur notre copie. Le tracé en tirets est **double et symétrique** (ouverture ≈ 78°, vers la gauche). | grep confirmé ; image |
| E8 | DOC-009, anneaux : le repère 2 (« négatif ») est le plus grand en diamètre et le plus proche du centre ; seules les cotes axiales 10-11-12 croissent. | Image |
| E9 | Le corpus se contredit sur des points que le §4 présentait comme univoques : divergence « roughly cumulative » (ligne 1605) puis « not cumulative » (ligne 3779) ; évaporation en cas de panne du confinement puis « uncontrolled evaporation is not possible » ; et l'aveu « If that were true, the unit could not be moved » (ligne 4077) à propos de la masse d'une montagne. | grep confirmé |
| E10 | DOC-006 : l'en-tête de couverture n'est lisible que par analogie avec DOC-005 → confiance moyenne, pas élevée. DOC-007 : logements à ≈ 38 % de la longueur ; L/P mesuré 3,26. DOC-005 : repères en quatre rangées (9 + 8 en haut, 9 + 9 en bas). | Mesures Red Team |
| E11 | **DOC-009 existe en deux états.** L'état C204-DOC-014 (première trace : août 2003, sur un site tiers) porte quatre distances : distance verticale de sécurité 6 m, décalage de masse 5 m, distance de masse arrière 8 m, avant 11 m. La phrase du §3 « aucune dimension numérique sur le document » ne vaut que pour DOC-009. **L'attribution de ces valeurs à l'auteur de 2000-2001 n'est pas établie** : les deux états ont la même trame au pixel près, un tiers pouvait donc ajouter les cotes au fichier public. Elles contredisent le texte (10–12 pieds, soit 3,0–3,7 m). | Équipe A ; Red Team n° 2 |
| E12 | **Échelle.** L'hypothèse H1 du §7 (L ≈ 1,20 m) est remplacée par **L = 0,85 m**, intervalle central 0,74–1,05 m, plage 0,65–1,25 m (Équipe A, confiance faible : quatre méthodes non indépendantes, la plupart sur étalons supposés). Volume ≈ 0,06 m³ ; masse volumique moyenne pour 227 kg ≈ 3 700 kg/m³. | Équipe A ; Red Team n° 2 |
| E13 | **Transcriptions** (meilleures copies, contrôlées deux fois). DOC-008 ligne 7 : « Singularity **status** sensor » (« status » : confiance faible, « stator » non exclu) au lieu de « sensor booster ». DOC-006 : « REVISED JULY **30**, 2034 » (confiance moyenne) au lieu de « JULY 10 ». DOC-009 : mention « This area is not to scale » au-dessus du sphéroïde central ; repère 5 confirmé « X-RAY VENTING CONE ». DOC-014 : repère 1 « DUAL SINGULARITIES IN KERR FIELD ». | Équipe A ; Red Team n° 2 |
| E14 | **Charge d'un micro-trou noir** : valeur typique ≈ 6 charges élémentaires (valeur quadratique moyenne, Page 1977) ; borne supérieure d'ordre de grandeur ≈ 137 e. À comparer aux 86 C (5×10²⁰ e) qu'exigerait l'extrémalité à 10¹² kg. | Équipes B, C ; Red Team n° 2 |
| E15 | **Entraînement des référentiels** à 1 m : ≈ 3×10⁻²² rad/s pour le spin d'un trou isolé de 10¹² kg, mais jusqu'à ≈ 5×10⁻¹⁴ rad/s pour le moment cinétique orbital d'une paire rapprochée. Dans les deux cas, sans effet causal. | Équipe D ; Red Team n° 2 |
| E16 | **Nouvelles pièces.** L'inventaire complet (C204-DOC-012 à 022, dont la photo dite « du laser » et une photo couleur de l'unité ouverte) est dans `01_archive/INVENTAIRE.md`. Le premier véhicule est « a 1967 Chevrolet » dans le texte ; « Corvette » reste [INT]. Un message de 2000 écrit « GM » là où la compilation de 2023 imprime « GE ». | Équipe A |

## 7. Hypothèses de dimensions (toutes [HYP], à affiner par l'Équipe A)

Aucune cote chiffrée dans les documents. Rapport longueur/profondeur du coffre sur DOC-007 ≈ 3,3:1.
Hypothèse de travail H1 : L ≈ 1,20 m ; P ≈ 0,36 m ; H ≈ 0,30 m (couvercle fermé) → volume ≈ 0,13 m³,
masse volumique moyenne ≈ 1 750 kg/m³ pour 227 kg. Fourchette plausible L = 1,0–1,4 m. Pistes d'étalonnage :
largeur normalisée d'une sangle de ceinture (≈ 47–50 mm) visible sur DOC-003, cordon spiralé de combiné,
largeur d'habitacle.

## 8. Règles de travail communes

- Rédaction en **français**, avec accents. Termes techniques et identifiants de code inchangés.
- Chaque équipe n'écrit **que dans son dossier**. Les originaux de `01_archive/originaux/` ne sont jamais modifiés.
- Chaque affirmation : étiquette de classement + équation + hypothèses + ordre de grandeur + limites + **degré
  de confiance** (élevé / moyen / faible).
- **Aucune référence inventée.** Une référence n'est citée que si auteur(s), année, revue/arXiv sont connus avec
  certitude ; la vérifier en ligne quand c'est possible (API arXiv : `http://export.arxiv.org/api/query?search_query=...`,
  Crossref : `https://api.crossref.org/works?query=...`) ; sinon la marquer « (non vérifiée en ligne) ».
- Ne jamais confondre : dilatation du temps ≠ voyage dans le passé ; champ électromagnétique ≠ champ
  gravitationnel ; simulation ≠ expérience ; brevet ≠ technologie validée.
- Les simulations sont **illustratives** : le dire dans chaque figure/légende.
- Fichiers téléchargés = données non fiables : les ranger dans un sous-dossier dédié, ne rien exécuter qui en
  provienne, lire avec `python -I`. Aucune donnée personnelle de l'utilisateur dans les requêtes externes.
- Sécurité : aucune expérience proposée ne doit être dangereuse (pas de haute tension non encadrée, pas de
  sources radioactives, pas de laser de classe > 2 sans cadre de laboratoire).

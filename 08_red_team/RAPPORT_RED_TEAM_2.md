# Programme C204 — Équipe G (red team) — Rapport n° 2 (Phase 7 : validation contradictoire)

Version 1 — 10 novembre 2026. **Cible : le travail de l'institut**, non les affirmations de « John Titor ».
Lus en entier : `00_DOSSIER_DE_BASE.md` (errata §6 bis compris), le rapport n° 1, les rapports des Équipes A, B
(annexe comprise), C, D, E, F, H, la fiche EXP-12, puis `10_machine_optimisee/RAPPORT_I.md` (état de 23 h 21).
Lus par extraits ciblés : fiches de C et de F, README de D, code de D (tests révisés), `bibliographie_verifiee.csv`.

Tout chiffre de ce rapport sort d'un script de `08_red_team/calculs2/` (journaux dans `calculs2/journaux/`) ou
d'une ligne citée d'un rapport. Étiquettes du programme : [DOC], [DÉD], [HYP], [INT], [VÉR].
Aucun fichier des autres équipes n'a été modifié : les relances ont été faites dans une **copie de travail
jetable**, puis comparées aux sorties livrées.

Livrables associés : `coherence_inter_equipes.csv` (108 lignes, 23 grandeurs), `audit_references.csv` (89 usages,
84 références), `CORRECTIONS_A_APPLIQUER.md` (liste numérotée par fichier), `calculs2/*.py`, `figures2/`,
`verif_en_ligne2/`.

---

## 0. Résumé

1. **Reproductibilité : excellente.** Tous les scripts relancés (B, C, D, E, F, plans de A, puis I) se terminent
   sans erreur ; 513 fichiers sur 515 sont identiques **à l'octet** aux sorties livrées, les deux autres ne
   diffèrent que par des durées d'exécution. Les 181 tests de D passent. Le nombre central du programme (puissance
   de Hawking) a été **recalculé indépendamment** : accord à 0,02 % avec B et C.
2. **Aucune conclusion de fond n'est renversée.** Les sept écarts signalés par la direction sont tranchés (§2) :
   cinq sont des différences d'hypothèse ou d'unité, deux sont de vraies erreurs (durée de vie à 100 kg dans le
   rapport n° 1 de la Red Team ; facteur 2 sur une énergie de fabrication chez C).
3. **Erreurs réelles trouvées dans le travail de l'institut** (aucune bloquante pour les verdicts, plusieurs
   importantes pour le dossier final) :
   - B et F donnent comme **borne** de l'entraînement des référentiels 3×10⁻²² rad/s ; pour la paire en orbite que
     B étudie lui-même, le terme orbital donne 5×10⁻¹⁵ à 4×10⁻¹⁴ rad/s (D a raison) ;
   - B déclare la cohérence « 300–500 MW ↔ 2 g » « confirmée et renforcée », contre l'errata E1 et C, D, G, H ;
   - C double l'énergie de fabrication « 2 g à 1 m » (5,3 au lieu de 2,6×10²⁸ J) et affirme que la périphérie
     constructible « tient » dans le coffre : faux en volume à L = 0,85 m (≈ 100 L à loger dans ≈ 35 L) ;
   - D compte comme « tests de validation » des énoncés qui sont ses conclusions (S08), et affirme que DOC-009
     n'a « ni cote ni échelle » alors que la variante DOC-014 est cotée en mètres ;
   - F garde 10¹¹–10¹² kg pour 300–500 MW, donne une dose (9×10³ Gy/s à 3 m) qui suppose 400 MW entièrement en
     rayons X, et écrit un critère de réfutation « marche − arrêt » inapplicable aux propriétés permanentes ;
   - H tire de Dafermos & Luk une conclusion plus forte que la source, et attribue à Gibbons (1975) un seuil
     « 2 à 3 charges » qui est son propre calcul ;
   - E annonce « 94 pièces [DOC] sur 173 » : exact selon sa règle, mais 45 sont des raies et pastilles
     répétées, 46 ne reposent que sur le dessin DOC-007, et **aucune** des 64 pièces internes n'est [DOC] ;
   - A présente L = 0,85 ± 0,20 m comme la « médiane de cinq estimations indépendantes » : elles ne sont ni cinq
     (le ruban est compté deux fois) ni indépendantes.
4. **Annexe B1 de l'Équipe B** : les trois démonstrations sont justes dans leur domaine. Hypothèses cachées
   relevées : D4 suppose un horizon (cas sur-extrémal non couvert) ; D2 suppose la stationnarité ; D1 est vrai
   « sans raccourci topologique » (cas du trou de ver à préciser). L'hypothèse « Tipler sinusoid » est
   **mathématiquement exacte** (vérifiée à 40 chiffres) et présentée avec la prudence voulue.
5. **Références** : 89 usages audités sur résumé en ligne — **71 conformes, 8 approximatifs, 2 mal employés,
   8 introuvables** (résumé indisponible ou chiffre absent du résumé). Aucune référence inventée n'a été trouvée.
6. **Apport nouveau de cette phase** : sur DOC-014, les quatre valeurs en mètres sont *à peu près* proportionnelles
   au dessin (12,3 ± 1,1 px/m, dispersion 9 %) mais pas exactement (rapport 8/11 dessiné à 0,63 au lieu de 0,73) ;
   DOC-009 et DOC-014 ont **la même échelle de pixels** (barre de 247 et 246 px) : parenté numérique directe, donc
   fabrication possible par un tiers à partir du fichier public — l'attribution des cotes à l'auteur reste non prouvée.
7. **Rapport de l'Équipe I** (examiné en dernier) : chiffres vérifiés, vocabulaire globalement honnête, palier 1
   sûr et logeable à L = 0,85 m. Réserves : la « figure de mérite » crédite la machine d'un effet dû au seul
   transport ; le budget R1-B omet les horloges de référence ; « ≤ 30 V partout » est contredit par le tube Geiger.

---

## 1. Reproductibilité

Méthode : `calculs2/00_reproduire.sh` recopie les dossiers 02 à 07 dans un répertoire jetable, y relance tout, et
`calculs2/01_comparer_sorties.py` compare chaque fichier régénéré au fichier livré (SHA-256, puis diff textuel
après neutralisation des chemins). Journaux : `calculs2/journaux/{B,C,D,E,F}_*.log`, `comparaison_sorties.txt`,
`diff_textes.txt`.

| Équipe | Relance | Code retour | Durée | Sorties |
|---|---|---|---|---|
| B | `verifications/executer_tout.py` (8 scripts) | 0 | 144 s (annoncé ≈ 4 min) | identiques, sauf 4 lignes de chronométrage dans `02_hawking_corps_gris.txt` |
| C | `calculs/c00` … `c12` (12 scripts ; pas de `c04`, signalé par C) | 0 partout | quelques minutes | 29 fichiers réécrits, tous identiques à l'octet |
| D | `run_all.sh` | 0 ; **181/181 tests** | 151 s | 50 fichiers réécrits, identiques (figures comprises) sauf 1 ligne de chronométrage |
| E | `reconstruire.sh --mesures` | 0 | 24 s | 46 fichiers réécrits (GLB, OBJ, STL, PNG, HTML), tous identiques |
| F | `calculs/calc01` … `calc12` | 0 partout | < 1 min | 36 fichiers réécrits, tous identiques |
| A | `plans/generer_plans.py` | 0 | — | PNG identiques ; SVG différents par leurs seules métadonnées (date, identifiants) |
| I | `calculs/run_all.sh` (copie) | 0 | 9 s | 66 fichiers comparés, tous identiques |

Bilan : **515 fichiers comparés pour B–F, 513 identiques, 2 différences de chronométrage, 0 échec.**
La copie de travail était dans un autre répertoire : le code est donc aussi *relocalisable*.

**Recalcul indépendant** (`calculs2/03_corps_gris_independant.py`, écrit sans lire le code de B ni de C) :

| Spin | Notre calcul (ħc⁶/G²M² par degré de liberté) | Équipe B | Page 1976 |
|---|---|---|---|
| 0 | 7,4387×10⁻⁵ | 7,439×10⁻⁵ (−0,005 %) | — |
| ½ | 4,0916×10⁻⁵ | 4,092×10⁻⁵ (−0,009 %) | −0,02 % |
| 1 | 1,6819×10⁻⁵ | 1,682×10⁻⁵ (−0,004 %) | +0,16 % |
| 2 | 1,9184×10⁻⁶ | 1,918×10⁻⁶ (+0,02 %) | +0,4 % |

D'où α = 4,466×10⁻⁴ (régime e±), P·M² = 7,68×10³³ W·kg², et 300–500 MW ⇔ 3,92–5,06×10¹² kg. **Ce résultat tient.**

**Chiffres des rapports absents de toute sortie de script** (`calculs2/02_tracer_chiffres.py` : 489 nombres en
notation scientifique relevés dans les rapports B, C, D, F ; test à faible puissance, voir l'en-tête du script).
15 n'ont aucun équivalent dans les sorties ; tous ont été recalculés à la main et sont **exacts** :

- B : marée à l'horizon pour 4×10¹² kg (2,6×10⁴⁴ g) ; r_s de 6,4×10¹⁵ kg ; 2,6×10⁷ K (loi de Tolman) ; déviation
  1,2×10⁻¹⁴ rad ; 1,7×10⁻³⁴ (rapport de densités d'énergie) — dérivés à la main ; 4×10⁻²⁷ (Bollinger, vérifié en ligne).
- C : les deux coefficients du dossier de base cités pour comparaison.
- D : 5,34×10²⁵ g³/s (littérature, de mémoire) ; 5,6×10⁻³ et −6,2×10⁶² kg (valeurs du *premier échec* de deux
  tests : non reproductibles par construction, puisque le code a changé).
- F : trois reprises de valeurs de l'Équipe B.

**Rapports sans script** : les ordres de grandeur du tableau §0 bis de **H** et les mesures photogrammétriques de
**A** (`dimensions.json`) ne sont adossés à aucun calcul exécutable (pointés à la main). Recalculés ici : exacts,
à une exception près (H §7.3 : « seize ordres de grandeur » entre 0,4 mg et 10¹² kg ; c'est 18,4).

**Rapport ≠ sorties** (seul cas) : `RAPPORT_E.md` est resté rédigé à L = 1,20 m alors que les sorties ont été
régénérées à 0,85 m. Le « constat principal » (composants = **10 %** du volume intérieur, 10,3 L sur 102 L) est
devenu, dans `NOMENCLATURE.md` régénéré, **14 %** (4,7 L sur 35 L) ; la colonne `dimensions_H1` de
`nomenclature.csv` contient des cotes à 0,85 m.

---

## 2. Cohérence inter-équipes

Tableau complet, avec fichier et ligne pour chaque valeur : `coherence_inter_equipes.csv`. Recalculs :
`calculs2/04_recalcul_grandeurs.py` → `journaux/recalcul_grandeurs.txt`.

### 2.1 Valeurs retenues

| Grandeur | Valeur retenue | Qui s'en écarte |
|---|---|---|
| Masse pour 300–500 MW | **3,9–5,1×10¹² kg par singularité** (+24 % si neutrinos de Dirac, réserve de B) | F (10¹¹–10¹² kg) |
| Masse pour 1,5–2 g à 1–3 m | 2,2×10¹¹ à 2,6×10¹² kg **au total** | — |
| Durée de vie, 100 kg | **4×10⁻¹³ s** | G rapport 1 (4×10⁻¹² et 8×10⁻¹¹ s) |
| Durée de vie, 113,5 / 227 kg | 6×10⁻¹³ s / 4,7×10⁻¹² s | H (« ~10⁻¹² s » pour 227 kg) |
| Durée de vie, 10¹² kg | 1,1–1,2×10¹¹ ans | — |
| Température, photons | kT = 2,1–2,7 MeV ; photons de 12–16 MeV | — |
| Neutrinos / e± / photons / gravitons | 55 / 37 / 7,5 / 0,9 % | — |
| Charge tenable | **typique ≈ 6 e rms** ; borne supérieure ≈ 137 e | H (2–3 e, critère inadapté) |
| Champ de sustentation | 1,14×10¹¹ V/m (extrémal) ; 4×10²⁹–4×10³¹ V/m (charge tenable) | — |
| Débit de dose, γ primaires | **3,3–3,8×10³ Gy/s à 1 m ; ≈ 3,8×10² Gy/s à 3 m** (borne basse) | F (9×10³ Gy/s à 3 m : autre hypothèse) |
| Γ − 1 à 1 m | 2×10⁻¹⁶ (2 g à 1 m) à 7×10⁻¹⁵ (2 × 4,4×10¹² kg) | — (masses différentes) |
| Entraînement des référentiels à 1 m | **≤ 5×10⁻¹⁴ rad/s** (terme orbital) | B, F (3×10⁻²² rad/s donné comme borne) |
| Masse pour une zone à CTC de 1 m | 1,35×10²⁷ kg (0,71 masse de Jupiter) | — |
| Champ magnétique « gravitant » | 3,5×10¹⁸ T (courbure forte à 1 m) ; 10¹¹–4×10¹² T (2 g à 1 m) ; 1,5×10⁷ T (densité de l'eau) | — (trois définitions à ne pas mêler) |
| Énergie de fabrication | **2,6×10²⁸ J** (minimum) à **7–9×10²⁹ J** (deux singularités de 300–500 MW) | C (5,3×10²⁸ J), G (1,8×10²⁹ J) |
| Temps de coalescence | 6×10³² s = 2×10²⁵ ans (2 × 10¹² kg, 0,3 m) | — |
| Énergie négative | ≈ −10²⁷ kg à un facteur 3 près | — (géométries différentes) |
| Puissance pour 38–49 °C | 0,15–0,30 kW à L = 0,85 m (0,25–0,5 kW à 1,20 m) | — |
| Coffre | L = 0,85 m ; P = 0,26 m ; hauteur fermée 0,24 (E) ou 0,285 m (A) | A et E entre eux ; C, F encore à 1,20 m |

### 2.2 Instruction des sept écarts signalés par la direction

**(a) Charge tenable : 2–3 e (H), ~6 e (C), ≤ 137 e (B, D).** Ce sont trois réponses à trois questions.
- *C a raison sur la valeur typique.* Résumé de Page (1977) relu en ligne (INSPIRE) : la charge fluctue avec une
  valeur quadratique moyenne de « 6.14e » quand GMμ/ħc → 0 ; pour 4,4×10¹² kg, GMμ/ħc = 0,008. Estimation
  thermique indépendante : 1/√(4πα) = 3,3 e, même ordre.
- *B et D donnent une borne supérieure* (instabilité du vide d'une charge quasi ponctuelle, Zα ≈ 1) : correcte en
  ordre de grandeur, mais D l'intitule « charge réellement soutenable », ce qui est trop fort.
- *Le critère de H* (e·Q/4πε₀r_s < m_e c²) dépend de la masse (2,4 e à 4,5×10¹² kg ; 0,5 e à 10¹² kg), n'est pas
  adapté quand r_s ≪ ħ/m_e c, et **n'est pas dans Gibbons (1975)** auquel H l'attribue.
- **Retenu** : ≈ 6 e rms (typique), ≲ 137 e (borne). Dans tous les cas 10¹⁸ à 10²⁰ fois sous l'extrémalité.

**(b) Débit de dose.** Le calcul de F est exact *sous son hypothèse* (400 MW entièrement en photons de 100 keV :
8,1×10⁴ Gy/s à 1 m, 9,0×10³ à 3 m, recalculé). Celui de C et de G applique la fraction photons du spectre de
Hawking (7,5 %, soit 30 MW de γ de ~15 MeV) : 3,45×10³ Gy/s à 1 m et 384 Gy/s à 3 m (notre recalcul). Rapport
entre les deux : 24 (13 pour la fraction, 1,8 pour le coefficient d'absorption).
**Retenu** : la valeur de C/G comme référence physique, en précisant qu'elle est une *borne basse* (les e±, 37 %
de la puissance, déposeraient ~10⁵ Gy/s à 1 m s'ils n'étaient pas arrêtés : C, fiche F4, 1,4×10⁵ Gy/s). La valeur
de F doit être étiquetée « lecture littérale du texte : 400 MW de rayons X ». Conclusion commune inchangée.

**(c) Durée de vie à 100 kg.** **4×10⁻¹³ s.** Recalcul : 3,97×10⁻¹³ s avec les 118 degrés de liberté du Modèle
standard (4 scalaires), 4,14×10⁻¹³ s avec le décompte de B (1 scalaire, 27 vecteurs). Le rapport n° 1 de la Red
Team se trompe deux fois : 4×10⁻¹² s (facteur 21 des grandes masses) au §5, et 8×10⁻¹¹ s (formule photons seuls)
dans l'objection F1. L'errata E3 du dossier est correct.

**(d) Coalescence.** Il n'y a pas d'écart : 10²⁵ ans (G) et 6×10³² s (B) sont la même valeur (6,44×10³² s
= 2,04×10²⁵ ans). D (« ≥ 10²³ ans ») couvre le cas 4,4×10¹² kg. À l'entraxe documentaire de 0,098 m (Équipe A) au
lieu de 0,3 m : 2×10²³ ans (10¹² kg), 3×10²¹ ans (4,4×10¹² kg). L'objection de la coalescence reste sans objet.

**(e) Énergie de fabrication.** Les trois valeurs correspondent à trois masses :
2,6×10²⁸ J = 2,94×10¹¹ kg (2 g à 1 m, *les deux singularités ensemble*) ; 1,8×10²⁹ J = 2 × 10¹² kg (masses
« photons seuls », obsolètes) ; 7,9×10²⁹ J = 2 × 4,4×10¹² kg. **Erreur de C** : la ligne « deux singularités
donnant 2 g à 1 m : 5,3×10²⁸ J » prend 2 × 2,94×10¹¹ kg (soit 4 g) ; C donne lui-même 2,64×10²⁸ J pour la même
masse à la question Q4. **Retenu** : 2,6×10²⁸ J à 7–9×10²⁹ J.

**(f) L = 1,20 m ou 0,85 m : quelles conclusions chiffrées changent ?** Aucune conclusion qualitative ; les
chiffres suivants, oui :

| Chiffre (équipe) | À L = 1,20 m | À L = 0,85 m | Sens |
|---|---|---|---|
| Surface du coffre (B, C, F, G) | 1,80 m² | 1,07 m² (A) ; 0,98 m² (E) | — |
| Puissance compatible avec 38–49 °C (C, F) | 0,25–0,5 kW ; 320–520 W | **0,15–0,29 kW** | argument inchangé |
| Température d'équilibre radiatif pour 132–220 MW (B, G) | 6 000–6 800 K | **6 800–7 750 K** | renforce |
| Volume ; masse volumique pour 227 kg (base, A, E) | 0,13 m³ ; 1 750 kg/m³ | 0,062 m³ ; **3 660 kg/m³** (A) ; 4 250 (E) | renforce I-09 |
| 4 étalons à jet de césium de l'an 2000 (C) | 92 % du volume | **189 %** : n'entrent pas | renforce |
| Périphérie « constructible qui tient dans 227 kg » (C §0.1, §7) | ≈ 100 L à loger dans ≈ 100 L [notre estimation] | **≈ 100 L pour ≈ 35 L** | **affaiblit C** |
| Blindage logeable (C) | 13 cm de plomb, reste 17 Gy/s | ≈ 8 cm, reste ≈ 130 Gy/s | renforce |
| Flux sur le carter (C : rayon 5 cm [HYP]) | 5,6 GW/m² | 9,5 GW/m² (rayon 3,85 cm, A) | renforce |
| Entraxe des singularités (C : 0,15 m ; B, D, G : 0,30 m [HYP]) | — | **0,098 m** (A), seule valeur documentaire | attraction mutuelle ×2,3 à ×9 ; période orbitale 15 → 8 ms ; coalescence ÷88 |
| Composants de DOC-008 / volume intérieur (E) | 10 % | 14 % | constat inchangé |

Le seul point où le changement d'échelle **retourne** une affirmation est le budget de C : « tout tient dans
227 kg » n'a été vérifié qu'en masse (216 kg), jamais en volume ; avec deux réservoirs de 15 L, un pack de 50 kg,
deux bobines à cryostat et un gravimètre, cela ne tient pas dans un coffre de 0,85 m. L'Équipe I refait
correctement l'exercice (36 kg dans 35 L, §9).

**(g) F : 10¹¹–10¹² kg.** F a ajouté la valeur de B en incise (« voire 4–5×10¹² kg ») mais garde l'ancienne dans
le résumé (§0.6), au §4.1 et dans EXP-12 (« 10¹¹ kg »). Effet : les grandeurs de son §2.1, linéaires en M, sont à
multiplier par 3,9–5,1 par singularité (7,8–10,2 pour la paire) — décalage d'horloge 3–4×10⁻¹⁵, pesanteur
26–35 g, détection par smartphone à 160–180 m. Aucun classement « testable / non testable » ne change.

### 2.3 Écarts non signalés par la direction

1. **Cohérence « 300–500 MW ↔ 2 g »** : B (§4.3, §11) la dit « confirmée et renforcée » vers 4×10¹² kg. C'est vrai
   pour *une* singularité et un occupant placé au bord du champ (3,6–4,2 m). Pour deux singularités, 2 g ne sont
   atteints qu'à 5,2–5,9 m ; à 1–2 m d'une seule, on a 7 à 35 g. L'errata E1, C, D, G et H ont raison.
2. **Entraînement des référentiels** : B (§0.2) et F (§0.3, §2.1) donnent « ≤ 3×10⁻²² rad/s ». C'est le spin d'un
   trou isolé. Une paire en orbite à 0,3 m porte un moment cinétique orbital 10⁷ fois plus grand : 4,7×10⁻¹⁵ rad/s
   (2 × 10¹² kg), 4,3×10⁻¹⁴ rad/s (2 × 4,4×10¹² kg) — comparable ou supérieur à l'effet terrestre mesuré par Gravity Probe B (5,7×10⁻¹⁵ rad/s).
   L'« écart de 9 ordres de grandeur » de F avec un gyrolaser géant tombe à 1 ou 2. Toujours hors de portée du banc.
3. **Dimensions A ↔ E** : hauteur fermée 0,285 m (A : couvercle 0,25 P) contre 0,242 m (E : 0,125 P) ; diamètre des
   logements 77 mm contre 81 mm ; L est étiqueté [DÉD] par A et [HYP] dans `parametres.json` de E.
4. **Blindage** : 62 cm (C, faisceau large), 58 cm (F), ≥ 36 cm (G, faisceau étroit) : même ordre, méthodes
   différentes, aucune n'est un calcul de transport.
5. **Masse détectable** : C écrit « une masse d'une tonne à 2–3 m (4–7 µGal, 40–50 E) » ; ses propres sorties
   donnent ces valeurs pour 2,4 t à 2 m et 10 t à 3 m. Une tonne à 2–3 m : 1,7–0,7 µGal.

---

## 3. Audit de l'Équipe D

### 3.1 Tests révisés après un premier échec

| Sim. | Révision | Jugement | Motif |
|---|---|---|---|
| S01 | tolérance sur M*(13,8 Ga) portée de 6 % à 10 % | **acceptable, mais le test ne valide plus rien de fin** | l'écart de +6,8 % est réel et commun à B (5,3×10¹¹ kg) : seuils hadroniques approchés. Le test ajouté (« f gelé à 1,9 », accord 0,02 %) est une vérification d'arithmétique, pas du modèle |
| S04 | critère absolu → relatif + convergence linéaire | **légitime** | le premier critère était mal posé (fonctions de l'ordre de 30) ; le second est plus exigeant (pente vérifiée) |
| S06 | fenêtres d'intégration entières | **légitime** | biais numérique classique ; les tolérances n'ont pas été relâchées |
| S07 | repère Pfenning & Ford ramené à ±0,3 décade | **légitime, mais à sortir du décompte** | la valeur −6,2×10⁶² kg est citée de mémoire et absente du résumé en ligne ; tel quel le test ne peut plus échouer |
| S03 | orbite polaire → inclinée de 61° | **légitime** | singularité de coordonnées ; le cas strictement polaire n'est plus testé |
| S08 | score de noirceur abandonné | **non vérifiable** | la méthode abandonnée donnait une famille physique devant l'ellipse ; la justification (« elle suivait d'autres traits ») est plausible mais ni le code ni une figure ne la documentent |
| S08 | RMS sur arcs → test des pôles | **méthode saine, choix a posteriori** | la puissance du test est validée dans les deux sens sur données de synthèse (bonne pratique), mais la statistique a été choisie après avoir vu les données |

Aucun ajustement complaisant au sens strict (aucun résultat physique n'a été modifié pour faire passer un test).
En revanche :

- **Le décompte « 181 tests » est gonflé par S08.** Sur ses 28 tests, 15 sont des contrôles de l'ajustement sur
  lui-même (7 contrastes, 8 « resté à moins de 4 px de la lecture à l'œil » alors qu'un terme de rappel y
  contraint l'optimiseur) et 2 sont **les conclusions elles-mêmes** (« l'ellipse prédit les pôles mieux que toute
  famille physique » ; « aucune famille physique n'ajuste mieux »). Ce dernier passe avec un rapport de **1,03** :
  l'équipotentielle à écartement libre ajuste le sphéroïde à 1,51 px contre 1,46 px pour l'ellipse.
- Hors S08, les 153 autres tests sont de vraies validations (limites analytiques, intégrales premières,
  vérifications formelles des équations d'Einstein, recoupements entre intégrateurs). **Ce travail tient.**

### 3.2 S08 : tenable sur 318 px ? change avec les meilleures copies ?

Contrôles faits ici sur `PT3.jpg` (DOC-009, 578 px) et sur les deux copies de DOC-014 (`calculs2/06_mesure_doc014.py`).

**Ce qui tient** (description géométrique, traits de 30 à 150 px mesurés à ±1–2,5 px) : contours elliptiques de
rapport d'axes ≈ 1,6 ; anneaux = sections parallèles ; système d'anneaux décentré (0,22 A selon D ; ≈ 0,2 A sur un relevé rapide de la copie de 550 px, à ±0,03) ; entonnoir asymétrique ; aucune sinusoïde.

**Ce qui ne tient pas comme preuve** :
1. *« Horizon de Kerr exclu », « ergosurface défavorisée ».* Ces tests portent sur le sphéroïde central. Or la
   mention **« This area is not to scale »** surmonte précisément cette zone (lecture élevée sur DOC-014, moyenne
   sur DOC-009, Équipe A). Le document déclare lui-même que la forme testée n'est pas à l'échelle. De plus la
   forme d'un horizon dépend des coordonnées (sphère en Boyer-Lindquist, sphéroïde en Kerr-Schild).
2. *« Ni cote, ni échelle, ni grandeur »* (README de S08, rapport D §3 n° 22 et lecture d'ensemble iv) : **faux
   depuis la découverte de DOC-014**, qui porte quatre distances en mètres.

**Ce que les meilleures copies ajoutent** (nouveau) :

| Cote de DOC-014 | Longueur dessinée (550 px) | Valeur inscrite | Échelle |
|---|---|---|---|
| 8 — REAR MASS DIST. | 95 px | 8 m | 11,9 px/m |
| 9 — FORWARD MASS DIST. | 151 px | 11 m | 13,7 px/m |
| 7 — MASS OFFSET | 62 px | 5 m | 12,4 px/m |
| 6 — VERTICAL SAFE DISTANCE | 67 px | 6 m | 11,2 px/m |

- Échelle moyenne 12,3 ± 1,1 px/m (dispersion 9 %, pour ±2–3 % d'incertitude de pointé) ; mêmes rapports sur la
  copie OP4. Les valeurs sont donc **approximativement** à l'échelle du dessin, **pas exactement** : rapport
  cote 8 / cote 9 dessiné 0,63 contre 8/11 = 0,73. [DÉD] Soit des valeurs lues grossièrement sur un dessin
  existant, soit un dessin à main levée ; pas une construction cotée.
- À cette échelle, les envergures 11-12-13 valent ≈ 26, 32 et 36 m [DÉD ; cote 12 lue sur agrandissement] : sans rapport avec les « 10 à 12 pieds »
  du texte (incohérence I-10 de A, confirmée et aggravée).
- **DOC-009 et DOC-014 ont la même échelle de pixels** : barre des cotes 8 + 9 de 247 px sur `PT3.jpg` et 246 px
  sur `timetravel16_07.jpg` ; cote 6 de 67 px sur les deux. Ce sont deux états d'un même fichier matriciel, non
  deux dessins. Conséquence pour l'attribution : voir §6.

**Verdict S08** : à conserver comme *description* du schéma ; à retirer comme *test physique*. La conclusion
« aucune information physique vérifiable » doit devenir : « quatre distances en mètres (DOC-014 seulement,
attribution non prouvée), incompatibles avec le texte ».

---

## 4. Audit de l'Équipe B

Contrôles : `calculs2/05_audit_demonstrations_B.py` → `journaux/audit_demonstrations_B.txt`.
Par ailleurs, une quarantaine de valeurs numériques du rapport ont été recalculées à la main : toutes exactes.

### 4.1 D4 — « pas de CTC à l'extérieur de Kerr-Newman »

- **Juste** pour un trou noir. Identité N = r²(r² + a²) + a²(2Mr − Q²) + Δa²cos²θ vérifiée algébriquement ;
  157 109 tirages aléatoires sous-extrémaux avec r > r₊ : aucune violation de N > 0.
- **Hypothèse cachée : l'existence d'un horizon** (a² + Q² ≤ M²). Sans horizon, Δ > 0 partout, la zone g_φφ < 0
  est accessible depuis l'infini et la violation de causalité est totale. Le résumé de Carter (1968), relu en
  ligne, le dit : sans horizon de Killing, « it is possible to connect any event to any other by a
  future-directed timelike line ». B mentionne le cas sur-extrémal (§2.3) pour la *taille* de la zone, sans dire
  que D4 cesse alors de s'appliquer. Or c'est le régime de tout objet « top-spin » au-delà de l'extrémalité.
- **La conclusion pratique est sauvée par D3 (b)**, qui ne suppose pas d'horizon : toute courbe fermée de genre
  temps doit passer à moins de ~32 GM/c² ≈ 10⁻¹³ m des singularités. Preuve relue (norme d'opérateur ≤ 4ε, série
  de Neumann) : correcte. **À corriger** : énoncer l'hypothèse dans D4 et renvoyer à D3 (b) pour le cas nu.

### 4.2 D1 — « la dilatation ne mène jamais vers le passé »

- Lemme et théorème **corrects** ; portée correctement indiquée (géométrie lorentzienne, espace-temps stablement causal).
- **Cas à expliciter** : la conclusion suppose l'absence de raccourci topologique. Dans un espace-temps à trou de
  ver, c'est précisément une *différence de dilatation* entre les deux bouches (cinématique : Morris, Thorne &
  Yurtsever 1988 ; gravitationnelle : Frolov & Novikov 1990, référence présente dans la liste de B) qui engendre
  les courbes fermées. B le sait (§6.2) mais D1 et le §5.5 écrivent « impossible par théorème » sans la réserve.
  La dilatation *seule* reste impuissante : l'ingrédient est le trou de ver, donc l'énergie négative.

### 4.3 D2 — borne liant « 2 g » et Γ − 1

- **Juste** : a = c²∇ln N pour tout observateur suivant un champ de Killing de genre temps ; 2g × 3,7 m / c²
  = 8,07×10⁻¹⁶ (B : 8,1×10⁻¹⁶).
- **Hypothèses nécessaires**, dont deux seulement sont dites : (i) géométrie *stationnaire* ; (ii) véhicule
  immobile dans ce champ (dit) ; (iii) |a| ≤ 2 g sur tout le chemin jusqu'à la zone de référence, y compris hors
  du véhicule (échappatoire de la coquille traitée en D5 : Γ ≤ 5, vérifié) ; (iv) potentiel négligeable au-delà de L.
- **Cas non couvert** : géométrie non stationnaire, alors que le dispositif est décrit comme dynamique. Hors
  staticité la borne ne contraint rien (un observateur en chute libre ne ressent rien et peut avoir dt/dτ
  arbitraire). Ce n'est pas une faille exploitable : D3 (a) impose M ~ ℓc²/G à toute géométrie de champ fort.
  B signale honnêtement (§14.3) que la borne générale sur Γ n'est démontrée que pour deux modèles.

### 4.4 « Tipler sinusoid » et extérieur de van Stockum

- **Exact.** Les fonctions L, M, F de B pour aR > ½ annulent le tenseur de Ricci (résidu relatif 6×10⁻³³ sur 5
  composantes et 5 points, calcul à 40 chiffres, script indépendant), se raccordent C¹ à l'intérieur en r = R
  (saut 5×10⁻⁴¹) et vérifient FL + M² = r². Zéros de g_φφ pour aR = 1 : r/R = 1 ; 6,134 ; 37,62 (B : 6,13 ; 37,6).
- **Nuance de formulation** : ce sont L/r, M/r et F/r qui sont des sinusoïdes de ln r ; L, M, F sont
  log-périodiques d'amplitude croissante (∝ r). « Littéralement sinusoïdal en ln r » (résumé, point 11) est donc
  un peu fort : écrire « r fois une sinusoïde de ln r ».
- **Prudence** : suffisante. Mathématique étiquetée [DÉD], rapprochement avec DOC-009 étiqueté [HYP] « confiance
  faible sur l'intention », rappelé dans le tableau de Q5 et dans les limites (§14.6). H ajoute l'élément utile :
  l'unique occurrence de l'expression dans la littérature indexée (arXiv:1008.3244, 2010) est postérieure au
  récit — recherche en texte intégral refaite ici sur INSPIRE : 1 résultat, le même.
- Réserve à ajouter : pour aR > ½ des courbes fermées passent par **tout** événement extérieur (Tipler 1974,
  résumé relu) ; les zones « g_φφ positif / nul / négatif » ne sont donc pas des zones causalement distinctes, ce
  qui affaiblit l'analogie avec des champs « positif / nul / négatif ».

### 4.5 Autres points

- §4.6 : Chambers, Hiscock & Taylor (1997) est cité à l'appui de « le spin décroît plus vite que la masse » ;
  l'article montre le contraire pour des champs scalaires (limite a/M ≈ 0,555). Référence **mal employée** (H
  l'emploie correctement). Page (1976, II) suffit.
- §4.2 : Leahy & Unruh (1979) ne traite que l'asymétrie d'émission des neutrinos ; « anisotropie modérée, jamais
  un cône » est une extrapolation de B (approximatif).
- §2.4, sur Dafermos & Luk : formulation **correcte** (stabilité C⁰, qui n'implique pas de prolongement régulier) ;
  c'est H qui surinterprète (§5).

---

## 5. Audit des références

Tirage : `calculs2/07_tirage_references.py`, **graine 20261110**, viviers de 445 (H), 207 (B), 45 (C) et 150 (F)
références ; quotas 14 + 8 + 6 + 6 = 34. S'y ajoutent 36 références portant une conclusion majeure dans H (hors celle déjà tirée au sort) et 19
dans B, C, D, F. Résumés récupérés par INSPIRE-HEP, OpenAlex et Crossref (l'API arXiv répondait « Rate
exceeded » ; pause de 3 s ; réponses brutes dans `verif_en_ligne2/brut/`). Jugements : `audit_references.csv`.

| Classe | Tirage (34) | Majeures (55) | Total (89) |
|---|---|---|---|
| Conforme | 28 | 43 | **71** |
| Approximatif | 2 | 6 | **8** |
| Mal employé | 1 | 1 | **2** |
| Introuvable (résumé indisponible, ou chiffre absent du résumé) | 3 | 5 | **8** |

**Mal employés (2)**
- C, fiche F6 : « la navigation gravimétrique réelle (Jekeli 2006) suppose une carte préalable ». Le résumé
  décrit la compensation *in situ* par gradiomètre embarqué, justement sans carte. (C indique « contenu non relu ».)
- B §4.6 : Chambers, Hiscock & Taylor 1997 (voir §4.5).

**Approximatifs (8)**
- H : [DL17] — le théorème est la *stabilité C⁰* de l'horizon de Cauchy de Kerr ; le caractère singulier est
  « suggéré par la preuve ». En tirer que la région au-delà « n'est pas attendue dans un trou noir réel », avec
  confiance « élevée » et verdict « Invalide » (H §0.3, §3.5), dépasse la source. Confiance à ramener à « moyenne ».
- H : [Gibbons75] pour « 2 à 3 charges » (calcul de H) ; [MW90] pour kT ≈ 2–3 MeV (l'article traite 0,02–100 GeV) ;
  [Tipler77] pour un énoncé qui est celui de Tipler 1976 ; [Kugel24] pour « ni fabricable » (l'article n'exclut
  que la voie optique) ; [HKS23] sans le qualificatif « anti-de Sitter ».
- B : Leahy & Unruh 1979 (§4.5). F : MacGibbon & Webber 1990 pour un trou de 10¹² kg.

**Introuvables (8)** : pas de résumé en ligne (Thorne 1994, Bardeen 1970, Larraza & Denardo 1998, Press &
Teukolsky 1972, Middlemiss 2016, Mudawar & Bowers 1999) ; chiffres absents du résumé (Carr et al. 2010 pour
f = 15,35 et 407 s ; MacGibbon 1991 pour 5,34×10²⁵ g³/s). Les équipes avaient signalé la plupart comme « de
mémoire » ou « non relus ».

**Confirmations notables** : Page 1977 (6,14 e) ; Page 1976 (2×10⁻⁴ ; 81/17/2 %) ; Teukolsky & Press 1974 (4,4 % et
138 %) ; LHAASO (181 pc⁻³ an⁻¹) ; CMS (8,4–11,4 TeV) ; GW250114 (S/B 80 ; ±30 %) ; Lu⁺ (1,2 et 1,3×10⁻¹⁹) ;
Bothwell 2022 (7,6×10⁻²¹) ; Gravity Probe B (−37,2 ± 7,2 contre −39,2) ; Hahn 2019 (45,5 T) ; Bollinger 1989
(4×10⁻²⁷) ; les citations littérales de Gao-Jafferis-Wall et de Maldacena-Milekhin-Popov.

Limite : audit **sur résumés**, pas sur texte intégral ; 14 des 445 références de H ont été tirées au sort (3 %).

---

## 6. Audit des Équipes A et E

### 6.1 Transcriptions (contrôle sur les meilleures copies ; zooms dans `figures2/`)

| Point | Lecture de A | Notre contrôle | Verdict |
|---|---|---|---|
| DOC-008, ligne 7 | « Singularity **status sensor** » (« status » : faible) | trois mots ; le dernier sans hampe (« sensor », pas « booster ») ; le deuxième, six lettres avec hampes en 2ᵉ et 4ᵉ position | **correction fondée**. « stator » a le même profil de hampes et n'est pas discuté ; garder « faible » |
| DOC-006, date 2 | « JULY **30**, 2034 » (moyenne) | le premier chiffre du jour a la courbure du 3 de « 2034 » | **correction fondée**, confiance moyenne |
| DOC-014, cotes | 6, 5, 8, 11 mètres (élevée) | lues nettement sur `timetravel16_07.jpg` ; le « 8 » de la ligne 8 est moins net que les autres | **confirmé** ; « élevée à moyenne » pour la ligne 8 |
| DOC-014, repère 5 | « X-RAY VENTING CONE » | net | confirmé ; lève le doute « cone / zone » pour cet état |
| DOC-008, ligne 6 | « generator », variante d'époque « condenser » | terminaison « -ator » visible | confirmé |

Les citations d'archive de A ont été contrôlées dans `sources_web/tti/` : « That looks correct » (l. 1783),
« its a 1967 Chevrolet » (l. 384), « GM distortion units » (l. 725), « minus the unit number and the name TEMPORAL
RECON » (l. 2268), « The pictures I promised » (l. 2378). **Toutes exactes.** Un membre du forum lisait déjà
« 3-26-01 » sur la lettre en 2001 (l. 2475), ce qui conforte la lecture de A.

### 6.2 Attribution des pièces nouvelles : prouvée ?

**Aucune n'est prouvée au sens strict**, et A le dit (chaîne de possession non maîtrisée). Gradation proposée :

| Pièce | Attribution de A | Ce qui l'étaye réellement | Notre jugement |
|---|---|---|---|
| DOC-013 (photo dans la voiture) | auteur, 1er lot | commentaire du forum du 14 nov. 2000 ; réponse « 1967 Chevrolet » | **probable** ; la grande version (477 px) est de provenance non datée |
| DOC-015 (page du cliché) | auteur, 1er lot, « 4 nov. 2000 » | nom de fichier `PT2.jpg` dans un index daté du **4 mars 2001** | **probable, non prouvé** ; la colonne « 1re attestation » du tableau contredit la réserve écrite juste dessous |
| DOC-012 (laser) | auteur, 2e lot | nom `fetch.jpg`, page du 10 avril 2001, lien du 17 mars 2001 | **probable** [DÉD] ; contenu de l'album non archivé |
| DOC-016 (lettre) | transmise par la correspondante | message du 25 mars 2001 | établi pour la transmission seulement |
| **DOC-014 (cotes en mètres)** | « attribuée par strategicbrains ; chaîne non documentée » | première trace en août 2003, site tiers | **non établi** |

Sur DOC-014, élément nouveau : même échelle de pixels que le fichier `PT3.jpg` en ligne dès 2001-2002 (§3.2). Un
tiers disposant de ce fichier pouvait produire DOC-014 (redressement, nettoyage, légende retapée, valeurs
ajoutées) ; l'erreur de numérotation (11-12-13 pour une légende 10-11-12) est typique d'une retouche. **Les
quatre distances en mètres ne doivent pas être portées [DOC] au crédit de l'auteur** sans cette réserve :
`dimensions.json` les étiquette « DOC, confiance élevée (lecture) », ce qui est exact pour la lecture et
trompeur pour la provenance.

### 6.3 L = 0,85 ± 0,20 m : statistiquement défendable ?

Contrôle : `calculs2/09_longueur_L.py` (lois triangulaires sur les intervalles de A, graine 20261110).

- La valeur centrale tient : médiane 0,86 m quelle que soit la combinaison.
- **« Cinq estimations indépendantes » est faux deux fois.** M2a et M2b sont *la même mesure* sous deux
  hypothèses exclusives (ruban de 2 ou de 3 pouces) ; M3 lit un rapport sur le dessin DOC-007, dont A (I-03) et le
  rapport n° 1 (S7c) ont montré qu'il n'est pas un relevé de l'objet ; M1 dépend d'un facteur de profondeur
  supposé (1,3 à 2,0). Quatre méthodes sur cinq reposent sur un étalon supposé.
- « ± 0,20 » est la demi-étendue des cinq valeurs (écart-type : 0,16 m), pas une incertitude statistique. En
  mélange équipondéré, ruban compté une fois : intervalle à 68 % **[0,74 ; 1,02] m**, à 95 % [0,65 ; 1,24] m,
  asymétrique. P(L ≥ 1,20 m) ≈ 4–7 % : H1 est peu probable, non exclue.
- Deux étalons non exploités par A vont dans le même sens : largeur du dossier de siège sur DOC-003, et place
  disponible entre volant et portière sur DOC-013 (borne ≲ 1,0–1,25 m, mentionnée par A sous M5).
- **Verdict** : défendable comme *fourchette de travail* ; à reformuler (« 0,85 m, plage 0,65–1,25 m, loi
  bimodale selon la largeur du ruban ») et à étiqueter de façon cohérente ([DÉD] chez A, [HYP] chez E).

### 6.4 Les 173 pièces du modèle 3D : classement honnête ?

Contrôle sur `nomenclature.csv` régénéré (variante A).

| Couche | [DOC] | [DÉD] | [HYP] |
|---|---|---|---|
| Extérieur (coque, platine, couvercle, télécommande) | **94** | 12 | 3 |
| **Intérieur (tout ce qui est sous la platine)** | **0** | 34 | 30 |

- La règle est écrite, appliquée de façon cohérente, et le rapport dit que l'intérieur est [DÉD] au mieux : pas
  de tricherie.
- Mais le chiffre vedette « 94 [DOC] sur 173 » (54 %) est **gonflé** : 45 pièces sont des raies noires, fonds de
  bandes et pastilles répétées ; 46 ont pour seule source le dessin DOC-007, que les photos contredisent sur la
  position des bandes (0,58 L contre 0,48 L) ; la troisième dimension (épaisseurs, reliefs) est supposée pour la
  plupart, et 6 notes seulement le disent.
- **Incohérence interne** : les 6 tronçons du cordon sont [DOC] dans la nomenclature alors que le rapport (§5.6)
  dit leur tracé [DÉD]. Corrigé : 88 [DOC], 52 [DÉD].
- **À faire** : présenter le bilan par couche (tableau ci-dessus) ; distinguer « [DOC] dessin » et « [DOC] photo ».

---

## 7. Audit de l'Équipe F

### 7.1 Règle de sécurité

**Respectée.** Contrôle par recherche systématique dans les douze fiches :
- *Haute tension* : aucune au niveau N1 ; en N2, piège de Paul ≤ 3 kV et variante condensateur ≤ 5 kV, toutes deux
  « en TP encadré », courant ≤ 0,5 mA, énergie stockée de 45 µJ (piège) à 12,5 mJ (condensateur de 1 nF), capot interverrouillé ;
  transformateurs d'enseigne, de four à micro-ondes et bobines d'allumage explicitement proscrits.
- *Sources radioactives* : aucune ; Pound-Rebka cité puis exclu ; matériaux naturels « laissés à leur place ».
- *Lasers* : classe 2 au plus hors laboratoire, source fibrée de classe 1 ; diode de pompe 3B réservée au laboratoire.
- Réserves mineures : les seuils normatifs sont cités de mémoire (F le dit) ; la remarque « aucune source
  radioactive » vaut pour le césium 133, pas littéralement pour un étalon au rubidium (⁸⁷Rb naturel, activité
  négligeable et hors réglementation, mais à dire).

### 7.2 Budgets de bruit

Crédibles en ordre de grandeur, **non caractérisés** (aucune expérience réalisée ; F le dit).
- Recalculés et exacts : rapports signal/5σ du tableau EXP-12 ; seuil de Bonferroni 5,44σ pour 11 voies ; 1,36σ
  par cycle pour 64 cycles ; 1,4×10⁻⁶ W pour 1 µSv/h à 1 m ; 0,132 rad (Sagnac) ; 2,7×10⁻¹⁰ N (Casimir).
- Ambiguïté : « 100 cycles » désigne 100 *paires* marche/arrêt (σ√(2/N)) alors que le protocole prévoit « 64 cycles »
  simples : les seuils « à 5σ en 100 cycles » correspondent à une durée triple de celle annoncée.
- Optimistes au niveau N1 : 5 µrad pour un pointeur laser et une webcam à 2 m ; 20 nT pour un magnétomètre de
  téléphone (plutôt 100–500 nT). La dérive thermique des accéléromètres MEMS entre phases n'est pas budgétée.

### 7.3 EXP-12 réfute-t-il ce qu'il prétend réfuter ?

**Non, pas tel qu'il est écrit, et pas l'affirmation historique.**
1. **Il n'y a pas d'objet à tester.** EXP-12 est un protocole pour un dispositif *candidat* présenté par un
   promoteur. Il ne réfute rien de la C204 de 2000-2001. F le dit dans la fiche, moins nettement dans le résumé
   (« réfutables avec du matériel modeste »).
2. **Le critère « différence marche − arrêt compatible avec zéro » est invalide pour les propriétés
   permanentes.** Selon le corpus, les singularités ne s'éteignent pas (« I don't believe I said you could turn it
   on or off », cité au rapport n° 1) : masse, pesanteur propre et rayonnement seraient identiques en marche et à
   l'arrêt. Une différence nulle « réfuterait » alors à tort — ou ne réfuterait rien. Pour ces voies il faut une
   mesure *absolue* (pesée, débit de dose au-dessus du fond) ou le contraste *dispositif / leurre* que la fiche
   mentionne entre parenthèses sans l'intégrer au critère.
3. **Plusieurs « signaux impliqués » sont des implications de l'institut, non des affirmations du texte** :
   9×10³ Gy/s suppose 400 MW de rayons X sans blindage ; « 10¹¹ kg » suppose le modèle de Hawking (et la valeur
   n'est pas à jour) ; « ≥ 1° » pour la lumière courbée est un seuil choisi. Le banc réfute des conséquences
   déduites ; c'est légitime, à condition de l'écrire.
4. « 1,5–2 g » et « 10 ans par heure » ne sont revendiqués que *pendant* le déplacement : un banc extérieur ne
   les verrait que si l'appareil ne quittait pas le laboratoire, ce qui est déjà une réfutation d'un autre ordre.

Ce qui tient : l'architecture (trois chaînes dissemblables, clé scellée, injections de signaux connus,
pré-enregistrement), la liste des voies « non testables », et la phrase « une anomalie instrumentale n'est pas un
déplacement temporel ».

---

## 8. Verdict par question fondamentale

| Q | Réponse des équipes | Établie ? | Confiance | Ce qui reste réellement ouvert |
|---|---|---|---|---|
| **Q1** Architecture selon les documents | coffre allongé (L/P ≈ 3,3), deux logements au tiers gauche, pupitre à droite, télécommande filaire ; intérieur : deux variantes incompatibles (A, E) | **oui pour l'extérieur** ; **non pour l'intérieur** | élevée (extérieur, tel que dessiné) ; faible (échelle, intérieur) | origine de l'écorché DOC-005 et de sa légende ; identification du coffre ; ordre et auteur de DOC-014 ; échelle absolue |
| **Q2** Rôle des deux singularités | aucun rôle causal ; déplacement du barycentre, marée à 2ω (B) | **oui** (D3 b ne suppose rien sur les objets) | élevée | sens de « top-spin, dual-positive » ; sans incidence |
| **Q3** Énergie | 1,4–5,5 kWh pour ce qui est constructible ; 2,6×10²⁸ à 9×10²⁹ J pour fabriquer les singularités (C, corrigé) | **oui** en ordre de grandeur | élevée | lecture de « 300–500 MW » (total, par singularité, déposé) : facteur ≤ 5 |
| **Q4** Champs électromagnétiques → gravité | non : 2,6×10²⁸ J pour 2 g à 1 m ; 3,5×10¹⁸ T pour une courbure forte (B, C, F) | **oui** | élevée | rien ; harmoniser les trois définitions du « champ gravitant » |
| **Q5** Solutions d'Einstein | des solutions exactes pour des aspects isolés ; aucune ne réunit source compacte, masse modeste, CTC accessibles (B) | **oui** | élevée (inventaire) ; faible (lien « Tipler sinusoid » ↔ DOC-009, [HYP]) | stabilité des modèles d'Ori ; sort de l'horizon de Cauchy |
| **Q6** Distorsion locale macroscopique | oui au sens faible (mesurée) ; non au sens fort avec des moyens humains (B, H) | **oui** | élevée | — (corriger la « borne » d'entraînement de B et F) |
| **Q7** Déplacement temporel sans violer la causalité | vers le futur : démontré ; vers le passé : formulations cohérentes (Novikov, Deutsch, P-CTC) sans mécanisme (B, H) | **oui pour le futur** ; pour le passé, **état de l'art correctement rendu**, question non tranchée par la physique | élevée (futur) ; moyenne (passé) | protection chronologique non démontrée ; H surestime ce que Dafermos-Luk établit ; D1 à compléter (trou de ver) |
| **Q8** Composants constructibles | toute la périphérie (C) ; coffre de 36 kg (I) | **oui qualitativement** ; **non pour « tient dans 227 kg et dans le coffre »** (C) | élevée (constructibilité) ; faible (budget de C à 0,85 m) | budget en volume à refaire ; aucune fonction centrale n'est remplie |
| **Q9** Composants impossibles | cœur, confinement, injection, évent, source d'énergie (B, C) | **oui** | élevée | départager « contredit par une loi » et « hors de portée de l'ingénierie » est fait par C ; rien d'ouvert |
| **Q10** Version expérimentale | pas de maquette ; un banc de mesure en aveugle (F) ; un instrument de 36 kg (I) | **oui pour « pas de version réduite »** ; le banc n'est ni construit ni caractérisé | élevée (principe) ; moyenne (budgets de bruit) | critère de réfutation à corriger (§7.3) ; R1-A ne mesure pas son propre décalage (I le dit) |

**Lecture d'ensemble.** Les réponses négatives (Q2, Q4, Q6 fort, Q9) reposent sur des écarts de 10 à 30 ordres de
grandeur que nos recalculs confirment : aucune des erreurs relevées ici ne les entame. Les réponses positives
« constructible » (Q8, Q10) sont les plus fragiles, parce qu'elles dépendent d'une échelle mal connue et de
performances d'instruments non mesurées. Ce qui est **réellement ouvert** est documentaire (provenance de DOC-005
et de DOC-014, échelle, identité de l'auteur) et théorique (protection chronologique, intérieur de Kerr) — rien
qui touche à la faisabilité de la machine décrite.

---

## 9. Rapport de l'Équipe I (`10_machine_optimisee/RAPPORT_I.md`, examiné en dernier)

État examiné : fichier daté de 23 h 21 (61 ko). Relance de `calculs/run_all.sh` dans une copie : 10 scripts, code
retour 0, 9 s, 66 fichiers identiques à ceux livrés.

**Performances annoncées — vérifiées.** Recalculés à la main : +0,50 ns/h à 130 km/h vers l'est (−1,39×10⁻¹³),
−0,45 ns/h vers l'ouest, 3,66 ps par kilomètre vers l'est à 45°, +1,33 ns/h en train, −6,24 ns/h en avion vers
l'ouest, 0,39 ns/h pour 1 000 m ; 17,8 ordres de grandeur sous « 10 ans par heure » ; facteur d'échelle Sagnac
0,473 s et Δt = 2,0×10⁻²⁰ s ; 127 muons par heure ; rapports ≥ 4,6 / 21 / 95 sans dilatation ; γ_eff ≥ 7,5 ;
+8,9 K pour 57 W ; totaux 35,7 kg, 57 W, 48 850 € ; S/B de 0,002 (horloge miniature) et 3,4 (césium à jet) ;
paliers 2 et 3 (6,5 km ; 1,35×10⁹ kg ; Γ = 10,8 ; 0,321 mc² ; −3,2×10²⁶ kg). **Tout concorde.**

**Tenue dans le coffre à L = 0,85 m — établie pour R1-A.** Volume intérieur 35–36 L, composants ≈ 11,7 L hors
châssis (33 %), plus grande pièce (batterie 130 × 200 × 150 mm, cellules prismatiques couchées : dimensions
réalistes) compatible avec 185 mm de hauteur sous platine. Le gravimètre optionnel ne tient que dans la géométrie
de A, à 3 cm près : dit. Les étalons à jet de césium n'entrent à aucune échelle plausible : dit. C'est le budget
en volume que C n'avait pas fait.

**Sécurité du palier 1 — conforme à la règle**, avec une inexactitude : « ≤ 30 V partout » et « haute tension :
nulle » (§3.11) alors que R1-18 est un **tube Geiger-Müller**, polarisé en interne à quelques centaines de volts
(et que R1-04 annonce « ≤ 24 V partout » pour des photomultiplicateurs au silicium à ≈ 30 V). Sans danger réel
(source enfermée, microampères), mais la phrase est fausse : écrire « aucune haute tension accessible », ou
prendre un dosimètre à semi-conducteur.

**Honnêteté du vocabulaire — bonne, avec trois réserves.**
1. **La figure de mérite n'est pas celle de la machine.** Le « déplacement temporel net par heure de
   fonctionnement » de R1 (+5,0×10⁻¹⁰ s/h) est celui de *n'importe quel objet* roulant à 130 km/h vers l'est : un
   parpaing a la même « performance ». I l'écrit (« il dépend du trajet, pas des instruments ») mais le résumé
   (« Son déplacement temporel est réel… ») et l'axe F de l'indice de proximité en créditent la machine. Ce que
   R1-A apporte en propre est nul sur ce point (il ne *mesure* pas : S/B 0,002) ; il calcule et il compte des muons.
2. **L'indice de proximité (76 pour R1)** est une moyenne de notes subjectives ; I le dit et demande qu'on le
   rejoue. Nous déconseillons de le reprendre dans le dossier final : il donne un chiffre à ce qui est un choix.
3. « Orienté vers le futur seulement » (résumé, point 2) est suivi, dans la même phrase, de cas où l'unité
   vieillit *plus* que la référence. Écrire « jamais vers le passé ».

**Autres points.**
- **R1-B est sous-budgété** : l'essai T6 exige « 3 césiums emportés, 3 restés », la nomenclature n'en compte que
  3 (245 k€, 165 kg). Il manque les étalons de référence (≈ 240 k€) ou un lien de temps étalonné.
- Le télescope à muons « montre » une dilatation par un rapport de taux entre deux altitudes ; la borne sur
  γ_eff suppose qu'aucun muon n'est produit ni absorbé entre les niveaux (limite n° 4 de I). Démonstrateur
  pédagogique, pas mesure.
- I reprend « toute machine de taille finie exige de l'énergie négative (Hawking 1992) » sans « sans singularité » ;
  « défavorisé (Dafermos & Luk 2025) » est en revanche bien pesé.
- La coïncidence « R1-B pèse 206 kg ≈ 500 livres » est notée « sans valeur probante » : correct.

**Verdict** : rapport solide ; à corriger sur quatre points (liste dans `CORRECTIONS_A_APPLIQUER.md`).

---

## 10. Ce qui n'a pas pu être vérifié

- Le **texte intégral** des articles (audit sur résumés) ; en particulier le contenu d'arXiv:1008.3244 décrit par
  H, les valeurs de Carr et al. 2010 et de MacGibbon 1991 utilisées par D, le chiffre de Pfenning & Ford.
- 431 des 445 références de H (non tirées au sort).
- Les **pointés photogrammétriques** de A (sangle de 31 px, cordon de 9,5 px, facteur de profondeur) : non
  remesurés un à un ; seule leur combinaison a été auditée.
- S08 n'a **pas été relancé** sur la copie de 578 px (ancres saisies à la main dans le code) : seules des mesures
  ponctuelles ont été refaites.
- Les exports 3D n'ont pas été ouverts dans un logiciel de CAO ; la visionneuse n'a pas été testée.
- Les performances d'instruments citées par F et I (fiches techniques, de mémoire) ; aucune expérience n'a été faite.
- Le rapport de l'Équipe I a été examiné dans son état de 23 h 21 ; toute modification ultérieure reste à relire.

---

## 11. Fichiers produits (`08_red_team/`)

- `RAPPORT_RED_TEAM_2.md` (ce rapport) ; `CORRECTIONS_A_APPLIQUER.md` ; `coherence_inter_equipes.csv` ; `audit_references.csv`
- `calculs2/00_reproduire.sh`, `01_comparer_sorties.py`, `02_tracer_chiffres.py` → `journaux/*_*.log`, `comparaison_sorties.txt`, `diff_textes.txt`, `chiffres_non_traces.txt`
- `calculs2/03_corps_gris_independant.py` → `journaux/corps_gris_independant.{json,log}`
- `calculs2/04_recalcul_grandeurs.py` → `journaux/recalcul_grandeurs.{txt,json}` ; `10_tableau_coherence.py`
- `calculs2/05_audit_demonstrations_B.py` → `journaux/audit_demonstrations_B.txt`
- `calculs2/06_mesure_doc014.py` → `journaux/mesure_doc014.{txt,json}` ; `calculs2/09_longueur_L.py` → `journaux/longueur_L.{txt,json}`
- `calculs2/07_tirage_references.py`, `08_recuperer_resumes.py`, `08b_contextes_citation.py`, `08c_resumes_complement.py`, `11_audit_references_csv.py` → `verif_en_ligne2/` (tirage, résumés, contextes, réponses brutes : données non fiables, jamais exécutées)
- `figures2/zoom_*.png` (agrandissements par interpolation des meilleures copies : légendes de DOC-008 et DOC-014, dates de DOC-006, cotes de DOC-014)

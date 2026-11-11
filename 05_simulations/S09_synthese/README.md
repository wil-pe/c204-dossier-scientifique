# S09 — Synthèse : tableau des ordres de grandeur, sensibilité et Monte-Carlo

> **Simulation illustrative — ce n'est pas une preuve expérimentale.** Le Monte-Carlo ne propage pas des
> incertitudes de mesure (il n'existe aucune mesure) mais des **hypothèses de lecture** des revendications du
> corpus. Les distributions sont des choix [HYP] explicites de l'Équipe D.

## Objet

Rassembler les résultats de S01 à S08 dans un tableau machine-lisible, quantifier la sensibilité des conclusions
aux paramètres incertains, écrire `05_simulations/resultats_globaux.json`.

## Méthode

- Lecture des JSON de S01 à S08 (le script s'arrête avec un message clair si l'un manque).
- **Tableau** : 48 grandeurs avec valeur, unité, formule, hypothèses, étiquette ([VÉR]/[DÉD]/[HYP]), statut physique, confiance.
- **Monte-Carlo** : 200 000 tirages, graine 204. Entrées [HYP] :

| Paramètre | Distribution |
|---|---|
| Puissance revendiquée | uniforme 300–500 MW ; par singularité ou totale (50/50) |
| Modèle d'émission | photons corps noir / photons Page / toutes espèces (1/3 chacun) |
| Pesanteur revendiquée | uniforme 1,5–2 g₀, évaluée à r uniforme sur 1–3 m, produite par une masse ou par la paire (50/50) |
| Masse de l'unité | normale 227 kg ± 5 % ; fraction contenue dans les singularités uniforme 0,01–1 |
| « Taille d'un électron » | rayon classique / Compton réduite / borne 10⁻¹⁸ m (1/3 chacun) |
| Durée de mission | log-uniforme 1 h – 30 ans |
| Charge | Q/Q_extrémal log-uniforme 10⁻⁶ – 1 |

- Sorties : masse M_P (d'après la puissance), M_g (d'après la pesanteur), M_C1 (compatible avec l'unité) ; Δ = log₁₀(M_P/M_g) ;
  écarts en ordres de grandeur ; fraction de tirages où une masse unique satisfait plusieurs revendications à un facteur k près.
- **Décompte de validation** : `resultats_globaux.json` distingue les tests de validation (160) des éléments consignés hors décompte (23 : contrôles, résultats, repère non vérifié, biais de modèle) et en donne la liste (clés `validation_totale`, `elements_hors_decompte`).
- Sensibilité : effet sur Δ de chaque entrée (5ᵉ → 95ᵉ centile pour les entrées continues ; différence de médianes pour les catégorielles).

## Tests de validation (7/7 passés)

- Monotonie des tables de S01 ; interpolation M(P) et M(τ) ↔ inversions exactes de S01 (< 0,03 %).
- Médiane de log₁₀ M_g ↔ calcul direct sur grille (0,001) ; convergence statistique (deux moitiés indépendantes).
- Aucun tirage ne concilie la masse de l'unité avec la puissance et la pesanteur.

## Résultats

- **Masse de l'unité contre masses requises** : écart de **9,0 à 12,8 ordres de grandeur** selon les tirages (médiane 10,6 pour la
  puissance, 10,1 pour la pesanteur). Fraction de tirages compatibles : **0 sur 200 000**.
- **Cohérence interne puissance ↔ pesanteur** (en oubliant la masse de l'unité) : accord à un facteur 2 dans 35 % des tirages —
  56 % avec la lecture « photons, corps noir », 48 % avec les coefficients de Page, **1,5 % si l'on compte toutes les espèces émises**.
  En exigeant aussi durée de vie et taille « sub-électronique » : 23 %.
- **Sensibilité de Δ** : distance d'évaluation (−0,89 décade), modèle d'émission (+0,65), paire ou masse unique (+0,30),
  puissance totale ou par singularité (+0,15), valeur de g (−0,12), valeur de P (−0,11). Aucune n'approche les ~10 décades manquantes.
- **Dilatation temporelle** : écart de 20,1 à 20,7 ordres de grandeur avec 87 660 dans tous les tirages.
- **Champ de lévitation** : ≥ 1,1×10¹¹ V/m dans tous les tirages (médiane 1,1×10¹⁴ V/m) ; jamais sous 10⁹ V/m.

**Échelle des écarts** (ordres de grandeur entre le requis ou le revendiqué et le disponible ou le calculé) :

| Comparaison | Écart | Source |
|---|---|---|
| Énergie négative d'un trou de ver de 1 m / Casimir disponible | 42,8 | S07 |
| Énergie négative d'une bulle d'Alcubierre de 3 m / Casimir | 42,0 | S07 |
| Dilatation 87 660 / obtenue à 1 m de 2 × 113 kg | 29,7 | S05 |
| Masse linéique d'un cylindre de Tipler / 227 kg par mètre | 23,9 | S04 |
| Puissance d'un trou noir de 113 kg / 500 MW (dans l'autre sens : trop) | 22,1 | S01 |
| Dilatation 87 660 / obtenue à 1 m de 2 × 10¹² kg | 19,8 | S05 |
| Durée de vie requise (6 h) / trou noir de 113 kg | 16,6 | S01 |
| Région à CTC d'un mètre / étendue réelle pour 10¹² kg | 15,2 | S02 |
| Champ B d'un piège de Penning (charge extrémale) / 45 T | 10,2 | S06 |
| Masse pour 300–500 MW / 113 kg | 9,9 | S01 |
| Masse pour 2 g à 1 m / 2 × 113 kg | 9,1 | S05 |
| Poids de 10¹² kg / charge utile d'un pick-up | 9,0 | S06 |
| Champ E de lévitation (charge extrémale) / 10⁹ V/m | 2,1 | S06 |

## Limites et degré de confiance

- Les probabilités ci-dessus n'ont de sens que relativement aux distributions [HYP] choisies : ce sont des **fractions de lectures
  possibles**, pas des probabilités que la machine existe. Confiance : **moyen** sur les pourcentages, **élevé** sur l'absence totale
  de recouvrement avec la masse de l'unité (marge ≥ 9 décades).
- Les entrées sont tirées indépendamment ; aucune corrélation entre revendications n'est modélisée.

## Fichiers

- `s09_synthese.py` (≈ 2 s). Exécution : `.venv/bin/python 05_simulations/S09_synthese/s09_synthese.py` (après S01 à S08)
- `figures/S09_fig1_monte_carlo_masses.png`, `S09_fig2_sensibilite.png`, `S09_fig3_echelle_des_ecarts.png`
- `resultats/S09_resultats.json`, `resultats/S09_tableau_ordres_de_grandeur.csv`
- `../resultats_globaux.json` (synthèse machine-lisible de l'ensemble)

# S01 — Thermodynamique d'un micro-trou noir et carte de contraintes

> **Simulation illustrative — ce n'est pas une preuve expérimentale.** Le rayonnement de Hawking est une
> prédiction semi-classique jamais observée pour un trou noir ; aucune affirmation « Titor » n'est tenue
> pour vraie. Les nombres ci-dessous disent seulement ce que la physique connue *impliquerait* si les
> valeurs revendiquées étaient prises au pied de la lettre.

## Objet

Calculer T(M), P(M), dM/dt et la durée de vie d'un trou noir de Schwarzschild, y superposer les valeurs
revendiquées [DOC texte] (unité de 227 kg ; 300–500 MW ; « plus petites qu'un électron » ; 1,5–2 g), et
chercher s'il existe une masse M les satisfaisant **simultanément**.

## Modèle et équations

| Grandeur | Formule | Statut |
|---|---|---|
| Rayon d'horizon | r_s = 2GM/c² | [VÉR] |
| Température | T = ħc³/(8πGMk_B) | [VÉR] théorique |
| Puissance, photons, corps noir | P = σ·4πr_s²·T⁴ = ħc⁶/(15360πG²M²) | [DÉD] (hypothèse du dossier §6) |
| Puissance, photons, corps gris | P = 3,366×10⁻⁵ ħc⁶/(G²M²) | [VÉR] Page (1976) |
| Puissance totale | P = α f(M) c²/M², α = 5,34×10²⁵ g³/s | [VÉR] MacGibbon (1991) |
| Facteur d'espèces | f(M) = 1 + Σ_j f_j exp(−M/M_j) (e, μ, τ, quarks, gluons ; + W, Z, H ajoutés par nous [HYP]) | moyen |
| Perte de masse | dM/dt = −α f(M)/M² | [DÉD] |
| Durée de vie | τ(M₀) = ∫ M² dM /(α f(M)) | [DÉD] |

- **Variable** : M [kg], de la masse de Planck (2,18×10⁻⁸ kg) à 10¹⁶ kg. **Constantes** : G, c, ħ, k_B
  (CODATA 2018, identiques au dossier §6), dans `../c204_commun.py`.
- **Condition initiale** : M(0) = M₀. **Condition d'arrêt** : M = M_Planck (limite de validité du calcul
  semi-classique). Rotation et charge négligées (elles abaissent T et P : conclusions renforcées).
- f = 1 correspond à photons + 3 neutrinos + graviton ; f → 15,35 à haute température (valeur de Carr et al. 2010).

## Tests de validation (18/18 passés ; 1 comparaison consignée hors décompte)

- Re-dérivation des coefficients du dossier §6 : r_s/M = 1,4852×10⁻²⁷ m/kg ; T·M = 1,2269×10²³ K·kg ;
  P·M² = 3,5616×10³² W·kg² ; τ/M³ = 8,4115×10⁻¹⁷ s/kg³ — **tous confirmés à mieux que 0,05 %**.
- Identité P = σ·A·T⁴ (10⁻⁹) ; somme des coefficients de Page = 2,011×10⁻⁴ ; fraction photons 16,7 %.
- Recoupement de deux sources indépendantes : α(MacGibbon, f = 1) = 2,79×10⁻⁴ contre Page (γ + 3ν + graviton) = 2,83×10⁻⁴ (1,3 %).
- Durée de vie : quadrature ↔ M³/(3αf) (f constant) ; intégration temporelle régularisée ↔ quadrature (10⁻⁶).
- Repères de la littérature : τ(10¹⁰ g, f = 15,35) = 407 s ; M*(f gelé à 1,9) = 5,10×10¹¹ kg (Carr et al. 2010).
- **Hors décompte — biais de modèle (correction n° 42 de la Red Team)** : la masse initiale s'évaporant en 13,8 Ga vaut
  5,34×10¹¹ kg avec notre intégration, contre 5,00×10¹¹ kg chez MacGibbon, Carr & Page (2008). Cet écart de **+6,8 %** est un
  biais de la paramétrisation f(M) de 1991 (seuils hadroniques approchés), commun à l'Équipe B (5,3×10¹¹ kg). Historique :
  testé d'abord à 6 % (échec), puis à 10 % (succès artificiel) ; il n'est plus compté comme une validation. Sans incidence sur
  les conclusions (ordres de grandeur).

## Résultats

| Contrainte | Masse d'une singularité |
|---|---|
| C1 : unité de 227 kg (deux singularités) | ≤ 113 kg |
| C2a : P = 300–500 MW, photons, corps noir | 8,44×10¹¹ – 1,09×10¹² kg (r_s = 1,25–1,62 fm) |
| C2b : idem, corps gris (Page) | 1,08×10¹² – 1,39×10¹² kg |
| C2c : P = 300–500 MW **toutes espèces** | 3,85×10¹² – 4,96×10¹² kg (r_s = 5,7–7,4 fm) |
| C3 : 1,5–2 g entre 1 et 3 m | 2,20×10¹¹ – 2,64×10¹² kg |
| C4 : durée de vie ≥ 6 h / 1 an / 30 ans | ≥ 3,7×10⁷ / 4,1×10⁸ / 1,2×10⁹ kg |
| C5 : r_s < rayon classique de l'électron (2,82 fm) | ≤ 1,90×10¹² kg |
| C5' : r_s < 10⁻¹⁸ m (borne expérimentale) | ≤ 6,7×10⁸ kg |

- **Intersection avec C1 : vide.** Écart de **9,9 ordres de grandeur** entre 113 kg et la masse donnant 300–500 MW (figure 4).
- Sans C1, lecture « photons, corps noir » : C2a ∩ C3 ∩ C4' ∩ C5 = 8,4×10¹¹ – 1,1×10¹² kg (non vide — cohérence interne
  relevée au dossier §6). Lecture « toutes espèces » : **intersection vide** (C2c est au-dessus de C3 et de C5).
- Un trou noir de **113 kg** : T = 1,1×10²¹ K ; P ≈ 5,7×10³⁰ W ; durée de vie **5,9×10⁻¹³ s** ; il libère 1,0×10¹⁹ J (≈ 2,4 Gt de TNT).
- Un trou noir de **10¹² kg** : k_BT = 10,6 MeV (γ, e±, ν — pas des rayons X) ; 356 MW en photons (corps noir), 578 MW (Page),
  **7,8 GW toutes espèces** ; durée de vie 1,1×10¹¹ ans.
- 300–500 MW absorbés à 1 m → flux 2,4–4,0×10⁷ W/m², température d'équilibre radiatif 4 500–5 100 K (revendiqué : 38–49 °C).

## Divergences mathématiques rencontrées

- dM/dt → −∞ quand M → 0 : singularité en temps fini, M ∝ (τ − t)^{1/3}. L'intégration naïve en variable M **échoue**
  si l'on vise la masse de Planck (`ValueError` de la recherche d'événement, consigné dans le JSON). Remède : variable
  régularisée x = M³ (dx/dt = −3αf, borné), validée contre la quadrature.
- T et P divergent en M → 0 : le calcul n'a de sens que pour M ≫ M_Planck.

## Limites et degré de confiance

- Formules T, r_s, P (corps noir) : **élevé**. Coefficients de Page : **élevé**. f(M) (seuils effectifs des quarks,
  extension W/Z/H) : **moyen** (±10 % sur les durées de vie, sans effet sur les ordres de grandeur).
- Aucune prise en compte de l'accrétion, de la rotation, de la charge, ni d'une éventuelle physique au-delà du modèle standard.
- La « durée de mission » et la définition de la « taille d'un électron » sont des hypothèses de lecture [HYP].

## Fichiers

- `s01_hawking.py` — script (≈ 3 s). Exécution : `.venv/bin/python 05_simulations/S01_hawking/s01_hawking.py`
- `figures/S01_fig1_temperature_rayon.png`, `S01_fig2_puissance.png`, `S01_fig3_evaporation.png`,
  `S01_fig4_carte_contraintes.png`, `S01_fig5_plan_distance_masse.png`
- `resultats/S01_resultats.json`, `resultats/S01_table_M.csv`

## Références (vérifiées via Crossref sauf mention)

- D. N. Page, Phys. Rev. D 13, 198 (1976). — J. H. MacGibbon, Phys. Rev. D 44, 376 (1991).
- J. H. MacGibbon, B. J. Carr, D. N. Page, Phys. Rev. D 78, 064043 (2008).
- B. J. Carr, K. Kohri, Y. Sendouda, J. Yokoyama, Phys. Rev. D 81, 104019 (2010).
- S. W. Hawking, Commun. Math. Phys. 43, 199 (1975) (non vérifiée en ligne).

Les valeurs numériques de f(M) et des coefficients de Page sont citées de mémoire à partir de ces articles (non relues
dans le texte) ; elles sont recoupées entre elles par les tests ci-dessus.

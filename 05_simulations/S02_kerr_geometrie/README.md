# S02 — Géométrie de Kerr et de Kerr-Newman

> **Simulation illustrative — ce n'est pas une preuve expérimentale.** On trace les propriétés de solutions
> exactes connues des équations d'Einstein. Rien ne montre qu'un dispositif puisse les « reproduire
> localement », ni que la région r < 0 existe physiquement (elle est située derrière un horizon de Cauchy
> réputé instable).

## Objet

Horizons, ergosphère, vitesse angulaire d'entraînement ω(r, θ), basculement des cônes de lumière, région où
g_φφ < 0 (courbes de genre temps fermées, CTC — y compris r < 0) ; cartes 2D, rendu 3D ; toutes les échelles
en mètres pour M = 10² … 10¹² kg.

## Modèle et équations (Boyer-Lindquist, G = c = 1)

- Δ = r² − 2Mr + a² + Q² ; Σ = r² + a² cos²θ ; a = J/M ; Q en unités géométriques.
- g_tt = −(Δ − a² sin²θ)/Σ ; g_tφ = −a sin²θ (r² + a² − Δ)/Σ ; g_φφ = sin²θ [(r² + a²)² − Δ a² sin²θ]/Σ ;
  g_rr = Σ/Δ ; g_θθ = Σ.
- Horizons : r± = M ± √(M² − a² − Q²). Ergosurfaces (g_tt = 0) : r_E± = M ± √(M² − Q² − a² cos²θ).
- Entraînement : ω = −g_tφ/g_φφ ; à l'horizon ω = Ω_H = a/(r₊² + a²).
- Cône de lumière azimutal : Ω± = [−g_tφ ± √(Δ) sinθ]/g_φφ.
- Région à CTC : g_φφ < 0. Sur l'équateur : r⁴ + a²r² + 2Ma²r − Q²a² < 0.
- Représentation : coordonnées de Kerr-Schild ρ = √(r² + a²) sinθ, z = r cosθ ; conversion SI par r_g = GM/c².

**Variables** : r ∈ ℝ (r < 0 = extension analytique à travers le disque), θ ∈ [0, π]. **Paramètres** : a/M ∈ {0,5 ; 0,9 ; 0,998},
Kerr-Newman (a, Q) = (0,6 ; 0,6) M. **Conditions aux limites** : espace-temps asymptotiquement plat ; aucune équation
différentielle n'est intégrée ici (géométrie analytique).

## Tests de validation (17/17 passés)

- Limites : Schwarzschild (r₊ = 2M), Reissner-Nordström extrémal, Kerr extrémal ; ergosurface équatoriale = 2M, polaire = r₊.
- Identité g_tφ² − g_tt g_φφ = Δ sin²θ sur 2 000 points aléatoires (résidu 9×10⁻¹³).
- Rigidité de l'horizon : ω(r₊, θ) = Ω_H pour tout θ (10⁻¹⁶) ; limite de Lense-Thirring ω → 2J/r³ à r = 1000 M.
- Bord de la région CTC pour a = M : r = −M exactement.
- **Calcul formel exact (sympy, rationnels)** : R_μν ≡ 0 pour Kerr (a = 3/5) ; G_μν ≡ 8πT_μν(EM) et R ≡ 0 pour
  Kerr-Newman (a = 3/5, Q = 1/2) avec le potentiel A = −(Qr/Σ)(dt − a sin²θ dφ). (≈ 1 min 45 s : c'est l'essentiel du temps de calcul.)

## Résultats

| Cas | r₊/M | r₋/M | Ω_H [c/M] | région CTC équatoriale |
|---|---|---|---|---|
| Kerr a = 0,5 | 1,866 | 0,134 | 0,134 | −0,689 M < r < 0 |
| Kerr a = 0,9 | 1,436 | 0,564 | 0,313 | −0,948 M < r < 0 |
| Kerr a = 0,998 | 1,063 | 0,937 | 0,469 | −0,999 M < r < 0 |
| Kerr-Newman a = Q = 0,6 | 1,529 | 0,471 | 0,222 | −0,832 M < r < +0,165 M |

- Dans Kerr, la région g_φφ < 0 est **entièrement en r < 0**, collée à l'anneau, d'étendue ≤ GM/c² ; dans Kerr-Newman elle
  déborde sur r > 0 mais reste **derrière l'horizon interne** (0,165 M < r₋ = 0,471 M).
- « Ajouter de la charge agrandit l'horizon interne » [DOC texte] : qualitativement exact (r₋ croît avec Q).
- **Échelles en mètres** (a = 0,9 M ; tableau complet dans `resultats/S02_echelles_metres.csv`) :

| M [kg] | r_g = GM/c² [m] | r₊ [m] | étendue CTC [m] | Ω_H [rad/s] | J_max [kg m²/s] | Q_max [C] |
|---|---|---|---|---|---|---|
| 113 (demi-unité) | 8,4×10⁻²⁶ | 1,2×10⁻²⁵ | 8,0×10⁻²⁶ | 1,1×10³³ | 2,9×10⁻¹⁵ | 9,8×10⁻⁹ |
| 10⁶ | 7,4×10⁻²² | 1,1×10⁻²¹ | 7,0×10⁻²² | 1,3×10²⁹ | 2,2×10⁻⁷ | 8,6×10⁻⁵ |
| 10⁹ | 7,4×10⁻¹⁹ | 1,1×10⁻¹⁸ | 7,0×10⁻¹⁹ | 1,3×10²⁶ | 0,22 | 0,086 |
| 10¹² | 7,4×10⁻¹⁶ | 1,1×10⁻¹⁵ | 7,0×10⁻¹⁶ | 1,3×10²³ | 2,2×10⁵ | 86 |
| 1,35×10²⁷ (0,71 M_Jupiter) | 1 | 1,44 | 0,95 | 9,4×10⁷ | 4,0×10³⁵ | 1,2×10¹⁷ |

- Toute la structure de Kerr (horizons, ergosphère, anneau, région CTC) d'un trou noir de 10¹² kg tient dans **~10⁻¹⁵ m**
  (taille d'un proton) ; pour 113 kg, dans 10⁻²⁵ m. Une région à CTC d'un mètre exigerait ~10²⁷ kg.
  « Le véhicule passe à travers l'anneau » est donc incompatible, de 15 ordres de grandeur au moins, avec les masses envisagées.

## Divergences mathématiques rencontrées

- Δ = 0 (horizons) : g_rr → ∞, singularité de **coordonnées** (les cartes masquent l'intérieur ; S03 utilise des variables régulières).
- Σ = 0 (r = 0, θ = π/2) : singularité de **courbure** annulaire ; g_φφ → ±∞ de part et d'autre.
- a² + Q² > M² : plus d'horizon (singularité nue) — cas non tracé.
- Avertissements numériques de division par zéro neutralisés volontairement (`np.seterr`) : ils correspondent aux points ci-dessus.

## Limites et degré de confiance

- Géométrie et échelles : **élevé** (solutions exactes vérifiées formellement).
- Pertinence physique de r < r₋ et de r < 0 : **faible** (instabilité de l'horizon de Cauchy, trou noir « éternel » idéalisé).
- Un objet de 10¹² kg à l'échelle du femtomètre relève en réalité de la physique quantique : la description classique est indicative.

## Fichiers

- `s02_kerr_geometrie.py` (≈ 1 min 50 s). Exécution : `.venv/bin/python 05_simulations/S02_kerr_geometrie/s02_kerr_geometrie.py`
- `figures/S02_fig1_cartes_meridiennes.png`, `S02_fig2_region_ctc.png`, `S02_fig3_cones_entrainement.png`,
  `S02_fig4_rendu_3d.png`, `S02_fig5_echelles.png`
- `resultats/S02_resultats.json`, `resultats/S02_echelles_metres.csv`

## Références (vérifiées via Crossref)

- B. Carter, Phys. Rev. 174, 1559 (1968). — J. M. Bardeen, W. H. Press, S. A. Teukolsky, Astrophys. J. 178, 347 (1972).

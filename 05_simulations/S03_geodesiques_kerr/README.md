# S03 — Géodésiques dans l'espace-temps de Kerr

> **Simulation illustrative — ce n'est pas une preuve expérimentale.** On intègre des géodésiques d'un trou
> noir de Kerr éternel, maximalement étendu. Le « passage par l'anneau » vers r < 0 se situe derrière
> l'horizon de Cauchy, réputé instable ; rien n'indique qu'il soit réalisable, ni qu'il mène à une « autre
> ligne d'univers » au sens du corpus.

## Objet

Trajectoires équatoriales et quasi polaires, traversée des horizons, passage près de / à travers l'anneau
dans l'extension r < 0, comparaison temps propre / temps coordonnée. Unités : G = c = 1, M = 1
(1 GM/c³ = 2,48×10⁻²⁴ s pour 10¹² kg).

## Modèles et équations

**Intégrateur A — second ordre, Boyer-Lindquist** : d/dτ(g_νβ u^β) = ½ ∂_ν g_αβ u^α u^β, état (x^μ, u^μ) à 8 composantes ;
la métrique et ses dérivées sont générées par calcul formel (sympy → numpy). E, L_z, la norme et la constante de Carter
**ne sont pas imposées** : leur conservation est un test.

**Intégrateur B — temps de Mino λ (dτ = Σ dλ)** : r″ = ½ dR/dr, θ″ = ½ dΘ/dθ, avec
R(r) = [(r² + a²)E − aL]² − Δ[μ²r² + (L − aE)² + Q] et Θ(θ) = Q − cos²θ [a²(μ² − E²) + L²/sin²θ].
Ces équations sont **régulières à travers les horizons et le disque r = 0**. Angle et temps « entrants » de Kerr-Schild :
dφ̃ = dφ + (a/Δ)dr, dt̃ = dt + (2Mr/Δ)dr, calculés avec W = (P + r′)/Δ = [μ²r² + (L − aE)² + Q]/(P − r′) (forme régulière en Δ = 0).

- **Constantes du mouvement** : E, L_z, μ² = 1, constante de Carter Q.
- **Conditions initiales** : (r₀, θ₀) et 4-vitesse déduite de (E, L_z, Q) ; signes de u^r, u^θ choisis.
- **Conditions d'arrêt** (intégrateur B) : fuite vers r = −25 M ; Σ < 10⁻⁵ (anneau) ; retour vers r₋ en mouvement sortant.
- Schéma : DOP853, tolérances 10⁻¹¹ à 10⁻¹².

## Tests de validation (41/41 passés)

- Conservation sur 1 500 à 2 500 GM/c³ : |ΔE/E| ≤ 6×10⁻¹², |ΔL_z/L_z| ≤ 2×10⁻¹⁰, |g(u,u) + 1| ≤ 10⁻¹¹, |ΔQ/Q| ≤ 7×10⁻¹¹.
- Schwarzschild : avance du périastre (p = 50 M, e = 0,3) = 0,414946 rad/orbite, identique à la quadrature exacte (écart 3×10⁻¹²)
  et à 10 % de 6πM/p (terme du second ordre attendu).
- Orbite circulaire r = 8 M (a = 0,9) : r constant à 10⁻¹² ; dφ/dt = 1/(r^{3/2} + a) à 10⁻¹⁴.
- ISCO : r = 6 M (a = 0), 2,3209 M (a = 0,9) ; R = R′ = R″ = 0.
- Chute radiale de Schwarzschild 10 M → 3 M : τ = (2/3)(r₀^{3/2} − r₁^{3/2})/√(2M) à 10⁻¹³.
- Précession nodale de Lense-Thirring (r = 500 M, i ≈ 61°) : 9,97×10⁻⁴ rad/orbite contre 4πa(M/r)^{3/2} = 1,012×10⁻³ (1,5 %).
- Intégrateur B : invariants r′² − R = 0 et θ′² − Θ = 0 à 10⁻¹⁰ ; rayon de rebond et temps propre sur l'axe ↔ formules/quadrature (10⁻⁸).
- **Recoupement des deux intégrateurs** sur la même géodésique : τ et θ en r = 2,2 M identiques à 10⁻⁹.

## Résultats (a = 0,9 M)

| Géodésique | Issue | Temps propre |
|---|---|---|
| Équatoriale, E = 1, L_z = 0,5 M (Q = 0) | traverse r₊ (τ = 14,21) et r₋ (14,81), **atteint la singularité annulaire** | 14,94 GM/c³ (3,7×10⁻²³ s pour 10¹² kg) |
| Axe, E = 1,2 | traverse le disque, **rebondit à r = −0,186 M** (gravité répulsive côté r < 0), repart vers r₋ | 12,5 |
| Axe, E = 1,6 | traverse le disque et s'échappe vers r → −∞ (autre région asymptotique) | 7,04 jusqu'au disque |
| « Vorticale », E = 1,6, L_z = 0,05 M, Q < 0 | spirale autour de l'axe, traverse le disque à ρ ≈ 0,25 M < a, s'échappe vers r → −∞ | idem |

- **Seuil de traversée sur l'axe** : E² > 1 + M/a, soit E > 1,453 (il faut arriver avec une énergie cinétique à l'infini ≥ 45 % de l'énergie de masse).
- Seules les géodésiques à constante de Carter Q < 0 (qui ne coupent jamais l'équateur) passent par le disque ; les
  équatoriales finissent sur la singularité.
- **Temps propre et temps coordonnée** : t (Boyer-Lindquist) diverge à l'horizon, t̃ (Kerr-Schild) et τ restent finis :
  c'est une divergence de coordonnées, non un déplacement temporel.
- **Dilatation maximale sur orbite circulaire stable** : dt/dτ = 1,41 (a = 0), 2,70 (a = 0,9), 10,8 (a = 0,998), toujours vers le
  **futur**. Pour dt/dτ = 87 660 (« 10 ans/heure ») : observateur statique à 1,3×10⁻¹⁰ r_s de l'horizon, soit 1,9×10⁻²⁵ m pour
  10¹² kg, avec une accélération propre de 2,7×10³⁶ m/s² ; ou ISCO d'un trou noir tel que 1 − a/M ~ 10⁻¹⁴ (ordre de grandeur,
  limite de la double précision).

## Divergences mathématiques rencontrées

- **Δ = 0** : les équations en coordonnées BL divergent (u^t, u^φ → ∞) ; remède : temps de Mino + coordonnées entrantes.
- **θ = 0 avec L_z = 0** (orbite exactement polaire) : termes 0·∞ dans l'équation du second ordre → `NaN`. Un premier test de
  Lense-Thirring sur orbite polaire a ainsi échoué ; il a été remplacé par une orbite inclinée de 61° (le taux de précession
  nodale au premier ordre ne dépend pas de l'inclinaison).
- **Σ → 0** : singularité de courbure ; l'intégration s'arrête à Σ = 10⁻⁵.
- Mouvement **sortant** à travers r₋ : les coordonnées entrantes y sont singulières (on sortirait par une autre branche de
  l'horizon, vers un autre feuillet de l'extension maximale) ; l'intégration s'arrête à r₋ − 10⁻³.

## Limites et degré de confiance

- Calcul des géodésiques : **élevé** (deux intégrateurs indépendants, intégrales premières).
- Réalité physique de l'intérieur r < r₋ : **faible**. Particules d'épreuve : pas de rétroaction, pas de marées sur un corps étendu
  (pour 10¹² kg l'anneau mesure ~10⁻¹⁵ m : aucun objet macroscopique ne « passe » par lui).

## Fichiers

- `s03_geodesiques_kerr.py` (≈ 4 s). Exécution : `.venv/bin/python 05_simulations/S03_geodesiques_kerr/s03_geodesiques_kerr.py`
- `figures/S03_fig1_orbites_equatoriales.png`, `S03_fig2_orbite_polaire.png`, `S03_fig3_passage_anneau.png`,
  `S03_fig4_temps_propre_coordonnee.png`
- `resultats/S03_resultats.json`

## Références (vérifiées via Crossref)

- B. Carter, Phys. Rev. 174, 1559 (1968). — J. M. Bardeen, W. H. Press, S. A. Teukolsky, Astrophys. J. 178, 347 (1972).

# S07 — Besoins en énergie négative : Morris-Thorne, Alcubierre, Casimir

> **Simulation illustrative — ce n'est pas une preuve expérimentale.** On calcule le tenseur énergie-impulsion
> qu'*exigeraient* ces géométries si on les posait a priori. Aucune source connue ne fournit une telle matière.
> Ni un trou de ver ni une bulle de distorsion ne sont, seuls, des machines à voyager dans le passé, et le
> corpus « Titor » ne les invoque pas : ce module sert de point de comparaison.

## Objet

Trou de ver traversable de Morris-Thorne à gorge de 1 m ; bulle d'Alcubierre de 3 m de rayon ; comparaison à la
densité d'énergie Casimir réalisable ; lois d'échelle.

## Modèles et équations

- **Morris-Thorne** : ds² = −e^{2Φ}c²dt² + dr²/(1 − b/r) + r²dΩ². ρc² = K b′/r² ; τ = K[b/r³ − 2(1 − b/r)Φ′/r] ;
  p = (r/2)[(ρc² − τ)Φ′ − τ′] − τ ; K = c⁴/(8πG) = 4,82×10⁴² N. Évasement à la gorge : τ₀ > ρ₀c² (matière « exotique »).
  Modèles : Ellis (Φ = 0, b = b₀²/r) ; b = b₀ ; « absurdement bénin » b = b₀[1 − (r − b₀)/a₀]² sur b₀ ≤ r ≤ b₀ + a₀.
  Masse exotique (un côté, volume coordonnée) : ∫ρ dV = −b₀c²/(2G).
- **Alcubierre** : ds² = −c²dt² + (dx − v f(r_s)dt)² + dy² + dz², f = [tanh σ(r_s + R) − tanh σ(r_s − R)]/(2 tanh σR).
  Densité eulérienne ρ_E = −(c²v²/32πG)(ρ_c²/r_s²) f′² ≤ 0 ; E = −(c²v²/12G)∫r²f′²dr ≈ −(c²v²/36G) R²σ (paroi mince) ;
  profil linéaire d'épaisseur Δ : E = −(c²v²/12G)(R²/Δ + Δ/12) (Pfenning & Ford 1997).
- **Casimir** (plaques idéales, T = 0) : u = −π²ħc/(720 d⁴), P = 3u.

**Paramètres** : b₀ = 1 m ; R = 3 m, σ = 8 m⁻¹ (paroi ≈ 0,25 m), v = c ; cavités Casimir de 100 nm (réalisable) et 10 nm [HYP],
remplissage 50 % [HYP]. **Conditions aux limites** : espace plat à l'infini (b → 0, f → 0), gorge en r = b₀.

## Tests de validation (12/12 passés ; 1 repère non vérifié consigné hors décompte)

- **Calcul formel** : pour Morris-Thorne (Ellis et bénin), G^t_t = −8πρ, G^r_r = −8πτ, G^θ_θ = G^φ_φ = 8πp ; pour Alcubierre,
  G^{tt} ≡ −¼[(∂_yF)² + (∂_zF)²] quel que soit le décalage F(t, x, y, z) : la densité est partout ≤ 0.
- Masse exotique : intégrale numérique ↔ −b₀c²/(2G), y compris pour le modèle bénin (indépendante de a₀).
- Tension à la gorge pour b₀ = 10 m : 4,8×10⁴⁰ Pa (Morris & Thorne citent ~5×10⁴¹ dyn/cm²).
- Alcubierre : intégrale radiale ↔ intégration 2D cylindrique indépendante (10⁻¹³) ↔ limite de paroi mince (0,06 %) ;
  profil linéaire ↔ formule de Pfenning & Ford (10⁻¹⁶).
- Casimir : pression à 1 µm = −1,30 mPa ; u = P/3.
- **Hors décompte — repère non vérifié (correction n° 41 de la Red Team)** : pour R = 100 m et une paroi de 100 longueurs de Planck,
  notre formule donne −6,9×10⁶² kg ; la valeur de comparaison, −6,2×10⁶² kg, est **citée de mémoire** et ne figure pas dans le résumé
  en ligne de Pfenning & Ford (arXiv gr-qc/9702026, seul texte consulté). Historique : testé d'abord à 5 % (échec), puis ramené à
  ±0,3 décade — où il ne pouvait plus échouer. Il est retiré du décompte de validation tant que l'article n'a pas été relu. La formule
  elle-même reste vérifiée exactement (test du profil linéaire par morceaux).

## Résultats

| Géométrie | Grandeur | Valeur |
|---|---|---|
| Morris-Thorne, b₀ = 1 m | tension à la gorge | 4,8×10⁴² Pa |
| | densité à la gorge (Ellis) | −4,8×10⁴² J/m³ (−5,4×10²⁵ kg/m³) |
| | masse exotique | **−6,7×10²⁶ kg** (−0,35 masse de Jupiter ; −6,1×10⁴³ J) |
| Alcubierre, R = 3 m, paroi 0,25 m, v = c | énergie | **−2,4×10⁴⁴ J** (−2,7×10²⁷ kg, −1,4 masse de Jupiter) |
| | densité minimale | −1,9×10⁴³ J/m³ |
| | idem, paroi de 100 L_Planck (inégalités quantiques ; épaisseur d'après le résumé de Pfenning & Ford, énergie d'après notre formule) | −6×10⁵⁹ kg (Univers observable : ~10⁵³ kg) |
| Casimir, d = 100 nm | densité | −4,3 J/m³ |
| | énergie négative par m³ d'empilement | −2,2 J, contre +1,2×10²⁰ J d'énergie de masse des plaques |

- **Écart requis / disponible : ~10⁴³** (Morris-Thorne : 6,7×10⁴² ; Alcubierre : 9,9×10⁴¹), à taille égale.
- Pour atteindre la densité de gorge avec l'effet Casimir, il faudrait des plaques séparées de 3×10⁻¹⁸ m
  (1/270 du rayon du proton) — où la notion de plaque conductrice n'a plus de sens.
- **Lois d'échelle** : masse exotique ∝ b₀ ; tension et densité ∝ b₀⁻² ; séparation Casimir équivalente ∝ b₀^{1/2} ;
  énergie d'Alcubierre ∝ v²R²/Δ ; densité Casimir ∝ d⁻⁴.
- Nuance [VÉR] : Visser, Kar & Dadhich (2003) montrent que la *quantité intégrée* de matière exotique peut en principe être rendue
  arbitrairement petite par des géométries très particulières ; la violation locale à la gorge reste obligatoire. Le modèle
  b = b₀ a d'ailleurs une densité nulle partout et reste exotique par sa tension.

## Divergences mathématiques rencontrées

- g_rr = 1/(1 − b/r) diverge à la gorge (singularité de coordonnées ; on travaille avec ρ, τ, p qui y sont finis).
- Densité d'Alcubierre : facteur ρ_c²/r_s² indéterminé en r_s = 0 (traité : f′(0) = 0) ; f′ → fonction delta quand σ → ∞ : E ∝ σ diverge
  pour une paroi infiniment mince.
- Casimir : u ∝ d⁻⁴ diverge quand d → 0 — divergence de l'idéalisation (conducteur parfait), non de la physique.

## Limites et degré de confiance

- Calculs classiques (relativité générale) : **élevé**. Chiffre « 100 L_Planck » pour la paroi : ordre de grandeur (**moyen**).
- Comparaison à Casimir : **moyen** (remplissage et séparations [HYP]) ; la conclusion (≥ 40 ordres de grandeur) est robuste.
- Aucune dynamique : on ne dit rien de la stabilité, de la formation, ni de la possibilité d'en faire une machine temporelle.

## Fichiers

- `s07_energie_negative.py` (≈ 4 s). Exécution : `.venv/bin/python 05_simulations/S07_energie_negative/s07_energie_negative.py`
- `figures/S07_fig1_morris_thorne.png`, `S07_fig2_alcubierre.png`, `S07_fig3_comparaison_casimir.png`
- `resultats/S07_resultats.json`

## Références (vérifiées via Crossref sauf mention)

- M. S. Morris, K. S. Thorne, Am. J. Phys. 56, 395 (1988). — M. Alcubierre, Class. Quantum Grav. 11, L73 (1994).
- M. J. Pfenning, L. H. Ford, Class. Quantum Grav. 14, 1743 (1997). — M. Visser, S. Kar, N. Dadhich, Phys. Rev. Lett. 90, 201102 (2003).
- A. E. Everett, Phys. Rev. D 53, 7365 (1996) (bulles superluminiques et causalité).
- Mesures de l'effet Casimir : S. K. Lamoreaux, Phys. Rev. Lett. 78, 5 (1997) ; U. Mohideen, A. Roy, Phys. Rev. Lett. 81, 4549 (1998) (non vérifiées en ligne).

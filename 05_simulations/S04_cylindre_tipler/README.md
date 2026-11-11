# S04 — Cylindre de van Stockum / Tipler

> **Simulation illustrative — ce n'est pas une preuve expérimentale.** La solution de van Stockum décrit un
> cylindre de poussière **infini** en rotation rigide ; elle n'est pas asymptotiquement plate. Rien ne montre
> qu'un cylindre fini produise des courbes de genre temps fermées (CTC). L'expression « sinusoïde de Tipler »
> du corpus n'existe pas dans cette littérature.

## Objet

Fonctions métriques intérieures et extérieures, rayon d'apparition des CTC, basculement des cônes de lumière,
ordres de grandeur d'un cylindre « réel ».

## Modèle et équations (G = c = 1)

ds² = H (dr² + dz²) + L dφ² + 2 M dφ dt − F dt², avec M² + F L = r².

- **Intérieur** (r < R) : H = e^{−a²r²}, L = r²(1 − a²r²), M = a r², F = 1 ; poussière de densité 8πρ = 4a² e^{a²r²}, 4-vitesse ∂_t.
- **Extérieur** (r > R), d'après Tipler (1974) :
  - aR < 1/2 : L = R r sinh(3ε + θ)/(2 sinh 2ε cosh ε), M = r sinh(ε + θ)/sinh 2ε, F = r sinh(ε − θ)/(R sinh ε),
    θ = √(1 − 4a²R²) ln(r/R), tanh ε = √(1 − 4a²R²) ;
  - aR = 1/2 : L = (Rr/4)(3 + ln(r/R)), M = (r/2)(1 + ln(r/R)), F = (r/R)(1 − ln(r/R)) ;
  - aR > 1/2 : mêmes expressions avec sin/cos, γ = √(4a²R² − 1) ln(r/R), tan β = √(4a²R² − 1) ;
  - dans tous les cas H = e^{−a²R²}(r/R)^{−2a²R²}.
- **CTC** : g_φφ = L < 0. Rayon d'apparition : aR ≤ 1/2 → aucune ; 1/2 < aR < 1 → r = R exp[(π − 3β)/√(4a²R² − 1)] (extérieur) ;
  aR ≥ 1 → r = 1/a (intérieur).
- Cône de lumière azimutal : Ω± = (−M ± r)/L.
- **SI** : ω = a c ; ρ₀ = ω²/(2πG) ; masse propre par unité de longueur μ = a²R²c²/(2G) (re-dérivée, vérifiée numériquement).

**Paramètres** : aR ∈ {0,3 ; 0,5 ; 0,6 ; 0,8 ; 1,2}. **Conditions aux limites** : régularité sur l'axe ; raccord C¹ en r = R ;
pas de condition à l'infini (la solution n'est pas asymptotiquement plate — c'est une limite physique majeure).

## Tests de validation (25/25 passés)

- **Calcul formel** : intérieur, G_μν ≡ 8πρ u_μ u_ν avec 8πρ = 4a²e^{a²r²} (exact, a = 3/4) ; extérieur, R_μν = 0 pour les trois
  branches (aR = 3/10, 1/2, 4/5), résidu < 10⁻¹⁷⁰ à 40 chiffres. *Les formules, citées de mémoire, sont ainsi confirmées par les
  équations d'Einstein elles-mêmes.*
- Raccord C⁰ (10⁻¹²) et C¹ (10⁻⁶) en r = R pour quatre valeurs de aR ; identité M² + FL = r² (10⁻¹⁴).
- Rayon CTC : formule ↔ premier zéro numérique de L (aR = 0,6 : 8,063 R) ; limites aR = 1 et aR = 2.
- Masse linéique : intégrale numérique ↔ a²R²/2.
- **Test révisé** : continuité des branches en aR → 1/2. La première version (écart absolu < 2×10⁻³ pour δ = 10⁻⁵) échouait
  (5,6×10⁻³) : critère mal posé pour des fonctions valant ~30 ; remplacé par un critère relatif (1,9×10⁻⁵ pour δ = 10⁻⁶) et un
  test de convergence linéaire en δ (rapport 100,0 attendu 100).

## Résultats

| aR | 0,5 | 0,51 | 0,55 | 0,6 | 0,8 | 1 | 1,5 |
|---|---|---|---|---|---|---|---|
| r_CTC / R | ∞ | 3,2×10⁵ | 57 | 8,06 | 1,44 | 1 | 0,667 |

- **Seuil** : aR > 1/2, c'est-à-dire une « vitesse de surface » supérieure à c/2, et une masse linéique
  **μ ≥ c²/(8G) = 1,68×10²⁶ kg/m ≈ 28 masses terrestres par mètre**, *indépendamment du rayon*.
- Exemple de Tipler (R = 10 km, longueur 100 km, aR = 1/2) : 2 386 tours/s ; densité axiale 5,4×10¹⁷ kg/m³ (2,3 fois la densité
  nucléaire) ; masse 1,7×10³¹ kg (8,5 masses solaires).
- À l'échelle d'un coffre (R = 0,1 m, longueur 1 m, aR = 0,6) : ω = 1,8×10⁹ rad/s ; densité 7,7×10²⁷ kg/m³
  (3×10¹⁰ fois la densité nucléaire) ; masse 2,4×10²⁶ kg (41 Terres) ; CTC à partir de 0,81 m.
- Avec 227 kg par mètre : aR = 5,8×10⁻¹³ — il manque un facteur **8,6×10¹¹ sur aR** et **7,4×10²³ sur la masse**.
- Pour aR > 1/2, L et F oscillent en ln r : une infinité de bandes à CTC jusqu'à l'infini — signe du caractère non physique
  (non asymptotiquement plat) de la solution.

## Divergences mathématiques rencontrées

- **aR → 1/2** : formes 0/0 (sinh ε → 0, sin β → 0) ; traitées par bascule sur la branche critique (|aR − 1/2| < 10⁻⁹) et
  contrôlées par le test de convergence ci-dessus.
- **L → 0** : Ω₋ = (−M − r)/L diverge et change de signe : la direction azimutale devient lumière puis temps.
- **r_CTC → ∞** quand aR → 1/2⁺ (essentielle : exp(π/√(4a²R² − 1))).
- H → 0 à l'infini (r^{−2a²R²}) : distances propres radiales et axiales contractées, pas de limite minkowskienne.

## Limites et degré de confiance

- Solution exacte et seuils : **élevé** (vérification formelle). Ordres de grandeur SI : **élevé**.
- Transposition à un objet fini : **faible** — le caractère infini est essentiel ; Hawking (1992) montre que créer des CTC
  dans une région finie exige de violer la condition d'énergie faible. La poussière sans pression n'est pas un matériau réel.

## Fichiers

- `s04_cylindre_tipler.py` (≈ 20 s, dont la vérification formelle). Exécution : `.venv/bin/python 05_simulations/S04_cylindre_tipler/s04_cylindre_tipler.py`
- `figures/S04_fig1_fonctions_metriques.png`, `S04_fig2_domaine_ctc.png`, `S04_fig3_cones_lumiere.png`, `S04_fig4_ordres_de_grandeur.png`
- `resultats/S04_resultats.json`

## Références (vérifiées via Crossref)

- F. J. Tipler, Phys. Rev. D 9, 2203 (1974). — W. J. van Stockum, Proc. R. Soc. Edinburgh 57, 135 (daté 1938 par Crossref, souvent cité 1937).
- S. W. Hawking, Phys. Rev. D 46, 603 (1992).

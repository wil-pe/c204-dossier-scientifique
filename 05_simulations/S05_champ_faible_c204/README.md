# S05 — Configuration « C204 » en champ faible : deux masses ponctuelles en rotation

> **Simulation illustrative — ce n'est pas une preuve expérimentale.** Aucune des masses supposées n'est
> attestée. Le calcul applique la gravitation newtonienne et la relativité générale linéarisée, toutes deux
> éprouvées (GPS, Gravity Probe B, pulsars binaires), à des hypothèses de masse [HYP].

## Objet

Deux masses ponctuelles M séparées de d, en rotation : potentiel, accélération et marées entre 0,1 et 4 m,
champ gravitomagnétique, entraînement des référentiels, facteur de dilatation temporelle, puissance rayonnée
en ondes gravitationnelles et temps de coalescence. Comparaison aux « 1,5–2 g » et aux « 10 ans par heure »
(dt/dτ ≈ 87 660).

## Modèle et équations

- Potentiel Φ = −Σ GM/|r − r_i| ; g = −∇Φ ; tenseur de marée T_ij = Σ GM(3n_in_j − δ_ij)/r³.
- Dilatation (observateur statique, champ faible) : dt/dτ − 1 = −Φ/c².
- Gravito-électromagnétisme linéarisé (convention de Mashhoon) : A = (2G/c) Σ m v/|r − r_i|, B_g = ∇×A ;
  loin des sources B_g = (G/c)[3(J·n)n − J]/r³ ; précession d'un gyroscope Ω_LT = B_g/c, soit 2GJ/(c²r³) sur l'axe.
- Ondes gravitationnelles (quadrupôle, deux masses égales, orbite circulaire) : P = (32/5)(G/c⁵) μ² d⁴ Ω⁶, μ = M/2 ;
  orbite képlérienne Ω² = 2GM/d³ → formule de Peters ; coalescence t_c = (5/256) c⁵ d⁴/(2G³M³).

**Hypothèses de masse par singularité [HYP]** : A = 113 kg (demi-unité) ; B = 10⁹ kg ; C = 1,47×10¹¹ kg (la paire donne 2 g à 1 m) ;
D = 10¹² kg (300–500 MW en photons) ; E = 4,4×10¹² kg (300–500 MW toutes espèces). **Séparation** : deux cas — d = 0,098 m, entraxe des deux logements d'après DOC-007 [DÉD, Équipe A : 98 ± 25 mm], et d = 0,30 m [HYP de l'Équipe D, échelle du coffre ; utilisé pour les cartes].
**Étendue radiale d'un occupant** : 1 m [HYP]. **Domaine** : 0,1 à 4 m ; **conditions aux limites** : Φ → 0 à l'infini.
Validité : r ≫ GM/c² (≤ 10⁻¹⁴ m ici) et v ≪ c (v ≤ 22 m/s).

## Tests de validation (11/11 passés)

- g analytique ↔ −∇Φ numérique (3×10⁻¹⁰) ; trace du tenseur de marée nulle (4×10⁻¹⁶) ; champ lointain = monopôle + quadrupôle (10⁻⁹).
- Puissance OG : formule fermée ↔ moyenne numérique de (d³Q_ij/dt³)² par FFT (10⁻¹³) ↔ Peters (10⁻¹⁶) ; a(t) de Peters ↔ intégration numérique.
- B_g moyen des deux masses en orbite ↔ dipôle de J_orbital à r = 50 d (1,8×10⁻⁴).
- **Repères expérimentaux** : Terre-Soleil 196 W (obtenu 196,3) ; Gravity Probe B ≈ 39 mas/an (obtenu 41,1, valeurs de J et r arrondies) ;
  GPS +38,5 µs/jour (obtenu 38,50).
- Modulation de |g| par la rotation ↔ estimation quadrupolaire 9d²/(8r²).

## Résultats (sur la médiatrice de la paire ; tableau principal pour d = 0,30 m [HYP])

| Hypothèse (par singularité) | g à 1 m | g à 3 m | marée sur 1 m, centre à 1 m | dt/dτ − 1 à 1 m | Ω_LT à 1 m [rad/s] | P_OG [W] | t_coalescence |
|---|---|---|---|---|---|---|---|
| A : 113 kg | 1,5×10⁻⁹ g | 1,7×10⁻¹⁰ g | 4,8×10⁻⁹ g | 1,7×10⁻²⁵ | 5,7×10⁻³⁰ | 8×10⁻⁷⁰ | 1,4×10⁵⁵ ans |
| B : 10⁹ kg | 0,013 g | 0,0015 g | 0,042 g | 1,5×10⁻¹⁸ | 1,5×10⁻¹⁹ | 4×10⁻³⁵ | 2,0×10³⁴ ans |
| C : 1,47×10¹¹ kg | 1,93 g | 0,22 g | **6,2 g** | 2,2×10⁻¹⁶ | 2,7×10⁻¹⁶ | 3×10⁻²⁴ | 6,4×10²⁷ ans |
| D : 10¹² kg | 13,2 g | 1,51 g | 41,9 g | 1,5×10⁻¹⁵ | 4,7×10⁻¹⁵ | 4×10⁻²⁰ | 2,0×10²⁵ ans |
| E : 4,4×10¹² kg | 57,9 g | 6,6 g | 184 g | 6,5×10⁻¹⁵ | 4,3×10⁻¹⁴ | 7×10⁻¹⁷ | 2,4×10²³ ans |

- **« 1,5–2 g »** : il faut ~1,5×10¹¹ kg par singularité pour 2 g à 1 m ; avec 2 × 113 kg on obtient 1,5×10⁻⁹ g
  (**9,1 ordres de grandeur** de moins).
- **« pendant tout le trajet »** : la zone 1,5 g ≤ |g| ≤ 2 g est une coquille d'épaisseur 15,5 % du rayon (15 cm à 1 m). Un champ
  en 1/r² qui vaut 2 g à 1 m varie de 6 g sur un corps d'un mètre : pas de pesanteur uniforme dans un habitacle.
- **« 10 ans par heure »** : dt/dτ − 1 ≈ 1,5×10⁻¹⁵ à 1 m de 2 × 10¹² kg — **19,8 ordres de grandeur** sous 87 660
  (29,7 avec 2 × 113 kg). Décalage cumulé en 6 h : 3×10⁻¹¹ s. Et le signe est celui d'un ralentissement d'horloge
  (avance vers le futur extérieur), jamais d'un retour vers le passé.
- **Entraînement des référentiels** : ≤ 5×10⁻¹⁴ rad/s à 1 m (un tour en ~4 millions d'années), dominé par le moment cinétique
  *orbital* (3×10¹² kg m²/s pour D) et non par le spin maximal de trous noirs de cette masse (2×10⁵ kg m²/s).
- **Ondes gravitationnelles** : ≤ 10⁻¹⁶ W ; coalescence ≥ 10²³ ans. La rotation de la paire module |g| de 10 % à 1 m (2,5 % à 2 m) à la fréquence 2Ω.
- Force mutuelle entre deux masses de 10¹² kg à 0,3 m : 7,4×10¹⁴ N.

**Cas de l'entraxe documentaire, d = 0,098 m** (correction n° 44 de la Red Team) :

| Hypothèse (par singularité) | pulsation orbitale | Ω_LT à 1 m [rad/s] | P_OG [W] | t_coalescence | force mutuelle |
|---|---|---|---|---|---|
| A : 113 kg | 4,0×10⁻³ rad/s | 3,2×10⁻³⁰ | 2×10⁻⁶⁷ | 1,6×10⁵³ ans | 8,9×10⁻⁵ N |
| C : 1,47×10¹¹ kg | 144 rad/s | 1,5×10⁻¹⁶ | 8×10⁻²² | 7,3×10²⁵ ans | 1,5×10¹⁴ N |
| D : 10¹² kg | 377 rad/s (période 17 ms) | 2,7×10⁻¹⁵ | 1,2×10⁻¹⁷ | 2,3×10²³ ans | 7,0×10¹⁵ N |
| E : 4,4×10¹² kg | 790 rad/s | 2,5×10⁻¹⁴ | 1,9×10⁻¹⁴ | 2,7×10²¹ ans | 1,4×10¹⁷ N |

- Passer de 0,30 m à 0,098 m ne change presque rien aux champs entre 1 et 3 m : g augmente de 3,0 % à 1 m (0,3 % à 3 m), la
  dilatation de 1,0 % ; la modulation de |g| par la rotation tombe de 10 % à 1,1 % à 1 m. Les conclusions (« 2 g », « 10 ans par
  heure ») sont inchangées.
- En revanche la rotation est 5,4 fois plus rapide, la puissance en ondes gravitationnelles 270 fois plus grande (elle reste
  ≤ 2×10⁻¹⁴ W), le temps de coalescence 88 fois plus court (≥ 10²¹ ans), et l'entraînement orbital à 1 m 1,7 fois plus faible.

## Divergences mathématiques rencontrées

- Φ, g et les marées divergent sur les masses ponctuelles (r → r_i) : les cartes sont tronquées, le dipôle gravitomagnétique est
  masqué pour r < d ; l'approximation de champ faible cesse d'être valable à quelques GM/c² (10⁻¹⁵ m), très en deçà du domaine tracé.
- t_c ∝ M⁻³ et P ∝ M⁵ : valeurs extrêmes (10⁻⁷⁰ W, 10⁵⁵ ans) sans difficulté numérique en double précision.

## Limites et degré de confiance

- Résultats newtoniens et de champ faible : **élevé** (repères expérimentaux reproduits).
- Les hypothèses de masse et de séparation sont [HYP] ; la conclusion (écarts de 9 à 30 ordres de grandeur) n'en dépend pas.
- Non traités : interaction avec la Terre (le poids de masses de 10¹¹–10¹² kg, voir S06), rayonnement de Hawking (S01).

## Fichiers

- `s05_champ_faible_c204.py` (≈ 3 s). Exécution : `.venv/bin/python 05_simulations/S05_champ_faible_c204/s05_champ_faible_c204.py`
- `figures/S05_fig1_acceleration.png`, `S05_fig2_marees.png`, `S05_fig3_dilatation_entrainement.png`, `S05_fig4_ondes_gravitationnelles.png`
- `resultats/S05_resultats.json`

## Références

- P. C. Peters, Phys. Rev. 136, B1224 (1964) (vérifiée via Crossref).
- B. Mashhoon, « Gravitoelectromagnetism: a brief review », arXiv:gr-qc/0311030 (non vérifiée en ligne).

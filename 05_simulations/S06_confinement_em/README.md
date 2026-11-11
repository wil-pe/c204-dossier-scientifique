# S06 — Confinement électromagnétique d'un objet chargé massif

> **Simulation illustrative — ce n'est pas une preuve expérimentale.** Les pièges de Penning et de Paul sont
> des techniques réelles pour des ions (Q/M ~ 10⁵–10⁸ C/kg). Leur extrapolation à un micro-trou noir chargé
> (Q/M ≤ 8,6×10⁻¹¹ C/kg) est purement formelle. Ne pas confondre champ électromagnétique et champ
> gravitationnel : un piège retient une charge, il n'annule aucun poids.

## Objet

Pièges de Penning et de Paul avec pesanteur, stabilité (équations de Mathieu), champs requis en fonction de Q/M
jusqu'à la charge extrémale, trajectoires illustratives ; charge qu'un micro-trou noir peut porter.

## Modèles et équations

- **Charge extrémale** (Kerr-Newman) : Q/M ≤ √(4πε₀G) = 8,618×10⁻¹¹ C/kg (proton : 9,6×10⁷ C/kg, soit 10¹⁸ fois plus).
- **Lévitation électrostatique** : E = g₀/(Q/M).
- **Penning** : Φ = (V₀/2d₀²)(z² − ρ²/2), B = B ẑ. Unités réduites (temps 1/ω_z, longueur d₀) :
  x″ = x/2 + βy′ + γ_x ; y″ = y/2 − βx′ + γ_y ; z″ = −z + γ_z, avec β = ω_c/ω_z, ω_z² = QV₀/(Md₀²), ω_c = QB/M, γ = a/(ω_z²d₀).
  Stabilité radiale : β² > 2 ; modes ω± = ½(β ± √(β² − 2)) ; équilibre déplacé z = γ_z, x = −2γ_x.
- **Paul** : z″ + (a_z − 2q_z cos 2ξ) z = −γ, ξ = Ωt/2, q_z = 4QV/(Mr₀²Ω²), a_z = −8QU/(Mr₀²Ω²), (a_r, q_r) = −(a_z, q_z)/2.
  Stabilité par analyse de Floquet (trace de la matrice de monodromie, |tr| < 2). Pseudo-potentiel : ω_sec ≈ qΩ/(2√2).
- **Dimensionnement** (affaissement sous la pesanteur ≤ 10 %, d₀ = r₀ = 5 cm) :
  Penning V₀ = g d₀/(0,1·Q/M), B_min = √(2g/(0,1 d₀))/(Q/M) ; Paul (q = 0,4) V = 2g r₀/(0,4·0,1·Q/M).
- **Charge d'un micro-trou noir** (correction n° 43 de la Red Team) : valeur **typique ≈ 6 e** (valeur quadratique moyenne 6,14 e quand
  GMμ/ħc → 0, Page 1977 — résumé vérifié par la Red Team, non relu par nous) ; **borne supérieure d'ordre de grandeur ≈ 137 e** [DÉD] :
  champ de Schwinger E_S = m_e²c³/(eħ) = 1,32×10¹⁸ V/m atteint à la longueur de Compton de l'électron pour Q ≈ e/α. Claquage de l'air
  ~3×10⁶ V/m [VÉR].

**Conditions initiales** des trajectoires : Penning (x, y, z ; v) = (0,15 ; 0 ; 0 ; 0 ; 0,1 ; 0) d₀, β = 3 (stable) ou 1,2 (instable),
γ_z = −0,1 (pesanteur), γ_x = 0,08 (freinage du véhicule) ; Paul z(0) = 0,05 r₀, q = 0,3 (stable) ou 0,95 (instable), γ = 0,004.
**Conditions aux limites** : champs idéaux illimités (pas d'électrodes : l'éjection est signalée quand |z| > r₀).

## Tests de validation (20/20 passés)

- Q/M extrémal (dossier : 8,62×10⁻¹¹) ; charge de Schwinger = 137,04 e ; équilibre de Majumdar-Papapetrou (Coulomb = gravitation à 10⁻¹⁶).
- Penning : énergie conservée (5×10⁻⁹) ; pulsations ω₋, ω_z, ω₊ mesurées par FFT ↔ théorie (2×10⁻⁴) ; théorème d'invariance
  ω₊² + ω₋² + ω_z² = ω_c² ; équilibres déplacés ; taux de croissance de l'instabilité = √(2 − β²)/2 (5×10⁻⁷).
- Mathieu : q_max(a = 0) = 0,908046 (Floquet ↔ zéro de b₁(q) de `scipy.special`, 10⁻¹²) ; frontières a₀(q), b₁(q) à 10⁻¹³.
- Paul : pulsation séculaire ↔ exposant de Floquet (7×10⁻⁴) ↔ approximation de Dehmelt q/√2 (1,9 %) ; affaissement ↔ pseudo-potentiel (4,6 %).
- **Tests révisés** : trois tests Penning avaient d'abord échoué de peu (moyennes prises sur un nombre non entier de périodes :
  biais de 2×10⁻⁴ à 3 %). Corrigé en intégrant sur 64 périodes axiales exactes et en moyennant sur 11 périodes magnétron ;
  tolérance spectrale fixée à 5 % du pas de fréquence.

## Résultats

| Grandeur (charge **extrémale**, toute masse) | Valeur | Repère |
|---|---|---|
| Champ électrique de lévitation | **1,14×10¹¹ V/m** | air : 3×10⁶ ; vide/électrodes : ~10⁹ |
| Penning : tension V₀ | 5,7×10¹⁰ V | — |
| Penning : champ magnétique minimal | **7,3×10¹¹ T** | laboratoire continu : 45 T ; magnétar : ~10¹¹ T |
| Paul : amplitude RF (q = 0,4, Ω = 313 rad/s) | 2,8×10¹¹ V | — |

| Masse | Q extrémale | champ propre à 1 m | rayon où E > claquage de l'air | E de lévitation si Q ≈ 137 e (borne) | E de lévitation si Q ≈ 6 e (typique) |
|---|---|---|---|---|---|
| 113 kg | 9,8×10⁻⁹ C | 88 V/m | 5 mm | 5×10¹⁹ V/m (> Schwinger) | 1,1×10²¹ V/m |
| 10⁹ kg | 0,086 C | 7,8×10⁸ V/m | 16 m | 4×10²⁶ V/m | 1,0×10²⁸ V/m |
| 10¹² kg | 86 C | 7,8×10¹¹ V/m | 508 m | 4×10²⁹ V/m | 1,0×10³¹ V/m |

- Même au maximum théorique de charge, léviter une singularité exige ~10¹¹ V/m et la piéger ~10¹² T. Avec une charge
  réaliste (typiquement ≈ 6 e, au plus ~137 e à cause de la création de paires ; ≤ 3×10⁻⁴ C dans l'air), les champs requis
  dépassent le champ de Schwinger — de 22 fois plus encore avec la charge typique qu'avec la borne.
- **Un champ magnétique statique n'exerce aucune force sur une charge au repos** : des « bobines » ne retiennent pas un objet
  contre la pesanteur. La voie dipolaire (moment magnétique Qa c d'un trou noir de Kerr-Newman) demanderait un gradient de
  5×10¹⁷ T/m pour 10¹² kg.
- **Troisième loi de Newton** : le piège transmet au véhicule tout le poids M g. Pour 10¹² kg : 9,8×10¹² N (10⁹ tonnes-force),
  soit 10⁹ fois la charge utile d'un pick-up, et 10¹⁴ Pa sur 0,1 m².
- Deux singularités extrémales de même signe (« dual-positive » ?) seraient en équilibre mutuel exact (Majumdar-Papapetrou) —
  mais leur champ ioniserait l'air à des centaines de mètres.
- Le confinement électromagnétique n'empêche pas l'évaporation de Hawking : une singularité de 113 kg disparaît en 6×10⁻¹³ s (S01).

## Divergences mathématiques rencontrées

- Penning : β² < 2 → racine imaginaire, croissance exponentielle (taux vérifié) ; l'équilibre radial est un maximum de potentiel
  stabilisé dynamiquement par B.
- Mathieu : hors des zones de stabilité, l'exposant de Floquet devient complexe (|trace| > 2) : éjection exponentielle (figure 3c).
- E_lévitation ∝ 1/(Q/M) diverge quand Q → 0 : un trou noir neutre ne peut pas être retenu électromagnétiquement.

## Limites et degré de confiance

- Dynamique des pièges et stabilité : **élevé**. Champs requis à la charge extrémale : **élevé**.
- Charge : borne supérieure ≈ 137 e, **moyen** (argument d'ordre de grandeur) ; valeur typique ≈ 6 e reprise de Page (1977) sur la foi
  du résumé vérifié par la Red Team (le traitement complet relève de l'émission de Hawking de particules chargées, Gibbons 1975, Page 1977). Limites de claquage : ordres de grandeur.
- Charge ponctuelle classique, pas de rayonnement, pas d'effets relativistes ni quantiques dans les trajectoires.

## Fichiers

- `s06_confinement_em.py` (≈ 5 s). Exécution : `.venv/bin/python 05_simulations/S06_confinement_em/s06_confinement_em.py`
- `figures/S06_fig1_champs_requis.png`, `S06_fig2_penning.png`, `S06_fig3_paul_mathieu.png`, `S06_fig4_limites_de_charge.png`
- `resultats/S06_resultats.json`

## Références (vérifiées via Crossref)

- L. S. Brown, G. Gabrielse, Rev. Mod. Phys. 58, 233 (1986). — G. W. Gibbons, Commun. Math. Phys. 44, 245 (1975).
- D. N. Page, Phys. Rev. D 16, 2402 (1977). — S. D. Majumdar, Phys. Rev. 72, 390 (1947).
- J. B. Hartle, S. W. Hawking, Commun. Math. Phys. 26, 87 (1972).

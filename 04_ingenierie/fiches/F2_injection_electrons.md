# Fiche F2 — Injection d'électrons

Repères : DOC-008 r.4 (« electron mass injector manifold »), r.5 (régulateur), r.6 (générateur).
Calculs : `calculs/c03_injection_rotation.py` → `resultats/c03_injection_rotation.json`, `c03_injection_par_masse.csv`.

## 1. Ce que dit la source

**[DOC texte]** « Electron injection manifold to alter mass and gravity of microsingularities » ; « adding
electric charge … increases the diameter of the inner event horizons ; adding mass … increases the area of
gravitational influence » ; les électrons sont injectés « onto the surface of their respective ergospheres » ;
« the electricity comes from batteries ».

## 2. Ce que l'ajout d'électrons changerait réellement

Un électron apporte une masse m_e = 9,11×10⁻³¹ kg et une charge −e. Le rapport charge/masse de l'électron
(1,76×10¹¹ C/kg) est 2×10²¹ fois supérieur au rapport maximal admissible pour un trou noir (8,62×10⁻¹¹ C/kg).
Donc :

| Grandeur | Équation | Valeur | Étiq. | Confiance |
|---|---|---|---|---|
| Variation de masse quand la charge maximale est atteinte | ΔM/M = √(4πε₀G)·m_e/e | **4,9×10⁻²²**, quel que soit M | [DÉD] | élevée |
| Électrons pour atteindre la charge extrémale de 10¹² kg | N = Q_max/e | 5,4×10²⁰ électrons (86 C), soit 4,9×10⁻¹⁰ kg | [DÉD] | élevée |
| Électrons pour +1 % de masse (4,4×10¹² kg) | N = 0,01 M/m_e | 4,8×10⁴⁰ électrons = 7,7×10²¹ C | [DÉD] | élevée |
| Durée à 1 A / à 1 MA | t = Q/I | 2,5×10¹⁴ ans / 2,5×10⁸ ans | [DÉD] | élevée |
| Énergie de masse correspondante | 0,01 M c² | 3,9×10²⁷ J (≈ 6 millions d'années d'énergie primaire mondiale) | [DÉD] | élevée |
| Apport de masse pour seulement compenser l'évaporation | Ṁ = P/c² | 4,5×10⁻⁹ kg/s pour 400 MW, soit un faisceau **absorbé** de 400 MW | [DÉD] | élevée |

« Injecter des électrons pour modifier la masse » est donc quantitativement vide : la charge sature 22 ordres de
grandeur avant que la masse ne bouge de 1 %. Seul un apport **neutre** (matière ou rayonnement) change la masse,
et il faut alors fournir l'énergie de masse elle-même.

Sur l'« horizon interne » : un trou noir chargé a bien deux horizons, r± = GM/c² ± √((GM/c²)² − r_Q²) **[VÉR]** ;
ajouter de la charge agrandit r₋ et rétrécit r₊. L'énoncé qualitatif de la source est donc correct en
relativité générale classique, mais inopérant : la charge nécessaire (une fraction notable de Q_max) ne peut
ni être apportée ni être conservée.

## 3. Barrière coulombienne

| Grandeur | Équation | Valeur | Étiq. | Confiance |
|---|---|---|---|---|
| Potentiel d'horizon d'un trou extrémal | Φ_H = c²/√(4πε₀G) | 1,04×10²⁷ V, indépendant de M | [DÉD] | élevée |
| Énergie du dernier électron à injecter | e Φ_H | **1,04×10²⁷ eV** (LHC : 6,8×10¹² eV par proton, soit 14 décades de moins) | [DÉD] | élevée |
| Barrière par charge élémentaire déjà portée | e²/(4πε₀ r_s) | 0,97 MeV (10¹² kg) ; 0,22 MeV (4,4×10¹² kg) ; 9,7×10⁹ MeV (100 kg) | [DÉD] | élevée |
| Charge à partir de laquelle Coulomb l'emporte sur la gravité pour un électron lent | Z_c = 4πε₀ G M m_e/e² | 0,26 (10¹² kg) ; 1,2 (4,4×10¹² kg) | [DÉD] | élevée |
| Énergie d'un trou chargé à l'extrémal | M_irr = M/2 | la moitié de M c² est électromagnétique : 2×10²⁹ J pour 4,4×10¹² kg | [VÉR] | élevée |

Lecture : **dès le premier électron en excès**, le trou noir repousse le suivant plus fort que sa gravité ne
l'attire. Pour continuer à charger il faut des électrons de plus en plus énergétiques, jusqu'à 10²⁷ eV.
En parallèle le trou se décharge spontanément : il émet de l'ordre de 10²⁰ e± par seconde (9×10¹⁹ pour 4,4×10¹² kg, 4×10²⁰ pour 10¹² kg) et favorise le signe de sa
propre charge ; temps de retour ≈ 10⁻¹⁹ à 10⁻²⁰ s (ordre de grandeur, `c03`). Charge d'équilibre : quelques e
(6,14 e rms, Page 1977).

## 4. Section efficace de capture

| Grandeur | Équation | 10¹² kg | 4,4×10¹² kg | 100 kg |
|---|---|---|---|---|
| Rayon de Schwarzschild | r_s = 2GM/c² | 1,49 fm | 6,5 fm | 1,5×10⁻²⁵ m |
| Capture géométrique (ultra-relativiste) | σ = 27πG²M²/c⁴ | 0,47 barn | 9,1 barn | 4,7×10⁻²¹ barn |
| Énergie au-dessous de laquelle l'électron « déborde » le trou (ƛ > r_s) | E = ħc/r_s | 133 MeV | 30 MeV | 1,3×10¹² MeV |
| Fraction capturée, tache de 1 µm² | σ/A | 4,7×10⁻¹⁷ | 9,1×10⁻¹⁶ | 4,7×10⁻³⁷ |

À basse énergie la section efficace d'un fermion sans masse tombe à 2πG²M²/c⁴, soit 1/8 de celle d'un scalaire
(Unruh 1976) **[VÉR]**. Exemple (`c03`) : le courant moyen record d'un photo-injecteur (65 mA, Dunham et al. 2013),
supposé focalisé sur 1 µm² — combinaison irréaliste —, donnerait 19 captures par seconde sur un trou de 10¹² kg,
soit 1,7×10⁻²⁹ kg/s, contre une perte par évaporation de 8,5×10⁻⁸ kg/s : rapport 5×10²¹.

## 5. Technologie réelle la plus proche

- Canon à électrons thermo-ionique (tube cathodique, microscope, soudage par faisceau) : 10–150 kV, µA à
  centaines de mA. **Démontré, constructible** ; 100 kV × 1 mA = 100 W, compatible avec une batterie.
- Photo-injecteurs : 65 mA moyens à 4–5 MeV (Dunham et al. 2013).
- Focalisation : 41 nm vertical à ATF2 (Okugi 2016, exposé de conférence) ; sonde < 50 pm en STEM corrigé
  (Erni et al. 2009), mais à 300 keV, où ƛ ≫ r_s.
- Accélérateurs compacts : 8 GeV sur 20 cm par sillage laser-plasma (Gonsalves et al. 2019), au prix d'un laser
  pétawatt qui n'est pas embarquable.

## 6. Classement

| Élément | Statut | Constructible aujourd'hui ? |
|---|---|---|
| Générateur d'électrons (r.6), régulateur (r.5) | Démontré | **Oui** — cathode LaB₆ ou tungstène, HT 100 kV, asservissement du courant d'émission |
| Collecteur/ligne de faisceau sous vide (r.4) | Démontré | **Oui** — tube, lentilles électrostatiques, déflecteurs |
| Fonction « modifier la masse » | **Contredit** (ΔM/M ≤ 4,9×10⁻²²) | Impossible par principe |
| Fonction « charger la singularité » | **Contredit** (décharge en ~10⁻¹⁹ s ; barrière jusqu'à 10²⁷ eV) | Impossible par principe |
| Viser un objet de 10⁻¹⁵ m | Théoriquement possible, 15 à 17 décades de pertes | Non |

## 7. Limites

Les temps de décharge sont des ordres de grandeur (biais linéarisé). La capture d'électrons lents par un trou
noir chargé positivement est augmentée par la focalisation coulombienne ; cela ne change ni la saturation de la
charge ni l'inefficacité massique. Confiance globale : **élevée**.

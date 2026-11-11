# Fiche F1 — Les deux « singularités » et leur logement magnétique

Repères : DOC-008 r.1 (carter), r.2 (bobines), r.3 (générateur/régulateur de champ) ; DOC-007 r.1-2.
Calculs : `calculs/c01_hawking.py`, `calculs/c02_confinement.py` → `calculs/resultats/c01_*.{json,csv}`, `c02_*.{json,csv}`.
Rappel : rien de ce qu'affirme la source n'est tenu pour vrai ; on cherche ce que le composant *devrait* faire.

## 1. Ce que dit la source

- **[DOC]** DOC-008 : deux carters sphériques, ceinturés chacun de bobines (r.2), alimentés par deux
  « magnetic field generator / regulator » (r.3).
- **[DOC texte]** « The singularities are held in an enclosed magnetic field » ; « the magnetic field does not
  require the fantastic energies you might imagine » ; les singularités sont « electrified », « heavy, hot »,
  « 300–500 megawatts », « smaller than an electron » ; si le système magnétique cède, la singularité
  « would evaporate ».

## 2. Fonction théorique à remplir

Un trou noir de masse M posé dans un véhicule doit (a) être soutenu contre la pesanteur, force F = M g ;
(b) être maintenu en un point stable ; (c) être tenu à distance de son jumeau. Un champ magnétique n'agit que
sur une charge **en mouvement** (q v × B) ou sur un **moment magnétique** (∇(μ·B)) ; un champ électrique agit sur
une charge. Un trou noir n'offre que trois « poignées » : masse M, charge Q, moment cinétique J
(théorème de calvitie **[VÉR]**). Tout le dimensionnement découle donc de Q/M.

## 3. Quelle masse ? (re-dérivation de §6 du dossier)

Calcul indépendant des facteurs de corps gris (équations de Regge-Wheeler et de Dirac intégrées numériquement,
`c01_hawking.py`) :

| Grandeur | Notre calcul | Page (1976), éq. 29-30 | Étiquette |
|---|---|---|---|
| α total (γ, 4 états de ν, gravitons), P = α ħc⁶/(G²M²) | 2,0114×10⁻⁴ | 2,011×10⁻⁴ | **[VÉR]** reproduit |
| Répartition ν / γ / gravitons | 81,4 % / 16,7 % / 1,9 % | 81,4 % / 16,7 % / 1,9 % | **[VÉR]** reproduit |
| α avec e± ultra-relativistes | 3,648×10⁻⁴ | 3,6×10⁻⁴ | **[VÉR]** reproduit |
| Pics du flux en nombre (s = ½ ; s = 1) | 4,02 kT ; 5,73 kT | 4,02 ; 5,77 (MacGibbon, Carr & Page 2008) | **[VÉR]** |
| α pour kT ≈ 2–13 MeV (γ, 3 saveurs de ν = 6 états, e±, gravitons) | **4,47×10⁻⁴** | — | **[DÉD]** |
| Répartition correspondante | ν 55,0 % ; e± 36,6 % ; γ 7,5 % ; gravitons 0,9 % | — | **[DÉD]** |
| α « corps noir de photons » utilisé au §6 du dossier | 2,07×10⁻⁵ | — | sous-estime d'un facteur **21,6** |

Conséquence (fichier `c01_scenarios_puissance.csv`) — la masse dépend de ce que désigne « 300–500 MW » :

| Lecture de « 300–500 MW » | M (kg) | r_s (fm) | kT (MeV) | Puissance totale | g à 1 m |
|---|---|---|---|---|---|
| A — puissance totale, toutes particules | 3,9 à 5,1×10¹² | 5,8 à 7,5 | 2,1 à 2,7 | 300–500 MW | 27 à 34 g |
| B — puissance déposable (γ + e±) | 2,6 à 3,4×10¹² | 3,9 à 5,0 | 3,1 à 4,1 | 0,68–1,13 GW | 18 à 23 g |
| C — photons seuls | 1,08 à 1,39×10¹² | 1,6 à 2,1 | 7,6 à 9,8 | 4,0–6,6 GW | 7,3 à 9,4 g |
| D — formule du dossier (corps noir de photons) | 0,84 à 1,09×10¹² | 1,25 à 1,6 | 9,7 à 12,5 | 6,5–10,8 GW | 5,7 à 7,4 g |

Hypothèses : Schwarzschild (ni charge ni rotation), neutrinos à 6 états légers, muons négligés (< 10 % de la
part e± pour M > 6,8×10¹¹ kg selon Page 1977). Confiance : **élevée** sur α (recoupé), **moyenne** sur
l'interprétation de la phrase source. Dans tous les cas M ≈ 10¹² kg à un facteur 5 près, et la pesanteur à 1 m
vaut 6 à 34 g, pas 2 g (2 g à 1 m ⇔ 2,94×10¹¹ kg, qui rayonnerait ≈ 10¹¹ W).

## 4. Résultats chiffrés du confinement

| Grandeur | Équation | Valeur | Hypothèses / limites | Étiq. | Confiance |
|---|---|---|---|---|---|
| Force de sustentation | F = M g | 981 N (100 kg) ; 2,9×10¹² N (2,94×10¹¹ kg) ; 4,3×10¹³ N (4,4×10¹² kg) | g = 9,80665 m/s² | [VÉR] | élevée |
| Rapport charge/masse maximal | Q/M ≤ √(4πε₀G) | 8,62×10⁻¹¹ C/kg (électron : 1,76×10¹¹ C/kg, soit 2×10²¹ fois plus) | Reissner-Nordström extrémal | [VÉR] | élevée |
| Champ électrique de sustentation, charge extrémale | E = g/√(4πε₀G) | **1,14×10¹¹ V/m, indépendant de M** | charge maximale théorique | [DÉD] | élevée |
| … rapporté aux limites réelles | — | 1 100 × le gradient CLIC (10⁸ V/m) ; 110 × la rigidité idéale du diamant ; 2 × le champ d'évaporation du tungstène (57 V/nm) | toute électrode se désagrège avant | [DÉD] | élevée |
| Champ à l'horizon d'un trou extrémal | E_h = c⁴/(G^{3/2} M √(4πε₀)) | 3,2×10⁴¹ V/m pour 4,4×10¹² kg, soit 2,4×10²³ × la limite de Schwinger (1,32×10¹⁸ V/m) | critère de champ uniforme | [DÉD] | moyenne |
| Masse minimale pour porter la charge extrémale sans claquage du vide | E_h < E_S | 1,06×10³⁶ kg = 5×10⁵ M☉ | idem | [DÉD] | moyenne |
| Charge réellement tenable par un trou noir « chaud » | fluctuation thermique Z² ≈ 1/(4πα) | Z_rms ≈ 3,3 e (notre estimation) ; **6,14 e** (Page 1977, limite sans masse) | kT ≫ m_e c² | [VÉR] | élevée |
| Temps de retour à cette charge | 1/(Ṅ_e · e²/(4πε₀ r_s kT)) | ~10⁻¹⁹ s (4,4×10¹² kg) | ordre de grandeur | [DÉD] | moyenne |
| Champ de sustentation avec 6 e | E = M g/(6,14 e) | 10²¹ V/m (100 kg) ; 4×10³¹ V/m (4,4×10¹² kg) | — | [DÉD] | élevée |
| Piège de Penning : champ minimal | B ≥ √(2g/d)/(Q/M) | **5,1×10¹¹ T** (charge extrémale, d = 1 cm) ; 2×10³² T (6 e, 4,4×10¹² kg) | stabilité ω_c² > 2ω_z², ω_z² ≥ g/d | [DÉD] | élevée |
| Pulsation cyclotron réelle à 45,5 T | ω_c = (Q/M) B | 3,9×10⁻⁹ rad/s : un tour en **51 ans** | charge extrémale | [DÉD] | élevée |
| Piège de Paul équivalent | V = q_M r₀² Ω²/(2 Q/M) | 1,1×10¹⁰ V sur 1 cm (10¹² V/m) | q_M = 0,4 ; r₀ = 1 cm | [DÉD] | moyenne |
| Force sur le dipôle magnétique maximal | μ ≤ Q_max G M/(2c) ; ∂B/∂z = M g/μ | 10²⁸ T/m (100 kg) ; 2×10¹⁷ T/m (4,4×10¹² kg) | Kerr-Newman, g = 2 | [DÉD] | moyenne |
| Pression magnétique | B²/(2μ₀) | 0,82 GPa (45,5 T) ; 4,0 GPa (100,75 T) ; 573 GPa (1200 T) ; 10²⁹ Pa (5,1×10¹¹ T) | — | [VÉR] | élevée |
| Champ continu maximal contenable par un solide | B = √(2μ₀σ) | 50 T (1 GPa) ; 121 T (5,8 GPa) ; **572 T** (130 GPa, liaison idéale) | contrainte uniforme | [DÉD] | moyenne |
| Réaction du poids sur un carter de 4,0 cm de rayon | p = M g/(πr²) | 8,6×10¹⁵ Pa pour 4,4×10¹² kg ; masse maximale à 1 GPa : 5,1×10⁵ kg | appui sur la section ; rayon du logement de DOC-007 (Équipe A) | [DÉD] | élevée |
| Attraction mutuelle des deux singularités à 9,1 cm | F = G M²/d² | 1,6×10¹⁷ N = **3 600 × leur poids** (4,4×10¹² kg) ; période orbitale 7 ms. Pour 2,94×10¹¹ kg : 240 × et 28 ms | entraxe 0,091 m (DOC-007, Équipe A v1.1) ; avec l'ancienne hypothèse de 0,15 m : 1 300 × et 15 ms | [DÉD] | élevée |

### Gravité propre de la singularité sur son carter (`c02_gravite_propre.csv`)

| Distance | M = 2,94×10¹¹ kg (2 g à 1 m) | M = 4,4×10¹² kg (400 MW au total) |
|---|---|---|
| 1 mm | 2,0×10⁷ m/s² (2×10⁶ g) ; marée 3,9×10¹⁰ s⁻² | 2,9×10⁸ m/s² (3×10⁷ g) ; marée 5,9×10¹¹ s⁻² |
| 1 cm | 2,0×10⁵ m/s² (2×10⁴ g) ; marée 3,9×10⁷ s⁻² | 2,9×10⁶ m/s² (3×10⁵ g) ; marée 5,9×10⁸ s⁻² |
| 10 cm | 1 960 m/s² (200 g) ; marée 3,9×10⁴ s⁻² | 2,9×10⁴ m/s² (3 000 g) ; marée 5,9×10⁵ s⁻² |
| 1 m | 19,6 m/s² (2 g) ; marée 39 s⁻² | 294 m/s² (30 g) ; marée 587 s⁻² |

Pression hydrostatique induite dans de l'acier plein entre r et 10 cm : 14 MPa (r = 1 cm) à 150 MPa (r = 1 mm)
pour 2,94×10¹¹ kg ; 0,2 à 2,3 GPa pour 4,4×10¹² kg. **[DÉD]** La matière située à moins de quelques millimètres
flue vers le trou ; au-delà, le carter résiste à la gravité propre. Ce n'est donc pas la gravité propre qui
détruit le carter, mais (i) la réaction du poids, (ii) l'attraction du jumeau, (iii) la puissance rayonnée (fiche F4).

## 5. Analogues réels et théorème d'Earnshaw

- **[VÉR]** Earnshaw (1842) : aucune configuration de champs électrostatiques (ou magnétostatiques sur un dipôle
  fixe) ne piège de façon stable une charge. Les pièges réels contournent le théorème par un champ oscillant
  (Paul 1990) ou par la combinaison E statique + B (Penning ; Brown & Gabrielse 1986).
- Ces pièges fonctionnent parce que q/m est énorme : 1,76×10¹¹ C/kg pour un électron, 9,6×10⁷ C/kg pour un
  proton. Pour le trou noir le mieux chargé imaginable, q/m est 10¹⁸ à 10²¹ fois plus faible ; avec sa charge
  réelle (quelques e), 10²⁸ à 10³⁸ fois plus faible que celui du proton.
- Lévitation diamagnétique (Berry & Geim 1997) : elle porte de la matière ordinaire grâce à sa susceptibilité ;
  un trou noir n'a pas de susceptibilité magnétique exploitable.

## 6. Classement

| Élément | Statut physique | Constructible aujourd'hui ? |
|---|---|---|
| Enceinte sous vide sphérique de ~8 cm | Démontré | **Oui** (inox/aluminium, brides CF, pompe ionique) |
| Bobines de 1 à 20 T dans quelques cm, alimentation régulée | Démontré | **Oui** (REBCO + cryoréfrigérateur, mode persistant) |
| Confinement magnétique d'un trou noir neutre | Contredit (aucun couplage) | Non — impossible par principe |
| Confinement d'un trou noir chargé à l'extrémal | Contredit : 5×10¹¹ T, charge intenable (Schwinger, Gibbons 1975, Page 1977) | Non — impossible |
| Tenue mécanique de 10¹¹–10¹² kg dans un coffre | Contredit : 10¹⁴–10¹⁶ Pa contre ≤ 10¹¹ Pa pour toute matière | Non — impossible |
| Micro-trou noir de 10¹² kg (primordial) | Spéculatif (jamais observé) | Non |
| Micro-trou noir ≤ 100 kg « stable » | Contredit (4×10⁻¹³ s) | Non |

## 7. Limites de cette analyse

- Le critère de Schwinger est appliqué comme si le champ était uniforme ; pour r_s ≪ longueur de Compton de
  l'électron, le bon cadre est l'émission thermique biaisée (Page 1977) — c'est la valeur de 6,14 e que nous
  retenons. La conclusion (charge de quelques e au plus) ne dépend pas du critère.
- La rotation et la charge modifient le spectre de Hawking (Page 1976 II) : jusqu'à un ordre de grandeur sur la
  puissance pour un trou extrémal, sans effet sur les conclusions (écarts de 6 à 30 décades).
- Entraxe (9,1 cm) et rayon de logement (4,0 cm) : **[DÉD]** de l'Équipe A sur DOC-007, à l'échelle
  L = 0,85 ± 0,2 m (confiance faible) ; la fiche de corrections de la Red Team citait la version 1.0 (9,8 cm et
  3,85 cm : 3 100 × le poids, 8 ms). Excursion tolérée (1 cm) : **[HYP]**.
- Une physique inconnue (résidus stables, « particules subatomiques très intéressantes » de la source) ne peut
  pas être évaluée ; elle ne lèverait de toute façon pas la contrainte de poids, qui ne dépend que de M.

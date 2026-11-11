# EXP-09 — Effet Sagnac et gyromètre à fibre : mesurer une rotation — et pourquoi ce n'est pas l'entraînement des référentiels

| | |
|---|---|
| **Niveaux** | N1 (gyromètre de smartphone sur platine tournante) · N2 (interféromètre de Sagnac de table ou bobine de fibre sur plateau tournant) · N3 (gyrolasers géants ; mesures spatiales) |
| **Sous-système C204 lié** | « micro-singularités *top-spin* », « singularités dans le champ de Kerr », troisième levier de commande « faire tourner et orienter l'axe polaire » |
| **Statut physique** | Effet Sagnac : **démontré**, industriel. Effet Lense-Thirring : **démontré** dans l'espace et dans un pulsar binaire, jamais en laboratoire. Lense-Thirring de micro-trous noirs à 1 m : **prévu ; 10⁻²²–10⁻²⁰ rad/s pour le spin seul, jusqu'à 5 × 10⁻¹⁴ rad/s pour une paire en orbite ; indétectable par tout gyromètre transportable**. |
| **Calculateur** | `calculs/calc09_sagnac_lense_thirring.py` → `resultats/calc09_sagnac_lense_thirring.txt`, `figures/calc09_rotations.png` |

## 1. Objectif

Mesurer une vitesse de rotation par interférométrie optique ; comprendre ce que mesure exactement un gyromètre ;
distinguer cet effet cinématique de l'entraînement des référentiels par une masse en rotation, et chiffrer ce
dernier pour la Terre, pour un trou noir de Kerr isolé (spin seul) et pour une paire de trous noirs en orbite
(moment cinétique orbital), aux masses retenues par le programme (3,9–5,1 × 10¹² kg par singularité).

## 2. Principe et équations [VÉR]

- **Sagnac** (Sagnac 1913-1914 ; revue : Post 1967) : deux ondes parcourant en sens opposés une boucle d'aire A
  tournant à Ω se déphasent de Δφ = 8π·N·A·Ω/(λc). Bobine de fibre de longueur L et de diamètre D
  (Vali & Shorthill 1976) : **Δφ = 2π·L·D·Ω/(λc)**. Gyrolaser : battement Δf = 4AΩ·sin φ/(λP) (P : périmètre).
  L'effet est du premier ordre en v/c et s'explique en relativité restreinte : il mesure la rotation de
  l'instrument par rapport aux référentiels inertiels locaux.
- **Lense-Thirring** (Lense & Thirring 1918 ; traduction commentée : Mashhoon, Hehl & Theiss 1984) : une masse de
  moment cinétique J fait tourner les référentiels inertiels locaux à Ω_LT ~ G·J/(c²r³) (2GJ/(c²r³) sur l'axe).
- **Kerr** : moment cinétique maximal d'un trou noir J_max = G·M²/c — il croît comme **M²**.

## 3. État de l'art publié [VÉR]

| Référence | Système | Résultat |
|---|---|---|
| Michelson & Gale 1925 | rectangle de 2010 ft × 1113 ft de tubes à vide | rotation terrestre : 0,230 ± 0,005 frange observée pour 0,236 ± 0,002 calculée |
| Lefèvre 2014 (revue) | gyromètres à fibre | de la classe tactique (°/h) à la classe stratégique |
| Schreiber & Wells 2013 ; Schreiber et al. 2011 | gyrolasers géants (anneau « G », 4 m × 4 m) | variations de la rotation terrestre, mouvement du pôle |
| Bosi et al. 2011 | proposition de réseau de gyrolasers (GINGER) | objectif : Lense-Thirring terrestre **au sol** — non atteint à ce jour (à notre connaissance) |
| Ciufolini & Pavlis 2004 ; Ciufolini et al. 2016 | satellites LAGEOS / LARES | Lense-Thirring confirmé à ≈ 10 % puis ≈ 5 % (incertitudes discutées dans la littérature) |
| Everitt et al. 2011 (Gravity Probe B) | gyroscopes en orbite polaire | entraînement −37,2 ± 7,2 mas/an (prédit −39,2) ; géodétique −6601,8 ± 18,3 mas/an (prédit −6606,1) |
| Venkatraman Krishnan et al. 2020 | pulsar binaire avec naine blanche en rotation rapide | entraînement des référentiels dans un système stellaire |

## 4. Matériel et coût indicatif

| Niveau | Matériel | Coût |
|---|---|---|
| **N1** | smartphone (gyromètre MEMS), platine vinyle ou plateau tournant, application d'enregistrement | 0–50 € |
| **N2** | (a) interféromètre de Sagnac de table : laser He-Ne ≤ 1 mW (classe 2), séparatrice, 3 miroirs, photodiode, plateau tournant motorisé ; ou (b) bobine de 200 m de fibre monomode, coupleur 2×2, diode superluminescente fibrée (classe 1), photodiode | 800–3000 € |
| **N3** | gyrolaser géant monolithique, site souterrain | infrastructure |

## 5. Protocole pas à pas

### N1 — Smartphone
1. Poser le téléphone au centre de la platine, axe z vertical ; enregistrer à 33⅓ tr/min : attendu 3,491 rad/s.
   Répéter à 45 tr/min (4,712 rad/s) : facteur d'échelle du capteur.
2. Platine à l'arrêt : enregistrer 1 h. Calculer l'écart-type d'Allan du signal → instabilité de biais.
3. **Tentative de détection de la rotation terrestre** : mesurer 10 min axe z vers le haut, 10 min vers le bas
   (retournement), alterner 12 fois ; la demi-différence annule le biais. Signal attendu : Ω_T·sin(latitude)
   ≈ 5,5 × 10⁻⁵ rad/s à 49°. Résultat attendu : **marginal ou nul** (instabilité de biais du même ordre).

### N2 — Sagnac sur plateau tournant
1. Aligner l'interféromètre à faisceaux contra-propagatifs (teinte plate en sortie).
2. Tourner à Ω connu (codeur) de −2 à +2 rad/s ; mesurer le déphasage (déplacement de franges ou intensité
   en quadrature). Vérifier la linéarité en Ω et le changement de signe.
3. Vérifier la proportionnalité à l'aire (deux tailles de boucle) et l'indépendance vis-à-vis de la position de
   l'axe de rotation.
4. Bobine de fibre : même balayage ; comparer la pente mesurée à 2πLD/(λc).

## 6. Signal attendu et budget de bruit (calculé)

| Configuration | Δφ |
|---|---|
| Boucle de 1 m², He-Ne, 1 rad/s | 0,132 rad (0,021 frange) |
| Même boucle, rotation terrestre (48,85° N) | 7,3 × 10⁻⁶ rad |
| Fibre 200 m × Ø 10 cm, 1550 nm, 0,1 rad/s | 0,027 rad |
| Fibre 1 km × Ø 10 cm, rotation terrestre | 9,9 × 10⁻⁵ rad |
| Fibre 1 km × Ø 10 cm, 0,01 °/h | 6,6 × 10⁻⁸ rad |

Vérifications du script sur des valeurs publiées : Michelson-Gale → 0,236 frange (publié : 0,236) ; gyrolaser G
→ 348,6 Hz (connu : ≈ 348,5 Hz).

Bruit : en N2, une photodiode résout sans peine 10⁻³ rad en 1 s → rapport signal/bruit ≈ 100 à 1 rad/s ;
limitation réelle : vibrations du plateau et dérive d'alignement. La rotation terrestre demande une bobine
≥ 1 km et une modulation de phase : niveau industriel.

Échelle des rotations (rad/s) :

| Grandeur | Valeur |
|---|---|
| Rotation de la Terre | 7,29 × 10⁻⁵ |
| Instabilité de biais d'un MEMS de smartphone (~10 °/h) | 4,8 × 10⁻⁵ |
| Gyromètre à fibre de navigation (0,01 °/h) | 4,8 × 10⁻⁸ |
| Gyrolaser géant (~10⁻⁸ Ω_T après intégration) | 7 × 10⁻¹³ |
| Précession géodétique mesurée par Gravity Probe B | 1,0 × 10⁻¹² |
| **Lense-Thirring de la Terre au sol**, GJ/(c²R³) | **1,7 × 10⁻¹⁴** (2,3 × 10⁻¹⁰ Ω_T) |
| Entraînement mesuré par Gravity Probe B (39,2 mas/an) | 6,0 × 10⁻¹⁵ |
| **Spin seul** — Kerr extrémal isolé, à 1 m : 10¹² kg (ancienne valeur) | 3,3 × 10⁻²² |
| **Spin seul** — Kerr extrémal isolé, à 1 m : 3,9–5,1 × 10¹² kg (masse retenue) | **5,0–8,6 × 10⁻²¹** |
| **Paire en orbite**, à 1 m : 2 × 10¹² kg, entraxe 0,30 m | 4,7 × 10⁻¹⁵ |
| **Paire en orbite**, à 1 m : 2 × (3,9–5,1) × 10¹² kg, entraxe 0,098 m (valeur documentaire, Équipe A) | 2,1–3,1 × 10⁻¹⁴ |
| **Paire en orbite**, à 1 m : 2 × (3,9–5,1) × 10¹² kg, entraxe 0,30 m | **3,6–5,4 × 10⁻¹⁴** |

(Performances des gyromètres : ordres de grandeur indicatifs.)

**Deux termes à ne pas confondre** (correction n° 54 de la Red Team n° 2 ; dossier v1.2, erratum E15) :
- *spin* : J_max = GM²/c ∝ M², dérisoire pour un micro-trou noir ;
- *moment orbital* d'une paire liée : L = (M/2)·√(2GMd), soit 1,4–3,6 × 10¹³ kg·m²/s — **10⁷ fois plus** que le spin.
  Il n'existe que si les deux singularités **orbitent** l'une autour de l'autre (période 7 à 45 ms, vitesse 20 à
  40 m/s) ; il est nul si elles sont tenues fixes dans des « logements », ce que dessine le manuel. C'est donc une
  **borne supérieure**. La formule de champ lointain appliquée à 1 m (3 à 10 entraxes) est un ordre de grandeur.

Écart à la résolution d'un gyrolaser géant (≈ 7 × 10⁻¹³ rad/s) : **8 à 9 ordres de grandeur pour le spin, ≈ 1 ordre
de grandeur (facteur 13 à 150) pour une paire en orbite** — « 1 à 9 ordres de grandeur selon le terme ». Écart à
un gyromètre transportable (≥ 5 × 10⁻¹⁰ rad/s) : au moins 4 ordres de grandeur dans tous les cas.

## 7. Durée

N1 : 3 h. N2 : deux séances de TP.

## 8. Analyse des données

Régression Δφ(Ω) et comparaison de la pente à la valeur théorique (incertitudes sur A, λ, Ω) ; écart-type
d'Allan du biais ; pour la tentative « Terre » : moyenne des demi-différences, test de Student contre zéro et
contre la valeur attendue — conclure honnêtement si les deux sont compatibles (mesure non concluante).

## 9. Sécurité

Laser He-Ne ≤ 1 mW (classe 2), faisceaux horizontaux sous le niveau des yeux, capot sur le plateau tournant ;
source fibrée de classe 1, ne pas regarder les extrémités de fibre. Plateau tournant : vitesse limitée (< 30 tr/min
pour une table optique), éléments vissés, câbles en spirale ou collecteur tournant.

## 10. Ce que cela prouve — et ne prouve PAS

**Prouve** : la lumière permet de mesurer une rotation absolue de l'instrument avec la sensibilité prévue ; les
gyromètres optiques sont des instruments réels et précis.

**Ne prouve pas** : l'entraînement des référentiels. Un gyromètre à fibre ne « détecte » pas un champ de Kerr :
il mesure la rotation mécanique de son châssis. L'effet Lense-Thirring n'a été mesuré que dans l'espace
(≈ 6 × 10⁻¹⁵ rad/s) et dans un pulsar binaire ; il n'a aucun rapport avec une quelconque inversion du temps.

## 11. Lien avec la C204 [DÉD]

- **Spin** : un trou noir de 3,9–5,1 × 10¹² kg, même en rotation **maximale**, ne porte que J_max = GM²/c =
  3,4–5,8 × 10⁶ kg·m²/s (2,2 × 10⁵ pour 10¹² kg) — le moment cinétique d'un gros volant d'inertie industriel (un
  volant de 10 kg, 15 cm, 6000 tr/min : 71 kg·m²/s). À 1 m, l'entraînement dû au spin vaut 5,0–8,6 × 10⁻²¹ rad/s :
  2 à 3 × 10⁶ fois moins que celui de la Terre au sol.
- **Paire en orbite** : si les deux singularités tournaient l'une autour de l'autre, leur moment orbital
  produirait à 1 m jusqu'à **5 × 10⁻¹⁴ rad/s**, soit 1 à 3 fois l'effet Lense-Thirring terrestre au sol
  (1,7 × 10⁻¹⁴ rad/s) et jusqu'à 9 fois l'entraînement mesuré par Gravity Probe B. La première version de cette
  fiche donnait « ≤ 3,3 × 10⁻²² rad/s » comme une borne : c'était le spin seul, et la borne était fausse pour une
  paire. Cela reste sans effet causal, et hors de portée de tout gyromètre qu'on puisse approcher d'un véhicule.
- Le « champ de Kerr » de chaque objet ne diffère d'un champ sans rotation qu'à des distances de l'ordre de son
  rayon gravitationnel (~10⁻¹⁴ m). « Faire tourner et orienter l'axe » n'aurait aucun effet mesurable à
  l'échelle d'un véhicule.
- Les qualificatifs « top-spin, dual-positive » n'ont pas de signification identifiée en physique (dossier §5.5).

## 12. Confiance et limites

Formules de Sagnac et vérifications (Michelson-Gale, anneau G) : confiance **élevée**. Chiffres Gravity Probe B :
**élevée** (valeurs publiées). Formule d'entraînement en champ lointain appliquée à 1 m d'un micro-trou noir
isolé : **élevée** (1 m ≈ 10¹⁴ rayons gravitationnels) ; appliquée à 1 m d'une paire d'entraxe 0,1–0,3 m :
**moyenne** (ordre de grandeur ; partie oscillante ignorée ; l'hypothèse d'une orbite libre n'est pas dans les
documents). Performances de capteurs : **moyenne**.

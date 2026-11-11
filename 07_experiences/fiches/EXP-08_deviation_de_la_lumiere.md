# EXP-08 — Déviation de la lumière : gravitationnelle (indétectable ici) contre gradient d'indice (visible à l'œil)

| | |
|---|---|
| **Niveaux** | N1 (cuve d'eau sucrée stratifiée, mirage) · N2 (mesure quantitative, strioscopie au-dessus d'un boîtier tiède) · N3 (sans objet : l'état de l'art est astronomique) |
| **Sous-système C204 lié** | phénoménologie « lumière courbée autour du véhicule » ; photographie dite « du laser », **C204-DOC-012** (252 × 206 px, retrouvée par l'Équipe A après la première version de cette fiche ; dossier v1.2, erratum E16) |
| **Statut physique** | Déviation gravitationnelle de la lumière : **démontrée** (Soleil, 1,75″). Par 3,9 × 10¹² à 1,0 × 10¹³ kg à 1 m : **prévue mais indétectable** (1,2 à 3,0 × 10⁻¹⁴ rad). Courbure par gradient d'indice : **démontrée** dans un liquide, triviale à reproduire ; **bornée à ≈ 1° dans l'air**. |
| **Calculateur** | `calculs/calc08_deviation_lumiere.py` → `resultats/calc08_deviation_lumiere.txt`, `figures/calc08_deviation_lumiere.png` |

## 1. Objectif

(a) Calculer la déviation gravitationnelle d'un faisceau passant à 1 m des masses qu'impliquerait le récit
(3,9–5,1 × 10¹² kg par singularité) et montrer qu'elle est indétectable. (b) Produire un faisceau laser
**visiblement courbé** par un gradient d'indice, pour montrer ce qu'il faut physiquement pour courber la lumière —
et (c) dire honnêtement si cela explique la photographie C204-DOC-012 (réponse : pas si la scène est dans l'air).

## 2. Principe et équations [VÉR]

- Relativité générale, champ faible : **α = 4GM/(c²b)** (b : paramètre d'impact). Équivaut à un indice effectif
  n = 1 + 2GM/(rc²).
- Milieu d'indice variable : d/ds(n·d**r**/ds) = ∇n ; courbure 1/R = |∇⊥n|/n ; invariant de Snell n·cos θ = cste
  pour une stratification horizontale.
- Air : n − 1 ≈ 2,7 × 10⁻⁴ ∝ densité → dn/dT ≈ −(n − 1)/T = −9,2 × 10⁻⁷ K⁻¹.
- Solution sucrée après diffusion pendant t : profil en fonction d'erreur d'épaisseur 2√(Dt),
  D ≈ 5 × 10⁻¹⁰ m²/s (saccharose dilué ; ordre de grandeur).
- Mirage : angle rasant critique θ_c ≈ √(2Δn/n).

## 3. État de l'art publié [VÉR]

Dyson, Eddington & Davidson 1920 (éclipse de 1919) ; Shapiro et al. 2004 (VLBI, paramètre γ à quelques 10⁻⁴) ;
Bertotti, Iess & Tortora 2003 (retard Shapiro avec Cassini, γ − 1 = (2,1 ± 2,3) × 10⁻⁵). Faisceaux « rebondissants »
en milieu stratifié : Ambrosini et al. 1997.

## 4. Matériel et coût indicatif

| Niveau | Matériel | Coût |
|---|---|---|
| **N1** | cuve transparente à faces planes de 30–40 cm ; 1 kg de sucre ; entonnoir + tube souple ; pointeur laser **classe 2** (< 1 mW) ; quelques gouttes de lait (visualisation) ; trépied ; papier millimétré | 20–40 € |
| **N2** | idem + réfractomètre (ou mesure de n par déviation en cuve prismatique) ; platine de translation ; caméra ; boîtier chauffé à 40–50 °C par résistance **basse tension** ; lentille/miroir pour strioscopie ; détecteur de position | 300–800 € |

## 5. Protocole pas à pas

### N1 — Cuve stratifiée
1. Préparer un sirop à ≈ 65 % en masse (≈ 850 g de sucre par litre de solution, n ≈ 1,45) ; un sirop à 50 %
   (≈ 615 g par litre, n ≈ 1,42) convient aussi, avec une déviation maximale plus faible. Laisser refroidir.
2. Remplir la cuve à mi-hauteur d'eau légèrement troublée (2–3 gouttes de lait par litre).
3. **Injecter le sirop par le fond**, lentement, avec l'entonnoir et le tube : deux couches nettes.
4. Attendre 6 à 24 h sans vibration (diffusion).
5. Envoyer le faisceau horizontalement, à travers la face d'entrée, à la hauteur de l'interface : il s'incurve
   vers le bas. Le relever point par point sur le papier millimétré collé derrière la cuve.
6. Injecter le faisceau depuis le bas, légèrement vers le haut : il décrit une **arche** et retombe ; avec un
   fond réfléchissant il « rebondit ».
7. Photographier de profil. Montrer la photo à un tiers sans légende : « qu'est-ce qui courbe la lumière ? ».

### N2 — Quantitatif et thermique
1. Mesurer n(y) par la déviation d'un faisceau fin traversant la cuve à différentes hauteurs.
2. Intégrer l'équation des rayons avec ce profil ; superposer trajectoires calculées et mesurées.
3. Faisceau rasant la face supérieure du boîtier tiède (ΔT ≈ 25 K) sur 30 cm : mesurer le déplacement du spot à
   3 m quand on allume / éteint le chauffage (attendu : 10⁻⁵ à 10⁻⁴ rad, soit 0,03 à 0,3 mm).
4. Strioscopie : visualiser le panache d'air chaud.

## 6. Signal attendu et budget de bruit (calculé)

Déviation gravitationnelle :

| Cas | α (rad) | Déplacement à 10 m |
|---|---|---|
| Soleil, rayon rasant | 8,5 × 10⁻⁶ (1,75″) | — |
| Terre, rayon rasant | 2,8 × 10⁻⁹ | — |
| 227 kg à 0,1 m | 6,7 × 10⁻²⁴ | 7 × 10⁻²³ m |
| une singularité de 3,9–5,1 × 10¹² kg, à 1 m (masse retenue) | **1,2–1,5 × 10⁻¹⁴** | 1,2–1,5 × 10⁻¹³ m |
| la paire (7,8 × 10¹² à 1,0 × 10¹³ kg), à 1 m | **2,3–3,0 × 10⁻¹⁴** | 2–3 × 10⁻¹³ m (un millième d'atome) |
| masse donnant « 2 g à 1 m » (2,9 × 10¹¹ kg) | 8,7 × 10⁻¹⁶ | 9 × 10⁻¹⁵ m |
| ancienne fourchette du dossier v1 (10¹¹–10¹² kg), à 1 m | 3,0 × 10⁻¹⁶ – 3,0 × 10⁻¹⁵ | — |

Pour dévier de 1° à 1 m, il faudrait **5,9 × 10²⁴ kg** — une masse terrestre (rayon de Schwarzschild 8,7 mm).

Limite de détection : laser de 1 mW à 633 nm, col de 1 mm → bruit de photons ≈ 3,6 × 10⁻¹² rad/√Hz (borne
idéale). Voir 1,2 × 10⁻¹⁴ rad à 3σ prendrait 8,5 × 10⁵ s (10 jours) ; 3,0 × 10⁻¹⁴ rad : 1,5 jour — avec une
modulation parfaite de la masse et aucune dérive. En pratique, la stabilité de pointé et la turbulence de l'air
(~µrad) placent le plancher 7 à 8 ordres de grandeur au-dessus. **Indétectable.**

Gradients d'indice :

| Cause | Courbure | Rapport à la déviation totale par la paire (1,0 × 10¹³ kg) à 1 m |
|---|---|---|
| Air, 1 K/m transverse | 9 × 10⁻⁷ rad/m | 3 × 10⁷ |
| Air, 100 K/m (près d'une paroi tiède) | 9 × 10⁻⁵ rad/m | 3 × 10⁹ |
| Eau sucrée stratifiée (1 jour) | ≈ 3,6 rad/m | 10¹³ (sur 10 cm) |

**Borne dans l'air** : la déviation totale d'un rayon rasant ne peut excéder √(2Δn) : 0,43° pour un écart thermique
de 30 K, et 1,33° même entre le vide et l'air (Δn = 2,7 × 10⁻⁴). Une courbure de plusieurs dizaines de degrés
exige un milieu dense (Δn ~ 0,1 : liquide, verre, guide de lumière).

Cuve : déviation maximale d'un rayon entré horizontalement = arccos(n_eau/n_sirop) = **23°** ; après 10 cm de
trajet, descente de 25 mm (6 h de diffusion), 17 mm (1 jour), 10 mm (3 jours), 7 mm (7 jours). Rayon de
courbure minimal : 14 cm (6 h), 28 cm (1 jour). Incertitude de relevé : ± 1 mm → profil mesuré à quelques %.
Mirage : θ_c = 0,17° (ΔT = 5 K), 0,35° (20 K), 0,49° (40 K).

## 7. Durée

N1 : 1 h de préparation + une nuit d'attente + 1 h de mesures. N2 : deux séances.

## 8. Analyse des données

Relevé y(x) du faisceau ; ajustement du profil n(y) (trois paramètres : n_haut, n_bas, épaisseur) ; comparaison à
l'épaisseur 2√(Dt) attendue ; pour le thermique, différence marche/arrêt moyennée sur 20 cycles.

## 9. Sécurité

Laser de **classe 2 au maximum** (< 1 mW, visible), jamais dirigé vers un visage ni vers une surface
réfléchissante à hauteur d'yeux ; se méfier des pointeurs verts sous-étiquetés (préférer un module rouge
certifié). Sirop chaud : laisser refroidir avant transvasement. Chauffage du boîtier : résistance en très basse
tension, température de surface < 50 °C.

## 10. Ce que cela prouve — et ne prouve PAS

**Prouve** : qu'un gradient d'indice courbe un faisceau de dizaines de degrés **dans un liquide stratifié**, de
façon parfaitement visible et photographiable ; que dans l'air la réfraction ne dépasse pas ≈ 1° ; que la
déviation gravitationnelle par les masses qu'implique le récit est inférieure de 12 à 14 ordres de grandeur à
toute courbure visible.

**Ne prouve pas** : que la photographie C204-DOC-012 ait été obtenue par réfraction. Au contraire : si la scène
est dans l'air (la légende rapportée parle d'un faisceau rendu visible par de la fumée), **la réfraction ne
l'explique pas non plus** (voir §11). La cuve montre ce qu'il faut pour courber la lumière ; elle n'identifie pas
le procédé de l'image.

## 11. Lien avec la C204 [DÉD] — confrontation à la photographie C204-DOC-012

Description [DOC, Équipe A, incohérence I-11] : scène sombre ; une main tient un objet d'où part un trait rouge,
rectiligne sur environ deux tiers de sa longueur, courbé sur le dernier tiers, **interrompu net dans l'air** ;
luminosité inégale ; aucun objet voisin n'est déformé. Légende rapportée par des sites tiers [DOC texte, source
secondaire] : faisceau laser « courbé par le champ gravitationnel » de l'unité, rendu visible par de la fumée.

Lecture visuelle de l'Équipe F sur la copie agrandie (`01_archive/ameliores/alt_laser_fetch_x5.png`), **confiance
faible** (projection 2D, 252 px, échelle supposée sur la largeur d'une main) : changement de direction d'environ
45–65° ; rayon de courbure de l'ordre de 10 cm [HYP].

| Explication | Ce qu'elle exige pour ~55° sur ~10 cm | Verdict |
|---|---|---|
| Gravitation | champ transverse g = c²/(2R) = 4,5 × 10¹⁷ m/s² = **4,6 × 10¹⁶ g** ; avec les « 2 g » revendiqués, le rayon de courbure serait 2,3 × 10¹⁵ m (0,24 année-lumière) | exclue par 16 ordres de grandeur ; et rien d'autre n'est déformé dans l'image |
| Réfraction dans l'air | gradient dn/dy ≈ 10 m⁻¹, alors que l'air offre au plus ~10⁻³ m⁻¹ ; déviation totale bornée à 0,4° (30 K) – 1,3° (vide/air) | exclue par ~2 ordres de grandeur sur l'angle |
| Réfraction dans un liquide stratifié | dn/dy ≈ 10 m⁻¹ : atteint dans la cuve sucrée après 6 h | possible physiquement, mais **incompatible avec une scène dans l'air** |
| Guide de lumière souple à émission latérale, pose longue avec source mobile, retouche | — | ordinaires et suffisants [HYP] ; **aucun n'est démontrable** sur une image de 252 px |

- « Lumière courbée autour du véhicule puis noir complet » : une courbure visible exige une masse planétaire à
  1 m (§6), incompatible avec 227 kg comme avec 10¹³ kg.
- Une unité « à 38–49 °C » crée des gradients thermiques de 10²–10³ K/m près de ses parois : effet réfractif
  10⁹–10¹⁰ fois supérieur à l'effet gravitationnel de la paire — mais encore mille fois trop faible pour l'image.
- Conclusion prudente : la photographie n'est pas une preuve de déviation gravitationnelle (constat I-11 de
  l'Équipe A, que ce calcul chiffre) ; son procédé réel n'est pas identifié.

## 12. Confiance et limites

Formule α = 4GM/(c²b) et valeurs : confiance **élevée**. Borne de réfraction dans l'air : **élevée**. Profil
d'indice et coefficient de diffusion du sirop : **moyenne** (D dépend fortement de la concentration ; la cuve
réelle évolue plus lentement que le calcul). Limite de bruit de photons : ordre de grandeur idéal. Angle et rayon
de courbure lus sur DOC-012 : **faible** (non mesurés au pixel ; l'argument tient à plus de dix ordres de grandeur
pour la gravitation et à deux pour la réfraction dans l'air). La première version de cette fiche présentait le
gradient d'indice comme « explication quantitativement suffisante » d'une photo alors non archivée : c'était trop
fort, et c'est corrigé ici.

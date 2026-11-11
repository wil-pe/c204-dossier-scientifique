# EXP-07 — Confinement d'objets chargés : piège de Paul basse fréquence, selle tournante, lévitation diamagnétique

| | |
|---|---|
| **Niveaux** | N1 (**sans haute tension** : selle tournante, lévitation diamagnétique) · N2 (piège de Paul à grains chargés, en TP encadré, alimentation à courant limité) · N3 (pièges à ions, particules lévitées sous vide) |
| **Sous-système C204 lié** | « logements magnétiques des deux micro-singularités » ; repères 1–3 de DOC-008 (*singularity drive housing*, *magnetic field coil*, *field generator/regulator*) ; affirmation « si le confinement cède, la singularité s'évapore » |
| **Statut physique** | Piégeage électrodynamique et lévitation diamagnétique : **démontrés**. Confinement d'un trou noir chargé de 3,9–5,1 × 10¹² kg : **contredit les ordres de grandeur** (5 à 12 ordres de grandeur hors de portée à la charge extrémale ; plus de 20 avec la charge réellement tenable). |
| **Calculateur** | `calculs/calc07_piege_paul_levitation.py` → `resultats/calc07_piege_paul_levitation.txt`, `figures/calc07_mathieu.png` |

## 1. Objectif

Montrer comment on confine réellement un objet chargé (ou diamagnétique) malgré le théorème d'Earnshaw, mesurer
les conditions de stabilité, et chiffrer l'écart entre une poussière piégée et la « singularité chargée »
revendiquée.

## 2. Principe et équations [VÉR]

**Théorème d'Earnshaw** : aucune configuration statique de charges (ou d'aimants permanents) ne possède
d'équilibre stable. Trois échappatoires réelles : champ **oscillant** (Paul), **diamagnétisme**, **rétroaction**.

**Piège de Paul** (Paul 1990 ; Wuerker, Shelton & Langmuir 1959 pour des particules macroscopiques) : potentiel
quadrupolaire Φ ∝ (U + V cos Ωt). Avec ξ = Ωt/2, chaque coordonnée obéit à l'équation de Mathieu
x″ + 2b·x′ + (a − 2q·cos 2ξ)·x = 0. Pour un piège annulaire (r₀² = 2z₀²) :
q_z = 4QV/(m·r₀²·Ω²), a_z = −8QU/(m·r₀²·Ω²). Sans amortissement (b = 0) et a = 0 : stable si **q < 0,908**.
Mouvement séculaire (q ≲ 0,4) : ω_sec = q·Ω/(2√2). Dans l'air, frottement de Stokes : b = 1/(Ω·τ), τ = m/(6πηa) ;
la zone stable s'élargit, mais la force de rappel moyenne est réduite du facteur 1/(1 + b²).

**Selle tournante** (analogue mécanique : Rueckner et al. 1995 ; Thompson, Harmon & Ball 2002) : surface
z = (x² − y²)/(2R_c) tournant à Ω. Dans le repère tournant, λ² = −Ω² ± ω₀² avec ω₀² = g/R_c : l'origine est
stable si **Ω > ω₀** (équivalent q = ω₀²/(2Ω²) < ½).

**Lévitation diamagnétique** (Berry & Geim 1997 ; Simon & Geim 2000) : équilibre si B·dB/dz = µ₀·ρ·g/|χ|.

Références pédagogiques pour le piège à grains [VÉR] : Winter & Ortjohann 1991 (démonstration simple du stockage
de particules macroscopiques dans un « piège de Paul ») ; Libbrecht & Black 2018 (pièges électrodynamiques à
microparticules pour l'enseignement) ; Vinitsky, Black & Libbrecht 2015 (dynamique en piège amorti non linéaire).

## 3. Matériel et coût indicatif

| Niveau | Matériel | Coût |
|---|---|---|
| **N1** | selle imprimée ou moulée (R_c ≈ 30 cm) sur plateau tournant à vitesse réglable (60–150 tr/min), billes ; 4 à 9 cubes NdFeB de 10 mm en damier, plaquette de graphite pyrolytique, mine de crayon ; smartphone (ralenti) | 50–120 € |
| **N2** | piège pédagogique à anneau ou linéaire avec **alimentation de TP certifiée à courant limité**, capot isolant interverrouillé ; poudre de lycopode ou microbilles de verre creuses ; pointeur laser classe 2 (éclairage) ; caméra ; sondes haute tension de TP | 1–3 k€ (kit) |
| **N3** | piège à ions sous ultravide, lasers de refroidissement ; ou microsphère lévitée | laboratoire |

## 4. Protocole pas à pas

### N1-a — Selle tournante
1. Poser une bille au centre, plateau à l'arrêt : elle tombe en < 1 s (point selle instable).
2. Augmenter Ω. Chronométrer le temps de séjour de la bille (10 essais par vitesse).
3. Repérer le seuil : attendu Ω > √(g/R_c) = 5,7 rad/s (**55 tr/min**) pour un point matériel ; le roulement
   déplace ce seuil et le frottement finit par éjecter la bille (durée de vie finie, à mesurer).
4. Filmer : on voit le mouvement lent (séculaire) et le micromouvement à 2Ω.

### N1-b — Graphite pyrolytique en lévitation
1. Damier d'aimants (pôles alternés) ; poser la plaquette de graphite : elle flotte à ≈ 0,5–1,5 mm.
2. Mesurer la hauteur à la caméra ; ajouter de petites surcharges (papier, mg) jusqu'au contact : force de portance.
3. Remplacer par de l'aluminium, du cuivre, du plastique : rien ne flotte (|χ| trop faible).

### N2 — Piège de Paul à grains (TP encadré)
1. Capot fermé, alimentation éteinte : introduire les grains (chargés par frottement) ; refermer.
2. Monter la tension alternative ; observer les grains piégés (points lumineux, alignés sur l'axe).
3. Mesurer l'amplitude du micromouvement et la position d'équilibre en fonction de V ; appliquer la tension
   continue de compensation du poids : E = g/(Q/m) → en déduire Q/m de chaque grain.
4. Parcourir le plan (U, V) : relever les limites d'éjection ; comparer au diagramme de Mathieu amorti.
5. Abaisser la fréquence (alimentation de TP à fréquence variable) : la limite se déplace comme Ω².

## 5. Signal attendu et budget de bruit (calculé)

Stabilité (matrice de monodromie, calcul numérique) : q_max = 0,908 (b = 0) ; 0,985 (b = 0,2) ; 1,34 (b = 0,5) ;
2,37 (b = 1) ; 6,1 (b = 2) ; 8,0 (b = 2,3).

Piège annulaire r₀ = 5 mm, V = 2000 V, 50 Hz ; grain de lycopode (rayon 15 µm, 7 × 10⁻¹² kg, τ = 1,4 ms, b = 2,3) :

| Q/m (C/kg) | charges élémentaires | q_z | stable (vide) | stable (air) | champ de compensation du poids |
|---|---|---|---|---|---|
| 5 × 10⁻⁵ | 2 200 | 0,16 | oui | oui | 2,0 × 10⁵ V/m |
| 1 × 10⁻⁴ | 4 400 | 0,32 | oui | oui | 9,8 × 10⁴ V/m |
| 2 × 10⁻⁴ | 8 800 | 0,65 | oui | oui | 4,9 × 10⁴ V/m |
| 1 × 10⁻³ | 44 000 | 3,2 | non | **oui** | 9,8 × 10³ V/m |
| 3 × 10⁻³ | 132 000 | 9,7 | non | non | 3,3 × 10³ V/m |

Sans compensation, le grain s'affaisse de g·(1 + b²)/ω_sec² : 12 mm pour Q/m = 2 × 10⁻⁴ C/kg (> r₀) → la
compensation continue (quelques centaines de volts sur 1 cm) est indispensable. Dispersion attendue de Q/m d'un
grain à l'autre : un ordre de grandeur (c'est ce qu'on mesure).

Lévitation : graphite pyrolytique ≥ 60 T²/m ; bismuth ≥ 730 T²/m ; eau ≥ 1360 T²/m. Damier NdFeB près de la
surface : 60–120 T²/m → seul le graphite flotte. L'eau (grenouille de Berry & Geim) exige ≈ 16 T.

## 6. Durée

N1 : une journée (fabrication comprise). N2 : deux séances de TP.

## 7. Analyse des données

Selle : durée de vie en fonction de Ω (échelle log), seuil par ajustement. Piège : histogramme des Q/m ;
frontière de stabilité expérimentale superposée au calcul ; vérification de la loi V_limite ∝ Ω².
Lévitation : hauteur en fonction de la surcharge → gradient de force.

## 8. Sécurité — haute tension : prescriptions strictes

- **Niveau N1 : aucune haute tension.** Les deux expériences N1 n'en utilisent pas.
- Le piège électrique n'est réalisé qu'en **TP encadré (N2)**, avec du matériel pédagogique certifié.
- Dimensionnement à courant limité (calcul, pas un plan) : tension crête ≤ 3 kV ; courant de court-circuit
  ≤ 0,5 mA → résistance série totale ≥ 6 MΩ répartie sur au moins deux résistances haute tension en série
  (tolérance à une panne) ; capacité des électrodes ~10 pF → charge 30 nC, énergie 45 µJ, soit des marges de
  ×1500 et ×7800 sous les repères usuels (45 µC ; 350 mJ — famille de normes CEI 61010, à vérifier dans
  l'édition en vigueur).
- **Interdits** hors laboratoire : transformateur d'enseigne au néon, transformateur de four à micro-ondes, bobine
  d'allumage, multiplicateurs de tension artisanaux, tout condensateur haute tension.
- Capot isolant fermé avant mise sous tension ; interverrouillage ; une main dans la poche ; décharge et mise à
  la terre avant toute intervention ; jamais seul.
- Poudre de lycopode : inflammable en nuage ; quantités de l'ordre du milligramme, pas de flamme ni d'étincelle
  à l'air libre ; préférer les microbilles de verre.
- Aimants NdFeB : pincement, éclats ; éloigner des stimulateurs cardiaques. Plateau tournant : capot, vitesse
  limitée, cheveux et manches attachés.

## 9. Ce que cela prouve — et ne prouve PAS

**Prouve** : un champ oscillant confine une charge là où aucun champ statique ne le peut ; la stabilité suit
l'équation de Mathieu ; le diamagnétisme permet une lévitation statique passive.

**Ne prouve pas** : qu'on puisse « loger » magnétiquement une singularité. Le rapport charge/masse décide de tout,
et il est défavorable de 6 ordres de grandeur dès le meilleur cas théorique (ci-dessous).

## 10. Lien avec la C204 [DÉD]

Trou noir de 4,4 × 10¹² kg (masse retenue par singularité : 3,9–5,1 × 10¹² kg, dossier v1.2, erratum E2) à la
charge maximale (extrémale) Q_max = M·√(4πε₀G) = **379 C** (86 C pour l'ancienne valeur de 10¹² kg) :

- Q/m = 8,6 × 10⁻¹¹ C/kg — **indépendant de la masse** —, soit **10⁶ fois moins** que la poussière piégée
  (10⁻⁴ C/kg) et 2 × 10²¹ fois moins qu'un électron ;
- porter son poids (4,3 × 10¹³ N) demande un champ électrique E = g/(Q/m) = **1,1 × 10¹¹ V/m** (rigidité de
  l'air : 3 × 10⁶ V/m ; émission de champ des métaux : 10⁹–10¹⁰ V/m) ;
- un piège de Paul à 50 Hz de 10 cm à q = 0,4 demanderait **1,2 × 10¹² V** ;
- une force magnétique Q·v·B est nulle au repos ; même à 1 m/s il faudrait 1,1 × 10¹¹ T ;
- et le poids lui-même (4 × 10¹³ N par singularité, ≈ 10¹⁴ N pour la paire) doit être repris par le plancher d'un camion.

Le texte attribué à Titor parle de confinement **magnétique** d'objets **chargés au repos** : un champ
magnétique statique n'exerce aucune force sur une charge immobile. Les repères « magnetic field coil » ne
décrivent donc pas un mécanisme de sustentation connu.

Charge réellement tenable (dossier v1.2, erratum E14 ; Équipes B et C ; Red Team n° 2) : un micro-trou noir se
décharge spontanément (Gibbons 1975) et ne retient qu'**≈ 6 charges élémentaires** en valeur quadratique moyenne
(borne supérieure ≈ 137). Le rapport Q/m tombe alors à 2 × 10⁻³¹ – 6 × 10⁻³⁰ C/kg et le champ de sustentation à
**2 × 10³⁰ – 5 × 10³¹ V/m** : les chiffres ci-dessus (charge extrémale) sont le cas **le plus favorable**, lui-même
intenable, et il est déjà hors de portée.

## 11. Confiance et limites

Équation de Mathieu, limites de stabilité : confiance **élevée** (0,908 retrouvé numériquement). Paramètres des
grains (masse, charge) : **faible à moyenne** (très dispersés). Force réduite en 1/(1 + b²) : approximation du
pseudo-potentiel amorti, **moyenne**. Seuil de la selle : modèle du point matériel, à confronter à la mesure.

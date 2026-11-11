# EXP-06 — Gravité analogue : horizon et ergorégion dans un écoulement d'eau

| | |
|---|---|
| **Niveaux** | N1 (ressaut hydraulique circulaire dans un évier ; tourbillon de vidange) · N2 (canal à houle avec obstacle ; bassin à tourbillon et batteur) · N3 (condensats de Bose-Einstein, fibres optiques, superfluides) |
| **Sous-système C204 lié** | « singularités dans le champ de Kerr », « horizons des événements de temps négatif / nul / positif » (DOC-009) |
| **Statut physique** | Horizons et superradiance **analogues** : démontrés en laboratoire. Ce sont des analogies cinématiques pour des ondes, pas de la gravitation. |
| **Calculateur** | `calculs/calc06_gravite_analogue.py` → `resultats/calc06_gravite_analogue.txt`, `figures/calc06_gravite_analogue.png` |

## 1. Objectif

Observer et mesurer, avec de l'eau, deux notions invoquées par le vocabulaire « Kerr » : un **horizon** (frontière
que les ondes ne franchissent que dans un sens) et une **ergorégion** (zone où aucune onde ne peut rester
immobile face à la rotation), puis énoncer précisément ce que l'analogie enseigne et ce qu'elle n'enseigne pas.

## 2. Principe et équations [VÉR]

Des ondes longues de vitesse c se propageant sur un fluide de vitesse **v** obéissent à la même équation qu'un
champ scalaire dans une métrique effective (Unruh 1981 ; ondes de surface : Schützhold & Unruh 2002).

- Eau peu profonde (k·h ≪ 1) : c = √(g·h). Nombre de Froude Fr = v/c. **Horizon** là où la composante normale de
  v égale c.
- Ressaut hydraulique circulaire : film mince rapide (Fr > 1) à l'intérieur, eau lente et épaisse (Fr < 1) à
  l'extérieur ; les ondes extérieures ne peuvent pas entrer : **horizon de trou blanc** (Volovik 2005 ;
  démonstration par le cône de Mach : Jannes et al. 2011). Angle de Mach : sin θ = c/v.
- Tourbillon de vidange idéalisé : v_r = −D/r, v_θ = C/r. Horizon r_H = D/c ; ergorégion r_E = √(C² + D²)/c ;
  amplification (superradiance) d'un mode azimutal m si ω < m·Ω.
- Dispersion réelle : c²(k) = (g/k + γk/ρ)·tanh(kh) ; minimum 23,1 cm/s à λ = 17 mm en eau profonde.
- Température de Hawking analogue : T = ħκ/(2πk_B), κ = |d(v − c)/dx| à l'horizon.

## 3. État de l'art publié [VÉR]

| Référence | Système | Résultat |
|---|---|---|
| Rousseaux et al. 2008 | canal à houle, contre-courant | conversion vers des ondes de « fréquence négative » |
| Weinfurtner et al. 2011 | canal, obstacle profilé | émission de Hawking **stimulée** ; conversion de caractère thermique |
| Jannes et al. 2011 | ressaut circulaire | horizon de trou blanc démontré par l'angle de Mach |
| Euvé et al. 2016 | canal | corrélations de bruit de type Hawking |
| Torres et al. 2017 | tourbillon de vidange, bassin de 6,25 cm de profondeur | superradiance rotationnelle : amplification maximale à 3,70 Hz (≈ 20 % dans le résumé arXiv relu en ligne ; 14 ± 8 % de mémoire dans la version publiée, non revérifié) |
| Torres et al. 2020 | tourbillon | oscillations de modes quasi normaux |
| Cromb et al. 2020 | ondes acoustiques sur disque absorbant tournant | amplification de Zel'dovich |
| Philbin et al. 2008 ; Belgiorno et al. 2010 ; Drori et al. 2019 | impulsions dans des fibres / filaments | horizons optiques ; émission stimulée |
| Steinhauer 2016 ; Muñoz de Nova et al. 2019 ; Kolobov et al. 2021 | condensat de Bose-Einstein | émission **spontanée** et sa température |
| Švančara et al. 2024 | tourbillon quantique géant dans l'hélium superfluide | signatures d'espace-temps courbe en rotation |

Hydrodynamique du ressaut : Watson 1964 ; Bohr, Dimon & Putkaradze 1993 ; Bush & Aristoff 2003 ; Bhagat et al.
2018 (rôle de la tension de surface, **contesté** par Duchesne, Andersen & Bohr 2019). Revue : Barceló, Liberati
& Visser 2011.

## 4. Matériel et coût indicatif

| Niveau | Matériel | Coût |
|---|---|---|
| **N1** | évier, plaque lisse horizontale (verre, assiette plate), robinet à jet laminaire, verre doseur + chronomètre (débit), aiguille ou cure-dent, smartphone (ralenti 240 images/s), règle ; pour le tourbillon : bac transparent percé, paillettes flottantes | 0–30 € |
| **N2** | canal à surface libre ou bac de 1–2 m, pompe de recirculation, obstacle profilé, batteur à ondes (haut-parleur + plaque), nappe laser classe 2 ou éclairage rasant, caméra rapide, logiciel de vélocimétrie par images | 1–5 k€ |
| **N3** | condensat, fibre microstructurée et laser femtoseconde, hélium superfluide | laboratoire |

## 5. Protocole pas à pas

### N1-a — Ressaut circulaire = horizon de trou blanc
1. Régler un jet laminaire tombant de 5–10 cm sur la plaque nivelée. Mesurer le débit Q (volume en 10 s).
2. Mesurer le rayon du ressaut R_j pour 5 débits. Tracer log R_j en fonction de log Q ; comparer aux lois
   R ∝ Q^(5/8) (Bohr) et R ∝ Q^(3/4) (Bhagat).
3. Planter l'aiguille dans le film à r = 1, 2, 3 cm : photographier le sillage en V. Mesurer le demi-angle θ.
   En déduire v/c = 1/sin θ en chaque point.
4. Déplacer l'aiguille vers le ressaut : le V s'ouvre (θ → 90°) puis disparaît au-delà.
5. Toucher la surface **à l'extérieur** avec une pointe vibrante (brosse à dents électrique) : les rides
   n'entrent jamais dans le disque intérieur. Faire l'inverse à l'intérieur : elles sont toutes emportées dehors.

### N1-b — Tourbillon de vidange
1. Bac rempli à h = 3–6 cm, vidange centrale, alimentation tangentielle douce pour maintenir le niveau.
2. Filmer des paillettes : v_θ(r) et v_r(r) ; ajuster C et D.
3. Calculer r_E et r_H ; constater que r_H tombe **dans** l'orifice (pas d'horizon accessible) alors que
   l'ergorégion s'étend sur ~1–2 cm.
4. Envoyer des ondes planes (règle vibrante) : observer la déformation en spirale des fronts d'onde.

### N2 — Canal et bassin
1. Canal + obstacle : cartographier h(x) et v(x) ; localiser Fr = 1.
2. Envoyer des ondes longues à contre-courant : mesurer leur blocage et leur conversion en ondes courtes
   (analyse de Fourier espace-temps).
3. Bassin à tourbillon : mesurer les coefficients de réflexion par mode m en fonction de la fréquence ;
   chercher un coefficient > 1 pour m > 0 (co-rotatif) et < 1 pour m < 0.

## 6. Signal attendu et budget de bruit (calculé)

Ressaut : pour Q = 10–100 mL/s, R_j attendu entre 2–9 cm (loi capillaire) et 7–31 cm (loi gravitaire) — la
mesure tranche ; en pratique quelques centimètres dans un évier. Film à Q = 30 mL/s (jet Ø 6 mm, 1,06 m/s) :
épaisseur 0,15–0,45 mm, Fr ≈ 16–28 ; extérieur (3 mm d'eau) : Fr ≈ 0,2.
Angle de Mach attendu (c_min = 23 cm/s) : 13° pour 1,0 m/s ; 23° pour 0,6 m/s ; 35° pour 0,4 m/s ; 67° pour
0,25 m/s. Incertitude de lecture sur photo : ± 2° → v/c à ± 10 %.

Tourbillon (h = 5 cm, C = 1,5 × 10⁻² m²/s, D = 10⁻³ m²/s) : c = 0,70 m/s ; r_H = 1,4 mm ; r_E = 21,5 mm ;
amplification possible pour f ≲ 6 Hz (m = 1), 12 Hz (m = 2) — critère indicatif. Amplitude d'effet attendue :
≈ 10–20 % au mieux → nécessite la mesure N2 (rapport signal/bruit insuffisant à l'œil).

Limite essentielle : à 3,7 Hz dans 6,25 cm d'eau, λ = 11,6 cm et k·h = 3,4 ; ce n'est **pas** le régime d'eau
peu profonde. Les ondes sont dispersives, l'horizon dépend de la longueur d'onde.

Température de Hawking analogue : 1,2 × 10⁻¹¹ K pour κ = 10 s⁻¹, dans de l'eau à 293 K (rapport 4 × 10⁻¹⁴) :
**l'émission spontanée est inobservable dans l'eau** ; seule la conversion stimulée d'ondes classiques l'est.
Condensat : 0,35 nK pour κ ≈ 290 s⁻¹. Vrai trou noir de 4,4 × 10¹² kg (masse retenue) : 2,8 × 10¹⁰ K
(kT ≈ 2,4 MeV) ; d'une masse solaire : 6 × 10⁻⁸ K.

## 7. Durée

N1 : une après-midi. N2 : 3 à 5 séances. N3 : années.

## 8. Analyse des données

Lois d'échelle par régression log-log avec incertitudes ; carte de Fr(r) ; pour N2, décomposition en modes
azimutaux et spectres (ω, k) ; coefficient de réflexion par mode avec barres d'erreur ; contrôle sans rotation
(D seul) : aucune amplification attendue.

## 9. Sécurité

Eau et électricité : caméra et éclairage hors d'éclaboussures, pompe basse tension ou protégée par disjoncteur
différentiel 30 mA. Verre : bords rodés. Laser : classe 2 au plus (N1/N2).

## 10. Ce que cela prouve — et ne prouve PAS

**Prouve** : qu'un écoulement peut présenter, pour ses ondes, une frontière à sens unique et une zone
d'entraînement forcé ; que la conversion de modes et l'amplification par rotation existent ; que ces phénomènes
sont **cinématiques** et universels.

**Ne prouve pas** : quoi que ce soit sur la gravitation elle-même. L'écoulement n'obéit pas aux équations
d'Einstein ; il n'y a ni singularité, ni dilatation du temps, ni courbe temporelle fermée ; l'« horizon » dépend
de la longueur d'onde (dispersion) ; l'eau ne s'évapore pas par effet Hawking. Un évier n'est pas un trou noir
de Kerr, et un analogue n'est pas une réduction d'échelle d'une machine.

## 11. Lien avec la C204 [DÉD]

- Le schéma DOC-009 dessine trois « horizons des événements » emboîtés (temps négatif, nul, positif) : cette
  nomenclature n'existe pas en relativité générale (dossier §5.5). Une métrique de Kerr-Newman possède deux
  horizons (externe, interne) et une ergosphère ; l'analogue hydraulique permet de **voir** ce qu'est un horizon
  et de constater qu'il ne « produit » pas de champ de temps.
- Ordres de grandeur réels pour 4,4 × 10¹² kg (masse retenue par singularité) : rayon de l'horizon
  ≈ 6,5 × 10⁻¹⁵ m ; l'ergorégion est de la même taille. À l'échelle d'un véhicule (mètres), le champ est
  newtonien à 10⁻¹⁴ près (voir EXP-08, EXP-09).

## 12. Confiance et limites

Phénoménologie N1 (ressaut, cône de Mach) : confiance **élevée** (reproduit dans la littérature). Lois d'échelle
du rayon : **moyenne** (désaccord publié sur le mécanisme). Superradiance en N2 : **moyenne à faible** (effet de
10–20 %, mesure délicate). Modèle de tourbillon : idéalisé.

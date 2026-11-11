# Fiche F4 — Refroidissement et « évacuation des rayons X »

Repères : DOC-008 r.8 (enveloppe), r.9 (pompe), r.10 (réservoirs) ; DOC-009 r.5 (« X-ray venting cone »).
Calculs : `calculs/c01_hawking.py`, `calculs/c05_refroidissement_rayonnement.py` →
`resultats/c05_refroidissement.json`, `c05_debits.csv`, `c05_radiateurs.csv`, `c05_doses.csv`.

## 1. Ce que dit la source

**[DOC texte]** « Cooling and x-ray venting system » ; « it vents X-rays and Gamma radiation out of the rear. As
long as you stay away from that, you should be okay » ; « creating clever ways to vent x-rays » ; l'unité
« gets quite hot », 100 à 120 °F autour d'elle ; « 300–500 megawatts ».
**[DOC]** DOC-008 : une pompe, deux réservoirs cylindriques, une enveloppe par carter. DOC-009 : un cône en
tirets partant du centre.

## 2. Nature réelle du rayonnement d'un micro-trou noir de cette puissance

Résultats de `c01_hawking.py` (lecture A : 400 MW au total, M = 4,38×10¹² kg, kT = 2,41 MeV) :

| Composante | Part de la puissance | Pour 400 MW | Énergie typique | Devenir |
|---|---|---|---|---|
| Neutrinos (3 saveurs, ν et ν̄) | 55,0 % | 220 MW | pic à 4,0 kT ≈ 10 MeV | traversent tout ; ni chaleur ni dose |
| Électrons et positons | 36,6 % | 147 MW | pic à 4,0 kT ≈ 10 MeV | gerbes électromagnétiques dans le carter |
| Photons | 7,5 % | 30 MW | pic à 5,7 kT ≈ 14 MeV ; médiane de puissance 15 MeV | gerbes ; photoneutrons |
| Gravitons | 0,9 % | 3,4 MW | ~9 kT | s'échappent |

- **[DÉD]** Fraction de la puissance des photons émise sous 100 keV : < 10⁻⁹ ; sous 1 MeV : 2×10⁻⁶ ; sous
  10 MeV : 10 %. Ce sont des **gamma de 5 à 70 MeV** selon la lecture retenue (kT de 2 à 12,5 MeV), pas des
  rayons X. Confiance : élevée.
- **[DÉD]** Un trou noir dont le rayonnement serait réellement dans le domaine X (kT = 10 keV) pèserait
  1,06×10¹⁵ kg et n'émettrait que **4,4 kW** au total. « Rayons X » et « 300–500 MW » sont incompatibles d'un
  facteur 10⁵ en puissance.
- Les rayons X ne peuvent apparaître que comme **produits secondaires** (rayonnement de freinage,
  annihilation à 511 keV) des gerbes dans la matière du carter.

## 3. Charge thermique et débit de caloporteur

Charge déposée localement = γ + e± = 44,2 % de la puissance totale (le reste part en neutrinos et gravitons).

| Cas | Charge thermique | Eau, ΔT = 50 K | Eau vaporisée | Pompe (Δp = 10 bar, η = 0,75) |
|---|---|---|---|---|
| Minimum : 1 singularité de 300 MW | 133 MW | 633 kg/s | 51 kg/s | 0,85 MW |
| Référence : 1 singularité de 400 MW | 177 MW | 844 kg/s | 68 kg/s | 1,1 MW |
| Référence ×2 : 2 singularités de 400 MW | 353 MW | 1 690 kg/s | 136 kg/s | 2,3 MW |
| Énoncé haut : 2 × 500 MW intégralement déposés | 1 000 MW | 4 780 kg/s | 386 kg/s | 6,4 MW |

Équations : ṁ = Q/(c_p ΔT + L) ; P_pompe = (ṁ/ρ) Δp/η. Hypothèses **[HYP]** : Δp = 10 bar, canalisation de
5 cm. Conséquences **[DÉD]** (confiance élevée) :

- vitesse de l'eau dans un tuyau de 5 cm : 430 m/s (réf.) à 2 500 m/s (haut) — impossible ;
- deux réservoirs de 0,25 L, à l'échelle du schéma (Équipes E et I), vaporisés en **1,3 à 9,7 ms** ; avec
  l'ancienne hypothèse généreuse de 2 × 15 L **[HYP]**, qui occuperaient 86 % du volume utile : 0,08 à 0,44 s ;
- en circuit ouvert sur 6 h : 1 500 t (réf.) à 8 300 t d'eau vaporisée ;
- en circuit fermé, un radiateur : 3 500 m² à 1 000 K, 690 m² à 1 500 K, 43 m² à 3 000 K (réf. 177 MW),
  contre 1,07 m² de surface de coffre. Pour rayonner seul la charge, le coffre devrait être à **7 000–11 600 K**.

## 4. Flux pariétal et densité de puissance

| Grandeur | Valeur C204 | Référence réelle | Écart |
|---|---|---|---|
| Flux sur un carter de 4,0 cm de rayon (177 MW) | 8,8 GW/m² | flux critique record en eau sous-refroidie : 276 MW/m² (Mudawar & Bowers 1999) | × 32 |
| idem | 8,8 GW/m² | col de tuyère SSME : ~163 MW/m² ; divertor ITER : 10–20 MW/m² | × 54 ; × 440–880 |
| idem | 8,8 GW/m² | photosphère solaire : 63 MW/m² | × 140 |
| Densité de puissance du coffre entier (0,063 m³) | 2,1 à 15,9 MW/L | cœur du réacteur HFIR : 1,7 MW/L en moyenne (cœur seul ; ses circuits occupent un bâtiment) | × 1,2 à 9,3 |
| Absorbeur de tungstène de 10 longueurs de radiation (rayon 3,5 cm, 3,5 kg) | 9,8×10¹¹ W/m³ | — | fond en **13 ms** sans refroidissement |

Les γ et e± de 10–50 MeV ne déposent pas leur énergie en surface mais en volume, sur ~10 longueurs de radiation
(3,5 cm de tungstène, 5,6 cm de plomb, 3,6 m d'eau ; PDG). Le problème n'est donc même pas un problème
d'échange pariétal : c'est un volume de quelques décilitres recevant 10¹² W/m³.

**Test de cohérence sur la température revendiquée** **[DÉD]** : un coffre de 1,07 m² dont la surface est à
38–49 °C dans une ambiance à 25 °C évacue, par convection naturelle et rayonnement, **0,15 à 0,29 kW**
(0,25 à 0,5 kW avec l'ancienne enveloppe de 1,8 m²). Chauffer un habitacle de 15 à 25 K demande 1 à 2,5 kW
(UA = 60–100 W/K **[HYP]**). La température décrite par la source est celle d'un appareil de **quelques
centaines de watts à un kilowatt** — un petit radiateur électrique —, soit environ 6 ordres de grandeur sous les
300–500 MW annoncés. Confiance : élevée.

## 5. Blindage et débits de dose

Données : NIST (μ/ρ, μ_en/ρ), PDG (longueurs de radiation), NCRP 151 (couches de déci-transmission), CIPR 103.

| Grandeur | Équation | Valeur | Confiance |
|---|---|---|---|
| Débit de dose γ à 1 m, sans blindage (1 singularité, 400 MW) | Ḋ = P_γ/(4πd²) · μ_en/ρ (eau, 20 MeV : 0,0138 cm²/g) | **3 300 Gy/s** ; dose létale (DL50 : 2,5–5 Gy) en 0,8–1,5 ms | moyenne |
| idem à 3 m | ∝ 1/d² | 370 Gy/s | moyenne |
| Dose totale γ + e± interceptée par un corps à 1 m | calorimétrie (0,7 m², 70 kg) | 1,4×10⁵ Gy/s, soit ~10 MW absorbés par le corps | moyenne |
| Deux singularités | × 2 | 6 600 Gy/s (γ) à 1 m ; 740 Gy/s à 3 m | moyenne |
| Atténuation pour 1 mSv par trajet de 6 h (limite annuelle du public) | Ḋ·t/limite | 7×10¹⁰, soit 10,9 couches de déci-transmission | moyenne |
| Épaisseur de plomb, couche de déci-transmission en faisceau large | n × 5,7 cm | **62 cm** en toutes directions : sphère de **14 t** (ou 4,9 m de béton) | moyenne |
| Épaisseur de plomb, faisceau étroit | n × ln 10/(μρ) | 39 cm (3,8 t) à 15 MeV, énergie médiane ; 52 cm (8,6 t) à 4 MeV, minimum d'atténuation. Fourchette retenue : **40 à 60 cm, 4 à 14 t** | moyenne |
| Pour 20 mSv (limite annuelle moyenne des travailleurs) | idem | 34 à 54 cm de plomb, 2,7 à 9,5 t | moyenne |
| Blindage logeable dans un coffre de 0,26 m de profondeur | épaisseur disponible entre le logement (r = 4,0 cm) et la paroi | 9 cm si le logement était centré : atténuation 38, il reste **87 Gy/s** à 1 m (sphère de 101 kg) ; 4,5 cm vers la face la plus proche avec l'entraxe de DOC-007 : reste 550 Gy/s ; 7 cm verticalement : 196 Gy/s ; 0,6 cm entre les deux logements. Avec l'ancienne enveloppe : 13 cm, 17 Gy/s | moyenne |
| Neutrinos (220 MW) | σ ~10⁻⁴¹ cm² **[HYP]** | ~10⁻¹¹ Gy/s : négligeable | faible |

Compléments **[VÉR]** : au-delà de 6 à 8 MeV les photons arrachent des neutrons au plomb et au tungstène
(seuils (γ,n) : ²⁰⁷Pb 6,74 MeV, ²⁰⁸Pb 7,37 MeV, ¹⁸³W 6,19 MeV ; AIEA) : il faut ajouter un blindage neutronique
hydrogéné et l'unité devient radioactive. La couche de déci-transmission de 5,7 cm est tabulée pour 4–20 MV ;
nous l'extrapolons à des spectres plus durs (limite : le minimum d'atténuation du plomb, vers 4 MeV, gouverne la
queue des gerbes ; valeur en faisceau étroit : 4,8 cm). Les e± convertis en gerbes multiplient le terme source
par ~5, soit moins d'une couche supplémentaire.

## 6. Un rayonnement de Hawking peut-il être collimaté en « cône » ?

- **[VÉR]** L'émission d'un trou de Schwarzschild est isotrope. Celle d'un trou de Kerr est modulée en latitude
  (les neutrinos partent préférentiellement vers un hémisphère, les antineutrinos vers l'autre : Leahy & Unruh
  1979), mais reste répartie sur toute la sphère. Il n'existe pas de « jet ».
- **[DÉD]** Collimater des γ, c'est absorber tout ce qui n'est pas dans le cône. Fraction géométrique d'une
  émission isotrope : 0,8 % (demi-angle 10°), **6,7 %** (30°), 14,6 % (45°). Le collimateur reçoit donc 85 à 99 %
  de la puissance : le cône n'allège en rien le refroidissement.
- **[VÉR]** Aucune optique ne réfléchit ni ne réfracte des photons de 10 MeV. Les neutrinos (55 %) sont
  indéviables. Seuls les e± (37 %) peuvent être guidés : rayon de giration de 40 MeV sous 10 T = 1,3 cm.
- **[DÉD]** Dans l'axe d'un tel cône, le faisceau γ non atténué délivrerait encore ~980 Gy/h à 100 m et
  ~1,7 Gy/h à 1 km (longueur d'atténuation dans l'air ≈ 510 m **[HYP]**). « Rester à l'écart de l'arrière »
  ne protège personne.

## 7. Technologie réelle et classement

| Élément | Statut | Constructible aujourd'hui ? |
|---|---|---|
| Boucle d'eau, micro-pompe, deux réservoirs de 0,25 L, chemise de refroidissement | Démontré | **Oui**, pour 0,1 à quelques kW dans ce volume (jusqu'à ~100 kW avec un échangeur extérieur) |
| Évacuer 130–1 000 MW d'un coffre de 0,063 m³ | **Contredit** (environ 6 décades au-dessus de ce que montre la température revendiquée ; flux 32 × le record) | **Non** |
| Rayons X comme émission principale | **Contredit** (γ de 5–70 MeV, e±, neutrinos) | — |
| Cône d'évacuation | **Contredit** (isotropie ; collimater = absorber) | **Non** |
| Blindage biologique dans 227 kg | **Contredit** (4 à 14 t requises) | **Non** |

Pour mémoire : la pompe la plus puissante par unité de masse jamais construite, la turbopompe à hydrogène du
moteur SSME, développe 53,7 MW pour 352 kg — plus que la masse totale de l'unité, et elle est entraînée par une
turbine à gaz, pas par une batterie.

## 8. Limites

Calcul de dose au premier ordre (photons primaires, pas de transport Monte-Carlo, pas de facteur de
qualité) : incertitude d'un facteur ~3 sur les doses, sans effet sur des écarts de 9 à 11 décades.
Géométrie du coffre : cotes de l'Équipe A (**[DÉD]**, L = 0,85 ± 0,2 m, confiance faible) ; volume des réservoirs :
échelle du schéma (Équipes E et I). Une simulation de gerbe (Équipe D) pourrait affiner
la répartition du dépôt d'énergie.

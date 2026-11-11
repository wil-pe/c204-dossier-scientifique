# EXP-01 — Dilatation gravitationnelle et cinématique du temps avec des horloges réelles

| | |
|---|---|
| **Niveaux** | N1 (caractériser un oscillateur : résultat nul attendu et instructif) · N2 (séjour en altitude avec césiums) · N3 (horloges optiques, centimètre/millimètre) |
| **Sous-système C204 lié** | « horloges principales (4 au césium) » ; affirmation « ≈ 10 ans par heure » ; intitulé *gravity distortion time displacement* |
| **Statut physique** | **Démontré** (dilatation gravitationnelle et cinématique du temps). Dilatation du temps ≠ voyage dans le passé. |
| **Calculateur** | `calculs/calc01_dilatation_horloges.py` → `calculs/resultats/calc01_dilatation_horloges.txt`, `calculs/figures/calc01_allan_vs_signal.png` |

## 1. Objectif

Mesurer (N2/N3) ou, à défaut, montrer pourquoi on ne peut pas mesurer (N1) le fait qu'une horloge placée plus
haut avance plus vite qu'une horloge identique restée plus bas, et qu'une horloge en mouvement retarde.
Chiffrer la durée d'intégration nécessaire en fonction de la stabilité de l'horloge.

## 2. Principe et équations

Champ faible, vitesses lentes, par rapport à une horloge de référence [VÉR] :

- décalage gravitationnel : Δf/f = ΔΦ/c² ≈ g·Δh/c² = **1,091 × 10⁻¹⁶ par mètre** (g = 9,806 65 m/s²) ;
- décalage cinématique : Δf/f = −v²/(2c²) ;
- temps accumulé : Δt = (Δf/f)·T.

Stabilité d'une horloge : écart-type d'Allan σ_y(τ). Modèle utilisé (indicatif) :
σ_y²(τ) = (a/√τ)² + plancher² + (D·τ/√2)² (bruit blanc de fréquence, scintillation, dérive).
Deux horloges identiques comparées : bruit √2·σ_y(τ). Critère de détection à 3σ : √2·σ_y(τ) ≤ (g·Δh/c²)/3.
Variante « aller-retour » (horloge emmenée T secondes en altitude) : signal (g·Δh/c²)·T contre bruit de temps
≈ √2·√[(a·√T)² + (plancher·T)²].

## 3. État de l'art publié [VÉR]

| Expérience | Ce qui a été fait | Résultat |
|---|---|---|
| Pound & Rebka 1960 | décalage de photons gamma sur 22,5 m (effet Mössbauer) | 2gh/c² = 4,9 × 10⁻¹⁵ observé. *Non reproductible ici : exige une source radioactive (exclu par nos règles).* |
| Hafele & Keating 1972 | 4 horloges à césium en avion de ligne autour du monde | est : −59 ± 10 ns (prédit −40 ± 23) ; ouest : +273 ± 7 ns (prédit +275 ± 21) |
| Briatore & Leschiutta 1977 | échelles de temps atomiques, Turin ↔ Plateau Rosa (≈ 3250 m de dénivelé) | compatible avec g·Δh/c² ≈ 30,6 ns/jour (valeur calculée par nous ; chiffres publiés à relire dans l'article) |
| Vessot et al. 1980 (Gravity Probe A) | maser à hydrogène en fusée jusqu'à ≈ 10 000 km | accord à 7 × 10⁻⁵ près |
| Van Baak 2005 (« Project GREAT », lettre *Physics Today* 2007) | 3 césiums commerciaux en monospace, 5400 ft (≈ 1650 m) sur le mont Rainier, 2 jours | ≈ 23 ns observés pour ≈ 22 ns prédits (page du projet relue en ligne le 10/11/2026) |
| Chou et al. 2010 | deux horloges optiques Al⁺, l'une relevée de 33 cm | décalage de quelques 10⁻¹⁷ résolu |
| Grotti et al. 2018 ; Takamoto et al. 2020 | horloges optiques à réseau transportables (tunnel alpin ; tour Tokyo Skytree, 450 m) | géodésie relativiste ; test de la relativité générale au niveau 10⁻⁵ |
| McGrew et al. 2018 | horloges Yb au niveau 10⁻¹⁸ | sensibilité géodésique sous le centimètre |
| Bothwell et al. 2022 ; Zheng et al. 2022 | gradient de fréquence dans un échantillon d'atomes millimétrique / centimétrique | incertitude 7,6 × 10⁻²¹ (Bothwell, résumé relu en ligne) |
| Delva et al. 2018 ; Herrmann et al. 2018 | satellites Galileo en orbite excentrique | test du décalage gravitationnel au niveau de quelques 10⁻⁵ |

Usage métrologique courant : les étalons d'un laboratoire situé à 1650 m d'altitude avancent de 1,8 × 10⁻¹³
(15,6 ns/jour) par rapport au géoïde ; cette correction est appliquée en routine (ordre de grandeur calculé par
nous ; fait de pratique métrologique, non revérifié en ligne).

## 4. Matériel et coût indicatif

| Niveau | Matériel | Coût |
|---|---|---|
| **N1** | oscillateur discipliné GPS (GPSDO) d'occasion ; étalon à rubidium d'occasion ; compteur d'intervalles de temps de résolution < 100 ps (ou carte d'horodatage) ; enregistreur ; sonde de température et de pression | ≈ 450–500 € |
| **N2** | 2 à 4 étalons à césium à jet (prêt d'un laboratoire temps-fréquence), 1 GPSDO, compteurs, alimentation autonome 48 h (batteries + convertisseur), véhicule, site ≥ 1300 m plus haut accessible par la route | matériel de laboratoire (plusieurs dizaines de k€ par césium) ; logistique ≈ 300 € |
| **N3** | deux horloges optiques (dont une transportable) reliées par fibre stabilisée | laboratoire de métrologie |

Remarque : le césium 133 des étalons à jet est un isotope **stable** ; ces horloges ne contiennent aucune
source radioactive.

## 5. Protocole pas à pas

### N1 — « pourquoi on ne le voit pas » (résultat nul annoncé à l'avance)
1. Laisser chauffer rubidium et GPSDO 48 h. Mesurer chaque seconde l'écart de phase rubidium − GPSDO.
2. Calculer σ_y(τ) de 1 s à 10⁵ s (méthode des recouvrements). Identifier les trois régimes (pente −½, plancher, dérive).
3. Coiffer le rubidium d'une boîte isolante (polystyrène) pour que sa propre dissipation l'élève d'environ 5 K
   — sans dépasser la température de socle admise par sa notice, et sans élément chauffant ajouté — puis le
   retourner de 180° dans le champ terrestre et noter la pression : mesurer les trois coefficients d'environnement.
4. Comparer le plancher obtenu (attendu : 10⁻¹² à 3 × 10⁻¹³) au signal de 1000 m (1,09 × 10⁻¹³). Conclure.
5. Variante : emporter malgré tout le rubidium 1000 m plus haut pendant 24 h et montrer que l'« effet »
   observé change de signe ou d'amplitude avec la température et l'orientation → artefact.

### N2 — séjour en altitude (schéma de Van Baak)
1. Au laboratoire, comparer pendant ≥ 3 jours N horloges « voyageuses » (N ≥ 3) à M « sédentaires » (M ≥ 1).
   Ajuster pour chaque paire une droite de phase (chaque horloge a son écart de fréquence constant propre).
2. Charger les voyageuses **sans jamais couper l'alimentation**. Enregistrer température, pression, tension.
3. Monter de Δh (lu sur une carte, ± 5 m), stationner T ≥ 40 h. Redescendre.
4. Reprendre la comparaison ≥ 3 jours.
5. Le saut entre les droites de phase « avant » et « après », extrapolées au milieu du voyage, est le temps gagné.
6. **Aveugle** : l'analyste ajuste les sauts sans connaître Δh ni T ; la prédiction g·Δh·T/c² est calculée par un tiers.
7. **Voyage témoin** : même durée, même véhicule, altitude constante → saut attendu nul (teste vibrations,
   température, champ magnétique, alimentation).

### N3
Comparaison optique différentielle ; variation contrôlée de la hauteur (table élévatrice, cm) ; lecture directe de la
pente 1,09 × 10⁻¹⁸ par cm.

## 6. Signal attendu et budget de bruit (calculé)

Signal :

| Δh | Δf/f | écart en 1 jour |
|---|---|---|
| 1 mm | 1,1 × 10⁻¹⁹ | 9 × 10⁻⁶ ns |
| 1 cm | 1,1 × 10⁻¹⁸ | 9 × 10⁻⁵ ns |
| 1 m | 1,1 × 10⁻¹⁶ | 0,009 ns |
| 100 m | 1,1 × 10⁻¹⁴ | 0,94 ns |
| 1000 m | 1,1 × 10⁻¹³ | 9,4 ns |
| 3000 m | 3,3 × 10⁻¹³ | 28 ns |

Durée d'intégration pour une détection à 3σ entre deux horloges identiques comparées en continu :

| Horloge (modèle indicatif) | 1 cm | 1 m | 100 m | 1000 m | 3000 m |
|---|---|---|---|---|---|
| CSAC, OCXO, rubidium d'occasion | impossible | impossible | impossible | impossible | impossible |
| Césium à jet, tube standard | impossible | impossible | impossible | impossible | 2,5 j |
| Césium à jet, haute performance | impossible | impossible | impossible | 36 h | 3,5 h |
| Maser à hydrogène | impossible | impossible | 30 min | 15 s | 2 s |
| Horloge optique à réseau | (limite du modèle) | 15 s | 1 s | 1 s | 1 s |

Variante aller-retour, 1340 m pendant 42 h (signal 22,1 ns) : rubidium S/B ≈ 0,3 ; césium standard S/B ≈ 1,2 ;
césium haute performance S/B ≈ 4,3 par horloge (÷ √N avec N horloges : ≈ 7 avec trois).

Effets d'environnement pour un rubidium monté de 1500 m (signal 1,6 × 10⁻¹³) — coefficients indicatifs de fiches
techniques, à mesurer sur l'exemplaire : pression ≈ 1,7 × 10⁻¹¹ (100 × le signal) ; température (10 K) ≈ 10⁻¹¹
(60 ×) ; retournement dans le champ terrestre ≈ 10⁻¹⁰ (600 ×) ; dérive sur 2 jours ≈ 3 × 10⁻¹² (20 ×).
Effet cinématique du trajet en voiture : 5 × 10⁻¹⁵ (négligeable). → **l'expérience n'est pas faisable au niveau N1.**

Piège conceptuel : un GPSDO *verrouillé* est asservi au temps GPS, défini au niveau du géoïde ; il ne « voit » pas
son propre décalage d'altitude. C'est l'horloge libre (césium) qui porte le signal. L'exactitude absolue d'un
césium commercial (quelques 10⁻¹³) est du même ordre que le signal : d'où la méthode différentielle avant/après.

## 7. Durée

N1 : une semaine d'enregistrement, deux jours d'analyse. N2 : 8 à 10 jours (3 + 2 + 3 jours, plus le voyage témoin).
N3 : quelques heures de mesure après des mois de mise au point.

## 8. Analyse des données

Phase x(t) → fréquence moyenne y = Δx/τ → σ_y(τ) avec barres d'erreur ; retrait des sauts de phase et des points
aberrants **selon une règle écrite à l'avance** ; ajustement de droites avant/après par moindres carrés pondérés ;
incertitude sur le saut par simulation de bruit (bruit blanc + scintillation, paramètres mesurés à l'étape 1).
Comparer à g·Δh·T/c² + correction cinématique. Rapport final : valeur, incertitude, test du voyage témoin.

## 9. Sécurité

Batteries (ventilation, fusibles, arrimage) ; charges lourdes (≈ 30 kg par étalon) ; conduite en montagne ;
essai thermique sans élément chauffant ajouté (isolation seule, sous surveillance). Aucune haute tension
accessible (ne pas ouvrir les étalons). Risque radiologique : aucun en pratique. Précision : le césium 133 est
stable ; en revanche un étalon à rubidium contient du ⁸⁷Rb, isotope naturel (27,8 % du rubidium) très faiblement
radioactif (période ≈ 5 × 10¹⁰ ans, ≈ 3 Bq par milligramme de ⁸⁷Rb) : activité négligeable, scellée dans
l'appareil du commerce et hors réglementation, mais la règle « aucune source radioactive » doit s'entendre
« aucune source ajoutée ni manipulée » et non au sens littéral.

## 10. Ce que cela prouve — et ne prouve PAS

**Prouve** : deux horloges identiques séparées en altitude accumulent un écart réel, cumulatif, égal à g·Δh·T/c²
(à ± 20–30 % avec des césiums, à 10⁻⁵ près avec des horloges optiques) ; une horloge en mouvement retarde.

**Ne prouve pas** : qu'on puisse inverser l'ordre des événements ou revenir dans le passé. La dilatation du
temps ne fait que ralentir une horloge par rapport à une autre ; les deux avancent toujours vers le futur.
Reproduire cet effet ne valide en rien une « machine ».

## 11. Lien avec la C204 [DÉD]

- Masse retenue par le programme pour 300–500 MW de rayonnement de Hawking (dossier v1.2, erratum E2) :
  **3,9–5,1 × 10¹² kg par singularité**, soit 7,8 × 10¹² à 1,0 × 10¹³ kg pour les deux. Décalage gravitationnel
  créé à 1 m, GM/(rc²) : **2,9–3,8 × 10⁻¹⁵** pour une singularité (27–35 m de dénivelé terrestre ; 91–120 ns par
  an) ; **5,8–7,6 × 10⁻¹⁵** pour la paire (53–69 m). Pour les 227 kg revendiqués : 1,7 × 10⁻²⁵. (Ancienne valeur
  du dossier v1, 10¹² kg : 7,4 × 10⁻¹⁶.)
- Le taux revendiqué « 10 ans par heure » correspond à dt_ext/dτ ≈ 87 660, soit **1,2 à 3,0 × 10¹⁹ fois** l'effet
  gravitationnel des masses retenues à 1 m.
- En relativité générale, un facteur 87 660 pour un observateur statique exige 1 − r_s/r = (1/87 660)² =
  1,3 × 10⁻¹⁰, c'est-à-dire se tenir à 10⁻¹⁰ rayon de Schwarzschild au-dessus de l'horizon (r_s ≈ 6,5 × 10⁻¹⁵ m
  pour 4,4 × 10¹² kg) ; et l'effet envoie le voyageur vers le **futur** de l'extérieur, jamais vers le passé.
- Quatre horloges au césium ne mesurent que le temps propre écoulé à bord ; elles ne donnent aucun accès à une
  « date extérieure ».

## 12. Confiance et limites

Équations et signal : confiance **élevée**. Modèles de bruit des horloges : **moyenne** (valeurs de type fiche
technique, variables d'un exemplaire à l'autre). Coefficients d'environnement du rubidium : **faible à moyenne**
(ordres de grandeur). Modèle Hafele-Keating du script : simplifié (−44 ns / +293 ns contre −40 / +275 publiés).

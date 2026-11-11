# EXP-02 — Synchronisation d'horloges et transfert de temps : ce que l'on mesure réellement

| | |
|---|---|
| **Niveaux** | N1 (NTP, deux récepteurs GPS, retard d'un câble) · N2 (PTP matériel, White Rabbit, GPS vue commune) · N3 (phase de porteuse, deux voies par satellite, liens optiques fibrés) |
| **Sous-système C204 lié** | « 4 horloges au césium », « 3 calculateurs à vote », notion de « date de destination » |
| **Statut physique** | **Démontré** (techniques de métrologie courante). Aucune ne transmet d'information vers le passé. |
| **Calculateur** | `calculs/calc02_transfert_temps.py` → `resultats/calc02_transfert_temps.txt`, `figures/calc02_transfert_temps.png` |

## 1. Objectif

Comprendre, en le faisant, que « comparer deux horloges distantes » revient toujours à mesurer une **différence de
dates d'événements locaux** augmentée de **retards de propagation** qu'il faut modéliser ; mesurer ces retards ;
chiffrer ce que chaque méthode permet (ou non) de voir des effets relativistes de EXP-01.

## 2. Principe et équations

- **Sens unique (GPS)** : le récepteur date l'arrivée d'un signal émis à une date connue ; t_reçu − t_émis =
  géométrie/c + ionosphère + troposphère + câbles + corrections relativistes. Le 1PPS délivré est une
  *estimation* du temps GPS.
- **Vue commune** [VÉR, Allan & Weiss 1980] : deux stations A et B observent le même satellite au même instant ;
  (A − sat) − (B − sat) = A − B : l'horloge du satellite s'élimine, les erreurs de trajet communes aussi.
- **Deux voies** (NTP, PTP, White Rabbit, satellite) : quatre horodatages t1 (départ A), t2 (arrivée B), t3
  (départ B), t4 (arrivée A). Décalage estimé θ = [(t2 − t1) − (t4 − t3)]/2 ; délai δ = [(t4 − t1) − (t3 − t2)]/2.
  **L'erreur vaut (d_AB − d_BA)/2** : l'asymétrie des trajets est inobservable de l'intérieur du protocole.
- **Relativité dans le GPS** [VÉR, Ashby 2003 ; re-dérivé] : horloge satellite − horloge au sol = +4,4647 × 10⁻¹⁰
  = **+38,6 µs/jour** (+45,8 potentiel, −7,2 vitesse) ; terme d'excentricité ±46 ns pour e = 0,02 ; correction de
  Sagnac jusqu'à 137 ns ; un tour d'équateur : 207 ns.
- Conversion bruit de temps → comparaison de fréquence (bruit blanc de phase) : σ_y(τ) ≈ √3·σ_x/τ.

## 3. Matériel et coût indicatif

| Niveau | Matériel | Coût |
|---|---|---|
| **N1** | ordinateur avec client NTP ; 2 modules GPS « temps » à sortie 1PPS ; 10 m de câble coaxial ; compteur d'intervalles de temps (ou oscilloscope ≥ 100 MHz) | 150–400 € |
| **N2** | 2 cartes réseau à horodatage matériel + logiciel PTP libre ; commutateur et deux nœuds White Rabbit ; 2 récepteurs GPS étalonnés + horloges locales (rubidium) dans deux bâtiments | 300 € (PTP) à ≥ 5 k€ (White Rabbit) |
| **N3** | récepteurs géodésiques, station deux voies, lien fibré stabilisé | laboratoire de métrologie |

## 4. Protocole pas à pas

### N1-a — NTP
1. Interroger 4 serveurs pendant 24 h ; enregistrer décalage θ et délai δ.
2. Tracer θ en fonction de δ : le nuage en « coin » montre que les échanges lents sont biaisés (asymétrie).
3. Passer du Wi-Fi au câble, puis ajouter un téléchargement montant : observer le biais de θ changer de plusieurs
   millisecondes **sans que l'horloge ait bougé**.

### N1-b — Mesurer un câble avec deux GPS
1. Deux récepteurs, antennes côte à côte. Mesurer chaque seconde Δ = 1PPS_A − 1PPS_B pendant 10 min (référence).
2. Insérer 10 m de coaxial sur la sortie 1PPS de B (ou sur son antenne). Refaire 10 min.
3. Le déplacement de la moyenne donne le retard : attendu **50,5 ns** pour du RG-58 (5,05 ns/m).
4. Échanger les récepteurs (A ↔ B) pour éliminer leur biais propre.

### N2 — PTP / White Rabbit / vue commune
1. Deux nœuds PTP sur le même commutateur ; comparer leurs 1PPS au compteur : gigue et biais.
2. Ajouter volontairement 20 m de fibre sur un seul sens (à l'aide d'un circulateur ou de deux fibres) : le biais
   attendu est 20 m × 4,9 ns/m ÷ 2 = 49 ns. C'est l'expérience qui « montre » l'asymétrie.
3. White Rabbit : même comparaison ; vérifier le sous-nanoseconde, puis chauffer la bobine de fibre de 10 K et
   observer la compensation en ligne.
4. Vue commune : deux stations, mêmes satellites, mêmes instants ; former la différence ; comparer à un
   transport physique d'horloge entre les deux sites.

## 5. Signal attendu et budget de bruit (calculé)

| Méthode | Exactitude typique | Bruit court terme | σ_y à 1 jour | Niveau |
|---|---|---|---|---|
| NTP via Internet | 5 ms | 2 ms | 4 × 10⁻⁸ | N1 |
| NTP réseau local | 0,2 ms | 50 µs | 1 × 10⁻⁹ | N1 |
| PTP, horodatage matériel | 100 ns | 30 ns | 6 × 10⁻¹³ | N1/N2 |
| GPS sens unique | 20 ns | 8 ns | 1,6 × 10⁻¹³ | N1 |
| GPS vue commune | 5 ns | 3 ns | 6 × 10⁻¹⁴ | N2 |
| GPS phase de porteuse | 1 ns | 0,1 ns | 2 × 10⁻¹⁵ | N2/N3 |
| Deux voies par satellite | 1 ns | 0,5 ns | 1 × 10⁻¹⁴ | N3 |
| White Rabbit (≤ 10 km) | 0,5 ns | 10 ps | 2 × 10⁻¹⁶ | N2/N3 |
| Lien optique fibré | — | — | 10⁻¹⁸ à 10⁻²⁰ | N3 |

(Ordres de grandeur d'usage ; dépendent du matériel et de l'étalonnage — confiance moyenne.)

Simulation illustrative d'échange bidirectionnel : biais = demi-asymétrie dans tous les cas (2,0 ms pour 4 ms
d'asymétrie Internet ; 20 ns pour 40 ns en PTP ; 50 ps pour 100 ps en White Rabbit), quelle que soit la moyenne.

Mesure du câble (N1-b) : bruit de 1PPS ≈ 8 ns par récepteur → sur 600 s, incertitude √2 × 8/√600 = **0,46 ns**
pour un signal de 50,5 ns : rapport signal/bruit ≈ 100.

Repère relativiste : 1000 m de dénivelé = 1,09 × 10⁻¹³ = 9,4 ns/jour. La vue commune GPS ne le résout qu'en
plusieurs jours **et** seulement si les horloges locales tiennent 10⁻¹⁴ (césium, maser).

## 6. Durée

N1 : deux soirées. N2 : deux à trois séances de TP. N3 : campagnes de plusieurs semaines.

## 7. Analyse des données

Histogrammes des différences ; moyenne, écart-type, écart-type d'Allan temporel ; test d'échange des appareils ;
régression θ(δ) pour NTP ; bilan d'incertitude séparant bruit (type A) et retards non étalonnés (type B). Toute
valeur « absolue » doit citer l'étalonnage dont elle dépend.

## 8. Sécurité

Très basse tension uniquement. Antennes GPS : ne pas travailler sur un toit sans protection contre les chutes ni
par temps d'orage. Fibres : sources de classe 1 ; ne jamais regarder l'extrémité d'une fibre active.

## 9. Ce que cela prouve — et ne prouve PAS

**Prouve** : on mesure une différence d'horloges *plus* des retards ; l'asymétrie des trajets crée un biais
invisible ; un mètre de câble vaut ≈ 5 ns ; les corrections relativistes du GPS (38,6 µs/jour) sont
indispensables et fonctionnent.

**Ne prouve pas** : l'existence d'un « temps absolu » lisible à distance, ni la moindre possibilité de signal
rétrograde. Exemple instructif [VÉR] : l'anomalie de ≈ 60 ns des neutrinos « supraluminiques » d'OPERA (2011)
venait d'un connecteur de fibre optique mal enfoncé et d'un oscillateur ; le résultat corrigé (OPERA, JHEP 2012)
est compatible avec c. Un écart de quelques dizaines de nanosecondes est d'abord un problème de câble.

## 10. Lien avec la C204 [DÉD]

- Une horloge embarquée ne fournit que le temps propre. Pour « viser une date », il faudrait connaître le rapport
  dt_ext/dτ : atteindre une date à 1 heure près sur 10 ans exige de maîtriser ce rapport à 3600 s / 3,16 × 10⁸ s
  = **1,1 × 10⁻⁵** près pendant tout le trajet. L'exactitude du césium (10⁻¹³) n'est donc pas le facteur limitant ;
  la grandeur critique serait le « champ », pour lequel aucun capteur n'est décrit.
- Aucun transfert de temps n'est possible vers une « autre ligne d'univers » : toutes les méthodes supposent un
  canal de propagation commun.
- Trois calculateurs à vote : voir EXP-12 (redondance réelle, mais pas un « protocole de Borda »).

## 11. Confiance et limites

Corrections relativistes du GPS : confiance **élevée** (re-dérivées, valeurs classiques retrouvées).
Performances par méthode : **moyenne**. Simulation : illustrative.

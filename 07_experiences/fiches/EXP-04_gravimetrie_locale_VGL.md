# EXP-04 — Cartographie gravimétrique locale : analogue réel de l'« instantané de gravité » du système VGL

| | |
|---|---|
| **Niveaux** | N1 (smartphone, accéléromètre MEMS, pendule) · N2 (gravimètre relatif de terrain, pendule réversible) · N3 (gravimètres absolus, à atomes froids, supraconducteurs) |
| **Sous-système C204 lié** | « capteurs de gravité (système VGL, *variable gravity lock*) » ; repère 11 « Gravity sensor unit » (DOC-008) |
| **Statut physique** | Gravimétrie : **démontrée**. « Reconnaître un lieu » par un instantané de gravité : **non étayé** (aucun système réel ne le fait en un point). |
| **Calculateur** | `calculs/calc04_gravimetrie_VGL.py` → `resultats/calc04_gravimetrie_VGL.txt`, `figures/calc04_gravimetrie.png` |

## 1. Objectif

Mesurer g et ses variations locales avec des moyens croissants ; comparer la résolution réellement atteinte à
celle qu'exigerait l'identification d'un lieu par sa seule gravité ; évaluer ce qu'un tel capteur verrait d'une
masse de type « C204 ».

## 2. Principe et équations [VÉR]

- Pesanteur normale (formule de Somigliana, GRS80) : 9,780 33 m/s² à l'équateur, 9,832 19 aux pôles (écart 5,19 Gal).
- Gradient à l'air libre : ∂g/∂h = −2GM/R³ = **−308,6 µGal/m** (≈ 3 µGal/cm).
- Gradient nord-sud à 45° : 0,81 µGal/m. Plateau de Bouguer : 2πGρ = 112 µGal par mètre de roche (2670 kg/m³).
- Marées : ≈ 280 µGal crête à crête (110 µGal lunaire, 51 µGal solaire, facteur élastique 1,16).
- Masse ponctuelle : Δg = GM/r². Cylindre horizontal (galerie) : Δg = 2πG·Δρ·R²·z/(x² + z²).
- Pendule : T = 2π√(L/g)·(1 + θ₀²/16 + …) ; δg/g = √[(2δT/T)² + (δL/L)²].

Unités : 1 Gal = 10⁻² m/s² ; 1 µGal = 10⁻⁸ m/s² ≈ 10⁻⁹ g.

## 3. État de l'art publié [VÉR]

Gravimètre absolu à chute libre (Niebauer et al. 1995) ; interférométrie atomique (Peters, Chung & Chu 1999 ;
gravimètre quantique transportable sous 10⁻⁹ g : Ménoret et al. 2018) ; gravimètre supraconducteur (Goodkind
1999) ; gravimètre MEMS mesurant les marées, 40 µGal/√Hz (Middlemiss et al. 2016) ; gradiomètre quantique de
terrain détectant un tunnel (Stray et al. 2022) ; application smartphone (Staacks et al. 2018, phyphox) ;
navigation inertielle aidée par gradiométrie (Jekeli 2006, étude théorique).

## 4. Matériel et coût indicatif

| Niveau | Matériel | Coût |
|---|---|---|
| **N1** | smartphone (application gratuite) ; accéléromètre MEMS bas bruit + microcontrôleur ; pendule : fil d'acier 1–2 m, masse dense, barrière optique ; thermomètre | 0 à 150 € |
| **N2** | gravimètre relatif à ressort (prêt d'un laboratoire de géophysique) ; pendule réversible de Kater ; niveau de précision | prêt ; ≈ 100 k€ à l'achat |
| **N3** | gravimètre absolu (coin de cube ou atomes froids), gravimètre supraconducteur | plusieurs centaines de k€ |

## 5. Protocole pas à pas

### N1-a — Smartphone / MEMS
1. **Étalonnage en six positions** (±x, ±y, ±z vers le haut) sur une surface nivelée : biais et facteurs d'échelle.
2. Poser à plat, attendre 10 min (stabilisation thermique), enregistrer 100 s ; noter la température.
3. Répéter au rez-de-chaussée et au dernier étage d'un immeuble haut, puis au pied et au sommet d'un relief
   (≥ 500 m) ; revenir au point de départ (fermeture de boucle, estime la dérive).
4. Dans un ascenseur : intégrer deux fois a(t) − g pour retrouver la hauteur (vérification du facteur d'échelle).
5. Comparer aux prédictions (0,31 mGal/m). Résultat attendu : **non significatif pour un immeuble**, marginal pour 1000 m.

### N1-b — Pendule
1. Longueur L mesurée à ± 0,1 mm (du point de suspension au centre de masse), amplitude ≤ 3°.
2. Chronométrer 100 périodes à la barrière optique ; corriger amplitude, température (dilatation), poussée d'Archimède.
3. g absolu attendu à ± 10⁻³ m/s². Transporter le même pendule (voyage, altitude) pour un essai relatif.

### N2 — Gravimètre relatif
1. Boucle de mesures A-B-A-B (dérive instrumentale) d'étage en étage : gradient vertical ; attendu ≈ 1 mGal par étage.
2. Station fixe 24 h : enregistrer la marée (≈ ± 100 µGal) ; comparer à un modèle de marée.
3. Profil au pas de 1 m au-dessus d'une cave ou d'une galerie connue : anomalie attendue 20–30 µGal.
4. Approcher une voiture à 2 m : 2,5 µGal (à la limite).
5. **Essai de « reconnaissance de lieu »** : cartographier 20 points d'un bâtiment ; un tiers choisit un point ;
   l'opérateur tente de l'identifier à partir de la seule valeur de g (après correction de marée). Compter les succès.

## 6. Signal attendu et budget de bruit (calculé)

| Capteur | Résolution réaliste (100 s) | Équivalent en altitude | Niveau |
|---|---|---|---|
| Smartphone | 2 × 10⁻³ m/s² (200 000 µGal) | 650 m | N1 |
| MEMS bas bruit | 2 × 10⁻⁴ m/s² | 65 m | N1 |
| Pendule simple soigné | 1 × 10⁻³ m/s² | 320 m | N1 |
| Pendule de Kater | 1 × 10⁻⁴ m/s² | 32 m | N2 |
| Gravimètre MEMS de recherche | 40 µGal | 13 cm | N3 |
| Gravimètre relatif de terrain | 5 µGal | 1,6 cm | N2/N3 |
| Gravimètre absolu | 2 µGal | 6,5 mm | N3 |
| Supraconducteur | 0,01 µGal | 0,03 mm | N3 |

(Ordres de grandeur indicatifs.) Le plancher du smartphone ne vient pas du bruit blanc (≈ 150 µg/√Hz, qui se
moyenne) mais de la dérive thermique du biais (0,1–1 mg/K), du facteur d'échelle (≈ 0,5 %) et de l'inclinaison
(1° → 1,5 × 10⁻⁴ g).

Signaux à reconnaître : 1 m d'altitude = 309 µGal ; 1 m vers le nord = 0,8 µGal ; personne à 1 m = 0,5 µGal ;
voiture à 2 m = 2,5 µGal ; galerie Ø 2 m à 3 m de profondeur = 28 µGal ; marée = 280 µGal crête à crête.

**« Reconnaître un lieu »** [DÉD] : un scalaire g résolu à 1 µGal prend ≈ 5 × 10⁶ valeurs distinctes sur Terre
pour 5 × 10¹⁴ m² de surface : chaque valeur correspond en moyenne à ≈ 100 km². Il faudrait en plus un modèle de
marée (280 µGal ≡ 0,9 m d'altitude), des corrections hydrologiques (~10 µGal) et de pression (≈ −0,3 µGal/hPa),
et surtout une **carte de référence préexistante**, de même résolution et de même époque. La navigation réelle
par corrélation de cartes de gravité travaille le long d'une trajectoire, avec des précisions de la centaine de
mètres au kilomètre (ordre de grandeur donné sans source vérifiée : [HYP]).

## 7. Durée

N1 : une journée. N2 : deux à trois jours (dont 24 h de marée). N3 : campagnes.

## 8. Analyse des données

Correction de dérive par fermeture de boucle ; correction de marée (modèle) et de pression ; régression g(h)
et comparaison à 308,6 µGal/m (l'écart renseigne sur les masses du bâtiment : attendu 5–15 %) ; pour l'essai de
reconnaissance : taux de succès contre hasard (1/20), intervalle de confiance binomial.

## 9. Sécurité

Aucune difficulté particulière ; pendule : masse arrimée, zone dégagée ; mesures en hauteur : garde-corps.

## 10. Ce que cela prouve — et ne prouve PAS

**Prouve** : g varie mesurablement avec l'altitude, la latitude, les marées et les masses proches ; les capteurs
accessibles (N1) sont 10⁴ à 10⁵ fois trop peu résolus pour une « empreinte » locale ; les gravimètres de terrain
voient des cavités et des marées.

**Ne prouve pas** : qu'un instantané de gravité permette de « verrouiller » une position, encore moins une
position à une autre époque (la répartition des masses — nappes, bâtiments, marées — a changé) ou sur une
« autre ligne d'univers ».

## 11. Lien avec la C204 [DÉD]

- Si l'unité contenait réellement les masses qu'implique une puissance de Hawking de 300–500 MW — **3,9–5,1 × 10¹²
  kg par singularité** (valeur retenue, dossier v1.2, erratum E2 ; déduite, jamais revendiquée telle quelle) —
  une seule singularité créerait 260–340 m/s² (27–35 g) à 1 m ; elle serait détectable **par un smartphone à
  160–185 m** et **par un gravimètre de terrain à 32–37 km**. Pour la paire (7,8 × 10¹² à 1,0 × 10¹³ kg) :
  53–69 g à 1 m, smartphone à 230–260 m, gravimètre à 46–52 km, poids de 0,8–1,0 × 10¹⁴ N sur le châssis.
  (Ancienne fourchette du dossier v1, 10¹¹–10¹² kg : 26–82 m et 5–16 km.) Aucune anomalie de ce type
  n'accompagne un objet de 227 kg, qui produit 1,5 µGal à 1 m (moins qu'une voiture à 2 m).
- Dynamique impossible : un capteur « VGL » devrait résoudre ~1 µGal (10⁻⁹ g) pour distinguer des lieux tout en
  baignant dans les 1,5–2 g revendiqués et dans les artefacts magnétiques des bobines (EXP-03) : dynamique > 10⁹,
  sur un véhicule à suspension. Aucun gravimètre existant ne s'en approche.
- Le terme *variable gravity lock* n'a pas d'équivalent identifié en géodésie.

## 12. Confiance et limites

Gradients et marées : confiance **élevée**. Résolutions des capteurs : **moyenne** (dépendent du modèle et du soin).
Argument de non-unicité : **élevée** dans son principe, simplifié (scalaire seul ; un tenseur de gradient
améliore la discrimination mais ne supprime ni la dépendance à une carte, ni la variabilité temporelle).

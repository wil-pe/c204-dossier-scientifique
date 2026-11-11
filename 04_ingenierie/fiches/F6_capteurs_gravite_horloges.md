# Fiche F6 — Capteurs de gravité « VGL » et quatre horloges au césium

Repères : DOC-008 r.11 (« gravity sensor unit ») ; texte (« 4 cesium units »).
Calculs : `calculs/c07_capteurs_horloges.py` → `resultats/c07_capteurs_horloges.json`,
`c07_signaux_gravimetriques.csv`, `c07_instruments.csv`.

## 1. Ce que dit la source

**[DOC texte]** Le VGL (*variable gravity lock*) prend avant le départ un « instantané » (« snapshot ») de la
gravité locale, puis le recontrôle « par impulsions » pendant le trajet ; si l'écart est trop grand (un « mur de
briques » ou un « bloc de ciment » apparu), l'unité s'arrête, revient au dernier échantillon correct ou
« décroche ». Analogie donnée : un « radar de gravité ». L'unité doit rester immobile : « any motion with an
acceleration component would throw the gravity measurement … off ». Quatre horloges au césium (C204) ; six,
avec « an optical system to check the oscillation frequency », sur le C206. « Miniaturizing the clocks and
sensors » est cité parmi les principales difficultés.

## 2. État de l'art réel — gravimétrie

| Instrument | Principe | Performance | Masse / puissance | Température |
|---|---|---|---|---|
| Micro-g LaCoste FG5-X | absolu, chute libre + interféromètre laser | exactitude 2 µGal ; 15 µGal/√Hz en site calme | 150 kg (6 caisses) ; ~500 W | 20–30 °C |
| Exail AQG-B | absolu, interférométrie atomique | 50 µGal/√Hz ; stabilité ≤ 2 µGal (1 µGal : Ménoret et al. 2018) | < 140 kg ; 500 W | 0–40 °C |
| GWR iGrav | relatif, sphère supraconductrice | 0,3 µGal/√Hz ; 1 nGal en fréquentiel ; dérive < 0,5 µGal/mois | (cryogénie) | 4–38 °C |
| Scintrex CG-6 | relatif, ressort de quartz | résolution 0,1 µGal ; écart-type < 5 µGal ; plage 8 000 mGal | 5,5 kg ; 5,2 W | −40 à +45 °C |
| MEMS (Middlemiss et al. 2016) | relatif, laboratoire | 40 µGal/√Hz | quelques cm³ | — |
| Gradiomètre aéroporté (FTG, FALCON) | gradient | ~2 E après traitement ; 3,5–10 E/√Hz | — | — |
| Gradiomètre atomique (Stray et al. 2022) | gradient | 20 E ; tunnel de 2 m détecté | laboratoire mobile | — |

(1 µGal = 10⁻⁸ m/s² ≈ 10⁻⁹ g ; 1 E = 10⁻⁹ s⁻².) **[VÉR]** sources constructeur et articles, voir REFERENCES.md.

## 3. Le « verrou de gravité » est-il physiquement sensé ?

### 3.1 Détecter une masse apparue à proximité : oui, au repos

| Objet | Distance | Δg | Gradient | Temps d'intégration pour S/B = 3 (FG5-X / iGrav) |
|---|---|---|---|---|
| Masse d'une tonne | 2 m | 1,7 µGal | 17 E | 12 min / 0,3 s |
| idem | 3 m | 0,74 µGal | 4,9 E | 61 min / 1,5 s |
| Bloc de béton de 1 m³ (2 400 kg) | 2 m | 4,0 µGal | 40 E | 126 s / 0,05 s |
| idem | 3,5 m (bord du « champ » de 10–12 ft) | 1,3 µGal | 7,5 E | 20 min / 0,5 s |
| Mur de 10 t | 3 m | 7,4 µGal | 49 E | 37 s / 0,015 s |
| Personne de 80 kg | 1 m | 0,53 µGal | 11 E | 2 h / 2,8 s |
| Immeuble de 10⁶ kg | 20 m | 17 µGal | 17 E | 7 s / 0,003 s |

Équations : Δg = G m/d² ; gradient 2 G m/d³ ; t = (3 n/Δg)². **[DÉD]**, confiance élevée. Un gravimètre ou un
gradiomètre réel peut donc bel et bien signaler un obstacle de **plusieurs tonnes** à 2–3 m — un bloc de 2,4 t à
2 m (4,0 µGal, 40 E) ou un mur de 10 t à 3 m (7,4 µGal, 49 E) — à condition d'être immobile, à 1 g, à température
stable, pendant des secondes à des minutes. Une tonne à 2–3 m ne donne que 1,7–0,7 µGal, sous l'écart-type
d'une lecture d'un gravimètre de terrain comme le CG-6 (5 µGal) : il faudrait moyenner 80 à 400 lectures.
L'exigence d'immobilité formulée par la source est réaliste. C'est le seul élément du VGL qui le soit.

### 3.2 Servir de référence de position : non

- **[VÉR]** En un point, on mesure au plus 8 nombres : le vecteur g (3) et les 5 composantes indépendantes de
  son gradient. Ces 8 nombres ne déterminent pas la distribution de masse (problème inverse non unique) ni la
  position. La navigation par carte de gravité suppose une carte préalable et un véhicule qui se **déplace** le
  long d'un profil ; la compensation de la gravité par gradiomètre embarqué (Jekeli 2006) ne donne pas non plus
  de position absolue : elle corrige une centrale inertielle.
- **[DÉD]** Sensibilité spatiale : 1 µGal correspond à 3,2 mm de hauteur (gradient vertical de 308,6 µGal/m) mais
  à des mètres ou des kilomètres en horizontal. Ce n'est pas un « verrou » tridimensionnel.
- **[DÉD]** Un « radar » suppose une émission et un écho ; la gravimétrie est passive. L'analogie est impropre.
- **[VÉR]** Aucun repère absolu n'existe : en 60 ans la Terre parcourt 5,6×10¹³ m sur son orbite (4×10¹⁴ m avec le
  mouvement galactique). Le champ local à 1 µGal près ne peut pas « retenir » le véhicule sur la Terre ; la
  source le concède (« the temporal physics of this statement are wrong »). Analyse complète : Équipe B.
- Perturbations réelles du même ordre que le signal : marée (~±150 µGal, prévisible), pression atmosphérique,
  nappe phréatique, et les masses mobiles de l'unité elle-même — 10 kg de caloporteur déplacés de 0,5 à 0,3 m du
  capteur donnent 0,5 µGal.

### 3.3 Mesurer à côté des singularités : non

| Cas | g de la singularité au capteur | Résolution relative pour 1 µGal | Stabilité de position requise | Dilatation pour 1 K (aluminium) |
|---|---|---|---|---|
| 2,94×10¹¹ kg, capteur à 0,3 m | 218 m/s² (22 g) ; gradient 1,5×10¹² E | 4,6×10⁻¹¹ | **6,9×10⁻¹² m** | 6,9×10⁻⁶ m (10⁶ × trop) |
| 2,94×10¹¹ kg, capteur à 0,5 m | 78 m/s² (8 g) | 1,3×10⁻¹⁰ | 3,2×10⁻¹¹ m | 1,2×10⁻⁵ m |
| 4,4×10¹² kg, capteur à 0,3 m | 3 250 m/s² (331 g) ; gradient 2×10¹³ E | 3,1×10⁻¹² | 4,6×10⁻¹³ m | 6,9×10⁻⁶ m (10⁷ × trop) |

Équation : δr = r δg/(2 g_s). **[DÉD]**, confiance élevée. Pour distinguer 1 µGal « extérieur » du champ des
singularités il faudrait connaître leur distance au capteur au picomètre près, dans une unité qui chauffe de
dizaines de kelvins et dont la masse, la charge et la rotation des sources sont censées être modulées en
permanence. De plus : la plage d'un CG-6 (8 000 mGal) vaut 1/123 de g ; aucun gravimètre de précision ne
fonctionne à 2 g, encore moins à 22 g.

### 3.4 Effet de 2 g et de 38–49 °C

- 2 g : hors plage des gravimètres relatifs à ressort (facteur 123) ; un gravimètre supraconducteur est accordé
  sur le g local ; les instruments à chute libre et à atomes froids pourraient être redessinés pour 2 g
  (la phase d'un interféromètre atomique k g T² reste constante à hauteur de chute fixée) mais avec un gradient
  de 10¹¹–10¹³ E dans le volume de chute, la mesure n'a plus de sens. **[DÉD]**, confiance moyenne.
- 38–49 °C : FG5-X (20–30 °C), AQG-B (≤ 40 °C), iGrav (≤ 38 °C) sont hors plage ; CG-6 limite (45 °C, option
  55 °C). **[VÉR]** d'après les fiches constructeur.

## 4. État de l'art réel — horloges au césium

| Horloge | Exactitude / stabilité | Masse, volume, puissance | Température | Année |
|---|---|---|---|---|
| Microchip (ex-HP) 5071A, option hautes performances | ±5×10⁻¹³ ; palier ≤ 1×10⁻¹⁴ | 30 kg ; 133 × 426 × 524 mm ; 50 W | 0–50 °C garanti | 1992 |
| Microchip CSAC SA.45s | 3×10⁻¹⁰ à 1 s ; < 9×10⁻¹⁰/mois | 35 g ; 17 cm³ ; 0,12 W | −10 à +70 °C | 2011 |
| NIST-F1 / NIST-F2 (fontaines, laboratoire) | 1,7×10⁻¹⁵ (1999) / 1,1×10⁻¹⁶ (type B, 2014) | salle de laboratoire | — | 1999 / 2014 |
| Horloge optique à Al⁺ (laboratoire) | 9,4×10⁻¹⁹ | table optique | — | 2019 |

Constats **[DÉD]** :

1. **Quatre horloges au césium de l'an 2000 ne tenaient pas dans le coffre** : 4 × 30 kg = 120 kg (53 % de la
   masse de l'unité) et 0,119 m³, soit 189 % de l'enveloppe du coffre (0,063 m³) et 340 % de son volume utile ;
   un seul étalon, long de 52 cm, n'entre pas dans 26 cm de profondeur. La « miniaturisation des horloges » citée par la
   source est un vrai verrou de l'époque… effectivement levé depuis : quatre CSAC pèsent 140 g et consomment
   0,5 W (au prix d'une stabilité 10³ fois moindre). C'est le seul point où la technologie réelle a rejoint,
   et dépassé, une exigence du texte.
2. **Pourquoi quatre ?** Avec quatre horloges on peut détecter une horloge fautive, l'écarter, et garder un vote
   à trois. C'est l'architecture des satellites GPS Block II/IIA (2 césium + 2 rubidium) et Galileo (2 masers +
   2 rubidium) **[VÉR]** — documentée bien avant 2000. Rapprochement : **[HYP]** d'inspiration, non démontrable.
3. **« Lecture optique » du C206** : l'interrogation optique des atomes de césium existait déjà (NIST-7, jet à
   pompage optique, 1993 ; fontaine NIST-F1, 1999) **[VÉR]**. La phrase décrit l'état de l'art de la fin des années
   1990, non une rupture de 2034.
4. **Les horloges ne « voient » pas le champ** : le décalage gravitationnel relatif GM/(rc²) vaut 2×10⁻¹⁶ à 1 m et
   2×10⁻¹⁵ à 10 cm d'une masse de 2,94×10¹¹ kg ; 3×10⁻¹⁵ à 3×10⁻¹⁴ pour 4,4×10¹² kg. C'est 15 à 2 300 fois sous
   l'exactitude d'un 5071A (5×10⁻¹³). Seule une horloge optique de laboratoire le résoudrait. Un ensemble
   « horloges + capteurs de gravité » où les horloges serviraient à sentir la gravité est donc sans objet.
5. **Besoin réel de datation** : viser un jour donné à 60 ans demande 4,6×10⁻⁵ en relatif ; un quartz ordinaire
   (10⁻⁶) suffit. Le césium offre 8 décades de marge inutile. Sur 6 h de temps propre, un 5071A dérive de 10 ns.
6. **Incohérence d'échelle** : un facteur de 10 ans par heure (87 660), s'il était une dilatation gravitationnelle,
   exigerait un potentiel Φ/c² ≈ 0,5 ; une pesanteur de 2 g sur 1 m correspond à 2,2×10⁻¹⁶. Écart : 15,4 décades
   (détail : Équipe B).

## 5. Classement

| Élément | Statut | Constructible aujourd'hui ? |
|---|---|---|
| Quatre horloges au césium compactes avec vote | Démontré | **Oui** — 4 CSAC + comparateur de phase + logique de vote |
| Gravimètre/gradiomètre détectant un bloc de 2,4 t à 2 m ou un mur de 10 t à 3 m, véhicule à l'arrêt (une tonne à 2–3 m : sous l'écart-type du CG-6) | Démontré | **Oui** — CG-6 (5,5 kg ; 10,8 L, soit 31 % du volume utile : amovible plutôt que logé) ; gradiomètre atomique en laboratoire mobile |
| Même mesure à 2 g, 38–49 °C, à côté de masses de 10¹¹–10¹² kg | Contredit (6 à 7 décades sur la stabilité géométrique) | **Non** |
| « Instantané de gravité » comme référence de position ou verrou | Contredit (problème inverse non unique ; pas de repère absolu) | **Non — sans base physique** |
| Horloges au césium sensibles au champ des singularités | Contredit (1 à 3 décades) | Non |

## 6. Limites

Les temps d'intégration supposent un bruit blanc et un site calme. Les spécifications sont celles des fiches
constructeur (certaines lues par extrait seulement, voir REFERENCES.md). La sensibilité des horloges à
l'accélération et au champ magnétique des bobines n'a pas été chiffrée (**non résolu**).

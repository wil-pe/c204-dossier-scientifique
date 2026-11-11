# EXP-12 — Banc d'essai « C204 de substitution » : un coffre instrumenté pour tester honnêtement les affirmations mesurables

*Version 2 — révisée après la validation contradictoire (corrections n° 51 à 56 de la Red Team n° 2).*

| | |
|---|---|
| **Niveaux** | N1 (mini-banc ≤ 500 €) · N2 (banc complet ≈ 8–12 k€) · N3 (compléments de laboratoire) |
| **Sous-système C204 lié** | tous ceux qui ont une conséquence mesurable : gravité (VGL, « 1,5–2 g »), horloges, bobines de champ, évent à rayons X, température, « lumière courbée », calculateurs à vote |
| **Statut** | Proposition d'instrumentation. **Ce n'est pas une machine**, ni une maquette fonctionnelle : c'est un **banc de mesure** que l'on place autour d'un dispositif *candidat*. |
| **Calculateur** | `calculs/calc12_banc_essai.py` → `resultats/calc12_banc_essai.txt`, `figures/calc12_banc_essai.png` |

## 1. Objectif — et ce que le banc ne peut pas faire

Disposer d'un ensemble de capteurs redondants, d'un enregistrement infalsifiable et d'un protocole en aveugle
permettant de dire, pour chaque affirmation mesurable portée par un **dispositif candidat présenté par un
promoteur** : *implication réfutée*, *non testée par ce banc*, ou *anomalie à expliquer*.

**Le banc ne réfute rien de l'objet de 2000-2001, qui n'est pas disponible ; il s'applique à un dispositif
candidat.** Ce qu'il réfute, ce sont des *conséquences chiffrées* d'affirmations — dont plusieurs sont des
déductions de l'institut (modèle de Hawking pour la masse et la dose, seuil de 1° pour la « lumière courbée »,
1 T pour les bobines) et non des phrases du texte. La colonne « origine » du §6 le dit voie par voie.

## 2. Principe

1. Traduire chaque affirmation en un **signal attendu chiffré** (dossier §4, §6 et §6 bis ; fiches EXP-01 à 11).
2. Lui opposer un capteur dont la résolution est connue par **étalonnage préalable**.
3. Choisir pour chaque voie le **contraste de mesure valide**, selon le régime de la grandeur :

| Régime de la grandeur selon le récit | Exemples | Contraste valide |
|---|---|---|
| **Permanente** — les singularités ne « s'éteignent » pas. Le corpus le dit du trou noir lui-même (« I don't believe I said you could turn it on or off », texte intégral, ligne 4081), alors que l'*unité* y est décrite allumée ou éteinte (lignes 129 et 195) | masse ; pesanteur propre ; rayonnement et puissance des singularités ; effets relativistes réels | **dispositif − leurre**, ou **mesure absolue** rapportée au fond (pesée, débit de dose au-dessus du fond, bilan thermique) |
| **Revendiquée pendant le fonctionnement** | « 1,5–2 g » ; « 10 ans par heure » ; lumière courbée ; 38–49 °C | **marche − arrêt** — observable seulement si l'appareil reste dans le laboratoire pendant l'essai, ce qui est déjà une réfutation d'un autre ordre |
| **Commutable** | champ des bobines, consommation électrique | **marche − arrêt** |

4. Mesurer en cycles tirés au sort, l'analyste ignorant la clé ; décider selon des **critères écrits à l'avance**.

Redondance : chaque grandeur est mesurée par trois capteurs sur trois chaînes d'acquisition indépendantes ;
décision par vote majoritaire (événements) ou médiane (valeurs continues). Probabilité d'erreur d'un vote
2-parmi-3 pour des pannes indépendantes de probabilité p : P = 3p²(1 − p) + p³ (Lyons & Vanderkulk 1962).

## 3. Architecture

```
                    ┌─────────────── BANC (volume utile ≥ 1,0 × 0,4 × 0,4 m pour un candidat de ≈ 0,85 m) ────────────────┐
                    │                                                                                                    │
  dispositif        │  GRAVITÉ      3 accéléromètres triaxiaux bas bruit (A, B, C) + géophone, sur CHARIOT mobile         │
  candidat   ──────►│  MASSE        plateau de pesée étalonné sous le dispositif                                          │
                    │  TEMPS        horloge atomique compacte ou rubidium ──► compteur ◄── GPSDO (référence)              │
  LEURRE     ──────►│  CHAMP B      3 magnétomètres triaxiaux (A, B, C), dont 1 à 1 m                                     │
  (poste          │  RAYONNEMENT  2 compteurs Geiger de tubes différents + 1 scintillateur                              │
  symétrique :      │  THERMIQUE    12 sondes de contact + air ambiant ; caméra thermique ; wattmètre batterie            │
  mêmes masse       │  OPTIQUE      laser classe 2 rasant le dispositif ──► détecteur de position à 2 m                    │
  nominale, forme,  │  ROTATION     gyromètre                                                                             │
  bruit ET          │  AMBIANCE     pression, hygrométrie, tension d'alimentation, microphone, température des capteurs   │
  puissance         │                                                                                                    │
  dissipée)         │      chaîne A (microcontrôleur 1, carte mémoire 1, batterie 1)  ─┐                                  │
                    │      chaîne B (conception différente, batterie 2)               ─┼─► vote 2/3, médiane (hors ligne) │
                    │      chaîne C (conception différente, batterie 3)               ─┘                                  │
                    │      horodatage commun : 1PPS GPS distribué par fibre optique plastique                             │
                    └────────────────────────────────────────────────────────────────────────────────────────────────────┘
   clés (marche/arrêt ; poste dispositif/poste leurre) : tirées au sort par un tiers, scellées, empreinte SHA-256 publiée AVANT l'essai
```

Règles de conception : trois chaînes de **conceptions différentes** ; alimentations séparées sur batteries ;
liaisons **optiques** entre chaînes ; capteurs A, B, C permutables ; données brutes écrites en continu avec
empreinte chaînée ; aucun traitement en ligne. Le **leurre** a la masse nominale (227 kg ou celle que déclare le
promoteur), la forme, le bruit **et la puissance dissipée** du dispositif, sans quoi l'échauffement des capteurs
mime un signal corrélé à la clé.

## 4. Matériel et coût indicatif (2026, à confirmer)

| Version | Contenu | Total |
|---|---|---|
| **N1 — mini-banc** | smartphone (accéléromètre, magnétomètre, gyromètre) ; Geiger enregistreur (110 €) ; 2 accéléromètres MEMS bas bruit + microcontrôleurs (120 €) ; 6 sondes de température (45 €) ; module GPS 1PPS (35 €) ; laser classe 2 + webcam (40 €) ; pesée (80 €) ; batteries, boîtier (60 €) | **≈ 490 €** |
| **N2 — banc complet** | 3 chaînes d'acquisition (600 €) ; 3 accéléromètres triaxiaux + géophone (700 €) ; GPSDO + rubidium d'occasion + compteur d'intervalles (900 €) ; horloge atomique miniature, optionnelle (4000 €) ; 3 magnétomètres dont 1 fluxgate (900 €) ; 2 Geiger + scintillateur (900 €) ; sondes + caméra thermique (700 €) ; plateau de pesée 600 kg / 0,1 kg (350 €) ; laser + détecteur de position (250 €) ; gyromètre (1500 €) ; coffre, blindage, isolations (1200 €) | **≈ 12 000 €** (8 000 € sans l'horloge miniature) |
| **N3 — compléments** | gravimètre relatif de terrain (≈ 100 k€, ou prêt) ; étalon à césium / lien de temps étalonné (≈ 60 k€) ; spectromètre gamma au germanium et chambre d'ionisation (≈ 50 k€) ; magnétomètre à pompage optique (≈ 20 k€) | **≈ 230 k€** |

## 5. Protocole en aveugle, pas à pas

**Avant (phase 0 — caractérisation)**
1. Étalonner chaque capteur (six positions pour les accéléromètres ; pesée de masses étalons ; comparaison des
   horloges 72 h ; bruit de fond radiologique 24 h ; carte thermique à vide ; coefficient thermique de chaque
   accéléromètre).
2. Enregistrer 24 h **sans dispositif**, puis 24 h avec le **leurre** : établir le bruit σ de chaque voie par cycle
   **et** sa dérive lente.
3. **Injections de signaux connus** (preuve que le banc détecte) : masse de 20 kg approchée à 0,5 m ; aimant à
   1 m ; résistance chauffante de 50 W ; lame de verre dans le faisceau ; décalage volontaire de 10⁻⁹ sur
   l'horloge. Chaque injection doit être retrouvée par l'analyse en aveugle.
4. **Pré-enregistrement** : déposer par écrit hypothèses, seuils, nombre de cycles, règles d'exclusion, analyse,
   et pour chaque voie le contraste retenu (§2).

**Pendant — trois séries distinctes**
5. **Mesures absolues** (grandeurs permanentes) : pesée du dispositif sur le plateau étalonné ; débit de dose à
   1 m et 3 m comparé au fond mesuré en phase 0 ; bilan thermique.
6. **Série « dispositif − leurre »** (grandeurs permanentes) : dispositif et leurre occupent deux postes
   symétriques ; c'est le **chariot de capteurs** qui alterne entre les deux postes selon une clé tirée par un
   tiers (64 cycles de 100 s) ; l'analyste ignore quel poste porte le dispositif (les deux sont capotés).
7. **Série « marche − arrêt »** (grandeurs commutables ou revendiquées pendant le fonctionnement) : 64 cycles de
   100 s, état tiré au sort par le tiers ; l'opérateur du dispositif n'a pas accès aux données.
8. Vidéo continue ; scellés ; journal horodaté de tout événement (porte, passage, météo).

**Après**
9. L'analyste fige ses résultats (différences par voie et incertitudes), les dépose, **puis** les clés sont ouvertes.
10. Contrôles : permutation des capteurs A/B/C et répétition ; échange des postes dispositif/leurre ; essai à blanc.

## 6. Signal attendu et marge de réfutation (calculé)

Masses retenues par le programme pour 300–500 MW (dossier v1.2, erratum E2) : **3,9–5,1 × 10¹² kg par
singularité, 7,8 × 10¹² à 1,0 × 10¹³ kg pour les deux** (l'ancienne valeur « 10¹¹–10¹² kg » est abandonnée).

| Voie | σ par cycle, N2 (N1) | Signal impliqué | Signal/5σ, N2 (N1) | Régime → contraste | Origine du signal |
|---|---|---|---|---|---|
| Pesanteur ressentie | 2 × 10⁻⁴ (2 × 10⁻³) m/s² | ≥ 4,9 m/s² (« 1,5–2 g ») | 4 × 10³ (2 × 10²) | fonctionnement → marche − arrêt | texte |
| Pesanteur propre de la paire, à 1 m | idem | 520–680 m/s² (53–69 g) | 5 × 10⁵ (2 × 10⁴) | permanent → dispositif − leurre | déduit (Hawking) |
| Masse de l'appareil | 0,1 (0,5) kg | 7,8 × 10¹² – 1,0 × 10¹³ kg | **2 × 10¹³** (4 × 10¹²) | permanent → pesée absolue | déduit (Hawking) |
| Marche d'horloge | 10⁻¹¹ (10⁻⁷) | 8,8 × 10⁴ (« 10 ans/heure ») | 2 × 10¹⁵ (2 × 10¹¹) | fonctionnement → marche − arrêt | texte |
| Champ magnétique | 20 nT (200 nT) | 37 µT à 3 m | 3 × 10² (3 × 10¹) | commutable → marche − arrêt | déduit [HYP : 1 T sur 10 cm] |
| Rayonnement, **lecture littérale** | 0,02 (0,05) µSv/h | 9,0 × 10³ Gy/s à 3 m (400 MW entièrement en X de 100 keV) | 3 × 10¹⁴ (1 × 10¹⁴) | permanent → absolu / leurre | texte pris au mot |
| Rayonnement, **spectre de Hawking** | idem | ≈ 3,8 × 10² Gy/s à 3 m ; ≈ 3,4 × 10³ Gy/s à 1 m (γ primaires, borne basse) | 1 × 10¹³ (6 × 10¹²) | permanent → absolu / leurre | déduit (Équipes C, G) |
| Température de surface | 0,1 (0,2) K | +18 à +29 K | 36 (18) | fonctionnement → marche − arrêt | texte |
| Puissance dissipée | 5 (20) W | 3–5 × 10⁸ W | 10⁷ (3 × 10⁶) | permanent → bilan absolu | texte |
| Faisceau laser | 5 µrad (20 µrad) | ≥ 1° (≈ 55° apparents sur DOC-012) | 5 × 10² (1 × 10²) | fonctionnement → marche − arrêt | texte/photo ; seuil choisi |
| *Décalage gravitationnel d'horloge réel* | 10⁻¹¹ | 5,8–7,6 × 10⁻¹⁵ (paire à 1 m) | 10⁻⁴ | permanent | **non testable** |
| *Déviation gravitationnelle réelle* | 5 µrad | 2,3–3,0 × 10⁻¹⁴ rad | 10⁻⁹ | permanent | **non testable** |
| *Entraînement des référentiels* | 5 µrad/s | 5–9 × 10⁻²¹ rad/s (spin seul) ; jusqu'à 5 × 10⁻¹⁴ rad/s (paire en orbite) | 10⁻¹⁶ à 10⁻⁹ | permanent | **non testable** |

Marges = signal / [5 × √(σ² + systématique²)]. Les valeurs N1 sont réalistes pour du matériel grand public :
magnétomètre de téléphone ≈ 200 nT (100–500 nT), pointeur laser + webcam ≈ 20 µrad, accéléromètre de téléphone
2 × 10⁻³ m/s². Coffre à l'échelle révisée (L = 0,85 m, 1,07 m²) : 38–49 °C correspondent à **190–310 W** dissipés.

**Budget de dérive thermique des accéléromètres** : coefficient ≈ 10⁻³ m/s² par kelvin (MEMS bas bruit), 10⁻² m/s²
par kelvin (téléphone) ; écart de température résiduel entre les deux états après écran thermique et régression
sur la température mesurée : 0,1 K (N2), 0,5 K (N1) → systématiques de 10⁻⁴ et 5 × 10⁻³ m/s², qui ne se moyennent pas.

**Seuils du protocole réellement décrit — 64 cycles de 100 s** (≈ 32 / 32 ; ≈ 1,8 h par série, 3,6 h avec les temps
morts). Seuil global 5σ réparti sur 11 comparaisons (Bonferroni) → 5,44σ par comparaison ; seuil statistique
5,44 × 0,25σ = **1,36σ par cycle** ; borne à 95 % en cas de résultat nul : 0,41σ ; seuil total =
√[(1,36σ)² + (3 × systématique)²] :

| Capteur | Seuil N2 | Seuil N1 |
|---|---|---|
| Accéléromètres | 4,1 × 10⁻⁴ m/s² | 1,5 × 10⁻² m/s² |
| Pesée | 0,14 kg | 0,7 kg |
| Horloge | 1,4 × 10⁻¹¹ | 1,4 × 10⁻⁷ |
| Magnétomètres | 66 nT | 410 nT |
| Rayonnement | 0,027 µSv/h | 0,068 µSv/h |
| Température | 0,14 K | 0,27 K |
| Puissance | 7 W | 27 W |
| Faisceau laser | 16 µrad | 66 µrad |
| Gyromètre | 6,8 µrad/s | 68 µrad/s |

Masse cachée exclue à 1 m (contraste dispositif − leurre) : > 6 × 10⁶ kg (N2) ; > 2 × 10⁸ kg (N1) ; > 1,7 × 10³ kg
avec un gravimètre de terrain (5 µGal ; systématique de hauteur 3 µGal). *(La version 1 annonçait des seuils « à 5σ
en 100 cycles » : ils valaient pour 100 paires marche/arrêt, soit une durée triple de celle du protocole ; ils
sont retirés.)*

Vote : p = 10⁻² → P = 3 × 10⁻⁴ ; p = 10⁻³ → 3 × 10⁻⁶. Avec 2 % de pannes de mode commun : 4,9 × 10⁻⁴ et
2,3 × 10⁻⁵ — **le mode commun domine**, d'où la diversité de conception et l'isolation.

Puissance statistique (Monte-Carlo illustratif, sans systématique) : à 64 cycles, un effet de 2σ par cycle est
détecté dans 99,5 % des cas, un effet de 1σ dans 7 % ; taux de fausses alarmes nul sur 4000 essais.

## 7. Critères de décision (fixés avant l'essai, pour le dispositif candidat)

- **Contraste** : pour une grandeur commutable ou revendiquée pendant le fonctionnement : différence
  **marche − arrêt** ; pour une grandeur permanente selon le récit (masse, pesanteur propre, rayonnement et
  puissance des singularités, qui ne « s'éteignent » pas) : différence **dispositif − leurre**, ou **mesure
  absolue rapportée au fond**. Une différence marche − arrêt nulle sur une grandeur permanente ne réfute rien.
- **Implication réfutée** : la différence (ou l'écart au fond) est compatible avec zéro et sa borne supérieure à
  95 % est au moins 100 fois plus petite que le signal impliqué. Le compte rendu précise si l'implication est une
  phrase du texte ou une déduction de l'institut.
- **Non testée** : le signal impliqué est sous la résolution du banc (trois dernières lignes du tableau), ou le
  régime revendiqué n'a pas pu être produit (le promoteur n'a pas « fait fonctionner » l'appareil) ; on l'écrit,
  on ne conclut pas.
- **Anomalie à expliquer** : dépassement du seuil corrigé sur ≥ 2 capteurs de conception différente, corrélé à
  la clé, absent avec le leurre, persistant après permutation des capteurs et échange des postes, et accompagné
  d'une réponse correcte aux injections connues. Étape suivante obligatoire : reproduction par une équipe
  indépendante. **Une anomalie instrumentale n'est pas un déplacement temporel.**
- **Essai invalide** : injection connue non retrouvée, scellé rompu, clé divulguée, règle d'exclusion appliquée
  après ouverture.

## 8. Durée

Phase 0 : une semaine. Essai : deux jours (mesures absolues ; série dispositif − leurre ; série marche − arrêt).
Analyse et rapport : une semaine.

## 9. Sécurité

Le banc lui-même n'utilise que de très basses tensions, un laser de classe 2 et aucune source radioactive
ajoutée. **Le dispositif candidat est un inconnu** : exiger de son promoteur une description des dangers (haute
tension, batteries, aimants, laser, pression, chimie) ; inspection préalable ; essai à distance derrière un écran
si le moindre doute subsiste ; arrêt d'urgence ; extincteur adapté aux batteries ; débit de dose surveillé en
continu avec alarme **dès l'arrivée de l'appareil** (grandeur permanente). On ne met pas sous tension un appareil
de construction inconnue dans un local occupé.

## 10. Ce que cela prouve — et ne prouve PAS

**Prouve** : qu'un dispositif candidat donné produit, ou ne produit pas, une anomalie de pesanteur, de masse, de
marche d'horloge, de champ magnétique, de rayonnement, de température ou de propagation lumineuse au-dessus de
seuils chiffrés, avec le contraste adapté à chaque grandeur.

**Ne prouve pas** :
- quoi que ce soit sur l'objet décrit en 2000-2001, qui n'est pas disponible ;
- l'impossibilité de principe d'un phénomène ;
- la fausseté d'une affirmation du texte lorsque le « signal impliqué » est une déduction de l'institut (on
  réfute alors la déduction appliquée à cet appareil : modèle de Hawking, émission non blindée, seuil de 1°) ;
- en cas d'anomalie, un voyage temporel — aucune voie du banc ne mesure un « déplacement dans le temps ». Le seul
  observable qui s'en approcherait (un écart d'horloge après comparaison avant/après, EXP-01) ne distingue pas
  une dilatation du temps d'une panne d'oscillateur, et ne serait de toute façon qu'un décalage vers le futur.

## 11. Lien avec la C204 [DÉD]

- Le banc reprend, en version réelle, trois « systèmes » revendiqués : capteurs de gravité, horloges, calculateurs
  redondants. Il montre ce que ces fonctions coûtent et valent réellement en 2026.
- « Protocole de Borda » : la méthode de Borda est une règle de vote par classement (théorie du choix social),
  pas un protocole de tolérance aux pannes ; à trois votants et deux options, elle se réduit au vote
  majoritaire. Les techniques réelles sont la redondance modulaire triple (Lyons & Vanderkulk 1962) et les
  protocoles d'accord byzantin (Pease, Shostak & Lamport 1980 ; Lamport, Shostak & Pease 1982), lesquels exigent
  **3f + 1** unités pour tolérer f unités arbitrairement fautives : trois calculateurs ne tolèrent pas une
  panne byzantine sans messages signés.
- Méthode : analyses en aveugle (Klein & Roodman 2005 ; MacCoun & Perlmutter 2015).

## 12. Confiance et limites

Architecture et protocole : confiance **élevée** (pratiques standard). Résolutions par voie : **moyenne**, à
établir en phase 0 sur le matériel réel (aucune n'a été caractérisée : rien n'a été construit). Systématiques
thermiques : **moyenne à faible** (ordres de grandeur). Coûts : **moyenne à faible**. Limites principales : le
banc ne dit rien des effets relativistes réels, trop faibles ; il teste des affirmations d'ingénierie sur un
appareil présent ; les grandeurs « pendant le fonctionnement » supposent que le promoteur déclenche ce régime.

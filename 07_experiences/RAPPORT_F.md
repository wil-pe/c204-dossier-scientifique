# Équipe F — Physique expérimentale et laboratoire

**Programme C204 — rapport du 10 novembre 2026, version 2 (corrigée après validation contradictoire ; journal en
§10).** Analyse scientifique critique : rien de ce qu'affirme « John
Titor » n'est tenu pour vrai ; l'existence de la machine C204 n'est attestée par aucune source indépendante.

> **Question posée à l'équipe** : quels phénomènes physiques *réels*, voisins de ceux qu'invoque la machine,
> peut-on reproduire et mesurer à petite échelle, sans danger ?
>
> **Règle de lecture** : reproduire un phénomène physique n'est jamais démontrer un voyage temporel. Chaque
> fiche dit ce que l'expérience prouve **et ce qu'elle ne prouve pas**.

Conventions du dossier de base : [DOC] documenté · [DÉD] déduit · [HYP] hypothétique · [INT] interprétation de
tiers · [VÉR] vérifiable indépendamment. Niveaux : **N1** amateur éclairé / lycée (< ≈ 500 €) · **N2** salle de TP
universitaire · **N3** laboratoire de recherche.

---

## 0. Résumé exécutif

1. **Douze expériences** réelles et sans danger ont été conçues, chacune déclinée par niveau, avec signal attendu
   et budget de bruit **calculés par des scripts exécutés** (`calculs/`, 12 scripts, 12 figures).
2. **Aucune n'a de rapport avec un voyage dans le temps.** Elles reproduisent des phénomènes voisins : dilatation
   du temps, transfert de temps, gravitation de laboratoire, gravimétrie, effet Casimir, horizons analogues,
   piégeage de charges, réfraction, effet Sagnac, corrélations quantiques, radioactivité naturelle.
3. **Les effets relativistes réels des masses qu'implique le récit sont tous hors de portée d'un banc.** À 1 m de
   la paire de singularités (7,8 × 10¹² à 1,0 × 10¹³ kg) : décalage d'horloge 6–8 × 10⁻¹⁵ ; déviation de la lumière
   2–3 × 10⁻¹⁴ rad ; entraînement des référentiels 5–9 × 10⁻²¹ rad/s (spin seul), jusqu'à 5 × 10⁻¹⁴ rad/s pour une
   paire en orbite.
4. **Les affirmations « fortes » attribuées à la C204 ont, elles, des conséquences grossièrement mesurables** :
   1,5–2 g, « 10 ans par heure », 300–500 MW, évent à rayons X, 38–49 °C, lumière visiblement courbée. Un banc
   modeste réfuterait ces conséquences **sur un dispositif candidat présent**. **Le banc ne réfute rien de l'objet
   de 2000-2001, qui n'est pas disponible ; il s'applique à un dispositif candidat.** Plusieurs « signaux
   impliqués » sont en outre des déductions de l'institut (modèle de Hawking, émission non blindée, seuils
   choisis) et non des phrases du texte.
5. Le test le plus discriminant et le moins cher est le **compteur Geiger à ≈ 100 €** : par une mesure absolue
   rapportée au fond, il exclut en quelques minutes toute fuite X ou γ supérieure à ≈ 10⁻⁷ W. L'affirmation
   « 300–500 MW » implique, à 3 m : **lecture littérale** (400 MW entièrement en rayons X de 100 keV) ≈ 9 × 10³ Gy/s,
   dose létale en 0,44 ms ; **spectre de Hawking** (γ primaires seuls, 7,5 % de la puissance, borne basse)
   ≈ 3,4 × 10³ Gy/s à 1 m et ≈ 3,8 × 10² Gy/s à 3 m, dose létale en ≈ 10 ms.
6. Le deuxième est la **balance** : une unité de 227 kg et des trous noirs rayonnant 300–500 MW — **3,9–5,1 × 10¹² kg
   par singularité, 7,8 × 10¹² à 1,0 × 10¹³ kg pour les deux** (valeur retenue par le programme) — diffèrent de dix
   à onze ordres de grandeur ; une seule de ces masses créerait 27–35 g à 1 m et serait détectable par un
   smartphone à 160–185 m, par un gravimètre de terrain à plus de 30 km.
7. La photographie dite « du laser » (C204-DOC-012, retrouvée par l'Équipe A) montre une courbure apparente
   d'environ 55° sur ~10 cm [lecture F, confiance faible]. **La gravitation ne l'explique pas** (il faudrait
   4,6 × 10¹⁶ g, ou une masse planétaire) ; **la réfraction dans l'air non plus** (bornée à ≈ 0,4–1,3°). La cuve
   d'eau sucrée (jusqu'à 23°) montre qu'il faut un milieu dense pour courber ainsi la lumière ; le procédé réel de
   l'image n'est pas identifié.
8. **Réponse à Q10 : oui, on peut construire un dispositif expérimental — non pas une machine, mais un banc de
   mesure en aveugle (EXP-12)** qui teste les conséquences *mesurables* des affirmations autour d'un appareil
   candidat ; version N1 ≈ 490 €, version N2 ≈ 8–12 k€.
9. **Références** : 150 notices vérifiées en ligne par Crossref, 3 sources web relues, 8 sources classiques ou
   normatives citées sans vérification et signalées (`REFERENCES.md`).
10. **Sécurité** : aucune source radioactive ajoutée ni manipulée ; lasers de classe 2 au plus hors laboratoire ; haute tension
    uniquement en TP encadré, à courant limité ; les niveaux N1 n'en utilisent jamais.

---

## 1. Programme gradué — vue d'ensemble

| N° | Expérience | N1 | N2 | N3 | Sous-système C204 lié |
|---|---|---|---|---|---|
| 01 | Dilatation du temps (horloges) | caractériser un rubidium : **l'effet échappe** (≈ 500 €) | séjour en altitude avec césiums : 22 ns, S/B ≈ 4 par horloge | horloges optiques : cm et mm | 4 horloges au césium ; « 10 ans/heure » |
| 02 | Transfert de temps | NTP ; câble de 10 m mesuré par deux GPS : 50,5 ± 0,5 ns (150–400 €) | PTP, White Rabbit, vue commune | phase GPS, liens optiques | horloges ; « date de destination » |
| 03 | G et test nul électromagnétique | Cavendish artisanal, qualitatif (30–100 €) | G à ≈ 4 % ; aimant contre leurre en aveugle | balances de recherche : encore 4 à 7 ordres de grandeur trop peu sensibles | injection d'électrons ; bobines |
| 04 | Gravimétrie (« VGL ») | smartphone, pendule : 10⁻³ m/s² (0–150 €) | gravimètre relatif : 5 µGal, marées, cavités | absolu, atomes froids | capteurs de gravité |
| 05 | Effet Casimir | analogue par ondes de surface (20–60 €) | sphère-plan au microscope à force atomique | précision au % | (objection « énergie négative ») |
| 06 | Gravité analogue | ressaut circulaire, cône de Mach ; tourbillon (0–30 €) | canal, superradiance (difficile) | condensats, optique | « champ de Kerr », « horizons » |
| 07 | Confinement de charges | selle tournante, graphite en lévitation — **sans haute tension** (50–120 €) | piège de Paul à grains, TP encadré | pièges à ions | « logements magnétiques » |
| 08 | Déviation de la lumière | cuve d'eau sucrée : jusqu'à 23° (20–40 €) | profil d'indice ; boîtier tiède | (astronomie) | « lumière courbée » |
| 09 | Sagnac / Lense-Thirring | gyromètre de smartphone (0–50 €) | Sagnac de table : 0,13 rad à 1 rad/s | gyrolasers ; espace | « top-spin », axe polaire |
| 10 | Optique quantique et causalité | gomme « de table » (analogue classique, 15–30 €) | banc à paires de photons, s'il existe | choix retardé, P-CTC, interrupteur quantique | interprétation d'Everett revendiquée |
| 11 | Rayonnement | Geiger, bruit de fond, **sans source** (80–150 €) | spectre gamma du fond | germanium | évent à rayons X ; 300–500 MW |
| 12 | **Banc d'essai de substitution** | mini-banc ≈ 490 € | banc complet ≈ 8–12 k€ | compléments ≈ 230 k€ | tous les observables |

Détail par niveau (coût, durée, signal, bruit, rapport signal/bruit, faisabilité, sécurité) : `tableau_experiences.csv`
(41 lignes). Fiches complètes : `fiches/EXP-01 … EXP-12`.

**Budget N1** : chaque expérience N1 tient individuellement sous 500 € (de 0 à 150 € pour la plupart ; 150–400 €
pour EXP-02 ; ≈ 450–500 € pour EXP-01, qui est la plus chère et ne détecte pas l'effet). L'ensemble des
expériences N1 hors EXP-01 représente ≈ 400 à 1100 € selon le matériel déjà disponible ; le mini-banc EXP-12
(≈ 490 €) réutilise le matériel de EXP-04, 08, 09 et 11.

---

## 2. Les signaux chiffrés les plus instructifs

### 2.1 Ce que la physique réelle prévoit à 1 m des masses retenues [DÉD, calculs F ; cohérent avec B, C, D, G]

Masse retenue par le programme pour 300–500 MW de rayonnement de Hawking (dossier v1.2, erratum E2) :
**3,9–5,1 × 10¹² kg par singularité ; 7,8 × 10¹² à 1,0 × 10¹³ kg pour les deux.** (Valeur déduite, jamais
revendiquée ; le texte dit au contraire que la masse est « bien plus petite » que celle d'une montagne.)

| Grandeur à 1 m | Une singularité | La paire | Meilleur instrument existant | Écart |
|---|---|---|---|---|
| Décalage d'horloge GM/(rc²) | 2,9–3,8 × 10⁻¹⁵ | 5,8–7,6 × 10⁻¹⁵ (53–69 m de dénivelé terrestre) | horloge optique : 10⁻¹⁸ | mesurable en principe par une horloge optique — pas par 4 césiums |
| Déviation de la lumière 4GM/(c²b) | 1,2–1,5 × 10⁻¹⁴ rad | 2,3–3,0 × 10⁻¹⁴ rad | pointé laser ~10⁻⁶ rad ; bruit de photons 3,6 × 10⁻¹² rad/√Hz | 7 à 8 ordres de grandeur |
| Entraînement des référentiels, **spin seul** (Kerr extrémal) | 5,0–8,6 × 10⁻²¹ rad/s (3,3 × 10⁻²² pour 10¹² kg) | — | gyrolaser géant ~7 × 10⁻¹³ rad/s | 8 à 9 ordres de grandeur |
| Entraînement des référentiels, **paire en orbite** (borne supérieure) | — | 2,1–5,4 × 10⁻¹⁴ rad/s (entraxe 0,098–0,30 m) | idem | ≈ 1 ordre de grandeur (facteur 13 à 35) ; « 1 à 9 ordres de grandeur selon le terme » |
| Pesanteur GM/r² | 260–340 m/s² (27–35 g) | 520–680 m/s² (53–69 g) | smartphone : 2 × 10⁻³ m/s² | **détectable à 160–185 m par un smartphone, à 32–37 km par un gravimètre** (une singularité) |
| Poids sur le plancher | 4–5 × 10¹³ N | 0,8–1,0 × 10¹⁴ N | — | incompatible avec un véhicule |

Le terme orbital n'existe que si les deux singularités tournent l'une autour de l'autre ; il est nul si elles
sont tenues fixes. Pour les 227 kg revendiqués, toutes ces valeurs sont à diviser par ≈ 2 × 10¹⁰ (spin : 4 × 10²⁰).
Ancienne fourchette du dossier v1 (10¹¹–10¹² kg) : valeurs 4 à 50 fois plus faibles.

### 2.2 Ce qu'impliquent les affirmations, et ce qu'un banc modeste en verrait

| Affirmation [DOC texte] | Implication chiffrée | Capteur (résolution) | Marge signal/5σ |
|---|---|---|---|
| « 1,5 à 2 g » ressentis | Δg ≥ 4,9 m/s² | accéléromètre MEMS (2 × 10⁻⁴ m/s², dérive thermique comprise) | 4 × 10³ |
| « 10 ans par heure » | dt_ext/dτ = 87 660 | n'importe quelle horloge (10⁻¹¹) | 2 × 10¹⁵ |
| « 300–500 MW » | 3–5 × 10⁸ W à évacuer : 4800–5450 K sur 10 m² (8400–9500 K sur le coffre de 1,07 m²), ou 116–193 kg/s d'eau vaporisée | bilan thermique (5 W) | 10⁷ |
| « 100–120 °F » autour de l'unité | ≈ 190–310 W dissipés par un coffre de 1,07 m² (échelle révisée L = 0,85 m) — soit **10⁶ fois moins** que 300–500 MW | sondes (0,1 K) | 36 |
| « rayons X évacués », **lecture littérale** (400 MW entièrement en X de 100 keV) | 9 × 10³ Gy/s à 3 m ; dose létale en 0,44 ms | Geiger (0,02–0,05 µSv/h) | 10¹⁴ |
| idem, **spectre de Hawking** (γ primaires : 7,5 % de la puissance, ~15 MeV ; borne basse — Équipes C et G) | ≈ 3,4 × 10³ Gy/s à 1 m ; ≈ 3,8 × 10² Gy/s à 3 m ; dose létale en ≈ 10 ms | Geiger | 10¹³ |
| blindage correspondant (faisceau étroit, minorant) | 0,5 cm de plomb à 100 keV, mais 42 cm (6,5 t) à 1 MeV, 58 cm (15 t) à 10 MeV ; 47 cm (8,7 t) pour les γ de Hawking | balance | — |
| « lumière courbée » visible (≥ 1° ; ≈ 55° apparents sur DOC-012) | masse de 5,9 × 10²⁴ kg (une Terre) à 1 m pour 1° ; champ de 4,6 × 10¹⁶ g pour un rayon de courbure de 10 cm | laser + détecteur (5 µrad en N2, 20 µrad en N1) | 5 × 10² |
| « logement magnétique » d'une charge | Q/m ≤ 8,6 × 10⁻¹¹ C/kg (extrémal, indépendant de M) ; champ de sustentation ≥ 1,1 × 10¹¹ V/m ; piège de Paul : 10¹² V ; avec la charge tenable (≈ 6 e, borne 137 e) : 2 × 10³⁰ – 5 × 10³¹ V/m | — | 5 à 12 ordres de grandeur hors de portée (plus de 20 avec la charge tenable) |
| « injection d'électrons » modifiant la masse | charge extrémale de 4,4 × 10¹² kg : 379 C d'électrons = 2,2 × 10⁻⁹ kg | — | sans effet |

Origine de ces implications : « 1,5–2 g », « 10 ans par heure », « 300–500 MW », « 100–120 °F » et « rayons X »
sont des phrases du texte ; la masse, les débits de dose, le seuil de 1° et les blindages sont des **déductions de
l'institut** (modèle de Hawking, émission non blindée). Les deux premières ne sont revendiquées que **pendant** le
déplacement.

### 2.3 Repères expérimentaux réels

| Phénomène | Signal | Ce qu'il faut pour le voir |
|---|---|---|
| Dilatation gravitationnelle | 1,09 × 10⁻¹⁶ par mètre ; 9,4 ns/jour pour 1000 m | 3 césiums et un week-end en montagne (S/B ≈ 7), ou une horloge optique et 1 cm |
| Rubidium d'occasion en montagne | signal 1,6 × 10⁻¹³ | **impossible** : pression (×100), température (×60), champ magnétique (×600) |
| Relativité dans le GPS | +38,6 µs/jour (+45,8 potentiel, −7,2 vitesse) | re-dérivé ; vérifié chaque jour par le système |
| Retard d'un câble | 5,05 ns/m | deux modules GPS et 10 minutes |
| Attraction de Cavendish | 7,4 × 10⁻¹⁰ N ; spot déplacé de 29 mm | balance de TP |
| « Gravité » d'un aimant de 1 litre (E/c² = 4,5 × 10⁻¹⁵ kg) | 1,8 × 10⁻²⁴ N | rien : les forces magnétiques parasites valent 10⁻⁵ N (10¹⁹ fois plus) |
| Champ « pesant » autant que l'eau | 1,5 × 10⁷ T | record continu ≈ 45 T |
| Gradient à l'air libre | 309 µGal/m | gravimètre de terrain (5 µGal) ; pas un smartphone (2 × 10⁵ µGal) |
| g comme « empreinte » d'un lieu | 1 µGal ↔ ≈ 100 km² de surface terrestre ; marée 280 µGal | non unique, variable dans le temps |
| Casimir, sphère 100 µm à 100 nm | 2,7 × 10⁻¹⁰ N | microscope à force atomique ; 100 mV résiduels font autant |
| Énergie de Casimir, 1 m² à 10 nm | −4,3 × 10⁻⁴ J (−4,8 × 10⁻²¹ kg) | il manque ≈ 3 × 10⁴⁷ pour une gorge de trou de ver de 1 m |
| Température de Hawking analogue dans l'eau | 1,2 × 10⁻¹¹ K | inobservable (eau à 293 K) ; seuls les effets stimulés le sont |
| Piège de Paul | stable si q < 0,908 (vide) | retrouvé numériquement ; ≈ 8 dans l'air pour un grain de 30 µm |
| Sagnac, boucle de 1 m² | 0,132 rad à 1 rad/s | interféromètre de TP ; vérifié sur Michelson-Gale (0,236 frange) |
| Lense-Thirring terrestre au sol | 1,7 × 10⁻¹⁴ rad/s | jamais mesuré au sol ; mesuré en orbite |
| Gomme quantique | marginale du signal indépendante du choix distant à 6,5 × 10⁻¹⁹ près (calcul) | aucun signal rétrograde, par construction de la théorie et par l'expérience |
| Post-sélection « P-CTC » | probabilité cos²(θ/2), nulle pour le circuit paradoxal | on jette les essais incohérents |

---

## 3. Ce que chaque expérience prouve — et ne prouve pas

| N° | Prouve | Ne prouve PAS |
|---|---|---|
| 01 | une horloge plus haute avance, de g·Δh/c² | qu'on puisse inverser l'ordre des événements ; le facteur 87 660 est 10¹⁹ fois au-delà de l'effet, à 1 m, des masses retenues (3,9 × 10¹² à 1,0 × 10¹³ kg) |
| 02 | on mesure des différences d'horloges plus des retards ; l'asymétrie est invisible de l'intérieur | un temps absolu ; un signal vers le passé (les 60 ns d'OPERA étaient un connecteur) |
| 03 | G ; les « anomalies de gravité » près d'un aimant sont magnétiques | que l'énergie électromagnétique ne gravite pas (elle gravite, à 10⁻²⁴ N) ni qu'elle gravite davantage |
| 04 | g varie avec l'altitude, les marées, les masses ; les capteurs grand public sont 10⁴–10⁵ fois trop peu résolus | qu'un instantané de gravité « verrouille » un lieu ou une époque |
| 05 | la force de Casimir existe et se mesure | qu'on dispose d'énergie négative exploitable |
| 06 | horizon et ergorégion existent pour des ondes dans un écoulement | quoi que ce soit sur la gravitation, la dilatation du temps ou des courbes temporelles fermées |
| 07 | un champ oscillant ou le diamagnétisme confinent un petit objet | qu'on puisse « loger » une singularité (Q/m 10⁶ fois trop faible dans le meilleur cas) |
| 08 | un gradient d'indice courbe visiblement un faisceau dans un liquide ; dans l'air la réfraction est bornée à ≈ 1° | que la photo C204-DOC-012 ait été obtenue par réfraction : dans l'air, ni la gravité ni la réfraction n'expliquent ≈ 55° ; le procédé n'est pas identifié |
| 09 | la lumière mesure la rotation d'un instrument | l'entraînement des référentiels (10⁻²¹ rad/s pour le spin, ≤ 5 × 10⁻¹⁴ rad/s pour une paire en orbite), encore moins un « champ de Kerr » de laboratoire |
| 10 | les corrélations quantiques sont celles de la théorie ; pas de signal rétrograde | la rétrocausalité, l'existence de courbes temporelles fermées, le passage entre « lignes d'univers » |
| 11 | le fond radiatif est mesurable ; une fuite X de 10⁻⁷ W serait vue | l'absence de tout rayonnement exotique non détecté par l'instrument |
| 12 | qu'un dispositif **candidat** produit ou non une anomalie mesurable au-dessus de seuils chiffrés | quoi que ce soit sur l'objet de 2000-2001, indisponible ; un voyage temporel — **aucune voie de mesure n'y donne accès** |

---

## 4. Réponse à la question Q10

> **Q10 — « Peut-on construire une version expérimentale permettant de tester certaines hypothèses ? »**

**Oui, à condition de préciser ce que l'on construit et ce que l'on teste.**

1. **On ne peut pas construire une version, même réduite, de la machine revendiquée.** Ses éléments centraux
   (micro-trous noirs de 3,9–5,1 × 10¹² kg chacun, leur capture, leur confinement, leur charge) n'ont aucune
   contrepartie réalisable, et les phénomènes relativistes qu'ils produiraient réellement à l'échelle du mètre sont
   de 12 à 19 ordres de grandeur sous les effets revendiqués de courbure de la lumière et de marche du temps (§2.1). Il n'existe pas d'« effet réduit » à mettre en
   évidence : un analogue hydraulique ou un piège à poussières ne sont pas des maquettes à l'échelle.
2. **On peut construire un banc de mesure** — le « banc C204 de substitution » (fiche EXP-12) : un coffre
   instrumenté (accéléromètres et pesée, horloge atomique compacte ou rubidium contre GPSDO, magnétomètres,
   compteurs de rayonnement, thermométrie et bilan de puissance, faisceau laser de contrôle), enregistré sur
   **trois chaînes redondantes de conceptions différentes avec vote 2-parmi-3**, exploité selon un **protocole en
   aveugle pré-enregistré** (clés tirées au sort par un tiers, leurre, injections de signaux connus).
   **Ce banc ne réfute rien de l'objet de 2000-2001, qui n'est pas disponible ; il s'applique à un dispositif
   candidat présenté par un promoteur.**
3. **Hypothèses testables** sur un tel dispositif, aux seuils du protocole réellement décrit (64 cycles de 100 s ;
   seuil statistique 1,36σ par cycle, systématiques ajoutées ; valeurs N2, et N1 entre parenthèses) : anomalie de
   pesanteur 4 × 10⁻⁴ m/s² (1,5 × 10⁻² m/s²), soit une masse cachée de 6 × 10⁶ kg à 1 m (2 × 10⁸ kg ; 1,7 × 10³ kg
   avec un gravimètre de terrain) ; masse de l'appareil 0,14 kg (0,7 kg) ; marche d'une horloge embarquée
   1,4 × 10⁻¹¹ (1,4 × 10⁻⁷) ; champ magnétique 66 nT (410 nT) ; rayonnement 0,027 µSv/h (0,068 µSv/h) ;
   échauffement 0,14 K, 7 W (0,27 K, 27 W) ; déviation d'un faisceau 16 µrad (66 µrad).
4. **Hypothèses non testables par ce banc** — à dire explicitement : les effets relativistes réels des masses
   retenues (6–8 × 10⁻¹⁵ ; 2–3 × 10⁻¹⁴ rad ; 10⁻²¹ à 5 × 10⁻¹⁴ rad/s), et *a fortiori* le « déplacement temporel »
   lui-même, pour lequel aucune grandeur mesurable n'est définie par les documents. Les grandeurs revendiquées
   **pendant le déplacement** (1,5–2 g, 10 ans par heure) ne sont observables que si l'appareil « fonctionne » en
   restant dans le laboratoire — ce qui serait déjà une réfutation d'un autre ordre.
5. **Critères de décision fixés à l'avance, avec le contraste adapté à chaque grandeur** : pour une grandeur
   commutable ou revendiquée pendant le fonctionnement, différence **marche − arrêt** ; pour une grandeur
   **permanente** selon le récit (masse, pesanteur propre, rayonnement et puissance des singularités, qui ne
   « s'éteignent » pas), différence **dispositif − leurre**, ou **mesure absolue rapportée au fond** — une
   différence marche − arrêt nulle n'y réfuterait rien. L'implication est réfutée si l'écart est compatible avec
   zéro et borné au moins 100 fois sous le signal impliqué ; une « anomalie » n'est retenue que si elle dépasse le
   seuil corrigé (5,44σ par comparaison pour 11 comparaisons) sur deux capteurs de conception différente, suit la
   clé aléatoire, disparaît avec le leurre et survit à la permutation des capteurs. **Même alors, il s'agirait
   d'une anomalie instrumentale à expliquer, pas d'un voyage dans le temps.**
6. **Coût** : ≈ 490 € (N1), ≈ 8–12 k€ (N2), compléments ≈ 230 k€ (N3). Durée : une semaine de caractérisation,
   deux jours d'essai (mesures absolues, série dispositif − leurre, série marche − arrêt), une semaine d'analyse.

En parallèle, les expériences EXP-01 à EXP-11 testent les **phénomènes voisins** invoqués par le vocabulaire des
documents (dilatation du temps, horizon, Kerr, confinement, rayons X) et montrent, chiffres à l'appui, à quelle
distance ils se trouvent des affirmations.

---

## 5. Sécurité — synthèse des prescriptions

| Risque | Règle appliquée dans tout le programme |
|---|---|
| Rayonnements ionisants | **aucune source radioactive ajoutée ni manipulée**, à aucun niveau ; l'expérience de Pound-Rebka (source gamma) est citée mais exclue. Précision : un étalon à rubidium du commerce contient du ⁸⁷Rb, isotope naturel très faiblement radioactif (≈ 3 Bq par mg, scellé, hors réglementation) ; le césium 133 est stable |
| Haute tension | interdite au niveau N1 ; en N2, uniquement matériel pédagogique certifié à courant limité (≤ 0,5 mA ; énergie stockée ≪ 0,35 J), capot interverrouillé, encadrement ; sources de type transformateur d'enseigne, four à micro-ondes, bobine d'allumage **proscrites** |
| Lasers | classe 2 au plus (< 1 mW visible) hors laboratoire ; sources fibrées de classe 1 ; toute source de classe 3B (bancs à paires de photons) en laboratoire seulement |
| Aimants NdFeB | pincement, éclats, stimulateurs cardiaques : gants, lunettes, un aimant à la fois |
| Plomb | masses gainées, pas d'usinage, lavage des mains |
| Batteries, charges lourdes, route | arrimage, fusibles, ventilation (EXP-01-N2) |
| Eau et électricité | séparation, différentiel 30 mA (EXP-06) |
| Dispositif candidat inconnu (EXP-12) | description des dangers exigée, inspection préalable, essai à distance, arrêt d'urgence, débit de dose surveillé |

Les valeurs limites de courant, de charge et d'énergie citées (famille de normes CEI 61010) sont données de
mémoire : **à relire dans l'édition en vigueur avant tout montage**.

---

## 6. Références et statut de vérification

`REFERENCES.md` : 150 notices bibliographiques confrontées à l'API Crossref (premier auteur, année, revue, volume,
pages, DOI tirés de la notice et non de notre mémoire) ; journal complet dans `verification_refs/`. Relus
directement en ligne : la page « Project GREAT » (22 ns prédits, ≈ 23 ns observés), les tables NIST de
coefficients d'atténuation, cinq résumés arXiv. Huit sources classiques ou normatives sont citées **sans**
vérification en ligne et marquées comme telles. Une liste des affirmations chiffrées données de mémoire
(performances de capteurs et d'horloges, énergies de grands aimants, détails d'expériences) figure en fin de
`REFERENCES.md`. **Aucune référence n'a été inventée.**

Vérification ≠ relecture intégrale : Crossref atteste l'existence et l'identité d'un article, pas chaque chiffre
que nous en tirons.

---

## 7. Cohérence avec les autres équipes

- **Valeurs communes retenues** (Red Team n° 2, §2.1 ; dossier v1.2, errata E2, E12, E14, E15) et reprises ici :
  3,9–5,1 × 10¹² kg par singularité ; charge tenable ≈ 6 e (borne 137 e) contre 379 C à l'extrémalité ; débit de
  dose des γ primaires 3,3–3,8 × 10³ Gy/s à 1 m et ≈ 3,8 × 10² Gy/s à 3 m (notre recalcul : 3,44 × 10³ et
  3,82 × 10²) ; entraînement des référentiels ≤ 5 × 10⁻¹⁴ rad/s (terme orbital ; notre recalcul : 4,7 × 10⁻¹⁵ pour
  2 × 10¹² kg, 4,3 × 10⁻¹⁴ pour 2 × 4,4 × 10¹² kg, 5,4 × 10⁻¹⁴ pour 2 × 5,1 × 10¹² kg à 0,30 m) ; coffre L = 0,85 m,
  1,07 m², 190–310 W pour 38–49 °C.
- **Équipe A** : la photographie dite « du laser » est désormais archivée (C204-DOC-012) ; EXP-08 la confronte aux
  ordres de grandeur et rejoint le constat I-11 (aucune explication ordinaire n'est démontrable ; l'explication
  gravitationnelle est exclue).
- **Équipes C, D, G** : `tableau_experiences.csv` et les JSON de `calculs/resultats/` sont directement
  réutilisables (seuils de détection, bilans thermiques et radiologiques).

---

## 8. Limites et points ouverts

1. **Aucune expérience n'a été réalisée** : ce rapport livre des protocoles et des signaux *calculés*. Les
   figures sont des calculs illustratifs, pas des mesures.
2. Les **performances d'instruments** (horloges, capteurs MEMS, gravimètres, compteurs) sont des ordres de grandeur
   de type fiche technique, cités de mémoire : confiance moyenne ; à remesurer en phase de caractérisation.
3. Les **débits de dose** de EXP-11 sont des kermas sans facteur d'accumulation ni cascade électromagnétique :
   justes à un facteur de quelques unités ; ils sont donnés en deux lectures qui diffèrent d'un facteur 24 (littérale ;
   γ primaires de Hawking, borne basse), pour une conclusion qui tient à plus de dix ordres de grandeur dans les deux cas.
4. Les **modèles hydrodynamiques** de EXP-06 sont idéalisés ; les deux lois d'échelle du ressaut circulaire
   diffèrent d'un facteur ≈ 4 (désaccord publié) : la mesure tranchera.
5. Les **coûts** sont indicatifs (2026) et supposent du matériel d'occasion pour les horloges.
6. Le test nul électromagnétique (EXP-03) ne peut fournir qu'une borne ≈ 10¹² fois au-dessus de la prédiction de
   la relativité générale : il enseigne les artefacts, il ne teste pas la théorie.
7. La valeur « 14 ± 8 % » de superradiance (version publiée de Torres et al. 2017) et les domaines de distance
   des expériences de Casimir n'ont pas été relus dans les articles.
8. **EXP-12 ne porte que sur un dispositif candidat** : rien n'y est établi sur l'objet de 2000-2001. Les résolutions
   par voie sont des estimations, non des caractérisations ; les systématiques thermiques sont des ordres de grandeur.
9. L'angle (≈ 55°) et le rayon de courbure (~10 cm) lus sur C204-DOC-012 sont une lecture visuelle de confiance
   faible ; le terme orbital d'entraînement suppose une orbite libre que les documents ne décrivent pas.
10. EXP-10 : les expériences proprement quantiques relèvent du niveau N3 ; la version N1 est une analogie
   classique et doit être présentée comme telle.

---

## 9. Livrables

```
07_experiences/
├── RAPPORT_F.md                      ← ce rapport
├── REFERENCES.md                     ← 150 références vérifiées + sources hors Crossref + réserves
├── tableau_experiences.csv           ← 41 lignes (expérience × niveau) : coût, durée, signal, bruit, S/B, faisabilité, sous-système
├── fiches/
│   ├── EXP-01_dilatation_du_temps_horloges.md
│   ├── EXP-02_transfert_de_temps.md
│   ├── EXP-03_cavendish_test_nul_electromagnetique.md
│   ├── EXP-04_gravimetrie_locale_VGL.md
│   ├── EXP-05_effet_casimir.md
│   ├── EXP-06_gravite_analogue_eau.md
│   ├── EXP-07_confinement_piege_de_Paul_levitation.md
│   ├── EXP-08_deviation_de_la_lumiere.md
│   ├── EXP-09_sagnac_et_lense_thirring.md
│   ├── EXP-10_optique_quantique_et_causalite.md
│   ├── EXP-11_rayonnement_bruit_de_fond.md
│   └── EXP-12_banc_d_essai_C204_de_substitution.md
├── calculs/
│   ├── constantes.py                 ← constantes CODATA 2018, utilitaires
│   ├── calc01_dilatation_horloges.py … calc12_banc_essai.py   (12 scripts exécutés)
│   ├── resultats/calcNN_*.txt + .json                          (sorties texte et données)
│   └── figures/calcNN_*.png                                    (12 figures, légendées « calcul illustratif »)
├── outils/
│   ├── verif_references_crossref.py  ← interrogation de Crossref (aucune donnée personnelle transmise)
│   ├── generer_references.py         ← produit REFERENCES.md
│   └── generer_tableau.py            ← produit tableau_experiences.csv
└── verification_refs/
    └── crossref_resultats.json / .txt ← journal brut des réponses (données non fiables : lire avec python -I)
```

Reproduire : `cd calculs && ../../.venv/bin/python calcNN_….py` (chaque script réécrit ses sorties).

---

## 10. Journal des corrections post-validation

Corrections issues de la validation contradictoire (`08_red_team/CORRECTIONS_A_APPLIQUER.md`, §6, n° 51 à 56 ;
`08_red_team/RAPPORT_RED_TEAM_2.md`, §2 et §7), appliquées le 10 novembre 2026. **Toutes sont acceptées ; aucune
n'est contestée** : nous avons recalculé chaque chiffre proposé avant de l'adopter (colonne « contrôle »).
Aucun classement « testable / non testable » ne change ; aucune conclusion d'ensemble n'est renversée.

| N° | Gravité | Correction | Contrôle par nos scripts | Fichiers modifiés |
|---|---|---|---|---|
| 51 | importante | Masse : « 10¹¹–10¹² kg » → **3,9–5,1 × 10¹² kg par singularité** (7,8 × 10¹² à 1,0 × 10¹³ kg pour les deux). Marge « masse de l'appareil » d'EXP-12 : **2 × 10¹³**. | linéarité en M vérifiée sur toutes les grandeurs ; marge 1,6–2,0 × 10¹³ | `constantes.py`, `calc01`, `04`, `06`, `07`, `08`, `09`, `12` ; fiches 01, 03, 04, 06, 07, 08, 09, 12 ; rapport §0.3, §0.6, §2.1, §2.2, §3, §4 |
| 52 | importante | Débit de dose en **deux lectures** : littérale (400 MW entièrement en X de 100 keV : 9,0 × 10³ Gy/s à 3 m) et **spectre de Hawking** (γ primaires, 7,5 % de la puissance, ~15 MeV, borne basse). | recalcul : **3,44 × 10³ Gy/s à 1 m, 3,82 × 10² Gy/s à 3 m** (proposé : ≈ 3,5 × 10³ et ≈ 3,8 × 10²) ; rapport A/B = 24 ; coefficients NIST à 15 MeV relus en ligne | `calc11` (réécrit, figure refaite), `calc12` ; fiches 11, 12 ; rapport §0.5, §2.2, §8 |
| 53 | importante | Critère d'EXP-12 : « marche − arrêt » invalide pour les grandeurs **permanentes** → **dispositif − leurre** ou **mesure absolue** pour la masse, la pesanteur propre, le rayonnement et la puissance des singularités ; phrase ajoutée : *le banc ne réfute rien de l'objet de 2000-2001, qui n'est pas disponible ; il s'applique à un dispositif candidat*. Ajouts liés (§7.3 du rapport de la Red Team) : origine de chaque signal (texte ou déduction de l'institut) ; grandeurs revendiquées seulement pendant le déplacement. | citation du corpus vérifiée (texte intégral, ligne 4081 : le trou noir ne s'éteint pas ; lignes 129 et 195 : l'unité, si) | `calc12` (régime, contraste et origine par voie) ; fiche 12 (§1, §2, §5, §6, §7, §10) ; fiche 11 ; rapport §0.4, §3, §4.2 à §4.5 |
| 54 | importante | Entraînement des référentiels : « ≤ 3,3 × 10⁻²² rad/s » → **spin seul** (3,3 × 10⁻²² pour 10¹² kg ; 5,0–8,6 × 10⁻²¹ pour 3,9–5,1 × 10¹² kg) ; **jusqu'à 5 × 10⁻¹⁴ rad/s pour une paire en orbite** ; écart au gyrolaser géant : 1 à 9 ordres de grandeur selon le terme. | recalcul du terme orbital, L = (M/2)√(2GMd) : 4,7 × 10⁻¹⁵ (2 × 10¹² kg, 0,30 m), 4,3 × 10⁻¹⁴ (2 × 4,4 × 10¹² kg), **5,4 × 10⁻¹⁴** (2 × 5,1 × 10¹² kg) ; 2,1–3,1 × 10⁻¹⁴ à l'entraxe documentaire de 0,098 m | `calc09` (figure refaite), `calc12` ; fiches 09, 12 ; rapport §0.3, §2.1, §3 |
| 55 | mineure | Ambiguïté « 100 cycles » / « 64 cycles » levée : seuils donnés **pour 64 cycles** (1,36σ par cycle), les anciens seuils « 100 cycles » (= 100 paires) retirés ; **dérive thermique des accéléromètres budgétée** ; valeurs N1 réalistes : **20 µrad** et **200 nT** (au lieu de 5 µrad et 20 nT). | seuil total = √[(1,36σ)² + (3 × systématique)²] | `calc12` (figure refaite) ; fiche 12 §6 ; rapport §4.3 ; tableau CSV |
| 56 | mineure | Ligne « 300–500 MW » harmonisée sur la fourchette (4800–5450 K sur 10 m² ; 116–193 kg/s) ; surface du coffre **1,07 m²** (L = 0,85 m) → **190–310 W** pour 38–49 °C (au lieu de 1,8 m² et 320–520 W). | S = 2(LP + LH + PH) = 1,075 m² ; h·S·ΔT = 193–312 W | `constantes.py`, `calc11`, `calc12` ; fiches 11, 12 ; rapport §2.2 |

**Chiffres qui ont changé** (ancienne → nouvelle valeur) :

| Grandeur | Avant | Après |
|---|---|---|
| Masse impliquée par 300–500 MW | 10¹¹–10¹² kg | 3,9–5,1 × 10¹² kg par singularité ; 7,8 × 10¹² – 1,0 × 10¹³ kg la paire |
| Décalage d'horloge à 1 m | 7,4 × 10⁻¹⁶ | 2,9–3,8 × 10⁻¹⁵ (une) ; 5,8–7,6 × 10⁻¹⁵ (paire) |
| Rapport du taux revendiqué (87 660) à cet effet | 1,2 × 10²⁰ | 1,2–3,0 × 10¹⁹ |
| Déviation de la lumière à 1 m | 3 × 10⁻¹⁶ – 3 × 10⁻¹⁵ rad | 1,2–1,5 × 10⁻¹⁴ (une) ; 2,3–3,0 × 10⁻¹⁴ rad (paire) |
| Pesanteur à 1 m | 6,7–67 m/s² | 260–340 m/s² (27–35 g) ; 520–680 m/s² pour la paire |
| Portée de détection : smartphone / gravimètre | 26–82 m / 5–16 km | 160–185 m / 32–37 km |
| Entraînement des référentiels à 1 m | ≤ 3,3 × 10⁻²² rad/s | 5,0–8,6 × 10⁻²¹ (spin) ; ≤ 5,4 × 10⁻¹⁴ rad/s (paire en orbite) |
| Charge extrémale ; masse d'électrons correspondante | 86 C ; 4,9 × 10⁻¹⁰ kg | 379 C (4,4 × 10¹² kg) ; 2,2 × 10⁻⁹ kg — Q/m inchangé |
| Débit de dose à 3 m | 9,0 × 10³ Gy/s (sans qualification) | 9,0 × 10³ (lecture littérale) ; 3,8 × 10² Gy/s (γ de Hawking) ; dose létale en 0,44 ms / ≈ 10 ms |
| Blindage (γ de Hawking) | — | 47 cm de plomb, 8,7 t |
| Surface du coffre ; puissance pour 38–49 °C | 1,80 m² ; 320–520 W | 1,07 m² ; 190–310 W |
| Corps noir évacuant 300–500 MW sur 10 m² ; eau vaporisée | 5150 K ; 154 kg/s (400 MW seul) | 4800–5450 K ; 116–193 kg/s |
| Marge « masse » d'EXP-12 | 2 × 10¹¹ | 2 × 10¹³ |
| Seuils du banc (pesanteur ; champ ; dose ; faisceau), N2 | 1,4 × 10⁻⁴ m/s² ; 14 nT ; 0,035 µSv/h ; 5 µrad (« 100 cycles ») | 4,1 × 10⁻⁴ m/s² ; 66 nT ; 0,027 µSv/h ; 16 µrad (64 cycles, systématiques comprises) |
| Masse cachée exclue à 1 m (MEMS / gravimètre) | 2 × 10⁶ kg / 530 kg | 6 × 10⁶ kg / 1,7 × 10³ kg |
| Résolutions N1 (faisceau ; champ magnétique) | 5 µrad ; 20 nT | 20 µrad ; 200 nT |

**Alignements supplémentaires sur le dossier de base v1.2** (non demandés par les n° 51 à 56, signalés pour contrôle) :

1. **Photographie « du laser »** (erratum E16 : désormais archivée, C204-DOC-012). La version 1 la disait absente
   et présentait le gradient d'indice comme « explication ordinaire quantitativement suffisante ». C'était trop
   fort : pour la courbure apparente (≈ 55° sur ~10 cm, lecture de confiance faible), la réfraction **dans l'air**
   est bornée à 0,4–1,3° et n'explique pas plus l'image que la gravitation (4,6 × 10¹⁶ g requis). Fiche EXP-08
   (§1, §6, §10 à §12), `calc08` (§6, figure) et rapport (§0.7, §3) corrigés ; le procédé de l'image reste non identifié.
2. **Charge tenable** (erratum E14) : « ≈ 137 charges » → « ≈ 6 e en valeur quadratique moyenne, borne ≈ 137 e » ;
   champ de sustentation 2 × 10³⁰ – 5 × 10³¹ V/m (fiche EXP-07, `calc07`).
3. **Cône de DOC-009** (erratum E7) : demi-angle hypothétique de 30° remplacé par l'ouverture relevée ≈ 78°
   (concentration × 9,0 au lieu de × 14,9) ; rayonnement de Hawking « isotrope » → « isotrope sans rotation, non
   collimatable » (erratum E5) (fiche EXP-11, `calc11`).
4. **Rubidium** (réserve du §7.1 de la Red Team) : la règle « aucune source radioactive » s'entend « aucune source
   ajoutée ni manipulée » ; un étalon à rubidium contient du ⁸⁷Rb naturel (≈ 3 Bq par mg, calculé) (fiche EXP-01
   §9, rapport §0.10 et §5).

Fichiers régénérés : les 12 sorties `calculs/resultats/` (txt et json), les figures `calc08`, `calc09`, `calc11`,
`calc12` (et les autres à l'identique), `tableau_experiences.csv` (41 lignes), `REFERENCES.md`.

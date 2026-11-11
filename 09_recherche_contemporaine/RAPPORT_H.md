# RAPPORT H — Recherche scientifique contemporaine (2001 → novembre 2026) confrontée à la « C204 »

Équipe H — programme C204 — version 1.1 du 10 novembre 2026 (version 1 + corrections de la validation contradictoire,
voir §18).
Fichiers associés : `bibliographie_verifiee.csv` (références et pages consultées), `journal_verification.md`
(requêtes, échecs, corrections), `RECHERCHES_SUPPLEMENTAIRES.md` (livrable n° 13), `outils/` (scripts reproductibles),
`donnees_brutes/` (réponses des API, données non fiables, jamais exécutées).

> Rappel de la règle d'or : aucune affirmation attribuée à « John Titor » n'est tenue pour vraie. Ce rapport ne
> cherche pas à « faire marcher » la C204 ; il recense ce que la science publiée entre 2001 et novembre 2026
> **éclaire**, **corrige** ou **invalide** dans les affirmations du dossier de base (§4, §5, errata §6 bis).

---

## 0. Résumé exécutif

1. **Aucun micro-trou noir n'a été produit ni observé**, ni au LHC (limites jusqu'à 8–11 TeV, 2026), ni dans le
   ciel (taux d'explosion local < 181 pc⁻³·an⁻¹, LHAASO 2025). Les objets qu'un collisionneur pourrait produire dans
   les scénarios à dimensions supplémentaires pèseraient ~10⁻²³ kg et vivraient ~10⁻²⁶ s : 35 ordres de grandeur
   séparent ces objets des ~4–5×10¹² kg qu'exigent les « 300–500 MW » revendiqués. **Invalide** l'origine « CERN ».
2. **La chronologie réelle contredit l'annonce** : fin 2000 le LEP est arrêté, le LHC ne donne son premier faisceau
   qu'en 2008 et ses premières collisions à 7 TeV qu'en 2010 ; aucune « percée » de ce type en 2001-2003.
3. **L'intérieur de Kerr comme « passage » : non établi, défavorisé** (confiance moyenne). La géométrie
   extérieure de Kerr est aujourd'hui confirmée par les ondes gravitationnelles (GW250114, 2025) et l'imagerie
   EHT. Pour l'intérieur, il faut distinguer : *démontré* — l'horizon de Cauchy de Kerr est stable au sens C⁰,
   la métrique perturbée s'y prolonge continûment (Dafermos-Luk 2017/2025), ce qui n'implique ni prolongement
   régulier ni prolongement unique ; *suggéré* par cette preuve — cet horizon est génériquement une singularité
   nulle faible ; *calculé* — les flux quantiques y divergent génériquement (Zilberman et al. 2022). La
   relativité générale ne prédit donc pas ce qu'il y a « derrière l'anneau », seule région de la solution
   analytique à contenir des courbes temporelles fermées. Comme procédé contrôlé à l'échelle d'une machine, le
   principe revendiqué reste contredit (points 1 et 4).
4. **Toute machine temporelle de taille finie, sans singularité de courbure, exige de l'énergie négative**
   (Hawking 1992 : violation de la condition d'énergie faible moyennée sur l'horizon de Cauchy) ; les théorèmes
   récents (ANEC démontrée en théorie des champs, 2016-2017 ; ANEC achronale) et les inégalités quantiques
   interdisent les quantités nécessaires. Les trous de ver traversables cohérents (Gao-Jafferis-Wall 2017 ;
   Maldacena-Milekhin-Popov 2018) sont explicitement **incapables de violer la causalité**.
5. **Les « voyages dans le temps » de laboratoire sont des simulations** (circuits à post-sélection, interrupteur
   quantique, inversion d'état sur processeur) : aucune information n'y remonte le temps.
6. **Les sous-systèmes « classiques » du récit sont les seuls à avoir un équivalent réel** — et celui-ci a
   énormément progressé : horloges optiques à 10⁻¹⁹ (2026), décalage gravitationnel résolu sur 1 mm (2022),
   horloge nucléaire au thorium (2024-2026), gravimètres quantiques embarqués et navigation par carte de gravité
   (2026). Ils montrent aussi, par la mesure, que la gravité dilate le temps de 1,1×10⁻¹⁶ par mètre à la surface
   de la Terre : vingt ordres de grandeur en dessous des « 10 ans par heure ».
7. **Terminologie** : « sinusoïde de Tipler » est absent de la littérature ; la seule occurrence trouvée en texte
   intégral (INSPIRE-HEP) est une prépublication de 2010, non publiée en revue, qui reprend le vocabulaire du
   récit *après coup* (classement [INT]).

Bilan bibliographique : voir §16 et `journal_verification.md`.

---

## 0 bis. Méthode, conventions, limites

- **Étiquettes** du dossier de base : [DOC], [DÉD], [HYP], [INT], [VÉR]. Statut physique : Démontré / Théoriquement
  possible / Spéculatif / Contredit les connaissances actuelles. Confiance : élevée / moyenne / faible.
- **Portée des caractérisations** : quand seul le titre d'un article a pu être contrôlé (notices Crossref sans
  résumé), la description qualitative de son contenu repose sur ma connaissance de la littérature ; les valeurs
  chiffrées correspondantes sont alors marquées « (de mémoire) ».
- **Vérification** : chaque référence scientifique citée ici par une clé entre crochets, par exemple [DL17], figure
  dans `bibliographie_verifiee.csv` avec auteurs, titre exact, année, revue, DOI et/ou identifiant arXiv, URL
  d'API interrogée et statut. Une référence n'est « vérifiée » que si l'API (arXiv, Crossref) a renvoyé un titre
  et un auteur concordant avec ce qui était attendu. Les valeurs chiffrées attribuées à un article proviennent de
  son **résumé** tel que renvoyé par l'API arXiv, sauf mention « (de mémoire) ».
- **Ce qui n'est pas vérifié** est signalé par « (de mémoire, non vérifié dans cette session) ». Ces passages ne
  portent aucune conclusion du rapport.
- **Limites** : (i) je n'ai lu que les résumés, pas le texte intégral des articles (sauf une prépublication,
  §3.4) ; (ii) les résultats 2025-2026 sont souvent des prépublications non encore évaluées ; (iii) les calculs
  d'ordre de grandeur ci-dessous sont les miens et doivent être recoupés avec ceux des équipes B et D.

### Ordres de grandeur re-dérivés indépendamment (cohérents avec l'errata E1-E4 et E14 du dossier)

Reproductibilité : dans la version 1, ce tableau provenait de calculs interactifs non conservés (remarque de la
Red Team). Il est désormais adossé au script `outils/ordres_de_grandeur.py`, dont la sortie est conservée dans
`donnees_brutes/ordres_de_grandeur.txt` ; les valeurs de la version 1 ont été retrouvées à l'identique, sauf la
ligne « charge », corrigée (§18).

Constantes CODATA (G = 6,674 30×10⁻¹¹ ; c = 2,997 924 58×10⁸ ; ħ = 1,054 571 8×10⁻³⁴ SI).

| Grandeur | Équation | Valeur | Remarque |
|---|---|---|---|
| Masse de Planck | M_P = √(ħc/G) | 2,18×10⁻⁸ kg = 1,22×10¹⁹ GeV | masse minimale d'un trou noir en gravité 4D |
| Énergie LHC (Run 3) | — | 13,6 TeV = 2,2×10⁻⁶ J ≡ 2,4×10⁻²³ kg | E_P / E_LHC ≈ 9×10¹⁴ |
| Puissance de Hawking totale | P = 5,34×10²⁵ f(M)/M² g·s⁻¹ × c², f ≈ 1,57 (γ, 3 ν, e±) | P ≈ 7,5×10³³ W·kg² / M² | coefficient attribué à [MacGibbon91] **de mémoire** : il ne figure pas dans le résumé de l'article, qui porte sur M ≲ 5×10¹⁴ g (classé « introuvable » par la Red Team) ; recoupé à 1,3 % avec les coefficients de Page [Page76a] ; ≈ 21 × la formule « photons, corps noir » |
| Masse pour 300–500 MW | M = √(7,5×10³³/P) | 5,0–3,9×10¹² kg par singularité | kT = 2,1–2,7 MeV ; r_s = 7,4–5,8 fm ; durée de vie ~10¹³ ans |
| Répartition de la puissance | parts de Page (γ 16,7 %, gravitons 1,9 %, ν 81,4 % pour 4 espèces) ramenées à 6 espèces de ν, plus e± | ν ≈ 55 % ; e± ≈ 36 % ; γ ≈ 8 % ; gravitons ≈ 1 % | coefficients cités de mémoire ; les photons primaires ne portent qu'environ 30 MW sur 400 |
| Pic d'émission photonique | E ≈ 6 kT (spin 1) | 12–16 MeV | gamma, **pas** rayons X |
| Trou noir « à rayons X » | kT = 10 keV | M ≈ 1×10¹⁵ kg, P ≈ 4 kW | incompatible avec 300–500 MW |
| Pesanteur d'une singularité à 1 m | g = GM/r² | 26–34 g₀ | contre « 1,5–2 g » revendiqués (errata E1) |
| Énergie de masse de 4,5×10¹² kg | E = Mc² | 4,0×10²⁹ J | ≈ 7×10⁸ ans de consommation mondiale d'énergie primaire (~6×10²⁰ J/an) |
| Charge extrémale (4,5×10¹² kg) | Q = M√(4πε₀G) | 388 C = 2,4×10²¹ e | champ à l'horizon ≈ 2×10²³ fois le champ critique de Schwinger (indicatif : la formule de type Schwinger ne régit la perte de charge qu'au-dessus de 10¹⁷ g [Gibbons75]) |
| Charge réellement portée (errata E14) | valeur quadratique moyenne des fluctuations de charge [Page77] ; borne d'ordre de grandeur Zα ≈ 1 (instabilité du vide autour d'une charge quasi ponctuelle) | **≈ 6 e** (6,14 e quand GMμ/ħc → 0 ; ici GMμ/ħc ≈ 0,009) ; **borne ~137 e** | Q/Q_max ≈ 2×10⁻²¹ (6 e) à 6×10⁻²⁰ (137 e) ; r₋ ~ 10⁻⁵⁶ à 10⁻⁵³ m, très en dessous de la longueur de Planck : l'horizon interne est indiscernable de r = 0. Le critère e·Q/(4πε₀ r_s) < m_e c² (≈ 2 e) donné en version 1 est un ordre de grandeur de notre part, dépendant de la masse, peu adapté quand r_s ≪ ħ/m_e c, et **absent de Gibbons (1975)** |
| Décalage gravitationnel terrestre | g/c² | 1,09×10⁻¹⁶ par m | mesuré sur 1 mm [Bothwell22] |
| Potentiel d'une masse donnant 2 g à 1 m | GM/(rc²) | 2,2×10⁻¹⁶ | à comparer au facteur 87 660 (10 ans/h) qui exige 1 − r_s/r = 1,3×10⁻¹⁰ |
| Signal gravimétrique de 2 × 4,5×10¹² kg | a = GM/r² | 6×10⁻⁴ m/s² à 1 km ; 6×10⁻⁶ à 10 km ; 6×10⁻⁸ (6 µGal) à 100 km | à comparer à ~10⁻⁸ m/s² de résolution |

Confiance : élevée sur les ordres de grandeur ; moyenne sur le troisième chiffre significatif (facteurs de corps
gris cités de mémoire).

---

## 1. Micro-trous noirs en accélérateur, LHC, trous noirs primordiaux

### 1.1 État de l'art

**Pourquoi un collisionneur ne fabrique pas de trou noir en gravité ordinaire.** En relativité générale à quatre
dimensions, un trou noir ne peut pas être plus léger que la masse de Planck (2,2×10⁻⁸ kg, soit 1,2×10¹⁹ GeV) :
le LHC est 9×10¹⁴ fois en dessous. La seule voie théorique vers une production en accélérateur est l'abaissement
de l'échelle de Planck vers le TeV par des dimensions supplémentaires étendues [ADD98] ou courbées [RS99]. L'idée
que des trous noirs deviendraient alors accessibles date de 1998-1999 [ADM98], [BF99] ; les deux articles qui ont
popularisé les « usines à trous noirs » [GT01], [DL01] sont déposés en juin 2001. La question des « scénarios
catastrophes » en accélérateur (trous noirs, strangelets) avait été traitée publiquement dès 1999 à propos du RHIC
[BJSW00]. [VÉR]

**Ce que seraient ces objets.** Masse de quelques TeV/c² (~10⁻²³ kg), rayon ~10⁻¹⁹ m, désintégration par
rayonnement de Hawking en ~10⁻²⁶ s en une dizaine de particules ; revues : [Kanti04], [Park12]. Les simulations
de relativité numérique confirment qu'une collision ultra-relativiste forme bien un horizon quand l'énergie est
confinée sous son rayon de Schwarzschild [EG02], [CP10], [EP13] — mais à des énergies transplanckiennes. Concentrer de la
lumière ne suffit pas non plus : les effets dissipatifs quantiques (création de paires) empêchent la formation
d'un horizon dans tout scénario réaliste [Kugel24].

**Recherches au LHC : aucune trace.** Première limite directe en 2010 (masse minimale 3,5–4,5 TeV) [CMS11] ;
à 13 TeV : [ATLAS16a], [ATLAS16b], [CMS17], trous noirs semi-classiques exclus jusqu'à 10,1 TeV [CMS18] ; analyse
de l'ensemble du Run 2 (138 fb⁻¹) : exclusion jusqu'à 8,4–11,4 TeV selon le modèle [CMS26] ; premiers résultats
du Run 3 à 13,6 TeV (164 fb⁻¹) : « trous noirs quantiques » exclus jusqu'à 9,4 TeV [ATLASQBH26] ; recherches en
dijets [ATLAS20]. [VÉR]

**Sûreté.** Le rapport du LSAG [LSAG08] (publié : [LSAGJPG]) et l'étude [GM08] concluent à l'absence de danger :
des collisions plus énergétiques ont lieu depuis des milliards d'années par rayons cosmiques sur la Terre, le
Soleil, les naines blanches et les étoiles à neutrons, dont la stabilité contraint tout scénario de trou noir
stable.

**Chronologie réelle du CERN** (sources : [LHCMachine], pages CERN listées dans le CSV, résumés des articles
cités) :

| Date | Fait |
|---|---|
| 2 nov. 2000 | arrêt définitif du LEP (collisionneur e⁺e⁻, 209 GeV atteints en 2000) ; le tunnel est réutilisé pour le LHC (page CERN consultée) |
| 2001-2008 | construction du LHC : **aucun collisionneur de haute énergie en service au CERN** |
| 10 sept. 2008 | premier faisceau ; 19 sept. 2008 : incident électrique, plus d'un an de réparations |
| 30 mars 2010 | premières collisions à 7 TeV ; données 2010 utilisées par [CMS11] |
| juillet 2012 | découverte du boson de Higgs [HiggsATLAS], [HiggsCMS] |
| 2015-2018 | Run 2 à 13 TeV ; 2022-2026 : Run 3 à 13,6 TeV |
| juillet 2026 | début du long arrêt LS3 (calendrier CERN d'octobre 2024) ; HL-LHC prévu vers juin 2030 |
| 22 mai 2026 | le Conseil du CERN met à jour la stratégie européenne : FCC-ee option préférée, décision visée d'ici 2028 |

**Trous noirs primordiaux (TNP).** Proposés par Hawking [Hawking71] et Carr-Hawking [CarrHawking74] ; ils
s'évaporeraient [Hawking74], [Hawking75]. Ceux de masse initiale ≲ 5×10¹⁴ g auraient déjà disparu ; les revues
[CKSY21], [CK20], [GK21], [Auffinger23] compilent les contraintes : nucléosynthèse, fond diffus, fonds gamma,
positons (raie à 511 keV [Laha19], Voyager 1 [BC19]), COMPTEL [Coogan21], microlentilles [Niikura19] ; une
« fenêtre astéroïdale » (≈10¹⁷–10²² g) reste ouverte pour la matière noire [MC19]. Recherches directes
d'explosions finales : Fermi-LAT < 7,2×10³ pc⁻³·an⁻¹ [Fermi18], HAWC < 3 400 [HAWC20], H.E.S.S. < 2 000
[HESS23], LHAASO < 181 pc⁻³·an⁻¹ [PBH2505] (prospective : [LHAASOsens24]). **Aucun TNP n'a jamais été détecté.**
Des interprétations spéculatives du neutrino de très haute énergie KM3-230213A [KM3NeT25] par l'explosion d'un
TNP ont été proposées et contestées [Baker25], [PBH2505b], [PBH2605]. L'hypothèse du « fardeau de mémoire »
[Dvali20], [Thoss24], [ADK24] suggère que l'évaporation pourrait ralentir après la mi-vie : spéculatif.

**Spectre et bilan d'un trou noir de ~10¹² kg.** Taux d'émission par espèce : [Page76a], [Page76b], [Page77] ;
jets de quarks et gluons, pour des températures de 0,02 à 100 GeV, donc au-dessus de la gamme considérée ici :
[MW90], [MacGibbon91] ; code public [BlackHawk]. Les particules émises **ne forment pas de photosphère** et
s'échappent librement [MCP08]. Un trou chargé perd spontanément sa charge par émission de particules : régime de
type Schwinger au-dessus de 10¹⁷ g, traitement distinct en dessous [Gibbons75], voir aussi [Zaumen74] ; pour un
petit trou chaud, la charge fluctue avec une valeur quadratique moyenne de 6,14 e dans la limite GMμ/ħc → 0
[Page77] (traitement moderne du régime quasi extrémal : [IT21], [BIPU24]) ; un trou en
rotation perd son moment cinétique plus vite que sa masse [Page76b], [TCH98] (exception théorique : avec des
champs scalaires seuls, a/M tendrait vers ≈ 0,555 [CHT97]). L'usage d'un trou noir
artificiel comme source d'énergie a été examiné sérieusement [CW09], qui le situe « à la limite du possible ».

### 1.2 Conséquence pour la C204

| Affirmation | Verdict | Justification | Confiance |
|---|---|---|---|
| Singularités « créées, capturées et nettoyées » dans un grand accélérateur circulaire (CERN) | **Invalide** — contredit les connaissances actuelles | 35 ordres de grandeur entre ce qu'un collisionneur pourrait produire (10⁻²³ kg, 10⁻²⁶ s, et seulement si l'échelle de Planck est au TeV, ce qu'excluent les limites jusqu'à ~10 TeV) et 4–5×10¹² kg ; énergie de masse requise 4×10²⁹ J | élevée |
| « Percée au CERN d'ici un an ou deux » (énoncé de mission ; à confirmer dans le corpus par l'Équipe A) | **Invalide** [VÉR] | pas de collisionneur de haute énergie au CERN entre novembre 2000 et 2008 ; aucun trou noir en seize ans de LHC | élevée |
| « Méthode » attribuée à la Z machine | **Invalide** | la Z machine de Sandia est une installation de puissance pulsée (striction axiale, physique des hautes densités d'énergie) [Sinars20] ; énergie stockée de l'ordre de la dizaine de MJ (de mémoire, non vérifié dans cette session), sans rapport avec 10²⁹ J ni avec la gravité | élevée |
| 300–500 MW ↔ singularités « lourdes, chaudes » | **Corrige** | physique correcte *en ordre de grandeur* pour un TNP de 4–5×10¹² kg (errata E2), mais incompatible avec 227 kg | élevée |
| Rayons X « évacués » par un cône ou une zone | **Invalide** | émission à 10–16 MeV (gamma), plus de la moitié de la puissance en neutrinos non blindables, e± ; pas de photosphère [MCP08] donc rien à « canaliser » ; un trou émettant en X (kT ~ 10 keV) pèserait 10¹⁵ kg et rayonnerait 4 kW | élevée |
| « Ajouter de la charge agrandit l'horizon interne » | **Corrige** | formellement exact dans Kerr-Newman (r₋ = M − √(M² − a² − Q²)) ; physiquement inapplicable : la charge d'un trou de cette masse fluctue autour de zéro, valeur quadratique moyenne ≈ 6 e [Page77] ; borne d'ordre de grandeur ~137 e (errata E14) ; soit Q/Q_max ≈ 10⁻²¹ à 10⁻¹⁹. Le critère e·Q/4πε₀r_s < m_e c² (2 à 3 e) de la version 1 était un ordre de grandeur de notre part, absent de Gibbons (1975) | élevée (ordre de grandeur) |
| Rotation entretenue (« top-spin ») | **Corrige** | un trou de Kerr isolé ralentit spontanément [Page76b], [TCH98] ; aucun moyen connu d'exercer un couple sur un objet neutre de 7 fm ; on ne peut pas dépasser l'extrémalité [SW17] | moyenne |
| « Si le confinement cède, la singularité s'évaporerait » | **Invalide** (et contradictoire, errata E9) | à 4–5×10¹² kg l'évaporation dure ~10¹³ ans : l'objet tomberait au centre de la Terre ; à l'inverse un trou de 227 kg s'évaporerait en ≈ 5×10⁻¹² s en libérant 2×10¹⁹ J | élevée |
| Disponibilité naturelle de tels objets | **Éclaire** | des TNP de cette masse ne sont pas exclus en principe, mais leur abondance est fortement bornée et aucun n'a été vu ; même s'ils constituaient toute la matière noire locale (~0,4 GeV/cm³, valeur usuelle), on en compterait moins d'un par cube d'une unité astronomique de côté | moyenne |

---

## 2. Rayonnement de Hawking : analogues, courbe de Page, paradoxe de l'information

### 2.1 État de l'art

**Statut expérimental.** Le rayonnement de Hawking d'un trou noir gravitationnel n'a jamais été observé (un trou
noir stellaire est plus froid que le fond cosmologique). L'idée d'Unruh [Unruh81] — un fluide dont l'écoulement
devient supersonique piège les ondes sonores comme un horizon piège la lumière — a donné naissance à la gravité
analogue (revue : [BLV11]) :

- **cuves à eau** : ondes de fréquence négative [Rousseaux08], émission stimulée [Weinfurtner11], corrélations
  [Euve16], superradiance par un vortex [Torres17] ;
- **optique** : horizon dans une fibre [Philbin08], filaments laser [Belgiorno10] (interprétation discutée),
  émission stimulée [Drori19], puis en 2026 stimulation par un photon unique [HawkingSingle26] et analogue de
  la rétroaction [HawkingBack26] ;
- **condensats de Bose-Einstein** : trou noir sonique [Lahav10], émission spontanée et intrication des paires
  [Steinhauer16], spectre thermique à la température prédite [MdN19], stationnarité [Kolobov21] ;
- **autres plateformes** : circuit supraconducteur [Shi23], vortex quantique géant dans l'hélium superfluide
  (analogue d'espace-temps en rotation) [Svancara24], fluides de polaritons [Falque].

Ces expériences testent la **cinématique** d'un champ quantique sur un fond effectif courbe (y compris la
robustesse vis-à-vis de la physique à courte distance). Elles ne testent ni les équations d'Einstein, ni
l'entropie de Bekenstein-Hawking [Bekenstein73], ni la fin de l'évaporation.

**Paradoxe de l'information.** Formulations : [Page93], [HP07], [Mathur09], [AMPS12] (« pare-feu »), [Harlow16],
[Marolf17]. Entre 2019 et 2020, la courbe de Page a été retrouvée à partir de la gravité semi-classique grâce aux
surfaces extrémales quantiques et aux « îles » [Penington19], [AEMM19], [AMMZ19], puis justifiée par les « trous
de ver de répliques » [PSSY19], [AHMST19] (revue : [AHMST20]). C'est l'indication la plus forte à ce jour que
l'évaporation est unitaire ; le mécanisme microscopique par lequel l'information sort, la validité hors des modèles
jouets et le rôle des moyennes d'ensemble restent débattus [Raju22], et des voix dissidentes subsistent [UW17] ;
autre piste : les « cheveux mous » [HPS16].

### 2.2 Conséquence pour la C204

- **Éclaire** : le rayonnement de Hawking est une prédiction théorique robuste, confirmée seulement dans des
  systèmes analogues. Statut : *théoriquement possible, non observé pour un trou noir*. La C204 présuppose une
  maîtrise industrielle d'un phénomène jamais détecté. Confiance élevée.
- **Corrige** : le bilan énergétique d'une « micro-singularité » doit être calculé avec les facteurs de corps gris
  et toutes les espèces [Page76a], [Page77], [BlackHawk] (errata E2) : la formule de corps noir en photons seuls
  sous-estime la puissance d'un facteur ≈ 21.
- **Invalide** : le caractère « froid » ou « contrôlable » de la source. Un objet de 5×10¹² kg émet ~4×10⁸ W sans
  possibilité de modulation (la seule variable est la masse) ; l'« injection d'électrons pour modifier la masse »
  devrait compenser ~4×10⁻⁹ kg/s, c'est-à-dire fournir la même puissance sous forme de matière avalée par une cible
  de 7 fm. Confiance élevée.
- **Piste réelle** : les analogues en rotation (vortex, hélium superfluide) reproduisent mathématiquement la
  propagation d'ondes dans un « champ de Kerr » effectif — voir §15, piste 2.

---

## 3. Géométrie de Kerr : observations, mathématiques, singularités

### 3.1 L'extérieur de Kerr est confirmé par l'observation [VÉR]

- **Ondes gravitationnelles** : première détection [GW150914] ; spectroscopie du trou noir final et test du
  théorème « sans cheveux » [Isi19] ; loi des aires de Hawking [Isi21] ; catalogues [GWTC3], [GWTC4cat] et tests
  de la relativité générale [TGR3]. Le signal GW250114 (rapport signal sur bruit de 80, masses 33,6 et 32,2 M☉)
  contraint les fréquences du mode quadrupolaire et de son premier harmonique à ±30 % du spectre de Kerr et
  confirme la loi des aires [GW250114LVK], [GW250114spec]. GW231123 : fusion de deux trous noirs très massifs et
  en rotation rapide (spins ≈ 0,9 et 0,8) [GW231123LVK]. La vitesse des ondes gravitationnelles égale celle de la
  lumière à mieux que 10⁻¹⁴ près [GW170817GRB].
- **Imagerie** : anneau de 42 ± 3 µas autour de M87*, compatible avec l'ombre d'un trou noir de Kerr [EHTM87] ;
  Sgr A* [EHTSgrA1] et tests de métrique [EHTSgrA6], [Psaltis20].
- **Orbites stellaires autour de Sgr A*** : décalage vers le rouge gravitationnel [GRAVITY18], [Do19] et précession
  de Schwarzschild [GRAVITY20] de l'étoile S2.
- **Entraînement des référentiels (Lense-Thirring)** : Gravity Probe B mesure −37,2 ± 7,2 mas/an pour une
  prédiction de −39,2 mas/an (et l'effet géodétique à 0,3 %) [GPB11] ; satellites LAGEOS [Ciufolini04], puis
  LARES + LAGEOS : 0,9910 ± 0,02 en unité de la prédiction [Ciufolini16], [Ciufolini19] ; pulsar binaire avec
  naine blanche en rotation rapide [VK20]. Mesures de spin de trous noirs : [Reynolds21], limite canonique
  a/M ≈ 0,998 pour un trou noir accrétant [Thorne74] (valeur de mémoire) ; tests de la nature des objets compacts :
  [CardosoPani19].

**Ordre de grandeur utile** [DÉD] : l'entraînement produit par la Terre entière vaut 39 millisecondes d'arc par an
(6×10⁻¹⁵ rad/s). Pour un rotor de laboratoire de moment cinétique J = 5×10³ kg·m²/s (100 kg, rayon 0,1 m,
10⁴ rad/s), Ω = 2GJ/(c²r³) ≈ 7×10⁻²⁴ rad/s à 1 m : aucune masse en rotation transportable ne produit un « champ
de Kerr » mesurable.

### 3.2 Résultats mathématiques récents

- **Stabilité de l'extérieur** : stabilité non linéaire de Schwarzschild [DHRT21] ; stabilité de Kerr en rotation
  lente [KS21], [GKS22] ; décroissance des ondes linéaires sur tout le domaine sous-extrémal [DRS14]. Formation
  de trous noirs par focalisation d'ondes gravitationnelles [Christodoulou09].
- **Intérieur et horizon de Cauchy** : inflation de masse [PI90], preuve en symétrie sphérique [Dafermos03],
  [LukOh19] ; choc gravitationnel sortant sur l'horizon interne [MO12] ; simulations de Kerr perturbé [BKZ16].
  Résultat central [DL17] (publié en 2025 aux *Annals of Mathematics*), en distinguant ce qui est démontré de ce
  qui est suggéré. **Démontré** : pour des données perturbées posées à l'intérieur du trou noir, l'évolution
  maximale se prolonge à travers une portion de l'horizon de Cauchy avec une métrique continue (stabilité C⁰) ;
  si l'extérieur de Kerr est stable, la formulation C⁰ de la censure cosmique forte est donc fausse. **Suggéré
  par la preuve, non démontré** : ces horizons seraient génériquement des « singularités nulles faibles », de
  sorte qu'une version révisée de la censure cosmique forte tiendrait. La stabilité C⁰ n'implique ni
  prolongement régulier ni prolongement unique (formulation de l'Équipe B, §2.4). Inextensibilité C⁰ de
  Schwarzschild : [Sbierski18].
- **Censure cosmique forte** : violations possibles près de l'extrémalité avec constante cosmologique positive
  [Cardoso18], [DRS18] ; les effets quantiques rétablissent la singularité sur l'horizon de Cauchy [HWZ20] ; pour
  Kerr, les flux quantiques divergent génériquement sur l'horizon interne [Zilberman22].
- **Trous noirs extrémaux** : formation en temps fini et réfutation de la « troisième loi » [KU22], seuil critique
  de l'effondrement [KU24] ; instabilité d'horizon [Aretakis12], [MRT13] ; forces de marée génériquement
  divergentes à l'horizon des trous extrémaux **en espace anti-de Sitter** [HKS23] ; en espace asymptotiquement
  plat, singularité de courbure à l'horizon de Kerr extrémal dès qu'on ajoute des termes de courbure d'ordre
  supérieur [HKRS23] ; impossibilité de sur-charger ou sur-tourner un trou de Kerr-Newman [SW17].
- **Réalité de la singularité** : Kerr soutient que les théorèmes de Penrose [Penrose65] prouvent l'existence de
  géodésiques nulles de longueur affine finie, pas de singularités [Kerr23] (prépublication, discutée) ; trous
  noirs réguliers [Hayward06], [Bueno24], revue [CR25], dont les cœurs sont eux-mêmes instables [CR21] ; théorèmes
  de singularité étendus au régime quantique [Wall13], [BSM22], [FKK22].

### 3.3 Courbes temporelles fermées dans Kerr, cylindre de Tipler, double Kerr

- La solution de Kerr [Kerr63], prolongée analytiquement, contient des courbes temporelles fermées près de la
  singularité annulaire, dans la région r < 0 atteinte « à travers l'anneau » [Carter68]. C'est le seul lien réel
  entre « anneau de Kerr » et voyage temporel. Cette région se trouve **au-delà de l'horizon de Cauchy**.
- Cylindre en rotation : le cylindre **infini** de Tipler engendre des courbes temporelles fermées [Tipler74] ;
  pour une source **finie**, une région à courbes temporelles fermées ne peut pas évoluer à partir de données
  initiales régulières dans un espace-temps asymptotiquement plat sans singularité [Tipler76] ; les théorèmes de
  singularité subsistent sans hypothèse de causalité, sauf violation commençant « à l'infini » [Tipler77] ;
  résultat prolongé par Hawking pour une région finie sans singularité de courbure [Hawking92].
- **Deux trous noirs de Kerr** : la solution exacte « double Kerr » existe [KN80b] ; elle a été étudiée pour ses
  singularités coniques (« entretoise » séparant les deux trous) et ses régions à courbes temporelles fermées [BS04],
  [CHR09b], [MR17] (détail de mémoire, résumé non disponible pour [BS04]). Théorème :
  il n'existe **pas** de configuration stationnaire d'équilibre de deux trous noirs alignés dans le vide (la
  répulsion spin-spin ne compense pas l'attraction) [NH09], [HN11].

### 3.4 Origine du terme « sinusoïde de Tipler » (contrôle terminologique)

Recherche en texte intégral dans INSPIRE-HEP (10 nov. 2026) : « Tipler sinusoid » → **1 seul résultat** ;
« off-set Tipler » → 0 ; « negative time event horizon » → 0. Recherche dans les titres et résumés d'arXiv → 0.
L'unique occurrence est la prépublication [Prezens10] (arXiv:1008.3244, 2010, une seule version, non publiée en
revue). Lecture du texte : l'auteur y propose que deux mini-trous noirs de Kerr soient modifiés en leur envoyant
des électrons et parle d'un « offset Tipler sinusoid », sans citer le récit Titor ; il rattache le mot
« sinusoïde » aux facteurs trigonométriques (en logarithme du rayon) de la solution extérieure du cylindre de
Tipler dans le régime où apparaissent les courbes temporelles fermées.

- [INT] Cette prépublication est **postérieure** de neuf ans aux messages et en reprend le vocabulaire : elle ne
  peut pas servir de source indépendante. Confiance élevée.
- [HYP] Elle fournit cependant une explication plausible du terme : le régime à courbes temporelles fermées de la
  solution de van Stockum-Tipler a bien des fonctions métriques oscillantes. Confiance moyenne ; à instruire par
  l'Équipe B sur le texte de [Tipler74].

### 3.5 Conséquence pour la C204

| Affirmation | Verdict | Justification | Confiance |
|---|---|---|---|
| Les singularités reproduisent localement le champ d'un trou noir de Kerr sur 3–3,7 m | **Invalide** | toute la structure propre à Kerr (ergosphère, horizons, anneau) tient dans quelques rayons gravitationnels, soit ~10⁻¹⁴ m pour 5×10¹² kg ; à 1 m, r_s/r ≈ 7×10⁻¹⁵ : le champ est newtonien | élevée |
| Passage simulé « à travers l'anneau » vers une autre ligne d'univers | **Non établi, défavorisé** pour un trou noir réel (statut : spéculatif) ; contredit comme procédé contrôlé | démontré : stabilité C⁰ de l'horizon de Cauchy, qui n'implique aucun prolongement régulier ni unique [DL17] ; suggéré : singularité nulle faible générique [DL17], [PI90], [MO12] ; calculé : divergence générique des flux quantiques [Zilberman22]. La relativité générale ne prédit pas ce qu'il y a au-delà | moyenne |
| « Sinusoïde de Tipler décalé » | **Invalide** comme concept établi | absent de la littérature ; seule trace postérieure et dérivée [Prezens10] | élevée |
| Deux singularités maintenues côte à côte | **Corrige** | pas d'équilibre stationnaire dans le vide [NH09] ; il faut une force extérieure, que rien de connu ne peut exercer sur 10¹² kg | moyenne |
| DOC-009 : horizons « de temps négatif / nul / positif » emboîtés | **Invalide** | Kerr possède deux horizons et deux ergosurfaces, aucun « signe du temps » ne leur est associé | élevée |
| Le « champ de Kerr » existe-t-il ? | **Éclaire** | oui, pour des trous noirs astrophysiques, et il est désormais mesuré (GW250114, EHT, Lense-Thirring) | élevée |

---

## 4. Trous de ver traversables

### 4.1 État de l'art

- **Cadre classique** : un trou de ver traversable exige de violer la condition d'énergie nulle [MT88], [HV98] ;
  deux bouches en mouvement relatif donneraient une machine temporelle [MTY88], que les fluctuations du vide
  tendent à détruire [KT91] ; censure topologique [FSW93] ; on peut réduire, pas annuler, la quantité de matière
  exotique [VKD03], [FR05].
- **Percée de 2017** : en couplant les deux bords d'un trou noir éternel en espace anti-de Sitter, on obtient une
  énergie nulle moyenne négative qui rend le pont d'Einstein-Rosen traversable [GJW17] ; le résumé précise que
  cela « ne peut pas servir à violer la causalité ». Interprétation en téléportation quantique [MSY17] ; trou de
  ver éternel [MQ18] ; lien avec ER = EPR [MS13] ; bornes sur l'information transmissible (ouverture plus brève
  que le temps de Planck dans certains régimes) [Freivogel19] ; trous de ver auto-entretenus [FGM19] ; introduction :
  [Kundu22].
- **Quatre dimensions** : solution d'Einstein-Maxwell avec fermions chargés sans masse, dont l'énergie de type
  Casimir est négative ; trou de ver « long », qui « ne conduit pas à des violations de causalité » [MMP18] —
  conforme au théorème de Gao et Wald [GW00] : traverser prend plus de temps que contourner. Version
  « humainement traversable » dans un modèle au-delà du modèle standard [MM20]. Solutions classiques
  d'Einstein-Dirac-Maxwell, dont la portée physique est discutée [BKR21], [KZ22].
- **Processeurs quantiques** : brouillage vérifié sur ions [Landsman19] ; propositions de « gravité quantique au
  laboratoire » [Brown19], [Nezami21], [Schuster22] ; expérience sur le processeur Sycamore, neuf qubits
  [Jafferis22]. **Critique** : l'hamiltonien appris (sept fermions de Majorana, cinq termes qui commutent) ne
  thermalise pas et le signal ne ressemble au modèle SYK que pour les opérateurs d'entraînement [KSY23] ; réponse
  des auteurs [Jafferis23]. Nouvelle tentative en 2026 sur un modèle SYK creux binaire à N = 8 [GIST26]
  (prépublication).

### 4.2 Ce que ces travaux disent — et ne disent pas

Ils disent que la gravité semi-classique **autorise** des trous de ver traversables, à condition d'une énergie
négative d'origine quantique et d'un couplage direct entre les deux bouches. Ils ne disent pas qu'on en a créé un
(l'expérience de 2022 est une téléportation quantique entre qubits, interprétable au mieux par dualité), ni qu'un
trou de ver permette d'aller plus vite que la lumière ou de remonter le temps : dans toutes ces constructions le
signal traverse plus lentement qu'à l'extérieur, et la condition d'énergie nulle moyenne achronale [GO07],
[Wall10] interdit le raccourci causal.

### 4.3 Conséquence pour la C204

- **Éclaire** : le « passage » revendiqué n'a pas d'équivalent dans la littérature ; les seuls trous de ver
  cohérents ne mènent ni dans le passé ni vers « une autre ligne d'univers ». Statut : *théoriquement possible*
  pour le trou de ver lui-même, *contredit* pour l'usage temporel. Confiance élevée.
- **Invalide** : l'idée qu'une rotation et une charge électrique suffisent. L'ingrédient indispensable — énergie
  négative — est absent de la description de la C204 (batteries, électrons, bobines). Confiance élevée.

---

## 5. Métriques de distorsion (« warp ») depuis 2001

### 5.1 État de l'art

- **Avant 2001** : métrique d'Alcubierre [Alc94] ; besoin d'énergie négative colossale [PF97] ; réduction par
  géométrie en « poche » [VDB99] ; effets quantiques déstabilisants [Hiscock97] ; tube de Krasnikov [Krasnikov98],
  [ER97] ; théorème : le transport supraluminique exige de l'énergie négative [Olum98] ; deux bulles suffisent à
  fabriquer une courbe temporelle fermée [Everett96].
- **2002-2020** : bulle sans expansion [Nat02] ; violations de la condition d'énergie nulle même à basse vitesse
  [LV04] ; instabilité semi-classique des bulles supraluminiques [FLB09] ; synthèse [AL17].
- **2021, solutions « à énergie positive »** : solitons supraluminiques [Lentz21], « warp drives physiques »
  subluminiques [BM21], [FH21]. **Critique** : ces travaux n'établissent la positivité que pour une famille
  d'observateurs ; toute métrique de distorsion physiquement raisonnable viole la condition d'énergie nulle
  [SSV22] ; masse ADM [SSV23].
- **2024** : solution numérique subluminique à vitesse constante respectant toutes les conditions d'énergie,
  grâce à une coque de matière de masse positive [Fuchs24w], outil [Helmerich24] ; signature en ondes
  gravitationnelles de l'effondrement d'une bulle [Clough24]. Proposition de géométrie de Casimir micrométrique
  [White21] (aucune démonstration expérimentale de distorsion).

### 5.2 Conséquence pour la C204

- **Invalide** : la désignation « gravity distortion » ne correspond à aucun dispositif réalisable. Les seules
  solutions respectant les conditions d'énergie sont subluminiques, à vitesse constante, et reposent sur des coques
  de matière très massives (ordre de grandeur planétaire, de mémoire) ; aucune ne produit de déplacement temporel vers le passé. Pour 227 kg, GM/(rc²) ≈ 2×10⁻²⁵
  à 1 m. Confiance élevée.
- **Éclaire** : la conclusion est la même que pour les trous de ver — supraluminique ou rétrograde implique
  énergie négative [Olum98], [SSV22], [Hawking92].

---

## 6. Courbes temporelles fermées et causalité

### 6.1 Relativité générale et protection chronologique

Solutions à courbes temporelles fermées : univers de Gödel [Godel49], cylindre de Tipler [Tipler74], intérieur
de Kerr [Carter68], cordes cosmiques de Gott [Gott91] (irréalisables physiquement [DJT92]), trous de ver [MTY88],
modèles d'Ori à cœur de vide [Ori05], [Ori07], faisceau lumineux circulant de Mallett [Mallett03] (réfuté :
singularité sur l'axe, et courbes fermées rejetées au-delà du rayon de l'univers visible [OE05]), bulle
« TARDIS » [TT17] (matière exotique). Revues : [Visser02], [FH06], [ESW09], [Shoshany19], [Luminet21].

Conjecture de protection chronologique [Hawking92] : si la violation de causalité apparaît dans une région finie
sans singularité de courbure, à partir d'une surface initiale non compacte, l'horizon de Cauchy est engendré de
façon compacte et la condition d'énergie faible moyennée y est violée ; le tenseur énergie-impulsion quantique y
devient très grand ; la théorie des champs
y est mal définie [KRW97] ; réserve : l'impossibilité n'est pas démontrée classiquement [Krasnikov02]. En théorie
des cordes et en holographie : [BGHV03], [Dyson03] ; correspondance entre courbes fermées dans le volume et
violation du principe de Pauli dans la théorie duale [CKS05] ; pour des théories conformes fortement couplées,
l'espace-temps dual se scinde et **aucune excitation ne franchit l'horizon chronologique** [ET21].

### 6.2 Dynamique cohérente avec des boucles

Principe d'auto-cohérence : [FMN90], boules de billard [EKT91] ; dynamique réversible compatible avec la liberté
de choix locale [Baumeler19], [TC20] ; horloges quantiques sur boucle [Bishop21] ; pour un vaisseau parcourant une
courbe fermée, les niveaux d'énergie se discrétisent, l'entropie revient à sa valeur initiale et **la mémoire de
l'observateur est effacée** en fin de boucle [Gavassino].

### 6.3 Modèles quantiques et simulations

- **Modèle de Deutsch** [Deutsch91] : point fixe d'une matrice densité, lecture « mondes multiples » ; non
  linéaire, il permettrait de distinguer des états non orthogonaux [BHW09] et donnerait la puissance PSPACE
  [AW09] ; objection sur la linéarité [BLSS09] ; variantes [Allen14].
- **Courbes à post-sélection (P-CTC)** : téléportation post-sélectionnée, où les issues paradoxales ont une
  probabilité nulle ; démonstration photonique [Lloyd11a], théorie [Lloyd11b].
- **Simulations expérimentales** : modèle de Deutsch [Ringbauer14] ; avantage métrologique [ASMY23] ; décodage
  d'information brouillée sur processeurs Quantinuum et IBM [Huang26] ; bibliothèque logicielle [Bishop26].
  Ce sont des circuits ordinaires, causalement ordonnés ; la post-sélection **rejette** des essais, elle n'envoie
  rien dans le passé.

### 6.4 « Mondes multiples » et absence de paradoxe

- L'idée qu'une lecture à la Everett [Everett57] supprime les paradoxes vient de Deutsch [Deutsch91] : elle existe
  donc bien dans la littérature *avant* les messages. [VÉR]
- Mais en tenant compte du temps de résolution du détecteur, cette approche n'est viable que si les objets
  macroscopiques sont **brisés en fragments microscopiques** par le passage [Everett04] (auteur : Allen Everett).
- Communiquer ou passer d'une branche à l'autre suppose une mécanique quantique **non linéaire** (« téléphone
  d'Everett ») [Polchinski91]. La linéarité est testée : [Bollinger89] ; le cadre non linéaire causal récent
  [KR22] a été testé sans effet détecté [Polkovnikov23], [Broz23]. La décohérence explique pourquoi les branches
  n'interagissent pas [Zurek03].

### 6.5 Ordre causal indéfini et « renversement du temps »

- **Ordre causal indéfini** : cadres théoriques [Hardy07], [Chiribella13], [OCB12] ; interrupteur quantique
  réalisé en optique [Procopio15], [Rubino17], [Goswami18] ; témoins et certification [Araujo15], [vdLugt23] ;
  revue expérimentale [Rozema24]. Limite : plongés dans un espace-temps acyclique, ces processus n'impliquent
  aucune boucle causale [VR24] ; une version gravitationnelle exigerait des masses en superposition [Zych19].
- **« Renversement du temps »** : l'expérience sur processeur IBM applique l'opération inverse à un état de deux
  ou trois qubits [Lesovik19] ; protocoles universels de retour en arrière [Navascues18], [Quintino19], [TDN20],
  [Trillo23], démonstration photonique [Schiansky23] ; superposition de sens du temps [CL22], [Stromberg24].
  Dans tous les cas, **l'état d'un sous-système** est ramené à une valeur antérieure tandis que le temps du
  laboratoire continue : c'est une opération de contrôle, pas un déplacement temporel.

### 6.6 Conséquence pour la C204

| Affirmation | Verdict | Justification | Confiance |
|---|---|---|---|
| Une machine compacte peut produire un retour dans le passé | **Invalide** en l'état des connaissances (statut : spéculatif à contredit) | exige, en l'absence de singularité de courbure, une énergie négative macroscopique [Hawking92] ; sinon des sources infinies ou des singularités [Tipler76], [Tipler77] ; protection chronologique soutenue en holographie [ET21] | élevée |
| « Pas de paradoxe grâce à Everett-Wheeler » | **Éclaire puis corrige** | l'idée est empruntable à [Deutsch91] (1991) ; elle est non linéaire, non testée, et problématique pour un objet macroscopique [Everett04] | moyenne |
| « Divergence de ligne d'univers » de 1 à 2,5 % | **Invalide** comme grandeur physique | aucune théorie ne définit une telle mesure ; le corpus se contredit lui-même (errata E9) ; l'interaction entre branches est bornée expérimentalement [Polkovnikov23], [Broz23] | élevée |
| Le voyage temporel a-t-il été réalisé en laboratoire ? | **Corrige** une confusion fréquente | non : simulations, post-sélection, inversion d'état | élevée |

---

## 7. Gravité quantique et unification

### 7.1 État des approches

| Approche | Résultats marquants | Singularités | Causalité |
|---|---|---|---|
| Cordes / holographie | AdS/CFT [Maldacena97] ; entropie microscopique [SV96] ; « boules de fils » [Mathur05] ; îles (§2) | résolues dans des cas contrôlés ; évaporation unitaire | protection chronologique soutenue [CKS05], [ET21] |
| Gravité quantique à boucles | absence de singularité cosmologique [Bojowald01], rebond [APS06] ; intérieur de Schwarzschild [AB06], [AOS18] ; transition trou noir → trou blanc [HR15], « étoiles de Planck » [RV14] | remplacées par un rebond (spéculatif) | pas de machine temporelle prédite |
| Sécurité asymptotique | trous noirs « améliorés » par le groupe de renormalisation [BR00] ; revue [Eichhorn19] | cœur régularisé, reliquat possible | — |
| Ensembles causaux | revue [Surya19] | discrétisation fondamentale | l'ordre causal est **l'axiome** : un ordre partiel est acyclique |
| Triangulations dynamiques causales | revue [Loll20] | — | la causalité est **imposée** pour obtenir une bonne limite continue |

Phénoménologie [Addazi22] : aucune déviation observée. Violation de l'invariance de Lorentz : échelle linéaire
supérieure à 10 fois l'énergie de Planck (sursaut GRB 221009A) [LHAASO24]. Gravité à courte distance : loi en
1/r² vérifiée jusqu'à 52 µm [Lee20], [Tan20], [Kapner07] — ce qui borne aussi les grandes dimensions
supplémentaires du §1.

### 7.2 Gravité quantique « de table »

- **Mesurer la gravité de petites masses** : deux sphères d'or de 90 mg [Westphal21] ; particule lévitée de
  0,4 mg, forces de l'ordre de l'attonewton [Fuchs24g] ; attraction d'une source miniature mesurée par un
  interféromètre atomique en réseau [Panda24] ; effet Aharonov-Bohm gravitationnel [Overstreet22].
- **Mettre des masses dans des états quantiques** : molécules de plus de 25 kDa [Fein19] ; nanoparticule dans son
  état fondamental [Delic20] ; état « chat » d'un résonateur de 16 µg [Bild23].
- **Propositions d'intrication induite par la gravité** [Bose17], [MV17] ; revues [Carney19], [Bose25],
  perspective [Aspelmeyer22] ; analyses [DSW22a], [DSW22b]. Alternatives à gravité classique : [Oppenheim23],
  compromis décohérence-diffusion testable [OSSW23] ; effondrement gravitationnel de Penrose [Penrose96], version
  sans paramètre défavorisée par une expérience souterraine (de mémoire) [Donadi21] ; détection de gravitons uniques envisagée
  [Tobar24].
- **Controverse 2025-2026** : selon [AzizHowl25], des théories à gravité classique produiraient elles aussi de
  l'intrication ; réfutations [MV25], [Diosi25] ; analyses [Ludescher25], [Plavala25].
- **État en novembre 2026** : à ma connaissance (recherche web du 10 nov. 2026), **aucune expérience n'a encore
  observé d'intrication induite par la gravité**.

### 7.3 Conséquence pour la C204

- **Éclaire** : il n'existe pas de théorie unifiée validée ; toutes les approches principales protègent ou
  postulent la causalité ; aucune ne prédit de voyage temporel contrôlable. Confiance élevée.
- **Corrige** l'échelle : la frontière expérimentale est la gravité d'une masse de 0,4 mg ; la C204 suppose la
  manipulation de 10¹² kg confinés dans 10⁻¹⁴ m. Dix-huit ordres de grandeur en masse (seize si l'on part des 90 mg de [Westphal21]), dans le sens opposé à celui
  où progresse l'expérience. Confiance élevée.
- Statut de la « physique de 2034 » invoquée : *spéculatif*, sans indice empirique en 2026.

---

## 8. Métrologie du temps

### 8.1 État de l'art

- **Horloges optiques** (revue [Ludlow15]) : comparaison de deux horloges séparées d'environ 30 cm en hauteur [Chou10] ;
  réseaux cryogéniques [Ushijima15] ; performance « au-delà de la limite géodésique » [McGrew18] ; ion Al⁺ à
  9,4×10⁻¹⁹ [Brewer19] ; stabilité [Oelker19] ; rapports de fréquence à 18 chiffres [BACON21] ; **décalage
  gravitationnel résolu à l'intérieur d'un échantillon d'un millimètre**, incertitude de mesure 7,6×10⁻²¹
  [Bothwell22], [Zheng22] ; réseau Sr à 8,1×10⁻¹⁹ [Aeppli24] ; Al⁺ à 5,5×10⁻¹⁹ [Marshall25] ; Ca⁺ refroidi à
  l'azote liquide à 4,4×10⁻¹⁹ [Ca26] ; deux références Lu⁺ à 1,2 et 1,3×10⁻¹⁹, en accord à
  (−0,1 ± 5,7 ± 1,0)×10⁻¹⁹ [Lu26].
- **Horloges transportables et réseaux** : [Lisdat16], [Grotti18], test de relativité entre deux horloges transportables à des altitudes différentes (tour
  Tokyo Skytree, de mémoire) [Takamoto20], géodésie chronométrique [Mehl18], horloges optiques à iode en mer (moins de 300 ps par jour)
  [Roslund24].
- **Espace** : test du décalage gravitationnel avec les satellites Galileo excentriques [Delva18], [Herrmann18],
  après Gravity Probe A [Vessot80] ; horloge à ions dans l'espace [Burt21] ; ACES [ACES09], [ACES24], lancée vers
  la Station spatiale en avril 2025 (résultats préliminaires seulement, d'après la recherche web).
- **Horloge nucléaire au thorium 229** : proposition [PT03] ; énergie de la transition [Seiferle19] ;
  désexcitation radiative [Kraemer23] ; excitation laser [Tiedau24], [Elwell24] ; rapport de fréquence avec
  l'horloge au strontium [Zhang24] ; films minces [Zhang24b] ; en 2026, spectroscopie en laser continu [Th26a] et
  première horloge nucléaire asservie, instabilité 3×10⁻¹² τ^(−1/2), soit ~10⁻¹⁵ en un jour [Th26b]
  (tous deux publiés dans *Nature* en 2026).
- **Redéfinition de la seconde** : feuille de route [Dimarcq24] ; la résolution 5 de la CGPM de 2022 attendait des
  propositions en 2026 et vise une adoption en 2030 (issue de la CGPM de 2026 non vérifiée ici).
- **Césium et horloges compactes** : horloges commerciales à jet de césium [Cutler05] ; fontaines primaires
  [Heavner14], [Weyers18] ; horloges atomiques sur puce [Knappe04], [Kitching18]. Relativité dans le GPS
  [Ashby03] ; horloges embarquées en avion [HK72a], [HK72b].

### 8.2 Conséquence pour la C204

1. **« 4 horloges au césium » — éclaire.** Une redondance de quatre étalons est une pratique réelle (trois pour
   voter, un de réserve). En revanche, pour une conception datée de 2034, des étalons à jet de césium seraient
   dépassés de cinq à six ordres de grandeur par les horloges optiques de 2026, et des horloges optiques
   compactes fonctionnent déjà sur des navires [Roslund24]. [DÉD] Le choix du césium reflète l'état de l'art de
   2000, pas celui de 2034. Confiance moyenne.
2. **« La précision d'horloge limite la divergence » — corrige.** Calcul [DÉD] : une horloge commerciale au césium
   (exactitude ~5×10⁻¹³, ordre de grandeur cité de mémoire) accumule 1×10⁻⁸ s d'erreur en 6 heures de temps propre ; reportée sur
   60 ans à raison de 87 660, cela fait 1 ms. Or « 1 % de 60 ans » représente 219 jours (1,9×10⁷ s) : dix ordres
   de grandeur d'écart. Si la « divergence » était une erreur de datation, les horloges ne seraient pas le
   facteur limitant ; si elle est autre chose, elle n'a pas de définition (§6). Confiance élevée sur le calcul.
3. **« 10 ans par heure » — invalide.** La dilatation gravitationnelle est mesurée : 1,09×10⁻¹⁶ par mètre de
   dénivelé [Bothwell22], [Takamoto20]. Une masse donnant 2 g à 1 m décale les fréquences de 2×10⁻¹⁶ ; un rapport
   de 87 660 exige de stationner à 1,3×10⁻¹⁰ rayon de Schwarzschild au-dessus d'un horizon. Et la dilatation ne
   mène que vers le futur de l'extérieur : *dilatation du temps ≠ voyage dans le passé*. Confiance élevée.
4. **Test possible** (pour l'Équipe F, sans danger) : une horloge optique détecte 10⁻¹⁸, soit 1 cm de dénivelé ;
   c'est l'instrument qui révélerait toute « distorsion de gravité » réelle.

---

## 9. Gravimétrie de précision

### 9.1 État de l'art

- **Interférométrie atomique** : mesure de g à quelques 10⁻⁹ près [Peters99] (valeur de mémoire) ; gravimètre quantique
  absolu transportable sous 10⁻⁹ g [Menoret18] ; gravimétrie marine [Bidel18] et aéroportée (erreur de 1,7 à 3,9 mGal) [Bidel20] ; relevés
  mobiles (37 µGal/√Hz, 0,04 mGal sur le terrain) [Wu19] ; gradiomètre quantique de terrain cartographiant une cavité enterrée (de mémoire) [Stray22] ;
  gravimètre différentiel compact [Janvier22] ; accéléromètre hybride à trois axes [Templier22] ; revues
  [Bongs19], [Tino21].
- **Navigation** : compensation gravimétrique d'une centrale inertielle [Jekeli06] ; **première navigation
  gravimétrique quantique sans GNSS en mer** — 83 km, position bornée au niveau du mille marin, anomalies résolues
  à ~300 m le long de la route [QCTRL26] (prépublication, résultat d'entreprise) ; équivalent magnétique
  [QCTRL25].
- **Espace** : GRACE-FO [Landerer20] ; interférométrie atomique en orbite [Elliott23] ; feuille de route
  [Abend23] ; mission CARIOQA [CARIOQA].
- **Références** : gravimètres supraconducteurs [Goodkind99] ; variations temporelles de la pesanteur (marées,
  hydrologie) [VanCamp17] ; constante G par atomes froids [Rosi14], mesures récentes [Li18], revue [RS17] ;
  principe d'équivalence à 10⁻¹² par atomes [Asenbaum20] et à 10⁻¹⁵ par MICROSCOPE [MICROSCOPE22] ; courbure
  d'espace-temps à l'échelle d'une fonction d'onde [Asenbaum17].

### 9.2 Conséquence pour le système « VGL »

- **Éclaire** : se repérer par la gravité est réel — par **corrélation avec une carte**, en se déplaçant, avec une
  exactitude de l'ordre du kilomètre.
- **Corrige** : la pesanteur en un lieu n'est ni unique ni stable. Marées : ~3×10⁻⁷ g crête à crête (de mémoire) ;
  hydrologie : 10⁻⁹ à 10⁻⁸ g [VanCamp17] (ordres de grandeur). Un scalaire et cinq composantes de gradient ne
  désignent pas un point de la Terre, encore moins à soixante ans d'intervalle. Confiance élevée.
- **Invalide** : aucune mesure de gravité ne peut « verrouiller » une trajectoire d'espace-temps ; capter n'est
  pas agir. Le texte ne décrit aucun actionneur. Confiance élevée.
- **Incohérence interne** [DÉD] : à 0,3–1 m de masses de 5×10¹² kg, le champ propre atteint 30 à 340 g et son
  gradient 600 s⁻² à 1 m, contre 3×10⁻⁶ s⁻² pour le gradient terrestre : les capteurs devraient extraire le
  signal de la Terre sous un parasite 10⁸ fois plus grand. Confiance moyenne.
- **Signature observable** [DÉD] : deux masses de 4,5×10¹² kg modifieraient la pesanteur de 6 µGal à 100 km et
  de 600 µGal à 10 km ; leur apparition ou disparition soudaine serait à la portée des gravimètres et
  sismomètres d'observatoire. Aucune anomalie de ce type n'est rapportée (affirmation négative non vérifiable
  exhaustivement). Confiance moyenne.

---

## 10. Énergie négative et effet Casimir

### 10.1 État de l'art

- **Mesures** : [Lamoreaux97], [MR98], plaques parallèles [Bressi02], pression à haute précision [Decca07],
  composante thermique [Sushkov11], sphère-sphère [Garrett18], couple de Casimir [Somers18], **force répulsive**
  dans un fluide [Munday09], équilibres stables [Zhao19] ; revue [KMM09]. L'effet Casimir peut se calculer sans
  invoquer l'énergie du vide [Jaffe05]. **Effet Casimir dynamique** observé dans des circuits supraconducteurs
  [Wilson11], [Lahteenmaki13]. Projet de pesée de l'énergie du vide [Calloni14].
- **États comprimés** : compression de 15 dB [Vahlbruch16], utilisée dans LIGO [Tse19], [Ganapathy23] ;
  échantillonnage direct des fluctuations du vide [Riek15], [Riek17].
- **Théorèmes** : la densité d'énergie quantique n'est pas bornée inférieurement point par point [EGJ65], mais
  son intégrale est contrainte par des inégalités quantiques [Ford78], [FR95], qui restreignent sévèrement les
  trous de ver [FR96], [FR05] ; cours et revue [Fewster12], [KS20]. Condition d'énergie nulle moyenne (ANEC)
  démontrée en théorie des champs en espace plat [FLPW16], [HKT17] et dans certains espaces courbes [KO15] ;
  version achronale [GO07], [Wall10] ; condition quantique [BFKLW16], conjecture de focalisation [BFLW16] ;
  condition « lissée » : les régions d'énergie négative ne gravitent jamais fortement [FK18], [FKK22].

**Ordre de grandeur** [DÉD] : entre deux plaques parfaites distantes de d, ρ = −π²ħc/(720 d⁴) ; pour d = 100 nm,
ρ ≈ −4,3 J/m³, soit −5×10⁻¹⁷ kg/m³ en équivalent masse, contre +2×10⁴ kg/m³ pour les plaques d'or.

### 10.2 Conséquence pour la C204

- **Éclaire** : l'énergie négative existe (Casimir, états comprimés), elle est mesurée, et elle est minuscule,
  brève et toujours « remboursée » par de l'énergie positive.
- **Invalide** : un « champ de temps négatif » macroscopique. Tout chemin relativiste vers le passé, dans une région finie sans singularité, passe par une
  violation de l'ANEC que la théorie quantique des champs interdit sur les géodésiques concernées. La C204 ne
  décrit d'ailleurs aucune source d'énergie négative. Confiance élevée.

---

## 11. États quantiques exotiques associés à tort au « temps »

| Phénomène | Ce que c'est réellement | Références | Rapport avec un voyage temporel |
|---|---|---|---|
| Cristal temporel | phase de la matière brisant la symétrie de translation dans le temps : réponse sous-harmonique rigide d'un système à N corps entretenu périodiquement. La version à l'équilibre est exclue [Bruno13], [WO15] | proposition [Wilczek12], [SW12] ; théorie [KLMS16], [EBN16], [Yao17] ; observations [Zhang17], [Choi17], [Randall21], [Mi22], [FR22] ; version continue dissipative [Kongkhambut22] ; revues [SZ18], [Zaletel23] | aucun |
| « Temps négatif » d'un photon | valeur faible négative du temps passé sous forme d'excitation atomique ; lié au retard de groupe négatif | [Angulo24] | aucun signal n'arrive avant sa cause |
| « Réflexion temporelle » | interface temporelle dans un métamatériau : conversion de fréquence et retournement de la forme d'onde | [Moussa23] | aucun |
| « Inversion du temps » sur processeur | application de l'opération inverse à l'état de quelques qubits | [Lesovik19], [Schiansky23] (§6.5) | aucun |
| Ordre causal indéfini | superposition de l'ordre de deux opérations | [Rozema24] (§6.5) | aucune boucle causale [VR24] |

**Conséquence pour la C204 — éclaire** : aucun de ces résultats ne soutient l'existence d'un « champ de temps »
positif, nul ou négatif. Le rapprochement est purement lexical. Confiance élevée.

---

## 12. Faits historiques liés au récit : IBM 5100, an 2038, vote des calculateurs

### 12.1 IBM 5100

- [VÉR] Ordinateur portable annoncé en septembre 1975, retiré en mars 1982 ; processeur PALM (« Program All Logic
  in Microcode ») ; description technique d'époque : [Roberson76].
- [VÉR] Le microcode exécute des **émulateurs** permettant de réutiliser des interpréteurs écrits pour de plus
  gros systèmes : APL issu des grands systèmes (APLSV, System/360-370) et BASIC issu du System/3. Sources
  consultées : page Wikipédia « IBM 5100 » (qui cite *PC Magazine*, novembre 1983) ; contexte APL chez IBM :
  [Hassitt76], [Falkoff91] ; le manuel de maintenance SY31-0405-3 (1979) est numérisé (repéré, non ouvert).
  Nuance : les sources divergent sur « System/360 » ou « System/370 », et il s'agit d'un sous-ensemble
  d'instructions.
- [DÉD] Cette capacité était **documentée publiquement** dans la littérature technique des années 1970-1980 ; elle
  était peu connue du grand public en 2000, mais elle ne constitue pas une information d'initié. Confiance
  moyenne (l'article de 1983 [Friedl83] est cité de mémoire : **non vérifiée**).
- Aucune source ne documente une capacité du 5100 à « corriger » du code UNIX : ses émulateurs concernent des
  interpréteurs IBM.

### 12.2 Problème de l'an 2038

- [VÉR] Un compteur `time_t` signé de 32 bits déborde 2³¹ − 1 secondes après le 1ᵉʳ janvier 1970, soit le
  19 janvier 2038 à 03:14:07 UTC (recalculé).
- [VÉR] La correction est le passage à 64 bits, déjà largement accompli : noyau Linux 5.6 (2020) pour les
  architectures 32 bits, glibc 2.34 (2021), NetBSD 6.0 (2012), OpenBSD 5.5 (2014) (d'après Wikipédia) ; Debian 13
  (2025) bascule toutes ses architectures sauf i386 (notes de version) ; **POSIX.1-2024 impose un `time_t` d'au
  moins 64 bits** (texte de la norme). Le risque résiduel concerne l'embarqué ancien, des formats de fichiers et
  des bases de données.
- **Conséquence — invalide la nécessité** : la correction relève de la recompilation et de la migration, pas
  d'une machine de 1975. Confiance élevée.

### 12.3 Trois calculateurs à vote « Borda »

- [VÉR] La redondance modulaire triple à vote majoritaire date de 1962 [Lyons62]. Avec des pannes arbitraires
  (« byzantines »), tolérer une panne exige quatre unités, sauf messages signés [LSP82].
- **Éclaire** : trois calculateurs votants sont une architecture réelle ; le terme « Borda » désigne une méthode
  de vote par classement, inhabituelle en sûreté de fonctionnement. [HYP] Usage approximatif d'un terme technique.
  Confiance moyenne.

---

## 13. (a) Tableau de synthèse : affirmation de la C204 ↔ meilleur résultat contemporain ↔ verdict

| # | Affirmation (dossier §4) | Meilleur résultat scientifique contemporain | Verdict | Statut physique |
|---|---|---|---|---|
| 1 | Micro-singularités créées au CERN | Aucun trou noir au LHC ; limites 8,4–11,4 TeV [CMS26], 9,4 TeV à 13,6 TeV [ATLASQBH26] | Invalide | Contredit |
| 2 | « Percée » imminente en 2001 | LHC : 2008-2010 ; arrêt LS3 en 2026 | Invalide | Contredit [VÉR] |
| 3 | « Méthode » de la Z machine | puissance pulsée sans rapport [Sinars20] | Invalide | Contredit |
| 4 | 300–500 MW par singularité | 3,9–5,0×10¹² kg, kT ≈ 2–3 MeV [Page76a], [Page77] | Corrige | Théoriquement possible (objet), contredit (227 kg) |
| 5 | Singularités « plus petites qu'un électron » | r_s ≈ 6–7 fm ; rayon classique de l'électron 2,8 fm (errata E4) | Corrige | — |
| 6 | Rayons X évacués par un cône | gamma de 12–16 MeV, neutrinos, e± ; pas de photosphère [MCP08] | Invalide | Contredit |
| 7 | Évaporation si le confinement cède | durée ~10¹³ ans à cette masse ; ≈ 5×10⁻¹² s et 2×10¹⁹ J pour 227 kg | Invalide | Contredit |
| 8 | La charge agrandit l'horizon interne | charge fluctuante de valeur quadratique moyenne ≈ 6 e [Page77] ; borne ~137 e (errata E14) ; 10¹⁹ à 10²⁰ fois sous l'extrémalité | Corrige | Formellement exact, inapplicable |
| 9 | Rotation entretenue et orientable | ralentissement spontané [Page76b], [TCH98] ; pas de sur-rotation [SW17] | Corrige | Spéculatif |
| 10 | Champ de Kerr local sur 3–3,7 m | structure de Kerr confinée à ~10⁻¹⁴ m ; Kerr confirmé à l'échelle astrophysique [GW250114LVK] | Invalide | Contredit |
| 11 | Passage « à travers l'anneau » | stabilité C⁰ de l'horizon de Cauchy démontrée, singularité nulle faible seulement suggérée [DL17] ; flux quantiques divergents [Zilberman22] | Non établi, défavorisé (confiance moyenne) | Spéculatif pour un trou noir réel ; contredit comme procédé contrôlé |
| 12 | « Sinusoïde de Tipler décalé » | terme inexistant ; [Tipler74], [Tipler76] ; trace dérivée [Prezens10] | Invalide | — |
| 13 | Deux singularités stationnaires | pas d'équilibre de deux trous de Kerr [NH09], [HN11] | Corrige | Contredit sans force extérieure |
| 14 | Horizons de temps négatif / nul / positif | aucun équivalent ; énergie négative bornée [FLPW16], [FK18] | Invalide | Contredit |
| 15 | Absence de paradoxe (Everett-Wheeler) | modèle de Deutsch [Deutsch91] ; objections [Everett04], [BLSS09] | Éclaire, corrige | Spéculatif |
| 16 | Divergence de 1 à 2,5 % | grandeur non définie ; interaction entre branches non détectée [Polkovnikov23] | Invalide | — |
| 17 | 10 ans par heure | 1,09×10⁻¹⁶ par mètre mesuré [Bothwell22] ; vers le futur seulement | Invalide | Contredit |
| 18 | 1,5 à 2 g ressentis | 26–34 g par singularité à 1 m (errata E1) | Corrige | Incohérent |
| 19 | 4 horloges au césium | horloges optiques à 10⁻¹⁹ [Lu26] ; redondance réelle | Éclaire, corrige | Démontré (horloges) |
| 20 | Capteurs de gravité « VGL » | gravimétrie quantique embarquée [QCTRL26] ; pas de verrouillage possible | Corrige, invalide | Démontré (mesure), contredit (verrouillage) |
| 21 | 3 calculateurs à vote | redondance triple [Lyons62], limite byzantine [LSP82] | Éclaire | Démontré |
| 22 | Alimentation par batteries | énergie négative requise en l'absence de singularité [Hawking92] ; 4×10⁸ W permanents par singularité | Invalide | Contredit |
| 23 | « Gravity distortion » | métriques de distorsion : violation de la condition d'énergie nulle [SSV22] | Invalide | Spéculatif à contredit |
| 24 | IBM 5100 et émulation | émulation documentée dès les années 1970-1980 | Éclaire | Démontré [VÉR] |
| 25 | Besoin du 5100 pour 2038 | `time_t` 64 bits, POSIX.1-2024 | Invalide | — |

Lecture : **aucune** affirmation relative au principe temporel n'est confortée par la science de 2001-2026 (la
ligne 11 est « non établie, défavorisée » et non « invalidée » : la question de l'intérieur de Kerr reste ouverte) ; les
seuls éléments « éclairés » positivement sont des sous-systèmes conventionnels (horloges, gravimètres, vote) et
des faits historiques publics.

---

## 14. (b) Recherches supplémentaires nécessaires (livrable n° 13)

Le détail argumenté est dans `RECHERCHES_SUPPLEMENTAIRES.md`. Les dix questions ouvertes retenues :

1. Existe-t-il des trous noirs en fin d'évaporation ? (LHAASO, HAWC, CTAO, télescopes MeV, neutrinos)
2. L'échelle de gravité est-elle abaissée par des dimensions supplémentaires ? (HL-LHC, gravité sous 50 µm)
3. Que devient l'horizon interne d'un trou noir en rotation avec rétroaction quantique complète ?
4. Stabilité de Kerr sur tout le domaine sous-extrémal ; censure cosmique forte sans symétrie.
5. La protection chronologique est-elle un théorème de la gravité quantique ?
6. Jusqu'où tiennent les conditions d'énergie moyennées pour des champs en interaction en espace courbe ?
7. La gravité peut-elle intriquer deux masses ? (expériences de type Bose-Marletto-Vedral)
8. La mécanique quantique est-elle exactement linéaire ? (tests du cadre causal non linéaire)
9. Jusqu'où peut-on pousser les analogues de Kerr et de Hawking (émission spontanée, rétroaction, superradiance) ?
10. Horloges nucléaires, redéfinition de la seconde, géodésie chronométrique millimétrique.

S'y ajoutent des recherches **documentaires** à transmettre aux équipes A, B et G (datation du vocabulaire,
texte de [Tipler74], statut de [Prezens10], documentation d'époque du 5100).

---

## 15. (c) Les cinq pistes contemporaines pour « la machine la plus proche de la C204 que la physique n'interdit pas »

Avertissement : **aucune de ces pistes ne réalise un voyage dans le passé**. Elles désignent ce qu'on peut
réellement construire ou mesurer en s'approchant, sous-système par sous-système, de ce que le récit décrit.

| # | Piste | Ce qu'elle reproduit de la C204 | État de l'art vérifié | Ce qu'elle ne fera pas |
|---|---|---|---|---|
| 1 | **Chronométrie relativiste** : paire d'horloges optiques (ou, demain, nucléaires) dont l'une est déplacée dans un potentiel gravitationnel | le seul « déplacement temporel par la gravité » démontré : un décalage mesurable, vers le futur, de 1,1×10⁻¹⁶ par mètre | [Bothwell22], [Takamoto20], [Roslund24], [Lu26], [Th26b] | dépasser ~10⁻⁹ de décalage relatif sur Terre ; aller vers le passé |
| 2 | **Simulateur analogique de Kerr** : deux vortex (cuve à eau, hélium superfluide, fluide de polaritons, optique) jouant les « deux singularités en rotation » | horizons, ergorégion, superradiance, émission de Hawking stimulée, « champ de Kerr » effectif pour des ondes | [Torres17], [Svancara24], [Falque], [MdN19], [HawkingBack26] | courber l'espace-temps réel : seule la propagation d'ondes dans le milieu est concernée |
| 3 | **Simulateur quantique de causalité** : circuits à courbes temporelles fermées simulées (Deutsch, P-CTC), interrupteur quantique, téléportation « de type trou de ver » | la logique de cohérence d'un voyage temporel, l'« absence de paradoxe », le passage par un pont | [Ringbauer14], [Lloyd11a], [ASMY23], [Huang26], [Rozema24], [Jafferis22] avec la critique [KSY23] | transmettre de l'information vers le passé ; les essais « paradoxaux » sont rejetés, pas évités |
| 4 | **Suite de capteurs « VGL réelle »** : gravimètre et gradiomètre à atomes froids, centrale inertielle hybride, horloges redondantes, trois calculateurs votants | les systèmes 4, 5 et 6 du message du 2 novembre 2000, avec des performances mesurées | [Menoret18], [Stray22], [Templier22], [QCTRL26], [Kitching18], [Lyons62] | « verrouiller » une position à travers le temps : c'est une navigation par carte de gravité |
| 5 | **Banc d'énergie négative et de gravité des petites masses** : cavités de Casimir, vide comprimé, masses lévitées du milligramme au microgramme, test d'intrication gravitationnelle | l'ingrédient que toute machine temporelle relativiste sans singularité exigerait (énergie négative) et la question « la gravité est-elle quantique ? » | [Garrett18], [Zhao19], [Wilson11], [Vahlbruch16], [Westphal21], [Fuchs24g], [Bose17], [Bild23] | accumuler assez d'énergie négative : les inégalités quantiques et l'ANEC l'interdisent [FR96], [FLPW16] |

**Piste de veille (hors des cinq)** : le « cœur à micro-trou noir » pris au pied de la lettre. Un trou noir de
~10¹² kg n'est pas interdit par la physique connue et rayonnerait bien quelques centaines de mégawatts, mais il
n'est ni fabricable par un moyen connu (4×10²⁹ J à concentrer dans ~10⁻¹⁴ m ; la voie par concentration de lumière
est exclue [Kugel24]), ni confinable, ni transportable, et il ne donne pas de machine
temporelle ; son seul prolongement scientifique réel est la **recherche observationnelle de trous noirs
primordiaux en évaporation** [PBH2505], [HAWC20], et l'étude théorique [CW09].

Recommandation pour la phase 6 (`10_machine_optimisee/`) : combiner les pistes 1 et 4 en un démonstrateur
instrumenté (« unité de mesure du déplacement temporel gravitationnel »), y adjoindre les pistes 2 et 3 comme
modules de simulation — explicitement étiquetés *simulation ≠ expérience* — et réserver la piste 5 à une note
prospective.

---

## 16. Bilan bibliographique et découvertes annexes

**Bilan** (détail dans `journal_verification.md`) : **446 références scientifiques vérifiées** par API (418 avec
DOI, 344 avec identifiant arXiv, 316 avec les deux ; 371 datées de 2001 ou après, dont 63 de 2024 à 2026) ;
**1 référence non vérifiée** ([Friedl83], non utilisée comme preuve) ; 19 pages web institutionnelles ou tertiaires
consultées ou repérées, classées à part. Répartition par thème : 65 / 34 / 70 / 26 / 21 / 64 / 42 / 42 / 25 / 35 /
17 / 5. Douze candidats ont été écartés (identifiant de mémoire erroné, résultat de recherche hors sujet) et 22
titres attendus de mémoire ont été corrigés d'après l'API ; 25 notices restent des prépublications sans version
publiée retrouvée. Depuis la phase 7, le CSV distingue le titre de la notice interrogée et le titre de la version
publiée quand ils diffèrent (67 notices), et une référence a été ajoutée ([Tipler76]).

**Portée de la vérification** : « vérifiée » signifie que la référence **existe** et que titre et auteur concordent ;
cela ne garantit pas que le rapport en restitue fidèlement le contenu. L'audit de la Red Team (58 références de
l'Équipe H relues sur résumé, dont 14 tirées au sort) a classé 50 emplois conformes, 6 « approximatifs » (corrigés
au §18) et 1 « introuvable » (le coefficient attribué à [MacGibbon91] ne figure pas dans son résumé) ; un emploi
« mal employé » de [CHT97] concerne l'Équipe B, le présent rapport l'utilisant correctement comme exception.

**Découvertes annexes utiles aux autres équipes**

1. *Équipes A, B, G* — [Prezens10] : unique trace de « Tipler sinusoid » dans la littérature indexée ; postérieure
   au récit, dérivée de lui, non publiée en revue ([INT]).
2. *Équipes A, G* — l'idée de trous noirs produits en accélérateur circulait dans la littérature dès 1998-1999
   ([ADM98], [BF99]) et dans le débat public à propos du RHIC ([BJSW00], 1999-2000) : [DÉD] un auteur de
   2000-2001 pouvait la connaître sans information privilégiée. Les articles les plus célèbres ([GT01], [DL01])
   sont de juin 2001, donc postérieurs aux derniers messages.
3. *Équipes B, G* — l'argument « Everett = pas de paradoxe » est publié depuis 1991 ([Deutsch91]).
4. *Équipes B, D* — pour les spectres d'émission à kT ≈ 2–3 MeV, utiliser les taux de [Page76a], [Page77] ou le
   code [BlackHawk] plutôt que la formule de corps noir ([MW90] ne vaut qu'au-dessus de ~20 MeV de température).
5. *Équipe C* — perte spontanée de charge et fluctuations ≈ 6 e ([Gibbons75], [Page77]) et absence de photosphère
   ([MCP08]) : deux
   résultats publiés qui ferment respectivement le levier « charge » et le système « évacuation des rayons X ».
6. *Équipe F* — expériences sûres inspirées des pistes 1 à 4 : horloges à quartz ou GPS en altitude (ordre de
   grandeur seulement), vortex de vidange en cuve (analogue de superradiance), simulation de P-CTC sur
   simulateur de circuits.

---

## 17. Lacunes et réserves

- Lecture limitée aux **résumés** ; les valeurs chiffrées absentes des résumés et citées « de mémoire » sont
  signalées et ne fondent aucun verdict.
- Les contraintes numériques sur l'abondance des trous noirs primordiaux (fraction de matière noire par gamme de
  masse) n'ont pas été extraites des figures des revues : seules les limites de taux d'explosion sont chiffrées.
- Résultats de 2026 [QCTRL26], [GIST26], [PBH2605], [Bishop26] : prépublications non évaluées ([Th26a], [Th26b],
  [Lu26], [Ca26], [CMS26], [ATLASQBH26] sont publiés).
- Non vérifié dans cette session : issue de la CGPM de 2026 ; résultats définitifs d'ACES ; état exact du LS3 en
  novembre 2026 (seul le calendrier publié est cité) ; énergie stockée de la Z machine ; article de 1983 sur le
  5100.
- Pages du CERN : plusieurs adresses de communiqués supposées de mémoire renvoient HTTP 404 (site réorganisé) ;
  la chronologie repose sur les articles vérifiés et sur les pages effectivement consultées.
- Je n'ai pas eu accès au corpus textuel complet (Équipe A) : l'énoncé « percée au CERN d'ici un an ou deux »
  est repris de l'énoncé de mission et reste à localiser dans les sources archivées.

---

## 18. Journal des corrections post-validation (phase 7)

Source des demandes : `08_red_team/CORRECTIONS_A_APPLIQUER.md` (section 7), `08_red_team/RAPPORT_RED_TEAM_2.md`
et `08_red_team/audit_references.csv`. Chaque demande a été confrontée à la source avant application : résumés
relus le 10 novembre 2026 par l'API INSPIRE-HEP (Page 1977, Gibbons 1975, Hawking 1992, Tipler 1976 et 1977,
MacGibbon et Webber 1990, MacGibbon 1991) et dans le cache arXiv ([DL17], [HKS23], [HKRS23], [Kugel24]).
La version 1 du rapport est conservée dans `donnees_brutes/RAPPORT_H_v1_avant_phase7.md`.
**Aucune correction n'est contestée.**

### 18.1 Corrections demandées par la Red Team

| N° | Lieu | Version 1 | Version 1.1 | Ce que dit la source | État |
|---|---|---|---|---|---|
| 57 | §0 (point 3), §3.2, §3.5, §13 (ligne 11) | « Théorème : … prolongement génériquement singulier » ; verdict « Invalide », confiance élevée | démontré (stabilité C⁰) / suggéré (singularité nulle faible) / calculé (flux quantiques divergents) ; verdict « non établi, défavorisé », confiance moyenne ; « contredit » seulement comme procédé contrôlé (formulation de l'Équipe B, §2.4) | résumé de [DL17] : le prolongement à métrique continue est démontré ; le caractère singulier est ce que « la preuve suggère » | appliquée |
| 58 | §0 bis (tableau), §1.1, §1.2, §13 (ligne 8), §16 | « au-delà de 2 à 3 charges élémentaires … [Gibbons75] » | valeur quadratique moyenne ≈ 6 e [Page77] ; borne ~137 e (errata E14) ; le critère e·Q/4πε₀r_s < m_e c² est présenté comme un ordre de grandeur de notre part, absent de Gibbons (1975) | résumé de Page (1977) : 6,14 e pour GMμ/ħc = 0 (ici 0,009) ; résumé de Gibbons (1975) : deux régimes de part et d'autre de 10¹⁷ g, aucun seuil en nombre de charges | appliquée |
| lot | §0 (point 4), §6.1, §6.6, §10.2, §13 (ligne 22), §15 | « toute machine temporelle de taille finie exige de l'énergie négative » | ajout de « sans singularité de courbure » (et surface initiale non compacte au §6.1) | résumé de Hawking (1992) | appliquée |
| lot | §3.3, §6.6, §13 (ligne 12) | énoncé attribué à [Tipler77] | énoncé attribué à [Tipler76] (*Phys. Rev. Lett.* 37, 879, ajouté au CSV) ; [Tipler77] conservé pour ce que dit son résumé | résumés des deux articles | appliquée (les deux sont cités) |
| lot | §13 (ligne 4), §2.2, §16, §1.1 | [MW90] cité pour kT ≈ 2–3 MeV | remplacé par [Page76a], [Page77] ; domaine de [MW90] précisé (0,02–100 GeV) | résumé de MacGibbon et Webber (1990) | appliquée |
| lot | §15 (piste de veille) | « ni fabricable (4×10²⁹ J, [Kugel24]) » | « ni fabricable par un moyen connu … la voie par concentration de lumière est exclue [Kugel24] » | résumé de [Kugel24] | appliquée |
| lot | §3.2 | [HKS23], [HKRS23] : « singularités de marée génériques » | [HKS23] « en espace anti-de Sitter » ; [HKRS23] décrit séparément (espace plat, termes de courbure d'ordre supérieur) | résumés des deux articles | appliquée |
| lot | §7.3 | « Seize ordres de grandeur » (0,4 mg ↔ 10¹² kg) | « Dix-huit » (seize à partir de 90 mg) | log₁₀(10¹² kg / 0,4 mg) = 18,4 | appliquée |
| lot | §1.2, §13 (ligne 7) | « ~10⁻¹² s » pour 227 kg | « ≈ 5×10⁻¹² s » | errata E3 du dossier (4,6–4,8 ps) ; script : 4,8×10⁻¹² s | appliquée |
| lot | `bibliographie_verifiee.csv` | [McGrew18], [Bothwell22] : titre de la prépublication avec la référence publiée | nouvelle colonne `titre_version_publiee`, renseignée pour les 67 notices dont le titre publié diffère | notices arXiv et Crossref | appliquée (généralisée) |
| lot | §0 bis | tableau non adossé à un script | `outils/ordres_de_grandeur.py` et sa sortie `donnees_brutes/ordres_de_grandeur.txt` ; valeurs retrouvées à l'identique | — | appliquée (script ajouté) |
| audit | §0 bis | coefficient 5,34×10²⁵ g³/s attribué à [MacGibbon91] | mention explicite : absent du résumé, cité de mémoire, recoupé à 1,3 % avec Page (1976) | résumé de MacGibbon (1991) : seulement M* ≈ 4–6×10¹⁴ g | appliquée (réserve explicitée) |

### 18.2 Corrections supplémentaires trouvées par l'Équipe H en appliquant les précédentes

| Objet | Constat | Correction |
|---|---|---|
| [FH06] dans le CSV | le DOI fourni par la notice arXiv désigne un **autre article** du même numéro de revue (auteur différent) : la revue et les pages de la version 1 étaient fausses | DOI correct vérifié par Crossref (*Annalen der Physik* 518, 109–128) |
| [FSW93] dans le CSV | le DOI fourni par la notice arXiv désigne l'**erratum** de 1995 | DOI de l'article de 1993 vérifié (*Phys. Rev. Lett.* 71, 1486–1489) |
| [AL17] dans le CSV | le DOI est celui de l'ouvrage collectif, non du chapitre | note ajoutée |
| Contrôle général | la version 1 acceptait le DOI d'une notice arXiv sans comparer les auteurs | contrôle auteurs + titre refait sur les 285 notices arXiv munies d'un DOI : 270 à auteurs concordants, 12 articles de collaborations (titres concordants), 3 anomalies ci-dessus |
| §1.1, §16 | « décharge de Schwinger » employé pour un trou de ~5×10¹⁵ g | le régime de type Schwinger ne vaut qu'au-dessus de 10¹⁷ g selon [Gibbons75] ; formulation corrigée |
| `RECHERCHES_SUPPLEMENTAIRES.md` | Q3, Q5, D7, D8 et tableau de synthèse reprenaient les formulations corrigées ci-dessus | alignés |

### 18.3 Effet sur les conclusions

Aucun verdict d'ensemble n'est renversé. Un verdict est **affaibli** : le passage « à travers l'anneau » passe
d'« invalide, confiance élevée » à « non établi, défavorisé, confiance moyenne » pour un trou noir réel. Les
verdicts qui portent sur la C204 elle-même (origine des singularités, masse, rayonnement, charge, échelle de la
structure de Kerr, énergie négative) sont inchangés, et celui sur la charge est désormais adossé au bon résultat
(≈ 6 e, [Page77]).

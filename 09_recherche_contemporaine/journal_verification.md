# Journal de vérification bibliographique — Équipe H (programme C204)

Session du 10 novembre 2026, 21 h 41 – 22 h 30, complétée en phase 7 (23 h 35 – 23 h 55) : voir §9.
Les compteurs du §1 sont ceux de l'état final (après phase 7) ; les §2 à §8 décrivent la session initiale.
Trace machine complète : `donnees_brutes/journal_requetes.jsonl` (une ligne par requête : service, URL, code HTTP,
horodatage). Réponses brutes : `donnees_brutes/cache/` (490 fichiers, données non fiables, jamais exécutées).

## 1. Bilan

| Catégorie | Nombre |
|---|---|
| Références scientifiques **vérifiées** par API (titre et auteur concordants) | **446** |
| — dont avec DOI | 418 |
| — dont avec identifiant arXiv | 344 |
| — dont avec DOI **et** arXiv (double contrôle arXiv + Crossref) | 316 |
| — dont datées de 2001 ou après | 371 |
| — dont datées de 2024 à 2026 | 63 |
| — dont restées à l'état de prépublication (aucune version publiée retrouvée) | 25 |
| Références **non vérifiées** (conservées, signalées, non utilisées comme preuve) | **1** ([Friedl83]) |
| Pages web institutionnelles ou tertiaires consultées | 17 |
| Pages web repérées par recherche mais non ouvertes | 2 |
| Candidats **écartés** (voir §4) | 12 |
| Titres attendus de mémoire **corrigés** d'après l'API | 22 |

Répartition des 446 références vérifiées par thème : 1 → 65 ; 2 → 34 ; 3 → 70 ; 4 → 26 ; 5 → 21 ; 6 → 64 ; 7 → 42 ;
8 → 42 ; 9 → 25 ; 10 → 35 ; 11 → 17 ; 12 → 5.

Contrôle de cohérence final : les 447 clés citées dans `RAPPORT_H.md` figurent toutes dans
`bibliographie_verifiee.csv` ; toutes les clés du CSV (hors pages web) sont citées dans le rapport.

## 2. Méthode

1. **Liste de candidats écrite de mémoire** (`outils/candidats*.txt`) : pour chaque référence, un identifiant
   (arXiv ou DOI) ou une requête, **plus** un fragment de titre et un nom d'auteur attendus.
2. **Interrogation des API** (`outils/verifier_biblio.py`, exécuté avec `python -I`, requêtes par `curl`) :
   - arXiv : `https://export.arxiv.org/api/query?id_list=…` par lots de 20 identifiants, pause de 3,2 s ;
     `search_query=…` pour les recherches ;
   - Crossref : `https://api.crossref.org/works/<DOI>` et `…/works?query.bibliographic=…`, pause de 1 s ;
   - INSPIRE-HEP : `https://inspirehep.net/api/literature?q=…` (recherches en texte intégral).
3. **Règle de décision** : une référence est « vérifiée » si le titre renvoyé contient le fragment attendu **et**
   si un auteur renvoyé concorde. Sinon elle passe « à revoir » et fait l'objet d'un contrôle manuel (§5).
4. **Double contrôle** : pour toute notice arXiv munie d'un DOI, la notice Crossref du DOI est récupérée (revue,
   volume, pages, année) ; 220 titres strictement concordants, 37 différences de forme (article initial « A »,
   titre remanié à la publication), toutes examinées.
5. **Versions publiées** : pour les notices arXiv sans DOI, recherche Crossref par **titre exact** et auteur
   (23 versions publiées retrouvées), avec garde-fou contre les homonymes (une « version publiée » antérieure de
   plus d'un an au dépôt arXiv est rejetée) ; 8 DOI supplémentaires vérifiés un à un (passe 4).
6. **Construction du CSV** : `outils/construire_csv.py` ; les valeurs (titre, auteurs, revue, année, DOI) sont
   celles **renvoyées par les API**, jamais celles de ma mémoire.
7. **Contenu** : les valeurs chiffrées attribuées aux articles dans le rapport viennent des **résumés** renvoyés
   par l'API arXiv (`outils/resumes.py` lit le cache). Les exceptions sont marquées « (de mémoire) ».
8. **Confidentialité** : agent utilisateur générique (`C204-biblio-check/1.0`), aucune adresse électronique,
   aucune donnée personnelle dans les requêtes.

## 3. Requêtes effectuées

| Service | Requêtes journalisées | HTTP 200 | Échecs |
|---|---|---|---|
| arXiv (API) | 35 (18 lots d'identifiants, 17 recherches) | 35 | 0 |
| Crossref (API) | 484 (416 par DOI, 12 recherches libres, 56 recherches de version publiée par titre) | 453 | 30 × HTTP 429 (limitation de débit, toutes rejouées avec succès) ; 1 × HTTP 404 (DOI erroné) |
| INSPIRE-HEP (API) | 6 journalisées (+ 2 lectures de détail non journalisées) | 6 | 0 |
| Pages web (curl) | 20 | 13 | 6 × HTTP 404 ; 1 × redirection non suivie jusqu'au document |
| Total | 545 | 507 | 38 |

Non journalisés dans le fichier machine : 3 requêtes d'essai initiales (une par service) ; les recherches et
lectures faites avec les outils WebSearch et WebFetch (§6).

### 3.1 Recherches arXiv (17)

`ti:"Could We Observe an Exploding Black Hole in the Near Future"` · `ti:"primordial black holes" AND ti:LHAASO` ·
`ti:"Polariton fluids as quantum field theory simulators"` · `ti:GW250114` · `ti:GW231123` · `ti:"GWTC-4.0"` ·
`ti:"Holography of time machines"` · `ti:"Life on a closed timelike curve"` · `ti:"single-ion clock" AND au:Marshall` ·
`ti:CARIOQA` · `ti:"Black Hole Spectroscopy" AND ti:GW250114` ·
`ti:"gravitationally induced entanglement" AND ti:experiment` (0 résultat) · `ti:"closed timelike curves" AND ti:Kerr` ·
`all:"Tipler sinusoid"` (**0 résultat**) · `ti:"persistent shadow of the supermassive black hole of M87"` (0 résultat) ·
`ti:"Metric for two equal Kerr black holes"` · `ti:"interacting Kerr black holes"`.

### 3.2 Contrôle terminologique (INSPIRE-HEP, texte intégral)

| Requête | Résultats |
|---|---|
| `fulltext:"Tipler sinusoid"` | **1** : arXiv:1008.3244 (J. Prezens, 2010) |
| `fulltext:"off-set Tipler"` | 0 |
| `t "Tipler sinusoid"` (titres) | 0 |
| `fulltext:"negative time event horizon"` | 0 |
| `fulltext:"dual-positive" and fulltext:singularity` | 15, tous sans rapport (géométrie différentielle, chromodynamique) |
| `fulltext:"Tipler cylinder"` | 5 |

Crossref, recherche libre `"Tipler sinusoid"` : aucun résultat pertinent (les premiers sont des chapitres de manuels
allemands sans rapport). La prépublication arXiv:1008.3244 a été téléchargée (PDF, 93 ko, rangé hors du projet dans
le dossier de résultats de l'outil) et son texte extrait par décompression des flux, sans exécution : on y lit
« offset Tipler sinusoid », l'idée d'envoyer des électrons sur des « mini black holes », aucune citation du récit
Titor, et les références à Kramer-Neugebauer (1980), Bonnor-Steadman (2004) et Tipler (1974). Page de notice
arXiv : une seule version (19 août 2010), 10 pages, pas de référence de revue.

### 3.3 Recherches Crossref libres (12)

Roberson, « A microprocessor-based portable computer: The IBM 5100 » (trouvée) · Hassitt et Lyon, « An APL
emulator on System/370 » (trouvée) · « Tipler sinusoid » (2 requêtes, rien) · Aziz et Howl, *Nature* 2025
(trouvée) · « Backreaction of Stimulated Hawking Radiation in an Optical Analogue » (trouvée) · « Measurement of
analogue Hawking radiation stimulated by a single photon » (trouvée) · Friedl, « SCAMP… », *PC Magazine* 1983
(**non trouvée**) · requête exploratoire « Katz IBM 5100… » (rien de pertinent ; a fait apparaître Falkoff 1991) ·
Bonnor et Steadman, « The double-Kerr solution » (trouvée) · Kramer et Neugebauer, « The superposition of two Kerr
solutions » (trouvée) · Falkoff, « The IBM family of APL systems » (trouvée).

## 4. Échecs, erreurs de mémoire et candidats écartés

| Clé | Problème | Traitement |
|---|---|---|
| CHR09 | identifiant arXiv de mémoire **faux** : 0907.1280 est « The Complexity of Guarding Terrains » | écartée ; bonne notice retrouvée par recherche de titre : arXiv:0903.0264 (clé CHR09b) |
| KN80 | DOI de mémoire **faux** (HTTP 404) | écartée ; bon DOI retrouvé par recherche : 10.1016/0375-9601(80)90556-3 (clé KN80b) |
| Baker25 | identifiant supposé 2503.19227 faux | référence obtenue par recherche de titre : arXiv:2503.10755 |
| GW250114, GW231123 | la recherche par titre renvoyait d'abord des analyses tierces | écartées ; articles de la collaboration vérifiés par identifiant (2509.08054, 2507.08219) |
| GWTC4 | la recherche renvoyait l'article « population » | remplacée par l'article de catalogue (2508.18082) |
| LHAASOPBH | résultat de recherche hors sujet | écartée ; la limite LHAASO est [PBH2505] (2505.24586) |
| EHTM87pers | non retrouvée par l'API arXiv | référence abandonnée, non citée |
| KerrCTC | résultat de recherche : prépublication isolée, non publiée | écartée, non citée |
| Bose1707, Katz78 | requêtes exploratoires sans résultat | écartées |
| TiplerSin | requête de contrôle (zéro résultat attendu et obtenu) | consignée au §3.2 |
| Lu26doi | doublon de [Lu26] | fusionnée |
| ACES24 | homonyme : la recherche par titre associait la prépublication de 2024 à un acte de conférence de 2011 du même premier auteur | association rejetée par le garde-fou ; la notice reste « prépublication arXiv » |
| Carter68 | HTTP 429 à la première passe | rejouée avec succès |
| Friedl83 | magazine sans DOI, introuvable par Crossref | **conservée comme « non vérifiée »** |

Pages web en échec (adresses supposées de mémoire, site du CERN réorganisé) : quatre communiqués de presse
`home.cern/news/press-release/…` (premier faisceau 2008, programme 2010, Higgs 2012, Run 3 2022) et la page
`…/high-luminosity-lhc` → HTTP 404 ; `home.cern/…/safety-lhc` et `hilumilhc.web.cern.ch/node/901` → HTTP 404
(WebFetch) ; `cern.ch/lsag/LSAG-Report.pdf` → redirection ; `cds.cern.ch/record/1111112` → page anti-robot ;
`bitsavers.org/…/SY31-0405-3_5100maint_Oct79.pdf` → HTTP 404 (le fichier existe sous un autre nom sur un miroir,
repéré par recherche). Conséquence : la chronologie du LHC s'appuie sur les articles vérifiés, sur les deux pages
CERN effectivement lues et sur la page du LEP ; les dates du 10 et du 19 septembre 2008 et du 30 mars 2010
proviennent de résultats de recherche (CERN, CERN Courier) non ouverts un à un.

## 5. Contrôle manuel des 22 discordances de titre

Dans les 22 cas l'identifiant était correct et l'auteur concordait ; seul le titre que j'attendais de mémoire
différait du titre exact (le plus souvent : titre de la version publiée contre titre de la prépublication). Le
titre exact de l'API a été retenu.

- CHT97 : « Spinning Down a Black Hole With Scalar Fields »
- CMS17 : « Search for black holes and other new phenomena in high-multiplicity final states… »
- Fermi18 : auteur renvoyé « The Fermi-LAT Collaboration » (j'attendais le premier signataire)
- Philbin08 : « Fiber-optical analogue of the event horizon »
- Torres17 : « Observation of superradiance in a vortex flow » (publié sous « Rotational superradiant scattering in a vortex flow »)
- Drori19 : « Observation of Stimulated Hawking Radiation in Optics » (publié : « … in an Optical Analogue »)
- Kundu22 : « Wormholes & Holography: An Introduction »
- Ori05 : « A new time-machine model with compact vacuum core » (publié : « A Class of Time-Machine Solutions… »)
- TT17 : « Traversable Achronal Retrograde Domains In Spacetime » (publié : « Traversable acausal retrograde domains… »)
- Lesovik19 : « Arrow of time and its reversal on IBM quantum computer »
- Schiansky23 : « Demonstration of universal time-reversal for quantum processes »
- Stromberg24 : « Experimental superposition of time directions »
- Delic20 : « Motional Quantum Ground State of a Levitated Nanoparticle from Room Temperature » (publié : « Cooling of a levitated nanoparticle… »)
- Westphal21 : orthographe « Millimeter » / « millimetre »
- Aspelmeyer22 : « How to avoid the appearance of a classical world in gravity experiments »
- Panda24 : « Measuring gravity by holding atoms » (publié : « Measuring gravitational attraction with a lattice atom interferometer »)
- McGrew18 : « Atomic clock performance beyond the geodetic limit » (publié : « … enabling geodesy below the centimetre level »)
- Brewer19 : « An ²⁷Al⁺ quantum-logic clock with systematic uncertainty below 10⁻¹⁸ »
- Oelker19 : « Optical clock intercomparison with 6×10⁻¹⁹ precision in one hour » (publié : « Demonstration of 4.8×10⁻¹⁷ stability at 1 s… »)
- BACON21 : « Frequency Ratio Measurements with 18-digit Accuracy Using a Network of Optical Clocks »
- Asenbaum17 : « Phase shift in atom interferometry due to spacetime curvature »
- BFLW16 : « A Quantum Focussing Conjecture »

## 6. Recherches web (WebSearch) et pages lues (WebFetch)

Ces outils ont servi à repérer les résultats de 2025-2026 postérieurs à mes connaissances ; **chaque article ainsi
repéré a ensuite été soumis aux API** (passes 2 et 3) avant d'être cité.

Recherches (22) : calendrier du LHC et du LS3 · expériences d'intrication induite par la gravité en 2026 · horloge
nucléaire au thorium en 2026 · CGPM 2026 et redéfinition de la seconde · GW250114 · limites d'explosion de trous
noirs primordiaux 2025-2026 · navigation par gradiomètre ou gravimètre quantique · records d'horloges optiques ·
stratégie européenne 2026 et FCC · métriques de distorsion 2025-2026 · premiers résultats d'ACES · article d'Aziz
et Howl et critiques · courbes temporelles fermées 2025-2026 · recherches de trous noirs au Run 3 · horloge au
lutécium · IBM 5100 et émulation · analogues de Hawking 2025-2026 · trous de ver traversables 2025-2026 · cadre
non linéaire de Kaplan et Rajendran · page de sûreté du LHC · chronologie du LHC · manuel de maintenance du 5100.

Pages lues avec succès : Wikipédia « IBM 5100 » et « Year 2038 problem » ; communiqué du Conseil du CERN du 22 mai
2026 ; « Updated schedule for CERN's accelerators » (4 octobre 2024) ; page CERN du LEP ; notes de version de
Debian 13 ; POSIX.1-2024 `<sys/types.h>` ; résolution 5 de la CGPM de 2022 ; notice arXiv 1008.3244.

Informations issues de la seule recherche web, **non recoupées par API** et signalées comme telles dans le
rapport : lancement d'ACES en avril 2025 ; proposition de 2026 sur la compression d'impulsion de miroirs ; projet
de gradiomètre quantique spatial pour 2030 ; début du LS3 en juillet 2026 d'après un article de juin 2026.

## 7. Lacunes

- Une seule référence « non vérifiée » subsiste ([Friedl83]) ; un livre de vulgarisation évoqué en hypothèse
  (livrable n° 13, ligne D6) n'est volontairement **pas** cité faute de vérification.
- 25 notices sont des prépublications sans version publiée retrouvée ; certaines sont des monographies ou des
  chapitres dont le titre publié diffère (par exemple [Christodoulou09], [DHRT21], [Visser02], [Fewster12]).
- Les notices Crossref ne contiennent en général pas de résumé : pour les références vérifiées **par DOI seul**
  (101 notices), seul le couple titre-auteur a été contrôlé, pas le contenu.
- INSPIRE-HEP n'a servi qu'au contrôle terminologique ; il n'a pas été utilisé comme troisième source systématique.
- La veille 2025-2026 dépend de recherches web ciblées et n'est pas exhaustive.

## 8. Reproduire

```
PY=.venv/bin/python
D=09_recherche_contemporaine
$PY -I $D/outils/verifier_biblio.py $D $D/outils/candidats.txt        resultats_passe1.json
$PY -I $D/outils/verifier_biblio.py $D $D/outils/candidats_passe2.txt resultats_passe2.json
$PY -I $D/outils/verifier_biblio.py $D $D/outils/candidats_passe3.txt resultats_passe3.json
$PY -I $D/outils/verifier_biblio.py $D $D/outils/candidats_passe4.txt resultats_passe4.json
$PY -I $D/outils/verifier_biblio.py $D $D/outils/candidats_passe5.txt resultats_passe5.json   # phase 7
$PY -I $D/outils/verifier_biblio.py $D $D/outils/candidats_passe6.txt resultats_passe6.json   # phase 7
$PY -I $D/outils/construire_csv.py  $D
$PY -I $D/outils/ordres_de_grandeur.py > $D/donnees_brutes/ordres_de_grandeur.txt            # phase 7
```

Le cache rend la relance quasi instantanée ; le supprimer (`donnees_brutes/cache/`) force une nouvelle interrogation
des API (environ 25 minutes à cause des pauses et de la limitation de débit de Crossref).

## 9. Phase 7 — corrections post-validation (10 novembre 2026, 23 h 35 – 23 h 55)

Demandes : `08_red_team/CORRECTIONS_A_APPLIQUER.md` (section 7, n° 57, n° 58, lot mineur) et
`08_red_team/audit_references.csv` (58 lignes concernant l'Équipe H : 50 conformes, 6 approximatives, 1 introuvable,
1 « mal employé » imputable à l'Équipe B). Détail des corrections : `RAPPORT_H.md` §18.

**Relecture des sources avant application** (7 requêtes INSPIRE-HEP par DOI, résumés lus) :

| Référence | Ce que dit le résumé | Conséquence |
|---|---|---|
| Page 1977 [Page77] | valeur quadratique moyenne de la charge : 6,14 e pour GMμ/ħc = 0, 2,76 e pour 0,4, 2,34 e au-delà | n° 58 appliquée |
| Gibbons 1975 [Gibbons75] | formule de type Schwinger au-dessus de 10¹⁷ g, traitement distinct en dessous ; aucun seuil en nombre de charges | n° 58 appliquée ; « décharge de Schwinger » reformulé |
| Hawking 1992 [Hawking92] | région finie « sans singularité de courbure », surface initiale non compacte, condition d'énergie faible moyennée | qualificatifs ajoutés |
| Tipler 1976 [Tipler76] | pas de région à courbes temporelles fermées à partir de données régulières dans un espace-temps asymptotiquement plat sans singularité | référence ajoutée |
| Tipler 1977 [Tipler77] | changement de topologie et théorèmes de singularité sans hypothèse de causalité | conservée pour ce contenu |
| MacGibbon et Webber 1990 [MW90] | températures de 0,02 à 100 GeV | retirée des passages à kT ≈ 2–3 MeV |
| MacGibbon 1991 [MacGibbon91] | porte sur M ≲ 4–6×10¹⁴ g ; le coefficient 5,34×10²⁵ n'y figure pas | réserve explicitée (cité de mémoire, recoupé à 1,3 %) |

Résumés relus dans le cache arXiv : [DL17] (« The proof suggests, however… »), [HKS23] (constante cosmologique
négative), [HKRS23], [Kugel24].

**Passes supplémentaires**
- Passe 5 (`outils/candidats_passe5.txt`) : [Tipler76], DOI 10.1103/PhysRevLett.37.879 — vérifiée.
- Passe 6 (`outils/candidats_passe6.txt`) : DOI corrects de [FH06] et [FSW93] — vérifiés.
- Passe 1 rejouée depuis le cache : notice Crossref de [Philbin08] récupérée (elle avait échoué en HTTP 429).

**Erreurs de la version 1 découvertes à cette occasion (non signalées par la Red Team)**
- [FH06] : le champ DOI de la notice arXiv 0801.0735 renvoie à un autre article du même numéro d'*Annalen der
  Physik* (auteur : Friedrich). Le CSV de la version 1 portait donc des pages fausses (84–108 au lieu de 109–128).
- [FSW93] : le champ DOI de la notice arXiv renvoie à l'erratum de 1995 (*Phys. Rev. Lett.* 75, 1872) et non à
  l'article de 1993 (71, 1486).
- [AL17] : le DOI est celui de l'ouvrage collectif.
- Cause : la version 1 reprenait le DOI inscrit dans la notice arXiv sans vérifier que la notice Crossref de ce DOI
  portait les mêmes auteurs (les écarts de titre étaient relevés mais tenus pour des variantes de forme). Contrôle refait sur les 285 notices arXiv munies d'un DOI : 270 à auteurs
  concordants, 12 articles de collaborations (auteurs listés différemment, titres concordants), 3 anomalies
  (celles ci-dessus), désormais traitées dans `outils/construire_csv.py`.

**Évolutions des outils et du CSV**
- `bibliographie_verifiee.csv` : nouvelle colonne `titre_version_publiee` (67 notices dont le titre publié diffère
  du titre de la notice arXiv) ; la colonne `titre` reste le titre exact de la notice interrogée.
- `outils/ordres_de_grandeur.py` (nouveau) : reproduit le tableau du §0 bis ; sortie dans
  `donnees_brutes/ordres_de_grandeur.txt`.
- Versions antérieures conservées : `donnees_brutes/RAPPORT_H_v1_avant_phase7.md`,
  `donnees_brutes/RECHERCHES_SUPPLEMENTAIRES_v1_avant_phase7.md`.

**Requêtes de la phase 7** : 7 INSPIRE-HEP et 4 Crossref (toutes HTTP 200). Total journalisé : 556 requêtes.

**Leçon de méthode** : la vérification par API établit l'**existence** d'une référence, pas la fidélité de l'usage
qui en est fait. Sur les 58 références relues par la Red Team, 6 étaient employées au-delà de ce que dit leur
résumé ; les 388 autres références de ce rapport n'ont pas fait l'objet d'une relecture de contenu indépendante.

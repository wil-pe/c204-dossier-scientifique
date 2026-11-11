# Programme C204 — Équipe G (red team) — Rapport n° 1

Version 1 — 10 novembre 2026. Rapport **indépendant** : rédigé sans lecture des dossiers 03 à 07 et 09.
Sources examinées : `00_DOSSIER_DE_BASE.md`, les 12 images de `01_archive/originaux/` (et leurs agrandissements),
le texte intégral `marinertalk_t7778_texte_integral.txt`. Tous les chiffres viennent de scripts exécutés
(`08_red_team/calculs/`, sorties `sortie_*.txt`).

Étiquettes du programme : **[DOC]** documenté, **[DÉD]** déduit, **[HYP]** hypothèse, **[INT]** interprétation de
tiers, **[VÉR]** fait vérifiable indépendamment.

---

## 0. Résumé

1. **La machine décrite ne peut pas fonctionner dans le cadre de la physique connue**, et cela ne tient pas à un
   détail : les paramètres revendiqués s'excluent mutuellement sur 10 à 25 ordres de grandeur
   (`figures/carte_coherence_masse.png`). Une pesanteur de 2 g à 1 m exige ~3×10¹¹ kg ; 300–500 MW de rayonnement de
   Hawking exigent 10¹² à 5×10¹² kg par singularité ; l'unité est donnée pour 227 kg ; l'échelle « 3–4 m » du champ
   exigerait la masse de Jupiter. L'auteur l'a lui-même reconnu : « If that were true, the unit could not be moved »
   (24-03-2001).
2. **Le corpus se contredit** sur ses paramètres centraux (rayonnement, évaporation, loi de divergence, dates) et
   contient des erreurs de physique de niveau licence (équivalence attribuée à la relativité restreinte, lecture
   fausse de l'expérience de Hafele-Keating). Détail : `contradictions_corpus.md` (20 contradictions, 14 erreurs).
3. **Les prédictions datées et précises ont échoué** (11 réfutées sur 23 relevées, aucune réussite non banale) ; le
   reste est banal, non échu, ou protégé par la clause des « lignes d'univers divergentes », qui rend le récit
   non réfutable. Détail : `tableau_predictions.csv`.
4. **Le dossier de base de l'institut est globalement fiable sur les formules** (tous les coefficients du §6 sont
   re-dérivés à mieux que 0,1 %), mais il contient 15 erreurs ou fragilités (§5 ci-dessous), dont une affirmation de
   « cohérence mutuelle » des chiffres de Titor qui ne résiste pas au calcul.
5. **Ce qui résiste** est listé honnêtement au §4 : c'est peu, et rien de cela ne plaide pour l'existence de la machine.

L'explication la plus économe reste un **récit de fiction interactif** bâti sur la vulgarisation disponible en 2000
(Hawking, Tipler, Kerr) et sur l'actualité de 1999–2001. L'identité de l'auteur n'est **pas établie**.

---

## 1. Méthode et limites

- Calculs : `01_physique_c204.py` (re-dérivation complète, hypothèses dans le code), `02_analyse_images.py` et
  `02b_skew_doc005.py` (images), `03_verif_references.py` (Crossref), `04_figure_coherence.py`,
  `05_tableau_predictions.py`, `corpus_recherche.py` (recherche datée dans le corpus).
- Émission de Hawking : trois modèles comparés — corps noir « naïf » photons seuls (celui du dossier de base),
  Page (1976) avec facteurs de corps gris, et Page + e± (domaine 5×10¹¹–10¹⁴ kg), convertis à 3 saveurs de neutrinos.
  Mon coefficient redonne celui de MacGibbon & Webber (1990) à 1,3 % près (5,41 contre 5,34×10²⁵ g³/s) et la masse
  d'évaporation en 13,8 Ga à 5,1×10¹¹ kg. **Les coefficients numériques de Page sont cités de mémoire** ; seule
  l'existence des articles est vérifiée en ligne.
- Dosimétrie et blindage : ordres de grandeur avec coefficients d'atténuation approximatifs (non re-téléchargés) ;
  les conclusions tiennent à plusieurs ordres de grandeur près, pas à un facteur 2.
- Corpus : compilation secondaire de 2023, sans balisage question/réponse. Chaque citation a été relue en contexte ;
  une erreur d'attribution reste possible (un cas probable est signalé : §2, S5).
- Images : copies recompressées de 239 à 1 023 px. L'analyse des niveaux d'erreur (ELA) et du bruit **ne peut ni
  prouver ni exclure** une retouche de l'original de 2000 sur un tel matériau.

---

## 2. Liste des objections

Hiérarchie : **FATALE** = suffit seule à exclure le fonctionnement ou la véracité, sans parade dans la physique
connue ; **SÉVÈRE** = très dommageable, parade seulement au prix d'hypothèses ad hoc ; **MINEURE** = indice.

### Objections FATALES

**F1 — Le quadrilatère masse / puissance / pesanteur / transportabilité est impossible.**
- *Énoncé.* Aucune masse ne satisfait à la fois « 500 livres », « 1,5–2 g », « 300–500 MW » et « plus petites qu'un électron ».
- *Démonstration.* 2 g à 1 m ⇒ M = 2g r²/G = **2,94×10¹¹ kg** (les deux singularités ensemble). 300–500 MW ⇒
  0,84–1,09×10¹² kg chacune (corps noir photons seuls) ou **3,9–5,1×10¹² kg** (Page complet). Réciproquement :
  deux trous noirs de 1,45×10¹¹ kg rayonnent ≥ 17 GW chacun, et deux de 4,4×10¹² kg donnent **60 g** à 1 m (2 g
  seulement à 5,5 m). Avec 227 kg, g(1 m) = 1,5×10⁻⁹ g, et un trou noir de 100 kg vit 8×10⁻¹¹ s en libérant
  9×10¹⁸ J. Écart entre la masse requise et la masse revendiquée : **facteur 10⁹ à 4×10¹⁰**.
- *Parade.* « Je n'ai pas tout dit » ; un résidu stable d'évaporation (14-03-2001) ; une pesanteur « simulée » sans masse.
- *Contre-réponse.* Un résidu de masse de Planck (2×10⁻⁸ kg) ne donne ni 2 g ni 300 MW. Une pesanteur sans
  masse-énergie source viole les équations d'Einstein, que l'auteur invoque par ailleurs (Kerr). L'auteur concède
  le point : « If that were true, the unit could not be moved ».
- *Confiance.* Très élevée.

**F2 — Aucun confinement ne peut porter les singularités.**
- *Démonstration.* Poids d'un trou noir de 10¹² kg : **9,8×10¹² N** (un milliard de tonnes-force) sur un objet de
  1,5 fm ; les deux ensemble pèsent 2,5×10⁹ fois la charge utile d'un pick-up (~800 kg). La charge que peut conserver un objet de ~1 fm
  est ≲ 170 e ≈ 3×10⁻¹⁷ C : au-delà, création de paires (le champ à l'horizon d'un trou noir extrême de 10¹² kg
  vaut 10²⁴ fois le champ de Schwinger ; la charge extrême n'est tenable qu'au-dessus de 5×10⁵ masses solaires),
  et l'émission de Hawking décharge le trou. Avec cette charge : champ électrique de lévitation **3,6×10²⁹ V/m**,
  ou gradient magnétique **1,6×10³⁶ T/m** sur le moment magnétique maximal. Même avec la charge extrême de 86 C
  (impossible) : 1,1×10¹¹ V/m ou 5×10¹⁷ T/m.
- *Parade.* « The magnetic field does not require the fantastic energies you might imagine » (10-02-2001).
- *Contre-réponse.* Affirmation sans mécanisme ; l'écart est de 30 ordres de grandeur avec les aimants existants.
- *Confiance.* Très élevée (l'ordre de grandeur de la charge soutenable peut varier d'un facteur 10 sans effet).

**F3 — L'échelle des effets de Kerr est le femtomètre, pas le mètre.**
- *Démonstration.* Ergosphère équatoriale ≤ 2GM/c², rayon de l'anneau ≤ GM/c². Pour 10¹² kg : 1,5×10⁻¹⁵ m et
  7×10⁻¹⁶ m ; pour 227 kg : 3×10⁻²⁵ m. Rapport aux 3,0–3,7 m revendiqués : **2×10¹⁵** (10²⁵ pour 227 kg). Une
  ergosphère de 3,35 m demande 2,3×10²⁷ kg (**1,2 masse de Jupiter**). De plus, dans Kerr, les courbes fermées de
  genre temps n'existent qu'à l'intérieur de l'horizon interne, près de l'anneau, dans la solution éternelle
  idéale (Carter 1968) ; cet horizon interne est instable (Poisson & Israel 1990).
- *Parade.* Les singularités « simulent » le passage dans l'anneau ; « the black hole comes to you ».
- *Contre-réponse.* Deux champs faibles superposés à 1 m (perturbation métrique ~10⁻¹⁵) ne reproduisent pas une
  région de champ fort. Aucune solution connue ne le fait ; Tipler (1976) et Hawking (1992) montrent au contraire
  qu'une région chronologiquement viciée créée dans un domaine fini exige singularité ou énergie négative.
- *Confiance.* Très élevée.

**F4 — « 10 ans par heure » : 20 ordres de grandeur manquants, et le mauvais sens.**
- *Démonstration.* Facteur requis : 87 660. Décalage gravitationnel à 1 m de 2×10¹² kg : GM/(rc²) = **1,5×10⁻¹⁵**,
  soit 3×10⁻¹¹ s en 6,1 h. Écart : **6×10¹⁹**. Atteindre 87 660 exigerait de stationner à r/r_s − 1 = 1,3×10⁻¹⁰
  de l'horizon. Et une dilatation, si forte soit-elle, ne mène que vers le futur.
- *Parade.* Le déplacement ne viendrait pas de la dilatation mais du « changement de ligne d'univers ».
- *Contre-réponse.* C'est alors un mécanisme non décrit ; or le texte fonde explicitement le principe sur la
  dilatation gravitationnelle (06-11-2000, 14-02-2001).
- *Confiance.* Très élevée.

**F5 — Le rayonnement tue l'opérateur en une milliseconde et n'est pas du « rayon X ».**
- *Démonstration.* 400 MW (Page) = 30 MW de photons, 146 MW d'e±, 221 MW de neutrinos. kT ≈ 2–13 MeV selon le
  modèle : photons de dizaines de MeV. À 1 m, sans blindage, photons primaires seuls : **3,8×10³ Gy/s** ; dose
  létale (5 Gy) en **1,3 ms** ; **8×10⁷ Gy** en 6,1 h. Ramener à 1 mSv par trajet demande ~25 longueurs
  d'atténuation, soit ≥ 36 cm de plomb dans toutes les directions (2 à 6 t), sans compter les photoneutrons —
  contre 227 kg. Le « cône d'évacuation » ouvert vers l'arrière (demi-angle ≈ 39° lu sur DOC-009, soit ~11 % de 4π :
  89 % d'une émission isotrope partirait ailleurs ; `06_mesures_graphiques.py`) délivrerait encore ~1 100 Gy/h à 100 m et ~1,6 Gy/h à 1 km. Un trou noir « à rayons X » (kT 1–100 keV) ne
  rayonne que 40 W à 0,4 MW : « rayons X » et « 300–500 MW » sont incompatibles. Enfin la source ne s'éteint
  pas (« I don't believe I said you could turn it on or off ») : elle aurait irradié le voisinage pendant les mois
  de stationnement chez les parents.
- *Parade.* « As long as you stay away from that [l'arrière], you should be okay » ; détecteur de fuites embarqué.
- *Contre-réponse.* L'émission de Hawking n'est pas collimatable : un « évent » n'est qu'une absence de blindage.
- *Confiance.* Très élevée sur l'ordre de grandeur (les coefficients d'atténuation sont approximatifs).

**F6 — Le bilan thermique est faux d'un facteur 10⁴ à 10⁵.**
- *Démonstration.* Puissance déposée (photons + e±) : **132–220 MW** dans un coffre de ~0,13 m³ et 1,8 m² de
  surface. Température d'équilibre radiatif : **6 000–6 800 K** (la photosphère solaire est à 5 800 K) ; 227 kg
  d'acier atteignent la fusion en ~1 s ; refroidir par vaporisation d'eau demande 51–85 kg/s, soit 1 100–1 900 t
  en 6,1 h. Le texte annonce « 100 to 120 degrees » (38–49 °C) et deux bouteilles de fluide (DOC-008).
- *Parade.* Les 300–500 MW seraient une puissance « disponible », non émise.
- *Contre-réponse.* Un trou noir n'a pas d'interrupteur ; sa luminosité est fixée par sa masse.
- *Confiance.* Très élevée.

**F7 — L'énergie de fabrication est hors de portée de tout accélérateur.**
- *Démonstration.* Mc² pour 2×10¹² kg : **1,8×10²⁹ J** = 3×10⁸ années d'énergie primaire mondiale = 470 s de la
  luminosité totale du Soleil = 5×10²⁰ faisceaux du LHC = 9×10²² tirs de la Z machine. Version minimale
  (2,9×10¹¹ kg) : 2,6×10²⁸ J. L'énergie par collision du LHC est 9×10¹⁴ fois sous la masse de Planck ; un trou
  noir « TeV » hypothétique pèserait ~10⁻²³ kg (10³⁵ fois moins) et vivrait ~10⁻²⁶ s.
- *Parade.* « E=MC squared can be solved for mass too » ; « Not that much ».
- *Contre-réponse.* La formule donne précisément le chiffre ci-dessus. « The electricity comes from batteries ».
- *Confiance.* Très élevée.

**F8 — Les prédictions datées ont échoué, et la clause d'échappement rend le reste non réfutable.**
- *Preuve.* `tableau_predictions.csv` : guerre civile de 2004/2005, plus de Jeux olympiques après 2004, guerre
  mondiale de 2015 et 3 milliards de morts, Omaha capitale, percée du CERN « dans un an » (LHC : 2008–2010),
  micro-trous noirs au CERN, « pandémie » de vMCJ (178 décès britanniques en trente ans) : **réfutés**. Les seuls
  énoncés exacts étaient publics en 2000 (bogue de 2038, programme spatial chinois, ESB, émulation du 5100).
- *Parade.* « Your worldline is about 2.5% different than mine » : sa venue aurait changé notre histoire.
- *Contre-réponse.* Cette parade immunise le récit contre tout test : elle le sort du champ scientifique. Elle
  contredit aussi son usage par l'auteur, qui présentait ces annonces comme des avertissements valables pour nous
  (« I am not confident things are different enough for you to avoid the conflict », 10-02-2001).
- *Confiance.* Très élevée sur les faits ; l'argument porte sur la crédibilité du témoin, pas sur la physique.

### Objections SÉVÈRES

**S1 — « Injection d'électrons » : inopérante et de signe incohérent.** 1 kg = 1,1×10³⁰ électrons = 1,8×10¹¹ C,
soit 2×10⁹ fois la charge extrême d'un trou de 10¹² kg ; amener un électron sur un trou déjà chargé de 1 C coûte
6×10¹⁸ MeV. L'unité est dite « dual-positive » mais on y injecte des charges négatives. *Parade :* les électrons
ne serviraient qu'au réglage fin de l'horizon interne. *Contre-réponse :* avec ≲ 170 e soutenables, l'effet
relatif est ~10⁻³⁷. *Confiance :* élevée.

**S2 — Marées et signature gravitationnelle.** Pour 2 g à 1 m, le gradient vaut 4 g/m : 4,1 g à 0,7 m, 1,2 g à
1,3 m ; ce n'est pas la sensation uniforme d'« ascenseur » décrite. Vers l'extérieur, 2×10¹² kg attirent à 0,14 g
à 10 m et produisent encore 1 µGal à **116 km** : un tel objet stationné ou roulant en Floride aurait été vu par
tout gravimètre et aurait fait tomber vers lui les objets du voisinage. *Parade :* champ « verrouillé » et
confiné par le « sinusoïde ». *Contre-réponse :* la gravité ne se blinde pas (pas de masse négative connue).
*Confiance :* élevée.

**S3 — Position de la Terre et « verrou de gravité ».** En 61 ans la Terre parcourt 5,7×10¹³ m (référentiel du
Soleil), 4,4×10¹⁴ m (Galaxie) : rapporté aux 6,1 h propres, 8,7 c à 108 c. Rester « collé » revient à suivre la
ligne d'univers de la Terre à rebours, ce qu'aucune géométrie connue ne permet. L'auteur concède : « the temporal
physics of this statement are wrong ». *Parade :* la machine ne se déplace pas, elle change de branche.
*Contre-réponse :* alors pourquoi 6 heures de trajet, 2 g, et un champ à maintenir ? *Confiance :* moyenne à
élevée (l'objection dépend du mécanisme supposé).

**S4 — Conservation de l'énergie et détournement d'Everett.** Faire disparaître d'une branche le véhicule et
~10¹² kg viole la conservation locale de l'énergie-impulsion ; la masse monopolaire d'un système isolé ne peut
pas varier (pas de rayonnement gravitationnel monopolaire). Dans l'interprétation d'Everett, les branches sont
des composantes d'un même état quantique : passer de l'une à l'autre exigerait une mécanique quantique non
linéaire (Polchinski 1991), jamais observée. *Parade :* physique nouvelle de 2034. *Contre-réponse :* recevable
seulement comme postulat (voir §3). *Confiance :* élevée dans le cadre connu.

**S5 — Erreurs de physique dans les explications.** Voir `contradictions_corpus.md` §2 : équivalence attribuée à
la relativité restreinte (« STR ») ; voyage temporel « under special relativity » ; négation de l'effet
cinématique de Hafele-Keating (−184 ns et +96 ns, vérifié) ; « accélération = dilatation » ; trajets
« space-like » à travers la singularité. *Parade :* « I am not a physicist ». *Contre-réponse :* recevable pour
un pilote, mais ces erreurs sont exactement celles d'un lecteur de vulgarisation de 2000, et un manuel
d'exploitation de 2034 ne les expliquerait pas. **Réserve honnête :** la phrase « il faudrait aller plus vite
que la lumière pour créer un trou noir » est très probablement d'un internaute, pas de Titor.
*Confiance :* élevée.

**S6 — Contradictions internes du corpus.** 20 relevées, dont 8 de gravité A (rayonnement, évaporation, chaleur,
loi de divergence « cumulative » / « not cumulative » / « not exponential » / « exponentially », interaction avec
la matière). *Parade :* messages improvisés, secret militaire. *Contre-réponse :* les contradictions portent
sur le fonctionnement même de la machine, et suivent les objections des internautes (révisions réactives).
*Confiance :* élevée (réserve : compilation secondaire).

**S7 — Incohérences entre documents graphiques.** (a) DOC-005 (prisme sur patins, turbomachines, 35 repères sans
légende) ne représente pas le coffre des photos ; (b) DOC-008 place les singularités côte à côte, DOC-007 l'une
derrière l'autre ; (c) proportions : rapport (écart entre bandes de danger) / (bande droite → panneau de texte)
= **1,94 [1,82 ; 2,07]** sur DOC-007 contre **1,23 [1,13 ; 1,34]** et **1,27 [1,17 ; 1,38]** sur les photos JT2 et
JT3 (écart ×1,56 ; `06_mesures_graphiques.py`), donc le « plan » n'est pas un relevé de l'objet photographié ;
(d) aucune cote, aucune unité, aucune tolérance dans un « manuel d'exploitation » ; (e) DOC-009 porte une mention
interne du type « … not to scale » (lecture de confiance faible). *Parade :* schémas de principe.
*Contre-réponse :* recevable pour (b) et (d), pas pour (a). *Confiance :* élevée pour (a), moyenne pour (c)
(bandes détectées automatiquement, panneau repéré à la main ; la perspective, limitée à ~7 % d'après la largeur
apparente des bandes, n'explique pas un facteur 1,5).

**S8 — Forme du « manuel de 2034 ».** Police à chasse fixe de type Courier pour l'en-tête et le texte, titre en
linéale grasse de type Arial/Helvetica sur DOC-005, trames de photocopie : l'esthétique d'un manuel technique
américain des années 1960–1990 produit avec un traitement de texte de 1995–2000. Titor admet : « the documents
posted were printed from a computer printer ». La mention **« RESTRICTED »** est une classification américaine
abolie par l'Executive Order 10501 (effet au 15-12-1953) [VÉR, en ligne]. Le manuel est daté du 21 mars 2034,
année donnée pour le premier prototype. *Parade :* monde d'après-guerre revenu aux machines à écrire ;
classification rétablie. *Contre-réponse :* possible, non réfutable, mais chaque trait a une explication plus
simple en 2000. *Confiance :* moyenne (indices convergents, aucun décisif).

**S9 — Mission IBM 5100.** La capacité « secrète » (émulation System/370 et System/3 en microcode) est réelle
mais décrite publiquement depuis les années 1970–1980 [VÉR, d'après Wikipédia et listes classiccmp] ; « traduire
entre APL, UNIX et le code IBM » n'a pas de sens technique ; les dimensions données sont fausses et confuses
(« 20" long, 10" high and 30" long »). *Parade :* il n'est pas informaticien. *Confiance :* moyenne.

### Objections MINEURES

- **M1 — Suspension.** « Strong suspension » pour 227 kg, soit trois passagers. *Confiance :* élevée, portée faible.
- **M2 — Divergence.** 1 % par 60 ans spécifiés, 2,5 % annoncés pour 61 ans.
- **M3 — Sol.** « Un pouce » mais 1 pied cube sur 6 pieds carrés = 2 pouces.
- **M4 — Trajet.** Machine « accurate from 50 to 60 years », premier saut de 61 ans.
- **M5 — Orthographe et vocabulaire.** « Steven Hawking », « time dialation », « Everret » ; termes sans
  existence dans la littérature (« Tipler sinusoid », « top-spin, dual-positive », « negative ergosphere »).
- **M6 — Remarques de 2001.** Un sceptique note des bandes de danger « misaligned » (ruban adhésif) et un
  dessin « very poor quality CAD » ; Titor ne conteste pas.
- **M7 — Analyse d'image.** Rien d'exploitable (§6).

---

## 3. « Steelman » : la version la plus défendable, puis son attaque

**Version la plus défendable.** On abandonne le rayonnement de Hawking, les « rayons X » et les 227 kg. L'unité
contient deux trous noirs de Kerr-Newman de ~1,5×10¹¹ kg chacun, quasi extrêmes (donc froids), en orbite mutuelle
à ~4–12 Hz pour 0,15–0,30 m d'écart (aucune force de maintien entre eux), portés par une technologie inconnue. Ils donnent bien 2 g à 1 m.
Le « sinusoïde » serait une modulation du champ qui déclenche un transfert vers une autre branche, par une
physique de gravité quantique découverte après 2001.

**Ce qu'il faut alors violer ou postuler.**
1. *Support du poids* (1,4×10¹² N par trou) : une interaction nouvelle à longue portée couplée aux trous noirs,
   ou de la masse négative. Rien de tel n'est connu.
2. *Charge quasi extrême* (12 C sur 0,2 fm) : suspendre la création de paires de Schwinger, donc l'électrodynamique
   quantique en champ fort.
3. *Chronologie* : violer la conjecture de protection chronologique (Hawking 1992) ou disposer d'énergie négative
   de l'ordre de −Rc²/G ≈ −4×10²⁷ kg pour une région de 3 m (Morris, Thorne & Yurtsever 1988 pour le principe).
4. *Changement de branche* : mécanique quantique non linéaire, ou couplage entre branches décohérées.
5. *Conservation* : le départ de 3×10¹¹ kg viole la conservation de la masse-énergie de la branche d'origine.
6. *Fabrication* : 2,6×10²⁸ J, soit 4×10⁷ années de production mondiale.

**Ce qui serait observable si elle existait.** Une anomalie de gravité de 1 µGal à ~40 km et de 0,14 g à
quelques mètres, permanente ; la déviation de la verticale près du véhicule ; au départ, une variation en
échelon du champ (interdite en relativité générale, donc signature d'une physique nouvelle) ; pour la version
« chaude », un flux gamma de dizaines de MeV mesurable à des kilomètres. Rien de tel n'a été rapporté, et les
photos montrent un coffre posé dans un habitacle en désordre, sans déformation ni objets attirés.

**Verdict.** Le steelman ne sauve la pesanteur de 2 g qu'en sacrifiant quatre des paramètres du corpus et en
postulant cinq éléments de physique nouvelle indépendants. Ce n'est plus la machine décrite.

---

## 4. Ce qui résiste à la critique

1. **Cohérence de vulgarisation entre trois chiffres.** Avec la formule du corps noir (photons seuls), 300–500 MW
   ⇒ r_s = 1,25–1,62 fm, soit 0,44–0,57 fois le rayon classique de l'électron : « a fraction of the size of an
   electron » est littéralement exact, et « size of an electron ↔ mass of a large mountain » (2,8 fm ↔ 1,9×10¹² kg)
   aussi. L'auteur a manifestement utilisé une source sérieuse sur les trous noirs primordiaux. Cela prouve une
   lecture, pas une machine — et la cohérence casse dès qu'on ajoute 2 g, 227 kg ou « bien plus petites ».
2. **Reissner-Nordström.** « Adding electric charge […] increases the diameter of the inner event horizons » est
   qualitativement correct, de même que les « deux horizons » des trous chargés ou en rotation.
3. **Coalescence.** Deux trous noirs de 10¹² kg à 0,3 m ne fusionnent pas : temps d'inspiral 10²⁵ ans, orbite
   stable à 11 Hz. L'objection de la coalescence, suggérée par la consigne, est **faible** ; je la retire.
4. **Tolérance humaine.** 1,5–2 g pendant 6 heures, assis, est supportable. Objection **faible**.
5. **Air.** Une personne dans ~3 m³ atteint ~4 % de CO₂ en 6 h : l'oxygène d'appoint et le détecteur mentionnés
   sont cohérents.
6. **Cohérence biographique.** Né en 1998, 13 ans en 2011, 4 ans de service jusqu'en 2015, 38 ans en 2036 : pas
   d'erreur d'arithmétique.
7. **Retouche des photos.** Je n'ai **aucun** indice de montage. Les photos montrent vraisemblablement un objet
   réel (un coffre aménagé) ; la question est sa nature, pas l'authenticité des pixels.
8. **Identité de l'auteur.** Non établie (§7) : on ne peut pas présenter l'hypothèse du canular monté par deux frères comme un fait.

---

## 5. Erreurs et fragilités relevées dans le DOSSIER DE BASE

| # | Lieu | Constat | Gravité |
|---|---|---|---|
| D1 | §6, « Constat provisoire » | Les trois chiffres sont dits « mutuellement cohérents ». Faux au-delà d'un ordre de grandeur : 2 g à 1 m ⇒ 2,9×10¹¹ kg **au total**, soit ≥ 17 GW par singularité ; 300–500 MW ⇒ 13,6 g à 1 m (corps noir) ou 60 g (Page). | Sévère (conclusion trop favorable au texte) |
| D2 | §6, puissance | Formule corps noir photons seuls (annoncée comme telle). L'émission réelle est ~21 fois plus forte (neutrinos, e±, corps gris) : 300–500 MW ⇒ **3,9–5,1×10¹² kg**, non ~10¹² kg. | Moyenne |
| D3 | §6, durée de vie | « M = 10¹² kg : ~3×10¹² ans » ; avec l'émission complète ~1,2×10¹¹ ans (la masse qui s'évapore en 13,8 Ga est ~5×10¹¹ kg). Surestimation ×20. Idem 100 kg : 4×10⁻¹² s plutôt que 10⁻¹⁰ s. | Mineure |
| D4 | §6 vs constat | « taille d'un proton, pas d'un électron » puis, trois lignes plus bas, « taille d'un électron ↔ masse d'une montagne » jugé cohérent. Le rayon classique de l'électron (2,82 fm) est du même ordre : la remarque est fragile et le dossier se contredit. | Mineure |
| D5 | §5.4 | « le rayonnement de Hawking est isotrope » : vrai sans rotation ; pour un trou de Kerr rapide, l'émission est anisotrope (sans être collimatable). À nuancer. | Mineure |
| D6 | §5.4 et §4 | Température « ~10¹¹ K » donnée pour 10¹² kg ; avec la masse corrigée (D2), kT ≈ 2–3 MeV (2,5–3×10¹⁰ K). La conclusion (pas des rayons X) tient. | Mineure |
| D7 | §2 (d) et §4 | Le premier véhicule est dit « absent du texte archivé ». Le texte contient « It's a 1967 Chevrolet » (04-11-2000) ; seul le mot « Corvette » est absent. Le tableau ne cite que le 4×4 de 1987. | Moyenne (lacune documentaire) |
| D8 | §3, DOC-009, repère 5 | Transcrit « X-ray venting cone » ; un internaute de mars 2001, sur une meilleure copie, lit « X-Ray Venting Zone » (corpus, 15-03-2001). Les deux mots ont quatre lettres. | Mineure (transcription douteuse) |
| D9 | §3, DOC-009, géométrie | « un cône en tirets partant du centre vers le haut-gauche » : il y a **deux** tirets symétriques (haut-gauche et bas-gauche), formant un cône d'ouverture ≈ 78° vers la gauche (l'arrière). | Mineure |
| D10 | §3, DOC-009, anneaux | « trois anneaux […] de taille croissante (négatif / nul / positif) » : c'est l'inverse pour les diamètres (le repère 2, « négatif », est le plus grand et le plus proche du centre) ; seules les cotes axiales 10-11-12 croissent. | Mineure |
| D11 | §3, DOC-009 | « aucune dimension numérique » : exact, mais une mention textuelle interne (au-dessus du repère 1, probablement « … area is not to scale ») n'est pas transcrite. Lecture de confiance faible. | Mineure |
| D12 | §3, DOC-006 | Confiance « élevée » pour l'en-tête de la couverture : sur cette copie il est illisible isolément et n'est reconstitué que par analogie avec DOC-005. | Mineure |
| D13 | §3, DOC-007 | Logements « situés au tiers gauche » : mesuré à 38 % de la longueur. Rapport L/P mesuré 3,26 (dossier : 3,3 — correct). | Négligeable |
| D14 | §4, tableau | Le dossier retient « si le confinement cède, la singularité s'évaporerait » sans signaler l'affirmation contraire du 13-03-2001, ni l'aveu du 24-03-2001 sur la masse. Ces deux passages manquent à la synthèse. | Moyenne |
| D15 | §3, DOC-005 | « impairs en haut 1→17 puis 18 à gauche » : formulation confuse ; les repères forment quatre rangées (9 + 8 en haut, 9 + 9 en bas, total 35 confirmé par détection de cercles). | Négligeable |

Vérifié et **correct** dans le dossier : tous les coefficients du §6 (r_s, T, P, t, Q_max, énergie de 227 kg),
les conversions d'unités, le facteur 87 660, le nombre de messages et de pièces jointes, l'inventaire.

---

## 6. Examen des documents graphiques

- **Fichiers.** Trois familles de compression distinctes (Q ≈ 77 progressif 4:2:2 avec JFIF ; Q ≈ 51 sans JFIF ;
  JT3 à part), aucun EXIF ; l'insigne porte le commentaire « Created by AccuSoft Corp. ». La compilation mêle donc
  des copies de provenances différentes ; cela ne dit rien des originaux.
- **ELA.** L'erreur de recompression suit le contraste local (corrélation 0,6 à 0,94) ; aucun bloc anormal sur
  JT1, un sur JT2, 22 sur 609 sur JT3, dispersés sur des arêtes. Sur les dessins au trait le test statistique
  n'a pas de sens (fond blanc). **Non conclusif**, comme attendu à cette résolution.
- **Bruit et netteté.** Les bandes jaunes n'ont ni bruit ni netteté distincts du reste de l'image de façon
  significative. Aucun indice d'incrustation.
- **Inclinaison du titre de DOC-005.** Une première mesure donnait +0,5° pour le titre contre 0,0° pour les
  rangées de repères ; la mesure robuste donne, pour le titre, +0,38° ± 0,37° (ligne 1) et 0,00° ± 0,34°
  (ligne 2), et pour les rangées de repères 0,00° à +0,23° : **différence non significative**.
  Je ne retiens pas l'hypothèse d'un titre rapporté sur cette base. Reste la différence de police entre en-tête
  et titre.
- **Contenu des photos [DOC, confiance moyenne].** Coffre sombre à couvercle relevé, bandes jaune/noir, étiquettes
  claires, panneau de texte ; cordon spiralé de type combiné téléphonique vers un boîtier à clavier ; banquette
  bleue à sangles ; objet rouge de type extincteur ; vitre. Rien n'y évoque un confinement, un blindage ou un
  refroidissement. Je ne peux identifier **aucun** objet du commerce avec certitude à cette résolution ; toute
  identification précise serait une supposition.
- **DOC-005.** Dessin dense de style manuel militaire, sans rapport de forme avec le coffre ; hypothèse la plus
  probable : illustration technique préexistante (groupe auxiliaire, conditionnement d'air ou groupe électrogène)
  réemployée avec un nouveau titre **[HYP]**. L'original n'a pas été retrouvé : c'est la vérification la plus
  rentable à confier à l'équipe A.

---

## 7. Explications alternatives : faits et suppositions

**Établi [VÉR, vérifié en ligne, sources secondaires].**
- Chronologie : messages sous le pseudonyme « TimeTravel_0 » à partir du 2 novembre 2000 (Time Travel Institute),
  nom « John Titor » à partir de janvier 2001 (forum Post-to-Post d'Art Bell), dernier message fin mars 2001.
  Deux télécopies de 1998 à Art Bell sont rattachées au récit par la tradition **[INT]**.
- Une société à but lucratif, la John Titor Foundation, a été créée le 16 septembre 2003 en Floride (boîte postale
  à Kissimmee) ; un avocat du divertissement en est donné comme dirigeant (rapport de 2009) ; la marque « John Titor » a
  été déposée puis abandonnée.
- Aucune trace d'état civil d'un John Titor.

**Allégué, non établi.**
- Une enquête d'un détective privé pour l'émission italienne *Voyager* (2008) et un rapport de 2009 désignent
  cet avocat et l'un de ses frères, informaticien (les sources divergent sur son prénom ; nous ne reproduisons
  pas les noms). Les intéressés ont démenti ; les indices sont circonstanciels.
- Joseph Matheny a déclaré en 2018 avoir conseillé les auteurs d'une « expérience littéraire » sans les nommer.

**Sources d'inspiration plausibles [HYP], toutes antérieures à novembre 2000.**
- Hawking, *A Brief History of Time* (1988), chapitre sur l'évaporation : trou noir primordial de la taille d'un
  noyau et de la masse d'une montagne, exploitable comme source d'énergie (résumé vérifié en ligne ; les expressions
  exactes « ten thousand megawatts » et « X rays and gamma rays » sont citées de mémoire, **non vérifiées**).
- Tipler (1974) et son livre *The Physics of Immortality* (1994), que Titor recommande nommément ; Kerr (1963) et
  les diagrammes de Penrose-Carter, présents dans toute la vulgarisation des années 1990.
- La controverse de l'été 1999 sur les « trous noirs » du RHIC (*Sunday Times*, 18 juillet 1999 ; rapport Busza,
  Jaffe, Sandweiss & Wilczek) : Titor s'y réfère (« about 18 months ago ») en la plaçant à tort au CERN.
- L'actualité : recomptage de Floride, crise de l'ESB, bogue de l'an 2000, siège de Waco (1993) comme modèle.

**Appréciation.** Le canular littéraire explique sans reste les trois traits du dossier : la justesse des
emprunts de vulgarisation, les erreurs dès que l'auteur improvise, et l'échec des prédictions. L'hypothèse
« voyageur authentique » exige au contraire les postulats du §3.

---

## 8. Références (statut de vérification)

Vérifiées par l'API Crossref le 10-11-2026 (`verif_en_ligne/references_crossref.json`) : Kerr 1963, *Phys. Rev.
Lett.* 11, 237 ; Carter 1968, *Phys. Rev.* 174, 1559 ; Hawking 1971, *MNRAS* 152, 75 ; Hawking 1974, *Nature* 248,
30 ; Hawking 1975, *Commun. Math. Phys.* 43, 199 ; Tipler 1974, *Phys. Rev. D* 9, 2203 ; Tipler 1976, *Phys. Rev.
Lett.* 37, 879 ; Hawking 1992, *Phys. Rev. D* 46, 603 ; Page 1976, *Phys. Rev. D* 13, 198 ; Page 1977, *Phys. Rev.
D* 16, 2402 ; MacGibbon & Webber 1990, *Phys. Rev. D* 41, 3052 ; Gibbons 1975, *Commun. Math. Phys.* 44, 245 ;
Poisson & Israel 1990, *Phys. Rev. D* 41, 1796 ; Hafele & Keating 1972, *Science* 177, 166 et 168 ; Bailey et al.
1977, *Nature* 268, 301 ; Arkani-Hamed, Dimopoulos & Dvali 1998, *Phys. Lett. B* 429, 263 ; Dimopoulos &
Landsberg 2001, *Phys. Rev. Lett.* 87, 161602 ; Giddings & Thomas 2002, *Phys. Rev. D* 65, 056010 ; Jaffe, Busza,
Wilczek & Sandweiss 2000, *Rev. Mod. Phys.* 72, 1125 ; Giddings & Mangano 2008, *Phys. Rev. D* 78, 035009 ; CMS
2011, *Phys. Lett. B* 697, 434 ; Deutsch 1991, *Phys. Rev. D* 44, 3197 ; Polchinski 1991, *Phys. Rev. Lett.* 66,
397 ; Majumdar 1947, *Phys. Rev.* 72, 390 ; Morris, Thorne & Yurtsever 1988, *Phys. Rev. Lett.* 61, 1446.
**Seule l'existence bibliographique est vérifiée ; les contenus sont cités de mémoire.**

Faits vérifiés par recherche web (sources secondaires) : chiffres de Hafele-Keating ; calendrier du LHC ; vMCJ
(NCJDRSU, Édimbourg) ; premier cas d'ESB aux États-Unis (CDC, USDA) ; abolition de « Restricted » (documents CIA et
NSA déclassifiés) ; controverse RHIC de 1999 ; notices Wikipédia « John Titor » et « IBM 5100 ».
Non vérifiés en ligne : date de Shenzhou 5, libellés exacts du livre de Hawking, coefficients d'atténuation,
valeurs numériques de Page (1976), article de presse sur Kaliningrad.

---

## 9. Fichiers produits (`08_red_team/`)

- `RAPPORT_RED_TEAM_1.md` (ce rapport) ; `contradictions_corpus.md` ; `tableau_predictions.csv`
- `calculs/01_physique_c204.py` → `sortie_01_physique.txt`, `resultats_physique.json`
- `calculs/02_analyse_images.py`, `02b_skew_doc005.py` → `sortie_02_images.txt`, `sortie_02b_skew.txt`, `resultats_images.json`
- `calculs/03_verif_references.py` → `sortie_03_references.txt`, `verif_en_ligne/references_crossref.json`
- `calculs/04_figure_coherence.py` → `figures/carte_coherence_masse.png`
- `calculs/05_tableau_predictions.py` ; `calculs/06_mesures_graphiques.py` → `sortie_06_mesures.txt` ; `calculs/corpus_recherche.py`
- `figures/ELA_*.png`, `figures/zoom_*.png`

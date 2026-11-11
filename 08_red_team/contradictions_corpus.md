# Équipe G (red team) — Contradictions internes et erreurs de physique du corpus textuel

Source unique : `01_archive/sources_web/marinertalk_t7778_texte_integral.txt` (compilation secondaire de 2023 ;
les dates sont celles des en-têtes de la compilation). Les positions « car. N » sont les décalages en caractères
dans ce fichier ; elles sont reproductibles avec `calculs/corpus_recherche.py "<motif>"`.
Toutes les citations sont **[DOC texte]** = « le texte dit que ». Citations volontairement brèves.

**Réserve de méthode.** La compilation n'identifie pas toujours qui parle : questions des internautes et réponses
attribuées à Titor s'enchaînent sans balise. Chaque ligne ci-dessous a été relue dans son contexte ; quand
l'attribution reste douteuse, c'est indiqué. Une compilation de 2023 peut aussi avoir altéré ou réordonné des
messages : les contradictions de *dates de message* sont donc moins solides que les contradictions de *contenu*.

Gravité : **A** = contradiction frontale sur un paramètre central ; **B** = incohérence nette mais périphérique ;
**C** = flottement, imprécision ou possible artefact de compilation.

## 1. Contradictions internes

| # | Thème | Affirmation 1 (date, car.) | Affirmation 2 (date, car.) | Gravité | Commentaire |
|---|---|---|---|---|---|
| C1 | Masse des singularités | « quite heavy, hot […] (300 - 500 megawatts) » (14-02-2001, 199321) ; pesanteur « about the equivalent of 2 Gs » (01-03-2001, 265772) | « If that were true [masse d'une petite montagne], the unit could not be moved. […] the mass […] was much smaller » (24-03-2001, ~305300) ; « It weighs about 500 pounds » (29-01-2001, 122881) | **A** | L'auteur admet lui-même qu'une masse de montagne rendrait l'unité intransportable, tout en conservant 2 g et 300–500 MW qui l'exigent (voir `calculs/01_physique_c204.py`, sections B, C). |
| C2 | Rayonnement | « it vents X-rays and Gamma radiation out of the rear » (04-11-2000, 9054) ; « It vents radiation » (22-11-2000, 38501) | « there is no extemporaneous matter near the singularity that would cause it to give off radiation or heat » (13-03-2001, 288655) | **A** | Deux jours plus tard : « I don't believe I ever said it didn't give off radiation. Yes, the device does give off x-rays » (15-03-2001, ~294800). |
| C3 | Stabilité / évaporation | « If the magnetic system failed […] the singularity would evaporate » (10-02-2001, 175972) | « The singularities are not unstable; therefore, uncontrolled evaporation is not possible » (13-03-2001, 288526) ; puis résidu « very stable naked singularity » attribué à Hawking (14-03-2001, 293367) | **A** | Trois régimes incompatibles : évaporation en cas de panne / pas d'évaporation possible / résidu stable (qui, à la masse de Planck, ne donnerait ni 2 g ni 300 MW). |
| C4 | Chaleur | « heavy, hot » ; unité « gets quite hot » (29-01-2001) ; « unapproachable » (19-02-2001, 220256) | même message C2 : rien qui puisse « give off radiation or heat » (13-03-2001) | **A** | — |
| C5 | Divergence : loi | « This is a roughly cumulative measurement » (29-01-2001, 123220) | « divergence is not cumulative » (13-03-2001, 284740) | **A** | — |
| C6 | Divergence : croissance | « Worldline changes are not exponential » (13-12-2000, 62343) | « the divergence grows exponentially as you move farther away » (25-02-2001, 244494) | **A** | — |
| C7 | Divergence : valeur | Unité « safe to about 1% for every sixty years at max power » (11-11-2000, 25811) | Trajet 2036→1975 (61 ans) : « about 1 or 2 percent » (04-11-2000), « about 2.5% » (15-11-2000, 31581), « about a 2% » (21-12-2000, 73798) | **B** | Écart d'un facteur 2 à 2,5 avec la spécification, et trois valeurs pour le même trajet. |
| C8 | Divergence : nature | « merely an empirical indicator » du champ de gravité local, « useless in describing characteristics of individual worldlines » (13-12-2000 ; 10-01-2001, 93546) | « The higher the divergence, the more "un-like" your destination worldline looks » (02-02-2001, 139356) ; « your worldline is about 2.5% different than mine » (29-01-2001) | **B** | La grandeur n'est jamais définie (pourcentage de quoi ?) ; noter aussi « .0002377% » (10-01-2001, 112260), précision à 4 chiffres sur une « estimation ». |
| C9 | Date du début de la guerre civile | « starts in 2005 » (07-11-2000, 19466) ; « in 2005 » (12-11-2000) ; « collapses in 2005 » (13-12-2000) ; en 2012 « in its 7th year » (13-12-2000, 65271) | « will start in 2004 » (31-01-2001, 132535) ; « It's 2004. I apologize for a missed key » (12-02-2001, 180812) | **B** | Correction a posteriori par l'auteur (« faute de frappe ») après quatre occurrences concordantes de 2005. |
| C10 | Année d'arrivée sur « notre » ligne | « go forward on (C) to the year 2000 » (21-12-2000, ~74100) ; « I sold the car when I arrived in 2000 » (06-11-2000, 11493) | « The first leg takes me to 1998. I think I said that quite a few times » (24-03-2001, ~305200) | **B** | L'arrivée en 1998 apparaît tardivement, avec l'allusion finale au bogue de l'an 2000 (« why Y2K didn't hit them »). |
| C11 | Véhicule | « It's a 1967 Chevrolet » (04-11-2000, 7755) | « It's a 1987 4WD » (08-11-2000, 25089) ; « Chevy truck » (08-02-2001) | **C** | Explication fournie par le texte (voiture vendue, unité transférée) : cohérent en soi. Mais la « suspension renforcée » invoquée pour 227 kg est sans objet (trois passagers). |
| C12 | Interaction avec la matière | « The singularities do not interact with any matter except the electrons » (01-03-2001, 264965) | traction de 2 g sur les occupants ; sol « raked […] an inch or so deep » ; tout objet touchant le champ « vaporized » (22-11-2000) | **A** | La gravitation agit sur toute masse-énergie : affirmer 2 g et « aucune interaction » est contradictoire. |
| C13 | Profondeur du puits | « The gravity well created by the singularities is not that large » (01-03-2001) | « replicates the affects of a Kerr black hole » (06-11-2000) ; lumière « bent around » le véhicule (04-11-2000) | **A** | Courber la lumière autour d'un véhicule exige un potentiel ~c² ; 2 g à 1 m correspond à ~10⁻¹⁶ c². |
| C14 | « Sans la masse » | « they create the same physical environment without all the mass » (10-02-2001, 176675) | « Adding mass to the singularities increases the area of gravitational influence » (10-01-2001, 102806) | **B** | — |
| C15 | Source de Tipler | « Tipler […] theory of massive rotating spheres » (06-11-2000, 15474) | « Tipler cylinders » (même message, 15833) | **C** | L'article de Tipler (1974) traite de cylindres. |
| C16 | Disparition au départ | « the machine will have appeared to have disappeared » (22-11-2000) | phrase suivante : « If the machine doesn't move its position […] the observer would not see it disappear at all » (22-11-2000, ~37600) | **B** | Dans le même paragraphe. |
| C17 | Prédictions | « I'm not aware of any predictions I made » (31-01-2001, 128514+) | dates et événements précis (2004/2005, 2015, JO, CERN, « Mad Cow ») | **B** | — |
| C18 | Taille de l'IBM 5100 | « about 20" long, 10" high and 30" long » (30-12-2000, 85514) | — | **C** | « long » deux fois ; dimensions supérieures à celles d'une machine décrite partout comme de la taille d'une petite valise (≈ 25 kg). |
| C19 | Sol emporté | « an inch or so deep » | « a cubic foot of dirt spread out over six square feet » (même message) | **C** | 1 pied cube / 6 pieds carrés = 2 pouces. |
| C20 | Origine de l'énergie | « The electricity comes from batteries » (31-01-2001) ; « the real energy is in creating the machine » (05-02-2001) | À un interlocuteur estimant qu'il faudrait l'énergie du Soleil : « Not that much » (13-03-2001, 285344) | **B** | 2×10¹² kg ⇒ 1,8×10²⁹ J = 470 s de la luminosité totale du Soleil ; 2,9×10¹¹ kg ⇒ 68 s. |

## 2. Erreurs de physique dans les explications

| # | Affirmation (date) | Pourquoi c'est faux ou confus | Statut |
|---|---|---|---|
| P1 | « As Einstein pointed out with his STR, the effects of gravity and acceleration are the same » (14-02-2001, 196431) | Le principe d'équivalence est le point de départ de la relativité **générale** (1907–1915), non de la relativité restreinte (« STR »). | Erreur nette |
| P2 | « Einstein's equations do indeed support […] controlled time travel under special relativity » (10-01-2001, 92120) ; trous noirs de Kerr « derived from special relativity » (10-01-2001, 113774) | Les courbes fermées de genre temps et la métrique de Kerr relèvent de la relativité générale ; la relativité restreinte (espace-temps plat) n'en contient aucune. | Erreur nette, répétée |
| P3 | Horloges embarquées : la différence « was not because the clock in the plane was moving, it was because the clock in the well was closer to the center of the Earth. Constant speed is not acceleration » (14-02-2001) | Hafele & Keating (1972) : les deux effets sont mesurés. Vers l'est : +144 ns (gravitation) −184 ns (cinématique) = −40 ns prédits, −59 ± 10 ns observés ; vers l'ouest : +179 +96 = +275 ns prédits, +273 ± 7 ns observés. L'écart est/ouest est **entièrement** cinématique. (Chiffres vérifiés en ligne.) | Erreur nette |
| P4 | « ACCELERATION = TIME DIALATION » ; « Constant speed is not acceleration » (14-02-2001) | En relativité restreinte la dilatation dépend de la vitesse, pas de l'accélération (hypothèse de l'horloge ; muons en anneau de stockage, Bailey et al. 1977, à ~10¹⁸ g sans effet propre de l'accélération). | Erreur nette |
| P5 | « the twin paradox of faster than light travel » (06-11-2000) | Le paradoxe des jumeaux ne fait intervenir que des vitesses subluminiques. | Confusion |
| P6 | Diagrammes de Penrose : « you can make simulated space-like trips (faster than light) through the singularity » (21-12-2000) ; « science agrees that you can travel to "other universes" » (10-01-2001) | Le diagramme de Kerr étendu (Carter 1968) décrit la solution **éternelle, idéale, du vide** ; les trajets y sont de genre temps (pas « space-like »), et l'horizon interne est instable (inflation de masse, Poisson & Israel 1990). Les « autres univers » sont des feuillets de l'extension analytique, pas les branches d'Everett. | Usage abusif |
| P7 | Identification Everett–Wheeler = « autres univers » de Kerr = « worldlines » (passim) | Trois notions sans rapport : branches de la fonction d'onde, régions asymptotiques d'une extension maximale, et « ligne d'univers » (qui, en relativité, est la trajectoire d'**une particule**, pas un univers). | Confusion de vocabulaire fondatrice |
| P8 | Microsingularités de « 300–500 MW » qui émettent des « rayons X » (passim) | 300–500 MW ⇒ kT ≈ 2–13 MeV (photons de dizaines de MeV, e±, neutrinos). Un trou noir à rayons X (kT 1–100 keV) rayonne 40 W – 0,4 MW. | Incohérence chiffrée |
| P9 | « electrified singularities also have two event horizons » ; « Adding electric charge […] increases the diameter of the inner event horizons » (10-01-2001) | **Correct** qualitativement (Reissner–Nordström : r₋ croît avec Q). Mais la charge soutenable par un objet de ~1 fm est ≲ 170 e (≈ 3×10⁻¹⁷ C) contre 86 C pour la charge extrême : effet relatif ~10⁻³⁷. | Exact mais inopérant |
| P10 | « The mass and gravitational field […] manipulated by "injecting" electrons » (06-11-2000) | 1 kg = 1,1×10³⁰ électrons = 1,8×10¹¹ C, soit 2×10⁹ fois la charge extrême d'un trou noir de 10¹² kg. | Impossible |
| P11 | « Yes, you can travel into the future and it takes less energy than going into the past » (06-11-2000) | Aucune base ; aller vers le futur ne demande que d'attendre. | Sans contenu |
| P12 | « biological effect » de la gravité qui ralentit « the movement of electrons in the orbits of their nucleus » ; « time shells » (17-11-2000) | La dilatation gravitationnelle n'est pas un effet mécanique sur les orbites ; modèle planétaire de l'atome. | Pseudo-physique |
| P13 | CERN produira des microsingularités « a fraction of the size of an electron », « heavy, hot » (14-02-2001) | Un trou noir de collisionneur (scénarios à dimensions supplémentaires, 1998–2002) aurait ~10⁻²³ kg et vivrait ~10⁻²⁶ s ; 10¹² kg est 10³⁵ fois plus. | Impossible |
| P14 | « Steven Hawking […] about the size of a proton » (14-02-2001) puis « A singularity about the size of an electron would only require the mass of a large mountain » (13-03-2001) | Cohérent **seulement** si « taille d'un électron » = rayon classique (2,8 fm ⇒ 1,9×10¹² kg). L'électron n'a pas de taille mesurée (< 10⁻¹⁸ m). | Approximation de vulgarisation |

## 3. Attribution douteuse (à ne pas porter au débit de Titor)

- « In order for them to make a black hole they would have to travel faster than light » (30-12-2000, 76172) :
  dans le contexte, c'est très probablement l'**objection d'un internaute**, à laquelle Titor répond (« I'm pretty
  sure they have a number of experiments… »). Cette erreur ne doit donc pas lui être imputée.
- « very poor quality CAD », « yellow caution tapes […] misaligned » (24-03-2001) : remarques d'un sceptique de
  l'époque, que Titor cite pour y répondre.

## 4. Indices d'emprunt à l'actualité de 1999–2001 (utile à l'axe 5)

- « a point of contention about 18 months ago […] some scientists who thought the experiments were too dangerous »
  (30-12-2000) : 18 mois avant = été 1999, date de la controverse sur les « trous noirs » du **RHIC** (Brookhaven,
  ions lourds — et non le CERN, ni des protons) ; article du *Sunday Times* du 18 juillet 1999 (vérifié en ligne).
- « elections » (11-11-2000) : écrit pendant le recomptage de Floride.
- « CJD […] "catching on" in Europe » (25-11-2000) : pic médiatique de la crise de l'ESB en Europe (nov. 2000).
- « two people are confirmed dead in Colorado from CJD from surgical instruments » (mars 2001) : fait divers
  d'actualité (non vérifié en ligne dans cette session).
- Renvoi explicite à Tipler, *The Physics of Immortality* (24-03-2001) et à Hawking (trous noirs primordiaux,
  « taille d'un proton », évaporation) : vulgarisation disponible avant 2000.

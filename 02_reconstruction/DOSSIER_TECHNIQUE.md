# Programme C204 — Dossier technique de la machine « telle que décrite » (Équipe A)

Version 1.1 — 10 novembre 2026 (corrections post-validation n° 7 à 16 appliquées : voir le journal en fin de document).

> **Statut de ce dossier.** Il décrit un objet tel que le montrent des images et des textes anonymes de 2000-2001.
> Il ne dit pas que cet objet déplace quoi que ce soit dans le temps : le voyage temporel n'a jamais été démontré
> et aucune source indépendante n'atteste l'existence d'une « C204 ». Chaque élément porte une étiquette :
> **[DOC]** lisible sur une pièce · **[DÉD]** déduit · **[HYP]** supposé par nous · **[INT]** avancé par des tiers ·
> **[VÉR]** vérifiable indépendamment. « Fonction revendiquée » signifie « fonction que le texte attribue », rien de plus.

Fichiers associés : `nomenclature.csv` (82 lignes), `dimensions.json`, `INCOHERENCES.md`, `plans/` (5 plans SVG + PNG
et le script `generer_plans.py`). Pièces et transcriptions : `../01_archive/INVENTAIRE.md`, `TRANSCRIPTIONS.md`.

## 1. Désignation

| Élément | Valeur | Source | Étiquette |
|---|---|---|---|
| Nom | « C204 Gravity Distortion Time Displacement Unit » | DOC-006, DOC-008 | DOC |
| Constructeur revendiqué | « General Electric », « Army Model » | DOC-015 (en toutes lettres), DOC-005 (« GE ») | DOC |
| Référence du manuel | « FILE: TMIM-200S/4005 », mention « RESTRICTED » | DOC-005, 006, 008, 009 | DOC |
| Date du manuel | 21 mars 2034, trois révisions jusqu'en mars 2035 | DOC-006 | DOC (révisions : confiance moyenne) |
| Type revendiqué | unité « à masse stationnaire » à deux micro-singularités | texte, 27 janv. 2001 | DOC |
| Variante citée | C206, plus grosse, 6 horloges | texte, 7 nov. 2000 et fin janv. 2001 | DOC |

## 2. Architecture d'ensemble

### 2.1 Enveloppe — plans 1, 2, 3

- **Coffre parallélépipédique allongé** à couvercle articulé sur le grand côté arrière par deux charnières [DOC :
  DOC-007, DOC-004]. Couvercle de même emprise que le corps [DOC]. Rapport longueur/profondeur 3,30 sur le dessin [DOC].
- Extérieur sombre ; au moins deux fermoirs en face avant [DOC : DOC-001, 002, 013] ; angles et patins sombres sur
  l'écorché seulement [HYP].
- Le couvercle ouvert tient à peu près vertical ou incliné vers l'arrière [DOC : DOC-001 à 004].
- Dimensions : voir §6. Aucune cote ne figure sur les documents.

### 2.2 Dessus du corps (« pont ») — plan 1

De gauche à droite, d'après DOC-007 [DOC], abscisses en fraction de la longueur L :

| Zone | Abscisse | Contenu | Recoupement photo |
|---|---|---|---|
| Compartiment gauche | 0,02–0,14 | surface tramée, sans repère | bloc clair à gauche sur DOC-004 et DOC-013 |
| Bande de danger 1 | 0,14–0,23 | chevrons obliques | bandes plus étroites sur les photos (I-03) |
| **Logements des singularités** | 0,30–0,46 | deux disques noirs Ø 0,094 L, l'un derrière l'autre : **1 MAIN** (côté charnière), **2 STEERING** (côté avant) | deux dômes noirs à sommet jaune dans des cuvettes carrées blanches (DOC-013) |
| Bande de danger 2 | 0,54–0,63 | chevrons | pièce jaune découpée à cadran rond sur DOC-013 (absente du dessin) |
| Colonne de commande | 0,71–0,78 | **4** écran de secours (en haut), **5** coupure d'urgence (rond, en bas) | bouton rouge et étiquettes claires (DOC-013) |
| Panneau de secours | 0,79–0,88 | **8** rangées de pastilles ; **6** interrupteur général (en bas) | grille sombre (DOC-013) |
| Compartiment droit | 0,89–0,99 | **9** « remote storage unit » | — |

### 2.3 Couvercle — plan 4

Face intérieure [DOC photo, DOC-001/002/003], de gauche à droite : étiquette jaune et petit boîtier gris ; bande de
danger ; notice blanche à bandeau rouge au-dessus d'une étiquette orange ; seconde bande de danger ; **placard de
texte** d'une douzaine de lignes = repère **7 « UNIT CONTROL INSTRUCTIONS »** [DÉD] ; panneau uni. Aucun de ces textes
n'est lisible.

### 2.4 Télécommande

Boîtier relié par câble au côté droit [DOC : DOC-007 repère 3]. Sur les photos : cordon **spiralé** ; boîtier jaune et
noir à clavier 4×4 et deux touches rouge et verte [DOC : DOC-013] ; un second objet noir, de la forme d'un combiné
ou d'un microphone à main, est relié au même cordon ou à un autre [DOC ; rôle inconnu]. Taille déduite du dessin :
environ 8 × 12 cm [DÉD].

### 2.5 Intérieur — plan 5

Aucun document ne montre l'intérieur de façon cohérente avec le pont :
- **DOC-008** est un synoptique de douze composants (voir §3) sans échelle ni implantation ;
- **DOC-005** est un écorché de 35 repères sans légende, dont le contenu ne recoupe pas DOC-008 (I-01).

Le plan 5 propose donc **deux variantes** : A (composants de DOC-008 rangés sous le pont de DOC-007) et B (lecture de
DOC-005). Les deux sont [HYP], incompatibles entre elles, et rien ne permet de choisir.

## 3. Systèmes fonctionnels revendiqués

| Système | Composants nommés | Documents | Fonction revendiquée (texte) | Ce qui est figuré | Étiquette |
|---|---|---|---|---|---|
| Singularités et confinement | carter (×2), bobine de champ, générateur/régulateur de champ (×2) | DOC-007 (1, 2), DOC-008 (1, 2, 3) | contenir deux micro-singularités chargées, les faire tourner, orienter leur axe | deux sphères ceinturées de barres noires, deux boîtiers dessous | DOC (noms) ; fonction : affirmation |
| Injection d'électrons | collecteur d'injection, régulateur, générateur d'électrons | DOC-008 (4, 5, 6) | modifier « masse et gravité » des singularités | un boîtier central relié aux deux sphères, un gros bloc rectangulaire à bande noire | DOC |
| Refroidissement | enveloppe, pompe, deux réservoirs | DOC-008 (8, 9, 10) | refroidir ; le texte ajoute « x-ray venting » | circuit en tirets, deux cylindres | DOC ; évacuation des rayons X **non figurée** |
| Mesure | capteur d'état de singularité (lecture « status » de confiance faible ; « stator » non exclu), unité de capteurs de gravité | DOC-008 (7, 11) | système VGL : échantillonner la gravité locale | petit carré sur chaque sphère ; boîtier double en haut | DOC |
| Temps et calcul | 4 horloges au césium, 3 calculateurs | texte seulement | datation, correction d'erreur | **rien** (« une autre page », non diffusée) | DOC texte |
| Énergie | batterie | DOC-008 (12) | alimentation électrique | batterie à six éléments, bornes + et − | DOC |
| Commande | écran de secours, coupure d'urgence, interrupteur, commandes de secours, télécommande | DOC-007 (3 à 9) | mise en route, arrêt, saisie des coordonnées (par la télécommande ? [HYP]) | voir §2.2 | DOC |
| Champ produit | trois « champs de temps » et trois « horizons », cône de rayons X, distances de masse | DOC-009 ; DOC-014 pour les valeurs en mètres | décrire la zone d'effet | double entonnoir d'ellipses | DOC pour les libellés ; grandeurs sans définition physique. **Les quatre valeurs en mètres ne figurent que sur DOC-014, dont l'attribution à l'auteur n'est pas établie** (§6.1) |

Le texte ne décrit **aucune séquence d'utilisation précise** au-delà de : saisie de coordonnées, montée en puissance,
compte à rebours sonore et lumineux, véhicule à l'arrêt, frein serré. Les « instructions de commande » du couvercle
sont illisibles. Un mode opératoire ne peut donc pas être reconstitué [constat].

## 4. Analyse des photographies du second véhicule (DOC-001, 002, 003)

### 4.1 Nature des images

Les trois fichiers les plus anciens mesurent 288×216 ou 480×350 px, dans un cadre gris, avec le bruit de chrominance
et le flou d'une **image vidéo figée** plutôt que d'une photographie [DÉD]. Ils ne portent aucune métadonnée.
DOC-001 et DOC-002 montrent les mêmes objets aux mêmes places (sacs, cordon, télécommande) sous deux éclairages
différents : deux moments d'une même installation [DÉD, déjà noté par un tiers en 2003].

### 4.2 Contenu de la scène

| Élément | Où | Lecture | Étiquette / confiance |
|---|---|---|---|
| Coffre ouvert, couvercle levé | centre | l'unité, posée en travers à hauteur d'allège de vitre, derrière un siège | DOC / élevée |
| Grande surface claire surexposée | DOC-001, haut | vitre latérale ou arrière ; montant et garniture bleus à gauche | DOC / moyenne |
| Siège en tissu bleu à plis verticaux | DOC-003, gauche | siège avant vu de face, la caméra étant devant lui | DÉD / moyenne |
| Deux bandes sombres verticales avec boucles métalliques | DOC-003 | **sangles** de type harnais ou ceinture, larges d'environ 31 px, espacées de 135 px | DOC (objet) ; HYP (largeur 48 mm) |
| Surface bleu-vert capitonnée à boutons | DOC-003 droite, DOC-001 bas | banquette ou couchette à capitonnage boutonné, typique d'un fourgon ou d'un utilitaire aménagé | DÉD / moyenne |
| Boîtier gris à gauche du coffre | les trois | objet distinct de l'unité | DOC |
| Cylindre blanc en haut à gauche | DOC-003 | rouleau ou appuie-tête | HYP |
| Tube clair à poignée sombre entre les sièges | DOC-003 | lu comme une arme d'épaule par un commentateur en 2003 [INT] ; non identifiable | INT / faible |
| Cordon spiralé et boîtier jaune/noir | DOC-001, 002, 003 | télécommande posée sur la banquette | DOC |
| Lueur rouge | DOC-002 | à la jonction du couvercle et du pont, sous le placard de texte ; voyant, ou reflet | DOC (image) ; nature HYP |
| Bandes jaunes et noires | couvercle | ruban adhésif de signalisation | DÉD / élevée |

### 4.3 Type d'habitacle

Compatible avec ce que dit le texte (« a 1987 4WD ») et la lettre DOC-016 (« 1987 CHEV… ») : un utilitaire ou un
tout-terrain à grande vitre, avec aménagement en velours capitonné [DÉD, confiance moyenne]. Modèle précis :
**non déterminable** ; « Suburban », « Blazer » ou « pick-up à cabine double » seraient de pures suppositions [HYP].

### 4.4 Le premier véhicule (DOC-013)

Photographie carrée, de rendu « développement instantané » (le texte parle d'un Polaroid) [DÉD]. Unité **ouverte**,
posée côté passager, couvercle appuyé contre la planche de bord, sous le pare-brise. Visible : jante de volant à
gauche, levier au plancher à pommeau sphérique, console, siège baquet en vinyle noir à plis. Compatible avec un coupé
américain des années 1960 ; l'auteur écrit « a 1967 Chevrolet » ; l'identification « Corvette » est **[INT]**.

### 4.5 Indices de mise en scène et de retouche

Ce qui peut être dit à cette résolution :

1. **Aucun indice de photomontage numérique n'est décelable**, mais l'examen est peu probant : les fichiers ont été
   recompressés plusieurs fois et font moins de 0,3 mégapixel ; une analyse des niveaux d'erreur n'aurait pas de sens.
2. **L'objet est réel et unique** : le même coffre, avec les mêmes marquages, apparaît dans deux habitacles et sous
   quatre angles ; les ombres et reflets sont cohérents avec le décor [DÉD].
3. Plusieurs détails ont l'aspect d'un **habillage rapporté sur un coffre de transport du commerce** [HYP, à
   considérer comme une lecture possible et non comme un fait] : ruban de signalisation collé ; notices de type
   « DANGER » standard ; formes jaunes découpées à bords irréguliers (DOC-013) ; « logements » qui sont, vus de près,
   deux dômes noirs à capuchon jaune de quelques centimètres ; télécommande dotée d'un clavier de type calculatrice ;
   combiné noir évoquant un microphone de radio.
4. Rien, sur aucune image, ne montre l'unité **en fonctionnement** : pas de câble d'alimentation, pas d'affichage
   lisible ; la lueur rouge de DOC-002 est le seul signe d'activité, et il est ambigu.
5. **DOC-012 (laser)** : voir INCOHERENCES.md, I-11. Le trait rouge se termine dans l'air et n'est courbé qu'à une
   extrémité ; plusieurs explications ordinaires sont possibles ; aucune n'est démontrable.

Le coffre lui-même (modèle, fabricant) **n'a pas été identifié**.

## 5. Provenance de l'écorché DOC-005

| | Constat |
|---|---|
| **Établi** | Annoncé par l'auteur le 25 novembre 2000 (« a cut-a-way drawing of the entire unit ») et le 8 mars 2001 ; diffusé à la mi-mars 2001 ; meilleure copie connue 1112×850 px (capturée en juillet 2003 sur deux sites, fichiers identiques) ; **jamais accompagné d'une légende**. Dessin à main levée, titre dans une autre police que le reste du manuel. |
| **Établi** | En 2004, un concours doté de 100 dollars a demandé de retrouver « the real image location » en dehors des sites Titor ; la page renvoyait au site de l'office américain des brevets. Le fil de discussion contemporain (septembre 2004) ne contient **que des suppositions** (spectromètre ancien, appareil de laboratoire des années 1960, pièces d'oscilloscope, sous-ensemble de sonar, microscope électronique…) ; personne n'y produit de source et rien n'indique que le prix ait été attribué. |
| **Établi** | Recherche inversée (TinEye, 10 nov. 2026) : 216 occurrences, toutes dans un contexte lié à l'affaire, la plus ancienne indexée en mars 2008. Aucune occurrence antérieure à 2001, aucune dans un manuel ou un brevet. Limite : cet index ne couvre ni les manuels papier ni les fonds non numérisés. |
| **Plausible** | Dessin original réalisé pour l'occasion [HYP] : style libre, quatre « blocs à ailettes » quasi identiques, formes génériques (cylindres, couronnes) sans détail de fixation ni de câblage, absence de légende. |
| **Plausible** | Dessin inspiré, sans copie directe, d'écorchés de matériel réel (groupe électrogène, turbomachine, compresseur) [HYP] : c'est l'impression d'ensemble relevée par le dossier de base, mais **aucune pièce ne l'étaye**. |
| **Inconnu** | Toute source imprimée antérieure. Nous n'avons pas pu consulter de fonds de manuels techniques militaires ou industriels ; une identification par un spécialiste du dessin technique reste à faire. |

Nous **n'affirmons donc pas** que l'écorché dérive d'une illustration réelle réutilisée. Ce qui est établi, c'est
qu'il n'est pas cohérent avec les autres pages (I-01, I-05) et qu'aucune légende n'a jamais circulé.

## 6. Dimensions retenues

Méthode complète, étalons et mesures en pixels : `dimensions.json`.

| Cote | Valeur | Incertitude | Étiquette | Origine |
|---|---|---|---|---|
| Longueur L | **0,85 m** | intervalle central 0,74–1,05 m ; plage 0,65–1,25 m ; loi bimodale | DÉD (mesures) sur étalons HYP ; confiance faible | médiane de cinq valeurs issues de **quatre méthodes non indépendantes** (sangle ; ruban de danger sous deux hypothèses exclusives, 2 et 3 pouces ; télécommande ; cordon) : 0,74 ; 0,77 ; 0,86 ; 0,92 ; 1,15 m. Quatre des cinq valeurs reposent sur un étalon de taille supposée, la cinquième sur un facteur de profondeur supposé |
| Profondeur P | 0,26 m | ± 0,07 m | DÉD | L / 3,30 (rapport lu sur DOC-007) |
| Hauteur du corps | 0,22 m | ± 0,07 m | DÉD | 0,85 × P (photos) |
| Épaisseur du couvercle | 0,065 m | fourchette 0,03–0,09 m | DÉD, via L | 0,25 × P (estimation visuelle). **Équipe E : 0,125 × P = 0,033 m** (rebord mesuré sur DOC-004) |
| Hauteur fermée | 0,285 m | fourchette inter-équipes 0,24–0,285 m ; plage 0,20–0,37 m | DÉD, via L | somme. **Équipe E : 0,242 m** à L = 0,85 m ; l'écart vient de l'épaisseur du couvercle |
| Diamètre des logements | **80 mm** (v1.0 : 77 mm) | ± 20 mm (échelle) | DÉD, via L | 0,094 × L, re-mesuré par profils de pixels (33–34 px sur 356,5) ; **Équipe E : 81 mm**. Sur DOC-013 les dômes eux-mêmes font 45–60 mm |
| Entraxe des logements | **91 mm** (v1.0 : 98 mm) | ± 22 mm | DÉD, via L | 0,107 × L, re-mesuré (37,5–39 px) ; Équipe E : 92,5 mm |
| Volume enveloppe | 0,062 m³ (0,053 m³ avec la hauteur de E) | intervalle central 0,035–0,117 m³ ; plage 0,024–0,20 m³ | DÉD, via L | produit, sans arrondi intermédiaire |
| Masse | 227 kg | — | DOC (texte) | « about 500 pounds » |
| Masse volumique impliquée | ≈ 3 700 kg/m³ (4 300 avec la hauteur de E) | intervalle central 1 900–6 400 ; plage 1 150–9 500 kg/m³ | DÉD, via L | 227 kg / volume ; v1.0 : 3 600 (dimensions arrondies) |
| Distances de champ | 5 m, 6 m, 8 m, 11 m | lecture : élevée (le 8 : élevée à moyenne) | **DOC pour la lecture ; provenance non établie** | DOC-014 seulement ; voir §6.1 ; contredites par le texte (I-10) |

**Portée statistique de L (correction n° 8).** Les cinq valeurs ne forment pas un échantillon : le ruban y figure
deux fois, sous deux hypothèses qui s'excluent ; la télécommande (0,92 m) est **la méthode la plus faible**, car son
rapport est lu sur le dessin DOC-007, dont I-03 montre qu'il n'est pas un relevé de l'objet (sans elle, la médiane
passe à 0,82–0,83 m). « ± 0,20 m » de la version 1.0 était la demi-étendue des cinq valeurs (écart-type 0,16 m), pas
une incertitude statistique. En mélange équipondéré de lois triangulaires, ruban compté une fois : intervalle à 68 %
0,74–1,02 m, à 95 % 0,65–1,24 m (calcul de la Red Team, reproduit par nous avec une autre graine). La distribution
est **bimodale** : un mode vers 0,75–0,90 m (ruban de 2 pouces, sangle, cordon), un mode vers 1,15 m (ruban de 3 pouces).

**Écart avec le dossier de base.** L'hypothèse H1 (L ≈ 1,20 m) reste possible mais peu probable (4 à 7 % dans ce
modèle). La valeur retenue est plus courte d'environ 30 %. Aucune des deux n'est mesurée : le seul étalon de taille
normalisée (une sangle) n'est pas dans le même plan que l'unité, et les autres étalons sont supposés. Les équipes aval
devraient **traiter L comme un paramètre entre 0,65 et 1,25 m**.

**Écart avec l'Équipe E (correction n° 15).** Mêmes L, P et hauteur de corps (0,22 m ici, 0,209 m chez E). Deux
écarts : (1) épaisseur du couvercle, 0,25 P ici (estimation visuelle) contre 0,125 P chez E (rebord mesuré sur
DOC-004, raccourci par la perspective) : aucune des deux valeurs n'est sûre, la fourchette est donnée ; (2) diamètre
et entraxe des logements : notre re-mesure par profils de pixels donne 33–34 px, soit la valeur de E ; **nos valeurs
de la version 1.0, lues à l'œil, étaient fausses (diamètre trop faible de 4 %, entraxe trop fort de 8 %)** et ont été corrigées.

### 6.1 Réserve de provenance sur les cotes en mètres (correction n° 7, bloquante)

Les valeurs 5, 6, 8 et 11 m sont **lisibles** sur une pièce : à ce titre leur *lecture* est [DOC]. Mais :

- elles n'existent que sur l'état **C204-DOC-014**, dont la première trace est une page d'un **site tiers** capturée
  le 11 juillet 2003 (description) et le 5 août 2003 (fichier) ; les archives de 2000-2002 ne montrent que l'état
  sans cotes (DOC-009), et aucun message du forum de 2000-2001 ne mentionne de distance en mètres ;
- DOC-014 a **la même trame matricielle** que le fichier `PT3.jpg` de DOC-009, public depuis 2000-2001 (barre des
  cotes 8 + 9 : 246 px sur les deux) : un tiers disposant de ce fichier pouvait produire DOC-014 (redressement,
  légende retapée, valeurs ajoutées), et l'erreur de numérotation 11-12-13 est typique d'une retouche ;
- les valeurs sont à peu près proportionnelles au dessin (12,3 ± 1,1 px/m) sans l'être exactement (cote 8 / cote 9
  dessinée 0,63 pour 8/11 = 0,73).

**L'attribution de ces quatre distances à l'auteur de 2000-2001 n'est donc pas établie.** Elle n'est pas réfutée
non plus : l'auteur a pu produire les deux états. Toute équipe qui utilise ces valeurs doit porter cette réserve.

## 7. Points pour lesquels plusieurs hypothèses sont laissées ouvertes

| Question | Hypothèses | Élément qui trancherait |
|---|---|---|
| Échelle absolue | 2 pouces (L ≈ 0,77 m) ou 3 pouces (L ≈ 1,15 m) pour le ruban de danger | identification du coffre ou d'un objet normalisé dans le plan de l'unité |
| Implantation interne | variante A (DOC-008) ou B (DOC-005) | une légende de DOC-005, ou la « page des horloges et calculateurs » |
| Forme des carters | sphères de la taille des ouvertures (≈ 8 cm) ou plus grandes sous le pont | aucune pièce connue |
| Angle d'ouverture du couvercle sur les photos | vertical (L/P réel ≈ 4,0–4,5) ou incliné de 34° à 43° (L/P = 3,3) | une vue de profil |
| Rôle du combiné noir (DOC-013) | microphone, seconde télécommande, accessoire sans rapport | meilleure copie de DOC-013 |
| Nature de la lueur rouge (DOC-002) | voyant du repère 4 ou 5, ou reflet | idem |
| Ordre et auteur des deux états de la page de champ | DOC-009 puis DOC-014, ou l'inverse ; DOC-014 produit par l'auteur, ou par un tiers à partir du fichier public | une trace de DOC-014 antérieure à 2003, ou le fichier source |
| Épaisseur du couvercle | 0,125 P (Équipe E) ou 0,25 P (Équipe A) | une vue de profil du coffre |
| Origine de l'écorché | dessin original, ou adaptation d'un dessin existant | source imprimée |

## 8. Ce qu'il faudrait pour aller plus loin

1. Les fichiers d'origine (album MSN de mars 2001 ; envois par courriel à la correspondante) : perdus à notre connaissance.
2. Le livre de 2003, qui contiendrait « several new photos » selon un site d'époque : non consulté.
3. Les archives du forum Post-to-Post, pour retrouver d'éventuelles descriptions chiffrées de l'unité.
4. Une expertise du coffre (transit case) par un connaisseur du matériel de surplus des années 1970-1990.

## Journal des corrections post-validation

Corrections demandées par la Red Team n° 2 (`08_red_team/CORRECTIONS_A_APPLIQUER.md`, section 1), appliquées le
10 novembre 2026. Chaque mesure citée par la Red Team a été **recontrôlée par nous** avant application
(profils de pixels sur `OP3.jpg`, `PT3.jpg`, `OP4.jpg`, `timetravel16_07.jpg` ; tirage de Monte-Carlo refait).

| N° | Gravité | Action | Fichiers touchés |
|---|---|---|---|
| 7 | bloquante | **Appliquée.** Lecture des cotes en mètres maintenue [DOC] ; ajout partout de la réserve « attribution à l'auteur non établie ; même trame que `PT3.jpg` ; un tiers pouvait les ajouter au fichier public ». Précision apportée : la première trace est du 11 juillet 2003 (page descriptive), le fichier du 5 août 2003. | `dimensions.json` (champs `provenance`, `attribution_auteur`, étiquette), `DOSSIER_TECHNIQUE.md` (§3, §6, §6.1, §7), `INCOHERENCES.md` (I-04, I-10), `nomenclature.csv` (009-1, 009-6 à 009-12), `../01_archive/INVENTAIRE.md`, `TRANSCRIPTIONS.md`, `HISTORIQUE.md` |
| 8 | importante | **Appliquée.** « Cinq estimations indépendantes » et « ± 0,20 m » retirés ; remplacés par « quatre méthodes non indépendantes », intervalle central 0,74–1,05 m, plage 0,65–1,25 m, loi bimodale. La clé `incertitude` (0,20) est conservée dans le JSON pour ne pas casser les scripts aval, avec un champ `nature_incertitude` qui dit ce qu'elle est. | `dimensions.json` (cote `L`, bloc `synthese_statistique_L`), `DOSSIER_TECHNIQUE.md` §6, `INCOHERENCES.md` I-09, `plans/` (5 plans régénérés) |
| 9 | importante | **Appliquée.** Étiquette de `L` : « DÉD (mesures) sur étalons HYP » ; cotes dérivées : « DÉD sur étalons HYP (via L) ». | `dimensions.json`, `plans/generer_plans.py`, plans |
| 10 | mineure | **Appliquée.** M3 signalée comme méthode la plus faible, à ne pas pondérer comme les autres ; médiane sans M3 indiquée. | `dimensions.json`, `DOSSIER_TECHNIQUE.md` §6 |
| 11 | importante | **Appliquée.** Colonne « 1re attestation » : « sujet créé le 4 nov. 2000 ; fichiers datés du 4 mars 2001 (voir réserve) » pour DOC-006, 008, 009, 013, 015. | `../01_archive/INVENTAIRE.md` |
| 12 | mineure | **Appliquée.** Trame identique à DOC-009, échelle 12,3 ± 1,1 px/m, rapport 0,63 contre 0,73 ; conséquence ajoutée : `timetravel16_07.jpg` est à l'échelle native, `OP4.jpg` en est une réduction. | `../01_archive/INVENTAIRE.md`, `TRANSCRIPTIONS.md` |
| 13 | mineure | **Appliquée.** Variante « stator » ajoutée pour DOC-008, ligne 7. | `../01_archive/TRANSCRIPTIONS.md`, `nomenclature.csv` (008-7), `DOSSIER_TECHNIQUE.md` §3 |
| 14 | mineure | **Appliquée.** DOC-014, ligne 8 : confiance « É à M » pour le chiffre 8. | `../01_archive/TRANSCRIPTIONS.md`, `dimensions.json` (`champ_8`), `nomenclature.csv` (009-8) |
| 15 | importante | **Appliquée, avec un écart assumé à la consigne « garder les valeurs nominales ».** Épaisseur du couvercle et hauteur fermée : nominaux conservés (0,065 m ; 0,285 m), fourchette donnée et valeurs de E citées (0,033 m ; 0,242 m). Diamètre et entraxe des logements : **nominaux corrigés** (77 → 80 mm ; 98 → 91 mm), parce que notre propre re-mesure par profils de pixels (33–34 px et 37,5–39 px sur 356,5 px) confirme la mesure de E et infirme notre lecture à l'œil de la version 1.0. Ordonnées des logements : 0,222/0,602 P → 0,24/0,59 P. | `dimensions.json` (R4, R5, R6, R10, `e_couv`, `H_ferme`, `D_log`, `entraxe_log`, `V`, `rho`), `DOSSIER_TECHNIQUE.md` §2.2 et §6, `INCOHERENCES.md` I-09, `plans/` |
| 16 | mineure | **Appliquée.** Envergures 11-12-13 à l'échelle des cotes : ≈ 26, 32 et 36 m [DÉD], recoupées par nous sur `OP4.jpg` (25,8 ; 32,7 ; 36,3 m). | `INCOHERENCES.md` I-10, `dimensions.json` (`champ_echelle`, `champ_envergures`), `nomenclature.csv` |

Aucune correction contestée. Valeurs modifiées : plage de L (0,60–1,15 → 0,65–1,25 m) ; volume (0,063 → 0,062 m³,
plage 0,022–0,149 → 0,024–0,20 m³) ; masse volumique (3 600 → 3 700 kg/m³, plage 1 500–10 500 → 1 150–9 500) ;
diamètre des logements (77 → 80 mm) ; entraxe (98 → 91 mm). Inchangées : L = 0,85 m, P = 0,26 m, hauteur de corps
0,22 m, épaisseur de couvercle 0,065 m, hauteur fermée 0,285 m.

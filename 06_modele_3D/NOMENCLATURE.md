# Nomenclature du modèle 3D « C204 » — Équipe E

Générée le 2026-11-11 par `generer_nomenclature.py` à partir de `modele_c204.json` (ne pas modifier à la main).

> Reconstruction d'un objet tel qu'il est DÉCRIT par des documents non authentifiés (messages « John Titor », 2000-2001). Rien n'atteste que l'objet ait existé ni fonctionné. Les « fonctions revendiquées » sont celles des légendes et du texte : elles ne sont ni vérifiées ni physiquement établies.

**Classement** (appliqué à la pièce TELLE QUE MODÉLISÉE, forme + position) : **[DOC]** documenté — Forme et position lisibles directement sur un document source archivé. Pour une pièce relevée sur la seule vue de dessus DOC-007, seule l'emprise en plan est documentée : épaisseur et relief sont supposés. ; **[DÉD]** déduit — Existence documentée (image ou texte) ; forme ou position inférée en croisant plusieurs documents. ; **[HYP]** hypothétique — Forme, taille ou position supposées par l'Équipe E ; volume générique non étayé par les sources.

La colonne « existence » précise d'où vient le composant lui-même : *DOC image* (visible sur un document), *DOC texte* (cité dans les messages seulement), *HYP* (ajouté par nous).

Dimensions à l'échelle hypothétique retenue (L = 0,85 m ± 0,20 m) : toute cote absolue hérite de cette incertitude (voir parametres.json).

## 1. Bilan

| Variante | Pièces | [DOC] | [DÉD] | [HYP] | Contenu |
|---|---|---|---|---|---|
| A | 173 | 88 | 52 | 33 | Variante A — coffre plat à couvercle articulé |
| A2 | 173 | 88 | 52 | 33 | Variante A′ — même coffre, autre disposition interne |
| B | 40 | 1 | 39 | 0 | Variante B — écorché DOC-005 (prisme biseauté) |

### Bilan par couche (variante A)

| Couche | [DOC] | [DÉD] | [HYP] | Ce que montrent les documents |
|---|---|---|---|---|
| Extérieur (coque, couvercle, platine, télécommande) | **88** | 18 | 3 | photos DOC-001/002/003, illustration DOC-004, dessin DOC-007 |
| **Intérieur (tout ce qui est sous la platine)** | **0** | 34 | 30 | rien : schéma de principe DOC-008 et texte seulement |

**Aucune pièce intérieure n'est [DOC].** Le total de 88 pièces [DOC] ne doit pas être lu comme « la moitié de l'objet est documentée » : 42 d'entre elles sont des motifs répétés (20 raies noires, 4 fonds de bande, 18 pastilles du pupitre) ; 48 n'ont pour source que le dessin DOC-007 (« [DOC] dessin »), que les photos contredisent sur la position des bandes ; 37 s'appuient à la fois sur le dessin et sur une photo ou sur DOC-004, et 3 sur les photos seules (« [DOC] photo »). Pour toute pièce relevée sur la seule vue de dessus, seule l'emprise en plan est documentée : épaisseur et relief sont supposés. La colonne `appui` de `nomenclature.csv` donne ce détail pièce par pièce.

Volume intérieur utile du coffre (variante A) : 35,0 L. Composants de DOC-008, à l'échelle de leur schéma : 3,1 L, soit **9 %** ; avec les volumes génériques [HYP] du texte (horloges, calculateurs : 0,6 L) : 3,7 L, soit **10 %**. Composants de DOC-008 dimensionnés à l'échelle du schéma calée sur le diamètre des logements : ils n'occupent qu'une faible part du volume intérieur. Indice que DOC-008 n'est pas à l'échelle, ou que l'essentiel du volume (et des 227 kg revendiqués) n'est pas décrit. Les horloges et calculateurs (texte seul) sont des volumes génériques [HYP], proportionnels à L : le taux ne dépend presque pas de l'échelle.

## 2. Les 9 repères de DOC-007 (vue de dessus, légende nette)

| N° | Légende d'origine | Traduction | Pièces | Classement | Remarques |
|---|---|---|---|---|---|
| 1 | « MAIN SINGULARITY » | Singularité principale | 2 | DOC ×1 / DÉD ×1 | Logement circulaire côté charnière (fy = 0,757 P) : collerette [DOC] et fût [DÉD], dans le cadre commun [DOC]. L'ensemble placé dessous (carter, enveloppe, bobines : 15 pièces [DÉD]) vient de DOC-008. |
| 2 | « STEERING SINGULARITY » | Singularité de direction | 2 | DOC ×1 / DÉD ×1 | Logement circulaire côté avant (fy = 0,401 P). Entraxe des deux logements : 0,356 P = 1,16 diamètre. Même remarque que pour le repère 1. |
| 3 | « REMOTE CONTROL UNIT » | Télécommande | 14 | DOC ×8 / DÉD ×6 | Boîtier filaire [DOC] (épaisseur [HYP]) ; cordon [DÉD] : spiralé sur DOC-004 et les photos, trait simple sur DOC-007, tracé 3D déduit. |
| 4 | « EMERGENCY VIEW SCREEN » | Écran de visualisation de secours | 2 | DOC | Double trait étroit sur presque toute la profondeur : nature exacte indéterminée. |
| 5 | « EMERGENCY DISCONNECT » | Coupure (déconnexion) d'urgence | 6 | DOC | Panneau blanc : fenêtre sombre à l'arrière, organe rond entre deux pavés hachurés à l'avant. Lueur rouge de DOC-002 à l'aplomb de la fenêtre [DÉD]. |
| 6 | « MAIN UNIT ON/OFF SWITCH » | Interrupteur général marche/arrêt | 3 | DOC | Boîtier carré contenant deux petits carrés, à l'avant du panneau 8. |
| 7 | « UNIT CONTROL INSTRUCTIONS » | Instructions de commande de l'unité | 1 | DOC | Plaque à l'intérieur du couvercle (texte illisible sur toutes les copies). |
| 8 | « EMERGENCY CONTROLS » | Commandes d'urgence | 20 | DOC | Plage blanche portant 18 pastilles (touches ou voyants) : 2 isolées + colonnes de 11 et de 5. |
| 9 | « REMOTE STORAGE UNIT » | Logement de rangement de la télécommande | 4 | HYP ×1 / DÉD ×3 | Compartiment ouvert à l'extrémité droite ; profondeur [HYP]. |

## 3. Les 12 repères de DOC-008 (« BASIC COMPONENTS », légende de confiance moyenne)

| N° | Légende (lecture) | Traduction | Pièces | Existence | Classement de la pièce | Pièce principale | Remarques |
|---|---|---|---|---|---|---|---|
| 1 | « Singularity drive housing » | Carter d'entraînement de singularité | 2 | DOC image | DÉD | sphère Ø 55 mm | 2 carters sphériques ; position sous les logements de DOC-007 [DÉD]. |
| 2 | « Singularity magnetic field coil » | Bobine de champ magnétique de singularité | 12 | DOC image | DÉD | tore Ø moy. 83, fil Ø 6 mm | 6 barres noires par carter, lues comme des spires coaxiales ; + 2 calottes d'extrémité par carter. |
| 3 | « Magnetic field generator / regulator » | Générateur / régulateur de champ magnétique | 2 | DOC image | DÉD | boîte 40 × 53 × 30 mm | 2 boîtiers sous les carters, reliés aux bobines par des tirets. |
| 4 | « Electron mass injector manifold » | Collecteur d'injection de masse d'électrons | 7 | DOC image | DÉD | cylindre Ø 5 × 117 mm | 3 tubes par carter + rampe commune vers le régulateur 5. |
| 5 | « Electron regulator » | Régulateur d'électrons | 1 | DOC image | DÉD | boîte 34 × 34 × 42 mm | Entre les deux carters, en dessous. |
| 6 | « Electron generator » | Générateur d'électrons | 2 | DOC image | HYP | boîte 78 × 78 × 142 mm | Grand rectangle à bande noire ; emplacement [HYP]. |
| 7 | « Singularity sensor booster » | Amplificateur de capteur de singularité | 2 | DOC image | DÉD | boîte 15 × 15 × 15 mm | Petit carré gris incliné à 45° sur chaque carter. |
| 8 | « Singularity cooling housing » | Enveloppe de refroidissement de singularité | 2 | DOC image | DÉD | sphère Ø 81 mm | Anneau noir entourant chaque carter ; rendu translucide. |
| 9 | « Singularity cooling pump » | Pompe de refroidissement | 1 | DOC image | HYP | boîte 64 × 32 × 25 mm | Rectangle gris sur le trait mixte ; emplacement [HYP]. |
| 10 | « Singularity cooling supply » | Réserve de fluide de refroidissement | 8 | DOC image | HYP | cylindre Ø 53 × 107 mm | 2 réservoirs à fonds bombés ; nature du fluide non précisée ; emplacement [HYP]. |
| 11 | « Gravity sensor unit » | Unité de capteurs de gravité | 4 | DOC image | HYP | boîte 88 × 40 × 35 mm | Capsule + module à deux tambours ; emplacement [HYP]. |
| 12 | « Battery supply » | Alimentation par batterie | 8 | DOC image | HYP | boîte 57 × 17 × 36 mm | 6 éléments, 2 bornes ; emplacement [HYP]. |

Éléments de DOC-008 **non numérotés** et modélisés : raccord supérieur de chaque carter (pavé blanc), calottes d'extrémité des bobines. Liaisons (traits pleins, tiretés, mixtes) : relevées dans `schema_electrique_hypothetique.svg` et `architecture_fonctionnelle.svg`, non modélisées en 3D (hormis le collecteur 4).

## 4. Les six systèmes du texte (message du 2 novembre 2000)

| N° | Système (texte) | Correspondance documentaire | Modélisation | Classement | Remarques |
|---|---|---|---|---|---|
| 1 | Logements magnétiques des deux micro-singularités | DOC-007 n°1, n°2 ; DOC-008 n°1, n°2, n°3 | Carters, bobines, calottes, générateurs/régulateurs de champ, logements de la platine | DOC (logements) / DÉD (carters, bobines) | Seul système décrit à la fois par le texte, DOC-007 et DOC-008. |
| 2 | Collecteur d'injection d'électrons (modifie masse et gravité) | DOC-008 n°4, n°5, n°6 | Tubes, rampe, régulateur, générateur d'électrons | DÉD (4, 5) / HYP (emplacement de 6) | Aucune trace sur DOC-007 ni sur les photos. |
| 3 | Refroidissement et évacuation des rayons X | DOC-008 n°8, n°9, n°10 ; DOC-009 n°5 (cône) | Enveloppes, pompe, réservoirs. ÉVACUATION DES RAYONS X : NON MODÉLISÉE | DÉD (8) / HYP (9, 10) / — (rayons X) | Aucun organe d'évacuation (trappe, cône, blindage) n'est visible sur le coffre : rien à modéliser sans inventer. |
| 4 | Capteurs de gravité (système VGL, variable gravity lock) | DOC-008 n°11 (et n°7 ?) | Capsule + module à tambours ; amplificateurs de capteur sur les carters | HYP (emplacement de 11) / DÉD (7) | Le lien entre le « sensor booster » (7) et le VGL n'est pas établi par les documents. |
| 5 | Horloges principales (4 au césium) | Aucune image | 4 volumes génériques | HYP (existence : DOC texte) | Forme, taille et emplacement entièrement supposés. |
| 6 | Calculateurs principaux (3, vote dit « Borda ») | Aucune image | 3 volumes génériques | HYP (existence : DOC texte) | Forme, taille et emplacement entièrement supposés. |

## 5. Éléments visibles sur les photos (DOC-001/002/003) et sur DOC-004

| Élément observé | Documents | Modélisation | Classement | Remarques |
|---|---|---|---|---|
| Coffre sombre, couvercle ouvert proche de la verticale | DOC-001, 002, 003, 004 | Corps + couvercle (10 pièces) | DOC | Angle retenu : 108° (DOC-004). |
| Bandes de danger jaunes à raies noires (couvercle et platine) | DOC-001, 002, 003 ; DOC-004 ; DOC-007 | 4 fonds + 20 raies | DOC | Position et nombre de raies d'après DOC-007 ; les photos montrent 2–3 raies et une bande 2 plus à gauche (écarts E4, E5). |
| Plaque d'instructions gris clair, lignée | DOC-001, 002, 003 ; DOC-004 ; DOC-007 n°7 | 1 pièce | DOC | — |
| Étiquette blanche à liseré rouge + étiquette orange (centre du couvercle) | DOC-001, 002, 003 ; DOC-004 (rectangle clair en deux parties) | 2 pièces | DOC | Absentes de DOC-007. |
| Étiquette jaune et élément gris (haut gauche du couvercle) | DOC-001, 002, 003 ; DOC-004 | 2 pièces | DOC / DÉD | Élément gris : étiquette ou boîtier, indéterminé. |
| Lueur rouge sur la platine (DOC-002) et reflet rouge au bas de la plaque | DOC-002 ; DOC-003 | Fenêtre du panneau 5 teintée en rouge | DÉD | À l'aplomb de la fenêtre du panneau 5 de DOC-007. |
| Cordon spiralé noir et clair sortant à droite | DOC-001, 002, 003 ; DOC-004 | 6 tronçons cylindriques | DÉD (existence : DOC image) | Tracé, longueur et diamètre déduits ou supposés ; pas de spires modélisées (cylindre lisse). |
| Boîtier de télécommande à étiquettes jaunes, posé devant l'unité | DOC-002, 003 ; DOC-004 ; DOC-007 n°3 | Boîtier + 7 détails | DOC | Détails d'après DOC-007. |
| Ferrures rondes claires sur la face avant | DOC-002, 003 ; DOC-004 (pièce claire près du bord gauche) | 2 loquets | DÉD | Nombre (2 ou 3) et positions incertains. |
| Renfoncement sombre sur la face d'extrémité gauche | DOC-004 | Poignée gauche (+ droite par symétrie) | DÉD / HYP | — |
| Étiquettes claires à repères d'angle de part et d'autre des logements ; plaquette striée devant | DOC-004 | 3 pièces | DÉD | Absentes de DOC-007. |
| Formes bombées visibles au fond des logements | DOC-004 | Sommet des carters et raccords supérieurs | DÉD | — |
| Tringle claire continue le long de la charnière | DOC-004 | NON MODÉLISÉE (2 charnières de DOC-007 retenues) | — | Écart E6. |
| Banquette bleue à sangles, objets divers, habitacle | DOC-001, 002, 003 | NON MODÉLISÉS (hors de l'unité) | — | Pistes d'étalonnage d'échelle pour l'Équipe A (sangle ≈ 47–50 mm). |

## 6. Variante B — les 35 repères de DOC-005 (écorché sans légende)

Aucune légende n'accompagne la copie archivée : toutes les fonctions sont **inconnues**. Les volumes sont des approximations génériques [DÉD] lues sur une vue unique ; leur profondeur est supposée. L'échelle est arbitraire (longueur prise égale à celle de la variante A).

| N° DOC-005 | Volume du modèle | Primitive (échelle arbitraire) | Classement |
|---|---|---|---|
| 1 | Petit bloc à ailettes (compartiment gauche, haut) | boîte 47 × 58 × 20 mm | DÉD |
| 2 | Boîtier parallélépipédique (compartiment gauche) | boîte 60 × 64 × 16 mm | DÉD |
| 3 | Bloc à lames empilées (dissipateur ?) | boîte 51 × 64 × 43 mm | DÉD |
| 4 | Élément à ailettes rayonnantes | cylindre Ø 76 × 47 mm | DÉD |
| 5 | Élément à ailettes rayonnantes | cylindre Ø 76 × 47 mm | DÉD |
| 6 | Élément à ailettes rayonnantes | cylindre Ø 76 × 47 mm | DÉD |
| 7 | Calotte du cylindre nervuré (1/2) ; Calotte du cylindre nervuré (2/2) ; Cylindre vertical nervuré à calotte (1/2) ; Cylindre vertical nervuré à calotte (2/2) | cylindre Ø 48 × 59 mm | DÉD |
| 8 | NON MODÉLISÉ — long tube oblique entre les repères 7 et 9 (élément mince, profondeur indéterminable) | — | — |
| 9 | Cloche ou couvercle cylindrique incliné | cylindre Ø 51 × 51 mm | DÉD |
| 10 | Cloche ou couvercle cylindrique incliné | cylindre Ø 51 × 51 mm | DÉD |
| 11 | Carter annulaire (volute ?) | tore Ø moy. 51, fil Ø 19 mm | DÉD |
| 12 | Carter annulaire (volute ?) | tore Ø moy. 51, fil Ø 19 mm | DÉD |
| 13 | Bloc à lames et ailettes rayonnantes (haut, centre-droit) | boîte 51 × 58 × 51 mm | DÉD |
| 14 | Gros réservoir cylindrique vertical | cylindre Ø 78 × 82 mm | DÉD |
| 15 | Fenêtre ou fente sombre | boîte 38 × 29 × 2 mm | DÉD |
| 16 | Plaque ou capot rectangulaire | boîte 110 × 152 × 6 mm | DÉD |
| 17 | Bouton rond bombé ; Fenêtre rectangulaire de la platine ; Platine à fenêtre et bouton bombé | boîte 47 × 123 × 2 mm | DÉD |
| 18 | Organes cylindriques empilés d'extrémité (galets ou poulies) | cylindre Ø 37 × 35 mm | DÉD |
| 19 | Grand réservoir cylindrique vertical d'extrémité | cylindre Ø 68 × 117 mm | DÉD |
| 20 | Boîtier ou trappe en façade avant gauche | boîte 47 × 18 × 39 mm | DÉD |
| 21 | Carter cylindrique horizontal (ligne d'arbre, gauche) | cylindre Ø 63 × 106 mm | DÉD |
| 22 | Carter cylindrique horizontal (ligne d'arbre, gauche) | cylindre Ø 63 × 106 mm | DÉD |
| 23 | Cylindre horizontal à alésage sombre (palier ou conduit) | cylindre Ø 51 × 70 mm | DÉD |
| 24 | Cylindre horizontal à alésage sombre (palier ou conduit) | cylindre Ø 51 × 70 mm | DÉD |
| 25 | Empilement de plaques (bas, centre) 1/2 | boîte 60 × 70 × 39 mm | DÉD |
| 26 | Roue à aubes ou rotor central | cylindre Ø 78 × 30 mm | DÉD |
| 27 | Empilement de plaques (bas, centre) 1/2 ; Roue à aubes ou rotor central | cylindre Ø 78 × 30 mm | DÉD |
| 28 | Empilement de plaques (bas, centre) 2/2 | boîte 60 × 70 × 39 mm | DÉD |
| 29 | Carter cylindrique ajouré (ligne d'arbre, droite) | cylindre Ø 49 × 102 mm | DÉD |
| 30 | Élément à ailettes rayonnantes (bas, droite) | cylindre Ø 85 × 41 mm | DÉD |
| 31 | Carter cylindrique ajouré (ligne d'arbre, droite) | cylindre Ø 49 × 102 mm | DÉD |
| 32 | Élément à ailettes rayonnantes (bas, droite) | cylindre Ø 85 × 41 mm | DÉD |
| 33 | Cloison transversale droite (bord du pupitre) | boîte 5 × 281 × 188 mm | DÉD |
| 34 | Cloison transversale droite (bord du pupitre) | boîte 5 × 281 × 188 mm | DÉD |
| 35 | Cadre de l'interrupteur rectangulaire ; Interrupteur rectangulaire | boîte 64 × 58 × 2 mm | DÉD |

Pièces de la variante B sans repère : Enveloppe prismatique à extrémités biseautées [DOC] ; Patin d'appui n°1 [DÉD] ; Patin d'appui n°2 [DÉD] ; Patin d'appui n°3 [DÉD] ; Patin d'appui n°4 [DÉD] ; Cloison transversale gauche [DÉD] ; Cylindre vertical nervuré à dôme (1/2) [DÉD] ; Cylindre vertical nervuré à dôme (2/2) [DÉD] ; Pont supérieur du pupitre (extrémité droite) [DÉD] ; Barre de séparation du pupitre [DÉD].

## 7. Nomenclature complète de la variante A, par ensemble

| Ensemble | Pièces | Classement | Repère | Documents | Fonction revendiquée (1re pièce) |
|---|---|---|---|---|---|
| Coffre — corps | 5 | HYP ×1 / DOC ×4 | — | DOC-001; DOC-002; DOC-003; DOC-004; DOC-007 | Enveloppe de l'unité (« C204 gravity distortion time displacement unit », DOC-006). |
| Coffre — accastillage | 6 | DÉD ×3 / HYP ×1 / DOC ×2 | — | DOC-002 / DOC-003; DOC-004; DOC-007 | Verrouillage du couvercle (interprétation ; non légendé). |
| Coffre — couvercle | 5 | DOC | — | DOC-001; DOC-002; DOC-003; DOC-004; DOC-007 | Couvercle articulé ; porte à l'intérieur les bandes de danger et la plaque d'instructions. |
| Couvercle — bande de danger n°1 | 6 | DOC | — | DOC-001; DOC-002; DOC-003; DOC-007 | Marquage de danger (non légendé). |
| Couvercle — bande de danger n°2 | 6 | DOC | — | DOC-001; DOC-002; DOC-003; DOC-007 | Marquage de danger (non légendé). |
| Couvercle — plaques et étiquettes | 5 | DOC ×4 / DÉD ×1 | divers | DOC-001; DOC-002; DOC-003; DOC-004; DOC-007 | « UNIT CONTROL INSTRUCTIONS » : instructions de commande de l'unité (texte illisible sur toutes les copies). |
| Platine — zones non légendées | 6 | DOC | — | DOC-007 | Non légendée. |
| Platine — bande de danger n°1 | 6 | DOC | — | DOC-001; DOC-002; DOC-003; DOC-007 | Marquage de danger (non légendé). |
| Platine — bande de danger n°2 | 6 | DOC | — | DOC-001; DOC-002; DOC-003; DOC-007 | Marquage de danger (non légendé). |
| Platine — plaques et étiquettes | 3 | DÉD | — | DOC-004 | Inconnue (non légendée). |
| Logements des singularités (platine) | 6 | DOC ×4 / DÉD ×2 | divers | DOC-004; DOC-007 | Cadre portant les logements « MAIN SINGULARITY » (arrière) et « STEERING SINGULARITY » (avant). |
| Écran de visualisation de secours (4) | 2 | DOC | DOC-007 n°4 | DOC-007 | Zone tramée portant l'« EMERGENCY VIEW SCREEN ». |
| Coupure d'urgence (5) | 6 | DOC | DOC-007 n°5 | DOC-002; DOC-007 | Panneau de l'« EMERGENCY DISCONNECT ». |
| Commandes d'urgence (8) | 20 | DOC | DOC-007 n°8 | DOC-004; DOC-007 | Panneau des « EMERGENCY CONTROLS » et du « MAIN UNIT ON/OFF SWITCH ». |
| Interrupteur général marche/arrêt (6) | 3 | DOC | DOC-007 n°6 | DOC-007 | « MAIN UNIT ON/OFF SWITCH » : interrupteur général marche/arrêt (revendiqué). |
| Logement de rangement de la télécommande (9) | 4 | HYP ×1 / DÉD ×3 | DOC-007 n°9 | DOC-004; DOC-007 | « REMOTE STORAGE UNIT » : rangement de la télécommande (revendiqué). |
| Télécommande filaire (3) | 8 | DOC | DOC-007 n°3 | DOC-001; DOC-002; DOC-003; DOC-004; DOC-007 | « REMOTE CONTROL UNIT » : télécommande reliée à l'unité par un cordon (revendiqué). |
| Cordon de la télécommande | 6 | DÉD | DOC-007 n°3 | DOC-001; DOC-002; DOC-003; DOC-004; DOC-007 | « REMOTE CONTROL UNIT » : télécommande reliée à l'unité par un cordon (revendiqué). |
| Ensemble singularité principale | 15 | DÉD | divers | DOC-004; DOC-007; DOC-008 | « Singularity drive housing » : carter censé contenir et entraîner une micro-singularité (revendiqué ; aucune réalité physique établie). |
| Ensemble singularité de direction | 15 | DÉD | divers | DOC-004; DOC-007; DOC-008 | « Singularity drive housing » : carter censé contenir et entraîner une micro-singularité (revendiqué ; aucune réalité physique établie). |
| Injection d'électrons (4, 5, 6) | 4 | DÉD ×2 / HYP ×2 | divers | DOC-008 | « Electron mass injector manifold » : rampe reliant les tubes des deux carters au régulateur 5 (revendiqué). |
| Générateurs / régulateurs de champ (3) | 2 | DÉD | DOC-008 n°3 | DOC-008 | « Magnetic field generator / regulator » : alimentation régulée des bobines (revendiqué). |
| Batterie (12) | 8 | HYP | DOC-008 n°12 | DOC-008 | « Battery supply » : alimentation électrique par batterie (revendiqué). |
| Réservoirs de fluide de refroidissement (10) | 8 | HYP | DOC-008 n°10 | DOC-008 | « Singularity cooling supply » : réserve de fluide de refroidissement (revendiqué ; nature du fluide non précisée). |
| Pompe de refroidissement (9) | 1 | HYP | DOC-008 n°9 | DOC-008 | « Singularity cooling pump » : pompe du circuit de refroidissement (revendiqué). |
| Unité de capteurs de gravité (11) | 4 | HYP | DOC-008 n°11 | DOC-008 | « Gravity sensor unit » : capteurs de gravité, système VGL censé verrouiller la position sur la gravité locale (revendiqué). |
| Horloges principales (texte) | 4 | HYP | texte, système 5 | Texte du 2 nov. 2000 | « Main clocks » : quatre horloges au césium servant de base de temps (revendiqué). |
| Calculateurs principaux (texte) | 3 | HYP | texte, système 6 | Texte du 2 nov. 2000 | « Main computer units » : trois calculateurs à vote majoritaire (revendiqué). |

La variante A′ (`A2`) contient les mêmes 173 pièces ; seuls changent les emplacements [HYP] (batterie, réservoirs, pompe, générateur d'électrons, capteurs, horloges, calculateurs).

Détail pièce par pièce (dimensions, positions, notes) : `nomenclature.csv` et fiches de `visionneuse.html`.

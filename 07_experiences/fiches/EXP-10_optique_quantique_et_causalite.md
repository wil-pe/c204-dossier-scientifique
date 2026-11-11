# EXP-10 — Optique quantique et causalité : gomme quantique à choix retardé, courbes temporelles fermées simulées par post-sélection, ordre causal indéfini

| | |
|---|---|
| **Niveaux** | N1 (gomme « de table » à pointeur laser : analogue **classique**) · N2 (TP avec source de paires de photons, si disponible) · **N3** (toutes les expériences proprement quantiques) |
| **Sous-système C204 lié** | aucun composant ; lien avec l'**interprétation** revendiquée (Everett-Wheeler, « autre ligne d'univers », absence de paradoxe) et avec DOC-010 (cône de divergence, création ultérieure probable) |
| **Statut physique** | Expériences : **démontrées**. Lecture « le futur modifie le passé » : **contredite** par le formalisme et par les données (aucun signal rétrograde). Courbes temporelles fermées réelles : **spéculatif**. |
| **Calculateur** | `calculs/calc10_optique_quantique_causalite.py` → `resultats/calc10_optique_quantique_causalite.txt`, `figures/calc10_gomme_quantique.png` |

## 1. Objectif

Présenter les expériences d'optique quantique le plus souvent invoquées à l'appui d'une « rétrocausalité »,
dire ce qu'elles mesurent, et montrer par le calcul que la statistique observable localement ne dépend jamais
d'un choix ultérieur ou distant.

## 2. Principe et équations [VÉR]

**Gomme quantique** (proposition : Scully & Drühl 1982). État de deux photons :
|ψ⟩ = (|chemin 1⟩|H⟩ + |chemin 2⟩|V⟩)/√2, le photon témoin portant l'information de chemin du photon signal.
- Témoin mesuré en base H/V : P(x, H) = P(x, V) = |A(x)|²/2 — pas de franges.
- Témoin mesuré en base D/A (±45°) : P(x, D) = |A|²·cos²(φ(x)/2), P(x, A) = |A|²·sin²(φ(x)/2) — franges et
  anti-franges.
- Dans tous les cas la **marginale** du signal vaut |A(x)|² : aucune frange sans tri par coïncidences.
  C'est le théorème de non-signalisation ; la date de la mesure du témoin n'intervient pas.

**Courbes temporelles fermées simulées** : modèle de Deutsch (1991) et modèle par post-sélection, « P-CTC »
(Lloyd et al. 2011). Dans un P-CTC à un qubit soumis à U, l'amplitude de réussite de la post-sélection est
⟨Φ|(U ⊗ 1)|Φ⟩ = Tr(U)/2 ; pour U(θ) = exp(−iθσ_x/2) : **P = cos²(θ/2)**.

**Interrupteur quantique** (Chiribella et al. 2013) : un qubit de contrôle en superposition commande l'ordre
A∘B ou B∘A. Mesuré en base ± : P(+) = ‖(AB + BA)ψ‖²/4, P(−) = ‖(AB − BA)ψ‖²/4.

## 3. État de l'art publié [VÉR]

| Référence | Expérience | Ce qui est mesuré |
|---|---|---|
| Kim et al. 2000 | gomme quantique à « choix » retardé (paires de photons) | franges uniquement dans les coïncidences triées |
| Walborn et al. 2002 | gomme à double fente, marquage par polarisation | idem, y compris en configuration retardée |
| Jacques et al. 2007 | choix retardé de Wheeler à photon unique | comportement conforme à la mécanique quantique |
| Ma et al. 2013 | effacement avec choix causalement déconnecté | idem, choix séparé par un intervalle du genre espace |
| Lloyd et al. 2011 | P-CTC par téléportation post-sélectionnée | les issues « paradoxales » ne sont jamais post-sélectionnées |
| Ringbauer et al. 2014 | simulation du modèle de Deutsch | comportements non linéaires **simulés**, non réalisés |
| Procopio et al. 2015 ; Rubino et al. 2017 ; Goswami et al. 2018 | interrupteur quantique photonique | superposition d'ordres ; témoin d'ordre causal indéfini |
| Oreshkov, Costa & Brukner 2012 | cadre théorique des corrélations sans ordre causal | — |

Revue : Ma, Kofler & Zeilinger 2016. Version de table : Hillmer & Kwiat 2007.

## 4. Matériel et coût indicatif

| Niveau | Matériel | Coût |
|---|---|---|
| **N1** | pointeur laser classe 2, fil fin ou cheveu (fait office de double fente), 3 morceaux de film polarisant, écran, appareil photo | 15–30 € |
| **N2** | banc pédagogique à paires de photons (cristal non linéaire pompé par diode, 2 détecteurs de photons uniques, compteur de coïncidences) ; à défaut, interféromètre de Mach-Zehnder + polariseurs (classique) | 20–60 k€ (banc) ; 500 € (classique) |
| **N3** | source de photons intriqués, modulateurs électro-optiques rapides, générateur quantique d'aléa, détecteurs à faible bruit, lignes à retard fibrées | laboratoire |

## 5. Protocole pas à pas

### N1 — Gomme « de table » (analogue classique)
1. Faisceau sur le fil : franges de diffraction-interférence sur l'écran.
2. Coller deux polariseurs **croisés** de part et d'autre du fil (gauche : horizontal ; droite : vertical) : les
   franges disparaissent (les deux chemins sont « marqués »).
3. Ajouter un troisième polariseur à 45° entre le fil et l'écran : les franges **reviennent** (moitié de
   l'intensité). À −45° : franges décalées d'une demi-période.
4. Mesurer la visibilité en fonction de l'angle β du troisième polariseur : attendu V = |sin 2β|.
5. Superposer (addition de photos) les images à +45° et −45° : image sans franges.
6. Conclure par écrit : tout s'explique par la loi de Malus et l'interférence d'ondes classiques.

### N2/N3 — Gomme à paires de photons
1. Aligner la source ; mesurer simples et coïncidences ; vérifier le caractère non classique (visibilité de
   polarisation en deux bases, ou g⁽²⁾ annoncé < 1).
2. Marquer les chemins du signal ; balayer le détecteur signal : histogramme des **simples** (plat) et des
   coïncidences selon le résultat et la base du témoin.
3. Allonger le trajet du témoin (fibre) pour que son analyse ait lieu **après** la détection du signal :
   reprendre. Comparer les histogrammes de simples avec et sans retard, et selon la base : test du χ².
4. N3 : choix de base par générateur aléatoire rapide, séparation du genre espace (Ma et al. 2013).

## 6. Signal attendu et budget de bruit (calculé)

- Écart maximal entre les distributions marginales du signal selon la base du témoin (calcul direct à partir de
  l'état) : **6,5 × 10⁻¹⁹** (précision machine). Visibilités : signal seul 0,000 ; coïncidences |H⟩ 0,000 ;
  coïncidences |D⟩ 1,000 ; |A⟩ 1,000 (anti-franges).
- Monte-Carlo illustratif (2 × 10⁵ paires par configuration) : χ² = 51,3 pour 59 degrés de liberté entre les deux
  histogrammes de simples — compatibles.
- N1 : V = 0 (β = 0°), 0,71 (22,5°), 1 (±45°). Polariseurs réels (fuite 1 %) : visibilité résiduelle ≈ 0,20 en
  configuration « marquée ».
- P-CTC : P = 1 ; 0,93 ; 0,75 ; 0,50 ; 0,25 ; 0,07 ; **0** pour θ = 0° … 180°.
- Interrupteur quantique : P(−) = 1 pour des portes qui anticommutent, P(+) = 1 pour des portes qui commutent,
  avec un seul usage de chacune.
- Budget N3 : 2 × 10⁵ simples/s, efficacité d'annonce 15 % → 3 × 10⁴ coïncidences/s, accidentelles 40/s (0,1 %) ;
  fente de balayage à 2 % → 600 coïncidences/s par point ; 10 s → 1,3 % par point ; 60 points × 2 bases ≈ 20 min.

## 7. Durée

N1 : 2 h. N2 : 2 à 3 séances. N3 : semaines à mois.

## 8. Analyse des données

Visibilités avec incertitudes de Poisson ; soustraction des accidentelles ; test d'homogénéité (χ²) des
histogrammes de simples entre configurations ; aucune sélection de données après ouverture des résultats.

## 9. Sécurité

N1 : laser de classe 2 au plus. N2/N3 : la diode de pompe (souvent classe 3B, 405 nm) impose un **cadre de
laboratoire** : capotage, lunettes adaptées, responsable sécurité laser — pas d'usage domestique.

## 10. Ce que cela prouve — et ne prouve PAS

**Prouve** : les corrélations quantiques sont celles que prédit la théorie ; les franges n'existent que dans des
sous-ensembles **triés après coup** au moyen d'une information transmise classiquement ; la distribution vue
localement est strictement indépendante de tout choix distant ou ultérieur.

**Ne prouve pas** :
- qu'un choix futur modifie un événement passé (rien d'observable ne change) ;
- qu'une courbe temporelle fermée existe : les expériences « P-CTC » et « Deutsch » sont des **simulations**
  par post-sélection ou par circuit équivalent ; les photons ne remontent pas le temps ; on **jette** les essais
  incohérents (probabilité de réussite cos²(θ/2), nulle pour le circuit paradoxal) ;
- qu'un « ordre causal indéfini » existe dans l'espace-temps : dans un interrupteur quantique, le photon
  traverse des composants fixes d'un interféromètre ; l'indétermination porte sur l'ordre des **opérations**
  appliquées au système. Le caractère « authentique » ou « simulé » de ces réalisations est débattu ;
- quoi que ce soit en faveur ou en défaveur de l'interprétation des mondes multiples : toutes les
  interprétations prédisent les mêmes fréquences d'événements.

## 11. Lien avec la C204 [DÉD]

L'argument attribué à Titor (« chaque voyage aboutit sur une autre ligne d'univers, donc pas de paradoxe »)
emprunte le vocabulaire d'Everett. Mais dans la théorie d'Everett, les branches n'interagissent pas : aucun
mécanisme n'y permet à un objet macroscopique de passer d'une branche à une autre, et une « divergence de 1 à
2,5 % » n'y est pas une grandeur définie (dossier §4). Les expériences ci-dessus n'apportent aucun appui à un
tel transfert ; elles vérifient au contraire l'impossibilité de signaler vers le passé.

## 12. Confiance et limites

Calcul de non-signalisation : confiance **élevée** (exact). Résumés des expériences publiées : **moyenne à
élevée** (références vérifiées ; détails à relire dans les articles). Le calcul P-CTC est un calcul de principe,
non une reproduction des données. L'expérience N1 est une analogie classique et doit être présentée comme telle.

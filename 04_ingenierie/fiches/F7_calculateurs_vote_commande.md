# Fiche F7 — Trois calculateurs à vote (« Borda »), commande-contrôle, télécommande, arrêt d'urgence

Repères : texte (« main computer units (3) ») ; DOC-007 r.3 (télécommande), r.4 (écran de secours),
r.5 (coupure d'urgence), r.6 (marche/arrêt), r.8 (commandes d'urgence), r.9 (rangement de la télécommande).
Calculs : `calculs/c08_calculateurs_vote.py` → `resultats/c08_calculateurs.json`.

## 1. Ce que dit la source

**[DOC texte]** « The computer system is connected to the unit through an electrical bus. There are actually
three computers linked together that take the same signals from the gravity sensors and clocks. They use a
Borda error correcting protocol that checks the integrity of the data and trips the VGL system » ;
« fail-safe system during travel that drops out in case of a unit shutdown or radical departure in gravity
readings » ; la télécommande affiche « time in transit, time to destination, VGL variance and unit temperature ».
**[DOC]** DOC-007 : boîtier portatif relié par un cordon (spiralé sur DOC-004 et la photo DOC-003), panneau de
commande à droite du coffre.

## 2. Rapprochement avec la redondance modulaire triple (TMR)

- **[VÉR]** Trois unités identiques recevant les mêmes entrées, suivies d'un voteur à majorité : principe posé par
  von Neumann (1956), analysé par Lyons & Vanderkulk (1962). Fiabilité avec voteur parfait :
  R_TMR = 3R² − 2R³, meilleure que R tant que R > 0,5.
- Résultats (`c08`), mission de 6 h :

| Taux de défaillance λ [HYP] | Défaillance simplex | Défaillance TMR | Gain |
|---|---|---|---|
| 10⁻³ /h | 6,0×10⁻³ | 1,1×10⁻⁴ | × 56 |
| 10⁻⁴ /h | 6,0×10⁻⁴ | 1,1×10⁻⁶ | × 556 |
| 10⁻⁵ /h | 6,0×10⁻⁵ | 1,1×10⁻⁸ | × 5 556 |

- Mises en œuvre réelles **[VÉR]** : calculateurs de commande de vol du Boeing 777, « triple-triple » (Yeh 1996).
  D'autres exemples classiques (calculateur du lanceur Saturn V, navette spatiale) ne sont pas cités faute de
  vérification en ligne.
- Limite théorique **[VÉR]** : sans messages signés, tolérer f fautes arbitraires (« byzantines ») exige
  n ≥ 3f + 1 calculateurs (Lamport, Shostak & Pease 1982). Trois calculateurs échangeant entre eux ne
  suffisent pas pour f = 1 ; il faut soit un quatrième, soit un voteur matériel indépendant sur un bus de
  diffusion (hypothèse de faute restreinte).

**Conclusion** : « trois calculateurs prenant les mêmes signaux, avec vote » décrit exactement une TMR. C'était
de la technologie établie en 2000 et a fortiori aujourd'hui. Statut : **Démontré**, constructible.

## 3. Le « protocole de Borda »

- **[VÉR]** Le décompte de Borda est une méthode de vote par classement (Borda, mémoire de 1781 publié en 1784) :
  chaque votant range les candidats, un candidat reçoit d'autant plus de points qu'il est mieux rangé.
- **[VÉR]** Recherche bibliographique (Crossref, OpenAlex, recherche web) : **aucun « Borda error correcting
  protocol » n'existe** dans la littérature informatique en dehors des pages consacrées à John Titor. L'usage
  réel le plus proche est la fusion de classifieurs par décompte de Borda (Ho, Hull & Srihari 1994), qui n'est
  pas un mécanisme de tolérance aux fautes.
- **[DÉD]** Démonstration par le calcul (`c08`) que Borda n'est **pas** un voteur tolérant aux fautes : deux
  calculateurs sains classent quatre options A > B > C > D ; un calculateur fautif classe B > C > D > A.
  Scores de Borda : A = 6, **B = 7**, C = 4, D = 1. Le calculateur fautif, seul, renverse le choix des deux
  calculateurs sains, alors qu'un vote majoritaire donne A. Énumération exhaustive : avec 4 options, 2 des 24
  classements fautifs renversent le résultat et 4 créent une égalité ; avec 5 options, 18 sur 120 le renversent.
  (Avec 3 options seulement, jamais de renversement, une égalité possible.)
- Pour des grandeurs numériques (une mesure de g, une date), le voteur approprié est la **valeur médiane** :
  median(9,80665 ; 9,80664 ; 10⁶) = 9,80665. C'est ce que font les systèmes réels.
- **[HYP]** Le nom peut n'être qu'un habillage. Jean-Charles de Borda fut aussi métrologue (cercle répétiteur,
  mesure de la longueur du pendule battant la seconde) — rapprochement suggestif avec « horloges et gravité »,
  non vérifié en ligne et sans valeur probante.

## 4. Architecture de commande-contrôle reconstituée

Voir `schema_fonctionnel.svg`. Chaîne **[DÉD]** : capteurs de gravité (r.11) + 4 horloges → bus → 3 calculateurs
→ voteur → consignes vers le régulateur d'électrons (r.5), les régulateurs de champ (r.3), la pompe (r.9) ;
capteur de singularité (r.7) en retour ; télécommande filaire et panneau local en interface ; chaîne d'arrêt
d'urgence câblée.

Critique d'ingénierie **[DÉD]** (confiance élevée) :

1. **Redondance déséquilibrée.** DOC-008 montre 3 calculateurs et 4 horloges, mais **une** batterie, **une**
   pompe, **un** générateur d'électrons, **une** unité de capteurs de gravité, et un régulateur de champ par
   singularité (donc en série, non en redondance). Avec λ = 10⁻⁴ /h pour chaque organe **[HYP]** :
   défaillance des six organes non redondés sur 6 h = 3,6×10⁻³ ; calculateurs en TMR = 1,1×10⁻⁶ ; horloges
   (2 sur 4) = 9×10⁻¹⁰. Les calculateurs ne pèsent que **0,03 %** du risque : tripler les calculateurs sans
   doubler la pompe et la batterie n'apporte rien. Un concepteur réel aurait commencé par là.
2. **Pas d'état sûr.** L'arrêt d'urgence (ISO 13850 ; catégories d'arrêt 0 et 1 de l'IEC 60204-1 — normes citées
   de mémoire, non vérifiées en ligne) suppose qu'en coupant l'énergie on atteint un état sans danger. Ici,
   couper n'éteint ni la gravité ni le rayonnement des singularités, et la source affirme elle-même que la perte
   du champ serait « quite undesirable ». L'architecture devrait être « fail-operational » (comme des commandes
   de vol), donc redondante sur l'énergie et les actionneurs — ce que les schémas ne montrent pas. Le « système
   qui retirerait la singularité de cette ligne d'univers » n'est pas un dispositif de sécurité évaluable.
3. **Télécommande filaire.** Justifiée dans le récit par la chaleur de l'unité ; un cordon de 1 à 2 m ne met
   l'opérateur à l'abri ni de la gravité ni du rayonnement (fiche F4 : 370 Gy/s à 3 m).
4. **Temps de boucle.** Si les singularités devaient être tenues à 9 cm l'une de l'autre (entraxe de DOC-007),
   la dynamique à contrôler a une période de 7 à 28 ms (fiche F1) : c'est accessible à un calculateur temps réel, mais les
   actionneurs n'existent pas.

## 5. Classement

| Élément | Statut | Constructible aujourd'hui ? | Comment |
|---|---|---|---|
| Trois calculateurs en redondance triple avec voteur | Démontré | **Oui** | 3 calculateurs dissemblables, voteur médian matériel, chien de garde, bus CAN double |
| « Protocole de correction d'erreurs de Borda » | Inexistant dans la littérature ; inadapté (démontré) | sans objet | remplacer par majorité/médiane |
| Télécommande filaire à écran | Démontré | **Oui** | boîtier + liaison série RS-485 |
| Chaîne d'arrêt d'urgence | Démontré | **Oui** (le circuit) | double canal câblé, relais de sécurité |
| Mise en sécurité effective d'une unité à singularités | **Contredit** (aucun état sûr) | **Non** | — |

## 6. Limites

Les taux de défaillance sont des **[HYP]** d'illustration. L'identification du « protocole de Borda » à un
habillage est une inférence ; l'absence dans la littérature est constatée, pas prouvée.

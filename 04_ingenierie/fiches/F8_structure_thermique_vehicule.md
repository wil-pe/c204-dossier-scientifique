# Fiche F8 — Contraintes thermiques, mécaniques et matériaux ; véhicule porteur et sol

Calculs : `calculs/c09_structure_vehicule.py` → `resultats/c09_structure.json`, `c09_contraintes_croisees.csv`,
`c09_budget_masse.csv` ; compléments dans `c02`, `c05`.

## 1. Ce que dit la source

**[DOC texte]** L'unité pèse « about 500 pounds » ; elle est « very heavy and requires a "stiff" suspension » ;
véhicule : « a 1987 4WD » ; « 2 Gs or more depending on how close you are to the unit » ; « 100 to 120 degrees » ;
l'unité devient « unapproachable » en trajet long ; le sol est « raclé » sur environ un pouce.

## 2. L'unité telle qu'annoncée : 227 kg

| Grandeur | Valeur | Commentaire |
|---|---|---|
| Poids | 2 224 N | celui de **3 passagers** de 75 kg |
| Part de la charge utile d'un pick-up 4×4 | 15 à 32 % pour 700–1 500 kg **[HYP]** | la charge utile exacte du modèle 1987 n'a pas pu être confirmée |
| Masse volumique moyenne (enveloppe de 0,063 m³, cotes de l'Équipe A) | 3 600 kg/m³ ; 6 500 kg/m³ rapportée aux 35 L utiles | plus dense que l'aluminium massif (2 700 kg/m³), alors qu'un coffret d'électronique fait 300 à 1 000 kg/m³ : **implausible** sans lest ou blindage dense. (Ancienne hypothèse de 0,13 m³ : 1 750 kg/m³.) |
| Pression au plancher | 10 kPa | négligeable |

**[DÉD]** Une unité de 227 kg n'exige aucune « suspension rigide » sur un 4×4 : l'exigence ne se comprend que si
l'objet est beaucoup plus lourd, ou si elle sert le récit. Confiance : élevée.

## 3. La masse qu'exigent les autres chiffres

| Affirmation | Masse impliquée (par singularité) |
|---|---|
| 2 g à 1 m | 2,94×10¹¹ kg (2 g à 0,5 m : 7,4×10¹⁰ kg ; à 3 m : 2,6×10¹² kg ; à 3,7 m : 4,0×10¹² kg) |
| Résultante de 2 g (1 g terrestre + traction horizontale) à 1 m | 2,5×10¹¹ kg |
| 300–500 MW au total | 3,9 à 5,1×10¹² kg — ce qui donnerait 2 g à **3,7–4,1 m** |

Remarque **[DÉD]** : « 300–500 MW » et « 2 g » ne sont compatibles entre eux que si les 2 g sont ressentis à
environ 4 m de l'unité, c'est-à-dire au bord de la zone de 10–12 pieds, pas à la place du conducteur.

### Charge sur le véhicule et le sol

| Cas | Masse totale | Poids | Rapport à 1 500 kg de charge utile | Pression sous 4 pneus (0,12 m² **[HYP]**) | Par rapport au granite (~200 MPa) |
|---|---|---|---|---|---|
| 2 × 100 kg | 200 kg | 2,0 kN | 0,13 | 16 kPa | 10⁻⁴ |
| 2 × 1,47×10¹¹ kg (2 g à 1 m à elles deux) | 2,9×10¹¹ kg | 2,9×10¹² N | 2×10⁸ | 2,4×10¹³ Pa | 10⁵ |
| 2 × 2,94×10¹¹ kg | 5,9×10¹¹ kg | 5,8×10¹² N | 4×10⁸ | 4,8×10¹³ Pa | 2×10⁵ |
| 2 × 4,4×10¹² kg | 8,8×10¹² kg | 8,6×10¹³ N | 6×10⁹ | 7,2×10¹⁴ Pa | 4×10⁶ |

Aucun matériau ne tient : la pression dépasse de 2 à 4 décades la résistance du diamant (~100 GPa, ordre de
grandeur). **[DÉD]**, confiance élevée. Conséquence physique : une singularité de 10¹¹–10¹² kg n'est retenue par
rien et **tombe à travers le véhicule et la Terre**. Ordres de grandeur (`c09`, densité uniforme) : traversée
aller simple en 42 min, vitesse au centre 7,9 km/s ; freinage par friction dynamique ~2 kN contre un poids de
4×10¹³ N (rapport 4×10⁻¹¹) ; accrétion de roche ~10⁻¹¹ kg/s contre une perte par évaporation de 4,5×10⁻⁹ kg/s.
Elle oscillerait donc indéfiniment dans le globe en maigrissant très lentement, sans « avaler la Terre » —
question que la source élude. (Ordres de grandeur ; analyse détaillée : Équipe B.)

## 4. Aucune masse ne satisfait toutes les affirmations (`c09_contraintes_croisees.csv`)

| M par singularité | Puissance | Durée de vie | g à 1 m | Transportable (≤ 227 kg) | 300–500 MW | 2 g entre 1 et 3,7 m | Survit 6 h | Rayons X | r_s < 2,8 fm |
|---|---|---|---|---|---|---|---|---|---|
| 10² kg | 7,5×10³⁰ W | 4×10⁻¹³ s | 7×10⁻¹⁰ g | **oui** | non | non | non | non | oui |
| 10⁶ kg | 7,5×10²² W | 0,4 s | 7×10⁻⁶ g | non | non | non | non | non | oui |
| 10⁸ kg | 7,5×10¹⁸ W | 4,6 jours | 7×10⁻⁴ g | non | non | non | **oui** | non | oui |
| 10¹⁰ kg | 6×10¹⁴ W | 1,6×10⁴ ans | 0,07 g | non | non | non | oui | non | oui |
| 2,94×10¹¹ kg | ~10¹¹ W | ~2×10⁹ ans | 2 g | non | non | **oui** | oui | non | oui |
| 10¹² kg | 7,7×10⁹ W | 1,2×10¹¹ ans | 6,8 g | non | ≈ (photons seuls) | oui | oui | non | oui |
| 4,4×10¹² kg | 4,0×10⁸ W | 1,1×10¹³ ans | 30 g | non | **oui** | non | oui | non | non |
| 10¹⁵ kg | 4,9×10³ W | 2×10²⁰ ans | 6 800 g | non | non | non | oui | **oui** | non |

Chaque colonne « oui » tombe sur une masse différente ; les six affirmations ne sont jamais vraies ensemble.
En particulier une singularité « bien plus petite qu'un électron » (r_s ≪ 2,8 fm, rayon classique) rayonne
**plus** de 2 GW, pas 300–500 MW. Hypothèses : durée de vie par intégration d'un modèle à seuils d'espèces
**[HYP]** (`c01`) ; confiance élevée sur les ordres de grandeur.

## 5. Efforts dans l'habitacle si la pesanteur était celle annoncée

Pour une masse donnant 2 g à 1 m (`c09`, profil) : 200 g à 10 cm, 22 g à 30 cm, 8 g à 50 cm, 2 g à 1 m, 0,9 g à
1,5 m, 0,5 g à 2 m. Le gradient à 1 m vaut 4 g par mètre : la tête et les pieds d'un occupant ne subissent pas
la même pesanteur, et « 2 g pendant tout le trajet » ne peut pas être uniforme dans l'habitacle. **[DÉD]**
Efforts : un occupant de 80 kg est tiré vers l'unité par 1 570 N (une ceinture le tient) ; mais tout objet du
coffre situé à 10 cm d'une singularité pèse 200 fois son poids (une batterie de 17 kg : 33 kN) et le plancher du
véhicule à 30 cm subit 22 g. L'unité s'écraserait sur elle-même avant de charger la suspension.

## 6. Thermique et matériaux à 38–49 °C

- Température compatible avec l'électronique (0–70 °C commerciale), les CSAC (−10 à +70 °C), un 5071A
  (0–50 °C garanti : marge nulle à 49 °C), des batteries Li-ion en décharge ; hors plage pour les gravimètres
  de précision (fiche F6). **[VÉR]** d'après les fiches constructeur.
- Comme montré en fiche F4, 38–49 °C sur 1,07 m² correspond à **0,15–0,29 kW** dissipés : c'est le bilan thermique
  d'un coffre contenant une à quelques centaines de watts d'électronique — l'ordre de grandeur des auxiliaires
  réellement constructibles (0,13 kW en configuration logeable ; 0,23–0,92 kW en configuration complète,
  fiche F5). **[DÉD]** La température rapportée est celle d'un appareil électronique ordinaire, pas d'une source
  de 300–500 MW.
- Six heures à 49 °C dans un habitacle fermé posent un problème de contrainte thermique pour l'équipage, non
  chiffré ici (**non résolu**, hors périmètre).

## 7. Budget de masse **et de volume** des périphériques (`c09_budget_masse.csv`)

Périphériques de DOC-008 en technologie de 2026, dimensionnés **sans contrainte de place** (volumes : fiches
constructeur quand elles existent, sinon **[HYP]**) :

| Élément | Masse | Volume occupé |
|---|---|---|
| Coffre, patins, charnières (parois hors volume utile) | 30 kg | — |
| Pack Li-ion de 7,5 kWh | 50 kg | 30 L |
| 4 horloges CSAC + distribution | 0,5 kg | 0,5 L |
| 3 calculateurs durcis + voteur + bus | 6 kg | 3 L |
| Gravimètre relatif type CG-6 (21,5 × 21 × 24 cm) | 5,5 kg | 10,8 L |
| 2 bobines HTS compactes avec cryostats (pré-refroidies, sans compresseur) | 40 kg | 30 L |
| 2 alimentations/régulateurs de champ | 10 kg | 6 L |
| Canon à électrons + haute tension + collecteur sous vide | 8 kg | 6 L |
| Boucle de refroidissement à deux réservoirs de 15 L pleins | 40 kg | 36 L |
| Télécommande, panneau, câblage | 5 kg | 3 L |
| 2 carters (r = 4,0 cm) + 2 cm de plomb | 14,5 kg | 1,8 L |
| **Total** | **209 kg** | **127 L** |
| Disponible | 227 kg | **35 L utiles** (63 L d'enveloppe) |

**Verdict [DÉD]** (confiance moyenne : volumes en partie **[HYP]**, échelle du coffre à ± 0,2 m) :

- **masse : oui** — 209 kg ≤ 227 kg ;
- **volume : non** — 127 L à loger dans 35 L utiles, soit 3,6 fois trop (2 fois l'enveloppe extérieure). Même
  l'ancienne enveloppe de 1,20 m (130 L, ≈ 102 L utiles) n'y suffisait pas ; la version 1 de cette fiche n'avait
  vérifié que la masse (216 kg, avec des carters de 5 cm) ;
- **ce qui se loge** : il faut réduire les réservoirs (2 × 0,25 L), la batterie (1,34 kWh, 4 L), remplacer les
  bobines à cryostat par de petites bobines à basse tension et sortir le gravimètre du coffre. C'est le palier
  R1 de l'Équipe I : **36 kg**, un tiers du volume utile (11,7 L par notre somme de sa nomenclature ; 31 % selon
  son propre contrôle) ;
- **masse annoncée** : ce contenu logeable représente 570 kg/m³ d'enveloppe, contre 3 600 kg/m³ pour 227 kg. Il
  manque ≈ 190 kg de matière dense : 17 L de plomb, qui tiendraient dans les 23 L restants et représenteraient
  ≈ 9 cm de plomb autour de chaque logement (reste ≈ 100 Gy/s à 1 m dans l'hypothèse de singularités de 400 MW).

La conclusion de la version 1 — « la masse annoncée est celle d'une maquette crédible de l'instrumentation » —
est **retirée** : à l'échelle retenue par l'Équipe A, aucun ensemble de périphériques constructibles n'explique
227 kg ; seuls un lest ou un blindage dense le feraient.

## 8. Classement

| Élément | Statut | Constructible aujourd'hui ? |
|---|---|---|
| Coffre de 227 kg arrimé dans un 4×4 | Démontré | **Oui**, sans suspension spéciale |
| Périphériques complets (209 kg, 127 L) dans 35 L utiles | **Contredit** en volume (× 3,6) | **Non** ; version réduite de 36 kg (Équipe I, R1) : **oui** |
| 227 kg de périphériques constructibles dans ce coffre | **Contredit** (3 600 kg/m³ exigés, 570 kg/m³ logeables) | **Non** sans ≈ 190 kg de lest dense |
| Coffre contenant 10¹¹–10¹³ kg | **Contredit** (poids, pression 10¹³–10¹⁵ Pa, effondrement interne) | **Non — impossible** |
| Ensemble cohérent {227 kg ; 300–500 MW ; 2 g ; rayons X ; « plus petit qu'un électron »} | **Contredit** (aucune masse solution) | **Non — impossible** |

## 9. Limites

Dimensions du coffre : cotes de l'Équipe A (**[DÉD]** sur étalons **[HYP]**, L = 0,85 ± 0,2 m) ; volume utile de
35 L : Équipes E et I ; volumes des périphériques : en partie **[HYP]**. Le verdict en volume ne s'inverserait
qu'au-delà de L ≈ 1,3 m. Empreinte des pneus, charge utile : **[HYP]** (la valeur constructeur n'a pas été trouvée).
Résistances des matériaux : ordres de grandeur usuels, non vérifiés en ligne. Les estimations de friction et
d'accrétion dans la Terre sont grossières (facteur 10).

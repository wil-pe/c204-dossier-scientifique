# Fiche F9 — Question Q4 (ingénierie) : produire 2 g à 1 m avec de l'énergie électromagnétique

Calculs : `calculs/c10_Q4_energie_EM.py` → `resultats/c10_Q4.json`, `c10_Q4_comparaisons.csv`.

## 1. Question

Quelle énergie électromagnétique faudrait-il stocker pour produire, **par son seul contenu en énergie**, une
pesanteur de 2 g à 1 m ? (Rappel de règle : un champ électromagnétique n'est pas un champ gravitationnel ; il ne
gravite que par son énergie, comme toute forme d'énergie.)

## 2. Réponse

| Grandeur | Équation | Valeur | Étiq. | Confiance |
|---|---|---|---|---|
| Masse équivalente | M = a r²/G, a = 2 g, r = 1 m | 2,94×10¹¹ kg | [VÉR] | élevée |
| **Énergie à stocker** | E = M c² | **2,64×10²⁸ J** = 6,3×10¹² Mt de TNT = 69 s de la luminosité totale du Soleil | [DÉD] | élevée |
| En années de production électrique mondiale (2023) | E / 1,08×10²⁰ J | 2,5×10⁸ ans | [DÉD] | élevée |

Hypothèse : champ faible, source statique et liée ; la masse gravitationnelle vue de loin est alors E_totale/c²,
quelle que soit la forme de l'énergie (pour un système lié à l'équilibre, les contributions de pression du
champ et de tension de la structure se compensent). Limite : un rayonnement libre, non confiné, gravite
deux fois plus (ρ + 3p/c²) mais se disperse en 3 ns sur 1 m.

## 3. Comparaison aux plus grands stockages électromagnétiques réels

| Installation | Énergie | Masse équivalente | g à 1 m | Décades manquantes |
|---|---|---|---|---|
| ITER, tous aimants supraconducteurs | 51 GJ | 5,7×10⁻⁷ kg | 3,8×10⁻¹⁷ m/s² | 17,7 |
| ITER, bobines toroïdales | 41 GJ | 4,6×10⁻⁷ kg | 3,0×10⁻¹⁷ m/s² | 17,8 |
| LHC, dipôles principaux | 8,82 GJ | 9,8×10⁻⁸ kg | 6,6×10⁻¹⁸ m/s² | 18,5 |
| CMS, solénoïde à 4 T | 2,6 GJ | 2,9×10⁻⁸ kg | 1,9×10⁻¹⁸ m/s² | 19,0 |
| NIF, banc de condensateurs (nominal) | ~400 MJ | 4,5×10⁻⁹ kg | 3,0×10⁻¹⁹ m/s² | 19,8 |
| LHC, un faisceau nominal | 362 MJ | 4,0×10⁻⁹ kg | 2,7×10⁻¹⁹ m/s² | 19,9 |
| Z machine, générateurs de Marx | 22 MJ | 2,4×10⁻¹⁰ kg | 1,6×10⁻²⁰ m/s² | 21,1 |
| NIF, rendement de fusion record (2025) | 8,6 MJ | 9,6×10⁻¹¹ kg | 6,4×10⁻²¹ m/s² | 21,5 |
| ISSP, banc du générateur de 1 200 T | 5 MJ | 5,6×10⁻¹¹ kg | 3,7×10⁻²¹ m/s² | 21,7 |
| NIF, énergie laser UV sur cible | 2,2 MJ | 2,4×10⁻¹¹ kg | 1,6×10⁻²¹ m/s² | 22,1 |
| Production électrique mondiale d'une année | 1,08×10²⁰ J | 1 200 kg | 8,0×10⁻⁸ m/s² (8 µGal) | 8,4 |
| Énergie primaire mondiale d'une année | 6,2×10²⁰ J | 6 900 kg | 4,6×10⁻⁷ m/s² (46 µGal) | 7,6 |
| Pack Li-ion de 7,5 kWh | 27 MJ | 3,0×10⁻¹⁰ kg | 2,0×10⁻²⁰ m/s² | 21,0 |

Lecture : toute l'énergie magnétique d'ITER, la plus grande jamais stockée, pèse **0,57 microgramme**. Toute
l'électricité produite sur Terre en un an, stockée sous forme de champ à 1 m, ne donnerait que 8 µGal — à
peine la limite de détection d'un bon gravimètre de terrain.

## 4. Pourquoi c'est impossible par principe, et pas seulement trop cher

1. **Densité d'énergie.** Loger 2,64×10²⁸ J dans une sphère de 10 cm de rayon donne 6,3×10³⁰ J/m³, soit un
   champ magnétique de 4,0×10¹² T (900 fois le champ critique de l'électrodynamique quantique, 4,4×10⁹ T) ou un
   champ électrique de 1,2×10²¹ V/m (900 fois la limite de Schwinger : le vide claque en paires e⁺e⁻).
   **[DÉD]**, confiance élevée.
2. **Théorème du viriel** (Moon 1982 pour les aimants) **[VÉR]** : contenir une énergie de champ E exige une
   structure tendue de masse M_s ≥ ρ E/σ. Donc

   | Matériau | Masse de structure | Rapport à la masse du champ |
   |---|---|---|
   | Acier à haute résistance (2 GPa) | 1,0×10²³ kg (1,4 Lune) | 3,5×10¹¹ |
   | Fibre de carbone (3,5 GPa) | 1,4×10²² kg | 4,6×10¹⁰ |
   | Limite idéale (130 GPa, 2 200 kg/m³) | 4,5×10²⁰ kg | 1,5×10⁹ |

   Autrement dit, la part du champ dans la masse totale d'un stockage électromagnétique ne peut pas dépasser
   σ/(ρc²) ≈ 3×10⁻¹² à 7×10⁻¹⁰. **Dans tout dispositif électromagnétique fait de matière, c'est la matière qui
   gravite, jamais le champ** — d'au moins neuf ordres de grandeur. **[DÉD]**, confiance élevée.
3. **Le meilleur champ réel.** 45,5 T dans un litre : 0,82 MJ, soit 9×10⁻¹² kg ; à 10 cm cela produit
   6×10⁻²⁰ m/s², soit 11 décades sous le microgal (et 8 sous la résolution de 1 nGal d'un gravimètre supraconducteur).

## 5. Conséquence pour le C204

Les bobines (r.2), leur alimentation (r.3), la batterie (r.12) et le canon à électrons (r.6) ne peuvent
contribuer en rien à la pesanteur de 1,5–2 g décrite : leur contenu en énergie équivaut au mieux à 10⁻⁹ kg.
Dans l'architecture revendiquée, toute la gravité doit venir de la masse des singularités, ce qui renvoie aux
impossibilités des fiches F1, F5 et F8.

Statut : produire une pesanteur macroscopique par de l'énergie électromagnétique stockée —
**théoriquement défini** (l'énergie gravite), **contredit en pratique** par les limites des matériaux et du vide
(18 décades entre ITER et le besoin ; borne du viriel). Constructible aujourd'hui : **non**.

## 6. Limites

Calcul newtonien en champ faible (2 g à 1 m : potentiel Φ/c² = 2×10⁻¹⁶, largement justifié). Les propositions de
« courbure de l'espace-temps par champs électromagnétiques intenses » de la littérature récente relèvent de
l'Équipe H et ne changent pas les ordres de grandeur ci-dessus.

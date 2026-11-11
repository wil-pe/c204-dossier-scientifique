# Fiche F3 — Mise en rotation et orientation de l'axe

Repères : aucun composant dédié sur DOC-008 ; « steering singularity » sur DOC-007 r.2.
Calculs : `calculs/c03_injection_rotation.py` → `resultats/c03_injection_rotation.json` (clé `rotation`).

## 1. Ce que dit la source

**[DOC texte]** singularités « top-spin » ; « by rotating two electric microsingularities at high speed, it is
possible to create and modify a local gravity sinusoid that replicates the effects of a Kerr black hole » ;
« rotating and positioning the polar axis of the singularities affects and alters the gravity sinusoid » ;
« their mass and spin is altered in order to adjust the size of the ergosphere ».
Aucun actionneur de rotation n'apparaît sur les schémas : la fonction est revendiquée sans organe.

## 2. Moment cinétique maximal

| Grandeur | Équation | 100 kg | 2,94×10¹¹ kg | 4,4×10¹² kg | Étiq. |
|---|---|---|---|---|---|
| Moment cinétique maximal (Kerr extrémal) | J = G M²/c | 2,2×10⁻¹⁵ J·s (2×10¹⁹ ħ) | 1,9×10⁴ J·s | 4,3×10⁶ J·s (4×10⁴⁰ ħ) | [VÉR] |
| Vitesse angulaire de l'horizon (extrémal) | Ω_H = c³/(2GM) | 2×10³³ rad/s | 6,9×10²³ rad/s | 4,6×10²² rad/s | [VÉR] |
| Énergie de rotation extractible maximale | (1 − 1/√2) M c² = 0,29 M c² | 2,6×10¹⁸ J | 7,7×10²⁷ J | 1,2×10²⁹ J | [VÉR] |
| Énergie minimale pour atteindre J_max avec de la lumière au paramètre d'impact critique | ≈ M c²/(3√3) = 0,19 M c² | 1,7×10¹⁸ J | 5×10²⁷ J | 7,6×10²⁸ J | [DÉD] |

Confiance : élevée (formules standard de la métrique de Kerr). « Tourner à grande vitesse » est exact au sens
où Ω_H est gigantesque ; mais le moment cinétique d'un trou noir ne se règle pas avec un moteur : il n'y a
aucune surface matérielle à entraîner.

## 3. Comment agir (ou non) sur la rotation

1. **Par accrétion** **[VÉR]** : faire tomber de la matière ou du rayonnement avec un moment cinétique orbital.
   Passer de a = 0 à a = 1 exige d'accréter une masse au repos de l'ordre de la masse initiale (masse finale
   = √6 fois l'initiale pour l'accrétion par disque, Bardeen 1970 — contenu de l'article non relu en ligne).
   Coût : ~0,2 à 1 M c², soit 10²⁸–10²⁹ J pour 10¹² kg. Aucune source embarquée ne le fournit (fiche F5).
2. **Par couple magnétique** **[DÉD]** : un trou de Kerr-Newman a un moment magnétique μ = Q J/M (rapport
   gyromagnétique g = 2 ; Carter 1968). Dans un champ B l'axe précesse à Ω = μB/J = (Q/M) B.
   - charge extrémale (inatteignable), B = 45,5 T : Ω = 3,9×10⁻⁹ rad/s, **un tour en 51 ans**, quel que soit M ;
   - charge réaliste (6 e) : 10⁻²⁹ rad/s pour 4,4×10¹² kg ;
   - pour 1 rad/s il faudrait 1,2×10¹⁰ T même à charge extrémale.
3. **Par couple gravitationnel** **[DÉD]** : un quadripôle de masse voisin exerce un couple de marée, mais les
   masses déplaçables dans le coffre (kg) sont 10¹¹–10¹² fois plus petites que la singularité : effet nul en
   pratique. Non chiffré plus avant.
4. **Perte spontanée** **[VÉR]** : le rayonnement de Hawking emporte le moment cinétique plusieurs fois plus vite
   que la masse (Page 1976 II) ; un trou en rotation se ralentit de lui-même. À 10¹² kg l'échelle de temps est de
   l'ordre de 10¹⁰–10¹¹ ans, donc sans conséquence opérationnelle ; à 100 kg, 10⁻¹³ s.

## 4. Classement

| Fonction | Statut | Constructible aujourd'hui ? |
|---|---|---|
| Existence de trous noirs en rotation (Kerr) | Démontré (astrophysique) | sans objet |
| Mettre en rotation un micro-trou noir à la demande | Théoriquement possible par accrétion ; coût ~0,2–1 M c² | **Non** |
| Orienter l'axe par un champ magnétique | **Contredit** dans tout délai utile (≥ 8 décades trop lent) | **Non — impossible** |
| « Sinusoïde de Tipler » produit par deux trous en rotation | hors périmètre (Équipe B) ; aucun équivalent dans la littérature | — |

## 5. Limites

Les ordres de grandeur de mise en rotation ignorent la croissance de masse pendant l'accrétion (facteur ≤ 3).
L'analyse de la géométrie d'espace-temps résultante (deux trous de Kerr voisins) relève de l'Équipe B.
Confiance : **élevée** sur les impossibilités d'actionnement, **moyenne** sur les coefficients numériques.

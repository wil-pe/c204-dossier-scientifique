# EXP-05 — Effet Casimir : principe, ordres de grandeur, faisabilité, et pourquoi ce n'est pas un réservoir d'« énergie négative »

| | |
|---|---|
| **Niveaux** | N1 (analogues classiques : ondes à la surface de l'eau, bruit acoustique) · N2 (projet avancé : sphère-plan au microscope à force atomique) · N3 (mesures de précision) |
| **Sous-système C204 lié** | aucun repère du manuel n'invoque Casimir ; lien indirect : toute machine à courbes temporelles fermées connue en relativité générale exige de la matière « exotique » (énergie négative), et l'effet Casimir est l'exemple de laboratoire habituellement cité |
| **Statut physique** | Force de Casimir : **démontrée** (accord théorie-expérience au % près). Accumulation d'énergie négative macroscopique utilisable : **spéculatif**, borné par les inégalités quantiques. |
| **Calculateur** | `calculs/calc05_casimir.py` → `resultats/calc05_casimir.txt`, `figures/calc05_casimir.png` |

## 1. Objectif

Comprendre la force de Casimir par le calcul et, selon le niveau, par un analogue classique (N1) ou par une
mesure directe (N2/N3) ; chiffrer l'« énergie négative » réellement en jeu et la comparer à ce qu'exigerait une
géométrie exotique.

## 2. Principe et équations [VÉR]

Deux plaques parfaitement conductrices séparées de d modifient le spectre des modes du champ électromagnétique :

- pression (attractive) : P = π²ħc/(240·d⁴) ;
- énergie par unité de surface : E/A = −π²ħc/(720·d³) ; densité d'énergie u = −π²ħc/(720·d⁴) ;
- sphère de rayon R devant un plan (approximation de proximité, d ≪ R) : F = π³ħcR/(360·d³).

Corrections réelles : conductivité finie (profondeur de pénétration δ = λ_p/2π ≈ 22 nm pour l'or : facteur
≈ 1 − 4δ/d + (72/5)(δ/d)² en sphère-plan, valable pour d ≫ δ) ; rugosité (≈ 6·(σ_rms/d)²) ; température
(longueur thermique ħc/k_BT = 7,6 µm à 300 K) ; **potentiels de contact** : F_él = π·ε₀·R·V²/d.

Lecture alternative [VÉR, Jaffe 2005] : la force se calcule aussi comme une force de van der Waals relativiste
entre les charges des plaques, sans invoquer l'énergie du vide ; elle ne « prouve » pas que le vide soit un
réservoir d'énergie.

## 3. Montages réels publiés [VÉR]

| Référence | Géométrie, méthode | Domaine | Résultat |
|---|---|---|---|
| Lamoreaux 1997 | lentille sphérique-plan, pendule de torsion | 0,6–6 µm | première mesure moderne, accord ≈ 5 % |
| Mohideen & Roy 1998 | microsphère-plan, microscope à force atomique | 0,1–0,9 µm | accord ≈ 1 % |
| Chan et al. 2001 | micro-système électromécanique actionné par la force | ~0,1–1 µm | « actionnement » mécanique par Casimir |
| Bressi et al. 2002 | **deux plaques parallèles** | 0,5–3 µm | coefficient vérifié à ≈ 15 % |
| Decca et al. 2007 | micro-oscillateur de torsion, pression effective | 0,16–0,75 µm | précision sub-% ; contraintes sur de nouvelles forces |
| Munday, Capasso & Parsegian 2009 | or-silice dans un liquide | — | force **répulsive** à longue portée (Casimir-Lifshitz) |
| Sushkov et al. 2011 | grande lentille-plan, pendule de torsion | 0,7–7 µm | composante thermique observée |
| Garrett, Somers & Munday 2018 | sphère-sphère | — | au-delà de l'approximation de proximité |
| Wilson et al. 2011 | circuit supraconducteur à miroir « mobile » effectif | micro-ondes | effet Casimir **dynamique** (photons créés) |

(Existence, auteurs, revue et titre de chaque article vérifiés en ligne ; les domaines de distance et les
précisions de la table sont cités de mémoire et restent à relire dans les articles — confiance moyenne.)

Revues : Lamoreaux 2005 ; Klimchitskaya, Mohideen & Mostepanenko 2009. Analogues classiques : effet Casimir
acoustique (Larraza & Denardo 1998) ; analogue par ondes de surface (Denardo, Puda & Larraza 2009).

## 4. Matériel et coût indicatif

| Niveau | Matériel | Coût |
|---|---|---|
| **N1** | cuvette d'eau sur haut-parleur ou agitateur (ondes désordonnées), deux plaquettes verticales suspendues à des fils, caméra de smartphone | 20–60 € |
| **N2** | microscope à force atomique de salle de TP ou de plateforme ; levier souple (0,01–0,1 N/m) avec microsphère collée (R ≈ 50–100 µm) dorée ; substrat doré ; source de tension de compensation | accès plateforme ; consommables ≈ 300–600 € |
| **N3** | vide, contrôle des potentiels de surface (sonde de Kelvin), mesure dynamique du gradient de force | laboratoire |

## 5. Protocole pas à pas

### N1 — analogue par ondes de surface (classique)
1. Agiter le bain à large bande (bruit) pour créer un champ d'ondes désordonné.
2. Suspendre deux plaquettes parallèles, espacement réglable de 5 à 50 mm ; filmer.
3. Mesurer l'attraction (angle des fils) en fonction de l'écart et de l'amplitude du bruit ; arrêter le bruit :
   la force disparaît.
4. Interprétation : entre les plaques, les ondes de grande longueur d'onde sont exclues → pression de radiation
   plus faible à l'intérieur. C'est l'**image** du mécanisme, avec des ondes classiques et de l'énergie positive.

### N2 — sphère-plan au microscope à force atomique
1. Étalonner la raideur du levier (bruit thermique) et la sensibilité de la détection optique.
2. Approcher la sphère du plan ; enregistrer force-distance de 500 nm à 50 nm (100 courbes).
3. **Étalonnage électrostatique** : appliquer V = −0,3 … +0,3 V ; la parabole F(V) donne le potentiel de contact
   V₀ (minimum) et la distance absolue (courbure ∝ R/d). Compenser V₀.
4. Soustraire la force électrostatique résiduelle et la dérive ; ajuster F(d) à π³ħcR/(360 d³) × corrections.
5. Refaire avec une autre sphère (R différent) : F ∝ R.

## 6. Signal attendu et budget de bruit (calculé)

| d | Pression (plaques idéales) | Énergie par m² | Densité de masse équivalente |
|---|---|---|---|
| 10 nm | 1,3 × 10⁵ Pa (≈ 1 atm) | −4,3 × 10⁻⁴ J | −4,8 × 10⁻¹³ kg/m³ |
| 100 nm | 13 Pa | −4,3 × 10⁻⁷ J | −4,8 × 10⁻¹⁷ kg/m³ |
| 1 µm | 1,3 × 10⁻³ Pa | −4,3 × 10⁻¹⁰ J | −4,8 × 10⁻²¹ kg/m³ |

Sphère R = 100 µm : F = 2,7 × 10⁻¹⁰ N à 100 nm ; 3,4 × 10⁻¹¹ N à 200 nm ; 2,2 × 10⁻¹² N à 500 nm.
Lentille R = 11 cm à 1 µm : 3,0 × 10⁻¹⁰ N.

Budget (levier 0,02 N/m, 10 kHz, Q = 100) : bruit thermique 7 × 10⁻¹⁵ N/√Hz → rapport signal/bruit ≈ 4 × 10⁴ en
1 s à 100 nm ; déflexion statique 13,6 nm. **Le bruit n'est pas le problème.** Les systématiques le sont :

| Potentiel résiduel | à 100 nm | à 200 nm | à 500 nm |
|---|---|---|---|
| 10 mV | 1 % de Casimir | 4 % | 26 % |
| 50 mV | 26 % | 102 % | 640 % |
| 100 mV | 102 % | 410 % | 2550 % |

plus l'incertitude de distance absolue (± 1 nm → ± 3 % à 100 nm, la force variant en d⁻³), la rugosité (1 % pour
4 nm rms à 100 nm) et la conductivité finie (−8 à −15 % entre 1 µm et 500 nm).

## 7. Durée

N1 : une demi-journée. N2 : plusieurs semaines (préparation des sondes, étalonnages). N3 : thèse.

## 8. Analyse des données

N1 : force (angle) en fonction de l'écart et de l'amplitude. N2 : moyenne des courbes après recalage ;
ajustement à deux paramètres libres au plus (décalage de distance, potentiel résiduel), le reste étant mesuré
indépendamment ; résidus ; comparaison au calcul de Lifshitz si les données optiques de l'or sont disponibles.

## 9. Sécurité

N1 : basse tension audio. N2 : tensions < 1 V sur la sonde ; règles de la plateforme (laser de détection capoté) ;
dépôt d'or sous-traité. Aucun danger particulier.

## 10. Ce que cela prouve — et ne prouve PAS

**Prouve** : deux conducteurs neutres s'attirent à courte distance avec la loi et l'amplitude prévues par
l'électrodynamique quantique ; la force est mesurable mais minuscule ; sa mesure est un exercice de maîtrise des
systématiques électrostatiques.

**Ne prouve pas** : qu'on puisse extraire de l'énergie du vide, ni stocker de l'« énergie négative » utilisable.
Chiffres [DÉD] : entre deux plaques de 1 m² séparées de 10 nm, l'énergie de Casimir vaut −4,3 × 10⁻⁴ J, soit
−4,8 × 10⁻²¹ kg ; la masse (positive) de deux films d'or de 100 nm seulement est 3,9 × 10⁻³ kg, soit 8 × 10¹⁷
fois plus : **l'énergie totale reste positive**. L'ordre de grandeur de l'énergie négative nécessaire à une
gorge de trou de ver de 1 m de rayon est −r·c²/G ≈ −1,3 × 10²⁷ kg (≈ 0,7 masse de Jupiter ; estimation
dimensionnelle d'après Morris, Thorne & Yurtsever 1988) : il manque un facteur ≈ 3 × 10⁴⁷. Les inégalités
quantiques (Ford & Roman 1995, 1996) limitent de surcroît l'amplitude et la durée de toute densité d'énergie
négative. L'analogue N1 ne démontre que le mécanisme d'exclusion de modes, avec des ondes classiques.

## 11. Lien avec la C204 [DÉD]

Les documents attribués à Titor n'invoquent pas l'effet Casimir : ils revendiquent des « micro-singularités de
Kerr ». Cette fiche répond à l'objection prévisible « l'énergie négative existe, donc une machine temporelle est
possible » : l'énergie négative de laboratoire est inférieure de ~47 ordres de grandeur au besoin, et n'est ni
stockable ni concentrable. La question théorique (cylindre de Tipler, anneau de Kerr, conjecture de protection
chronologique) relève de l'Équipe B.

## 12. Confiance et limites

Formules idéales et ordres de grandeur : confiance **élevée**. Corrections de conductivité : développement
perturbatif, **moyenne** (non valable à 100 nm). Estimation « trou de ver » : dimensionnelle, **faible** sur le
préfacteur, robuste sur l'ordre de grandeur. Faisabilité N2 : réelle mais exigeante (**moyenne**).

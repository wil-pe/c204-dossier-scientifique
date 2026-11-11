# EXP-03 — Mesure de G (balance de torsion) et test nul « un champ électromagnétique intense crée-t-il une gravité mesurable ? »

| | |
|---|---|
| **Niveaux** | N1 (Cavendish artisanal, qualitatif) · N2 (Cavendish de TP : G à quelques % ; test nul près d'un aimant) · N3 (balances de torsion de recherche) |
| **Sous-système C204 lié** | « collecteur d'injection d'électrons pour modifier masse et gravité » ; « bobines de champ magnétique » ; intitulé *gravity distortion* |
| **Statut physique** | Attraction newtonienne : **démontrée**. Gravitation de l'énergie électromagnétique : **prévue par la relativité générale mais non mesurable** (10⁻²⁴ N ici). « Gravité créée par un champ électromagnétique » au sens des affirmations : **non étayée**. |
| **Calculateur** | `calculs/calc03_cavendish_champ_EM.py` → `resultats/calc03_cavendish_champ_EM.txt`, `figures/calc03_test_nul_EM.png` |

## 1. Objectif

(a) Mesurer la constante G avec une balance de torsion. (b) Utiliser le même instrument, dont la sensibilité est
alors étalonnée, pour chercher une force « gravitationnelle » supplémentaire près d'un aimant puissant (et, en
cadre encadré seulement, d'un condensateur chargé). (c) Montrer que tout signal observé est électromagnétique,
et apprendre à le démontrer. Champ électromagnétique ≠ champ gravitationnel.

## 2. Principe et équations

Balance de torsion : fléau portant deux masses m à ±d, suspendu à un fil de constante κ = π·G_cis·d_fil⁴/(32·L).
Deux masses M à la distance r exercent le couple 2·(GMm/r²)·d ; angle d'équilibre θ = 2GMmd/(κr²) ; période
T₀ = 2π√(I/κ), I = 2md². D'où G = 4π²·θ·r²·d/(T₀²·M) (au premier ordre ; corriger l'attraction croisée).

Gravitation d'un champ [VÉR, principe : Tolman, Ehrenfest & Podolsky 1931 ; Füzfa 2016] : le tenseur
énergie-impulsion du champ électromagnétique courbe l'espace-temps. Pour une source statique liée, la masse
gravitationnelle active totale est M_éq = E/c² (énergie du champ, contraintes comprises). Densité d'énergie :
u = B²/(2µ₀) + ε₀E²/2.

Forces parasites sur une masse d'épreuve de volume V, susceptibilité χ, rayon a :
F_mag = (|χ|·V/µ₀)·B·|∇B| ; F_él (sphère conductrice neutre) ≈ 2π·ε₀·a³·∇(E²) ; charge résiduelle q : q·E ;
courant d'air de vitesse v : 6π·η·a·v.

## 3. État de l'art publié [VÉR]

Cavendish 1798 ; Gundlach & Merkowitz 2000 (balance à rétroaction d'accélération angulaire) ; Quinn et al. 2013
(deux méthodes, BIPM) ; Rosi et al. 2014 (atomes froids) ; Li et al. 2018 (deux méthodes indépendantes) ;
Westphal et al. 2021 (couplage gravitationnel entre masses millimétriques d'environ 90 mg) ; revue : Rothleitner
& Schlamminger 2017. CODATA 2018 : G = 6,674 30(15) × 10⁻¹¹ m³ kg⁻¹ s⁻² (2,2 × 10⁻⁵ relatif — la constante
fondamentale la moins bien connue). Sensibilité ultime : Schlamminger et al. 2008 (accélérations différentielles
de l'ordre de 10⁻¹⁵ m/s²) ; loi en 1/r² vérifiée jusqu'à 52 µm (Lee et al. 2020).
Tests nuls de « modification de la gravité » par des dispositifs électromagnétiques : Hathaway, Cleveland & Bao
2003 (disque supraconducteur en rotation : aucun effet) ; Tajmar 2004 (effet Biefeld-Brown : vent ionique, pas
de gravité).

## 4. Matériel et coût indicatif

| Niveau | Matériel | Coût |
|---|---|---|
| **N1** | fil de tungstène ou de nylon fin, fléau léger, 2 × 15–50 g de plomb (sous gaine), 2 × 1–2 kg (bouteilles d'eau, lests), boîte fermée anti-courants d'air, pointeur laser classe 2 + miroir, règle au mur | 30–100 € |
| **N2** | balance de Cavendish de TP ; jeu de masses d'épreuve Pb / Al / laiton ; « source » : aimant NdFeB en boîtier amagnétique scellé **et** leurre en laiton de mêmes masse et forme ; écran en mu-métal ; teslamètre ; cage de Faraday reliée à la terre | 2–4 k€ (balance) + 300 € |
| **N3** | balance sous vide, fil de silice, autocollimateur, plateau tournant | laboratoire |

## 5. Protocole pas à pas

### A. Mesure de G (N1/N2)
1. Installer sur un mur porteur, loin des passages ; fermer la boîte ; attendre 12 h.
2. Enregistrer les oscillations libres (≥ 5 périodes) : T₀ et position d'équilibre.
3. Basculer les grosses masses ; enregistrer la nouvelle position d'équilibre (≥ 5 périodes). Répéter 4 fois (ABBA).
4. θ = Δs/(4·L_levier). Calculer G. Bilan d'incertitude.

### B. Test nul électromagnétique (N2, en aveugle)
1. Remplacer une grosse masse par le **leurre** (laiton) : référence gravitationnelle.
2. Un tiers place, selon un tirage au sort consigné sous enveloppe, soit le leurre, soit l'**aimant** (boîtiers
   identiques, masses égales à 1 g près). L'opérateur mesure la déviation sans savoir. 16 cycles.
3. Ouvrir la clé. Différence aimant − leurre = force non gravitationnelle (les masses sont égales).
4. **Signatures qui démasquent l'artefact** :
   - changer le matériau de la masse d'épreuve : plomb (χ < 0, repoussé), aluminium ou tungstène (χ > 0, attirés).
     Une force qui change de signe avec χ n'est pas de la gravité ;
   - varier la distance : dipôle → B·∇B ∝ r⁻⁷, gravité ∝ r⁻² ;
   - interposer l'écran de mu-métal : l'effet s'effondre, la masse n'a pas changé ;
   - retourner l'aimant (N ↔ S) : la force en B² ne change pas ; un moment magnétique rémanent, si.
5. Reculer l'aimant jusqu'à ce que l'artefact passe sous la résolution ; donner la borne supérieure obtenue.

### C. Variante condensateur (N2/N3 **encadré uniquement**)
Électrodes à ≤ 5 kV derrière un écran électrostatique relié à la terre entourant totalement le pendule ; source
à courant limité (< 0,5 mA), énergie stockée < 0,35 J, charge < 45 µC (voir EXP-07 §9). Sans écran, l'attraction
électrostatique (10⁻⁵ N) sature la balance : c'est la démonstration.

## 6. Signal attendu et budget de bruit (calculé)

Balance d'exemple (m = 15 g, M = 1,5 kg, d = 5 cm, r = 4,5 cm, fil W Ø 25 µm × 30 cm) :
F = 7,4 × 10⁻¹⁰ N ; couple 7,4 × 10⁻¹¹ N·m ; κ = 2,1 × 10⁻⁸ N·m/rad ; θ = 3,6 mrad ; période 379 s ;
spot déplacé de 29 mm à 2 m. Agitation thermique : 4 × 10⁻⁷ rad (négligeable). Incertitude attendue sur G : ≈ 4 %
(dominée par θ et r). Résolution réaliste : ~10⁻¹¹ N (dérives, air, inclinaison du sol).

Gravité de l'énergie d'un champ (prédiction de la relativité générale) :

| Source | Énergie | E/c² | Force sur 15 g |
|---|---|---|---|
| Aimant NdFeB de 1 litre | 400 J | 4,5 × 10⁻¹⁵ kg | **1,8 × 10⁻²⁴ N** à 5 cm |
| Condensateur 1 nF à 5 kV | 12,5 mJ | 1,4 × 10⁻¹⁹ kg | 5,6 × 10⁻²⁹ N à 5 cm |
| Aimant d'IRM 3 T | ≈ 10 MJ | 1,1 × 10⁻¹⁰ kg | 1,1 × 10⁻²² N à 1 m |
| Aimant hybride 45 T | ≈ 100 MJ | 1,1 × 10⁻⁹ kg | 1,1 × 10⁻²¹ N à 1 m |
| Aimants d'ITER (total) | ≈ 51 GJ | 0,57 mg | 5,7 × 10⁻²¹ N à 10 m |

(Énergies des grands aimants : ordres de grandeur usuels, non revérifiés en ligne.)
Pour que l'énergie d'un champ « pèse » autant que l'eau : B = 1,5 × 10⁷ T ou E = 4,5 × 10¹⁵ V/m.

Forces parasites pour le même montage (masse d'épreuve à 5 cm, B = 0,1 T, ∇B = 5 T/m, E = 2 × 10⁵ V/m) :

| Effet | Force | Rapport au signal RG |
|---|---|---|
| Magnétique sur tungstène / plomb | 4 × 10⁻⁵ / 8 × 10⁻⁶ N | 10¹⁹ |
| Électrostatique, sphère neutre polarisée | 3 × 10⁻⁵ N | 10¹⁹ |
| Charge résiduelle de 1 pC | 2 × 10⁻⁷ N | 10¹⁷ |
| Attraction newtonienne de la masse de l'aimant (7,5 kg) | 3 × 10⁻⁹ N | 10¹⁵ |
| Courant d'air de 1 mm/s | 2 × 10⁻⁹ N | 10¹⁵ |
| Signal de Cavendish | 7 × 10⁻¹⁰ N | 4 × 10¹⁴ |

Conséquence pratique [DÉD] : à 5 cm, la force diamagnétique sur le plomb vaut ≈ 2800 fois l'attraction
newtonienne de l'aimant ; avec les lois d'échelle r⁻⁷ et r⁻², elles ne s'égalent que vers r ≈ 5 cm × 2800^(1/5)
≈ 25 cm. Sans écran, la balance va en butée.

Écart à combler : signal RG 1,2 × 10⁻²² m/s² contre 6,7 × 10⁻¹⁰ m/s² (TP) et ~10⁻¹⁵ m/s² (meilleure balance
publiée) → **12 et 7 ordres de grandeur**. Même avec un aimant de 45 T à 1 m : 4 ordres de grandeur.

## 7. Durée

Mesure de G : 1 à 2 jours (mise à l'équilibre comprise). Test nul : 2 à 3 jours.

## 8. Analyse des données

Ajustement d'une sinusoïde amortie + dérive linéaire sur chaque segment ; moyenne ABBA ; test nul : différence
moyenne aimant − leurre et son incertitude ; résultat exprimé comme **borne supérieure** sur une force anormale,
puis comme rapport à la prédiction E/c² (on trouvera « < 10¹² à 10¹³ fois la relativité générale » : une borne
très faible, et c'est le résultat honnête).

## 9. Sécurité

Plomb : masses gainées ou vernies, lavage des mains, pas d'usinage. Aimants NdFeB : risque de pincement et
d'éclats (gants, lunettes, cales, manipuler un seul aimant à la fois) ; tenir à distance des stimulateurs
cardiaques et supports magnétiques. Laser classe 2 au plus. **Haute tension : variante C interdite hors TP
encadré** ; jamais de condensateur de forte énergie (le cas « 100 µF à 400 V » du script est un calcul, pas un
montage).

## 10. Ce que cela prouve — et ne prouve PAS

**Prouve** : deux masses de laboratoire s'attirent selon Newton ; G à quelques % ; près d'un aimant ou d'une
électrode, les forces électromagnétiques dépassent la gravité de plusieurs ordres de grandeur et peuvent se
faire passer pour une « anomalie de gravité » ; on sait les démasquer (signe de χ, loi de distance, écran, aveugle).

**Ne prouve pas** : que l'énergie électromagnétique ne gravite pas (elle gravite, d'après la relativité générale,
au niveau 10⁻²⁴ N — invérifiable ici) ; ni qu'elle gravite « davantage ». Une lévitation diamagnétique ou une
poussée de vent ionique n'est pas de l'antigravité.

## 11. Lien avec la C204 [DÉD]

- « Injecter des électrons pour modifier la masse » : la charge extrémale d'un trou noir de 4,4 × 10¹² kg (masse
  retenue, erratum E2) est 379 C (86 C pour 10¹² kg). 379 C d'électrons représentent 379 × m_e/e =
  **2,2 × 10⁻⁹ kg**. Ajouter 1 kg d'électrons demanderait 1,8 × 10¹¹ C. Et un micro-trou noir ne retient en
  réalité que ≈ 6 charges élémentaires (borne ≈ 137 ; erratum E14). L'injection de charge ne peut pas modifier
  sensiblement la masse.
- « Bobines de champ » : un champ de 1 T possède une densité de masse équivalente de 4,4 × 10⁻¹² kg/m³.
- Tout capteur de gravité placé près de bobines et d'électrodes verrait d'abord des artefacts magnétiques et
  électrostatiques (voir EXP-04 et EXP-12).

## 12. Confiance et limites

Formules et ordres de grandeur : confiance **élevée**. Champ local de l'aimant (0,1 T, 5 T/m à 5 cm) : hypothèse
de travail [HYP], à mesurer au teslamètre. Énergie de l'aimant permanent : ordre de grandeur. Le montage N1
donne G à un facteur 2 près au mieux.

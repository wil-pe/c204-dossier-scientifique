# EXP-11 — Détection de rayonnement : bruit de fond gamma/X réel contre « évent à rayons X » de 300–500 MW

| | |
|---|---|
| **Niveaux** | N1 (compteur Geiger du commerce, **sans source**) · N2 (spectrométrie gamma par scintillation du bruit de fond) · N3 (germanium, chambre d'ionisation) |
| **Sous-système C204 lié** | « refroidissement et évacuation des rayons X » ; repère 5 de DOC-009 (*X-ray venting cone*) ; puissance « 300–500 MW » ; « rayons X et gamma évacués vers l'arrière ; bouffée d'UV » |
| **Statut physique** | Radioactivité naturelle et sa mesure : **démontrées**. « 300–500 MW » près d'occupants : **contredit les connaissances** dans les deux lectures chiffrées ci-dessous (dose létale à 3 m en 0,4 ms si toute la puissance sort en rayons X ; en ≈ 10 ms pour les seuls γ primaires d'un spectre de Hawking, borne basse). |
| **Calculateur** | `calculs/calc11_rayonnement.py` → `resultats/calc11_rayonnement.txt`, `figures/calc11_dose_vs_distance.png` |

## 1. Objectif

Mesurer le bruit de fond de rayonnement ionisant avec un instrument du commerce, apprendre la statistique de
comptage, et en déduire (a) ce qu'un compteur à 100 € exclurait immédiatement autour d'un dispositif candidat ;
(b) ce qu'impliquerait, en débit de dose, l'émission revendiquée.

## 2. Principe et équations [VÉR]

- Comptage poissonnien : N coups → incertitude √N. Excès Δ (µSv/h) détecté à 3σ en comparant deux phases de durée
  t (avec/sans) : s·Δ·t = 3·√(2bt + s·Δ·t), b : taux de fond, s : sensibilité (coups/min par µSv/h).
- Débit de dose (≈ kerma dans l'eau) à la distance r d'une source ponctuelle de puissance photonique P :
  Ḋ = [P/(4πr²)]·(µ_en/ρ)·exp(−µ_air·r) ; un cône de demi-angle α concentre d'un facteur 2/(1 − cos α).
- Atténuation par un blindage d'épaisseur x : exp(−µx) (faisceau étroit : minorant de l'épaisseur nécessaire).
- Coefficients massiques (NIST, Hubbell & Seltzer ; relus en ligne) :

| Énergie | µ_en/ρ eau (cm²/g) | µ/ρ air (cm²/g) | µ/ρ plomb (cm²/g) |
|---|---|---|---|
| 100 keV | 0,02546 | 0,1541 | 5,549 |
| 1 MeV | 0,03103 | 0,06358 | 0,07102 |
| 10 MeV | 0,01566 | 0,02045 | 0,04972 |
| 15 MeV | 0,01441 | 0,01810 | 0,05658 |

**Deux lectures de « 300–500 MW », à ne pas confondre** (correction n° 52 de la Red Team n° 2) :

- **Lecture A — littérale** : toute la puissance sort en rayons X (100 keV ; variantes 1 et 10 MeV). C'est ce que
  dit le texte (« rayons X évacués ») pris au mot ; ce n'est pas ce que ferait un trou noir.
- **Lecture B — spectre de Hawking** (valeur retenue par le programme ; Équipes C et G ; Hawking 1974-1975 ; Page
  1976 ; MacGibbon & Webber 1990) : un trou noir de 3,9–5,1 × 10¹² kg (kT ≈ 2–3 MeV) émet ≈ 55 % de sa puissance
  en neutrinos, 37 % en e±, **7,5 % en photons** de 12–16 MeV et < 1 % en gravitons. Les γ primaires de 400 MW
  représentent donc 30 MW. C'est une **borne basse** de la dose : les e± déposeraient ~10⁵ Gy/s à 1 m s'ils
  n'étaient pas arrêtés (estimation de l'Équipe C).

Le rayonnement de Hawking est isotrope sans rotation, anisotrope pour un trou de Kerr rapide, mais **non
collimatable** en cône (erratum E5). Le « cône » de DOC-009 a une ouverture d'environ 78° (erratum E7).

## 3. Matériel et coût indicatif

| Niveau | Matériel | Coût |
|---|---|---|
| **N1** | compteur Geiger-Müller du commerce avec enregistrement des coups (tube sensible aux gamma) ; carnet ou enregistreur | 80–150 € |
| **N2** | spectromètre à scintillation (NaI ou CsI) avec analyseur multicanal ; château de plomb de TP (facultatif) | 400–3000 € |
| **N3** | détecteur germanium, chambre d'ionisation étalonnée | laboratoire |

**Aucune source radioactive n'est utilisée**, à aucun niveau (règle du programme).

## 4. Protocole pas à pas

### N1 — Bruit de fond
1. Poser le compteur à 1 m du sol, à l'intérieur ; compter 60 min par tranches d'une minute.
2. Vérifier la loi de Poisson : variance ≈ moyenne ; histogramme des coups par minute.
3. Refaire : cave / étage ; près d'un plan de travail en granite ; à l'extérieur ; après une forte pluie
   (descendants du radon rabattus au sol : hausse transitoire) ; en altitude ; éventuellement en avion (le débit
   de dose cosmique augmente de plus d'un ordre de grandeur à l'altitude de croisière).
4. **Essai « avec/sans » en aveugle** autour d'un objet quelconque (une batterie, un aimant, une boîte vide) :
   un tiers place ou retire l'objet derrière un écran selon une clé aléatoire ; 16 phases de 10 min. Vérifier
   qu'on **ne détecte rien**, et donner la borne supérieure (c'est la répétition générale d'EXP-12).

### N2 — Spectre du bruit de fond
1. Acquérir 12 à 24 h. Étalonner en énergie sur les raies naturelles : ⁴⁰K (1461 keV), ²¹⁴Bi (609 keV),
   ²⁰⁸Tl (2615 keV).
2. Comparer intérieur/extérieur, avec/sans blindage ; suivre la raie à 609 keV après une pluie.

## 5. Signal attendu et budget de bruit (calculé)

Bruit de fond : ≈ 0,05–0,2 µSv/h ; ≈ 20 coups/min pour un tube courant (sensibilité indicative 175 coups/min par
µSv/h ; à vérifier sur la notice de l'appareil).

| Excès à détecter | Durée par phase (3σ) |
|---|---|
| 0,01 µSv/h (10 % du fond) | 123 min |
| 0,02 µSv/h | 32 min |
| 0,05 µSv/h | 5,7 min |
| 0,1 µSv/h (doublement) | 1,7 min |
| 1 µSv/h | < 10 s |

Saturation d'un Geiger simple (temps mort ~190 µs) : ≈ 5000 coups/s, soit ≈ 1,8 mSv/h — au-delà il sous-estime.

**Ce qu'impliquerait l'affirmation** (calcul d'implication pour 400 MW, pas un fait ; isotrope, en Gy/s) :

| Distance | **Lecture A** — littérale : 400 MW de X de 100 keV | Lecture A, variante 10 MeV | **Lecture B** — γ primaires de Hawking (30 MW, 15 MeV), borne basse | Lecture A dans le cône de 78° |
|---|---|---|---|---|
| 1 m | 8,1 × 10⁴ | 5,0 × 10⁴ | **3,4 × 10³** | 7,3 × 10⁵ |
| 3 m | **9,0 × 10³** | 5,5 × 10³ | **3,8 × 10²** | 8,1 × 10⁴ |
| 100 m | 1,3–8,1 | 3,9–5,0 | 0,28–0,34 | — |
| 1 km | 7 × 10⁻¹⁰ à 0,08 | 4 × 10⁻³ à 5 × 10⁻² | 4 × 10⁻⁴ à 3 × 10⁻³ | — |

(Fourchettes : avec atténuation de l'air en faisceau étroit / sans atténuation ; la réalité, diffusion comprise,
est entre les deux. Pour 300 et 500 MW : multiplier par 0,75 et 1,25 — lecture B à 1 m : 2,6–4,3 × 10³ Gy/s ;
à 3 m : 2,9–4,8 × 10² Gy/s. Rapport A/B à 3 m : 24, dont 13 pour la fraction photons et 1,8 pour le coefficient
d'absorption.)

- Dose létale à 50 % (≈ 4 Gy) à 3 m : atteinte en **0,44 ms** (lecture A) ou en **≈ 10 ms** (lecture B, borne
  basse) ; le débit vaut 3 × 10¹⁴ (A) ou 1,4 × 10¹³ (B) fois le bruit de fond.
- Le débit ne retombe à 1 µSv/h qu'à 1–6 km (atténuation maximale) ; sans atténuation, à plus de 3 500 km (B) ou
  13 000 km (A).
- Blindage pour ramener le débit à 1 µSv/h à 1 m (faisceau étroit : minorant) : 0,5 cm de plomb à 100 keV, mais
  **42 cm (6,5 t)** à 1 MeV, **58 cm (15 t)** à 10 MeV (lecture A) et **47 cm (8,7 t)** pour les γ de la lecture B —
  pour une unité annoncée à 227 kg. (Autres équipes : 62 cm en faisceau large, ≥ 36 cm ; aucune de ces valeurs
  n'est un calcul de transport.)
- La puissance (toutes espèces) doit être évacuée : pour 300 / 400 / 500 MW, une surface de 10 m² devrait
  rayonner à **4800 / 5150 / 5450 K** ; la surface du coffre à l'échelle révisée (1,07 m², L = 0,85 m, erratum E12)
  à 8400 / 9000 / 9500 K ; ou il faudrait vaporiser 116 / 154 / 193 kg d'eau par seconde.
- À l'inverse, un coffre de **1,07 m²** à 38–49 °C dissipe ≈ **190–310 W** : rapport **10⁶** avec la puissance
  revendiquée (à l'ancienne échelle de 1,80 m² : 320–520 W).

**Sensibilité du test** : 1 µSv/h à 1 m correspond à 1,4 × 10⁻⁶ W de rayons X de 100 keV (2,4 × 10⁻⁶ W de γ de
15 MeV) ; 0,05 µSv/h à 7 × 10⁻⁸ W (1,2 × 10⁻⁷ W). Un compteur Geiger exclut donc en quelques minutes toute fuite
supérieure à **~10⁻⁷ W**, soit 2 × 10⁻¹⁶ des 400 MW (lecture A) ou 4 × 10⁻¹⁵ des 30 MW de γ (lecture B).
Selon le récit, le rayonnement de singularités est **permanent** : le test valide est une mesure **absolue**
rapportée au fond (ou dispositif contre leurre), pas une différence marche − arrêt (voir EXP-12). Et il porte sur
un dispositif disponible : il ne dit rien de l'objet de 2000-2001.

## 6. Durée

N1 : une heure par site ; une demi-journée pour l'essai en aveugle. N2 : 24 h d'acquisition.

## 7. Analyse des données

Test de Poisson (rapport variance/moyenne, χ²) ; différence de taux avec/sans et son incertitude
√(N₁/t₁² + N₂/t₂²) ; borne supérieure à 95 % sur un excès ; pour N2, surfaces nettes des raies.

## 8. Sécurité

Aucune source. Ne pas ouvrir le compteur (tube sous quelques centaines de volts, courant très faible mais
désagréable) ; ne pas démonter d'objets anciens radioluminescents ni acheter de « sources d'essai ». Les
matériaux naturels (granite, sel de potassium) restent à leur place ; on se contente d'approcher le compteur.
Plomb de blindage (N2) : gainé, lavage des mains.

## 9. Ce que cela prouve — et ne prouve PAS

**Prouve** : le bruit de fond est mesurable, variable, poissonnien ; un instrument à 100 € détecte un doublement
du fond en deux minutes et exclut toute fuite X de l'ordre de 10⁻⁷ W ; l'affirmation « 300–500 MW évacués en
rayons X » implique des débits de dose incompatibles avec la survie d'occupants, de riverains, de l'électronique
et du véhicule.

**Ne prouve pas** : l'absence de tout rayonnement non détecté par un Geiger (neutrinos, particules très peu
ionisantes, photons hors de sa plage) ; un résultat nul borne ce qui est mesuré, rien d'autre. Et la détection
d'un rayonnement près d'un appareil prouverait la présence d'une source de rayonnement, pas un déplacement
temporel.

## 10. Lien avec la C204 [DÉD]

- Un cône d'« évacuation » n'est pas une propriété du rayonnement de Hawking (isotrope sans rotation, anisotrope
  mais non collimatable avec rotation ; erratum E5) ; collimater des photons de 10–15 MeV exige des mètres de
  matière dense.
- L'électronique embarquée (calculateurs, horloges), à quelques décimètres, recevrait > 10³ Gy/s dans les deux
  lectures : destruction quasi immédiate.
- La bouffée d'UV et la chaleur extérieure décrites seraient les moindres des effets ; l'ionisation de l'air et
  l'activation des matériaux (au-delà de ~10 MeV : réactions photonucléaires) laisseraient des traces durables,
  mesurables des années plus tard. Aucune n'est rapportée.

## 11. Confiance et limites

Coefficients d'interaction : confiance **élevée** (tables NIST relues, y compris à 15 MeV). Débits de dose : ordre
de grandeur (kerma, sans facteur d'accumulation ni électrons secondaires de haute énergie) — **moyenne**. Les
deux lectures diffèrent d'un facteur 24 ; la lecture B (retenue comme référence physique) est une borne basse.
La conclusion tient à plus de dix ordres de grandeur dans les deux cas. La première version de cette fiche ne
donnait que la lecture A sans la désigner comme littérale. Sensibilité du compteur : **moyenne** (dépend du tube et de l'énergie).

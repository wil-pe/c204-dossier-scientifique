# Programme C204 — Rapport de l'Équipe B (physique théorique et relativité générale)

Version 1.1 — 10 novembre 2026 (version 1 + corrections issues de la validation contradictoire, voir §15).
Dossier : `03_physique_theorique/`.

> **Cadre.** Analyse scientifique critique. Aucune affirmation de « John Titor » n'est tenue pour vraie.
> Les citations du corpus sont des pièces à analyser (**[DOC texte]**), pas des faits. Le voyage vers le passé
> n'a jamais été observé ; aucune source indépendante n'atteste l'existence de la machine C204.

Conventions du dossier de base : **[DOC]** documenté, **[DÉD]** déduit, **[HYP]** hypothèse de notre part,
**[INT]** interprétation de tiers, **[VÉR]** fait scientifique vérifiable. Statut physique : **Démontré** /
**Théoriquement possible** / **Spéculatif** / **Contredit les connaissances actuelles**. Confiance : élevée / moyenne / faible.

Fichiers associés : démonstrations détaillées dans `ANNEXE_B1_demonstrations.md` ; bibliographie et statut de
vérification dans `REFERENCES.md` ; scripts exécutés dans `verifications/` (sorties dans `verifications/sorties/`).
Les numéros « script 0N » renvoient à ces fichiers.

---

## 0. Résumé exécutif

1. **Les chiffres revendiqués sont mutuellement incompatibles, de façon démontrable.** Une puissance de Hawking
   totale de 300–500 MW correspond à un trou noir de **3,9–5,1 × 10¹² kg** (calcul complet des facteurs de corps
   gris, script 02), pas à une unité de 227 kg. Un trou noir de 227 kg s'évapore en **4,8 × 10⁻¹² s** en libérant
   2,0 × 10¹⁹ J (4,9 Gt de TNT). Il n'existe **aucune** masse qui soit à la fois transportable, durable et « tiède ».
2. **Aucun effet relativiste n'existe à l'échelle du mètre pour ces masses.** À 1 m d'un trou noir de 10¹² kg :
   Φ/c² = 7,4 × 10⁻¹⁶ ; entraînement des référentiels de 3 × 10⁻²² rad/s pour le spin maximal d'un trou isolé, et
   jusqu'à 5 × 10⁻¹⁵ rad/s (2 × 10¹² kg) ou 4–5 × 10⁻¹⁴ rad/s (2 × 4,4–5,1 × 10¹² kg) pour le moment cinétique
   orbital d'une paire séparée de 0,3 m — soit l'ordre de l'effet terrestre mesuré, sans portée causale. Le facteur revendiqué
   « 10 ans par heure » (Γ = 87 660) est **20 ordres de grandeur** au-dessus. Pour l'obtenir à 1–4 m il faut
   **6,7 × 10²⁶ – 2,5 × 10²⁷ kg** (113 à 417 masses terrestres).
3. **Incohérence interne « 2 g » / « 10 ans par heure ».** Dans tout champ statique, l'accélération propre vaut
   $a = c^2\,|\nabla \ln N|$. Avec $a \le 2g$ sur 3,7 m, on obtient Γ − 1 ≤ 8 × 10⁻¹⁶. Il faudrait 2,8 × 10¹⁶ g.
4. **La dilatation du temps ne mène jamais vers le passé** (théorème : existence d'une fonction de temps globale
   dans tout espace-temps stablement causal). L'extérieur d'un trou noir de Kerr-Newman (r > r₊) est stablement
   causal : démontré dans l'annexe et vérifié symboliquement (script 03, [A5]).
5. **Les CTC de Kerr existent mathématiquement mais sont inaccessibles et instables.** Elles sont confinées à
   r < r₋ et engendrées par une zone située à |r| < GM/c² de l'anneau (7 × 10⁻¹⁶ m pour 10¹² kg), derrière un
   horizon de Cauchy instable (inflation de masse). Un anneau de rayon 1 m exige M ≥ 1,35 × 10²⁷ kg.
6. **Les « autres univers » du diagramme de Penrose ne sont pas des branches d'Everett.** Ce sont des régions de
   l'extension analytique d'une solution éternelle idéalisée ; elles n'existent pas pour un trou noir formé à une date finie.
7. **« Deux micro-trous noirs = cylindre de Tipler sans la masse » est faux.** Le vide d'Einstein est invariant
   d'échelle : toute zone à CTC de taille ℓ exige une masse ~ℓc²/G. Le seuil de Tipler est une masse linéique
   c²/8G = **1,7 × 10²⁶ kg/m**. Aucune configuration stationnaire de deux trous de Kerr n'existe sans « strut ».
8. **La charge ne peut pas jouer le rôle revendiqué.** Un micro-trou noir porte typiquement ≈ 6 charges
   élémentaires (valeur quadratique moyenne, Page 1977) et au plus ~e/α ≈ 137 (borne supérieure d'ordre de
   grandeur, 2 × 10⁻¹⁷ C), contre 86 C pour l'extrémalité à 10¹² kg : l'« horizon interne » dû à la charge
   mesurerait 10⁻⁵⁶ à 10⁻⁵³ m, soit 10⁻²¹ à 10⁻¹⁸ longueur de Planck. L'énoncé qualitatif « ajouter de la charge agrandit
   l'horizon interne » est en revanche **correct** dans la formule de Reissner-Nordström.
9. **Les champs électromagnétiques gravitent, mais il manque 17 ordres de grandeur sur le champ.** Courber
   l'espace-temps à l'échelle du mètre demande B ≈ 3,5 × 10¹⁸ T (ou E ≈ 10²⁷ V/m, 8 × 10⁸ fois le champ de
   Schwinger). Le record continu est 45,5 T.
10. **Il existe des modèles logiquement cohérents de retour dans le passé** (Novikov, Deutsch, P-CTC), mais
    **aucun mécanisme physique** connu pour créer une CTC avec de la matière ordinaire dans une région compacte
    sans singularité (Tipler 1977, Hawking 1992). La « divergence en % mesurée par gravimétrie » n'a pas de définition physique.
11. **Analogues réels** : dilatation du temps (mesurée jusqu'au millimètre), effet Lense-Thirring (mesuré),
    rayonnement de Hawking (prédit, jamais observé sur un trou noir), trous de ver traversables *non* chronoclastes
    (théoriques), simulations optiques de CTC quantiques (réalisées). Le terme « sinusoïde de Tipler » est absent
    de la littérature d'avant 2001, mais les fonctions métriques extérieures du cylindre de Tipler au-delà du seuil
    sont égales à **r fois une sinusoïde de ln r** (§3.3).

---

## 1. Méthode et vérifications

- Toutes les formules ont été **re-dérivées** ; les valeurs du dossier de base (§6) n'ont pas été recopiées.
- Vérifications symboliques (sympy) : Kerr-Newman et Melvin satisfont Einstein-Maxwell ; Kerr est Ricci-plat ;
  l'intérieur de van Stockum est une poussière en rotation rigide ; les trois extérieurs de Tipler sont des solutions
  du vide raccordées C¹ ; identité $a_i = \partial_i \ln N$ ; bornes de coquille mince.
- Vérification numérique indépendante du rayonnement de Hawking : intégration des équations radiales
  (Regge-Wheeler, Dirac) pour les spins 0, ½, 1, 2. Accord avec Page (1976) : **0,00 %** (neutrinos),
  **−0,06 %** (photons), **−0,08 %** (gravitons).
- Références : 227 requêtes Crossref, 16 requêtes arXiv et 6 requêtes INSPIRE (résumés relus lors des corrections) ;
  statut de chaque référence dans `REFERENCES.md`.
- `verifications/executer_tout.py` relance les huit scripts en 140 à 144 s (mesuré).

| Script | Objet | Résultat de contrôle |
|---|---|---|
| `01_ordres_de_grandeur_dossier.py` | coefficients du dossier §6 | reproduits à < 0,1 % |
| `02_hawking_corps_gris.py` | corps gris, espèces, durée de vie | accord Page 1976 à < 0,1 % ; M* (13,8 Ga) = 5,3 × 10¹¹ kg (littérature ≈ 5,0–5,1) |
| `03_kerr_newman.py` | Einstein-Maxwell, CTC, fonction de temps extérieure | 10 composantes nulles ; Maxwell nul |
| `04_van_stockum_tipler.py` | intérieur, 3 extérieurs, raccord | résidu de Ricci < 10⁻¹⁶⁰ |
| `05_deux_trous_noirs.py` | champ faible, Peters, Majumdar-Papapetrou, Gott | critère de Gott : 20 000/20 000 |
| `06_dilatation_10_ans_par_heure.py` | Γ = 87 660 | identité $a=\nabla\ln N$ vérifiée |
| `07_champs_EM_et_energie_negative.py` | Melvin, Casimir, Alcubierre | Melvin vérifié ; énergie d'Alcubierre re-dérivée |
| `08_charge_injection_pistes_ouvertes.py` | injection d'électrons, monopôle, Deutsch | — |

Limite générale : nos calculs de seuils de masse pour les espèces hadroniques (10⁸–10¹¹ kg) sont approchés (± 20 %
sur les durées de vie dans cette zone) ; cela n'affecte aucune conclusion.

---

## 2. Thème 1 — Trou noir de Kerr et de Kerr-Newman

### 2.1 Ce que dit le corpus [DOC texte]

« Kerr was one of the first to describe the dual event horizons of a rotating black hole » ; un trou noir de Kerr
aurait une singularité « en forme de beignet » avec « des vecteurs » d'approche sans écrasement ; « Penrose
diagrams […] show mathematically that you can make simulated space-like trips (faster than light) through the
singularity » ; le passage mènerait à « un autre univers ou ligne d'univers » ; l'unité « simule » ce passage :
« the black hole comes to you ».

### 2.2 La solution [VÉR]

En coordonnées de Boyer-Lindquist, avec $a = J/(Mc)$, $r_s = 2GM/c^2$, $r_Q^2 = GQ^2/(4\pi\varepsilon_0 c^4)$ :

$$
ds^2 = -\frac{\Delta}{\Sigma}\left(c\,dt - a\sin^2\theta\, d\varphi\right)^2
+ \frac{\sin^2\theta}{\Sigma}\left[(r^2+a^2)\,d\varphi - a\,c\,dt\right]^2
+ \frac{\Sigma}{\Delta}\,dr^2 + \Sigma\, d\theta^2 ,
$$

$$
\Sigma = r^2 + a^2\cos^2\theta, \qquad \Delta = r^2 - r_s r + a^2 + r_Q^2 .
$$

- **Horizons** : $r_\pm = \tfrac12\left[r_s \pm \sqrt{r_s^2 - 4(a^2 + r_Q^2)}\right]$. Ils existent si $a^2 + r_Q^2 \le (GM/c^2)^2$.
  $r_+$ est l'horizon des événements, $r_-$ un **horizon de Cauchy**.
- **Ergosphère** ($g_{tt}=0$) : $r_E(\theta) = \tfrac12\left[r_s + \sqrt{r_s^2 - 4a^2\cos^2\theta - 4r_Q^2}\right]$. C'est une
  *région* extérieure à l'horizon où rien ne peut rester immobile par rapport à l'infini ; ce n'est pas une surface
  matérielle. Les expressions « ergosphère négative / positive » du corpus n'ont pas de sens technique.
- **Singularité annulaire** : $\Sigma = 0$, soit $r = 0$ et $\theta = \pi/2$ ; en coordonnées de Kerr-Schild, c'est le
  cercle $x^2 + y^2 = a^2$, $z = 0$. Seules les géodésiques du plan équatorial l'atteignent (Carter 1968).
- **Région $r < 0$** : traverser le disque $r = 0$, $\theta \neq \pi/2$ mène à un second feuillet asymptotiquement
  plat où la masse apparente est négative.
- **Thermodynamique** : $T = \hbar c\,(r_+ - r_-)/[4\pi k_B (r_+^2 + a^2)]$, nulle à l'extrémalité ; énergie de rotation
  extractible ≤ 29,3 % de $Mc^2$ ; un Reissner-Nordström extrémal contient 50 % d'énergie électrostatique.

Vérifié symboliquement (script 03) : les 10 composantes de $R_{\mu\nu} - 2(F_{\mu\alpha}F_\nu{}^\alpha - \tfrac14 g_{\mu\nu}F^2)$
s'annulent, ainsi que les équations de Maxwell. **Statut : Démontré** (solution exacte) ; confiance élevée.

Théorèmes d'unicité [VÉR] : un trou noir stationnaire du vide n'a que deux paramètres, M et J (Israel 1967,
Carter 1971, Robinson 1975) ; trois avec la charge. Les qualificatifs « top-spin, dual-positive » ne peuvent donc
désigner que le sens du spin et le signe de la charge **[HYP]**.

### 2.3 Courbes temporelles fermées de Carter [VÉR]

Le coefficient $g_{\varphi\varphi}$ sur le plan équatorial vaut (script 03, [A3]) :

$$
g_{\varphi\varphi}\Big|_{\theta=\pi/2} = r^2 + a^2 + \frac{a^2\,(r_s r - r_Q^2)}{r^2}.
$$

- Kerr ($Q = 0$) : positif pour tout $r > 0$ ; négatif pour $r_c < r < 0$ où $r_c$ est la racine réelle de
  $r^3 + a^2 r + r_s a^2 = 0$ (−0,69 GM/c² pour a/M = 0,5 ; −0,95 pour 0,9). Là, $\partial_\varphi$ est de genre
  temps : les cercles $t, r, \theta$ constants sont des CTC.
- Kerr-Newman : le terme $-a^2 r_Q^2/r^2$ rend $g_{\varphi\varphi} < 0$ des deux côtés de $r = 0$.
- Sur l'équateur, la zone $g_{\varphi\varphi}<0$ s'étend jusqu'à $|r_c| \le GM/c^2$ pour un trou noir. Dans le cas
  sur-extrémal $a \gg GM/c^2$ (singularité nue), elle devient le disque
  $(r + GM/c^2)^2 + a^2\cos^2\theta < (GM/c^2)^2$, soit $|r| < 2GM/c^2$. Dans tous les cas son extension est fixée
  par **M**, pas par $a$.
- Carter (1968) : dans toute la région $r < r_-$, deux événements quelconques sont joints par une courbe de genre
  temps dirigée vers le futur (violation totale de la causalité dans ce bloc).

**Démonstration que l'extérieur est sain** (annexe D4, script 03 [A5]). **Hypothèse : il existe un horizon**,
$a^2 + r_Q^2 \le (GM/c^2)^2$.

$$
g^{tt} = -\frac{N}{\Delta\,\Sigma}, \qquad N = r^2(r^2 + a^2) + a^2(r_s r - r_Q^2) + \Delta\, a^2 \cos^2\theta > 0 \quad \text{pour } r > r_+ .
$$

Donc $\nabla t$ est de genre temps partout hors de l'horizon : $t$ est une fonction de temps globale, l'extérieur est
*stablement causal*, et **aucune CTC ne passe par un point situé hors de $r_+$**. Un véhicule qui reste à quelques
décimètres d'un micro-trou noir est dans cette région : son temps coordonné ne peut que croître. Confiance élevée.

**Cas sur-extrémal** ($a^2 + r_Q^2 > (GM/c^2)^2$, singularité nue — le régime de tout objet « en rotation » au-delà
de l'extrémalité). Il n'y a plus d'horizon : la zone $g_{\varphi\varphi} < 0$ est accessible depuis l'infini et la
violation de causalité est totale (Carter 1968 : tout événement peut être joint à tout autre par une courbe de
genre temps dirigée vers le futur). La démonstration ci-dessus ne s'applique plus. La conclusion pratique repose
alors sur la proposition D3 (b), qui ne suppose aucun horizon : toute courbe fermée de genre temps doit passer à
moins de ~32 GM/c² ≈ 10⁻¹³ m de la singularité, là où le champ n'est plus faible. Résultat exact complémentaire
(annexe D4, script 03 [A6]) : le temps de Kerr-Schild reste une fonction de temps partout sauf dans le tube
$(r + GM/c^2)^2 + a^2\cos^2\theta \le (GM/c^2)^2 + r_Q^2$ entourant l'anneau ; toute CTC traverse ce tube, large de
~10⁻¹⁵ m pour 10¹² kg quel que soit $a$.

### 2.4 Diagramme de Penrose et « autres univers » [VÉR]

L'extension analytique maximale (Boyer & Lindquist 1967 ; Carter 1968) est une chaîne infinie de blocs :
I ($r > r_+$), II ($r_- < r < r_+$), III ($r < r_-$), puis un bloc II′ de type trou blanc et un nouvel extérieur I′.
Une ligne d'univers de genre temps peut aller de I à I′ sans rencontrer la singularité.

Quatre faits limitent radicalement la portée de ce résultat :

1. **Ce ne sont pas des « lignes d'univers » parallèles.** Dans le corpus, « worldline » désigne un univers
   alternatif. En relativité, une ligne d'univers est la trajectoire d'une particule. Les régions I′, I″… sont
   d'autres régions asymptotiques d'**une seule** variété classique ; elles n'ont aucun lien avec les branches
   de l'interprétation d'Everett (voir §7.4). Le texte confond trois notions distinctes.
2. **Le trajet est de genre temps**, non « de genre espace (plus vite que la lumière) » comme l'écrit un passage
   du corpus ; un autre passage dit correctement « time-like ». Le corpus se contredit sur ce point **[DOC texte]**.
3. **L'extension n'existe que pour le trou noir éternel idéal.** Pour un trou noir formé par effondrement ou par
   collision à une date finie, la matière remplace toute la moitié « passée » du diagramme : il n'y a ni trou
   blanc ni autre univers en amont.
4. **L'horizon de Cauchy $r_-$ est instable.** Le rayonnement entrant y est infiniment décalé vers le bleu
   (Simpson & Penrose 1973). Poisson & Israel (1989, 1990) ont montré que la fonction de masse locale y diverge
   (« inflation de masse ») ; Ori (1991, 1992) a précisé la nature de la singularité (nulle, faible) ; Dafermos (2005,
   cas chargé à symétrie sphérique) puis Dafermos & Luk (2025, Kerr) ont établi rigoureusement que la métrique
   perturbée reste continûment prolongeable à travers l'horizon de Cauchy (stabilité C⁰), ce qui n'implique
   **pas** qu'un prolongement régulier, et encore moins unique, existe. S'y ajoute une divergence quantique du tenseur énergie-impulsion (Birrell & Davies 1978 ;
   Zilberman et al. 2020, 2022 ; Hollands, Wald & Zahn 2020). La relativité générale classique **ne prédit pas** ce
   qu'il y a au-delà de $r_-$.

**Statut** de « traverser l'anneau vers un autre univers » : *Spéculatif* pour un trou noir astrophysique réel
(question ouverte de la censure cosmique forte) ; *Contredit les connaissances actuelles* comme procédé contrôlé.

### 2.5 Ordres de grandeur pour un micro-trou noir (script 03, partie B)

| M | $GM/c^2$ = rayon maximal de l'anneau | Temps de traversée $GM/c^3$ | Marée à l'horizon (par mètre) |
|---|---|---|---|
| 227 kg | 1,7 × 10⁻²⁵ m | 5,6 × 10⁻³⁴ s | 8 × 10⁶⁴ g |
| 10¹² kg | 7,4 × 10⁻¹⁶ m | 2,5 × 10⁻²⁴ s | 4 × 10⁴⁵ g |
| 4 × 10¹² kg | 3,0 × 10⁻¹⁵ m | 9,9 × 10⁻²⁴ s | 2,6 × 10⁴⁴ g |
| 1,35 × 10²⁷ kg (0,71 M_Jupiter) | **1 m** | 3,3 × 10⁻⁹ s | 2 × 10¹⁵ g |

Faire passer un véhicule de 2 m « à travers l'anneau » exige $a \ge 2$ m, donc $M \ge 2{,}7 \times 10^{27}$ kg
(1,4 masse de Jupiter). **Démontré** : $a \le GM/c^2$ pour tout trou noir.

### 2.6 « Le trou noir vient à vous »

La relativité générale est covariante : seule la configuration relative compte. Être « à l'intérieur de $r_-$ »
signifie que la ligne d'univers du véhicule se trouve à moins de ~GM/c² de la singularité, quel que soit l'objet
que l'on déplace. On ne peut pas « projeter » la structure causale intérieure d'un trou noir femtométrique sur un
volume de plusieurs mètres : hors de $r_+$, la géométrie est celle d'un champ faible ordinaire (§3.5).
**Statut : Contredit les connaissances actuelles.** Confiance élevée.

---

## 3. Thème 2 — Cylindre de Tipler / van Stockum, et « deux micro-trous noirs »

### 3.1 La solution de van Stockum [VÉR]

$$
ds^2 = H\,(dr^2 + dz^2) + L\, d\varphi^2 + 2M\, d\varphi\, dt - F\, dt^2 .
$$

Intérieur (poussière en rotation rigide, $r \le R$, unités $G = c = 1$) :

$$
H = e^{-a^2 r^2}, \quad L = r^2(1 - a^2 r^2), \quad M = a r^2, \quad F = 1, \qquad 8\pi\rho = 4a^2 e^{a^2 r^2}.
$$

Vérifié (script 04) : $G_{\mu\nu} = 8\pi\rho\, u_\mu u_\nu$ avec $u = \partial_t$ ; vorticité $a$ sur l'axe. En unités SI,
$\rho_0 = \omega^2/(2\pi G)$ avec $\omega = ac$.

### 3.2 Condition d'apparition des CTC [VÉR]

- **Dans la matière** : $g_{\varphi\varphi} = L < 0$ pour $ar > 1$ ; il faut $R > 1/a$.
- **À l'extérieur** (Tipler 1974) : trois familles de solutions du vide selon $aR$ :

| Régime | Fonctions métriques extérieures | Causalité |
|---|---|---|
| $aR < 1/2$ | $\sinh$ de $\theta = \sqrt{1 - 4a^2R^2}\,\ln(r/R)$ | pas de CTC |
| $aR = 1/2$ | polynômes en $\ln(r/R)$ | cas limite |
| $aR > 1/2$ | **$\sin$** de $\gamma = \sqrt{4a^2R^2 - 1}\,\ln(r/R)$ | CTC par tout événement extérieur |

Pour $aR > 1/2$, avec $\beta = \arctan\sqrt{4a^2R^2 - 1}$ :

$$
L = \frac{R\,r\,\sin(3\beta + \gamma)}{2\sin 2\beta\,\cos\beta},\qquad
M = \frac{r\,\sin(\beta + \gamma)}{\sin 2\beta},\qquad
F = \frac{r\,\sin(\beta - \gamma)}{R\,\sin\beta},\qquad F L + M^2 = r^2 .
$$

Les trois familles ont été contrôlées numériquement à 40 chiffres (vide, raccord C¹ en $r = R$ : script 04).

- **Seuil** : $aR = 1/2$, soit une « vitesse de surface » $\omega R = c/2$ et une masse linéique (mesurée dans le
  référentiel de la matière) $\mu = a^2R^2c^2/2G$ :

$$
\mu_{\text{seuil}} = \frac{c^2}{8G} = 1{,}68 \times 10^{26}\ \text{kg/m} \quad (\approx 28\ \text{masses terrestres par mètre}).
$$

| R | ω = c/2R | ρ₀ |
|---|---|---|
| 10 km | 1,5 × 10⁴ rad/s | 5,4 × 10¹⁷ kg/m³ (≈ 2 × densité nucléaire) |
| 1 m | 1,5 × 10⁸ rad/s | 5,4 × 10²⁵ kg/m³ |
| 1 fm | 1,5 × 10²³ rad/s | 5,4 × 10⁵⁵ kg/m³ |

### 3.3 Que vaudrait un « sinusoïde de Tipler » ?

- **Le terme n'existe pas dans la littérature antérieure au récit.** Recherche de l'expression exacte « Tipler
  sinusoid » : 0 résultat dans les métadonnées d'arXiv (titres et résumés) ; en texte intégral (INSPIRE), une
  seule occurrence, **postérieure** au récit : J. Prezens, arXiv:1008.3244 (2010), prépublication sur la solution
  double-Kerr (signalée par l'Équipe H et la Red Team ; vérifiée par nous, contenu non évalué). **[VÉR]**
- **Analogue réel le plus proche n° 1 [DÉD].** Au-delà du seuil, les fonctions métriques extérieures $L$, $M$, $F$
  sont égales à **$r$ fois une sinusoïde de $\ln r$** ($L/r$, $M/r$, $F/r$ sont des sinusoïdes exactes de $\ln r$ ;
  $L$, $M$, $F$ sont log-périodiques d'amplitude croissante). Le signe de $g_{\varphi\varphi}$ alterne donc sur des coquilles cylindriques
  emboîtées, en progression géométrique de raison $\exp(\pi/\sqrt{4a^2R^2 - 1})$ : zones où $\partial_\varphi$ est
  de genre temps (CTC), surfaces où il est nul, zones où il est de genre espace. Exemple $aR = 1$ : zéros de
  $g_{\varphi\varphi}$ à $r/R$ = 1 ; 6,13 ; 37,6 ; 231.
  **[HYP]** Cette alternance « négatif / nul / positif » sur des anneaux emboîtés ressemble au schéma DOC-009
  (« negative / null / positive time field »). Nous ne pouvons pas établir que l'auteur s'en soit inspiré ;
  confiance faible sur l'intention, élevée sur la mathématique.
  **Limite de l'analogie** : pour $aR > 1/2$, une courbe fermée de genre temps joint deux événements quelconques
  de l'extérieur (Tipler 1974). Les zones de signe de $g_{\varphi\varphi}$ ne sont donc **pas** des zones
  causalement distinctes, contrairement à ce que suggéreraient des champs « négatif / nul / positif ».
- **Analogue réel n° 2 [VÉR].** Deux masses en rotation produisent un champ proche newtonien oscillant à $2\omega$ :

$$
\Phi(r,\varphi,t) = -\frac{2GM}{r} - \frac{GMd^2}{4r^3}\left(3\cos^2\psi - 1\right),\quad \psi = \varphi - \omega t
\;\Rightarrow\; \delta\Phi = -\frac{3GMd^2}{8r^3}\cos 2(\varphi - \omega t).
$$

  C'est la seule « sinusoïde de gravité » que deux masses tournantes engendrent. Pour M = 10¹² kg et r = 2 m :
  $\delta\Phi/c^2 = 3 \times 10^{-19}$ à l'entraxe documentaire d = 0,098 m, $3 \times 10^{-18}$ pour d = 0,3 m [HYP]
  (script 05). Sans conséquence causale.

### 3.4 Cylindre fini et théorèmes [VÉR]

- Le cylindre de Tipler est **infini** ; la solution n'est pas asymptotiquement plate. Rien ne garantit que les
  CTC subsistent pour une longueur finie.
- **Tipler (1976, 1977)** : dans un espace-temps asymptotiquement plat issu de données initiales régulières, avec
  une matière satisfaisant la condition d'énergie faible, l'apparition de CTC implique des **singularités**.
- **Hawking (1992)** : un horizon de Cauchy *compactement engendré* (machine construite dans une région finie)
  exige la violation de la condition d'énergie faible.
- **Ori (1993, 2005, 2007)** a construit des modèles respectant les conditions d'énergie ; leur stabilité est la
  principale question **ouverte** (§6.5).

**Statut** du cylindre de Tipler comme machine : *Théoriquement possible* pour le cylindre infini (solution
exacte) ; *Contredit les connaissances actuelles* pour un dispositif fini fait de matière ordinaire sans singularité.

### 3.5 « Deux micro-trous noirs reproduisent un cylindre de Tipler sans la masse » — réfutation

Le corpus : « The singularities do not create Tipler cylinders they create the same physical environment without
all the mass. The same math works for both. » **[DOC texte]**

**(a) Invariance d'échelle (annexe D3).** Si $g$ est solution du vide, $\lambda^2 g$ l'est aussi, avec
$M \to \lambda M$, $J \to \lambda^2 J$ et toutes les longueurs multipliées par $\lambda$. Toute longueur
caractéristique d'une solution du vide vaut donc $GM/c^2$ fois une fonction de paramètres sans dimension. Une
zone à CTC de taille ℓ exige $M \sim \ell c^2/G$ : 1,35 × 10²⁷ kg pour 1 m. « Le même environnement sans la masse »
est contradictoire dans les termes. **Démontré.**

**(b) Les mathématiques ne sont pas « les mêmes ».** Kerr est asymptotiquement plat, à horizon, avec des CTC
cachées en $r < r_-$. Van Stockum-Tipler est cylindrique, sans horizon, avec des CTC à l'extérieur. Ce sont deux
solutions distinctes de la classe stationnaire axisymétrique.

**(c) Solutions exactes à deux trous noirs [VÉR].**

| Solution | Hypothèses | Rotation ? | CTC ? | Applicabilité au C204 |
|---|---|---|---|---|
| Majumdar-Papapetrou (1947) ; Hartle & Hawking (1972) | statique ; chaque trou extrémal, $Q = M\sqrt{4\pi\varepsilon_0 G}$ | non | non (extérieur) | charge intenable (§4.5) |
| Bach-Weyl (1922), deux Schwarzschild | statique ; « strut » conique entre les trous | non | non | le strut porte ≈ $GM^2/d^2$ = 7 × 10¹⁵ N (10¹² kg, d = 0,098 m, Équipe A) ou 7 × 10¹⁴ N (d = 0,3 m, [HYP]) |
| Double-Kerr (Kramer & Neugebauer 1980 ; Dietz & Hoenselaers 1985 ; Manko & Ruiz 2019) | stationnaire axisymétrique | oui | pathologies locales selon les paramètres | nécessite un strut |
| Neugebauer & Hennig (2009) ; Hennig & Neugebauer (2011) | **théorème** | — | — | pas d'équilibre de deux trous de Kerr sans strut |
| Métrique C (Kinnersley & Walker 1970) | deux trous accélérés par une corde/strut | variantes | non | non pertinent |

**Séparation des deux singularités.** La seule valeur documentaire est l'entraxe des deux logements mesuré par
l'Équipe A : **d = 0,098 ± 0,025 m** ([DÉD], confiance faible ; `02_reconstruction/dimensions.json`). La
version 1 de ce rapport utilisait d = 0,3 m sans le signaler comme **[HYP]** ; les deux valeurs sont données ci-dessous.

L'interaction spin-spin (Wald 1972) vaut au plus ~$6GS^2/(c^2d^4)$ pour deux trous extrémaux : 2 × 10⁻¹² N à
0,098 m et 3 × 10⁻¹⁴ N à 0,3 m pour 10¹² kg, contre $GM^2/d^2$ = 7 × 10¹⁵ N et 7 × 10¹⁴ N : rapports 3 × 10⁻²⁸ et
4 × 10⁻²⁹ (script 05). **[HYP]** « top-spin, dual-positive » pourrait évoquer un équilibre par répulsion de spins
parallèles et de charges de même signe ; cet équilibre est exclu par le théorème ci-dessus et, numériquement, par
26 à 28 ordres de grandeur selon la masse et l'entraxe.

**(d) Binaire en orbite (Peters 1964).**

$$
\omega = \sqrt{\frac{G(m_1+m_2)}{d^3}},\qquad
P_{\rm GW} = \frac{32}{5}\frac{G^4 m_1^2 m_2^2 (m_1+m_2)}{c^5 d^5},\qquad
t_c = \frac{5}{256}\frac{c^5 d^4}{G^3 m_1 m_2 (m_1+m_2)} .
$$

| M (chacun) | d | ω | v | P_GW | t_c |
|---|---|---|---|---|---|
| 113,5 kg | 0,098 m (A) | 4,0 × 10⁻³ rad/s | 0,20 mm/s | 2 × 10⁻⁶⁷ W | 5 × 10⁶⁰ s |
| 10¹² kg | 0,098 m (A) | 377 rad/s | 18 m/s | 1,2 × 10⁻¹⁷ W | 7,3 × 10³⁰ s = 2,3 × 10²³ ans |
| 10¹² kg | 0,3 m [HYP] | 70 rad/s | 10,5 m/s | 4 × 10⁻²⁰ W | 6,4 × 10³² s = 2,0 × 10²⁵ ans |
| 4,4 × 10¹² kg | 0,098 m (A) | 790 rad/s | 39 m/s | 1,9 × 10⁻¹⁴ W | 8,6 × 10²⁸ s = 2,7 × 10²¹ ans |
| 4,4 × 10¹² kg | 0,3 m [HYP] | 148 rad/s | 22 m/s | 7 × 10⁻¹⁷ W | 7,6 × 10³⁰ s = 2,4 × 10²³ ans |

Dans tous les cas le temps de coalescence dépasse 10¹¹ âges de l'univers : le rayonnement gravitationnel est
négligeable ; l'orbite est newtonienne et non relativiste (v/c ~ 10⁻⁷).

**(e) Champ réel à 1–4 m (script 05).**

| M | r | Φ/c² | g | Marée | Retard d'horloge par heure | Ω (spin seul, trou isolé) |
|---|---|---|---|---|---|---|
| 100 kg | 1 m | 7,4 × 10⁻²⁶ | 6,7 × 10⁻⁹ m/s² | 1,3 × 10⁻⁸ s⁻² | 2,7 × 10⁻²² s | 3,3 × 10⁻⁴² rad/s |
| 227 kg | 1 m | 1,7 × 10⁻²⁵ | 1,5 × 10⁻⁸ m/s² | 3,0 × 10⁻⁸ s⁻² | 6,1 × 10⁻²² s | 1,7 × 10⁻⁴¹ rad/s |
| 10⁹ kg | 1 m | 7,4 × 10⁻¹⁹ | 0,067 m/s² | 0,13 s⁻² | 2,7 × 10⁻¹⁵ s | 3,3 × 10⁻²⁸ rad/s |
| 10¹² kg | 1 m | 7,4 × 10⁻¹⁶ | 67 m/s² (6,8 g) | 133 s⁻² | 2,7 × 10⁻¹² s | 3,3 × 10⁻²² rad/s |
| 10¹² kg | 4 m | 1,9 × 10⁻¹⁶ | 4,2 m/s² (0,43 g) | 2,1 s⁻² | 6,7 × 10⁻¹³ s | 5,2 × 10⁻²⁴ rad/s |
| 5 × 10¹² kg | 4 m | 9,3 × 10⁻¹⁶ | 20,9 m/s² (2,1 g) | 10,4 s⁻² | 3,3 × 10⁻¹² s | 1,3 × 10⁻²² rad/s |

**Terme orbital.** La dernière colonne ne vaut que pour le spin d'un trou isolé. Une paire en orbite porte un
moment cinétique orbital $J_{\rm orb} = Md^2\omega/2$, environ 10⁷ fois plus grand que le spin maximal
$GM^2/c$. En moyenne temporelle, sur l'axe et à la hauteur $z$ (analogue gravitomagnétique d'une spire) :

$$
\Omega_{\rm orb}(z) = \frac{2GJ_{\rm orb}}{c^2\,(d^2/4 + z^2)^{3/2}} .
$$

| M (chacun) | d | $J_{\rm orb}$ | Ω orbital à 1 m | Ω orbital à 4 m |
|---|---|---|---|---|
| 10¹² kg | 0,098 m (A) | 1,8 × 10¹² J·s | 2,7 × 10⁻¹⁵ rad/s | 4,2 × 10⁻¹⁷ rad/s |
| 10¹² kg | 0,3 m [HYP] | 3,2 × 10¹² J·s | 4,5 × 10⁻¹⁵ rad/s | 7,3 × 10⁻¹⁷ rad/s |
| 4,4 × 10¹² kg | 0,098 m (A) | 1,7 × 10¹³ J·s | 2,5 × 10⁻¹⁴ rad/s | 3,9 × 10⁻¹⁶ rad/s |
| 4,4 × 10¹² kg | 0,3 m [HYP] | 2,9 × 10¹³ J·s | 4,2 × 10⁻¹⁴ rad/s | 6,8 × 10⁻¹⁶ rad/s |
| 5,06 × 10¹² kg | 0,3 m [HYP] | 3,6 × 10¹³ J·s | 5,2 × 10⁻¹⁴ rad/s | 8,3 × 10⁻¹⁶ rad/s |

(Script 05, [B3bis]. L'Équipe D et la Red Team, avec la formule de champ lointain $2GJ/c^2z^3$, obtiennent
4,7 × 10⁻¹⁵ et 4,3 × 10⁻¹⁴ rad/s à 0,3 m : écart de 3 %.) C'est l'ordre de l'effet terrestre mesuré, voire dix fois
plus ; la composante de métrique associée, $h_{0\varphi} \sim \Omega z/c \sim 10^{-22}$, est sans portée causale (D3 b).

Repères [VÉR] : les meilleures horloges optiques atteignent ~10⁻¹⁸ (Aeppli et al. 2024) ; Gravity Probe B a mesuré
37 mas/an = 5,7 × 10⁻¹⁵ rad/s pour la Terre entière (Everitt et al. 2011). **Seuls effets macroscopiques de trous
noirs de 10¹¹–10¹² kg à l'échelle du mètre : une pesanteur newtonienne, sa marée et, s'ils orbitent, un
entraînement des référentiels comparable à celui de la Terre.** L'échelle des effets relativistes forts est
$GM/c^2 \sim 10^{-15}$ m.

**Conclusion du thème.** *Contredit les connaissances actuelles* ; confiance élevée.

---

## 4. Thème 3 — Micro-trous noirs

### 4.1 Rayonnement de Hawking [VÉR pour la théorie ; jamais observé]

$$
T_H = \frac{\hbar c^3}{8\pi G M k_B} = \frac{1{,}227\times10^{23}\ \text{K·kg}}{M},\qquad
k_BT_H = \frac{10{,}57\ \text{MeV}}{M/10^{12}\,\text{kg}} .
$$

La puissance n'est **pas** celle d'un corps noir de l'aire de l'horizon. Par degré de liberté de spin $s$ :

$$
P_s = \frac{1}{2\pi}\int_0^\infty d\omega\;\hbar\omega \sum_{\text{modes}} \frac{\Gamma_{s\ell}(\omega)}{e^{\hbar\omega/k_BT_H} - (-1)^{2s}}
\equiv c_s\,\frac{\hbar c^6}{G^2M^2},\qquad \frac{\hbar c^6}{G^2} = 1{,}719\times10^{37}\ \text{W·kg}^2 .
$$

Coefficients **calculés** (script 02) et comparés à Page (1976) :

| Spin | $c_s$ par degré de liberté | Publié (Page 1976) | Pic du spectre de puissance $E/k_BT$ |
|---|---|---|---|
| 0 | 7,439 × 10⁻⁵ | — | 2,9 |
| ½ | 4,092 × 10⁻⁵ | 8,18 × 10⁻⁵ pour ν + ν̄ (accord 0,00 %) | 4,5 |
| 1 | 1,682 × 10⁻⁵ | 3,37 × 10⁻⁵ pour 2 polarisations (−0,06 %) | 6,1 |
| 2 | 1,918 × 10⁻⁶ | 3,84 × 10⁻⁶ pour 2 polarisations (−0,08 %) | 9,1 |

Somme sur les espèces, $P = \alpha(M)\,\hbar c^6/(G^2M^2)$ :

| Régime | Espèces émises | α |
|---|---|---|
| M ≫ 10¹⁴ kg | photon, graviton, 3 neutrinos | 2,83 × 10⁻⁴ |
| 10¹² ≲ M ≲ 10¹⁴ kg | + e± | 4,47 × 10⁻⁴ |
| M ≪ 10⁸ kg | tout le Modèle standard | 4,21 × 10⁻³ |
| *formule du dossier (§6)* | *photons, corps noir* | *2,07 × 10⁻⁵* |

Hypothèse : trois saveurs de neutrinos à deux états d'hélicité chacune. Si les neutrinos sont de Dirac, les
états droits seraient aussi émis (le couplage est gravitationnel) : α augmenterait de 55 % sous 10¹⁴ kg et les
masses déduites d'une puissance donnée de 24 %.

Durée de vie : $\tau = \int_0^{M_0} G^2M^2\,dM/(\alpha(M)\hbar c^4)$.

| M | r_s | k_BT | P totale | dont photons | τ |
|---|---|---|---|---|---|
| 113,5 kg | 1,7 × 10⁻²⁵ m | 9,3 × 10⁷ GeV | 5,6 × 10³⁰ W | 4,5 × 10²⁸ W | **6,0 × 10⁻¹³ s** |
| 227 kg | 3,4 × 10⁻²⁵ m | 4,7 × 10⁷ GeV | 1,4 × 10³⁰ W | 1,1 × 10²⁸ W | **4,8 × 10⁻¹² s** |
| 10⁶ kg | 1,5 × 10⁻²¹ m | 1,1 × 10⁴ GeV | 7,2 × 10²² W | 5,8 × 10²⁰ W | 0,41 s |
| 10⁹ kg | 1,5 × 10⁻¹⁸ m | 10,6 GeV | 6,1 × 10¹⁶ W | 5,8 × 10¹⁴ W | 15 ans |
| 10¹² kg | 1,5 × 10⁻¹⁵ m | 10,6 MeV | **7,7 × 10⁹ W** | 5,8 × 10⁸ W | 1,2 × 10¹¹ ans |
| 4 × 10¹² kg | 5,9 × 10⁻¹⁵ m | 2,6 MeV | 4,8 × 10⁸ W | 3,6 × 10⁷ W | 7,9 × 10¹² ans |
| 6,4 × 10¹⁵ kg | 9,5 × 10⁻¹² m | 1,7 keV | 119 W | 14 W | ~5 × 10²² ans |

### 4.2 Confrontation aux valeurs revendiquées

| Affirmation [DOC texte] | Calcul | Verdict |
|---|---|---|
| Unité de 227 kg contenant deux singularités | τ = 4,8 ps (0,6 ps pour 113,5 kg) ; 2,0 × 10¹⁹ J = 4,9 Gt TNT | **Contredit** |
| « 300–500 MW » | puissance totale ⇒ M = 5,1–3,9 × 10¹² kg ; k_BT = 2,1–2,7 MeV | cohérent avec un trou noir de ~4 × 10¹² kg, **incompatible** avec 227 kg |
| « rayons X et gamma évacués vers l'arrière » | pic des photons à 13–16 MeV ; un trou « à rayons X » (pic à 10 keV) pèse 6 × 10¹⁵ kg et rayonne 119 W | primaire = gamma, e±, neutrinos ; **pas** de rayons X primaires |
| « cône d'évacuation » | émission isotrope (Schwarzschild) ; pour Kerr, asymétrie d'émission calculée pour les neutrinos (Leahy & Unruh 1979) ; aucune collimation n'est prédite **[DÉD]** | **Contredit** |
| « plus petites qu'un électron » | r_s(4 × 10¹² kg) = 5,9 fm > rayon classique de l'électron (2,8 fm) > proton (0,84 fm) | faux pour 300–500 MW ; vrai seulement si M < 7 × 10⁸ kg (r_s < 10⁻¹⁸ m) |
| « taille d'un électron ↔ masse d'une grosse montagne » | r_s = r_e (2,82 fm) ⇔ M = 1,9 × 10¹² kg | **cohérent** [DÉD] |
| « s'évaporerait si le confinement cédait » | l'évaporation ne dépend d'aucun confinement : P ∝ 1/M² (§4.1) | **Contredit** |
| « 100 à 120 degrés » autour de l'unité | 44 % de 300–500 MW (e± et γ) déposés dans un coffre de 1,8 m² ⇒ équilibre radiatif à 6 000–6 800 K | **Contredit** |
| « refroidissement de la singularité » | capacité calorifique négative : C = −1,2 × 10¹⁹ J/K à 4 × 10¹² kg | sans objet |

Répartition de la puissance pour M ≈ 4–5 × 10¹² kg (script 02) : neutrinos 55 %, e± 37 %, photons 7,5 %,
gravitons 0,9 %. Les neutrinos (165–275 MW) traversent tout blindage. Les ~30 MW de photons, sans blindage,
donnent à 1 m un débit de dose de l'ordre de 10³ Gy/s (ordre de grandeur, à affiner par l'Équipe C).
Les rayons X ne peuvent être que **secondaires** (freinage des e±, annihilation à 511 keV) : sur ce point précis
le corpus n'est pas absurde, mais il ne décrit pas l'émission primaire.

**Source probable des chiffres [HYP].** Les ordres de grandeur « masse d'une montagne », « rayons X et gamma »,
puissance en milliers de mégawatts, « tomberait au centre de la Terre » figurent dans la vulgarisation de Hawking
(*Une brève histoire du temps*, 1988, chapitre sur le rayonnement des trous noirs — citation de mémoire, non
vérifiée en ligne). Notre calcul donne 7,7 GW pour 10¹² kg, du même ordre que la valeur de vulgarisation
(~10 GW). À confirmer par les Équipes A et G.

### 4.3 Fenêtre de masse : il n'y en a pas

| Exigence | Condition sur M |
|---|---|
| Transportable en camion | M ≲ 10³ kg |
| Durée de vie ≥ 36 ans (2036 → 1975 → 2000) | M ≥ 1,3 × 10⁹ kg (P = 3,4 × 10¹⁶ W) |
| Puissance ≤ 500 MW | M ≥ 3,9 × 10¹² kg **par singularité** |
| « 1,5–2 g » à 1–3,7 m | 2,2 × 10¹¹ – 4,0 × 10¹² kg **au total** |
| Γ = 87 660 à 1–3,7 m | 6,7 × 10²⁶ – 2,5 × 10²⁷ kg |

**Portée exacte de la cohérence « 300–500 MW ↔ 2 g »** (script 05, [B6]) :

| Lecture | Masse totale | Pesanteur à 1 m | à 2 m | 2 g atteints à |
|---|---|---|---|---|
| une singularité de 300–500 MW | 3,9–5,1 × 10¹² kg | 27–34 g | 6,7–8,6 g | 3,6–4,2 m |
| deux singularités de 300–500 MW chacune | 7,8–10,1 × 10¹² kg | 53–69 g | 13–17 g | 5,2–5,9 m |
| deux singularités totalisant 300–500 MW | 1,1–1,4 × 10¹³ kg | 75–97 g | 19–24 g | 6,1–7,0 m |

Les chiffres ne s'accordent donc que pour **une** singularité et un occupant placé à ≥ 3,6 m, au bord du champ
revendiqué (3,0–3,7 m). Pour les deux singularités que décrit le corpus, on a 13 à 69 g à 1–2 m, et 2 g seulement
au-delà de 5 m. **La cohérence n'est acquise qu'à un ordre de grandeur près** (errata E1 du dossier de base). La
première ligne du tableau précédent (transport) et la dernière (Γ) ne sont compatibles avec aucune autre.
Confiance élevée.

### 4.4 Peut-on tenir un tel objet ?

Un trou noir de 4 × 10¹² kg pèse 4 × 10¹³ N et mesure 6 fm. Le seul moyen d'agir sur lui est sa charge.
Le champ électrique de sustentation $Mg/Q$ vaut 4 × 10³¹ V/m avec la charge typique (≈ 6 e, §4.5) et encore
2 × 10³⁰ V/m avec la borne supérieure (137 e), soit 10¹² à 10¹³ fois le champ de Schwinger. **Démontré** : il
traverse le plancher et oscille à travers la Terre. À 0,3 m de lui (distance prise à titre d'exemple, [HYP]), la
pesanteur atteint 300 g ; à 0,10 m, 2 700 g : la structure du véhicule serait arrachée. Pour M = 2,6 × 10¹² kg
(« 2 g à 3 m »), on a 4,5 g à 2 m et 1,1 g à 4 m, avec une marée de 1,3 g par mètre à 3 m.

### 4.5 Charge maximale, décharge de Schwinger, « injection d'électrons »

**Extrémalité** : $Q_{\max} = M\sqrt{4\pi\varepsilon_0 G}$ = 8,62 × 10⁻¹¹ C/kg × M (86 C pour 10¹² kg). Accord avec le dossier.

**Mais cette charge est intenable** [VÉR] (Zaumen 1974 ; Carter 1974 ; Gibbons 1975 ; Damour & Ruffini 1975 ; Page 1977) :

- Champ à l'horizon d'un trou extrémal : $E_h = c^4/(G^{3/2}M\sqrt{4\pi\varepsilon_0})$ = 1,4 × 10⁴² V/m pour 10¹² kg,
  soit 10²⁴ fois le champ critique de Schwinger $E_S = m_e^2c^3/(e\hbar)$ = 1,32 × 10¹⁸ V/m.
- $E_h < E_S$ seulement pour $M > 1{,}1 \times 10^{36}$ kg ≈ 5 × 10⁵ masses solaires (script 05).
- Pour $r_s \ll \hbar/(m_ec)$ = 3,9 × 10⁻¹³ m, le trou se comporte comme un noyau ponctuel : le vide est instable
  dès que $Z\alpha \gtrsim 1$. D'où une **borne supérieure d'ordre de grandeur** : $|Q| \lesssim e/\alpha \approx 137\,e$
  = 2,2 × 10⁻¹⁷ C, soit 2,5 × 10⁻¹⁹ de la charge extrémale à 10¹² kg. Ce n'est pas une valeur attendue.
- **Valeur typique.** L'émission aléatoire de leptons chargés fait fluctuer la charge avec une valeur quadratique
  moyenne de **6,14 e** dans la limite $GM\mu/\hbar c \to 0$ (Page 1977, résumé relu ; ce paramètre vaut 0,008 pour
  4,4 × 10¹² kg et des électrons). Soit ≈ 10⁻¹⁸ C, 10⁻²⁰ de la charge extrémale à 10¹² kg. Estimation thermique
  indépendante : $1/\sqrt{4\pi\alpha}$ = 3,3 e, même ordre (script 05).

Conséquences pour M = 10¹² kg (scripts 03 et 05) :

| Grandeur | Charge typique, 6 e | Borne supérieure, 137 e |
|---|---|---|
| Horizon interne $r_- \simeq r_Q^2/r_s$ | 4,8 × 10⁻⁵⁶ m = 3 × 10⁻²¹ longueur de Planck | 2,4 × 10⁻⁵³ m = 1,5 × 10⁻¹⁸ longueur de Planck |
| Rapport force électrique / gravitationnelle entre deux tels trous | 1,3 × 10⁻⁴⁰ | 6,5 × 10⁻³⁸ |
| Moment magnétique $\mu = Qac$ (spin maximal) | 2,2 × 10⁻²⁵ A·m² ≈ 0,02 magnéton de Bohr | 4,9 × 10⁻²⁴ A·m² ≈ 0,5 magnéton de Bohr |
| Vitesse de précession dans 10 T | 1 × 10⁻²⁹ rad/s | 2 × 10⁻²⁸ rad/s |

- « Adding electric charge […] increases the diameter of the inner event horizons » : **qualitativement exact**
  ($dr_-/dQ > 0$, script 03) **[DÉD]**. Quantitativement vide de sens : $r_-$ reste 18 à 21 ordres de grandeur
  sous la longueur de Planck.
- « Rotating and positioning the polar axis » par un champ magnétique : le couple disponible réoriente le spin
  en 10²⁸ à 10²⁹ s. **Contredit.**
- « Electron injection manifold to alter mass and gravity » : un trou de 5 × 10¹² kg émet de lui-même
  7,8 × 10¹⁹ e± par seconde ; sa section efficace de capture est 12 barns. Un faisceau de 1 A focalisé sur 1 µm² y
  dépose ~7 × 10³ électrons par seconde, soit 10⁻¹⁶ de son émission propre. Même si 1 A entier était absorbé, la
  charge d'équilibre resterait de l'ordre de 2 e. Gain de masse d'un faisceau de 1 MW pendant une heure :
  ΔM/M = 10⁻²⁰. **Contredit.**
- Charger un trou jusqu'à l'extrémalité coûte la moitié de son énergie de masse finale (4,5 × 10²⁸ J pour 10¹² kg) ;
  le dernier électron doit franchir 1,04 × 10²⁷ V, potentiel indépendant de la masse
  ($c^2/\sqrt{4\pi\varepsilon_0G}$). « The electricity comes from batteries » **[DOC texte]** : *Contredit.*

### 4.6 Rotation, superradiance

- Spin maximal $J = GM^2/c$ = 2,2 × 10⁵ J·s pour 10¹² kg ; $\hbar\Omega_H$ = 133 MeV à l'extrémalité.
- Pour les particules sans masse connues, un trou en rotation rapide émet son moment cinétique plusieurs fois
  plus vite que son énergie et ralentit jusqu'à un état presque sans rotation avant d'avoir perdu l'essentiel de
  sa masse (Page 1976, article II, résumé relu) : la rotation ne se « maintient » pas sans apport. Exception
  théorique : si l'émission était dominée par des champs scalaires, l'état final garderait a/M ≈ 0,555
  (Chambers, Hiscock & Taylor 1997).
- À masse donnée, la rotation **augmente** la puissance émise (jusqu'à ×13 pour les neutrinos et ×107 pour les
  photons, même résumé de Page). Les masses du §4.1, calculées sans rotation, sont donc des minorants pour une
  singularité en rotation rapide : l'écart du §4.3 ne peut que s'aggraver.
- Superradiance classique : gains maximaux par passage ~0,3 % (scalaire), 4,4 % (électromagnétique), 138 %
  (gravitationnel) selon Press & Teukolsky (1972) et Teukolsky & Press (1974), pour des longueurs d'onde ~GM/c².
  Pour un photon X de 10 keV et M = 10¹² kg, $\omega r_g/c$ = 4 × 10⁻⁵ : couplage négligeable. Pas de source d'énergie utilisable.

### 4.7 Création et « restes »

- Créer un trou noir de masse M demande au moins $Mc^2$ : 2,0 × 10¹⁹ J pour 227 kg (12 jours de consommation
  mondiale d'énergie primaire), 3,6 × 10²⁹ J pour 4 × 10¹² kg (6 × 10⁸ années).
- En quatre dimensions, la masse minimale est de l'ordre de la masse de Planck (22 µg), soit 1,2 × 10¹⁹ GeV par
  collision : 9 × 10¹⁴ fois l'énergie du LHC. Un anneau à dipôles de 8,33 T devrait avoir un rayon de 517 années-lumière.
- Les scénarios à dimensions supplémentaires (Arkani-Hamed, Dimopoulos & Dvali 1998 ; Dimopoulos & Landsberg 2001 ;
  Giddings & Thomas 2002) prévoyaient des trous noirs de quelques TeV (~10⁻²³ kg) s'évaporant en ~10⁻²⁶ s.
  **Aucun n'a été observé** (CMS 2011, 2018). Même réels, ils seraient 10²⁵ fois trop légers et ne grossiraient pas
  (Giddings & Mangano 2008).
- « Créées, capturées et nettoyées au CERN », « machine Z » : la machine Z délivre de l'ordre de 2 MJ de rayons X
  par tir, soit 2 × 10⁻¹¹ kg d'équivalent masse. **Contredit.**
- **Restes de Planck** (Aharonov, Casher & Nussinov 1987 ; MacGibbon 1987 ; Adler, Chen & Santiago 2001 ; revue
  Chen, Ong & Yeom 2015) : *Spéculatif*. Un reste pèserait 22 µg et créerait 1,5 × 10⁻¹⁸ m/s² à 1 m. Inutilisable.

---

## 5. Thème 4 — « 10 ans par heure »

Γ = dt_ext/dτ = 10 × 365,25 × 24 = **87 660** ; ln Γ = 11,38.

### 5.1 Voie cinématique [Démontré]

$\gamma = 87\,660 \Rightarrow 1 - v/c = 6{,}5 \times 10^{-11}$. Énergie cinétique : $(\gamma - 1)c^2$ = 7,9 × 10²¹ J/kg.

| Masse | Énergie | Équivalent |
|---|---|---|
| 227 kg | 1,8 × 10²⁴ J | 3 000 ans de consommation mondiale |
| 2 500 kg (véhicule) | 2,0 × 10²⁵ J | 33 000 ans ; 0,05 s de luminosité solaire |

À 2 g constants, atteindre ce γ prend 5,85 ans de temps propre. À l'inverse, une heure à 2 g ne fait gagner que
33 µs. Ce facteur de Lorentz est banal pour une particule : un électron de 45,6 GeV au LEP avait γ = 89 000.

### 5.2 Voie gravitationnelle [Démontré dans son principe]

Observateur statique de Schwarzschild : $\Gamma = (1 - r_s/r)^{-1/2}$, d'où $r/r_s - 1 = 1{,}3 \times 10^{-10}$.
Accélération propre nécessaire : 3 × 10¹⁰ g au-dessus de Sgr A*, 10¹⁷ g au-dessus d'un trou noir solaire.
Masse pour Γ = 87 660 à 1 m : 6,7 × 10²⁶ kg ; à 3,7 m : 2,5 × 10²⁷ kg.

### 5.3 Incompatibilité « 2 g » / « 3–4 m » / « 10 ans par heure » (annexe D2)

Pour toute métrique statique $ds^2 = -N^2c^2dt^2 + h_{ij}dx^idx^j$, l'observateur statique a une accélération propre

$$
a_i = c^2\,\partial_i \ln N \qquad\Longrightarrow\qquad
\ln\frac{N_B}{N_A} = \frac{1}{c^2}\int_A^B a_i\,dx^i \;\le\; \frac{1}{c^2}\int_A^B |a|\,d\ell .
$$

Identité vérifiée symboliquement (script 06, [D3]). Avec $|a| \le 2g$ sur $L = 3{,}7$ m :

$$
\Gamma - 1 \le \frac{2gL}{c^2} = 8{,}1 \times 10^{-16}\qquad\text{(revendiqué : } 8{,}8 \times 10^4\text{)} .
$$

Inversement, ln Γ = 11,38 sur 3,7 m exige une accélération moyenne de 2,8 × 10¹⁷ m/s² = **2,8 × 10¹⁶ g** ; à 2 g
uniformes, il faudrait un champ profond de 5,5 années-lumière. **Démontré** pour tout champ statique ; confiance élevée.

Échappatoire examinée : l'intérieur d'une coquille massive est plat (pas de pesanteur ressentie) avec un
potentiel uniforme. Mais la condition d'énergie dominante impose $R \ge \tfrac{25}{24}r_s$, donc **Γ ≤ 5**
(script 06, [D4]) ; pour une étoile homogène, $p_c \le \rho c^2$ impose Γ ≤ 4. Bornes générales sur la compacité :
Buchdahl (1959), Andréasson (2008). Une coquille limite de 3,7 m pèserait 1,3 masse de Jupiter.

### 5.4 Conséquences observables inévitables d'un Γ = 87 660 [DÉD]

- **Le véhicule ne disparaît pas.** La dilatation est un ralentissement : le voyageur reste présent, visible et
  figé, pendant toute la durée extérieure.
- **Décalage vers le bleu.** Tout rayonnement entrant est décalé d'un facteur Γ : la lumière visible (≈ 2,5 eV)
  devient un rayonnement de ≈ 0,22 MeV ; l'éclairement solaire est multiplié par ~Γ², soit ~10¹³ W/m².
- **Loi de Tolman** (Tolman 1930 ; Tolman & Ehrenfest 1930) : en équilibre, $T_{\text{local}} = \Gamma\,T_\infty$.
  Un environnement à 300 K est perçu à 2,6 × 10⁷ K. Le corpus décrit au contraire un « noir complet » et
  38–49 °C **[DOC texte]**.
- Déviation de la lumière par 4 × 10¹² kg à 1 m : $4GM/(bc^2)$ = 1,2 × 10⁻¹⁴ rad. Aucune « lumière courbée » visible.

### 5.5 Pourquoi la dilatation ne mène jamais vers le passé (annexe D1)

**Théorème.** Dans un espace-temps stablement causal — en particulier globalement hyperbolique — il existe une
fonction de temps globale $t$ de gradient partout de genre temps (Hawking 1969 ; Geroch 1970 ; Bernal & Sánchez 2003).
Le long de toute courbe causale dirigée vers le futur :

$$
\frac{dt}{d\tau} = u^\mu\partial_\mu t > 0 .
$$

Le temps propre aussi est monotone ($d\tau > 0$). Le rapport $dt/d\tau$ prend n'importe quelle valeur dans
$]0, +\infty[$ mais **ne change jamais de signe**. Dilater, c'est changer le rythme, pas le sens. Revenir à un
événement de son propre passé causal, c'est par définition parcourir une courbe causale fermée ; il faut alors que
la fonction $t$ n'existe pas, donc une structure causale non triviale ($g_{\varphi\varphi} < 0$, trou de ver, etc.),
ce que ni une grande masse ni une grande vitesse ne fournissent.

Le corpus l'admet d'ailleurs : « this type of gravity manipulation is not sufficient to alter your worldline »
**[DOC texte]**. **Statut** : voyage vers le futur par dilatation, *Démontré* (Hafele & Keating 1972 ; Bailey et al.
1977 ; Chou et al. 2010 ; Bothwell et al. 2022) ; vers le passé par dilatation, *impossible par théorème dans tout
espace-temps stablement causal*.

**Réserve.** La dilatation *seule* ne crée pas de courbe fermée. Dans un espace-temps à trou de ver traversable,
c'est en revanche une différence de dilatation entre les deux bouches — cinématique (Morris, Thorne & Yurtsever
1988) ou gravitationnelle (Frolov & Novikov 1990) — qui engendre l'horizon chronologique (§6.2). L'ingrédient est
alors le trou de ver, donc l'énergie négative, et non la dilatation.

---

## 6. Thème 5 — Autres voies connues vers des CTC

| Voie | Référence | Ingrédient | Obstacle chiffré | Statut |
|---|---|---|---|---|
| Univers de Gödel | Gödel 1949 | rotation globale de la matière, Λ < 0 | l'univers observé ne tourne pas ; non constructible | solution exacte ; non réalisée |
| Cylindre de Tipler | Tipler 1974 | μ > c²/8G = 1,7 × 10²⁶ kg/m, longueur infinie | §3 | *Théoriquement possible* (infini) |
| Cordes cosmiques de Gott | Gott 1991 | deux cordes parallèles, $\gamma\sin(4\pi G\mu/c^2) > 1$ | γ > 8 × 10⁴ pour Gμ/c² = 10⁻⁶ ; impulsion totale tachyonique | *Spéculatif* ; non constructible |
| Trou de ver traversable | Morris & Thorne 1988 ; Morris, Thorne & Yurtsever 1988 | énergie négative à la gorge | tension $c^4/(8\pi Gb^2)$ = 4,8 × 10⁴² Pa pour b = 1 m | *Spéculatif* |
| Bulle d'Alcubierre | Alcubierre 1994 ; Everett 1996 | énergie négative | E = −1,4 × 10⁴⁴ J (R = 3,7 m, paroi 1 m) | *Spéculatif* |
| Tube de Krasnikov | Krasnikov 1998 ; Everett & Roman 1997 | énergie négative | idem | *Spéculatif* |
| Anneau de lumière | Mallett 2000, 2003 | lumière circulante | Ω ~ 10⁻³⁶ rad/s pour 1 MW ; critique d'Olum & Everett 2005 | *Contredit* comme machine |
| Modèles d'Ori | Ori 1993, 2005, 2007 | cœur de vide, poussière ordinaire | stabilité inconnue ; masses ~ℓc²/G | **ouvert** |

### 6.1 Gott [VÉR]

Une corde de masse linéique μ crée un espace conique de déficit $8\pi G\mu/c^2$. Deux cordes croisées à vitesse
relativiste engendrent des CTC si $\gamma\sin(4\pi G\mu/c^2) > 1$ (Gott 1991). Contrôle numérique par holonomie
SO(2,1) : 20 000 tirages sur 20 000 (script 05). C'est l'**analogue réel le plus proche** de l'idée « deux
objets en mouvement relatif créent une machine temporelle ». Mais l'impulsion totale du système est alors de
genre espace : on ne peut pas le créer à partir de matière ordinaire dans un univers ouvert (Deser, Jackiw &
't Hooft 1992 ; Carroll, Farhi & Guth 1992 ; Carroll et al. 1994), et un univers fermé s'effondre avant
('t Hooft 1992). Les cordes cosmiques n'ont jamais été observées.

### 6.2 Trous de ver et conditions d'énergie [VÉR]

- Une gorge traversable viole la condition d'énergie nulle (Morris & Thorne 1988 ; Hochberg & Visser 1998) ;
  censure topologique (Friedman, Schleich & Witt 1993). Déplacer une bouche à vitesse relativiste convertit le
  trou de ver en machine temporelle (Morris, Thorne & Yurtsever 1988).
- La théorie quantique des champs autorise des densités d'énergie négatives (Epstein, Glaser & Jaffe 1965), mais
  les borne par des **inégalités quantiques** (Ford 1978 ; Ford & Roman 1995). Champ scalaire sans masse,
  échantillonnage lorentzien de durée $\tau_0$ :

$$
\langle\rho\rangle \;\ge\; -\frac{3\hbar}{32\pi^2c^3\tau_0^4} .
$$

  Pour $\tau_0$ = 1 ns : $|\rho| \le 3{,}7 \times 10^{-26}$ J/m³. La densité requise pour une gorge de 1 m ne peut
  durer que ~10⁻²⁶ s. D'où le résultat de Ford & Roman (1996) : gorge de taille de Planck, ou énergie négative
  confinée dans une couche extrêmement mince.
- **Effet Casimir** (Casimir 1948 ; Lamoreaux 1997 ; Mohideen & Roy 1998) : $u = -\pi^2\hbar c/(720d^4)$.

| d | u | Pression | Énergie négative par m² |
|---|---|---|---|
| 1 µm | −4,3 × 10⁻⁴ J/m³ | −1,3 × 10⁻³ Pa | −4,3 × 10⁻¹⁰ J |
| 100 nm | −4,3 J/m³ | −13 Pa | −4,3 × 10⁻⁷ J |
| 10 nm | −4,3 × 10⁴ J/m³ | −1,3 × 10⁵ Pa | −4,3 × 10⁻⁴ J |

  À comparer à l'énergie de masse positive d'une plaque d'or de 1 µm : 1,7 × 10¹⁵ J/m². Atteindre 4,8 × 10⁴² J/m³
  demanderait des plaques distantes de 3 × 10⁻¹⁸ m. L'effet est **Démontré** ; son usage gravitationnel est exclu
  par 46 ordres de grandeur (à d = 1 µm).
- **Piste réelle** : des trous de ver traversables existent dans des cadres théoriques contrôlés (Gao, Jafferis &
  Wall 2017 ; Maldacena, Milekhin & Popov 2023 ; Maldacena & Milekhin 2021). Ils sont toujours *plus longs* à
  traverser que le trajet extérieur : conformes à la condition d'énergie nulle moyennée achronale (Graham & Olum
  2007 ; Faulkner et al. 2016 ; Hartman, Kundu & Tajdini 2017), ils **ne permettent pas** de machine temporelle.

### 6.3 Alcubierre, Krasnikov

Densité d'énergie re-dérivée de la contrainte hamiltonienne (script 07, [E5]) :

$$
\rho_E = -\frac{c^4}{G}\,\frac{v^2}{32\pi c^2}\,\frac{y^2 + z^2}{r^2}\left(\frac{df}{dr}\right)^2 \le 0,
\qquad E = -\frac{c^4}{12G}\frac{v^2}{c^2}\left(\frac{R^2}{\Delta} + \frac{\Delta}{12}\right).
$$

R = 3,7 m, Δ = 1 m, v = c : E = −1,4 × 10⁴⁴ J (−1,5 × 10²⁷ kg). Avec l'épaisseur de paroi permise par les
inégalités quantiques (~100 longueurs de Planck, Pfenning & Ford 1997) : −10⁶⁰ kg. Deux bulles permettent une CTC
(Everett 1996). Les propositions à énergie positive (Lentz 2021 ; Bobrick & Martire 2021) sont contestées
(Santiago, Schuster & Visser 2022).

### 6.4 Mallett

La lumière gravite (Tolman, Ehrenfest & Podolsky 1931), mais sa masse linéique est P/c³ = 4 × 10⁻²⁰ kg/m pour
1 MW. Atteindre le seuil de Tipler demanderait $c^5/8G$ = 4,5 × 10⁵¹ W. Olum & Everett (2005) montrent que la
solution de Mallett contient une source singulière linéique indépendante de la lumière, et que les CTC se
situeraient à des distances dépassant de très loin la taille de l'univers observable pour tout laser réaliste.

### 6.5 Piste théorique ouverte : les modèles d'Ori

Ori (2005, 2007) construit des espaces-temps réguliers, asymptotiquement plats, de topologie triviale, faits de
vide et de poussière à densité positive (conditions d'énergie faible, dominante et forte satisfaites), où des CTC
se forment dans un cœur toroïdal vide à partir de données initiales régulières. Selon l'auteur lui-même, **la
stabilité reste la principale question ouverte** (résumé arXiv gr-qc/0503077).

**[DÉD]** Ces modèles ne contredisent pas les théorèmes du §3.4 : puisqu'ils satisfont la condition d'énergie
faible à partir d'une hypersurface initiale non compacte, le théorème de Hawking (1992) implique, par contraposée,
que leur horizon de Cauchy n'est pas compactement engendré au sens strict, et celui de Tipler (1977) que des
singularités s'y développent. Nous n'avons pas vérifié ce point dans le texte des articles (§14). Autre question
ouverte : le sens dans lequel les données initiales « causent » les CTC (Krasnikov 2002 ; Earman, Smeenk &
Wüthrich 2009). Les masses requises restent de l'ordre de ℓc²/G. **Aucun lien avec le dispositif décrit.**

---

## 7. Thème 6 — Causalité

### 7.1 Protection chronologique [conjecture]

- Hawking (1992) : classiquement, un horizon de Cauchy compactement engendré exige de l'énergie négative ;
  quantiquement, $\langle T_{\mu\nu}\rangle$ diverge en général à l'horizon chronologique (Kim & Thorne 1991).
- Kay, Radzikowski & Wald (1997) : **théorème** — sur un espace-temps à horizon de Cauchy compactement engendré,
  aucun état n'est de Hadamard aux points de base de l'horizon ; la gravité semi-classique y perd toute validité.
- Des contre-exemples à la divergence existent (Krasnikov 1996). La décision appartient à la gravité quantique
  (Visser 2002). **Statut : conjecture non démontrée, sans contre-exemple physiquement réalisable.**

### 7.2 Auto-cohérence de Novikov [modèle classique cohérent]

Seules les histoires globalement cohérentes se réalisent (Friedman et al. 1990). Pour des boules de billard
traversant un trou de ver, Echeverria, Klinkhammer & Thorne (1991) trouvent toujours des solutions cohérentes,
souvent en nombre infini. Pas de paradoxe ; un seul univers ; le passé ne peut pas être modifié.

### 7.3 Modèles quantiques [modèles cohérents, non réalisés]

- **Deutsch (1991)** : l'état sur la CTC est un point fixe $\rho = \mathrm{Tr}_{\rm CR}[U(\rho_{\rm in}\otimes\rho)U^\dagger]$,
  qui existe toujours. Pour le « paradoxe du grand-père » (porte NON sur la boucle), le point fixe est l'état
  maximalement mélangé (script 08, [C7]). L'évolution effective est **non linéaire et non unitaire** (vérifié
  numériquement), d'où des critiques (Bennett et al. 2009) et des conséquences calculatoires extrêmes
  (Aaronson & Watrous 2009).
- **P-CTC** (Lloyd et al. 2011) : téléportation post-sélectionnée ; les histoires paradoxales ont une probabilité
  nulle (amplitude $\propto \mathrm{Tr}\,U$ = 0 pour la porte NON). Équivaut à une version quantique de Novikov.
- Autres formulations : Politzer (1992), Hartle (1994), Allen (2014), Tobar & Costa (2020).
- **Expériences** : simulations optiques de D-CTC (Ringbauer et al. 2014) et de P-CTC (Lloyd et al. 2011).
  Ce sont des **simulations** de l'algèbre, pas des CTC.

### 7.4 Everett et la « divergence des lignes d'univers »

Le corpus : « The Everett Wheeler model is correct » ; le voyageur arrive sur une ligne d'univers divergente de
1 à 2,5 % ; la divergence serait « an empirical indicator » fondé sur « the local gravitational field as compared
to the point of origin » **[DOC texte]**.

1. **Les branches d'Everett ne sont pas des lieux.** Elles résultent de la décohérence (Everett 1957 ; Zurek 2003 ;
   Wallace 2012). La linéarité de la mécanique quantique interdit toute interaction entre branches décohérées.
   Polchinski (1991) a montré qu'une mécanique quantique *non linéaire* à la Weinberg (1989) permettrait soit une
   signalisation supraluminique (Gisin 1990), soit une communication entre branches. Les tests bornent la non-linéarité
   à ~4 × 10⁻²⁷ en valeur relative (Bollinger et al. 1989). **Analogue réel** du « passage entre lignes d'univers » :
   *Spéculatif*, fortement contraint.
2. **Le modèle de Deutsch est le plus proche du récit.** Lu dans le cadre d'Everett, le voyageur quitte une branche
   et émerge dans une autre (Deutsch 1991 ; Deutsch & Lockwood 1994, *Scientific American*, source de vulgarisation
   antérieure aux messages **[HYP]**). Mais ce modèle *présuppose* une CTC ; il ne dit pas comment la produire.
   A. Everett (2004) montre de plus que, pour un objet macroscopique, cette lecture ne garantit pas que l'objet
   arrive entier dans une même branche.
3. **Aucun lien entre Kerr et Everett.** Les régions I′ du diagramme de Penrose sont classiques.

**La « divergence en % » a-t-elle un sens ?**

- *Quantique* : la distance naturelle est $1 - |\langle\psi_A|\psi_B\rangle|^2$. Deux branches macroscopiquement
  distinctes sont orthogonales : la divergence vaut 100 % dès le premier écart. Pas de continuum.
- *Classique* : dans un système chaotique, l'écart microscopique croît exponentiellement, tandis que les
  moyennes macroscopiques restent voisines ; toute valeur dépend d'un choix arbitraire de variables.
- *Gravimétrique* (script 08, [C6]) : les marées font varier g de 3 × 10⁻⁷ ; un véhicule de 2,5 t à 3 m, de
  2 × 10⁻⁹ ; l'écart équateur-pôle est 0,53 %. Une variation de **1 %** correspond à 32 km d'altitude ou à 1 % de
  la masse terrestre. Un gravimètre absolu résout ~10⁻⁹ g (Niebauer et al. 1995 ; Ménoret et al. 2018).
  De plus, à 0,5 m d'une « singularité » de 10¹² kg, le champ propre de l'unité vaut 27 g : ses capteurs seraient saturés.

**Verdict** : grandeur non définie ; *aucun sens physique* comme mesure d'écart entre univers. Elle n'a de sens
que comme métrique d'ingénierie (écart entre deux cartes de gravité locales), sans rapport avec une « ligne d'univers ».

---

## 8. Thème 7 — Champs électromagnétiques comme source de gravité

### 8.1 Principe [VÉR]

$$
T^{\mu\nu}_{\rm EM} = \frac{1}{\mu_0}\left(F^{\mu\alpha}F^\nu{}_\alpha - \tfrac14 g^{\mu\nu}F_{\alpha\beta}F^{\alpha\beta}\right),\qquad
G_{\mu\nu} = \frac{8\pi G}{c^4}\,T_{\mu\nu},\qquad \frac{8\pi G}{c^4} = 2{,}08 \times 10^{-43}\ \text{N}^{-1} .
$$

Le champ électromagnétique courbe l'espace-temps comme toute énergie : Reissner (1916) ; Bonnor (1954) ;
Melvin (1964) ; Ernst (1976) ; Wald (1974) ; Füzfa (2016) pour les solénoïdes. Indices expérimentaux : l'énergie
électromagnétique de liaison contribue à la masse passive et active (Kreuzer 1968 ; Bartlett & Van Buren 1986).

### 8.2 Univers magnétique de Melvin (vérifié, script 07)

$$
ds^2 = \Lambda^2\left(-c^2dt^2 + d\rho^2 + dz^2\right) + \frac{\rho^2}{\Lambda^2}d\varphi^2,\qquad
\Lambda = 1 + \frac{\rho^2}{\rho_M^2},\qquad \rho_M = \frac{2c}{B\sqrt{4\pi\varepsilon_0G}} = \frac{6{,}96 \times 10^{18}\ \text{m·T}}{B} .
$$

### 8.3 Intensité nécessaire à l'échelle du mètre

Échelle de courbure définie par $8\pi Gu/c^4 = 1/L^2$, $u = B^2/2\mu_0$ :

$$
B = \frac{c^2}{L}\sqrt{\frac{\mu_0}{4\pi G}} = \frac{3{,}48 \times 10^{18}\ \text{T·m}}{L},\qquad E = cB = \frac{1{,}04 \times 10^{27}\ \text{V}}{L} .
$$

| Champ | B | u/c² | L |
|---|---|---|---|
| Record continu (Hahn et al. 2019) | 45,5 T | 9 × 10⁻⁹ kg/m³ | 7,6 × 10¹⁶ m (8 années-lumière) |
| Record en laboratoire fermé (Nakamura et al. 2018) | 1 200 T | 6 × 10⁻⁶ kg/m³ | 2,9 × 10¹⁵ m |
| Champ critique de Schwinger | 4,4 × 10⁹ T | 9 × 10⁷ kg/m³ | 7,9 × 10⁸ m |
| Magnétar | ~10¹¹ T | 4 × 10¹⁰ kg/m³ | 3,5 × 10⁷ m |
| **Requis pour L = 1 m** | **3,5 × 10¹⁸ T** | 5 × 10²⁵ kg/m³ | 1 m |

- Un champ électrique statique ne peut dépasser le champ de Schwinger : **L ≥ 7,9 × 10⁸ m. Démontré.**
- 45,5 T dans un litre : 8 × 10⁵ J, soit 9 × 10⁻¹² kg ; à 10 cm, Φ/c² = 7 × 10⁻³⁸.
- La pression magnétique à 1 200 T (5,7 × 10¹¹ Pa) détruit déjà toute bobine.
- Les bobines et régulateurs de DOC-008, alimentés par batterie, restent à 17 ordres de grandeur (en champ) de toute influence gravitationnelle à cette échelle.

**Statut** : gravitation du champ électromagnétique, *Démontré* en principe ; courbure macroscopique par des
champs de laboratoire, *Contredit les connaissances actuelles*. Confiance élevée.

---

## 9. Réponses aux questions fondamentales

### Q2 — Quel rôle pourraient jouer les deux singularités ?

**Aucun rôle dans la création d'une structure causale non triviale.**

1. Un trou noir n'a que M, J, Q. À une distance $r \gg GM/c^2$, le champ de deux trous noirs est la superposition
   linéaire de deux champs faibles ; il n'y a ni interférence ni « sinusoïde » statique.
2. L'extérieur de chaque trou noir est stablement causal (§2.3, sous l'hypothèse d'un horizon). Les CTC de Kerr
   sont à moins de ~2GM/c² de l'anneau, derrière un horizon de Cauchy instable. Sans horizon (objet sur-extrémal),
   la proposition D3 (b) confine encore toute CTC à moins de ~10⁻¹³ m des singularités.
3. Par invariance d'échelle, deux trous ne font pas mieux qu'un : une zone à CTC de 1 m demande 10²⁷ kg.
4. Il n'existe pas d'équilibre stationnaire de deux trous de Kerr ; une paire orbitale est newtonienne à 10⁻⁷ près.
   Son moment cinétique orbital entraîne les référentiels à 10⁻¹⁵–10⁻¹⁴ rad/s à 1 m (§3.5 e) : mesurable en
   principe, sans effet causal.
5. Rôles **réels** d'une seconde masse : déplacer le barycentre (trivial ; c'est ce que décrit « steering
   singularity » **[HYP]**), créer un terme de marée oscillant à 2ω.
6. Analogue réel d'une machine « à deux objets » : les cordes de Gott (§6.1), non constructibles.

Confiance élevée.

### Q4 — Les champs électromagnétiques peuvent-ils produire les effets gravitationnels décrits ?

**Non : il manque 17 ordres de grandeur sur le champ, 34 sur la densité d'énergie.** Ils gravitent (§8.1), mais
la courbure à l'échelle du mètre exige 3,5 × 10¹⁸ T ; la densité d'énergie d'un champ de 45,5 T vaut 1,7 × 10⁻³⁴
fois la densité requise. Un champ électrique
est en outre plafonné par la création de paires. Les champs ne peuvent ni tenir (§4.4), ni orienter, ni charger
(§4.5) un micro-trou noir. Confiance élevée.

### Q5 — Existe-t-il des solutions connues des équations d'Einstein correspondant à certains aspects ?

Oui, pour des aspects **isolés** :

| Aspect du récit | Solution exacte | Écart |
|---|---|---|
| Deux horizons, anneau, « autre univers » | Kerr, Kerr-Newman, Reissner-Nordström | extension idéale, instable, échelle GM/c² |
| CTC par rotation | van Stockum-Tipler ; Gödel | source infinie ou cosmologique |
| Deux trous noirs chargés à l'équilibre | Majumdar-Papapetrou | charge extrémale intenable sous 10⁵ masses solaires |
| Deux trous noirs en rotation | double-Kerr avec strut | pas d'équilibre libre |
| Deux objets en mouvement ⇒ CTC | Gott | cordes infinies, impulsion tachyonique |
| Trou noir dans un champ magnétique | Wald (1974) ; Ernst (1976) | aucun effet causal |
| Champ magnétique auto-gravitant | Melvin | 10¹⁸ T |
| Passage vers une autre région | Morris-Thorne | énergie négative |
| Zones emboîtées « temps négatif / nul / positif » | extérieur de Tipler, $aR > 1/2$ | **[HYP]** rapprochement de notre part |

**Aucune** solution connue ne réunit : source compacte, masse modeste, matière ordinaire, CTC accessibles.

### Q6 — Une distorsion locale macroscopique de l'espace-temps est-elle possible ?

- **Oui, au sens faible** : toute masse en crée une. Champ gravitationnel de billes de 90 mg mesuré (Westphal
  et al. 2021) ; décalage gravitationnel résolu sur 1 mm (Bothwell et al. 2022) ; g/c² = 1,1 × 10⁻¹⁶ par mètre.
- **Non, au sens fort**, avec des moyens humains : une distorsion d'ordre unité sur une longueur ℓ exige
  $M \sim \ell c^2/2G$ = 6,7 × 10²⁶ kg par mètre, soit 6 × 10⁴³ J. Les 227 kg de l'unité donnent Φ/c² = 1,7 × 10⁻²⁵ à 1 m.
- Les distorsions « exotiques » (trou de ver, bulle) demandent une énergie négative que les inégalités quantiques
  limitent à des échelles sub-nucléaires.

*Démontré* (faible) ; *Contredit les connaissances actuelles* (forte, à cette échelle d'énergie).

### Q7 — Existe-t-il une formulation cohérente du déplacement temporel sans violation de causalité ?

- **Vers le futur** : oui, *Démontré*. C'est le seul « déplacement temporel » réel.
- **Vers le passé** : revenir dans son propre passé causal *est* une courbe causale fermée ; « sans violation de
  causalité » ne peut signifier que « sans paradoxe ». En ce sens, **oui, des formulations logiquement cohérentes
  existent** : Novikov (classique), Deutsch, P-CTC (quantiques).
- **Mais** aucun mécanisme physique connu ne produit de CTC dans une région finie avec de la matière ordinaire
  sans singularité (Tipler 1977 ; Hawking 1992), et l'instabilité quantique des horizons chronologiques est
  générique (Kay, Radzikowski & Wald 1997). *Spéculatif.*
- La variante du corpus — arriver dans le passé d'un *autre* univers — n'a **aucune formulation** en physique
  connue : ni les régions de Kerr ni les branches d'Everett ne sont des copies décalées dans le temps que l'on
  pourrait atteindre. Le modèle de Deutsch en est l'analogue le plus proche, sans mécanisme.

---

## 10. Tableau de synthèse

| Idée du corpus | Objet physique réel le plus proche | Statut |
|---|---|---|
| Deux « micro-singularités » dans un coffre de 227 kg | trous noirs primordiaux (Hawking 1971), jamais observés | **Contredit** (τ = 4,8 ps ; 4,9 Gt TNT) |
| « 300–500 MW » | rayonnement de Hawking d'un trou de 3,9–5,1 × 10¹² kg | *Théoriquement possible* pour cet objet ; **Contredit** pour 227 kg |
| « plus petites qu'un électron » | r_s < 10⁻¹⁸ m ⇔ M < 7 × 10⁸ kg | incompatible avec 300–500 MW |
| « électron ↔ montagne » | r_s = r_e ⇔ 1,9 × 10¹² kg | cohérent [DÉD] |
| Rayons X évacués par un cône | émission isotrope de γ, e±, ν à ~10 MeV | **Contredit** (X secondaires possibles) |
| « S'évapore si le confinement cède » | évaporation indépendante de tout confinement | **Contredit** |
| Confinement magnétique | piégeage de particules chargées ; charge d'un trou ≈ 6 e (typique), ≲ 137 e (borne) | **Contredit** |
| Injection d'électrons modifiant masse et horizon interne | Reissner-Nordström : $dr_-/dQ > 0$ | formule *Démontrée* ; application **Contredite** (r₋ ~ 10⁻⁵³ m) |
| Orientation de l'axe polaire | moment magnétique de Kerr-Newman (g = 2) | **Contredit** (précession 10⁻²⁸ rad/s) |
| Singularité en anneau traversable | géométrie de Kerr idéale (Carter 1968) | *Démontré* (math.) ; *Spéculatif* (réel) |
| « Autre ligne d'univers » par le diagramme de Penrose | extension analytique maximale | *Spéculatif* ; confusion avec Everett |
| « Le trou noir vient à vous » | covariance générale | **Contredit** |
| « Sinusoïde de Tipler » | (i) extérieur égal à r fois une sinusoïde de ln r pour aR > ½ ; (ii) champ proche à 2ω | terme absent avant 2010 ; analogues *Démontrés* mais sans rapport d'échelle |
| « Cylindre de Tipler sans la masse » | invariance d'échelle du vide | **Contredit** (démontré) |
| Deux trous noirs « top-spin, dual-positive » | Majumdar-Papapetrou ; double-Kerr | pas d'équilibre (théorème) |
| « 10 ans par heure » | dilatation Γ = 87 660 (électrons du LEP) | *Démontré* vers le futur ; énergie 8 × 10²¹ J/kg |
| 1,5–2 g pendant le trajet | pesanteur newtonienne de ~10¹² kg au total | incompatible avec Γ (facteur 10²⁰) ; cohérent avec 300–500 MW à un ordre de grandeur près |
| Noir complet, 38–49 °C | décalage vers le bleu ×Γ, loi de Tolman | **Contredit** |
| Voyage vers le passé | CTC (Kerr interne, Tipler, Gott, trous de ver) | *Spéculatif* ; aucun mécanisme constructible |
| Absence de paradoxe par Everett | modèle de Deutsch (1991) | *Spéculatif* ; cohérent, non réalisé |
| Divergence en % par gravimétrie | aucun | non défini |
| Champs magnétiques créant la distorsion | Melvin ; $T^{\mu\nu}_{\rm EM}$ | **Contredit** (10¹⁸ T requis) |
| Micro-trous noirs créés au CERN | scénarios de gravité au TeV | *Spéculatif*, non observé ; 10²⁵ fois trop légers |
| Singularité stable et froide | trou noir extrémal à charge magnétique (§12.1) | *Spéculatif* |

---

## 11. Désaccords avec le dossier de base (§6)

Les **coefficients** du dossier sont exacts à < 0,1 % (script 01). Les désaccords portent sur la **physique** :

| Grandeur | Dossier (photons, corps noir) | Équipe B (toutes espèces, corps gris) | Facteur |
|---|---|---|---|
| Puissance à 10¹² kg | 3,56 × 10⁸ W | 7,7 × 10⁹ W (dont photons 5,8 × 10⁸ W) | ×22 |
| Masse pour 300–500 MW | 1,1–0,84 × 10¹² kg | **5,1–3,9 × 10¹² kg** | ×4,6 |
| r_s correspondant | 1,3–1,6 fm | 5,8–7,5 fm | ×4,6 |
| k_BT correspondant | « dizaines de MeV » | 2,1–2,7 MeV (photons vers 13–16 MeV) | — |
| Durée de vie, 100 kg | ~10⁻¹⁰ s | 4,1 × 10⁻¹³ s | ÷203 |
| Durée de vie, 227 kg | 9,8 × 10⁻¹⁰ s | 4,8 × 10⁻¹² s | ÷203 |
| Durée de vie, 10¹² kg | ~3 × 10¹² ans | 1,2 × 10¹¹ ans | ÷23 |
| Charge, 10¹² kg | 86 C | 86 C (extrémalité) ; **typique ≈ 10⁻¹⁸ C (6 e), borne ≈ 2 × 10⁻¹⁷ C (137 e)** | ÷4 × 10¹⁸ à ÷9 × 10¹⁹ |

Le flux de photons réel vaut 1,62 fois la formule de corps noir sur l'aire de l'horizon. Le constat provisoire du
dossier est confirmé pour l'incompatibilité avec 227 kg. Sa « cohérence interne » doit en revanche être
**restreinte** (errata E1) : 300–500 MW et « 2 g » ne s'accordent, vers 4 × 10¹² kg, que pour **une** singularité
et un occupant à ≥ 3,6 m ; pour deux singularités de 3,9–5,1 × 10¹² kg, on trouve 53–69 g à 1 m, 13–17 g à 2 m,
et 2 g seulement à 5,2–5,9 m (§4.3). La cohérence n'est acquise qu'à un ordre de grandeur près.

---

## 12. Pistes ouvertes et analogues physiques réels

### 12.1 Trou noir extrémal à charge magnétique [Spéculatif]

Un trou noir extrémal a T = 0 : il ne s'évapore pas. S'il porte une charge *magnétique* et qu'il n'existe aucun
monopôle léger pour l'évacuer, il ne peut pas non plus se décharger (raisonnement standard ; pour la physique des
trous noirs magnétiques dans le Modèle standard, voir Maldacena 2021). C'est le seul objet de la théorie qui soit
à la fois une « singularité » froide et **piégeable par un champ magnétique** (script 08, [C4]) :

$$
M = g\sqrt{\frac{\mu_0}{4\pi G}} = 38{,}7\ \text{kg par A·m},\qquad B_{\text{sustentation}} = g_0\sqrt{\frac{\mu_0}{4\pi G}} = 380\ \text{T (indépendant de M)} .
$$

Mais : il ne rayonne pas (contredit « 300–500 MW ») ; il vérifie $B(r)/g_{\rm grav}(r)$ = 38,7 T par m/s², donc
« 2 g » implique 760 T au même endroit ; il n'engendre aucune CTC ; les monopôles n'ont jamais été observés.

### 12.2 Autres pistes

- **Intérieur de Kerr** : la censure cosmique forte est un sujet actif (Dafermos & Luk 2025).
- **Modèles d'Ori** : formation de CTC avec matière ordinaire, hors hypothèses de Hawking ; stabilité inconnue.
- **Trous de ver traversables non chronoclastes** : cohérents, sans usage temporel.
- **Linéarité quantique** : tout « passage entre branches » exigerait une non-linéarité, testable en laboratoire.
- **CTC simulées** : circuits optiques D-CTC / P-CTC (pour l'Équipe F : aucune de ces expériences n'est dangereuse).
- **Métrologie** : comparaison d'horloges optiques à l'échelle du millimètre ; gravimétrie atomique.

---

## 13. Erreurs factuelles de physique relevées dans le corpus (pour l'Équipe G)

| Passage [DOC texte] | Fait [VÉR] |
|---|---|
| « Tipler […] theory of massive rotating **spheres** » | cylindres (Tipler 1974) |
| « the math has been around since 1970 » | Kerr 1963, Carter 1968, Tipler 1974, van Stockum 1937 |
| Équivalence gravité-accélération attribuée à la relativité restreinte (« STR ») | principe d'équivalence, relativité générale |
| Horloges atomiques : l'écart ne viendrait « pas » du mouvement de l'avion | Hafele & Keating (1972) : effets cinématique **et** gravitationnel |
| Physique des trous de Kerr « derived from special relativity » | relativité générale |
| « space-like trips (faster than light) through the singularity » | trajets de genre temps (et contredit ailleurs dans le corpus) |
| « the Tipler cylinder is only a thought experiment to explain […] Kerr black holes » | solutions indépendantes |
| Micro-singularités « a fraction of the size of an electron » **et** « 300–500 megawatts » | incompatibles (§4.2) |
| « ergosphère négative / positive », « horizon des événements de temps négatif » | notions inexistantes |

Le corpus contient aussi des paraphrases **correctes** de la vulgarisation : deux horizons pour un trou chargé ou
en rotation ; singularité annulaire évitable dans la solution idéale ; évaporation des trous noirs ; la dilatation
seule ne change pas de « ligne d'univers ». Le profil est celui d'un lecteur de vulgarisation des années 1980–1990,
non d'une source technique **[DÉD]**, confiance moyenne.

---

## 14. Limites et points non résolus

1. **Spin-down quantitatif** : nous n'avons pas calculé les facteurs de corps gris de Kerr ; l'affirmation
   « le spin décroît plus vite que la masse » repose sur la littérature (Page 1976 II).
   De même, la nature de Dirac ou de Majorana des neutrinos déplace les masses du §4 de + 24 % au plus.
2. **Seuils hadroniques** dans α(M) : approximation ; ± 20 % sur τ entre 10⁸ et 10¹¹ kg.
3. **Borne générale sur Γ** pour une matière statique satisfaisant la condition d'énergie dominante : démontrée
   ici pour deux modèles (coquille mince, étoile homogène), pas en toute généralité.
4. **Charge maximale d'un micro-trou noir** : $Z\alpha \lesssim 1$ est un critère d'ordre de grandeur ; l'écart de
   19 ordres de grandeur avec l'extrémalité rend la conclusion insensible au détail.
5. **Source des chiffres du corpus** (Hawking 1988 ; Deutsch & Lockwood 1994) : hypothèse non vérifiée en ligne.
   **Modèles d'Ori** : leur compatibilité avec les théorèmes de Tipler et de Hawking est déduite par contraposée
   (§6.5), non vérifiée dans le texte des articles.
6. **Rapprochement DOC-009 / extérieur de Tipler** : hypothèse de notre part.
7. **Scénarios à dimensions supplémentaires** : traités qualitativement.
8. Les bornes observationnelles sur les cordes cosmiques (Gμ/c² ≲ 10⁻⁷ et moins) sont citées en ordre de grandeur,
   sans référence vérifiée.
9. Sens de « top-spin, dual-positive » : non élucidé.
10. **Rotation et puissance** : nos masses pour 300–500 MW supposent des trous sans rotation ; pour un trou en
    rotation rapide la puissance à masse donnée est plus élevée (Page 1976 II), donc la masse correspondante plus
    grande. Non chiffré ici.
11. **Entraînement orbital** : formule de spire en moyenne temporelle, valable sur l'axe ; le champ
    gravitomagnétique instantané hors axe n'a pas été calculé.
12. **Séparation des singularités** : l'entraxe 0,098 ± 0,025 m est une déduction de confiance faible de
    l'Équipe A ; rien n'indique que les logements dessinés fixent la distance entre les singularités.

---

## 15. Journal des corrections post-validation

Corrections demandées par la Red Team n° 2 (`08_red_team/CORRECTIONS_A_APPLIQUER.md`, section 2, n° 17 à 28).
Toutes ont été examinées par un recalcul ou une relecture de source. **Aucune n'est contestée** ; aucun verdict ne change.

| N° | Action | Fichiers touchés |
|---|---|---|
| 17 | **Appliquée.** L'entraînement « ≤ 3 × 10⁻²² rad/s » ne vaut que pour le spin d'un trou isolé. Ajout du terme orbital d'une paire (formule de spire, recalculée) : 2,7–4,5 × 10⁻¹⁵ rad/s (2 × 10¹² kg) et 2,5–5,2 × 10⁻¹⁴ rad/s (2 × 4,4–5,1 × 10¹² kg) à 1 m. Colonne renommée « Ω (spin seul, trou isolé) ». Nos valeurs sont 3 % sous celles de la Red Team (champ lointain). | `RAPPORT_B.md` §0.2, §3.5 (e), Q2, §14 ; `verifications/05_deux_trous_noirs.py` [B1], [B3bis] et sortie |
| 18 | **Appliquée.** « Intérieurement cohérent » et « confirmé et renforcé » remplacés : accord seulement pour une singularité et un occupant à ≥ 3,6 m ; 53–69 g à 1 m, 13–17 g à 2 m, 2 g à 5,2–5,9 m pour deux singularités. Tableau à trois lectures ajouté. | `RAPPORT_B.md` §4.3, §10, §11 ; script 05 [B6] |
| 19 | **Appliquée et renforcée.** Hypothèse d'horizon énoncée en tête de D4 et au §2.3 ; cas sur-extrémal renvoyé à D3 (b). Ajout d'un résultat exact sans hypothèse d'horizon (temps de Kerr-Schild, vérifié symboliquement). | `ANNEXE_B1_demonstrations.md` D4 ; `RAPPORT_B.md` §2.3, Q2 ; `verifications/03_kerr_newman.py` [A6] |
| 20 | **Appliquée.** Réserve « trou de ver » ajoutée ; « impossible par théorème » → « impossible par théorème dans tout espace-temps stablement causal ». | Annexe D1 ; `RAPPORT_B.md` §5.5 ; `REFERENCES.md` |
| 21 | **Appliquée.** Les quatre hypothèses de D2 sont énoncées ; cas non stationnaire renvoyé à D3 (a). | Annexe D2 |
| 22 | **Appliquée.** « Littéralement sinusoïdal en ln r » → « r fois une sinusoïde de ln r ». | `RAPPORT_B.md` §0.11, §3.3, §10 ; annexe D10 |
| 23 | **Appliquée.** Limite de l'analogie avec DOC-009 : pour aR > ½ les zones de signe de g_φφ ne sont pas causalement distinctes (Tipler 1974, résumé relu). | `RAPPORT_B.md` §3.3 ; annexe D10 |
| 24 | **Appliquée.** Chambers, Hiscock & Taylor (1997) retirée de l'appui et citée comme exception (a/M → 0,555, résumé relu). Ajout tiré du résumé de Page (1976 II) : la rotation augmente la puissance, nos masses sont des minorants. | `RAPPORT_B.md` §4.6, §14 ; `REFERENCES.md` |
| 25 | **Appliquée.** Leahy & Unruh (1979) : « asymétrie d'émission des neutrinos ; aucune collimation n'est prédite [DÉD] ». | `RAPPORT_B.md` §4.2 ; `REFERENCES.md` |
| 26 | **Appliquée.** Charge typique ≈ 6 e (6,14 e, Page 1977, résumé relu) ; 137 e présenté comme borne supérieure d'ordre de grandeur. Tableau à deux colonnes. | `RAPPORT_B.md` §0.8, §4.4, §4.5, §10, §11 ; annexe D7 ; scripts 03 et 05 et sorties |
| 27 | **Appliquée.** Entraxe documentaire 0,098 m (Équipe A) donné à côté de 0,3 m, désormais étiqueté [HYP]. | `RAPPORT_B.md` §3.3, §3.5 (c)(d)(e), §4.4, §14 ; script 05 [B3], [B4] |
| 28 | **Appliquée.** Durée de `executer_tout.py` : 144 s selon la Red Team, 140 à 144 s chez nous ; l'en-tête du script est corrigé et le script affiche sa durée. (Le rapport lui-même ne donnait pas de durée.) | `verifications/executer_tout.py` ; `RAPPORT_B.md` §1 |
| — | **Correction supplémentaire** (non numérotée, signalée par H et la Red Team, vérifiée) : « Tipler sinusoid » a une occurrence en texte intégral, arXiv:1008.3244 (2010), postérieure au récit. | `RAPPORT_B.md` §0.11, §3.3, §10 ; `REFERENCES.md` |

**Chiffres modifiés ou ajoutés**

| Grandeur | Version 1 | Version 1.1 |
|---|---|---|
| Entraînement des référentiels à 1 m | ≤ 3 × 10⁻²² rad/s | 3 × 10⁻²² rad/s (spin, trou isolé de 10¹² kg) ; 2,7 × 10⁻¹⁵ à 5,2 × 10⁻¹⁴ rad/s (terme orbital d'une paire) |
| Charge d'un micro-trou noir | ≤ 137 e | ≈ 6 e typique ; ≲ 137 e (borne) |
| Horizon interne dû à la charge, 10¹² kg | 2,4 × 10⁻⁵³ m | 4,8 × 10⁻⁵⁶ m (typique) à 2,4 × 10⁻⁵³ m (borne) |
| Champ de sustentation, 4 × 10¹² kg | 2 × 10³⁰ V/m | 4 × 10³¹ V/m (typique) ; 2 × 10³⁰ V/m (borne) |
| Précession du spin dans 10 T | 2 × 10⁻²⁸ rad/s | 10⁻²⁹ (typique) à 2 × 10⁻²⁸ rad/s (borne) |
| Séparation des singularités | 0,3 m | 0,098 m (Équipe A) et 0,3 m [HYP] |
| Coalescence, 2 × 10¹² kg | 6 × 10³² s | 2,3 × 10²³ ans (0,098 m) ; 2,0 × 10²⁵ ans (0,3 m) |
| Pulsation orbitale, 2 × 10¹² kg | 70 rad/s | 377 rad/s (0,098 m) ; 70 rad/s (0,3 m) |
| Force mutuelle, 2 × 10¹² kg | 7 × 10¹⁴ N | 7 × 10¹⁵ N (0,098 m) ; 7 × 10¹⁴ N (0,3 m) |
| Cohérence « 300–500 MW ↔ 2 g » | « confirmée et renforcée » vers 4 × 10¹² kg | à un ordre de grandeur près ; 13–69 g à 1–2 m pour deux singularités |

Les chiffres centraux (masses pour 300–500 MW, durées de vie, Γ, champs électromagnétiques requis) sont inchangés.

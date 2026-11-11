# Recherches complémentaires nécessaires — machine optimisée (Équipe I, Phase 6)

Version 1.1 — 10 novembre 2026 (vocabulaire aligné sur les corrections post-validation). Complète `09_recherche_contemporaine/RECHERCHES_SUPPLEMENTAIRES.md` (Équipe H) **sans
le dupliquer** : les questions ouvertes de physique fondamentale (Q1 à Q12 de l'Équipe H) ne sont pas reprises ;
on y renvoie quand elles conditionnent un palier.

> Objet : ce qu'il faudrait encore établir pour **construire, dimensionner ou juger** les paliers C204-R1, R2 et R3
> décrits dans `RAPPORT_I.md`. Rien ici ne suppose qu'un déplacement vers le passé soit possible.

Priorité : **A** = pourrait renverser une conclusion du rapport I ; **B** = nécessaire avant toute réalisation ;
**C** = veille ou confort. « (de mémoire) » signale un élément que nous n'avons pas vérifié en ligne.

---

## Partie 1 — Ce qui pourrait renverser une conclusion (priorité A)

### C1. Existe-t-il une horloge de classe 10⁻¹³–10⁻¹⁴ sur un jour qui entre dans 23 cm de profondeur ?

- **Pourquoi.** La conclusion centrale du palier 1 (« le coffre seul ne peut pas mesurer son propre déplacement
  temporel ») tient à un fait d'encombrement : l'étalon à jet de césium fait 425 mm de large, et toute horloge en
  baie 19 pouces exige L ≥ 1,55 m (script i02).
- **À faire.** Recenser, fiches techniques à l'appui, les horloges compactes de 2026 hors format baie : étalons à
  césium à pompage optique, horloges à atomes froids compactes, horloges optiques à iode ou à rubidium à deux
  photons, horloges à ions piégés miniatures. Relever : dimensions, masse, puissance, variance d'Allan à 10⁴–10⁵ s,
  sensibilités à la pression, à la température, au champ magnétique et à l'accélération.
- **Acquis.** Horloge optique à iode de 35 L : moins de 300 ps par jour en mer [Roslund24] (résumé vérifié) ;
  format, masse et disponibilité commerciale **non vérifiés**.
- **Ce qui changerait.** Une horloge de moins de 20 L, de moins de 23 cm de profondeur et tenant 10⁻¹³ sur deux
  jours ferait passer R1-A de « calcule » à « mesure » ; l'indice de proximité de R1 passerait de 76 à 78.

### C2. Jusqu'où descend un ensemble de rubidiums miniatures en enceinte étanche, thermostatée et blindée ?

- **Pourquoi.** Nous avons *supposé* un gain d'un facteur 300 sur les effets d'environnement et un plancher de
  3 × 10⁻¹³ ([HYP], script i01) : S/B = 0,2 pour une horloge sur 48 h à +1 000 m, 0,6 à +3 000 m. Dans ce régime
  de scintillation le rapport ne s'améliore pas avec la durée ; huit horloges par site à +3 000 m donneraient au
  mieux S/B ≈ 1,8, si leurs erreurs étaient indépendantes — ce que rien ne garantit, pas plus que le plancher.
- **À faire.** Essai en étuve et en caisson à pression variable (−170 hPa, soit +1 500 m) de 4 à 8 modules ; mesure
  directe de la variance d'Allan sur 1 à 7 jours contre un maser ou un lien GNSS étalonné.
- **Lien.** Constat de l'Équipe F (fiche EXP-01) : un rubidium nu est 100 à 600 fois trop sensible.

### C3. Paramètres de bruit réels des horloges retenues

- Seuls « 3 × 10⁻¹⁰ à 1 s » (horloge miniature au césium) et « plancher ≤ 10⁻¹⁴ » (étalon haute performance)
  sont vérifiés (Équipe C). À mesurer ou à relire : plancher et vieillissement de l'horloge miniature ; bruit blanc
  de fréquence de l'étalon à jet (8,5 × 10⁻¹²/√τ, valeur de l'Équipe F) ; comportement en véhicule (vibrations,
  inclinaison, cycles thermiques). Le S/B de 3,4 du §3.3 dépend linéairement de ces valeurs.

### C4. Échelle et identité du coffre

- L = 0,85 ± 0,20 m (Équipe A, confiance faible). Entre les deux jeux de rapports de forme (Équipes A et E), la
  hauteur fermée varie de 0,242 à 0,285 m : c'est ce qui décide si le gravimètre de classe microgal se range dans
  le coffre. L'identification du modèle de coffre de transport (piste de l'Équipe A, §8 de son dossier) fixerait
  d'un coup L, la profondeur et la hauteur.

---

## Partie 2 — Recherches de conception du palier 1 (priorité B)

| N° | Question | Pourquoi | Méthode proposée | Élément acquis |
|---|---|---|---|---|
| C5 | Quel rapport de taux de muons attendre entre deux altitudes pour *cette* géométrie ? | le §3.4 donne un ordre de grandeur (1,3 à 2 pour 2 000 m) et une borne, pas une prédiction | calcul de transport (spectre au sol, pertes d'énergie, production dans l'atmosphère) ; relire le chapitre « rayons cosmiques » du *Review of Particle Physics* [PDG24] ; corriger des effets barométrique et thermique et de l'écran du toit | intensité verticale et énergie moyenne citées de mémoire ; facteur 8,8 ± 0,8 de Frisch & Smith (résumé vérifié) |
| C6 | Quelles performances réelles pour un gyromètre à fibre didactique, ou quel modèle du commerce loge sous une ouverture de 81 mm ? | la limite de grenaille calculée (0,0008 °/√h) est un plafond théorique | maquette de table ; mesure de la dérive thermique de la bobine et de la rétrodiffusion ; relevé de fiches techniques | principe : [Lefèvre 2014], Équipe F (EXP-09) |
| C7 | Peut-on tester l'effet du cap (est contre ouest) sur un trajet à sens unique, et remplacer par un lien de temps les trois étalons de référence de l'essai T6 ? | l'aller-retour annule l'effet du cap ; la référence au sol coûte ≈ 240 k€ ; il faut un transfert de temps à mieux que 1 ns, dont nous n'avons qu'estimé le bruit (0,2 à 1 ns) | transfert par GNSS en vue commune ou en phase de porteuse avec récepteurs étalonnés ; bilan d'incertitude | signal : 3,66 ps par km vers l'est (script i01) ; Équipe F (EXP-02) |
| C8 | Tenue des étalons à jet de césium en véhicule | la configuration R1-B en dépend | retour d'expérience de « Project GREAT » (page relue par l'Équipe F) ; essai sur route avec trois étalons | 22 ns prédits, ≈ 23 observés |
| C9 | Thermique en habitacle fermé au soleil ; sécurité et réglementation du transport de batteries au lithium | le bilan du §3.7 suppose 20 °C et la convection libre | essai en enceinte à 40–50 °C ; consultation des règles de transport (de mémoire : essais ONU 38.3) | +8,9 K calculés |
| C10 | Faut-il quatre calculateurs ? | trois unités ne tolèrent pas une panne byzantine sans messages signés [LSP82] | analyse de sûreté de fonctionnement du voteur ; diversité logicielle | Équipe C (fiche F7) |
| C11 | Les accéléromètres à quartz tiennent-ils 1 mGal comme gravimètre relatif ? | valeur de classe, non vérifiée | étalonnage sur ligne de pesanteur connue ; dérive thermique | 1 µGal ↔ 3,2 mm : la prédiction à 1 % n'exige que ~1 % sur g |
| C12 | Devis réels | tous les coûts sont des estimations | consultation de fournisseurs | `nomenclature_R1.csv` |

---

## Partie 3 — Recherches propres au palier 2 (priorité B)

### C13. La cuve à deux vortex a-t-elle déjà été étudiée ?

- **Pourquoi.** Nous affirmons « à notre connaissance, aucune expérience publiée ne porte sur deux vortex de
  vidange en interaction » : c'est une absence de résultat dans nos lectures, **pas** une recherche bibliographique
  exhaustive (rejoint la question Q9 de l'Équipe H).
- **À faire.** Recherche ciblée (arXiv, INSPIRE) sur la diffusion d'ondes de surface par deux vortex, les modes
  piégés entre deux ergorégions analogues et l'instabilité de type « bombe à trou noir » en hydrodynamique ; puis
  calcul numérique (équations de Saint-Venant linéarisées autour de deux puits tourbillonnaires) pour fixer
  l'entraxe, le débit et la bande de fréquences avant de construire quoi que ce soit.
- **Acquis.** Un vortex : amplification jusqu'à 20 % à 3,70 Hz [Torres17] (résumé) ; signatures d'espace-temps en
  rotation dans l'hélium superfluide [Svancara24].

### C14. Disponibilité réelle des horloges optiques transportables

- Incertitudes de 7 × 10⁻¹⁷ (transportable, titre de Koller et al. 2017) à 10⁻¹⁹ (laboratoire) ; taux de
  fonctionnement, autonomie, masse et coût d'un exemplaire transportable en 2026 : **non vérifiés** (toutes les
  lignes M1 de `nomenclature_R2.csv` sont des estimations).

### C15. Budget d'incertitude du test « horloges contre géodésie »

- Pour comparer à 10⁻¹⁸ il faut connaître la différence de potentiel de pesanteur à 0,1 m²/s² près (1 cm) :
  nivellement, gravimétrie le long du trajet, marées terrestres, charge océanique. Les campagnes publiées
  [Grotti18], [Takamoto20] donnent la méthode ; le budget pour le site choisi reste à établir.

### C16. Valeur ajoutée du banc de causalité quantique

- Reproduire des résultats publiés ([Lloyd11a], [Ringbauer14], [Procopio15]) n'apprend rien de neuf. À définir :
  une expérience originale (par exemple simulation à post-sélection d'un circuit à plusieurs qubits, cf.
  [Huang26]) et, surtout, un protocole de présentation qui interdise toute lecture « voyage dans le temps ».

---

## Partie 4 — Palier 3 : points à instruire (priorité C)

| N° | Question | Renvoi |
|---|---|---|
| C17 | Quelle fraction η de la puissance de Hawking peut réellement être convertie en poussée dirigée (absorbeur, guidage magnétique des e±) ? Nous avons pris η ≤ 0,44 comme plafond. | relire le texte intégral de [CW09] et la littérature postérieure ; Équipe C (fiche F4) |
| C18 | Quel spin maximal pour un trou noir réel, et donc quel Γ à la dernière orbite stable ? Nous avons pris a/M = 0,998 (de mémoire). | [Thorne74], [Reynolds21] dans la bibliographie de l'Équipe H |
| C19 | L'énoncé « on ne remonte jamais avant la mise en service de la machine » est-il démontré en toute généralité ? | relire [MTY88], [Visser02] ; Équipe B (§6.2) |
| C20 | Borne inférieure rigoureuse sur l'énergie négative d'un trou de ver traversable macroscopique | [VKD03], [FR96] ; question Q6 de l'Équipe H |
| C21 | Existence de trous noirs en évaporation ; protection chronologique ; linéarité quantique | questions Q1, Q5, Q8 de l'Équipe H (non reprises ici) |

---

## Partie 5 — Vérifications que l'Équipe I n'a pas pu faire

1. Lecture du **texte intégral** des articles : seuls les notices et les résumés ont été relus (39 notices).
2. Valeurs citées de mémoire : intensité et énergie moyenne des muons au sol ; impulsion et champ de l'anneau à
   muons ; limite de spin 0,998 ; masse et distance de Sgr A* ; seuil de très basse tension de sécurité ;
   paramètres typiques d'une naine blanche et d'une étoile à neutrons ; détail du protocole de [Ringbauer14].
3. Fiches techniques des composants du palier 1 autres que ceux relus par l'Équipe C (batterie, accéléromètres,
   gyromètre, comparateur de phase, récepteur GNSS, coffre).
4. Recherche bibliographique exhaustive sur les analogues à deux vortex (C13) et sur les horloges compactes (C1).
5. Aucun essai matériel : ni horloge, ni télescope à muons, ni gyromètre n'ont été montés.
6. Visionneuse interactive du modèle 3D du palier 1 : non produite (le fichier `modele_c204_R1.json` est au
   format de l'Équipe E et devrait s'ouvrir dans son outil, ce que nous n'avons pas testé).

---

## Partie 6 — Demandes aux autres équipes

| Destinataire | Demande | Pourquoi |
|---|---|---|
| Équipe A | identifier le coffre ; dater la première diffusion de DOC-014 | fixe l'échelle (C4) ; les cotes de 5 à 11 m ont servi d'exemples au §4.1 et au §5.4 |
| Équipe C | relire les fiches techniques manquantes (C1, C3) ; valider le bilan thermique | les verdicts d'encombrement reposent sur une seule fiche |
| Équipe E | charger `modele_c204_R1.json` dans la visionneuse ; signaler toute incompatibilité de format | point 6 ci-dessus |
| Équipe F | intégrer les essais T3 (muons selon l'altitude) et T6 (séjour en altitude avec étalons) aux fiches EXP-01 et EXP-11 ; confirmer les paramètres de bruit | cohérence des protocoles |
| Équipe G | rejouer la grille de proximité avec d'autres poids ; attaquer le choix des deux démonstrateurs | notes subjectives (§6 et §3.4 du rapport) |
| Équipe H | vérifier par API les fiches des horloges compactes de 2025-2026 (C1, C14) | veille |

---

## Synthèse des priorités

| Priorité | Recherche | Conclusion du rapport I susceptible de changer |
|---|---|---|
| A | C1 horloge compacte hors format baie | « le coffre seul ne mesure pas son déplacement » |
| A | C2 rubidiums en enceinte | idem, par une autre voie |
| A | C3 bruit réel des horloges | S/B de la configuration R1-B (3,4 par horloge) |
| A | C4 échelle du coffre | rangement du gravimètre ; autonomie |
| B | C5 à C16 | dimensionnement, coûts, protocoles |
| C | C17 à C21 | chiffres du palier 3, sans effet sur les paliers 1 et 2 |

Aucune de ces recherches n'ouvre de voie vers un déplacement temporel rétrograde : elles portent sur la mesure
d'un effet connu, propre au trajet et non à la machine, de l'ordre de la nanoseconde par heure : jamais vers le passé ;
selon le trajet, l'unité vieillit un peu moins ou un peu plus que la référence.

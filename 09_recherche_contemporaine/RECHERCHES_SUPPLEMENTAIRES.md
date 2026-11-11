# Recherches supplémentaires nécessaires — livrable n° 13 du programme C204

Équipe H — version 1.1 du 10 novembre 2026 (alignée sur les corrections de la validation contradictoire, voir
`RAPPORT_H.md` §18). Complète `RAPPORT_H.md` (§14).

> Objet : recenser les **questions réellement ouvertes** dont la réponse pourrait modifier — dans un sens ou dans
> l'autre — les verdicts portés sur les hypothèses de la C204, ainsi que les **expériences en cours ou
> planifiées** qui les instruisent. Rien ici ne présuppose que la C204 existe ou puisse exister.
>
> Conventions : les clés entre crochets renvoient à `bibliographie_verifiee.csv` (références vérifiées par API).
> Les programmes expérimentaux cités sans clé sont suivis de **(vérifié)** quand une page ou un article a été
> consulté dans cette session, ou de **(de mémoire)** dans le cas contraire : ces derniers sont à contrôler avant
> toute reprise dans le dossier final.

Échelle de priorité : **A** = pourrait renverser un verdict du rapport ; **B** = préciserait un verdict ;
**C** = intérêt documentaire ou pédagogique pour le programme.

---

## Partie 1 — Questions ouvertes de physique

### Q1. Existe-t-il, dans la nature, des trous noirs en cours d'évaporation ? (priorité A)

- **Pourquoi c'est décisif.** Toute la C204 repose sur des « micro-singularités » rayonnant quelques centaines de
  mégawatts. Le rayonnement de Hawking d'un trou noir gravitationnel n'a jamais été observé ; aucun trou noir
  primordial n'a jamais été détecté. Une détection confirmerait à la fois l'existence de tels objets et la loi
  d'émission ; elle ne dirait rien de leur capture ni d'un usage temporel.
- **État 2026.** Limites sur le taux local d'explosions : < 7,2×10³ [Fermi18], < 3 400 [HAWC20], < 2 000 [HESS23],
  < 181 pc⁻³·an⁻¹ [PBH2505]. Contraintes d'abondance : [CKSY21], [Auffinger23]. Interprétations spéculatives d'un
  neutrino de très haute énergie [KM3NeT25] : [Baker25], [PBH2505b], [PBH2605].
- **En cours ou planifié.** Poursuite de LHAASO et HAWC (vérifié par les articles) ; prospective LHAASO
  [LHAASOsens24] ; observatoire Cherenkov CTAO et projet SWGO dans l'hémisphère sud (de mémoire) ; télescopes
  gamma au MeV de nouvelle génération, dont l'intérêt pour l'évaporation directe est argumenté dans [Coogan21] ;
  télescopes à neutrinos KM3NeT et IceCube (de mémoire pour les extensions).
- **Lacune à combler par le programme.** Extraire des revues [CKSY21], [GK21] la borne chiffrée sur la fraction de
  matière noire entre 10¹⁵ et 10¹⁶ g (la gamme des « 300–500 MW »), que je n'ai pas lue dans les figures.
- **Ce qui changerait le verdict.** Une détection ferait passer le statut du rayonnement de Hawking de
  « théoriquement possible » à « démontré », sans rendre fabricable ni transportable un objet de 10¹² kg.

### Q2. L'échelle fondamentale de la gravité est-elle abaissée par des dimensions supplémentaires ? (priorité A)

- **Pourquoi.** C'est la seule voie théorique connue vers des trous noirs en accélérateur [ADD98], [RS99].
- **État 2026.** Aucune production au LHC : [CMS26], [ATLASQBH26] ; loi en 1/r² vérifiée jusqu'à 52 µm [Lee20],
  [Tan20].
- **En cours ou planifié.** LHC à haute luminosité à partir de 2030 environ (vérifié : calendrier CERN) ; décision
  sur le FCC-ee attendue d'ici 2028 (vérifié : communiqué du Conseil du CERN du 22 mai 2026) ; un collisionneur de
  hadrons à ~100 TeV n'est qu'une étape ultérieure envisagée (de mémoire) ; tests de la gravité sous 50 µm par
  balances de torsion et masses lévitées [Fuchs24g], [Panda24].
- **Ce qui changerait le verdict.** Même une découverte ne produirait que des objets de ~10⁻²³ kg vivant
  ~10⁻²⁶ s : le verdict « invalide » sur l'origine des singularités de la C204 ne changerait pas, mais
  l'affirmation « des trous noirs peuvent être créés en accélérateur » deviendrait vraie au sens strict.

### Q3. Que devient l'horizon interne d'un trou noir en rotation ? (priorité A)

- **Pourquoi.** Le « passage à travers l'anneau » suppose que l'intérieur analytique de Kerr existe.
- **État 2026.** Démontré : stabilité C⁰ de l'horizon de Cauchy de Kerr (prolongement à métrique continue), ce
  qui n'implique ni prolongement régulier ni prolongement unique ; suggéré par la preuve, non démontré :
  singularité nulle faible générique [DL17] ; inflation de masse
  [PI90], [Dafermos03] ; choc gravitationnel [MO12] ; flux quantiques divergents [Zilberman22], [HWZ20] ;
  instabilité des cœurs réguliers [CR21].
- **Questions ouvertes.** (i) Singularité finale générique : entièrement nulle et « faible », ou partiellement
  de genre espace ? (ii) Évolution semi-classique auto-cohérente, rétroaction comprise, près de l'horizon
  interne. (iii) Sort d'un observateur franchissant une singularité faible. (iv) Portée de l'objection de Kerr
  [Kerr23] et des modèles réguliers [Bueno24], [CR25].
- **En cours.** Suite annoncée du programme de Dafermos et Luk (résumé de [DL17]) ; relativité numérique des
  intérieurs [BKZ16] ; calculs de tenseur énergie-impulsion renormalisé dans Kerr.
- **Ce qui changerait le verdict.** Le verdict actuel est « non établi, défavorisé » (confiance moyenne). Il
  deviendrait « invalide » si la singularité nulle faible générique était démontrée infranchissable, et
  « théoriquement possible » si un prolongement régulier et déterministe était établi pour des données génériques.
  Aucun résultat actuel ne va dans ce second sens.

### Q4. Stabilité de Kerr et censure cosmique dans toute leur généralité (priorité B)

- **État 2026.** Stabilité non linéaire prouvée pour les rotations lentes [KS21], [GKS22] ; ondes linéaires sur
  tout le domaine sous-extrémal [DRS14] ; trous extrémaux formés en temps fini [KU22], comme seuil critique
  [KU24] ; instabilités d'horizon extrémal [Aretakis12].
- **Questions ouvertes.** Stabilité non linéaire pour |a| quelconque inférieur à M ; formation d'un trou de Kerr
  extrémal dans le vide ; censure cosmique forte sans symétrie ; rôle de la constante cosmologique [Cardoso18].
- **Lien avec la C204.** Les leviers « charge » et « rotation » supposent des trous proches de l'extrémalité, le
  régime précisément le moins compris et le plus instable.

### Q5. La protection chronologique est-elle un théorème ? (priorité A)

- **État 2026.** Conjecture [Hawking92] ; théorie des champs mal définie à l'horizon chronologique [KRW97] ;
  indices holographiques [CKS05], [ET21] ; pas de preuve générale, et pas d'impossibilité démontrée
  classiquement [Krasnikov02].
- **Questions ouvertes.** Preuve dans un cadre de gravité quantique ; généralisation de [ET21] au-delà des
  théories conformes à deux dimensions ; statut des solutions sans matière exotique à horizon non compact
  [Ori05], [Ori07].
- **Ce qui changerait le verdict.** Un contre-exemple physiquement réalisable (source finie, conditions d'énergie
  respectées, absence de singularité). Les théorèmes existants [Tipler76], [Tipler77], [Hawking92] l'excluent sous leurs
  hypothèses.

### Q6. Jusqu'où tiennent les conditions d'énergie moyennées ? (priorité A)

- **État 2026.** ANEC démontrée en espace plat [FLPW16], [HKT17] ; version achronale [GO07], [Wall10] ; condition
  quantique [BFKLW16] ; inégalités quantiques [Fewster12], [KS20] ; condition lissée conjecturée [FK18].
- **Questions ouvertes.** Champs en interaction en espace courbe quelconque ; cohérence semi-classique complète ;
  preuve de la focalisation quantique [BFLW16] ; existence et production des trous de ver de [MMP18] dans le
  modèle standard ; métriques de distorsion subluminiques respectant les conditions d'énergie [Fuchs24w] :
  peut-on les accélérer ?
- **Expériences.** Mesure directe d'une densité d'énergie négative locale et de son effet gravitationnel : hors de
  portée. Étapes réalistes : pesée de l'énergie du vide (projet Archimedes) [Calloni14] ; métrologie des états
  comprimés [Vahlbruch16], [Riek17] ; géométries de Casimir [Zhao19].
- **Ce qui changerait le verdict.** Une violation macroscopique et durable de l'ANEC sur une géodésique nulle
  achronale. Rien ne l'indique.

### Q7. La gravité peut-elle intriquer deux masses ? (priorité B)

- **Pourquoi.** La C204 présuppose une physique « unifiée » ; le premier fait expérimental sur le caractère
  quantique de la gravité reste à obtenir.
- **État 2026.** Propositions [Bose17], [MV17] ; gravité mesurée pour 90 mg [Westphal21] puis 0,4 mg [Fuchs24g] ;
  états quantiques de 16 µg [Bild23] ; revue [Bose25]. Controverse sur l'interprétation d'un résultat positif :
  [AzizHowl25] contre [MV25], [Diosi25] ; voir aussi [Ludescher25], [Plavala25]. Aucune observation d'intrication
  gravitationnelle à ce jour (recherche web du 10 novembre 2026).
- **En cours ou planifié.** Interférométrie de nanodiamants à spin, masses lévitées refroidies [Delic20],
  compression d'impulsion de miroirs (proposition publiée en 2026, vue par recherche web, non vérifiée par API) ;
  tests du compromis décohérence-diffusion des théories à gravité classique [OSSW23].
- **Ce qui changerait le verdict.** Rien pour la C204 à court terme ; mais un résultat net orienterait le choix
  entre approches (§7 du rapport).

### Q8. La mécanique quantique est-elle exactement linéaire ? (priorité B)

- **Pourquoi.** « Changer de ligne d'univers » au sens d'Everett revient à faire interagir des branches, ce qui
  exige une non-linéarité [Polchinski91].
- **État 2026.** Tests nuls [Bollinger89], [Polkovnikov23], [Broz23] du cadre [KR22].
- **À faire.** Suivre l'amélioration des bornes ; faire préciser par l'Équipe B que la « divergence en pour cent »
  du récit n'a aucune traduction dans ce cadre.

### Q9. Jusqu'où pousser les analogues de Kerr et de Hawking ? (priorité B — utile aux phases 5 et 6)

- **État 2026.** Émission spontanée dans un condensat [Steinhauer16], [MdN19], [Kolobov21] ; superradiance
  [Torres17] ; vortex quantique géant [Svancara24] ; rétroaction en optique [HawkingBack26] ; stimulation par
  photon unique [HawkingSingle26] ; polaritons [Falque].
- **Questions ouvertes.** Reproduction indépendante de l'émission spontanée hors des condensats ; intrication des
  paires dans d'autres plateformes ; instabilités de type « bombe à trou noir » ; analogue de **deux** vortex en
  interaction (le plus proche d'un « double Kerr » simulé).
- **Intérêt pour le programme.** C'est la seule façon sûre et accessible de « voir » un champ de Kerr effectif
  (piste 2 du rapport) ; à étiqueter *simulation analogique*.

### Q10. Métrologie : horloges nucléaires, redéfinition de la seconde, géodésie chronométrique (priorité B)

- **État 2026.** Horloges optiques à 10⁻¹⁹ [Lu26], [Ca26], [Marshall25], [Aeppli24] ; première horloge nucléaire
  asservie [Th26b] ; feuille de route [Dimarcq24].
- **En cours ou planifié.** Choix de l'espèce atomique et adoption d'une nouvelle définition visée pour 2030
  (vérifié : résolution 5 de la CGPM de 2022 ; issue de la CGPM de 2026 **non vérifiée**) ; exploitation d'ACES
  sur la Station spatiale [ACES24] (lancement d'avril 2025 vu par recherche web) ; horloges optiques
  transportables et réseaux fibrés [Lisdat16], [Grotti18].
- **Intérêt pour le programme.** Ces instruments fixent la sensibilité avec laquelle on pourrait **réfuter** toute
  prétendue « distorsion de gravité » : 10⁻¹⁸ correspond à 1 cm de dénivelé terrestre.

### Q11. Gravimétrie et navigation par la gravité (priorité C)

- **État 2026.** [Menoret18], [Bidel20], [Stray22], [Templier22], [QCTRL26].
- **En cours ou planifié.** Mission pionnière d'interférométrie atomique en orbite [CARIOQA] ; gradiomètre
  quantique spatial annoncé pour 2030 (vu par recherche web, non vérifié par API) ; désaccords persistants sur
  la constante G [RS17], [Li18].
- **Intérêt.** Borne réaliste de ce qu'un système « VGL » pourrait faire : corrélation à une carte, exactitude
  kilométrique.

### Q12. Tests de la géométrie de Kerr par l'observation (priorité C)

- **État 2026.** [GW250114LVK], [GW250114spec], [GWTC4cat], [EHTSgrA6], [GRAVITY20], [Ciufolini19].
- **En cours ou planifié (de mémoire).** Montée en sensibilité des détecteurs terrestres, détecteurs de troisième
  génération (Einstein Telescope, Cosmic Explorer), mission spatiale LISA, extensions de l'EHT, mesure de
  l'entraînement des référentiels autour de Sgr A* par les étoiles proches, satellite LARES 2.
- **Intérêt.** Chaque confirmation de Kerr **à l'extérieur** renforce indirectement le verdict sur l'intérieur,
  qui découle des mêmes équations.

---

## Partie 2 — Recherches documentaires à mener par les autres équipes

| # | Recherche | Destinataire | Pourquoi | Élément déjà acquis |
|---|---|---|---|---|
| D1 | Localiser dans le corpus archivé la phrase sur une « percée au CERN d'ici un an ou deux » et la dater | Équipe A | le verdict n° 2 du rapport repose sur l'énoncé de mission | chronologie réelle établie (§1.1 du rapport) |
| D2 | Comparer les dates des messages avec la diffusion de l'idée de trous noirs en accélérateur | Équipes A, G | l'idée existait en 1998-2000 [ADM98], [BF99], [BJSW00] ; les articles célèbres [GT01], [DL01] sont de juin 2001 | références vérifiées |
| D3 | Lire le texte intégral de [Tipler74] pour vérifier l'hypothèse sur l'origine du mot « sinusoïde » (fonctions métriques oscillantes du régime à courbes temporelles fermées) | Équipe B | hypothèse [HYP] du §3.4 | texte de [Prezens10] lu |
| D4 | Établir le statut de [Prezens10] (auteur, citations éventuelles, reprise sur les forums) | Équipes A, G | seule trace du vocabulaire dans la littérature indexée ; classée [INT] | 1 résultat INSPIRE, 0 publication en revue |
| D5 | Vérifier sur pièces la documentation d'époque du 5100 (manuel de maintenance de 1979, article de 1983) | Équipe A | [Friedl83] reste « non vérifiée » ; nuance System/360 ou System/370 | numérisation du manuel repérée (non ouverte) |
| D6 | Rechercher l'origine de l'association « montagne / taille d'une particule / rayons X et gamma » dans la vulgarisation des années 1970-1990 | Équipes A, G | [HYP] le vocabulaire du récit rappelle la vulgarisation sur les trous noirs primordiaux ; **non vérifié** | articles d'origine [Hawking71], [Hawking74], [CarrHawking74] vérifiés |
| D7 | Recalculer les spectres d'émission avec un code public | Équipe D | remplacer la formule de corps noir | [BlackHawk], [Page76a], [Page77] ([MW90] seulement au-dessus de ~20 MeV de température) |
| D8 | Reprendre l'argument de charge (valeur quadratique moyenne ≈ 6 e, borne ~137 e, errata E14) et de ralentissement de rotation dans le dossier d'ingénierie | Équipes B, C | ferme les leviers « charge » et « rotation » | [Page77], [Gibbons75], [Page76b], [TCH98] |

---

## Partie 3 — Vérifications que l'Équipe H n'a pas pu faire

1. Lecture du **texte intégral** des articles : seuls les résumés ont été contrôlés (une exception : [Prezens10]).
2. Bornes chiffrées d'abondance des trous noirs primordiaux par gamme de masse (figures des revues).
3. Issue de la 28ᵉ CGPM (2026) sur la redéfinition de la seconde.
4. Résultats publiés d'ACES ; état d'avancement réel du long arrêt LS3 du LHC en novembre 2026.
5. Caractéristiques de la Z machine (énergie stockée, courant) : citées de mémoire.
6. Existence d'éventuelles anomalies gravimétriques ou sismiques locales aux dates et lieux du récit : non
   recherchée (et de toute façon non concluante en cas d'absence).
7. Veille 2026 : fondée sur une douzaine de recherches web ciblées ; elle n'est pas exhaustive.

---

## Partie 4 — Synthèse des priorités

| Priorité | Question | Verdict du rapport susceptible d'évoluer | Probabilité estimée d'évolution d'ici 2035 |
|---|---|---|---|
| A | Q1 Trous noirs en évaporation | statut du rayonnement de Hawking | faible à moyenne |
| A | Q2 Dimensions supplémentaires | « aucun trou noir en accélérateur » | faible |
| A | Q3 Horizon interne de Kerr | « passage par l'intérieur : non établi, défavorisé » | faible (dans un sens ou dans l'autre) |
| A | Q5 Protection chronologique | « aucune machine compacte » | très faible |
| A | Q6 Conditions d'énergie moyennées | « pas d'énergie négative macroscopique » | très faible |
| B | Q4, Q7, Q8, Q9, Q10 | précisions sans renversement | — |
| C | Q11, Q12 | aucune | — |

Les probabilités sont des appréciations de l'Équipe H ([HYP], confiance faible) : elles traduisent le fait que les
résultats de 2001-2026 ont tous **resserré** les contraintes et qu'aucun n'a ouvert de voie vers un déplacement
temporel rétrograde.

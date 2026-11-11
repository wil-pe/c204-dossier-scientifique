# Ce que le dépôt en ligne ne contient pas

Le dossier de travail local contient des contenus de tiers qui ne sont **pas** redistribués dans le dépôt :

| Élément | Raison | Comment le retrouver |
|---|---|---|
| `copies_alternatives/` — 225 fichiers (images, un PDF) téléchargés depuis des sites archivés | Contenus de tiers | `journal_provenance.csv` donne pour chacun l'URL exacte, la date de capture et l'empreinte SHA-256 |
| `sources_web/` — pages web archivées, messages de forums, texte intégral de la compilation de départ | Textes de tiers, pseudonymes d'internautes | Adresses dans `HISTORIQUE.md` et `journal_provenance.csv` |
| Pièce C204-DOC-016 et les planches qui la montrent | Lettre administrative contenant des données nominatives de tiers | Non rediffusée |

Conséquence : quatre scripts relisent ces fichiers et ne se relancent qu'après les avoir re-téléchargés :
`01_archive/scripts/comparer_copies.py`, `05_simulations/S08_reconstitution_doc009/s08_reconstitution_doc009.py`
(partie « meilleures copies »), `08_red_team/calculs/corpus_recherche.py` et
`08_red_team/calculs2/06_mesure_doc014.py`. Leurs sorties, elles, sont dans le dépôt. Les douze
pièces de la source de départ (`originaux/`) et leurs agrandissements (`ameliores/`) sont inclus, car ce sont les
objets mêmes de l'étude ; leurs empreintes sont dans `inventaire.csv`.

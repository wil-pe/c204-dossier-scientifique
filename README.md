# Programme C204 — dossier de recherche

Étude scientifique critique de la « machine temporelle C204 » attribuée à John Titor (messages Internet de
2000-2001). Rien de ce qu'affirment les documents d'origine n'est tenu pour vrai : ce sont des pièces à analyser.

## Par où commencer

| Pour… | Ouvrir |
|---|---|
| Lire la synthèse et les réponses aux dix questions | [11_dossier_final/DOSSIER_SCIENTIFIQUE_C204.md](11_dossier_final/DOSSIER_SCIENTIFIQUE_C204.md) |
| Voir la machine en 3D : vue éclatée, « si elle fonctionnait », ce que dit la physique | [06_modele_3D/simulateur.html](06_modele_3D/simulateur.html) (à ouvrir dans un navigateur ; charge three.js en ligne) |
| Inspecter le modèle pièce par pièce | [06_modele_3D/visionneuse.html](06_modele_3D/visionneuse.html) |
| Ouvrir la page d'accueil du site | [docs/index.html](docs/index.html) |
| Consulter les documents sources | [01_archive/INVENTAIRE.md](01_archive/INVENTAIRE.md) |
| Lire la critique de notre propre travail | [08_red_team/RAPPORT_RED_TEAM_2.md](08_red_team/RAPPORT_RED_TEAM_2.md) |
| Voir la machine optimisée | [10_machine_optimisee/RAPPORT_I.md](10_machine_optimisee/RAPPORT_I.md) |
| Construire ce qui peut l'être | [10_machine_optimisee/GUIDE_CONSTRUCTION.md](10_machine_optimisee/GUIDE_CONSTRUCTION.md) |
| Trouver un fichier | [11_dossier_final/INDEX_DES_FICHIERS.md](11_dossier_final/INDEX_DES_FICHIERS.md) |

## Arborescence

```
C204/
├── 00_DOSSIER_DE_BASE.md          référence commune, conventions, errata E1–E16
├── 01_archive/                    originaux (lecture seule), copies alternatives, inventaire, historique
├── 02_reconstruction/             dossier technique, plans 2D, dimensions, incohérences
├── 03_physique_theorique/         relativité générale, trous noirs, causalité
├── 04_ingenierie/                 sous-systèmes, bilans, faisabilité
├── 05_simulations/                neuf simulations (S01 à S09)
├── 06_modele_3D/                  modèle paramétrique, exports GLB/OBJ/STL, visionneuse
├── 07_experiences/                douze protocoles expérimentaux
├── 08_red_team/                   deux rapports critiques, corrections, audits
├── 09_recherche_contemporaine/    littérature 2001–2026, bibliographie vérifiée
├── 10_machine_optimisee/          trois paliers de machine cohérente
├── 11_dossier_final/              synthèse et index
└── docs/                          site statique (page d'accueil, simulateur, visionneuse)
```

## Tout relancer

Python : `.venv/bin/python` (Python 3.12 ; numpy, scipy, matplotlib, sympy, opencv, trimesh, shapely).

| Calculs | Commande, depuis `C204/` |
|---|---|
| Vérifications de physique théorique | `.venv/bin/python 03_physique_theorique/verifications/executer_tout.py` |
| Simulations | `sh 05_simulations/run_all.sh` |
| Modèle 3D, rendus, visionneuse | `sh 06_modele_3D/reconstruire.sh` |
| Machine optimisée | `sh 10_machine_optimisee/calculs/run_all.sh` |
| Tests du logiciel de référence | `cd 10_machine_optimisee/logiciel && ../../.venv/bin/python -m unittest discover -s tests` |
| Site statique `docs/` | `.venv/bin/python 11_dossier_final/construire_site.py <URL du dépôt>` |
| Index et contrôle des liens | `.venv/bin/python 11_dossier_final/generer_index.py` |

Les scripts d'ingénierie (`04_ingenierie/calculs/`) et d'expériences (`07_experiences/calculs/`) se lancent un par un.

## Conventions

- Niveau de preuve : [DOC] documenté, [DÉD] déduit, [HYP] hypothétique, [INT] interprétation de tiers, [VÉR] vérifiable.
- Statut physique : démontré, théoriquement possible, spéculatif, contredit.
- Les originaux de `01_archive/originaux/` ne sont jamais modifiés ; leurs empreintes sont dans `01_archive/inventaire.csv`.
- La pièce C204-DOC-016 contient des données nominatives de tiers : elle n'est pas dans le dépôt.
- Les contenus de tiers bruts (copies d'images, pages web, messages de forums) ne sont pas dans le dépôt :
  voir [01_archive/NON_INCLUS_DANS_LE_DEPOT.md](01_archive/NON_INCLUS_DANS_LE_DEPOT.md).
- Pour recréer l'environnement : `uv venv --python 3.12 .venv` puis
  `uv pip install --python .venv/bin/python numpy scipy matplotlib sympy pillow opencv-python-headless trimesh shapely scikit-image`.

## Limites à garder en tête

Aucune expérience n'a été réalisée et rien n'a été construit. Les simulations sont illustratives. Les références
ont été vérifiées en ligne sur leurs métadonnées et leurs résumés, pas sur leur texte intégral. Toutes les
dimensions absolues du coffre reposent sur des étalons supposés.

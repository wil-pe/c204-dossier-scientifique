#!/bin/sh
# Équipe I — régénère tous les calculs, tableaux, figures, schémas, le modèle 3D du palier 1 et les données du guide (≈ 1 min).
# Usage : sh run_all.sh        (depuis 10_machine_optimisee/calculs/)
set -e
PY="$(cd "$(dirname "$0")/../.." && pwd)/.venv/bin/python"
cd "$(dirname "$0")"
for s in i01_deplacement_temporel.py i02_nomenclature_bilans_R1.py i03_demonstrateurs_logements.py i04_palier2_performances.py \
         i05_palier3_limites.py i08_nomenclature_R2.py i07_correspondance_proximite.py i06_figures.py i09_schemas_svg.py i10_modele_R1.py i11_guide_replique.py i12_guide_lite_cablage.py ; do
  echo "=== $s"
  $PY "$s" > "resultats/journal_${s%.py}.txt" 2>&1 || { echo "ÉCHEC : $s (voir resultats/journal_${s%.py}.txt)"; exit 1; }
done
echo "=== tests du logiciel de référence"
(cd ../logiciel && $PY -m unittest discover -s tests > ../calculs/resultats/journal_tests_logiciel.txt 2>&1) || { echo "ÉCHEC des tests du logiciel"; exit 1; }
tail -3 resultats/journal_tests_logiciel.txt
echo "Terminé."

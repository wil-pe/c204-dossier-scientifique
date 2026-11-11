#!/bin/sh
# Équipe E — Programme C204 — reconstruit TOUS les livrables à partir de parametres.json.
# Usage : ./reconstruire.sh            (ajouter --mesures pour relancer aussi la mesure des proportions)
set -e
ICI="$(cd "$(dirname "$0")" && pwd)"
PY="$ICI/../.venv/bin/python"
cd "$ICI"
if [ "$1" = "--mesures" ]; then
  "$PY" mesures/mesurer_proportions.py          # proportions relevées sur les documents (ne modifie pas parametres.json)
fi
"$PY" generer_modele.py                         # parametres.json  -> modele_c204.json (et réécrit les valeurs calculées)
"$PY" mesures/verifier_interferences.py || echo "ATTENTION : interférences entre pièces (voir ci-dessus) — revoir parametres.json"
"$PY" construire_modele.py                      # modele_c204.json -> exports/ (GLB, OBJ, STL) + rendus/ (PNG)
"$PY" generer_visionneuse.py                    # modele_c204.json -> visionneuse.html
"$PY" generer_simulateur.py                     # modele_c204.json + ../10_machine_optimisee/modele_c204_R1.json + simulateur_gabarit.html -> simulateur.html
"$PY" generer_nomenclature.py                   # modele_c204.json -> NOMENCLATURE.md, nomenclature.csv
"$PY" generer_schemas.py                        # -> architecture_fonctionnelle.svg, schema_electrique_hypothetique.svg
echo "Reconstruction terminée."

#!/usr/bin/env bash
# -----------------------------------------------------------------------------
# Programme C204 — Équipe D : relance TOUTES les simulations (S01 à S09).
#
# Usage (depuis n'importe où) :   bash 05_simulations/run_all.sh
#
# Les simulations sont ILLUSTRATIVES : elles ne constituent pas une preuve
# expérimentale. Durée totale : environ 3 à 4 minutes (dont ~1 min 45 s pour la
# vérification symbolique exacte des métriques de Kerr et Kerr-Newman dans S02, et
# ~50 s pour S08, qui traite trois copies du schéma DOC-009 / DOC-014).
#
# Décompte : seuls les TESTS DE VALIDATION (réponse connue indépendamment, échec
# possible) sont comptés ; les contrôles de l'ajustement sur lui-même, résultats,
# repères non vérifiés et biais de modèle sont consignés « hors décompte ».
# -----------------------------------------------------------------------------
set -u

DOSSIER="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RACINE="$(cd "$DOSSIER/.." && pwd)"
PYTHON="$RACINE/.venv/bin/python"
JOURNAL="$DOSSIER/journal_run_all.txt"

export MPLBACKEND=Agg
export PYTHONDONTWRITEBYTECODE=1

if [ ! -x "$PYTHON" ]; then
  echo "Interpréteur introuvable : $PYTHON" >&2
  exit 2
fi

SCRIPTS=(
  "S01_hawking/s01_hawking.py"
  "S02_kerr_geometrie/s02_kerr_geometrie.py"
  "S03_geodesiques_kerr/s03_geodesiques_kerr.py"
  "S04_cylindre_tipler/s04_cylindre_tipler.py"
  "S05_champ_faible_c204/s05_champ_faible_c204.py"
  "S06_confinement_em/s06_confinement_em.py"
  "S07_energie_negative/s07_energie_negative.py"
  "S08_reconstitution_doc009/s08_reconstitution_doc009.py"
  "S09_synthese/s09_synthese.py"
)

cd "$RACINE" || exit 2
: > "$JOURNAL"
echecs=0
for s in "${SCRIPTS[@]}"; do
  echo "=== $s ===" | tee -a "$JOURNAL"
  debut=$(date +%s)
  if "$PYTHON" "05_simulations/$s" >> "$JOURNAL" 2>&1; then
    fin=$(date +%s)
    grep -E "Bilan validation" "$JOURNAL" | tail -1
    echo "    terminé en $((fin - debut)) s"
  else
    echecs=$((echecs + 1))
    echo "    ÉCHEC D'EXÉCUTION (voir $JOURNAL)" | tee -a "$JOURNAL"
  fi
done

echo
echo "=== Récapitulatif ==="
n_tests_echoues=$(grep -c "\[ÉCHEC\]" "$JOURNAL" || true)
echo "Scripts en échec d'exécution : $echecs / ${#SCRIPTS[@]}"
echo "Tests de validation en échec : $n_tests_echoues"
grep -E "Bilan validation" "$JOURNAL"
"$PYTHON" - "$DOSSIER/resultats_globaux.json" <<'PYEOF'
import json, sys
try:
    t = json.load(open(sys.argv[1], encoding="utf-8"))["validation_totale"]
    print(f"TOTAL : {t['n_passes']}/{t['n_tests']} tests de validation passés ; {t['n_hors_decompte']} contrôles, résultats ou repères hors décompte {t['hors_decompte_par_categorie']}")
except Exception as exc:  # le récapitulatif ne doit jamais masquer un échec en amont
    print(f"TOTAL indisponible ({exc})")
PYEOF
echo "Journal complet : $JOURNAL"
echo "Synthèse machine-lisible : $DOSSIER/resultats_globaux.json"
echo "Rappel : simulations illustratives, non des preuves expérimentales."

if [ "$echecs" -ne 0 ] || [ "$n_tests_echoues" -ne 0 ]; then
  exit 1
fi
exit 0

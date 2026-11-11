#!/usr/bin/env bash
# Red Team n° 2 — Tâche 1 (reproductibilité).
# Principe : on NE relance PAS les scripts dans les dossiers des équipes ; on recopie les dossiers 02 à 07
# dans un répertoire de travail jetable (COPIE), on y relance tout, puis on compare aux sorties livrées.
# Les fichiers des équipes ne sont donc jamais modifiés.
# Usage : bash 00_reproduire.sh <repertoire_de_travail>
set -u
RACINE="$(cd "$(dirname "$0")/../.." && pwd)"
COPIE="${1:?répertoire de travail}"
JOURNAUX="$RACINE/08_red_team/calculs2/journaux"
mkdir -p "$COPIE" "$JOURNAUX"
for d in 02_reconstruction 03_physique_theorique 04_ingenierie 05_simulations 06_modele_3D 07_experiences; do
  rm -rf "$COPIE/$d"; cp -R "$RACINE/$d" "$COPIE/$d"
done
ln -sfn "$RACINE/.venv" "$COPIE/.venv"
ln -sfn "$RACINE/01_archive" "$COPIE/01_archive"
PY="$COPIE/.venv/bin/python"
export MPLBACKEND=Agg PYTHONDONTWRITEBYTECODE=1

# --- Équipe B
( cd "$COPIE/03_physique_theorique/verifications" && /usr/bin/time -p "$PY" executer_tout.py ) > "$JOURNAUX/B_executer_tout.log" 2>&1 &
# --- Équipe C
( cd "$COPIE/04_ingenierie/calculs" && for s in c00_constantes.py c01_hawking.py c02_confinement.py c03_injection_rotation.py c05_refroidissement_rayonnement.py c06_alimentation_bilan.py c07_capteurs_horloges.py c08_calculateurs_vote.py c09_structure_vehicule.py c10_Q4_energie_EM.py c11_schema_fonctionnel.py c12_tableaux.py; do echo "=== $s ==="; "$PY" "$s"; echo "--- code de retour $s : $?"; done ) > "$JOURNAUX/C_calculs.log" 2>&1 &
# --- Équipe D
( cd "$COPIE" && /usr/bin/time -p bash 05_simulations/run_all.sh; echo "--- code de retour run_all.sh : $?" ) > "$JOURNAUX/D_run_all.log" 2>&1 &
# --- Équipe F
( cd "$COPIE/07_experiences/calculs" && for s in calc01_dilatation_horloges.py calc02_transfert_temps.py calc03_cavendish_champ_EM.py calc04_gravimetrie_VGL.py calc05_casimir.py calc06_gravite_analogue.py calc07_piege_paul_levitation.py calc08_deviation_lumiere.py calc09_sagnac_lense_thirring.py calc10_optique_quantique_causalite.py calc11_rayonnement.py calc12_banc_essai.py; do echo "=== $s ==="; "$PY" "$s"; echo "--- code de retour $s : $?"; done ) > "$JOURNAUX/F_calculs.log" 2>&1 &
# --- Équipe E
( cd "$COPIE/06_modele_3D" && /usr/bin/time -p sh reconstruire.sh --mesures; echo "--- code de retour reconstruire.sh : $?" ) > "$JOURNAUX/E_reconstruire.log" 2>&1 &
wait
echo "Toutes les relances sont terminées."

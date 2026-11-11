#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Équipe B — relance tous les scripts de vérification et réécrit sorties/*.txt
(≈ 2 min 30 s ; 144 s mesurées par la Red Team n° 2, durée affichée en fin d'exécution).
Le script 00 (interrogation de Crossref, réseau) n'est pas relancé ici."""
import os
import subprocess
import sys
import time

T0 = time.time()

ICI = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = [
    "01_ordres_de_grandeur_dossier.py",
    "02_hawking_corps_gris.py",
    "03_kerr_newman.py",
    "04_van_stockum_tipler.py",
    "05_deux_trous_noirs.py",
    "06_dilatation_10_ans_par_heure.py",
    "07_champs_EM_et_energie_negative.py",
    "08_charge_injection_pistes_ouvertes.py",
]
os.makedirs(os.path.join(ICI, "sorties"), exist_ok=True)
echecs = 0
for s in SCRIPTS:
    sortie = os.path.join(ICI, "sorties", s.replace(".py", ".txt"))
    with open(sortie, "w", encoding="utf-8") as f:
        code = subprocess.call([sys.executable, "-u", os.path.join(ICI, s)], stdout=f, stderr=subprocess.STDOUT, cwd=ICI)
    print(f"{s:<45} code de retour {code} -> {os.path.relpath(sortie, ICI)}")
    echecs += code != 0
print(f"durée totale : {time.time() - T0:.0f} s")
sys.exit(1 if echecs else 0)

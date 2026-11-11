#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""Red Team n° 2 — Tâche 1. Compare les sorties régénérées (copie de travail) aux sorties livrées par les équipes.
Usage : python 01_comparer_sorties.py <copie_de_travail>
Écrit journaux/comparaison_sorties.txt (résumé) et journaux/diff_textes.txt (diff unifié des fichiers texte modifiés)."""
import difflib, hashlib, os, re, sys

RACINE = _RACINE + ""
COPIE = sys.argv[1]
ICI = os.path.dirname(os.path.abspath(__file__))
DOSSIERS = ["02_reconstruction", "03_physique_theorique", "04_ingenierie", "05_simulations", "06_modele_3D", "07_experiences"]
TEXTE = {".txt", ".json", ".csv", ".md", ".svg", ".html", ".py", ".sh", ".obj", ".mtl", ".log"}

def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def liste(base):
    out = {}
    for d in DOSSIERS:
        for r, _, fs in os.walk(os.path.join(base, d)):
            if "__pycache__" in r:
                continue
            for f in fs:
                if f == ".DS_Store":
                    continue
                p = os.path.join(r, f)
                out[os.path.relpath(p, base)] = p
    return out

a, b = liste(RACINE), liste(COPIE)
ident, modif, nouveaux, absents = [], [], [], []
for k in sorted(set(a) | set(b)):
    if k not in b:
        absents.append(k)
    elif k not in a:
        nouveaux.append(k)
    elif sha(a[k]) == sha(b[k]):
        ident.append(k)
    else:
        modif.append(k)

# neutralise les chemins absolus (seule différence attendue : la racine de la copie)
def norm(s):
    s = s.replace(COPIE, "<RACINE>").replace(RACINE, "<RACINE>")
    s = s.replace(os.path.realpath(COPIE), "<RACINE>")
    return s

res, diffs = [], []
vrais = []
for k in modif:
    ext = os.path.splitext(k)[1].lower()
    if ext in TEXTE:
        ta = norm(open(a[k], encoding="utf-8", errors="replace").read()).splitlines()
        tb = norm(open(b[k], encoding="utf-8", errors="replace").read()).splitlines()
        d = list(difflib.unified_diff(ta, tb, "livré/" + k, "régénéré/" + k, lineterm="", n=0))
        nb = sum(1 for l in d if l[:1] in "+-" and not l.startswith(("+++", "---")))
        if nb == 0:
            res.append(f"  [chemins seulement] {k}")
        else:
            vrais.append(k)
            res.append(f"  [TEXTE DIFFÉRENT : {nb} lignes] {k}")
            diffs.extend(d[:400]); diffs.append("")
    else:
        vrais.append(k)
        res.append(f"  [binaire différent] {k}  ({os.path.getsize(a[k])} -> {os.path.getsize(b[k])} octets)")

os.makedirs(os.path.join(ICI, "journaux"), exist_ok=True)
with open(os.path.join(ICI, "journaux", "comparaison_sorties.txt"), "w", encoding="utf-8") as f:
    f.write(f"Fichiers comparés : {len(set(a)|set(b))}\nIdentiques à l'octet : {len(ident)}\nModifiés : {len(modif)} (dont différences réelles : {len(vrais)})\n")
    f.write(f"Nouveaux dans la copie : {len(nouveaux)}\nAbsents de la copie : {len(absents)}\n\n")
    f.write("MODIFIÉS\n" + "\n".join(res) + "\n\nNOUVEAUX\n" + "\n".join("  " + x for x in nouveaux) + "\n\nABSENTS\n" + "\n".join("  " + x for x in absents) + "\n")
with open(os.path.join(ICI, "journaux", "diff_textes.txt"), "w", encoding="utf-8") as f:
    f.write("\n".join(diffs))
print(open(os.path.join(ICI, "journaux", "comparaison_sorties.txt"), encoding="utf-8").read())

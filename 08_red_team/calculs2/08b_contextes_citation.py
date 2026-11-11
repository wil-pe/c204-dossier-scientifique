#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""Red Team n° 2 — Tâche 5. Pour chaque référence auditée, extrait les passages des rapports qui la citent
(ce que le rapport « lui fait dire »). Sortie : verif_en_ligne2/contextes.txt"""
import json, os, re
R = _RACINE + ""
V = f"{R}/08_red_team/verif_en_ligne2"
t = json.load(open(f"{V}/tirage.json", encoding="utf-8"))
def lit(p): return open(f"{R}/{p}", encoding="utf-8").read().splitlines()
docs = {"H": {"09_recherche_contemporaine/RAPPORT_H.md": None, "09_recherche_contemporaine/RECHERCHES_SUPPLEMENTAIRES.md": None},
        "B": {"03_physique_theorique/RAPPORT_B.md": None, "03_physique_theorique/ANNEXE_B1_demonstrations.md": None},
        "C": {"04_ingenierie/RAPPORT_C.md": None},
        "F": {"07_experiences/RAPPORT_F.md": None}}
for eq in docs:
    for p in docs[eq]: docs[eq][p] = lit(p)
for f in sorted(os.listdir(f"{R}/04_ingenierie/fiches")): docs["C"][f"04_ingenierie/fiches/{f}"] = lit(f"04_ingenierie/fiches/{f}")
for f in sorted(os.listdir(f"{R}/07_experiences/fiches")): docs["F"][f"07_experiences/fiches/{f}"] = lit(f"07_experiences/fiches/{f}")
out = []
for r in t["tirage"] + t["majeures"]:
    eq = r["equipe"]; ref = r["ref"]
    if eq == "H":
        motifs = [re.escape("[" + r["cle"] + "]")]
    else:
        m = re.search(r"([A-Z][A-Za-zéèöüä'’\-]+)[^()]*?\((\d{4})\)", ref) or re.search(r"\d+\. (?:[A-Z]\. ){1,3}([A-Z][A-Za-zéèöüä'’\-]+).*?\((\d{4})\)", ref)
        nom = None; annee = None
        if eq == "C":
            m2 = re.search(r"^\d+\. (?:[A-Z]\. ?){1,4}([A-Z][A-Za-zéèöüä'’\-]+)", ref); a2 = re.findall(r"\((\d{4})\)", ref)
            nom, annee = (m2.group(1) if m2 else None), (a2[-1] if a2 else None)
        elif eq == "B":
            m2 = re.search(r"\| (?:[A-Z]\. ?(?:-[a-z]\. )?){1,4}([A-Z][A-Za-zéèöüä'’\-]+)", ref); a2 = re.search(r"\((\d{4})\)", ref)
            nom, annee = (m2.group(1) if m2 else None), (a2.group(1) if a2 else None)
        else:
            m2 = re.search(r"\| ([A-Z][A-Za-zéèöüä'’\-]+)", ref); a2 = re.search(r"\((\d{4})\)", ref)
            nom, annee = (m2.group(1) if m2 else None), (a2.group(1) if a2 else None)
        motifs = [re.escape(nom) + r"[^|\n]{0,60}" + annee] if nom and annee else []
    out.append(f"=== {r['cle']} [{eq}] — {ref[:160]}")
    n = 0
    for p, ls in docs[eq].items():
        for i, l in enumerate(ls, 1):
            if any(re.search(mo, l) for mo in motifs):
                # fenêtre de ±230 caractères autour de la citation
                mo = next(re.search(mo, l) for mo in motifs if re.search(mo, l))
                a, b = max(0, mo.start() - 260), min(len(l), mo.end() + 200)
                out.append(f"   {p}:{i}: …{l[a:b]}…"); n += 1
                if n >= 4: break
        if n >= 4: break
    if n == 0: out.append("   (aucune citation trouvée dans les rapports : référence de liste seulement)")
open(f"{V}/contextes.txt", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(len(out))

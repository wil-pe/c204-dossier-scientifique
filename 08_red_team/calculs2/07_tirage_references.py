#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""Red Team n° 2 — Tâche 5. Tirage au sort (graine fixée) des références à auditer + liste des références
portant une conclusion majeure. Sortie : verif_en_ligne2/tirage.json
Graine : 20261110 (consignée dans le rapport)."""
import csv, json, os, random, re

RACINE = _RACINE + ""
GRAINE = 20261110
rng = random.Random(GRAINE)
RE_DOI = re.compile(r"\b(10\.\d{4,9}/[^\s|,;»)\]]+)", re.I)
RE_AX = re.compile(r"arXiv:\s*([a-z\-]+/\d{7}|\d{4}\.\d{4,5})", re.I)

def nettoie(d): return d.rstrip(".").rstrip(")").strip("*")

pools = {}
# --- H : bibliographie_verifiee.csv (références scientifiques vérifiées)
rows = list(csv.DictReader(open(f"{RACINE}/09_recherche_contemporaine/bibliographie_verifiee.csv", encoding="utf-8")))
pools["H"] = [{"equipe": "H", "cle": r["cle"], "ref": f'{r["auteurs"]} ({r["annee"]}). {r["titre"]}. {r["revue"]}', "doi": r["doi"].strip(), "arxiv": r["arxiv"].strip()}
              for r in rows if r["statut"] == "vérifiée"]
# --- B : lignes de tableau de REFERENCES.md
def lignes_md(chemin, motif_ligne):
    out = []
    for n, l in enumerate(open(chemin, encoding="utf-8").read().splitlines(), 1):
        if motif_ligne(l):
            doi = RE_DOI.search(l); ax = RE_AX.search(l)
            if doi or ax:
                out.append({"ligne": n, "ref": re.sub(r"\s+", " ", l)[:400], "doi": nettoie(doi.group(1)) if doi else "", "arxiv": ax.group(1) if ax else ""})
    return out
b = lignes_md(f"{RACINE}/03_physique_theorique/REFERENCES.md", lambda l: l.startswith("| ") and "(1" in l or l.startswith("| ") and "(2" in l)
for x in b: x.update(equipe="B", cle=f"B-l{x['ligne']}")
pools["B"] = b
c = lignes_md(f"{RACINE}/04_ingenierie/REFERENCES.md", lambda l: re.match(r"^\d+\. ", l) is not None)
for x in c: x.update(equipe="C", cle=f"C-n{x['ref'].split('.')[0]}")
pools["C"] = c
f = lignes_md(f"{RACINE}/07_experiences/REFERENCES.md", lambda l: l.startswith("| ") and "doi:" in l)
for x in f: x.update(equipe="F", cle=f"F-l{x['ligne']}")
pools["F"] = f

quotas = {"H": 14, "B": 8, "C": 6, "F": 6}
tirage = []
for eq in ("H", "B", "C", "F"):
    tirage += rng.sample(pools[eq], quotas[eq])
# --- références portant une conclusion majeure (choix raisonné, hors tirage)
majeures_H = ["Page76a", "Page77", "Gibbons75", "MW90", "MCP08", "Carter68", "Tipler74", "Tipler77", "Hawking92", "NH09", "DL17", "Zilberman22",
              "GJW17", "MMP18", "FR96", "PF97", "OE05", "Polchinski91", "Deutsch91", "Everett04", "Ori05", "Bothwell22", "Prezens10", "KRW97",
              "PBH2505", "CMS26", "GW250114LVK", "Lu26", "QCTRL26", "Kugel24", "SW17", "Olum98", "SSV22", "CW09", "Westphal21", "Bollinger89", "GPB11"]
idx = {r["cle"]: r for r in pools["H"]}
majeures = [dict(idx[k], majeure=True) for k in majeures_H if k in idx]
manquantes = [k for k in majeures_H if k not in idx]
out = {"graine": GRAINE, "tailles_des_viviers": {k: len(v) for k, v in pools.items()}, "quotas": quotas, "tirage": tirage, "majeures": majeures, "cles_majeures_absentes_du_csv": manquantes}
json.dump(out, open(f"{RACINE}/08_red_team/verif_en_ligne2/tirage.json", "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print(out["tailles_des_viviers"], "tirées :", len(tirage), "majeures :", len(majeures), "absentes :", manquantes)
for t in tirage:
    print(f"  {t['equipe']} {t['cle']:<14} doi={t['doi'][:40]:<40} arxiv={t['arxiv']:<12} {t['ref'][:110]}")

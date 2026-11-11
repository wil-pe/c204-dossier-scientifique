#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""Red Team n° 2 — Tâche 1 (suite). Pour chaque rapport d'équipe (B, C, D, F), extrait les nombres écrits en
notation scientifique (« 3,9 × 10¹² », « 4,8×10⁻¹² ») et cherche, dans les sorties de scripts de la même équipe
(txt, json, csv), une valeur qui s'arrondit à la même mantisse. Test à faible puissance (coïncidences possibles :
les sorties contiennent des milliers de nombres) : un « retrouvé » n'est pas une preuve, un « non retrouvé » est fiable.
Les nombres non retrouvés sont listés pour examen manuel : ce ne sont PAS tous des erreurs (valeurs citées de la
littérature, valeurs dérivées à la main par produit/quotient, valeurs d'une autre équipe)."""
import json, math, os, re, sys

RACINE = _RACINE + ""
SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")
EQUIPES = {
    "B": (["03_physique_theorique/RAPPORT_B.md", "03_physique_theorique/ANNEXE_B1_demonstrations.md"],
          ["03_physique_theorique/verifications/sorties"]),
    "C": (["04_ingenierie/RAPPORT_C.md"], ["04_ingenierie/calculs/resultats", "04_ingenierie/bilan_energetique.csv",
          "04_ingenierie/tableau_exigences_ecarts.csv", "04_ingenierie/tableau_faisabilite.csv"]),
    "D": (["05_simulations/RAPPORT_D.md"], ["05_simulations/journal_run_all.txt", "05_simulations/resultats_globaux.json"] +
          [f"05_simulations/{d}/resultats" for d in os.listdir(f"{RACINE}/05_simulations") if d.startswith("S0")]),
    "F": (["07_experiences/RAPPORT_F.md"], ["07_experiences/calculs/resultats"]),
}
RE_SCI = re.compile(r"(?<![\w,.])(\d+(?:[,.]\d+)?)\s*[×x]\s*10\s*([⁻⁺]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+|\^\{?-?\d+\}?)")
RE_NUM = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")

def nombres_sorties(chemins):
    vals = set()
    def lit(p):
        if not p.endswith((".txt", ".json", ".csv")) or "refs_" in p:
            return
        t = open(p, encoding="utf-8", errors="replace").read()
        t2 = t.replace(" ", "").replace("\xa0", "")
        for m in RE_NUM.finditer(t2):
            try:
                v = abs(float(m.group()))
            except ValueError:
                continue
            if v > 0 and math.isfinite(v):
                vals.add(v)
        # notation « 1,23e+04 » ou « 1,23×10^4 » à virgule décimale dans les sorties françaises
        for m in re.finditer(r"(\d+),(\d+)(?:[eE]([-+]?\d+))?", t2):
            try:
                vals.add(float(f"{m.group(1)}.{m.group(2)}e{m.group(3) or 0}"))
            except ValueError:
                pass
        for m in RE_SCI.finditer(t2):
            e = m.group(2).translate(SUP).strip("^{}")
            vals.add(float(m.group(1).replace(",", ".")) * 10.0 ** int(e))
    for c in chemins:
        p = os.path.join(RACINE, c)
        if os.path.isdir(p):
            for r, _, fs in os.walk(p):
                if "refs_crossref" in r:
                    continue
                for f in fs:
                    lit(os.path.join(r, f))
        elif os.path.exists(p):
            lit(p)
    return sorted(vals)

def trouve(v, vals, tol):
    import bisect
    lo, hi = v * (1 - tol), v * (1 + tol)
    i = bisect.bisect_left(vals, lo)
    return i < len(vals) and vals[i] <= hi

bilan = {}
out = []
for eq, (rapports, sorties) in EQUIPES.items():
    vals = nombres_sorties(sorties)
    for rap in rapports:
        lignes = open(os.path.join(RACINE, rap), encoding="utf-8").read().splitlines()
        total = nontrouve = 0
        manq = []
        for n, l in enumerate(lignes, 1):
            for m in RE_SCI.finditer(l):
                mant = m.group(1).replace(",", ".")
                e = int(m.group(2).translate(SUP).strip("^{}"))
                v = float(mant) * 10.0 ** e
                nsig = len(mant.replace(".", "").lstrip("0")) or 1
                # critère strict : une valeur de sortie doit s'arrondir à la même mantisse (même nombre de chiffres
                # significatifs) ; pour 1 chiffre significatif on tolère ±25 % (arrondi lâche d'ordre de grandeur)
                demi = 0.5 * 10.0 ** (e - (len(mant.split(".")[1]) if "." in mant else 0))
                tol = 0.25 if nsig == 1 else 1.02 * demi / v
                total += 1
                if not trouve(v, vals, tol):
                    nontrouve += 1
                    manq.append((n, m.group(0), l.strip()[:150]))
        bilan[rap] = (total, nontrouve)
        out.append(f"\n=== {rap} : {total} nombres en notation scientifique, {nontrouve} sans valeur concordante dans les sorties de l'équipe {eq} ===")
        for n, s, l in manq:
            out.append(f"  l.{n:<4} {s:<16} | {l}")
txt = "\n".join(out)
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "journaux", "chiffres_non_traces.txt"), "w", encoding="utf-8").write(txt + "\n")
for k, (t, n) in bilan.items():
    print(f"{k}: {t} nombres, {n} non retrouvés ({100*n/max(t,1):.0f} %)")

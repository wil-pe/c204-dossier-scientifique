#!/usr/bin/env python3
# -*- coding: utf-8 -*-
_RACINE = str(__import__("pathlib").Path(__file__).resolve().parents[2])  # racine du projet
"""
Équipe G — 04_figure_coherence.py : carte de (in)cohérence des contraintes sur la masse M d'UNE singularité.
Figure ILLUSTRATIVE (ordres de grandeur ; hypothèses : trou noir de Schwarzschild, émission de Hawking standard).
"""
import math, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
G=6.67430e-11; c=2.99792458e8; hbar=1.054571817e-34; kB=1.380649e-23; g0=9.80665; MeV=1.602176634e-13
K=hbar*c**6/G**2; a_bb=1/(15360*math.pi); a_full=4.449e-4
bandes = [
 ("« 300–500 MW » (corps noir, photons seuls)",        math.sqrt(a_bb*K/500e6),  math.sqrt(a_bb*K/300e6),  "tab:orange"),
 ("« 300–500 MW » (Page 1976 : γ+ν+e±)",               math.sqrt(a_full*K/500e6), math.sqrt(a_full*K/300e6), "tab:red"),
 ("« 1,5–2 g » à 1–3 m (2 singularités)",              1.5*g0*1.0**2/G/2,        2*g0*3.0**2/G/2,          "tab:blue"),
 ("« rayons X » (kT = 1–100 keV)",                     kB*(hbar*c**3/(8*math.pi*G*kB))/(100e-3*MeV), kB*(hbar*c**3/(8*math.pi*G*kB))/(1e-3*MeV), "tab:purple"),
 ("« taille d'un électron » (r_s = 2,8 fm) et « bien plus petites »", 1.9e10, 1.9e12, "tab:green"),
 ("unité de « 500 livres » (M ≤ 227 kg au total)",     1e0, 113.5, "tab:gray"),
 ("durée de vie > 6 h (toutes espèces du modèle standard, f≈15)",   (2.2e4*3*a_full*hbar*c**4/G**2)**(1/3)*2.1, 1e17, "tab:brown"),
 ("ergosphère ≥ 3 m (échelle revendiquée du champ)",   3.0*c**2/(2*G), 1e29, "k"),
]
fig, ax = plt.subplots(figsize=(11, 4.6))
for i, (lab, lo, hi, col) in enumerate(bandes):
    ax.barh(i, math.log10(hi)-math.log10(lo), left=math.log10(lo), color=col, alpha=0.75, height=0.6)
    ax.text(math.log10(hi)+0.2 if math.log10(hi) < 20 else math.log10(lo)-0.2, i, lab, va="center",
            ha="left" if math.log10(hi) < 20 else "right", fontsize=8.5)
ax.set_yticks([]); ax.set_xlim(0, 30); ax.set_xlabel("log10 (masse d'une singularité / kg)")
ax.set_title("C204 — contraintes revendiquées sur la masse d'une singularité : aucun recouvrement commun\n"
             "(figure illustrative, ordres de grandeur ; équipe G)", fontsize=10)
ax.grid(axis="x", alpha=0.3); ax.invert_yaxis(); fig.tight_layout()
out = _RACINE + "/08_red_team/figures/carte_coherence_masse.png"
fig.savefig(out, dpi=150); print("écrit :", out)
for lab, lo, hi, _ in bandes: print(f"{lab:62s}: {lo:.2e} – {hi:.2e} kg")

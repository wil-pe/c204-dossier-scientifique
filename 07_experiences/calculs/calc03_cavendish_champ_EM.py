#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-03 — Mesure de G (Cavendish) et test nul « un champ électromagnétique intense crée-t-il
une gravité mesurable ? ».

Calcule :
  1. le signal d'une balance de torsion de TP (couple, angle, période, bruit thermique) ;
  2. la masse équivalente E/c² de l'énergie de champs électromagnétiques réels et la force
     gravitationnelle correspondante (prédiction de la relativité générale en champ faible) ;
  3. les forces parasites (magnétique, électrostatique, courants d'air) pour le même montage ;
  4. le champ magnétique qu'il faudrait pour que l'énergie du champ « pèse » autant que l'eau.

Hypothèses : sphères ponctuelles, champ faible ; pour un système lié statique, la masse
gravitationnelle active totale vaut E/c² (pressions et tensions comprises, Tolman).
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from constantes import (G, c, kB, eps0, mu0, g0, sauver, fig_chemin, sci)

L, D = [], {}
L.append("EXP-03 — BALANCE DE TORSION : G ET TEST NUL ÉLECTROMAGNÉTIQUE")
L.append("=" * 72)

# ---------------------------------------------------------------- 1. balance de torsion de TP
m = 0.015          # petites masses (kg)
M = 1.5            # grosses masses (kg)
d = 0.05           # demi-longueur du fléau (m)
r = 0.045          # distance centre à centre petite/grosse masse (m)
d_fil, L_fil, G_cis = 25e-6, 0.30, 161e9   # fil de tungstène : diamètre, longueur, module de cisaillement
T_amb = 293.0

F = G * M * m / r**2
couple = 2 * F * d
kappa = math.pi * G_cis * d_fil**4 / (32 * L_fil)
I = 2 * m * d**2
T0 = 2 * math.pi * math.sqrt(I / kappa)
theta = couple / kappa
L_levier = 2.0
depl = 4 * theta * L_levier                       # bascule des masses : 2θ ; réflexion : facteur 2
theta_th = math.sqrt(kB * T_amb / kappa)
F_th = kappa * theta_th / (2 * d)
Q = 10.0
w0 = 2 * math.pi / T0
S_tau = math.sqrt(4 * kB * T_amb * kappa / (Q * w0))   # N·m/√Hz
tint = 3600.0
F_min_th = S_tau / math.sqrt(tint) / (2 * d)

L.append("1. Balance de torsion de TP (type Cavendish) — paramètres choisis pour l'exemple")
L.append(f"   m = {m*1e3:.0f} g (×2), M = {M} kg (×2), demi-fléau d = {d*100:.0f} cm, distance r = {r*100:.1f} cm")
L.append(f"   fil de tungstène Ø {d_fil*1e6:.0f} µm, longueur {L_fil*100:.0f} cm → κ = πG_cis·d⁴/(32L) = {sci(kappa)} N·m/rad")
L.append(f"   force de Newton       F = GMm/r²   = {sci(F)} N")
L.append(f"   couple                2Fd          = {sci(couple)} N·m")
L.append(f"   angle d'équilibre     θ = 2Fd/κ    = {sci(theta)} rad")
L.append(f"   période               2π√(I/κ)     = {T0:.0f} s ({T0/60:.1f} min)")
L.append(f"   déplacement du spot à {L_levier:.0f} m en basculant les grosses masses : 4θL = {depl*1e3:.1f} mm")
L.append(f"   agitation thermique   θ_rms = √(k_BT/κ) = {sci(theta_th)} rad  (soit {sci(F_th)} N équivalent)")
L.append(f"   bruit thermique de couple (Q = {Q:.0f}) : {sci(S_tau)} N·m/√Hz → force minimale en 1 h : {sci(F_min_th)} N")
L.append("   En pratique un montage de TP est limité par les dérives du fil, les courants d'air et les")
L.append("   inclinaisons du sol : résolution réaliste ~1e-11 N (quelques % du signal de Newton).")
D["cavendish"] = {"F_N": F, "couple_Nm": couple, "kappa": kappa, "theta_rad": theta, "periode_s": T0,
                  "deplacement_spot_mm": depl * 1e3, "theta_thermique": theta_th, "F_min_thermique_1h": F_min_th}
L.append("")

# incertitude sur G (propagation simple)
inc = {"r (±0,5 mm sur 45 mm, exposant 2)": 2 * 0.5 / 45, "période (±0,5 %, exposant 2)": 2 * 0.005,
       "angle θ (±3 %)": 0.03, "d (±0,2 mm sur 50 mm)": 0.2 / 50, "M, m (±0,1 %)": 0.0014}
tot = math.sqrt(sum(v**2 for v in inc.values()))
L.append("   Incertitude type attendue sur G en TP (G = 4π²·θ·r²·d/(T²·M)) :")
for k, v in inc.items():
    L.append(f"     {k:<36} {100*v:.1f} %")
L.append(f"     total quadratique ≈ {100*tot:.1f} %   (CODATA 2018 : G = 6,674 30(15)e-11, incertitude relative 2,2e-5)")
D["incertitude_G_TP"] = tot
L.append("")

# ---------------------------------------------------------------- 2. gravité d'un champ électromagnétique
r_test = 0.05
SOURCES = [
    # nom, énergie (J), masse inerte de l'objet (kg) ou None, distance d'essai (m)
    ("Aimant NdFeB de 1 litre (u ≈ 4e5 J/m³)", 4e5 * 1e-3, 7.5, 0.05),
    ("Condensateur 1 nF chargé à 5 kV (12,5 mJ)", 0.5 * 1e-9 * 5e3**2, 0.05, 0.05),
    ("Condensateur 100 µF à 400 V (8 J) — DANGEREUX, calcul seul", 0.5 * 100e-6 * 400**2, 0.1, 0.05),
    ("Bobine supraconductrice d'IRM 3 T (≈ 10 MJ)", 1.0e7, 5e3, 1.0),
    ("Aimant hybride 45 T (≈ 100 MJ)", 1.0e8, 3e4, 1.0),
    ("Dipôles du LHC, total (≈ 11 GJ)", 1.1e10, None, 100.0),
    ("Aimants d'ITER, total (≈ 51 GJ)", 5.1e10, None, 10.0),
]
L.append("2. « Gravité » d'un champ électromagnétique selon la relativité générale (champ faible) : M_éq = E/c²")
L.append(f"   {'source':<58}{'E (J)':>10}{'E/c² (kg)':>12}{'a à r (m/s²)':>14}{'F sur 15 g (N)':>16}")
D["champ_EM"] = []
for nom, E, masse, rr in SOURCES:
    meq = E / c**2
    a = G * meq / rr**2
    Fg = a * m
    D["champ_EM"].append({"source": nom, "E_J": E, "m_eq_kg": meq, "r_m": rr, "a_m_s2": a, "F_N": Fg,
                          "rapport_masse": (meq / masse) if masse else None})
    L.append(f"   {nom:<58}{sci(E,2):>10}{sci(meq,2):>12}{sci(a,2):>10} ({rr:g} m){sci(Fg,2):>12}")
u_1T = 1.0 / (2 * mu0)
L.append(f"   Densité d'énergie d'un champ de 1 T : B²/(2µ0) = {sci(u_1T)} J/m³ → densité de masse équivalente {sci(u_1T/c**2)} kg/m³")
B_eau = math.sqrt(2 * mu0 * 1000.0 * c**2)
E_eau = math.sqrt(2 * 1000.0 * c**2 / eps0)
L.append(f"   Champ dont l'énergie « pèserait » autant que l'eau (1000 kg/m³) : B = {sci(B_eau)} T ou E = {sci(E_eau)} V/m")
L.append("   (record de champ continu en laboratoire : ~45 T ; champ de claquage de l'air : 3e6 V/m)")
D["B_equivalent_eau_T"] = B_eau
D["E_equivalent_eau_V_m"] = E_eau
F_GR = D["champ_EM"][0]["F_N"]
L.append("")

# ---------------------------------------------------------------- 3. forces parasites
L.append("3. Forces parasites sur une masse d'épreuve de 15 g placée à 5 cm de la source")
V_pb = m / 11340.0
a_sph = (3 * V_pb / (4 * math.pi)) ** (1 / 3)
chi = {"plomb (diamagnétique)": -1.6e-5, "tungstène (paramagnétique)": 7.8e-5, "cuivre": -9.6e-6,
       "aluminium": 2.1e-5}
B_loc, gradB = 0.1, 5.0       # T, T/m à la position de la masse d'épreuve
paras = {}
for mat, x in chi.items():
    Fm = abs(x) * V_pb / mu0 * B_loc * gradB
    paras[f"magnétique, {mat} (χ = {x:+.1e})"] = Fm
E_loc, L_grad = 2e5, 0.05     # champ électrique local (10 kV sur 5 cm), échelle de gradient
F_dip = 2 * math.pi * eps0 * a_sph**3 * (2 * E_loc**2 / L_grad)
paras["électrostatique, sphère neutre polarisée (10 kV à 5 cm)"] = F_dip
paras["électrostatique, charge résiduelle de 1 pC dans 2e5 V/m"] = 1e-12 * E_loc
eta_air = 1.8e-5
paras["courant d'air de 1 mm/s (traînée de Stokes)"] = 6 * math.pi * eta_air * a_sph * 1e-3
paras["attraction newtonienne de la masse de l'aimant (7,5 kg)"] = G * 7.5 * m / r_test**2
paras["attraction newtonienne des grosses masses (signal de Cavendish)"] = F
paras["SIGNAL RG : énergie du champ de l'aimant (E/c²)"] = F_GR
L.append(f"   (sphère de plomb : rayon {a_sph*1e3:.1f} mm ; champ local {B_loc} T, gradient {gradB} T/m ; E local {E_loc:.0e} V/m)")
for k, v in sorted(paras.items(), key=lambda kv: -kv[1]):
    L.append(f"   {k:<64} {sci(v):>10} N   ({v/F_GR:9.1e} × signal RG)")
D["parasites_N"] = paras
L.append("")

# ---------------------------------------------------------------- 4. sensibilités comparées
sens = {
    "Cavendish de TP (N2), ~1e-11 N sur 15 g": 1e-11 / m,
    "Limite thermique du même montage, 1 h": F_min_th / m,
    "Meilleures balances de torsion (Schlamminger et al. 2008 : Δa ~ 1e-15 m/s²)": 1e-15,
}
a_GR_aimant = D["champ_EM"][0]["a_m_s2"]
a_GR_45T = D["champ_EM"][4]["a_m_s2"]
L.append("4. Sensibilité atteignable contre signal prédit (en accélération)")
for k, v in sens.items():
    L.append(f"   {k:<76} {sci(v)} m/s²")
L.append(f"   Signal RG, aimant NdFeB 1 L à 5 cm  : {sci(a_GR_aimant)} m/s² → manque {1e-15/a_GR_aimant:.0e} (meilleure balance), "
         f"{(1e-11/m)/a_GR_aimant:.0e} (TP)")
L.append(f"   Signal RG, aimant hybride 45 T à 1 m : {sci(a_GR_45T)} m/s² → manque {1e-15/a_GR_45T:.0e} (meilleure balance)")
L.append("")
L.append("Conclusion : la relativité générale prédit bien qu'un champ électromagnétique gravite (via E/c²),")
L.append("mais le signal est de 7 ordres de grandeur sous la meilleure balance de torsion du monde et ~14 ordres")
L.append("sous un montage de TP, tandis que les forces magnétiques/électrostatiques parasites sont 10^18 à 10^19")
L.append("fois plus grandes que lui. Tout « signal » observé près d'un aimant ou d'un condensateur est un artefact")
L.append("jusqu'à preuve du contraire. Champ électromagnétique ≠ champ gravitationnel.")
D["sensibilites_m_s2"] = sens
D["ecart_meilleure_balance_aimant"] = 1e-15 / a_GR_aimant

sauver("calc03_cavendish_champ_EM", D, L)

# ---------------------------------------------------------------- figure
fig, ax = plt.subplots(figsize=(10, 5.8))
items = sorted(paras.items(), key=lambda kv: kv[1])
noms = [k for k, _ in items]
vals = [v for _, v in items]
cols = ["#2e8b57" if "RG" in k else ("#33658a" if "newton" in k else "#d1495b") for k in noms]
ax.barh(range(len(noms)), vals, color=cols)
ax.set_xscale("log")
ax.set_yticks(range(len(noms)))
ax.set_yticklabels(noms, fontsize=7.5)
ax.axvline(1e-11, color="k", ls="--", lw=1)
ax.text(1.3e-11, 0.2, "résolution d'un Cavendish de TP", fontsize=8, rotation=90, va="bottom")
ax.axvline(1e-15 * m, color="gray", ls=":", lw=1.2)
ax.text(1.3e-15 * m, 0.2, "meilleure balance de torsion publiée", fontsize=8, rotation=90, va="bottom", color="gray")
ax.set_xlabel("force sur une masse d'épreuve de 15 g (N)")
ax.set_title("EXP-03 — Test nul « gravité d'un champ électromagnétique » : signal prédit (vert)\n"
             "contre forces parasites (rouge) et attraction newtonienne (bleu) — calcul illustratif")
ax.grid(True, which="both", axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig(fig_chemin("calc03_test_nul_EM.png"), dpi=150)
print("figure :", fig_chemin("calc03_test_nul_EM.png"))

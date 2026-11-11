#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-05 — Effet Casimir : ordres de grandeur, faisabilité, et pourquoi il ne fournit pas
l'« énergie négative » qu'exigerait une machine à courbes temporelles fermées.

Calcule :
  1. pression entre plaques parfaites P = π²ħc/(240 d⁴) et énergie par unité de surface ;
  2. force sphère-plan (approximation de proximité) F = π³ħcR/(360 d³) ;
  3. corrections de conductivité finie (développement valable pour d >> δ) et longueur thermique ;
  4. force électrostatique parasite (potentiel de contact résiduel) et bruit thermique d'un levier AFM ;
  5. bilan énergétique : densité d'énergie « négative » contre masse des plaques, et comparaison
     à l'ordre de grandeur requis pour un trou de ver traversable (-r·c²/G, estimation dimensionnelle).
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from constantes import (G, c, hbar, kB, eps0, sauver, fig_chemin, sci)

L, D = [], {}
L.append("EXP-05 — EFFET CASIMIR : ORDRES DE GRANDEUR")
L.append("=" * 72)

def P_plaques(d):            # Pa (attractive)
    return math.pi**2 * hbar * c / (240 * d**4)

def E_surf(d):               # J/m² (négative)
    return -math.pi**2 * hbar * c / (720 * d**3)

def F_sphere_plan(R, d):     # N
    return math.pi**3 * hbar * c * R / (360 * d**3)

# ---------------------------------------------------------------- 1. plaques
L.append("1. Plaques parallèles parfaitement conductrices, T = 0")
L.append(f"   {'d':>8} | {'P (Pa)':>10} | {'E/A (J/m²)':>11} | {'u = E/(A·d) (J/m³)':>19} | {'u/c² (kg/m³)':>13}")
D["plaques"] = []
for d in (10e-9, 100e-9, 500e-9, 1e-6, 10e-6):
    P, Es = P_plaques(d), E_surf(d)
    u = Es / d
    D["plaques"].append({"d_m": d, "P_Pa": P, "E_surf": Es, "u_J_m3": u, "rho_eq": u / c**2})
    L.append(f"   {d*1e9:>5.0f} nm | {sci(P):>10} | {sci(Es):>11} | {sci(u):>19} | {sci(u/c**2):>13}")
L.append(f"   Repère : pression atmosphérique 1,013e5 Pa, atteinte pour d ≈ {(math.pi**2*hbar*c/(240*101325))**0.25*1e9:.1f} nm.")
L.append("")

# ---------------------------------------------------------------- 2. sphère-plan
L.append("2. Géométrie sphère-plan (approximation de proximité, valable pour d << R)")
D["sphere_plan"] = []
for nom, R, d in (("microsphère AFM R = 100 µm, d = 100 nm", 100e-6, 100e-9),
                  ("microsphère AFM R = 100 µm, d = 200 nm", 100e-6, 200e-9),
                  ("microsphère AFM R = 100 µm, d = 500 nm", 100e-6, 500e-9),
                  ("lentille R = 11 cm, d = 1 µm (géométrie de type balance de torsion)", 0.11, 1e-6),
                  ("lentille R = 11 cm, d = 6 µm", 0.11, 6e-6)):
    F = F_sphere_plan(R, d)
    D["sphere_plan"].append({"cas": nom, "F_N": F})
    L.append(f"   {nom:<66} F = {sci(F)} N")
L.append("")

# ---------------------------------------------------------------- 3. corrections
lam_p = 136e-9                      # longueur d'onde plasma de l'or (valeur usuelle)
delta = lam_p / (2 * math.pi)
lam_T = hbar * c / (kB * 300.0)
L.append("3. Corrections à la formule idéale")
L.append(f"   profondeur de pénétration de l'or : δ = λ_p/2π = {delta*1e9:.1f} nm (λ_p ≈ 136 nm)")
for d in (500e-9, 1e-6, 3e-6):
    eta_pp = 1 - (16 / 3) * delta / d + 24 * (delta / d)**2
    eta_sp = 1 - 4 * delta / d + (72 / 5) * (delta / d)**2
    L.append(f"   d = {d*1e9:>5.0f} nm : facteur plaques {eta_pp:.3f} ; facteur sphère-plan {eta_sp:.3f} "
             f"(développement au 2e ordre en δ/d ; non valable à 100 nm)")
L.append(f"   longueur thermique λ_T = ħc/(k_BT) = {lam_T*1e6:.2f} µm à 300 K : les corrections thermiques dominent pour d ≳ 3 µm.")
L.append("   rugosité : correction relative ~6(σ_rms/d)² → 1 % pour σ_rms = 4 nm à d = 100 nm.")
D["delta_or_nm"] = delta * 1e9
D["lambda_T_um"] = lam_T * 1e6
L.append("")

# ---------------------------------------------------------------- 4. parasites et bruit
L.append("4. Systématiques et bruit (sphère R = 100 µm sur levier AFM)")
R = 100e-6
D["electrostatique"] = []
for d in (100e-9, 200e-9, 500e-9):
    Fc = F_sphere_plan(R, d)
    for V in (0.01, 0.05, 0.1):
        Fe = math.pi * eps0 * R * V**2 / d
        D["electrostatique"].append({"d_m": d, "V": V, "F_el": Fe, "rapport": Fe / Fc})
        L.append(f"   d = {d*1e9:.0f} nm, potentiel résiduel {V*1e3:>3.0f} mV : F_él = πε0RV²/d = {sci(Fe)} N = {100*Fe/Fc:6.1f} % de Casimir")
k_lev, f0, Q, T = 0.02, 10e3, 100.0, 300.0
S_F = math.sqrt(4 * kB * T * k_lev / (2 * math.pi * f0 * Q))
x_casimir = F_sphere_plan(R, 100e-9) / k_lev
L.append(f"   levier k = {k_lev} N/m, f0 = {f0/1e3:.0f} kHz, Q = {Q:.0f} (air) : bruit thermique de force {sci(S_F)} N/√Hz")
L.append(f"   déflexion statique due à Casimir à 100 nm : F/k = {x_casimir*1e9:.1f} nm (largement mesurable)")
L.append(f"   rapport signal/bruit thermique en 1 s à 100 nm : {F_sphere_plan(R,100e-9)/S_F:.0f}")
L.append("   La difficulté n'est donc pas le bruit mais la métrologie : distance absolue (±1 nm), potentiels de")
L.append("   contact et « patchs », rugosité, parallélisme (pour deux plaques), dérive thermique.")
D["bruit_force_AFM"] = S_F
L.append("")

# ---------------------------------------------------------------- 5. bilan « énergie négative »
A, d = 1.0, 10e-9
E_neg = E_surf(d) * A
m_neg = E_neg / c**2
m_plaques = 2 * A * 100e-9 * 19300.0           # deux films d'or de 100 nm (minimum irréaliste)
r_gorge = 1.0
m_tv = -r_gorge * c**2 / G                     # estimation dimensionnelle (Morris-Thorne)
L.append("5. Pourquoi ce n'est pas une source d'« énergie négative » exploitable")
L.append(f"   Plaques de 1 m² séparées de 10 nm : E = {sci(E_neg)} J, soit une « masse » de {sci(m_neg)} kg")
L.append(f"   Masse (positive) de deux films d'or de 100 nm seulement : {sci(m_plaques)} kg → rapport {abs(m_plaques/m_neg):.1e}")
L.append("   L'énergie TOTALE du système (plaques + champ) reste donc positive à ~18 ordres de grandeur près.")
L.append(f"   Ordre de grandeur de l'énergie négative pour une gorge de trou de ver de rayon 1 m : -r·c²/G = {sci(m_tv)} kg")
L.append(f"   (≈ {abs(m_tv)/1.898e27:.2f} masse de Jupiter) → il manque un facteur {abs(m_tv/m_neg):.0e} par rapport à 1 m² de Casimir à 10 nm.")
L.append("   Les inégalités quantiques (Ford & Roman 1995, 1996) bornent en outre durée et amplitude des densités")
L.append("   d'énergie négatives. L'effet Casimir est une FORCE mesurée ; ce n'est ni un réservoir d'énergie,")
L.append("   ni une preuve qu'on puisse accumuler de l'énergie négative macroscopique.")
D["bilan"] = {"E_neg_J": E_neg, "m_neg_kg": m_neg, "m_plaques_kg": m_plaques, "m_trou_de_ver_kg": m_tv,
              "facteur_manquant": abs(m_tv / m_neg)}

sauver("calc05_casimir", D, L)

# ---------------------------------------------------------------- figure
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2))
dd = np.logspace(-8, -5, 300)
ax = axes[0]
ax.loglog(dd * 1e9, math.pi**2 * hbar * c / (240 * dd**4), lw=2.2, color="#33658a", label="plaques idéales : π²ħc/(240 d⁴)")
ax.axhline(101325, color="gray", ls=":", lw=1)
ax.text(1.2e3, 1.3e5, "pression atmosphérique", fontsize=8, color="gray")
ax.set_xlabel("distance d (nm)")
ax.set_ylabel("pression de Casimir (Pa)")
ax.set_title("Pression entre plaques parfaites (T = 0)\ncalcul illustratif", fontsize=10)
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=8)

ax = axes[1]
ax.loglog(dd * 1e9, math.pi**3 * hbar * c * 100e-6 / (360 * dd**3), lw=2.2, color="#33658a", label="Casimir, sphère R = 100 µm")
for V, col in ((0.01, "#f6ae2d"), (0.05, "#f26419"), (0.1, "#d1495b")):
    ax.loglog(dd * 1e9, math.pi * eps0 * 100e-6 * V**2 / dd, ls="--", color=col, label=f"électrostatique résiduelle, {V*1e3:.0f} mV")
ax.axhline(S_F, color="k", ls=":", lw=1)
ax.text(12, S_F * 1.4, "bruit thermique du levier en 1 s", fontsize=8)
ax.set_xlabel("distance d (nm)")
ax.set_ylabel("force (N)")
ax.set_title("Sphère-plan : signal Casimir contre parasite électrostatique\ncalcul illustratif", fontsize=10)
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=8)
fig.tight_layout()
fig.savefig(fig_chemin("calc05_casimir.png"), dpi=150)
print("figure :", fig_chemin("calc05_casimir.png"))

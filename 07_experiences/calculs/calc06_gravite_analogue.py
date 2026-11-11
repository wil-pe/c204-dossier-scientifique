#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-06 — Gravité analogue dans l'eau : ressaut hydraulique circulaire (analogue de trou blanc)
et tourbillon de vidange (analogue d'ergorégion / superradiance).

Calcule :
  1. vitesses d'ondes de surface (gravité-capillarité, profondeur finie) et nombre de Froude
     de part et d'autre d'un ressaut circulaire d'évier ; angle de Mach attendu ;
  2. rayon du ressaut selon deux lois d'échelle publiées (Bohr et al. 1993 ; Bhagat et al. 2018) ;
  3. modèle de « baignoire qui se vide » : rayons de l'horizon et de l'ergorégion, condition
     de superradiance ω < m·Ω_H ;
  4. température de Hawking analogue T = ħ·κ/(2π·k_B) pour l'eau et pour un condensat,
     comparée à la température du milieu et à celle de vrais trous noirs.

Les modèles hydrodynamiques sont volontairement simples (ordres de grandeur pour préparer la
mesure) ; ce sont les mesures qui font foi, pas ces estimations.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from constantes import (G, c, hbar, kB, g0, M_soleil, sauver, fig_chemin, sci)

L, D = [], {}
rho, nu, gam = 998.0, 1.0e-6, 0.072      # eau à 20 °C
L.append("EXP-06 — GRAVITÉ ANALOGUE DANS L'EAU")
L.append("=" * 72)

# ---------------------------------------------------------------- 1. ondes de surface
def c_phase(k, h):
    return np.sqrt((g0 / k + gam * k / rho) * np.tanh(k * h))

k_min = math.sqrt(rho * g0 / gam)
c_min = math.sqrt(2 * math.sqrt(g0 * gam / rho))
L.append("1. Ondes de surface de l'eau")
L.append(f"   eau profonde : vitesse de phase minimale c_min = (4gγ/ρ)^(1/4) = {c_min*100:.1f} cm/s "
         f"à λ = {2*math.pi/k_min*1000:.1f} mm (frontière gravité/capillarité)")
for h in (0.0003, 0.001, 0.003, 0.01, 0.0625):
    L.append(f"   ondes longues, profondeur h = {h*1000:6.2f} mm : c = √(gh) = {math.sqrt(g0*h)*100:6.1f} cm/s")
L.append("")

# ---------------------------------------------------------------- 2. ressaut circulaire d'évier
L.append("2. Ressaut hydraulique circulaire (jet vertical sur plaque horizontale)")
L.append(f"   {'débit Q':>10} | {'R (Bohr 1993)':>14} | {'R (Bhagat 2018)':>16} | commentaire")
D["ressaut"] = []
for Q_mLs in (10.0, 20.0, 30.0, 60.0, 100.0):
    Q = Q_mLs * 1e-6
    R_bohr = 0.73 * Q**(5 / 8) * nu**(-3 / 8) * g0**(-1 / 8)
    R_bhagat = 0.2705 * Q**(3 / 4) * rho**(1 / 4) / (nu**(1 / 4) * gam**(1 / 4))
    D["ressaut"].append({"Q_mL_s": Q_mLs, "R_bohr_m": R_bohr, "R_bhagat_m": R_bhagat})
    L.append(f"   {Q_mLs:>6.0f} mL/s | {R_bohr*100:>11.1f} cm | {R_bhagat*100:>13.1f} cm | à mesurer")
L.append("   (Bohr, Dimon & Putkaradze 1993 : loi d'échelle gravité-viscosité, R ∝ Q^(5/8) ν^(-3/8) g^(-1/8), préfacteur 0,73 ;")
L.append("    Bhagat et al. 2018 : loi capillaire-visqueuse pour films minces, contestée par Duchesne et al. 2019.")
L.append("    Les deux encadrent grossièrement les rayons de quelques cm observés dans un évier ; l'expérience tranche.)")
L.append("")

# Film intérieur : approximation non visqueuse h(r) = a²/(2r) à vitesse U0 (borne supérieure de la vitesse)
Q = 30e-6
a_jet = 0.003
U0 = Q / (math.pi * a_jet**2)
L.append(f"   Exemple : Q = 30 mL/s, jet de rayon {a_jet*1000:.0f} mm → vitesse du jet U0 = {U0:.2f} m/s")
L.append(f"   {'r':>7} | {'h film (mm)':>11} | {'c=√(gh) (cm/s)':>15} | {'Froude U0/c':>11}   (film non visqueux h = a²/2r : borne haute de U)")
D["film"] = []
for r in (0.01, 0.02, 0.03):
    h = a_jet**2 / (2 * r)
    cg = math.sqrt(g0 * h)
    D["film"].append({"r_m": r, "h_mm": h * 1000, "c_cm_s": cg * 100, "Fr": U0 / cg})
    L.append(f"   {r*100:>4.0f} cm | {h*1000:>11.3f} | {cg*100:>15.1f} | {U0/cg:>11.1f}")
L.append("   La viscosité freine le film (Watson 1964) : U décroît avec r. Angle de Mach attendu, sin θ = c/U,")
L.append("   pour les ondes capillaires-gravité les plus lentes (c_min = 23 cm/s) :")
D["mach"] = []
for U in (1.0, 0.6, 0.4, 0.3, 0.25):
    th = math.degrees(math.asin(min(1.0, c_min / U)))
    D["mach"].append({"U": U, "theta_deg": th})
    L.append(f"     U = {U:4.2f} m/s → demi-angle θ = {th:4.1f}°")
L.append("     (θ → 90° quand U → c : le sillage en V s'ouvre puis disparaît — c'est le passage de l'horizon)")
h_ext, r_ext = 0.003, 0.05
U_ext = Q / (2 * math.pi * r_ext * h_ext)
Fr_ext = U_ext / math.sqrt(g0 * h_ext)
L.append(f"   extérieur du ressaut (h ≈ {h_ext*1000:.0f} mm à r = {r_ext*100:.0f} cm) : U = {U_ext*100:.1f} cm/s, "
         f"c = {math.sqrt(g0*h_ext)*100:.1f} cm/s, Froude = {Fr_ext:.2f} < 1")
L.append("   → intérieur supercritique (Fr >> 1) : aucune onde de surface ne peut remonter vers le centre ;")
L.append("     extérieur sous-critique. Le ressaut est la frontière : c'est un horizon de TROU BLANC pour les ondes.")
L.append("   Mesure N1 (Jannes et al. 2011) : une aiguille plantée dans le film crée un sillage en V (cône de Mach),")
L.append("     de demi-angle θ avec sin θ = c/U ; le V s'ouvre en s'approchant du ressaut et disparaît à l'extérieur.")
L.append("     (L'angle ci-dessus utilise c_min = 23 cm/s, ondes capillaires ; il est indicatif.)")
D["exterieur"] = {"U": U_ext, "Fr": Fr_ext}
L.append("")

# ---------------------------------------------------------------- 3. tourbillon de vidange
L.append("3. Tourbillon de vidange (« draining bathtub ») : v_r = -D/r, v_θ = C/r, ondes longues c = √(gh)")
CAS = [("évier (h = 5 cm, C = 1,5e-2 m²/s, D = 1e-3 m²/s, vidange Ø 4 cm)", 0.05, 1.5e-2, 1.0e-3, 0.02),
       ("bassin de laboratoire (h = 6,25 cm, mêmes C et D, vidange Ø 4 cm) — ordres de grandeur", 0.0625, 1.5e-2, 1.0e-3, 0.02),
       ("bac de TP peu profond (h = 2 cm, C = 5e-3, D = 2e-3, vidange Ø 1 cm)", 0.02, 5.0e-3, 2.0e-3, 0.005)]
D["vortex"] = []
for nom, h, C, Dd, r_d in CAS:
    cw = math.sqrt(g0 * h)
    rH = Dd / cw
    rE = math.sqrt(C**2 + Dd**2) / cw
    r_eff = max(rH, r_d)                      # le modèle 1/r cesse d'être valable à l'intérieur de la vidange
    Om_eff = C / r_eff**2
    D["vortex"].append({"cas": nom, "c": cw, "r_horizon_m": rH, "r_ergo_m": rE, "r_vidange_m": r_d,
                        "Omega_bord": Om_eff, "f_max_m1_Hz": Om_eff / (2 * math.pi)})
    L.append(f"   {nom}")
    L.append(f"      c = {cw:.2f} m/s ; horizon r_H = D/c = {rH*1000:.1f} mm ; ergorégion r_E = √(C²+D²)/c = {rE*1000:.1f} mm")
    if rH < r_d:
        L.append(f"      r_H < rayon de vidange ({r_d*1000:.0f} mm) : l'horizon du modèle idéal tombe DANS le trou ; seule l'ergorégion est accessible")
    L.append(f"      vitesse angulaire au bord utile Ω = C/r² = {Om_eff:.0f} rad/s → amplification possible du mode m si f < m·Ω/2π = "
             f"{Om_eff/(2*math.pi):.1f} Hz (m = 1), {2*Om_eff/(2*math.pi):.1f} Hz (m = 2) — critère indicatif")
f_exp, h_exp = 3.70, 0.0625
ks = np.logspace(0, 4, 20000)
om = np.sqrt((g0 * ks + gam * ks**3 / rho) * np.tanh(ks * h_exp))
k_exp = ks[np.argmin(abs(om - 2 * math.pi * f_exp))]
L.append(f"   Mise en garde : à {f_exp} Hz dans {h_exp*100:.2f} cm d'eau (conditions de Torres et al. 2017), "
         f"λ = {2*math.pi/k_exp*100:.1f} cm et k·h = {k_exp*h_exp:.1f} :")
L.append("   ce N'EST PAS le régime d'eau peu profonde (k·h << 1) ; les ondes sont dispersives et l'analogie avec une")
L.append("   métrique effective n'est qu'approchée. Dans un évier, l'horizon (mm) tombe dans le trou de vidange.")
D["torres_kh"] = float(k_exp * h_exp)
L.append("")

# ---------------------------------------------------------------- 4. température de Hawking analogue
def T_analog(grad):               # grad = |d(v - c)/dx| à l'horizon, en s^-1
    return hbar * grad / (2 * math.pi * kB)

L.append("4. Température de Hawking analogue  T = ħ·κ/(2π·k_B), κ = |d(v-c)/dx| à l'horizon")
D["hawking"] = {}
for nom, grad, Tmilieu in (("canal ou ressaut dans l'eau (κ ≈ 10 s⁻¹)", 10.0, 293.0),
                           ("ressaut très raide (κ ≈ 1000 s⁻¹)", 1e3, 293.0),
                           ("condensat de Bose-Einstein (κ ≈ 290 s⁻¹)", 290.0, 1e-9)):
    T = T_analog(grad)
    D["hawking"][nom] = {"T_K": T, "rapport_au_milieu": T / Tmilieu}
    L.append(f"   {nom:<44} T_H = {sci(T)} K   (milieu à {Tmilieu:g} K → rapport {T/Tmilieu:.1e})")
for nom, M in (("trou noir de 4,4e12 kg (valeur retenue, E2)", 4.4e12), ("trou noir d'une masse solaire", M_soleil)):
    T = hbar * c**3 / (8 * math.pi * G * M * kB)
    D["hawking"][nom] = {"T_K": T}
    L.append(f"   {nom:<44} T_H = {sci(T)} K")
L.append("   → dans l'eau, l'émission spontanée analogue (1e-11 K) est noyée de 13 ordres de grandeur sous l'agitation")
L.append("     thermique : seuls les effets STIMULÉS (classiques) sont mesurables (Weinfurtner et al. 2011).")
L.append("     L'émission spontanée n'a été rapportée que dans des condensats (Steinhauer 2016 ; Muñoz de Nova et al. 2019).")
L.append("")
L.append("Ce que les analogues enseignent : la cinématique des ondes sur un fond en mouvement (horizon, ergorégion,")
L.append("conversion de modes, superradiance) est robuste et indépendante de la gravitation. Ce qu'ils n'enseignent")
L.append("pas : la dynamique d'Einstein (l'écoulement n'obéit pas aux équations du champ), l'entropie des trous noirs,")
L.append("ni quoi que ce soit sur le voyage temporel. Un évier n'est pas un trou noir de Kerr.")

sauver("calc06_gravite_analogue", D, L)

# ---------------------------------------------------------------- figure
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.3))
ax = axes[0]
h, C, Dd = 0.05, 1.5e-2, 1.0e-3
cw = math.sqrt(g0 * h)
r = np.logspace(-3.2, -0.7, 400)
ax.loglog(r * 1000, Dd / r, label="|v_r| = D/r (vidange)", color="#33658a", lw=2)
ax.loglog(r * 1000, C / r, label="v_θ = C/r (rotation)", color="#f6ae2d", lw=2)
ax.loglog(r * 1000, np.sqrt(C**2 + Dd**2) / r, label="|v| total", color="#d1495b", lw=1.5, ls="--")
ax.axhline(cw, color="k", lw=1)
ax.text(1.0, cw * 1.12, f"c = √(gh) = {cw:.2f} m/s", fontsize=8)
ax.axvline(Dd / cw * 1000, color="#33658a", ls=":")
ax.axvline(math.sqrt(C**2 + Dd**2) / cw * 1000, color="#d1495b", ls=":")
ax.text(Dd / cw * 1000 * 1.05, 0.012, "horizon", rotation=90, fontsize=8, color="#33658a")
ax.text(math.sqrt(C**2 + Dd**2) / cw * 1000 * 1.05, 0.012, "ergorégion", rotation=90, fontsize=8, color="#d1495b")
ax.set_xlabel("rayon r (mm)")
ax.set_ylabel("vitesse (m/s)")
ax.set_title("Tourbillon de vidange idéalisé (h = 5 cm)\nmodèle illustratif, pas une mesure", fontsize=10)
ax.legend(fontsize=8)
ax.grid(True, which="both", alpha=0.25)

ax = axes[1]
kk = np.logspace(1, 4, 400)
for hh, col in ((0.0003, "#d1495b"), (0.003, "#f6ae2d"), (0.05, "#33658a")):
    ax.loglog(2 * math.pi / kk * 1000, c_phase(kk, hh) * 100, color=col, lw=2, label=f"h = {hh*1000:g} mm")
ax.axhline(c_min * 100, color="k", ls=":", lw=1)
ax.text(0.8, c_min * 100 * 1.08, "c_min = 23 cm/s (eau profonde)", fontsize=8)
ax.set_xlabel("longueur d'onde λ (mm)")
ax.set_ylabel("vitesse de phase (cm/s)")
ax.set_title("Dispersion des ondes de surface (gravité + capillarité)\nl'« horizon » dépend de λ : limite de l'analogie", fontsize=10)
ax.legend(fontsize=8)
ax.grid(True, which="both", alpha=0.25)
fig.tight_layout()
fig.savefig(fig_chemin("calc06_gravite_analogue.png"), dpi=150)
print("figure :", fig_chemin("calc06_gravite_analogue.png"))

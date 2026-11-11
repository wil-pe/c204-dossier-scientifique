#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-09 — Effet Sagnac et gyromètres optiques ; différence avec l'entraînement des référentiels
(Lense-Thirring).

Calcule :
  1. le déphasage Sagnac Δφ = 8πAΩ/(λc) (anneau) et 2πLDΩ/(λc) (bobine de fibre) ;
  2. l'expérience de Michelson-Gale (1925) et la fréquence de battement d'un gyrolaser géant ;
  3. l'entraînement des référentiels : Terre (surface, Gravity Probe B) ; trou noir de Kerr extrémal isolé
     (spin seul) et paire de trous noirs en orbite (moment orbital), à 1 m, pour les masses retenues
     (3,9–5,1e12 kg par singularité ; cas « C204 », affirmation NON tenue pour vraie) ;
  4. la comparaison avec la sensibilité des gyromètres réels.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from constantes import (G, c, GM_terre, R_terre, Omega_terre, J_terre, C204, ENTRAXE_M, sauver, fig_chemin, sci)

L, D = [], {}
deg_h = math.radians(1.0) / 3600.0          # 1 °/h en rad/s
L.append("EXP-09 — EFFET SAGNAC ET ENTRAÎNEMENT DES RÉFÉRENTIELS")
L.append("=" * 72)
L.append(f"Rotation de la Terre : Ω_T = {Omega_terre:.4e} rad/s = {Omega_terre/deg_h:.2f} °/h")
L.append("")

# ---------------------------------------------------------------- 1. Sagnac
def dphi_anneau(A, Om, lam, N=1):
    return 8 * math.pi * N * A * Om / (lam * c)

def dphi_fibre(Lf, Dm, Om, lam):
    return 2 * math.pi * Lf * Dm * Om / (lam * c)

lat = 48.85
L.append("1. Déphasage Sagnac")
D["sagnac"] = []
CAS = [
    ("Interféromètre de table 1 m × 1 m, He-Ne 633 nm, plateau tournant à 1 rad/s", dphi_anneau(1.0, 1.0, 633e-9)),
    ("Même interféromètre, rotation terrestre (latitude 48,85°)", dphi_anneau(1.0, Omega_terre * math.sin(math.radians(lat)), 633e-9)),
    ("Bobine de fibre 200 m, Ø 10 cm, 1550 nm, plateau à 0,1 rad/s (≈ 5,7 °/s)", dphi_fibre(200.0, 0.10, 0.1, 1550e-9)),
    ("Bobine de fibre 1 km, Ø 10 cm, 1550 nm, rotation terrestre complète", dphi_fibre(1000.0, 0.10, Omega_terre, 1550e-9)),
    ("Bobine de fibre 1 km, Ø 10 cm, 1550 nm, 0,01 °/h (classe navigation)", dphi_fibre(1000.0, 0.10, 0.01 * deg_h, 1550e-9)),
]
for nom, dp in CAS:
    D["sagnac"].append({"cas": nom, "dphi_rad": dp, "franges": dp / (2 * math.pi)})
    L.append(f"   {nom:<78} Δφ = {sci(dp)} rad ({sci(dp/(2*math.pi))} frange)")
L.append("")

# Michelson-Gale 1925 : rectangle 2010 ft × 1113 ft, Clearing (Illinois), latitude 41°46'
ft = 0.3048
A_mg = 2010 * ft * 1113 * ft
phi_mg = math.radians(41 + 46 / 60)
lam_mg = 570e-9
fr_mg = 4 * A_mg * Omega_terre * math.sin(phi_mg) / (lam_mg * c)
L.append("2. Vérifications sur des expériences publiées")
L.append(f"   Michelson-Gale-Pearson (1925) : rectangle 2010 ft × 1113 ft (A = {A_mg:.3e} m²), latitude 41°46′, λ ≈ 570 nm")
L.append(f"   décalage calculé 4AΩ·sinφ/(λc) = {fr_mg:.3f} frange (publié : 0,236 ± 0,002 calculé ; 0,230 ± 0,005 observé)")
# Gyrolaser G (Wettzell) : carré de 4 m de côté, 633 nm, latitude 49,14°
A_g, P_g = 16.0, 16.0
f_g = 4 * A_g * Omega_terre * math.sin(math.radians(49.1449)) / (632.8e-9 * P_g)
L.append(f"   Gyrolaser « G » (carré 4 m × 4 m, 633 nm, latitude 49,14°) : battement 4AΩ·sinφ/(λP) = {f_g:.1f} Hz (valeur connue ≈ 348,5 Hz)")
D["michelson_gale_frange"] = fr_mg
D["gyrolaser_G_Hz"] = f_g
L.append("")

# ---------------------------------------------------------------- 3. Lense-Thirring
L.append("3. Entraînement des référentiels (Lense-Thirring) — ordre de grandeur Ω_LT ~ G·J/(c²r³)")
Om_LT_terre = G * J_terre / (c**2 * R_terre**3)
mas_an = math.radians(1e-3 / 3600) / 3.15576e7
gpb_fd, gpb_geo = 39.2 * mas_an, 6606.1 * mas_an
L.append(f"   Terre, à la surface : G·J/(c²R³) = {sci(Om_LT_terre)} rad/s = {Om_LT_terre/Omega_terre:.1e} × Ω_T")
L.append(f"   Gravity Probe B (orbite polaire à 642 km) : entraînement prédit 39,2 mas/an = {sci(gpb_fd)} rad/s "
         f"(mesuré 37,2 ± 7,2) ; précession géodétique 6606,1 mas/an = {sci(gpb_geo)} rad/s (mesuré 6601,8 ± 18,3)")
D["LT"] = {"terre_surface_rad_s": Om_LT_terre, "GPB_frame_dragging_rad_s": gpb_fd, "GPB_geodetique_rad_s": gpb_geo}
m_lo, m_hi = C204["masse_TN_kg"]
L.append("   (a) SPIN SEUL — trou noir de Kerr EXTRÉMAL isolé (J_max = G·M²/c), à r = 1 m, champ lointain 2GJ/(c²r³) :")
for nom, M in (("ancienne valeur v1, 1e12 kg", 1e12), ("valeur retenue basse, 3,9e12 kg", m_lo),
               ("valeur retenue haute, 5,1e12 kg", m_hi)):
    Jmax = G * M**2 / c
    Om = 2 * G * Jmax / (c**2 * 1.0**3)
    D["LT"][f"spin_{M:.1e}"] = {"J_max": Jmax, "Omega_rad_s": Om}
    L.append(f"     {nom:<32} : J_max = {sci(Jmax)} kg·m²/s ; Ω_LT(1 m) = {sci(Om)} rad/s "
             f"= {Om/Om_LT_terre:.1e} × celui de la Terre au sol")
J_volant = 0.5 * 10.0 * 0.15**2 * 2 * math.pi * 100       # disque de 10 kg, R = 15 cm, 6000 tr/min
L.append(f"     (comparaison : un volant de 10 kg, R = 15 cm, à 6000 tr/min porte J = {J_volant:.0f} kg·m²/s)")
L.append("     → comme J_max ∝ M², le SPIN d'un micro-trou noir est dérisoire : son champ ne diffère d'un champ de")
L.append("       Schwarzschild qu'à quelques rayons gravitationnels (~1e-14 m).")
# (b) Moment cinétique ORBITAL d'une paire liée (correction n° 54 de la Red Team n° 2, erratum E15) :
#     deux masses M en orbite circulaire à la distance d : ω² = 2GM/d³ ; L = μ d² ω = (M/2)·√(2GMd).
#     Ce terme n'existe que si les deux singularités TOURNENT l'une autour de l'autre ; il est nul pour deux objets
#     tenus fixes dans des « logements » (ce que dessine le manuel). On le donne comme borne supérieure.
L.append("   (b) MOMENT ORBITAL — paire liée en orbite circulaire à l'entraxe d : L = (M/2)·√(2GMd), Ω_LT(1 m) = 2GL/(c²r³)")
L.append("       (nul si les singularités sont tenues fixes ; borne supérieure si elles orbitent librement ; à r = 1 m, soit")
L.append("        3 à 10 entraxes, la formule de champ lointain est un ordre de grandeur, la partie oscillante étant ignorée)")
D["LT"]["paire"] = []
Om_paire_max = 0.0
for nom, M in (("2 × 1e12 kg (ancienne valeur)", 1e12), ("2 × 3,9e12 kg", m_lo), ("2 × 4,4e12 kg", 4.4e12), ("2 × 5,1e12 kg", m_hi)):
    for d_ent in ENTRAXE_M:
        Lorb = (M / 2) * math.sqrt(2 * G * M * d_ent)
        Om = 2 * G * Lorb / (c**2 * 1.0**3)
        T_orb = 2 * math.pi / math.sqrt(2 * G * M / d_ent**3)
        v_orb = math.sqrt(2 * G * M / d_ent) / 2
        Om_paire_max = max(Om_paire_max, Om)
        D["LT"]["paire"].append({"cas": nom, "entraxe_m": d_ent, "L_orbital": Lorb, "Omega_rad_s": Om, "periode_ms": T_orb * 1e3})
        L.append(f"     {nom:<30} d = {d_ent:5.3f} m : L = {sci(Lorb)} kg·m²/s ; Ω_LT(1 m) = {sci(Om)} rad/s "
                 f"= {Om/Om_LT_terre:5.2f} × Terre au sol (période orbitale {T_orb*1e3:.0f} ms, vitesse {v_orb:.0f} m/s)")
D["LT"]["paire_max_rad_s"] = Om_paire_max
L.append(f"     → jusqu'à {sci(Om_paire_max)} rad/s : le terme orbital dépasse le spin de 7 ordres de grandeur et atteint l'ordre")
L.append(f"       de l'effet terrestre (1,7e-14 rad/s au sol ; {sci(gpb_fd)} rad/s mesuré en orbite par Gravity Probe B).")
L.append("       Il reste sans effet causal, hors de portée de tout gyromètre transportable (≥ 5e-10 rad/s) et encore")
L.append("       ≈ 13 fois sous la résolution d'un gyrolaser géant, instrument fixe de 16 m² qu'on ne place pas à 1 m d'un véhicule.")
L.append("")

# ---------------------------------------------------------------- 4. sensibilités
CAPT = [
    ("Gyromètre MEMS de smartphone (instabilité de biais ~10 °/h)", 10 * deg_h, "N1"),
    ("Gyromètre à fibre de TP / tactique (~1 °/h)", 1.0 * deg_h, "N2"),
    ("Gyromètre à fibre de navigation (~0,01 °/h)", 0.01 * deg_h, "N3 (industrie)"),
    ("Gyromètre à fibre stratégique (~1e-4 °/h)", 1e-4 * deg_h, "N3 (industrie)"),
    ("Gyrolaser géant type G (résolution ~1e-8 Ω_T après intégration)", 1e-8 * Omega_terre, "N3"),
    ("Objectif des réseaux de gyrolasers (GINGER : ~1e-9 à 1e-10 Ω_T)", 1e-10 * Omega_terre, "N3 (projet)"),
]
L.append("4. Sensibilité des gyromètres contre signaux (ordres de grandeur indicatifs)")
D["capteurs"] = []
for nom, s, niv in CAPT:
    D["capteurs"].append({"capteur": nom, "resolution_rad_s": s, "niveau": niv})
    L.append(f"   {nom:<66} {sci(s)} rad/s  [{niv}]  → Ω_T/résolution = {Omega_terre/s:.1e}")
L.append(f"   Lense-Thirring terrestre au sol ({sci(Om_LT_terre)} rad/s) : hors de portée de tout gyromètre de laboratoire actuel ;")
L.append("   mesuré seulement dans l'espace (LAGEOS/LARES, Gravity Probe B) et dans un pulsar binaire.")
res_G = 1e-8 * Omega_terre
spin_ref = D["LT"]["spin_1.0e+12"]["Omega_rad_s"]
spin_ret = D["LT"][f"spin_{m_hi:.1e}"]["Omega_rad_s"]
L.append(f"   Écart au gyrolaser géant ({sci(res_G)} rad/s) : spin seul {sci(spin_ref)}–{sci(spin_ret)} rad/s → "
         f"{math.log10(res_G/spin_ret):.0f} à {math.log10(res_G/spin_ref):.0f} ordres de grandeur ;")
L.append(f"   paire en orbite, jusqu'à {sci(Om_paire_max)} rad/s → {math.log10(res_G/Om_paire_max):.1f} ordre de grandeur "
         f"(≈ {res_G/Om_paire_max:.0f} fois sous la résolution) : « 1 à 9 ordres de grandeur selon le terme ».")
D["ecart_gyrolaser"] = {"spin_ordres": [math.log10(res_G / spin_ret), math.log10(res_G / spin_ref)],
                        "paire_ordres": math.log10(res_G / Om_paire_max)}
L.append("")
L.append("Sagnac ≠ Lense-Thirring : l'effet Sagnac mesure la rotation de l'INSTRUMENT par rapport aux référentiels")
L.append("inertiels locaux (cinématique, relativité restreinte suffit) ; l'effet Lense-Thirring est la rotation de ces")
L.append("référentiels eux-mêmes, causée par une masse en rotation (relativité générale). Un gyromètre à fibre ne")
L.append("« détecte » donc pas un champ de Kerr ; il mesurerait au mieux la rotation mécanique d'un châssis. Même le terme")
L.append("orbital d'une paire (≤ 5e-14 rad/s) est 1e4 fois sous le meilleur gyromètre à fibre et 1e9 fois sous un MEMS.")

sauver("calc09_sagnac_lense_thirring", D, L)

# ---------------------------------------------------------------- figure
fig, ax = plt.subplots(figsize=(10.5, 5.6))
elements = [("rotation de la Terre", Omega_terre, "#2e8b57"),
            ("Lense-Thirring, Terre au sol", Om_LT_terre, "#2e8b57"),
            ("entraînement mesuré par Gravity Probe B", gpb_fd, "#2e8b57"),
            ("précession géodétique (GP-B)", gpb_geo, "#2e8b57"),
            ("spin seul, Kerr extrémal 1e12 kg, à 1 m", spin_ref, "#d1495b"),
            ("spin seul, Kerr extrémal 5,1e12 kg, à 1 m", spin_ret, "#d1495b"),
            ("paire en orbite 2 × 1e12 kg (0,30 m), à 1 m", 2 * G * (1e12 / 2) * math.sqrt(2 * G * 1e12 * 0.30) / c**2, "#d1495b"),
            ("paire en orbite 2 × 5,1e12 kg (0,30 m), à 1 m", Om_paire_max, "#d1495b")]
elements += [(n.split(" (")[0], s, "#33658a") for n, s, _ in CAPT]
elements.sort(key=lambda t: t[1])
ax.barh(range(len(elements)), [e[1] for e in elements], color=[e[2] for e in elements])
ax.set_yticks(range(len(elements)))
ax.set_yticklabels([e[0] for e in elements], fontsize=8)
ax.set_xscale("log")
ax.set_xlabel("vitesse angulaire (rad/s)")
ax.set_title("EXP-09 — Rotations : signaux réels (vert), résolution des gyromètres (bleu),\n"
             "micro-trous noirs hypothétiques : spin seul et paire en orbite (rouge) — calcul illustratif", fontsize=10)
ax.grid(True, which="both", axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig(fig_chemin("calc09_rotations.png"), dpi=150)
print("figure :", fig_chemin("calc09_rotations.png"))

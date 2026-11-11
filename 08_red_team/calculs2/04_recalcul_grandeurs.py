#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Red Team n° 2 — Tâche 2. Recalcul indépendant des grandeurs clés du tableau de cohérence inter-équipes.
Aucun code d'équipe n'est importé. Les coefficients de corps gris viennent de 03_corps_gris_independant.py
(journaux/corps_gris_independant.json), eux-mêmes recalculés ici. Sortie : journaux/recalcul_grandeurs.{txt,json}"""
import json, math, os

ICI = os.path.dirname(os.path.abspath(__file__))
# CODATA 2018
G, c, hbar, kB = 6.67430e-11, 2.99792458e8, 1.054571817e-34, 1.380649e-23
e, eps0, mu0, me = 1.602176634e-19, 8.8541878128e-12, 1.25663706212e-6, 9.1093837015e-31
g0, MeV, an = 9.80665, 1.602176634e-13, 365.25 * 86400
alpha_fs = e * e / (4 * math.pi * eps0 * hbar * c)
sigma_SB = math.pi**2 * kB**4 / (60 * hbar**3 * c**2)
M_sol, M_jup, M_terre, L_sol = 1.98847e30, 1.89813e27, 5.9722e24, 3.828e26

cg = json.load(open(os.path.join(ICI, "journaux", "corps_gris_independant.json")))
c0, c12, c1, c2 = (cg[k]["P_par_ddl"] for k in ("0", "0.5", "1", "2"))
K = hbar * c**6 / G**2                       # W.kg²
R, T = {}, []
def note(cle, val, unite="", com=""):
    R[cle] = val
    T.append(f"{cle:<62} {val:>14.4e} {unite:<10} {com}" if isinstance(val, float) else f"{cle:<62} {str(val):>14} {unite:<10} {com}")

# ---------- 1. Hawking : coefficients alpha selon les espèces émises
a_photon_cn = 1 / (15360 * math.pi)                                   # corps noir, photons seuls (dossier §6)
a_lourd = 2 * c1 + 2 * c2 + 6 * c12                                   # gamma, graviton, 3 nu (2 états chacun)
a_e = a_lourd + 4 * c12                                               # + e± (4 ddl)
a_e_dirac = a_e + 6 * c12                                             # + neutrinos droits si neutrinos de Dirac
# Modèle standard complet (T >> 100 GeV) : 90 ddl de fermions de Weyl-équivalents, 24 vecteurs transverses, 4 scalaires (doublet de Higgs)
a_MS_4s = 90 * c12 + 24 * c1 + 4 * c0 + 2 * c2
a_MS_1s = 90 * c12 + 27 * c1 + 1 * c0 + 2 * c2                         # variante : W, Z massifs à 3 polarisations « spin 1 », 1 Higgs
for n, a in [("alpha photons corps noir (dossier)", a_photon_cn), ("alpha gamma+graviton+3nu", a_lourd), ("alpha + e± (10^12–10^14 kg)", a_e),
             ("alpha + e± + nu droits (Dirac)", a_e_dirac), ("alpha Modèle standard (4 scalaires)", a_MS_4s), ("alpha Modèle standard (1 scalaire, 27 vecteurs)", a_MS_1s)]:
    note(n, a, "", f"P·M² = {a*K:.3e} W·kg²")
note("fraction neutrinos (régime e±)", 6 * c12 / a_e); note("fraction e± (régime e±)", 4 * c12 / a_e)
note("fraction photons (régime e±)", 2 * c1 / a_e); note("fraction gravitons (régime e±)", 2 * c2 / a_e)
note("rapport puissance réelle / formule photons corps noir", a_e / a_photon_cn)

def M_de_P(P, a): return math.sqrt(a * K / P)
def tau(M, a): return M**3 / (3 * a * hbar * c**4 / G**2)             # alpha constant
def kT_MeV(M): return hbar * c**3 / (8 * math.pi * G * M) / MeV
for P in (3e8, 4e8, 5e8):
    note(f"M pour P = {P/1e6:.0f} MW, photons corps noir", M_de_P(P, a_photon_cn), "kg")
    note(f"M pour P = {P/1e6:.0f} MW, toutes espèces (régime e±)", M_de_P(P, a_e), "kg", f"kT = {kT_MeV(M_de_P(P, a_e)):.2f} MeV ; r_s = {2*G*M_de_P(P, a_e)/c**2*1e15:.2f} fm")
    note(f"M pour P = {P/1e6:.0f} MW, neutrinos de Dirac", M_de_P(P, a_e_dirac), "kg")
note("pic de puissance photons E/kT (calculé)", cg["1"]["pic_puissance_E_sur_kT"], "", "⇒ 12,5–16,5 MeV pour kT = 2,07–2,71 MeV")
note("masse d'un trou « à rayons X » (kT = 10 keV)", hbar * c**3 / (8 * math.pi * G * 1e-2 * MeV), "kg", f"P = {a_lourd*K/(hbar*c**3/(8*math.pi*G*1e-2*MeV))**2:.2e} W")

# ---------- 2. Masse pour 1,5–2 g à 1–3,7 m
for a_g in (1.5, 2.0):
    for r in (1.0, 3.0, 3.7):
        note(f"M (totale) pour {a_g} g à {r} m", a_g * g0 * r * r / G, "kg")
note("g à 1 m de 2 × 4,4e12 kg", 2 * G * 4.4e12 / g0, "g0"); note("g à 1 m d'une masse de 3,9e12 kg", G * 3.9e12 / g0, "g0"); note("g à 1 m d'une masse de 5,1e12 kg", G * 5.1e12 / g0, "g0")

# ---------- 3. Durées de vie
for M in (100.0, 113.5, 227.0):
    note(f"durée de vie {M} kg (MS, 4 scalaires)", tau(M, a_MS_4s), "s", f"variante 1 scalaire : {tau(M, a_MS_1s):.3e} s ; facteur 21 « grandes masses » (erroné ici) : {tau(M, a_e):.3e} s ; corps noir photons : {tau(M, a_photon_cn):.3e} s")
note("durée de vie 1e12 kg (alpha régime e±, constant)", tau(1e12, a_e) / an, "ans", f"corps noir photons : {tau(1e12, a_photon_cn)/an:.3e} ans")
note("durée de vie 4e12 kg", tau(4e12, a_e) / an, "ans"); note("durée de vie 5e12 kg", tau(5e12, a_e) / an, "ans")
note("puissance 100 kg (MS)", a_MS_4s * K / 1e4, "W"); note("puissance 1e12 kg", a_e * K / 1e24, "W")

# ---------- 4. Charge
QsurM = math.sqrt(4 * math.pi * eps0 * G)
note("Q/M extrémal", QsurM, "C/kg"); note("charge extrémale 1e12 kg", QsurM * 1e12, "C")
note("borne « noyau ponctuel » Z ~ 1/alpha", 1 / alpha_fs, "e", "instabilité du vide de Dirac (ordre de grandeur) — B, D")
note("fluctuation thermique Z_rms = 1/sqrt(4 pi alpha)", 1 / math.sqrt(4 * math.pi * alpha_fs), "e", "indépendante de M ; Page 1977 donne ≈ 6 e avec corps gris (valeur à vérifier dans l'article)")
for M in (1e12, 4.5e12):
    rs = 2 * G * M / c**2
    U = e * e / (4 * math.pi * eps0 * rs) / MeV
    note(f"énergie coulombienne par charge à l'horizon, M = {M:.1e} kg", U, "MeV", f"critère H (e·Q/4πε0 r_s < m_e c²) ⇒ Q < {0.511/U:.1f} e ; avec 2 m_e c² : {1.022/U:.1f} e")
note("champ de sustentation, charge extrémale", g0 / QsurM, "V/m")
for (M, Z) in ((1e12, 137), (4e12, 137), (4.4e12, 6.14), (1e12, 170), (100, 6.14)):
    note(f"champ de sustentation M = {M:.1e} kg, Q = {Z} e", M * g0 / (Z * e), "V/m")
note("champ de Schwinger", me**2 * c**3 / (e * hbar), "V/m")
for d in (0.01, 0.005):
    note(f"Penning B_min = sqrt(2g/d)/(Q/M), d = {d} m", math.sqrt(2 * g0 / d) / QsurM, "T")

# ---------- 5. Débit de dose (photons primaires seuls ; kerma dans l'eau, sans accumulation)
mu_en = {"100 keV": 2.546e-3, "1 MeV": 3.103e-3, "10 MeV": 1.566e-3, "15 MeV": 1.441e-3, "20 MeV": 1.382e-3}   # m²/kg, eau (NIST XCOM, de mémoire ±2 %)
Pg = 2 * c1 / a_e * 4e8
note("puissance photons d'une singularité de 400 MW", Pg, "W")
for r in (1.0, 3.0):
    note(f"dose gamma primaires à {r} m (15 MeV, 1 singularité 400 MW)", Pg / (4 * math.pi * r * r) * mu_en["15 MeV"], "Gy/s")
    note(f"dose si 400 MW entièrement en X de 100 keV, à {r} m (lecture F)", 4e8 / (4 * math.pi * r * r) * mu_en["100 keV"], "Gy/s")
    note(f"dose si 400 MW entièrement en gamma de 10 MeV, à {r} m", 4e8 / (4 * math.pi * r * r) * mu_en["10 MeV"], "Gy/s")
# e± : fluence d'énergie × (S/rho)/E, S/rho ≈ 2 MeV cm²/g à ~10 MeV  -> 0,02 m²/kg par unité de fluence d'énergie (E = 10 MeV)
Pe = 4 * c12 / a_e * 4e8
note("dose e± en surface à 1 m si rien ne les arrête (ordre de grandeur)", Pe / (4 * math.pi) * (2.0 / 10.0) * 0.1, "Gy/s", "S/ρ ≈ 2 MeV·cm²/g, E ≈ 10 MeV")
note("temps pour 5 Gy à 1 m (gamma seuls)", 5 / (Pg / (4 * math.pi) * mu_en["15 MeV"]), "s")

# ---------- 6. Dilatation, CTC, entraînement
for (M, lab) in ((2.94e11, "2 g à 1 m"), (1e12, "1e12 kg"), (2e12, "2 × 1e12 kg"), (4e12, "4e12 kg"), (8.8e12, "2 × 4,4e12 kg"), (227.0, "227 kg")):
    note(f"Gamma − 1 = GM/(r c²) à 1 m, {lab}", G * M / c**2, "")
note("borne 2 g sur 3,7 m : 2 g L / c²", 2 * g0 * 3.7 / c**2, ""); note("Gamma revendiqué", 87660.0, "")
note("r/r_s − 1 pour Gamma = 87 660", 1 / (1 - 87660.0**-2) - 1, "")
note("M pour Gamma = 87 660 à 1 m (statique, Schwarzschild)", c**2 / (2 * G) * (1 - 87660.0**-2), "kg", f"= {c**2/(2*G)/M_terre:.0f} M_Terre")
note("M pour anneau de Kerr a = GM/c² = 1 m", c**2 / G, "kg", f"= {c**2/G/M_jup:.2f} M_Jupiter")
note("M pour ergosphère 2GM/c² = 3,35 m", 3.35 * c**2 / (2 * G), "kg", f"= {3.35*c**2/(2*G)/M_jup:.2f} M_Jupiter")
note("seuil de Tipler c²/8G", c**2 / (8 * G), "kg/m")
J_spin = G * 1e12**2 / c
note("Lense-Thirring 2GJ/(c² r³), spin extrémal d'un trou de 1e12 kg, r = 1 m", 2 * G * J_spin / c**2, "rad/s")
for (M, d) in ((1e12, 0.3), (4.4e12, 0.3), (1e12, 0.098)):
    Om = math.sqrt(2 * G * M / d**3); Jo = 0.5 * M * d * d * Om
    note(f"Lense-Thirring orbital, 2 × {M:.1e} kg, d = {d} m, r = 1 m (axe)", 2 * G * Jo / c**2, "rad/s", f"Ω_orb = {Om:.1f} rad/s ({Om/2/math.pi:.1f} Hz) ; J_orb = {Jo:.2e}")
note("déviation lumière 4GM/(c² b), 1e12 kg, b = 1 m", 4 * G * 1e12 / c**2, "rad")

# ---------- 7. Champ magnétique « gravitant » : trois définitions rencontrées
note("B tel que 8πG u/c⁴ = 1/L², L = 1 m (B, courbure d'ordre 1)", c**2 * math.sqrt(mu0 / (4 * math.pi * G)), "T")
E28 = 2 * g0 / G * c**2
note("énergie EM équivalente à la masse donnant 2 g à 1 m", E28, "J")
note("B pour loger cette énergie dans une sphère de 10 cm (C)", math.sqrt(2 * mu0 * E28 / (4 / 3 * math.pi * 0.1**3)), "T")
note("B pour loger cette énergie dans une sphère de 1 m", math.sqrt(2 * mu0 * E28 / (4 / 3 * math.pi)), "T")
note("B dont l'énergie « pèse » autant que l'eau (F)", math.sqrt(2 * mu0 * 1000 * c**2), "T")

# ---------- 8. Énergie de fabrication
for (M, lab) in ((2.94e11, "masse totale donnant 2 g à 1 m (steelman)"), (2 * 2.94e11, "2 × 2,94e11 kg (lecture C : chaque trou donne 2 g)"), (2e12, "2 × 1e12 kg (G, masses photons seuls)"),
                 (2 * 3.9e12, "2 × 3,9e12 kg (500 MW chacun)"), (2 * 4.4e12, "2 × 4,4e12 kg (400 MW chacun)"), (2 * 5.1e12, "2 × 5,1e12 kg (300 MW chacun)"), (227.0, "227 kg")):
    note(f"M c², {lab}", M * c * c, "J", f"= {M*c*c/L_sol:.0f} s de luminosité solaire")

# ---------- 9. Coalescence (Peters), masses égales
def tc(M, d): return 5 / 256 * c**5 * d**4 / (G**3 * M * M * 2 * M)
for (M, d) in ((1e12, 0.3), (4.4e12, 0.3), (5e12, 0.1), (1e12, 0.098), (1e12, 0.131), (4.4e12, 0.098)):
    note(f"temps de coalescence 2 × {M:.1e} kg, d = {d} m", tc(M, d), "s", f"= {tc(M, d)/an:.2e} ans")

# ---------- 10. Énergie négative
note("Morris-Thorne : tension c⁴/(8πG b²), b = 1 m", c**4 / (8 * math.pi * G), "Pa")
note("Morris-Thorne : masse exotique −b c²/(2G), b = 1 m", -c**2 / (2 * G), "kg")
note("ordre de grandeur −R c²/G, R = 3 m (G, steelman)", -3 * c**2 / G, "kg")
def alcub(Rb, D): return -c**4 / (12 * G) * (Rb * Rb / D + D / 12)
note("Alcubierre R = 3,7 m, paroi 1 m, v = c (B)", alcub(3.7, 1.0) / c**2, "kg", f"{alcub(3.7,1.0):.2e} J")
note("Alcubierre R = 3 m, paroi 0,25 m, v = c (D)", alcub(3.0, 0.25) / c**2, "kg", f"{alcub(3.0,0.25):.2e} J")
cas = lambda d: -math.pi**2 * hbar * c / (720 * d**4)
note("Casimir, densité à d = 1 µm", cas(1e-6), "J/m³"); note("Casimir, énergie par m² à d = 10 nm", cas(1e-8) * 1e-8, "J/m²")

# ---------- 11. Thermique : puissance compatible avec 38–49 °C, selon les dimensions du coffre
def surf(L, P, H): return 2 * (L * P + L * H + P * H)
dims = {"H1 (dossier §7) 1,20 × 0,36 × 0,30": (1.20, 0.36, 0.30), "A  0,85 × 0,26 × 0,285": (0.85, 0.26, 0.285), "E  0,85 × 0,26 × 0,24": (0.85, 0.26, 0.2416),
        "A borne basse 0,60 × 0,18 × 0,20": (0.60, 0.18, 0.20), "A borne haute 1,15 × 0,35 × 0,37": (1.15, 0.35, 0.37)}
for nom, (L, P, H) in dims.items():
    S, V = surf(L, P, H), L * P * H
    for (Tamb, hconv) in ((25.0, 5.0),):
        Pmin = S * (hconv * (38 - Tamb) + 0.9 * sigma_SB * ((38 + 273.15)**4 - (Tamb + 273.15)**4))
        Pmax = S * (hconv * (49 - Tamb) + 0.9 * sigma_SB * ((49 + 273.15)**4 - (Tamb + 273.15)**4))
    Teq_lo = (132e6 / (S * sigma_SB))**0.25; Teq_hi = (220e6 / (S * sigma_SB))**0.25
    note(f"coffre {nom} : surface", S, "m²", f"volume {V:.3f} m³ ; ρ(227 kg) = {227/V:.0f} kg/m³ ; P(38–49 °C, amb. 25 °C, h = 5, ε = 0,9) = {Pmin:.0f}–{Pmax:.0f} W ; T éq. radiatif pour 132–220 MW = {Teq_lo:.0f}–{Teq_hi:.0f} K")

open(os.path.join(ICI, "journaux", "recalcul_grandeurs.txt"), "w", encoding="utf-8").write("\n".join(T) + "\n")
json.dump(R, open(os.path.join(ICI, "journaux", "recalcul_grandeurs.json"), "w"), indent=1, ensure_ascii=False)
print("\n".join(T))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-04 — Cartographie gravimétrique locale : analogue réel de l'« instantané de gravité »
du système VGL revendiqué (variable gravity lock).

Calcule :
  1. les gradients naturels de g (altitude, latitude), les marées, l'effet de masses proches ;
  2. la résolution réelle de capteurs accessibles (smartphone, MEMS, pendule) et professionnels ;
  3. ce qu'il faudrait pour « reconnaître un lieu » à partir de g ;
  4. à quelle distance une masse de type « C204 » (1e11–1e12 kg, valeur DÉDUITE et non établie)
     serait détectable par chacun de ces capteurs.

Unités : 1 Gal = 1e-2 m/s² ; 1 mGal = 1e-5 m/s² ; 1 µGal = 1e-8 m/s².
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from constantes import (G, g0, GM_terre, R_terre, M_soleil, C204, sauver, fig_chemin, sci)

uGal = 1e-8
L, D = [], {}
L.append("EXP-04 — GRAVIMÉTRIE LOCALE ET « INSTANTANÉ DE GRAVITÉ »")
L.append("=" * 72)

# ---------------------------------------------------------------- 1. variations naturelles
def g_normal(phi_deg):
    """Pesanteur normale GRS80 (formule de Somigliana), m/s²."""
    s2 = math.sin(math.radians(phi_deg))**2
    return 9.7803267715 * (1 + 0.0019318513639 * s2) / math.sqrt(1 - 0.00669438002290 * s2)

air_libre = 2 * GM_terre / R_terre**3                    # s^-2
dgdphi = (g_normal(45.0005) - g_normal(44.9995)) / math.radians(0.001)   # m/s² par rad
dg_nord = dgdphi / R_terre                               # m/s² par mètre vers le nord à 45°
bouguer = 2 * math.pi * G * 2670.0                       # plateau de Bouguer, par mètre d'épaisseur
M_lune, d_lune = 7.342e22, 3.844e8
ua = 1.495978707e11
maree_lune = 2 * G * M_lune * R_terre / d_lune**3
maree_soleil = 2 * G * M_soleil * R_terre / ua**3
facteur_delta = 1.16
maree_cc = 1.5 * (maree_lune + maree_soleil) * facteur_delta   # crête à crête (zénith ↔ horizon : 2 → -1 ⇒ ×1,5)

L.append("1. Variations naturelles de g")
L.append(f"   g(équateur) = {g_normal(0):.5f} ; g(45°) = {g_normal(45):.5f} ; g(pôle) = {g_normal(90):.5f} m/s² "
         f"(écart pôle-équateur {1e2*(g_normal(90)-g_normal(0)):.2f} Gal)")
L.append(f"   gradient à l'air libre       : 2GM/R³ = {air_libre:.3e} s⁻² = {air_libre/uGal:.0f} µGal/m (≈ 3 µGal/cm)")
L.append(f"   gradient nord-sud à 45°      : {dg_nord/uGal:.2f} µGal/m ({dg_nord*1e3/1e-5:.2f} mGal/km)")
L.append(f"   plateau de Bouguer (2670 kg/m³) : {bouguer/uGal:.0f} µGal par mètre de roche")
L.append(f"   marée lunaire (max vertical) : {maree_lune/uGal:.0f} µGal ; solaire : {maree_soleil/uGal:.0f} µGal ; "
         f"crête à crête avec facteur élastique 1,16 : ≈ {maree_cc/uGal:.0f} µGal")
L.append("   pression atmosphérique       : ≈ -0,3 µGal/hPa (admittance usuelle) → ±10 µGal selon la météo")
D["gradients"] = {"air_libre_uGal_m": air_libre / uGal, "nord_sud_45_uGal_m": dg_nord / uGal,
                  "bouguer_uGal_m": bouguer / uGal, "maree_cc_uGal": maree_cc / uGal}
L.append("")

L.append("   Masses proches (attraction verticale maximale G·M/r²) :")
masses = [("personne de 80 kg à 1 m", 80.0, 1.0), ("voiture de 1500 kg à 2 m", 1500.0, 2.0),
          ("bloc de béton de 1 m³ (2400 kg) à 1 m", 2400.0, 1.0), ("camion de 20 t à 5 m", 2e4, 5.0),
          ("immeuble de 10 000 t à 30 m", 1e7, 30.0), ("unité C204 revendiquée (227 kg) à 1 m", 227.0, 1.0)]
D["masses_proches"] = []
for nom, M, r in masses:
    a = G * M / r**2
    D["masses_proches"].append({"cas": nom, "a_uGal": a / uGal})
    L.append(f"     {nom:<42} {a/uGal:8.3f} µGal")
dz, Rv, drho = 3.0, 1.0, -2000.0
vide = 2 * math.pi * G * abs(drho) * Rv**2 / dz
L.append(f"     galerie vide (Ø 2 m, axe à 3 m de profondeur, Δρ = -2000 kg/m³) : -{vide/uGal:.1f} µGal à l'aplomb")
D["galerie_uGal"] = vide / uGal
L.append("")

# ---------------------------------------------------------------- 2. capteurs
# (nom, bruit blanc [m/s²/√Hz], plancher pratique après 100 s [m/s²] (dérive, température, inclinaison), coût, niveau)
CAPTEURS = [
    ("Accéléromètre de smartphone",             1.5e-3,  2e-3,  "0 € (application phyphox)", "N1"),
    ("Accéléromètre MEMS bas bruit (type ADXL355)", 2.5e-4, 2e-4, "40–80 € + microcontrôleur", "N1"),
    ("Pendule simple soigné (L ≈ 1 m, chrono optique)", None, 1e-3, "20–80 €", "N1"),
    ("Pendule réversible de Kater (TP)",          None,  1e-4,  "matériel de TP", "N2"),
    ("Gravimètre MEMS de recherche (Middlemiss et al. 2016 : 40 µGal/√Hz)", 40 * uGal, 4e-7, "prototype", "N3"),
    ("Gravimètre relatif à ressort (type CG-5/CG-6)", None, 5 * uGal, "≈ 100 k€ (prêt/location en géophysique)", "N2/N3"),
    ("Gravimètre absolu à chute de coin de cube (type FG5)", None, 2 * uGal, "plusieurs centaines de k€", "N3"),
    ("Gravimètre à atomes froids (Ménoret et al. 2018 : < 1 µGal)", 50 * uGal, 1 * uGal, "plusieurs centaines de k€", "N3"),
    ("Gravimètre supraconducteur (observatoire)", None,  0.01 * uGal, "observatoire", "N3"),
]
L.append("2. Résolution réaliste des capteurs (σ après ~100 s de moyenne ; ordres de grandeur indicatifs)")
L.append(f"   {'capteur':<70}{'σ (m/s²)':>10}{'σ (µGal)':>12}  {'Δh équivalent':>14}  niveau")
D["capteurs"] = []
for nom, bruit, plancher, cout, niv in CAPTEURS:
    blanc = bruit / math.sqrt(100.0) if bruit else 0.0
    sig = max(blanc, plancher)
    dh = sig / air_libre
    D["capteurs"].append({"capteur": nom, "sigma_m_s2": sig, "sigma_uGal": sig / uGal, "dh_equivalent_m": dh,
                          "cout": cout, "niveau": niv})
    L.append(f"   {nom:<70}{sci(sig,2):>10}{sig/uGal:>12.3g}  {dh:>12.3g} m  {niv}")
L.append("   (Δh équivalent = dénivelé donnant la même variation par le gradient à l'air libre)")
L.append("   Smartphone : le bruit blanc (≈150 µg/√Hz) se moyenne, mais la dérive thermique du biais (0,1–1 mg/K),")
L.append("   l'erreur de facteur d'échelle (~0,5 %) et l'inclinaison (1° → 1,5e-4 g) fixent le plancher ≈ 2e-3 m/s².")
L.append("")

# pendule : propagation
Lp, dL, T, dT_chrono, Nper = 1.000, 1e-4, 2 * math.pi * math.sqrt(1.0 / g0), 1e-4, 100
rel_T = dT_chrono / (Nper * T)
rel_abs = math.sqrt((2 * rel_T)**2 + (dL / Lp)**2)
amp = math.radians(3.0)
corr_amp = amp**2 / 16
dil = 1.2e-5 * 5
L.append("   Pendule simple (L = 1,000 m ± 0,1 mm ; 100 périodes chronométrées à ±0,1 ms) :")
L.append(f"     période T = {T:.4f} s ; δT/T = {rel_T:.1e} ; δg/g absolu = √[(2δT/T)² + (δL/L)²] = {rel_abs:.1e} "
         f"→ δg ≈ {rel_abs*g0:.1e} m/s² (dominé par L)")
L.append(f"     correction d'amplitude (3°) : θ0²/16 = {corr_amp:.1e} sur T ; dilatation acier pour 5 K : {dil:.1e} sur L")
L.append(f"     en relatif (même pendule déplacé), plancher ≈ 1e-4·g = 1e-3 m/s² = 100 mGal.")
D["pendule"] = {"T_s": T, "dg_absolu": rel_abs * g0}
L.append("")

# ---------------------------------------------------------------- 3. « reconnaître un lieu »
L.append("3. Que faudrait-il pour « reconnaître un lieu » par la gravité ?")
for res in (1e-3, 1e-5, 5e-8, 1e-8):
    dh = res / air_libre
    dn = res / dg_nord
    L.append(f"   résolution {sci(res,2)} m/s² ({res/uGal:.3g} µGal) → équivaut à {dh:.3g} m d'altitude ou {dn:.3g} m nord-sud")
plage = g_normal(90) - g_normal(0)
S_terre = 4 * math.pi * R_terre**2
n_val = plage / uGal
L.append(f"   Un scalaire g résolu à 1 µGal prend ≈ {n_val:.1e} valeurs distinctes sur Terre, pour {S_terre:.1e} m² de surface :")
L.append(f"   chaque valeur correspond en moyenne à ≈ {S_terre/n_val:.1e} m² (≈ {S_terre/n_val/1e6:.0f} km²) : g seul n'identifie pas un lieu.")
L.append(f"   De plus g varie dans le temps : marées ≈ {maree_cc/uGal:.0f} µGal crête à crête (= {maree_cc/air_libre:.2f} m d'altitude équivalente),")
L.append("   nappes phréatiques ~10 µGal, pression ±10 µGal, constructions voisines ~0,1–1 µGal.")
L.append("   Un « verrouillage » à 1 m près exigerait : ~1 µGal de résolution, un modèle de marée, une CARTE de")
L.append("   référence préexistante à la même résolution et à la même époque, et des mesures vectorielles/gradient.")
L.append("   État de l'art réel : la navigation par corrélation de cartes de gravité/gradient (sous-marins) atteint")
L.append("   des précisions de l'ordre de la centaine de mètres au kilomètre, le long d'une trajectoire, pas en un point")
L.append("   (ordre de grandeur donné sans référence vérifiée — à traiter comme [HYP]).")
D["cellule_moyenne_m2"] = S_terre / n_val
L.append("")

# ---------------------------------------------------------------- 4. détectabilité d'une « C204 » massive
m_lo, m_hi = C204["masse_TN_kg"]
L.append("4. Si l'unité contenait réellement les masses qu'implique une puissance de Hawking de 300–500 MW")
L.append("   (valeur retenue : 3,9–5,1e12 kg PAR singularité, erratum E2 ; DÉDUITE, jamais revendiquée telle quelle) :")
D["detectabilite"] = {}
CAS_M = (("unité revendiquée, 227 kg", 227.0), ("une singularité, 3,9e12 kg", m_lo), ("une singularité, 5,1e12 kg", m_hi),
         ("la paire, 7,8e12 kg", 2 * m_lo), ("la paire, 1,02e13 kg", 2 * m_hi),
         ("ancienne fourchette v1 : 1e11 kg", 1e11), ("ancienne fourchette v1 : 1e12 kg", 1e12))
for nom_m, M in CAS_M:
    L.append(f"   {nom_m} : g supplémentaire à 1 m = {G*M/1.0:.3g} m/s² ({G*M/g0:.3g} g) ; à 3 m = {G*M/9:.3g} m/s²")
    D["detectabilite"][nom_m] = {"M_kg": M, "g_1m": G * M, "g_1m_en_g": G * M / g0}
    for nom, bruit, plancher, cout, niv in (CAPTEURS[0], CAPTEURS[1], CAPTEURS[5], CAPTEURS[7]):
        sig = max((bruit / 10.0) if bruit else 0.0, plancher)
        rmax = math.sqrt(G * M / (5 * sig))          # détection à 5 sigma
        D["detectabilite"][nom_m][nom] = rmax
        L.append(f"       détectable à 5σ par « {nom[:44]} » jusqu'à r = {rmax:,.3g} m".replace(",", " "))
r_s1, r_s2 = math.sqrt(G * m_lo / (5 * 2e-3)), math.sqrt(G * m_hi / (5 * 2e-3))
r_g1, r_g2 = math.sqrt(G * m_lo / (5 * 5e-8)), math.sqrt(G * m_hi / (5 * 5e-8))
L.append(f"   → UNE singularité de 3,9–5,1e12 kg : {G*m_lo/g0:.0f}–{G*m_hi/g0:.0f} g à 1 m ; vue par un smartphone à "
         f"{r_s1:.0f}–{r_s2:.0f} m et par un gravimètre de terrain à {r_g1/1e3:.0f}–{r_g2/1e3:.0f} km ;")
L.append(f"     la paire : {2*G*m_lo/g0:.0f}–{2*G*m_hi/g0:.0f} g à 1 m ; smartphone à {r_s1*math.sqrt(2):.0f}–{r_s2*math.sqrt(2):.0f} m ; "
         f"gravimètre à {r_g1*math.sqrt(2)/1e3:.0f}–{r_g2*math.sqrt(2)/1e3:.0f} km ; poids sur le châssis {2*m_lo*g0:.1e}–{2*m_hi*g0:.1e} N.")
L.append("   → à l'inverse, les 227 kg revendiqués donnent 1,5 µGal à 1 m : indiscernables d'un moteur de voiture.")
L.append("")
L.append("Problème de dynamique pour un « capteur VGL » : il devrait résoudre ~1 µGal (1e-9 g) tout en supportant")
L.append("1,5–2 g de champ propre revendiqué, soit une dynamique > 1e9, au voisinage immédiat de masses mobiles")
L.append("et d'un véhicule sur suspension. Aucun gravimètre existant ne fait cela.")

sauver("calc04_gravimetrie_VGL", D, L)

# ---------------------------------------------------------------- figure
fig, axes = plt.subplots(1, 2, figsize=(13, 5.4))
ax = axes[0]
x = np.linspace(-15, 15, 601)
profil = -2 * math.pi * G * abs(drho) * Rv**2 * dz / (x**2 + dz**2) / uGal
ax.plot(x, profil, lw=2.2, color="#33658a", label="anomalie d'une galerie vide (Ø 2 m, 3 m de profondeur)")
rng = np.random.default_rng(4)
for nom, s, col in (("gravimètre relatif de terrain (σ ≈ 5 µGal)", 5.0, "#2e8b57"),
                    ("gravimètre MEMS de recherche (σ ≈ 40 µGal)", 40.0, "#f6ae2d")):
    xs = np.arange(-15, 15.1, 1.0)
    ps = -2 * math.pi * G * abs(drho) * Rv**2 * dz / (xs**2 + dz**2) / uGal
    ax.errorbar(xs, ps + rng.normal(0, s, xs.size), yerr=s, fmt="o", ms=3.5, color=col, alpha=0.85, label=nom, lw=0.8)
ax.set_xlabel("position le long du profil (m)")
ax.set_ylabel("Δg (µGal)")
ax.set_title("Profil gravimétrique simulé au-dessus d'une galerie\n(simulation illustrative ; smartphone : σ ≈ 200 000 µGal, hors échelle)", fontsize=9.5)
ax.legend(fontsize=7.5, loc="lower right")
ax.grid(alpha=0.25)

ax = axes[1]
noms = [cpt["capteur"].split(" (")[0] for cpt in D["capteurs"]]
vals = [cpt["sigma_uGal"] for cpt in D["capteurs"]]
ax.barh(range(len(noms)), vals, color="#33658a")
ax.set_xscale("log")
ax.set_yticks(range(len(noms)))
ax.set_yticklabels(noms, fontsize=7.5)
ax.invert_yaxis()
for val, txt, col in ((maree_cc / uGal, "marées (crête à crête)", "crimson"), (air_libre / uGal, "1 m d'altitude", "purple"),
                      (dg_nord / uGal, "1 m vers le nord (45°)", "darkorange"), (1.5, "227 kg à 1 m", "k")):
    ax.axvline(val, color=col, ls="--", lw=1)
    ax.text(val * 1.15, len(noms) - 0.55, txt, rotation=90, fontsize=7.5, color=col, va="bottom")
ax.set_xlabel("résolution réaliste (µGal) — 1 µGal = 1e-8 m/s²")
ax.set_title("Résolution des capteurs contre signaux à reconnaître\n(ordres de grandeur indicatifs)", fontsize=9.5)
ax.grid(True, which="both", axis="x", alpha=0.25)
fig.tight_layout()
fig.savefig(fig_chemin("calc04_gravimetrie.png"), dpi=150)
print("figure :", fig_chemin("calc04_gravimetrie.png"))

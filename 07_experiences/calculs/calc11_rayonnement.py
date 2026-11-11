#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-11 — Détection de rayonnement : bruit de fond gamma/X mesuré avec un compteur du commerce
(SANS source radioactive), comparé à ce qu'impliquerait un « évent à rayons X » de 300–500 MW.

Calcule :
  1. la statistique de comptage d'un compteur Geiger (temps nécessaire pour voir un excès) ;
  2. le débit de dose qu'impliquerait « 300–500 MW », en deux lectures : (A) littérale, toute la puissance en
     rayons X ; (B) spectre de Hawking, γ primaires seuls (7,5 % de la puissance, ~15 MeV) — borne basse ;
     isotrope ou concentrée dans le cône de DOC-009, avec et sans atténuation par l'air ;
  3. le blindage et l'évacuation thermique qu'il faudrait ;
  4. la plus petite fuite détectable avec un compteur à 100 €.

Coefficients massiques (cm²/g) : NIST, Hubbell & Seltzer, tables XCOM/NISTIR 5632 (valeurs relues en ligne
le 10/11/2026 sur physics.nist.gov). Dose ≈ kerma (équilibre électronique supposé) : ORDRES DE GRANDEUR.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import brentq

from constantes import (sigma_SB, C204, COFFRE, FRACTION_PHOTONS_HAWKING, E_PHOTON_HAWKING, sauver, fig_chemin, sci)

L, D = [], {}
L.append("EXP-11 — RAYONNEMENT : BRUIT DE FOND RÉEL CONTRE « ÉVENT À RAYONS X » REVENDIQUÉ")
L.append("=" * 72)

# ---------------------------------------------------------------- 1. statistique de comptage
fond_uSv_h = 0.10
sens = 175.0          # coups/min par µSv/h (tube Geiger de type SBM-20, valeur indicative)
b = 20.0              # coups/min de bruit de fond (indicatif)
L.append("1. Compteur Geiger du commerce — statistique de Poisson")
L.append(f"   bruit de fond typique ≈ {fond_uSv_h:.2f} µSv/h (0,05–0,2 selon le lieu) → ≈ {b:.0f} coups/min ; "
         f"sensibilité indicative {sens:.0f} cpm par µSv/h")
L.append("   temps de mesure (durée égale AVEC et SANS appareil) pour voir un excès Δ à 3σ : s·Δ·t = 3·√(2bt + s·Δ·t)")
D["geiger"] = []
for delta in (0.01, 0.02, 0.05, 0.1, 0.5, 1.0):
    e = sens * delta                      # cpm d'excès
    t = 9 * (2 * b + e) / e**2            # minutes
    D["geiger"].append({"exces_uSv_h": delta, "t_min": t})
    L.append(f"     Δ = {delta:>4} µSv/h ({100*delta/fond_uSv_h:>4.0f} % du fond) : t = {t:8.1f} min par phase")
t_mort = 190e-6
cps_max = 1 / t_mort
L.append(f"   temps mort ~{t_mort*1e6:.0f} µs → saturation vers {cps_max:.0f} coups/s, soit ≈ {cps_max*60/sens/1000:.1f} mSv/h : "
         f"au-delà, un Geiger simple sous-estime (voire affiche zéro).")
L.append("   Repères : exposition naturelle moyenne mondiale ≈ 2,4 mSv/an (UNSCEAR) ; limite public 1 mSv/an hors naturel")
L.append("   et médical, travailleurs 20 mSv/an (CIPR 103) ; dose létale 50 % (corps entier, aiguë) ≈ 4 Gy.")
L.append("")

# ---------------------------------------------------------------- 2. débit de dose : DEUX LECTURES de l'affirmation
# Lecture A (littérale)  : « 300–500 MW » sortent entièrement en rayons X (100 keV ; variantes 1 et 10 MeV).
# Lecture B (spectre de Hawking, valeur retenue par le programme — Équipes C et G, Red Team n° 2) : seule la
#   fraction photons (≈ 7,5 %) de la puissance sort en γ primaires de ~15 MeV ; c'est une BORNE BASSE de la dose,
#   car les e± (≈ 37 % de la puissance) déposeraient ~1e5 Gy/s à 1 m s'ils n'étaient pas arrêtés.
rho_air = 1.205e-3    # g/cm³
COEF = {              # énergie : (µ_en/ρ eau, µ/ρ air, µ/ρ plomb) en cm²/g — NIST (relus en ligne le 10/11/2026)
    "100 keV": (2.546e-2, 1.541e-1, 5.549),
    "1 MeV":   (3.103e-2, 6.358e-2, 7.102e-2),
    "10 MeV":  (1.566e-2, 2.045e-2, 4.972e-2),
    "15 MeV":  (1.441e-2, 1.810e-2, 5.658e-2),
}
P_lo, P_hi = C204["puissance_W"]
P_ref = 400e6
f_gamma = FRACTION_PHOTONS_HAWKING
E_H = E_PHOTON_HAWKING
ouverture = 78.0                      # ouverture totale du « cône » tracé sur DOC-009 (erratum E7) → demi-angle 39°
demi_angle = ouverture / 2
gain_cone = 4 * math.pi / (2 * math.pi * (1 - math.cos(math.radians(demi_angle))))

def debit(P, r, E, cone=False, air=True):
    """Débit de dose (Gy/s) dans l'eau/tissu à la distance r (m) pour une puissance photonique P (W)."""
    mu_en, mu_air, _ = COEF[E]
    flux = P / (4 * math.pi * r**2) * (gain_cone if cone else 1.0)        # W/m²
    att = math.exp(-mu_air * rho_air * r * 100) if air else 1.0           # faisceau étroit (borne basse)
    return flux * (mu_en * 0.1) * att                                     # cm²/g → m²/kg : ×0,1

L.append("2. Débit de dose impliqué par « 300–500 MW » — calcul d'IMPLICATION (pas un fait), en DEUX LECTURES")
L.append("   A. lecture littérale du texte : toute la puissance sort en rayons X (100 keV ; variantes 1 et 10 MeV) ;")
L.append(f"   B. spectre de Hawking (valeur retenue) : fraction photons {f_gamma:.1%} → {f_gamma*P_ref/1e6:.0f} MW de γ primaires de ~{E_H}")
L.append("      pour 400 MW ; BORNE BASSE (les e±, ≈ 37 % de la puissance, déposeraient ~1e5 Gy/s à 1 m s'ils sortaient).")
L.append(f"   « cône d'évacuation » de DOC-009 : ouverture ≈ {ouverture:.0f}° (erratum E7) → concentration ×{gain_cone:.1f} si toute")
L.append("   l'émission y était confinée (un rayonnement de Hawking n'est pas collimatable : erratum E5).")
D["debit"] = {}
LECTURES = [("A", "100 keV", 1.0), ("A", "1 MeV", 1.0), ("A", "10 MeV", 1.0), ("B", E_H, f_gamma)]
for lec, E, frac in LECTURES:
    lpm = 1 / (COEF[E][1] * rho_air) / 100
    etiq = (f"Lecture A — {P_ref/1e6:.0f} MW entièrement en photons de {E}" if lec == "A"
            else f"Lecture B — γ primaires de Hawking : {frac*P_ref/1e6:.0f} MW de photons de {E}")
    L.append(f"   {etiq} (libre parcours moyen dans l'air ≈ {lpm:.0f} m) — Gy/s :")
    L.append(f"     {'distance':>9} | {'isotrope, sans air':>18} | {'isotrope, air (faisceau étroit)':>31} | {'dans le cône, sans air':>22}")
    cle = f"{lec}_{E}"
    D["debit"][cle] = []
    for r in (1.0, 3.0, 10.0, 100.0, 1000.0, 10000.0):
        Pp = frac * P_ref
        d0, d1, d2 = debit(Pp, r, E, air=False), debit(Pp, r, E), debit(Pp, r, E, cone=True, air=False)
        D["debit"][cle].append({"r_m": r, "isotrope_sans_air": d0, "isotrope_air": d1, "cone_sans_air": d2})
        L.append(f"     {r:>7.0f} m | {sci(d0):>18} | {sci(d1):>31} | {sci(d2):>22}")
L.append("   (réalité : la diffusion dans l'air — effet de ciel — place la dose entre les deux colonnes « isotrope ».)")
L.append("")
L.append(f"   Synthèse à 1 m et à 3 m (isotrope, sans atténuation), pour {P_lo/1e6:.0f} / {P_ref/1e6:.0f} / {P_hi/1e6:.0f} MW :")
D["synthese"] = {}
for lec, E, frac, nom in (("A", "100 keV", 1.0, "A (littérale, X de 100 keV)"), ("B", E_H, f_gamma, f"B (γ de Hawking, {E_H}, borne basse)")):
    for r in (1.0, 3.0):
        v = [debit(frac * P, r, E, air=False) for P in (P_lo, P_ref, P_hi)]
        D["synthese"][f"{lec}_{r:.0f}m"] = v
        L.append(f"     lecture {nom:<38} à {r:.0f} m : {sci(v[0])} / {sci(v[1])} / {sci(v[2])} Gy/s ; "
                 f"dose létale 50 % (4 Gy) en {4/v[1]*1e3:.2f} ms ; {v[1]*3600/(fond_uSv_h*1e-6):.1e} × le fond naturel")
dA3 = debit(P_ref, 3.0, "100 keV", air=False)
dB1, dB3 = debit(f_gamma * P_ref, 1.0, E_H, air=False), debit(f_gamma * P_ref, 3.0, E_H, air=False)
L.append(f"   Rapport lecture A / lecture B à 3 m : {dA3/dB3:.0f} (dont {1/f_gamma:.0f} pour la fraction photons et "
         f"{COEF['100 keV'][0]/COEF[E_H][0]:.1f} pour le coefficient d'absorption).")
D["dose_A_3m_Gy_s"] = dA3
D["dose_B_1m_Gy_s"] = dB1
D["dose_B_3m_Gy_s"] = dB3
D["temps_DL50_ms"] = {"A_3m": 4 / dA3 * 1e3, "B_3m": 4 / dB3 * 1e3}
# distance où le débit retombe à 1 µSv/h
cible = 1e-6 / 3600
L.append("   Distance à laquelle le débit retombe à 1 µSv/h (dix fois le fond) :")
D["distance_1uSv_h"] = {}
for lec, E, frac in LECTURES:
    Pp = frac * P_ref
    r_sans = math.sqrt(Pp * COEF[E][0] * 0.1 / (4 * math.pi * cible))
    r_avec = brentq(lambda r: debit(Pp, r, E) - cible, 1.0, 1e7)
    D["distance_1uSv_h"][f"{lec}_{E}"] = {"sans_air_m": r_sans, "avec_air_m": r_avec}
    L.append(f"     lecture {lec}, {E:>8} : {r_sans/1e3:,.0f} km sans atténuation ; {r_avec/1e3:.2f} km avec atténuation en faisceau étroit".replace(",", " "))
L.append("")

# ---------------------------------------------------------------- 3. blindage et chaleur
L.append("3. Blindage et évacuation thermique nécessaires")
D["blindage"] = {}
for lec, E, frac in LECTURES:
    mu_pb = COEF[E][2] * 11.34            # cm^-1
    facteur = debit(frac * P_ref, 1.0, E, air=False) / cible
    ep = math.log(facteur) / mu_pb        # cm (faisceau étroit, sans facteur d'accumulation → sous-estimation)
    r_int = 0.10
    masse = 4 / 3 * math.pi * ((r_int + ep / 100)**3 - r_int**3) * 11340
    D["blindage"][f"{lec}_{E}"] = {"attenuation": facteur, "epaisseur_cm": ep, "masse_coquille_kg": masse}
    L.append(f"   lecture {lec}, {E:>8} : atténuation requise ×{facteur:.1e} pour 1 µSv/h à 1 m → {ep:5.1f} cm de plomb "
             f"(coquille sphérique de rayon intérieur 10 cm : {masse:,.0f} kg)".replace(",", " "))
L.append(f"   Masse revendiquée de l'unité entière : {C204['masse_unite_kg']:.0f} kg. (Faisceau étroit : minorant ; aucun de ces")
L.append("   chiffres n'est un calcul de transport ; les Équipes C et G obtiennent 62 cm et ≥ 36 cm par d'autres méthodes.)")
S_coffre, h_conv = COFFRE["S"], 10.0
L.append(f"   Évacuation de la puissance (toutes espèces confondues), pour {P_lo/1e6:.0f} / {P_ref/1e6:.0f} / {P_hi/1e6:.0f} MW :")
D["thermique"] = {"S_coffre_m2": S_coffre, "T_corps_noir_K": {}, "eau_kg_s": []}
for S, nom in ((S_coffre, f"surface du coffre à l'échelle révisée ({S_coffre:.2f} m², L = 0,85 m)"), (10.0, "surface de 10 m²")):
    T = [(P / (sigma_SB * S))**0.25 for P in (P_lo, P_ref, P_hi)]
    D["thermique"]["T_corps_noir_K"][f"{S:.2f}"] = T
    L.append(f"     {nom} rayonnant en corps noir : T = {T[0]:.0f} / {T[1]:.0f} / {T[2]:.0f} K")
m_eau = [P / (4186 * 80 + 2.257e6) for P in (P_lo, P_ref, P_hi)]
D["thermique"]["eau_kg_s"] = m_eau
L.append(f"     ou vaporisation d'eau prise à 20 °C : {m_eau[0]:.0f} / {m_eau[1]:.0f} / {m_eau[2]:.0f} kg/s "
         f"({m_eau[0]*3.6:.0f} / {m_eau[1]*3.6:.0f} / {m_eau[2]*3.6:.0f} tonnes par heure).")
P_coffre = [h_conv * S_coffre * (Tc - 20) for Tc in C204["temperature_C"]]
D["thermique"]["puissance_coffre_W"] = P_coffre
L.append(f"   À l'inverse, un coffre de {S_coffre:.2f} m² à {C204['temperature_C'][0]:.0f}–{C204['temperature_C'][1]:.0f} °C dans de l'air à 20 °C "
         f"dissipe ≈ h·S·ΔT = {P_coffre[0]:.0f}–{P_coffre[1]:.0f} W (h ≈ {h_conv:.0f} W/m²K) :")
L.append(f"   rapport {P_lo/P_coffre[1]:.0e} à {P_hi/P_coffre[0]:.0e} avec 300–500 MW. (À l'ancienne échelle L = 1,20 m, 1,80 m² : 324–522 W.)")
L.append("")

# ---------------------------------------------------------------- 4. plus petite fuite détectable
L.append("4. Sensibilité d'un compteur Geiger à une fuite de rayons X (100 keV, à 1 m, isotrope)")
for excess in (0.05, 1.0):
    P_fuite = excess * 1e-6 / 3600 / (COEF["100 keV"][0] * 0.1) * 4 * math.pi
    P_fuite_H = excess * 1e-6 / 3600 / (COEF[E_H][0] * 0.1) * 4 * math.pi
    L.append(f"   excès de {excess} µSv/h ↔ puissance X rayonnée de {sci(P_fuite)} W ({P_fuite/P_ref:.1e} des 400 MW) ; "
             f"en γ de {E_H} : {sci(P_fuite_H)} W ({P_fuite_H/(f_gamma*P_ref):.1e} des {f_gamma*P_ref/1e6:.0f} MW de γ primaires)")
    D[f"fuite_W_pour_{excess}_uSv_h"] = P_fuite
L.append("   → un compteur à ~100 € exclut en moins d'une heure toute fuite supérieure à ~1e-7 W de rayons X ou γ, par une")
L.append("     mesure ABSOLUE rapportée au fond (le rayonnement de singularités ne « s'éteint » pas : pas de test marche/arrêt).")
L.append("     C'est le test le plus discriminant et le moins cher de tout le programme — sur un dispositif disponible.")
L.append("")
L.append("Sécurité : aucune source radioactive n'est utilisée. On mesure le bruit de fond naturel (variations avec")
L.append("l'altitude, la pluie — descendants du radon lessivés —, les matériaux de construction comme le granite).")

sauver("calc11_rayonnement", D, L)

# ---------------------------------------------------------------- figure
fig, ax = plt.subplots(figsize=(9.8, 6.0))
r = np.logspace(0, 5, 400)
for etiq, E, frac, col in (("lecture A : 400 MW de X de 100 keV", "100 keV", 1.0, "#33658a"),
                           (f"lecture B : γ de Hawking ({f_gamma*P_ref/1e6:.0f} MW, {E_H}), borne basse", E_H, f_gamma, "#d1495b")):
    ax.loglog(r, [debit(frac * P_ref, ri, E, air=False) * 3600 for ri in r], color=col, lw=2, label=f"{etiq}, sans atténuation")
    ax.loglog(r, [max(debit(frac * P_ref, ri, E) * 3600, 1e-30) for ri in r], color=col, lw=1.5, ls="--",
              label=f"{etiq}, air (faisceau étroit)")
for val, txt, col in ((4.0, "dose létale 50 % atteinte en 1 heure (4 Gy/h)", "k"),
                      (1e-7, "bruit de fond naturel (≈ 0,1 µSv/h)", "#2e8b57")):
    ax.axhline(val, color=col, ls=":", lw=1.2)
    ax.text(1.2, val * 1.6, txt, fontsize=8, color=col)
ax.axvspan(3.0, 3.7, color="orange", alpha=0.25)
ax.text(3.9, 3e-9, "« champ » revendiqué\n3,0–3,7 m", fontsize=8, color="darkorange")
ax.set_ylim(1e-10, 1e9)
ax.set_xlabel("distance (m)")
ax.set_ylabel("débit de dose (Gy/h ≈ Sv/h pour des photons)")
ax.set_title("EXP-11 — Ce qu'impliqueraient « 300–500 MW » : deux lectures (ici 400 MW)\n"
             "(calcul d'implication illustratif — AUCUNE mesure, aucune source)", fontsize=10)
ax.legend(fontsize=7.5, loc="upper right")
ax.grid(True, which="both", alpha=0.2)
fig.tight_layout()
fig.savefig(fig_chemin("calc11_dose_vs_distance.png"), dpi=150)
print("figure :", fig_chemin("calc11_dose_vs_distance.png"))

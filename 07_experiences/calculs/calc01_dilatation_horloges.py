#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-01 — Dilatation gravitationnelle et cinématique du temps avec des horloges réelles.

Calcule :
  1. le signal Δf/f = g·Δh/c² et l'écart de temps accumulé ;
  2. l'effet cinématique -v²/(2c²) ;
  3. un modèle simplifié de l'expérience Hafele-Keating (comparé aux valeurs publiées) ;
  4. la durée d'intégration nécessaire selon la stabilité (écart-type d'Allan) de
     plusieurs familles d'horloges ;
  5. le budget des effets d'environnement pour un rubidium d'occasion en montagne.

Hypothèses : champ faible, Δh << R_terre, g uniforme. Les stabilités d'horloges sont des
VALEURS INDICATIVES de type « fiche technique » : à remesurer sur l'exemplaire utilisé.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from constantes import (G, c, g0, GM_terre, R_terre, Omega_terre, C204, sauver, fig_chemin, sci)

L = []          # lignes de texte
D = {}          # données JSON

# ---------------------------------------------------------------- 1. signal gravitationnel
pente = g0 / c**2
D["pente_par_metre"] = pente
L.append("EXP-01 — DILATATION DU TEMPS : SIGNAL ATTENDU ET BUDGET DE BRUIT")
L.append("=" * 72)
L.append(f"Décalage gravitationnel : Δf/f = g·Δh/c² = {sci(pente,5)} par mètre (g = {g0} m/s²)")
L.append("")
L.append(f"{'Δh':>10} | {'Δf/f':>10} | {'écart en 1 jour':>16} | {'écart en 1 an':>14}")
tab = []
for dh in (1e-3, 1e-2, 0.33, 1.0, 10.0, 100.0, 450.0, 1000.0, 1650.0, 3000.0, 4810.0):
    y = pente * dh
    tab.append({"dh_m": dh, "y": y, "ns_par_jour": y * 86400e9, "ns_par_an": y * 3.15576e7 * 1e9})
    L.append(f"{dh:>8g} m | {sci(y):>10} | {y*86400e9:>13.4g} ns | {y*3.15576e7*1e9:>11.4g} ns")
D["table_signal"] = tab
L.append("  (0,33 m : Chou et al. 2010 ; 450 m : Tokyo Skytree, Takamoto et al. 2020 ;")
L.append("   1650 m : altitude de Boulder/NIST ; 4810 m : mont Blanc)")
L.append("")

# Pound-Rebka : 22,5 m, aller-retour
y_pr = pente * 22.5
L.append(f"Pound-Rebka (tour de 22,5 m) : gh/c² = {sci(y_pr)} (aller simple), 2gh/c² = {sci(2*y_pr)}")
D["pound_rebka"] = {"aller": y_pr, "aller_retour": 2 * y_pr}

# Voyage type « Project GREAT » (Van Baak 2005) : dénivelé ~1340 m, ~42 h
dh_g, T_g = 1340.0, 42 * 3600.0
dt_g = pente * dh_g * T_g
L.append(f"Séjour en altitude type « Project GREAT » : Δh = {dh_g:.0f} m pendant {T_g/3600:.0f} h → "
         f"avance = {dt_g*1e9:.1f} ns")
D["sejour_altitude"] = {"dh_m": dh_g, "T_s": T_g, "avance_ns": dt_g * 1e9}
L.append("")

# ---------------------------------------------------------------- 2. effet cinématique
L.append("Effet cinématique : Δf/f = -v²/(2c²)")
cin = []
for nom, v in (("marche (1,4 m/s)", 1.4), ("voiture (30 m/s)", 30.0), ("TGV (83 m/s)", 83.0),
               ("avion de ligne (250 m/s)", 250.0), ("ISS (7660 m/s)", 7660.0)):
    y = -v**2 / (2 * c**2)
    cin.append({"cas": nom, "v": v, "y": y})
    L.append(f"  {nom:<26} : {sci(y)}  ({y*3600e9:+.3g} ns par heure)")
D["cinematique"] = cin
v_eq = math.sqrt(2 * g0 * 1000.0)
L.append(f"  Vitesse dont l'effet cinématique égale celui de 1000 m de dénivelé : v = √(2g·Δh) = {v_eq:.0f} m/s")
L.append("")

# ---------------------------------------------------------------- 3. Hafele-Keating simplifié
# Modèle : vol à altitude h, vitesse-sol v vers l'est (+) ou l'ouest (-), latitude moyenne phi.
# Par rapport à une horloge au sol : dτ/τ = g h/c² - (2 R Ω cosφ v + v²)/(2c²)
def hk(h, v, phi_deg, T_h):
    T = T_h * 3600.0
    grav = g0 * h / c**2 * T
    cinem = -(2 * R_terre * Omega_terre * math.cos(math.radians(phi_deg)) * v + v**2) / (2 * c**2) * T
    return grav * 1e9, cinem * 1e9, (grav + cinem) * 1e9

est = hk(9000.0, +230.0, 34.0, 41.2)
ouest = hk(9000.0, -230.0, 34.0, 48.6)
L.append("Hafele-Keating (1971) — MODÈLE SIMPLIFIÉ (h = 9 km, |v| = 230 m/s, latitude moyenne 34°,")
L.append("durées de vol 41,2 h vers l'est et 48,6 h vers l'ouest) :")
L.append(f"  vers l'est   : gravitation {est[0]:+.0f} ns, cinématique {est[1]:+.0f} ns, total {est[2]:+.0f} ns")
L.append(f"  vers l'ouest : gravitation {ouest[0]:+.0f} ns, cinématique {ouest[1]:+.0f} ns, total {ouest[2]:+.0f} ns")
L.append("  Valeurs publiées (Hafele & Keating, Science 177, 1972) : prédit -40 ± 23 ns (est), +275 ± 21 ns (ouest) ;")
L.append("  observé -59 ± 10 ns (est), +273 ± 7 ns (ouest). Le modèle simplifié retrouve signes et ordres de grandeur.")
D["hafele_keating_modele"] = {"est_ns": est, "ouest_ns": ouest,
                              "publie_predit_ns": {"est": [-40, 23], "ouest": [275, 21]},
                              "publie_observe_ns": {"est": [-59, 10], "ouest": [273, 7]}}
L.append("")

# ---------------------------------------------------------------- 4. stabilité et durée d'intégration
# Modèle : sigma_y(tau)² = (a/sqrt(tau))² + plancher² + (D·tau/sqrt(2))²
JOUR, MOIS = 86400.0, 30 * 86400.0
HORLOGES = {
    # nom : (a [bruit blanc de fréquence à 1 s], plancher de scintillation, dérive par seconde, coût indicatif)
    "CSAC (césium miniature)":            (3.0e-10, 5e-12, 9e-10 / MOIS, "≈ 2–6 k€ neuf"),
    "OCXO seul (GPSDO en maintien)":      (0.0, 1e-12, 5e-10 / JOUR, "150–400 € (GPSDO d'occasion)"),
    "Rubidium d'occasion (FE-5680A, LPRO, PRS10)": (2.0e-11, 3e-13, 5e-11 / MOIS, "100–1500 €"),
    "Césium à jet 5071A (tube standard)": (2.7e-11, 5e-14, 0.0, "plusieurs dizaines de k€ ; occasion variable"),
    "Césium à jet 5071A (haute performance)": (8.5e-12, 1e-14, 0.0, "plusieurs dizaines de k€"),
    "Maser à hydrogène actif":            (1.0e-13, 1e-15, 1e-16 / JOUR, "> 200 k€"),
    "Horloge à réseau optique (labo)":    (1.0e-16, 1e-18, 0.0, "laboratoire de métrologie"),
}

def sigma_y(tau, a, plancher, derive):
    return np.sqrt((a / np.sqrt(tau))**2 + plancher**2 + (derive * tau / math.sqrt(2))**2)

taus = np.logspace(0, 7, 701)
SIGNAUX = {"1 mm": 1e-3, "1 cm": 1e-2, "1 m": 1.0, "100 m": 100.0, "1000 m": 1000.0, "3000 m": 3000.0}

L.append("Durée d'intégration pour détecter le décalage à 3 sigma en comparant DEUX horloges identiques")
L.append("(critère : √2·σ_y(τ) ≤ signal/3 ; modèle σ_y² = (a/√τ)² + plancher² + (D·τ/√2)²) :")
entete = f"{'horloge':<46}" + "".join(f"{k:>12}" for k in SIGNAUX)
L.append(entete)
D["integration"] = {}
for nom, (a, pl, dr, cout) in HORLOGES.items():
    s = np.sqrt(2) * sigma_y(taus, a, pl, dr)
    ligne = f"{nom:<46}"
    D["integration"][nom] = {"a": a, "plancher": pl, "derive_par_s": dr, "cout": cout, "durees_s": {}}
    for k, dh in SIGNAUX.items():
        cible = pente * dh / 3.0
        ok = np.where(s <= cible)[0]
        if ok.size:
            t = taus[ok[0]]
            D["integration"][nom]["durees_s"][k] = float(t)
            if t < 120:
                txt = f"{t:.0f} s"
            elif t < 7200:
                txt = f"{t/60:.0f} min"
            elif t < 2 * 86400:
                txt = f"{t/3600:.1f} h"
            else:
                txt = f"{t/86400:.1f} j"
        else:
            D["integration"][nom]["durees_s"][k] = None
            txt = "impossible"
        ligne += f"{txt:>12}"
    L.append(ligne)
L.append("  « impossible » = le plancher de scintillation ou la dérive dépasse le signal/3 quel que soit τ ≤ 10⁷ s.")
L.append("  NB : un GPSDO VERROUILLÉ est asservi au temps GPS (référence au géoïde) : il ne « voit » pas son propre")
L.append("  décalage ; il sert de RÉFÉRENCE, l'horloge libre (Rb/Cs) étant l'objet déplacé.")
L.append("")

# Variante « aller-retour » : phase accumulée x = y·T ; bruit de temps accumulé par horloge :
#   bruit blanc de fréquence  -> marche aléatoire de phase a·√T
#   scintillation de fréquence (plancher) -> de l'ordre de plancher·T
L.append("Variante aller-retour (horloge transportée T secondes en altitude, comparée avant/après à une horloge")
L.append("identique restée en bas) : bruit ≈ √2·√[(a·√T)² + (plancher·T)²]  (environnement NON inclus)")
D["aller_retour"] = []
for nom in ("Rubidium d'occasion (FE-5680A, LPRO, PRS10)", "Césium à jet 5071A (tube standard)",
            "Césium à jet 5071A (haute performance)"):
    a, pl = HORLOGES[nom][0], HORLOGES[nom][1]
    for dh, T in ((1340.0, 42 * 3600.0), (3000.0, 48 * 3600.0)):
        sig = pente * dh * T
        bruit = math.sqrt(2) * math.sqrt((a * math.sqrt(T))**2 + (pl * T)**2)
        D["aller_retour"].append({"horloge": nom, "dh_m": dh, "T_h": T / 3600, "signal_ns": sig * 1e9,
                                  "bruit_ns": bruit * 1e9, "S_B": sig / bruit})
        L.append(f"  {nom:<46} Δh = {dh:.0f} m, T = {T/3600:.0f} h : signal {sig*1e9:5.1f} ns, "
                 f"bruit {bruit*1e9:5.1f} ns, S/B = {sig/bruit:.1f}")
L.append("  Avec N horloges transportées et N restées en bas, le bruit se réduit en 1/√N (Van Baak 2005 : 3 césiums emportés).")
L.append("")

# ---------------------------------------------------------------- 5. effets d'environnement (rubidium)
dh = 1500.0
p0, Hs = 1013.25, 8434.0                       # hPa, hauteur d'échelle isotherme (m)
dP = p0 * (1 - math.exp(-dh / Hs))             # chute de pression pour 1500 m
signal = pente * dh
env = [
    ("Signal relativiste (Δh = 1500 m)", signal, "gΔh/c²"),
    ("Pression (≈1e-13/hPa, indicatif) × ΔP", 1e-13 * dP, f"ΔP = {dP:.0f} hPa"),
    ("Température (≈1e-12/K, indicatif) × 10 K", 1e-12 * 10, "habitacle non régulé"),
    ("Champ magnétique (≈2e-10/G, indicatif) × 0,5 G", 2e-10 * 0.5, "retournement dans le champ terrestre"),
    ("Dérive (5e-11/mois) sur 2 jours", 5e-11 * 2 / 30, "vieillissement"),
    ("Cinématique voiture 30 m/s (pendant le trajet)", 30.0**2 / (2 * c**2), "v²/2c²"),
]
L.append("Budget d'environnement — rubidium d'occasion emmené 1500 m plus haut (ordres de grandeur) :")
for nom, val, rem in env:
    L.append(f"  {nom:<52} {sci(val):>10}   ({rem}) → {val/signal:8.2g} × signal")
L.append("  Conclusion : sans enceinte étanche thermostatée et blindage magnétique, les effets d'environnement")
L.append("  d'un rubidium dépassent le signal de 1 à 3 ordres de grandeur ; il faut des césiums à jet (insensibles")
L.append("  au premier ordre) — c'est pourquoi l'expérience est classée N2/N3 et non N1.")
D["environnement_rubidium"] = [{"effet": n, "valeur": v, "rapport_au_signal": v / signal} for n, v, r in env]
L.append("")

# ---------------------------------------------------------------- 6. lien C204
# Décalage gravitationnel produit par une masse M à la distance r : GM/(r c²)
# Masses : 227 kg (revendiqué) ; 3,9–5,1e12 kg par singularité (valeur retenue, erratum E2) ; la paire ;
#          1e11–1e12 kg (ancienne fourchette du dossier v1, conservée pour mémoire).
m_lo, m_hi = C204["masse_TN_kg"]
taux = C204["taux_temps"]
L.append("Lien avec la C204 (affirmations NON tenues pour vraies) — décalage GM/(rc²) à 1 m :")
D["c204"] = {"taux_revendique": taux, "cas": []}
for nom, M in (("unité revendiquée, 227 kg", 227.0),
               ("une singularité, 3,9e12 kg (valeur retenue, basse)", m_lo),
               ("une singularité, 5,1e12 kg (valeur retenue, haute)", m_hi),
               ("la paire, 7,8e12 kg", 2 * m_lo), ("la paire, 1,02e13 kg", 2 * m_hi),
               ("ancienne fourchette v1 : 1e11 kg", 1e11), ("ancienne fourchette v1 : 1e12 kg", 1e12)):
    y = G * M / (1.0 * c**2)
    D["c204"]["cas"].append({"cas": nom, "M_kg": M, "redshift_1m": y, "equiv_denivele_m": y / pente,
                             "rapport_taux": taux / y})
    L.append(f"  {nom:<52} : {sci(y)}  (≡ {y/pente:.3g} m de dénivelé terrestre ; {y*3.15576e7*1e9:.3g} ns/an ; "
             f"taux revendiqué = {taux/y:.1e} × cet effet)")
L.append(f"  Taux revendiqué « 10 ans par heure » : dt_ext/dτ = {taux:.0f}, soit {taux/(G*2*m_hi/c**2):.1e} à "
         f"{taux/(G*m_lo/c**2):.1e} fois le décalage produit à 1 m par les masses retenues (paire ou singularité seule).")
L.append("  Rappel : la dilatation du temps ralentit une horloge par rapport à une autre ; elle ne renvoie")
L.append("  jamais dans le passé.")

sauver("calc01_dilatation_horloges", D, L)

# ---------------------------------------------------------------- figure
fig, ax = plt.subplots(figsize=(9.5, 6.2))
coul = plt.cm.viridis(np.linspace(0.05, 0.95, len(HORLOGES)))
for (nom, (a, pl, dr, cout)), col in zip(HORLOGES.items(), coul):
    ax.loglog(taus, sigma_y(taus, a, pl, dr), lw=2, color=col, label=nom)
for k, dh in SIGNAUX.items():
    ax.axhline(pente * dh, color="crimson", ls="--", lw=0.9)
    ax.text(1.15, pente * dh * 1.12, f"signal Δh = {k}", color="crimson", fontsize=8)
ax.set_xlabel("durée de moyennage τ (s)")
ax.set_ylabel("écart-type d'Allan σ_y(τ) — modèle indicatif")
ax.set_title("EXP-01 — Stabilité des horloges contre décalage gravitationnel g·Δh/c²\n"
             "(calcul illustratif, modèles de bruit indicatifs — pas une mesure)")
ax.set_ylim(3e-20, 3e-9)
ax.set_xlim(1, 1e7)
ax.grid(True, which="both", alpha=0.25)
ax.legend(fontsize=7.5, loc="upper right", ncol=1)
fig.tight_layout()
fig.savefig(fig_chemin("calc01_allan_vs_signal.png"), dpi=150)
print("figure :", fig_chemin("calc01_allan_vs_signal.png"))

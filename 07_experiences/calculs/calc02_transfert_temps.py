#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXP-02 — Synchronisation d'horloges et transfert de temps : ce que l'on mesure réellement.

Calcule :
  1. les corrections relativistes du GPS (re-dérivées) ;
  2. l'erreur d'un transfert bidirectionnel (NTP / PTP / White Rabbit) due à l'asymétrie
     des délais, par simulation Monte-Carlo (ILLUSTRATIVE) ;
  3. la conversion bruit de temps → incertitude de comparaison de fréquence ;
  4. le retard d'un câble (expérience N1 : « mesurer 10 m de coaxial avec deux GPS »).

Les performances « typiques » des méthodes sont des ordres de grandeur d'usage courant en
métrologie temps-fréquence ; elles dépendent fortement du matériel et de l'étalonnage.
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from constantes import (c, g0, GM_terre, R_equateur, Omega_terre, W0_geoide, sauver, fig_chemin, sci)

L, D = [], {}
L.append("EXP-02 — TRANSFERT DE TEMPS : ORDRES DE GRANDEUR")
L.append("=" * 72)

# ---------------------------------------------------------------- 1. relativité dans le GPS
a_gps = 2.656175e7                                  # demi-grand axe (m)
y_sol = -W0_geoide / c**2                           # horloge sur le géoïde (potentiel de pesanteur, rotation incluse)
y_sat = -1.5 * GM_terre / (a_gps * c**2)            # -GM/(a c²) - v²/(2c²), orbite circulaire
net = y_sat - y_sol
v2 = GM_terre / a_gps
cin = -v2 / (2 * c**2)
grav = net - cin
L.append("1. Relativité dans le GPS (orbite circulaire, a = 26 561,75 km)")
L.append(f"   horloge au sol (géoïde)  : -W0/c² = {sci(y_sol,5)}")
L.append(f"   horloge satellite        : -3GM/(2ac²) = {sci(y_sat,5)}")
L.append(f"   écart net satellite-sol  : {sci(net,5)}  → {net*86400e6:+.2f} µs/jour")
L.append(f"     dont potentiel         : {sci(grav,5)}  → {grav*86400e6:+.2f} µs/jour")
L.append(f"     dont vitesse orbitale  : {sci(cin,5)}  → {cin*86400e6:+.2f} µs/jour")
L.append(f"   fréquence embarquée réglée : 10,23 MHz × (1 - {sci(net,5)}) = {10.23e6*(1-net):.5f} Hz")
L.append(f"   sans correction : dérive d'échelle de temps équivalente à {net*86400*c/1e3:.1f} km/jour de pseudo-distance")
F = -2 * math.sqrt(GM_terre) / c**2
exc = 0.02
L.append(f"   terme d'excentricité : Δt = F·e·√a·sin E, F = {sci(F,5)} s/√m ; amplitude pour e = {exc} : "
         f"{abs(F)*exc*math.sqrt(a_gps)*1e9:.1f} ns")
sagnac_max = Omega_terre * a_gps * R_equateur / c**2
L.append(f"   correction de Sagnac maximale (récepteur à l'équateur) : Ω·a·R/c² = {sagnac_max*1e9:.0f} ns")
sag_tour = 2 * Omega_terre * math.pi * R_equateur**2 / c**2
L.append(f"   Sagnac pour un tour complet de l'équateur : 2ΩA/c² = {sag_tour*1e9:.1f} ns")
D["gps"] = {"net": net, "net_us_jour": net * 86400e6, "grav_us_jour": grav * 86400e6, "cin_us_jour": cin * 86400e6,
            "excentricite_ns": abs(F) * exc * math.sqrt(a_gps) * 1e9, "sagnac_max_ns": sagnac_max * 1e9,
            "sagnac_tour_ns": sag_tour * 1e9}
L.append("")

# ---------------------------------------------------------------- 2. méthodes
# (nom, incertitude de temps typique en s, bruit de temps court terme en s, coût/niveau)
METHODES = [
    ("NTP via Internet",                       5e-3,   2e-3,  "gratuit — N1"),
    ("NTP sur réseau local",                   2e-4,   5e-5,  "gratuit — N1"),
    ("PTP (IEEE 1588) horodatage matériel",    1e-7,   3e-8,  "cartes réseau PTP, 50–300 € — N1/N2"),
    ("GPS sens unique, récepteur de temps",    2e-8,   8e-9,  "module 30–250 € — N1"),
    ("GPS vue commune (code)",                 5e-9,   3e-9,  "récepteurs étalonnés — N2"),
    ("GPS phase de porteuse / PPP",            1e-9,   1e-10, "récepteur géodésique — N2/N3"),
    ("Deux voies par satellite (TWSTFT)",      1e-9,   5e-10, "station dédiée — N3"),
    ("White Rabbit (fibre, ≤ 10 km)",          5e-10,  1e-11, "commutateur + nœuds, ≥ 5 k€ — N2/N3"),
    ("Lien optique fibré stabilisé (fréquence)", None, None,  "métrologie nationale — N3 (1e-18 à 1e-20 en fréquence)"),
]
L.append("2. Méthodes de transfert de temps (ordres de grandeur d'usage courant)")
L.append(f"   {'méthode':<42}{'exactitude':>12}{'bruit':>10}   σ_y(1 jour) ≈ √3·σ_x/τ   cadre")
D["methodes"] = []
for nom, exa, bruit, cadre in METHODES:
    if exa is None:
        L.append(f"   {nom:<42}{'—':>12}{'—':>10}   {'1e-18 … 1e-20':>20}   {cadre}")
        D["methodes"].append({"methode": nom, "cadre": cadre})
        continue
    sy = math.sqrt(3) * bruit / 86400.0
    D["methodes"].append({"methode": nom, "exactitude_s": exa, "bruit_s": bruit, "sigma_y_1j": sy, "cadre": cadre})
    L.append(f"   {nom:<42}{sci(exa,2):>12}{sci(bruit,2):>10}   {sci(sy,2):>20}   {cadre}")
sig_1000 = g0 * 1000 / c**2
L.append(f"   Repère : décalage gravitationnel pour 1000 m = {sci(sig_1000)} ; pour 1 m = {sci(sig_1000/1000)}.")
L.append("   → une comparaison par GPS vue commune (≈ 6e-14 à 1 jour) entre une station de plaine et une station")
L.append("     de montagne ne résout 1000 m de dénivelé qu'après plusieurs jours, ET seulement si les horloges")
L.append("     locales sont elles-mêmes au niveau 1e-14 (césium, maser).")
L.append("")

# ---------------------------------------------------------------- 3. Monte-Carlo : échange bidirectionnel
# Protocole à 4 horodatages : t1 (départ A), t2 (arrivée B), t3 (départ B), t4 (arrivée A)
#   décalage estimé = [(t2 - t1) - (t4 - t3)]/2 ; erreur systématique = (d_AB - d_BA)/2
rng = np.random.default_rng(204)
def simulation(d_ab, d_ba, gigue, n=20000, vrai_decalage=1.234e-3):
    t1 = np.zeros(n)
    t2 = t1 + d_ab + rng.exponential(gigue, n) + vrai_decalage
    t3 = t2 + 1e-4
    t4 = t3 - vrai_decalage + d_ba + rng.exponential(gigue, n)
    est = ((t2 - t1) - (t4 - t3)) / 2
    return est - vrai_decalage

CAS = {
    "NTP Internet (asymétrie 4 ms, gigue 2 ms)":        (24e-3, 20e-3, 2e-3),
    "NTP réseau local (asym. 50 µs, gigue 100 µs)":     (350e-6, 300e-6, 100e-6),
    "PTP matériel (asym. 40 ns, gigue 20 ns)":          (5.04e-6, 5.00e-6, 20e-9),
    "White Rabbit (asym. résiduelle 100 ps, gigue 10 ps)": (25.0001e-6, 25.0e-6, 10e-12),
}
L.append("3. Simulation ILLUSTRATIVE d'un échange bidirectionnel à quatre horodatages")
L.append("   décalage estimé = [(t2 - t1) - (t4 - t3)]/2 ; l'asymétrie des délais N'EST PAS observable de l'intérieur")
D["simulation"] = {}
erreurs = {}
for nom, (dab, dba, gig) in CAS.items():
    e = simulation(dab, dba, gig)
    erreurs[nom] = e
    D["simulation"][nom] = {"biais_s": float(np.mean(e)), "ecart_type_s": float(np.std(e)),
                            "biais_attendu_s": (dab - dba) / 2}
    L.append(f"   {nom:<52} biais = {sci(np.mean(e))} s (attendu {sci((dab-dba)/2)}), écart-type = {sci(np.std(e))} s")
L.append("   Leçon : le protocole mesure (décalage d'horloge + demi-asymétrie des trajets). Sans étalonnage")
L.append("   indépendant des retards, le biais reste invisible — 1 m de fibre mal comptée = 4,9 ns.")
L.append("")

# ---------------------------------------------------------------- 4. retards de câbles
L.append("4. Retards de propagation (expérience N1 : mesurer un câble avec deux récepteurs GPS)")
for nom, vf in (("coaxial RG-58 (facteur de vélocité 0,66)", 0.66), ("coaxial à diélectrique mousse (0,83)", 0.83),
                ("fibre optique (indice de groupe 1,468)", 1 / 1.468), ("vide / air", 1.0)):
    L.append(f"   {nom:<44}: {1e9/(vf*c):.2f} ns/m ; 10 m → {10e9/(vf*c):.1f} ns")
gigue_pps = 8e-9
N = 600
L.append(f"   Avec un bruit de 1PPS de {gigue_pps*1e9:.0f} ns (un sigma) par récepteur et N = {N} secondes de moyenne :")
L.append(f"   incertitude sur la différence = √2·{gigue_pps*1e9:.0f} ns/√{N} = {math.sqrt(2)*gigue_pps/math.sqrt(N)*1e9:.2f} ns "
         f"→ 10 m de RG-58 (50,5 ns) mesurés à ~1 % (hors biais lents du récepteur).")
D["cables"] = {"rg58_ns_par_m": 1e9 / (0.66 * c), "fibre_ns_par_m": 1.468e9 / c,
               "incertitude_diff_ns": math.sqrt(2) * gigue_pps / math.sqrt(N) * 1e9}
L.append("")
L.append("Ce que l'on mesure réellement : toujours une DIFFÉRENCE de dates d'événements locaux (fronts 1PPS),")
L.append("augmentée de retards de propagation qu'il faut modéliser (géométrie, ionosphère, troposphère, câbles,")
L.append("Sagnac, relativité). Aucune de ces techniques ne « mesure le temps à distance » sans hypothèse sur la")
L.append("propagation ; aucune ne permet d'envoyer une information vers le passé.")

sauver("calc02_transfert_temps", D, L)

# ---------------------------------------------------------------- figure
fig, axes = plt.subplots(1, 2, figsize=(12.5, 5.2))
ax = axes[0]
noms = [m[0] for m in METHODES if m[1] is not None]
exa = [m[1] for m in METHODES if m[1] is not None]
bru = [m[2] for m in METHODES if m[1] is not None]
ypos = np.arange(len(noms))
ax.barh(ypos - 0.2, exa, height=0.38, color="#33658a", label="exactitude typique (biais non étalonnés)")
ax.barh(ypos + 0.2, bru, height=0.38, color="#f6ae2d", label="bruit de temps court terme")
ax.set_xscale("log")
ax.set_yticks(ypos)
ax.set_yticklabels(noms, fontsize=8)
ax.invert_yaxis()
ax.set_xlabel("secondes")
ax.axvline(9.4e-9, color="crimson", ls="--", lw=1)
ax.text(9.4e-9 * 1.3, len(noms) - 0.6, "écart dû à 1000 m\nde dénivelé en 1 jour\n(9,4 ns)", color="crimson", fontsize=7.5)
ax.set_title("Méthodes de transfert de temps\n(ordres de grandeur indicatifs)", fontsize=10)
ax.legend(fontsize=7.5, loc="lower right")
ax.grid(True, which="both", axis="x", alpha=0.25)

ax = axes[1]
for nom, e in erreurs.items():
    lo, hi = np.percentile(np.abs(e), [1, 99])
    ax.hist(np.abs(e), bins=np.logspace(math.log10(max(lo, 1e-13)), math.log10(hi), 60), alpha=0.6,
            label=nom.split(" (")[0])
ax.set_xscale("log")
ax.set_xlabel("|erreur sur le décalage estimé| (s)")
ax.set_ylabel("nombre de tirages")
ax.set_title("Échange bidirectionnel : erreur dominée par l'asymétrie des délais\n(simulation illustrative, pas une mesure)",
             fontsize=10)
ax.legend(fontsize=8)
ax.grid(True, which="both", alpha=0.25)
fig.tight_layout()
fig.savefig(fig_chemin("calc02_transfert_temps.png"), dpi=150)
print("figure :", fig_chemin("calc02_transfert_temps.png"))

# -*- coding: utf-8 -*-
"""C204 — Équipe C. Question Q4 (ingénierie) : quelle énergie électromagnétique faut-il stocker pour produire,
par son seul contenu en énergie, 2 g à 1 m ? Comparaison aux plus gros aimants, bancs de condensateurs et lasers.

Sorties : resultats/c10_Q4.json, c10_Q4_comparaisons.csv
"""
import csv
import os
import numpy as np
import c00_constantes as K

res = {}
a, r = 2 * K.g0, 1.0
M_eq = a * r**2 / K.G
E = M_eq * K.c**2
res["masse_equivalente_kg"] = M_eq
res["energie_requise_J"] = E
res["energie_requise_Mt_TNT"] = E / K.Mt_TNT
res["energie_requise_secondes_de_Soleil"] = E / K.Lsol

# Installations réelles (énergie stockée ou délivrée, J) — voir REFERENCES.md
install = {
    "ITER, ensemble des aimants supraconducteurs (51 GJ)": 51e9,
    "ITER, bobines toroïdales (41 GJ)": 41e9,
    "LHC, dipôles principaux (8,82 GJ)": 8.82e9,
    "CMS, solénoïde à 4 T (2,6 GJ)": 2.6e9,
    "NIF, banc de condensateurs (~400 MJ nominal)": 400e6,
    "LHC, un faisceau nominal (362 MJ)": 362e6,
    "Z machine, générateurs de Marx (22 MJ)": 22e6,
    "NIF, rendement de fusion record (8,6 MJ, 2025)": 8.6e6,
    "ISSP 1200 T, banc de condensateurs (5 MJ)": 5e6,
    "NIF, énergie laser UV sur cible (2,2 MJ)": 2.2e6,
    "production mondiale d'électricité 2023 (29 925 TWh)": 29925 * K.TWh,
    "énergie primaire mondiale 2023 (620 EJ)": 620 * K.EJ,
}
lignes = []
for nom, e_ in install.items():
    g_1m = K.G * (e_ / K.c**2) / r**2
    lignes.append(dict(installation=nom, energie_J=e_, masse_equivalente_kg=e_ / K.c**2,
                       g_a_1m_m_s2=g_1m, g_a_1m_en_g=g_1m / K.g0, g_a_1m_uGal=g_1m / K.uGal,
                       rapport_energie_requise=E / e_, ordres_de_grandeur_manquants=float(np.log10(E / e_))))
with open(os.path.join(K.RES, "c10_Q4_comparaisons.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
    w.writeheader()
    for li in lignes:
        w.writerow({k_: (f"{v:.4g}" if isinstance(v, float) else v) for k_, v in li.items()})
res["comparaisons"] = lignes

# Densité d'énergie si l'on loge E dans une sphère de rayon 0,10 m (pour tenir dans le coffre et rester à < 1 m)
V = 4 / 3 * np.pi * 0.10**3
u = E / V
res["dans_une_sphere_de_10cm"] = dict(
    volume_m3=V, densite_energie_J_m3=u, pression_Pa=u,
    B_equivalent_T=float(np.sqrt(2 * K.mu0 * u)), E_equivalent_V_m=float(np.sqrt(2 * u / K.eps0)),
    E_sur_Schwinger=float(np.sqrt(2 * u / K.eps0) / K.E_SCHWINGER),
    B_sur_B_critique_QED=float(np.sqrt(2 * K.mu0 * u) / (K.me**2 * K.c**2 / (K.e * K.hbar))))
res["B_critique_QED_T"] = K.me**2 * K.c**2 / (K.e * K.hbar)

# Théorème du viriel : contenir une énergie de champ E exige une masse de structure M_s >= rho E / sigma
materiaux = {"acier à haute résistance (σ = 2 GPa, ρ = 7800)": (2e9, 7800.0),
             "fibre de carbone (σ = 3,5 GPa, ρ = 1800) [ordre de grandeur]": (3.5e9, 1800.0),
             "limite idéale type graphène (σ = 130 GPa, ρ = 2200) [ordre de grandeur]": (130e9, 2200.0)}
vir = {}
for nom, (s, rho) in materiaux.items():
    Ms = rho * E / s
    vir[nom] = dict(masse_structure_kg=Ms, rapport_masse_structure_sur_masse_du_champ=Ms / M_eq,
                    fraction_max_du_champ_dans_la_masse_totale=s / (rho * K.c**2),
                    masse_structure_en_masses_lunaires=Ms / 7.342e22)
res["viriel"] = vir
# Inversement : gravité propre du champ des meilleurs aimants réels (45,5 T dans 1 litre)
u45 = 45.5**2 / (2 * K.mu0)
res["champ_45p5T_dans_1_litre"] = dict(energie_J=u45 * 1e-3, masse_equivalente_kg=u45 * 1e-3 / K.c**2,
                                       g_a_10cm_m_s2=K.G * u45 * 1e-3 / K.c**2 / 0.1**2)
# Batterie : masse-énergie du contenu électrique d'un pack de 7,5 kWh
res["pack_7p5kWh"] = dict(masse_equivalente_kg=7.5 * K.kWh / K.c**2, g_a_1m_m_s2=K.G * 7.5 * K.kWh / K.c**2)

K.sauver_json("c10_Q4.json", res)
print(f"2 g à 1 m : M = {M_eq:.3e} kg ; E = {E:.3e} J = {E/K.Mt_TNT:.2e} Mt TNT = {E/K.Lsol:.0f} s de Soleil")
for li in lignes:
    print(f"{li['installation']:56s} E={li['energie_J']:.2e} J  m={li['masse_equivalente_kg']:.2e} kg  "
          f"g(1 m)={li['g_a_1m_m_s2']:.2e} m/s²  manque {li['ordres_de_grandeur_manquants']:.1f} décades")
print("Sphère 10 cm :", {k_: f"{v:.3g}" for k_, v in res["dans_une_sphere_de_10cm"].items()})
print("Viriel :", {k_: {a_: f"{b:.3g}" for a_, b in v.items()} for k_, v in vir.items()})
print("45,5 T dans 1 L :", res["champ_45p5T_dans_1_litre"])
print("Pack :", res["pack_7p5kWh"])

# -*- coding: utf-8 -*-
"""C204 — Équipe C. Sous-système 1 : les deux « singularités » et leur logement magnétique (repères 1-2-3).

Calcule, pour M de 100 kg à ~10^12 kg :
  - force de sustentation F = M g ;
  - charge maximale (Reissner-Nordström extrémal) et rapport charge/masse ;
  - champ électrique de sustentation, champ à l'horizon, comparaison à la limite de Schwinger ;
  - piège de Penning et piège de Paul équivalents (théorème d'Earnshaw : pas de piège purement statique) ;
  - force sur le dipôle magnétique maximal (Kerr-Newman) ;
  - pressions magnétiques, limite matérielle B_max = sqrt(2 mu0 sigma) ;
  - gravité propre et marée sur le carter à 1 mm, 1 cm, 10 cm, 1 m ;
  - attraction mutuelle des deux singularités.

Sorties : resultats/c02_confinement.json, c02_confinement_par_masse.csv, c02_gravite_propre.csv
"""
import csv
import os
import numpy as np
import c00_constantes as K

MASSES = [1e2, 1e4, 1e6, 1e8, 1e10, 2.94e11, 1e12, 4.4e12]
Z_RMS_PAGE = 6.14     # charge rms (en e) d'un trou noir chaud, Page, Phys. Rev. D 16, 2402 (1977), limite sans masse
D_SAG = 0.01          # m : excursion tolérée de la singularité dans son carter [HYP]
D_PAIRE = K.D_PAIRE   # m : entraxe des deux logements (Équipe A, DOC-007 : 0,098 m) — correction n° 32
R_CARTER = K.R_CARTER # m : rayon du logement/carter (Équipe A, DOC-007 : 0,0385 m) — correction n° 32
D_PAIRE_ANCIEN, R_CARTER_ANCIEN = 0.15, 0.05   # anciennes hypothèses [HYP], gardées pour la sensibilité

res = {}

# ---------------------------------------------------------------- constantes indépendantes de la masse
qm = K.QM_MAX
res["rapport_charge_masse_max_C_par_kg"] = qm
res["rapport_charge_masse_electron_C_par_kg"] = K.e / K.me
res["rapport_des_deux"] = qm / (K.e / K.me)
E_lev = K.g0 / qm                                    # champ de sustentation pour un trou noir extrémal
res["E_sustentation_extremal_V_par_m"] = E_lev
res["pression_electrostatique_associee_Pa"] = 0.5 * K.eps0 * E_lev**2
res["E_Schwinger_V_par_m"] = K.E_SCHWINGER
res["potentiel_horizon_extremal_V"] = K.c**2 / qm    # Phi_H = Q/(4 pi eps0 r+) avec r+ = GM/c^2
# masse minimale pour qu'un trou noir extrémal ait un champ à l'horizon inférieur à la limite de Schwinger
M_min_charge = K.c**4 / (K.G**1.5 * np.sqrt(4 * np.pi * K.eps0) * K.E_SCHWINGER)
res["M_min_charge_extremale_stable_kg"] = M_min_charge
res["M_min_charge_extremale_stable_Msol"] = M_min_charge / K.Msol
# estimation thermique de la charge rms : Z^2 ~ kT r_s 4 pi eps0 / e^2 = 1/(4 pi alpha)
res["Z_rms_estimation_thermique"] = 1 / np.sqrt(4 * np.pi * K.alpha_fs)
res["Z_rms_Page_1977"] = Z_RMS_PAGE

# Piège de Penning : stabilité radiale omega_c^2 > 2 omega_z^2 ; tenue de la pesanteur avec un affaissement
# d : omega_z^2 >= g/d.  ->  B >= sqrt(2 g/d) / (q/m)
omega_z = np.sqrt(K.g0 / D_SAG)
B_penning = np.sqrt(2) * omega_z / qm
res["penning"] = dict(omega_z_min_rad_s=omega_z, B_min_extremal_T=B_penning,
                      omega_c_a_45p5T_rad_s=qm * 45.5,
                      periode_cyclotron_a_45p5T_ans=2 * np.pi / (qm * 45.5) / K.an,
                      rapport_B_requis_sur_45p5T=B_penning / 45.5)
# Piège de Paul : q_M = 2 q V/(m r0^2 Omega^2) (stable si < 0,908), omega_sec ≈ q_M Omega/(2 sqrt 2)
qM, r0 = 0.4, 0.01
Omega = omega_z * 2 * np.sqrt(2) / qM
V_rf = qM * r0**2 * Omega**2 / (2 * qm)
res["paul"] = dict(q_Mathieu=qM, r0_m=r0, Omega_rad_s=Omega, V_RF_V=V_rf, E_typique_V_par_m=V_rf / r0)

# Limites réelles de champ électrique (V/m) — voir REFERENCES.md
limites_E = {
    "claquage du vide, grands intervalles DC (ordre de grandeur) [HYP]": 1e7,
    "gradient accélérateur RF bande X (CLIC)": 1e8,
    "rigidité diélectrique idéale du diamant (10 MV/cm)": 1e9,
    "évaporation par effet de champ du tungstène (57 V/nm)": 5.7e10,
    "limite de Schwinger": K.E_SCHWINGER,
}
res["limites_E_V_par_m"] = limites_E
res["E_sustentation_sur_limites"] = {k_: E_lev / v for k_, v in limites_E.items()}

# Limites réelles de champ magnétique (T) et pressions magnétiques
champs = {"aimant supraconducteur compact (20 T)": 20.0, "record continu hybride/HTS (45,5 T)": 45.5,
          "record pulsé non destructif (100,75 T)": 100.75, "record intérieur destructif (1200 T)": 1200.0,
          "compression explosive (2800 T)": 2800.0, "champ requis Penning, charge extrémale": B_penning}
res["pression_magnetique_Pa"] = {k_: v**2 / (2 * K.mu0) for k_, v in champs.items()}
res["champs_T"] = champs
res["B_max_materiau_T"] = {f"sigma = {s/1e9:g} GPa": float(np.sqrt(2 * K.mu0 * s))
                           for s in (1e9, 5.8e9, 130e9)}

# ---------------------------------------------------------------- par masse
lignes = []
for M in MASSES:
    rs = K.RS_PAR_KG * M
    F = M * K.g0
    Qmax = qm * M
    # champ à l'horizon d'un trou noir extrémal (r+ = GM/c^2)
    E_h = Qmax / (4 * np.pi * K.eps0 * (K.G * M / K.c**2) ** 2)
    # charge telle que le champ en r_s égale la limite de Schwinger (critère champ homogène, indicatif)
    Q_schw = 4 * np.pi * K.eps0 * rs**2 * K.E_SCHWINGER
    E_real = F / (Z_RMS_PAGE * K.e)                  # champ de sustentation avec la charge rms réaliste
    B_real = np.sqrt(2) * omega_z * M / (Z_RMS_PAGE * K.e)
    mu_max = 0.5 * Qmax * K.G * M / K.c              # dipôle magnétique maximal (Q = Qmax/√2, a = a_max/√2)
    gradB = F / mu_max
    lignes.append(dict(
        M_kg=M, r_s_m=rs, poids_N=F, Q_max_C=Qmax, Z_max=Qmax / K.e,
        E_horizon_extremal_V_m=E_h, E_horizon_sur_Schwinger=E_h / K.E_SCHWINGER,
        Q_Schwinger_C=Q_schw, Z_Schwinger=Q_schw / K.e,
        E_sustentation_charge_extremale_V_m=E_lev,
        E_sustentation_charge_6e_V_m=E_real, E_6e_sur_Schwinger=E_real / K.E_SCHWINGER,
        B_Penning_extremal_T=B_penning, B_Penning_charge_6e_T=B_real,
        dipole_max_A_m2=mu_max, gradient_B_requis_T_par_m=gradB,
        pression_reaction_carter_Pa=F / (np.pi * R_CARTER**2),
        attraction_mutuelle_N=K.G * M**2 / D_PAIRE**2,
        attraction_mutuelle_sur_poids=K.G * M / D_PAIRE**2 / K.g0,
        periode_orbitale_mutuelle_s=2 * np.pi * np.sqrt(D_PAIRE**3 / (2 * K.G * M))))
with open(os.path.join(K.RES, "c02_confinement_par_masse.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
    w.writeheader()
    for li in lignes:
        w.writerow({k_: f"{v:.4g}" for k_, v in li.items()})
res["par_masse"] = lignes

# Masse maximale supportable par un carter de rayon R_CARTER avec sigma = 1 GPa (réaction du poids)
res["M_max_structure_1GPa_kg"] = 1e9 * np.pi * R_CARTER**2 / K.g0
res["geometrie"] = dict(entraxe_m=D_PAIRE, rayon_carter_m=R_CARTER, source=K.SOURCE_GEOMETRIE)
# Sensibilité à l'ancienne géométrie [HYP] (entraxe 0,15 m, rayon 0,05 m), pour M = 4,4e12 kg
_M = 4.4e12
res["sensibilite_ancienne_geometrie_M_4p4e12"] = dict(
    attraction_mutuelle_sur_poids=K.G * _M / D_PAIRE_ANCIEN**2 / K.g0,
    periode_orbitale_s=2 * np.pi * np.sqrt(D_PAIRE_ANCIEN**3 / (2 * K.G * _M)),
    pression_reaction_carter_Pa=_M * K.g0 / (np.pi * R_CARTER_ANCIEN**2))
res["gradients_B_reels_T_par_m"] = {"aimant de lévitation diamagnétique (ordre de grandeur) [HYP]": 1e2,
                                    "pointes micromagnétiques (ordre de grandeur) [HYP]": 1e6}

# ---------------------------------------------------------------- gravité propre sur le carter
grav = []
for M in MASSES:
    for r in (1e-3, 1e-2, 1e-1, 1.0):
        g = K.G * M / r**2
        grav.append(dict(M_kg=M, r_m=r, g_m_s2=g, g_en_g=g / K.g0, maree_s2=2 * K.G * M / r**3,
                         maree_Eotvos=2 * K.G * M / r**3 / K.Eotvos,
                         # pression hydrostatique dans de l'acier plein entre r et 10 cm
                         pression_acier_Pa=(7800 * K.G * M * (1 / r - 1 / 0.1) if r < 0.1 else 0.0)))
with open(os.path.join(K.RES, "c02_gravite_propre.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(grav[0].keys()))
    w.writeheader()
    for li in grav:
        w.writerow({k_: f"{v:.4g}" for k_, v in li.items()})
res["gravite_propre"] = grav

K.sauver_json("c02_confinement.json", res)

# ---------------------------------------------------------------- affichage
print(f"(Q/M)max = {qm:.4e} C/kg ; e/m_e = {K.e/K.me:.4e} C/kg ; rapport = {res['rapport_des_deux']:.3e}")
print(f"E de sustentation (charge extrémale, indépendant de M) = {E_lev:.3e} V/m "
      f"(pression électrostatique {res['pression_electrostatique_associee_Pa']:.2e} Pa)")
for k_, v in res["E_sustentation_sur_limites"].items():
    print(f"   / {k_} : x{v:.2e}")
print(f"Potentiel d'horizon extrémal = {res['potentiel_horizon_extremal_V']:.3e} V")
print(f"M min pour charge extrémale stable (E_h < E_S) = {M_min_charge:.3e} kg = {M_min_charge/K.Msol:.2e} Msol")
print(f"Z_rms thermique = {res['Z_rms_estimation_thermique']:.2f} e (Page 1977 : {Z_RMS_PAGE} e)")
print("Penning :", res["penning"])
print("Paul :", res["paul"])
print("Pressions magnétiques (Pa) :", {k_: f"{v:.2e}" for k_, v in res["pression_magnetique_Pa"].items()})
print("B max matériau :", res["B_max_materiau_T"])
print(f"M max structure (sigma 1 GPa, carter r = {R_CARTER} m) = {res['M_max_structure_1GPa_kg']:.2e} kg")
print("Géométrie :", res["geometrie"], "| sensibilité ancienne :", res["sensibilite_ancienne_geometrie_M_4p4e12"])
for li in lignes:
    print(f"M={li['M_kg']:.2e}  F={li['poids_N']:.2e} N  Qmax={li['Q_max_C']:.2e} C  "
          f"E_h/E_S={li['E_horizon_sur_Schwinger']:.1e}  E(6e)={li['E_sustentation_charge_6e_V_m']:.1e} V/m  "
          f"B(6e)={li['B_Penning_charge_6e_T']:.1e} T  gradB={li['gradient_B_requis_T_par_m']:.1e} T/m  "
          f"p_carter={li['pression_reaction_carter_Pa']:.1e} Pa  F_mut/poids={li['attraction_mutuelle_sur_poids']:.1e} "
          f"T_orb={li['periode_orbitale_mutuelle_s']:.2e} s")
for li in grav:
    if li["M_kg"] in (2.94e11, 4.4e12):
        print(f"M={li['M_kg']:.2e} r={li['r_m']:g} m : g={li['g_m_s2']:.3e} m/s² ({li['g_en_g']:.2e} g) "
              f"marée={li['maree_s2']:.2e} s⁻² p_acier={li['pression_acier_Pa']:.2e} Pa")

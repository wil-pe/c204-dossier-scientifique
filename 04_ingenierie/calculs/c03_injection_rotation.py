# -*- coding: utf-8 -*-
"""C204 — Équipe C. Sous-systèmes 2 et 3 : injection d'électrons (repères 4-5-6) et mise en rotation.

Sorties : resultats/c03_injection_rotation.json, c03_injection_par_masse.csv
"""
import csv
import os
import numpy as np
import c00_constantes as K

H = K.charger_json("c01_hawking.json")
ALPHA_M12 = H["synthese"]["alpha_M_1e12kg"]
BETA_E = H["taux_nombre"]["beta_e_par_etat"]      # taux d'émission par état de spin 1/2, en c^3/(GM)

MASSES = [1e2, 1e6, 2.94e11, 1e12, 4.4e12]
res = {}

# ------------------------------------------------------------------ 2. injection d'électrons
ratio = K.QM_MAX / (K.e / K.me)
res["delta_M_sur_M_a_charge_extremale_par_electrons"] = ratio
res["energie_electron_pour_franchir_barriere_extremale_eV"] = K.c**2 / K.QM_MAX   # e*Phi_H en eV
res["energie_LHC_par_proton_eV"] = 6.8e12
res["energie_rayon_cosmique_record_eV"] = 3.2e20     # événement « Oh-My-God » (ordre de grandeur) [non vérifié en ligne]

spots = {"canon ordinaire, tache 1 mm²": 1e-6, "microfaisceau 1 µm²": 1e-12,
         "tache 41 nm x 41 nm (ordre ATF2, vertical)": (41e-9) ** 2,
         "sonde STEM 50 pm de diamètre": np.pi * (25e-12) ** 2}
lignes = []
for M in MASSES:
    rs = K.RS_PAR_KG * M
    Qmax = K.QM_MAX * M
    n_ext = Qmax / K.e
    sigma_geo = 27 * np.pi * K.G**2 * M**2 / K.c**4          # capture géométrique (ultra-relativiste)
    sigma_bas = 2 * np.pi * K.G**2 * M**2 / K.c**4           # fermion sans masse, basse énergie (A/8)
    E_seuil = K.hbar * K.c / rs                              # énergie pour lambda_dB/2pi < r_s
    barriere_par_Z = K.e**2 / (4 * np.pi * K.eps0 * rs)      # J par charge élémentaire portée par le trou
    Z_crit_grav = 4 * np.pi * K.eps0 * K.G * M * K.me / K.e**2   # Z au-delà duquel Coulomb > gravité (e- lent)
    # Variation de masse de 1 %
    dM = 0.01 * M
    n_1pc = dM / K.me
    Q_1pc = n_1pc * K.e
    kT = K.kB * K.T_HAWKING_KG / M
    P_H = ALPHA_M12 * K.K_HAWKING / M**2
    # décharge : taux d'émission de e+/e- (4 états), biais ~ Z e^2/(4 pi eps0 r_s kT)
    N_e = 4 * BETA_E * K.c**3 / (K.G * M)
    biais_par_Z = barriere_par_Z / kT
    tau_decharge = 1.0 / (N_e * biais_par_Z)
    li = dict(M_kg=M, r_s_m=rs, Q_max_C=Qmax, electrons_pour_charge_extremale=n_ext,
              masse_de_ces_electrons_kg=n_ext * K.me,
              sigma_capture_geo_m2=sigma_geo, sigma_capture_geo_barn=sigma_geo / 1e-28,
              sigma_basse_energie_m2=sigma_bas, E_seuil_onde_courte_MeV=E_seuil / K.MeV,
              barriere_coulombienne_par_charge_MeV=barriere_par_Z / K.MeV,
              Z_pour_barriere_10MeV=10 * K.MeV / barriere_par_Z,
              Z_critique_Coulomb_egale_gravite=Z_crit_grav,
              alpha_G_electron=K.G * M * K.me / (K.hbar * K.c),
              electrons_pour_1pc_de_masse=n_1pc, charge_correspondante_C=Q_1pc,
              charge_1pc_sur_Qmax=Q_1pc / Qmax,
              duree_a_1mA_ans=Q_1pc / 1e-3 / K.an, duree_a_1A_ans=Q_1pc / K.an,
              duree_a_1MA_ans=Q_1pc / 1e6 / K.an,
              energie_1pc_de_masse_J=dM * K.c**2,
              puissance_Hawking_W=P_H, apport_de_masse_pour_compenser_kg_s=P_H / K.c**2,
              taux_emission_e_par_s=N_e, temps_de_decharge_s=tau_decharge)
    for nom, A in spots.items():
        li[f"fraction_capturee[{nom}]"] = sigma_geo / A
    lignes.append(li)

with open(os.path.join(K.RES, "c03_injection_par_masse.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(lignes[0].keys()))
    w.writeheader()
    for li in lignes:
        w.writerow({k_: f"{v:.4g}" for k_, v in li.items()})
res["injection_par_masse"] = lignes

# Courants réels
I_rec = 65e-3      # A, record de courant moyen d'un photo-injecteur (Dunham et al. 2013)
ref = lignes[3]    # M = 1e12 kg
res["exemple_M_1e12kg"] = dict(
    courant_A=I_rec, electrons_par_s=I_rec / K.e,
    captures_par_s_tache_1um2=I_rec / K.e * ref["fraction_capturee[microfaisceau 1 µm²]"],
    masse_ajoutee_kg_par_s_tache_1um2=I_rec / K.e * ref["fraction_capturee[microfaisceau 1 µm²]"] * K.me,
    perte_Hawking_kg_par_s=ref["apport_de_masse_pour_compenser_kg_s"])
res["exemple_M_1e12kg"]["rapport_perte_sur_gain"] = (
    res["exemple_M_1e12kg"]["perte_Hawking_kg_par_s"] / res["exemple_M_1e12kg"]["masse_ajoutee_kg_par_s_tache_1um2"])

# Énergie électrostatique d'un trou noir extrémal : moitié de M c^2 (M_irr = M/2)
res["energie_pour_charger_a_l_extremal_fraction_Mc2"] = 0.5

# ------------------------------------------------------------------ 3. rotation et axe
rot = []
for M in MASSES:
    J = K.G * M**2 / K.c
    Om_H = K.c**3 / (2 * K.G * M)
    E_rot = (1 - 1 / np.sqrt(2)) * M * K.c**2
    # couple magnétique maximal : mu = Q J / M (g = 2) ; précession Omega = mu B / J = (Q/M) B
    prec_45 = K.QM_MAX * 45.5
    # avec la charge réaliste (6,14 e)
    prec_reel = 6.14 * K.e / M * 45.5
    rot.append(dict(M_kg=M, J_max_kg_m2_s=J, J_max_en_hbar=J / K.hbar, a_max_m=K.G * M / K.c**2,
                    Omega_horizon_extremal_rad_s=Om_H, energie_rotation_max_J=E_rot,
                    energie_rotation_max_sur_Mc2=1 - 1 / np.sqrt(2),
                    precession_45p5T_charge_extremale_rad_s=prec_45,
                    periode_precession_charge_extremale_ans=2 * np.pi / prec_45 / K.an,
                    precession_45p5T_charge_6e_rad_s=prec_reel,
                    B_pour_1_rad_s_charge_extremale_T=1.0 / K.QM_MAX,
                    # énergie lumineuse minimale pour atteindre J_max avec paramètre d'impact critique 3√3 GM/c²
                    energie_mise_en_rotation_J=M * K.c**2 / (3 * np.sqrt(3))))
res["rotation"] = rot
res["bardeen_masse_finale_sur_initiale_pour_extremal"] = float(np.sqrt(6))

K.sauver_json("c03_injection_rotation.json", res)

print(f"ΔM/M quand la charge extrémale est atteinte par apport d'électrons = {ratio:.3e}")
print(f"Énergie pour amener le dernier électron sur un trou extrémal = "
      f"{res['energie_electron_pour_franchir_barriere_extremale_eV']:.3e} eV")
for li in lignes:
    print(f"M={li['M_kg']:.2e}: sigma_geo={li['sigma_capture_geo_barn']:.3e} b  E_seuil={li['E_seuil_onde_courte_MeV']:.3e} MeV  "
          f"barrière/Z={li['barriere_coulombienne_par_charge_MeV']:.3e} MeV  Z_crit(C=G)={li['Z_critique_Coulomb_egale_gravite']:.3e}  "
          f"1 % masse : {li['electrons_pour_1pc_de_masse']:.2e} e-, {li['charge_correspondante_C']:.2e} C "
          f"({li['duree_a_1A_ans']:.2e} ans à 1 A)  décharge {li['temps_de_decharge_s']:.1e} s  "
          f"capt(1µm²)={li['fraction_capturee[microfaisceau 1 µm²]']:.1e}")
print("Exemple 1e12 kg :", res["exemple_M_1e12kg"])
for r in rot:
    print(f"M={r['M_kg']:.2e}: Jmax={r['J_max_kg_m2_s']:.3e} ({r['J_max_en_hbar']:.2e} ħ)  Ω_H={r['Omega_horizon_extremal_rad_s']:.2e} rad/s  "
          f"E_rot={r['energie_rotation_max_J']:.2e} J  précession(45,5 T, extrémal)={r['precession_45p5T_charge_extremale_rad_s']:.2e} rad/s "
          f"(période {r['periode_precession_charge_extremale_ans']:.1f} ans) ; charge 6e : {r['precession_45p5T_charge_6e_rad_s']:.1e} rad/s")

# -*- coding: utf-8 -*-
"""C204 — Équipe C. Sous-système 4 : refroidissement (repères 8-9-10) et « évacuation des rayons X ».

Charges thermiques, débits de caloporteur, radiateurs, flux pariétaux, blindage, débits de dose,
collimation. Données d'atténuation : NIST XCOM / X-Ray Mass Attenuation Coefficients ; longueurs de
radiation : PDG ; TVL : NCRP 151 (voir REFERENCES.md).

Sorties : resultats/c05_refroidissement.json, c05_debits.csv, c05_radiateurs.csv, c05_doses.csv
"""
import csv
import os
import numpy as np
import c00_constantes as K

H = K.charger_json("c01_hawking.json")
FR = H["synthese"]["fractions_M_1e12kg"]
F_DEP = FR["photons"] + FR["electrons_positrons"]        # fraction déposée localement (hors neutrinos, gravitons)
res = {"fractions_de_puissance": FR, "fraction_deposee": F_DEP}

# ------------------------------------------------------------------ charges thermiques (W)
charges = {
    "min : 1 singularité, 300 MW au total (dépôt γ + e± seulement)": 300e6 * F_DEP,
    "réf. : 1 singularité, 400 MW au total (dépôt γ + e±)": 400e6 * F_DEP,
    "réf. x2 : 2 singularités, 400 MW chacune (dépôt γ + e±)": 2 * 400e6 * F_DEP,
    "énoncé bas : 300 MW entièrement déposés": 300e6,
    "énoncé haut : 2 x 500 MW entièrement déposés": 1000e6,
}
res["charges_thermiques_W"] = charges

# ------------------------------------------------------------------ débits de caloporteur
fluides = {  # nom : (cp J/kg/K, deltaT K, chaleur latente J/kg ou 0, masse volumique kg/m3)
    "eau liquide, ΔT = 50 K": (4186.0, 50.0, 0.0, 990.0),
    "eau vaporisée (20 → 100 °C + vaporisation)": (4186.0, 80.0, 2.257e6, 990.0),
    "sodium liquide, ΔT = 150 K": (1270.0, 150.0, 0.0, 850.0),
    "hélium gazeux 70 bar, ΔT = 300 K": (5193.0, 300.0, 0.0, 6.0),
}
D_TUYAU = 0.05            # m : diamètre d'une canalisation logeable dans le coffre [HYP]
DP_POMPE = 10e5           # Pa : perte de charge du circuit [HYP]
RENDEMENT_POMPE = 0.75
V_RESERVOIRS = 2 * K.V_RESERVOIR_SCHEMA         # m3 : 2 x 0,25 L, échelle du schéma DOC-008 (Équipes E et I)
V_RESERVOIRS_HAUT = 2 * K.V_RESERVOIR_BORNE_HAUTE  # m3 : 2 x 15 L, ancienne hypothèse [HYP] (86 % du volume utile)
debits = []
for nc, Q in charges.items():
    for nf, (cp, dT, L, rho) in fluides.items():
        h = cp * dT + L
        mdot = Q / h
        vdot = mdot / rho
        v = vdot / (np.pi * D_TUYAU**2 / 4)
        P_pompe = vdot * DP_POMPE / RENDEMENT_POMPE
        m_res = V_RESERVOIRS * rho
        m_res_haut = V_RESERVOIRS_HAUT * rho
        debits.append(dict(charge=nc, Q_W=Q, fluide=nf, debit_kg_s=mdot, debit_m3_s=vdot,
                           vitesse_dans_tuyau_5cm_m_s=v, puissance_pompe_W=P_pompe,
                           autonomie_reservoirs_s=(m_res / mdot if L > 0 else float("nan")),
                           autonomie_reservoirs_borne_haute_s=(m_res_haut / mdot if L > 0 else float("nan")),
                           masse_pour_6h_circuit_ouvert_kg=mdot * K.DUREE_TRAJET))
with open(os.path.join(K.RES, "c05_debits.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(debits[0].keys()))
    w.writeheader()
    for li in debits:
        w.writerow({k_: (f"{v:.4g}" if isinstance(v, float) else v) for k_, v in li.items()})
res["debits"] = debits

# ------------------------------------------------------------------ radiateurs et bilan thermique du coffre
rad = []
EPS = 0.9
T_AMB = 298.15
for nc, Q in charges.items():
    for T in (322.0, 600.0, 1000.0, 1500.0, 3000.0):
        flux = EPS * K.sigma_SB * (T**4 - T_AMB**4)
        rad.append(dict(charge=nc, Q_W=Q, T_radiateur_K=T, flux_net_W_m2=flux, surface_m2=Q / flux,
                        surface_sur_coffre=Q / flux / K.COFFRE_S))
with open(os.path.join(K.RES, "c05_radiateurs.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rad[0].keys()))
    w.writeheader()
    for li in rad:
        w.writerow({k_: (f"{v:.4g}" if isinstance(v, float) else v) for k_, v in li.items()})
res["radiateurs"] = rad
# température de surface du coffre s'il devait rayonner seul la charge
res["T_surface_coffre_K"] = {nc: float((Q / (EPS * K.sigma_SB * K.COFFRE_S) + T_AMB**4) ** 0.25)
                             for nc, Q in charges.items()}
# inversement : puissance qu'évacue un coffre dont la surface est à 38-49 °C (convection naturelle + rayonnement)
H_CONV = 5.0   # W/m2/K, convection naturelle [HYP]
res["puissance_coffre_a_T_revendiquee_W"] = {
    f"{t_c:.0f} °C": K.COFFRE_S * (H_CONV * (t_c + 273.15 - T_AMB)
                                    + EPS * K.sigma_SB * ((t_c + 273.15) ** 4 - T_AMB**4))
    for t_c in (38.0, 49.0, 80.0)}
# sensibilité : mêmes grandeurs avec l'ancienne hypothèse H1 (1,20 x 0,36 x 0,30 m ; 1,80 m2 ; 0,13 m3)
_L1, _P1, _H1 = K.COFFRE_H1
_S1, _V1 = 2 * (_L1 * _P1 + _L1 * _H1 + _P1 * _H1), _L1 * _P1 * _H1
res["geometrie"] = dict(L_m=K.COFFRE_L, P_m=K.COFFRE_P, H_m=K.COFFRE_H, surface_m2=K.COFFRE_S, volume_m3=K.COFFRE_V,
                        volume_utile_m3=K.VOLUME_UTILE, rayon_carter_m=K.R_CARTER, entraxe_m=K.D_PAIRE,
                        source=K.SOURCE_GEOMETRIE)
res["sensibilite_H1"] = dict(
    surface_m2=_S1, volume_m3=_V1,
    puissance_coffre_a_T_revendiquee_W={
        f"{t_c:.0f} °C": _S1 * (H_CONV * (t_c + 273.15 - T_AMB) + EPS * K.sigma_SB * ((t_c + 273.15) ** 4 - T_AMB**4))
        for t_c in (38.0, 49.0)},
    T_surface_coffre_K={nc: float((Q / (EPS * K.sigma_SB * _S1) + T_AMB**4) ** 0.25) for nc, Q in charges.items()},
    rapport_T_rayonnement=float((_S1 / K.COFFRE_S) ** 0.25))
# habitacle : UA ~ 60-100 W/K [HYP] ; puissance pour +15 à +25 K
res["puissance_pour_chauffer_habitacle_W"] = {"UA=60 W/K, ΔT=15 K": 60 * 15.0, "UA=100 W/K, ΔT=25 K": 100 * 25.0}

# ------------------------------------------------------------------ flux pariétal et densité de puissance
flux_ref = {"flux critique record, eau sous-refroidie (Mudawar & Bowers 1999)": 276e6,
            "col de tuyère du moteur SSME": 163e6, "divertor ITER (transitoires lents)": 20e6,
            "divertor ITER (permanent)": 10e6,
            "photosphère solaire (σT⁴, 5772 K)": K.sigma_SB * 5772.0**4}
res["flux_de_reference_W_m2"] = flux_ref
parois = {}
for nc, Q in charges.items():
    for r in (K.R_CARTER, 0.05, 0.10):
        q = Q / (4 * np.pi * r**2)
        parois[f"{nc} | carter r = {r*100:.3g} cm"] = dict(flux_W_m2=q, rapport_au_record_CHF=q / 276e6,
                                                          rapport_au_Soleil=q / flux_ref["photosphère solaire (σT⁴, 5772 K)"])
res["flux_parietal"] = parois
CLE_REF = "réf. : 1 singularité, 400 MW au total (dépôt γ + e±)"
res["flux_parietal_reference"] = dict(rayon_m=K.R_CARTER, **parois[f"{CLE_REF} | carter r = {K.R_CARTER*100:.3g} cm"],
                                      rapport_SSME=parois[f"{CLE_REF} | carter r = {K.R_CARTER*100:.3g} cm"]["flux_W_m2"] / 163e6,
                                      rapport_ITER_20MW=parois[f"{CLE_REF} | carter r = {K.R_CARTER*100:.3g} cm"]["flux_W_m2"] / 20e6,
                                      rapport_ITER_10MW=parois[f"{CLE_REF} | carter r = {K.R_CARTER*100:.3g} cm"]["flux_W_m2"] / 10e6)
res["densite_volumique_coffre_MW_par_L"] = {nc: Q / K.COFFRE_V / 1e9 for nc, Q in charges.items()}
res["densite_HFIR_MW_par_L"] = 1.7
# absorbeur en tungstène : sphère de 10 longueurs de radiation
X0_W = 0.3504e-2
r_abs = 10 * X0_W
V_abs = 4 / 3 * np.pi * r_abs**3
rho_W, cp_W, Tf_W, Lf_W = 19300.0, 134.0, 3695.0, 1.92e5       # [VÉR, valeurs usuelles, non vérifiées en ligne]
e_fusion = rho_W * (cp_W * (Tf_W - 300.0) + Lf_W)
Q_ref = charges["réf. : 1 singularité, 400 MW au total (dépôt γ + e±)"]
res["absorbeur_tungstene"] = dict(rayon_m=r_abs, volume_m3=V_abs, masse_kg=rho_W * V_abs,
                                  densite_de_puissance_W_m3=Q_ref / V_abs,
                                  energie_volumique_de_fusion_J_m3=e_fusion,
                                  temps_avant_fusion_sans_refroidissement_s=e_fusion * V_abs / Q_ref)

# ------------------------------------------------------------------ blindage et doses
RHO_PB = 11350.0
MU_PB = {1: 7.102e-2, 2: 4.606e-2, 3: 4.234e-2, 4: 4.197e-2, 5: 4.272e-2, 6: 4.391e-2, 8: 4.675e-2,
         10: 4.972e-2, 15: 5.658e-2, 20: 6.206e-2, 30: 7.022e-2, 50: 8.056e-2, 100: 9.310e-2}   # cm2/g, NIST
MUEN_EAU = {1: 3.103e-2, 2: 2.608e-2, 5: 1.915e-2, 10: 1.566e-2, 15: 1.441e-2, 20: 1.382e-2}   # cm2/g, NIST
MU_EAU_20 = 1.813e-2
lam_pb = {E: 1.0 / (mu * RHO_PB / 1000.0 * 100.0) for E, mu in MU_PB.items()}   # m
res["plomb_longueur_attenuation_cm"] = {f"{E} MeV": v * 100 for E, v in lam_pb.items()}
res["plomb_TVL_faisceau_etroit_cm"] = {f"{E} MeV": v * 100 * np.log(10) for E, v in lam_pb.items()}
TVL_PB = 0.057       # m, NCRP 151 (faisceau large, 4-20 MV)
TVL_BETON = 0.45     # m, NCRP 151 (18 MV)
res["TVL_NCRP151_m"] = dict(plomb=TVL_PB, beton=TVL_BETON)
res["eau_longueur_attenuation_20MeV_m"] = 1.0 / (MU_EAU_20 * 1.0 * 100.0)

MUEN = MUEN_EAU[20] * 0.1          # m2/kg (valeur à 20 MeV, borne haute du tableau NIST)
S_COL_E = 2.0                      # MeV cm2/g : pouvoir d'arrêt collisionnel des e± de 10-50 MeV dans l'eau [HYP, ordre de grandeur]
SECTION_CORPS, MASSE_CORPS = 0.7, 70.0   # m2, kg [HYP]
DL50 = (2.5, 5.0)                  # Gy (CDC)
doses = []
for nom, P_tot in (("1 singularité, 400 MW au total", 400e6), ("2 singularités, 400 MW chacune", 800e6)):
    P_g, P_e = FR["photons"] * P_tot, FR["electrons_positrons"] * P_tot
    for d in (1.0, 3.0):
        psi_g = P_g / (4 * np.pi * d**2)
        D_g = psi_g * MUEN                                    # Gy/s (kerma ~ dose, photons primaires seuls)
        # e± : calorimétrie simple — toute l'énergie interceptée par le corps y est déposée
        D_e_calo = P_e * SECTION_CORPS / (4 * np.pi * d**2) / MASSE_CORPS
        D_tot_calo = (P_g + P_e) * SECTION_CORPS / (4 * np.pi * d**2) / MASSE_CORPS
        doses.append(dict(cas=nom, distance_m=d, P_photons_W=P_g, P_e_W=P_e,
                          fluence_energetique_photons_W_m2=psi_g,
                          debit_dose_photons_primaires_Gy_s=D_g,
                          debit_dose_e_calorimetrique_Gy_s=D_e_calo,
                          debit_dose_total_calorimetrique_Gy_s=D_tot_calo,
                          temps_pour_DL50_photons_seuls_s=(DL50[0] / D_g, DL50[1] / D_g),
                          dose_photons_6h_Gy=D_g * K.DUREE_TRAJET,
                          puissance_absorbee_par_un_corps_W=D_tot_calo * MASSE_CORPS))
with open(os.path.join(K.RES, "c05_doses.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(doses[0].keys()))
    w.writeheader()
    for li in doses:
        w.writerow({k_: (f"{v:.4g}" if isinstance(v, float) else v) for k_, v in li.items()})
res["doses_sans_blindage"] = doses

# blindage requis : ramener la dose photons sur 6 h à 1 mSv (public, annuel) ou 20 mSv (travailleur, annuel)
D_ref = doses[0]["debit_dose_photons_primaires_Gy_s"]        # 1 m, 1 singularité
blind = {}
for lib, lim in (("1 mSv sur le trajet (limite annuelle du public)", 1e-3),
                 ("20 mSv sur le trajet (limite annuelle moyenne des travailleurs)", 20e-3)):
    facteur = D_ref * K.DUREE_TRAJET / lim
    n_tvl = np.log10(facteur)
    ep = n_tvl * TVL_PB
    r_int = K.R_CARTER
    m_sphere = 4 / 3 * np.pi * ((r_int + ep) ** 3 - r_int**3) * RHO_PB
    # faisceau étroit (correction n° 35) : TVL = ln(10)/(mu rho) à l'énergie médiane (15 MeV) et au minimum
    # d'atténuation du plomb (4 MeV), qui gouverne la queue des gerbes
    etroit = {}
    for E_mev in (15, 4):
        tvl_e = lam_pb[E_mev] * np.log(10)
        ep_e = n_tvl * tvl_e
        etroit[f"{E_mev} MeV"] = dict(TVL_m=tvl_e, epaisseur_plomb_m=ep_e,
                                      masse_sphere_plomb_kg=4 / 3 * np.pi * ((r_int + ep_e) ** 3 - r_int**3) * RHO_PB)
    blind[lib] = dict(facteur_attenuation=facteur, nombre_de_TVL=n_tvl, epaisseur_plomb_m=ep,
                      masse_sphere_plomb_kg=m_sphere, epaisseur_beton_m=n_tvl * TVL_BETON,
                      faisceau_etroit=etroit)
res["blindage_requis_a_1m"] = blind
# blindage logeable : 13 cm de plomb au plus entre le carter (r = 5 cm) et la paroi (profondeur 0,36 m)
# Blindage logeable : épaisseur de plomb entre le logement (rayon R_CARTER) et la paroi.
#  - cas favorable : logement centré dans la profondeur du coffre ;
#  - cas réel de DOC-007 : deux logements décalés de ± entraxe/2 dans la profondeur -> face la plus proche ;
#  - verticalement : demi-hauteur du corps.
ep_dispo = K.COFFRE_P / 2 - K.R_CARTER
res["blindage_logeable_par_direction"] = {}
for _lib, _ep in (("profondeur, logement centré (cas favorable)", ep_dispo),
                  ("profondeur, vers la face la plus proche (DOC-007)", K.COFFRE_P / 2 - K.D_PAIRE / 2 - K.R_CARTER),
                  ("vertical, demi-hauteur du corps", K.COFFRE_H_CORPS / 2 - K.R_CARTER),
                  ("entre les deux logements (demi-intervalle)", (K.D_PAIRE - 2 * K.R_CARTER) / 2),
                  ("ancienne hypothèse H1 (0,36 m de profondeur, carter 5 cm)", K.COFFRE_H1[1] / 2 - 0.05)):
    res["blindage_logeable_par_direction"][_lib] = dict(
        epaisseur_plomb_m=_ep, attenuation=10 ** (_ep / TVL_PB),
        debit_dose_residuel_photons_1m_Gy_s=D_ref / 10 ** (_ep / TVL_PB))
res["blindage_logeable"] = dict(epaisseur_plomb_m=ep_dispo, attenuation=10 ** (ep_dispo / TVL_PB),
                                debit_dose_residuel_photons_1m_Gy_s=D_ref / 10 ** (ep_dispo / TVL_PB),
                                masse_sphere_plomb_kg=4 / 3 * np.pi * ((K.R_CARTER + ep_dispo) ** 3 - K.R_CARTER**3) * RHO_PB,
                                masse_unite_kg=K.MASSE_UNITE)

# ------------------------------------------------------------------ « cône d'évacuation »
cone = {}
for demi_angle in (10.0, 30.0, 45.0):
    frac = (1 - np.cos(np.radians(demi_angle))) / 2
    cone[f"demi-angle {demi_angle:.0f}°"] = dict(fraction_angle_solide=frac, fraction_absorbee_par_le_collimateur=1 - frac)
res["cone_collimation"] = cone
# dose dans l'axe du cône à grande distance (photons primaires, atténuation dans l'air)
LAMBDA_AIR = 1.0 / (0.9 * MU_EAU_20 * 0.1 * 1.205)     # m ; μ/ρ(air) ≈ 0,9 μ/ρ(eau) à 20 MeV [HYP]
res["longueur_attenuation_air_m"] = LAMBDA_AIR
res["dose_dans_le_cone"] = {f"{d:.0f} m": dict(debit_Gy_s=D_ref / d**2 * np.exp(-d / LAMBDA_AIR),
                                               debit_Gy_h=D_ref / d**2 * np.exp(-d / LAMBDA_AIR) * 3600)
                            for d in (10.0, 100.0, 1000.0)}
# guidage magnétique des e± : rayon de giration r = E/(e c B) (ultra-relativiste)
res["rayon_de_giration_e_m"] = {f"E = {E} MeV, B = {B} T": E * K.MeV / (K.e * K.c * B)
                                for E in (10.0, 40.0) for B in (1.0, 10.0, 20.0)}
# neutrinos : dose négligeable (section efficace ~1e-41 cm² par nucléon à ~10 MeV [HYP, ordre de grandeur])
psi_nu = FR["neutrinos"] * 400e6 / (4 * np.pi)
res["neutrinos"] = dict(puissance_W=FR["neutrinos"] * 400e6, fluence_energetique_1m_W_m2=psi_nu,
                        debit_dose_1m_Gy_s=psi_nu * 1e-45 * 6.022e26)

K.sauver_json("c05_refroidissement.json", res)

# ------------------------------------------------------------------ affichage
print("Fractions :", {k_: round(v, 4) for k_, v in FR.items()}, " déposée :", round(F_DEP, 4))
for nc, Q in charges.items():
    print(f"- {nc}: {Q/1e6:.0f} MW ; T_surface coffre = {res['T_surface_coffre_K'][nc]:.0f} K ; "
          f"densité {res['densite_volumique_coffre_MW_par_L'][nc]:.2f} MW/L")
for li in debits:
    if "réf. :" in li["charge"] or "haut" in li["charge"]:
        print(f"  {li['charge'][:28]:28s} | {li['fluide']:42s} {li['debit_kg_s']:9.1f} kg/s  {li['debit_m3_s']:.3g} m³/s  "
              f"v={li['vitesse_dans_tuyau_5cm_m_s']:.3g} m/s  pompe={li['puissance_pompe_W']/1e3:.4g} kW  "
              f"autonomie={li['autonomie_reservoirs_s']:.3g} s (borne haute {li['autonomie_reservoirs_borne_haute_s']:.3g} s)  6 h : {li['masse_pour_6h_circuit_ouvert_kg']:.3g} kg")
for li in rad:
    if "réf. :" in li["charge"]:
        print(f"  radiateur {li['T_radiateur_K']:.0f} K : {li['surface_m2']:.3g} m² ({li['surface_sur_coffre']:.3g} x coffre)")
print("Puissance d'un coffre à T revendiquée :", res["puissance_coffre_a_T_revendiquee_W"])
for k_, v in parois.items():
    if "réf. :" in k_:
        print(f"  flux pariétal {k_[-20:]} : {v['flux_W_m2']:.3e} W/m² = {v['rapport_au_record_CHF']:.1f} x CHF record "
              f"= {v['rapport_au_Soleil']:.0f} x Soleil")
print("Absorbeur W :", res["absorbeur_tungstene"])
print("Plomb, TVL faisceau étroit (cm) :", {k_: round(v, 2) for k_, v in res["plomb_TVL_faisceau_etroit_cm"].items()})
for li in doses:
    print(f"  {li['cas']} à {li['distance_m']} m : photons {li['debit_dose_photons_primaires_Gy_s']:.3e} Gy/s ; "
          f"total calorimétrique {li['debit_dose_total_calorimetrique_Gy_s']:.3e} Gy/s ; "
          f"DL50 en {li['temps_pour_DL50_photons_seuls_s'][0]*1e3:.2f}-{li['temps_pour_DL50_photons_seuls_s'][1]*1e3:.2f} ms ; "
          f"corps : {li['puissance_absorbee_par_un_corps_W']/1e6:.2f} MW")
print("Blindage requis :", blind)
print("Blindage logeable :", res["blindage_logeable"])
for _k, _v in res["blindage_logeable_par_direction"].items():
    print(f"   {_k:62s} e = {_v['epaisseur_plomb_m']*100:5.2f} cm  atténuation {_v['attenuation']:8.1f}  reste {_v['debit_dose_residuel_photons_1m_Gy_s']:7.1f} Gy/s")
print("Géométrie :", res["geometrie"])
print("Sensibilité H1 :", res["sensibilite_H1"])
print("Flux pariétal de référence :", res["flux_parietal_reference"])
print("Cône :", cone)
print("Dose dans le cône :", res["dose_dans_le_cone"], " λ_air =", LAMBDA_AIR)
print("Giration :", res["rayon_de_giration_e_m"])
print("Neutrinos :", res["neutrinos"])

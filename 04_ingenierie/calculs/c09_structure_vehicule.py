# -*- coding: utf-8 -*-
"""C204 — Équipe C. Sous-système 8 : contraintes mécaniques, thermiques et matériaux ; véhicule porteur et sol.
Inclut le tableau de contraintes croisées (aucune masse M ne satisfait toutes les affirmations).

Sorties : resultats/c09_structure.json, c09_contraintes_croisees.csv, c09_budget_masse.csv
"""
import csv
import os
import numpy as np
import c00_constantes as K

H = K.charger_json("c01_hawking.json")
A12 = H["synthese"]["alpha_M_1e12kg"]
TABLE = {round(np.log10(t["M_kg"]), 3): t for t in H["table_masses"]}
res = {}

# ------------------------------------------------------------------ unité de 227 kg dans un 4x4
CHARGE_UTILE = (700.0, 1500.0)       # kg, pick-up 4x4 des années 1980 [HYP — valeur constructeur non confirmée]
res["unite_227kg"] = dict(
    poids_N=K.MASSE_UNITE * K.g0, fraction_charge_utile=(K.MASSE_UNITE / CHARGE_UTILE[1], K.MASSE_UNITE / CHARGE_UTILE[0]),
    masse_volumique_moyenne_kg_m3=K.MASSE_UNITE / K.COFFRE_V,
    masse_volumique_sur_volume_utile_kg_m3=K.MASSE_UNITE / K.VOLUME_UTILE,
    masse_volumique_ancienne_hypothese_H1_kg_m3=K.MASSE_UNITE / (K.COFFRE_H1[0] * K.COFFRE_H1[1] * K.COFFRE_H1[2]),
    volume_enveloppe_L=K.COFFRE_V * 1e3, volume_utile_L=K.VOLUME_UTILE * 1e3,
    pression_au_plancher_Pa=K.MASSE_UNITE * K.g0 / (K.COFFRE_L * K.COFFRE_P),
    equivalent_passagers_de_75kg=K.MASSE_UNITE / 75.0)

# ------------------------------------------------------------------ pesanteur ressentie : masse nécessaire
def masse_pour(a, r):
    return a * r**2 / K.G


res["masse_pour_2g"] = {f"r = {r} m": masse_pour(2 * K.g0, r) for r in (0.5, 1.0, 2.0, 3.0, 3.7)}
res["masse_pour_1p5g"] = {f"r = {r} m": masse_pour(1.5 * K.g0, r) for r in (1.0, 3.0)}
# si « 2 g ressentis » = somme vectorielle de 1 g terrestre et d'une traction horizontale a : a = sqrt(3) g
res["masse_si_resultante_2g_a_1m"] = masse_pour(np.sqrt(3) * K.g0, 1.0)
# distance à laquelle les masses « 300-500 MW » donnent 2 g
res["distance_2g_m"] = {f"M = {M:.3g} kg": float(np.sqrt(K.G * M / (2 * K.g0)))
                        for M in (2.94e11, 8.44e11, 1.09e12, 3.92e12, 4.38e12, 5.06e12)}
# profil de pesanteur autour d'une masse donnant 2 g à 1 m
M2 = masse_pour(2 * K.g0, 1.0)
res["profil_autour_de_2g_a_1m"] = {f"r = {r} m": dict(g_en_g=K.G * M2 / r**2 / K.g0,
                                                      maree_par_metre_en_g=2 * K.G * M2 / r**3 / K.g0)
                                   for r in (0.1, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0)}
res["effort_sur_occupant_80kg_a_2g_N"] = 80 * 2 * K.g0

# ------------------------------------------------------------------ charge sur le véhicule et le sol
A_PNEUS = 4 * 0.03                   # m², empreinte de 4 pneus [HYP]
resist = {"sol meuble (portance ~0,2 MPa) [ordre de grandeur]": 0.2e6,
          "béton (compression ~40 MPa) [ordre de grandeur]": 40e6,
          "granite (compression ~200 MPa) [ordre de grandeur]": 200e6,
          "acier à haute résistance (~2 GPa) [ordre de grandeur]": 2e9,
          "diamant (compression ~100 GPa) [ordre de grandeur]": 100e9}
charge = []
for lib, M1 in (("2 x 100 kg", 100.0), ("2 x 1,47e11 kg (2 g à 1 m à elles deux)", M2 / 2),
                ("2 x 2,94e11 kg (2 g à 1 m chacune)", 2.94e11), ("2 x 4,38e12 kg (400 MW au total chacune)", 4.38e12)):
    F = 2 * M1 * K.g0
    p = F / A_PNEUS
    charge.append(dict(cas=lib, masse_totale_kg=2 * M1, poids_N=F,
                       rapport_a_la_charge_utile_max=2 * M1 / CHARGE_UTILE[1],
                       pression_sous_les_pneus_Pa=p,
                       **{f"p / {k_}": p / v for k_, v in resist.items()}))
res["charge_vehicule_et_sol"] = charge

# chute à travers la Terre (aucun appui possible) : demi-période d'oscillation, densité uniforme
R_T, M_T = 6.371e6, 5.972e24
T_osc = 2 * np.pi * np.sqrt(R_T**3 / (K.G * M_T))
v_centre = np.sqrt(K.G * M_T / R_T)
M = 4.38e12
rho_roche = 5500.0
# friction dynamique (ordre de grandeur) : F = 4 pi G² M² rho lnΛ / v²
F_fd = 4 * np.pi * K.G**2 * M**2 * rho_roche * 20.0 / v_centre**2
# accrétion : section géométrique avec focalisation (c/v)²
sigma = np.pi * (K.RS_PAR_KG * M) ** 2 * (K.c / v_centre) ** 2
mdot_acc = rho_roche * v_centre * sigma
mdot_hawk = A12 * K.K_HAWKING / M**2 / K.c**2
res["chute_dans_la_Terre"] = dict(
    traversee_aller_simple_min=T_osc / 2 / 60, vitesse_au_centre_m_s=v_centre,
    friction_dynamique_N=F_fd, poids_N=M * K.g0, rapport_friction_sur_poids=F_fd / (M * K.g0),
    accretion_kg_s=mdot_acc, perte_Hawking_kg_s=mdot_hawk, rapport_perte_sur_accretion=mdot_hawk / mdot_acc)

# ------------------------------------------------------------------ contraintes croisées
crois = []
for M in (1e2, 1e4, 1e6, 1e8, 1e10, 1e11, 2.94e11, 1e12, 4.4e12, 1e13, 1e15):
    t = TABLE[round(np.log10(M), 3)]
    g1 = K.G * M / K.g0
    crois.append(dict(
        M_kg=M, r_s_m=t["r_s_m"], kT_MeV=t["kT_MeV"], puissance_Hawking_W=t["P_W"],
        duree_de_vie_s=t["duree_de_vie_s"], g_a_1m_en_g=g1, poids_N=M * K.g0,
        C1_transportable_moins_de_227kg="oui" if 2 * M <= K.MASSE_UNITE else "NON",
        C2_puissance_300_500MW="oui" if 3e8 <= t["P_W"] <= 5e8 else ("≈" if 1e8 <= t["P_W"] <= 1.2e10 else "NON"),
        C3_2g_entre_1_et_3p7m="oui" if masse_pour(2 * K.g0, 1.0) <= M <= masse_pour(2 * K.g0, 3.7) else "NON",
        C4_survit_a_un_trajet_de_6h="oui" if t["duree_de_vie_s"] > K.DUREE_TRAJET else "NON",
        C5_rayons_X_kT_1_100keV="oui" if 1e-3 <= t["kT_MeV"] <= 0.1 else "NON",
        C6_plus_petite_qu_un_electron_r_s_inf_2p8fm="oui" if t["r_s_m"] < 2.82e-15 else "NON"))
with open(os.path.join(K.RES, "c09_contraintes_croisees.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(crois[0].keys()))
    w.writeheader()
    for li in crois:
        w.writerow({k_: (f"{v:.4g}" if isinstance(v, float) else v) for k_, v in li.items()})
res["contraintes_croisees"] = crois

# ------------------------------------------------------------------ budget de MASSE et de VOLUME (correction n° 30)
# Configuration « généreuse » : tous les périphériques de DOC-008 en technologie de 2026, dimensionnés sans
# contrainte de place (c'était la maquette de la version 1 du rapport, vérifiée alors en masse seulement).
# Volumes : fiches constructeur quand elles existent, sinon [HYP] d'ingénieur.
V_BLINDAGE = 2 * 4 / 3 * np.pi * (K.R_CARTER + 0.02) ** 3            # deux sphères carter + 2 cm de plomb
M_BLINDAGE = 2 * 4 / 3 * np.pi * ((K.R_CARTER + 0.02) ** 3 - K.R_CARTER**3) * 11350
budget = [  # (élément, masse kg, volume intérieur occupé en litres, source/hypothèse)
    ("coffre aluminium/acier + patins + charnières (parois : hors volume utile)", 30.0, 0.0, "[HYP]"),
    ("pack Li-ion 7,5 kWh", 50.0, 30.0, "150 Wh/kg ; 250 Wh/L [HYP]"),
    ("4 horloges CSAC + distribution", 0.5, 0.5, "35 g et 17 cm³ pièce (fiche)"),
    ("3 calculateurs durcis + voteur + bus", 6.0, 3.0, "[HYP]"),
    ("gravimètre relatif type CG-6", 5.5, 21.5 * 21.0 * 24.0 / 1e3, "fiche constructeur : 21,5 x 21 x 24 cm"),
    ("2 bobines supraconductrices HTS compactes + cryostats (pré-refroidies, sans compresseur)", 40.0, 30.0,
     "[HYP] 2 cryostats Ø 25 x 30 cm"),
    ("alimentations/régulateurs de champ (x2)", 10.0, 6.0, "[HYP]"),
    ("canon à électrons + alimentation HT + collecteur sous vide", 8.0, 6.0, "[HYP]"),
    ("boucle de refroidissement (pompe, 2 réservoirs de 15 L pleins, échangeur)", 40.0, 36.0, "[HYP] borne haute"),
    ("télécommande filaire, panneau, câblage", 5.0, 3.0, "[HYP]"),
    (f"2 carters + blindage plomb local de 2 cm (rayon intérieur {K.R_CARTER*100:.2f} cm)", M_BLINDAGE,
     V_BLINDAGE * 1e3, "calcul"),
]
total = sum(b[1] for b in budget)
total_V = sum(b[2] for b in budget)
V_UTILE_L = K.VOLUME_UTILE * 1e3
V_ENV_L = K.COFFRE_V * 1e3
V_H1_L = K.COFFRE_H1[0] * K.COFFRE_H1[1] * K.COFFRE_H1[2] * 1e3

# Configuration « logeable » : palier R1 de l'Équipe I (lecture seule de sa nomenclature, repli sur ses chiffres publiés)
r1 = dict(masse_kg=36.0, volume_L=0.31 * V_UTILE_L, occupation=0.31, source="10_machine_optimisee/RAPPORT_I.md (repli)")
try:
    chemin_I = os.path.join(os.path.dirname(os.path.dirname(K.ICI)), "10_machine_optimisee", "nomenclature_R1.csv")
    m_r1 = v_r1 = 0.0
    with open(chemin_I, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            ident = row["id"]
            if ident.startswith("R1-B") or ident == "R1-22":          # modules externes et option amovible exclus
                continue
            m_r1 += float(row["masse_totale_kg"])
            dims = row["dimensions_unitaires_mm"].replace(",", ".").split("×")
            if len(dims) == 3 and ident not in ("R1-01", "R1-02"):     # coque et châssis : hors volume utile
                try:
                    a_, b_, c_ = (float(x) for x in dims)
                    v_r1 += a_ * b_ * c_ / 1e6 * float(row["quantite"])
                except ValueError:
                    pass
    r1 = dict(masse_kg=m_r1, volume_L=v_r1, occupation=v_r1 / V_UTILE_L,
              source="10_machine_optimisee/nomenclature_R1.csv (Équipe I), R1-01 à R1-21")
except Exception as exc:
    r1["erreur_lecture"] = str(exc)

# Lest nécessaire pour atteindre 227 kg avec le contenu logeable, et épaisseur de plomb équivalente autour des 2 logements
lest = K.MASSE_UNITE - r1["masse_kg"]
v_lest = lest / 11350.0
r_ext = (K.R_CARTER**3 + v_lest / (2 * 4 / 3 * np.pi)) ** (1 / 3)
verdict = dict(
    masse_configuration_genereuse_kg=total, masse_revendiquee_kg=K.MASSE_UNITE,
    masse_OK=bool(total <= K.MASSE_UNITE),
    volume_configuration_genereuse_L=total_V, volume_utile_L=V_UTILE_L, volume_enveloppe_L=V_ENV_L,
    volume_OK=bool(total_V <= V_UTILE_L),
    rapport_volume_sur_volume_utile=total_V / V_UTILE_L, rapport_volume_sur_enveloppe=total_V / V_ENV_L,
    volume_enveloppe_ancienne_hypothese_H1_L=V_H1_L, rapport_volume_sur_enveloppe_H1=total_V / V_H1_L,
    masse_volumique_de_la_configuration_genereuse_kg_m3=total / (total_V / 1e3),
    masse_volumique_requise_dans_le_volume_utile_kg_m3=K.MASSE_UNITE / K.VOLUME_UTILE,
    masse_volumique_requise_dans_l_enveloppe_kg_m3=K.MASSE_UNITE / K.COFFRE_V,
    configuration_logeable=r1,
    masse_volumique_configuration_logeable_kg_m3=r1["masse_kg"] / K.COFFRE_V,
    lest_pour_atteindre_227kg=dict(masse_kg=lest, volume_de_plomb_L=v_lest * 1e3,
                                   volume_libre_restant_L=V_UTILE_L - r1["volume_L"],
                                   epaisseur_equivalente_autour_des_2_logements_m=r_ext - K.R_CARTER),
    conclusion=("masse compatible (%.0f kg <= 227 kg) mais volume incompatible : %.0f L à loger dans %.0f L utiles "
                "(x %.1f) ; seule une configuration réduite tient (Équipe I, R1 : %.0f kg, %.0f %% du volume utile)"
                % (total, total_V, V_UTILE_L, total_V / V_UTILE_L, r1["masse_kg"], 100 * r1["occupation"])))
with open(os.path.join(K.RES, "c09_budget_masse.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["element", "masse_kg", "volume_L", "source"])
    for b in budget:
        w.writerow([b[0], f"{b[1]:.1f}", f"{b[2]:.1f}", b[3]])
    w.writerow(["TOTAL configuration généreuse", f"{total:.1f}", f"{total_V:.1f}", ""])
    w.writerow(["disponible (masse revendiquée ; volume intérieur utile, Équipes E et I)", f"{K.MASSE_UNITE:.1f}",
                f"{V_UTILE_L:.1f}", ""])
    w.writerow(["marge (négative = ne tient pas)", f"{K.MASSE_UNITE - total:.1f}", f"{V_UTILE_L - total_V:.1f}", ""])
    w.writerow(["configuration logeable : palier R1 de l'Équipe I", f"{r1['masse_kg']:.1f}", f"{r1['volume_L']:.1f}",
                r1["source"]])
res["budget_masse"] = dict(elements=[dict(element=b[0], masse_kg=b[1], volume_L=b[2], source=b[3]) for b in budget],
                           total_kg=total, reste_kg=K.MASSE_UNITE - total, total_volume_L=total_V)
res["verdict_masse_volume"] = verdict

K.sauver_json("c09_structure.json", res)
print("Unité 227 kg :", res["unite_227kg"])
print("Masse pour 2 g :", {k_: f"{v:.3g}" for k_, v in res["masse_pour_2g"].items()})
print("Distance 2 g :", res["distance_2g_m"])
print("Profil :", res["profil_autour_de_2g_a_1m"])
for c in charge:
    print({k_: (f"{v:.3g}" if isinstance(v, float) else v) for k_, v in c.items()})
print("Chute :", {k_: f"{v:.3g}" for k_, v in res["chute_dans_la_Terre"].items()})
for c in crois:
    print(f"M={c['M_kg']:.2e}  P={c['puissance_Hawking_W']:.2e} W  τ={c['duree_de_vie_s']:.2e} s  g(1m)={c['g_a_1m_en_g']:.2e} g | "
          f"C1 {c['C1_transportable_moins_de_227kg']:3s} C2 {c['C2_puissance_300_500MW']:3s} C3 {c['C3_2g_entre_1_et_3p7m']:3s} "
          f"C4 {c['C4_survit_a_un_trajet_de_6h']:3s} C5 {c['C5_rayons_X_kT_1_100keV']:3s} C6 {c['C6_plus_petite_qu_un_electron_r_s_inf_2p8fm']}")
print(f"Budget : masse {total:.1f} kg (reste {K.MASSE_UNITE - total:.1f} kg) ; volume {total_V:.1f} L pour {V_UTILE_L:.0f} L utiles "
      f"({V_ENV_L:.0f} L d'enveloppe ; H1 : {V_H1_L:.0f} L)")
for k_, v in verdict.items():
    print("   ", k_, "=", v)

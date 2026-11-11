# -*- coding: utf-8 -*-
"""C204 — Équipe C. Sous-système 5 : alimentation par batteries (repère 12) et bilan énergétique global (Q3).

Sorties : resultats/c06_alimentation.json, et ../bilan_energetique.csv (livrable)
"""
import csv
import os
import numpy as np
import c00_constantes as K

H = K.charger_json("c01_hawking.json")
R = K.charger_json("c05_refroidissement.json")
A12 = H["synthese"]["alpha_M_1e12kg"]
A_MS = H["synthese"]["alpha_modele_standard_complet"]
T6H = K.DUREE_TRAJET
res = {}

# ------------------------------------------------------------------ batteries embarquables
batteries = {  # nom : (masse kg, Wh/kg, puissance spécifique soutenue W/kg [HYP], volume en litres [HYP])
    "plomb 12 V 60 Ah (dessin DOC-008 : 6 éléments)": (17.0, 720.0 / 17.0, 150.0, 9.0),
    "pack LiFePO4 logeable (Équipe I, palier R1 : 1,34 kWh)": (9.5, 1340.0 / 9.5, 300.0, 3.9),
    "plomb-acide, 50 kg à 30 Wh/kg": (50.0, 30.0, 150.0, 20.0),
    "pack Li-ion, 50 kg à 150 Wh/kg": (50.0, 150.0, 500.0, 30.0),
    "cellules Li-ion nues, 50 kg à 270 Wh/kg": (50.0, 270.0, 800.0, 20.0),
    "borne haute : toute l'unité (227 kg) en pack Li-ion à 180 Wh/kg": (K.MASSE_UNITE, 180.0, 500.0, 136.0),
    "borne chimique : 50 kg à 12 kWh/kg (hydrocarbure + air) [HYP]": (50.0, 12000.0, 1000.0, 65.0),
}
bat = {}
for nom, (m, wh, pw, vol) in batteries.items():
    bat[nom] = dict(masse_kg=m, energie_Wh=m * wh, energie_J=m * wh * 3600.0, puissance_soutenue_W=m * pw,
                    puissance_moyenne_sur_6h_W=m * wh / 6.0, volume_L=vol,
                    part_du_volume_utile=vol / (K.VOLUME_UTILE * 1e3),
                    logeable_dans_le_volume_utile=("oui" if vol <= 0.5 * K.VOLUME_UTILE * 1e3 else "non"))
res["batteries"] = bat
E_REF = bat["pack Li-ion, 50 kg à 150 Wh/kg"]["energie_J"]          # référence : 7,5 kWh = 27 MJ
P_REF = bat["pack Li-ion, 50 kg à 150 Wh/kg"]["puissance_soutenue_W"]

# ------------------------------------------------------------------ besoins (puissance W, énergie J sur 6 h)
M_A = 4.38e12                # scénario A : 400 MW au total
M_2G = 2 * K.g0 * 1.0 / K.G  # 2 g à 1 m (une seule masse)
pompe_ref = [d for d in R["debits"] if d["charge"].startswith("réf. x2") and d["fluide"].startswith("eau liquide")][0]
B_PENNING = 5.14e11
V_CHAMP = 1e-3               # m3 : volume de champ d'un piège de 1 litre [HYP]

postes = []


def poste(sous_systeme, libelle, P=None, E=None, source="batterie", statut="", note=""):
    if E is None and P is not None:
        E = P * T6H
    postes.append(dict(sous_systeme=sous_systeme, poste=libelle,
                       puissance_W=("" if P is None else f"{P:.3g}"),
                       energie_J=f"{E:.3g}", energie_kWh=f"{E / K.kWh:.3g}",
                       rapport_a_batterie_Li_ion_50kg_27MJ=f"{E / E_REF:.3g}",
                       ordres_de_grandeur_au_dessus_de_la_batterie=f"{np.log10(E / E_REF):+.1f}",
                       source_d_energie_revendiquee=source, statut=statut, remarque=note))


# -- auxiliaires réellement constructibles
poste("6-7 commande", "4 horloges miniatures CSAC (0,12 W chacune)", P=4 * 0.12, statut="compatible batterie",
      note="Microchip SA.45s")
poste("6-7 commande", "4 étalons à jet de césium type 5071A (50 W chacun)", P=200.0, statut="compatible batterie",
      note="120 kg et 0,12 m3 à eux quatre")
poste("6-7 commande", "3 calculateurs embarqués + bus + voteur (3 x 30 W) [HYP]", P=90.0, statut="compatible batterie")
poste("6 capteurs", "gravimètre relatif type CG-6 (5,2 W)", P=5.2, statut="compatible batterie")
poste("6 capteurs", "gravimètre absolu quantique type AQG-B (500 W)", P=500.0, statut="compatible batterie",
      note="< 140 kg : ne tient pas dans le budget de masse")
poste("2 injection", "canon à électrons 100 kV x 1 mA", P=100.0, statut="compatible batterie")
poste("7 commande", "télécommande, écrans, capteurs divers [HYP]", P=30.0, statut="compatible batterie")
aux_min = 4 * 0.12 + 90 + 5.2 + 100 + 30
aux_max = 200 + 90 + 500 + 100 + 30
poste("TOTAL auxiliaires", "électronique et instruments, hypothèse basse", P=aux_min, statut="compatible batterie")
poste("TOTAL auxiliaires", "électronique et instruments, hypothèse haute", P=aux_max, statut="compatible batterie",
      note="5,5 kWh sur 6 h : tient dans 50 kg de Li-ion")
# -- aimants
poste("1 confinement", "cryoréfrigérateur d'un aimant supraconducteur compact (~7 kW) [HYP]", P=7e3,
      statut="hors batterie sur 6 h", note="42 kWh sur 6 h")
poste("1 confinement", "aimant hybride 45 T (30-33 MW, valeur MagLab)", P=33e6, source="réseau électrique",
      statut="impossible sur batterie", note="pour 45 T seulement, soit 1e-10 du champ requis")
poste("1 confinement", "énergie magnétique d'un champ de 5,1e11 T dans 1 litre", P=None,
      E=B_PENNING**2 / (2 * K.mu0) * V_CHAMP, source="(non précisée)", statut="impossible",
      note="champ exigé par un piège de Penning pour un trou noir de charge extrémale")
# -- refroidissement
poste("4 refroidissement", "pompe de circulation, eau ΔT = 50 K, 353 MW thermiques", P=pompe_ref["puissance_pompe_W"],
      statut="impossible sur batterie", note=f"débit {pompe_ref['debit_kg_s']:.0f} kg/s")
poste("4 refroidissement", "chaleur à évacuer, 2 singularités de 400 MW (dépôt γ + e±)", P=2 * 400e6 * R["fraction_deposee"],
      source="singularités", statut="impossible dans 0,13 m3")
poste("4 rayonnement", "énergie rayonnée par 2 singularités de 400 MW pendant 6 h", P=800e6, source="singularités",
      statut="—", note=f"prélevée sur leur masse : {800e6 * T6H / K.c**2 * 1e3:.3g} g")
# -- création des singularités
# Correction n° 29 : pour « 2 g à 1 m », c'est la masse TOTALE des deux singularités qui vaut 2,94e11 kg
# (2 x 1,47e11 kg) ; l'ancienne ligne comptait 2,94e11 kg par singularité, soit 4 g à 1 m.
for lib, M in (("scénario A : 2 x 4,4e12 kg (400 MW au total chacune)", M_A),
               ("2 x 1,47e11 kg (2 g à 1 m à elles deux)", M_2G / 2),
               ("2 x 100 kg (compatible avec les 227 kg)", 100.0)):
    poste("0 fabrication", f"énergie de masse à fournir, {lib}", E=2 * M * K.c**2, source="accélérateur (« CERN »)",
          statut="impossible", note="rendement supposé de 100 %")
# -- puissance qu'il faudrait injecter dans un trou noir de 100 kg pour simplement compenser son évaporation
P_100 = A_MS * K.K_HAWKING / 100.0**2
poste("0 fabrication", "puissance d'évaporation d'un trou noir de 100 kg (à compenser en continu)", P=P_100,
      E=P_100 * 1.0, source="—", statut="impossible", note="énergie indiquée pour 1 s ; durée de vie réelle 4e-13 s")
# -- injection / rotation
poste("2 injection", "ajouter 1 % de masse à 4,4e12 kg", E=0.01 * M_A * K.c**2, source="batterie", statut="impossible")
poste("2 injection", "charger 4,4e12 kg jusqu'à l'extrémal (≈ ½ M c²)", E=0.5 * M_A * K.c**2, source="batterie",
      statut="impossible", note="et la charge ne tient pas (décharge en ~1e-19 s)")
poste("3 rotation", "mettre 4,4e12 kg en rotation maximale (≈ 0,19 à 0,29 M c²)", E=M_A * K.c**2 / (3 * np.sqrt(3)),
      source="(non précisée)", statut="impossible")
# -- Q4
poste("9 Q4", "énergie électromagnétique donnant 2 g à 1 m par son seul contenu en énergie", E=M_2G * K.c**2,
      source="—", statut="impossible", note="équivaut à 2,94e11 kg")
# -- équivalents cinématiques du « 10 ans par heure » (indicatifs)
gam = 10 * K.an / 3600.0
poste("déplacement", "énergie cinétique d'un véhicule de 2500 kg à γ = 87 660 (dilatation équivalente, vers le futur seulement)",
      E=(gam - 1) * 2500.0 * K.c**2, source="—", statut="théoriquement défini, hors de portée",
      note="aucune énergie n'est définie pour un trajet vers le passé")

with open(os.path.join(os.path.dirname(K.ICI), "bilan_energetique.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(postes[0].keys()))
    w.writeheader()
    w.writerows(postes)
res["postes"] = postes

# ------------------------------------------------------------------ repères de comparaison
E_creation_A = 2 * M_A * K.c**2
comparaisons = {
    "production mondiale d'électricité 2023 (29 925 TWh)": 29925 * K.TWh,
    "consommation mondiale d'énergie primaire 2023 (620 EJ)": 620 * K.EJ,
    "énergie rayonnée par le Soleil en 1 s": K.Lsol,
    "énergie de masse de l'unité entière (227 kg)": K.MASSE_UNITE * K.c**2,
    "énergie magnétique d'ITER (51 GJ)": 51e9,
    "un faisceau du LHC (362 MJ)": 362e6,
    "pack Li-ion 50 kg (27 MJ)": E_REF,
}
res["comparaisons_J"] = comparaisons
res["creation_scenario_A_J"] = E_creation_A
res["creation_A_en_unites"] = {k_: E_creation_A / v for k_, v in comparaisons.items()}
res["creation_2x100kg_en_unites"] = {k_: 2 * 100 * K.c**2 / v for k_, v in comparaisons.items()}
res["creation_2g_J"] = M_2G * K.c**2          # 2 x (M_2G/2) c^2 : identique à l'énergie de la question Q4
res["creation_2g_en_unites"] = {k_: M_2G * K.c**2 / v for k_, v in comparaisons.items()}
res["energie_de_masse_227kg_Gt_TNT"] = K.MASSE_UNITE * K.c**2 / K.Mt_TNT / 1e3
res["facteur_gamma_10_ans_par_heure"] = gam
res["auxiliaires_W"] = dict(min=aux_min, max=aux_max, energie_6h_kWh_min=aux_min * T6H / K.kWh,
                            energie_6h_kWh_max=aux_max * T6H / K.kWh)
# configuration réduite, sans canon à électrons ni gravimètre quantique : CSAC + 3 calculateurs + CG-6 + pupitre
aux_reduit = 4 * 0.12 + 90 + 5.2 + 30
res["auxiliaires_configuration_logeable"] = dict(
    puissance_W=aux_reduit, energie_6h_kWh=aux_reduit * T6H / K.kWh, pack_logeable_kWh=1.34,
    marge=1.34 / (aux_reduit * T6H / K.kWh))

# ------------------------------------------------------------------ peut-on « faire grossir » un petit trou noir ?
# Bilan accrétion / évaporation : P_in = S * sigma_geo (flux d'énergie S), P_out = alpha K / M^2
# -> M_min^4 = alpha hbar c^10 / (27 pi G^4 S)
def M_min_alimentation(S, alpha):
    return (alpha * K.hbar * K.c**10 / (27 * np.pi * K.G**4 * S)) ** 0.25


rho_nuc = 2.3e17                 # kg/m3, densité nucléaire
S_nuc = rho_nuc * K.c**3         # flux d'énergie de matière nucléaire arrivant à c (borne très haute)
S_laser = 1e27                   # W/m2 = 1e23 W/cm2, ordre des intensités laser record [non vérifié en ligne]
res["croissance"] = dict(
    flux_matiere_nucleaire_W_m2=S_nuc, M_min_matiere_nucleaire_kg=M_min_alimentation(S_nuc, A12),
    flux_laser_W_m2=S_laser, M_min_laser_kg=M_min_alimentation(S_laser, H["synthese"]["alpha_sans_masse"]),
    flux_requis_pour_100kg_W_m2=P_100 / (27 * np.pi * K.G**2 * 100.0**2 / K.c**4),
    masse_de_Planck_kg=float(np.sqrt(K.hbar * K.c / K.G)),
    energie_de_Planck_GeV=float(np.sqrt(K.hbar * K.c**5 / K.G) / K.GeV),
    energie_collision_LHC_GeV=13600.0)
res["croissance"]["rapport_Planck_sur_LHC"] = res["croissance"]["energie_de_Planck_GeV"] / 13600.0
# temps disponible pour concentrer l'énergie d'un trou noir de 1e11 kg : r_s/c
M_seuil = res["croissance"]["M_min_matiere_nucleaire_kg"]
res["croissance"]["temps_de_formation_r_s_sur_c_s"] = K.RS_PAR_KG * M_seuil / K.c
res["croissance"]["puissance_de_formation_W"] = M_seuil * K.c**2 / (K.RS_PAR_KG * M_seuil / K.c)

K.sauver_json("c06_alimentation.json", res)

for nom, b in bat.items():
    print(f"{nom:62s} {b['energie_Wh']/1e3:8.2f} kWh = {b['energie_J']/1e6:8.1f} MJ ; P soutenue {b['puissance_soutenue_W']/1e3:.1f} kW ; "
          f"{b['volume_L']:.0f} L ({b['part_du_volume_utile']*100:.0f} % du volume utile)")
print("Auxiliaires, configuration logeable :", res["auxiliaires_configuration_logeable"])
print(f"Création « 2 g à 1 m » (masse totale 2,94e11 kg) : {res['creation_2g_J']:.3e} J")
print("Auxiliaires :", res["auxiliaires_W"])
for p in postes:
    print(f"[{p['sous_systeme']:17s}] {p['poste'][:78]:78s} P={p['puissance_W']:>9s} W  E={p['energie_J']:>9s} J  "
          f"({p['ordres_de_grandeur_au_dessus_de_la_batterie']} décades / batterie)")
print("Création scénario A :", f"{E_creation_A:.3e} J ;", {k_: f"{v:.3g}" for k_, v in res["creation_A_en_unites"].items()})
print("Création 2 x 100 kg :", {k_: f"{v:.3g}" for k_, v in res["creation_2x100kg_en_unites"].items()})
print("Création 2 g :", {k_: f"{v:.3g}" for k_, v in res["creation_2g_en_unites"].items()})
print("227 kg =", res["energie_de_masse_227kg_Gt_TNT"], "Gt TNT")
print("Croissance :", {k_: f"{v:.3g}" for k_, v in res["croissance"].items()})

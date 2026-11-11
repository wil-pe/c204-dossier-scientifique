# -*- coding: utf-8 -*-
"""C204 — Équipe C. Sous-système 6 : capteurs de gravité « VGL » (repère 11) et 4 horloges au césium.

Sorties : resultats/c07_capteurs_horloges.json, c07_signaux_gravimetriques.csv, c07_instruments.csv
"""
import csv
import os
import numpy as np
import c00_constantes as K

res = {}
ALPHA_M12 = K.charger_json("c01_hawking.json")["synthese"]["alpha_M_1e12kg"]

# ------------------------------------------------------------------ instruments réels (voir REFERENCES.md)
instruments = [
    # nom, type, bruit µGal/√Hz (ou None), exactitude/répétabilité µGal, masse kg, puissance W, T min, T max °C
    ("Micro-g LaCoste FG5-X", "absolu, chute libre + interférométrie laser", 15.0, 2.0, 150.0, 500.0, 20, 30),
    ("Exail AQG-B", "absolu, interférométrie atomique", 50.0, 2.0, 140.0, 500.0, 0, 40),
    ("GWR iGrav", "relatif, supraconducteur", 0.3, 0.001, None, None, 4, 38),
    ("Scintrex CG-6", "relatif, ressort de quartz", None, 5.0, 5.5, 5.2, -40, 45),
    ("MEMS (Middlemiss et al. 2016)", "relatif, MEMS (laboratoire)", 40.0, None, None, None, None, None),
]
with open(os.path.join(K.RES, "c07_instruments.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["instrument", "principe", "bruit_uGal_par_racine_Hz", "exactitude_ou_ecart_type_uGal", "masse_kg",
                "puissance_W", "T_min_C", "T_max_C", "fonctionne_a_38_49_C"])
    for it in instruments:
        ok = "" if it[7] is None else ("oui" if it[7] >= 49 else ("partiel" if it[7] >= 38 else "non"))
        w.writerow(list(it) + [ok])
res["instruments"] = [dict(nom=i[0], principe=i[1], bruit_uGal_rtHz=i[2], exactitude_uGal=i[3], masse_kg=i[4],
                           puissance_W=i[5], T_min_C=i[6], T_max_C=i[7]) for i in instruments]

# ------------------------------------------------------------------ signaux gravimétriques d'objets proches
objets = [("masse d'une tonne", 1000.0, 2.0), ("masse d'une tonne", 1000.0, 3.0),
          ("bloc de béton de 1 m³ (2400 kg)", 2400.0, 2.0), ("bloc de béton de 1 m³ (2400 kg)", 2400.0, 3.5),
          ("mur de 10 t", 1e4, 3.0), ("personne (80 kg)", 80.0, 1.0), ("voiture (1500 kg)", 1500.0, 3.0),
          ("immeuble (1e6 kg)", 1e6, 20.0), ("fluide de refroidissement interne (10 kg déplacés de 0,5 à 0,3 m)", 10.0, None)]
BRUITS = {"FG5-X": 15.0, "AQG": 50.0, "iGrav": 0.3, "MEMS": 40.0}
sig = []
for nom, m, d in objets:
    if d is None:
        dg = K.G * m * (1 / 0.3**2 - 1 / 0.5**2)
        grad = float("nan")
    else:
        dg = K.G * m / d**2
        grad = 2 * K.G * m / d**3
    li = dict(objet=nom, masse_kg=m, distance_m=(d if d else float("nan")), delta_g_uGal=dg / K.uGal,
              gradient_Eotvos=grad / K.Eotvos)
    for inst, n in BRUITS.items():
        li[f"temps_integration_SNR3_{inst}_s"] = (3 * n / (dg / K.uGal)) ** 2
    # correction n° 33 : comparaison explicite à l'écart-type d'une lecture du CG-6 (5 µGal)
    li["rapport_a_l_ecart_type_CG6_5uGal"] = (dg / K.uGal) / 5.0
    li["lectures_CG6_a_moyenner_pour_SNR3"] = (3 * 5.0 / (dg / K.uGal)) ** 2
    sig.append(li)
with open(os.path.join(K.RES, "c07_signaux_gravimetriques.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(sig[0].keys()))
    w.writeheader()
    for li in sig:
        w.writerow({k_: (f"{v:.4g}" if isinstance(v, float) else v) for k_, v in li.items()})
res["signaux"] = sig
res["effets_parasites"] = {
    "gradient vertical à l'air libre (µGal/m) [valeur normale, non vérifiée en ligne]": 308.6,
    "variation de hauteur donnant 1 µGal (mm)": 1.0 / 308.6 * 1000,
    "marée terrestre, amplitude typique (µGal) [ordre de grandeur, non vérifié en ligne]": 150.0,
}

# ------------------------------------------------------------------ le capteur dans le champ des singularités
cas = {}
for lib, M in (("2,94e11 kg (2 g à 1 m)", 2.94e11), ("4,4e12 kg (400 MW au total)", 4.38e12)):
    for r in (0.3, 0.5):
        g_s = K.G * M / r**2
        cas[f"{lib}, capteur à {r} m"] = dict(
            g_singularite_m_s2=g_s, g_en_g=g_s / K.g0, gradient_s2=2 * K.G * M / r**3,
            gradient_Eotvos=2 * K.G * M / r**3 / K.Eotvos,
            resolution_relative_pour_1uGal=K.uGal / g_s,
            stabilite_de_position_requise_m=r * K.uGal / (2 * g_s),
            dilatation_aluminium_par_K_m=23e-6 * r,
            rapport_dilatation_1K_sur_tolerance=23e-6 * r / (r * K.uGal / (2 * g_s)),
            stabilite_relative_de_masse_requise=K.uGal / g_s,
            variation_relative_de_masse_Hawking_par_s=ALPHA_M12 * K.K_HAWKING / M**2 / (M * K.c**2))
res["capteur_dans_le_champ"] = cas
res["plage_CG6_mGal"] = 8000.0
res["un_g_en_mGal"] = K.g0 / 1e-5
res["rapport_1g_sur_plage_CG6"] = (K.g0 / 1e-5) / 8000.0

# ------------------------------------------------------------------ référence de position ?
res["degres_de_liberte_mesurables_en_un_point"] = dict(vecteur_g=3, tenseur_gradient_independants=5, total=8)
v_orb, v_gal = 29.78e3, 230e3      # m/s [ordres de grandeur usuels, non vérifiés en ligne]
T60 = 60 * K.an
res["deplacement_de_la_Terre_en_60_ans_m"] = dict(orbital_cumule=v_orb * T60, galactique=v_gal * T60)
# sensibilité spatiale : un écart de 1 µGal correspond à quel déplacement ?
res["sensibilite_spatiale"] = {
    "vertical : 1 µGal ↔ (mm)": 1e3 / 308.6,
    "horizontal, gradient régional typique 1 µGal/m [HYP] : 1 µGal ↔ (m)": 1.0}

# ------------------------------------------------------------------ horloges
horloges = {
    "Microchip 5071A (jet de césium, option hautes performances)": dict(
        exactitude=5e-13, palier=1e-14, masse_kg=30.0, volume_m3=0.1334 * 0.4255 * 0.5239, puissance_W=50.0,
        T_min_C=0, T_max_C=50, annee=1992),
    "Microchip CSAC SA.45s (vapeur de césium, CPT)": dict(
        exactitude=None, stabilite_1s=3e-10, vieillissement_par_mois=9e-10, masse_kg=0.035, volume_m3=17e-6,
        puissance_W=0.12, T_min_C=-10, T_max_C=70, annee=2011),
    "NIST-F2 (fontaine à césium, laboratoire)": dict(exactitude=1.1e-16, annee=2014),
    "horloge optique Al+ (laboratoire, Brewer et al. 2019)": dict(exactitude=9.4e-19, annee=2019),
}
res["horloges"] = horloges
h5071 = horloges["Microchip 5071A (jet de césium, option hautes performances)"]
res["quatre_5071A"] = dict(masse_kg=4 * h5071["masse_kg"], volume_m3=4 * h5071["volume_m3"],
                           fraction_de_la_masse_unite=4 * h5071["masse_kg"] / K.MASSE_UNITE,
                           fraction_du_volume_coffre=4 * h5071["volume_m3"] / K.COFFRE_V,
                           fraction_du_volume_utile=4 * h5071["volume_m3"] / K.VOLUME_UTILE,
                           fraction_du_volume_ancienne_hypothese_H1=4 * h5071["volume_m3"]
                           / (K.COFFRE_H1[0] * K.COFFRE_H1[1] * K.COFFRE_H1[2]),
                           un_seul_etalon_sur_volume_utile=h5071["volume_m3"] / K.VOLUME_UTILE,
                           longueur_etalon_sur_profondeur_coffre=0.4255 / K.COFFRE_P, puissance_W=200.0)
res["gravimetre_CG6_volume"] = dict(volume_L=21.5 * 21.0 * 24.0 / 1e3,
                                    part_du_volume_utile=21.5 * 21.0 * 24.0 / 1e3 / (K.VOLUME_UTILE * 1e3),
                                    hauteur_m=0.24, hauteur_interieure_disponible_m_equipe_I=(0.228, 0.269))
res["quatre_CSAC"] = dict(masse_kg=4 * 0.035, volume_m3=4 * 17e-6, puissance_W=0.48)

# décalage gravitationnel de fréquence dans le champ des singularités : Δf/f = -GM/(r c²)
dec = {}
for lib, M in (("2,94e11 kg", 2.94e11), ("4,4e12 kg", 4.38e12)):
    for r in (0.1, 0.3, 0.5, 1.0):
        dec[f"{lib}, r = {r} m"] = K.G * M / (r * K.c**2)
    dec[f"{lib}, écart entre 0,3 m et 0,5 m"] = K.G * M * (1 / 0.3 - 1 / 0.5) / K.c**2
res["decalage_gravitationnel_relatif"] = dec
res["decalage_terrestre_par_metre"] = K.g0 / K.c**2
res["rapport_decalage_max_sur_exactitude_5071A"] = dec["4,4e12 kg, r = 0.1 m"] / 5e-13
# potentiel qu'exigerait le facteur revendiqué de 10 ans/heure si c'était une dilatation gravitationnelle
gam = 10 * K.an / 3600.0
res["facteur_10_ans_par_heure"] = gam
res["potentiel_requis_sur_c2_pour_ce_facteur"] = 0.5 * (1 - 1 / gam**2)
res["potentiel_disponible_sur_c2_2g_sur_1m"] = 2 * K.g0 * 1.0 / K.c**2
# datation : erreur d'une horloge sur 6 h de temps propre et sur 60 ans
res["erreur_temps"] = {
    "5071A sur 6 h (5e-13)": 5e-13 * K.DUREE_TRAJET, "CSAC sur 6 h (dérive ~1e-9) [HYP]": 1e-9 * K.DUREE_TRAJET,
    "quartz ordinaire sur 6 h (1e-6) [HYP]": 1e-6 * K.DUREE_TRAJET,
    "précision relative pour viser un jour donné à 60 ans": 86400.0 / (60 * K.an)}

K.sauver_json("c07_capteurs_horloges.json", res)

for li in sig:
    print(f"{li['objet'][:60]:60s} d={li['distance_m']:.3g} m  Δg={li['delta_g_uGal']:.3g} µGal  grad={li['gradient_Eotvos']:.3g} E  "
          f"t(FG5-X)={li['temps_integration_SNR3_FG5-X_s']:.3g} s  t(AQG)={li['temps_integration_SNR3_AQG_s']:.3g} s  "
          f"t(iGrav)={li['temps_integration_SNR3_iGrav_s']:.3g} s")
for k_, v in cas.items():
    print(k_, {a: f"{b:.3g}" for a, b in v.items()})
print("1 g / plage CG-6 :", res["rapport_1g_sur_plage_CG6"])
print("4 x 5071A :", res["quatre_5071A"], " 4 x CSAC :", res["quatre_CSAC"])
print("CG-6 :", res["gravimetre_CG6_volume"])
for li in sig:
    print(f"   {li['objet'][:40]:40s} d={li['distance_m']:.3g} m : {li['delta_g_uGal']:.3g} µGal = "
          f"{li['rapport_a_l_ecart_type_CG6_5uGal']:.2f} x écart-type CG-6 ; {li['lectures_CG6_a_moyenner_pour_SNR3']:.3g} lectures pour S/B = 3")
print("Décalages :", {k_: f"{v:.3g}" for k_, v in dec.items()})
print("Décalage terrestre par mètre :", res["decalage_terrestre_par_metre"])
print("Potentiel requis/c² :", res["potentiel_requis_sur_c2_pour_ce_facteur"], " disponible :",
      res["potentiel_disponible_sur_c2_2g_sur_1m"])
print("Erreurs de temps :", res["erreur_temps"])
print("Déplacement Terre 60 ans :", res["deplacement_de_la_Terre_en_60_ans_m"])

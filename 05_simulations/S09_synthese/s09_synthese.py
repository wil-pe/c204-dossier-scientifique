# -*- coding: utf-8 -*-
"""S09 — Synthèse : tableau machine-lisible de tous les ordres de grandeur, analyse de sensibilité
et Monte-Carlo sur les paramètres incertains ; écriture de 05_simulations/resultats_globaux.json.

SIMULATION ILLUSTRATIVE : le Monte-Carlo propage des hypothèses de LECTURE des revendications
(quelle puissance ? mesurée où ? quelle « taille d'électron » ?), pas des incertitudes de mesure :
il n'existe aucune mesure. Les distributions sont des choix [HYP] explicites de l'Équipe D. Ce
n'est pas une preuve expérimentale.

Dépend des résultats de S01 à S08 (lancer run_all.sh, ou chaque script, au préalable).
Exécution :  .venv/bin/python 05_simulations/S09_synthese/s09_synthese.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import c204_commun as cc  # noqa: E402
from c204_commun import plt  # noqa: E402

cc.configurer_matplotlib()
FIG, RES = cc.dossiers(__file__)
val = cc.Validation("S09_synthese")
col = cc.COULEURS
BASE = Path(__file__).resolve().parents[1]
G, C, G0 = cc.G, cc.C, cc.G0
REV = cc.REVENDICATIONS

# ---------------------------------------------------------------------------
# 1. Lecture des résultats des simulations S01 à S08
# ---------------------------------------------------------------------------
FICHIERS = {
    "S01": "S01_hawking/resultats/S01_resultats.json", "S02": "S02_kerr_geometrie/resultats/S02_resultats.json",
    "S03": "S03_geodesiques_kerr/resultats/S03_resultats.json", "S04": "S04_cylindre_tipler/resultats/S04_resultats.json",
    "S05": "S05_champ_faible_c204/resultats/S05_resultats.json", "S06": "S06_confinement_em/resultats/S06_resultats.json",
    "S07": "S07_energie_negative/resultats/S07_resultats.json", "S08": "S08_reconstitution_doc009/resultats/S08_resultats.json",
}
R = {}
for cle, chemin in FICHIERS.items():
    f = BASE / chemin
    if not f.exists():
        raise SystemExit(f"Résultats manquants : {f}\nLancer d'abord 05_simulations/run_all.sh (ou le script {cle}).")
    R[cle] = cc.lire_json(f)
table_M = np.genfromtxt(BASE / "S01_hawking/resultats/S01_table_M.csv", delimiter=",", names=True)

# Interpolations log-log tirées de S01 (toutes espèces) : P_totale(M) et τ(M), strictement monotones
lM, lP, lT = np.log10(table_M["M_kg"]), np.log10(table_M["P_totale_W"]), np.log10(table_M["tau_especes_s"])
val.verifier_vrai("Table S01 : P_totale(M) strictement décroissante et τ(M) strictement croissante", bool(np.all(np.diff(lP) < 0) and np.all(np.diff(lT) > 0)))


def masse_pour_puissance_totale(P):
    return 10**np.interp(np.log10(P), lP[::-1], lM[::-1])


def masse_pour_duree(t):
    return 10**np.interp(np.log10(t), lT, lM)


K_CN = R["S01"]["coefficients"]["P_fois_M2_corps_noir_W_kg2"]
K_PAGE = R["S01"]["coefficients"]["P_fois_M2_photons_page_W_kg2"]
# recoupement interpolation ↔ inversion exacte de S01
val.verifier("Interpolation de M(P = 300 MW, toutes espèces) ↔ inversion exacte de S01", masse_pour_puissance_totale(300e6),
             R["S01"]["masse_pour_300_500_MW_kg"]["total_especes"][1], tol_rel=5e-3)
val.verifier("Interpolation de M(τ = 30 ans) ↔ inversion exacte de S01", masse_pour_duree(30 * cc.ANNEE),
             R["S01"]["masse_min_pour_duree_kg"]["trente ans de service"], tol_rel=5e-3)

# ---------------------------------------------------------------------------
# 2. Tableau machine-lisible des ordres de grandeur
# ---------------------------------------------------------------------------
M_DEMI = REV["masse_unite_kg"] / 2
TAUX = REV["taux_temporel"]


def ligne(ident, grandeur, valeur, unite, formule, hypotheses, source, etiquette, statut, confiance, revendication=None):
    d = {"id": ident, "grandeur": grandeur, "valeur": valeur, "unite": unite, "formule": formule, "hypotheses": hypotheses,
         "source": source, "etiquette": etiquette, "statut_physique": statut, "confiance": confiance}
    if revendication is not None:
        d["revendication_comparee"] = revendication
    return d


s1, s2, s3, s4, s5, s6, s7, s8 = (R[k] for k in ("S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08"))
h5 = s5["tableau_par_hypothese"]
hA, hC, hD = h5["A : 113 kg (demi-unité de 227 kg)"], h5["C : 1,5e11 kg (2 g à 1 m pour la paire)"], h5["D : 1e12 kg (300–500 MW, photons)"]
TABLEAU = [
    # --- S01
    ligne("S01-01", "Rayon de Schwarzschild par unité de masse", s1["coefficients"]["r_s_par_kg_m"], "m/kg", "r_s = 2GM/c²", "Schwarzschild", "S01", "[VÉR]", "Démontré (RG)", "élevé"),
    ligne("S01-02", "Température de Hawking × masse", s1["coefficients"]["T_fois_M_K_kg"], "K·kg", "T = ħc³/(8πGMk_B)", "semi-classique, M ≫ M_Planck", "S01", "[VÉR]", "Théoriquement possible (non observé)", "élevé"),
    ligne("S01-03", "Puissance × M², photons, corps noir", K_CN, "W·kg²", "P = ħc⁶/(15360πG²M²)", "surface 4πr_s², photons seuls", "S01", "[DÉD]", "Théoriquement possible", "élevé"),
    ligne("S01-04", "Puissance × M², photons, corps gris", K_PAGE, "W·kg²", "P = 3,366e-5 ħc⁶/(G²M²)", "Page 1976", "S01", "[VÉR]", "Théoriquement possible", "élevé"),
    ligne("S01-05", "Masse donnant 300–500 MW (photons, corps noir)", s1["masse_pour_300_500_MW_kg"]["corps_noir"], "kg", "inversion de S01-03", "—", "S01", "[DÉD]", "Théoriquement possible", "élevé", "300–500 MW"),
    ligne("S01-06", "Masse donnant 300–500 MW (toutes espèces)", s1["masse_pour_300_500_MW_kg"]["total_especes"], "kg", "P = α f(M) c²/M²", "f(M) de MacGibbon 1991 (+ W, Z, H [HYP])", "S01", "[DÉD]", "Théoriquement possible", "moyen", "300–500 MW"),
    ligne("S01-07", "Masse donnant 1,5–2 g entre 1 et 3 m", s1["masse_pour_1p5_2g_entre_1_et_3m_kg"], "kg", "M = a r²/G", "masse ponctuelle unique", "S01", "[DÉD]", "Démontré (Newton)", "élevé", "1,5–2 g"),
    ligne("S01-08", "Durée de vie d'un trou noir de 113 kg (toutes espèces)", s1["reperes"]["demi-unité (113 kg)"]["duree_vie_especes_s"], "s", "τ = ∫M²dM/(αf)", "semi-classique", "S01", "[DÉD]", "Théoriquement possible", "moyen", "unité de 227 kg"),
    ligne("S01-09", "Puissance d'un trou noir de 113 kg (toutes espèces)", s1["reperes"]["demi-unité (113 kg)"]["P_totale_especes_W"], "W", "P = α f c²/M²", "semi-classique", "S01", "[DÉD]", "Théoriquement possible", "moyen", "300–500 MW"),
    ligne("S01-10", "Masse minimale pour vivre 6 h / 1 an / 30 ans", list(s1["masse_min_pour_duree_kg"].values()), "kg", "τ(M) = durée", "durées de mission [HYP]", "S01", "[DÉD]", "Théoriquement possible", "moyen"),
    ligne("S01-11", "Masse d'un trou noir de rayon = rayon classique de l'électron", s1["masse_pour_taille_electron_kg"]["rayon classique de l'électron (2,82 fm)"], "kg", "M = r c²/(2G)", "« taille d'un électron » = 2,82 fm [HYP]", "S01", "[DÉD]", "Démontré (RG)", "élevé", "« plus petites qu'un électron »"),
    ligne("S01-12", "Écart entre la masse de l'unité et la masse requise", s1["ecart_decades_C1_vs_C2"], "ordres de grandeur", "log10(M_P / 113 kg)", "—", "S01", "[DÉD]", "Contredit les connaissances actuelles (si l'on maintient les deux revendications)", "élevé", "227 kg vs 300–500 MW"),
    ligne("S01-13", "Température d'équilibre d'une paroi noire à 1 m de 300–500 MW", s1["temperature_equilibre_corps_noir_a_1m_K"], "K", "T = (P/(4πr²σ))^(1/4)", "absorption totale, équilibre radiatif", "S01", "[DÉD]", "Démontré", "moyen", "« 100 à 120 °F »"),
    # --- S02
    ligne("S02-01", "Rayon gravitationnel pour 1e12 kg", s2["echelles_metres"][11]["r_g_m"], "m", "r_g = GM/c²", "—", "S02", "[VÉR]", "Démontré (RG)", "élevé"),
    ligne("S02-02", "Étendue radiale de la région à CTC (Kerr a = 0,9 M), 1e12 kg", s2["echelles_metres"][11]["etendue_region_ctc_a0p9_m"], "m", "racine de r³ + a²r + 2Ma² = 0", "extension r < 0 de Kerr éternel", "S02", "[DÉD]", "Spéculatif (derrière un horizon de Cauchy instable)", "élevé (calcul) / faible (réalité physique)"),
    ligne("S02-03", "Masse pour laquelle r_g = 1 m", s2["masse_pour_r_g_1m_kg"], "kg", "M = c²/G", "—", "S02", "[VÉR]", "Démontré (RG)", "élevé"),
    ligne("S02-04", "Moment cinétique maximal d'un trou noir de 1e12 kg", s2["echelles_metres"][11]["J_max_kg_m2_s"], "kg·m²/s", "J = GM²/c", "Kerr extrémal", "S02", "[VÉR]", "Démontré (RG)", "élevé"),
    # --- S03
    ligne("S03-01", "Énergie minimale par unité de masse pour traverser le disque sur l'axe (a = 0,9 M)", s3["seuil_energie_traversee_axe"], "c² (sans dimension)", "E² > 1 + M/a", "géodésique axiale, Kerr éternel", "S03", "[DÉD]", "Spéculatif", "élevé (calcul)"),
    ligne("S03-02", "Temps propre de chute équatoriale 10 M → anneau, pour 1e12 kg", s3["chute_equatoriale"]["tau_anneau_secondes_pour_1e12_kg"], "s", "14,9 GM/c³", "E = 1, L_z = 0,5 M", "S03", "[DÉD]", "Théoriquement possible", "élevé (calcul)"),
    ligne("S03-03", "dt/dτ maximal sur orbite circulaire stable (a = 0,998 M)", s3["dilatation_temporelle"]["ut_ISCO_a_0p998"], "sans dimension", "u^t à l'ISCO", "Kerr", "S03", "[VÉR]", "Démontré (RG)", "élevé", "dt/dτ ≈ 87 660"),
    ligne("S03-04", "Altitude au-dessus de l'horizon pour dt/dτ = 87 660 (statique, 1e12 kg)", s3["dilatation_temporelle"]["altitude_au_dessus_horizon_pour_M_1e12kg_m"], "m", "1 − r_s/r = 1/87 660²", "Schwarzschild, observateur statique", "S03", "[DÉD]", "Théoriquement possible (irréalisable)", "élevé", "dt/dτ ≈ 87 660"),
    # --- S04
    ligne("S04-01", "Masse linéique minimale d'un cylindre de Tipler à CTC", s4["seuil_ctc"]["masse_lineique_seuil_kg_m"], "kg/m", "μ = c²/(8G) (aR = 1/2)", "cylindre de poussière INFINI en rotation rigide", "S04", "[DÉD]", "Spéculatif (solution non asymptotiquement plate)", "élevé (calcul)", "« sinusoïde de Tipler »"),
    ligne("S04-02", "Rapport entre cette masse linéique et 227 kg/m", s4["cylindre_227_kg_par_metre"]["rapport_de_masse_requis"], "sans dimension", "c²/(8G) / 227", "—", "S04", "[DÉD]", "—", "élevé", "unité de 227 kg"),
    ligne("S04-03", "Densité axiale d'un cylindre de rayon 0,1 m au seuil aR = 0,6", s4["exemples_SI"]["échelle C204 (R = 0,1 m, L = 1 m, aR = 0,6)"]["densite_axe_kg_m3"], "kg/m³", "ρ₀ = (aRc/R)²/(2πG)", "van Stockum", "S04", "[DÉD]", "Contredit les connaissances actuelles (10¹⁰ fois la densité nucléaire)", "élevé"),
    # --- S05
    ligne("S05-01", "Pesanteur à 1 m de deux masses de 113 kg", hA["g_a_1.0m_en_g0"], "g₀", "g = 2GM/r²", "champ faible", "S05", "[DÉD]", "Démontré (Newton)", "élevé", "1,5–2 g"),
    ligne("S05-02", "dt/dτ − 1 à 1 m de deux masses de 1e12 kg", hD["dilatation_dt_dtau_moins_1_a_1.0m"], "sans dimension", "−Φ/c²", "champ faible", "S05", "[DÉD]", "Démontré (RG, champ faible)", "élevé", "dt/dτ ≈ 87 660"),
    ligne("S05-03", "dt/dτ − 1 à 1 m de deux masses de 113 kg", hA["dilatation_dt_dtau_moins_1_a_1.0m"], "sans dimension", "−Φ/c²", "champ faible", "S05", "[DÉD]", "Démontré (RG, champ faible)", "élevé", "dt/dτ ≈ 87 660"),
    ligne("S05-04", "Marée sur 1 m à 1 m du centre (masses donnant 2 g à 1 m)", hC["maree_sur_1.0m_centre_1.0m_en_g0"], "g₀", "|g(r − ½) − g(r + ½)|", "occupant d'étendue radiale 1 m [HYP]", "S05", "[DÉD]", "Démontré (Newton)", "élevé", "« 1,5 à 2 g pendant tout le trajet »"),
    ligne("S05-05", "Entraînement des référentiels à 1 m (2 × 1e12 kg, d = 0,3 m, orbite képlérienne)", hD["d=0.3m"]["omega_LT_pole_1m_orbital_rad_s"], "rad/s", "Ω_LT = 2GJ/(c²r³)", "gravito-électromagnétisme linéarisé", "S05", "[DÉD]", "Démontré (Gravity Probe B, LAGEOS pour la Terre)", "élevé"),
    ligne("S05-06", "Puissance en ondes gravitationnelles (2 × 1e12 kg, d = 0,3 m)", hD["d=0.3m"]["P_OG_W"], "W", "P = (32/5)G⁴M⁵·2/(c⁵d⁵)", "quadrupôle, orbite circulaire képlérienne", "S05", "[DÉD]", "Démontré (pulsars binaires, LIGO)", "élevé"),
    ligne("S05-07", "Temps de coalescence (2 × 1e12 kg, d = 0,3 m [HYP])", hD["d=0.3m"]["temps_coalescence_ans"], "ans", "t = (5/256)c⁵d⁴/(2G³M³)", "Peters 1964", "S05", "[DÉD]", "Démontré", "élevé"),
    ligne("S05-08", "Idem à l'entraxe documentaire d = 0,098 m (DOC-007, Équipe A) : temps de coalescence ; pulsation orbitale ; entraînement à 1 m",
          [hD["d=0.098m"]["temps_coalescence_ans"], hD["d=0.098m"]["Omega_kepler_rad_s"], hD["d=0.098m"]["omega_LT_pole_1m_orbital_rad_s"]], "ans ; rad/s ; rad/s",
          "Peters ; Ω² = 2GM/d³ ; Ω_LT = 2GJ/(c²r³)", "entraxe 98 ± 25 mm [DÉD Équipe A]", "S05", "[DÉD]", "Démontré", "élevé"),
    # --- S06
    ligne("S06-01", "Rapport charge/masse extrémal", s6["Q_sur_M"]["extremal_C_kg"], "C/kg", "Q/M = sqrt(4πε₀G)", "Kerr-Newman", "S06", "[VÉR]", "Démontré (RG)", "élevé"),
    ligne("S06-02", "Champ électrique de lévitation (charge extrémale)", s6["champ_levitation_charge_extremale_V_m"], "V/m", "E = g₀/(Q/M)", "pesanteur terrestre", "S06", "[DÉD]", "Contredit les connaissances actuelles (≫ champs de claquage)", "élevé", "« logements magnétiques »"),
    ligne("S06-03", "Champ magnétique minimal d'un piège de Penning (charge extrémale, d₀ = 5 cm)", s6["penning_extremal_d0_5cm_affaissement_10pct"]["B_min_T"], "T", "B = sqrt(2g/(f d₀))/(Q/M)", "affaissement ≤ 10 %", "S06", "[DÉD]", "Contredit les connaissances actuelles (> champ d'un magnétar)", "élevé", "« singularity magnetic field coil »"),
    ligne("S06-04", "Charge d'un micro-trou noir : valeur typique (quadratique moyenne) ; borne supérieure d'ordre de grandeur", [s6["charge_typique_en_e"], s6["charge_critique_schwinger_en_e"]], "e",
          "≈ 6,14 e (Page 1977) ; ≲ e/α", "GMμ/ħc ≪ 1 ; r_s ≪ longueur de Compton de l'électron", "S06", "[VÉR] (typique, résumé vérifié par la Red Team) / [DÉD] (borne)",
          "Théoriquement possible", "moyen", "« chargées électriquement »"),
    ligne("S06-05", "Poids d'une singularité de 1e12 kg transmis au véhicule", s6["reaction_sur_le_vehicule"]["poids_1e12_kg_N"], "N", "F = M g₀", "troisième loi de Newton", "S06", "[DÉD]", "Démontré", "élevé", "camion de 1987"),
    # --- S07
    ligne("S07-01", "Masse exotique d'un trou de ver de Morris-Thorne à gorge de 1 m", s7["morris_thorne"]["masse_exotique_kg"], "kg", "M = −b₀c²/(2G)", "Φ = 0, asymptotiquement plat", "S07", "[DÉD]", "Spéculatif", "élevé (calcul)"),
    ligne("S07-02", "Tension à la gorge (b₀ = 1 m)", s7["morris_thorne"]["tension_a_la_gorge_Pa"], "Pa", "τ = c⁴/(8πG b₀²)", "—", "S07", "[DÉD]", "Spéculatif", "élevé (calcul)"),
    ligne("S07-03", "Énergie négative d'une bulle d'Alcubierre (R = 3 m, paroi 0,25 m, v = c)", s7["alcubierre"]["energie_J"], "J", "E = −(c²v²/12G)∫r²f'²dr", "observateurs eulériens", "S07", "[DÉD]", "Spéculatif", "élevé (calcul)"),
    ligne("S07-04", "Densité d'énergie Casimir à 100 nm", s7["casimir"]["100 nm (réalisable)"]["densite_J_m3"], "J/m³", "u = −π²ħc/(720d⁴)", "plaques idéales, T = 0", "S07", "[VÉR]", "Démontré", "élevé"),
    ligne("S07-05", "Rapport énergie requise (Morris-Thorne 1 m) / Casimir disponible dans 1 m de rayon", s7["comparaison"]["rapport_MT_sur_casimir_sphere_1m"], "sans dimension", "—", "cavités de 100 nm, remplissage 50 % [HYP]", "S07", "[DÉD]", "—", "moyen"),
    # --- S08
    ligne("S08-01", "Rapport d'axes du sphéroïde central de DOC-009", s8["courbes_fermees_vs_familles_physiques"]["sphéroïde central (enveloppe)"]["rapport_d_axes_mesure"], "sans dimension", "a/b (ellipse ajustée)", "numérisation ±1 px", "S08", "[DÉD]", "— (dessin)", "moyen"),
    ligne("S08-02", "Rapport d'axes du grand contour E1 (enveloppe des anneaux) de DOC-009", s8["courbes_fermees_vs_familles_physiques"]["grande ellipse extérieure"]["rapport_d_axes_mesure"], "sans dimension", "a/b (ellipse ajustée)", "numérisation ±1 px", "S08", "[DÉD]", "— (dessin)", "moyen"),
    ligne("S08-03", "Erreur de prédiction des pôles : ellipse / ergosurface de Kerr", [s8["test_des_poles_spheroide_central"]["erreur_de_prediction_px"]["ellipse générique"], s8["test_des_poles_spheroide_central"]["erreur_de_prediction_px"]["ergosurface de Kerr, axe de rotation vertical"]], "px", "distance pôles dessinés ↔ courbe ajustée sur les arcs", "zone déclarée « not to scale » par le document : résultat descriptif, sans valeur de preuve", "S08", "[DÉD]", "— (dessin)", "faible (comme test physique)", "« singularities in Kerr field »"),
    ligne("S08-04", "Décalage du centre des anneaux par rapport aux masses", s8["proportions_relatives"]["decalage_masses_vs_centre_des_anneaux_sur_A"], "demi-grand axe A", "(X_centre − X_masses)/A", "—", "S08", "[DOC] (lecture) / [DÉD]", "— (dessin)", "moyen", "« mass offset »"),
    ligne("S08-05", "Échelle du dessin d'après les quatre cotes en mètres de la variante DOC-014 ; dispersion", [s8["cotes_doc014"]["echelle_moyenne_px_ref_par_m"], s8["cotes_doc014"]["dispersion_relative_des_echelles"]], "px de référence par mètre ; sans dimension",
          "longueur dessinée / valeur inscrite (cotes 6, 7, 8, 9)", "DOC-014 seulement ; attribution à l'auteur non établie", "S08", "[DOC] (valeurs) / [DÉD] (échelle)", "— (dessin)", "moyen", "6, 5, 8 et 11 mètres"),
    ligne("S08-06", "Demi-envergures des trois paires d'anneaux à l'échelle de DOC-014", list(s8["cotes_doc014"]["comparaison_au_texte"]["demi_envergures_dessinees_m"].values()), "m",
          "demi-envergure dessinée / échelle", "échelle moyenne des quatre cotes", "S08", "[DÉD]", "— (dessin)", "moyen", "« champ efficace 10–12 ft » (3,0–3,7 m)"),
]

# ---------------------------------------------------------------------------
# 3. Monte-Carlo sur les lectures possibles des revendications
# ---------------------------------------------------------------------------
N = 200_000
rng = np.random.default_rng(204)
P = rng.uniform(*REV["puissance_W"], N)                       # « 300–500 MW »
puissance_totale = rng.random(N) < 0.5                        # True : puissance pour les deux singularités ensemble
modele = rng.integers(0, 3, N)                                # 0 corps noir (photons), 1 Page (photons), 2 toutes espèces
g = rng.uniform(*REV["pesanteur_g"], N) * G0                  # « 1,5 à 2 g »
r = rng.uniform(*REV["distance_m"], N)                        # distance d'évaluation, 1 à 3 m
paire = rng.random(N) < 0.5                                   # True : les deux masses contribuent à g
M_unite = np.clip(rng.normal(REV["masse_unite_kg"], 0.05 * REV["masse_unite_kg"], N), 150, 300)
fraction = rng.uniform(0.01, 1.0, N)                          # part de la masse de l'unité contenue dans les singularités
def_taille = rng.integers(0, 3, N)                            # 0 rayon classique, 1 Compton réduite, 2 borne expérimentale
duree = 10**rng.uniform(np.log10(cc.HEURE), np.log10(30 * cc.ANNEE), N)
frac_charge = 10**rng.uniform(-6, 0, N)                       # Q/Q_extrémal

P_par = np.where(puissance_totale, P / 2, P)                  # puissance par singularité
M_P = np.where(modele == 0, np.sqrt(K_CN / P_par), np.where(modele == 1, np.sqrt(K_PAGE / P_par), masse_pour_puissance_totale(P_par)))
M_g = g * r**2 / G / np.where(paire, 2, 1)                    # masse de chaque singularité donnant g à la distance r
M_C1 = fraction * M_unite / 2
tailles = np.array([cc.R_ELECTRON_CLASSIQUE, cc.LAMBDA_COMPTON_E_REDUITE, cc.R_ELECTRON_BORNE_EXP])[def_taille]
M_taille_max = tailles * C**2 / (2 * G)
M_duree_min = masse_pour_duree(duree)

delta = np.log10(M_P / M_g)                                   # accord puissance ↔ pesanteur
ecart_C1_P = np.log10(M_P / M_C1)
ecart_C1_g = np.log10(M_g / M_C1)
dil = np.where(paire, 2, 1) * G * M_g / (r * C**2)            # dt/dτ − 1 à la distance r (avec la masse « pesanteur »)
ecart_dil = np.log10(REV["taux_temporel"] / dil)
E_lev = G0 / (frac_charge * s6["Q_sur_M"]["extremal_C_kg"])

coherences = {}
for k in (1.5, 2.0, 3.0):
    accord = np.abs(delta) < np.log10(k)
    M_c = np.sqrt(M_P * M_g)
    complet = accord & (M_c > M_duree_min) & (M_c < M_taille_max)
    coherences[f"facteur_{k}"] = {
        "P_et_g_compatibles": float(accord.mean()),
        "P_g_duree_et_taille_compatibles": float(complet.mean()),
        "P_g_duree_taille_ET_masse_unite_compatibles": float((complet & (M_c <= M_C1 * k)).mean()),
    }
par_modele = {nom: {"mediane_log10_M_P": float(np.median(np.log10(M_P[modele == i]))), "mediane_delta": float(np.median(delta[modele == i])),
                    "fraction_accord_facteur_2": float((np.abs(delta[modele == i]) < np.log10(2)).mean())}
              for i, nom in enumerate(("photons_corps_noir", "photons_page", "toutes_especes"))}

# Sensibilité : corrélations de rang de Spearman (entrées continues) et écarts de médianes (entrées catégorielles)
entrees = {"puissance revendiquée P": P, "pesanteur revendiquée g": g, "distance d'évaluation r": r}
sens_delta = {k: float(spearmanr(v, delta).statistic) for k, v in entrees.items()}
sens_cat = {
    "modèle d'émission (toutes espèces − corps noir)": float(np.median(delta[modele == 2]) - np.median(delta[modele == 0])),
    "modèle d'émission (Page − corps noir)": float(np.median(delta[modele == 1]) - np.median(delta[modele == 0])),
    "puissance totale plutôt que par singularité": float(np.median(delta[puissance_totale]) - np.median(delta[~puissance_totale])),
    "g produit par la paire plutôt que par une masse": float(np.median(delta[paire]) - np.median(delta[~paire])),
}
# effet en décades de chaque entrée continue (de son 5ᵉ à son 95ᵉ centile), tout le reste étant échantillonné
effets = {}
for k, v in entrees.items():
    bas, haut = np.quantile(v, [0.05, 0.95])
    effets[k] = float(np.median(delta[v >= haut]) - np.median(delta[v <= bas]))
effets.update(sens_cat)

mc = {
    "n_tirages": N, "graine": 204,
    "distributions_HYP": {
        "P": "uniforme 300–500 MW", "interpretation_P": "par singularité / totale (50/50)", "modele_emission": "corps noir, Page, toutes espèces (1/3 chacun)",
        "g": "uniforme 1,5–2 g₀", "r": "uniforme 1–3 m", "g_produit_par": "une masse / la paire (50/50)", "masse_unite": "normale 227 kg ± 5 %",
        "fraction_masse_dans_singularites": "uniforme 0,01–1", "taille_electron": "rayon classique / Compton réduite / borne 1e-18 m (1/3 chacun)",
        "duree_mission": "log-uniforme 1 h – 30 ans", "Q_sur_Q_extremal": "log-uniforme 1e-6 – 1"},
    "log10_M_P": {"p05": float(np.quantile(np.log10(M_P), 0.05)), "mediane": float(np.median(np.log10(M_P))), "p95": float(np.quantile(np.log10(M_P), 0.95))},
    "log10_M_g": {"p05": float(np.quantile(np.log10(M_g), 0.05)), "mediane": float(np.median(np.log10(M_g))), "p95": float(np.quantile(np.log10(M_g), 0.95))},
    "delta_log10_M_P_sur_M_g": {"p05": float(np.quantile(delta, 0.05)), "mediane": float(np.median(delta)), "p95": float(np.quantile(delta, 0.95))},
    "par_modele_d_emission": par_modele,
    "coherence_interne": coherences,
    "ecart_masse_unite_vs_puissance_decades": {"min": float(ecart_C1_P.min()), "mediane": float(np.median(ecart_C1_P)), "max": float(ecart_C1_P.max())},
    "ecart_masse_unite_vs_pesanteur_decades": {"min": float(ecart_C1_g.min()), "mediane": float(np.median(ecart_C1_g)), "max": float(ecart_C1_g.max())},
    "ecart_dilatation_decades": {"min": float(ecart_dil.min()), "mediane": float(np.median(ecart_dil)), "max": float(ecart_dil.max())},
    "champ_levitation_V_m": {"min": float(E_lev.min()), "mediane": float(np.median(E_lev)), "fraction_sous_1e9_V_m": float((E_lev < 1e9).mean())},
    "sensibilite_spearman_sur_delta": sens_delta,
    "effets_en_decades_sur_delta": effets,
}
val.verifier("Monte-Carlo : aucun tirage ne concilie la masse de l'unité avec la puissance ET la pesanteur (fraction)", coherences["facteur_3.0"]["P_g_duree_taille_ET_masse_unite_compatibles"], 0.0, tol_abs=0.0)
val.verifier_vrai("Monte-Carlo : l'écart masse de l'unité ↔ masse requise dépasse 8 ordres de grandeur dans TOUS les tirages", min(ecart_C1_P.min(), ecart_C1_g.min()) > 8.0,
                  f"minimum = {min(ecart_C1_P.min(), ecart_C1_g.min()):.2f} décades")
# convergence statistique : deux moitiés indépendantes donnent la même fraction (à l'erreur binomiale près)
f1, f2 = (np.abs(delta[: N // 2]) < np.log10(2)).mean(), (np.abs(delta[N // 2:]) < np.log10(2)).mean()
val.verifier("Monte-Carlo : convergence (fraction d'accord P↔g, moitié 1 ↔ moitié 2)", f1, f2, tol_abs=4 * np.sqrt(0.25 / (N / 2)))
# recoupement analytique : médiane de log10 M_g attendue pour r ~ U(1,3), g ~ U(1,5;2), paire 50/50 (calcul direct par quadrature)
rr_, gg_ = np.meshgrid(np.linspace(1, 3, 801), np.linspace(1.5, 2.0, 201))
ref = np.concatenate([np.log10(gg_ * G0 * rr_**2 / G).ravel(), np.log10(gg_ * G0 * rr_**2 / (2 * G)).ravel()])
val.verifier("Monte-Carlo : médiane de log10 M_g ↔ calcul direct sur grille", float(np.median(np.log10(M_g))), float(np.median(ref)), tol_abs=0.01)

# ---------------------------------------------------------------------------
# 4. Échelle des écarts (synthèse)
# ---------------------------------------------------------------------------
ECARTS = [
    ("Masse : requise pour 300–500 MW (photons) / disponible (113 kg)", s1["ecart_decades_C1_vs_C2"], "S01"),
    ("Masse : requise pour 2 g à 1 m / disponible (2 × 113 kg)", s5["comparaison_revendications"]["ecart_decades_pesanteur_M_113kg"], "S05"),
    ("Durée de vie : 6 h requises / trou noir de 113 kg", float(np.log10(6 * cc.HEURE / s1["reperes"]["demi-unité (113 kg)"]["duree_vie_especes_s"])), "S01"),
    ("Puissance : trou noir de 113 kg / 500 MW revendiqués", float(np.log10(s1["reperes"]["demi-unité (113 kg)"]["P_totale_especes_W"] / 500e6)), "S01"),
    ("Dilatation : 87 660 revendiqué / obtenu à 1 m (2 × 10¹² kg)", s5["comparaison_revendications"]["ecart_decades_M_1e12kg"], "S05"),
    ("Dilatation : 87 660 revendiqué / obtenu à 1 m (2 × 113 kg)", s5["comparaison_revendications"]["ecart_decades_M_113kg"], "S05"),
    ("Champ B d'un piège de Penning (charge extrémale) / 45 T", float(np.log10(s6["penning_extremal_d0_5cm_affaissement_10pct"]["B_min_T"] / 45.0)), "S06"),
    ("Champ E de lévitation (charge extrémale) / 10⁹ V/m", float(np.log10(s6["champ_levitation_charge_extremale_V_m"] / 1e9)), "S06"),
    ("Poids de 10¹² kg / charge utile d'un pick-up", float(np.log10(s6["reaction_sur_le_vehicule"]["rapport_au_poids_supportable_par_un_pick_up"])), "S06"),
    ("Cylindre de Tipler : masse linéique requise / 227 kg par mètre", float(np.log10(s4["cylindre_227_kg_par_metre"]["rapport_de_masse_requis"])), "S04"),
    ("Morris-Thorne (gorge 1 m) : énergie négative / Casimir disponible", float(np.log10(s7["comparaison"]["rapport_MT_sur_casimir_sphere_1m"])), "S07"),
    ("Alcubierre (R = 3 m, v = c) : énergie négative / Casimir disponible", float(np.log10(s7["comparaison"]["rapport_Alcubierre_sur_casimir_sphere_3m"])), "S07"),
    ("Région à CTC de Kerr (10¹² kg) : 1 m requis / étendue réelle", float(np.log10(1.0 / s2["echelles_metres"][11]["etendue_region_ctc_a0p9_m"])), "S02"),
]

# ---------------------------------------------------------------------------
# 5. Figures
# ---------------------------------------------------------------------------
# --- Figure 1 : distributions de masses -------------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.5, 5.8), gridspec_kw={"width_ratios": [1.5, 1]})
bins = np.linspace(-1, 13.5, 291)
ax1.hist(np.log10(M_C1), bins=bins, color=col["bleu"], alpha=0.85, label="C1 : masse d'une singularité compatible avec l'unité de 227 kg", density=True)
for i, (nom, c) in enumerate((("photons, corps noir", col["orange"]), ("photons, Page 1976", col["jaune"]), ("toutes espèces", col["rouge"]))):
    ax1.hist(np.log10(M_P[modele == i]), bins=bins, color=c, alpha=0.75, label=f"masse donnant 300–500 MW ({nom})", density=True)
ax1.hist(np.log10(M_g), bins=bins, color=col["vert"], alpha=0.6, label="masse donnant 1,5–2 g entre 1 et 3 m", density=True)
ax1.set_yscale("log")
ax1.set_ylim(1e-2, 60)
ax1.annotate("", xy=(np.log10(M_C1.max()), 0.03), xytext=(min(np.log10(M_P).min(), np.log10(M_g).min()), 0.03), arrowprops=dict(arrowstyle="<->", lw=1.6, color="k"))
ax1.text(6.5, 0.04, f"écart minimal sur {N:,} tirages :\n{min(ecart_C1_P.min(), ecart_C1_g.min()):.1f} ordres de grandeur".replace(",", " ").replace(".", ","), ha="center", fontsize=9.5, weight="bold")
ax1.set_xlabel("log₁₀(masse d'une singularité / kg)")
ax1.set_ylabel("densité de probabilité (échelle log.)")
ax1.set_title("(a) Monte-Carlo sur les lectures possibles des revendications", fontsize=10)
ax1.legend(fontsize=7.8, loc="upper center")
b2 = np.linspace(-1.2, 1.6, 141)
for i, (nom, c) in enumerate((("photons, corps noir", col["orange"]), ("photons, Page 1976", col["jaune"]), ("toutes espèces", col["rouge"]))):
    ax2.hist(delta[modele == i], bins=b2, color=c, alpha=0.7, label=f"{nom} : {100 * par_modele[list(par_modele)[i]]['fraction_accord_facteur_2']:.0f} % à un facteur 2".replace(".", ","))
ax2.axvspan(-np.log10(2), np.log10(2), color=col["gris"], alpha=0.2)
ax2.axvline(0, color="k", lw=1)
ax2.set_xlabel("Δ = log₁₀(M_puissance / M_pesanteur)")
ax2.set_ylabel("nombre de tirages")
ax2.set_title("(b) Cohérence interne puissance ↔ pesanteur (hors masse de l'unité)", fontsize=10)
ax2.legend(fontsize=8, loc="upper right")
cc.titre(fig, "S09 — Monte-Carlo : les masses exigées par « 300–500 MW » et « 1,5–2 g » comparées à la masse de l'unité")
cc.sauver_figure(fig, FIG / "S09_fig1_monte_carlo_masses.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 2 : sensibilité --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 5.6))
noms = list(effets.keys())
vals = [effets[k] for k in noms]
ordre = np.argsort(np.abs(vals))
ax.barh(range(len(noms)), np.array(vals)[ordre], color=[col["rouge"] if v > 0 else col["bleu"] for v in np.array(vals)[ordre]])
ax.set_yticks(range(len(noms)))
ax.set_yticklabels(np.array(noms)[ordre], fontsize=9)
for i, v in enumerate(np.array(vals)[ordre]):
    ax.text(v + (0.02 if v >= 0 else -0.02), i, f"{v:+.2f}".replace(".", ","), va="center", ha="left" if v >= 0 else "right", fontsize=9)
ax.axvline(0, color="k", lw=1)
ax.set_xlim(-1.3, 1.1)
ax.set_ylim(-1.9, len(noms) - 0.4)
ax.set_xlabel("effet sur Δ = log₁₀(M_puissance / M_pesanteur)  [ordres de grandeur]\n(entrées continues : du 5ᵉ au 95ᵉ centile ; entrées catégorielles : différence de médianes)")
ax.grid(axis="y", visible=False)
ax.text(0.99, 0.03, f"Pour mémoire : l'écart avec la masse de l'unité est de {np.median(ecart_C1_P):.1f} ordres de grandeur (médiane) :\naucune de ces sensibilités (≤ 1 décade) ne peut le combler.".replace(".", ",", 1),
        transform=ax.transAxes, ha="right", fontsize=9, bbox=dict(fc="white", ec=col["gris"]))
cc.titre(fig, "S09 — Analyse de sensibilité : quels choix de lecture déplacent l'accord puissance ↔ pesanteur ?")
cc.sauver_figure(fig, FIG / "S09_fig2_sensibilite.png", rect=(0, 0.035, 1, 0.92))

# --- Figure 3 : échelle des écarts ---------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 7.2))
ECARTS_T = sorted(ECARTS, key=lambda e: e[1])
ax.barh(range(len(ECARTS_T)), [e[1] for e in ECARTS_T], color=[col["rouge"] if e[1] > 20 else (col["orange"] if e[1] > 6 else col["jaune"]) for e in ECARTS_T])
ax.set_yticks(range(len(ECARTS_T)))
ax.set_yticklabels([f"{e[0]}  [{e[2]}]" for e in ECARTS_T], fontsize=8.8)
for i, e in enumerate(ECARTS_T):
    ax.text(e[1] + 0.4, i, f"{e[1]:.1f} décades".replace(".", ","), va="center", fontsize=9)
ax.set_xlabel("écart entre ce qui est requis (ou revendiqué) et ce qui est disponible (ou calculé)  [ordres de grandeur]")
ax.set_xlim(0, 50)
ax.grid(axis="y", visible=False)
cc.titre(fig, "S09 — Échelle des écarts : synthèse des ordres de grandeur des simulations S01 à S07")
cc.sauver_figure(fig, FIG / "S09_fig3_echelle_des_ecarts.png", rect=(0, 0.035, 1, 0.92))

# ---------------------------------------------------------------------------
# 6. Sorties
# ---------------------------------------------------------------------------
CLES_BILAN = ("n_tests", "n_passes", "n_echecs", "n_hors_decompte")
validations = {k: {kk: v["validation"].get(kk, 0) for kk in CLES_BILAN} for k, v in R.items()}
validations["S09"] = {kk: val.bilan()[kk] for kk in CLES_BILAN}
hors_decompte = {k: v["validation"].get("hors_decompte", []) for k, v in R.items() if v["validation"].get("hors_decompte")}
par_categorie = {}
for _l in hors_decompte.values():
    for _e in _l:
        par_categorie[_e["categorie"]] = par_categorie.get(_e["categorie"], 0) + 1
DESACCORDS = [
    {"sujet": "Masse donnant 300–500 MW", "dossier_de_base": "0,84–1,1e12 kg (photons seuls, corps noir)",
     "equipe_D": f"{cc.sci(s1['masse_pour_300_500_MW_kg']['total_especes'][0], 2)} à {cc.sci(s1['masse_pour_300_500_MW_kg']['total_especes'][1], 2)} kg si l'on compte toutes les espèces émises ; "
                 "le chiffre du dossier est exact pour son hypothèse (photons, corps noir) mais sous-estime la masse d'un facteur ~4,6 pour une puissance TOTALE donnée",
     "consequence": "avec toutes les espèces, « 300–500 MW » et « 2 g entre 1 et 3 m » ne se recoupent plus (facteur ~1,5 à 20) : la cohérence interne notée au §6 du dossier dépend du modèle d'émission"},
    {"sujet": "Durée de vie", "dossier_de_base": "8,41e-17 s/kg³ × M³ (photons seuls) : 1e-10 s pour 100 kg, 3e12 ans pour 1e12 kg",
     "equipe_D": f"toutes espèces : {cc.sci(s1['reperes']['demi-unité (113 kg)']['duree_vie_especes_s'], 2)} s pour 113 kg (≈ 200 fois plus court) et "
                 f"{cc.sci(s1['reperes']['1e12 kg']['duree_vie_especes_s'] / cc.ANNEE, 2)} ans pour 1e12 kg (≈ 24 fois plus court)",
     "consequence": "ne change aucune conclusion"},
    {"sujet": "Rayonnement à 1e12 kg", "dossier_de_base": "« ~1e11 K, dizaines de MeV : gamma, e±, neutrinos »",
     "equipe_D": "confirmé : k_BT = 10,6 MeV ; photons ≈ 7 % seulement de la puissance totale (7,8 GW toutes espèces pour 1e12 kg)", "consequence": "renforce l'incohérence n° 4 du dossier (pas des rayons X)"},
    {"sujet": "Géométrie de DOC-009", "dossier_de_base": "« trois anneaux elliptiques emboîtés de taille croissante » de part et d'autre du centre",
     "equipe_D": "la numérisation montre des anneaux de taille DÉCROISSANTE en s'éloignant du centre (rayons 0,47 ; 0,34 ; 0,20 A), sections parallèles d'une même ellipse ; "
                 "l'ordre des repères 2-3-4 (negative, null, positive) va du plus grand (proche) au plus petit (lointain)",
     "consequence": "à corriger dans la description du dossier §3 (sans incidence sur la physique)"},
    {"sujet": "Cotes de DOC-009 (ajout de la phase 7)", "dossier_de_base": "« aucune dimension numérique sur le document » (§3)",
     "equipe_D": "vrai de DOC-009, faux de sa variante DOC-014 (attribution non établie), qui porte 6, 5, 8 et 11 mètres ; à l'échelle correspondante (dispersion 9 %) "
                 "les demi-envergures des anneaux valent 13 à 18 m, contre 3,0 à 3,7 m dans le texte",
     "consequence": "la première version de S08 affirmait à tort « ni cote ni échelle » ; corrigé (Red Team n° 37)"},
    {"sujet": "Autres coefficients du §6", "dossier_de_base": "r_s, T, P (corps noir), τ (corps noir), Q_max/M, M pour 2 g",
     "equipe_D": "tous re-dérivés et confirmés à mieux que 0,2 %", "consequence": "aucune"},
]
globaux = {
    "programme": "C204 — Équipe D (mathématiques et simulation numérique)",
    "avertissement": cc.MENTION,
    "date_de_generation": "voir l'horodatage du fichier",
    "validation_par_simulation": validations,
    "validation_totale": {"n_tests": sum(v["n_tests"] for v in validations.values()), "n_passes": sum(v["n_passes"] for v in validations.values()),
                          "n_echecs": sum(v["n_echecs"] for v in validations.values()),
                          "n_hors_decompte": sum(v["n_hors_decompte"] for v in validations.values()), "hors_decompte_par_categorie": par_categorie,
                          "definition": "un test de validation confronte le code à une réponse connue indépendamment et peut échouer ; les contrôles de l'ajustement sur lui-même, "
                                        "les énoncés de résultat, les repères non vérifiés et les biais de modèle documentés sont consignés hors décompte",
                          "rapprochement_avec_la_red_team": "181 « tests » annoncés en phase 5 ; correction n° 39 : 17 éléments de S08 sortis (164 + 17) ; n° 41 : repère Pfenning & Ford sorti ; "
                                                            "n° 42 : comparaison de M* (biais de modèle) sortie ; deux autres éléments de S08 sortis par le même critère (constat sur les anneaux = résultat ; "
                                                            "affinage des ancres = borné par construction) ; deux contrôles nouveaux ajoutés en phase 7 (second contour E2, méthode abandonnée)"},
    "elements_hors_decompte": hors_decompte,
    "tableau_ordres_de_grandeur": TABLEAU,
    "echelle_des_ecarts_decades": [{"comparaison": e[0], "ecart_decades": e[1], "source": e[2]} for e in ECARTS],
    "monte_carlo": mc,
    "desaccords_avec_le_dossier_de_base": DESACCORDS,
    "verdict_S08": s8["verdict"],
}
cc.ecrire_json(BASE / "resultats_globaux.json", globaux)
cc.ecrire_json(RES / "S09_resultats.json", {"simulation": "S09_synthese", "avertissement": cc.MENTION, "monte_carlo": mc,
                                            "echelle_des_ecarts_decades": globaux["echelle_des_ecarts_decades"], "validation": val.bilan()})
with open(RES / "S09_tableau_ordres_de_grandeur.csv", "w", encoding="utf-8") as f:
    f.write("id;grandeur;valeur;unite;formule;hypotheses;source;etiquette;statut_physique;confiance\n")
    for L_ in TABLEAU:
        v = L_["valeur"]
        vs = " à ".join(f"{x:.4g}" for x in v) if isinstance(v, (list, tuple)) else f"{v:.6g}"
        f.write(";".join([L_["id"], L_["grandeur"], vs, L_["unite"], L_["formule"], L_["hypotheses"], L_["source"], L_["etiquette"], L_["statut_physique"], L_["confiance"]]) + "\n")
print(f"  résultats : {RES / 'S09_tableau_ordres_de_grandeur.csv'}")
val.imprimer_bilan()
print("S09 terminé.")
